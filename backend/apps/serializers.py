from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Producto,
    Order,
    OrderItem,
    CustomUser
)
class ProductoSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Producto
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):   
    class Meta:
        model = OrderItem
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = CustomUser
        fields = "__all__"

