# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/13 12:16

from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string  # 将当前字符串当做模块导入
from django.urls import URLResolver, URLPattern  # 获取url的状态值
import re

"""
	处理获取所有url信息
"""


def check_exclude_url(url):
	"""
	过滤不需查询的白名单url
	:param url:需要查询的url
	:return:状态
	"""
	for regex in settings.URL_EXCLUDE_LIST:
		condition = re.compile(regex)
		if condition.match(url):
			return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
	"""
	使用递归获取所有的urls字典
	URLResolver--url数据有下一层级
	URLPattern--无子级url
	:param pre_namespace: namespace前缀，用于最后拼接name值  rbac:menu_list
	:param pre_url:url前缀，用于拼接url
	:param urlpatterns:路由关系列表
	:param url_ordered_dict:用于保存递归中获取的所有路由信息
	:return:
	"""
	for item in urlpatterns:
		if isinstance(item, URLPattern):
			if not item.name:  # 必须有name值
				continue
			# 获取name值--》由namespace与name拼接而成
			if pre_namespace:
				name = "%s:%s" % (pre_namespace, item.name)
			else:
				name = item.name
			# /^rbac/^role/list/$--》将特殊字符替换
			url = (pre_url + str(item.pattern)).replace("^", "").replace("$", "")
			# 在生成数据之前判断该url是否需要过滤
			if check_exclude_url(url):
				continue
			url_ordered_dict[name] = {"name": name, "url": url}
		elif isinstance(item, URLResolver):  # 递归操作获取url
			if pre_namespace:
				if item.namespace:
					namespace = "%s:%s" % (pre_namespace, item.namespace)
				else:
					namespace = pre_namespace
			else:
				if item.namespace:
					namespace = item.namespace
				else:
					namespace = None
			recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)
	return url_ordered_dict


def get_all_urls_dict():
	"""
	获取当前项目中的所有路由信息(必须有name别名)
	设计的有序字典的结构为：
	{
		"rbac:menu_list": { 'name': "rbac:menu_list", "url": 'xxx/menu_list'}
	}
	:return:
	"""
	# 创建有序字典对象
	order_dict = OrderedDict()
	# 引入当前的根级url的urlpatterns数据  from xxx import urls
	url_module = import_string(settings.ROOT_URLCONF)
	# for item in url_module.urlpatterns:
	# 	print(item)
	# 使用递归获取所有的urls数据
	url_ordered_dict = recursion_urls(None, "/", url_module.urlpatterns, order_dict)
	return url_ordered_dict
