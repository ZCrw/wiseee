from django import forms

from .models import Contenedor


class ContenedorForm(forms.ModelForm):
    class Meta:
        model = Contenedor
        fields = ["nombre", "tipo", "condicion", "precio", "stock", "ubicacion", "descripcion", "activo"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}
