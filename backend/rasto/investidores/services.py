from django.db import transaction

from rasto.auditoria.services import registar
from rasto.catalogo.models import ItemCatalogo
from rasto.contas.models import Papel, Utilizador, registar_consentimento
from rasto.nucleo.erros import ErroDominio

from .models import Investidor, Mandato


def investidor_do_utilizador(utilizador) -> Investidor | None:
    return Investidor.objects.select_related("mandato").filter(utilizador=utilizador).first()


@transaction.atomic
def registar_investidor(*, email: str, palavra_passe: str, nome: str, tipo: str, organizacao: str = "",
                        request=None) -> tuple[Utilizador, Investidor]:
    email = email.strip().lower()
    if Utilizador.objects.filter(email__iexact=email).exists():
        raise ErroDominio("Já existe uma conta com este e-mail. Entre com essa conta ou use outro e-mail.")
    u = Utilizador.objects.create_user(email, palavra_passe, nome=nome.strip(), papel_id=Papel.INVESTIDOR)
    registar_consentimento(u)
    inv = Investidor.objects.create(utilizador=u, tipo=tipo, organizacao=organizacao.strip())
    Mandato.objects.create(investidor=inv)
    registar(actor=u, accao="investidor_registado", objecto=inv, depois={"tipo": tipo}, request=request)
    return u, inv


def _itens(ids, tipo) -> list[ItemCatalogo]:
    itens = list(ItemCatalogo.objects.filter(pk__in=ids or [], tipo=tipo, activo=True))
    if len(itens) != len(set(ids or [])):
        raise ErroDominio(f"Há opções de {tipo} que já não estão disponíveis. Actualize a página.")
    return itens


@transaction.atomic
def guardar_mandato(*, utilizador, sectores: list, fases: list, geografias: list, risco=None,
                    cheque_min: int | None = None, cheque_max: int | None = None, moeda_cheque: str = "USD") -> Mandato:
    inv = investidor_do_utilizador(utilizador)
    if inv is None:
        raise ErroDominio("Esta conta não é de investidor.")
    if cheque_min is not None and cheque_max is not None and cheque_min > cheque_max:
        raise ErroDominio("O cheque mínimo não pode ser maior do que o máximo.")
    m = inv.mandato
    m.sectores.set(_itens(sectores, "sector"))
    m.fases.set(_itens(fases, "fase"))
    m.geografias.set(_itens(geografias, "geografia"))
    m.risco = _itens([risco], "risco")[0] if risco else None
    m.cheque_min, m.cheque_max, m.moeda_cheque = cheque_min, cheque_max, moeda_cheque
    m.save()
    registar(actor=utilizador, accao="mandato_guardado", objecto=m,
             depois={"sectores": len(sectores), "fases": len(fases), "geografias": len(geografias)})
    return m
