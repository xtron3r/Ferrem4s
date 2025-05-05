from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Producto,
    Order,
    OrderItem,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


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