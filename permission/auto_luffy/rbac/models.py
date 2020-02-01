from django.db import models

"""
null--True  数据库中的数据可以为空
blank--True  Django中的admin对其操作可以为空
blank默认为false-如果在在admin中不填，则会报错This field is required.
"""


class Menu(models.Model):
	"""
		一级菜单
	"""
	title = models.CharField(verbose_name='一级菜单名', max_length=32)
	icon = models.CharField(verbose_name="图标", max_length=32)
	
	def __str__(self):
		return self.title


class Permission(models.Model):
	"""
		权限表
	"""
	title = models.CharField(verbose_name='标题', max_length=32)
	url = models.CharField(verbose_name='含正则的URL', max_length=128)
	# 添加字段-url别名
	name = models.CharField(verbose_name="url别名", max_length=32, unique=True)
	# 菜单关联字段
	menu = models.ForeignKey(verbose_name="所属菜单", max_length=32, null=True, blank=True, help_text="此字段可以为空，空为不是二级菜单",
							 on_delete=models.CASCADE, to='Menu')
	# 非菜单字段与菜单字段关联
	pid = models.ForeignKey(verbose_name="关联的权限", to="Permission", on_delete=models.CASCADE,
							null=True, blank=True, help_text="对于非菜单权限可以选择一个菜单权限作为默认值，用于默认展开和选中")
	
	def __str__(self):
		return self.title


class Role(models.Model):
	"""
	角色
	"""
	title = models.CharField(verbose_name='角色名称', max_length=32)
	permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)
	
	def __str__(self):
		return self.title


class UserInfo(models.Model):
	"""
	用户表
	"""
	name = models.CharField(verbose_name='用户名', max_length=32)
	password = models.CharField(verbose_name='密码', max_length=64)
	email = models.CharField(verbose_name='邮箱', max_length=32)
	roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)
	
	class Meta:
		# abstract = True 表明在此表中不创建UserInfo及相关联的表在rbac中
		# 此类可当做父类，被其他model类所继承
		abstract = True
	
	def __str__(self):
		return self.name
