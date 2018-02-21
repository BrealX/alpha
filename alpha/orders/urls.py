from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('ajax/get_cities/', views.get_cities, name='get_cities'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout1/', views.checkout1, name='checkout1'),
    path('checkout2/', views.checkout2, name='checkout2'),
]