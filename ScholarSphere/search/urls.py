from django.urls import path
from .views import *

urlpatterns = [
    # path('search/normalsearch', normalsearch),
    path('search/advancelsearch', advancesearch),
    path('search/get_work_pdf',get_work_pdf),
    path('search/add_work',add_work)
]