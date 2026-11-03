from django.conf import settings


def prazo(chave: str) -> int:
    """Valor inteiro de um prazo: tabela Parametro se existir, senão o valor de partida das definições."""
    from .models import Parametro

    linha = Parametro.objects.filter(chave=chave).first()
    if linha is not None:
        try:
            return int(linha.valor)
        except ValueError:
            pass
    return int(settings.PRAZOS_DEFEITO[chave])
