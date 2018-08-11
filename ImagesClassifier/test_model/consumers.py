from channels.generic.websocket import WebsocketConsumer
from model.models import Model_file
import json
from PIL import Image
import re
from io import BytesIO
import base64

class TestConsumer(WebsocketConsumer):
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
        if model_id != None:
            from  keras.models import Sequential
            from keras.layers import Input, Conv2D, Dense, Flatten, Dropout, Activation, MaxPooling2D
            from keras.models import model_from_json
            from keras.models import load_model
            import numpy as np
            import h5py
            
            #Prepare X
            image_data = re.sub('^data:image/.+;base64,', '', text_data_json['photo'])
            X = Image.open(BytesIO(base64.b64decode(image_data)))
            X = np.array(X)/255
            if X.shape[2] == 4:
                X = X[...,:3]
            X = np.array([X])
            
            #Prepare Model
            model = Model_file.objects.get(id=model_id)
            model_url = model.file.url[1:]
            if self.model == None and '.h5' in model_url:
                self.model = load_model(model_url)

            #Predict label and send
            preds = self.model.predict(X)
            label = np.argmax(preds, axis=1)
            self.send(text_data=json.dumps({'label': str(label[0])}))
            

