
from django.contrib import admin
from django.urls import path
from proyecto import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.vista_login),
    
    
    path('loguearse', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='logout'),
    
    path('home', views.home, name='home'),
    
    
    path('vista_usuario', views.vista_usuario, name='vista_usuario'),
    path('crear_usuario', views.crear_usuario, name='save_user'),
    path('usuarios/editar/<int:user_id>/', views.edit_usuario, name='extraerdatosusuarios'),
    path('usuarios/actualizar/', views.update_usuario, name='update_user'),
     path('usuarios/eliminar/<int:user_id>/', views.delete_usuario, name='eliminarusuarios'),
]
