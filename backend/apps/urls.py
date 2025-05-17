from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSett,
    OrderViewSet,
    OrderItemViewSet,
)

router = DefaultRouter()
router.register(r'Producto', ProductoViewSett, basename='producto')
router.register(r'Orden', OrderViewSet, basename='carrito')
router.register(r'CarritoItem', OrderItemViewSet, basename='carritoitem')

urlpatterns = [
    *router.urls,
]