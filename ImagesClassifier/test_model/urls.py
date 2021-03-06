from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_import', login_required(views.uploadView.as_view()), name='test_import'),
    path('delete/', views.delete_model, name='delete'),
]
