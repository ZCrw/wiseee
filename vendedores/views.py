from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from core.mixins import FormularioMixin

from .forms import VendedorCrearForm, VendedorEditarForm
from .models import Vendedor


class VendedorLista(LoginRequiredMixin, ListView):
    model = Vendedor
    template_name = "vendedores/lista.html"
    context_object_name = "vendedores"

    def get_queryset(self):
        return Vendedor.objects.select_related("user")


class VendedorCrear(FormularioMixin, CreateView):
    model = Vendedor
    form_class = VendedorCrearForm
    success_url = reverse_lazy("vendedores:lista")
    success_message = "Vendedor creado."
    titulo = "Nuevo vendedor"


class VendedorEditar(FormularioMixin, UpdateView):
    model = Vendedor
    form_class = VendedorEditarForm
    success_url = reverse_lazy("vendedores:lista")
    success_message = "Vendedor actualizado."
    titulo = "Editar vendedor"
