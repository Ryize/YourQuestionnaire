from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('create_poll/', create_poll, name='create_poll'),
]
