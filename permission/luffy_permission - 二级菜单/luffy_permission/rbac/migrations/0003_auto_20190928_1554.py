# Generated by Django 2.2.5 on 2019-09-28 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_permission_is_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='图标'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='is_menu',
            field=models.BooleanField(default=True, verbose_name='是否为菜单'),
        ),
    ]
