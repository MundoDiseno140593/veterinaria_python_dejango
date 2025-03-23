from django.urls import path 
from django.shortcuts import render 
from django.contrib.auth import logout
from django.shortcuts import redirect

def vista_login(request):
    return render(request, 'login/index.html')

def custom_login(request):
    request.method = 'POST'
    
def home(request):
    return render(request, 'home/index.html')

def vista_usuario(request):
    return render(request, 'usuario/index.html')

def custom_logout(request):
    request.method = 'POST'
    
def crear_usuario(request):
    request.method == 'POST',
    
def edit_usuario(request, user_id):
    request.method =='GET'
    
def update_usuario(request):
    request.method == 'POST',
    
def delete_usuario(request,user_id):
    request.method == 'POST',