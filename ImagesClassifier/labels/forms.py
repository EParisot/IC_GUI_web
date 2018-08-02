from .models import Photo
from django import forms

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file',)
