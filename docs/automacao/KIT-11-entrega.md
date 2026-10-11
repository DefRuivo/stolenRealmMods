# KIT-11 — Executor deterministico com permissoes separadas (entrega)

Cartao: `t_f2129aea` (run 649, perfil `default`).
Workspace: `C:/dev/stolen-realm`.
Status do documento: **ESQUELETO** — preenchido em blocos (checkpoints). As partes
incrementais ficam em `docs/automacao/KIT-11-parteNN.md`; este arquivo e o entregavel final.

## OBJETIVO (do cartao)

Reusar coletor/driver para executar cenarios CONHECIDOS sob autorizacao, sem IA improvisando:
maquina de estados que ESPERA menu/tela/condicao; handlers reais; diagnostico/timeout;
frente unica; cancelamento/rollback; encerra APENAS a instancia que criou.

## CRITERIOS DE ACEITE (checklist de cobertura)

- [ ] C1 Maquina de estados que espera menu/tela/condicao (nao "sleep cego").
- [ ] C2 Handlers REAIS por tipo de espera, com diagnostico do que faltou e timeout explicito.
- [ ] C3 Frente unica (lock) — uma execucao por vez.
- [ ] C4 Cancelamento e rollback exatos; encerra apenas a instancia criada pela propria execucao.
- [ ] C5 Modo ATIVO exige AUTORIZACAO SEPARADA (nao herda a autorizacao de observacao).
- [ ] C6 Perfil/save de TESTE verificados antes de qualquer acao ativa.
- [ ] C7 Observacao NAO concede acao (passivo != ativo).
- [ ] C8 Config/desconhecido/versao incompativel FALHAM FECHADO (nunca age por default).
- [ ] C9 Nao executar comandos ARBITRARIOS de cenario (whitelist de condicoes/acoes conhecidas).
- [ ] C10 Testes offline (stubs) de positivo, falha e cancelamento; navegacao real/clique fisico
      ficam para KIT-14 (apos KIT-G2).
- [ ] C11 Reuso da infra entregue (coletor/driver/controle_acesso/KIT-10 cenarios); sem duplicar.
- [ ] C12 Handoff nativo `kanban_request_review` com resumo+paths+hashes; revisao independente.

## ARQUIVOS VIVOS INVENTARIADOS (reuso)

- `tools/automacao/runtime/coletor.py` — driver opt-in (gated por `--autorizado`/`--jogo-disponivel`/
  `--confirmar-coleta`); NAO_EXERCITADO sem autorizacao.
- `tools/automacao/runtime/controle_acesso.py` — KIT-06: acoes conhecidas x ativas-proibidas,
  `habilitar_modo_ativo` sempre falha (passivo por construcao).
- `tools/automacao/runtime/observacao_passiva.py` — KIT-05F: pipeline passivo.
- `tools/automacao/runtime/roda_testes_runtime.py` — runner da suite (exit 0/1/2).
- `tools/automacao/cenarios/` — RSTV/tooltips/shrines (KIT-09/KIT-10).
- `tools/automacao/kit10/kit10_cenarios.py` — cenarios completos por avaliador (reuso literal).
- `tools/automacao/runtime/fixtures/`, `tools/automacao/runtime/testes/` — fixtures e testes.

## EVIDENCIA A PRODUZIR

- (a) modulo do executor + (b) testes offline com stubs (positivo/falha/cancelamento) +
  (c) saida real de terminal com exit code e caminhos.

## BLOCO 1 — inventario e desenho

(a ser preenchido)
