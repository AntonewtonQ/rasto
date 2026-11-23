"""Dados fictícios para demonstração e testes de usabilidade. Nenhum nome, entidade ou startup é real."""

from datetime import date, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from rasto.acessos import services as acessos
from rasto.catalogo.models import ItemCatalogo, TaxaCambio
from rasto.contas.models import Papel, Utilizador
from rasto.investidores import services as investidores
from rasto.organizacoes import services as org
from rasto.organizacoes.models import CRITERIOS
from rasto.sinais import services as sinais
from rasto.startups import services as startups
from rasto.turmas import services as turmas
from rasto.turmas.models import Convite

PALAVRA = "demonstracao-rasto-2026"
PDF = b"%PDF-1.4\n% comprovativo ficticio para demonstracao\n"


class Command(BaseCommand):
    help = f"Cria dados fictícios (palavra-passe de todas as contas: {PALAVRA})."

    @transaction.atomic
    def handle(self, *args, **opts):
        if Utilizador.objects.filter(email="admin@demo.rasto").exists():
            raise CommandError("Os dados de demonstração já existem.")
        admin = Utilizador.objects.create_user("admin@demo.rasto", PALAVRA, nome="Administração Rasto",
                                               papel_id=Papel.ADMIN, is_staff=True)

        # Entidade verificada com uma turma activa
        u, a = org.registar_entidade(email="gestora@kalandula.demo", palavra_passe=PALAVRA, nome="Teresa Domingos",
                                     tipo="aceleradora", nome_legal="Aceleradora Kalandula, Lda", nif="5000000001",
                                     site="https://kalandula.example", cidade="Luanda")
        self._submeter(u, a, "Aceleradora Kalandula", "Programa de Aceleração 2025, 12 startups, Março a Junho.")
        cumpre = {c: {"estado": "cumpre", "nota": "Confirmado (demonstração)"} for c, _, _ in CRITERIOS}
        org.decidir_verificacao(admin=admin, organizacao=a, decisao="verificar", criterios=cumpre)
        t = turmas.criar_turma(utilizador=u, organizacao=a, programa="Programa de Aceleração", edicao="2026 · Turma 3",
                               inicio=date(2026, 3, 2), fim=date(2026, 6, 26))

        aceites = []
        for email, pessoa, startup in [("nadia@kitanda.demo", "Nádia Kiala", "Kitanda Fresca"),
                                       ("joao@dikanza.demo", "João Mateus", "Dikanza Saúde"),
                                       ("ana@mbote.demo", "Ana Sebastião", "Mbote Pagamentos")]:
            _c, url, _m = turmas.gerar_ligacao_convite(utilizador=u, turma=t, email=email)
            _novo, st = turmas.aceitar_convite_nova_conta(token=url.rstrip("/").rsplit("/", 1)[-1], nome=pessoa,
                                                          nome_startup=startup, palavra_passe=PALAVRA, consentiu=True)
            aceites.append(st)
        sinais.validar_sinal(utilizador=u, sinal=aceites[2].startup.sinais.get())
        turmas.enviar_convites(utilizador=u, turma=t, texto="pendente@lumbu.demo\nerro@sem-entrega.demo")
        Convite.objects.filter(email="erro@sem-entrega.demo").update(estado=Convite.Estado.ERRO_ENVIO)
        c, _, _ = turmas.gerar_ligacao_convite(utilizador=u, turma=t, email="atrasada@kissanje.demo")
        Convite.objects.filter(pk=c.pk).update(estado=Convite.Estado.EXPIRADO,
                                               expira_em=timezone.now() - timedelta(days=2))

        # Entidade submetida, à espera da administração
        u2, b = org.registar_entidade(email="centro@universidade.demo", palavra_passe=PALAVRA, nome="Paulo Neto",
                                      tipo="universidade", nome_legal="Centro de Empreendedorismo Universitário",
                                      nif="5000000002", cidade="Luanda")
        self._submeter(u2, b, "Centro de Empreendedorismo", "Incubação 2025, 8 projectos.")

        # Perfis publicados (Kitanda e Mbote); Dikanza fica por publicar para a tarefa da startup
        TaxaCambio.objects.get_or_create(data=date(2026, 11, 1), defaults={"aoa_por_usd": 912})  # valor fictício
        cat = lambda tipo, codigo: ItemCatalogo.objects.get(tipo=tipo, codigo=codigo)  # noqa: E731
        perfis = [
            ("nadia@kitanda.demo", aceites[0].startup, "agritech", "pre_seed", "BGU", "Benguela",
             "Liga pequenos produtores de hortícolas a restaurantes e mercados, com recolha diária.", 90_000_000, "AOA"),
            ("ana@mbote.demo", aceites[2].startup, "fintech", "seed", "LUA", "Luanda",
             "Pagamentos por telemóvel para pequenos comércios, sem terminal físico.", 150_000, "USD"),
        ]
        for email, st, sector, fase, prov, cidade, resumo, valor, moeda in perfis:
            dono = Utilizador.objects.get(email=email)
            startups.actualizar_perfil(utilizador=dono, startup=st, dados={
                "sector": cat("sector", sector), "fase": cat("fase", fase), "provincia": cat("geografia", prov),
                "cidade": cidade, "resumo": resumo, "contacto_fundador": email})
            startups.definir_ronda(utilizador=dono, startup=st, valor_alvo=valor, moeda=moeda, data_inicio=date(2026, 10, 1))
            startups.adicionar_documento(utilizador=dono, startup=st, titulo="Apresentação (fictícia)",
                                         url="https://example.org/apresentacao.pdf")
            startups.publicar(utilizador=dono, startup=st)

        # Investidores: um com mandato pronto, outro com um pedido pendente à Mbote
        ui, _ = investidores.registar_investidor(email="rui@imbondeiro.demo", palavra_passe=PALAVRA, nome="Rui Gaspar",
                                                 tipo="anjo")
        investidores.guardar_mandato(utilizador=ui, sectores=[cat("sector", "agritech").id, cat("sector", "fintech").id],
                                     fases=[cat("fase", "pre_seed").id, cat("fase", "seed").id], geografias=[],
                                     cheque_min=20_000, cheque_max=80_000, moeda_cheque="USD")
        uf, fundo = investidores.registar_investidor(email="marta@muxima.demo", palavra_passe=PALAVRA, nome="Marta Lopes",
                                                     tipo="fundo", organizacao="Fundo Muxima")
        investidores.guardar_mandato(utilizador=uf, sectores=[cat("sector", "fintech").id], fases=[cat("fase", "seed").id],
                                     geografias=[cat("geografia", "LUA").id], cheque_min=50_000, cheque_max=200_000)
        fundo.refresh_from_db()
        acessos.pedir_acesso(investidor=fundo, startup=aceites[2].startup,
                             nota="Investimos em pagamentos em Luanda; gostaríamos de ver a apresentação.")

        # Entidade em rascunho (para a tarefa A1 começar do zero, use o registo público)
        self.stdout.write(self.style.SUCCESS(
            f"Dados criados. Contas (palavra-passe «{PALAVRA}»):\n"
            "  admin@demo.rasto (administração; pede 2FA na 1.ª entrada)\n"
            "  gestora@kalandula.demo (entidade verificada)\n"
            "  centro@universidade.demo (entidade à espera de verificação)\n"
            "  nadia@kitanda.demo (startup publicada, participação pendente)\n"
            "  joao@dikanza.demo (startup por publicar)\n"
            "  ana@mbote.demo (startup publicada, validada, com um pedido de acesso pendente)\n"
            "  rui@imbondeiro.demo (investidor com mandato definido)\n"
            "  marta@muxima.demo (investidora com pedido pendente à Mbote)"))

    def _submeter(self, u, o, nome_publico, programa):
        org.adicionar_comprovativo(utilizador=u, organizacao=o, descricao="Certidão ou registo comercial",
                                   ficheiro=SimpleUploadedFile("certidao.pdf", PDF, "application/pdf"))
        org.submeter_entidade(utilizador=u, organizacao=o, dados={
            "nome_publico": nome_publico, "responsavel_nome": u.nome, "responsavel_cargo": "Gestão de programa",
            "responsavel_email": u.email, "descricao_programa": programa})
