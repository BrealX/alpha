from django.urls import path, re_path, include
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views

urlpatterns = [
    re_path(r'^auth/login/', views.user_login, name="login"),
    re_path(r'^auth/logout/', views.user_logout, name="logout"),
    re_path(r'^mycabinet/', views.user_cabinet, name="user_cabinet"),

    # restore password urls
	re_path(r'^password-reset/$', password_reset, name='password_reset'),
	re_path(r'^password-reset/done/$', password_reset_done, name='password_reset_done'),
	re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
	re_path(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),

	# after registering new account
	re_path(r'^registration/', views.after_registration, name="after_registration"),
	re_path(r'^activation/(?P<activation_key>.+)/$', views.account_activation, name="account_activation"),		
]