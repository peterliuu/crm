# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/31 22:35
from django.urls import path

from app01 import views


class Demo:
	
	def __init__(self):
		self.register = []
	
	def get_patterns(self):
		tem_list = []
		for item in self.register:
			pattern = path('%s/' % item, views.login)
			tem_list.append(pattern)
		return tem_list
	
	@property
	def get_urls(self):
		return self.get_patterns()


demo = Demo()
