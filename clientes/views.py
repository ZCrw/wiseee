from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import BorrarMixin, FormularioMixin, QueryStringMixin

from operaciones.models import Operacion

from .forms import ClienteForm
from .models import Cliente


class ClienteLista(LoginRequiredMixin, QueryStringMixin, ListView):
    model = Cliente
    template_name = "clientes/lista.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        qs = Cliente.objects.all()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) | Q(rut__icontains=q) | Q(email__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class ClienteDetalle(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "clientes/detalle.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cliente = self.object
        cotizaciones = list(cliente.cotizaciones.prefetch_related("items")[:5])
        operaciones = list(cliente.operaciones.select_related("contenedor")[:5])

        actividad = [
            {
                "titulo": f"Cotización {c.numero}",
                "detalle": c.get_estado_display(),
                "fecha": c.fecha,
                "url": c.get_absolute_url(),
            }
            for c in cotizaciones
        ] + [
            {
                "titulo": f"{o.get_tipo_display()} · {o.cantidad} u.",
                "detalle": o.get_estado_display(),
                "fecha": o.fecha,
                "url": "",
            }
            for o in operaciones
        ]
        actividad.sort(key=lambda a: a["fecha"], reverse=True)

        ctx["n_cotizaciones"] = cliente.cotizaciones.count()
        ctx["n_compras"] = cliente.operaciones.exclude(
            tipo=Operacion.Tipo.DEVOLUCION
        ).count()
        ctx["n_devoluciones"] = cliente.operaciones.filter(
            tipo=Operacion.Tipo.DEVOLUCION
        ).count()
        ctx["actividad"] = actividad[:6]
        return ctx


class ClienteCrear(FormularioMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    success_message = "Cliente creado."
    titulo = "Nuevo cliente"

    def get_success_url(self):
        return reverse_lazy("clientes:lista") if not self.object else self.object.get_absolute_url()


class ClienteEditar(FormularioMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_message = "Cliente actualizado."
    titulo = "Editar cliente"

    def get_success_url(self):
        return self.object.get_absolute_url()


class ClienteEliminar(BorrarMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy("clientes:lista")
    success_message = "Cliente eliminado."
