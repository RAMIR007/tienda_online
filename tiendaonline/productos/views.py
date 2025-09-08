from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .models import Producto, Carrito, ItemCarrito
from .serializers import ProductoSerializer, CarritoSerializer
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generar_vale(request):
    # Información básica del usuario y fecha
    usuario = request.user
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vale_pago.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Vale de Pago")
    p.drawString(100, 780, f"Usuario: {usuario.email}")
    p.drawString(100, 760, f"Fecha: {request.GET.get('fecha', 'N/A')}")

    # Aquí puedes personalizar lo que necesites mostrar, por ejemplo:
    p.drawString(100, 740, "Detalle de compra:")
    p.drawString(120, 720, "Productos comprados, cantidades, total, etc.")

    # Por simplicidad, aquí solo mostramos texto estático.
    # Puedes extender para mostrar items reales de la compra.

    p.showPage()
    p.save()
    return response    
