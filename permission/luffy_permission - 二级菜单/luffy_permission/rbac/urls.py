from django.conf.urls import url
from rbac.views import role, user, menu

app_name='rbac'
urlpatterns = [
    # 角色url
    url(r'^role/list/$', role.role_list, name="role_list"), # 反向解析rbac:role_list
    url(r'^role/add/$', role.role_add, name="role_add"), # rbac:role_add
    url(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name="role_edit"),  # rbac:role_edit
    url(r'^role/del/(?P<pk>\d+)/$', role.role_del, name="role_del"),  # rbac:role_del

    # 用户url
    url(r'^user/list/$', user.user_list, name="user_list"), # 反向解析rbac:user_list
    url(r'^user/add/$', user.user_add, name="user_add"), # rbac:user_add
    url(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name="user_edit"),  # rbac:user_edit
    url(r'^user/del/(?P<pk>\d+)/$', user.user_del, name="user_del"),  # rbac:user_del
    url(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name="user_reset_pwd"),  # rbac:user_reset_pwd

    # 一级菜单和权限管理url
    url(r'^menu/list/$', menu.menu_list, name="menu_list"),  # rbac:menu_list
    url(r'^menu/add/$', menu.menu_add, name="menu_add"),  # rbac:menu_add
    url(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name="menu_edit"),  # rbac:menu_edit
    url(r'^menu/del/(?P<pk>\d+)/$', menu.menu_del, name="menu_del"),  # rbac:menu_del
    # 二级菜单
    url(r'^second/menu/add/(?P<mid>\d+)/$', menu.second_menu_add, name="second_menu_add"),  # rbac:second_menu_add
    url(r'^second/menu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name="second_menu_edit"),  # rbac:second_menu_edit
    url(r'^second/menu/del/(?P<pk>\d+)/$', menu.second_menu_del, name="second_menu_del"),  # rbac:second_menu_del

    # 权限菜单
    url(r'^permission/add/(?P<second_menu_id>\d+)/$', menu.permission_add, name="permission_add"),  # rbac:permission_add
    url(r'^permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name="permission_edit"),  # rbac:permission_edit
    url(r'^permission/del/(?P<pk>\d+)/$', menu.permission_del, name="permission_del"),  # rbac:permission_del

    # 获取所有URL路由
    url(r'^multi/permissions/$', menu.multi_permissions, name="multi_permissions"),  # rbac:multi_permissions
    url(r'^multi/permissions/del/(?P<pk>\d+)/$', menu.multi_permissions_del, name="multi_permissions_del"),  # rbac:multi_permissions_del
    
    # 角色权限分配
    url(r'^distribute/permissions/$', menu.distribute_permissions, name="distribute_permissions"),  # rbac:distribute_permissions

]
