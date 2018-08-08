from django.db import models
from django.contrib.auth.models import User

class Model_file(models.Model):
    title = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User, related_name='model', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    settings = models.CharField(max_length=255, blank=True)
