from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from labels.models import Photo
from django.views import View
from django.contrib.auth.decorators import login_required
from model.models import Model_file
from model.forms import ModelForm
import numpy as np
from PIL import Image
import json

@login_required
def index(request):
    photos = Photo.objects.filter(owner=request.user)
    photos_list = []
    labels_list = []
    photos_dim = []
    if len(photos) > 1:
        i = 0
        if '_' in photos[0].file.name:
            labels_list.append(photos[0].file.name.split('/')[-1].split('_')[0])  
        else:
            labels_list = []
        for image in photos:
            if '_' in image.file.name:
                if image.file.name.split('/')[-1].split('_')[0] != labels_list[i]:
                    labels_list.append(image.file.name.split('/')[-1].split('_')[0])
                    i = i + 1
            else:
                labels_list = []
            image = Image.open(image.file.name)
            image = np.array(image)
            if image.shape[2] == 4:
                photos_list.append(image[...,:3])
            elif image.shape[2] == 2:
                photos_list.append(image[...,:1])
            elif image.shape[2] == 3 or image.shape[2] == 1:
                photos_list.append(image)
        photos_list = np.array(photos_list)/255
        photos_dim = photos_list[0].shape

    model_infos = []
    model = request.GET.get('model', None)
    if model:
        from  keras.models import Sequential
        from keras.layers import Input, Conv2D, Dense, Flatten, Dropout, Activation, MaxPooling2D
        import keras.backend as K
        K.clear_session()
        from keras.models import model_from_json
        model = Model_file.objects.get(id=model)
        model_url = model.file.url[1:]
        with open(model_url) as f:
            data = f.read()
        model = model_from_json(data)
        model_dict = json.loads(data)
        model_infos = list(model.input_shape)
        if model_dict['config'][-1]['config']['activation'] == 'sigmoid':
            model_infos[0] = 2
        else:
            for layer in reversed(model_dict['config']):
                if layer['class_name'] == "Dense":
                    model_infos[0] = layer['config']['units']
                    break
        
    
    return render(request, 'train/train.html', {'photos': photos_list, 'photos_dim': photos_dim, 'labels_list': labels_list, 'model_infos': model_infos})

class uploadView(View):
    def get(self, request):
        models_list = Model_file.objects.filter(owner=self.request.user)
        return render(self.request, 'train/import.html', {'models': models_list})

    def post(self, request):
        form = ModelForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.owner = self.request.user
            model.file.name = self.request.user.username + '/' + model.file.name
            model.save()
            data = {'is_valid': True, 'name': model.file.name, 'url': model.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
