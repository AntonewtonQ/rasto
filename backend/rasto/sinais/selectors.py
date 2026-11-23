from django.db.models import Q

from rasto.organizacoes.models import MembroOrganizacao

from .models import Sinal


def sinais_da_entidade(utilizador):
    """Âmbito: sinais cujo validador é a entidade do utilizador e que dizem respeito a uma turma dela
    (participação, incluindo pedidos feitos pela startup) ou a uma startup de uma das suas turmas (marcos)."""
    orgs = MembroOrganizacao.objects.filter(utilizador=utilizador).values("organizacao_id")
    return (Sinal.objects.filter(validador_id__in=orgs)
            .filter(Q(turma__organizacao_id__in=orgs) | Q(startup__turmas__turma__organizacao_id__in=orgs))
            .select_related("startup", "turma", "validador", "validado_por").distinct())


def pendentes_da_entidade(utilizador):
    return sinais_da_entidade(utilizador).filter(estado=Sinal.Estado.PENDENTE).order_by("expira_em")
