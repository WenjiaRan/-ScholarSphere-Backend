from django.db import models
from user.models import User


# Create your models here.
class ChatInfo(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=False,related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=False,related_name='receiver')
    information = models.CharField('内容', max_length=50)
    readCheck = models.BooleanField(default=False)
    sendTime = models.DateTimeField('发送时间', default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'receiver']),
        ]
