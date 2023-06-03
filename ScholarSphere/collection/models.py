from django.db import models


class Collection(models.Model):
    work_id = models.CharField('对应作品的open_alex_id', max_length=200)
    user_id = models.EmailField() # 这一条收藏所属于的用户





