from django import forms
from .models import Libro
from django.contrib.auth import get_user_model

User = get_user_model()



class LibroForm(forms.ModelForm):
    class Meta:
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["archivoLibro"].widget.attrs.update(
            {"accept": ".pdf, .doc, .docx, .txt"}
        )

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