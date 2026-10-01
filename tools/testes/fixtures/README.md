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

Ao adicionar uma familia nova, acrescente a linha nesta tabela e o campo
`procedencia` no arquivo - a lista e o que permite auditar a fixture depois sem
adivinhar de onde o numero saiu.
