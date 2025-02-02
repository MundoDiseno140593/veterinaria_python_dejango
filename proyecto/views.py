from django.shortcuts import render, redirect  # Para renderizar plantillas y redirigir
from proyecto.models import User  # Importa el modelo de usuario personalizado
from django.contrib import messages  # Para mostrar mensajes de error o éxito
from django.contrib.auth import authenticate, login, logout  # Funciones de autenticación
from django.contrib.auth.decorators import login_required  # Para restringir acceso a vistas protegidas

# Vista que renderiza la página de inicio de sesión
def vista_login(request):
    return render(request, 'Login/index.html')

    # Vista personalizada para el inicio de sesión
def custom_login(request):
    if request.method == 'POST':  # Verifica si la solicitud es POST
        username = request.POST['username']  # Obtiene el nombre de usuario del formulario
        password = request.POST['password']  # Obtiene la contraseña del formulario

        try:
            user = User.objects.get(username=username)  # Busca el usuario en la base de datos
        except User.DoesNotExist:
            user = None
            messages.error(request, 'El usuario no existe.')  # Muestra un mensaje de error
        
        if user:  # Si el usuario existe
            user_authenticated = authenticate(request, username=username, password=password)  # Autentica al usuario
            
            if user_authenticated is not None:  # Si la autenticación es exitosa
                if user_authenticated.is_active:  # Verifica si el usuario está activo
                    login(request, user_authenticated)  # Inicia sesión
                    return redirect('home')  # Redirige a la página principal
                else:
                    messages.error(request, 'Tu cuenta de usuario está inactiva.')  # Mensaje si la cuenta está inactiva
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')  # Mensaje si la autenticación falla
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')  # Mensaje si el usuario no existe
    return render(request, 'Login/index.html')  # Si la autenticación falla, vuelve a la página de login

# Vista protegida que solo permite acceso a usuarios autenticados
@login_required(login_url='custom_login')  # Si no está autenticado, redirige al login
def home(request):
    return render(request, 'home/index.html', {'usuario': request.user})  # Muestra la página de inicio con datos del usuario

# Vista protegida para la gestión de usuarios
@login_required(login_url='custom_login')  # Protege la vista para usuarios autenticados
def vista_usuario(request):
    return render(request, 'usuario/index.html', {'usuario': request.user})  # Muestra la página del usuario con su información

# Vista personalizada para cerrar sesión
def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    response = redirect('custom_login')  # Redirige a la página de login
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Evita que el navegador almacene caché
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response  # Devuelve la respuesta con las cabeceras de caché desactivadas
