from django.urls import path, re_path, include
from . import views
from products import views

urlpatterns = [
    re_path(r'^product-land/(?P<product_id>\w+)/$', views.product_land, name='product_land'),
    path('ajax/contact/', views.contact, name='contact'),
]