# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/17 20:15


def func(c):    # 闭包函数
	def inner(a, b):
		return a + b + c
	
	return inner

 
print(func(5)(1, 2))


# 装饰器
def f(fun):
	def inner():
		print("washing")
		fun()
	
	return inner


@f  # eat = f(eat)
def eat():
	print('eating')


eat()
