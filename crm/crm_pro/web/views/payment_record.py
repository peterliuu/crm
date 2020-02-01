# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/16 22:24

from django import forms
from django.shortcuts import HttpResponse
from django.urls import re_path

from stark.service.stark_module import BaseModelFrom, get_choices_field
from web import models
from .base import PermissionHandler


class PaymentRecordModelForm(BaseModelFrom):
	class Meta:
		model = models.PaymentRecord
		fields = ["pay_type", 'paid_fee', 'class_list', 'note']


class PaymentStudentModelForm(BaseModelFrom):
	qq = forms.CharField(label="QQ号", max_length=32)
	mobile = forms.CharField(label="手机号", max_length=32)
	emergency_contract = forms.CharField(label="紧急联系人电话", max_length=32)
	
	class Meta:
		model = models.PaymentRecord
		fields = ["qq", "mobile", "emergency_contract", "pay_type", 'paid_fee', 'class_list', 'note']


class PaymentRecordHandler(PermissionHandler):
	display_list = [get_choices_field("缴费类型", "pay_type"), "paid_fee", "class_list", "consultant", get_choices_field(
		"缴费状态", "confirm_status")]
	customized_model_class = PaymentRecordModelForm
	
	def get_model_form(self, request, pk, is_add=True, *args, **kwargs):
		"""获取自定制表单模型，根据当前客户是否存储过信息来判别使用哪个"""
		customer_id = kwargs.get("customer_id")
		stu_obj = models.Student.objects.filter(customer__id=customer_id).first()
		if stu_obj:
			return PaymentRecordModelForm
		else:
			return PaymentStudentModelForm
	
	@property
	def get_urls(self):
		"""
		自定制记录相关的url,缴费记录不能有编辑和删除的按钮及url
		"""
		patterns = [
			re_path(r"^list/(?P<customer_id>\d+)/$", self.wrapper(self.show_view), name=self.get_url_list_name),
			re_path(r"^add/(?P<customer_id>\d+)/$", self.wrapper(self.add_view), name=self.get_url_add_name)
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
	
	def get_display_list(self, request, *args, **kwargs):
		"""
		缴费记录列数据不需要操作的删除与编辑
		:return:
		"""
		info = []
		if self.display_list:
			info.extend(self.display_list)
		return info
	
	def customize_save(self, request, form, is_update, *args, **kwargs):
		"""保存缴费记录"""
		cur_user_id = request.session["user_info"]["user_id"]
		customer_id = kwargs.get("customer_id")
		exist_obj = models.Customer.objects.filter(id=customer_id, consultant__id=cur_user_id).first()  # 用户是否属于此对象
		if not exist_obj:
			return HttpResponse("请检查此客户是否属于自己再操作记录")
		form.instance.customer_id = customer_id
		form.instance.consultant_id = cur_user_id
		# 添加当前客户的缴费记录信息
		form.save()
		# 添加学生信息,判断学生信息是否存在
		customer_id = kwargs.get("customer_id")
		class_list = form.cleaned_data.get("class_list")  # 班级对象
		stu_obj = models.Student.objects.filter(customer__id=customer_id).first()
		if not stu_obj:  # 添加学生表及多表信息
			qq = form.cleaned_data.get("qq")
			mobile = form.cleaned_data.get("mobile")
			emergency_contract = form.cleaned_data.get("emergency_contract")
			add_obj = models.Student.objects.create(customer_id=customer_id, qq=qq, mobile=mobile,
													emergency_contract=emergency_contract)
			# 添加多对多表信息
			add_obj.class_list.add(class_list)
		else:  # 添加多表信息
			stu_obj.class_list.add(class_list)
