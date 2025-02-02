from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.

def vista_login(request):
    return render(request, 'Login/index.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            user = None
            messages.error(request, 'usuario no existe')
            
        if user:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Tu cuenta de Usuario esta inactivo')
            else:
                messages.error(request, 'usuario no existe con esas credenciales.')
        else:
            messages.error(request, 'usuario o Contraseña es incorrecta')
            
    return render(request, 'Login/index.html')

def home(request):
    return render(request, 'home/index.html')