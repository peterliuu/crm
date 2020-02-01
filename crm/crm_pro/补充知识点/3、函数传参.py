# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/10 19:51
"""
print(func(1, True, 2, 4, a=1))--以这样的形式传参不可以
	TypeError: func() got multiple values for argument 'a'
"""


def func(a, flag=True, *args, **kwargs):
	return a, flag, args, kwargs


print(func(1, True, 2, 4, **{'A': 1}))  # 可以以这样的形式
