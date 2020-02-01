# Generated by Django 2.2.5 on 2019-10-02 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_auto_20190928_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='pid',
            field=models.ForeignKey(blank=True, help_text='对于非菜单权限可以选择一个菜单权限作为默认值，用于默认展开和选中', null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='关联的权限'),
        ),
    ]
