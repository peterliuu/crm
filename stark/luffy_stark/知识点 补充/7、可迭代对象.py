# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/25 23:02
"""
正常形况下对象是不可迭代的
for item in a:  # 'A' object is not iterable
	print(item)

如果一个类中定义了__iter__方法且该方法返回一个迭代器，那么就称该实例化的对象为可迭代对象
生成器是一种特殊的迭代器
"""


class A:
	
	def __init__(self, db_list):
		self.db = db_list
	
	def __iter__(self):
		print(type(iter(self.db)))
		print(next(iter(self.db)))
		return iter(self.db)
		# yield 1


a = A([1, 2, 3])
print(a.db)
# for item in a:  # 在此处a使用了__iter__方法，数据变为[1,2,3] a-->可迭代对象
# 	print(item)

# print(type(a.__iter__()))
from collections import Iterator
print(next(a.__iter__()))
print(isinstance(a.__iter__(), Iterator))
