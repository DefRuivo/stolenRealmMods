# CHG-REV — revisão factual dos CHANGELOGs (9 pacotes)

Data da auditoria: **2026-10-16**. Escopo: os 8 mods + a API. Nada foi publicado, instalado ou bumpado;
`version_number` de nenhum `manifest.json` foi alterado; nenhum arquivo de código foi alterado.

## Método e evidências

- **Versões:** comparação do título de versão mais recente de cada `CHANGELOG.md` com o `version_number`
  do `manifest.json` ao lado (os dois lidos do working tree).
- **Entradas reais:** cada commit citado no changelog foi conferido com `git log -1` (existência **e**
  assunto). 30 commits citados, 30 confirmados (lista em *Evidência de commits*).
- **Datas de publicação:** obtidas da API pública do Thunderstore (`latest.version_number` e
  `latest.date_created`), convertidas para BRT (UTC−3).
- **Pacotes publicados intactos:** os 6 ZIPs publicados foram baixados do CDN e o `CHANGELOG.md` de dentro
  de cada um comparado byte a byte (normalizando CRLF) com `git show HEAD:<mod>/CHANGELOG.md`:
  **6/6 idênticos**. Ou seja, as correções deste relatório **não** contradizem nada que já está no ar;
  elas descrevem o que mudou *depois* da publicação.
- **RealmApi:** claims conferidos em `api/Core`, `api/Hooks`, `api/Plugin` e `api/docs/smoke-result.json`
  (62 aprovados, 0 falhas).

Comando da conferência de ZIPs (reproduzível):

    python - <<'EOF'
    import zipfile, subprocess, os
    for m in ["BetterCombatText","BetterFont","BetterStats","BetterTooltips","RoguelikeDebugger","RoguelikeSkillTreeVisualizer"]:
        zf = zipfile.ZipFile(f"{m}-public.zip")
        head = subprocess.run(["git","-C","C:/dev/stolen-realm","show",f"HEAD:{m}/CHANGELOG.md"],capture_output=True).stdout
        for n in [n for n in zf.namelist() if n.lower().endswith("changelog.md")]:
            print(m, n, zf.read(n).replace(b"\r\n",b"\n") == head.replace(b"\r\n",b"\n"))
    EOF

## Tabela por mod

| Mod | versão manifest | versão changelog (mais recente) | casa? | entradas faltando (corrigidas) | entradas falsas (corrigidas) | ação |
|---|---|---|---|---|---|---|
| BetterCombatText | 0.1.2 | `Unreleased` + 0.1.2 (2026-10-07) | **sim** | dependência BetterFont 1.0.2→1.0.3 do pacote 0.1.2 (`0d33ef3`); BF-5 já implementado em `27b5e69` descrito como conserto futuro; retirada da dependência BetterFont (DEP-REV, hoje) sem registro | "Documentation release. No code change" (o pacote mudou README **e** dependência); "o atual é 0.1.2 → BetterFont 1.0.3" (o manifest do repo não declara mais BetterFont); `Fundo` descrito como decidindo polaridade só em `Fundo=auto` | 8 correções + **seção `Unreleased` nova** (estado atual do manifest) |
| BetterFont | 1.0.3 | 1.0.3 (2026-10-07) | **sim** | marcos de commit (`5a13c64`, `6cdd448`, `8c90483`, `254c9a2`, `2a93297`, `634e88b`, `27b5e69`, `0d33ef3`) | "behaves exactly like 1.0.2; the DLL differs only in the version string it reports" — afirmava identidade byte a byte fora do literal (não verificável) | 3 correções |
| BetterPortuguese | 0.1.0 | 0.1.0 (em preparação; implementação 2026-10-13) | **sim** | alteração do ícone local depois de `917c20a` | nenhuma encontrada | 2 correções (título/nota de data + ícone) |
| BetterStats | 1.0.2 | 1.0.2 (2026-10-07) | **sim** | marcos de commit (`5a13c64`, `254c9a2`, `c3d3aab`, `0d33ef3`) | subseção do aplicador de ganchos atribuía o conserto à **1.0.0** "sem subir número" — a correção saiu na **1.0.1** (`254c9a2`→`c3d3aab`), duplicando a entrada | 3 correções |
| BetterTooltips | 0.1.4 | 0.1.4 (2026-10-07) | **sim** | DWA-2 (`46fde11`), CHL-1 (`c5eeb5c`), COR-1/2/3 (`d586f28`), BT-10..13/NIV3-1/ARM-1 (`716ca22`), TX-1 (`95ca3f3`), RV-28 (`573596d`), `46acd97` | "`Worship` perk" tratado como fato; "doubling = defeito do próprio mod"; auras de perigo liam o bônus do **santuário**; "28% com os dois tiers" como resultado validado (a matriz de `573596d` registra 8/16 e 20/40 — **nunca 28/56**); RV-46 como regra universal "cada aura conta uma vez" (DWA-2 mudou) | **maior bloco** (115 linhas): 7 retratações/registros |
| RoguelikeDebugger | 0.1.2 | `Unreleased` + 0.1.2 (2026-10-07) | **sim** | proveniência `DBG-PROV-V1` (`097f950`); API opcional por reflexão; matriz Flame classificada como leitura **ativa** (`Game.EvalVoid`) | "Nada muda no jogo: o que muda é o TEXTO do log"; seção RD-2 atribuída à **0.1.1** ("a versão NÃO muda / dump ainda não lançado"), mas ela foi consolidada na **0.1.2** (`51a4aa5`→`88232fe`) | 5 correções + **seção `Unreleased` nova** |
| RoguelikeSkillTreeVisualizer | 0.3.3 | `Unreleased` + 0.3.3 (2026-10-07) | **sim** | integração UI `INT-R1-C4` (`097f950`): `UIFactory.Clone`/`BindClick`, `UiFamily.Bind`, e a dependência **HARD** `com.gumatos.realmapi` ≥ 0.1.0 | "The current Thunderstore manifest still declares only BepInEx" — falsa depois do DEP-REV de hoje (o manifest do repo declara RealmApi 0.1.0) | 4 correções + **seção `Unreleased` nova** |
| RoguelikeUnlimitedLevelProgression | 0.1.1 | 0.1.1 (em preparação; revisado 2026-10-16) | **sim** | **causa raiz** (o próprio `Plugin.OnDestroy` chamava `UnpatchSelf()` e desligava `GameplayGroupApplied`) e a correção; instrumentação RLP-1/2; failsafe pós-batalha; marcos de commit (`cd8e4ce`, `d1de4ea`, `8cabbe5`, `941e3c3`, `06564ce`, `931bcc4`); rename do pacote e ícone | 0.1.0 descrito como "Primeira versão" (nunca publicado); cabeçalho "Não publicado — identidade do pacote (13/10/2026)" misturava o rename com a versão 0.1.1; "Ícone `RU` 256×256" não corresponde à arte atual | 4 correções + **causa raiz registrada** |
| RealmApi (api/) | 0.1.0 | 0.1.0 (revisado em 2026-10-16) | **sim** | não existia `api/CHANGELOG.md` (arquivo **criado** nesta auditoria) | n/a (arquivo novo) | **criar** changelog descrevendo a API como ela é hoje |

**9/9 títulos de versão casam com o `version_number`.** Não há qualquer "Unreleased" declarando versão já
publicada: as duas seções `Unreleased` (RD, RSTV) e a de BCT descrevem mudanças **posteriores** ao pacote
publicado de 2026-10-07 e dizem isso explicitamente.

## O que eu corrigi

As correções de texto foram produzidas pela **rodada anterior desta mesma tarefa** (`run 1594`, morta por
quota às 13:33) e ficaram no working tree sem relatório. Nesta rodada eu **conferi cada uma** contra o
`git log` real (30/30 commits citados existem e têm o assunto alegado), contra os manifests, contra a API
pública do Thunderstore e contra os ZIPs publicados — e acrescentei **3 correções próprias**:

1. **BetterCombatText** — a nota do bloco histórico afirmava que o manifest atual era "0.1.2 → BetterFont
   1.0.3". Falsa desde a auditoria de dependências de hoje (o manifest do repositório deixou de declarar o
   BetterFont). Reescrita separando o **pacote publicado** do **manifest do repositório**, com a razão
   (o código não referencia o BetterFont; a única menção é o comentário `Plugin.cs:101`).
2. **RoguelikeSkillTreeVisualizer** — a entrada `Unreleased` dizia que "the current Thunderstore manifest
   still declares only BepInEx". Falsa pela mesma razão (hoje o manifest do repo declara
   `DefRuivo_StolenRealmMods-RealmApi-0.1.0`). Reescrita distinguindo pacote publicado de manifest do repo.
3. **BetterCombatText** — **seção `Unreleased` nova**, para o leitor não precisar garimpar a nota histórica
   para saber o que o manifest diz hoje (mesmo padrão já usado em RD e RSTV).

Resumo do que foi corrigido, por tipo:

- **Datas** — 6 pacotes passaram a ter a data de publicação real (`2026-10-07`, BRT) no título; cabeçalho
  padrão declara ISO 8601 (BRT, UTC−3) e que títulos antigos sem data **não** afirmam data de lançamento.
  Datas conferidas na API pública: as seis versões do topo têm `latest.version_number` igual ao manifest e
  `latest.date_created` em **2026-10-07 18:24–18:25 BRT**.
- **Falsidades** — 14 afirmações retiradas ou reescritas (as mais graves: o "`Worship` perk", que é
  fabricação; o "doubling é defeito do mod"; o "28%" como resultado validado; "nada muda no jogo no
  RoguelikeDebugger"; o conserto do aplicador atribuído à 1.0.0 publicada).
- **Lacunas** — 9 registros que existiam no `git log` e não no changelog: dependência BCT→BF 1.0.3
  (`0d33ef3`), BF-5 (`27b5e69`), DWA-2/CHL-1/COR-1..3/BT-10..13/TX-1/RV-28, proveniência `DBG-PROV-V1`
  (`097f950`), integração UI do RSTV (`097f950`) e a **causa raiz do ULLP**.
- **Formato** — numeração em ordem decrescente em todos os 9; títulos `## <versão> — <data>` uniformes;
  títulos de etapa histórica (`###`) marcados como "incorporado/superado", para não parecerem releases
  paralelas.

## Achados residuais (não corrigidos de propósito)

1. **`BetterCombatText/README.md:9,43-49`** ainda diz que o BetterFont é obrigatório. É README, não
   CHANGELOG — fora do escopo desta tarefa; fica para o **PUB-ALL-1** ao alinhar o pacote.
2. **Versões antigas sem data** (BCT 0.1.1, BF 1.0.2/1.0.1/1.0.0, BS 1.0.1/1.0.0, BT 0.1.3..0.1.0,
   RD 0.1.1/0.1.0, RSTV 0.3.2..0.1.0). Não há evidência de dia exato para elas além de commits de lote;
   o cabeçalho declara a ausência de afirmação em vez de inventar data.
3. **A API não foi executada em runtime** — o changelog da API diz isso explicitamente (62/0 é suíte
   *offline*). Este relatório não abre o jogo.
4. **A "Unreleased" de BCT/RSTV não é uma versão** — são mudanças de manifest/código ainda sem bump; o
   bump é do PUB-ALL-1.

## Evidência de commits (conferidos: 30/30)

`0d33ef3` bump 07/10 dos 6 mods + BCT passa a exigir BetterFont 1.0.3 · `27b5e69` entregas 02/10 (BF 1.0.2 +
BCT 0.1.1 + RSTV 0.3.0) · `254c9a2` CORRECAO GRAVE do aplicador gancho a gancho · `c3d3aab` bump dos mods do
conserto A-1 · `5a13c64` primeira entrega documentada · `ac0210f` lote de correção/dependência ·
`097f950` checkpoint 11/10 (proveniência RD + integração UI do RSTV) · `51a4aa5` RD-2R gatilho/tick/expressões ·
`88232fe` RD 0.1.2 bump + changelog honesto · `941e3c3` rename do ULLP · `8cabbe5` ícone 256×256 + publicar:false ·
`d1de4ea` R3-01 clamp de carga · `cd8e4ce` implementação LEVEL-R2 · `06564ce` lib na raiz do checkout ·
`931bcc4` marcador de boot `carregado.` · `917c20a` BetterPortuguese snapshots · `69c4a56` BF-2/BF-2R + BCT 0.1.1
dependência · `bc4e5d6` ícone real do BCT · `6cdd448`/`8c90483` BF 1.0.1 estilo e BF-1 · `2a93297`/`634e88b`
BF 1.0.2 transporte entre variantes e teto do diagnóstico · `46fde11` DWA-2 · `c5eeb5c` CHL-1 · `d586f28` COR-1..3 ·
`716ca22` BT-10..13/NIV3-1/ARM-1 · `95ca3f3` TX-1 · `573596d` RV-28 blindagem (8/16, 20/40, nunca 28/56) ·
`bc394e7` RV-46 · `46acd97` BT-TX-2/CHK-1.

## Handoff

Mudanças no working tree, **sem commit e sem publicação**: os 8 `CHANGELOG.md` rastreados + `api/CHANGELOG.md`
novo. A filha **PUB-ALL-1** (`t_d00f2bc6`) usa estas correções para escrever as entradas das novas versões.
