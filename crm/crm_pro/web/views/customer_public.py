# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/8 22:41

from django.db import transaction
from django.shortcuts import render, HttpResponse
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.service.stark_module import BaseHandler, get_m2m_field, get_choices_field, BaseModelFrom
from web import models
from .base import PermissionHandler


class CustomerPubModelForm(BaseModelFrom):
	class Meta:
		model = models.Customer
		exclude = ["consultant"]  # 在添加学生信息时，不能进行分配给销售人员


class CustomerPubHandler(PermissionHandler):
	
	def display_record_list(self, obj=None, is_header=None):
		if is_header:
			return "跟进记录"
		return mark_safe("<a href='%s'>跟进记录</a>" % self.get_reverse_record_url(pk=obj.pk))
	
	display_list = [BaseHandler.display_mul_op, "name", "qq", get_m2m_field("咨询课程", "course"), get_choices_field("状态",
																												 "status"),
					display_record_list]
	
	def multi_apply(self, request, *args, **kwargs):
		"""批量将学生添加至私户功能"""
		'''
		基本实现思路：
		pk_list = request.POST.getlist('pk')
		# 默认课程顾问id为4
		consultant_id = 4
		# 将获取到的学生id的学生集合在查询到(未报名+课程顾问为空)，改变其consultant字段信息
		self.model_class.objects.filter(id__in=pk_list, status=2, consultant__isnull=True).update(
			consultant=consultant_id)
		'''
		# 严谨方案
		pk_list = request.POST.getlist('pk')
		# 从session中获取对应的user id，
		consultant_id = request.session.get("user_info").get("user_id")
		# 判断当前老师的私户数量是否超过上限
		cur_customer_num = self.model_class.objects.filter(status=2, consultant__id=consultant_id).count()
		if self.model_class.MAX_CUSTOMER_NUM - cur_customer_num - len(pk_list) < 0:
			return HttpResponse(
				"您当前的私户数量为%s，最多只能申请的数量为%s" % (cur_customer_num, self.model_class.MAX_CUSTOMER_NUM - cur_customer_num))
		flag = False
		# 使用数据库事务的一致性
		with transaction.atomic():
			# 对于查询到的公户信息加锁，防止其他用户查询此条件
			origin_queryset = self.model_class.objects.filter(status=2, id__in=pk_list,
															  consultant__isnull=True).select_for_update()
			if len(origin_queryset) == len(pk_list):
				# 说明当前用户可以将选中的信息添加到私户中
				self.model_class.objects.filter(id__in=pk_list, status=2, consultant__isnull=True).update(
					consultant=consultant_id)
				flag = True
		if not flag:
			# 如果添加的过程出现异常情形
			return HttpResponse("添加过程异常，请重新选择")
	
	multi_apply.text = "批量将学生添加至我的私户"
	multi_list = [multi_apply]
	
	def get_queryset(self, request, *args, **kwargs):
		"""在公户中不应显示已跟进的学生信息"""
		# 课程顾问为空数据
		return self.model_class.objects.filter(consultant__isnull=True)
	
	customized_model_class = CustomerPubModelForm
	
	def extra_url(self):
		"""添加记录跟踪路由"""
		patterns = [
			re_path(r"^record/(?P<pk>\d+)/$", self.wrapper(self.record_view), name=self.get_url_record_name)
		]
		return patterns
	
	@property
	def get_url_record_name(self):
		"""获取跟踪记录名称"""
		return self.get_url_name("record")
	
	def get_reverse_record_url(self, *args, **kwargs):
		"""通过此方法获取具体要跳转至显示record页面的url，保留原条件信息"""
		return self.get_reverse_base(self.get_url_record_name, *args, **kwargs)
	
	def record_view(self, request, pk):
		"""跟踪记录视图函数"""
		record_queryset = models.ConsultRecord.objects.filter(customer=pk)
		return render(request, "reocrd_list.html", {"record_queryset": record_queryset})
