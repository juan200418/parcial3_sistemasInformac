from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
def home(request):
    tareas = Task.objects.all()
    return render(request, 'index.html', {'task': tareas})

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
    user_tasks = Task.objects.filter(user=request.user)
    all_tasks = Task.objects.all()
    return render(request, 'perfil.html', {'user_tasks': user_tasks, 'all_tasks': all_tasks})

@login_required
def crate_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm()  # Instancia del formulario para enviar al template
        })
    else:
        try:
            form = TaskForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES para manejar archivos
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect('perfil')
            else:
                return render(request, 'create_task.html', {
                    'form': TaskForm(),  # Instancia del formulario con errores para enviar al template
                    'error': 'Por favor, proporciona datos válidos.'
                })
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': 'Ha ocurrido un error. Por favor, intenta nuevamente.'
            })
@login_required
def eliminar_tarea(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('perfil')
    return render(request, 'eliminar_tarea.html', {'task': task})

@login_required
def editar_tarea(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = TaskForm(instance=task)
    return render(request, 'editar_tarea.html', {'form': form, 'task': task})

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