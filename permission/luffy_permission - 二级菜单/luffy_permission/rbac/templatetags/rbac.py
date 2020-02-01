# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/9/28 17:49

from django import template
from django.conf import settings
from collections import OrderedDict  # 有序字典
from rbac.service import url_related
register = template.Library()


@register.inclusion_tag("rbac/multi-menu.html")
def multi_menu(request):
	"""
	用于整合菜单中的html及渲染的数据
	有序字典目的：每次菜单显示顺序一致
	:param request:由调用此函数的html便签进行传值
	:return:rbac/static_menu.html需要用到的参数信息
	"""
	url = request.path  # 获取当前url
	menu_dict = request.session.get(settings.MENU_KEY)  # 获取session中存储的menu_dict
	'''
	自己代码
		for item in menu_dict.values():
		for ele in item['children']:
			if ele['url'] == url:
				ele.update({"status": "active"})
	'''
	# 课件代码
	# 1、对获取的字典key进行排序
	order_key = sorted(menu_dict)
	# 2、实例化一个有序字典对象
	ordered_dict = OrderedDict()
	# 3、为选中的元素添加class = active
	for key in order_key:
		ordered_dict[key] = menu_dict[key]
		ordered_dict[key]['class'] = 'hide'
		for ele in ordered_dict[key]['children']:
			# cur_url = "^%s$" % ele['url']  # 之前以url判断
			# if re.match(cur_url, url):
			if ele['id'] == request.judgement_info:  # 通过id具体判别
				ele['class'] = 'active'
				ordered_dict[key]['class'] = ''
	return {"menu_dict": ordered_dict}  # 向模板中传递参数，字典形式


@register.inclusion_tag("rbac/show_nav.html")
def show_nav(request):
	"""
	用于动态显示导航信息自定义
	:param request:
	:return: 导航所需数据
	"""
	return {"menu_record": request.menu_record}


@register.filter
def has_permission(request, name):
	"""
	通过自定义过滤器过滤权限是否显示
	在html中使用时格式：args1|has_permission:"args2"
	:param request:
	:param name: 别名
	:return:权限状态结果
	"""
	# 判断name是否在session中
	if name in request.session.get(settings.SESSION_KEY):
		return True


@register.simple_tag
def memory_url(request, path, *args, **kwargs):
	"""将功能写在rbac.service.url_related模块内，方便后期改动"""
	return url_related.memory_url(request, path, *args, **kwargs)
