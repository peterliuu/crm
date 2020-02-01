# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/19 21:38


def f1():
	return 5


def f2():
	return f1()
	# f1()


print(f2())
