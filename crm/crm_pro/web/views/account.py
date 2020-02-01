# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/27 22:49
from django.shortcuts import render, reverse, redirect

from rbac.service.init_permission import init_permission
from web import models
from web.utils.md5 import gen_md5

"""
登录相关
"""


def login(request):
	"""
	登录
	:param request:
	:return:
	"""
	if request.method == "GET":
		return render(request, "login.html")
	username = request.POST.get("user")
	pwd = request.POST.get("password")
	# 将密码加密后校验
	data_pwd = gen_md5(pwd)
	# 校验数据
	user_obj = models.UserInfo.objects.filter(name=username, password=data_pwd).first()
	if not user_obj:
		return render(request, "login.html", {"errmsg": "用户名或密码错误"})
	# 将数据信息添加至session状态保持
	request.session["user_info"] = {"user_id": user_obj.id, "user": username}
	# 权限初始化,将权限及菜单信息存储进session中
	init_permission(request, user_obj)
	# 重定向回index页面
	return redirect(reverse("index"))


def logout(request):
	"""
	注销
	:param request:
	:return:
	"""
	# 删除session中存储的数据
	request.session.delete()
	return redirect(reverse("login"))


def index(request):
	"""
	测试首页
	:param request:
	:return:
	"""
	return render(request, "index.html")
