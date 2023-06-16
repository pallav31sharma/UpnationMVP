from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path("",home),
    path("get_phrase/<str:phrase>/",get_phrase),
    path("world_map/<str:term>/",world_map),
    path("top_conversations/<str:term>/",top_conversations),
    path("word_cloud/<str:keyword>/",word_cloud),
]