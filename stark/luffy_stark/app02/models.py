from django.db import models


# Create your models here.

class Host(models.Model):
	"""
	主机表
	"""
	title = models.CharField(verbose_name="主机名", max_length=32)
	ip = models.GenericIPAddressField(verbose_name="IP")
	
	def __str__(self):
		return self.title
