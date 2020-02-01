from django.db import models


# Create your models here.

class Depart(models.Model):
	"""
	部门表
	"""
	title = models.CharField(verbose_name="部门名称", max_length=32)
	
	def __str__(self):
		return self.title


class UserInfo(models.Model):
	"""
	用户表
	"""
	gender_choice = (
		(1, "男"),
		(2, "女"),
	)
	classes_choice = (
		(1, "全栈1班"),
		(2, "全栈2班"),
	)
	name = models.CharField(verbose_name="姓名", max_length=32)
	gender = models.IntegerField(verbose_name="性别", choices=gender_choice, default=1)
	classes = models.IntegerField(verbose_name="班级", choices=classes_choice, default=1)
	age = models.CharField(verbose_name="年龄", max_length=32)
	email = models.CharField(verbose_name="邮箱", max_length=32)
	depart = models.ForeignKey(verbose_name="部门", to=Depart, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name


class Deploy(models.Model):
	"""配置表"""
	status_choice = (
		(1, "在线"),
		(2, "离线"),
	)
	title = models.CharField(verbose_name='标题信息', max_length=32)
	status = models.IntegerField(verbose_name='状态信息', choices=status_choice)
	
	def __str__(self):
		return self.title
