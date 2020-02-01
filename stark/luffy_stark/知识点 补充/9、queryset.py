# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/1 23:25

from django.http import QueryDict

q = QueryDict()
q._mutable = True
q.setlist(1, [1, 2])  # 可以为querySet集合设置列表值
q.get(1)   # 获取请求中的某个值
q.getlist(1)   # 获取请求中的数据列表


