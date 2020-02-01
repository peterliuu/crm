# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/4 15:10
"""
表单验证可以继承forms.Form或forms.ModelForm
"""
from django import forms
from django.forms import widgets, formset_factory
# 将页面标签转换为本来的样式，不转义--默认安全
from django.utils.safestring import mark_safe
from rbac import models
from .base import BootstrapModelForm

icon_lists = [
	"fa-bus", "fa-bullhorn", "fa-cloud-download", "fa-cube", "fa-envelope-o", "fa-futbol-o"
]


class MenuForm(forms.ModelForm):
	"""
	将常用的图标放置在radio单选框中，令用户选择使用
	choices中的参数以列表形式传递[value, 显示数据]
	forms.Form
	"""
	# title = forms.CharField(max_length=32, label="菜单名称",
	# 						widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入图标名称"}))
	# # 生成的标签为ul，需要清除浮动
	# icon = forms.CharField(max_length=32, label="图标名称",
	# 					   widget=widgets.RadioSelect(
	# 						choices=[
	# 							   [item, mark_safe('<i class="fa %s" aria-hidden="true"></i>' % item)] for item in
	# 							   icon_lists],
	# 						   attrs={"class": "clearfix"}
	# 					   ))
	"""
	通过forms.ModelForm实现页面展示及验证功能
	"""

	class Meta:
		model = models.Menu
		fields = ['title', 'icon']  # 显示的字段
		widgets = {
			"title": forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入图标名称"}),
			"icon": forms.RadioSelect(
				choices=[
					[item, mark_safe('<i class="fa %s" aria-hidden="true"></i>' % item)] for item in
					icon_lists],
				attrs={"class": "clearfix"}
			)
		}


class SecondMenuForm(BootstrapModelForm):
	"""
	二级菜单自定义表单
	"""

	class Meta:
		model = models.Permission
		exclude = ["pid"]  # 不显示此字段


class PermissionMenuForm(BootstrapModelForm):
	"""
	权限菜单自定义表单
	"""

	class Meta:
		model = models.Permission
		fields = ["title", "url", "name"]


class MultiPermissionAdd(forms.Form):
	"""
	批量增加操作数据
	"""
	title = forms.CharField(max_length=32, label="权限名称",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	url = forms.CharField(max_length=64, label="含正则的URL",
						    widget=widgets.TextInput(attrs={"class": "form-control"}))
	name = forms.CharField(max_length=32, label="url别名",
						    widget=widgets.TextInput(attrs={"class": "form-control"}))
	menu_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="所属菜单",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)
	pid_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="关联的权限",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)

	def __init__(self, *args, **kwargs):
		"""
		数据继承并为menu_id和pid_id增加内容
		:param args:
		:param kwargs:
		"""
		super().__init__(*args, **kwargs)
		# self.fields["menu_id"].choices-->[(None, "-----"), (xx, xx)……]
		self.fields["menu_id"].choices += models.Menu.objects.values_list("id", "title")
		self.fields["pid_id"].choices += models.Permission.objects.filter(menu_id__isnull=False,	pid_id__isnull=True).values_list("id", "title")


class MultiPermissionUpdate(forms.Form):
	"""
	批量更新操作数据
	"""
	id = forms.IntegerField(
		widget=forms.HiddenInput()  # 隐藏字段
	)
	title = forms.CharField(max_length=32, label="权限名称",
							widget=widgets.TextInput(attrs={"class": "form-control"}))
	url = forms.CharField(max_length=64, label="含正则的URL",
						    widget=widgets.TextInput(attrs={"class": "form-control"}))
	name = forms.CharField(max_length=32, label="url别名",
						    widget=widgets.TextInput(attrs={"class": "form-control"}))
	menu_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="所属菜单",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)
	pid_id = forms.ChoiceField(
		choices=[(None, "-----")],
		label="关联的权限",
		widget=forms.Select(attrs={"class": "form-control"}),
		required=False
	)

	def __init__(self, *args, **kwargs):
		"""
		数据继承并为menu_id和pid_id增加内容
		:param args:
		:param kwargs:
		"""
		super().__init__(*args, **kwargs)
		# self.fields["menu_id"].choices-->[(None, "-----"), (xx, xx)……]
		self.fields["menu_id"].choices += models.Menu.objects.values_list("id", "title")
		self.fields["pid_id"].choices += models.Permission.objects.filter(menu_id__isnull=False,	pid_id__isnull=True).values_list("id", "title")
