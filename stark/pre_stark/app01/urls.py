# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/29 23:13
from django.urls import path

from app01 import views

urlpatterns = [
	path('login/', views.login),
	path('index/', views.index),
]
