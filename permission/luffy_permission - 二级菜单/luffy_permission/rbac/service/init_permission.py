# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/9/26 23:26
from django.conf import settings


def init_permission(request, user_obj):
	"""
	用于将权限信息放入至session中，解耦功能
	:param request: 请求
	:param user_obj: 用户对象
	:return:
	"""
	# 通过当前的用户查询关联表查询出相关的权限url信息
	# 首先查询出用户对应的查询集，然后通过表关联获取到所有的权限查询集
	# 对查询的数据去重--distinct()
	# 某些角色可能未设置权限，查询出的数据为空，需要避免
	# url_list = user_obj.roles.filter(permissions__isnull=False).values_list( "permissions__url").distinct()
	# permission_dict = [item for item in url_list if None not in item]
	'''
	自己写的代码
	# 1、获取到对应的权限相关信息
	permission_queryset = user_obj.roles.filter(permissions__isnull=False).values("permissions__title", "permissions__url", "permissions__menu", "permissions__id").distinct()

	# 2、获取权限列表及菜单列表
	permission_dict, menu_dict = [], {}
	for item in permission_queryset:
		permission_dict.append(item)
		menu_id = item['permissions__menu']
		menu_obj = models.Menu.objects.filter(id=menu_id).first()
		if not menu_obj:
			continue
		# 判断菜单信息并添加进menu_list
		if item["permissions__menu"]:
			menu_data = {
				"title": item["permissions__title"],
				"url": item["permissions__url"],
			}
		# 判断menu_list是否有值
		if menu_id in menu_dict.keys():
			menu_dict[menu_id]["children"].append(menu_data)
		else:
			tem_dict = {"title": menu_obj.title, "icon": menu_obj.icon, "children":[]}
			tem_dict["children"].append(menu_data)
			menu_dict[menu_id] = tem_dict
	'''
	# 课程代码
	# 1、获取菜单及权限信息查询集
	queryset = user_obj.roles.filter(permissions__isnull=False).values(
		"permissions__title",
		"permissions__menu_id",
		"permissions__url",
		"permissions__menu__icon",
		"permissions__menu__title",
		"permissions__pid_id",
		"permissions__id",
		"permissions__pid__url",  # 为导航条动态显示做准备
		"permissions__pid__title",
		"permissions__name"
	).distinct()

	# 2、获取权限及菜单存储
	permission_dict, menu_dict = {}, {}
	for item in queryset:
		# 将id及pid放入permission_list
		permission_dict[item["permissions__name"]] = {"id": item["permissions__id"],
								"url": item["permissions__url"],
								"title": item["permissions__title"],
								"pid": item["permissions__pid_id"],
								"p_title": item["permissions__pid__title"],
								"p_url": item["permissions__pid__url"],
								}
		# 将数据添加进menu_dict
		menu_id = item["permissions__menu_id"]
		node = {
			"id": item["permissions__id"],
			"url": item["permissions__url"],
			"title": item["permissions__title"]
		}
		if not menu_id:
			continue
		if menu_id in menu_dict:
			menu_dict[menu_id]["children"].append(node)
		else:
			menu_dict[menu_id] = {
				"title": item["permissions__menu__title"],
				"icon": item["permissions__menu__icon"],
				"children": [node]
			}
	# key值可以配置在settings中，方便后期维护
	request.session[settings.SESSION_KEY] = permission_dict
	request.session[settings.MENU_KEY] = menu_dict
