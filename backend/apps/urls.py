from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSett,
    OrderViewSet,
    OrderItemViewSet,
    UserViewSet
)

router = DefaultRouter()
router.register(r'Producto', ProductoViewSett, basename='producto')
router.register(r'Orden', OrderViewSet, basename='carrito')
router.register(r'CarritoItem', OrderItemViewSet, basename='carritoitem')
router.register(r'Usuario', UserViewSet, basename='usuario')

urlpatterns = [
    *router.urls,
]