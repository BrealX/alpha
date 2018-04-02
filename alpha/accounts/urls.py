from django.urls import path, re_path, include
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views

urlpatterns = [
    path('avatar/', include('avatar.urls')),
    path('auth/login/', views.user_login, name="login"),
    path('auth/register/', views.user_register, name="register"),
    path('auth/logout/', views.user_logout, name="logout"),
    path('user_dashboard/', views.user_dashboard, name="user_dashboard"),
    path('user_dashboard/my_profile/', views.user_my_profile, name="user_my_profile"),
    path('user_dashboard/my-orders/', views.user_my_orders, name="user_my_orders"),
    path('user_dashboard/my-orders/order<order_id>-info/', views.user_order_info, name="user_order_info"),
    path('user_dashboard/my-reviews/', views.user_my_reviews, name="user_my_reviews"),
    path('user_dashboard/add_address/', views.add_address, name="add_address"),
    path('user_dashboard/delete_address/', views.delete_address, name="delete_address"),
    path('user_dashboard/add_personal/', views.add_personal, name="add_personal"),
    path('user_dashboard/delete_personal/', views.delete_personal, name="delete_personal"),
    path('user_dashboard/delete_account/', views.delete_account, name="delete_account"),

    # restore password urls
    re_path(r'^password-reset/$', password_reset, name='password_reset'),
    re_path(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    re_path(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

    # after registering new account
    re_path(r'^registration/', views.after_registration, name="after_registration"),
    re_path(r'^activation/(?P<activation_key>.+)/$', views.account_activation, name="account_activation"),
]
