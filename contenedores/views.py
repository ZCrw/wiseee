from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.mixins import BorrarMixin, FormularioMixin, QueryStringMixin

from .forms import ContenedorForm
from .models import Contenedor


class ContenedorLista(LoginRequiredMixin, QueryStringMixin, ListView):
    model = Contenedor
    template_name = "contenedores/lista.html"
    context_object_name = "contenedores"
    paginate_by = 10

    def get_queryset(self):
        qs = Contenedor.objects.all()
        q = self.request.GET.get("q", "").strip()
        tipo = self.request.GET.get("tipo", "")
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(ubicacion__icontains=q))
        if tipo in Contenedor.Tipo.values:
            qs = qs.filter(tipo=tipo)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["tipo"] = self.request.GET.get("tipo", "")
        ctx["tipos"] = Contenedor.Tipo.choices
        return ctx


class ContenedorCrear(FormularioMixin, CreateView):
    model = Contenedor
    form_class = ContenedorForm
    success_url = reverse_lazy("contenedores:lista")
    success_message = "Contenedor creado."
    titulo = "Nuevo contenedor"


class ContenedorEditar(FormularioMixin, UpdateView):
    model = Contenedor
    form_class = ContenedorForm
    success_url = reverse_lazy("contenedores:lista")
    success_message = "Contenedor actualizado."
    titulo = "Editar contenedor"


class ContenedorEliminar(BorrarMixin, DeleteView):
    model = Contenedor
    success_url = reverse_lazy("contenedores:lista")
    success_message = "Contenedor eliminado."
