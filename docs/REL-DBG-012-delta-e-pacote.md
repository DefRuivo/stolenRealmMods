# REL-DBG-012 — delta real do RoguelikeDebugger e preparação da 0.1.2

> Tarefa: **t_87f8dce8** (`REL-DBG-012`) · Rodada: **07/10/2026, LOCAL**.
> Natureza: **preparação**. Nada aqui abre o jogo, instala no perfil, faz push, tag,
> GitHub Release, dispatch de workflow ou upload na Thunderstore; `publicar:true` não foi
> tocado. Fechar esta preparação **não** é o DoD do mod nem aprovação de publicação.
> Revisão independente: **t_b2ae99df** (revisor ≠ autor).

---

## 1. Resumo do que foi decidido

O mod **não** era um caso "só documentação": o ZIP publicado na Thunderstore é
**anterior** ao dump do RD-2 (01/10) e ao probe `[FlameRV49]` (06/10), e o próprio ZIP
local (`dist/`, 04/10) é anterior ao probe. Três DLLs diferentes respondem por "0.1.1".

A 0.1.2 foi preparada com: bump nos **quatro** lugares, changelog honesto, texto público
em inglês, `dotnet build -c Release -p:DeployToBepInEx=false` e repack **depois** da
última edição, com prova por **decompilação do DLL extraído do ZIP** e comparação
**byte a byte** ZIP × build.

---

## 2. Três artefatos chamados "0.1.1" (e por que a diferença importa)

| artefato | como foi obtido | sha256 do ZIP | sha256 do DLL | versão no DLL | `FlameRV49` | `auraSts` / `~alvos=` / `TickTargets` |
|---|---|---|---|---|---|---|
| **público** 0.1.1 | `curl -sL https://thunderstore.io/package/download/DefRuivo_StolenRealmMods/RoguelikeDebugger/0.1.1/` | `6bd17a6d5ad997fddc011d0bf68a6527ef38ae72131ae2348a08d8fdacca7235` | `27dfe5a9fc3651f1f2e20b3e8e3a252908875e002f027021446ffcd0b2018dc3` | 0.1.1 | **0** | 0 / 0 / 0 |
| **dist local** 0.1.1 | `dist/gumatos-RoguelikeDebugger-0.1.1.zip` (04/10 02:11) | `41fd8c4b9b4b5805a4c06b39fa806956b1ce8523a81292ffe55c8d864f7bad7a` | `99c15679938097d9bc2bea8e9dec5ad6332e528da084ed70bde085d8f74c7d27` | 0.1.1 | **0** | 2 / 1 / 4 |
| **fonte de hoje** (pré-bump) | `dotnet build -c Release -p:DeployToBepInEx=false` | — | `81f150b45fb5aa71e3d6c3b87aca069aa0992bc6a9e9fdba610a17d850583e04` | 0.1.1 | **3** | 2 / 1 / 4 |

Contagens por `ilspycmd -o <dir> <dll>` + `grep -c` no `.decompiled.cs`
(`scratch/rel-dbg-012/decomp/{live,dist,fresh}/`).

Prova por API (pública, sem auth) de que **0.1.1 é a última publicada**:

```
GET https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/RoguelikeDebugger/
  latest.version_number = 0.1.1
  latest.date_created   = 2026-10-01T01:59:51.397143Z
  latest.description    = "Ferramenta de DESENVOLVIMENTO, nao e mod de jogador: ..."   <- em PORTUGUÊS
```

O `manifest.json` do repositório já traz a descrição em **inglês** — ou seja, a
**descrição da listagem** do pacote publicado está em português e só muda com versão nova
(metadado de versão é imutável).

### 2.1 Defeitos achados no pacote PUBLICADO (0.1.1) — não consertáveis sem versão nova

1. **O README publicado declara `- **Versão:** 0.1.0`** dentro do pacote que é 0.1.1
   (diff `live/README.md` × árvore). Afirmação falsa no texto público.
2. **O README publicado está em português**; o repositório já tinha a versão em inglês
   (commit `ddb6c3a`, 01/10 13:21) — posterior à publicação.
3. **A descrição da listagem está em português** (acima).
4. **O DLL publicado não tem o RD-2 nem o probe `[FlameRV49]`** — o pacote entregue é o
   mais antigo dos três.

---

## 3. Delta real desde a publicação

Commit publicado: `c3d3aab` (30/09 20:53, o da leva do run 36801937843). Comparação
`git diff --stat c3d3aab..HEAD -- RoguelikeDebugger`:

```
 RoguelikeDebugger/CHANGELOG.md                 |   9 +-
 RoguelikeDebugger/EfeitosInfo.cs               |  51 ++
 RoguelikeDebugger/Patches/ActionStatusInventoryPatch.cs | 302 ++++++--
 RoguelikeDebugger/Patches/FlameShrineProcPatch.cs       | 710 +++++++++++++++++++
 RoguelikeDebugger/README.md                    | 140 +--
 RoguelikeDebugger/RoguelikeDebugger.csproj     |  11 +-
 RoguelikeDebugger/manifest.json                |   2 +-
 7 files changed, 1086 insertions(+), 139 deletions(-)
```

| item | commit | o que é |
|---|---|---|
| campos `[Status]` do RD-2 (`expr`, `danoExpr`, `refAcao`/`refStatus`, `tick`, `auraSts`) + `~alvos=`/`~acoes=`/`~chances=`/`~cd=` no `trigEf` | `51a4aa5` (01/10) | dump, sem toque no jogo |
| RD-2F: guarda por campo (`!erro:<Tipo>`), laço sobre cópia, fim do corte por tamanho | `a2e4c18` (01/10) | dump, sem toque no jogo |
| DEPLOY-2 (deploy opt-in) no csproj + README | `82ff1af` (01/10) | **ferramenta de build** |
| `Patches/FlameShrineProcPatch.cs` (novo, 710 linhas) | `4e6588c` (06/10) | **instrumentação de diagnóstico** (RV-49) |
| README/manifest em inglês | `ddb6c3a` (01/10) → | texto público |

**Working tree não comprometido** (auditado, não inventado): `RoguelikeDebugger/README.md`
tinha uma edição **não commitada** trocando o parágrafo de build para o texto do DEPLOY-2
("a bare `dotnet build` installs **nothing**"). Ela foi **preservada** (não sobrescrita) e
entra no commit desta entrega. Nenhum outro arquivo do mod estava sujo.

**Concorrência observada:** às 03:22 desta rodada outro frente estava editando
`BetterCombatText/` (mtime 03:22:24, bump para 0.1.2). Nada disso foi tocado aqui; o build
desta tarefa foi só do `RoguelikeDebugger.csproj`. Os dois `dotnet.exe` vivos no momento
do build eram o backend do ILSpy do VS Code e o `VBCSCompiler` — **nenhum** build de repo
em curso (checado por `CommandLine` via CIM).

---

## 4. Flags, defaults, overhead e "altera gameplay?"

### 4.1 Não existe interruptor nenhum

`grep -rn 'Config\.|ConfigEntry|BaseConfig' RoguelikeDebugger/*.cs RoguelikeDebugger/Patches/*.cs`
→ **0 ocorrências**. O mod não cria `.cfg`; não há flag para ligar/desligar nada. O que
está no pacote roda **sempre** que o plugin carrega. (Item de aceite nº 2.)

### 4.2 O que roda por padrão

- **Dump de boot** (skills, `[ActionProps]`/`[Trigger]`, status, itens/afixos, powerups):
  pesado **por desenho** — milhares de linhas por boot. Não é novidade desta versão (está
  na 0.1.0/0.1.1) e é a razão de o README dizer "não distribuia para amigos".
- **`[FlameRV49]` (novo)**: só dispara no proc das duas auras de shrine de perigo.

### 4.3 O probe novo é limitado — e o limite é medido, não presumido

| afirmação | prova |
|---|---|
| só expressão que cita `ShrineEffectBonus` gera linha | `FlameProbe.Interessa` (IndexOf) é o filtro dos dois Prefix (`FlameShrineProcPatch.cs:71-74, 633-643, 661-664`) |
| essas expressões são só as 2 do proc das auras | `grep -c ShrineEffectBonus` no decompilado = **24**, e as 24 se distribuem assim: **18** = as **9 fórmulas de buff de aura** em `typeof(float)` (2 linhas cada: registro no cache + corpo do delegate), **4** = as **2 fórmulas do proc de perigo** em `typeof(void)` (Flame/Decay) e **2** = o teste de skill tree do próprio jogo (`LearnAndExpectAttributeDelta`) |
| `Game.EvalVoid` tem **uma** definição (sem overload) | `grep -E 'EvalVoid\(' Assembly-CSharp.decompiled.cs` → só `443912: public static void EvalVoid(string, GameFunctionParameters)` |
| `GetValueByEnemyType` (o `FlamePctPatch`, que **não** tem filtro) só é chamado por essas 2 fórmulas | `grep -c GetValueByEnemyType` = **5**: 1 definição (`39235`) + 2 fórmulas × (string do cache + corpo). Nenhum outro chamador. |

**Overhead do probe no proc:** 1 avaliação extra da string por variante da matriz —
**5 `Game.EvalVoid` a mais por proc** (5 variantes), todas com dicionários NOVOS.

### 4.4 Ele altera gameplay?

- As 14 classes de gancho do mod usam `Postfix` e `Prefix` que **devolvem `void`** (16
  métodos; nenhum `bool` de "pular o original") — conferido em `Patches/*.cs` e por
  `tools/check_patches.py` (0 reprovações). Logo o jogo executa exatamente o mesmo caminho.
- O probe mexe em **estado**, nunca em personagem: cria dicionários `SourceStored`/
  `TargetStored` novos, guarda e **devolve** `Game.CurrentGameFunctionParameters` no
  `finally` (`FlameShrineProcPatch.cs:335-368`), e só reavalia a matriz se a expressão
  passar em `FormaSegura` (uma ÚNICA atribuição, no início, do próprio dicionário).
  Leitura de dicionário do jogo passa por `ContainsKey` antes (o `SimpleDefaultDictionary`
  **insere na leitura**) — `AnexaCrus`, `:177-199`.
- Um efeito colateral **real e declarado**: `RegistrarTexto` acrescenta a string nova ao
  `CompiledDynamicExpresso.MissingExpressions` (campo estático privado do jogo) para
  suprimir o aviso "No Compiled Expression" por sessão. É estado do jogo, **não** gameplay,
  e falha de reflexão não suprime nada (`:270-290`).

**INDETERMINADO (não é verde):** o custo/hitch da matriz num combate real e a ausência de
efeito observável **não foram medidos em jogo** — ver §7.

---

## 5. Texto público (inglês), revisado

- `manifest.json` `description` (a linha da listagem): inglês, **172 chars** (≤ 250).
  Corrige o português que foi ao ar na 0.1.1.
- `README.md`: inglês (ferramenta de desenvolvimento, **não** mod para o jogador; "No
  gameplay change"; "Sends no data anywhere") + seção final **Português (BR)** — a mesma
  convenção dos outros 5 mods.
- **Novo no README desta versão:** bullet do probe de shrine e uma seção
  **"What is not verified in game yet"** declarando que as linhas do `[FlameRV49]` **não
  foram exercitadas em jogo** (RV-49 pendente).
- **Não distribui DLL/assembly do jogo:** o ZIP tem **5 arquivos**
  (`manifest.json`, `README.md`, `CHANGELOG.md`, `icon.png`, `plugins/RoguelikeDebugger/RoguelikeDebugger.dll`)
  e nenhuma `Assembly-CSharp.dll`/`lib/`. `icon.png` = **256x256**, 99.954 bytes.
- `RoguelikeDebugger.csproj` `<Description>` continua em português (não é publicado; não
  entra em nenhuma superfície da Thunderstore). Registrado aqui para não parecer descuido.

---

## 6. Pacote 0.1.2 — comandos, exit codes e provas

```
1) bump do <Version> no RoguelikeDebugger.csproj: 0.1.1 -> 0.1.2
2) python tools/pack-thunderstore.py --sincronizar-versao RoguelikeDebugger   -> exit 0
     manifest.json: 0.1.1 -> 0.1.2 | Plugin.cs: 0.1.1 -> 0.1.2 | README.md: 0.1.1 -> 0.1.2
3) python tools/check_versoes.py                                              -> exit 0
     "os 6 mods batem nos quatro lugares (csproj = manifest = Plugin.cs = README)"
4) dotnet build RoguelikeDebugger/RoguelikeDebugger.csproj -c Release \
        -p:DeployToBepInEx=false --no-incremental                              -> 0 Erro(s)
     bin/Release/netstandard2.1/RoguelikeDebugger.dll
     sha256 7465a7e04c5de3cc5a79fd16ad870bf51da0be1326977d67acc2a1ece86f51f4   (60.928 bytes)
     (build FEITO DEPOIS da última edição: DLL 03:23:45 > Plugin.cs 03:23:33)
5) python tools/pack-thunderstore.py RoguelikeDebugger                        -> exit 0
     dist/gumatos-RoguelikeDebugger-0.1.2.zip
     sha256 7ed347e15181cd480d9adc79ad49feaf9282f46c5829d9d817b2f1fc3f724149   (131.815 bytes)
```

### 6.1 Provas sobre o ZIP gerado (`scratch/rel-dbg-012/new/`)

| prova | resultado |
|---|---|
| DLL do ZIP × DLL do build (`cmp`) | **byte-idênticas** — `cmp` rc=0; sha256 `7465a7e0…` nos dois |
| manifest/README/CHANGELOG/icon do ZIP × árvore (`cmp`) | **idênticos** nos quatro |
| versão **dentro** do DLL do ZIP (decompilado) | `[BepInPlugin("com.gumatos.roguelikedebugger", "Roguelike Debugger", "0.1.2")]`; `AssemblyVersion/FileVersion 0.1.2.0`; `AssemblyInformationalVersion 0.1.2`; **`0.1.1` = 0 ocorrências** |
| marcadores do código novo no DLL do ZIP | `FlameRV49` 3 · `~alvos=` 1 · `auraSts` 2 · `TickTargets` 4 · `!erro:` 6 · `Campo(` 27 · `MATRIZ` 7 |
| estrutura do pacote | raiz com os 4 arquivos + `plugins/RoguelikeDebugger/` (1 diretório de plugin) |
| pre-flight do próprio empacotador (REL-1 artefato×fonte) | `ok RoguelikeDebugger v0.1.2` |

### 6.2 Travas do projeto (todas por execução própria)

| trava | exit | saída |
|---|---|---|
| `python tools/check_versoes.py` | **0** | 6 mods batem nos quatro lugares |
| `python tools/check_deploy_optin.py` | **0** | "7 alvo(s) de deploy, todos com Condition `== 'true'`" |
| `python tools/check_patches.py` | **0** | RoguelikeDebugger: 14 classes de patch, 16 métodos de gancho; filtro aceita todos; 0 reprovações |
| `python tools/check_dependencias.py --local` | **0** | todas as dependências resolvem |

---

## 7. O que NÃO está provado (honestidade de escopo)

1. **O `[FlameRV49]` nunca rodou numa sessão de jogo.** O RV-49 segue **aberto** e
   dependente de rodada autorizada (`docs/automacao/AUT-2-contexto.md`: "RV-49 … dependem
   de medição/estado do jogo → só humano/rotina autorizada"). Por isso o CHANGELOG diz
   "NÃO EXERCITADA EM JOGO" e o README ganhou a seção "not verified in game yet".
2. **Os campos novos do RD-2 foram medidos no asset, por leitor offline** (421 de 424
   `ActionStatusInfo`), não lendo o log de uma partida.
3. **O custo da matriz** (5 `EvalVoid` extras por proc) não foi medido em combate real.
4. **Nada desta rodada foi publicado, instalado ou aberto** — por regra da tarefa.

---

## 8. Dependências abertas reais

- **De pacote:** apenas `BepInEx-BepInExPack-5.4.2305` (publicada) — o mod é standalone
  (BepInEx + Harmony direto, sem depender de outro mod nosso nem da `StolenRealmModAPI`).
- **De ferramenta interna:** `tools/census.py` **consome** o log do boot (o censo de
  tooltips) — é consumidor, não dependência de build/pacote.
- **Da rodada de runtime (AUT-4):** **não é dependência deste mod.** O conjunto
  `tools/automacao/runtime/` (coletor/driver) é o veículo para uma rodada autorizada; o
  que **depende** dela é a **medição RV-49**, não o pacote. Portanto **AUT-4 não bloqueia**
  a preparação nem um eventual upload deste mod — coerente com a regra da tarefa
  ("sem dependência demonstrada"). Se o dono quiser exercitar o probe antes de publicar,
  aí sim a rodada passa a ser **gate de aceite** (item 3 do pedido abaixo).

---

## 9. Pedido de aceite (específico)

1. **Aprovar o bump 0.1.2** e o texto novo do `CHANGELOG.md` (que declara explicitamente
   o que não foi exercitado) e do `README.md`.
2. **Decidir sobre o interruptor:** hoje o `[FlameRV49]` **não tem** flag (`Config.Bind`)
   — ele roda sempre. O dono quer (a) manter sempre-ligado, ou (b) um `.cfg` para desligar
   a matriz/probe fora de investigação? (A opção (b) é mudança de comportamento e exigiria
   nova rodada de build+pacote.)
3. **Autorizar (ou recusar) a rodada em jogo** para exercitar o `[FlameRV49]` e conferir o
   dump novo do RD-2 — é o que fecha a pendência e o que o CHANGELOG promete que alguém
   confira.
4. **Publicação:** fora do escopo desta tarefa. `release/mods.json` não foi alterado
   (`RoguelikeDebugger` continua `publicar: true`, `versao_publicada: 0.1.1`), e o upload
   só depois do aceite humano.

---

## 10. Artefatos desta rodada

- Pacote: `C:\dev\stolen-realm\dist\gumatos-RoguelikeDebugger-0.1.2.zip`
  (sha256 `7ed347e15181cd480d9adc79ad49feaf9282f46c5829d9d817b2f1fc3f724149`)
- DLL de Release: `C:\dev\stolen-realm\RoguelikeDebugger\bin\Release\netstandard2.1\RoguelikeDebugger.dll`
  (sha256 `7465a7e04c5de3cc5a79fd16ad870bf51da0be1326977d67acc2a1ece86f51f4`)
- Provas brutas (não versionadas, `scratch/`): `scratch/rel-dbg-012/` —
  `live/` (ZIP público extraído), `pub/` (ZIP local 0.1.1), `new/` (ZIP 0.1.2),
  `decomp/{live,dist,fresh,new}/` (decompilados), `api-package.json`, `pub-0.1.1.zip`.
