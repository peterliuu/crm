from django.db import models

# Create your models here.
from rbac.models import UserInfo as RBACUserInfo
# from rbac.models import Role
"""
主机管理系统
"""


class Department(models.Model):
	"""
	部门表
	"""
	title = models.CharField(verbose_name="部门", max_length=32)
	
	def __str__(self):
		return self.title


# class UserInfo(models.Model):
# 	"""
# 	用户信息，与rbac中的用户信息结合起来，创建成一对一的关系，便于管理和避免冲突
# 	choices字段为一个二元组组成的一个可迭代对象，用来给字段提供选择项
# 	"""
# 	user = models.OneToOneField(verbose_name="用户信息", to=RBACUserInfo, on_delete=models.CASCADE)
# 	phone = models.CharField(verbose_name="手机号", max_length=32)
# 	level_choices = (
# 		(1, "T1"),
# 		(2, "T2"),
# 		(3, "T3"),
# 	)
# 	level = models.CharField(verbose_name="级别", choices=level_choices)
# 	depart = models.ForeignKey(verbose_name="关联部门", to=Department, on_delete=models.CASCADE)
#
# 	def __str__(self):
# 		return self.user.name

class UserInfo(RBACUserInfo):
	"""
	用户信息--将rbac中的UserInfo与业务表的数据结合起来，生成一张表，放置在业务中
	需要继承rbac表中的UserInfo类
	关联字段中的roles，此表在rbac中，未在业务模块中，需要将之前的关联to=“Role”变为Role，
	将其内存地址引此处
	get_xx_display  是django 为choices 写的一个内置的 现实 choice对应的value的方法
	"""
	phone = models.CharField(verbose_name="手机号", max_length=32)
	level_choices = (
		(1, "T1"),
		(2, "T2"),
		(3, "T3"),
	)
	level = models.IntegerField(verbose_name="级别", choices=level_choices)
	depart = models.ForeignKey(verbose_name="关联部门", to=Department, on_delete=models.CASCADE)
	

class Host(models.Model):
	"""
	主机信息
	"""
	hostname = models.CharField(verbose_name="主机名", max_length=32)
	ip = models.GenericIPAddressField(verbose_name="IP地址", protocol="both")
	depart = models.ForeignKey(verbose_name="关联部门", to=Department, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.hostname
