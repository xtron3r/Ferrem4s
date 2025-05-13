# ---- IMPORTACIONES ----
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
)
import json

from .models import *
from .forms import EmailAuthenticationForm, ProductoForm
from .serializers import ProductoSerializer, OrderSerializer, OrderItemSerializer

from rest_framework import viewsets
from rest_framework.response import Response

# ---- VISTAS DE AUTENTICACIÓN ----

def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": UserCreationForm})
    else:
        if request.POST["registerPassword"] == request.POST["confirmPassword"]:
            if User.objects.filter(email=request.POST["registerEmail"]).exists():
                return render(
                    request,
                    "register.html",
                    {
                        "form": UserCreationForm,
                        "error": "Ya existe una cuenta con ese correo electrónico.",
                    },
                )

            try:
                user = User.objects.create_user(
                    username=request.POST["registerName"],
                    email=request.POST["registerEmail"],
                    password=request.POST["registerPassword"],
                )
                user.save()
                login(request, user)
                return redirect("home_page")

            except IntegrityError:
                return render(
                    request,
                    "register.html",
                    {
                        "form": UserCreationForm,
                        "error": "El nombre de usuario ya está en uso.",
                    },
                )

        return render(
            request,
            "register.html",
            {"form": UserCreationForm, "error": "Las contraseñas no coinciden."},
        )

def signin_user(request):
    if request.method == "GET":
        form = EmailAuthenticationForm()
        return render(request, "signin.html", {"form": form})
    elif request.method == "POST":
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home_page")
        else:
            error = "Correo o contraseña incorrectos."
        return render(request, "signin.html", {"form": form, "error": error})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home_page")

def register_error(request):
    error = "Correo ya registrado."
    return render(request, "register.html", {"error": error})


# ---- PÁGINA DE INICIO ----

def home_page(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "home-page.html", context)
# ---- quienes somos  ----

def quienes_somos(request):
    return render(request, 'quienes-somos.html')
# ---- VISTAS DE CATÁLOGO Y PRODUCTOS ----

class catalogueListView(ListView):
    model = Producto
    template_name = "catalogue.html"
    context_object_name = "productos"

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.GET.get("categoria")
        if categoria:
            queryset = queryset.filter(categoriaProducto=categoria)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]
            

        context.update({
            "items": items,
            "order": order,
            "cartItems": cartItems,
            "categoria_seleccionada": self.request.GET.get("categoria", None),
        })

        return context

@login_required
def producto_detail(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"producto": producto, "items": items, "order": order, "cartItems": cartItems}
    return render(request, "catalogue_detail.html", context)


# ---- VISTAS DE CARRITO Y PAGO ----

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)

        # Eliminar automáticamente los ítems sin producto
        order.orderitem_set.filter(producto__isnull=True).delete()

        # Filtrar solo los ítems con producto válido
        items = order.orderitem_set.filter(producto__isnull=False)

        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "cart.html", context)

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "checkout.html", context)


@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productoId = data.get("productoId")
    action = data.get("action")

    print("Action:", action)
    print("productoId:", productoId)

    user = request.user
    producto = Producto.objects.get(id=productoId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    # Obtener el OrderItem correspondiente
    orderItem, created = OrderItem.objects.get_or_create(order=order, producto=producto)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        if orderItem.quantity > 1:
            orderItem.quantity -= 1
    elif action == "delete":
        orderItem.delete()
        # No es necesario hacer save después de eliminar el item

    # Solo guarda si el item fue modificado
    if action != "delete":
        orderItem.save()

    # Obtener el nuevo estado del carrito para enviar como respuesta
    cart_items = order.orderitem_set.all()
    cart_total = order.get_cart_total
    cart_items_count = order.get_cart_items

    response_data = {
        'cartItems': cart_items_count,
        'cartTotal': cart_total,
        'items': [{'producto': item.producto.name, 'quantity': item.quantity, 'total': item.get_total} for item in cart_items]
    }

    return JsonResponse(response_data, safe=False)


# ---- VISTAS DE PAGO TRANSBANK ----

import uuid
from django.http import HttpResponseBadRequest
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType

options = WebpayOptions(
    commerce_code='597055555532',
    api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
    integration_type=IntegrationType.TEST
)

tx = Transaction(options)

def iniciar_pago(request):
    if request.method == 'POST':
        amount = int(request.POST.get('total'))
        buy_order = str(uuid.uuid4())[:26]
        session_id = str(uuid.uuid4())[:61]
        return_url = request.build_absolute_uri('respuesta_pago')

        response = tx.create(buy_order, session_id, amount, return_url)
        return redirect(f"{response['url']}?token_ws={response['token']}")

    return render(request, 'checkout.html')

@csrf_exempt
def respuesta(request):
    token = request.GET.get('token_ws') or request.POST.get('token_ws')
    if not token:
        return HttpResponseBadRequest("Token no recibido")

    response = tx.commit(token)

    if response['status'] == 'AUTHORIZED':
        return render(request, 'pago_exito.html', {'response': response})
    else:
        return render(request, 'pago_error.html', {'response': response})


# ---- VISTAS ADMINISTRACIÓN PRODUCTOS ----

@login_required
def administracion(request):
    return render(request, "admin/adminhome.html")

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "admin/productos_list.html"
    context_object_name = "productos"

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "admin/productos_form.html"

    def form_valid(self, form):
        form.save()
        return redirect("productos_list")

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = [
        "codigoProducto", "nombreProducto", "marcaProducto", "descripcionProducto",
        "precioProducto", "portadaProducto", "stockProducto", "categoriaProducto",
    ]
    template_name = "admin/productos_update.html"
    success_url = reverse_lazy("productos_list")

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "admin/productos_confirm_delete.html"
    success_url = reverse_lazy("productos_list")


# ---- VISTAS ADMINISTRACIÓN USUARIOS ----

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "admin/user_list.html"
    context_object_name = "users"

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ["username", "email", "password", "is_superuser"]
    template_name = "admin/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "admin/user_update.html"
    success_url = reverse_lazy("user_list")

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "admin/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")


# ---- VISTAS BODEGUERO ----
@login_required
def home_bodeguero(request):
    return render(request, 'bodeguero/home_bodeguero.html')

@login_required
def bodeguero_pedidos(request):
    return render(request, 'bodeguero/order_list.html')

class ProductoBodegueroListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "bodeguero/productosb_list.html"
    context_object_name = "productos"

class ProductoBodegueroCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "bodeguero/productosb_form.html"

    def form_valid(self, form):
        form.save()
        return redirect("bodegueroprod_list")

class ProductoBodegueroUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = [
        "codigoProducto", "nombreProducto", "marcaProducto", "descripcionProducto",
        "precioProducto", "portadaProducto", "stockProducto", "categoriaProducto",
    ]
    template_name = "bodeguero/productosb_update.html"
    success_url = reverse_lazy("bodegueroprod_list")

class ProductoBodegueroDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "bodeguero/productosb_confirm_delete.html"
    success_url = reverse_lazy("bodegueroprod_list")

class OrderListView(ListView):
    model = Order
    template_name = 'bodeguero/order_list.html'
    context_object_name = 'ordenes'

class OrdenDetailView(DetailView):
    model = Order
    template_name = 'bodeguero/order_detail.html'
    context_object_name = 'orden'

class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    template_name = 'bodeguero/order_detail.html'
    success_url = reverse_lazy('order_list')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order.complete = not order.complete
        order.save()
        return redirect(self.success_url)


# ---- VISTA CONTACTO / EMAIL ----

def contact(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    if request.method == "POST":
        email = request.POST.get("email")
        subject = "Mensaje de ayuda desde formulario de contacto"
        email_content = f"Email: {email}\nSolicita ayuda con el siguiente mensaje:\n{request.POST.get('message')}"
        send_mail(subject, email_content, email, ["ferr3m4s@gmail.com"], fail_silently=False)
        return HttpResponseRedirect("/contact/enviado/")

    return render(request, "contact.html", {"cartItems": cartItems})

def contact_enviado(request):
    return render(request, "contact_enviado.html")


# ---- API REST FRAMEWORK ----
class ProductoViewSett(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
