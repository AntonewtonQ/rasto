"""O Django só serve a API (/api/v1/), a autenticação headless (/_allauth/), a saúde e o admin interno de
suporte. Os ecrãs são do Next.js (frontend/), na mesma origem através do Caddy (base técnica 1.5)."""

from django.contrib import admin
from django.urls import include, path

from rasto.nucleo import views as nucleo

handler404 = "rasto.nucleo.views.nao_encontrado"
handler500 = "rasto.nucleo.views.erro_servidor"

urlpatterns = [
    path("api/v1/", include("rasto.api.urls")),
    path("_allauth/", include("allauth.headless.urls")),
    path("saude", nucleo.saude, name="saude"),
    path("api/suporte-interno/", admin.site.urls),
]
