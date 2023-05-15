# Generated by Django 4.2 on 2023-05-15 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_realinformation_user_real_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(default=None, max_length=50, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_scholar',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='url',
            field=models.CharField(default=None, max_length=200, null=True, verbose_name='个人主页的访问路由'),
        ),
        migrations.AlterField(
            model_name='realinformation',
            name='name',
            field=models.CharField(db_index=True, max_length=10, verbose_name='名字'),
        ),
    ]
