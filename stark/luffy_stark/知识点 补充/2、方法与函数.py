# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/11/10 19:14


class A:
	
	def read(self):
		print(111)
	
	def run(self):
		A.read(self)
	
	@staticmethod
	def play():
		print(222)
		
	lis = [play]
	

a = A()
A.run()
item = a.lis[0]

class B(A):
	# B().read()
	def __init__(self):
		pass
	@classmethod
	def go(cls):
		cls.play()

b = B()
print(b.go())