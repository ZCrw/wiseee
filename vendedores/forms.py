from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Vendedor

User = get_user_model()


class VendedorCrearForm(forms.ModelForm):
    username = forms.CharField(label="Usuario", max_length=150)
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150, required=False)
    email = forms.EmailField(label="Correo", required=False)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    field_order = [
        "username", "first_name", "last_name", "email", "password", "telefono", "activo",
    ]

    class Meta:
        model = Vendedor
        fields = ["telefono", "activo"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ese nombre de usuario ya existe.")
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def save(self, commit=True):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data.get("last_name", ""),
            email=data.get("email", ""),
        )
        vendedor = super().save(commit=False)
        vendedor.user = user
        vendedor.save()
        return vendedor


class VendedorEditarForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150, required=False)
    email = forms.EmailField(label="Correo", required=False)

    field_order = ["first_name", "last_name", "email", "telefono", "activo"]

    class Meta:
        model = Vendedor
        fields = ["telefono", "activo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email

    def save(self, commit=True):
        vendedor = super().save(commit=commit)
        user = vendedor.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data.get("last_name", "")
        user.email = self.cleaned_data.get("email", "")
        user.save()
        return vendedor
