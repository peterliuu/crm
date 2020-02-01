# Generated by Django 2.2.5 on 2019-12-21 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='一级菜单名')),
                ('icon', models.CharField(max_length=32, verbose_name='图标')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('url', models.CharField(max_length=128, verbose_name='含正则的URL')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='url别名')),
                ('menu', models.ForeignKey(blank=True, help_text='此字段可以为空，空为不是二级菜单', max_length=32, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='所属菜单')),
                ('pid', models.ForeignKey(blank=True, help_text='对于非菜单权限可以选择一个菜单权限作为默认值，用于默认展开和选中', null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='关联的权限')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='角色名称')),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='拥有的所有权限')),
            ],
        ),
    ]
