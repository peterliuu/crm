from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class App01Config(AppConfig):
	name = 'app01'
	
	def ready(self):
		# from app01 import xxx
		# autodiscover_modules引用此app下的xxx模块
		autodiscover_modules("xxx")
