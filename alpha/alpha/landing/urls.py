from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^landing/', views.landing, name='landing'),
]