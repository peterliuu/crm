# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/4 20:36

from django.shortcuts import HttpResponse
from django.urls import re_path

from app02 import models
from stark.service.stark_module import site, BaseHandler


class HostHandler(BaseHandler):
	"""
	自定制的处理数据类，可以自由增添数据
	"""
	def detail_view(self, request):
		return HttpResponse("detail.....")
	
	@property
	def get_url_detail_name(self):
		return self.get_url_name("detail")
	
	def extra_url(self):
		extra = [
			re_path('^detail/$', self.detail_view, name=self.get_url_detail_name)
		]
		return extra


site.register(models.Host, HostHandler, prev="private")
site.register(models.Host, HostHandler)






