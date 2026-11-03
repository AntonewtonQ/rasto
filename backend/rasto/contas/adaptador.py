from allauth.account.adapter import DefaultAccountAdapter


class AdaptadorConta(DefaultAccountAdapter):
    """Não há registo aberto pelo allauth: as contas nascem do registo da entidade, do convite da turma ou
    (no Sprint 2) do registo do investidor, que têm formulários próprios."""

    def is_open_for_signup(self, request):
        return False
