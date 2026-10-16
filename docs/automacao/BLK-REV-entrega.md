# BLK-REV — auditoria dos cartões presos e desbloqueio com prova

Cartão `t_86ad5fc3` (BLK-REV) — 16/10/2026, run 1606, perfil `default`.
Regra que governou a auditoria: **o carimbo mente**. Cada razão foi reconferida na fonte viva
(banco do Kanban, arquivos do repo, código do mod, cron do vigia), não no texto do bloqueio.

Nada foi publicado, nada foi empurrado (`git push`), nenhuma aprovação humana foi fabricada,
nenhum arquivo de mod foi editado, nenhum runtime/jogo foi executado.

## 0. Correção da premissa: eram 17, não 18

O corpo do cartão dizia "são 18 cartões bloqueados". Medido no banco
(`kanban.db`, tabela `tasks`): havia **17** linhas com `status='blocked'`.
O 18º citado — `PUB-API-1` (`t_daf5efde`) — **não estava bloqueado**: estava `running` (run 1604).

E o quadro se mexeu *durante* esta auditoria, sozinho:

| hora (16/10) | evento real | fonte |
|---|---|---|
| 14:00:41 | `PUB-API-1` `t_daf5efde` liberado pela varredura de bloqueio morto e reclamado | `task_events` `stale_block_released` + `claimed` run 1604 |
| 14:03:54 | `PUB-API-1` **done** (`--listar-nomes` = NOVE, pre-flight verde) | evento `completed` |
| 14:05:02 | **dono autoriza o deploy** em `PUB-ALL-2` (`owner_authorized`, verbatim registrado) | evento `owner_authorized` by "Guilhe…" |
| 14:05:07 | `PUB-API-2` `t_c15cf9d8` liberado pela mesma varredura (pai `PKG-API-1` e pai `PUB-API-1` fechados) | `stale_block_released` + `claimed` run 1607 |
| 14:10:00 | `PUB-API-2` **done** (`release/mods.json` ganha a entrada RealmApi, `publicar:false`) | evento `completed` |

Consequência: dois dos "18" já não existem como bloqueio, e `PUB-ALL-2` deixou de ser um gate
de autorização em aberto. A entrega abaixo reflete o estado medido às 14:20, não o estado de 13:27.

## 1. Tabela da auditoria

Classes: **MORTA** (razão já não existe) · **REAL-DONO** (decisão humana) ·
**REAL-DEPENDENCIA** (pai/gate específico) · **REAL-TECNICA** (defeito técnico com escopo).

| cartão | carimbo (banco) | razão verificada hoje | classe | ação tomada | prova |
|---|---|---|---|---|---|
| `t_004ed4b0` EV-R2-NORMAL | `blocked`, kind vazio | revisão humana dos 160 eventos `Normal`; insumo durável pronto, nenhuma decisão do dono registrada | REAL-DONO | mantido bloqueado; pacote de decisão §2.2 | `docs/cobertura/EV-R1/lote-Normal-v2.md` (1.292.757 B); 38 arquivos `EV-R2-NORMAL-*` em `docs/automacao/`; 8 pais `b01..b08` **done**; 0 anexos e 0 veredito nos 5 cartões |
| `t_34205427` EV-R2-INICIOQUEST | `blocked`, kind vazio | revisão humana do único evento `QuestStart` | REAL-DONO | mantido | `lote-QuestStart-v2.md` (4.953 B) presente; pai `t_48d68679` done |
| `t_55517882` EV-R2-SEMPOOL | `blocked`, kind vazio | revisão humana dos 10 eventos de `EventSpawnTypes` vazio | REAL-DONO | mantido | `lote-SemPoolDeclarado-v2.md` (39.292 B) presente |
| `t_8e74c724` EV-R2-FORAPOOL | `blocked`, kind vazio | revisão humana dos 84 `NotInEventPool`; lotes b01/b02/b04 já entregues como **proposta** | REAL-DONO | mantido | 34 arquivos `EV-R2-FORAPOOL-*`; pais `b01..b04` **done**; comentários registram "aprovação PENDENTE nas 21 chaves" |
| `t_b10171fa` EV-R2-POSBATALHA | `blocked`, kind vazio | revisão humana do único `AfterBattle` | REAL-DONO | mantido | `lote-AfterBattle-v2.md` (1.891 B) presente |
| `t_71e4b22a` LANG-C1 | `blocked`, kind vazio | aprovação editorial das 1.293 ausências; **0** campos decididos | REAL-DONO | mantido | `entrega02/revisao-ausencias.csv`: `decisao_dono`/`texto_aprovado`/`observacoes` = **0/1293** preenchidos |
| `t_15176486` LANG-C2 | `blocked`, kind vazio | 268 textos idênticos ao inglês; **0** decididos | REAL-DONO | mantido | `revisao-identicos.csv`: **0/268** |
| `t_0bddb861` LANG-C3 | `blocked`, kind vazio | 847 IDs com placeholders/destaques; **0** decididos | REAL-DONO | mantido | `revisao-placeholders.csv`: **0/847** |
| `t_ec66f0bb` LANG-C4 | `blocked`, kind vazio | 85 IDs de tags/formatação; **0** decididos | REAL-DONO | mantido | `revisao-formatacao.csv`: **0/85**; `docs/automacao/LANG-C4-REVISAO-DONO.md` linhas 375–406: 16/16 campos `[ ] APROVAR [ ] REJEITAR [ ] AJUSTAR` em branco |
| `t_4da3d8a7` LANG-C5 | `blocked`, kind vazio | 376 textos longos; **0** decididos **+ 1 pai agêntico preso** | REAL-DONO **+ REAL-DEPENDENCIA** (`t_d5fb8625`) | mantido; pai técnico auditado e devolvido à fila (§3) | `revisao-layout.csv`: **0/376**; pais: `t_1398b50a` done, `t_8be12a0e` done, `t_990182b5` done, **`t_d5fb8625` triage** |
| `t_59f7fc24` BP-APL-1 | `blocked`/`needs_input` | falta ao menos 1 lote aprovado **e** há impedimento técnico medido no próprio mod | REAL-DEPENDENCIA (editorial) **+ REAL-TECNICA** | mantido bloqueado; cartão técnico criado (§3, BP-TG-1) | 5 gates em `blocked`, 0 aprovações; `BetterPortuguese/Core/Catalog.cs:130` chama `TokenGuard.Check`; `Catalog.cs:157-166` compara **inventário exato** de `[...]`/`{...}`/`*n`/`<...>` e lança `"Functional tokens/tags changed; explicit validated exception unsupported in 0.1.0"`; `BetterPortuguese/package.py:69` grava `contentState='NO_HUMAN_APPROVALS_NO_TEXT_CHANGES'` **fixo no código** |
| `t_87a7283d` REPO-PRESERVA | `blocked`/`owner_deferred` | adiamento **decidido pelo dono** em 13/10 ("deixar só no disco local por enquanto e revisitar depois"); checkpoint local intacto | REAL-DONO (deferido, não morto) | mantido bloqueado; comentário com a verificação do destino | `C:/dev/backups/REPO-PRESERVA-t_87a7283d/PRIVATE-CHECKPOINT-20261012/` existe com `CHECKPOINT-NOMINAL-WIP.txt`, `DELIVERY-VERIFIED.json`, `bundle-verify.txt`, `level-r2-staged.diff` (o workspace scratch `…/workspaces/t_87a7283d` **sumiu** — o dado não mora lá) |
| `t_b001720d` KIT-G4 | `blocked`/`needs_input` | aceite humano real, **mas não convocável hoje**: o pai `KIT-14R` está `todo` e o KIT está congelado | REAL-DONO **+ congelamento** | mantido bloqueado | pais: `t_effde07f` done, `t_d83f3ef6` done, **`t_9ce7d260` (KIT-14R) `todo`**; material de um clique já existe: `KIT-G4-PREP` `t_8d3678c2` **done** e `KIT-G4-MAT` `t_728bc587` **done**, com `docs/automacao/KIT-G4-PREP-entrega.md` e `KIT-G4-PREP-runbook-dono.md` |
| `t_73f69753` PUB-API-3 | `blocked`, kind vazio, sem assignee | autorização nominal do dono para publicar o RealmApi — **e agora é pré-requisito duro do deploy que ele autorizou** | REAL-DONO | mantido bloqueado, **sem** pais de grafo de propósito (§2.4) | medi agora: `python tools/check_dependencias.py --local` → `FALHA RoguelikeSkillTreeVisualizer: depende de DefRuivo_StolenRealmMods-RealmApi-0.1.0, que NAO existe na Thunderstore ==> 1 dependencia NAO resolve - o upload seria recusado`; `release/mods.json:66` RealmApi `publicar:false` |
| `t_75d8736e` PUB-ALL-2 | `blocked`, kind vazio, **sem assignee** | o dono **já autorizou** (14:05, condicional a 4 pais). Não é mais decisão em aberto; é execução esperando dependência | REAL-DEPENDENCIA | **assignee=`default`** (era `None`); mantido bloqueado; comentário com os 4 pais | evento `owner_authorized` com o verbatim e a condição `PUB-ALL-1 + PUB-API-2 + DOC-REV + BLK-REV`; pais medidos: `t_d00f2bc6` done, `t_c15cf9d8` done, `t_d9d74e4d` running, `t_86ad5fc3` running |
| `t_c15cf9d8` PUB-API-2 | kind limpo pelo operador; depois liberado | **MORTA** — liberado pela varredura às 14:05 e concluído às 14:10 | MORTA | nada a fazer; registrado como prova do mecanismo | `stale_block_released` → `claimed` run 1607 → `completed` (`docs/automacao/PUB-API-2-entrega.md`) |
| `t_daf5efde` PUB-API-1 | `running` no início da auditoria | **MORTA** — liberado 14:00, concluído 14:03 | MORTA | nada a fazer | `stale_block_released` → run 1604 → `completed` |
| `t_821396a1` KIT-14F4R | `blocked`/`needs_input` | revisão técnica **existe e reprovou** (3 achados); a devolução nativa falhou por falta de *provenance*; e o KIT está congelado pelo dono desde 15/10 | REAL-TECNICA (rework exequível) **sob congelamento** | mantido bloqueado (é ele que segura KIT-14); cartão de rework criado (§3, KIT-14F5, bloqueado) | `docs/automacao/KIT-14F4R-revisao.md`: "VEREDITO GERAL: NÃO APROVADO para liberar KIT14. 3 achados que exigem correção" + §3 "Correções exigidas (devolvido por rework)" com 4 itens |

### 1.1 Por que a liberação automática de `PUB-API-2` demorou (e por que estava certa)

O operador limpou o carimbo `needs_input` e ligou `PKG-API-1` como pai "para o desbloqueio
automático funcionar". Ele **não** ficou preso por defeito: `PUB-API-2` tinha **dois** pais
declarados — `PKG-API-1` (fechado 13:56) e `PUB-API-1` (que só fechou 14:03). A máquina de
estados só libera quando **todos** os pais estão `done`/`archived`.

Mecanismo conferido na fonte viva, não inferido:

- **Nativo** (`hermes_cli/kanban_db.py`, sha256 `c3e2046a5d030d76478b431d547e5f4ddde411f582063e4a6f2d18645486541b`,
  reproduzido em banco em memória por `probe_promotions.py`): `recompute_ready()` promove
  `todo`/`blocked` com pais 100% `done` — **exceto** se `_has_sticky_block()` (linha 2148) for
  verdadeiro, e ele é verdadeiro quando o **último** evento `blocked`/`unblocked` é `blocked`.
  Nosso caso: `blocked` de criação → *sticky* → `recompute_ready` **nunca** liberaria sozinho.
- **Varredura de bloqueio morto** (`…/hermes/cron/jobs.json`: `stolen-realm-vigia`, cron
  `*/5 * * * *`, **enabled**; código em `scripts/economy_dispatcher.py:543-570`): seleciona
  `status='blocked' AND COALESCE(block_kind,'')=''`, **pula** título com
  `Revisão humana`/`Revisao humana`/`Aprovar`/`Aceitar o kit` e título com
  `runtime`/`em jogo`/`ingame`/`bancada`, **pula** cartão sem pais, e libera quando todos os
  pais estão `done`/`archived`. Foi ela que soltou `t_daf5efde` e `t_c15cf9d8` (eventos
  `stale_block_released`), dentro do ciclo de 5 minutos.

Prova empírica final do encadeamento: exatamente às 14:05:07, 1 minuto depois de `PUB-API-1`
virar `done`, `PUB-API-2` saiu do bloqueio sem intervenção humana.

## 2. Decisões que precisam do dono

Curto: o que ele decide, o que destrava. Cada item já tem o material pronto.

**D1 — Aprovar os textos que MUDAM (5 gates LANG-C1..C5).** Formato já acordado por ele em
13/10 ("os MANTER eu considero aprovados por padrão; só me mostre o que muda").
Destrava: `BP-APL-1` → `BP-5` → `BP-6` → publicação do BetterPortuguese (hoje
`"publicar": false` em `release/mods.json:46`). Material: os 5 CSVs de `entrega02/` (2.869
linhas com `decisao_dono` vazio) + `LANG-C4-REVISAO-DONO.md` (16 itens, o único com digest
pronto). **É a cadeia mais longa hoje parada.**

**D2 — Revisar os eventos (EV-R2 ×5).** Destrava: implementação de eventos (cartões novos;
nada é escrito no jogo sem esses vereditos). Material: `docs/cobertura/EV-R1/lote-*-v2.md` +
as propostas `EV-R2-FORAPOOL-b0x-parteNN.md` e `EV-R2-NORMAL-b0x-parteNN.md`.

**D3 — Autorizar a publicação do RealmApi (`PUB-API-3`).** É o **único item do lote que ele
autorizou que ainda não pode subir**, e agora é pré-requisito duro: `RoguelikeSkillTreeVisualizer`
0.3.4 declara dependência HARD `DefRuivo_StolenRealmMods-RealmApi-0.1.0`, que **não existe** na
Thunderstore; medido com `python tools/check_dependencias.py --local` (o upload seria recusado).
Sem o RealmApi no ar, o deploy autorizado sobe no máximo 6 mods e falha no RSTV.
**Pergunta objetiva:** a autorização de 14:05 ("autorizo o deploy") já cobre o upload do
RealmApi, ou ele quer autorizá-lo nominalmente neste cartão? (Ver §4 — não decidi por ele.)

**D4 — Destino privado fora da máquina (`REPO-PRESERVA`).** Ele adiou em 13/10. Decidir se
retoma. Destrava: o único critério em aberto do cartão (o checkpoint local **está** intacto e
verificado hoje). Consequência assumida do adiamento: perda de disco = perda do checkpoint.

**D5 — Aceitar o kit / autorizar a distribuição (`KIT-G4`).** Bloqueado duas vezes na vida:
o pai `KIT-14R` está `todo` e o KIT está congelado (D6). Material de um clique **já pronto**:
`KIT-G4-PREP-entrega.md` + `KIT-G4-PREP-runbook-dono.md`.

**D6 — Descongelar o KIT (PAUSA TOTAL de 15/10).** Destrava de uma vez: `KIT-14`, `KIT-14R`,
`KIT-14F4R` → rework, `KIT-00` e `KIT-G4`. Enquanto durar, nenhum cartão de KIT pode rodar
(nem o rework que já está especificado).

**D7 — O clique final do upload.** O `workflow_dispatch` usa um GitHub Environment com reviewer
humano: o upload irreversível só acontece depois do clique dele. Isso não é bloqueio, é desenho.

## 3. O que eu desbloqueei / criei / devolvi à fila

1. **`PUB-ALL-2` `t_75d8736e` → assignee `default`.** Ele ganhou a autorização nominal do dono,
   deixou de ser "pedir autorização" e virou "executar depois dos pais" — mas continuava **sem
   assignee**. Efeito medido: um cartão `ready` sem assignee é *silenciosamente descartado* pelo
   despachante (fica em `ready` para sempre). Com a varredura de 5 min prestes a liberá-lo
   (título sem palavra humana + pais fechando), o deploy iria para uma fila que não despacha.
   Não mudei `block_kind` de propósito: um carimbo o **excluiria** da varredura que ele precisa.
2. **`LANG-C5-B1` `t_d5fb8625` → carimbo falso removido e devolvido à fila.** Não é um dos 18,
   mas é o pai que segura `LANG-C5`. O carimbo dizia `needs_input`; o último evento real é
   `block_loop_detected`/`WORKER_STAGNATION` (detector interno de laço, 15/10 23:39) e os
   runs anteriores são `changes_requested` ×4 + 3 `protocol_violation`. **Não há pergunta humana
   pendente nesse carimbo.** Defeito medido pelo revisor: o gerador só tentava encurtar com
   `expansion_pct > 80` e o dataset inteiro tem no máximo ~24% → `0/117` propostas de ENCURTAR
   saíram, e as partes MD divergiam do TSV (fonte autoritativa). Ação: carimbo limpo,
   `hermes kanban specify` (triage → fila) e comentário com o contrato consolidado.
3. **`BP-TG-1` (novo, `default`)** — cartão técnico para o impedimento que sobrevive à
   aprovação humana do BP-APL-1: `TokenGuard` recusa 15 das 16 propostas de tag
   (`Catalog.cs:157-166`) e o recibo do pacote é fixo (`package.py:69`). Sem isso, aprovação
   humana sozinha **não** torna o lote aplicável.
4. **`KIT-14F5` (novo, `default`, criado já `blocked`)** — rework do KIT-14F4 com escopo exato
   copiado do parecer (§3 de `KIT-14F4R-revisao.md`). Criado bloqueado **de propósito**: rodá-lo
   agora violaria a PAUSA TOTAL do dono. Ele é a "solução" do `KIT-14F4R`: basta descongelar (D6).
5. **`KIT-14F4R` deliberadamente NÃO concluído.** Ele é pai de `KIT-14` `t_a1f38855`; concluí-lo
   liberaria `KIT-14` na fila — contra o congelamento. A revisão já foi entregue; o que faltava
   era o objeto do rework, que agora existe.

## 4. Não consegui classificar com certeza

- **`PUB-API-3` × autorização de 14:05.** Tecnicamente o RealmApi **tem** que subir antes do
  RSTV, então a autorização do deploy implica o upload da API. Mas o dono autorizou no cartão do
  *deploy*, não no cartão da *API*, e publicação é irreversível: **não tratei como autorizado**.
  Fica a pergunta D3. Também **não** liguei `PUB-API-1`/`PUB-API-2` como pais dele: o título
  ("AUTORIZAR…") não está na lista de palavras humanas da varredura de bloqueio morto e o
  carimbo está vazio — se os pais fechassem, a varredura de 5 min **liberaria sozinha** um gate
  de publicação irreversível. Hoje ele é imune porque não tem pai nenhum (a varredura pula
  cartão sem pais). Isso é um risco de higiene do vigia, não deste cartão: vale corrigir a lista
  `HUMANOS` em `scripts/economy_dispatcher.py:548` (falta `AUTORIZAR`).
- **`KIT-G4`: o congelamento cobre o aceite?** O dono congelou "o kit (bancada/automação)". Se o
  aceite visual/funcional exigir a bancada, ele também está congelado; se for só olhar o
  material já pronto, não. Não decidí — é decisão dele (D5+D6 juntas).
- **`KIT-00` `t_dc6125a6`** (triage, acompanhamento): sem trabalho definido, sem critério de
  fechamento hoje além de "acompanhar". Não mexi.
- **`t_d5fb8625`: 5ª rodada vs. reduzir o escopo.** Devolvi à fila com o contrato consolidado.
  Se o dono preferir não gastar mais rodadas nesse lote, o caminho alternativo é excluir os 117
  itens do escopo aprovado de LANG-C5 — decisão editorial, dele.
- **Dependências do lote fora dos 18** que continuam presas e são de terceiros, não minhas:
  `BP-5` `t_49686933` e `BP-6` `t_36c75af4` (esperam os 5 gates) e `MON-DEPLOY` `t_f0414a3f`
  (espera `PUB-ALL-2`, que agora espera `DOC-REV` + este cartão).

## 5. Limites desta auditoria

Só leitura no repo e no jogo; nenhum build, deploy, runtime, commit ou push. As únicas escritas
foram no quadro: 17 comentários de auditoria, 1 assignee, 1 carimbo falso limpo, 1 `specify`,
2 cartões criados (1 `blocked` de propósito). Nada foi desbloqueado sem prova.
As provas foram produzidas por execução real nesta rodada (`python tools/check_dependencias.py`,
`probe_promotions.py` sobre cópia em memória, leitura direta de `kanban.db`, contagem dos CSVs
do pacote final, `ls` nos caminhos citados), não copiadas de relatórios anteriores.

## 6. Estado do quadro depois da auditoria (medido às 14:15)

| item | antes | depois |
|---|---|---|
| `blocked` no quadro | 17 (13:27) → 16 (14:10, `PUB-API-2` solto) | **17**: os 16 originais (15 gates/esperas + KIT-14F5 novo) — nenhum gate do dono foi solto |
| `PUB-API-1` `t_daf5efde` | `running` (não era bloqueio) | **done** |
| `PUB-API-2` `t_c15cf9d8` | `blocked` (pai aberto) | **done** |
| `PUB-ALL-2` `t_75d8736e` | `blocked`, **sem assignee** | `blocked` + **assignee `default`** (espera `DOC-REV` e `BLK-REV`) |
| `LANG-C5-B1` `t_d5fb8625` | `triage`, carimbo `needs_input` **falso**, 3 crashes | **`ready`**, carimbo limpo, contrato consolidado no cartão |
| `KIT-14F4R` `t_821396a1` | `blocked/needs_input`, sem objeto de rework | `blocked` (segurando `KIT-14`) + **`KIT-14F5` `t_b7560eb7`** criado `blocked` |
| `BP-APL-1` `t_59f7fc24` | `blocked/needs_input` | `blocked` + **`BP-TG-1` `t_dbbf67ee`** (técnico, gated no BLK-REV) |

Resultado líquido para o dono: **nenhum gate humano foi liberado por engano**, dois bloqueios
técnicos viraram cartões de trabalho com escopo, um carimbo falso foi corrigido, um cartão de
deploy sem dono ganhou dono, e as 7 decisões que faltam (D1–D7) estão listadas juntas na seção 2.

