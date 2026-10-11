# KIT-14G — parte07: item 3 (recorder com 0 eventos) — gate de projeto, provado por execução

Cartão `t_0e656658`, run714. Complementa parte01–06. Fonte de verdade por máquina no fim da rodada:
`scratch/kit/KIT-14G-run714/verification.json`.

A revisão run713 exigiu: *"explicar por que `roteiro2` clicou a rota `Play;Roguelike`
(3 estágios) e o recorder devolveu `eventos_total = 0` — se interação de menu deveria contar,
é defeito corrigível; se não, declarar bloqueado-por-design citando o gate do recorder."*

Resposta, com prova executada: **interação de menu NÃO deve contar — e não é um gate qualquer:
o recorder é cego a ela por construção.** Abaixo o caminho do dado, de ponta a ponta.

## 1. Por onde o recorder PODE ganhar evento (só existem duas portas)

`tools/automacao/runtime/core/CorePlugin.cs:152` `ResultadoFinal()` monta `eventos` a partir do
livro `_eventos` (`EventosImpl`), alimentado **apenas** por `RegistrarEvento(...)`. Quem chama
`RegistrarEvento` no repositório inteiro:

| origem | tipos emitidos | condição |
|---|---|---|
| `CorePlugin.Update()` (1º tick) | `inicializacao` | Core habilitado (o livro nasce aqui) |
| `SRAdapterPlugin.Update()` caminho **legado** | `tela_detectada`, `personagens_lidos` | Core habilitado **E** `passivoHabilitado = false` |
| `SRAdapterPlugin.Update()` caminho **passivo** → `AlimentarPassivo` → `PontePassivaRSTV.Observar()` | `passivo_janela_aberta`, `passivo_janela_fechada`, `passivo_clique_recebido`, `passivo_falha_clique_sem_janela` | Core habilitado **E** `passivoHabilitado = true` |

E `SRAdapterPlugin.cs:169` mostra que os dois caminhos são **excludentes**:

```csharp
if (p_PassivoHabilitado.Value)
{
    ...
    bool cliqueObservado = Input.GetMouseButtonDown(0);   // <-- SÓ input da ENGINE
    ...
    AlimentarPassivo(ativas, cliqueObservado, agoraMs);
    return;   // a trilha passiva substitui a emissao por frame
}
// legado (tela_detectada / personagens_lidos) só roda se passivoHabilitado == false
```

## 2. As duas únicas fontes de evento passivo são telas RSTV e clique de ENGINE

`PontePassivaRSTV.Observar()` (`tools/automacao/runtime/KIT04Adapter.SR/PontePassivaRSTV.cs:64`)
emite **exatamente**:

1. **transição** de estado das telas conhecidas — `SRScreenManager.TelasConhecidas`
   (`SRScreenManager.cs:22`) = `InventoryPanel`, `SkillsPanel`, `EquipmentPanel`, `MapPanel`,
   `DialogPanel`, `PausePanel`. **São 6 painéis do HUD de jogo.** `MainMenu`, `CharacterCreation`,
   `CreatingCharacter` **não estão na lista**;
2. `cliqueRecebido` — que vem de `Input.GetMouseButtonDown(0)`, isto é, **clique físico no
   dispositivo**. A ponte nunca emite clique (comentário do próprio arquivo, linha 12).

## 3. Por que `roteiro2` clicou 3 estágios e o recorder ficou em 0

O probe **não usa mouse**. `AUT4ProbePlugin.cs:1030`:

```csharp
lista.Add((rotulo, ativo, () => botao.onClick.Invoke()));
```

A navegação do instrumento é *por handler*: chama o `UnityEngine.Events.UnityEvent.onClick` do
botão direto, sem passar pelo `Input`. Consequência medida, item por item:

- os 3 estágios (`Play`, `Roguelike`, — ) foram para `CreatingCharacter`. Nenhuma das 6 telas
  monitoradas existe nessas telas → **0 transições**;
- `Input.GetMouseButtonDown(0)` nunca foi verdadeiro durante a navegação sintética → **0
  `clique_recebido`**;
- `passivoHabilitado = true` (conferido no `.cfg` real do boot irmão
  `roteiro5/bepinex-iso/BepInEx/config/com.gumatos.kit04.adapter.sr.cfg`:
  `habilitado = true`, `passivoHabilitado = true`) → o caminho **legado** (`tela_detectada`,
  `personagens_lidos`) **não roda** (`return` na linha 190).

`eventos_total = 0` é, portanto, **o comportamento projetado** para uma sessão que só navega menu
por handler. Não é "o recorder perdeu cliques que aconteceram": para ele, **nenhum clique
aconteceu**.

**Veredito do item 3: BLOQUEADO-POR-DESIGN**, citando o gate:
`PontePassivaRSTV.Observar()` só observa (i) transição das 6 telas de
`SRScreenManager.TelasConhecidas` e (ii) `Input.GetMouseButtonDown(0)`. `eventos_total > 0`
exige o **HUD da run** (onde vivem `InventoryPanel`/`SkillsPanel`/… e onde um clique físico pode
ocorrer) — exatamente a tela que o crash do item 1 impede de alcançar.

## 4. Prova executada do gate (offline, sem abrir o jogo)

```
$ dotnet run --project tools/automacao/runtime/harness-passivo -c Release
...
[OK    ] opt-in false => Observar devolve nada
[OK    ] opt-in false => pipeline inerte (0 eventos)
[OK    ] transicao inativa->ativa vira janela_aberta
[OK    ] transicao ativa->inativa vira janela_fechada
[OK    ] total de eventos coerente (3)
[OK    ] 500 quadros sem transicao nao geram evento novo
[OK    ] clique observado vira clique_recebido
[OK    ] clique sem tela nao cria pendencia
[OK    ] resumo nao promove runtime
...
 verificacoes: 29 OK, 0 FALHA
 VEREDITO HARNESS: VERDE (exit 0)
```

Dois resultados importam aqui:

- **`clique observado vira clique_recebido`** — o evento de clique só existe pelo parâmetro
  `cliqueObservado`, que é `Input.GetMouseButtonDown(0)`. O harness o recebe como booleano vindo do
  input: é o mesmo caminho do Adapter, e **não há** nenhum caminho alternativo por `onClick`;
- **`resumo nao promove runtime`** — achado colateral importante: `PipelinePassivo.Resumo()`
  (`PipelinePassivo.cs:395`) **escreve literalmente** `"runtime", "NAO_EXERCITADO"`. O rótulo
  `passivo.runtime` **é constante**, não é medição: ele sai `NAO_EXERCITADO` mesmo com eventos
  registrados. Citá-lo como prova de "nada foi exercitado" (o que o run712 fez, parte05 §4) é
  **errado** — o campo medido é `eventos_total`.

Comando exato acima registrado; saída completa em
`scratch/kit/KIT-14G-run714/logs-harness-passivo.log`.

## 5. Achado separado: o evento `inicializacao` do próprio Core NUNCA aparece (defeito candidato)

Isto é independente do menu e foi medido agora, nos três boots que finalizaram
(`mapa`, `roteiro1`, `roteiro2`): o Core estava **habilitado** (o bloco `passivo` existe no
resultado e traz o `sessao` da rodada — se estivesse desabilitado, `ResultadoFinal()` devolveria
apenas `{"status": "NAO_EXERCITADO"}` e `passivo` seria `null`, `CorePlugin.cs:154`), e mesmo assim:

```
recorder.json (mapa/roteiro1/roteiro2): eventos: []   eventos_descartados: 0
```

`eventos` sai de `ObterEventos()` → `_eventos?.ObterEventos() ?? new List<>()`
(`CorePlugin.cs:143-146`) e `_eventos` **só é criado** dentro de `RegistrarEvento`, chamado no
primeiro `Update()` do Core (`CorePlugin.cs:209-216`). Livro vazio ⇒ **`_eventos == null` ⇒ o
`Update()` do Core não executou nenhum tick** nos três boots em que ele estava carregado
(o log do BepInEx confirma que ele foi carregado: "Loading [KIT-04 Core Genérico 0.1.0]").

Leitura honesta: **não sei ainda a causa** — duas hipóteses, não separadas nesta rodada:
(a) o `GameObject` do plugin do Core não recebe `Update()` no arranjo de BepInEx desta bancada;
(b) o `Update()` roda e lança antes do `RegistrarEvento` (o log não mostra exceção do plugin).

Classificação: **defeito candidato de PRODUTO (Core), fora do escopo do KIT-14G** (o escopo do
cartão é o instrumento/navegação/recoleta, não o Core). Não corrigi o produto nesta rodada.
Registrado como pendência para cartão próprio, com o reprodutor exato: qualquer boot com
`Modo/habilitado=true` no Core devolve `eventos: []` neste ambiente.

Correção de afirmação, portanto: o `eventos_total = 0` do item 3 **não é só** o gate de projeto —
ele é a soma de (i) gate de projeto (menu não conta) **e** (ii) este defeito candidato (o único
evento que *deveria* estar lá, `inicializacao`, não está). As duas coisas ficam separadas aqui.

## 6. NÃO EXERCITADO

`eventos_total > 0` do recorder continua **NAO_EXERCITADO** no runtime: exige o HUD da run, que o
crash do item 1 impede de alcançar. Nada de FPS/frame/IO foi medido. A causa do defeito candidato
do §5 não foi isolada (falta cartão próprio com reprodutor de produto).
