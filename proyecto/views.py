from django.shortcuts import render, redirect
from proyecto.models import User  # Asegúrate de usar tu modelo personalizado
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

def vista_login(request):
    return render(request, 'Login/index.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            messages.error(request, 'El usuario no existe.')
        
        if user:  # Si el usuario fue encontrado
            # Ahora autenticamos al usuario
            user_authenticated = authenticate(request, username=username, password=password)
            
            if user_authenticated is not None:
                if user_authenticated.is_active:
                    login(request, user_authenticated)  # Iniciar sesión con el usuario autenticado
                    return redirect('home')  # Redirige a la página de inicio
                else:
                    messages.error(request, 'Tu cuenta de usuario está inactiva.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'Login/index.html')

def home(request):
    return render(request, 'home/index.html', {'usuario': request.user})

@login_required
def vista_usuario(request):
    return render(request, 'usuario/index.html', {'usuario': request.user})