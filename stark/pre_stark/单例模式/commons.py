# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/29 22:06
"""
在python中，如果导入过得文件再次被导入时，python不会重新解释一遍，而是从内存中直接将原来导入的值拿来使用
"""
from 单例模式 import utils

print(utils.f)  # <单例模式.utils.Foo object at 0x00000264D80CE648>

from 单例模式 import utils

print(utils.f)  # <单例模式.utils.Foo object at 0x00000154499E5308>

from 单例模式 import app


