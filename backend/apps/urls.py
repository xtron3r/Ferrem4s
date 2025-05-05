from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSett,
    OrderViewSet,
    OrderItemViewSet,
)

router = DefaultRouter()
router.register(r'Producto', ProductoViewSett, basename='producto')
router.register(r'Order', OrderViewSet, basename='order')
router.register(r'OrdeItem', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    *router.urls,
]