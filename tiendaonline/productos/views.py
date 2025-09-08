from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .models import Producto, Carrito, ItemCarrito
from .serializers import ProductoSerializer, CarritoSerializer
class ProductoListCreate(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CarritoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        serializer = CarritoSerializer(carrito)
        return Response(serializer.data)

    def update(self, request, pk=None):
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        items_data = request.data.get('items', [])
        
        # Limpiar items actuales
        carrito.items.all().delete()
        
        # Crear nuevos items enviados
        for item_data in items_data:
            producto_id = item_data.get('producto')
            cantidad = item_data.get('cantidad', 1)
            try:
                producto = Producto.objects.get(id=producto_id)
                ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)
            except Producto.DoesNotExist:
                continue
        
        carrito.refresh_from_db()
        serializer = CarritoSerializer(carrito)
        return Response(serializer.data)
