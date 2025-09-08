from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)    

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, blank=True)
    apellidos = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.email}"