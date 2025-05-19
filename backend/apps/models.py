from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('usuario', 'Usuario'),
        ('bodeguero', 'Bodeguero')
    ]
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
    telefono = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username','rol']

    def __str__(self):
        return self.first_name



class Producto(models.Model):
    codigoProducto = models.CharField(max_length=200, null=True, blank=True, unique=True)
    nombreProducto = models.CharField(max_length=200, null=True, blank=True)
    marcaProducto = models.CharField(max_length=200, null=True, blank=True)
    descripcionProducto = models.CharField(max_length=1000, null=True, blank=True)
    precioProducto = models.PositiveIntegerField()
    stockProducto = models.PositiveIntegerField(default=0)
    categoriaProducto = models.CharField(max_length=200, null=True, blank=True)
    portadaProducto = models.ImageField(upload_to="images/", null=True, blank=True)
    requiere_envio = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreProducto

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"


class Order(models.Model):
    ESTADOS = [
        ('carrito', 'Carrito activo'),
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pagado'),
        ('despachado', 'Despachado'),
        ('entregado', 'Entregado'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='carrito')
    region = models.CharField(max_length=100, null=True, blank=True)
    comuna = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.filter(producto__isnull=False)
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.filter(producto__isnull=False)
        total = sum([item.quantity for item in orderitems])
        return total
    class Meta:
        verbose_name = "orden"
        verbose_name_plural = "ordenes"


class OrderItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.producto.precioProducto * self.quantity
        return total

    def __str__(self):
        return f'{self.producto.nombreProducto} ({self.quantity})'

    class Meta:
        verbose_name = "item de orden"
        verbose_name_plural = "items de orden"