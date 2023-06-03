from django.urls import path
from .views import *

urlpatterns = [
    path('collection/add_to_collection', add_to_collection),
    path('collection/show_collection',show_collection)
]