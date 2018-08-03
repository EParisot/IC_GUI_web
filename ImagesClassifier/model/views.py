from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'model/model.html')

def in_layer(request):
    return render(request, 'model/in_layer.html')

def dense_layer(request):
    return render(request, 'model/dense_layer.html')

def conv2d_layer(request):
    return render(request, 'model/conv2d_layer.html')

def dropout_layer(request):
    return render(request, 'model/dropout_layer.html')

def max_pool_layer(request):
    return render(request, 'model/max_pool_layer.html')
