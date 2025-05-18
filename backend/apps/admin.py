from django.contrib import admin
from .models import (
    CustomUser,
    Producto,
    Order,
    OrderItem,
)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Producto)
admin.site.register(Order)
admin.site.register(OrderItem)
