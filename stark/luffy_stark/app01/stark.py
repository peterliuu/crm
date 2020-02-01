# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/4 20:36


from app01 import models
from stark.service.stark_module import site, BaseHandler, get_choices_field, BaseModelFrom, ComposeOption


class DepartHandler(BaseHandler):
	display_list = [BaseHandler.display_mul_op, "id", "title", BaseHandler.display_edit, BaseHandler.display_del]
	multi_list = [BaseHandler.multi_del]


# @property
# def get_urls(self):
# 	# 在此处减少当前model的url数量
# 	patterns = [
# 		re_path(r"list/$", self.show_view),
# 		re_path(r"add/$", self.add_view),
# 	]
# 	return patterns, None, None

class UserInfoModelForm(BaseModelFrom):
	# xx = forms.CharField()  # 可以增加字段信息
	
	class Meta:
		model = models.UserInfo
		fields = "__all__"
	# exclude = ['depart']  # 在页面中不填写depart字段


class MyOption(ComposeOption):
	def get_db_condition(self, request, *args, **kwargs):
		return {}


class UserInfoHandler(BaseHandler):
	"""
	在类的内部自定制需要显示的列名称--display_list
	"""
	
	customized_model_class = UserInfoModelForm
	order_list = ["-id"]  # 反向id排序
	filter_list = ["name__contains", "email__contains"]  # 自定制过滤条件
	multi_list = [BaseHandler.multi_del, BaseHandler.multi_edit]
	# 根据具体的表结构获取不同的过滤组合信息字段值
	"""
	方式1
	search_group = [
		{"field": "gender", "db_condition": {}},
		{"field": "classes", "db_condition": {}},
		{"field": "depart", "db_condition": {'id__gt': 1}},
		]
	"""
	# 方式2--将数据封住为对象，方便获取数据
	search_group = [
		ComposeOption("gender", is_multi=True),  # 可以自定制标签多选
		ComposeOption("classes"),
		ComposeOption("depart"),
		# ComposeOption("depart", {'id__gt': 1}),  # 可以自定制显示的过滤条件
		# 过滤显示数据-可以自定制
		# MyOption("depart", {'id__gt': 1}),
		# 自定制文本内容
		# ComposeOption("gender", text_func=lambda x: x[1] + '666'),
	
	]
	# def get_display_list(self):
	# 	"""可以根据不同用户显示不同列"""
	# 	return ["name", "age"]
	
	# 分别定义方法显示自定义的choices字段的中文信息
	# def get_gender(self, is_header=None, obj=None):
	# 	if is_header:
	# 		return "性别"
	# 	return obj.get_gender_display()
	#
	# def get_classes(self, is_header=None, obj=None):
	# 	if is_header:
	# 		return "班级"
	# 	return obj.get_classes_display()
	
	display_list = [BaseHandler.display_mul_op, "name", "age", "email", get_choices_field("性别", "gender"),
					get_choices_field(
						"班级", "classes"), 'depart',
					BaseHandler.display_edit, BaseHandler.display_del]

# def customize_save(self, form, is_update=False):
# 	form.instance.depart_id = 1  # 可以在后台默认新添加对


# 	象的部门id数据
# 	form.save()


site.register(models.UserInfo, UserInfoHandler)
site.register(models.Depart, DepartHandler)


# site.register(models.Depart, DepartHandler, prev="xx")  # 增加前缀

# ------------- 添加deploy页面， 使用stark组件 快速生成数据信息表---------

class DeployHandler(BaseHandler):
	display_list = ["title", get_choices_field("状态", 'status'), BaseHandler.display_edit, BaseHandler.display_del]


site.register(models.Deploy, DeployHandler)
