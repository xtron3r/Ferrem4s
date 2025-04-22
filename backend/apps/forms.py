from django import forms
from .models import Libro


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
