"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.urls")),
    # -------------------------------------------------------------------------
    path("", views.home_page, name="home_page"),
    path("catalogue/", views.catalogueListView.as_view(), name="catalogue"),
    path('producto/<int:producto_id>/', views.producto_detail, name='producto_detail'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path("contact/", views.contact, name="contact"),
    path('contact/enviado/', views.contact_enviado, name='contact_enviado'),
    path("register/", views.register, name="register"),
    path("register/error404/", views.register_error, name="register_error404"),
    path("signin/", views.signin_user, name="signin"),
    path("logout/", views.logout_view, name="logout"),
    path("administracion/", views.administracion, name="administracion"),
    path('pago/', views.iniciar_pago, name='iniciar_pago'),
    path('pago/respuesta/', views.respuesta, name='respuesta_pago'),
    # -------------------------------------------------------------------------
    path('administracion/productos/', views.ProductoListView.as_view(), name='productos_list'),
    path('administracion/productos/create/', views.ProductoCreateView.as_view(), name='productos_create'),
    path('administracion/productos/update/<int:pk>/', views.ProductoUpdateView.as_view(), name='productos_update'),
    path('administracion/productos/delete/<int:pk>/', views.ProductoDeleteView.as_view(), name='productos_delete'),
    # -------------------------------------------------------------------------
    path('administracion/users/', views.UserListView.as_view(), name='user_list'),
    path('administracion/user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('administracion/users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('administracion/users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    # -------------------------------------------------------------------------
    path("bodeguero/", views.home_bodeguero, name="home_bodeguero"),
    path("bodeguero/productos/", views.ProductoBodegueroListView.as_view(), name="bodegueroprod_list"),
    path('bodeguero/productos/create/', views.ProductoBodegueroCreateView.as_view(), name='bodegueroprod_create'),
    path('bodeguero/productos/update/<int:pk>/', views.ProductoBodegueroUpdateView.as_view(), name='bodegueroprod_update'),
    path('bodeguero/productos/delete/<int:pk>/', views.ProductoBodegueroDeleteView.as_view(), name='bodegueroprod_delete'),
    path("bodeguero/ordenes/", views.OrderListView.as_view(), name="order_list"),
    path("bodeguero/ordenes/<int:pk>/", views.OrdenDetailView.as_view(), name="orden_detail"),
    path("bodeguero/ordenes/update/<int:pk>/", views.OrderUpdateView.as_view(), name="orden_update"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)