from django.db import models
from django.utils import timezone


class Operacion(models.Model):
    class Tipo(models.TextChoices):
        VENTA = "venta", "Venta"
        COMPRA = "compra", "Compra"
        DEVOLUCION = "devolucion", "Devolución"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PROCESO = "en_proceso", "En proceso"
        COMPLETADA = "completada", "Completada"
        CANCELADA = "cancelada", "Cancelada"

    cliente = models.ForeignKey(
        "clientes.Cliente", on_delete=models.PROTECT, related_name="operaciones"
    )
    tipo = models.CharField(max_length=12, choices=Tipo.choices, default=Tipo.VENTA)
    contenedor = models.ForeignKey(
        "contenedores.Contenedor", on_delete=models.SET_NULL, null=True, blank=True
    )
    cotizacion = models.ForeignKey(
        "cotizaciones.Cotizacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operaciones",
    )
    vendedor = models.ForeignKey(
        "vendedores.Vendedor", on_delete=models.SET_NULL, null=True, blank=True
    )
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha = models.DateField(default=timezone.localdate)
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "operación"
        verbose_name_plural = "operaciones"

    def __str__(self):
        return f"{self.get_tipo_display()} · {self.cliente} · {self.cantidad}"

    @property
    def badge(self):
        return {
            "completada": "ok",
            "pendiente": "warn",
            "cancelada": "bad",
            "en_proceso": "info",
        }.get(self.estado, "")
