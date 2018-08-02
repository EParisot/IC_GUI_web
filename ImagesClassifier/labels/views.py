from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os

from .forms import PhotoForm
from .models import Photo

class uploadView(View):
    
    def get(self, request):
        photos_list = Photo.objects.filter(owner=self.request.user)
        return render(self.request, 'labels/labels.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = self.request.user
            photo.file.name = photo.owner.username + '/' + photo.file.name
            photo.save()
            print(photo.owner)
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

@login_required
def rename(request, user, old, label):
    if request.method == 'POST':
        old_file = Photo.objects.get(file='media/' + user + '/' + old)
        old_name = old_file.file.name
        new_name = label + '_' + old_name.split('/')[-1].split('_')[-1]
        new_name = 'media/' + user + '/' + new_name
        old_file.title = new_name
        old_file.file.name = new_name
        old_file.save()
        os.rename(old_name, new_name)
        photos_list = Photo.objects.all()
        return render(request, 'labels/labels.html', {'photos': photos_list, 'sel': new_name})
    photos_list = Photo.objects.all()
    return render(request, 'labels/labels.html', {'photos': photos_list})

@login_required
def delete(request, user, title):
    if request.method == 'POST':
        title = 'media/' + user + '/' + title
        Photo.objects.get(file=title).delete()
        os.remove(title);
    photos_list = Photo.objects.filter(owner=request.user)
    return render(request, 'labels/labels.html', {'photos': photos_list})

@login_required
def delete_all(request):
    if request.method == 'POST':
        photos_list = Photo.objects.filter(owner=request.user)
        for item in photos_list:
            os.remove(item.file.name);
        photos_list.delete()
    return redirect('/labels/')
