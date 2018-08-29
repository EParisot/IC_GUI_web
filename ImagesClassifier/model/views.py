from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
import os
import json
from .models import Model_file
from .forms import ModelForm

@login_required
def index(request):
    return render(request, 'model/model.html')

@login_required
def set_layer(request):
    return render(request, 'model/set_layer.html')

@login_required
def export(request, data):
    dict_data = json.loads(data)
    if (data and dict_data != None):
        if (len(dict_data) < 4):
            return HttpResponse('Error: Not enough layers')
        if not ('in_0' in dict_data):
            return HttpResponse('Error: first layer should be of type "In"')
        if not ('conv2d_1' in dict_data):
            return HttpResponse('Error: second layer should be of type "Conv2d"')
        try:
            dict_data['in_0']['dim_1'] = int(dict_data['in_0']['dim_1'])
            dict_data['in_0']['dim_2'] = int(dict_data['in_0']['dim_2'])
            dict_data['in_0']['dim_3'] = int(dict_data['in_0']['dim_3'])
            if (dict_data['in_0']['dim_1'] <= 0 or dict_data['in_0']['dim_2'] <= 0 or dict_data['in_0']['dim_3'] <= 0):
               return HttpResponse('Error: negative or null value in "in_0" layer') 
        except(ValueError, TypeError):
            return HttpResponse('Error: wrong value in "in_0" layer')
        for key, value in dict_data.items():
            
            if 'dense' in key:
                try:
                    dict_data[key]['neurons'] = int(dict_data[key]['neurons'])
                    if (dict_data[key]['neurons'] <= 0):
                        return HttpResponse('Error: negative or null value in ' + key + ' layer') 
                except(ValueError, TypeError):
                    return HttpResponse('Error: wrong value in '+ key +' layer')
                
            elif 'conv2d' in key:
                try:
                    dict_data[key]['filters'] = int(dict_data[key]['filters'])
                    dict_data[key]['kernel_w'] = int(dict_data[key]['kernel_w'])
                    dict_data[key]['kernel_h'] = int(dict_data[key]['kernel_h'])
                    dict_data[key]['stride_x'] = int(dict_data[key]['stride_x'])
                    dict_data[key]['stride_y'] = int(dict_data[key]['stride_y'])
                    if dict_data[key]['padding'] == '':
                        dict_data[key]['padding'] = 'valid';
                    else:
                        dict_data[key]['padding'] = 'same';
                    if (dict_data[key]['filters'] <= 0 or dict_data[key]['kernel_w'] <= 0 or dict_data[key]['kernel_h'] <= 0 or dict_data[key]['stride_x'] <= 0 or dict_data[key]['stride_y'] <= 0):
                        return HttpResponse('Error: negative or null value in ' + key + ' layer')
                except(ValueError, TypeError):
                    return HttpResponse('Error: wrong value in '+ key +' layer')
                
            elif 'flatten' in key:
                pass
            
            elif 'max_pool' in key:
                try:
                    dict_data[key]['pool_w'] = int(dict_data[key]['pool_w'])
                    dict_data[key]['pool_h'] = int(dict_data[key]['pool_h'])
                    dict_data[key]['stride_x'] = int(dict_data[key]['stride_x'])
                    dict_data[key]['stride_y'] = int(dict_data[key]['stride_y'])
                    if dict_data[key]['padding'] == '':
                        dict_data[key]['padding'] = 'valid';
                    else:
                        dict_data[key]['padding'] = 'same';
                    if (dict_data[key]['pool_w'] <= 0 or dict_data[key]['pool_h'] <= 0 or dict_data[key]['stride_x'] <= 0 or dict_data[key]['stride_y'] <= 0):
                        return HttpResponse('Error: negative or null value in ' + key + ' layer')
                except(ValueError, TypeError):
                    return HttpResponse('Error: wrong value in '+ key +' layer')
                
            elif 'dropout' in key:
                try:
                    dict_data[key]['ratio'] = round(float(dict_data[key]['ratio']), 2)
                    if (dict_data[key]['ratio'] <= 0):
                        return HttpResponse('Error: negative or null value in ' + key + ' layer')
                except(ValueError, TypeError):
                    return HttpResponse('Error: wrong value in '+ key +' layer')
            elif 'softmax' in key:
                pass
            elif 'relu' in key:
                pass
            elif 'sig' in key:
                pass
        

        from  keras.models import Sequential
        from keras.layers import Input, Conv2D, Dense, Flatten, Dropout, Activation, MaxPooling2D
        import keras.backend as K
        K.clear_session()
        
        model = Sequential()

        input_shape = (dict_data['in_0']['dim_1'], dict_data['in_0']['dim_2'], dict_data['in_0']['dim_3'])
        
        for key, value in dict_data.items():
            if (key != "type" and key != "optimizer"):
                if key == "conv2d_1":
                    model.add(Conv2D(input_shape=input_shape, filters=dict_data[key]["filters"], kernel_size=(dict_data[key]["kernel_h"], dict_data[key]["kernel_w"]), strides=(dict_data[key]["stride_y"], dict_data[key]["stride_x"]), padding=dict_data[key]["padding"]))
                elif key == "dense_1":
                    model.add(Dense(input_shape=input_shape, units=dict_data[key]["neurons"]))
                elif "conv2d" in key and key != "conv2d_1":
                    model.add(Conv2D(filters=dict_data[key]["filters"], kernel_size=(dict_data[key]["kernel_h"], dict_data[key]["kernel_w"]), strides=(dict_data[key]["stride_y"], dict_data[key]["stride_x"]), padding=dict_data[key]["padding"]))
                elif "dense" in key and key != "dense_1":
                    model.add(Dense(units=dict_data[key]["neurons"]))
                elif "flatten" in key:
                    model.add(Flatten())
                elif "max_pool" in key:
                    model.add(MaxPooling2D(pool_size=(dict_data[key]["pool_h"], dict_data[key]["pool_w"]), strides=(dict_data[key]["stride_y"], dict_data[key]["stride_x"]), padding=dict_data[key]["padding"]))
                elif "dropout" in key:
                    model.add(Dropout(dict_data[key]["ratio"]))
                elif "relu" in key:
                    model.add(Activation('relu'))
                elif "sig" in key:
                    model.add(Activation('sigmoid'))
                elif "softmax" in key:
                    model.add(Activation('softmax'))
                    
        model_json = model.to_json()

        response = HttpResponse()
        response.write("<form action='save/" + model_json + "/'><input name='name' type='text' value='myModel'><button type='submit'>Save</button></form>")
        response.write("<p>" + model_json + "</p>")

        return response
    else:
        return HttpResponse('Error: no data')

@login_required
def save(request, data):
    name = request.GET.get('name', None)
    with open("media/"+ request.user.username + '/' + name + ".json", "w") as json_file:
        json_file.write(data)

    model, created = Model_file.objects.get_or_create(owner=request.user, file="media/" + request.user.username + '/' + name + ".json")
    model.save()

    response = HttpResponse(FileWrapper(open("media/"+ request.user.username + '/' + name + ".json", 'rb')), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(name + ".json")
    #response['X-Sendfile'] = smart_str("media/" + request.user.username + "/" + name + ".json")
    return response

class uploadView(View):
    def get(self, request):
        models_list = Model_file.objects.filter(owner=self.request.user)
        return render(self.request, 'model/import.html', {'models': models_list})

    def post(self, request):
        form = ModelForm(self.request.POST, self.request.FILES)
        print(form)
        if form.is_valid():
            model = form.save(commit=False)
            model.owner = self.request.user
            model.file.name = self.request.user.username + '/' + model.file.name
            if ".json" in model.file.name:
                model.save()
                data = {'is_valid': True, 'name': model.file.name, 'url': model.file.url, 'id': model.id}
            else:
                data = {'is_valid': False}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

@login_required
def load(request):
    layers_list = []
    filename = request.GET.get('filename', None)
    return render(request, 'model/model.html', {'model': layers_list})

@login_required
def delete_model(request):
    model_id = request.GET.get('model', None)
    model = Model_file.objects.get(owner=request.user, id=model_id)
    model.delete()
    os.remove(model.file.url[1:])
    models_list = Model_file.objects.filter(owner=request.user)
    return redirect('/model/model_import', {'models': models_list})



