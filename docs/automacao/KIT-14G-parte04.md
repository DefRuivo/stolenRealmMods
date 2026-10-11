# KIT-14G — parte04: rodada de runtime iniciada (run712), 1º boot real e o defeito achado

Cartão `t_0e656658`, implementador `default/run712`, 10/10/2026. Complementa parte01–03.
Esta parte registra a **rodada de runtime** (o desbloqueio por Opção A: o dono desligou o
Steam Cloud do app `1330000`) e o **defeito real** que o primeiro boot mediu.

## 1. Pré-condições conferidas (leitura, antes de tocar no jogo)

- `require_cloud_off()` **OK**: `cloudenabled = ["0"]` em `sharedconfig.vdf` (medido 19:00).
- `production_diff().equal` **OK**: 111/111 arquivos dos dados do dono idênticos à baseline KIT-16.
- nenhum processo `Stolen Realm` vivo; diretório real **sem junction**.
- instrumento: `AUT4Probe.dll` sha256 `687b72f1a630e32b655925408189b9cb73011ee7c33c1b9eb389e3239b89b1a8`
  (a build do run711), `KIT04Core.dll` `84d911a8…`, `KIT04Adapter.SR.dll` `2a4386bd…`.
- sandbox da rodada: `scratch/kit/KIT-14G-run712/sandbox/` (cópia do produto **antes** do
  primeiro boot; a conferência de fonte compara o produto com esta cópia).
- runner: `scratch/kit/KIT-14G-run712/roda.py` — reusa a cadeia REVISADA do run710
  (`with-passive-expanded.py`) sem mudar o produto, trocando só identidade/dirs/sessão e
  **acrescentando** ao `.cfg` as chaves que o driver ainda não emite
  (`NavegarTentativasMax`, `NavegarRota`, `NavegarAlvoNome`).

## 2. Boot `mapa` (rota `Play`, alvo `RstvRunSkillTreeButton`, teto 3600, janela 120 s)

`scratch/kit/KIT-14G-run712/mapa/` — `result.json`, `probe/aut4probe.json`,
`probe/recorder.json`, `probe/01-ui.png`, `probe/02-final.png`, `LogOutput-isolado.txt`.

Desfecho do instrumento: `status CONCLUIDO`, `fase concluido`, duração 36,8 s;
jogo fechado graciosamente (`game_closed: true`); Cloud **OFF** antes e depois.

### 2.1 MAPA de botões REAIS (item: insumo do roteiro) — NOVO, medido em jogo

`botoes_vistos` (o campo que o run710 não tinha) trouxe os rótulos ATIVOS da tela inicial:

| rótulo | 1ª tentativa |
|---|---|
| `Play` | 306 |
| `Online` | 306 |
| `Options` | 306 |
| `Backers` | 306 |
| `Exit Game` | 306 |
| `PLAY NOW!` | 306 |
| `WISHLIST NOW!` | 320 |
| `WISHLIST ON STEAM!` | 320 |
| `OUT NOW ON STEAM!` | 306 |
| `Discord Btn (1)` | 306 |
| `Email` | 306 |
| `Version Text` | 306 |

`estado_da_tela_pos_navegacao`: `CurrentGuiState = InMainMenu`. É o **menu principal**,
com os botões de jogo e os banners promocionais.

### 2.2 PROVA do recorder (item 1) — PARCIAL, honesta

`probe/recorder.json` foi **gravado dentro do processo e preservado** (o run710 perdia a
trilha no rollback). Conteúdo real lido do Core por reflexão:

- `identidade.hash_dll_do_core = 84d911a8…` e `hash_fonte_declarado = 84d911a8…` (**conferem**);
- `eventos: []`, `passivo.runtime = "NAO_EXERCITADO"`, `eventos_total = 0`,
  `capturas_solicitadas = 0`.

Ou seja: **o consumidor funciona** (leu `ResultadoFinal`, identificou a DLL, gravou o
arquivo), mas a **trilha veio VAZIA** — a sessão ficou só no menu, sem navegação/interação
que gere evento passivo. `eventos_total = 0` é **leitura medida**, não "0 inventado":
o campo é a contagem real do recorder. **Item 1 ainda NÃO fechado**: falta gerar evento
(navegar até uma ação observável) para comprovar contagem > 0.

### 2.3 Recoleta após navegação (item 3) — mecanismo OK, alvo não alcançado

`recoleta = {apos_navegacao: true, frame: 1332, observacoes: 57, rota_estagios_clicados: 1,
alvo_invocado: null}`. E `eventos_frame`: `ui_pronta/leitura 137`, `png_01-ui 1332→1338`,
`png_02-final 1338→1344`. A leitura de objetos é **do mesmo instante** do pedido do PNG
(ambos 1332) — o descasamento 157/1352 do run710 **não existe mais**.

### 2.4 O DEFEITO que impediu a navegação (achado executado)

`navegacao` diz: `rota_total: 1`, `rota_etapa: null` (o estágio FOI clicado), e então
`esgotado` procurando `Skills` por 3600 quadros — mas `CurrentGuiState` continua
`InMainMenu` e os `botoes_ativos = 10` são **os mesmos do menu**.

Causa medida: o casador do roteiro é **substring** (`rotulo.IndexOf(procurando) >= 0`).
O estágio `Play` casa tambem com o banner **`PLAY NOW!`**, e o clique foi no **primeiro
candidato** da varredura — que, no caso, foi o anúncio. O clique caiu no banner
(inofensivo) e **a tela não mudou**. Logo "chegar a Skills" falhava por um alvo AMBÍGUO,
não por ausência do botão.

Correção (parte05): o casador prefere **IGUALDADE** (case-insensitive) e usa a substring
apenas como **FALLBACK** — o rótulo exato do roteiro vence `PLAY NOW!`. É correção de
produto no instrumento (`AUT4ProbePlugin.cs`), com a suíte offline re-rodada.

## 3. Não exercitado nesta parte

Tela de Skills / botão do RSTV (não instalado neste boot), criação/seleção de personagem,
eventos do recorder com contagem > 0, Runner positivo/negativo, RSTV sem kit, FPS/frame/IO.
