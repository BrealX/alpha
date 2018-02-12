from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^auth/login/', views.user_login, name="login"),
    re_path(r'^auth/logout/', views.user_logout, name="logout"),
    re_path(r'^mycabinet/', views.user_cabinet, name="user_cabinet"),
]