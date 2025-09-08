from django.urls import path
from .views import ProductoListCreate, CarritoViewSet, generar_vale, PerfilUsuarioView,

carrito_list = CarritoViewSet.as_view({'get': 'list', 'put': 'update'})

urlpatterns = [
    path('productos/', ProductoListCreate.as_view(), name='productos-list-create'),
    path('carrito/', carrito_list, name='carrito'),
    path('vale/', generar_vale, name='generar-vale'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),
    
]