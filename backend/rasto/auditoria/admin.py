from django.contrib import admin

from .models import RegistoAuditoria


@admin.register(RegistoAuditoria)
class RegistoAuditoriaAdmin(admin.ModelAdmin):
    """Só leitura: o registo é só de acréscimo (a base de dados também o impõe)."""

    list_display = ("id", "criado_em", "actor_descricao", "accao", "objecto_tipo", "objecto_id")
    list_filter = ("accao", "objecto_tipo")
    search_fields = ("objecto_id", "actor_descricao")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
