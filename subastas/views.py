from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

def home(request):
    return render(request, 'index.html')

def login(request):
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
                return HttpResponse('User created successfully')
            except:
                return render(request, 'login.html', {
                'form': UserCreationForm ,
                "error": 'usuario ya existe'
                })


        else:
            return render(request, 'login.html', {
                'form': UserCreationForm ,
                "error": 'password do not match'
                })
