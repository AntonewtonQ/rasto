from unittest import mock

from django.core.mail import EmailMessage

from rasto.nucleo.email_backend import SmtpSemDominiosReservados, reservado


def test_dominios_reservados():
    assert reservado("nadia@kitanda.demo") and reservado("x@startup.test") and reservado("a@exemplo.example")
    assert reservado("b@localhost") and not reservado("antonewtonquima@gmail.com")


def test_nao_envia_para_dominios_reservados_e_filtra_destinatarios_mistos():
    b = SmtpSemDominiosReservados(host="smtp.invalid", fail_silently=False)
    so_ficticio = EmailMessage("a", "b", "rasto@x.org", ["nadia@kitanda.demo"])
    misto = EmailMessage("a", "b", "rasto@x.org", ["real@gmail.com", "teste@startup.test"])
    with mock.patch("django.core.mail.backends.smtp.EmailBackend.send_messages", return_value=1) as envio:
        assert b.send_messages([so_ficticio, misto]) == 2
    enviados = envio.call_args.args[0]
    assert len(enviados) == 1 and enviados[0].to == ["real@gmail.com"]
