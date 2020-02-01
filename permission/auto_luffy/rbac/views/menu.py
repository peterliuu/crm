# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/4 10:43

from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.utils.module_loading import import_string  # 将字符串当做模块引入
from collections import OrderedDict
from django.forms import formset_factory
from rbac.myForms.menu import MenuForm, SecondMenuForm, PermissionMenuForm, MultiPermissionAdd, MultiPermissionUpdate
from rbac.service.url_related import get_url
from rbac.service.check_url import get_all_urls_dict  # 获取需要当前项目中的url
from rbac import models


def menu_list(request):
	"""
	菜单
	前端数字变量转为字符串--row.pk|safe
	:param request:
	:return:
	"""
	if request.method == 'GET':
		# 获取所有的menu信息
		form = models.Menu.objects.all()
		# 请求中后缀带?mid=1,可以使用get来获取具体数据,模板根据mid的值来判别具体哪个框被选中
		mid = request.GET.get("mid")  # 字符串格式
		# 当mid存在时二级菜单可正常显示，否则为空
		# 获取所有的二级菜单，通过mid关联数据
		# 判断mid是否正确存在
		m_state = models.Menu.objects.filter(id=mid).exists()
		if mid and m_state:
			second_menus = models.Permission.objects.filter(menu=mid)
		else:
			mid = None
		# 获取2级菜单中当前被选中的id
		sid = request.GET.get("sid")
		# 数据库查询，防止数据伪造
		s_state = models.Permission.objects.filter(pid_id=sid).exists()
		if sid and s_state:
			# 通过sid获取对应的权限--》pid == sid查询集
			permission_set = models.Permission.objects.filter(pid_id=sid)
		else:
			sid = None
		return render(request, "rbac/menu_list.html", locals())


def menu_add(request):
	"""
	添加菜单
	:param request:
	:return:
	"""
	if request.method == 'GET':
		form = MenuForm()
		return render(request, "rbac/change.html", locals())
	# 校验数据，无误后添加数据至数据库
	form = MenuForm(request.POST)
	if form.is_valid():
		# 添加数据至数据可
		title = request.POST.get("title")
		icon = request.POST.get("icon")
		models.Menu.objects.create(title=title, icon=icon)
		return redirect(get_url(request, "rbac:menu_list"))
	return render(request, "rbac/change.html", locals())


def menu_edit(request, pk):
	"""
	菜单编辑
	:param request:
	:param pk:
	:return:
	"""
	if request.method == 'GET':
		menu_obj = models.Menu.objects.filter(id=pk).first()
		if not menu_obj:
			return HttpResponse("您访问的页面不存在！ 404")
		form = MenuForm({"title": menu_obj.title, "icon": menu_obj.icon})
		return render(request, "rbac/change.html", locals())
	form = MenuForm(request.POST)
	if not form.is_valid():
		return render(request, "rbac/change.html", locals())
	title = request.POST.get("title")
	icon = request.POST.get("icon")
	models.Menu.objects.filter(id=pk).update(title=title, icon=icon)
	return redirect(get_url(request, "rbac:menu_list"))


def menu_del(request, pk):
	"""
	菜单删除
	:param request:
	:param pk:
	:return:
	"""
	url = get_url(request, "rbac:menu_list")
	if request.method == 'GET':
		return render(request, "rbac/del.html", {"cancel_url": url})
	menu_obj = models.Menu.objects.filter(id=pk).first()
	if not menu_obj:
		return HttpResponse("您访问的页面不存在！ 404")
	menu_obj.delete()
	return redirect(url)


def second_menu_add(request, mid):
	"""
	添加2级菜单数据
	:param request:
	:param mid: 一级菜单id,添加时显示默认为当前一级菜单添加二级菜单
	:return:
	"""
	if request.method == "GET":
		# 获取当前一级菜单对象--传递对象
		menu_obj = models.Menu.objects.filter(id=mid).first()
		form = SecondMenuForm(initial={"menu": mid})
		# form = SecondMenuForm(initial={"menu":menu_obj})
		return render(request, "rbac/change.html", locals())
	form = SecondMenuForm(data=request.POST)
	if form.is_valid():
		# 直接对获取的form对象save
		form.save()
		return redirect(get_url(request, "rbac:menu_list"))
	return render(request, "rbac/change.html", locals())


def second_menu_edit(request, pk):
	"""
	二级菜单编辑
	:param request:
	:param pk: sid
	:return:
	"""
	permission_obj = models.Permission.objects.filter(id=pk).first()
	if request.method == "GET":
		form = SecondMenuForm(instance=permission_obj)
		return render(request, "rbac/change.html", locals())
	form = SecondMenuForm(data=request.POST, instance=permission_obj)
	if form.is_valid():
		form.save()
		return redirect(get_url(request, "rbac:menu_list"))
	return render(request, "rbac/change.html", locals())


def second_menu_del(request, pk):
	"""
	二级菜单删除
	:param request:
	:param pk: sid
	:return:
	"""
	url = get_url(request, "rbac:menu_list")  # 获取到取消或删除后返回的url
	if request.method == "GET":
		return render(request, 'rbac/del.html', {"cancel_url": url})
	models.Permission.objects.filter(id=pk).delete()
	return redirect(get_url(request, "rbac:menu_list"))


def permission_add(request, second_menu_id):
	"""
	增加权限
	:param request:
	:param second_menu_id: 2级菜单ID
	:return:
	"""
	if request.method == "GET":
		form = PermissionMenuForm()
		return render(request, "rbac/change.html", locals())
	form = PermissionMenuForm(data=request.POST)
	if form.is_valid():
		# 数据保存之前需要获取到数据的pid对象
		second_menu_obj = models.Permission.objects.filter(id=second_menu_id).first()
		if not second_menu_obj:
			return HttpResponse("您查询的二级菜单不存在，请重新尝试！")
		'''
			form.instance包含用户提交的所有信息
			form.save()--内部实现过程
			instance = models.Permission(title=="", name="", url="", pid=second_menu_obj)
			instance.pid = second_menu_obj
			instance.save()
		'''
		# form.instance.pid_id = second_menu_id  # 通过id
		form.instance.pid = second_menu_obj  # 通过对象
		form.save()
		return redirect(get_url(request, "rbac:menu_list"))
	return render(request, "rbac/change.html", locals())


def permission_edit(request, pk):
	"""
	权限修改
	:param request:
	:param pk:主键ID
	:return:
	"""
	permission_obj = models.Permission.objects.filter(id=pk).first()
	if request.method == "GET":
		form = PermissionMenuForm(instance=permission_obj)
		return render(request, "rbac/change.html", locals())
	form = PermissionMenuForm(data=request.POST, instance=permission_obj)
	if form.is_valid():
		form.save()
		return redirect(get_url(request, "rbac:menu_list"))
	return render(request, "rbac/change.html", locals())


def permission_del(request, pk):
	"""
	权限删除
	:param request:
	:param pk:主键ID
	:return:
	"""
	url = get_url(request, "rbac:menu_list")
	if request.method == "GET":
		return render(request, "rbac/del.html", {"cancel_url": url})
	models.Permission.objects.filter(id=pk).delete()
	return redirect(get_url(request, "rbac:menu_list"))


def multi_permissions(request):
	"""
	批量操作权限
	:param request:
	:return:
	"""
	# 先创建批量操作表单类
	formset_update_class = formset_factory(MultiPermissionUpdate, extra=0)
	formset_add_class = formset_factory(MultiPermissionAdd, extra=0)
	# 通过get数据中的?type=generate获取具体的type数据
	type_data = request.GET.get("type")
	# 新增数据
	if request.method == "POST" and type_data == "generate":
		formset_add = formset_add_class(data=request.POST)
		if formset_add.is_valid():
			# 数据校验成功
			# [{'title': '客户列表', 'url': '/customer/list/', 'name': 'customer_list', 'menu_id': '1', 'pid_id': ''}……]
			clean_data_list = formset_add.cleaned_data
			object_lists = []  # 创建一个列表用于存放所有的对象，后面一次性添加至数据库
			err_status = False
			for index in range(formset_add.total_form_count()):
				row_data = clean_data_list[index]
				try:
					per_add_obj = models.Permission(**row_data)
					per_add_obj.validate_unique()  # 校验字段中的唯一性
					object_lists.append(per_add_obj)
				except Exception as e:
					# 将错误信息放入errors中，用于展示到页面中
					formset_add.errors[index].update(e)
					err_status = True
			# 当所有的数据校验无误后，将所有数据对象添加进数据库中
			if not err_status:
				# 批量添加数据-batch_size一次性向数据库中添加的数据量
				models.Permission.objects.bulk_create(object_lists, batch_size=100)
	# 如果失败，将formset_add的数据及错误信息显示在前端页面中
	# 更新数据
	if request.method == "POST" and type_data == "update":
		formset_update = formset_update_class(data=request.POST)
		if formset_update.is_valid():
			# 数据校验成功
			clean_data_list = formset_update.cleaned_data
			for index in range(formset_update.total_form_count()):
				row_data = clean_data_list[index]
				# 'id': 12, 获取主键
				update_id = row_data.pop("id")
				try:
					update_obj = models.Permission.objects.filter(id=update_id).first()
					# 将传入的数据添加进当前对象中，再进行数据校验
					for k, v in row_data.items():
						setattr(update_obj, k, v)
					update_obj.validate_unique()
					update_obj.save()
				except Exception as e:
					formset_update.errors[index].update(e)
	
	# for k, v in url_ordered_dict.items():
	# 	print(k, v)
	# 1、自动获取项目中的URL
	url_ordered_dict = get_all_urls_dict()
	'''
	{
		"rbac:menu_list": {"name": "rbac:menu_list", "url":"/rbac/menu/list"},
		"rbac:menu_add": {"name": "rbac:menu_add", "url":"/rbac/menu/add"},
	}
	'''
	# 获取数据name的集合
	url_ordered_set = set(url_ordered_dict.keys())
	
	# 2、获取数据库中的所有url相关信息
	permission_url_info = models.Permission.objects.all().values()  # [{},……]
	permission_url_dict = OrderedDict()
	'''
	{
		"rbac:menu_list": {"title":"菜单列表", "name": "rbac:menu_list", "url":"/rbac/menu/list"……},
		"rbac:menu_add": {"title":"增加菜单", "name": "rbac:menu_add", "url":"/rbac/menu/add"……},
	}
	'''
	permission_url_set = set()
	for item in permission_url_info:
		permission_url_dict[item["name"]] = item
		permission_url_set.add(item["name"])  # 获取数据name的集合
	# --增加一条判断，permission与自动获取url中的name值相同，但url可能不同，需要校验数据
	for name, value in permission_url_dict.items():
		url_value = url_ordered_dict.get(name)
		if url_value:
			if value["url"] != url_value["url"]:
				value["url"] = "数据库中的URL与路由不一致"
	
	# 3、根据数据库中的url与自动获取的url之间进行一个对比，然后增加、更新、删除操作
	# 3.1向数据库增加数据
	generate_url = url_ordered_set - permission_url_set
	# 3.1.1 获取所有的增加url及相关信息字典并创建多表验证
	
	generate_url_list = [item for name, item in url_ordered_dict.items() if name in generate_url]
	formset_add = formset_add_class(initial=generate_url_list)
	
	# 3.2从数据库删除数据
	delete_url = permission_url_set - url_ordered_set
	delete_url_list = [item for name, item in permission_url_dict.items() if name in delete_url]
	# 3.3向数据库更新数据
	update_url = permission_url_set & url_ordered_set
	update_url_dict = [item for name, item in permission_url_dict.items() if name in update_url]
	
	formset_update = formset_update_class(initial=update_url_dict)
	
	return render(request, "rbac/multi_permissions.html", {"formset_add": formset_add,
														   "delete_url_list": delete_url_list,
														   "formset_update": formset_update})


def multi_permissions_del(request, pk):
	"""
	删除权限信息
	:param request:
	:param pk: 主键
	:return:
	"""
	url = get_url(request, "rbac:multi_permissions")
	if request.method == "GET":
		return render(request, "rbac/del.html", {"cancel_url": url})
	models.Permission.objects.filter(id=pk).delete()
	return redirect(get_url(request, "rbac:multi_permissions"))


def distribute_permissions(request):
	"""
	用户、角色权限分配
	思路：
	显示权限分配中的一级二级三级菜单
	通过构造各菜单字典，通过字典中的key，便于在列表中判断是否在其children字段下及动态添加数据至all_menu_list
	页面中显示具体数据，根据当前用户或角色信息id与数据库中进行比对
	对用户--角色，角色--权限，更新数据需要使用form表单传输数据
	:param request:
	:return:
	"""
	# 获取所有用户-从业务表数据中获取settings中设置好
	# 将字符转为模块 "app01.models.UserInfo"
	user_model_class = import_string(settings.RBAC_USER_MODEL_CLASS)
	all_user_lists = user_model_class.objects.all()
	# 获取所有角色
	all_role_lists = models.Role.objects.all()
	'''
	根据一级菜单、二级菜单、三级菜单拼凑起来具体要向前端返回的数据
		[
			{id: 1, title:信息管理,children:[
				{id:1, title:客户列表, menu_id:1,children:[
					{id:1, title:添加客户}
				]},
				{id:1, title:账单列表, menu_id:1, children:[
					{id:1, title:添加账单}
				]},
			]
			}，
			{id: 1, title:权限管理,children:[……
		]
	'''
	# 获取所有一级菜单
	'''
		[
			{id:1, title:信息管理, "children":[]},
			{id:2, title:权限管理, "children":[]},
		]
		
	'''
	all_menu_list = models.Menu.objects.all().values("id", "title")
	all_menu_dict = {}
	'''
		{
			1:{id:1, title:信息管理, "children":[{id:1, title:客户列表, menu_id:1}]},
			2:{id:2, title:权限管理, "children":[{id:2, title:账单列表, menu_id:1}]},
		}
	'''
	for item in all_menu_list:
		item["children"] = []
		all_menu_dict[item["id"]] = item
	
	# 获取所有二级菜单--menu_id不为空
	'''
		[
			{id:1, title:客户列表, menu_id:1, children:[]},
			{id:2, title:账单列表, menu_id:1, children:[]},
		]
	
	'''
	all_second_list = models.Permission.objects.filter(menu_id__isnull=False).values("id", "title", "menu_id")
	all_second_dict = {}
	'''
		{
			1:{id:1, title:客户列表, menu_id:1, children:[]},
			2:{id:2, title:账单列表, menu_id:1, children:[]},
		}
	'''
	# 判断menu_id与all_menu_dict的key值是否相同，相同则添加至其children中
	for item in all_second_list:
		menu_id = item["menu_id"]
		if menu_id in all_menu_dict.keys():
			all_second_dict[item["id"]] = item
			item["children"] = []
			all_menu_dict[menu_id]["children"].append(item)
	# 获取所有三级菜单--menu_id为空,pid不为空
	'''
		[
			{id:1, title:添加客户, pid_id:1},
			{id:2, title:删除客户, pid_id:1},
		]
	'''
	all_permission_list = models.Permission.objects.filter(menu_id__isnull=True, pid_id__isnull=False).values("id",
																											  "title",
																											  "pid_id")
	for item in all_permission_list:
		pid_id = item["pid_id"]
		if pid_id in all_second_dict.keys():
			all_second_dict[pid_id]["children"].append(item)
	# 根据前端的菜单id决定是否选中
	user_id = request.GET.get('uid')
	user_obj = user_model_class.objects.filter(id=user_id).first()
	if not user_obj:
		user_id = None
	# 通过user_id找到对应的角色id并返回至前端页面
	if user_id:
		# 获取当前用户的所有角色
		role_list = user_obj.roles.all()
	else:
		role_list = []
	# 接收当前的角色id
	role_id = request.GET.get('rid')
	# 校验
	role_obj = models.Role.objects.filter(id=role_id).first()
	if not role_obj:
		role_id = None
	# 对数据保存更新
	if request.POST and request.POST.get("type") == "role":  # 保存用户--》角色
		# 根据具体的数据更新用户角色--获取当前用户选中的角色id
		role_id_list = request.POST.getlist("roles")
		if not user_obj:
			return HttpResponse("当前用户不存在")
		if not role_id_list:
			role_id_list = []
		user_obj.roles.set(role_id_list)  # 多对多数据更新
	if request.POST and request.POST.get("type") == "permission":  # 保存角色——》权限
		permission_id_list = request.POST.getlist("permissions")
		if not role_obj:
			return HttpResponse("不存在此角色信息")
		if not permission_id_list:
			permission_id_list = []
		role_obj.permissions.set(permission_id_list)
	# 前端判断，生成字典，key值为具体的role_id，如果role_id在dict中则选中多选框
	role_dict = {item.id: None for item in role_list if item}
	'''
		role_dict-->{
			1:None,
			2:None,
		}
	'''
	# 获取当前用户的所有权限--从优先级来讲，角色的权限更高
	if role_id:
		permission_list = role_obj.permissions.all()
		permission_dict = {item.id: None for item in permission_list}
	elif user_id:
		permission_list = user_obj.roles.filter(permissions__id__isnull=False).values("permissions__id").distinct()
		permission_dict = {item["permissions__id"]: None for item in permission_list}
	else:
		permission_dict = {}
	
	return render(request, "rbac/distribute_permissions.html", {
		"all_user_lists": all_user_lists,
		"all_role_lists": all_role_lists,
		"all_menu_list": all_menu_list,
		"user_id": user_id,
		"role_dict": role_dict,
		"permission_dict": permission_dict,
		"role_id": role_id,
		
	})
