# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/18 21:11


from django.forms.models import modelformset_factory
from django.shortcuts import HttpResponse, reverse, render
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.service.stark_module import BaseHandler, BaseModelFrom
from web import models
from .base import PermissionHandler


class CourseRecordModelForm(BaseModelFrom):
	class Meta:
		model = models.CourseRecord
		fields = ["day_num", "teacher"]


class StudyModelForm(BaseModelFrom):
	"""需要展示的出勤字段信息，以多选框的形式展现，只需要展示记录"""
	
	class Meta:
		model = models.StudyRecord
		fields = ['record']


class CourseRecordHandler(PermissionHandler):
	"""上课记录管理"""
	
	def display_attendance_list(self, obj=None, is_header=None, *args, **kwargs):
		"""出勤情况"""
		if is_header:
			return "出勤情况"
		url = reverse("%s:%s" % (self.stark_obj.namespace, self.get_url_name("attendance")),
					  kwargs={"course_record_id": obj.pk})
		return mark_safe("<a href='%s' target='_blank'>出勤情况</a>" % url)
	
	display_list = [BaseHandler.display_mul_op, "class_object", "day_num", 'teacher', 'date', display_attendance_list]
	customized_model_class = CourseRecordModelForm
	
	@property
	def get_urls(self):
		"""
		上课记录相关的url display_attendance_list
		"""
		patterns = [
			re_path(r"^list/(?P<class_id>\d+)/$", self.wrapper(self.show_view), name=self.get_url_list_name),
			re_path(r"^add/(?P<class_id>\d+)/$", self.wrapper(self.add_view), name=self.get_url_add_name),
			re_path(r"^edit/(?P<class_id>\d+)/(?P<pk>\d+)/$", self.wrapper(self.edit_view),
					name=self.get_url_edit_name),
			re_path(r"^del/(?P<class_id>\d+)/(?P<pk>\d+)/$", self.wrapper(self.del_view), name=self.get_url_del_name),
			# 添加出勤率的url
			re_path(r"^attendance/(?P<course_record_id>\d+)/$", self.wrapper(self.attendance_view),
					name=self.get_url_name("attendance"))
		
		]
		patterns.extend(self.extra_url())
		return patterns, None, None
	
	def attendance_view(self, request, course_record_id):
		"""
		展示及修改出勤信息的批量操作
		使用批量操作的多表--formset_factory
		"""
		# 显示出当前记录id中的所有考勤的学生信息--get请求
		all_records_queryset = models.StudyRecord.objects.filter(course_record_id=course_record_id)
		# extra-不额外添加行表单信息  创建一个formset_class
		formset_class = modelformset_factory(models.StudyRecord, form=StudyModelForm, extra=0)
		if request.method == 'GET':
			# 实例化具体formset对象，对需要展现的信息实例化
			formset = formset_class(queryset=all_records_queryset)
			return render(request, "attendance.html", {"formset": formset})
		formset = formset_class(queryset=all_records_queryset, data=request.POST)
		if formset.is_valid():
			formset.save()
		print(formset)
		return render(request, "attendance.html", {"formset": formset})
	
	def customize_save(self, request, form, is_update, *args, **kwargs):
		class_id = kwargs.get("class_id")
		form.instance.class_object_id = class_id
		form.save()
	
	def display_del_edit(self, obj=None, is_header=None, *args, **kwargs):
		"""反向解析时需要用到class_id，所以需要重写display_del_edit方法"""
		if is_header:
			return "操作"
		class_id = kwargs.get("class_id")
		del_edit = "<a href='%s'>编辑</a> <a href='%s'>删除</a>" % (
			self.get_reverse_edit_url(pk=obj.pk, class_id=class_id),
			self.get_reverse_del_url(pk=obj.pk, class_id=class_id))
		return mark_safe(del_edit)
	
	def get_queryset(self, request, *args, **kwargs):
		"""过滤当前student_id的数据信息"""
		class_id = kwargs.get("class_id")
		return self.model_class.objects.filter(class_object__id=class_id)
	
	def multi_add_record(self, request, *args, **kwargs):
		"""批量添加学生考勤记录"""
		# 1、获取所有的上课记录id
		class_record_pk_list = request.POST.getlist('pk')
		# 获取班级id
		class_id = kwargs.get("class_id")
		# 获取班级对象及判断是否存在
		class_obj = models.ClassList.objects.filter(id=class_id).first()
		if not class_obj:
			return HttpResponse("班级不存在！")
		# 获取此班级下的所有学生
		students_queryset = class_obj.student_set.all()
		# 判断当前记录对应的记录id及班级id是否存在
		for class_record_pk in class_record_pk_list:
			record_obj = models.CourseRecord.objects.filter(id=class_record_pk, class_object__id=class_id).first()
			if not record_obj:
				continue
			# 判断当前天数的考勤记录是否存在,存在则不添加
			status = models.StudyRecord.objects.filter(course_record__id=class_record_pk).exists()
			if status:
				continue
			# 单条添加记录
			# for stu in students_queryset:
			# 	models.StudyRecord.objects.create(course_record_id=class_record_pk, student_id=stu.id)
			# 一次性向数据库写入多条记录
			study_obj_list = [models.StudyRecord(course_record_id=class_record_pk, student_id=stu.id) for stu in
							  students_queryset]
			models.StudyRecord.objects.bulk_create(study_obj_list)
	
	multi_add_record.text = "批量添加学生考勤记录"
	multi_list = [multi_add_record]
