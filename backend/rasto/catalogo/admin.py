from django.contrib import admin

from .models import ItemCatalogo, TaxaCambio


@admin.register(ItemCatalogo)
class ItemCatalogoAdmin(admin.ModelAdmin):
    """Desactivar em vez de apagar: os mandatos e perfis antigos continuam a apontar para o item."""

    list_display = ("tipo", "nome", "codigo", "ordem", "activo")
    list_filter = ("tipo", "activo")
    list_editable = ("ordem", "activo")

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TaxaCambio)
class TaxaCambioAdmin(admin.ModelAdmin):
    list_display = ("data", "aoa_por_usd", "definida_por")
    readonly_fields = ("definida_por",)

    def save_model(self, request, obj, form, change):
        obj.definida_por = request.user
        super().save_model(request, obj, form, change)
