from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from clientes.models import Cliente
from cotizaciones.models import Cotizacion
from operaciones.models import Operacion
from vendedores.models import Vendedor


@login_required
def dashboard(request):
    total_cot = Cotizacion.objects.count()

    def pct(n):
        return round(n * 100 / total_cot) if total_cot else 0

    def fila(estado, etiqueta, icono, tono):
        n = Cotizacion.objects.filter(estado=estado).count()
        return {"estado": estado, "etiqueta": etiqueta, "n": n, "pct": pct(n), "icono": icono, "tono": tono}

    resumen = [
        fila(Cotizacion.Estado.APROBADA, "Aprobadas", "file-text", "indigo"),
        fila(Cotizacion.Estado.RECHAZADA, "Rechazadas", "check", "green"),
        fila(Cotizacion.Estado.PENDIENTE, "Pendientes", "clock", "amber"),
    ]

    recientes = (
        Cotizacion.objects.select_related("cliente").prefetch_related("items")[:4]
    )

    solicitudes = Operacion.objects.select_related("cliente")
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "")
    if q:
        solicitudes = solicitudes.filter(
            Q(cliente__nombre__icontains=q) | Q(cliente__rut__icontains=q)
        )
    if estado in Operacion.Estado.values:
        solicitudes = solicitudes.filter(estado=estado)

    return render(
        request,
        "core/dashboard.html",
        {
            "clientes_total": Cliente.objects.count(),
            "cotizaciones_abiertas": Cotizacion.objects.filter(
                estado=Cotizacion.Estado.PENDIENTE
            ).count(),
            "compras_registradas": Operacion.objects.exclude(
                tipo=Operacion.Tipo.DEVOLUCION
            ).count(),
            "vendedores_activos": Vendedor.objects.filter(activo=True).count(),
            "resumen": resumen,
            "recientes": recientes,
            "solicitudes": solicitudes[:8],
            "q": q,
            "estado": estado,
            "estados": Operacion.Estado.choices,
        },
    )
