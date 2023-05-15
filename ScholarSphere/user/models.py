from django.db import models

class RealInformation(models.Model):
    name = models.CharField('名字',max_length=10,db_index=True)
    phone = models.CharField('电话',max_length=12)
    id_num = models.CharField('身份证号',max_length=19)

class User(models.Model):
    # 基础信息
    # username = models.CharField('用户名', max_length=100, default='')
    password = models.CharField('密码', max_length=32)
    email = models.EmailField()

    # times_of_wa_password、
    times_of_wa_password = models.IntegerField('一天内密码输错次数',default=0)
    # forbiden_start_time、
    forbiden_start_time = models.DateTimeField('禁止登陆开始时间',default=None)
    # 7days_autologin_start_time
    sevendays_autologin_start_time = models.DateTimeField('设置自动登录开始时间',default=None)
    is_scholar=models.BooleanField(default=False)
    real_info = models.ForeignKey(RealInformation,on_delete=models.CASCADE,db_column='real_info',db_index=True,null=True)
    description=models.CharField('个人简介', max_length=50,default=None)
    url = models.CharField('个人主页的访问路由', max_length=200, null=True,default=None)