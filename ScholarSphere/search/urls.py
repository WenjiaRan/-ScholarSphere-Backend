from django.urls import path
from .views import *

urlpatterns = [
    path('search/normalsearch', normal_search),
    path('search/advancelsearch', advancesearch),
]