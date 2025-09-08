from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .models import Producto, Carrito, ItemCarrito
from .serializers import ProductoSerializer, CarritoSerializer
from reportlab.pdfgen import canvas
from django.http import FileResponse
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
    # Crear buffer para PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Datos usuario y fecha
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    nombre = perfil.nombre if perfil else ''
    apellidos = perfil.apellidos if perfil else ''
    telefono = perfil.telefono if perfil else 'No registrado'
    direccion = perfil.direccion if perfil else 'No registrada'
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Vale de Pago")
    p.setFont("Helvetica", 12)
    p.drawString(50, 770, f"Usuario: {usuario.email}")
    p.drawString(50, 750, f"Nombre: {nombre} {apellidos}")
    p.drawString(50, 730, f"Teléfono: {telefono}")
    p.drawString(50, 710, f"Dirección: {direccion}")
    p.drawString(50, 690, f"Fecha: {request.GET.get('fecha', 'N/A')}")

    # Obtener carrito con items
    try:
        carrito = Carrito.objects.get(usuario=usuario)
        items = carrito.items.all()
    except Carrito.DoesNotExist:
        items = []

    # Detalle productos en el vale
    y = 700
    total = 0
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Producto")
    p.drawString(300, y, "Cantidad")
    p.drawString(400, y, "Precio unitario")
    p.drawString(520, y, "Subtotal")
    y -= 20
    p.setFont("Helvetica", 12)

    for item in items:
        p.drawString(50, y, item.producto.nombre)
        p.drawString(300, y, str(item.cantidad))
        p.drawString(400, y, f"${item.producto.precio:.2f}")
        subtotal = item.cantidad * item.producto.precio
        p.drawString(520, y, f"${subtotal:.2f}")
        total += subtotal
        y -= 20
        if y < 100:
            p.showPage()
            y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(400, y - 20, f"Total: ${total:.2f}")

    # Cerrar y enviar PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="vale_pago.pdf")
