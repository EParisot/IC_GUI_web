from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.uploadView.as_view()), name='labels'),   
    path('delete_all', views.delete_all, name='delete_all'),
    path('crop/<crop_data>', views.crop, name='crop'),
    path('resize/<resize_data>', views.resize, name='resize'),
]
