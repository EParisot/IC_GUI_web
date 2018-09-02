#-*- coding: utf-8 -*-
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^reset$', auth_views.PasswordResetView, name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
