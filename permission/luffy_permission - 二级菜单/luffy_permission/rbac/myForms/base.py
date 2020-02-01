# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/5 11:23

"""
将model页面中显示的样式统一放置
"""

from django import forms


class BootstrapModelForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# 统一给model字段添加样式
		for name, field in self.fields.items():
			field.widget.attrs['class'] = "form-control"
