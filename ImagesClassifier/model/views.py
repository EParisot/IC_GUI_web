from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'model/model.html')

@login_required
def set_layer(request):
    return render(request, 'model/set_layer.html')
