from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('ajax/contact/', views.contact, name='contact'),
]
