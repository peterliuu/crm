**rbac组件使用说明文档**

1、将rbac组件拷贝至项目中

2、将rbac/migration目录中的数据库迁移记录删除，除___init__.py外

3、业务系统中用户表结构的设计


3、进行业务开发
	3.1 对于用户表使用 OneToOne 将用户表拆分到两张表中，如：
		业务/models.py
			class UserInfo(models.Model):
				user = models.OneToOneField(verbose_name="用户信息", to=RBACUserInfo, on_delete=models.CASCADE)
				phone = models.CharField(verbose_name="手机号", max_length=32)
				level_choices = (
					(1, "T1"),
					(2, "T2"),
					(3, "T3"),
				)
				level = models.CharField(verbose_name="级别", choices=level_choices)
				depart = models.ForeignKey(verbose_name="关联部门", to=Department, on_delete=models.CASCADE)
		rbac/models.py
			class UserInfo(models.Model):
				name = models.CharField(verbose_name='用户名', max_length=32)
				password = models.CharField(verbose_name='密码', max_length=64)
				email = models.CharField(verbose_name='邮箱', max_length=32)
				roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)
		缺点：
			- 用户数据分散
		优点：
			- 利用上rbac中的用户管理的功能：
		
	3.2 用户表整合在一张表中--推荐
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
		优点：
			- 将所有用户信息放到一张表中(业务的用户表中)
		缺点：	
			- 原rbac中的所有关于用户表的操作无法使用，需重新构建
		
		注意：原rbac中的两处使用了用户表
			- 用户管理 [删除] 将url的数据进行注释
			- 权限分配时的用户列表 [需要读取业务中的业务表表名]

	3.3 业务开发
		操作前提：
			- 注释权限相关的校验信息
			- 将模板信息layout.html文件放到rbac模板中
			- 将之前项目的static目录下的内容放置在rbac静态文件中
			
		- 用户表的增删改查
		- 主机表的增删改查
		
		开发中的问题点：主要是用户及主机的代码冗余过多，需要将其放置到stark组件中--后续
		
		
4 权限的应用
	
	4.1 将菜单及导航条添加到layout.html中
		<div class="menu-body">
		{#   使用rbac自定义模块添加动态菜单             #}
                {% load rbac %}
                {% multi_menu request %}
        </div>
        <div>
            <ol class="breadcrumb no-radius no-margin" style="border-bottom: 1px solid #ddd;">
            {#    动态显示导航数据信息           #}
                {% show_nav request %}
            </ol>
        </div>
	
	4.2 配置权限的中间件settings.py中
		MIDDLEWARE = [
				.....
				'rbac.middleware.rbac.RBACMiddleware'
			]
	
	4.3 白名单配置 在settings.py中
		# 白名单处理
		WHITE_LISTS = [
			"^/login/$",
			"^/admin/.*"  # 动态url页面
		]	
		
	4.4 权限的初始化
		SESSION_KEY = "luffy_permission_key"
		MENU_KEY = "menu_key"
		
	4.5 在批量操作权限时，自动发现路由中的所有URL，需要忽略的配置
		URL_EXCLUDE_LIST = [
				"/admin/.*",
				"/login/"
			]
	
	4.6 用户登录的逻辑
		- 用户完成逻辑登录，对于 /index/ /login/ /logout/ 是否分配权限？
			方案1 ：
				将 /index/ /logout/ 录入数据库，以后给每个用户都分配此权限
			方案2 ：
				默认用户登录，皆可访问 /index/ /logout/ 页面
				
				解决思路：
					- 将 /index/ /login/ /logout/ 从权限分配中取消显示  settings中配置
					- 将 /index/ /logout/ 在初始化时放入登录，但不添加的权限中，在settings中设置
						- 在rbac中间件验证时校验对应的url
						- 在返回前增加--防止在页面显示时rbac/templatetags/rbac.py页面的inclusion_tag无法找到数据
							request.menu_record = menu_record
							request.judgement_info = None
						
		
		
		
		
		
		
		
		
		

