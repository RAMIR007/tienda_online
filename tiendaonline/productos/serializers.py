from rest_framework import serializers
from .models import Producto, Carrito, ItemCarrito, PerfilUsuario

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        
class ItemCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrito
        fields = '__all__'
        
class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True)

    class Meta:
        model = Carrito
        fields = ['usuario', 'items']        
        
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre', 'apellidos', 'telefono', 'direccion']        
