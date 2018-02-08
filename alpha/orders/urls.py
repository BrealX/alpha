from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^checkout/$', views.checkout, name='checkout'),
    re_path(r'^auth/$', views.auth, name='auth'),
    re_path(r'^checkout1/$', views.checkout1, name='checkout1'),
    re_path(r'^checkout2/$', views.checkout2, name='checkout2'),
]