from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "rut", "email", "telefono", "direccion", "informacion_general"]
        widgets = {"informacion_general": forms.Textarea(attrs={"rows": 4})}
