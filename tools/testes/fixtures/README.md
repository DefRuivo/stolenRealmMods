# tools/testes/fixtures — entradas e saidas esperadas, versionadas

Cada teste que precisa de dado de entrada **e** de valor esperado usa duas
fixtures aqui, com nome previsivel. Nada de valor esperado escrito dentro do
teste: numero digitado a mao e o defeito que o projeto ja pagou caro (invariante
1: "todo numero exibido e o do MOTOR - nada somado a mao").

## Convencao de nome

```
<caso>.<papel>.<ext>
```

| parte | valor | observacao |
|-------|-------|------------|
| `<caso>` | o campo `nome` do META do teste | `soma-aura` -> `t_exemplo_soma_aura.py` |
| `<papel>` | `entrada` ou `esperado` | so estes dois |
| `<ext>` | `json` (padrao), `csv`, `log`, `txt` | a que o dado pedir |

Exemplos: `soma-aura.entrada.json`, `soma-aura.esperado.json`.

No teste:

```python
dados = arc.ler_json("soma-aura", "entrada")
esperado = arc.ler_json("soma-aura", "esperado")      # ou arc.ler_texto("x", "esperado", "csv")
```

`arc.caminho_fixture` levanta `Falhou` (exit 1) se o arquivo nao existir - fixture
versionada ausente e **defeito do repositorio**, nao dependencia do ambiente.

## Procedencia: de onde o `<esperado>` veio

Isto e a parte que faz a fixture valer alguma coisa. **Saida esperada gerada pela
mesma implementacao que o teste usa nao prova nada** - o teste passaria por
construcao. Entao cada familia de fixture declara a procedencia DENTRO do proprio
arquivo (campo `procedencia`, e `gerado_por` no `<esperado>`).

### `soma-aura.*` — escala de aura de shrine

* Formula: `Mathf.Round(BASE * (1 + shrineEffectBonus/100))`, fator e produto em
  **float** (o caminho do motor), `Math.Round` = half to even (bancario).
* Gerada por `geradores/oraculo_soma_aura/` — um programa **C#** (console, .NET 6)
  que passa pelo mesmo caminho de conta do motor. Ele escreve os dois arquivos.
* `soma-aura.entrada.json` traz, alem dos cenarios, uma **auditoria**: para todo
  par (base do censo x bonus alcancavel) o oraculo compara float e double e
  registra onde discordam. Resultado atual: 128 pares, **0 divergencias** - por
  isso a conta em double basta neste dominio. Fora do alcancavel eles divergem
  (ex.: base 5, bonus -90: float 1, double 0), e o teste tem um controle que
  quebra se a emulacao de float32 deixar de divergir - a emulacao nao pode ser
  decoracao.

Regenerar (mexe nos arquivos versionados - rode e revise o `git diff`):

```bash
dotnet run --project tools/testes/fixtures/geradores/oraculo_soma_aura -- tools/testes/fixtures
```

O `dotnet` **nao** e necessario para rodar os testes: a fixture esta versionada.
O oraculo existe para auditar e regerar.

### `excesso-shrine.*` — EXCESSO DE SHRINE (familia TST-2)

* Um par de fixtures para os QUATRO testes da familia (excecao documentada a
  convencao "um caso por teste": e a mesma familia, o mesmo oraculo e o mesmo
  material - bonus, agregado, dano e formato).
* Gerada por `geradores/oraculo_excesso_shrine/` — C# (console, .NET 6) que passa
  pelo caminho de conta do motor: **`float`** + `Math.Round` **ToEven** +
  `Mathf.CeilToInt` (a convencao inteira da ficha).
* As bases e os percentuais **nao sao digitados no oraculo**: ele LE
  `tools/dados/shrines-esperado.csv` (gerado por `tools/gera_shrines_esperado.py`
  de `docs/cobertura/status.csv` + `resources.assets`) e
  `tools/dados/shrines-percentuais.csv`, e **FALHA (exit 1)** se uma aura,
  atributo ou percentual esperado nao estiver la.
* O que a fixture carrega: a cadeia do `ShrineEffectBonus` (§3, com a substituicao
  do `Omnism I` pelo II), a escala das 12 auras em 10 bonus, a matriz do dano do
  Flame/Decay (6 tipos de inimigo x 5 vidas maximas x 4 bonus), as bordas de
  formato e a **linha agregada** `Your active shrine auras:` item por item
  (RV-31/44/46: deduplicacao, soma por atributo, itens sem atributo e os avisos).
* `conferencia_csv` dentro do esperado: o oraculo recalcula cada linha de
  `tools/dados/shrines-esperado.csv` e o teste confere a coincidencia - a fixture
  nao pode envelhecer em relacao a tabela gerada do repositorio.

Regenerar (mexe nos arquivos versionados - rode e revise o `git diff`):

```bash
dotnet run --project tools/testes/fixtures/geradores/oraculo_excesso_shrine -- tools/testes/fixtures
```

O `dotnet` **nao** e necessario para rodar os testes: a fixture esta versionada.
O oraculo existe para auditar e regerar.

## Fixtures de hoje

| caso | entrada | esperado | gerado por |
|------|---------|----------|------------|
| `soma-aura` | `soma-aura.entrada.json` | `soma-aura.esperado.json` | `geradores/oraculo_soma_aura` (C#, float + Math.Round) |
| `excesso-shrine` | `excesso-shrine.entrada.json` | `excesso-shrine.esperado.json` | `geradores/oraculo_excesso_shrine` (C#, float + Math.Round + Mathf.CeilToInt) |
| `cores-do-jogo` | `cores-do-jogo.entrada.json` | (so entrada: sao LEITURAS do jogo, sem saida calculada) | `scratch/cor2/le_cores_do_tooltip.py` + `le_guimanager_cores.py` (UnityPy sobre o prefab do jogo) |
| `bt12-berserkers-blood` | `bt12-berserkers-blood.entrada.json` | (so entrada: a TABELA DE CASOS da ancora do fator; o esperado e a leitura do parser) | formas EQUIVALENTES/RECUSADAS da formula do asset - a de referencia vem do dump do asset (`scratch/` nao e versionado); BT-12A |
| `deploy-optin-guarda` | `deploy-optin-guarda.entrada.json` | (so entrada: os casos de XML do opt-in de deploy; o veredito e o da trava) | os `Directory.Build.props` dos 6 mods + as iscas do FURO A/B, escritos a mao; DEPLOY-2 |
| `formato-notas` | `formato-notas.entrada.json` | (so entrada: sao LEITURAS do decompilado do `Tooltip`, sem saida calculada) | `scratch/bancada1/gera_fixture.py` (ilspycmd sobre a `Assembly-CSharp.dll` v1.3.1; `scratch/` nao e versionado); BANCADA-1/FORMATO |

### `cores-do-jogo.entrada.json` — as CORES dos tres niveis (COR-2, 01/10)

Nao e um par entrada/esperado: sao as **leituras datadas** que a convencao de cores
(`docs/TEXTO-TOOLTIPS.md` §7) cita. Os valores saem do **prefab serializado do jogo**
(`Assembly-CSharp::Tooltip` e `Assembly-CSharp::GUIManager`, via UnityPy + TypeTreeGenerator
com as DLLs de `Managed/`), convertidos com a mesma conta do `ColorUtility.ToHtmlStringRGB`.
Nada foi digitado a mao, e nada veio de print.

* **O CONTROLE da leitura** (campo `controle_da_leitura`): o mesmo leitor devolve
  `GUIManager.coldColor` = `#00D7FF`, que e **exatamente** o que o log de uma sessao real
  imprime ao ler o campo em jogo. Sem essa igualdade, um hex lido do asset seria numero solto.
* `log_de_runtime` guarda as linhas copiadas do LogOutput de 01/10 (sessao COM a DLL do
  perfil): o azul lido, o texto final ainda com o marcador, e as **0** ocorrencias da linha
  que o gancho da cor imprimiria se tivesse visto um marcador — a prova empirica do defeito
  de ordem dos ganchos.
* **RESSALVA (FIX-4):** essa sessao rodou com a DLL do perfil, que e a build **PRE-conserto** do
  COR-2 — **nao** e a build nova. Ela prova o comportamento da build ANTIGA (o defeito); **nao**
  prova o conserto. A propria fixture declara isso em `procedencia`/`dll_da_sessao`, e
  `t_cores_niveis.py` exige a declaracao — para a ressalva nao sumir em silencio.
* Quem consome: `tools/testes/testes/puros/t_cores_niveis.py` (via `regras_cor.py`).

Regenerar (mexe no arquivo versionado — rode e revise o `git diff`):

```bash
python scratch/cor2/le_cores_do_tooltip.py "$(date '+%Y-%m-%d %H:%M:%S')"
python scratch/cor2/le_guimanager_cores.py
python scratch/cor2/gera_fixture_cores.py
```

Ao adicionar uma familia nova, acrescente a linha nesta tabela e o campo
`procedencia` no arquivo - a lista e o que permite auditar a fixture depois sem
adivinhar de onde o numero saiu.
