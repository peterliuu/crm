**rbac组件使用说明文档**

1、将rbac组件拷贝至项目中

2、将rbac/migration目录中的数据库迁移记录删除，除___init__.py外

3、业务系统中用户表结构的设计

	rbac/models.py
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
		业务/models.py
			class UserInfo(RBACUserInfo):
				"""
				用户信息--将rbac中的UserInfo与业务表的数据结合起来，生成一张表，放置在业务中
				需要继承rbac表中的UserInfo类
				关联字段中的roles，此表在rbac中，未在业务模块中，需要将之前的关联to=“Role”变为Role，
				将其内存地址引此处
				"""
				phone = models.CharField(verbose_name="手机号", max_length=32)
				level_choices = (
					(1, "T1"),
					(2, "T2"),
					(3, "T3"),
				)
				level = models.IntegerField(verbose_name="级别", choices=level_choices)
				depart = models.ForeignKey(verbose_name="关联部门", to=Department, on_delete=models.CASCADE)

4、将业务系统中的用户表路径写到配置文件
	# 设置项目业务中的用户表
	RBAC_USER_MODEL_CLASS = "app01.models.UserInfo"
	用于在rbac分配权限时，读取业务表中的用户信息

5、业务逻辑开发
	- 将所有的路由都设置一个name值， 如：
		url('^login/$', account.login, name="login"),
	    url('^logout/$', account.logout, name="logout"),
	    url('^index/$', account.index, name="index"),
		用途：
			- 用于反向生成URL以及粒度控制（有权限显示，无权限不显示）到按钮级别的权限控制
		
6、权限的信息录入
	- 在url中添加rbac的路由分发，注意：必须设置namespace
		urlpatterns = [
   			……
		    # 权限相关
		    url("rbac/", include('rbac.urls', namespace="rbac")),
			……
		]
	- rbac提供的地址进行操作
		- .../rbac/menu/list
		- .../rbac/role/list
		- .../rbac/distribute/permissions
	- 自动发现路由中的URL时，排除的URL
		URL_EXCLUDE_LIST = [
			"/admin/.*",
			"/login/",
			"/logout/",
			"/index/",
		]

7、编写用户登录的逻辑--权限的初始化
	- 相关的配置文件:
		- 权限和菜单的session Key--settings.py
			SESSION_KEY = "luffy_permission_key"
			MENU_KEY = "menu_key"

		from django.shortcuts import render, reverse, redirect
		from app01.models import UserInfo
		from rbac.service.init_permission import init_permission

		def login(request):
			"""
			登录
			:param request:
			:return:
			"""
			if request.method == "GET":
				return render(request, "login.html")
			username = request.POST.get("user")
			pwd = request.POST.get("password")
			# 校验数据
			user_obj = UserInfo.objects.filter(name=username, password=pwd).first()
			if not user_obj:
				return render(request, "login.html", {"errmsg": "用户名或密码错误"})
			# 权限初始化,将权限及菜单信息存储进session中
			init_permission(request, user_obj)
			# 重定向回index页面
			return redirect(reverse("index"))

8、编写首页的逻辑
	def index(request):
		return render(request, "index.html")
	相关的配置：需登录但无需权限的URL
		NO_PERMISSIONS_LIST = [
			"/logout/",
			"/index/",
		]

9、通过中间件进行权限校验
	权限校验
		MIDDLEWARE = [
			……
			'rbac.middleware.rbac.RBACMiddleware'
		]
	白名单
		WHITE_LISTS = [
			"^/login/$",
			"^/admin/.*" 
		]


10、由权限对前端页面的粒度控制功能
	




总结：
	rbac组件用于在任何系统中应用权限系统

	- 用户登录 + 用户首页 + 用户注销 业务逻辑
	- 项目业务逻辑的开发
		注意：开发时灵活设置layout.html中的两个inclusion_tag
			 <div class="left-menu">
		        <div class="menu-body">
				{#   使用rbac自定义模块添加动态菜单             #}
		                {% load rbac %}
		                {% multi_menu request %}
		        </div>
		    </div>
		    <div class="right-body">
		        <div>
		            <ol class="breadcrumb no-radius no-margin" style="border-bottom: 1px solid #ddd;">
		            {#    动态显示导航数据信息           #}
		                {% show_nav request %}
		            </ol>
		        </div>
		        {% block content %} {% endblock %}
		    </div>
		- 权限信息的录入
		- 配置文件
			# 注册App
			INSTALLED_APPS = [
				……
				"app01",
				"rbac"
			]
			# 中间件的应用
			MIDDLEWARE = [
				……
				'rbac.middleware.rbac.RBACMiddleware'
			]
			# ############ 权限相关配置 ##############
			# 设置项目业务中的用户表
			RBAC_USER_MODEL_CLASS = "app01.models.UserInfo"
			# 权限在session中存储的key值
			SESSION_KEY = "luffy_permission_key"
			# 菜单在权限中存储的key值
			MENU_KEY = "menu_key"
			# 登录时白名单处理
			WHITE_LISTS = [
				"^/login/$",
				"^/admin/.*"  # 动态url页面
			]

			# 过滤url查询的白名单--便于后期修改
			URL_EXCLUDE_LIST = [
				"/admin/.*",
				"/login/",
				"/logout/",
				"/index/",
			]

			NO_PERMISSIONS_LIST = [
				"/logout/",
				"/index/",
			]






















