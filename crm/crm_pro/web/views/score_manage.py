# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/18 19:36

from django.urls import re_path

from stark.service.stark_module import BaseModelFrom
from web import models
from .base import PermissionHandler


class ScoreModelForm(BaseModelFrom):
	class Meta:
		model = models.ScoreRecord
		fields = ["content", "score"]


class ScoreHandler(PermissionHandler):
	"""积分管理-编辑及删除不应有"""
	display_list = ["student", "content", 'score', 'user']
	customized_model_class = ScoreModelForm
	
	@property
	def get_urls(self):
		"""
		自定制记录相关的url,缴费记录不能有编辑和删除的按钮及url
		"""
		patterns = [
			re_path(r"^list/(?P<student_id>\d+)/$", self.wrapper(self.show_view), name=self.get_url_list_name),
			re_path(r"^add/(?P<student_id>\d+)/$", self.wrapper(self.add_view), name=self.get_url_add_name)
		]
		patterns.extend(self.extra_url())
		return patterns, None, None
	
	def get_display_list(self, request, *args, **kwargs):
		"""
		积分管理记录列数据不需要操作的删除与编辑
		:return:
		"""
		info = []
		if self.display_list:
			info.extend(self.display_list)
		return info
	
	def customize_save(self, request, form, is_update, *args, **kwargs):
		"""在数据保存时需要对对应的表单对象进行save"""
		cur_user_id = request.session.get("user_info").get("user_id")
		student_id = kwargs.get("student_id")
		# 获取到积分表的对象字段
		form.instance.student_id = student_id
		form.instance.user_id = cur_user_id
		form.save()
		# 需要对学生表中对应的学生分数更新
		score = form.instance.score
		if score > 0:
			form.instance.student.score += score
		else:
			form.instance.student.score -= abs(score)
		form.instance.student.save()  # 学生对象进行保存操作
	
	def get_queryset(self, request, *args, **kwargs):
		"""过滤当前student_id的数据信息"""
		student_id = kwargs.get("student_id")
		return self.model_class.objects.filter(student__id=student_id)
