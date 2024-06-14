from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
def home(request):
    return render (request,'index.html')

def login(request):
    if request.method == 'GET ':
        return render(request, 'login.html', {
            'form': UserCreationForm
        })
    else :
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password2'])
                user.save()
                return HttpResponse('user created succerssfully')
            except:
                return HttpResponse('username already xists')
        return HttpResponse('password do nor match')
