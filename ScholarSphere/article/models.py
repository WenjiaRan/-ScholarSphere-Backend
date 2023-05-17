from django.db import models

class Work(models.Model):
    id = models.CharField('对应作品的open_alex_id', primary_key=True, max_length=200, db_index=True, default='')
    work_name = models.CharField('论文的名字', max_length=200, db_index=True, default='')
    author_id = models.CharField('上传pdf的作者的open_alex_id', max_length=200, db_index=True, default='')
    url = models.CharField('论文的访问路由', max_length=200, null=True)
    pdf = models.FileField('文章pdf', upload_to='pdf/', default='')
    has_pdf = models.IntegerField('是否有pdf', default=1)  # -1表示没有pdf，0表示正在审核，1表示有pdf
    content = models.TextField()
    send_time = models.DateTimeField('上传时间')
    author = models.CharField('上传pdf的作者', max_length=200,  default='')
    category = models.CharField('论文分类', max_length=200, default='')