# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/9 20:39


class A:
	def __init__(self, name):
		self.name = name
	
	def get_way(self):
		return self.name
	
	get_way.text = "中文"


a = A("oo")
print(a.get_way.__dict__)
print(a.get_way.text)
