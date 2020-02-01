# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/4 20:32
from functools import wraps
from types import FunctionType

from django import forms
from django.db.models import ForeignKey, ManyToManyField
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.urls import re_path
from django.utils.safestring import mark_safe

from stark.utils.pagination import Pagination  # 分页组件


class BaseModelFrom(forms.ModelForm):
	"""统一添加ModelForm表单样式信息"""
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs["class"] = "form-control"


class BaseForm(forms.Form):
	"""统一添加Form表单样式信息"""
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs["class"] = "form-control"


class SearchGroupRow:
	"""为了使组合搜索的数据统一在后台处理，将对象变为可迭代对象，在前台循环，获取信息"""
	
	def __init__(self, title, group_list, compose_obj=None, query_dict=None):
		"""
		:param title: 行标题
		:param group_list: 元组或queryset集合
		:param compose_obj: ComposeOption对象
		:param query_dict: 获取的request.GET
		"""
		self.title = title
		self.group_list = group_list
		self.compose_obj = compose_obj
		self.query_dict = query_dict
	
	def __iter__(self):
		"""内置方法可以将对象变为可迭代对象"""
		yield "<div class='whole'>"
		yield self.title  # 显示标题
		yield "</div>"
		yield "<div class='others'>"
		# 1 获取queryDict--request.GET
		origin_dict = self.query_dict
		origin_dict._mutable = True
		total_dict = origin_dict.copy()
		# 在初始页面中应该全部选择  ['1', '2']
		origin_list = self.query_dict.getlist(self.compose_obj.field)
		if not origin_list:
			yield "<a href='?%s' class='active'>全部</a>" % total_dict.urlencode()  # 显示标题
		else:
			total_dict.pop(self.compose_obj.field)  # 删除当前的字段在total_dict中
			yield "<a href='?%s'>全部</a>" % total_dict.urlencode()
		# 根据搜索对象的类型分别处理数据
		for item in self.group_list:  # item--对象或者元组
			text = self.compose_obj.get_text(item)  # 获取字段的名称
			# 页面显示数据gender=1&depart=2
			# 需要获取字段名称及id值--为了在前端根据不同的标签获取到对应的参数，需要获取request.GET，然后向其中添加数据，在使用urlencode()方法获取到url
			data_dict = origin_dict.copy()  # 拷贝数据，不能改变request.GET本身数据
			# 2 获取字段的id值
			value = str(self.compose_obj.get_value(item))
			if not self.compose_obj.is_multi:
				# 3 在querydict中添加或修改数据
				data_dict[self.compose_obj.field] = value
				if value in origin_list:
					data_dict.pop(self.compose_obj.field)
					yield "<a href='?%s' class='active'>%s</a>" % (data_dict.urlencode(), text)
				else:
					yield "<a href='?%s'>%s</a>" % (data_dict.urlencode(), text)
			else:
				# 多选逻辑处理
				multi_list = data_dict.getlist(self.compose_obj.field)  # 获取当前字段的前端请求值集合
				if value in multi_list:
					# 删除当前在列表中的值
					multi_list.remove(value)
					# 为字段设置列表数据
					data_dict.setlist(self.compose_obj.field, multi_list)
					yield "<a href='?%s' class='active'>%s</a>" % (data_dict.urlencode(), text)
				else:
					multi_list.append(value)
					data_dict.setlist(self.compose_obj.field, multi_list)
					yield "<a href='?%s'>%s</a>" % (data_dict.urlencode(), text)
		yield "</div>"


class ComposeOption:
	"""自定制获取组合搜索的相关条件信息"""
	
	def __init__(self, field, db_condition=None, text_func=None, is_multi=False):
		self.field = field
		if not db_condition:
			db_condition = {}
		self.db_condition = db_condition  # 筛选过滤条件
		self.text_func = text_func  # 对于显示的数据信息可以自定制样式
		self.is_tuple = False
		self.is_multi = is_multi
	
	def get_db_condition(self, request, *args, **kwargs):
		"""可以自定制筛选信息"""
		return self.db_condition
	
	def get_queryset_or_tuple(self, model_class, request, *args, **kwargs):
		"""
		根据不同的字段及需求完成逻辑处理数据字段或关联对象返回
		使用SearchGroupRow实例化：数据字段或关联对象
		:param model_class: 当前对象的模型类，通过模型类获取字段对象或关联查询集对象
		:param request:
		:return:
		"""
		field_obj = model_class._meta.get_field(self.field)  # 获取字段对象
		title = field_obj.verbose_name
		db_condition = self.get_db_condition(request, *args, **kwargs)  # 过滤条件
		if isinstance(field_obj, (ForeignKey, ManyToManyField)):
			# 判断字段是否为关联字段-并获取关联模型数据  <QuerySet [<Depart: 研发部>, <Depart: 技术部>, <Depart: 销售信息部>]>
			related_model = field_obj.related_model
			return SearchGroupRow(title, related_model.objects.filter(**db_condition), self, request.GET)
		else:
			self.is_tuple = True
			# 判断字段是否为choices字段--获取信息数据  ((1, '男'), (2, '女'))
			return SearchGroupRow(title, field_obj.choices, self, request.GET)
	
	def get_text(self, field):
		"""
		动态分析字段是元组或模型对象或自定制文本函数信息
		:param field: 元组或模型对象
		:return:
		"""
		if self.text_func:  # 自定制文本信息函数
			return self.text_func(field)
		if self.is_tuple:
			return field[1]
		else:
			return field
	
	def get_value(self, field):
		"""
		动态获取元组的id或对象的pk
		:param field: 元组或模型对象
		:return:
		"""
		if self.text_func:
			return self.text_func(field)
		if self.is_tuple:
			return field[0]
		else:
			return field.pk


# 使用闭包来解决choices字段的统一显示问题
def get_choices_field(title, field):
	"""
	闭包外部函数
	:param title: 显示的标题字段
	:param field: 数据库ORM定义的字段
	:return: 内部函数inner
	"""
	
	def inner(self, is_header=None, obj=None, *args, **kwargs):
		if is_header:
			return title
		show_info = "get_%s_display" % field
		return getattr(obj, show_info)  # 调用显示数据库choices中文字段的方法
	
	return inner


# 使用闭包来解决time字段的统一显示问题
def get_time_field(title, field, time_format='%Y-%m-%d'):
	"""
	闭包外部函数
	:param title: 显示的标题字段
	:param field: 数据库ORM定义的字段
	:param time_format: 可以自定义时间格式
	:return: 内部函数inner
	"""
	
	def inner(self, is_header=None, obj=None, *args, **kwargs):
		if is_header:
			return title
		time = getattr(obj, field)
		format_time = time.strftime(time_format)
		return format_time
	
	return inner


# 使用闭包来解决多对多字段的统一显示问题
def get_m2m_field(title, field):
	"""
	闭包外部函数
	:param title: 显示的标题字段
	:param field: 数据库ORM定义的字段
	:return: 内部函数inner
	"""
	
	def inner(self, is_header=None, obj=None, *args, **kwargs):
		if is_header:
			return title
		query_set = getattr(obj, field).all()  # 获取到查询集的集合对象 <QuerySet [<UserInfo: tom>]>
		res = '&'.join([str(obj) for obj in query_set])
		return res
	
	return inner


class BaseHandler:
	"""
	对各个表数据处理的基类，用于做CRUD
	如果未自定制处理数据类，直接使用此类即可
	在类的内部自定制需要显示的列名称--display_list，默认为[]
	当开发者未给模型类定制相应显示的列数据时，令数据显示当前对象即可
	通过在每个自定制类中定制函数，为每个表定制编辑、删除等表信息
	"""
	display_list = []
	per_page = 10  # 每页默认显示10条数据，在具体类中可自由设置
	has_add_btn = True  # 控制添加按钮是否显示在页面中
	customized_model_class = None  # 对于模型类所显示的字段可以选择自定制
	order_list = []  # 排序条件
	filter_list = []  # 显示过滤条件，自定制
	multi_list = []  # 批量操作的选择按钮，具体显示的操作
	search_group = []  # 获取需要显示的组合搜索信息数据
	# 基础的增删改查模板可以自定制也可直接使用设定好的
	list_template = None
	add_template = None
	edit_template = None
	del_template = None
	
	def __init__(self, stark_obj, model_class, prev=None):
		"""
		:param stark_obj: 传递的为StarkSite的对象，用于获取具体stark中的相关值
		:param model_class: 此数据用于保存及判别是哪一个模型类在处理数据及获取对应的数据
		:param prev: 获取自定制的前缀信息，默认为空数据
		"""
		self.stark_obj = stark_obj
		self.model_class = model_class
		self.prev = prev
		self.request = None
	
	def get_filter_list(self):
		"""获取程序自定制过滤条件"""
		return self.filter_list
	
	def get_multi_list(self):
		"""获取多选的操作列表"""
		return self.multi_list
	
	def multi_del(self, request, *args, **kwargs):
		"""批量删除功能，可以自定义预留执行完的功能，比如跳转等功能"""
		data_list = request.POST.getlist('pk')
		if data_list:
			# 对于id在传回列表中的值在数据库中查询并将其删除
			self.model_class.objects.filter(id__in=data_list).delete()
	
	# return redirect("https://www.baidu.com")
	
	multi_del.text = "批量删除"  # 为函数添加中文信息
	
	def multi_edit(self):
		pass
	
	multi_edit.text = "批量编辑"
	
	def display_edit(self, obj=None, is_header=None):
		"""
		自定制需要的编辑信息，通过调用函数，获取定制的表头及内容信息
		url通过反向解析生成
		namespace通过调用stark对象下的属性获取
		"""
		if is_header:
			return "编辑"
		# 通过反向解析获取真实的URL信息，通过namespace:name获取  stark:app01-userinfo-edit
		return mark_safe("<a href='%s'>编辑</a>" % self.get_reverse_edit_url(pk=obj.pk))
	
	def display_mul_op(self, obj=None, is_header=None, *args, **kwargs):
		"""
		批量操作列
		"""
		if is_header:
			return "批量选择"
		return mark_safe("<input type='checkbox' name='pk' value=%s>" % obj.pk)
	
	def display_del(self, obj=None, is_header=None):
		"""自定制需要的删除信息，通过调用函数，获取定制的表头及内容信息"""
		if is_header:
			return "删除"
		return mark_safe("<a href='%s'>删除</a>" % self.get_reverse_del_url(obj.pk))
	
	def display_del_edit(self, obj=None, is_header=None, *args, **kwargs):
		"""将编辑与删除放在统一栏中存放"""
		if is_header:
			return "操作"
		del_edit = "<a href='%s'>编辑</a> <a href='%s'>删除</a>" % (
			self.get_reverse_edit_url(pk=obj.pk), self.get_reverse_del_url(obj.pk))
		return mark_safe(del_edit)
	
	def get_display_list(self, request, *args, **kwargs):
		"""
		获取页面上应该显示的列，在此处预留一个方法，应对后期不同权限的用户访问不同列做准备
		在跟踪记录时编辑与删除页面需要重写display_del_edit，在执行时需要找到跟踪记录类的display_del_edit方法，当前self对象的类即为RecordHandler
		:return:
		"""
		info = []
		if self.display_list:
			info.extend(self.display_list)
			# info.append(BaseHandler.display_del_edit)  # 默认存在编辑与删除按钮
			info.append(type(self).display_del_edit)
		
		return info
	
	def get_add_btn(self, request, *args, **kwargs):
		"""
		预留一个添加按钮的钩子函数，可自定义样式及是否显示
		获取要添加按钮要跳转的URL-通过反向解析namespace:name
		记住原搜索条件，在添加跳转时携带
		对获取提添加url过程封装
		"""
		if self.has_add_btn:
			return "<a class='btn btn-success btn-sm' href='%s'>添加</a>" % self.get_reverse_add_url(*args, **kwargs)
		return None
	
	def get_order_list(self):
		"""获取排序的规则，优先使用用户自定制，否则默认以id排序"""
		return self.order_list or ["id"]
	
	def get_search_group(self):
		"""获取每个model类自定制的组合搜索信息"""
		return self.search_group
	
	def get_search_group_condition(self, request):
		"""
		目的：生成一个组合条件的字典，用于展示数据时过滤数据库
		:param request:
		:return:
		"""
		search_group = self.get_search_group()  # 获取组合条件的对象集合
		search_dict = {}
		for obj in search_group:  # 通过循环获取到需要在请求中获取的对象字段信息
			field_list = request.GET.getlist(obj.field)
			if field_list:
				search_dict["%s__in" % obj.field] = field_list
		return search_dict
	
	def get_queryset(self, request, *args, **kwargs):
		"""可以根据具体情形首先过滤一次数据信息"""
		return self.model_class.objects
	
	def show_view(self, request, *args, **kwargs):
		"""
		显示页面
		需要自定制获取页面显示的列标题及内容信息
		根据分页组件实现分页功能
		实现根据字段排序
		实现页面过滤条件  (OR: )   (OR: ('name__contains', 'alex'), ('email__contains', 'alex'))
		实现批量操作显示数据，有数据展示，无数据则隐藏
		:param request:
		:return:
		"""
		# 1 获取批量操作需要显示的信息数据并以生成字典形式的数据 {"multi_del":"批量删除","multi_edit":"批量编辑"}
		multi_list = self.get_multi_list()
		multi_dict = {func.__name__: func.text for func in multi_list}
		# 1.1 根据批量操作的数据来对所有数据进行操作--post请求request.POST
		if request.method == 'POST':
			multi_action = request.POST.get('multi_data')
			if hasattr(self, multi_action):
				response_action = getattr(self, multi_action)(request, *args, **kwargs)
				if response_action:
					return response_action  # 如果当前反射函数存在返回值，则不继续走下方逻辑
		# 2、获取到所有的查询条件数据,可能存在多条件过滤，需要引入Q对象，需要或关系查询条件
		filter_list = self.get_filter_list()
		search_value = request.GET.get("search", '')
		conn = Q(_connector="OR")  # 实例化Q对象
		if search_value:
			for item in filter_list:
				# conn.children.append(('name__contains', 'wu'))
				conn.children.append((item, search_value))  # 数据为元组形式
		# 3、实现排序功能
		order_list = self.get_order_list()
		# 4、排序查询所有数据集合
		# 组合搜索的条件字典信息,并将信息过滤得到结果
		search_dict = self.get_search_group_condition(request)
		query_set = self.get_queryset(request, *args, **kwargs).filter(conn).filter(**search_dict).order_by(*order_list)
		# 5、通过分页组件实现分页功能
		all_count = query_set.count()
		path_info = request.path_info  # '/stark/app01/depart/list/'
		query_params = request.GET.copy()  # This QueryDict instance is immutable
		query_params._mutable = True  # 令数据可修改
		pager = Pagination(
			current_page=request.GET.get("page"),
			all_count=all_count,
			base_url=path_info,
			query_params=query_params,
			per_page=self.per_page
		)
		data_lists = query_set[pager.start:pager.end]
		# 6 自定义显示数据信息
		# 6.1 通过定制的方法，获取不同的显示列信息
		display_list = self.get_display_list(request, *args, **kwargs)
		# 6.2 获取列信息-中文名称
		header_list = []
		if display_list:
			for key_or_func in display_list:
				# 如果元素为函数，则为自定制的表头
				if isinstance(key_or_func, FunctionType):
					header_list.append(key_or_func(self, is_header=True))
				else:
					header_list.append(self.model_class._meta.get_field(key_or_func).verbose_name)  # 获取字段对象的中文名称
		else:
			header_list.append(self.model_class._meta.model_name)  # 将当前模型类的名称添加进
		# 6.3 根据列获取具体信息
		'''
			需要生成类似的数据格式，并将其传递至前端页面进行渲染
			[
				[张三, 16, dd@qq.com],
				[李四, 16, dd@qq.com],
			]
			或
			[
				[obj],
				[obj],
			]
		'''
		info_list = []  # 整体数据信息
		for obj in data_lists:  # obj-->当前的数据对象
			temp_row = []  # 一个对象的数据列表
			if display_list:
				for key_or_func in display_list:
					if isinstance(key_or_func, FunctionType):
						temp_row.append(key_or_func(self, obj=obj, *args, **kwargs))
					elif hasattr(obj, key_or_func):
						temp_row.append(getattr(obj, key_or_func))
			else:
				temp_row.append(obj)  # 默认添加对象，显示其名称
			info_list.append(temp_row)
		# 7 自定义显示添加按钮标签
		add_btn = self.get_add_btn(request, *args, **kwargs)
		# 8 自定制显示组合搜索的信息
		search_group = self.get_search_group()  # ['gender_obj', 'classes_obj', 'depart_obj']
		# SearchGroupRow对象存储在列表中，每个对象都是可迭代对象
		search_group_row_list = []  # 将需要显示的组合搜索对象统一放置在列表中，传递至后台进行数据显示
		for option_object in search_group:
			tuple_or_obj = option_object.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
			search_group_row_list.append(tuple_or_obj)
		return render(request,
					  self.list_template or "stark/show_list.html", {
						  "header_list": header_list,
						  "info_list": info_list,
						  "pager": pager,
						  "add_btn": add_btn,
						  "filter_list": filter_list,
						  "search_value": search_value,
						  "multi_dict": multi_dict,
						  "search_group_row_list": search_group_row_list
					  })
	
	def get_model_form(self, request, pk, is_add=True, *args, **kwargs):
		"""
		根据不同的模型类对应获取不同的表单数据信息
		还可以自定制模型类中的字段，自由添加或删减
		应该根据add或edit来对页面展示不同的字段，在子类中get_model_form中重写获取模型类
		可以在获取表单时条件判断，从而选取适合的表单模型
		"""
		if self.customized_model_class:
			return self.customized_model_class
		
		class ShowModelForm(BaseModelFrom):
			class Meta:
				model = self.model_class
				fields = '__all__'
		
		return ShowModelForm
	
	def get_edit_obj(self, request, pk, *args, **kwargs):
		"""获取编辑对象的钩子函数，用于后期拓展"""
		return self.model_class.objects.filter(id=pk).first()
	
	def edit_view(self, request, pk, *args, **kwargs):
		"""
		编辑页面
		:param request:
		:param pk:
		:return:
		"""
		current_obj = self.get_edit_obj(request, pk, *args, **kwargs)
		if not current_obj:
			return HttpResponse("您要编辑的客户记录不存在，请重新检查后编辑！")
		form_class = self.get_model_form(request, pk, False, *args, **kwargs)
		if request.method == "GET":
			form = form_class(instance=current_obj)
			return render(request, self.edit_template or 'stark/change.html', {"form": form})
		form = form_class(data=request.POST, instance=current_obj)
		if form.is_valid():
			response = self.customize_save(request, form, True, *args, **kwargs)
			return response or redirect(self.get_reverse_list_url(*args, **kwargs))
		return render(request, self.edit_template or 'stark/change.html', {"form": form})
	
	def customize_save(self, request, form, is_update, *args, **kwargs):
		"""
		预留一个钩子函数，用于可自定制数据保存
		is_update--编辑或添加form信息
		"""
		form.save()
	
	def add_view(self, request, *args, **kwargs):
		"""
		添加页面
		:param request:
		:return:
		"""
		form_class = self.get_model_form(request, None, True, *args, **kwargs)
		if request.method == "GET":
			form = form_class()
			return render(request, self.add_template or 'stark/change.html', {"form": form})
		form = form_class(data=request.POST)
		if form.is_valid():
			# 获取返回值，如果有值则添加错误
			response = self.customize_save(request, form, False, *args, **kwargs)  # 数据在保存之前可以自定制存储方法来实现
			return response or redirect(self.get_reverse_list_url(*args, **kwargs))
		return render(request, self.add_template or 'stark/change.html', {"form": form})
	
	def get_del_obj(self, request, pk, *args, **kwargs):
		"""获取要删除的对象信息，预留钩子函数"""
		return self.model_class.objects.filter(id=pk).delete()
	
	def del_view(self, request, pk, *args, **kwargs):
		"""
		删除页面
		:param request:
		:param pk:
		:return:
		"""
		origin_url = self.get_reverse_list_url(*args, **kwargs)
		if request.method == "GET":
			return render(request, self.del_template or "stark/del.html", {"cancel_url": origin_url})
		response = self.get_del_obj(request, pk, *args, **kwargs)
		return response or redirect(origin_url)
	
	def get_reverse_base(self, name, *args, **kwargs):
		"""用于获取反向解析的url值的基础方法，只需传入获取当前url的name即可获取的携带条件的url"""
		name = "%s:%s" % (self.stark_obj.namespace, name)
		base_url = reverse(name, args=args, kwargs=kwargs)
		if not self.request.GET:
			url = base_url
		else:
			params = self.request.GET.urlencode()  # 携带get请求中的所有参数数据 page=1&name=lion
			new_query_dict = QueryDict(mutable=True)
			new_query_dict["_filter"] = params
			url = "%s?%s" % (base_url, new_query_dict.urlencode())
		return url
	
	def get_reverse_add_url(self, *args, **kwargs):
		"""用于获取由list页面到add页面的url-可保留原条件"""
		return self.get_reverse_base(self.get_url_add_name, *args, **kwargs)
	
	def get_reverse_list_url(self, *args, **kwargs):
		"""通过此方法获取具体要跳转至显示list页面的url，保留原条件信息"""
		name = "%s:%s" % (self.stark_obj.namespace, self.get_url_list_name)
		base_url = reverse(name, args=args, kwargs=kwargs)
		param = self.request.GET.get("_filter")
		if not param:
			return base_url
		return "%s?%s" % (base_url, param)
	
	def get_reverse_edit_url(self, *args, **kwargs):
		"""通过此方法获取具体要跳转至显示edit页面的url，保留原条件信息"""
		return self.get_reverse_base(self.get_url_edit_name, *args, **kwargs)
	
	def get_reverse_del_url(self, *args, **kwargs):
		"""通过此方法获取具体要跳转至显示del页面的url，保留原条件信息"""
		return self.get_reverse_base(self.get_url_del_name, *args, **kwargs)
	
	def get_url_name(self, param):
		"""
		将需要获取的name信息数据抽象出来，只对具体的url的类别传参
		:param param: 具体的url的类别参数
		:return: 具体的name
		"""
		app_name, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
		if self.prev:
			return "%s-%s-%s-%s" % (app_name, model_name, self.prev, param)
		return "%s-%s-%s" % (app_name, model_name, param)
	
	@property
	def get_url_list_name(self):
		"""获取list的name值"""
		return self.get_url_name("list")
	
	@property
	def get_url_add_name(self):
		"""获取add的name值"""
		return self.get_url_name("add")
	
	@property
	def get_url_edit_name(self):
		"""获取edit的name值"""
		return self.get_url_name("edit")
	
	@property
	def get_url_del_name(self):
		"""获取del的name值"""
		return self.get_url_name("del")
	
	def wrapper(self, func):
		"""
		闭包函数-为在执行前添加self.request = request至对象中
		:param func: 每个视图函数要执行的函数名
		:return:
		"""
		
		@wraps(func)  # 如果想要保留原函数的属性
		def inner(request, *args, **kwargs):
			self.request = request  # 添加显示页面的request请求信息
			return func(request, *args, **kwargs)
		
		return inner
	
	@property
	def get_urls(self):
		"""
		再分发一层级，具体实现路由分发功能,默认4个路由，如果自身有此方法，则可以自由定制路由信息
		name属性由：app名称-model名称-具体信息
		区分：前缀情形下的name值应不同，需要单独区别
		name数据整体由公共方法get_url_name统一调用，由各个分支分别传参
		为url中的视图函数添加wrapper装饰器
		为后续url中添加参数，而可以在视图中接收到并使用，在视图中添加接收参数的功能
		:return:
		"""
		patterns = [
			re_path(r"^list/$", self.wrapper(self.show_view), name=self.get_url_list_name),
			re_path(r"^add/$", self.wrapper(self.add_view), name=self.get_url_add_name),
			re_path(r"^edit/(?P<pk>\d+)/$", self.wrapper(self.edit_view), name=self.get_url_edit_name),
			re_path(r"^del/(?P<pk>\d+)/$", self.wrapper(self.del_view), name=self.get_url_del_name)
		]
		'''
				if self.prev:
			patterns = [
				re_path(r"^list/$", self.show_view, name="%s-%s-%s-list" % (app_name, model_name, self.prev)),
				re_path(r"^add/$", self.add_view, name="%s-%s-%s-add" % (app_name, model_name, self.prev)),
				re_path(r"^edit/(?P<pk>\d+)/$", self.edit_view, name="%s-%s-%s-edit" % (app_name, model_name, self.prev)),
				re_path(r"^del/(?P<pk>\d+)/$", self.del_view, name="%s-%s-%s-del" % (app_name, model_name, self.prev))
			]
		else:
			patterns = [
				re_path(r"^list/$", self.show_view, name="%s-%s-list" % (app_name, model_name)),
				re_path(r"^add/$", self.add_view, name="%s-%s-add" % (app_name, model_name)),
				re_path(r"^edit/(?P<pk>\d+)/$", self.edit_view, name="%s-%s-edit" % (app_name, model_name)),
				re_path(r"^del/(?P<pk>\d+)/$", self.del_view, name="%s-%s-del" % (app_name, model_name))
			]
		'''
		# 将需要额外添加的url添加进当前的patterns中，自动生成url列表
		patterns.extend(self.extra_url())
		return patterns, None, None
	
	def extra_url(self):
		"""
		用于4个url基础之上url的增加
		:return:
		"""
		return []


class StarkSite:
	"""
	用于自动根据具体表结构数据获取对应的url信息
	"""
	
	def __init__(self):
		self.registry = []
		self.app_name = "stark"
		self.namespace = "stark"
	
	def register(self, model_class, handler=BaseHandler, prev=None):
		"""
		为registry中添加每个app中的model类信息及处理视图对象
		:param model_class:当前model类
		:param handler:类名，设定默认值，在不需要自定制时，直接BaseHandler处理数据
		:param prev:可以为url配置中设定自定制前缀功能，默认为空
		:return:
		[{'model_class': <class 'app01.models.UserInfo'>, 'handler': <app01.stark.UserHandler object at 0x0000019B69DF5408>}, {'model_class': <class 'app01.models.Depart'>, 'handler': <app01.stark.DepartHandler object at 0x0000019B69DF5348>}, {'model_class': <class 'app02.models.Host'>, 'handler': <app02.stark.HostHandler object at 0x0000019B69DFC3C8>}]
		"""
		self.registry.append({"model_class": model_class, "handler": handler(self, model_class, prev), "prev": prev})
	
	def get_patterns(self):
		"""
		将实际拼接的数据添加进patterns中，动态生成url
		:return:
		model_class._meta.app_label:获取当前model类的对应app名称
		model_class._meta.model_name:获取当前model类的对应表名
		- app01/depart/add/
		- app01/depart/list/
		- app01/depart/edit/(\d+)/
		- app01/depart/add/(\d+)
		"""
		patterns = []
		for item in self.registry:
			model_class = item["model_class"]
			# print(model_class, model_class._meta.app_label, model_class._meta.model_name)
			handler = item["handler"]
			prev = item["prev"]
			app_name = model_class._meta.app_label
			label_name = model_class._meta.model_name
			# 将每个类中的具体信息放入相应的url中
			'''
			通过前缀prev，可以对当前的url再此进行路由include分发，减少冗余
			通过在BaseHandler或其子类中自定制get_urls，实现对url的灵活管理
			'''
			if prev:
				patterns.append(re_path(r"^%s/%s/%s/" % (app_name, label_name, prev), handler.get_urls))
			# patterns.append(re_path(r"^%s/%s/%s/add/$" % (app_name, label_name, prev), handler.add_view))
			# patterns.append(re_path(r"^%s/%s/%s/edit/(?P<pk>\d+)/$" % (app_name, label_name, prev), handler.edit_view))
			# patterns.append(re_path(r"^%s/%s/%s/del/(?P<pk>\d+)/$" % (app_name, label_name, prev), handler.del_view))
			else:
				patterns.append(re_path(r"^%s/%s/" % (app_name, label_name), handler.get_urls))
		# path("x1/", lambda x1: HttpResponse("x1")),
		# path("x2/", lambda x2: HttpResponse("x2"))
		
		return patterns
	
	@property
	def urls(self):
		return self.get_patterns(), self.app_name, self.namespace


site = StarkSite()  # 用于其他模块引入，生成单例模式
