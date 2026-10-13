from django.urls import path

from . import views

app_name = "operaciones"

urlpatterns = [
    path("", views.OperacionLista.as_view(), name="lista"),
    path("nueva/", views.OperacionCrear.as_view(), name="crear"),
    path("<int:pk>/editar/", views.OperacionEditar.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.OperacionEliminar.as_view(), name="eliminar"),
]
