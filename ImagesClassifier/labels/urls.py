from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.uploadView.as_view()), name='labels'),
    path('rename/media/<old>/<label>', views.rename, name='rename'),    
    path('delete/media/<title>', views.delete, name='delete'),
    path('delete_all', views.delete_all, name='delete_all'),
]
