# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/10 19:12
from types import FunctionType

"""
通过FunctionType判断元素是否为函数

"""


def func():
	pass


print(isinstance(func, FunctionType))
print(isinstance(111, FunctionType))
