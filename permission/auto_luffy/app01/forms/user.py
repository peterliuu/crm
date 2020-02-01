# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/27 16:00

from django import forms
from django.core.exceptions import ValidationError
from app01.models import UserInfo
from rbac.myForms.base import BootstrapModelForm


class UserForm(BootstrapModelForm):
	"""
	密码校验放置在BootstrapModelForm中
	"""
	confirm_password = forms.CharField(label="确认密码")
	
	class Meta:
		model = UserInfo
		fields = ["name", "password", "confirm_password", "email", "phone", "level", "depart", "roles"]
	
	
class UpdateUserForm(BootstrapModelForm):
	class Meta:
		model = UserInfo
		exclude = ['password']


class PasswordResetForm(BootstrapModelForm):
	confirm_password = forms.CharField(label="确认密码")
	
	class Meta:
		model = UserInfo
		fields = ["password", "confirm_password"]
