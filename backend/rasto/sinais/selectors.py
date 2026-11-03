from rasto.organizacoes.models import MembroOrganizacao

from .models import Sinal


def sinais_da_entidade(utilizador):
    """Âmbito: sinais cujo validador é a entidade do utilizador e cuja startup está numa das suas turmas."""
    orgs = MembroOrganizacao.objects.filter(utilizador=utilizador).values("organizacao_id")
    return (Sinal.objects.filter(validador_id__in=orgs, startup__turmas__turma__organizacao_id__in=orgs)
            .select_related("startup", "turma", "validador", "validado_por").distinct())


def pendentes_da_entidade(utilizador):
    return sinais_da_entidade(utilizador).filter(estado=Sinal.Estado.PENDENTE).order_by("expira_em")
