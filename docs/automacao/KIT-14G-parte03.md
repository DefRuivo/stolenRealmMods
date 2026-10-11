# KIT-14G — parte03: sessão isolada PREPARADA, o que falta e a decisão que trava

Cartão `t_0e656658`, implementador `default/run711`, 10/10/2026. Complementa parte01/parte02.
Este documento é o roteiro da **próxima** rodada (a única coisa que falta) e o pedido de
decisão humana. Volume: `scratch/kit/KIT-14G-run711/` (`estado-antes.json`,
`logs/`).

## 1. Por que a rodada de runtime não rodou agora

`estado-antes.json` (sha256 `97ea72cb96a026476ce765f6c1fcc67bc5b6dbaedc42c12cbc419a93764cdc86`)
mostra, medido às 18:10, que o dono **religou** o Steam Cloud do app `1330000`
(`cloudenabled = ["1"]`, era `["0"]` no run710 às 17:59) e que o **save do dono é objeto de
Cloud**: 21 arquivos (`Character0..16`, `GlobalSaveData.json`, `ItemStash.json`,
`TransmogList.json`, …) aparecem no `remotecache.vdf` com `syncstate=1`.

Com Cloud ligado, o boot do harness: (a) é **recusado pelo próprio guard**
`require_cloud_off()` (`scratch/kit/KIT-14-run704/suporte.py:69`); (b) se forçado, deixaria o
Steam importar os saves do dono para dentro da cópia isolada (a premissa de "dados vazios"
cai) e poderia **enviar de volta** o que a sessão escrevesse; (c) religar/desligar o toggle
exige UI do Steam (input de sistema proibido nesta rodada) ou edição do VDF (já recusada no
run710). Tudo o mais do ambiente está intacto: 111/111 arquivos dos dados, caminho real sem
junction, jogo fechado.

**Decisão necessária (uma das duas):**

- **A (recomendada, foi a do run710):** desligar de novo o Steam Cloud **somente** do
  Stolen Realm (Steam → Biblioteca → Stolen Realm → Propriedades → Geral → "Manter os jogos
  sincronizados com o Steam Cloud" OFF). Então a rodada técnica roda e **depois** o dono
  religa. Custo: dois cliques do dono.
- **B:** autorizar explicitamente a rodada **com** Cloud ligado, aceitando por escrito o
  risco sobre o save/cloud do dono. Sem essa autorização o agente não força o guard.

## 2. O que já está pronto (não precisa de outra rodada técnica de escrita)

- instrumento com roteiro/alvo por nome/mapa de botões/recoleta/consumidor do recorder
  (parte02), **build exercitada** `AUT4Probe.dll` sha256
  `687b72f1a630e32b655925408189b9cb73011ee7c33c1b9eb389e3239b89b1a8`, fonte
  `c32bbbd41e21d85ef05370fde091aac4e094239a2875b6faccae56d28c01019e`;
- harness offline com a parte4 verde (14 OK) e as partes 1–3 sem regressão (21 OK /
  5 OK / 10 OK), suite 16 testes e 33 iscas verdes;
- runbook `AUT-4-runbook-rodada-autorizada.md` e `AUT-4-estado.json` sincronizados com a
  nova build (senão as travas `t_aut4_runbook`/`t_aut4_estado_docs` reprovam).

## 3. Roteiro da rodada técnica (2 boots, reusando o que já é provado)

Reusa a cadeia do run710 (`scratch/kit/KIT-14-run710/coleta.py` → `with-passive-expanded.py`,
`prepare_empty`, `front-unica.sh`, `runtime-isolado.sh`, `kit16-save-isolado.sh`) — é o
caminho já revisado; muda só a identidade da build e as chaves novas do `.cfg`.

**Boot 1 — MAPA (roteiro vazio, só colhe rótulos).**
1. pré-checagem: `require_cloud_off()` **e** `production_diff().equal` (senão aborta);
2. perfil/BepInEx isolado (`runtime-isolado.sh preparar`) + Core/Adapter instalados com
   `com.gumatos.kit04.core.cfg` → `[Modo] habilitado = true` e
   `com.gumatos.kit04.adapter.sr.cfg` → `[Modo] habilitado = true`, `passivoHabilitado = true`
   (**a trilha passiva é opt-in duplo: sem isso o recorder não tem evento nenhum**);
3. `.cfg` do probe derivado + linhas acrescentadas (o driver ainda não emite estas chaves —
   mesmo padrão do `NavegarTentativasMax` no run710):
   `Navegar = true`, `NavegarTentativasMax = 3600`, `NavegarRota = ` (vazio),
   `NavegarAlvoNome = RstvRunSkillTreeButton`; registrar o sha256 do `.cfg` final;
4. dados isolados vazios (`kit16-save-isolado.sh preparar` + `prepare_empty`), junction
   conferida, boot via Steam `-applaunch 1330000` com os `--doorstop-*` do perfil isolado;
5. ao encerrar: **copiar `probe/aut4probe.json` + `probe/recorder.json` + PNGs ANTES do
   rollback**; conferir `botoes_vistos`, `recorder.status`, `recoleta.frame` e
   `prints_detalhe`; rollback e restauração conferidos por hash.

**Boot 2 — ROTEIRO (com o RSTV instalado no perfil temporário).**
6. escrever `NavegarRota` com os rótulos reais do boot 1 (ex.: `Play;Roguelike;…`), instalar
   a build do RSTV **apenas** no BepInEx temporário, repetir 1–5;
7. aceite do boot 2: roteiro percorre os estágios (`rota_clique`s no JSON), o alvo do RSTV
   aparece e o clique é invocado **uma vez**, `recoleta` com `apos_navegacao=true` no mesmo
   instante do PNG `01-ui`, `recorder.status=LIDO` com `eventos_contados > 0` e
   `recorder.json` preservado.

**Só depois** (item 4 do cartão): Runner positivo/negativo, RSTV sem kit, e medições
com/sem recorder. FPS/frame/I-O não medidos permanecem **NAO_EXERCITADO** — o dono dispensou
limiares e não se inventa número.

## 4. Limites declarados

- nenhum clique de sistema (`computer_use` indisponível sem supervisão), nenhum VDF editado;
- perfil/save real do dono intocados: o build desta rodada **não** instalou nada no perfil
  `Default` (conferido: sem `BepInEx/plugins/AUT4Probe`, sem `com.gumatos.aut4probe.cfg`);
- sem publicação, sem commit, sem deploy;
- o rótulo real das telas e a contagem real de eventos **só** existem com o jogo aberto:
  continuam NAO_EXERCITADO até a rodada acima acontecer.
