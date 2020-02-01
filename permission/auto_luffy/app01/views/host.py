# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/27 15:34
from django.shortcuts import render, HttpResponse, reverse, redirect
from app01.models import Host
from app01.forms.host import HostForm
from rbac.service.url_related import get_url

"""
主机相关逻辑
"""


def host_list(request):
	"""
	显示主机信息
	:param request:
	:return:
	"""
	# 获取所有主机信息
	host_lists = Host.objects.all()
	return render(request, "host_lists.html", {"host_lists": host_lists})


def host_add(request):
	"""
	添加主机数据
	:param request:
	:return:
	"""
	if request.method == "GET":
		form = HostForm()
		return render(request, "rbac/change.html", locals())
	# 校验传回的数据
	form = HostForm(data=request.POST)
	if form.is_valid():
		form.save()
		return redirect(get_url(request, "host_list"))
	# 如果数据校验出错
	# 将错误信息放回至前端页面
	return render(request, "rbac/change.html", {"form": form})


def host_edit(request, pk):
	"""
	用于编辑主机信息
	:param request:
	:param pk:主机信息主键
	:return:get: 返回更新界面
			post:返回错误信息或成功后host_list页面
	"""
	host_obj = Host.objects.filter(id=pk).first()
	if not host_obj:
		return HttpResponse("您访问的页面不存在 404")
	if request.method == 'GET':
		# 将已有的数据显示在input中
		form = HostForm(instance=host_obj)
		return render(request, "rbac/change.html", {"form": form})
	form = HostForm(data=request.POST, instance=host_obj)
	if not form.is_valid():
		# 校验失败
		return render(request, "rbac/change.html", {"form": form})
	# 校验成功
	form.save()
	return redirect(get_url(request, "host_list"))


def host_del(request, pk):
	"""
	用户删除--为今后所有删除页面中的a标签返回都使用同一个页面，需要在后台返回，取消的a标签路由
	:param request:
	:param pk:
	:return:
	"""
	cancel_url = get_url(request, "host_list")
	if request.method == "GET":
		return render(request, "rbac/del.html", locals())
	# 确认删除
	Host.objects.filter(id=pk).delete()
	return redirect(cancel_url)
