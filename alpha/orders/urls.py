from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^basket_adding/$', views.basket_adding, name='basket_adding'),
]