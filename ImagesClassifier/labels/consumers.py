from channels.generic.websocket import WebsocketConsumer
from labels.models import Photo
import json
import sys
import os

class LabelsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope["user"]

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        err = None
        new_name = None
        text_data_json = json.loads(text_data)
        old = text_data_json['old']
        label = text_data_json['label']
        #rename
        if label != 'null':
            old_file = Photo.objects.filter(owner=self.user, file=old)
            if len(old_file) > 0:
                old_name = old_file[0].file.name
                new_name = label + '_' + old_name.split('/')[-1].split('_')[-1]
                new_name = 'media/' + self.user.username + '/' + new_name
                old_file.title = new_name
                old_file[0].file.name = new_name
                old_file[0].save()
                try:
                    if len(old_file) > 1:
                        i = 1
                        while i < len(old_file):
                            os.remove(old_file[i].file.name)
                            i = i + 1
                    os.rename(old_name, new_name)
                except Exception as e:
                    err = str(e)
            self.send(text_data=json.dumps({'old': old, 'new': new_name, 'label': label, 'count': None, 'err': err}))
        #delete
        else:
            photos_list = []
            elem_list = Photo.objects.filter(owner=self.user, file=old)
            for elem in elem_list:
                elem.delete()
                try:
                    os.remove(elem.file.name);
                except Exception as e:
                    err = str(e)
                photos_list = Photo.objects.filter(owner=self.user)
            self.send(text_data=json.dumps({'old': old, 'new': new_name, 'label': label, 'count': len(photos_list), 'err': err}))
