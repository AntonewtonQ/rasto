"""Dados fictícios para demonstração e testes de usabilidade. Nenhum nome, entidade ou startup é real."""

from datetime import date, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from rasto.contas.models import Papel, Utilizador
from rasto.organizacoes import services as org
from rasto.organizacoes.models import CRITERIOS
from rasto.sinais import services as sinais
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

        # Entidade em rascunho (para a tarefa A1 começar do zero, use o registo público)
        self.stdout.write(self.style.SUCCESS(
            f"Dados criados. Contas (palavra-passe «{PALAVRA}»):\n"
            "  admin@demo.rasto (administração; pede 2FA na 1.ª entrada)\n"
            "  gestora@kalandula.demo (entidade verificada)\n"
            "  centro@universidade.demo (entidade à espera de verificação)\n"
            "  nadia@kitanda.demo · joao@dikanza.demo (startups com participação pendente)\n"
            "  ana@mbote.demo (startup com participação validada)"))

    def _submeter(self, u, o, nome_publico, programa):
        org.adicionar_comprovativo(utilizador=u, organizacao=o, descricao="Certidão ou registo comercial",
                                   ficheiro=SimpleUploadedFile("certidao.pdf", PDF, "application/pdf"))
        org.submeter_entidade(utilizador=u, organizacao=o, dados={
            "nome_publico": nome_publico, "responsavel_nome": u.nome, "responsavel_cargo": "Gestão de programa",
            "responsavel_email": u.email, "descricao_programa": programa})
