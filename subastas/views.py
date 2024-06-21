from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login
from django.http import HttpResponse
from django.db import IntegrityError

def home(request):
    return render(request, 'index.html')

def loginP(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': UserCreationForm()
        })
    else:
        try:
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
        except MultiValueDictKeyError:
            return HttpResponse('Please complete all fields.', status=400)

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password2)
                user.save()
                login(request, user)
                return redirect('perfil')
            except IntegrityError:
                return render(request, 'login.html', {
                'form': UserCreationForm ,
                "error": 'usuario ya existe'
                })


        else:
            return render(request, 'login.html', {
                'form': UserCreationForm ,
                "error": 'password do not match'
                })

def perfil (request):
    return render(request, 'perfil.html')