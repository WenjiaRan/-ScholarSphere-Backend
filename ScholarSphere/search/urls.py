from django.urls import path
from .views import *

urlpatterns = [
    # path('search/normalsearch', normalsearch),
    path('search/advancelsearch', advancesearch),
]