from django.urls import path
from .views import ProductoListCreate

urlpatterns = [
    path('productos/', ProductoListCreate.as_view(), name='productos-list-create'),
]
