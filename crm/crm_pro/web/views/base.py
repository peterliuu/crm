# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/22 1:12
from django.conf import settings

from stark.service.stark_module import BaseHandler


class PermissionHandler(BaseHandler):
	"""
	所有view视图中的类继承自当前PermissionHandler，然后再继承BaseHandler
	判断当前用户的粒度控制权限信息
	所有的权限控制是携带在session中的，所有的权限判断是以url别名是否在request.session.get(settings.SESSION_KEY)中
	"""
	
	def get_add_btn(self, request, *args, **kwargs):
		"""
			粒度控制添加按钮，如果有添加权限，再去基类中判断是否有添加url
		"""
		user_permission_dict = request.session.get(settings.SESSION_KEY)
		add_name = "%s:%s" % (self.stark_obj.namespace, self.get_url_add_name)
		if add_name not in user_permission_dict:
			return None
		return super().get_add_btn(request, *args, **kwargs)
	
	def get_display_list(self, request, *args, **kwargs):
		"""
			粒度控制编辑和删除按钮，判断当前用户的权限中是否有添加或删除key值
		"""
		info = []
		if self.display_list:
			info.extend(self.display_list)
			from django.conf import settings
			user_permission_dict = request.session.get(settings.SESSION_KEY)
			edit_name = "%s:%s" % (self.stark_obj.namespace, self.get_url_edit_name)
			del_name = "%s:%s" % (self.stark_obj.namespace, self.get_url_del_name)
			if edit_name in user_permission_dict and del_name in user_permission_dict:
				info.append(type(self).display_del_edit)
			elif del_name in user_permission_dict:
				info.append(type(self).display_del)
			elif edit_name in user_permission_dict:
				info.append(type(self).display_edit)
		return info
