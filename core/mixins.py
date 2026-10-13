from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect


class QueryStringMixin:
    """Expone `qs` (querystring sin 'page') para conservar filtros al paginar."""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["qs"] = params.urlencode()
        return ctx


class FormularioMixin(LoginRequiredMixin, SuccessMessageMixin):
    """Crear/editar con plantilla genérica form.html."""

    template_name = "form.html"
    titulo = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = self.titulo
        ctx["cancel_url"] = self.get_success_url()
        return ctx


class BorrarMixin(LoginRequiredMixin, SuccessMessageMixin):
    template_name = "confirm_delete.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cancel_url"] = self.get_success_url()
        return ctx

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "No se puede eliminar: tiene registros asociados (cotizaciones o compras).",
            )
            return redirect(self.get_success_url())
