from django.db import models

# Create your models here.

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
    menu = models.ForeignKey(verbose_name="所属菜单", max_length=32, null=True,
                                             blank=True, help_text="此字段可以为空，空为不是二级菜单", on_delete=models.CASCADE, to='Menu')
    # 非菜单字段与菜单字段关联
    pid = models.ForeignKey(verbose_name="关联的权限", to="Permission", on_delete=models.CASCADE,
                            null=True, blank=True, help_text="对于非菜单权限可以选择一个菜单权限作为默认值，用于默认展开和选中")

    def __str__(self):
        return self.title
