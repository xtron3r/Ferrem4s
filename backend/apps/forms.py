from django import forms
from .models import Producto
from django.contrib.auth import get_user_model

User = get_user_model()



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "codigoProducto",
            "nombreProducto",
            "marcaProducto",
            "descripcionProducto",
            "precioProducto",
            "portadaProducto",
            "stockProducto",
            "categoriaProducto",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# AUTENTICACION POR CORREO
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError("Correo o contraseña incorrectos")
            self.user = user
        except User.DoesNotExist:
            raise forms.ValidationError("Correo o contraseña incorrectos")

        return cleaned_data

    def get_user(self):
        return self.user