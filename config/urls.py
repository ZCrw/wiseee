from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("core.urls")),
    path("clientes/", include("clientes.urls")),
    path("cotizaciones/", include("cotizaciones.urls")),
    path("contenedores/", include("contenedores.urls")),
    path("compras/", include("operaciones.urls")),
    path("vendedores/", include("vendedores.urls")),
]
