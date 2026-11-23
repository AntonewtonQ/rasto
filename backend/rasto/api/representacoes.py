"""Representações JSON dos objectos (o que a API devolve). Funções simples em vez de serializadores de saída:
cada campo exposto está aqui, à vista, o que facilita rever o que sai para cada papel."""

from rasto.nucleo.formatos import fmt_periodo


def utilizador(u) -> dict:
    return {"id": str(u.id), "email": u.email, "nome": u.nome, "papel": u.papel_id}


def organizacao(o, completa: bool = False) -> dict:
    d = {"id": str(o.id), "nome": o.nome, "tipo": o.tipo, "tipo_rotulo": o.get_tipo_display(),
         "estado_verificacao": o.estado_verificacao, "estado_rotulo": o.get_estado_verificacao_display(),
         "verificada_em": o.verificada_em, "prazo_resposta": o.prazo_resposta}
    if completa:
        d.update(nome_legal=o.nome_legal, nome_publico=o.nome_publico, nif=o.nif, site=o.site, cidade=o.cidade,
                 descricao_programa=o.descricao_programa, responsavel_nome=o.responsavel_nome,
                 responsavel_cargo=o.responsavel_cargo, responsavel_email=o.responsavel_email,
                 motivo=o.motivo, submetida_em=o.submetida_em, passo_registo=o.passo_registo)
    return d


def comprovativo(c) -> dict:
    return {"id": str(c.id), "descricao": c.descricao, "nome_original": c.nome_original, "tipo_mime": c.tipo_mime,
            "tamanho_bytes": c.tamanho_bytes, "criado_em": c.criado_em}


def turma(t) -> dict:
    return {"id": str(t.id), "programa": t.programa, "edicao": t.edicao, "nome": str(t), "inicio": t.inicio,
            "fim": t.fim, "periodo": fmt_periodo(t.inicio, t.fim), "estado": t.estado,
            "estado_rotulo": t.get_estado_display()}


def convite(c) -> dict:
    return {"id": str(c.id), "email": c.email, "canal": c.canal, "estado": c.estado,
            "estado_rotulo": c.get_estado_display(), "expira_em": c.expira_em, "aceite_em": c.aceite_em,
            "criado_em": c.criado_em, "reenvios": c.reenvios,
            "enviado_por": (c.enviado_por.nome or c.enviado_por.email) if c.enviado_por else None}


def sinal(s, para_startup: bool = False) -> dict:
    d = {"id": str(s.id), "tipo": s.tipo, "tipo_rotulo": s.get_tipo_display(), "descricao": s.descricao,
         "data_facto": s.data_facto, "estado": s.estado_visivel, "estado_rotulo": s.get_estado_display(),
         "frase_validada": s.frase_validada, "validado_em": s.validado_em,
         "validador": {"id": str(s.validador.id), "nome": s.validador.nome,
                       "verificada_em": s.validador.verificada_em} if s.validador else None,
         "startup": {"id": str(s.startup.id), "nome": s.startup.nome},
         "turma": turma(s.turma) if s.turma else None, "pedido_em": s.pedido_em, "expira_em": s.expira_em,
         "actualizado_em": s.actualizado_em}
    if para_startup or s.estado in ("recusado", "retirado"):
        d["motivo"] = s.motivo
    if s.validado_por:
        d["validado_por"] = s.validado_por.nome or s.validado_por.email
    return d


def item(i) -> dict | None:
    return {"id": str(i.id), "codigo": i.codigo, "nome": i.nome} if i else None


def ronda(r) -> dict | None:
    return {"valor_alvo": r.valor_alvo, "moeda": r.moeda, "data_inicio": r.data_inicio} if r else None


def perfil_startup(s, camada: int, para_startup: bool = False) -> dict:
    """Camada 1: o que qualquer investidor autenticado vê. Camada 2: só com pedido de acesso aceite.
    Os URLs dos documentos nunca saem aqui: o investidor abre-os por /api/v1/startups/<id>/documentos/<doc>/abrir."""
    from rasto.startups.services import ronda_aberta

    sinais_vis = [sinal(x) for x in s.sinais.select_related("validador", "turma", "validado_por", "startup")
                  if x.estado_visivel in ("validado", "validado_com_aviso", "declarado")
                  or (x.estado in ("retirado", "expirado", "recusado") and x.tipo == "marco")]
    for x in sinais_vis:  # o que não está validado aparece como declarado ao investidor (base de UX 6.2)
        if x["estado"] not in ("validado", "validado_com_aviso"):
            x["estado"] = "declarado"
            x.pop("motivo", None)
    d = {
        "id": str(s.id), "nome": s.nome, "estado": s.estado, "sector": item(s.sector), "fase": item(s.fase),
        "provincia": item(s.provincia), "cidade": s.cidade, "resumo": s.resumo, "ronda": ronda(ronda_aberta(s)),
        "actualizado_em": s.actualizado_em, "camada": camada,
        "verificados": [x for x in sinais_vis if x["estado"] in ("validado", "validado_com_aviso")],
        "declarados": [x for x in sinais_vis if x["estado"] == "declarado"],
    }
    if camada >= 2:
        d["contacto_fundador"] = s.contacto_fundador
        d["documentos"] = [{"id": str(doc.id), "titulo": doc.titulo} | ({"url": doc.url} if para_startup else {})
                           for doc in s.documentos.all()]
        from rasto.actualizacoes.services import visiveis_para_investidor
        from rasto.api.vistas_pipeline import actualizacao

        d["actualizacoes"] = [actualizacao(a) for a in visiveis_para_investidor(s).select_related("corrige")[:12]]
    return d
