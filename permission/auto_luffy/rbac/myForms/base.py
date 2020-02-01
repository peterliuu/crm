# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/5 11:23

"""
将model页面中显示的样式统一放置及密码校验
"""

from django import forms
from django.core.exceptions import ValidationError


class BootstrapModelForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 统一给model字段添加样式
		for name, field in self.fields.items():
			field.widget.attrs['class'] = "form-control"

	def clean_confirm_password(self):
		"""
		校验两次密码是否一致
		:return:
		"""
		pwd = self.cleaned_data.get("password")
		re_pwd = self.cleaned_data.get("confirm_password")
		if pwd and re_pwd:
			if re_pwd != pwd:
				raise ValidationError("两次密码不一致")
			return re_pwd



