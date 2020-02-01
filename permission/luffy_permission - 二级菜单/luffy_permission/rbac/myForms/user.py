# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/3 16:08
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError  # 值错误校验
from rbac.models import UserInfo


class UserForm(forms.Form):
	"""用户验证表单组件类"""
	name = forms.CharField(max_length=32,
							label="用户名",
							widget=widgets.TextInput(attrs={"class":"form-control", "placeholder": "请输入角色名"})
							)
	email = forms.CharField(max_length=32,
							label="邮箱",
							widget=widgets.TextInput(attrs={"class":"form-control", "placeholder": "请输入邮箱"})
							)
	pwd = forms.CharField(max_length=32,
							label="密码",
							widget=widgets.PasswordInput(attrs={"class":"form-control", "placeholder": "请输入密码"})
							)
	re_pwd = forms.CharField(max_length=32,
							label="确认密码",
							widget=widgets.PasswordInput(attrs={"class":"form-control", "placeholder": "请再次输入密码"})
							)

	def clean_re_pwd(self):
		"""
		局部钩子，用于2次校验title有无重名问题
		:return:返回验证情况
		"""
		pwd = self.cleaned_data.get("pwd")
		re_pwd = self.cleaned_data.get("re_pwd")

		if pwd != re_pwd:
			# 数据不一致,返回错误信息,使用raise主动触发错误信息
			raise ValidationError("两次密码不一致！请重新输入")
		else:
			return re_pwd


class UpdateUserForm(forms.Form):
	"""用户数据更新验证表单组件类"""
	name = forms.CharField(max_length=32,
						   label="用户名",
						   widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入角色名"})
						   )
	email = forms.CharField(max_length=32,
							label="邮箱",
							widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入邮箱"})
							)

class PasswordResetForm(forms.Form):
	"""用户密码重置组件类"""
	pwd = forms.CharField(max_length=32,
							label="密码",
							widget=widgets.PasswordInput(attrs={"class":"form-control", "placeholder": "请输入密码"})
							)
	re_pwd = forms.CharField(max_length=32,
							label="确认密码",
							widget=widgets.PasswordInput(attrs={"class":"form-control", "placeholder": "请再次输入密码"})
							)

	def clean_re_pwd(self):
		"""
		局部钩子，用于2次校验title有无重名问题
		:return:返回验证情况
		"""
		pwd = self.cleaned_data.get("pwd")
		re_pwd = self.cleaned_data.get("re_pwd")
		if pwd != re_pwd:
			# 数据不一致,返回错误信息,使用raise主动触发错误信息
			raise ValidationError("两次密码不一致！请重新输入")
		else:
			return re_pwd
# 添加具体
# 	confirm_password = forms.CharField(label="确认密码")
# 	class Meta:
# 		model = UserInfo()
# 		fields = ["name", "email", "password", "confirm_password"]

