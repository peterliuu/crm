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
	# permission_list = [item for item in url_list if None not in item]
	# 1、获取到对应的权限相关信息
	permission_queryset = user_obj.roles.filter(permissions__isnull=False).values("permissions__title", "permissions__url", "permissions__is_menu", "permissions__icon").distinct()
	# 2、获取权限列表及菜单列表
	permission_list, menu_list = [], []
	for item in permission_queryset:
		permission_list.append(item)
		# 判断菜单信息并添加进menu_list
		if item["permissions__is_menu"]:
			menu_data = {
				"title": item["permissions__title"],
				"url": item["permissions__url"],
				"icon": item["permissions__icon"],
			}
			menu_list.append(menu_data)
	# key值可以配置在settings中，方便后期维护
	request.session[settings.SESSION_KEY] = permission_list
	request.session[settings.MENU_KEY] = menu_list


















