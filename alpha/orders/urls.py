from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('ajax/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('ajax/get_chained_cities/', views.get_chained_cities, name='get_chained_cities'),
    path('ajax/order_confirm/', views.order_confirm, name='order_confirm'),
    path('ajax/order_notification/', views.order_notification, name='order_notification'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout1/', views.checkout1, name='checkout1'),
    path('checkout2/', views.checkout2, name='checkout2'),
]