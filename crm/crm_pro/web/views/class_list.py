# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/8 15:56

from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from stark.forms.datetimepicker import DateTimePicker
from stark.service.stark_module import get_time_field, get_m2m_field, BaseModelFrom, ComposeOption
from web.models import ClassList
from .base import PermissionHandler


class ClassListModelForm(BaseModelFrom):
	class Meta:
		model = ClassList
		fields = "__all__"
		widgets = {
			"start_date": DateTimePicker,
			"graduate_date": DateTimePicker,
		}


class ClassListHandler(PermissionHandler):
	def display_course(self, obj=None, is_header=None):
		"""
		自定制的课程和学期组合列
		"""
		if is_header:
			return "班级"
		return "%s-%s期" % (obj.course.name, obj.semester)
	
	def display_course_record(self, obj=None, is_header=None):
		"""
		自定制的上课记录
		"""
		if is_header:
			return "上课记录"
		url = reverse("%s:web-courserecord-list" % self.stark_obj.namespace, kwargs={"class_id": obj.pk})
		return mark_safe("<a href='%s' target='_blank'>上课记录</a>" % url)
	
	display_list = ["school", display_course, "price", get_time_field("开课时间", "start_date"), "class_teacher",
					get_m2m_field("	任课老师", "tech_teacher"), display_course_record]
	customized_model_class = ClassListModelForm
	search_group = [
		ComposeOption("school"),
		ComposeOption("course"),
	]
