# KIT-06 — parte 01: esqueleto e inventário (artefato incremental)

Cartão `t_66ff87b5` · perfil `default` · run 633 · data 2026-10-09
Modo **offline**: sem jogo, sem save, sem instalar/deploy/publicar, sem gate humano.

## 0. Objetivo (do cartão)

Criar controles de uso **sem terminal** para modder/jogador: habilitar observação,
pausar e **marcar problema**. UI/atalhos configuráveis com **indicador de coleta**,
**contexto** e **marcação manual**. Guards de **chat/remapeamento** e ausência de
conflito com input. **Iniciar observação nunca autoriza modo ativo.** Sem foco
forçado nem encerrar sessão do dono. Tornar **exportação acessível sem Hermes/IA**;
integrar contrato **KIT-07** quando disponível. Fluxo completo offline onde
possível; **UI real necessita KIT-G2**.

## 1. Dependência lógica e estado verificado

- Pai `t_467952ea` (KIT-05F) concluído: APROVADO (run 632 ≠ 631). Entrega:
  `docs/automacao/KIT-05F-entrega.md`.
- Pipeline reaproveitado: `tools/automacao/runtime/observacao_passiva.py`
  (KIT-05F, SHA256 `63124b86...`), com `pausar`/`retomar`,
  `registrar`, teto/imites, degradação explícita.
- KIT-07 (`t_c364710f`) **não implementado** → contrato de integração será
  declarado como **stub/contrato** (schema de export), sem duplicar infra.

## 2. Itens a cobrir (checklist)

1. Inventário de arquivos vivos relevantes (KIT-05F + adapter C# + harness).
2. Módulo offline do plano de controle (`controle_acesso.py`):
   a. ações observar/parar, pausar/retomar, marcar_problema, exportar;
   b. atalhos configuráveis por arquivo (JSON) com validação;
   c. guards: contexto de chat/digitando, remapeamento de teclas, conflito de input;
   d. iniciar observação **nunca** habilita modo ativo (trava dura);
   e. sem foco forçado / sem encerrar sessão do dono;
   f. indicador de coleta + contexto + marcação manual;
   g. export acessível sem Hermes/IA (arquivo local, nome padrão).
3. Ponte C# de atalhos (offline, dependente de Unity só no wrapper) + harness.
4. Testes reais (`unittest`, "Ran N tests") mostrando reprovação.
5. Contra-prova adversarial (iscas + controle falso-verde).
6. Build em cópia isolada com `-p:DeployToBepInEx=false` (se a parte C# entrar).
7. Entrega final `docs/automacao/KIT-06-entrega.md` + hashes.

## 3. Limites declarados desde já

- Runtime/pixels/jogo: **NAO_EXERCITADO** (exige rodada autorizada do dono).
- UI real (overlay/BepInEx GUI): **necessita KIT-G2** → aqui provamos a **lógica**
  do plano de controle e a **ligação de teclas** offline.
- KIT-07: apenas contrato declarado (sem acoplamento obrigatório).

## 4. Progresso

- [x] parte01 gravado (inventário inicial + checklist).
