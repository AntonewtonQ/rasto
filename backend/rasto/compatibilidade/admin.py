from django.contrib import admin

from .models import ConfiguracaoCompatibilidade


@admin.register(ConfiguracaoCompatibilidade)
class ConfiguracaoAdmin(admin.ModelAdmin):
    """Cada alteração de pesos é uma versão nova; os pedidos guardam a versão com que foram pontuados."""

    list_display = ("versao", "activa", "peso_sector", "peso_fase", "peso_cheque", "peso_geografia", "peso_risco",
                    "limiar_compativel", "limiar_parcial")

    def has_delete_permission(self, request, obj=None):
        return False
