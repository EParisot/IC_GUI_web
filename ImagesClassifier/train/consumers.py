from channels.generic.websocket import WebsocketConsumer
from model.models import Model_file
from train.views import get_datas
import json
import sys
import os
from time import sleep

class TrainConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        import keras.backend as K
        K.clear_session()
        self.model = None

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        model_id = text_data_json['model_id']
        model_type = None
        optimizer = None
        batch_size = None
        epochs = None
        v_split = None
        e_stop = None
        patience = None
        if model_id != None:
            from  keras.models import Sequential
            from keras.layers import Input, Conv2D, Dense, Flatten, Dropout, Activation, MaxPooling2D
            from keras.models import model_from_json
            from keras.models import load_model
            import numpy as np
            import h5py
            
            #Prepare X Y
            self.user = self.scope["user"]
            data_dict = get_datas(self, False)
            X = data_dict["photos"]
            X = np.array(X)
            Y = np.array(data_dict["labels_list"])
            
            #Prepare Model
            model = Model_file.objects.get(id=model_id)
            model_url = model.file.url[1:]
            if self.model == None:    
                if '.json' in model_url:
                    with open(model_url) as f:
                        data = f.read()
                    self.model = model_from_json(data)
                    model_type = text_data_json['model_type']
                    optimizer = text_data_json['optimizer']
                    self.model.compile(optimizer=optimizer, loss=model_type, metrics=['accuracy'])
                elif '.h5' in model_url:
                    self.model = load_model(model_url)
            else:
                self.model = load_model(model_url)
            
            batch_size = int(text_data_json['batch_size'])
            epochs = int(text_data_json['epochs'])
            v_split = float(text_data_json['v_split'])
            e_stop = text_data_json['e_stop']
            patience = int(text_data_json['patience'])

            #Grab training output
            base_stdout = sys.stdout
            sys.stdout = Std_redirector(self)
        
            self.model.summary()
            
            #Train Loop
            x = 0
            while x < epochs:
               history = self.model.fit(X, Y, batch_size=batch_size, epochs=1, validation_split=v_split, verbose=1)
               x = x + 1
               for key, value in history.history.items():
                   history.history[key] = round(value[0], 2)
               #output to logs
               self.send(text_data=json.dumps({'log': json.dumps(history.history)}))
            #set output back
            sys.stdout = base_stdout

            #save model
            saved_model_path = 'media/' + self.user.username + '/' + model_url.split('/')[-1].split('.')[0] + '.h5'
            self.model.save(saved_model_path)
            saved_model, created = Model_file.objects.get_or_create(owner=self.user, file=saved_model_path)
            saved_model.save()

            
class Std_redirector(object):
    def __init__(self, cls):
        self.cls = cls

    def write(self,string):
        sleep(0.0001)
        self.cls.send(text_data=json.dumps({'output': string}))

    def flush(self):
        pass
