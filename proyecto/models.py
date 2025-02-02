from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Tipo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
class User(AbstractUser):
    # Aquí ya no importamos Tipo directamente
    tipo = models.ForeignKey('proyecto.Tipo', on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self):
        return f"{self.username} - {self.tipo.nombre if self.tipo else 'Sin rol'}"