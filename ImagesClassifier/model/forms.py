from .models import Model_file
from django import forms

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model_file
        fields = ('file',)
