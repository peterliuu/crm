# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/23 13:33
"""
通过函数内存地址(对象)获取到函数实际的名称__name__
"""


def func():
	pass


print(func.__name__)
print(func)

