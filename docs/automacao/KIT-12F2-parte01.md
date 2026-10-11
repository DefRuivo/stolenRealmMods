# KIT-12F2 — correcao dos achados F1R–F5R da revisao independente KIT-12R (parte 01)

Cartao: `t_51ca208a` (KIT-12F "Corrigir config/probe ausentes, relatorio indisponivel, coleta
invalida e saneamento OK"). Pai: `t_811b1717` (KIT-12R, parecer REPROVADO por `default/run674`).
Autor desta correcao: **instancia implementadora worker run675** (`!= run674`, o revisor).
Natureza: **OFFLINE**. Nada de jogo, build, deploy, instalacao, publicacao ou perfil do dono.

## Nota de nomenclatura (por que "KIT-12F2")

O nome `docs/automacao/KIT-12F-parte01.md` JA EXISTE no repo, produzido na rodada anterior
(run669, cartao `t_0a434c97`). O cartao pede "nao sobrescrever existentes" e admite "nome final
novo". Para nao destruir a entrega anterior, esta rodada usa o sufixo **F2** (convencao ja usada
no repo: `AUT-3R2`, `CIC-2R2`, `KIT-10R2`). Nenhum arquivo `KIT-12F-*` foi tocado.

## Alvo e fonte da verdade

- Produto: `tools/automacao/kit12/integracao.py`.
  - Baseline revisado (run674): sha256 `7785d8c1f624ff263b4ac89ad36e3ab9952db17d5a233d12affada091da8af87`.
  - Esta correcao: sha256 `480a9a02b7a2f13bb51d4bce32c29897ff944cfca00fd6431a924877a44da25c`.
- Fonte viva do parecer: `docs/automacao/KIT-12R-revisao.md`.
- **Orcamento independente IMUTAVEL**: `scratch/kit/KIT-12R-run674/test_review_kit12.py`
  (sha256 `cf5966527ac0276fbe827aeab0def2c7825deb5bc4fd27744d216d854c83f2c6`).
  NAO foi alterado — o alvo e tornar o MESMO oraculo 17 OK, reproduzindo 11 OK/6 FAIL no baseline.
- Invariantes medidos e inalterados: `test_kit12_integracao.py`
  `25284c7075633042efc6445a5856d5a24e40d152ccdb593d6cb94d661e96da8c`,
  `prove_ciclo.py` `4fc01b81572bdfbbea4cc3af33f1fb845659f23bc689cc94068e2d85b973b750`,
  `pertinencia.json` `b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320`.

## Achados a corrigir (do parecer KIT-12R)

| Id | Defeito | Correcao exigida |
|---|---|---|
| F1R | config explicitamente requerida ausente aprova OFFLINE/0 | lacuna tecnica nomeada + fila agente + INCOMPLETO/2; nao tornar opcional nao fornecida obrigatoria |
| F2R | relatorio ausente/erro IO aprova OFFLINE/0 | lacuna/fila agente + exit2; preservar motivo, nao inventar relatorio |
| F3R | probe solicitado e ilegivel usa fallback `dll_sha` e aprova | lacuna tecnica instrumento/exit2, SEM fallback silencioso |
| F4R | `observacoes` de tipo invalido aborta a CLI (exit1/traceback) | validar envelope/observacoes; INCOMPLETO/2 estruturado com causa tecnica |
| F5R | saneamento de campo executavel so alcanca criterios com item de fila | sanear TODOS os criterios, preservando a proposta como auditoria nao executavel |

## Plano deste bloco (executado)

1. `_validar_observacoes(doc)` — validacao fail-closed do campo `observacoes` (F4R).
2. `criterios_da_cadeia` — lacunas `cadeia/config-ausente/<rel>` (F1R) e
   `cadeia/instrumento-probe-ilegivel` (F3R), antes de anexar a cadeia.
3. `montar_fila` — saneamento GLOBAL de criterios sem item de fila (F5R) + proposta registrada
   no criterio (auditoria preservada e idempotente).
4. `cadeia` — montar o relatorio ANTES de classificar o estado; se indisponivel, lacuna
   `relatorio/indisponivel` + recalculo da fila (F2R); `propostas_do_resultado` (F5R).
5. Provar: baseline 6FAIL -> correcao 17OK; suite autor 30 OK; isca 14/14; CLI 2->1->2->2->2->2->3;
   controles proprios do revisor 0->1->0 reproduzidos; 38 sondas IRMAS.

Status: concluido. Detalhes nas partes 02 (o que mudou) e 03 (provas reais).
