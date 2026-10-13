from django import forms

from .models import Operacion


class OperacionForm(forms.ModelForm):
    class Meta:
        model = Operacion
        fields = ["cliente", "tipo", "contenedor", "cantidad", "estado", "fecha", "notas"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "notas": forms.Textarea(attrs={"rows": 3}),
        }
