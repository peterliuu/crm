# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/9/23 23:21

from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
	if request.method == "GET":
		return render(request, "login.html")
	user = request.POST.get('user')
	pwd = request.POST.get('pwd')
	user_obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
	if not user_obj:
		return render(request, "login.html", {"msg": "用户名或密码错误"})
	'''拆分存储权限相关功能--放置在rbac组件中'''
	init_permission(request, user_obj)
	# 验证权限信息由中间件中验证
	return redirect("/customer/list/")


def user(request):
	return render(request, "user.html")



