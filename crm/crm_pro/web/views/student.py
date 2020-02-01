# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/17 23:21

from django.shortcuts import reverse
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.service.stark_module import BaseModelFrom, get_choices_field, get_m2m_field, ComposeOption
from web import models
from .base import PermissionHandler


class StudentModelForm(BaseModelFrom):
	class Meta:
		model = models.Student
		fields = ["qq", 'mobile', 'emergency_contract', 'memo']


class StudentHandler(PermissionHandler):
	
	def display_score(self, obj=None, is_header=None, *args, **kwargs):
		"""查看积分"""
		if is_header:
			return "积分管理"
		url = reverse("%s:web-scorerecord-list" % self.stark_obj.namespace, kwargs={"student_id": obj.pk})
		return mark_safe("<a href='%s' target='_blank'>%s</a>" % (url, obj.score))
	
	display_list = ["customer", "qq", 'mobile', 'emergency_contract', get_m2m_field("班级信息", "class_list"),
					get_choices_field("学员状态",
									  "student_status"), display_score]
	has_add_btn = False
	customized_model_class = StudentModelForm
	filter_list = ["customer__name__contains", "mobile__contains"]
	search_group = [
		ComposeOption("class_list")
	]
	
	@property
	def get_urls(self):
		"""
		自定制记录相关的url
		"""
		patterns = [
			re_path(r"^list/$", self.wrapper(self.show_view), name=self.get_url_list_name),
			re_path(r"^edit/(?P<pk>\d+)/$", self.wrapper(self.edit_view), name=self.get_url_edit_name)
		]
		patterns.extend(self.extra_url())
		return patterns, None, None
	
	def get_display_list(self, request, *args, **kwargs):
		"""
		只需要编辑页面
		"""
		info = []
		if self.display_list:
			info.extend(self.display_list)
			info.append(type(self).display_edit)
		return info
