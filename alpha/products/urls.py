from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^product-land/(?P<product_id>\w+)/$', views.product_land, name='product_land'),
    re_path(r'^api/product-land/(?P<product_id>\w+)/like/$', views.ProductLikeAPIToggle.as_view(), name='like-api-toggle'),
]