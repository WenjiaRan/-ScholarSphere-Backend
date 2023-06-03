from django.urls import path
from .views import *

urlpatterns = [
    path('chat/sendinfo',send_info),
    path('chat/historyinfo',history_info),
    path('chat/checknewinfo',check_new_info),
    path('chat/userreadinfo',user_read_info),
]