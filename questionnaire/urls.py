from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('create_poll/', create_poll, name='create_poll'),
    path('create_question/', create_question, name='create_question'),
    path('create_answer/', create_answer, name='create_answer'),
    path('my_polls/', my_poll, name='my_poll'),
    path('take_poll/<int:poll_id>', take_poll, name='take_poll'),
]
