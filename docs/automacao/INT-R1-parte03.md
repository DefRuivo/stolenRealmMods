# INT-R1 — parte 03: varredura de defasagem e duplicação (4 baldes)

Base: `21` cartões vivos no board (`~/.hermes/kanban.db`, medido nesta rodada — parte 01 §2.1) + artefatos
vivos do repo (parte 01 §2.2) + as duas entregas em anexo (LANG-R1, DBG-R1).
Regra: cada item recebe **um** balde e **uma** linha de justificativa. Item em `[DEFASADO]`, `[DUPLICADO]`
ou `[SIMPLIFICAVEL]` ganha cartão (ou, quando já coberto por outro item, a cobertura é declarada
explicitamente). `[INTACTO]` só entra aqui.

## 1. Tabela de baldes

| Item | Balde | Justificativa (1 linha) |
|---|---|---|
| `ReloadProbe/` (67 linhas, **0** `HarmonyPatch`) | **[DEFASADO]** | Probe abandonado (INFRA-3/4/5 arquivadas: hot-reload não funciona neste jogo); a função foi absorvida por `scratch/test-cycle.sh` + leitura de log e, na observação, pelo `AUT4Probe` |
| `docs/cobertura/DUMP-TOOLTIPS-REVISAO.md` (4.516 linhas), `DUMP-DEBUFFS-REVISAO.md`, `DUMP-PASSIVAS-REVISAO.md` — parte **chaveada** | **[DEFASADO]** | Para o texto que passa pelo dicionário, `LANG-R1` entregou a tabela completa `chave→ptbr/en` (9.090 chaves) e o dump manual vira regenerável dela |
| `docs/cobertura/auditoria-tooltips.md` | **[INTACTO]** | É auditoria de **conteúdo/mecânica** (checagens A..H do RV-8b), não de localização: LANG-R1 não toca número de skill |
| `docs/cobertura/*.csv` (skills 452, skills-detalhe 454, status 561, itens 906, afixos 286, acoes 288, powerups 80, invocacoes 19) | **[SIMPLIFICAVEL]** | O caminho de regeneração **já existe** (`tools/census.py` lê o dump de boot; `tools/preserva_curado.py` guarda a coluna curada) — o que falta é **proveniência do instrumento**, e isso é o mesmo item do `RoguelikeDebugger` (coberto pelo cartão C3, sem cartão próprio) |
| `tools/*.py` (26 scripts offline: `census.py`, `audit_tooltips.py`, `verify_tree.py`, `check_*.py`…) | **[INTACTO]** | Operam sobre CSVs/assembly, não sobre o jogo; a API é in-game e observacional |
| `KIT-13` — `tools/automacao/kit13` (`Gumatos.KitSdk.V1`: `IExtensionV1`, `EventV1`, `ReadingV1`, `VerdictV1`, `RegistryV1`) | **[DUPLICADO]** | Núcleo versionado de eventos+registro+veredito concorrente com `RealmApi.Core` (`Signal<T>`, `HookNotification`, `ApiIdentity`): dois contratos ou um é dependência do outro |
| `AUT4Probe`/`CAP-1` — `tools/automacao/runtime/AUT4Probe` (observação) | **[SIMPLIFICAVEL]** | A observação que o probe faz por reflection própria coincide com os 4 hooks do catálogo; a parte de **input** não tem família no inventário (dobrado no cartão C2) |
| `AUT4Probe` — clique/navegação (`AUT4ProbePlugin.cs:1030`, `botao.onClick.Invoke()`) | **[INTACTO]** | O defeito `t_139f714f` (`0xc0000005`) é de **entrada sintética**; a API 0.1.0 não dirige input nem o inventário tem família de input |
| `RoguelikeDebugger` (14 classes Harmony em 10 arquivos) | **[SIMPLIFICAVEL]** | Adota o gate de identidade/proveniência da API (lacuna nº 1 do `DBG-R1-parte07.md` §1) sem virar dependência dura |
| `BetterTooltips` (9.251 linhas) | **[SIMPLIFICAVEL]** | O patch próprio **fica** (a API não reescreve `__result`), mas o hook `ui.localized` passa a alimentar a **cobertura das tabelas** por medição |
| `BetterFont` (único patch = gatilho em `Localize`) | **[INTACTO]** | O alvo coincide com o hook `ui.localized`, mas a **necessidade** é outra (disparar `FontUpdater`); migrar trocaria 1 linha por uma dependência dura num gate fail-closed |
| `BetterStats`, `BetterCombatText` | **[INTACTO]** | Nenhum de seus alvos está nos 4 hooks ou nas 7 famílias do inventário, e ambos **mutam** UI (fora do escopo observacional) |
| `RoguelikeSkillTreeVisualizer` (6.946 linhas) | **[SIMPLIFICAVEL→MIGRAR condicional]** | O que ele escreve à mão coincide com a família `UI` do inventário; como a família não existe, o cartão depende do cartão que a implementa (C1) |
| `t_9e2325d7` DBG-R1 (review) | **[INTACTO]** (entrega) / **[SIMPLIFICAVEL]** (fatia P0) | A auditoria entregue permanece válida; a fatia P0 "saber qual DLL observou" é o que a API simplifica (tratada no cartão C3) |
| `t_2a6474ff` LANG-R1 (running) | **[INTACTO]** | É **fonte** para outras frentes (os dumps e os 5 gates humanos), não candidata a substituição |
| `t_71e4b22a`, `t_15176486`, `t_0bddb861`, `t_ec66f0bb`, `t_4da3d8a7` (LANG-C1..C5) | **[INTACTO]** | Aprovação **humana** de texto; a API não muda a resolução de string (`ui.localized` é postfix observacional em `OptionsManager.Localize`, sem alterar chave/tabela/resultado) |
| `t_004ed4b0`, `t_34205427`, `t_55517882`, `t_8e74c724`, `t_b10171fa` (EV-R2×5) | **[INTACTO]** | Aprovação **humana** de eventos; nada na API ou no debugger decide conteúdo de evento |
| `t_9ce7d260` KIT-14R, `t_a1f38855` KIT-14, `t_a41dd22d` KIT14G-SEG1-RT, `t_139f714f` KIT14G-SEG2, `t_dc6125a6` KIT-00, `t_b001720d` KIT-G4 | **[INTACTO]** | São prova/entrega/aceite do **próprio kit**; a ferramenta nova muda o instrumento por baixo, não o critério de aceite |
| `t_cda5afa8` LEVEL-R3 (+ `t_918314e9` LEVEL-R2) | **[INTACTO]** | Mod + revisão independente de progressão de nível; a API 0.1.0 não expõe nível e `Skills.SkillRegistry` do inventário é criação de skill, não teto |
| `t_d87ea54d` API-R1-R1 | **[INTACTO]** | É a revisão da própria API — referência desta análise |
| `t_ecb8f32d` INT-R1 (este cartão) | **[INTACTO]** | Meta: a própria varredura |
| `ITEM_INVENTORY.md`, `ITEM_MOD_INVENTORY.md`, `SKILL_INVENTORY.md`, `STATUS_INVENTORY.md`, `TOOLTIP_SWEEP.md` (raiz do repo) | **[DEFASADO] — já tratado** | Superados pelo censo em `docs/cobertura/*.csv`; já retirados do rastreamento pelo INFRA-12 (`git rm --cached` + `.gitignore`). Nada a fazer — registro |
| `api/` (`Core`, `Hooks`, `Plugin`, `Smoke`, `tools/Inspect`, `docs`) + `DeployToBepInEx` opt-in | **[INTACTO]** | É o insumo desta revisão e já tem runbook/evidência de deploy opt-in (`docs/automacao/API-R1-runbook-runtime.md`) |

### Contagens por balde

| Balde | Itens | Cartões gerados |
|---|---:|---:|
| DEFASADO | 3 itens (1 `ReloadProbe/`; 3 dumps: `DUMP-TOOLTIPS/DEBUFFS/PASSIVAS-REVISAO.md`; 5 notas de IA da raiz) — `auditoria-tooltips.md` NÃO é defasado | **1** (C6 = dumps). ReloadProbe e as notas da raiz **já estavam tratados** (`.gitignore:45`, `git ls-files` = 0) → sem cartão |
| DUPLICADO | 1 (KIT-13 SDK × RealmApi.Core) | 1 (C2) |
| SIMPLIFICAVEL | 6 (debugger, censos, AUT4Probe-observação, BetterTooltips, RSTV, DBG-R1-fatia-P0) | **3** (C1 família UI→RSTV, C3 debugger/proveniência, C5 BetterTooltips) — censos e AUT4Probe-observação não geram cartão próprio: são o **mesmo** instrumento de C2/C3 |
| INTACTO | 30+ | 0 |

## 2. Checklist do operador — confirmado, refutado ou ampliado

> O operador pediu explicitamente: "confirme, refute ou amplie — não repita o trabalho, verifique".

### Item 1 — `DUMP-TOOLTIPS-REVISAO.md` e `auditoria-tooltips.md` × dump de localização do LANG-R1

**Resultado: CONFIRMADO PARA UM, REFUTADO PARA O OUTRO.**

- `DUMP-TOOLTIPS-REVISAO.md` — **confirmado em parte**: ele é gerado a partir do censo e serve à revisão
  humana dos textos. Para tudo que passa pelo dicionário (`OptionsManager.Localize`), a tabela do LANG-R1
  (9.090 chaves, colunas `chave`/`en`/`ptbr`/`alertas`/`decisao_dono`) é agora a fonte completa e
  regenerável. **Limite medido**: as descrições de **status** não passam por esse dicionário — o próprio
  projeto registrou isso no KANBAN (`BT-6`: "status NÃO estão no dicionário de localização — descrições são
  campos brutos dos assets"), e `relatorio-suspeitos.md` declara cobertura só "da localização serializada
  inspecionada". Ou seja: o dump **não** é 100% absorvido; a parte de asset cru fica.
- `auditoria-tooltips.md` — **refutado**: é auditoria de conteúdo/mecânica de skill (checagens A, B, C, D,
  E2, E, G, H em `tools/audit_tooltips.py`), fechada em 2.280/2.280 vereditos
  (`docs/cobertura/auditoria-cobertura.md`). Nada aí depende de texto localizado nem é coberto por um dump
  de localização.

### Item 2 — censos `docs/cobertura/*.csv` × censos do debugger aprimorado

**Resultado: REFUTADO (o caminho já é o proposto) + AMPLIADO.**

- Os CSVs **não são mantidos à mão**: `tools/census.py` declara no cabeçalho que lê "o dump de boot do
  `RoguelikeDebugger` (`LogOutput.log`)" e gera o checklist por categoria. O que é manual é a **coluna de
  veredito**, preservada entre regenerações por `tools/preserva_curado.py` — e isso deve continuar manual
  (é o trabalho de revisão em si).
- **Ampliação (o que realmente falta):** "regerar a partir do instrumento" só é confiável se o instrumento
  **provar o que observou**. É literalmente a lacuna nº 1 do `DBG-R1-parte07.md` §1: "saber qual DLL
  observou, **se o dump terminou**, o que não foi alcançado e se uma leitura era realmente passiva". Isso
  vira o cartão **C3**.

### Item 3 — KIT-13 (SDK pequeno e cenários declarativos) × API nova

**Resultado: CONFIRMADO — há duplicação real, e nenhum absorve o outro.**

- KIT-13 (`tools/automacao/kit13`): núcleo **sem Unity/BepInEx/jogo** (`KIT-13-entrega-final.md`,
  "Núcleo netstandard2.1 sem Unity/BepInEx/jogo") com `IExtensionV1`, `EventV1`, `ReadingV1`, `VerdictV1`,
  `RegistryV1`; pacotes declarativos `KIT13/scenario/1` com schema fechado; executor/`FrenteUnica` do KIT-11.
- API-R1 (`api/Core/Contracts.cs`): `Signal<T>`, `HookNotification`, `ApiIdentity` (gate fail-closed),
  `RealmAccess.ReadProperty`.
- **Diagnóstico:** são **dois núcleos de contrato versionado** desenhados para o mesmo problema (registrar
  observadores, versionar contrato, isolar erro de extensão). A diferença legítima de hoje é de **papel**:
  a API é o **produtor** in-game (Harmony, dentro do processo), o SDK é o **consumidor/validador** fora do
  jogo (Unity-free, cenários, veredito). Não há ponte entre os dois — essa ponte é a decisão de
  arquitetura e vira o cartão **C2** ("quem é dependência de quem").
- Registro honesto: o KIT-13 já tem `CoreBridge/CorePluginBinding.cs` (facade sobre os métodos públicos do
  Core do **kit**) — ou seja, o padrão de ponte existe dentro do kit; o que falta é a ponte para o núcleo
  da **API**.

### Item 4 — AUT4Probe/CAP-1 × hooks/eventos expostos pela API

**Resultado: CONFIRMADO EM PARTE.**

- **Observação:** sobreposta — o probe observa por código próprio o que os 4 hooks cobrem. Simplificável
  (dobrado no cartão **C2**, que é a ponte de eventos).
- **Input:** **não** coberto. Não existe família de input no inventário (as 7 famílias são `Combat`,
  `Skills`, `Quests`, `Enemies`, `UI`, `Data`, `ContractReference`), e o gate `EnableHooks` da API é
  observacional. O defeito aberto `t_139f714f` (clique sintético → `0xc0000005` em `ntdll.dll`) **continua
  valendo** e nenhum artefato da API o toca.

### Item 5 — cartões vivos do KIT e do LEVEL ficam defasados?

**Resultado: CONFIRMADO — NÃO ficam defasados.**

Verificado um por um: KIT-14 (`t_a1f38855`) e KIT-14R (`t_9ce7d260`) provam o kit ponta-a-ponta;
KIT14G-SEG1-RT (`t_a41dd22d`) prova por arquivo+contagem que `probe/recorder.json` traz `eventos > 0`;
KIT14G-SEG2 (`t_139f714f`) registra o defeito do clique; KIT-00 (`t_dc6125a6`) é o acompanhamento
(triage, sem assignee); KIT-G4 (`t_b001720d`) é o gate humano final. LEVEL-R3 (`t_cda5afa8`) revisa a
extração+mod de progressão. Em todos, **o instrumento por baixo é que muda** (é exatamente a suspeita do
operador) — nenhum perde sentido.

### Item 6 — LANG-C1..C5 continuam válidos? A API muda a resolução de string?

**Resultado: CONFIRMADO — continuam válidos; a API NÃO muda a resolução de string.**

- Prova: o hook `ui.localized` é um **postfix observacional** sobre `OptionsManager::Localize`
  (`api/Core/Contracts.cs:63`, forma `string` estática com `__result`) e `api/README.md:42,145-146`
  proíbe substituir argumentos/resultado nesta base. O jogo resolve `chave→texto` exatamente como antes.
- Os 5 cartões (`t_71e4b22a` C1, `t_15176486` C2, `t_0bddb861` C3, `t_ec66f0bb` C4, `t_4da3d8a7` C5) são
  aprovações humanas sobre a tabela do LANG-R1 — a API não interfere.

## 3. NAO_EXERCITADO desta parte

- Nenhuma migração foi executada (`LIMITES` do cartão).
- A "proveniência" proposta para o debugger (C3) é desenho, não medição: não houve rodada de jogo.
- A paridade entre a tabela do LANG-R1 e os textos das tabelas do `BetterTooltips` **não foi medida**
  nesta rodada (exigiria cruzar `localizacao-ptbr.csv` com as tabelas C# — trabalho do cartão C6).
