# INT-R1-C2 — parte 03: escopo fechado do cartão filho e critério de prova

Cartão `t_2ea91249`. Depende das decisões da parte 02 (D1–D8) e do mapa da parte 01. Aqui se decide
**o que o filho faz, o que ele não pode tocar, e como se prova que o adaptador não é código decorativo**.

---

## 1. Um cartão de implementação, com dois entregáveis delimitados

| Campo | Valor |
|---|---|
| Título proposto | `INT-R1-C2-I1: ponte RealmApi→KitSdk (adaptador offline) + AUT4Probe observando pelo hook` |
| Natureza | implementação |
| Modelo declarado | `deepseek-flash` / `deepseek` (regra do controlador para implementação) |
| Pai | `t_2ea91249` (este cartão) |
| Revisão | fecha com `kanban_request_review` (revisor independente no mesmo cartão; o controlador reatribui o modelo de arquitetura/revisão se necessário) |

**Entregável A — a ponte (offline, sem jogo, é o núcleo do cartão).**

Arquivos, e **só** estes:

| Ação | Caminho |
|---|---|
| NOVO | `tools/automacao/kit13/ApiBridge/ApiBridge.csproj` (`netstandard2.1`, sem Unity/BepInEx, com o mesmo `Kit13OfflinePreflight` que erra se `DeployToBepInEx != 'false'`) |
| NOVO | `tools/automacao/kit13/ApiBridge/RealmHooksBinding.cs` + `RealmHooksExtension.cs` (superfície fechada na parte 02, §D4) |
| NOVO | `tools/automacao/kit13/ApiBridgeHarness/ApiBridgeHarness.csproj` + `Program.cs` (offline, imprime `Ran N tests; failures=0`, no formato do `Harness/Program.cs:62`) |
| NOVO | `tools/automacao/kit13/prove_bridge_mutations.py` (mutações seletivas próprias; **não** editar `prove_mutations.py`, que é evidência do KIT-13) |
| NOVO | `docs/automacao/INT-R1-C2-I1-parteNN.md` |

Referências **permitidas** no `ApiBridge.csproj`: `../SDK/KitSdk.csproj` e
`../../../api/Core/RealmApi.Core.csproj`. Referência **proibida**: `api/Hooks`, `api/Plugin`, `BepInEx`,
`0Harmony`, qualquer `UnityEngine` — a ponte é consumidor, não produtor, e precisa continuar executável
offline.

**Congelado (o filho não pode tocar, nem "de passagem"):**

- `api/**` — o produtor está fechado (`api/Core/Contracts.cs`, `api/Hooks/HookInstallation.cs`,
  `api/Plugin/RealmApiPlugin.cs`). Se o filho achar que a API precisa mudar, isso é **frente nova**, não
  edição: os hashes da parte 01 §1 são a linha de base.
- `tools/automacao/kit13/SDK/**` e `CoreBridge/**` — KIT-13 está `done` e revisado por KIT-13R; a ponte nova
  é um projeto **ao lado**, não uma alteração do SDK entregue.
- `tools/automacao/kit13/prove_mutations.py`, `prove_offline.py`, `packages.py`, `test_packages.py` e os
  `examples/*.json` — são a prova do KIT-13.
- `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` **fora dos blocos listados no entregável B**.

**Entregável B — o `AUT4Probe` consome pelo hook (mesmo cartão, delimitado).**

Antes de escrever o que muda, o que o arquivo **faz hoje** (evidência):

| Bloco | Linhas | Natureza | Veredito |
|---|---|---|---|
| `_harmony = new Harmony(Guid)` | `AUT4ProbePlugin.cs:249` | dono Harmony próprio do probe | fica |
| `Gancho("GUIManager","Update")` | `AUT4ProbePlugin.cs:250` | **driver** de tick (não há hook equivalente no catálogo) | fica |
| `GanchoTodos("OptionsManager","Localize")` | `AUT4ProbePlugin.cs:251` | **driver** de tick que duplica o alvo do hook `ui.localized` (`Contracts.cs:63`) | **sai** |
| `InstalarNoPlayerLoop()` | `AUT4ProbePlugin.cs:255-290` | driver por quadro | fica |
| `POSTFIX → Tick("gancho")` | `AUT4ProbePlugin.cs:334-341` | despachante de tick | fica |
| leitura de estado por reflexão própria (`Tipo`/`Estatico`/`Membro`/`Recursos<T>`) | `AUT4ProbePlugin.cs:1824-1864` | coleta de texto/cor/geometria (não endereçável pelos 4 hooks) | fica |
| `botao.onClick.Invoke()` e a navegação | `AUT4ProbePlugin.cs:1143` e vizinhança | **input sintético** | **INTACTO** — `t_139f714f` não é resolvido pela API (`INT-R1-parte03.md:20`) |

Ponto honesto que o filho **tem de declarar**, não esconder: o patch em `OptionsManager.Localize` é um
**gatilho de tick**, não um coletor de conteúdo. Removê-lo troca um gatilho por outro (o evento
`ui.localized` entregue pela ponte), e a cobertura **não é idêntica**: a API cobre **exatamente uma**
assinatura — `ui.localized` é estático, retorno `System.String`, parâmetros
`(System.String, LanguageGender, Gender)` (`Contracts.cs:63`) — enquanto o probe hoje patcheia **todos** os
overloads (`GanchoTodos`, `AUT4ProbePlugin.cs:307-320`, filtra só por nome). Quantos overloads existem no
binário alvo é **`NAO_EXERCITADO` nesta rodada**: eu não inspecionei o `Assembly-CSharp.dll` para isso. O
filho mede com a ferramenta que já existe (`api/tools/Inspect/Program.cs:34` já lista `"OptionsManager"`
entre os tipos inspecionados) e registra a contagem na entrega. Sobrevivem dois drivers independentes
(`GUIManager.Update` e o `PlayerLoop`), então a função não fica sem gatilho.

Como o probe consome sem virar dependente duro (decisão, para o filho não escolher):

- Assinatura do `Signal` **dentro** de um assembly companheiro opcional
  (`tools/automacao/runtime/AUT4Probe/Companheiro/…`, projeto separado, sem Unity), carregado pelo probe
  **por nome exato** (`Assembly.Load("Gumatos.KitApiBridge.AUT4")`) dentro de `try/catch`, atrás de uma
  config **nova com default `false`**, no mesmo padrão de opt-in que o probe já usa
  (`Autorizado=false`, `AUT4ProbePlugin.cs:231-240`).
- Ausente → o probe se comporta **exatamente como hoje** (nenhuma exceção, nenhuma mudança de saída).
- **Por que a exceção de usar `Assembly.Load` aqui** e não na ponte do kit: a regra
  "No assembly loading, script execution, authorization" (`RegistryV1.cs:47-48`) protege o **contrato de
  extensões do kit**. O probe é um instrumento de bancada cujo trabalho é carregar e observar; a alternativa
  (referência dura) quebraria o probe quando a API não está instalada. O `Load` é por **nome exato**, sem
  varredura, sem sondagem de versão, e falha = comportamento de hoje.

Critério de aceite do entregável B (todos verificáveis por leitura/diff, nenhum em jogo):

1. `grep -n "OptionsManager" tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` **não** mostra mais uma
   chamada de patch em `Localize` (o texto ainda pode aparecer no nome do hook consumido).
2. O diff de `AUT4ProbePlugin.cs` é **linha-local**: nenhuma reformatação, nenhuma mudança nos blocos
   marcados "fica"/"INTACTO" da tabela acima (prova: `git diff --stat` + leitura do diff inteiro na revisão).
3. Com a config nova em `false` e sem o companheiro, a saída do probe é a de hoje (comparação contra a
   evidência já gravada em `docs/automacao/AUT-4-evidencias/`), **`NAO_EXERCITADO` para a rodada em jogo** —
   esta rodada não abre o jogo e não instala nada.
4. `AUT4ProbePlugin.cs` foi **relido imediatamente antes** de cada edição (o arquivo está sujo na árvore de
   trabalho por outros cartões — ver o `hotspot` na parte 04).

---

## 2. Critério de prova: o que o `ApiBridgeHarness` tem de exercitar offline

Regra: **cada asserção abaixo tem de falhar** quando o trecho correspondente do adaptador é substituído por
um stub (§3). Asserção que passa com o adaptador vazio não prova nada e é proibida no relatório.

Estados e gate (D5, D7):

- **P1** — criar com `KitApi = "1.0.0"` exato: registro aceito, `RegistryV1.Count == 1`, id `realmapi.hooks`.
- **P2** — criar com `KitApi = "2.0.0"`: `NotSupportedException` contendo `API_INCOMPATIVEL` e
  `RegistryV1.Count == 0`. (Mesmo formato do teste `version` do kit, `Harness/Program.cs:29`.)
- **P3** — criar com `ProducerVersion` divergente (ex. `"0.2.0"`): recusa `API_INCOMPATIVEL` **e** nenhuma
  assinatura no `Signal` — provado publicando depois e verificando **zero** efeito.
- **P4** — `session` vazia e `session` de 129 caracteres: `ArgumentException` **antes** de qualquer
  inscrição (`Count == 0`; nenhum lease órfão). Padrão: `CounterAdapter.cs:22-24`.
- **P5** — `producerActive() == false`: publicar 3 notificações conhecidas → **zero** `EventV1` chegam a uma
  extensão testemunha registrada no `RegistryV1`, e `Read("hooks.count")` devolve `NAO_EXERCITADO`.
- **P6** — `producerActive()` vira `true` (o `Func<bool>` fecha sobre variável mutável): publicar 3 →
  `Read("hooks.count") == "3"` com status `OBSERVADO`; e com **zero** publicações → `"0"` **OBSERVADO**
  (é o caso ambíguo que a D5 obriga a distinguir).

Mapeamento (D4, D6):

- **P7** — notificação com `HookId` do catálogo → exatamente 1 `EventV1` com `Kind == HookId`,
  `Session` igual à declarada, `Frame` = ordinal 0,1,2… e `Data` contendo a marca `quadro=ordinal`.
- **P8** — `HookId` desconhecido (`"game.desconhecido"`): zero `EventV1`, `Read("hooks.unknown") == "1"`, e
  `Validate` sobre esse hook devolve `NAO_EXERCITADO`/`AUSENTE` — **nunca** `PASSOU`.
- **P9** — `Read("hook.ui.localized.count")` conta só aquele hook; chave fora do vocabulário →
  `AUSENTE` (`RegistryV1.cs:133`).
- **P10** — `Result` de 10 000 caracteres → `Data` com `≤4096` e **marcador de truncamento** presente: nada
  de `ArgumentException` de `EventV1` (`RegistryV1.cs:17`) e nada de truncamento silencioso.

Honestidade do dado (D6, D8):

- **P11** — mutar o array de `Arguments` **depois** da publicação não altera o `Data` já publicado (a API
  clona a lista em `Contracts.cs:76`; o teste prova que o adaptador não guarda alias da lista viva).
- **P12** — `OnEvent` chamado de outro thread (`Task.Run`) não lança e não trava (limite de 2 s, padrão
  `dispose-waits`, `Harness/Program.cs:45-52`).
- **P13** — extensão testemunha que lança: o adaptador continua entregando às demais; o kit guarda
  diagnóstico **sem a mensagem** (marcador secreto não pode aparecer — mesmo teste `event-isolation` do kit,
  `Harness/Program.cs:34`); o canal `diagnostic` do adaptador registra o **tipo**, limitado.
- **P14** — `Dispose()` do adaptador: assinatura do `Signal` removida e lease do `RegistryV1` liberado;
  publicar depois → zero eventos novos e `Count` volta ao valor anterior (idempotente: `Dispose` duas vezes
  não lança).
- **P15** — reentrância: extensão do kit que chama `RegistryV1.Publish` dentro do `OnEvent` disparado pelo
  adaptador → `EVENTO_REENTRANTE` (`RegistryV1.cs:114`) e o adaptador **não** engole a exceção do kit em
  silêncio.

Saída exigida na entrega: `Ran 17 tests; failures=0` (ou N ≥ 15, com o N e o motivo de cada asserção
ausente declarados), `exit 0`, mais o JSON da evidência ao lado do relatório.

## 3. Prova de não-decorativo: mutação seletiva 0→1→0

Molde já validado no KIT-13 (`prove_mutations.py`, 33 mutações `0->1->0` com `source_sha_restored: true`).
O filho cria `prove_bridge_mutations.py` com **no mínimo** estas mutações, cada uma derrubando ≥ 1 asserção:

| Mutação | O que ela quebra | Asserção que tem de falhar |
|---|---|---|
| m1 — remover o gate `producerActive()` do `OnEvent` | publica com produtor inativo | P5 |
| m2 — remover o gate `producerActive()` do `Read` | `NAO_EXERCITADO` vira `OBSERVADO`/`AUSENTE` | P5, P6 |
| m3 — mapear **todo** `HookId` para `EventV1` | duplicação com lixo | P8 |
| m4 — não truncar / não marcar o `Data` | `Data > 4096` ou truncamento silencioso | P10 |
| m5 — guardar a referência viva de `Arguments` | dado muda depois do fato | P11 |
| m6 — deixar o `OnEvent` propagar exceção | exceção do consumidor no log do produtor | P12, P13 |
| m7 — trocar a comparação exata de versão por prefixo | aceita par incompatível | P2, P3 |
| m8 — `Frame = 0` fixo | numeração falsa indistinguível de "primeiro quadro" | P7 |

A entrega registra, por mutação: fonte, `sha256` antes, contagem de falhas observada, `sha256` restaurado,
e o total (padrão `0->1->0`).

## 4. `NAO_EXERCITADO` desta frente (declarado, com motivo)

- **Runtime do jogo**: BepInEx carregando `RealmApi.dll` com `EnableHooks=true`, os 4 hooks instalados, e a
  ponte recebendo notificações reais — **NAO_EXERCITADO**: esta rodada não instalou nada e não abriu o jogo;
  o filho também não pode (limite do cartão).
- **`RegistryV1` + `Signal<T>` no mesmo processo real**: **NAO_EXERCITADO** no jogo; o que é exercitável
  offline é o `Signal` real (é `netstandard2.1` puro, sem Unity) e o `RegistryV1` real — os dois podem ser
  exercitados de verdade no harness, sem fake, **exceto** `HookInstallation`, que exige Harmony e fica fora.
- **Número de overloads de `OptionsManager.Localize` no binário alvo**: **NAO_EXERCITADO** (não inspecionei
  o `Assembly-CSharp.dll` nesta rodada); o filho mede com `api/tools/Inspect`.
- **Clique/navegação do `AUT4Probe` (`t_139f714f`)**: **NAO_EXERCITADO** e fora do escopo — a API não dirige
  input.
- **Deploy em perfil r2modman / publicação**: **NAO_EXERCITADO** — `api/` não tem alvo de deploy e o
  instrumento nunca escreve no perfil por build (`AUT4Probe.csproj:18`).
