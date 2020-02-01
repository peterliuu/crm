# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/3 16:08
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError  # 值错误校验
from rbac.models import Role
"""
数据解耦，将forms组件用于校验表单数据
"""

class RoleForm(forms.Form):
	"""用户验证表单组件类"""
	title = forms.CharField(max_length=32,
							label="角色名称",
							widget=widgets.TextInput(attrs={"class":"form-control", "placeholder": "请输入角色名"})
							)

	def clean_title(self):
		"""
		局部钩子，用于2次校验title有无重名问题
		:return:返回验证情况
		"""
		title = self.cleaned_data.get("title")
		role_obj = Role.objects.filter(title=title).first()
		if role_obj:
			# 已存在数据,返回错误信息,使用raise主动触发错误信息
			raise ValidationError("该字段已存在！请重新输入")
		else:
			return title






