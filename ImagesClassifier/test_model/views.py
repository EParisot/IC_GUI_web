from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from model.models import Model_file
from model.forms import ModelForm
from PIL import Image
import json
import os

@login_required
def index(request):
    model_id = None
    model_infos = None
    if request.GET.get('model', None):
        model_id = request.GET.get('model', None)
        model = Model_file.objects.get(id=model_id)
        from keras.models import load_model
        import keras.backend as K
        K.clear_session()
        model_url = model.file.url[1:]
        if model != None and '.h5' in model_url:
            model = load_model(model_url)
        else:
            return render(request, 'test/test.html', {'model_id': model_id, 'model_infos': model_infos})
        model_infos = json.loads(model.to_json())
        model_infos = model_infos['config'][0]['config']['batch_input_shape']
        del model
    return render(request, 'test/test.html', {'model_id': model_id, 'model_infos': model_infos})

class uploadView(View):
    def get(self, request):
        models_list = Model_file.objects.filter(owner=self.request.user)
        return render(self.request, 'test/import.html', {'models': models_list})

    def post(self, request):
        form = ModelForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.owner = self.request.user
            model.file.name = self.request.user.username + '/' + model.file.name
            if ".h5" in model.file.name:
                model.save()
                data = {'is_valid': True, 'name': model.file.name, 'url': model.file.url, 'id': model.id}
            else:
                data = {'is_valid': False}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

@login_required
def delete_model(request):
    model_id = request.GET.get('model', None)
    model = Model_file.objects.get(owner=request.user, id=model_id)
    model.delete()
    os.remove(model.file.url[1:])
    models_list = Model_file.objects.filter(owner=request.user)
    return redirect('/test_model/test_import', {'models': models_list})
