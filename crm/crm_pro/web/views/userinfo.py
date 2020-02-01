# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/8 14:01
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse, render, redirect
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.service.stark_module import get_choices_field, BaseModelFrom, BaseForm, ComposeOption
from web import models
from web.utils.md5 import gen_md5
from .base import PermissionHandler


class MyAddUserInfo(BaseModelFrom):
	"""
	自定义编排添加页面的用户数据顺序
	"""
	confirm_pwd = forms.CharField(label="确认密码")
	
	class Meta:
		model = models.UserInfo
		fields = ["name", "password", "confirm_pwd", "gender", "phone", "email", "depart", "roles"]
	
	def clean_confirm_pwd(self):
		"""添加一个钩子函数，用户校验两次密码的数据是否一致"""
		pwd = self.cleaned_data.get("password")
		confirm_pwd = self.cleaned_data.get("confirm_pwd")
		if pwd and confirm_pwd:
			if confirm_pwd == pwd:
				return confirm_pwd
			raise ValidationError("两次密码不一致")
	
	def clean(self):
		"""将校验过的字段的密码加密"""
		pwd = self.cleaned_data.get("password")
		self.cleaned_data["password"] = gen_md5(pwd)
		return self.cleaned_data


class MyEditUserInfo(BaseModelFrom):
	"""
	自定义编排编辑页面的用户数据顺序
	"""
	
	class Meta:
		model = models.UserInfo
		fields = ["name", "gender", "phone", "email", "depart", "roles"]


class ResetPwdModelForm(BaseForm):
	"""显示重置密码表单数据"""
	password = forms.CharField(label="密码", widget=forms.PasswordInput)  # 密文显示
	confirm_pwd = forms.CharField(label="重置密码", widget=forms.PasswordInput)
	
	def clean_confirm_pwd(self):
		"""添加一个钩子函数，用户校验两次密码的数据是否一致"""
		pwd = self.cleaned_data.get("password")
		confirm_pwd = self.cleaned_data.get("confirm_pwd")
		if pwd and confirm_pwd:
			if confirm_pwd == pwd:
				return confirm_pwd
			raise ValidationError("两次密码不一致")
	
	def clean(self):
		"""将校验过的字段的密码加密"""
		pwd = self.cleaned_data.get("password")
		self.cleaned_data["password"] = gen_md5(pwd)
		return self.cleaned_data


class UserInfoHandler(PermissionHandler):
	"""
	用户模型数据
	应该根据add或edit来对页面展示不同的字段，在get_model_form中重写获取到的模型类
	"""
	filter_list = ["name__contains", "email__contains"]
	search_group = [
		ComposeOption("gender"),
		ComposeOption("depart")
	]
	
	def display_reset_pwd(self, obj=None, is_header=None):
		if is_header:
			return "重置密码"
		return mark_safe("<a href='%s'>重置密码</a>" % self.get_reverse_reset_pwd_url(pk=obj.id))
	
	display_list = ["name", get_choices_field("性别", "gender"), "phone", "email", "depart", display_reset_pwd]
	
	def get_model_form(self, request, pk, is_add=True, *args, **kwargs):
		"""添加或编辑时显示不同的界面，通过不同的模型类"""
		if is_add:
			return MyAddUserInfo
		return MyEditUserInfo
	
	@property
	def get_url_reset_pwd_name(self):
		"""获取reset-pwd的name值"""
		return self.get_url_name("reset-pwd")
	
	def reset_pwd_view(self, request, pk):
		"""用户密码重置页面逻辑"""
		user_obj = self.model_class.objects.filter(id=pk).first()
		if not user_obj:
			return HttpResponse("此用户不存在，无法重置密码")
		if request.method == "GET":
			form = ResetPwdModelForm()
			return render(request, "stark/change.html", {"form": form})
		form = ResetPwdModelForm(data=request.POST)
		if form.is_valid():
			pwd = form.cleaned_data.get('password')  # 获取密码MD5，存储进数据库
			user_obj.password = pwd
			user_obj.save()
			return redirect(self.get_reverse_list_url())
		return render(request, "stark/change.html", {"form": form})
	
	def get_reverse_reset_pwd_url(self, *args, **kwargs):
		"""获取点击重置密码标签时的跳转url"""
		return self.get_reverse_base(self.get_url_reset_pwd_name, *args, **kwargs)
	
	def extra_url(self):
		"""
		用于4个url基础之上url的增加--重置密码
		:return:
		"""
		return [re_path(r"^reset/pwd/(?P<pk>\d+)/$", self.wrapper(self.reset_pwd_view),
						name=self.get_url_reset_pwd_name)]
