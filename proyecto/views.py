from django.shortcuts import render, redirect  # Para renderizar plantillas y redirigir
from proyecto.models import User, Tipo  # Importa el modelo de usuario personalizado
from django.contrib import messages  # Para mostrar mensajes de error o éxito
from django.contrib.auth import authenticate, login, logout  # Funciones de autenticación
from django.contrib.auth.decorators import login_required  # Para restringir acceso a vistas protegidas
from django.contrib.auth.hashers import make_password  # Para encriptar contraseñas
from django.contrib.auth import get_user_model  # Para obtener el modelo de usuario personalizado

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
    User = get_user_model()  # Obtiene el modelo de usuario
    # Usamos select_related para obtener el tipo (rol) de los usuarios de manera eficiente
    usuarios = User.objects.select_related('tipo').all().values('id', 'first_name', 'last_name', 'username', 'email', 'is_active', 'tipo__nombre')  # Obtenemos el nombre del tipo de usuario
    # Filtramos los tipos que no sean 'root' ni 'cliente'
    roles = Tipo.objects.exclude(nombre__in=['root', 'cliente'])  # Excluye ciertos role
    return render(request, 'usuario/index.html', {'usuario': request.user, 'roles': roles, 'usuarios': usuarios,})  # Muestra la página del usuario con su información

# Vista personalizada para cerrar sesión
def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    response = redirect('custom_login')  # Redirige a la página de login
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Evita que el navegador almacene caché
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response  # Devuelve la respuesta con las cabeceras de caché desactivadas

# Decorador para requerir que el usuario esté autenticado antes de acceder a esta vista
@login_required(login_url='custom_login') 
def crear_usuario(request):
    # Verificamos si la petición es de tipo POST (cuando se envía el formulario)
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo_id = request.POST.get('rol')  # ID del rol seleccionado en el formulario

        # Validaciones básicas antes de crear el usuario

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect('vista_usuario')

        # Validar que todos los campos sean ingresados
        if not nombre or not apellido or not username or not password or not tipo_id:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('vista_usuario')

        # Intentamos obtener el tipo de usuario (rol) seleccionado
        try:
            tipo = Tipo.objects.get(id=tipo_id)
        except Tipo.DoesNotExist:
            messages.error(request, "El rol seleccionado no es válido.")
            return redirect('vista_usuario')

        # Crear el usuario con la contraseña encriptada para mayor seguridad
        user = User.objects.create(
            first_name=nombre,
            last_name=apellido,
            username=username,
            password=make_password(password),  # Encripta la contraseña antes de guardarla
            tipo=tipo  # Asigna el tipo de usuario seleccionado
        )

        # Mensaje de éxito y redirección después de crear el usuario
        messages.warning(request, "Usuario creado exitosamente.")
        return redirect('vista_usuario')

    # Si la petición es de tipo GET (cuando se carga la página del formulario)
    
    # Obtener todos los usuarios registrados en el sistema
    usuarios = User.objects.all()
    # Obtener todos los roles disponibles
    roles = Tipo.objects.all()

    # Construimos una lista de tuplas con cada usuario y su respectivo rol
    usuarios_con_rol = [(usuario, usuario.tipo.nombre if usuario.tipo else 'Sin rol') for usuario in usuarios]

    # Construimos el contexto que se pasará al template
    context = {
        'username': request.user.username,  # Nombre de usuario autenticado
        'role_name': request.user.tipo.nombre if request.user.tipo else 'Sin rol',  # Rol del usuario autenticado
        'usuarios_con_rol': usuarios_con_rol,  # Lista de usuarios con sus roles
        'roles': roles,  # Lista de roles disponibles
    }

    # Renderizamos la plantilla con el contexto
    return render(request, 'usuario/crear.html', context)
