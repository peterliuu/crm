# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/1 17:21
import copy

d = {1: [1], 2: 2}
# 1 字典为可变数据类型，修改字典中的值，另一个随之改变
d1 = d
d1[1].append(2)

# 2 浅拷贝 拷贝父对象，不会拷贝对象的内部的子对象。
d2 = d.copy()  # {1: 2, 2: 2}
d2[1].append(3)
print(d2)
print(d)

# 3 深拷贝  copy 模块的 deepcopy 方法，完全拷贝了父对象及其子对象。
d3 = copy.deepcopy(d)
d3[1].append(4)
print(d3)
print(d)
