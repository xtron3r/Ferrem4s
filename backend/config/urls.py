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
    path('libro/<int:libro_id>/', views.libro_detail, name='libro_detail'),
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
    # -------------------------------------------------------------------------
    path('administracion/libros/', views.LibroListView.as_view(), name='libros_list'),
    path('administracion/libros/create/', views.LibroCreateView.as_view(), name='libros_create'),
    path('administracion/libros/update/<int:pk>/', views.LibroUpdateView.as_view(), name='libros_update'),
    path('administracion/libros/delete/<int:pk>/', views.LibroDeleteView.as_view(), name='libros_delete'),
    # -------------------------------------------------------------------------
    path('administracion/users/', views.UserListView.as_view(), name='user_list'),
    path('administracion/user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('administracion/users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('administracion/users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)