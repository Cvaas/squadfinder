from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuario
class CustomUser(AbstractUser):
    gamertag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.gamertag

# Juego 
class Game(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    imagen = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre

#  Solicitud (Squad)
class SquadRequest(models.Model):
    # Relaciones 
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    juego = models.ForeignKey(Game, on_delete=models.CASCADE)
    # Datos 
    rango_requerido = models.CharField(max_length=50)
    usa_microfono = models.BooleanField(default=True)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return self.usuario.gamertag