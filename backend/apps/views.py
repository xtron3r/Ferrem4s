from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import EmailAuthenticationForm

from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    TemplateView,
)

from .models import *
from .forms import LibroForm


# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": UserCreationForm})
    else:
        if request.POST["registerPassword"] == request.POST["confirmPassword"]:
            # Verifica si el correo ya existe
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


def register_error(request):
    error = "Correo ya registrado."
    return render(request, "register.html", {"error": error})


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
def administracion(request):
    return render(request, "admin/adminhome.html")


class LibroListView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = "admin/libros_list.html"
    context_object_name = "libros"


class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = "admin/libros_form.html"

    def form_valid(self, form):
        libro = form.save(commit=False)
        archivo_libro = self.request.FILES.get("archivoLibro")
        if archivo_libro:
            if archivo_libro.name and len(archivo_libro.name) > 100:
                archivo_libro.name = archivo_libro.name[:100]
            libro.archivoLibro = archivo_libro
        libro.save()
        return redirect("libros_list")


class LibroUpdateView(LoginRequiredMixin, UpdateView):
    model = Libro
    fields = [
        "tituloLibro",
        "autorLibro",
        "anioLibro",
        "descripcionLibro",
        "precioLibro",
        "digital",
        "portadaLibro",
        "archivoLibro",
    ]
    template_name = "admin/libros_update.html"
    success_url = reverse_lazy("libros_list")


class LibroDeleteView(LoginRequiredMixin, DeleteView):
    model = Libro
    template_name = "admin/libros_confirm_delete.html"
    success_url = reverse_lazy("libros_list")


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
        password = form.cleaned_data["password"]
        user.set_password(password)
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


@login_required
def logout_view(request):
    logout(request)
    return redirect("home_page")


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


class catalogueListView(ListView):
    model = Libro
    template_name = "catalogue.html"
    context_object_name = "libros"

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

        context["items"] = items
        context["order"] = order
        context["cartItems"] = cartItems

        return context


@login_required
def libro_detail(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"libro": libro, "items": items, "order": order, "cartItems": cartItems}
    return render(request, "catalogue_detail.html", context)


def cart(request):
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
    libroId = data.get("libroId")
    action = data.get("action")

    print("Action:", action)
    print("libroId:", libroId)

    user = request.user
    libro = Libro.objects.get(id=libroId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, libro=libro)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
    elif action == "delete":
        orderItem.quantity = orderItem.quantity == 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


# ! Configuracion Email

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def contact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = "Recuperación Contraseña"
        email_content = f"Email: {email}\nSolicita recuperación de contraseña."

        send_mail(
            subject, email_content, email, ["@duocuc.cl"], fail_silently=False
        )

        return HttpResponseRedirect("/contact/enviado/")

    return render(request, "contact.html")


def contact_enviado(request):
    return render(request, "contact_enviado.html")


# -------------------------------------------------------------------------------


from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Libro, Order, OrderItem, TarjetaCompra
from django.contrib.auth.models import User
from .serializers import (
    LibroSerializer,
    OrderSerializer,
    OrderItemSerializer,
    TarjetaCompraSerializer,
)

# Create your views here.
class LibroViewSett(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class TarjetaCompraViewSet(viewsets.ModelViewSet):
    queryset = TarjetaCompra.objects.all()
    serializer_class = TarjetaCompraSerializer

