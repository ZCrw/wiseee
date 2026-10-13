from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from clientes.models import Cliente
from contenedores.models import Contenedor
from cotizaciones.models import Cotizacion, CotizacionItem
from operaciones.models import Operacion
from vendedores.models import Vendedor

User = get_user_model()


class Command(BaseCommand):
    help = "Carga datos de demostración (solo para desarrollo)."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin1234")
            self.stdout.write("Usuario admin / admin1234 creado (cámbialo).")

        vendedores = []
        for username, nombre in [("ana", "Ana Pérez"), ("luis", "Luis Soto"), ("marta", "Marta Rojas")]:
            user, creado = User.objects.get_or_create(
                username=username,
                defaults={"first_name": nombre.split()[0], "last_name": nombre.split()[1]},
            )
            if creado:
                user.set_password("demo1234")
                user.save()
            vendedor, _ = Vendedor.objects.get_or_create(user=user)
            vendedores.append(vendedor)
        admin_user = User.objects.get(username="admin")
        Vendedor.objects.get_or_create(user=admin_user)

        if Contenedor.objects.exists():
            self.stdout.write("Ya hay datos; no se cargó nada más.")
            return

        catalogo = [
            ("Contenedor 20' estándar", "20DC", "nuevo", 4200, 15, "Coronel"),
            ("Contenedor 20' estándar", "20DC", "usado", 2600, 22, "San Antonio"),
            ("Contenedor 40' estándar", "40DC", "nuevo", 6100, 10, "Coronel"),
            ("Contenedor 40' High Cube", "40HC", "nuevo", 6900, 8, "Valparaíso"),
            ("Contenedor 40' refrigerado", "40RF", "usado", 14500, 3, "San Antonio"),
            ("Contenedor 20' Open Top", "20OT", "nuevo", 5400, 4, "Coronel"),
        ]
        contenedores = [
            Contenedor.objects.create(
                nombre=n, tipo=t, condicion=c, precio=p, stock=s, ubicacion=u
            )
            for n, t, c, p, s, u in catalogo
        ]

        nombres = [
            "Agencia Alpha", "Construcciones S.A.", "Mercado Central", "Taller Mecánico",
            "Retail Sur", "Alimentos P&R", "Servicios Globales", "Alimentos Elementos",
        ]
        clientes = [
            Cliente.objects.create(
                nombre=n, email=f"contacto{i}@ejemplo.cl", telefono=f"+56 9 5555 00{i:02d}"
            )
            for i, n in enumerate(nombres, start=1)
        ]

        hoy = timezone.localdate()
        estados_cot = ["aprobada", "pendiente", "rechazada", "pendiente", "aprobada", "pendiente"]
        for i, estado in enumerate(estados_cot):
            cot = Cotizacion.objects.create(
                cliente=clientes[i % len(clientes)],
                vendedor=vendedores[i % len(vendedores)],
                estado=estado,
                fecha=hoy - timedelta(days=i),
            )
            cont = contenedores[i % len(contenedores)]
            CotizacionItem.objects.create(
                cotizacion=cot, contenedor=cont, cantidad=1 + i % 3, precio_unitario=cont.precio
            )

        ops = [
            (0, "venta", 25, "completada"), (1, "compra", 10, "pendiente"),
            (2, "venta", 30, "completada"), (3, "compra", 5, "cancelada"),
            (4, "venta", 20, "en_proceso"),
        ]
        for idx, tipo, cantidad, estado in ops:
            Operacion.objects.create(
                cliente=clientes[idx], tipo=tipo, cantidad=cantidad, estado=estado,
                contenedor=contenedores[idx % len(contenedores)],
                vendedor=vendedores[idx % len(vendedores)],
                fecha=hoy - timedelta(days=idx),
            )
        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados."))
