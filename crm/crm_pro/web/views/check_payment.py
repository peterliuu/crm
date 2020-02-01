# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/17 21:56
from django.urls import re_path

from stark.service.stark_module import BaseHandler, get_choices_field
from .base import PermissionHandler


class CheckPaymentHandler(PermissionHandler):
	"""查看所有缴费信息及批量操作数据"""
	display_list = [
		BaseHandler.display_mul_op,
		"customer", get_choices_field("缴费类型", "pay_type"), "paid_fee", "class_list", "apply_date",
		get_choices_field("状态", "confirm_status"), "consultant"
	]
	has_add_btn = False
	
	@property
	def get_urls(self):
		"""
		自定制记录相关的url
		"""
		patterns = [
			re_path(r"^list/$", self.wrapper(self.show_view), name=self.get_url_list_name),
		]
		patterns.extend(self.extra_url())
		return patterns, None, None
	
	def get_display_list(self, request, *args, **kwargs):
		"""
		缴费记录列数据不需要操作的删除与编辑
		:return:
		"""
		info = []
		if self.display_list:
			info.extend(self.display_list)
		return info
	
	def multi_confirm(self, request, *args, **kwargs):
		"""
		批量确认学生缴费情形
		更新缴费记录状态--已确认2
		学生表状态--在读2
		客户表状态--报名状态1
		"""
		pk_list = request.POST.getlist("pk")
		for pk in pk_list:
			payment_obj = self.model_class.objects.filter(id=pk, confirm_status=1).first()
			if payment_obj:
				payment_obj.confirm_status = 2
				payment_obj.save()
				payment_obj.customer.status = 1
				payment_obj.customer.save()
				payment_obj.customer.student.student_status = 2
				payment_obj.customer.student.save()
	
	multi_confirm.text = "批量确认"  # 为函数添加中文信息
	
	def multi_cancel(self, request, *args, **kwargs):
		"""
		批量驳回学生缴费情形
		更新缴费记录状态--已驳回3
		"""
		pk_list = request.POST.getlist("pk")
		self.model_class.objects.filter(id__in=pk_list, confirm_status=1).update(confirm_status=3)
	
	multi_cancel.text = "批量驳回"  # 为函数添加中文信息
	multi_list = [multi_confirm, multi_cancel]
	order_list = ["confirm_status"]  # 添加排序规则
