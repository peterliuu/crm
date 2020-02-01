# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/4 18:19
from django.shortcuts import reverse
from django.http import QueryDict


def get_url(request, params, *args, **kwargs):
	"""
	对于重定向时返回url的判断，有参数及无参数情形
	:param request:
	:param params:重定向的参数
	:return:拼接好的url
	"""
	# 获取前端页面中的_filter参数
	path = reverse(params, args=args, kwargs=kwargs)
	params = request.GET.get("_filter")
	if params:
		path = "%s?%s" % (path, params)
	return path


def memory_url(request, path, *args, **kwargs):
	"""
		生成带有原来搜索条件的url,替代原有模板中的url
		:param request: 获取请求中携带的参数
		:param path: 正常的路径信息
		:param args: 其余参数
		:param kwargs: 其余参数
		:return: 返回拼接好的url路径
		"""
	# 通过反向解析获取路径-rbac/menu/add
	# a标签路径在自定义标签中反向解析
	'''
	特别注意：在反向解析时对于参数传递，需要关注
	args：如果前端传递数据为值则为元祖row.id-->(1,)
	kwargs如果前端传递数据为表达式则为字典pk=row.id-->{'pk':1}
	'''
	url = reverse(path, args=args, kwargs=kwargs)
	# 判断get中是否有参数
	if request.GET:
		path = request.GET.urlencode()
		# 需要通过某种手段进行路径拼接
		query_dict = QueryDict(mutable=True)
		# 将get得到的数据与_filter进行拼接
		query_dict["_filter"] = path
		# 拼接整体路径
		url = "%s?%s" % (url, query_dict.urlencode())
		return url
	# 不带参数直接返回数据
	return url
