# PUB-API-2 — RealmApi no ledger (`release/mods.json`) e prova no pipeline (dry-run)

Cartao: `t_c15cf9d8`. Data: 16/10/2026. Nada foi publicado, nada foi empurrado, nenhum
`--go`, nenhum `publicar:true` novo, nenhuma entrada de outro mod alterada.

## 1. O que mudou

Arquivo unico alterado: `release/mods.json`.
`git diff --numstat` = **7 insercoes, 0 remocoes** (so o bloco novo).

```diff
@@ -62,6 +62,13 @@
       "publicado_em": "2026-10-07T21:25:01.979953Z",
       "motivo": "PUBLICAR 0.1.3 (substitui a 0.1.2, no ar desde 03/10/2026). ..."
     },
+    {
+      "nome": "RealmApi",
+      "publicar": false,
+      "versao_publicada": null,
+      "publicado_em": null,
+      "motivo": "PREPARACAO para publicacao do RealmApi 0.1.0 (categoria Mods, conforme
+ api/manifest.json): o pacote existe em dist/gumatos-RealmApi-0.1.0.zip e o empacotador ja
+ reconhece o nome (PKG-API-1), mas esta entrada NAO autoriza envio. TRAVADO para publicacao
+ ate o aceite humano do dono e o disparo explicito; nao entra em ordem_de_envio (o RealmApi
+ sobe ANTES do RoguelikeSkillTreeVisualizer, que declara a dependencia 0.1.0)."
+    },
     {
       "nome": "RoguelikeDebugger",
       "publicar": true,
```

Posicao: entre `BetterTooltips` e `RoguelikeDebugger` — a ordem alfabetica que o proprio
arquivo ja usa (`BetterTooltips < RealmApi < RoguelikeDebugger`).

### Preservacao byte a byte das outras entradas

A insercao foi feita em BYTES (`insere_realmapi.py`, anexo), com tres guardas:

1. aborta se `"RealmApi"` ja existir no arquivo;
2. aborta se a marca de insercao (`    {\r\n      "nome": "RoguelikeDebugger",`) aparecer
   mais de uma vez;
3. aborta se `novo.replace(BLOCO_NOVO, '', 1) != original` — ou seja, se a insercao tiver
   mexido em qualquer outro byte que nao o bloco novo.

Fim de linha: o arquivo e' CRLF (87 quebras). Continuou CRLF: **94 quebras** = 87 + as 7
linhas novas.

| | bytes | quebras CRLF | sha256 |
|---|---|---|---|
| antes | 8220 | 87 | `42e63efaa0872663053c96cbba8db34490be9be187cfb23f0f1bd3301da4127d` |
| depois | 8790 | 94 | `102be00e64e2b44889e789cc539f831e8cb45832e3c65e5171ac725d855accab` |

`mods.json` continua `esquema: 1`, com **9** entradas, e `ordem_de_envio` **intacta** (6
nomes, sem RealmApi — de proposito: um mod `publicar:false` nao entra na ordem de envio).

### Sobre "versao e categoria" do pedido

`esquema_de_um_mod` no proprio arquivo define CINCO campos: `nome`, `publicar`,
`versao_publicada`, `publicado_em`, `motivo`. Nao existe campo de versao planejada nem de
categoria. Em vez de inventar chave nova (que o gate nao le e o `registra` nao escreve),
a versao alvo (0.1.0) e a categoria (Mods, conforme `api/manifest.json`) foram escritas
dentro do `motivo`. `versao_publicada`/`publicado_em` ficam `null` — e' o contrato do
arquivo: quem preenche e' o job `registra` DEPOIS de um envio bem-sucedido, nunca a mao.

## 2. O nome casa o empacotador

`python tools/pack-thunderstore.py --listar-nomes` -> exit 0, **nove** nomes:

```
BetterCombatText, BetterFont, BetterPortuguese, BetterStats, BetterTooltips, RealmApi,
RoguelikeDebugger, RoguelikeSkillTreeVisualizer, RoguelikeUnlimitedLevelProgression
```

Comparacao com o ledger: `fantasmas` (no ledger, fora do packer) = `[]`;
`sem_ledger` (no packer, fora do ledger) = `[]`; conjuntos iguais. `RealmApi` aparece nos
dois, na mesma posicao alfabetica. (Antes desta tarefa o `sem_ledger` continha `RealmApi` e
o gate emitia `::warning::` por isso.)

## 3. Dry-run local (`tools/publish-thunderstore.sh`, sem `--go`)

### 3.1 Run direto (sem pular trava nenhuma) — para na trava de release

```
== ledger (release/mods.json + tools/pack-thunderstore.py) ==
  pacote                             estado    detalhe
  BetterCombatText                   LIBERADO  publicar:true
  BetterFont                         LIBERADO  publicar:true
  BetterPortuguese                   TRAVADO   BLOQUEADO para publicacao (BP-4): ...
  BetterStats                        LIBERADO  publicar:true
  BetterTooltips                     LIBERADO  publicar:true
  RealmApi                           TRAVADO   PREPARACAO para publicacao do RealmApi 0.1.0 ...
  RoguelikeDebugger                  LIBERADO  publicar:true
  RoguelikeSkillTreeVisualizer       LIBERADO  publicar:true
  RoguelikeUnlimitedLevelProgression TRAVADO   BLOQUEADO para publicacao (LEVEL-PACOTE-CONTRATO, ...)

  liberados: 6 | travados no ledger: 3 | sem entrada no ledger: 0
  pedido   : todos os liberados
  vao subir: BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer
== trava de segredo ==
  ==> nenhum padrao de credencial encontrado
== trava de release (tools/release-check.sh) ==
   ... PASSO 2/9 — PATCHES (trava TRV-1): REPROVA BetterPortuguese/Plugin.cs (sem linha 'carregado')
   [FALHA] 2. patch reprovado pela TRV-1 — release travada
!! release-check falhou; nada foi publicado        (exit 1)
```

Leitura: **RealmApi aparece TRAVADO com o motivo da propria entrada**, e os outros 8 no
estado deles (6 LIBERADO, 2 TRAVADO). O run aborta em `TRV-1 / BetterPortuguese` — achado
PRE-EXISTENTE de outro trabalho (cartao BP-6; a entrada do BetterPortuguese diz
`publicar:false`), nada a ver com esta mudanca. Nao pulei nada, nao mexi no
BetterPortuguese. Nao chegou a build, empacotamento nem envio.
Saida integral: `dryrun-1-direto.txt` (anexo).

### 3.2 Plano de envio inteiro (`PULAR_RELEASE_CHECK=1`) — exit 0

Ligando a opcao de pular a trava de release (nao proibida, e ainda dry-run) o run chega ao
fim e mostra o plano: os 6 liberados sao empacotados e listados como `[DRY-RUN] subiria`,
**RealmApi nao aparece no plano de envio**:

```
== empacotando (so os LIBERADOS: quem manda e' o ledger) ==
PRONTO - 6 pacote(s) em dist/:
  ...gumatos-BetterCombatText-0.1.3.zip  ...gumatos-BetterFont-1.0.3.zip
  ...gumatos-BetterStats-1.0.2.zip       ...gumatos-BetterTooltips-0.1.4.zip
  ...gumatos-RoguelikeDebugger-0.1.3.zip ...gumatos-RoguelikeSkillTreeVisualizer-0.3.4.zip
== envio ==
   [DRY-RUN] subiria: gumatos-BetterCombatText-0.1.3.zip (158144 bytes)
   [DRY-RUN] subiria: gumatos-BetterFont-1.0.3.zip (114529 bytes)
   [DRY-RUN] subiria: gumatos-BetterStats-1.0.2.zip (100872 bytes)
   [DRY-RUN] subiria: gumatos-BetterTooltips-0.1.4.zip (163851 bytes)
   [DRY-RUN] subiria: gumatos-RoguelikeDebugger-0.1.3.zip (136247 bytes)
   [DRY-RUN] subiria: gumatos-RoguelikeSkillTreeVisualizer-0.3.4.zip (108237 bytes)
== DRY-RUN terminou. Nada foi publicado. Use --go para publicar de verdade. ==
```

6 pacotes, 0 envios. Saida integral: `dryrun-2-plano.txt` (anexo).

### 3.3 Efeito colateral honesto no `dist/`

O passo de empacotamento do dry-run-2 regravou 3 zips em `dist/`:
`gumatos-BetterFont-1.0.3.zip`, `gumatos-BetterStats-1.0.2.zip`,
`gumatos-BetterTooltips-0.1.4.zip`. Causa: esses CHANGELOGs foram editados no disco pelo
CHG-REV a 13:30–13:32 e os zips estavam defasados em relacao a arvore; o empacotador le o
disco. Prova de que nao e' aleatoriedade: reempacotar os 3 de novo devolve **exatamente** os
mesmos sha256 (`dist-repack.txt` = `dist-depois.txt` nesses 3). Os outros 30 zips ficaram
byte a byte iguais. `mods.json` nao influencia conteudo de zip.

## 4. O gate do `publish.yml` precisa de ajuste? — **NAO**

Extrai o bloco Python do gate direto do workflow (heredoc `<<'PY'`, job `libera`, linhas
156–269) e rodei com o ledger novo, exatamente como o CI roda (`gate-extraido.py`):

| pedido | exit | resultado |
|---|---|---|
| `MOD=todos` | **0** | `alvos=[BetterCombatText, BetterFont, BetterStats, BetterTooltips, RoguelikeDebugger, RoguelikeSkillTreeVisualizer]`, `team=DefRuivo_StolenRealmMods`. Sem `::error::`, e **sem `::warning::` de `sem_ledger`** (era o aviso que existia antes desta tarefa). |
| `MOD=RealmApi` | **1** | `::error::RealmApi esta com publicar:false em release/mods.json e NAO sera publicado. Motivo registrado: PREPARACAO para publicacao do RealmApi 0.1.0 ...` |

Por que nao precisa de ajuste, ponto a ponto:

- **Gate (`libera`, ~190–208)**: a comparacao virou DIRECIONAL em PKG-API-1 (nome no ledger
  que o packer nao conhece -> erro; nome no packer sem ledger -> aviso). Agora que os dois
  lados tem os 9, nao ha nem erro nem aviso: a igualdade e' literal de novo.
- **Escolha a mao (`~215–221`)**: `RealmApi` ja existe no ledger, entao o gate nao cai mais
  em "mod desconhecido"; cai na trava de `publicar:false` e mostra o `motivo`. A unica
  trava do workflow que sobra aqui e' a que o dono quer que exista.
- **Job `publica`**: o pre-flight (`~464`, `for nome in alvos`) e o envio iteram somente os
  `alvos`, que saem de `publicar:true`. RealmApi nunca entra — nao precisa de caminho de
  upload nem de `categories` no metadata dele enquanto estiver travado.
- **Job `registra` (`~1026`)**: itera `alvos` tambem. Consequencia boa e' que o job nunca vai
  escrever `versao_publicada` no RealmApi por engano.
- **Tabela do resumo (`~240–249`)**: o RealmApi sai como `NAO` na coluna "liberado" com o
  motivo; a linha "sem entrada" (que aparecia para ele em PKG-API-1) deixa de existir.

O que **vai** precisar de ajuste — e NAO e' desta tarefa, e' da futura publicacao do
RealmApi (cartao PUB-API-3): (a) o input `mod` do `workflow_dispatch` e' um `type: choice`
com lista fixa de 6 mods (linhas 73–80) e nao inclui `RealmApi` — sem isso ele nao pode nem
ser escolhido a mao; (b) ao virar `publicar:true` ele tem de entrar em `ordem_de_envio`
ANTES do `RoguelikeSkillTreeVisualizer`. Nada disso bloqueia esta entrada.

## 5. Achado que afeta o lote de deploy (registrado, nao corrigido aqui)

`RoguelikeSkillTreeVisualizer/manifest.json` 0.3.4 — um mod `publicar:true` deste lote —
declara dependencia HARD `DefRuivo_StolenRealmMods-RealmApi-0.1.0`, que **nao existe** na
Thunderstore. `python tools/check_dependencias.py --local` aponta exatamente isso:

```
  FALHA RoguelikeSkillTreeVisualizer: depende de DefRuivo_StolenRealmMods-RealmApi-0.1.0, que NAO existe na Thunderstore
  ==> 1 dependencia(s) NAO resolvem - o upload seria recusado (No matching package found for reference).
```

Ou seja: enquanto o RealmApi estiver `publicar:false`, o upload do RSTV 0.3.4 seria recusado
pela Thunderstore. A ordem ja esta certa no ledger (RealmApi antes do RSTV), mas falta o
RealmApi ter `publicar:true` — decisao que NAO cabe a este cartao (trava explicita:
"nao virar publicar:true"). Registrado em comentario no cartao de deploy PUB-ALL-2.

## 6. Controles (nada mais foi tocado)

| arquivo | sha256 antes | depois |
|---|---|---|
| `release/mods.json` | `42e63efaa0872663…` | `102be00e64e2b448…` (esperado: esta tarefa) |
| `tools/pack-thunderstore.py` | `791f6809397ee04b…` | `791f6809397ee04b…` (igual) |
| `tools/publish-thunderstore.sh` | `ba3d3da8d7d981a1…` | `ba3d3da8d7d981a1…` (igual) |
| `.github/workflows/publish.yml` | `821058917ad1ae3e…` | `821058917ad1ae3e…` (igual) |

`git status --porcelain` continua mostrando `M .github/workflows/publish.yml` e
`M tools/pack-thunderstore.py` — sao as alteracoes de PKG-API-1, ja existentes antes desta
rodada, nao minhas. Sem commit, sem push.

## Anexos (na pasta de trabalho do cartao)

`insere_realmapi.py`, `roda_gate.py`, `gate-extraido.py`, `packer-nomes.txt`,
`gate-local.txt`, `gh-summary-todos.md`, `gh-output-todos.txt`, `dryrun-1-direto.txt`,
`dryrun-2-plano.txt`, `mods.diff`, `mods.json.antes`, `hashes-antes.txt`, `dist-antes.txt`,
`dist-depois.txt`, `dist-repack.txt`.
