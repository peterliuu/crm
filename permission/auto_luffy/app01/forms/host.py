# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/10/27 16:00


from app01.models import Host
from rbac.myForms.base import BootstrapModelForm


class HostForm(BootstrapModelForm):
	"""
	主机校验
	"""

	class Meta:
		model = Host
		fields = "__all__"
	
	

