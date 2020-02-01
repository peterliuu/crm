# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/8 22:47

from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from stark.service.stark_module import BaseHandler, get_m2m_field, get_choices_field, BaseModelFrom
from web import models
from .base import PermissionHandler


class CustomerPriModelForm(BaseModelFrom):
	class Meta:
		model = models.Customer
		exclude = ["consultant"]  # 私户添加信息时直接添加给自己


class CustomerPrivateHandler(PermissionHandler):
	def display_record_list(self, obj=None, is_header=None):
		"""当前的反向解析的url中不需要传递原条件，因为记录信息与其他无关"""
		if is_header:
			return "跟进记录"
		url = reverse("%s:web-consultrecord-list" % self.stark_obj.namespace, kwargs={"customer_id": obj.pk})
		# url = self.get_reverse_base("web-consultrecord-list", customer_id=obj.pk)
		return mark_safe("<a href='%s' target='_blank'>跟进记录</a>" % url)
	
	def display_payment_list(self, obj=None, is_header=None):
		"""缴费记录信息显示"""
		if is_header:
			return "缴费信息"
		url = reverse("%s:web-paymentrecord-list" % self.stark_obj.namespace, kwargs={"customer_id": obj.pk})
		return mark_safe("<a href='%s' target='_blank'>缴费记录</a>" % url)
	
	display_list = [BaseHandler.display_mul_op, "name", "qq", get_m2m_field("咨询课程", "course"), get_choices_field(
		"状态", "status"), display_record_list, display_payment_list]
	customized_model_class = CustomerPriModelForm
	
	def get_queryset(self, request, *args, **kwargs):
		"""在显示时只显示当前用户的id值相同的数据库数据"""
		cur_user_id = request.session["user_info"]["user_id"]
		return self.model_class.objects.filter(consultant_id=cur_user_id)
	
	def customize_save(self, request, form, is_update, *args, **kwargs):
		"""自定义form数据保存--在添加数据时需将当前的用户信息默认追加进form对象中"""
		cur_user_id = request.session["user_info"]["user_id"]
		form.instance.consultant_id = cur_user_id
		form.save()
	
	def multi_delete(self, request, *args, **kwargs):
		"""将客户批量从当前销售处移除"""
		pk_list = request.POST.getlist('pk')
		cur_user_id = request.session["user_info"]["user_id"]
		self.model_class.objects.filter(id__in=pk_list, consultant_id=cur_user_id).update(consultant_id=None)
	
	multi_delete.text = "批量将学生添加至我的私户"
	multi_list = [multi_delete]
