# INT-R1-C2 — parte 04: o que foi executado, higiene, `hotspot` e mapa de aceite

Cartão `t_2ea91249`. Esta parte é a prova de execução: comandos rodados nesta rodada com a saída literal, a
verificação de que nenhum código de produção mudou, o `hotspot` encontrado, e o mapa item-por-item do aceite
do cartão.

---

## 1. Comandos executados nesta rodada (saída literal)

### 1.1 Suíte de testes do SDK do kit (o contrato do consumidor, exercitado de verdade)

```bash
cd /c/dev/stolen-realm/tools/automacao/kit13 && \
  dotnet run --project Harness/Harness.csproj -c Release -p:DeployToBepInEx=false
```

Saída (17 linhas `PASS` + total; recorte final):

```
PASS|version
PASS|duplicate
PASS|unregister
PASS|replacement
PASS|mid-publish
PASS|event-isolation
PASS|reader-isolation
PASS|validator-isolation
PASS|absent
PASS|reentrant
PASS|limit
PASS|disposed
PASS|dto
PASS|adapter
PASS|mod-isolation
PASS|diagnostic-limit
PASS|dispose-waits
Ran 17 tests; failures=0; OFFLINE_ONLY
```

`PASS|version` é a prova executada da regra de recusa fechada por versão exata (F1 da parte 02): registrar com
`"2.0.0"` lança `NotSupportedException` e `Count` continua 0 (`Harness/Program.cs:29`).

### 1.2 Ponte existente do kit para o Core KIT-04 (o precedente que a decisão D4 espelha)

```bash
cd /c/dev/stolen-realm/tools/automacao/kit13 && \
  dotnet run --project CoreHarness/CoreHarness.csproj -c Release -p:DeployToBepInEx=false
```

```
CoreBridge PASSOU: disabled=0 enabled=1; ICoreEvento fake; game NAO_EXERCITADO
exit=0
```

Prova executada de que o padrão "host injeta a autorização e a extensão não publica nada com o gate fechado"
funciona hoje, dentro do kit, com serviço fake — é o contrato que a ponte nova estende para a API.

### 1.3 O produtor continua verde e intocado (5 builds + smoke)

```bash
cd /c/dev/stolen-realm && for p in api/Core/RealmApi.Core.csproj api/Hooks/RealmApi.Hooks.csproj \
  api/Plugin/RealmApi.csproj api/Smoke/RealmApi.Smoke.csproj api/tools/Inspect/Inspect.csproj; do
  dotnet build "$p" -c Release --nologo; done
```

Cada um dos 5 projetos: `0 Aviso(s)` / 0 erros.

```bash
cd /c/dev/stolen-realm && api/Smoke/bin/Release/net472/RealmApi.Smoke.exe \
  C:/dev/stolen-realm/lib/Assembly-CSharp.dll \
  C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll
```

```
PASS ui-tooltip-delegation-1para1
PASS ui-action-bar-delegation
PASS ui-skill-tree-delegation
PASS ui-menu-delegation
PASS ui-public-surface-in-plugin-metadata
PASS actual-game-ui-requirements-metadata
Ran 62 tests; failures: 0
NAO_EXERCITADO: BepInEx/Unity runtime, gameplay, saves, multiplayer; somente CLR fixtures + metadados locais.
exit=0
```

Isto fecha a pendência deixada na parte 01 §5 (o número do smoke era evidência gravada de outra sessão):
agora é medição **própria desta rodada** — `Ran 62 tests; failures: 0`, exit 0. O contador subiu de 25
(API-R1) para 62 com os 37 casos que a API-R1-I2 acrescentou (`api/README.md:191-192`).

## 2. Higiene: nenhum código de produção alterado nesta rodada

```bash
cd /c/dev/stolen-realm && \
  sha256sum api/Core/Contracts.cs tools/automacao/kit13/SDK/RegistryV1.cs && \
  find api tools/automacao/kit13 -name "*.cs" -newermt "2026-10-11 05:00" -not -path "*/obj/*" -not -path "*/bin/*" | wc -l && \
  git status --porcelain docs/automacao | grep INT-R1-C2
```

Resultado medido:

- `api/Core/Contracts.cs` → `7970780440d1682a7b3bb3d09ddc4812c7371ae5a85edf141e575caf7d48cb62` (idêntico ao
  da parte 01 §1: o hash foi calculado **antes** dos builds e conferido **depois**);
- `tools/automacao/kit13/SDK/RegistryV1.cs` → `9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700`
  (idêntico);
- **0** arquivos `.cs` de `api/` ou `kit13/` modificados nesta janela;
- **0** DLLs novos: os 5 builds da API foram "up-to-date" (`api/Plugin/bin/Release/netstandard2.1/RealmApi.dll`
  com mtime `2026-10-11 04:33:37`, ou seja, do API-R1-I2, não desta rodada);
- o único produto no repositório são os arquivos **novos** `?? docs/automacao/INT-R1-C2-parte01.md`,
  `-parte02.md`, `-parte03.md` (e este `-parte04.md`).

Observação honesta sobre o estado do repo: `git status --porcelain` mostra vários arquivos `M` de **outros**
cartões em voo (RoguelikeSkillTreeVisualizer, `AUT4Probe`, `aut5`, `cenarios`, `docs/automacao/AUT-4-*`) e
`api/` + `tools/automacao/kit13/` aparecem como **untracked** (`?? api/`, `?? tools/automacao/kit13/` — nunca
commitados). Nada disso foi tocado por esta rodada; a verificação acima é por conteúdo (hash/comando), não por
confiança.

## 3. `hotspot` encontrado (registrado também como comentário no cartão)

```
hotspot: tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs — já sujo na árvore de trabalho por outros
cartões (AUT-4) e seria editado pelo cartão filho INT-R1-C2-I1 no entregável B (remoção do patch duplicado
em OptionsManager.Localize).
```

Consequência prática, já escrita no corpo do filho: `AUT4ProbePlugin.cs` tem de ser **relido imediatamente
antes** de cada edição, o diff tem de ser **linha-local** (nenhuma reformatação), e os blocos de clique,
`PlayerLoop` e captura de PNG são intocáveis. Se o orquestrador preferir isolar, o entregável B pode ser
promovido a cartão próprio com o mesmo pai — a arquitetura não muda.

## 4. Mapa de aceite do cartão → onde cada item está respondido

| Item do aceite (`t_2ea91249`) | Resposta | Onde |
|---|---|---|
| 1. Mapa dos dois núcleos lado a lado, tipo por tipo, o que faz o mesmo, o que só um faz, com caminho:linha | Tabelas de tipos + tabela de função cruzada + duplicação concreta (`OptionsManager.Localize` patcheado por dois donos) | parte 01 §2–§4 |
| 2. Decisão escrita: produtor, consumidor, contrato sobrevivente, adaptador, ausência da API / `EnableHooks=false` | D1 (papéis), D2 (contrato), D3 (direção da dependência), D4 (adaptador + superfície fechada), D5 (tabela de 4 estados), D6 (sessão/quadro), D7 (autorização), D8 (thread/exceção) | parte 02 §1 |
| 3. Regra de versionamento única | F1–F4 (uma regra, quatro fronteiras, string exata, recusa fechada) + política de bump + o que é proibido (range, fallback, reflexão, config) | parte 02 §2 |
| 4. Escopo fechado dos cartões de implementação (idealmente UM, incluindo `AUT4Probe` pelos hooks) | **UM** cartão: `t_a706b09c` — entregável A (ponte offline) + entregável B (`AUT4Probe`), com arquivos permitidos, proibidos e congelados, e a mudança de cobertura declarada | parte 03 §1 + cartão `t_a706b09c` |
| 5. Critério de prova do adaptador (o que exercitar offline para não ser decorativo) | P1–P15 (asserções falsificáveis) + mutações m1–m8 (`0->1->0`) + regra "asserção que passa com o adaptador vazio é proibida" | parte 03 §2–§3 |
| Aceite: zero código de produção alterado | §2 desta parte (hashes + contagens + git) | parte 04 §2 |
| Aceite: `NAO_EXERCITADO` declarado para runtime/jogo | parte 01 §5 (parcial), parte 03 §4 (consolidado) | parte 01 §5, parte 03 §4 |

## 5. Cartão filho criado

| Campo | Valor |
|---|---|
| id | `t_a706b09c` |
| título | `INT-R1-C2-I1: ponte RealmApi→KitSdk (adaptador offline) + AUT4Probe observando pelo hook` |
| natureza / modelo | implementação — `deepseek-flash` / `deepseek` (declarado explicitamente, regra do controlador) |
| pai / gating | `parents=[t_2ea91249]` → fica em `todo` até este cartão fechar (`gated_by: t_2ea91249`) |
| workspace | `dir` em `C:/dev/stolen-realm` |
| revisão | o implementador fecha com `kanban_request_review` (revisor independente no **mesmo** cartão; nenhum cartão de revisão duplicado) |

O corpo do filho é auto-contido: carrega D1–D8, a superfície exata do adaptador, as chaves de leitura, P1–P15,
m1–m8, os arquivos congelados e o `hotspot` — porque um worker não vê o contexto dos irmãos.

## 6. `NAO_EXERCITADO` consolidado desta rodada (motivo por item)

| Item | Motivo |
|---|---|
| Runtime do jogo: BepInEx carregando `RealmApi.dll` com `EnableHooks=true` e instalando os 4 hooks | jogo não aberto nesta rodada; `EnableHooks` continua `false` por padrão (`RealmApiPlugin.cs:21`) |
| `HookInstallation` (Harmony real) exercitado com os alvos do jogo | exige o jogo/perfil; o smoke roda em CLR de fixtures (`api/README.md:202-204`), o que **não** é comportamento de jogo |
| A ponte nova (`t_a706b09c`) | não existe ainda — é o escopo do filho |
| Número de overloads de `OptionsManager.Localize` no binário alvo | não inspecionei o `Assembly-CSharp.dll` nesta rodada; o filho mede com `api/tools/Inspect` (o tipo já está na lista, `api/tools/Inspect/Program.cs:34`) |
| Clique/navegação do `AUT4Probe` (`t_139f714f`, `0xc0000005`) | fora do escopo; a API 0.1.0 é observacional e não dirige input |
| Deploy no perfil r2modman / publicação Thunderstore | `api/` não tem alvo de deploy; o instrumento nunca escreve no perfil por build (`AUT4Probe.csproj:18`) |

## 7. Limites do cartão — conferidos um por um

| Limite | Situação |
|---|---|
| não implementar a ponte aqui | cumprido: nenhum arquivo de `ApiBridge` criado; a ponte é escopo de `t_a706b09c` |
| não editar os mods | cumprido: nenhum arquivo de mod tocado (RSTV, BetterTooltips, AUT4Probe, etc.) |
| não instalar | cumprido: nenhum `dotnet build` com deploy, nenhuma cópia para perfil |
| não abrir o jogo | cumprido: nenhum processo do jogo iniciado |
| não publicar | cumprido: nenhum `git add`/`commit`/`push`, nenhuma publicação |
| não alterar o comportamento do kit entregue | cumprido: `RegistryV1.cs` e `KitSdk.csproj` com hash idêntico; os 17 testes do kit passam como antes |
