from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'model/model.html')

def set_layer(request):
    yield render(request, 'model/set_layer.html')
