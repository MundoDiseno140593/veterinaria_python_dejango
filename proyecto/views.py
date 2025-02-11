from django.shortcuts import render, redirect  # Para renderizar plantillas y redirigir
from proyecto.models import User, Tipo  # Importa el modelo de usuario personalizado
from django.contrib import messages  # Para mostrar mensajes de error o éxito
from django.contrib.auth import authenticate, login, logout  # Funciones de autenticación
from django.contrib.auth.decorators import login_required  # Para restringir acceso a vistas protegidas

# Vista que renderiza la página de inicio de sesión
def vista_login(request):
    return render(request, 'Login/index.html')

    # Vista personalizada para el inicio de sesión
def custom_login(request):
    # Verifica si la solicitud HTTP es de tipo POST (enviar datos a través de un formulario)
    if request.method == 'POST':
        # Obtiene el nombre de usuario enviado desde el formulario
        username = request.POST['username']
        # Obtiene la contraseña enviada desde el formulario
        password = request.POST['password']

        try:
            # Intenta encontrar al usuario en la base de datos usando el nombre de usuario
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Si el usuario no existe en la base de datos, asigna None a la variable user
            user = None
            # Muestra un mensaje de error indicando que el usuario no existe
            messages.error(request, 'El usuario no existe.')

        # Si se encuentra un usuario con el nombre de usuario proporcionado
        if user:
            # Intenta autenticar al usuario usando el nombre de usuario y la contraseña
            user_authenticated = authenticate(request, username=username, password=password)
            
            # Si la autenticación es exitosa (es decir, se proporciona la contraseña correcta)
            if user_authenticated is not None:
                # Verifica si el usuario está activo (no está deshabilitado o bloqueado)
                if user_authenticated.is_active:
                    # Si el usuario está activo, se realiza el inicio de sesión
                    login(request, user_authenticated)
                    # Redirige al usuario a la página principal (puedes cambiar 'home' por la URL deseada)
                    return redirect('home')
                else:
                    # Si el usuario está inactivo (deshabilitado o bloqueado), muestra un mensaje de error
                    messages.error(request, 'Tu cuenta de usuario está inactiva.')
            else:
                # Si la autenticación falla (la contraseña es incorrecta), muestra un mensaje de error
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            # Si el usuario no existe en la base de datos, muestra un mensaje de error
            messages.error(request, 'Usuario o contraseña incorrectos.')

    # Si la autenticación falla o la solicitud no es POST, se vuelve a mostrar el formulario de login
    return render(request, 'Login/index.html')


# Vista protegida que solo permite acceso a usuarios autenticados
@login_required(login_url='custom_login')  # Si no está autenticado, redirige al login
def home(request):
    return render(request, 'home/index.html', {'usuario': request.user})  # Muestra la página de inicio con datos del usuario

# Vista protegida para la gestión de usuarios
@login_required(login_url='custom_login')  # Protege la vista para usuarios autenticados
def vista_usuario(request):
    # Filtramos los tipos que no sean 'root' ni 'cliente'
    tipos = Tipo.objects.exclude(nombre__in=['root', 'cliente'])  # Obtener todos los objetos de la tabla 'Tipo'
    return render(request, 'usuario/index.html', {'usuario': request.user, 'tipos': tipos})  # Muestra la página del usuario con su información

# Vista personalizada para cerrar sesión
def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    response = redirect('custom_login')  # Redirige a la página de login
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Evita que el navegador almacene caché
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response  # Devuelve la respuesta con las cabeceras de caché desactivadas
