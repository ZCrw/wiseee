from django.urls import path

from . import views

app_name = "vendedores"

urlpatterns = [
    path("", views.VendedorLista.as_view(), name="lista"),
    path("nuevo/", views.VendedorCrear.as_view(), name="crear"),
    path("<int:pk>/editar/", views.VendedorEditar.as_view(), name="editar"),
]
