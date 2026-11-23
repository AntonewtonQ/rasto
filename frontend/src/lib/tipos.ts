// Tipos das respostas da API do Django (rasto/api/representacoes.py).

export type Papel = "startup" | "investidor" | "entidade" | "admin";

export type Utilizador = { id: string; email: string; nome: string; papel: Papel };

export type Organizacao = {
  id: string; nome: string; tipo: string; tipo_rotulo: string; estado_verificacao: string; estado_rotulo: string;
  verificada_em: string | null; prazo_resposta: string | null;
  nome_legal?: string; nome_publico?: string; nif?: string; site?: string; cidade?: string;
  descricao_programa?: string; responsavel_nome?: string; responsavel_cargo?: string; responsavel_email?: string;
  motivo?: string; submetida_em?: string | null; passo_registo?: number;
};

export type Eu =
  | { autenticado: false }
  | {
      autenticado: true; utilizador: Utilizador; mfa_activa: boolean;
      contadores: Record<string, number>; organizacao?: Organizacao | null;
      startup?: { id: string; nome: string; estado: string } | null;
    };

export type Turma = {
  id: string; programa: string; edicao: string; nome: string; inicio: string; fim: string; periodo: string;
  estado: string; estado_rotulo: string;
};

export type Contagens = {
  total: number; aceites: number; pendentes: number; expirados: number; erros: number; validados: number;
  perfis_publicados: number;
};

export type Convite = {
  id: string; email: string; canal: string; estado: string; estado_rotulo: string; expira_em: string;
  aceite_em: string | null; criado_em: string; reenvios: number; enviado_por: string | null;
};

export type Sinal = {
  id: string; tipo: string; tipo_rotulo: string; descricao: string; data_facto: string | null; estado: string;
  estado_rotulo: string; frase_validada: string; validado_em: string | null;
  validador: { id: string; nome: string; verificada_em: string | null } | null;
  startup: { id: string; nome: string }; turma: Turma | null; pedido_em: string | null; expira_em: string | null;
  actualizado_em: string; motivo?: string; validado_por?: string;
  frase?: string; validavel_em_lote?: boolean; dias_restantes?: number; nota?: string; pedido_pela_startup?: boolean;
};

export type Comprovativo = { id: string; descricao: string; nome_original: string; tipo_mime: string; tamanho_bytes: number; criado_em: string };
