from django.urls import path, re_path, include
from . import views
from products import views

urlpatterns = [
#    re_path(r'^', views.landing, name='landing'),
    re_path(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
]