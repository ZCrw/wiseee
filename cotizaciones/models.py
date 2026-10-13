from django.db import models
from django.urls import reverse
from django.utils import timezone


class Cotizacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        APROBADA = "aprobada", "Aprobada"
        RECHAZADA = "rechazada", "Rechazada"

    cliente = models.ForeignKey(
        "clientes.Cliente", on_delete=models.PROTECT, related_name="cotizaciones"
    )
    vendedor = models.ForeignKey(
        "vendedores.Vendedor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cotizaciones",
    )
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha = models.DateField(default=timezone.localdate)
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "cotización"
        verbose_name_plural = "cotizaciones"

    def __str__(self):
        return f"{self.numero} · {self.cliente}"

    @property
    def numero(self):
        return f"COT-{self.pk:04d}" if self.pk else "COT-nueva"

    @property
    def total(self):
        # usa items.all() para aprovechar prefetch_related("items")
        return sum(item.subtotal for item in self.items.all())

    @property
    def badge(self):
        return {"aprobada": "ok", "pendiente": "warn", "rechazada": "bad"}.get(self.estado, "")

    def get_absolute_url(self):
        return reverse("cotizaciones:detalle", args=[self.pk])


class CotizacionItem(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="items")
    contenedor = models.ForeignKey("contenedores.Contenedor", on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} × {self.contenedor.nombre}"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
