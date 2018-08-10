from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from labels.models import Photo
from django.views import View
from django.contrib.auth.decorators import login_required
from model.models import Model_file
from model.forms import ModelForm
from keras.models import load_model
import pandas as pd
import numpy as np
from PIL import Image
import json
import random


def get_datas(request, get_model):
    import keras.backend as K
    K.clear_session()
    #Query images
    photos = Photo.objects.filter(owner=request.user)
    photos_list = []
    labels_list = []
    labels_nb = ""
    photos_dim = []
    model_id = None
    model_infos = None
    if len(photos) > 1:
        #parse labels
        if '_' in photos[0].file.name:
            labels_nb = 1
            labels_list.append(photos[0].file.name.split('/')[-1].split('_')[0])  
        else:
            labels_list = []
            return render(self.request, 'train/train.html')
        for image in photos:
            if '_' in image.file.name:
                if image.file.name.split('/')[-1].split('_')[0] not in labels_list:
                    labels_nb = labels_nb + 1
                labels_list.append(image.file.name.split('/')[-1].split('_')[0])
            else:
                labels_list = []
                return render(self.request, 'train/train.html')
            #open image
            image = Image.open(image.file.name)
            image = np.array(image)/255
            if image.shape[2] == 4:
                photos_list.append(image[...,:3])
            elif image.shape[2] == 2:
                photos_list.append(image[...,:1])
            elif image.shape[2] == 3 or image.shape[2] == 1:
                photos_list.append(image)
        labels_list = np.array(pd.get_dummies(labels_list))
        photos_dim = photos_list[0].shape
        # Shuffle images and labels
        zipped_list = list(zip(photos_list, labels_list))
        random.shuffle(zipped_list)
        photos_list, labels_list = zip(*zipped_list)
    #parse model
    if get_model == True:
        model_infos = []
        model_id = request.GET.get('model', None)
        if model_id != None:
            model = Model_file.objects.get(id=model_id)
            model_url = model.file.url[1:]
            
            if '.json' in model_url:
                with open(model_url) as f:
                    data = f.read()
                    model_dict = json.loads(data)
            elif '.h5' in model_url:
                data = load_model(model_url)
                model_dict = json.loads(data.to_json())
            
            model_infos = model_dict['config'][0]['config']['batch_input_shape']
            if model_dict['config'][-1]['config']['activation'] == 'sigmoid' and model_dict['config'][-2]['class_name'] == "Dense" and model_dict['config'][-2]['config']['units'] == 1:
                model_infos[0] = 2
                model_infos.append(0)
            elif model_dict['config'][-1]['config']['activation'] == 'softmax' and model_dict['config'][-2]['class_name'] == "Dense":
                model_infos[0] = model_dict['config'][-2]['config']['units']
                model_infos.append(1)
            else:
                return render(self.request, 'train/train.html')
    return {'photos': photos_list, 'photos_dim': photos_dim, 'labels_list': labels_list, 'labels_nb': labels_nb, 'model_id': model_id, 'model_infos': model_infos}

@login_required
def index(request):
    data_dict = get_datas(request, True)            
    return render(request, 'train/train.html', data_dict)
    
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
            data = {'is_valid': True, 'name': model.file.name, 'url': model.file.url, 'id': model.id}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
