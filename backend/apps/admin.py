from django.contrib import admin
from .models import (
    Producto,
    Order,
    OrderItem,
)

# Register your models here.
admin.site.register(Producto)
admin.site.register(Order)
admin.site.register(OrderItem)
