from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^login/$', views.user_login, name="login"),
]