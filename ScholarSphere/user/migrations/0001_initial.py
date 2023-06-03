# Generated by Django 4.1 on 2023-06-03 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RealInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=10, verbose_name='名字')),
                ('phone', models.CharField(max_length=12, verbose_name='电话')),
                ('id_num', models.CharField(max_length=19, verbose_name='身份证号')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=254)),
                ('times_of_wa_password', models.IntegerField(default=0, null=True, verbose_name='一天内密码输错次数')),
                ('forbiden_start_time', models.DateTimeField(default=None, null=True, verbose_name='禁止登陆开始时间')),
                ('sevendays_autologin_start_time', models.DateTimeField(default=None, null=True, verbose_name='设置自动登录开始时间')),
                ('is_scholar', models.BooleanField(default=False)),
                ('has_real_info', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=50, verbose_name='个人简介')),
                ('url', models.CharField(max_length=200, verbose_name='个人主页的访问路由')),
                ('real_info', models.ForeignKey(db_column='real_info', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.realinformation')),
            ],
        ),
    ]
