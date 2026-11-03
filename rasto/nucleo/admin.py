from django.contrib import admin

from .models import EmailSaida, Parametro


@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = ("chave", "valor", "descricao", "alterado_por", "alterado_em")

    def save_model(self, request, obj, form, change):
        obj.alterado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(EmailSaida)
class EmailSaidaAdmin(admin.ModelAdmin):
    list_display = ("criado_em", "destinatario", "assunto", "estado", "tentativas")
    list_filter = ("estado",)
    readonly_fields = [f.name for f in EmailSaida._meta.fields]

    def has_add_permission(self, request):
        return False
