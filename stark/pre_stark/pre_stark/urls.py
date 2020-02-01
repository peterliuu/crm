"""pre_stark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demo import demo
from app01 import views

print("路由即将被加载至内存中")
"""
def include(arg, namespace=None):
    urlconf_module = arg
    urlconf_module = import_module(urlconf_module) == import urlconf_module
    return (urlconf_module, app_name, namespace)
"""
# 调用app中的urls方式1：
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('web/', include("app01.urls")),
# ]

# 方式2 将调用的include方法的返回值直接传入
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('web/', ("app01.urls", None, None)),  第一个参数是urls文件对象，通过此对象可以获取urls.pattrens获取分发的路由
# ]
"""
def url_patterns(self):
    如果urlconf_module.urlpatterns存在，则调用
    否则：调用自身数据
    令urlconf_module为一个列表，将路由放置在列表中，省去调用步骤
    patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
    return patterns
"""
# 方式3 直接传参


# urlpatterns = [
# 	path('admin/', admin.site.urls),
# 	path('web/', ([
# 					  path('login/', views.login),
# 					  path('index/', views.index),
# 				  ], None, None)),
# ]

# 示例：
print(demo.register)
print(demo.get_urls)
# 获取url中的数据通过单例模式+include+url执行前获取数据
urlpatterns = [
	path('web/', (demo.get_urls, None, None)),
]
