# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/3 10:53
from django.shortcuts import render, redirect, reverse, HttpResponse
from rbac.myForms.user import UserForm, UpdateUserForm, PasswordResetForm
from rbac import models

"""
用于解析用户相关的业务逻辑
今后所有添加的页面均可使用change.html来动态渲染页面
"""


def user_list(request):
	"""
	用户列表
	:param request:
	:return:角色列表
	"""
	# 获取所有角色信息
	user_lists = models.UserInfo.objects.all()
	return render(request, "rbac/user_list.html", locals())


def user_add(request):
	"""
	添加用户数据
	:param request:
	:return:
	"""
	if request.method == "GET":
		form = UserForm()
		return render(request, "rbac/change.html", locals())
	# 校验传回的数据
	form = UserForm(request.POST)
	if form.is_valid():
		name = request.POST.get("name")
		email = request.POST.get("email")
		pwd = request.POST.get("pwd")
		re_pwd = request.POST.get("re_pwd")
		models.UserInfo.objects.create(name=name, email=email, password=pwd)
		return redirect(reverse("rbac:user_list"))
	# 如果数据校验出错
	# 将错误信息放回至前端页面
	return render(request, "rbac/change.html", {"form": form})


def user_edit(request, pk):
	"""
	用于编辑用户信息
	:param request:
	:param pk:角色信息主键
	:return:get: 返回更新界面
			post:返回错误信息或成功后role_list页面
	"""
	user_obj = models.UserInfo.objects.filter(id=pk).first()
	if not user_obj:
		return HttpResponse("您访问的页面不存在 404")
	if request.method == 'GET':
		# 将已有的数据显示在input中
		form = UpdateUserForm({"name": user_obj.name, "email": user_obj.email})
		return render(request, "rbac/change.html", {"form": form})
	form = UpdateUserForm(request.POST)
	if not form.is_valid():
		# 校验失败
		return render(request, "rbac/change.html", {"form": form})
	# 校验成功
	name = request.POST.get("name")
	email = request.POST.get("email")
	models.UserInfo.objects.filter(pk=pk).update(name=name, email=email)
	return redirect(reverse("rbac:user_list"))


def user_reset_pwd(request, pk):
	"""
	密码重置功能
	:param request:
	:param pk:
	:return:
	"""
	if request.method == "GET":
		form = PasswordResetForm()
		return render(request, "rbac/change.html", locals())
	form = PasswordResetForm(request.POST)
	if not form.is_valid():
		# 校验失败
		return render(request, "rbac/change.html", {"form": form})
	# 校验成功
	pwd = request.POST.get("pwd")
	models.UserInfo.objects.filter(pk=pk).update(password=pwd)
	return redirect(reverse("rbac:user_list"))


def user_del(request, pk):
	"""
	用户删除--为今后所有删除页面中的a标签返回都使用同一个页面，需要在后台返回，取消的a标签路由
	:param request:
	:param pk:
	:return:
	"""
	cancel_url = reverse("rbac:user_list")
	if request.method == "GET":
		return render(request, "rbac/del.html", locals())
	# 确认删除
	models.UserInfo.objects.filter(id=pk).delete()
	return redirect(cancel_url)
