# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/27 15:34
from django.shortcuts import render, HttpResponse, reverse, redirect
from app01.models import UserInfo
from app01.forms.user import UserForm, UpdateUserForm, PasswordResetForm
from rbac.service.url_related import get_url

"""
用户相关逻辑
"""


def user_list(request):
	"""
	显示用户信息
	:param request:
	:return:
	"""
	# 获取所有角色信息
	user_lists = UserInfo.objects.all()
	return render(request, "user_list.html", locals())


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
	form = UserForm(data=request.POST)
	if form.is_valid():
		form.save()
		return redirect(get_url(request, "user_list"))
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
	user_obj = UserInfo.objects.filter(id=pk).first()
	if not user_obj:
		return HttpResponse("您访问的页面不存在 404")
	if request.method == 'GET':
		# 将已有的数据显示在input中
		form = UpdateUserForm(instance=user_obj)
		return render(request, "rbac/change.html", {"form": form})
	form = UpdateUserForm(data=request.POST, instance=user_obj)
	if not form.is_valid():
		# 校验失败
		return render(request, "rbac/change.html", {"form": form})
	# 校验成功
	form.save()
	return redirect(get_url(request, "user_list"))


def user_reset_pwd(request, pk):
	"""
	密码重置功能
	:param request:
	:param pk:
	:return:
	"""
	user_obj = UserInfo.objects.filter(id=pk).first()
	if request.method == "GET":
		form = PasswordResetForm()
		return render(request, "rbac/change.html", locals())
	form = PasswordResetForm(data=request.POST, instance=user_obj)
	if not form.is_valid():
		# 校验失败
		return render(request, "rbac/change.html", {"form": form})
	# 校验成功
	form.save()
	return redirect(reverse("user_list"))


def user_del(request, pk):
	"""
	用户删除--为今后所有删除页面中的a标签返回都使用同一个页面，需要在后台返回，取消的a标签路由
	:param request:
	:param pk:
	:return:
	"""
	cancel_url = get_url(request, "user_list")
	if request.method == "GET":
		return render(request, "rbac/del.html", locals())
	# 确认删除
	UserInfo.objects.filter(id=pk).delete()
	return redirect(cancel_url)


