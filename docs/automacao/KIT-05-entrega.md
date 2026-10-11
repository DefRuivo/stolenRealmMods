# KIT-05 — ENTREGA: observação passiva e captura por eventos (RSTV)

Cartão: `t_e9e569f8` (KIT-05) · perfil `default` · run 629 · author: implementer
Data: 2026-10-09 · **offline** (sem jogo, sem perfil do dono, sem deploy, sem publicação)

## 1. Objetivo e o que foi entregue

Estender a coleta pontual (AUT-4/CAP-1/Core KIT-04) para **observar** uma sessão
autorizada enquanto o humano joga, com o primeiro conjunto de eventos RSTV. O
pipeline (dedup/fila/retenção/teto/pausa/degradação/correlação) foi implementado
como **lógica pura executável** e provado por testes offline **reais**.

| Arquivo | Papel | sha256 |
|---|---|---|
| `tools/automacao/runtime/observacao_passiva.py` | pipeline (460 linhas) | `e3e89d5b2600a4d495465c55a612d60b48ba8746e59ad61b5a0e4ed6ffaac713` |
| `tools/automacao/kit05/teste_observacao_passiva.py` | 19 testes (261 linhas) | `bf7ae0e59901503be7f1a564f88da8bf4dcc4996bd9ee15557370f2ba9d496c6` |
| `tools/automacao/kit05/roda_testes_kit05.sh` | runner (suite + contra-prova) | `05bc6a34b233c2c78f7b8e8a073470175b74c6a04a24bf32eb048fb6affd80a3` |
| `tools/automacao/runtime/fixtures/kit05-observacao.entrada.json` | roteiro de exemplo | `6802717c901416f826fc5a020485893409871279c1559dd62d4134884f37cf73` |
| `scratch/kit/KIT-05/contra_prova.py` | controle negativo (defeito plantado) | `027e6ee37bcfbfe8f58510f18aadea8002c31b2982a449dc03e5e9b23a8b68a0` |

Peças de progresso (artefato incremental): `docs/automacao/KIT-05-parte01.md`
(`503cc52acb7d70eca8df2a1b35dd50a5cbc7cd6009e8aff1c80ff2bd1e1a935a`),
`-parte02.md` (`3db1d1831e7dbbe24911aa14aa5544cb4b683c609cd7f7a5ee9620a8381710fc`),
`-parte03.md` (`ad71796f34f7f5146c8e111d4bac1802290bec900b837a0caba75f7392641de8`),
`-parte04.md` (`deed1811971ae8836459e2b644a7334dc7862aa3b6b24f08efc55d5053f928a1`).
(Hash deste arquivo não é autocitado.)

## 2. Aceite — veredito por item (com prova)

| Item do cartão | Veredito | Prova |
|---|---|---|
| Registrar clique recebido | PASSOU | `test_aceita_tipos_observados` + CLI (`clique_recebido: 2`) |
| Registrar janela aberta/fechada | PASSOU | idem (`janela_aberta: 1`, `janela_fechada: 1`) |
| Registrar tooltip | PASSOU | idem (`tooltip: 1`) |
| Capturar falha clique-sem-janela com motivo/timeout | PASSOU | `test_timeout_gera_falha_com_motivo` (motivo + `timeout_ms=500` + `clique_id`) |
| Relacionar id evento + dados + quadro após atualização visual | PASSOU | `test_captura_apos_atualizacao_visual` (`captura_apos_atualizacao_visual=True`, `captura_id`, `indice_quadro`) |
| NÃO afirmar simultaneidade inexistente | PASSOU | `test_nenhum_evento_afirma_simultaneidade` (todos os quadros + resumo `False`) |
| Sem clique/save/equipamento/modificação no modo passivo | PASSOU | `test_rejeita_tipo_ativo`, `test_rejeita_dado_ativo` |
| Dedup por mudança | PASSOU | `test_estado_repetido_nao_vira_evento`, `test_clique_nao_deduplica` |
| Fila limitada | PASSOU | `test_fila_limitada_descarta_e_declara` (+ degradação `fila_cheia`) |
| Retenção | PASSOU | `test_retencao_por_idade`, `test_retencao_por_tamanho` |
| Teto de capturas | PASSOU | `test_teto_de_capturas` (+ degradação `teto_capturas_atingido`) |
| Pausa segura e degradação explícita | PASSOU | `test_pausa_descarta_e_retoma` (degradação `pausado`) |
| Sem captura contínua indiscriminada | PASSOU | captura só sob pedido explícito (`registrar_captura`) e dentro do teto |
| Testes offline reais | PASSOU | `Ran 19 tests ... OK`, exit 0 (abaixo) |
| Desempenho runtime | NAO_EXERCITADO | exige rodada autorizada do dono (fora do escopo) |

## 3. Prova de execução real (comandos + saída + exit)

```
$ python tools/automacao/kit05/teste_observacao_passiva.py
Ran 19 tests in 0.001s
OK
EXIT=0
```

```
$ python scratch/kit/KIT-05/contra_prova.py
[A_trava_modo_passivo        ] OK (reprovou: test_rejeita_tipo_ativo)
[B_dedup_por_mudanca         ] OK (reprovou: test_estado_repetido_nao_vira_evento)
[C_fila_limitada             ] OK (reprovou: test_fila_limitada_descarta_e_declara)
[D_teto_capturas             ] OK (reprovou: test_teto_de_capturas)
[E_pausa_segura              ] OK (reprovou: test_pausa_descarta_e_retoma)
[F_sem_simultaneidade        ] OK (reprovou: test_nenhum_evento_afirma_simultaneidade)
[G_timeout_clique_sem_janela ] OK (reprovou: test_timeout_gera_falha_com_motivo)
VEREDITO: VERDE (todas as iscas reprovaram)
EXIT=0
```

```
$ bash tools/automacao/kit05/roda_testes_kit05.sh
VEREDITO KIT-05: VERDE (exit 0)
```

Teste mostrando REPROVAR (primeira rodada, antes da correção de retenção por
tamanho): `Ran 19 tests ... FAILED (failures=1)` em `test_retencao_por_tamanho`,
`EXIT=1` — o teste reprovou de verdade e dirigiu a correção (`_enfileira` passou a
aplicar o teto de retenção).

CLI end-to-end (fixture): `eventos_por_tipo = {clique_recebido:2, janela_aberta:1,
tooltip:1, falha_clique_sem_janela:1, janela_fechada:1}`;
`degradacoes_motivos = [pausado, sem_mudanca, tipo_ativo]`; `simultaneidade_afirmada
= False`; exit 0.

## 4. Não-regressão da infra vizinha

A suite AUT-4 (`python tools/automacao/runtime/roda_testes_runtime.py`) continua
**VERDE, 16 teste(s), exit 0** — o teste do KIT-05 vive em `tools/automacao/kit05/`
(área autocontida), de propósito, para **não** tocar o inventário travado de
`runtime/testes/` (front AUT-4/R0F, ainda pendente de commit).

## 5. Lacunas declaradas (honestidade)

- **Runtime em jogo: NÃO_EXERCITADO.** A emissão real pelo Core C# (eventos RSTV a
  partir da sessão viva) depende de rodada autorizada (gate do dono) e não foi
  exercitada. O lado C# (`KIT04Core`) ainda tem a lista simples sem teto; este
  módulo é a **especificação executável** que ele deve reusar (dedup/fila/retenção/
  teto/pausa/degradação/correlação). Não houve compilação C# nesta frente (não foi
  necessário para a lógica entregue; nenhum arquivo C# foi alterado).
- **Desempenho runtime:** só se mede em rodada autorizada.

## 6. O que NÃO fiz

Nenhum jogo aberto/fechado, nenhum save/perfil do dono, nada instalado/publicado,
nenhum `git add`/commit, nenhum arquivo do produto (mods) alterado, nenhum
documento de outro front (`docs/AUT-4-*`) alterado, nenhuma mudança de
política/modelo/cron/prioridade.

## 7. Próximo passo

Revisão independente pelo cartão **KIT-05R (`t_43675d2e`)**: exercitar caminho
positivo e defeito plantado em sandbox, veredito por critério, refutar falso
sucesso visual / captura fora do evento / spam / interferência.
