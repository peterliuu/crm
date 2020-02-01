# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/3 10:53
from django.shortcuts import render, redirect, reverse, HttpResponse
from rbac.myForms.role import RoleForm
from rbac import models

"""
用于解析角色相关的业务逻辑
今后所有添加的页面均可使用change.html来动态渲染页面
"""


def role_list(request):
	"""
	角色列表
	:param request:
	:return:角色列表
	"""
	# 获取所有角色信息
	role_lists = models.Role.objects.all()
	return render(request, "rbac/role_list.html", locals())


def role_add(request):
	"""
	添加角色数据
	:param request:
	:return:
	"""
	if request.method == "GET":
		form = RoleForm()
		return render(request, "rbac/change.html", locals())
	# 校验传回的数据
	form = RoleForm(request.POST)
	if form.is_valid():
		title = request.POST.get("title")
		models.Role.objects.create(title=title)
		return redirect(reverse("rbac:role_list"))
	# 如果数据校验出错
	# 将错误信息放回至前端页面
	print(form.errors.get('title')[0])
	return render(request, "rbac/change.html", {"form": form})


def role_edit(request, pk):
	"""
	用于编辑角色信息
	:param request:
	:param pk:角色信息主键
	:return:get: 返回更新界面
			post:返回错误信息或成功后role_list页面
	"""
	role_obj = models.Role.objects.filter(id=pk).first()
	if not role_obj:
		return HttpResponse("您访问的页面不存在 404")
	if request.method == 'GET':
		# 将已有的数据显示在input中
		form = RoleForm({"title":role_obj.title})
		return render(request, "rbac/change.html", {"form": form})
	form = RoleForm(request.POST)
	if not form.is_valid():
		# 校验失败
		return render(request, "rbac/change.html", {"form": form})
	# 校验成功
	title = request.POST.get("title")
	models.Role.objects.filter(pk=pk).update(title=title)
	return redirect(reverse("rbac:role_list"))


def role_del(request, pk):
	"""
	角色删除--为今后所有删除页面中的a标签返回都使用同一个页面，需要在后台返回，取消的a标签路由
	:param request:
	:param pk:
	:return:
	"""
	cancel_url = reverse("rbac:role_list")
	if request.method == "GET":
		return render(request, "rbac/del.html", locals())
	# 确认删除
	models.Role.objects.filter(id=pk).delete()
	return redirect(cancel_url)




















