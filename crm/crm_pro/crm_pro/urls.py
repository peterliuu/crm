"""crm_pro URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from stark.service.stark_module import site
from web.views import account

urlpatterns = [
	path('admin/', admin.site.urls),
	path('stark/', site.urls),
	url("rbac/", include('rbac.urls', namespace="rbac")),
	# 添加登录等基础路由信息
	path('login/', account.login, name='login'),
	path('logout/', account.logout, name='logout'),
	path('index/', account.index, name='index'),
]
