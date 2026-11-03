from django.urls import path
from drf_spectacular.views import SpectacularAPIView

from . import vistas_admin as adm
from . import vistas_conta as conta
from . import vistas_entidade as ent
from . import vistas_startup as st
from . import vistas_turmas as tur
from . import vistas_validacoes as val

urlpatterns = [
    path("csrf", conta.Csrf.as_view(), name="api_csrf"),
    path("eu", conta.Eu.as_view(), name="api_eu"),
    path("esquema", SpectacularAPIView.as_view(), name="api_esquema"),
    # Entidade validadora
    path("registo/entidade", conta.RegistoEntidade.as_view(), name="api_registo_entidade"),
    path("entidade", ent.Entidade.as_view(), name="api_entidade"),
    path("entidade/painel", ent.Painel.as_view(), name="api_entidade_painel"),
    path("entidade/comprovativos", ent.Comprovativos.as_view(), name="api_comprovativos"),
    path("entidade/comprovativos/<uuid:pk>", ent.Comprovativo_.as_view(), name="api_comprovativo"),
    path("entidade/submeter", ent.Submeter.as_view(), name="api_submeter"),
    path("comprovativos/<uuid:pk>/ficheiro", ent.FicheiroComprovativo.as_view(), name="api_comprovativo_ficheiro"),
    path("turmas", tur.Turmas.as_view(), name="api_turmas"),
    path("turmas/<uuid:pk>", tur.Turma_.as_view(), name="api_turma"),
    path("turmas/<uuid:pk>/convites/verificar", tur.VerificarEmails.as_view(), name="api_verificar_emails"),
    path("turmas/<uuid:pk>/convites", tur.Convites.as_view(), name="api_convites"),
    path("turmas/<uuid:pk>/convites/ligacao", tur.ConviteLigacao.as_view(), name="api_convite_ligacao"),
    path("convites/<uuid:pk>/reenviar", tur.ReenviarConvite.as_view(), name="api_convite_reenviar"),
    path("convites/<uuid:pk>/cancelar", tur.CancelarConvite.as_view(), name="api_convite_cancelar"),
    path("validacoes", val.Validacoes.as_view(), name="api_validacoes"),
    path("validacoes/lote", val.ValidarLote.as_view(), name="api_validar_lote"),
    path("validacoes/<uuid:pk>", val.Validacao.as_view(), name="api_validacao"),
    path("validacoes/<uuid:pk>/<str:accao>", val.DecidirValidacao.as_view(), name="api_decidir_validacao"),
    # Convite público
    path("convites/publico/<str:token>", tur.ConvitePublico.as_view(), name="api_convite_publico"),
    path("convites/publico/<str:token>/aceitar", tur.AceitarConvite.as_view(), name="api_convite_aceitar"),
    path("convites/publico/<str:token>/recusar", tur.RecusarConvite.as_view(), name="api_convite_recusar"),
    # Startup
    path("startup/inicio", st.InicioStartup.as_view(), name="api_startup_inicio"),
    # Administração
    path("admin/verificacoes", adm.Verificacoes.as_view(), name="api_verificacoes"),
    path("admin/verificacoes/<uuid:pk>", adm.Verificacao.as_view(), name="api_verificacao"),
    path("admin/verificacoes/<uuid:pk>/abrir", adm.AbrirVerificacao.as_view(), name="api_verificacao_abrir"),
    path("admin/verificacoes/<uuid:pk>/decisao", adm.DecidirVerificacao.as_view(), name="api_verificacao_decisao"),
]
