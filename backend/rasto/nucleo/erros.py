class ErroDominio(Exception):
    """Regra de negócio violada. A mensagem é mostrada ao utilizador tal como está."""


class TransicaoInvalida(ErroDominio):
    pass
