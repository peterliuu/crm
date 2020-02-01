# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/8 17:59


class A:
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return self.name


a = A("alex")
a1 = A("alex")
print(str(a))

print(type(a))
"""
将对象循环使用字符拼接
方式1：
	将对象变为字符串 str(obj)
	print('-'.join(str(a)))
方式2：
	将对象变为可迭代对象
	# def __iter__(self):
	# 	return iter(self.name)
	print('-'.join(a))
"""


