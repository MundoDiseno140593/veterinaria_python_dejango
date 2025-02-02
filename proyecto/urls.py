from django.urls import path 
from django.shortcuts import render 

def vista_login(request):
    return render(request, 'login/index.html')

def custom_login(request):
    request.method = 'POST'
    
def home(request):
    return render(request, 'home/index.html')

def vista_usuario(request):
    return render(request, 'usuario/index.html')