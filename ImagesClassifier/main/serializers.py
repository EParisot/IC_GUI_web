# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



