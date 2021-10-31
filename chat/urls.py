from django.contrib import admin
from django.urls import path,include
from .views import index,room,start_chat
urlpatterns = [
    path('',index,name="index"),
    path('<str:room_name>/', room, name='room'),
    path('<str:id>', start_chat, name='start_chat'),
]