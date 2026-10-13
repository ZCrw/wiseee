from django.contrib import admin

from .models import Cotizacion, CotizacionItem


class ItemInline(admin.TabularInline):
    model = CotizacionItem
    extra = 0


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("numero", "cliente", "estado", "fecha")
    list_filter = ("estado",)
    inlines = [ItemInline]
