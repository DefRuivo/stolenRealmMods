# INT-R1-C5 — parte 02: o instrumento (o que mede, como se roda, o que ja esta provado)

Rodada de 2026-11-10 (iniciada 04:32, hora local). Todas as evidencias desta parte estao em
`docs/automacao/INT-R1-C5-evidencias/`.

## 1. Arquivos criados (nenhum arquivo do `BetterTooltips` foi tocado)

| Arquivo | Papel |
|---|---|
| `tools/cobertura_ui_localized.py` | **o instrumento**: le a observacao (JSONL de `chave`/`resultado`), cruza com as tabelas do mod (parser unico `tools/tabelas.py`) e com o censo (`docs/cobertura/*.csv`); roda a TRAVA do baseline; tem `--prova` |
| `tools/automacao/runtime/LocalizedProbe/LocalizedProbe.csproj` + `LocalizedProbePlugin.cs` | **o probe opt-in** que assina `ui.localized` pelo barramento da API e grava o JSONL (nao e mod, nao tem alvo de deploy) |
| `tools/testes/testes/puros/t_cobertura_ui_localized.py` + `tools/testes/fixtures/cobertura-ui-localized.{entrada,esperado}.json` | o teste da suite (categoria `pura`) |
| `tools/testes/contra-prova/cp_cobertura_ui_localized_isca.py` / `..._ok.py` | a isca (esperado REPROVAR, cita `entrada-removida`) e a metade OK |
| `tools/release-check.sh` | passo ADJACENTE `7b. COBERTURA` (nao renumera os 9 passos) |
| `.github/workflows/validate.yml` | passo CI `7b. Cobertura das tabelas (instrumento ui.localized)` = `--prova` |
| `docs/automacao/INT-R1-C5-*` | estes artefatos + evidencias |

## 2. A semantica da medicao (lida no fonte, nao suposta)

`BetterTooltips/Patches/LocalizePatch.cs:2482-2563`: o postfix so age quando `__result == original`
(ingles), procura `original` **primeiro** em `TextFixes` e depois em `TextAppends` (if/else if na
MESMA chave). Disso o instrumento tira quatro leituras, cada uma com nome proprio:

| observacao | leitura |
|---|---|
| chave sem entrada na tabela | `lacunas` — o mod nao toca nesse texto |
| chave em `TextFixes` e `resultado != chave` | `cobertos` (reescrito) |
| chave em `TextAppends` e `resultado != chave` | `cobertos` (nota anexada) |
| chave NA tabela e `resultado == chave` | `nao_aplicados` — **a entrada nao rodou** (familia INC-1/INC-2: chave errada falha em silencio) |

Mais duas listas de diagnostico: `chaves_mortas` (entrada da tabela que a observacao NUNCA serviu) e
`chaves_compartilhadas` (mesma chave nas duas tabelas = a de `TextAppends` nunca roda, BUG-32).

## 3. A prova do instrumento: `Ran 11 tests; failures: 0`

```
$ python tools/cobertura_ui_localized.py --prova
  [ ok  ] o parser unico le as duas tabelas reais e elas nao estao vazias
  [ ok  ] caso negativo: REMOVER uma entrada real faz a trava REPROVAR (e so ela)
  [ ok  ] chave que passa a existir nas DUAS tabelas e reprovada (BUG-32)
  [ ok  ] servido SEM entrada vira LACUNA, com a categoria do censo
  [ ok  ] chave na tabela servida SEM alteracao e ENTRADA QUE NAO RODOU (familia INC-1)
  [ ok  ] entrada da tabela que o jogo NUNCA serviu entra em chaves_mortas
  [ ok  ] resumo por categoria conta servidos/cobertos/lacunas certo
  [ ok  ] saida por arquivo traz contagem do censo e as contagens da medicao
  [ ok  ] baseline do repo real verifica VERDE com as tabelas de hoje
  [ ok  ] observacao valida e JSONL invalido DEFEITO (nao silencio)
  [ ok  ] procedencia e declarada: fixture nao se disfarca de runtime

Ran 11 tests; failures: 0
```

`docs/automacao/INT-R1-C5-evidencias/01-prova-verde.txt` (exit 0).

## 4. O CASO NEGATIVO (obrigatorio pelo cartao §3): vermelho -> verde

O caso negativo NAO e uma afirmacao no documento: e um comando. `--demonstrar-negativo <dir>` escreve,
DENTRO do dir, uma copia do `LocalizePatch.cs` com **uma entrada real removida** e roda a trava nos
dois:

```
$ python tools/cobertura_ui_localized.py --demonstrar-negativo scratch/int-r1-c5-negativo
entrada real removida na copia: '10% chance to cast Level [level value] {SKL=Meteor} when Striking.' (tabela TextFixes)
--- 1) METADE VERDE: o fonte INTACTO contra o MESMO baseline ---
   violacoes: 0 -> TRAVA VERDE
--- 2) METADE VERMELHA: a copia SEM a entrada, mesmo baseline ---
   [entrada-removida] '10% chance to cast Level [level value] {SKL=Meteor} when Striking.' esperada em TextFixes
veredito: intacto -> exit 0 (verde) | sem a entrada -> exit 1 (REPROVADO)
CASO NEGATIVO PROVADO: vermelho->verde pela remocao de UMA entrada real.
```

`02-caso-negativo.txt`. O arquivo do mod (`BetterTooltips/Patches/LocalizePatch.cs`) nunca e escrito: a
copia mutada vai para o diretorio pedido (`scratch/`, gitignored).

E o mesmo defeito plantado em **testes versionados**:

- `python tools/testes/roda.sh --teste tools/testes/testes/puros/t_cobertura_ui_localized.py` -> **PASSOU**
  (exit 0): prova verde, medicao sintetica pela fixture, medicao sobre o censo real, trava mordendo e o
  sha256 do `LocalizePatch.cs` igual no inicio e no fim;
- `python tools/testes/roda.sh --contra-prova` -> **VERDE (exit 0)**, 68 testes, "prova de fogo: 52 ok":
  a isca `contra-prova-cobertura-ui-localized` aparece como `[PROVA OK]` reprovando pelo motivo certo
  (`entrada-removida`), e a metade `...-ok` PASSOU. Evidencias `05-contra-prova.txt` e `06-suite-puros.txt`.

> Nota honesta sobre a suite: `roda.sh --puros` sai **exit 1** com 94 testes por causa de UM teste
> **pre-existente e alheio** a esta rodada (`deploy-optin-repo`, que varre o repositorio inteiro e tropeca
> nas iscas de rodadas anteriores em `scratch/kit/KIT-14-run699|run710/...`). Prova em
> `11-achados-passo3-pre-existentes.txt`: mtime dos 3 arquivos apontados = **2026-10-10 13:11, 13:14 e
> 17:46** (véspera), `scratch/` e gitignored (`.gitignore:49`), e `find scratch -name '*.csproj'
> -newermt '2026-10-11 04:32:00'` = **vazio**. Nada desta rodada entrou na varredura.

## 5. A medicao de verdade sobre o CENSO REAL (rotulada FIXTURE)

`--gerar-observacao` monta uma observacao derivada do censo + tabelas reais, com
`"procedencia":"FIXTURE"` em CADA linha (`03-gerar-observacao.txt`: 264 linhas). O relatorio
(`04-relatorio-fixture.txt`, JSON em `relatorio-fixture.json`):

```
 entradas na tabela ....: TextFixes=101  TextAppends=197
 COBERTOS (mod agiu) ...: 264      LACUNAS: 0      NAO RODARAM: 0      NUNCA SERVIDAS: 34
 categoria  servidos cobertos lacunas na tabela
 skills           85       85        0        85
 status          107      107        0       107
 itens             9        9        0         9
 afixos            9        9        0         9
 powerups         54       54        0        54
 arquivo             no censo servidos cobertos lacunas
 skills.csv               451       85       85        0
 status.csv               545      107      107        0
 itens.csv                192        9        9        0
 afixos.csv               285        9        9        0
 powerups.csv              79       54       54        0
```

O que isso **prova** e o que **nao prova**, com numero:

- 298 chaves distintas nas tabelas; **294** estao no censo e **4 nao** — `Resist Divine`,
  `Resistance Divine` (grafia duplicada) e duas dicas de loading (`Shops are refreshed...`,
  `A well timed healing or mana potion...`). As 2 dicas ja estao declaradas fora do censo
  (`docs/cobertura/README.md`, "O que este censo AINDA nao cobre"); `Resist Divine`/`Resistance Divine`
  sao **candidatas a chave morta** que o censo estatico sozinho nao separa (esta declarado como
  candidata, nao como conclusao).
- `por arquivo` traz a contagem do censo ao lado das contagens medidas (aceite §2). A coluna lida e
  `descricao` (o texto que o JOGO serve); por isso `skills` mede 85/451 aqui e o `check_fix_keys.py`
  conta 106 — ele tambem olha a coluna `nome`. Nao e divergencia: sao colunas diferentes, e a definicao
  de cada uma esta escrita.
- **FIXTURE nao e evidencia de jogo.** O instrumento carimba a procedencia e o passo do ritual trata
  fixture como `PENDENTE`. O numero acima e o mesmo tipo de medicao que a rodada em jogo daria, mas
  **nao substitui** a rodada: em jogo aparecem textos de UI que o censo nao cobre (a lista de `lacunas`
  de verdade so existe la).

## 6. O probe opt-in (compila hoje; runtime NAO_EXERCITADO)

```
$ dotnet build tools/automacao/runtime/LocalizedProbe/LocalizedProbe.csproj -c Release
Compilacao com exito.  0 Aviso(s)  0 Erro(s)          (07-build-probe.txt)
```

O probe: `Autorizado=false` (padrao) grava `{"status":"NAO_EXERCITADO"}` e **nao instala hook**; com
`Autorizado=true` confere a identidade do jogo (sha256 do `Assembly-CSharp.dll` contra
`ApiIdentity.AssemblySha256`, fail-closed) antes de assinar `ui.localized` e gravar o par
`(chave, resultado)` com `"procedencia":"runtime"`. Sem alvo de deploy: compilar nao escreve no perfil.

Conferencia offline da constante do gate (a copia local do assembly do jogo):

```
$ sha256sum lib/Assembly-CSharp.dll
8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a *lib/Assembly-CSharp.dll
api/Core/Contracts.cs:21:  AssemblySha256 = "8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a";
```

**NAO_EXERCITADO**: carregar o plugin no BepInEx, assinar o hook em jogo e gerar o JSONL de runtime —
depende de rodada autorizada pelo dono (runbook na parte 03). O que esta exercitado e o que da para
exercitar sem o jogo: compilacao limpa e o gate com o mesmo sha256 da copia local do assembly.
