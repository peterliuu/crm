# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/10 21:26
from django.shortcuts import HttpResponse
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.service.stark_module import BaseModelFrom
from web import models
from .base import PermissionHandler


class RecordModelForm(BaseModelFrom):
	class Meta:
		model = models.ConsultRecord
		fields = ["note"]


class RecordHandler(PermissionHandler):
	display_list = ["customer", "note", "consultant", "date"]
	list_template = "consult_record.html"
	customized_model_class = RecordModelForm
	
	@property
	def get_urls(self):
		"""
		自定制记录相关的url
		"""
		patterns = [
			re_path(r"^list/(?P<customer_id>\d+)/$", self.wrapper(self.show_view), name=self.get_url_list_name),
			re_path(r"^add/(?P<customer_id>\d+)/$", self.wrapper(self.add_view), name=self.get_url_add_name),
			re_path(r"^edit/(?P<customer_id>\d+)/(?P<pk>\d+)/$", self.wrapper(self.edit_view),
					name=self.get_url_edit_name),
			re_path(r"^del/(?P<customer_id>\d+)/(?P<pk>\d+)/$", self.wrapper(self.del_view), name=self.get_url_del_name)
		]
		patterns.extend(self.extra_url())
		return patterns, None, None
	
	def get_queryset(self, request, *args, **kwargs):
		"""
		根据前端的数据，获取到的具体参数--customer_id
		特别提示：当前用户只能操作当前用户中的客户记录的增删改查，而不能查看别人的或操作公户中的数据信息
		customer__consultant_id=cur_user_id过滤条件
		"""
		# () {'customer_id': '1'}--args, kwargs数据
		cur_user_id = request.session.get("user_info").get("user_id")
		customer_id = kwargs.get("customer_id")
		# 过滤具体客户的id，展示跟踪记录
		return self.model_class.objects.filter(customer__id=customer_id, customer__consultant_id=cur_user_id)
	
	def customize_save(self, request, form, is_update, *args, **kwargs):
		"""
		在添加记录时，默认添加给当前用户及url中携带的客户id
		在保存数据时，首先检查当前客户是否属于当前客户的私户信息
		"""
		cur_user_id = request.session["user_info"]["user_id"]
		customer_id = kwargs.get("customer_id")
		exist_obj = models.Customer.objects.filter(id=customer_id, consultant__id=cur_user_id)
		if not exist_obj:
			return HttpResponse("请检查此客户是否属于自己再操作记录")
		if not is_update:
			form.instance.consultant_id = cur_user_id
			form.instance.customer_id = customer_id
		form.save()
	
	def display_del_edit(self, obj=None, is_header=None, *args, **kwargs):
		"""将编辑与删除放在统一栏中存放"""
		if is_header:
			return "操作"
		customer_id = kwargs.get("customer_id")
		del_edit = "<a href='%s'>编辑</a> <a href='%s'>删除</a>" % (
			self.get_reverse_edit_url(pk=obj.pk, customer_id=customer_id),
			self.get_reverse_del_url(pk=obj.pk, customer_id=customer_id))
		return mark_safe(del_edit)
	
	def get_edit_obj(self, request, pk, *args, **kwargs):
		"""为记录的编辑做筛选工作，避免查看非当前用户的个人记录信息"""
		cur_user_id = request.session["user_info"]["user_id"]
		customer_id = kwargs.get("customer_id")
		return self.model_class.objects.filter(id=pk, customer__id=customer_id, consultant__id=cur_user_id).first()
	
	def get_del_obj(self, request, pk, *args, **kwargs):
		"""删除正确的对象，避免删除非当前用户的个人记录信息"""
		cur_user_id = request.session["user_info"]["user_id"]
		customer_id = kwargs.get("customer_id")
		delete_obj = models.ConsultRecord.objects.filter(id=pk, customer__id=customer_id, consultant__id=cur_user_id)
		if not delete_obj:
			return HttpResponse("您要删除的数据信息不存在！")
		delete_obj.delete()
