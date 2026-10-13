# SpaceWise

Plataforma Django para gestionar clientes, cotizaciones, compras y contenedores.

## Puesta en marcha

```bash
python -m venv venv
venv\Scripts\activate        # Windows  (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt

python manage.py makemigrations clientes contenedores vendedores cotizaciones operaciones
python manage.py migrate
python manage.py seed          # opcional: datos de demo + usuario admin / admin1234
python manage.py runserver
```

Abre http://127.0.0.1:8000/ e inicia sesión (con `seed`: `admin` / `admin1234`; cámbiala).
Sin `seed`, crea tu usuario con `python manage.py createsuperuser`.

## Módulos

| Ruta             | Qué hace                                                             |
|------------------|----------------------------------------------------------------------|
| `/`              | Dashboard con totales, resumen de cotizaciones y últimas solicitudes |
| `/clientes/`     | CRUD + detalle con historial y actividad                             |
| `/cotizaciones/` | Cotizaciones con varios contenedores; aprobar/rechazar               |
| `/compras/`      | Ventas, compras y devoluciones                                       |
| `/contenedores/` | Catálogo con precio y stock                                          |
| `/vendedores/`   | Equipo comercial (cada vendedor es un usuario)                       |
| `/admin/`        | Panel de administración de Django                                    |

Al **aprobar** una cotización se crea automáticamente una compra pendiente por cada contenedor cotizado.
