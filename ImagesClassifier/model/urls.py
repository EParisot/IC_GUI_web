from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.index, name='model'),
    path('set_layer', views.set_layer, name='set_layer'),
    path('export/<data>', views.export, name='export'),
    path('export/save/<data>/', views.save, name='save'),
    path('model_import', login_required(views.uploadView.as_view()), name='model_import'),
    path('load', views.load, name='load'),
    path('delete/', views.delete_model, name='delete'),
]
