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
    url(r'^api/signup/$', views.api_signup, name='api_signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),

    url(r'^reset$', auth_views.password_reset, name='password_reset'),
    url(r'^reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

    #url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    #url(r'^api/profile/(?P<username>\w+)/$', views.api_profile, name='api_profile'),
    #url(r'^api/contrib/(?P<username>\w+)/$', views.api_contrib, name='api_contrib'),

    #url(r'^profile/queues/(?P<username>\w+)/$', views.profile_queues, name='profile_queues'),
    #url(r'^api/profile/queues/(?P<username>\w+)/$', views.api_profile_queues, name='api_profile_queues'),

    #url(r'^profile/edit/(?P<username>\w+)/$', views.edit_profile, name='edit_profile'),
    #url(r'^api/profile/edit/(?P<username>\w+)/$', views.api_profile_edit, name='api_profile_edit'),

    #url(r'^profile/remove/(?P<username>\w+)/$', views.remove_profile, name='remove_profile')

    ]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
