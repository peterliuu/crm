# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/9/26 23:44
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class RBACMiddleware(MiddlewareMixin):
	"""
		放置在rbac组件中，用户后期维护和迁移
		用于校验用户权限信息
		1、获取登录的url
		2、获取当前用户的session中权限信息list
		3、登录的url是否与权限信息list匹配
	"""

	def process_request(self, request):
		"""
			url进入时直接校验权限
			在验证前需要设置白名单，所有人均可访问的信息--列表形式
			登录后不需权限分配，所有人皆可访问的url信息
			:param request:
			:return: 返回非空值表示不继续向下，直接运行response返回
		"""
		# 获取请求url
		request_url = request.path  # 获取url的方法
		# 设置白名单--将白名单放置配置中，方便后期管理
		white_lists = settings.WHITE_LISTS
		# 进入前url与白名单匹配
		for white in white_lists:
			if re.match(white, request_url):
				return None  # 不做阻拦
		# 获取当前用户的所有权限列表
		user_permission_dict = request.session.get(settings.SESSION_KEY)
		# 首先验证权限列表是否为空
		if not user_permission_dict:
			return HttpResponse("未查到用户权限，请登陆！")
		# 判断是否在权限中
		flag = False
		# 增加动态导航列表
		menu_record = [{"title": "首页", "url": "#"}]
		request.menu_record = menu_record
		request.judgement_info = None
		# 登录后不需要权限的验证
		for item in settings.NO_PERMISSIONS_LIST:
			if re.match(item, request_url):
				return None
		
		for user_permission in user_permission_dict.values():
			# 正则匹配-增加开头和结尾，避免匹配出错
			user_url = "^%s$" % user_permission["url"]
			pattern_compile = re.compile(user_url)
			if pattern_compile.match(request_url):
				flag = True
				# 当匹配成功后，在request中添加pid或id
				request.judgement_info = user_permission["pid"] or user_permission["id"]
				# 通过pid判别数据是否有父级单位
				if user_permission["pid"]:
					menu_record.extend([{"title": user_permission["p_title"], "url":user_permission["p_url"]}, {"title": user_permission["title"], "url":user_permission["url"], "class": 'active'}])
				else:
					menu_record.extend([{"title": user_permission["title"], "url": user_permission["url"], "class": 'active'}])
				# 将导航数据添加进request
				request.menu_record = menu_record
				break
		if not flag:
			return HttpResponse("您的权限不足，无法访问！！！")
		return None
