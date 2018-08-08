from channels.generic.websocket import WebsocketConsumer
from model.models import Model_file
from train.views import get_datas
import json
import sys

class TrainConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

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
            import keras.backend as K
            from keras.models import model_from_json

            import numpy as np
            import pandas as pd
            import random
            
            #Prepare X Y
            self.user = self.scope["user"]
            data_dict = get_datas(self, False)
            X = data_dict["photos"]
            Y = data_dict["labels_list"]

            # Shuffle images and labels
            zipped_list = list(zip(X, Y))
            random.shuffle(zipped_list)
            X, Y = zip(*zipped_list)
            
            X = np.array(X)/255
            Y = np.array(pd.get_dummies(Y))
            
            #Prepare Model
            K.clear_session()
            model = Model_file.objects.get(id=model_id)
            model_url = model.file.url[1:]
            with open(model_url) as f:
                data = f.read()
            model = model_from_json(data)
            model_type = text_data_json['model_type']
            optimizer = text_data_json['optimizer']
            batch_size = int(text_data_json['batch_size'])
            epochs = int(text_data_json['epochs'])
            v_split = float(text_data_json['v_split'])
            e_stop = text_data_json['e_stop']
            patience = int(text_data_json['patience'])

            model.compile(optimizer=optimizer, loss=model_type, metrics=['accuracy'])

            #Grab training output
            base_stdout = sys.stdout
            sys.stdout = Std_redirector(self)
        
            model.summary()
            
            #Train Loop
            x = 0
            while x < epochs:
               history = model.fit(X, Y, batch_size=batch_size, epochs=1, validation_split=v_split, verbose=1)
               x = x + 1
               for key, value in history.history.items():
                   history.history[key] = round(value[0], 2)
               #output to logs
               self.send(text_data=json.dumps({'log': json.dumps(history.history)}))
            #set output back
            sys.stdout = base_stdout
            
            #save model
            #import h5py
            
class Std_redirector(object):
    def __init__(self, cls):
        self.cls = cls

    def write(self,string):
        self.cls.send(text_data=json.dumps({'output': string}))

    def flush(self):
        pass
