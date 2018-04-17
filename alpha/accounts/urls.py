from django.urls import path, re_path, include
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views

urlpatterns = [
    path('avatar/', include('avatar.urls')),
    #path('auth/login/', views.user_login, name="login"),
    #path('auth/register/', views.user_register, name="register"),
    path('auth/logout/', views.user_logout, name="logout"),
    path('my-profile/', views.my_profile, name="my_profile"),
    path('my-profile/profile/', views.user_my_profile, name="user_my_profile"),
    path('my-profile/orders/', views.user_my_orders, name="user_my_orders"),
    path('my-profile/orders/order<order_id>-info/', views.user_order_info, name="user_order_info"),
    path('my-profile/reviews/', views.user_my_reviews, name="user_my_reviews"),
    path('my-profile/add-address/', views.add_address, name="add_address"),
    path('my-profile/delete-address/', views.delete_address, name="delete_address"),
    path('my-profile/add-personal/', views.add_personal, name="add_personal"),
    path('my-profile/delete-personal/', views.delete_personal, name="delete_personal"),
    path('my-profile/delete-account/', views.delete_account, name="delete_account"),
    path('ajax/delete-review/', views.delete_review, name="delete_review"),

    # password handling urls
    path('password-change/', views.change_password, name='password_change'),
    path('password-set/', views.set_password, name='password_set'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset/done/', password_reset_done, name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', password_reset_complete, name='password_reset_complete'),

    # email handling urls
    path('accounts/email-change/', views.email_change, name='email_change'),

    # after registering new account
    #re_path(r'^registration/', views.after_registration, name="after_registration"),
    #re_path(r'^activation/(?P<activation_key>.+)/$', views.account_activation, name="account_activation"),
]
