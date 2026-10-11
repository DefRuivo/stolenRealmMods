# INT-R1-C5 — parte 01: plano, decisoes e limites (instrumento de cobertura via `ui.localized`)

Cartao: `t_c6b435f8` (INT-R1-C5). Pai: `t_b7f6fc4a` (API-R1, done). Nasce de `INT-R1-parte04.md` §4 (veredito
`[SIMPLIFICAR SEM DEPENDER]`, cartao **C6**).
Rodada comecou em **2026-10-11 04:32** (hora local). Este e o primeiro artefato.

## 1. O que a tarefa pede (escopo fechado, do proprio cartao)

1. Instrumento de bancada (nao e mod publicado) que **assina `ui.localized`**, registra os pares
   (chave/resultado) observados e **cruza com as tabelas do `BetterTooltips`** (`TextFixes`/`TextAppends`)
   e com `docs/cobertura/*.csv`.
2. Saida: textos servidos **sem** entrada (lacuna de cobertura), entradas **nunca servidas** (candidata a
   chave morta), e **resumo por categoria** (skills/status/itens/afixos).
3. Ligado no ritual (`tools/release-check.sh` ou relatorio adjacente) com **caso NEGATIVO obrigatorio**
   (remover uma entrada real -> o instrumento tem de REPROVAR).
4. Veredito declarado: **o mod nao muda em nada** — continua standalone; o instrumento e opt-in.

## 2. Ponto exato do jogo que o instrumento observa (citado, nao inventado)

- `api/Core/Contracts.cs:63` — `HookDescriptor("ui.localized", "OptionsManager", "Localize", true,
  "System.String", "System.String", "LanguageGender", "Gender")`: alvo **estatico**, retorno `string`
  (postfix com `__result`).
- `api/Hooks/HookInstallation.cs` — `HookInstallation.Install(assembly, descriptors, owner, report)` aplica
  `StringPostfix` e emite `RealmHooks.Emit(id, ...)`; `HookNotification.Result` carrega o **`__result`**
  (`api/Core/Contracts.cs:68-77`).
- `api/README.md:42` e `:145-146` — a base 0.1.0 e **observacional**: nao muda resultado nem argumentos.

Consequencia para o desenho: como a API **nao** reescreve, o par observado e
`(chave = arguments[0] (o texto pedido), resultado = __result (o texto servido))`. Comparar os dois E o
instrumento: se o `BetterTooltips` cobre a chave, `resultado != chave`; se nao cobre, `resultado == chave`
(lacuna). Se a chave esta na tabela e mesmo assim `resultado == chave`, a entrada **nao rodou** — e
exatamente a familia de defeito do `INC-1`/`INC-2` (chave errada / entrada morta).

## 3. Decisoes de arquitetura desta entrega (do implementador, nao do cartao)

| # | Decisao | Motivo |
|---|---|---|
| D1 | O instrumento e **offline e deterministico**: le um arquivo de observacao (JSONL) e as tabelas do repo; nao abre o jogo | o cartao exige que o runtime em jogo fique `NAO_EXERCITADO` (a medicao em jogo depende de rodada autorizada pelo dono) |
| D2 | A captura em jogo e um **probe opt-in separado** (`tools/automacao/runtime/LocalizedProbe/`), fora do mod e fora do pacote | o mod precisa **reescrever** `__result`, entao nao pode migrar para a API; o instrumento fica fora dele |
| D3 | A trava (gate) e o **baseline**: as chaves que uma rodada de observacao provou servidas+cobertas. `--verificar` reprova se uma delas sumiu da tabela | e o que torna o instrumento uma **trava de regressao** (familia INC-1: chave que deixa de existir falha em silencio) e da o caso negativo pedido: remover uma entrada real -> REPROVAR |
| D4 | Procedencia explicita: `runtime` vs `FIXTURE`. Fixture **nunca** e evidencia de jogo | regra do projeto (`tools/automacao/runtime/README.md`, secao Regras) |
| D5 | O parser das tabelas e o **unico** (`tools/tabelas.py`), nao um regex novo | regra do repo: um leitor so, senao os numeros divergem (historico `check_dupes` x `check_chave_compartilhada`) |
| D6 | O passo no ritual entra como **adjacente** (`PASSO 7b/9`), com `PENDENTE` quando nao houver observacao | nao renumera os 9 passos existentes nem muda o veredito de release por ausencia de rodada autorizada |

## 4. O que NAO muda (veredito declarado, exigido pelo cartao §4)

- Nenhum arquivo do `BetterTooltips` e editado, movido ou reformatado. Prova por hash antes/depois
  (`docs/automacao/INT-R1-C5-evidencias/`).
- O mod **continua standalone**: nenhum `BepInDependency`, nenhuma referencia a `RealmApi` no `.csproj` do mod.
- O instrumento e **opt-in**: sem `--observacoes`/sem baseline ele nao reprova nada; o passo do ritual fica
  `PENDENTE` ate existir uma rodada autorizada.

## 5. NAO_EXERCITADO desta parte

- Runtime em jogo: `NAO_EXERCITADO` — nenhuma rodada autorizada, jogo nao aberto, perfil nao tocado.
- Nada foi instalado, nada foi publicado.
