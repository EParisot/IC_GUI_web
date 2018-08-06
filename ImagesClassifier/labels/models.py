from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
