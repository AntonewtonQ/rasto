import hashlib
import ipaddress
import json
from dataclasses import dataclass

from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection, transaction
from django.utils import timezone

from .models import RegistoAuditoria

GENESE = "0" * 64
_CHAVE_BLOQUEIO = 726_173  # pg_advisory_xact_lock: uma escrita de auditoria de cada vez


def _truncar_ip(ip: str | None) -> str:
    """IPv4 em /24 e IPv6 em /48: o suficiente para investigar abusos sem guardar o endereço completo."""
    if not ip:
        return ""
    try:
        endereco = ipaddress.ip_address(ip)
    except ValueError:
        return ""
    prefixo = 24 if endereco.version == 4 else 48
    return str(ipaddress.ip_network(f"{ip}/{prefixo}", strict=False))


def _conteudo(r: RegistoAuditoria) -> str:
    dados = {
        "actor": str(r.actor_id or ""),
        "accao": r.accao,
        "objecto_tipo": r.objecto_tipo,
        "objecto_id": r.objecto_id,
        "antes": r.antes,
        "depois": r.depois,
        "ip": r.ip_truncado,
        "criado_em": r.criado_em.isoformat(),
        "hash_anterior": r.hash_anterior,
    }
    return json.dumps(dados, sort_keys=True, cls=DjangoJSONEncoder, ensure_ascii=False)


def _calcular_hash(r: RegistoAuditoria) -> str:
    return hashlib.sha256(_conteudo(r).encode("utf-8")).hexdigest()


def _normalizar(valor):
    return json.loads(json.dumps(valor, cls=DjangoJSONEncoder)) if valor is not None else None


def registar(*, actor, accao: str, objecto, antes: dict | None = None, depois: dict | None = None,
             request=None) -> RegistoAuditoria:
    with transaction.atomic():
        with connection.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(%s)", [_CHAVE_BLOQUEIO])
        ultimo = RegistoAuditoria.objects.order_by("-id").values_list("hash", flat=True).first()
        r = RegistoAuditoria(
            actor=actor if getattr(actor, "pk", None) else None,
            actor_descricao=(getattr(actor, "email", "") or "sistema")[:160],
            accao=accao,
            objecto_tipo=objecto._meta.label_lower,
            objecto_id=str(objecto.pk),
            antes=_normalizar(antes),
            depois=_normalizar(depois),
            ip_truncado=_truncar_ip(request.META.get("REMOTE_ADDR")) if request is not None else "",
            criado_em=timezone.now(),
            hash_anterior=ultimo or GENESE,
        )
        r.hash = _calcular_hash(r)
        r.save(force_insert=True)
        return r


@dataclass
class ResultadoVerificacao:
    valido: bool
    registos: int
    primeiro_erro_id: int | None = None


def verificar_cadeia() -> ResultadoVerificacao:
    anterior = GENESE
    n = 0
    for r in RegistoAuditoria.objects.order_by("id").iterator():
        n += 1
        if r.hash_anterior != anterior or _calcular_hash(r) != r.hash:
            return ResultadoVerificacao(False, n, r.id)
        anterior = r.hash
    return ResultadoVerificacao(True, n)
