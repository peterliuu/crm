# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/8 20:34
from django import forms

"""
用于时间插件样式的重写，以后使用时间插件相关表单，继承自它即可
"""


class DateTimePicker(forms.TextInput):
	# 本身继承自forms.TextInput，对内部的template_name属性进行重写，使用插件的html样式
	template_name = 'stark/forms/widgets/datetimepicker.html'
