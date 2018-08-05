from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='model'),
    path('set_layer', views.set_layer, name='set_layer'),
    path('export/<data>', views.export, name='export'),
]
