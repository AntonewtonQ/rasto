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

// --- Sprint 2: perfil, mandato, compatibilidade e pedidos de acesso ---------------------------------------------

export type Item = { id: string; codigo: string; nome: string; descricao?: string };
export type Catalogo = { sector: Item[]; fase: Item[]; geografia: Item[]; risco: Item[]; taxa: { data: string; aoa_por_usd: string } | null };
export type Ronda = { valor_alvo: number; moeda: string; data_inicio: string };

export type PerfilStartup = {
  id: string; nome: string; estado: string; camada: 1 | 2;
  sector: Item | null; fase: Item | null; provincia: Item | null; cidade: string; resumo: string;
  ronda: Ronda | null; actualizado_em: string; verificados: Sinal[]; declarados: Sinal[];
  contacto_fundador?: string; documentos?: { id: string; titulo: string; url?: string }[]; actualizacoes?: Actualizacao[];
};

export type Criterio = { chave: string; rotulo: string; pontos: number; peso: number; estado: string; frase: string };
export type Compatibilidade = { total: number; classificacao: "compativel" | "parcial" | "incompativel"; versao: number; criterios: Criterio[]; aviso: string };

export type PedidoAcesso = {
  id: string; estado: string; estado_rotulo: string; nota: string; expira_em: string; criado_em: string;
  decidido_em: string | null; motivo?: string | null; novo_pedido_a_partir_de?: string | null;
};

export type PedidoRecebido = PedidoAcesso & {
  revogado_em: string | null;
  investidor: { nome: string; tipo: string; organizacao: string;
    mandato: { sectores: string[]; fases: string[]; geografias: string[]; cheque_min: number | null; cheque_max: number | null; moeda: string } };
  encaixe: Compatibilidade | null;
};

export type Mandato = {
  sectores: string[]; fases: string[]; geografias: string[]; risco: string | null;
  cheque_min: number | null; cheque_max: number | null; moeda_cheque: string; minimo_completo: boolean;
};

// --- Sprint 2 (parte 2): pipeline e actualizações -----------------------------------------------------------------

export type Etapa = { n: number; codigo: string; nome: string };
export type RelacaoPipeline = {
  id: string; lado: "startup" | "investidor"; nome: string; sub: string; externa: boolean; etapa: number; etapa_nome: string;
  valor: number | null; moeda: string; valor_texto: string | null; perdida: boolean; perdida_em: string | null;
  motivo_perda: string | null; nota_perda: string; ultima_actividade: string; parada: boolean; adiado_ate: string | null;
  versao: number; startup_id: string;
  movimentos?: { de: string | null; para: string; em: string; autor: string | null }[];
  interaccoes?: { id: number; tipo: string; tipo_rotulo: string; texto: string; em: string; autor: string | null }[];
};
export type Indicadores = {
  ronda: boolean; activas: number; paradas: number; perdidas: number; dias_ate_soft_commit: number | null;
  conversao: { etapa: number; nome: string; chegaram: number; passaram: number; pct: number | null }[] | null;
  comprometido: { valor: number; moeda: string; alvo: number; texto: string; pct: number | null; sem_conversao: number; taxa_data: string | null } | null;
};
export type Quadro = { etapas: Etapa[]; motivos: { valor: string; rotulo: string }[]; relacoes: RelacaoPipeline[]; indicadores?: Indicadores; pedidos_pendentes?: number };

export type Metrica = { codigo: string; rotulo: string; unidade: string; valor?: number; anterior?: number | null };
export type Actualizacao = {
  id: string; periodo: string; mes: string; estado: string; metricas: Metrica[]; destaques: string; pedidos_ajuda: string;
  corrige: { id: string; mes: string } | null; publicada_em: string | null; falhas_envio?: string[];
  metricas_brutas?: Record<string, number>;
};
