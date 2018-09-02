#-*- coding: utf-8 -*-
from datetime import datetime
from django.utils import timezone
from django.conf import settings

from .forms import SignUpForm, ConnexionForm
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from .serializers import UsersSerializer
import json
from .serializers import UsersSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    return render(request, 'home/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your IC_GUI Account'
            message = render_to_string('home/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'home/account_activation_sent.html')

def activate(request, uidb64, token):
    #try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    #except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #    user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'home/account_activation_invalid.html')

def log_in(request):
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                Next = request.GET.get('next', None)
                if Next:
                    if Next == '/profile/AnonymousUser/':
                        Next = '/profile/' + username
                    return redirect(Next)
                else:
                    return redirect('/')
            else: # sinon une erreur sera affichée
                error = True
                return render(request, 'home/login.html', {'form': form, 'error':error})
        else:
            form = ConnexionForm()
            Next = request.GET.get('next', None)
    else:
        form = ConnexionForm()
        Next = request.GET.get('next', None)
    return render(request, 'home/login.html', {'form': form, 'error':error, 'next': Next})

def log_out(request):
    logout(request)
    return redirect('/login/')

##@login_required
##def profile(request, username):
##    user = get_object_or_404(User, username=username)
##    current_user = request.user
##    if user != current_user:
##        user = get_object_or_404(User, username=username)
##
##    profile = Profile.objects.get(user=user)
##    level = profile.level
##
##    table = ContribTable(Contributions.objects.filter(user=user))
##    RequestConfig(request, paginate={'per_page': 10}).configure(table)
##
##    return render(request, 'home/profile.html', {'user': user, 'current_user': current_user, 'level': level, 'table': table})
##
##
##
##@login_required
##def edit_profile(request, username):
##    user = get_object_or_404(User, username=username)
##    current_user = request.user
##    if user == current_user:
##        form = SignUpForm(instance=user)
##        if request.method == 'POST':
##            form = SignUpForm(request.POST, instance=user)
##            if form.is_valid():
##                form.save()
##                return redirect('/profile/' + username)
##    else:
##        form = None
##    return render(request, 'home/edit_profile.html', {'user': user, 'form': form,})
##
##@login_required
##def remove_profile(request, username):
##    user = get_object_or_404(User, username=username)
##    current_user = request.user
##    if user == current_user:
##        user.delete()
##        return redirect('/')
##    else:
##        return redirect('/login/')

