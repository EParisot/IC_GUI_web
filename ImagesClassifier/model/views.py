from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'model/model.html')

@login_required
def set_layer(request):
    return render(request, 'model/set_layer.html')

@login_required
def export(request, data):
    import json
    dict_data = json.loads(data)
    print(dict_data)
    if (data and dict_data != None):
        if (len(dict_data) < 4):
            return HttpResponse('Error: Not enough layers')
        if (dict_data['type'] != 'binary' and dict_data['type'] != 'categorical' and dict_data['type'] != 'multiLayerPerceptron'):
            return HttpResponse('Error: wrong type')
        else:
            if dict_data['type'] == "binary":
                dict_data['type'] = "binary_crossentropy"
            elif dict_data['type'] == "categorial":
                dict_data['type'] = "categorial_crossentropy"
            elif dict_data['type'] == "multiLayerPerceptron":
                dict_data['type'] = "mse"
        if (dict_data['optimizer'] != 'adadelta' and dict_data['optimizer'] != 'adam' and dict_data['optimizer'] != 'nadam' and dict_data['optimizer'] != 'rmsprop' and dict_data['optimizer'] != 'sgd'):
            return HttpResponse('Error: wrong optimizer')
        
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
                    if (dict_data[key]['kernel_w'] <= 0 or dict_data[key]['kernel_h'] <= 0 or dict_data[key]['stride_x'] <= 0 or dict_data[key]['stride_y'] <= 0):
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
        print(input_shape)
        for key, value in dict_data.items():
            if (key != "type" and key != "optimizer"):
                if key == "conv2d_1":
                    model.add(Conv2D(input_shape=input_shape, filters=dict_data[key]["filters"], kernel_size=(dict_data[key]["kernel_h"], dict_data[key]["kernel_w"]), strides=(dict_data[key]["stride_y"], dict_data[key]["stride_x"]), padding=dict_data[key]["padding"]))
                #elif key == "dense_1":
                #    model.add(Dense(input_shape=input_shape, units=dict_data[key]["neurons"]))
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
                    
        model.compile(optimizer=dict_data["optimizer"], loss=dict_data["type"], metrics=['accuracy'])

        model.summary()
        return HttpResponse(model.to_json())
    else:
        return HttpResponse('Error: no data')
