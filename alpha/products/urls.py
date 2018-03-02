from django.urls import path, re_path, include
from . import views
from products import views

urlpatterns = [
    re_path(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
    re_path(r'^product-land/(?P<product_id>\w+)/$', views.product_land, name='product_land'),
]