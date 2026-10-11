# AUT-4 — parte 03: rodadas r2/r3/r4 — leitura viva, PNG, owners, ida-e-volta, isolamento e rollback

> Cartão `t_b8b9822e` · worker `default` (run 622) · 2026-10-09, 18:51–18:53 BRT.
> Continua `AUT-4-parte02.md`. Evidência bruta em `docs/automacao/AUT-4-evidencias/{r2-incompleto,r3-confirmada,r4-confirmada-log}/`.
> **Todas** as rodadas: jogo **FECHADO** antes, frente única sob lock, área **isolada**, somente leitura,
> sem save, sem navegação (`Navegar=false`), encerramento ao fim. O perfil/saves do dono terminaram
> **idênticos** ao “antes” (§4).

## 1. As três rodadas em uma tabela

| rodada | plano | status do probe | veredito do driver | exit | obs | prints | ida-e-volta | rollback | PID fechado |
|---|---|---|---|---|---|---|---|---|---|
| **r2** | r2 (`campos_alvo` inclui `texto_bruto`/`texto_renderizado`) | `CONCLUIDO` | **`INCOMPLETO`** | 1 | 24 | 2 PNG | `conferiu=true` | `limpo` | 27588 gracioso |
| **r3** | r3 (campos governantes = os que o instrumento mede em **todo** objeto lido) | `CONCLUIDO` | **`CONFIRMADA`** | 0 | 24 | 2 PNG | `conferiu=true` | `limpo` | 33484 gracioso |
| **r4** | r3 (repetição + observador externo preservando o log cru) | `CONCLUIDO` | **`CONFIRMADA`** | 0 | 24 | 2 PNG | `conferiu=true` | `limpo` | 23996 gracioso |

Duração da coleta dentro do jogo: **3,95 s / 4,22 s / 4,35 s**; boot → estado terminal visto pelo
driver: **16,5 s / 15,5 s / 16,5 s**. Uma sessão de teste inteira (abrir → coletar → fechar) levou ~22 s.

## 2. Leitura do objeto VIVO (o que a rodada foi buscar)

24 observações por rodada, sobre **488** `TMP_Text` em memória. Textos reais lidos do objeto vivo
(exemplos, `texto_bruto`): `Game Menu`, `Path Chosen!`, `V-sync`, `Fullscreen Display`, `Resolution`,
`Language`, `Display Mode`, `Quality Preset`, `Send Gold`, `Split Item`, `Lionheart Breastplate gggg`,
`Message Title`, `Twitch Streamer Mode allows viewers of …`, `Your party lost the last battle. How w…`.
Por objeto o instrumento registrou: `objeto`, `caminho` na hierarquia, `componente`, `ativo_na_hierarquia`,
`visivel_na_tela`, `texto_bruto`, `texto_renderizado`, `fonte`, `material`, `shader`, `shader_suportado`,
`keywords`, `cores`, `geometria`, `tamanho_fonte`, `owners`, `personagem`.

- Fontes reais: **`Regular Font (Minion Pro Regular) SDF …`** e **`Title Font (Trajan Pro Regular) SDF …`**;
- Material: `… SDF Material`; Shader: **`TextMeshPro/Distance Field`**;
- Cores (texto/face/contorno/sombra) e geometria presentes em **24/24** observações;
- `aplicacao`: **Stolen Realm 1.3.1**, Unity **2022.3.62f2**, **1920x1080**, `WindowsPlayer`.

**Agregados** (porte do CAP-1 em componente isolado):
- `inventario`: 488 textos, **18 `TMP_FontAsset` em memória**, inventário por shader/fonte e
  `textos_com_efeito_no_material` com o critério **espelhado do BetterFont** (`SombraDesenhada`);
- `textos_visiveis`: só o texto **renderizado** desenhado — na r3, `Path Chosen!` em
  `GUI Manager/Chosen Node Display (KEEP ACTIVE)/Text`, caixa na tela **178,92 × 42,3 px** em 1920×1080;
- `fontes`: 18 fontes com material/shader/atlas/glifos.

**PNG pela API do Unity** (`ScreenCapture.CaptureScreenshot`): `01-ui.png` e `02-final.png` por rodada,
**2,5–2,8 MB** cada, 1920×1080, posteriores ao lançamento. O `01-ui.png` da r2 foi **inspecionado
visualmente** por mim: é a tela de **LOADING** do Stolen Realm, com o texto de dica *“Difficulty
Scaling — Game difficulty scales with the size of your party…”* renderizado e a palavra `LOADING`.
Não é quadro preto nem imagem sintética.

**Owners Harmony** (`Harmony.GetPatchInfo` no método vivo, não presunção):

```
GUIManager.Update        -> owners: ["com.gumatos.aut4probe"]
OptionsManager.Localize  -> owners: ["com.gumatos.aut4probe"]
Tooltip.ShowTooltip      -> owners: []      (o probe CHAMA o handler; nao o patcheia)
Tooltip.ShowSkillTooltip -> owners: []
```

Honestidade aqui: no perfil **isolado** só o instrumento está carregado, então o único owner vivo é o
**próprio probe**. O que ficou provado é que os owners são **lidos do Harmony em execução** — não que
um mod de terceiro apareça.

## 3. Ida-e-volta (o critério de leitura reproduzível)

Por rodada, o driver **gerou** um marcador único e o injetou no `.cfg`; o probe chamou o handler REAL
`Tooltip.ShowTooltip(marcador)` e **releu** `Tooltip.Title`:

| rodada | marcador (do driver) | `titulo_lido` | `conferiu` |
|---|---|---|---|
| r2 | `AUT4-IDA-E-VOLTA-AUT4-20261009-185146-8504fd5b` | **igual ao marcador** | **true** |
| r3 | `AUT4-IDA-E-VOLTA-AUT4-20261009-185246-59e9796e` | **igual ao marcador** | **true** |
| r4 | `AUT4-IDA-E-VOLTA-AUT4-20261009-185335-54b1bed3` | **igual ao marcador** | **true** |

`titulo_renderizado_lido` saiu `""` nas três: o `Tooltip` lido está **inativo** no menu e o TMP só
preenche o mesh com o objeto ativo — é o mesmo fallback declarado do resto da coleta (nunca
apresentado como leitura renderizada). O driver **exige** o marcador do driver: `conferiu=true` sem
ele não fecha (A6/COR-AUT4-F2).

## 4. Isolamento medido, rollback e encerramento

`hash_tree` do dono **antes** (18:46) × **depois** das três rodadas (18:53) — **diff vazio**:

```
perfil_plugins  6eae7a3c…  == 6eae7a3c…
perfil_core     b1594200…  == b1594200…
perfil_log      9bedadac…  == 9bedadac…
saves_hash      04ef12fa…  == 04ef12fa…
```

- `find <perfil do dono> -newermt '2026-10-09 18:46' -type f` → **vazio** (nenhum arquivo do dono
  escrito depois que a sessão dele terminou);
- `find <perfil do dono> -iname '*AUT4*'` → **vazio** (nada instalado no perfil do dono);
- `restauracao.limpo == true` nas **três** rodadas (`residuos`, `divergentes`, `faltando`,
  `dirs_residuo` todos vazios): o probe, o `.cfg` e o log da rodada voltaram ao estado de antes;
- **encerramento**: nas três rodadas o PID só nasceu nesta rodada (`pids_antes=[]`) e fechou na
  **primeira** tentativa, **graciosa** (`CloseMainWindow` → `fechado: true`); o fallback forçado por
  PID **não foi acionado**. Nada de `taskkill /IM`, nada de tocar processo do dono (não havia).
- **Frente única** respeitada: lock `acquire` antes, `release` depois (holder inicial PID 978).

## 5. Evidência BRUTA do log — a prova independente de que o BepInEx rodou NA CÓPIA (r4)

O rollback exato **remove** o `LogOutput.log` da rodada (é o que ele deve fazer) — por isso, na r4,
um observador externo copiou o log da **cópia** no instante em que o chainloader terminou:
`docs/automacao/AUT-4-evidencias/r4-confirmada-log/LogOutput-copia.log`, 1312 bytes, integral:

```
[Message:   BepInEx] BepInEx 5.4.23.5 - Stolen Realm (12/09/2026 21:34:42)
[Info   :   BepInEx] Running under Unity v2022.3.62.7762112
[Info   :   BepInEx] CLR runtime version: 4.0.30319.42000
[Info   :   BepInEx] Supports SRE: True
[Info   :   BepInEx] System platform: Bits64, Windows
[Message:   BepInEx] Preloader started
[Info   :   BepInEx] Loaded 1 patcher method from [BepInEx.Preloader 5.4.23.5]
[Info   :   BepInEx] 1 patcher plugin loaded
[Info   :   BepInEx] Patching [UnityEngine.CoreModule] with [BepInEx.Chainloader]
[Message:   BepInEx] Preloader finished
[Message:   BepInEx] Chainloader ready
[Message:   BepInEx] Chainloader started
[Info   :   BepInEx] 1 plugin to load
[Info   :   BepInEx] Loading [AUT-4 Probe (coletor runtime, instrumento) 0.1.0]
[Info   :AUT-4 Probe (coletor runtime, instrumento)] AUT4 PROBE 0.1.0 carregado (coleta AUTORIZADA, somente leitura).
[Info   :AUT-4 Probe (coletor runtime, instrumento)] AUT4 PROBE: gancho aplicado em GUIManager.Update()
[Info   :AUT-4 Probe (coletor runtime, instrumento)] AUT4 PROBE: gancho aplicado em OptionsManager.Localize(3 arg)
[Info   :AUT-4 Probe (coletor runtime, instrumento)] AUT4 PROBE: subsistema injetado no PlayerLoop (Update) — motor por quadro ativo.
[Message:   BepInEx] Chainloader startup complete
```

Isto é o log **da área isolada** (não o do dono): o Preloader é o da cópia, **1 plugin** foi
carregado e é **o probe** — o único mod da cópia. A identidade do binário que leu aparece também
dentro do JSON do instrumento: `identidade.arquivo_dll_do_probe =
…\scratch\aut4-runtime-iso\BepInEx\plugins\AUT4Probe\AUT4Probe.dll` e
`hash_dll_do_probe == 407c5c63…` (sha256 **calculado em runtime** sobre o assembly carregado).

## 6. Reproducibilidade da leitura

As três rodadas deram a **mesma assinatura** de leitura viva — o par (`objeto`, `texto_bruto`) de
**24/24** observações é **idêntico** entre r2, r3 e r4; `total_tmp_text = 488` nas três; cada rodada
com **sessão própria** e ida-e-volta confirmada com o **seu** marcador. Repetível, e não uma cópia
do mesmo arquivo (JSONs distintos, gerados em boots distintos).

## 7. O que o instrumento NÃO fez

- Não navegou (`Navegar=false`; navegação **não autorizada** pelo KIT-G1);
- Não carregou save, não abriu combate, não escreveu em nada do jogo (`aviso` do JSON: “Coleta SOMENTE
  leitura; nenhum mod do pacote foi alterado”);
- Não ficou instalado: saiu no rollback da própria rodada; a área isolada inteira foi removida no fim
  (`scratch/aut4-runtime-iso` — ver `AUT-4-parte04.md` §5).
