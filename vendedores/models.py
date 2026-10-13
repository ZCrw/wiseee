from django.conf import settings
from django.db import models


class Vendedor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendedor"
    )
    telefono = models.CharField("Teléfono", max_length=30, blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user__first_name", "user__username"]
        verbose_name_plural = "vendedores"

    def __str__(self):
        return self.user.get_full_name() or self.user.username
