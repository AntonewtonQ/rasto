from django.contrib import admin

from .models import PedidoAcesso


@admin.register(PedidoAcesso)
class PedidoAcessoAdmin(admin.ModelAdmin):
    """Só leitura: as decisões são da startup, pela aplicação."""

    list_display = ("criado_em", "investidor", "startup", "estado", "pontuacao", "config_versao")
    list_filter = ("estado",)
    readonly_fields = [f.name for f in PedidoAcesso._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
