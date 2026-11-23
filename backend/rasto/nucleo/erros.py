class ErroDominio(Exception):
    """Regra de negócio violada. A mensagem é mostrada ao utilizador tal como está."""


class TransicaoInvalida(ErroDominio):
    pass


class Conflito(ErroDominio):
    """Outra pessoa alterou o objecto entretanto (concorrência optimista, base técnica 8.1)."""
