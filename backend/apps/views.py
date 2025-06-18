# ---- IMPORTACIONES ----
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

import requests


from .models import *
from .forms import EmailAuthenticationForm, ProductoForm
from .serializers import ProductoSerializer, OrderSerializer, OrderItemSerializer, UserSerializer

from rest_framework import viewsets, status 
from rest_framework.response import Response

User = get_user_model()

# ---- VISTAS DE AUTENTICACIÓN ----

@csrf_exempt
def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": UserCreationForm})

    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "JSON inválido"}, status=400)
        else:
            data = request.POST

        # Extraer datos
        email = data.get("registerEmail", "").strip()
        password = data.get("registerPassword", "").strip()
        confirm_password = data.get("confirmPassword", "").strip()
        name = data.get("registerName", "").strip()
        last_name = data.get("registerLastName", "").strip()
        phone = data.get("registerPhone", "").strip()

        # Validar campos vacíos
        if not all([email, password, confirm_password, name, last_name, phone]):
            error_msg = "Todos los campos son obligatorios."
            if request.content_type == "application/json":
                return JsonResponse({"error": error_msg}, status=400)
            return render(request, "register.html", {"form": UserCreationForm, "error": error_msg})

        if password != confirm_password:
            error_msg = "Las contraseñas no coinciden."
            if request.content_type == "application/json":
                return JsonResponse({"error": error_msg}, status=400)
            return render(request, "register.html", {"form": UserCreationForm, "error": error_msg})

        if User.objects.filter(email=email).exists():
            error_msg = "Ya existe una cuenta con ese correo electrónico."
            if request.content_type == "application/json":
                return JsonResponse({"error": error_msg}, status=400)
            return render(request, "register.html", {"form": UserCreationForm, "error": error_msg})

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name,
                last_name=last_name
            )

            user.telefono = phone
            user.rol = "usuario"
            user.save()

            login(request, user)

            if request.content_type == "application/json":
                return JsonResponse({
                    "mensaje": "Usuario registrado correctamente.",
                    "usuario": user.username,
                    "rol": user.rol
                }, status=201)

            if user.rol == "bodeguero":
                return redirect("bodeguero_home")
            else:
                return redirect("home_page")

        except IntegrityError:
            error_msg = "El nombre de usuario ya está en uso."
            if request.content_type == "application/json":
                return JsonResponse({"error": error_msg}, status=400)
            return render(request, "register.html", {"form": UserCreationForm, "error": error_msg})

@csrf_exempt
def signin_user(request):
    if request.method == "GET":
        form = EmailAuthenticationForm()
        return render(request, "signin.html", {"form": form})
    
    elif request.method == "POST":
        # Si la solicitud tiene JSON (Postman o API)
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                form = EmailAuthenticationForm(data=data)
            except json.JSONDecodeError:
                return JsonResponse({"error": "JSON inválido"}, status=400)
        else:
            form = EmailAuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if request.content_type == "application/json":
                return JsonResponse({
                    "rol": user.rol,
                    "user": user.username,
                    "mensaje": "Usuario autenticado correctamente.",
                    "id_sesion": request.session.session_key
                })

            if user.rol == "bodeguero":
                return redirect("home_bodeguero")
            else:
                return redirect("home_page")
        else:

            error = "Correo o contraseña incorrectos."

            if request.content_type == "application/json":
                return JsonResponse({"error": error}, status=401)

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
        order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
        if not order:
            order = Order.objects.create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "home-page.html", context)

@login_required
def historial_compras(request):
    if request.user.is_authenticated:
        user = request.user

        order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
        if not order:
            order = Order.objects.create(user=user, complete=False)

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    
    ordenes = Order.objects.filter(
            user=user,
            transaction_id__isnull=False
        ).exclude(transaction_id='').exclude(complete=False).order_by('-date_ordered')

    context = {
        'ordenes': ordenes,       
        'items': items,           
        'order': order,           
        'cartItems': cartItems,   
    }

    return render(request, 'historial_compras.html', context)

class OrdenDetailUsuarioView(DetailView):
    model = Order
    template_name = 'historial_compras_detalle.html'
    context_object_name = 'orden'

# ---- QUIENES SOMOS  ----

def quienes_somos(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
        if not order:
            order = Order.objects.create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "quienes-somos.html", context)


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
            order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
            if not order:
                order = Order.objects.create(user=user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
            cartItems = order["get_cart_items"]

        # Llamada a la API para obtener dólar
        try:
            url = (
                "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?"
                "user=gib.beiza@duocuc.cl&pass=Gucho2847%3F"
                "&timeseries=F073.TCO.PRE.Z.D&function=GetSeries"
            )
            response = requests.get(url)
            data = response.json()

            observaciones = data.get("Series", {}).get("Obs", [])
            if observaciones:
                # Reemplazo coma por punto para float correcto
                ultimo_valor_str = observaciones[-1]["value"].replace(',', '.')
                ultimo_valor = float(ultimo_valor_str)  # Valor dólar float
                fecha_valor = observaciones[-1]["indexDateString"]
            else:
                ultimo_valor = None
                fecha_valor = None
        except Exception as e:
            ultimo_valor = None
            fecha_valor = None

        productos = context.get("productos")
        if ultimo_valor and productos:
            for producto in productos:
                try:
                    producto.precio_usd = round(producto.precioProducto / ultimo_valor, 2)
                except Exception:
                    producto.precio_usd = None
        else:
            if productos:
                for producto in productos:
                    producto.precio_usd = None

        context.update({
            "items": items,
            "order": order,
            "cartItems": cartItems,
            "categoria_seleccionada": self.request.GET.get("categoria", None),
            "dolar": ultimo_valor,
            "fecha_dolar": fecha_valor,
            "productos": productos,  # actualizado con precio_usd
        })

        return context

@login_required
def producto_detail(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
        if not order:
            order = Order.objects.create(user=user, complete=False)
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
        order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
        if not order:
            order = Order.objects.create(user=user, complete=False)

        order.orderitem_set.filter(producto__isnull=True).delete()

        items = order.orderitem_set.filter(producto__isnull=False)

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}

    if request.headers.get('Accept') == 'application/json':
        def serialize_item(item):
            return {
                "producto_id": item.producto.id,
                "nombre": item.producto.nombreProducto,
                "cantidad": item.quantity,
                "precio_unitario": item.producto.precioProducto,
                "subtotal": item.quantity * item.producto.precioProducto,
            }

        items_data = [serialize_item(i) for i in items] if request.user.is_authenticated else []

        data = {
            "items": items_data,
            "order": {
                "Total_carrito": order.get_cart_total if request.user.is_authenticated else 0,
                "items_carrito": cartItems,
                "Comprando": getattr(order, 'shipping', False) if request.user.is_authenticated else False,
            },
        }
        return JsonResponse(data, safe=False)

    return render(request, "cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
        if not order:
            order = Order.objects.create(user=user, complete=False)
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
    action = data.get("action").strip()

    print("Action:", action)
    print("productoId:", productoId)

    user = request.user
    if not user.is_authenticated:
        return JsonResponse("Usuario no autenticado", status=401, safe=False)
    
    producto = Producto.objects.get(id=productoId)
    order = Order.objects.filter(user=user, complete=False).order_by('-date_ordered').first()
    if not order:
        order = Order.objects.create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, producto=producto)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        if orderItem.quantity > 1:
            orderItem.quantity = orderItem.quantity - 1
            
    elif action == "delete":
        orderItem.delete()
        return JsonResponse("Producto eliminado correctamente", safe=False)
    
    if action != "delete":
        orderItem.save()

    return JsonResponse("Producto añadido correctamente", safe=False)


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
        region = request.POST.get('region')
        comuna = request.POST.get('comuna')
        direccion = request.POST.get('direccion')

        # Buscar orden incompleta
        order = Order.objects.filter(user=request.user, complete=False).order_by('-date_ordered').first()

        if not order:
            messages.error(request, "No se encontró una orden para pagar.")
            return redirect('checkout')

        amount = int(request.POST.get('total'))
        buy_order = str(uuid.uuid4())[:26]
        session_id = str(uuid.uuid4())[:61]
        return_url = request.build_absolute_uri('/pago/respuesta/')

        order.region = region
        order.comuna = comuna
        order.direccion = direccion
        order.date_ordered = timezone.now()
        order.save()


        response = tx.create(buy_order, session_id, amount, return_url)
        return redirect(f"{response['url']}?token_ws={response['token']}")
        
    return redirect('checkout')

@csrf_exempt
def respuesta(request):
    token = request.GET.get('token_ws') or request.POST.get('token_ws')
    if not token:
        messages.error(request, "Token no recibido.")
        return redirect('checkout')

    response = tx.commit(token)

    if response['status'] == 'AUTHORIZED':
        # Buscar la orden incompleta más reciente del usuario
        order = Order.objects.filter(user=request.user, complete=False).order_by('-date_ordered').first()

        if not order:
            return render(request, 'pago_error.html', {'response': response, 'error': 'No se encontró una orden válida.'})
        
        order.complete = True
        order.transaction_id = response['buy_order']
        order.estado = 'pagado'
        order.date_ordered = timezone.now()
        order.save()

        # Actualizar el stock de los productos
        for item in order.orderitem_set.all():
            producto = item.producto
            producto.stockProducto -= item.quantity
            producto.save()

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
    fields = ["email", "first_name", "last_name", "rol", "telefono", "password", "is_superuser"]
    template_name = "admin/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        password = self.request.POST.get("password")
        confirm_password = self.request.POST.get("confirm_password")
        rol = self.request.POST.get("rol")
        first_name = self.request.POST.get("first_name")

        if password != confirm_password:
            return render(self.request, self.template_name, {"form": form, "error": "Las contraseñas no coinciden."})
        
        user = form.save(commit=False)
        user.username = first_name.lower()
        user.set_password(form.cleaned_data["password"])

        if rol == "admin":
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

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

class OrderAdminListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'admin/admin_ordenes.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        return Order.objects.annotate(num_items=Count('orderitem')).filter(
            estado__in=['pagado', 'despachado', 'entregado'],
            num_items__gt=0,
            transaction_id__isnull=False
        ).exclude(
            transaction_id=''
        )

class OrdenAdminDetailView(DetailView):
    model = Order
    template_name = 'admin/admin_ordenes_detail.html'
    context_object_name = 'orden'

class OrderAdminUpdateView(UpdateView):
    model = Order
    fields = []
    template_name = 'admin/admin_ordenes_detail.html'
    success_url = reverse_lazy('orden_adm_list')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        nuevo_estado = request.POST.get('nuevo_estado')

        if nuevo_estado in ['pagado', 'despachado', 'entregado']:
            order.estado = nuevo_estado
            order.save()

        return redirect(self.success_url)



# ---- VISTAS BODEGUERO ----
@login_required
def home_bodeguero(request):
    if request.user.rol != 'bodeguero':
        return redirect('home_page')
    return render(request, 'bodeguero/home_bodeguero.html')

@login_required
def bodeguero_pedidos(request):
    if request.user.rol != 'bodeguero':
        return redirect('home_page')
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

class OrderBodegueroListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'bodeguero/order_list.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        return Order.objects.annotate(num_items=Count('orderitem')).filter(
            estado__in=['pagado', 'despachado', 'entregado'],
            num_items__gt=0,
            transaction_id__isnull=False
        ).exclude(
            transaction_id=''
        )

class OrdenBodegueroDetailView(DetailView):
    model = Order
    template_name = 'bodeguero/order_detail.html'
    context_object_name = 'orden'

class OrderBodegueroUpdateView(UpdateView):
    model = Order
    fields = []
    template_name = 'bodeguero/order_detail.html'
    success_url = reverse_lazy('order_list')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        nuevo_estado = request.POST.get('nuevo_estado')

        if nuevo_estado in ['pagado', 'despachado', 'entregado']:
            order.estado = nuevo_estado
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "mensaje": "Producto creado correctamente",
            "producto": serializer.data
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response({"mensaje": "Producto eliminado correctamente"}, status=200)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Permite PATCH o PUT
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "mensaje": "Producto actualizado correctamente",
            "producto": serializer.data
        }, status=status.HTTP_200_OK)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'mensaje': 'Orden creada correctamente',
            'orden': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'mensaje': 'Orden actualizada correctamente',
            'orden': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'mensaje': 'Orden eliminada correctamente'
        }, status=status.HTTP_204_NO_CONTENT)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer