from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='model'),
    path('in_layer', views.in_layer, name='in_layer'),
    path('dense_layer', views.dense_layer, name='dense_layer'),
    path('conv2d_layer', views.conv2d_layer, name='conv2d_layer'),
    path('dropout_layer', views.dropout_layer, name='dropout_layer'),
    path('max_pool_layer', views.max_pool_layer, name='max_pool_layer'),
]
