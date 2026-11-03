import pytest
from django.db import DatabaseError, transaction

from rasto.auditoria.models import RegistoAuditoria
from rasto.auditoria.services import GENESE, _truncar_ip, registar, verificar_cadeia

pytestmark = pytest.mark.django_db


def test_cada_registo_encadeia_o_hash_do_anterior(admin):
    a = registar(actor=admin, accao="teste_1", objecto=admin, depois={"x": 1})
    b = registar(actor=admin, accao="teste_2", objecto=admin, antes={"x": 1}, depois={"x": 2})
    anterior = RegistoAuditoria.objects.filter(id__lt=a.id).order_by("-id").first()
    assert a.hash_anterior == (anterior.hash if anterior else GENESE)
    assert b.hash_anterior == a.hash
    assert verificar_cadeia().valido


def test_trigger_recusa_alteracao_e_eliminacao(admin):
    r = registar(actor=admin, accao="teste", objecto=admin)
    with pytest.raises(DatabaseError), transaction.atomic():
        RegistoAuditoria.objects.filter(pk=r.pk).update(accao="adulterado")
    with pytest.raises(DatabaseError), transaction.atomic():
        RegistoAuditoria.objects.filter(pk=r.pk).delete()


def test_verificacao_detecta_registo_inserido_com_hash_falso(admin):
    registar(actor=admin, accao="legitimo", objecto=admin)
    ultimo = RegistoAuditoria.objects.order_by("-id").first()
    RegistoAuditoria.objects.create(accao="forjado", objecto_tipo="x", objecto_id="1", criado_em=ultimo.criado_em,
                                    hash_anterior=ultimo.hash, hash="f" * 64)
    assert not verificar_cadeia().valido


def test_ip_e_truncado():
    assert _truncar_ip("197.149.80.123") == "197.149.80.0/24"
    assert _truncar_ip("2001:db8:abcd:12::1") == "2001:db8:abcd::/48"
    assert _truncar_ip("lixo") == ""
