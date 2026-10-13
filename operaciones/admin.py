from django.contrib import admin

from .models import Operacion


@admin.register(Operacion)
class OperacionAdmin(admin.ModelAdmin):
    list_display = ("cliente", "tipo", "cantidad", "estado", "fecha")
    list_filter = ("tipo", "estado")
