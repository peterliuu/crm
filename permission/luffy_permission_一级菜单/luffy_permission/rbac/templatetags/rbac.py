# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/9/28 17:49

from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag("rbac/static_menu.html")
def static_menu(request):
	"""
	用于整合菜单中的html及渲染的数据
	:param request:由调用此函数的html便签进行传值
	:return:rbac/static_menu.html需要用到的参数信息
	"""
	url = request.path
	menu_list = request.session.get(settings.MENU_KEY)
	for item in menu_list:
		if item['url'] == url:
			item.update({"status": "active"})
	return {"menu_list": menu_list}  # 向模板中传递参数，字典形式




