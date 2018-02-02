from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^checkout/$', views.checkout, name='checkout'),

]