from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login, logout, authenticate
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
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                login(request, user)
                return redirect('perfil')
            else:
                try:
                    user = User.objects.create_user(username=username, password=password2)
                    user.save()
                    login(request, user)
                    return redirect('perfil')
                except IntegrityError:
                    return render(request, 'login.html', {
                        'form': UserCreationForm(),
                        'error': 'El usuario ya existe'
                    })
        else:
            return render(request, 'login.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden'
            })

def perfil(request):
    return render(request, 'perfil.html')

def signout(request):
    logout(request)
    return redirect('home')
def signin(request):
    if request.method == 'GET' :
        return render (request, 'signin.html',{
        'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm(),
                'error': 'usuario incorrecto'
            })
        else:
            login(request,user)
            return redirect('perfil')

        