"""SMTP que nunca envia para domínios reservados (RFC 2606/6761), usados nos dados fictícios e nos testes.
Evita devoluções na caixa do remetente e e-mails para endereços inventados."""

import logging

from django.core.mail.backends.smtp import EmailBackend

RESERVADOS = (".test", ".demo", ".example", ".invalid", ".localhost")
log = logging.getLogger(__name__)


def reservado(endereco: str) -> bool:
    dominio = endereco.rsplit("@", 1)[-1].strip(" >").lower()
    return dominio.endswith(RESERVADOS) or dominio in {"localhost", "example.com", "example.org"}


class SmtpSemDominiosReservados(EmailBackend):
    def send_messages(self, email_messages):
        reais = []
        for m in email_messages:
            destinos = [d for d in m.recipients() if not reservado(d)]
            if not destinos:
                log.info("E-mail para domínio reservado não enviado: %s · %s", ", ".join(m.recipients()), m.subject)
                continue
            m.to = [d for d in m.to if not reservado(d)]
            m.cc = [d for d in m.cc if not reservado(d)]
            m.bcc = [d for d in m.bcc if not reservado(d)]
            reais.append(m)
        enviados = super().send_messages(reais) if reais else 0
        # Os não enviados de propósito contam como tratados (não são falhas de entrega).
        return enviados + (len(email_messages) - len(reais))
