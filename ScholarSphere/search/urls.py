from django.urls import path
from .views import *

urlpatterns = [
<<<<<<< HEAD
    # path('search/normalsearch', normalsearch),
=======
    path('search/normalsearch', normal_search),
>>>>>>> check_branch
    path('search/advancelsearch', advancesearch),
]