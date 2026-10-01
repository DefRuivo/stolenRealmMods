# tools/testes — arcabouco de testes do projeto

Runner unico, exit code honesto, separacao entre teste que roda sem o jogo e
teste que precisa dele, fixtures versionadas com procedencia e uma prova de fogo
do proprio runner.

Este README e o **contrato**. Quem escreve teste depois (TST-2..TST-6) segue o
que esta aqui em vez de inventar formato novo: o runner, o vocabulario e a
convencao de fixture sao de todo mundo.

A regra do projeto que este diretorio existe para tornar executavel esta em
`docs/PLANO-DE-TESTES.md`:

> **Todo teste tem de ser MOSTRADO REPROVANDO.** Planta o defeito, roda, ve
> falhar; tira o defeito, roda, ve passar. Teste que nunca falhou nao e teste -
> e decoracao.

---

## Como rodar

```bash
python tools/testes/roda_testes.py          # roda TUDO (logica pura + o que precisa do jogo)
bash tools/testes/roda.sh                   # idem, escolhendo o python certo (python3 no CI)
```

Um comando, tres saidas possiveis:

| exit | significado | quando |
|------|-------------|--------|
| **0** | tudo verde | todo teste que rodou passou **e nada ficou por rodar** |
| **1** | algo reprovou | um teste falhou (ou a prova de fogo do runner falhou) |
| **2** | nao consegui rodar | faltou dependencia (lib/ do jogo, dotnet, ...); a mensagem diz qual |

**Nao existe "pulado".** Existe `NAO RODOU`, que vale 2. Se voce rodar a suite
numa maquina sem a `lib/` do jogo, o runner devolve 2 e diz o que faltou - nao
devolve 0 escondendo metade da suite. Um verde que esconde teste que nao rodou e
exatamente o modo de falha que o projeto ja sofreu duas vezes (o `check_patches`
aprovando um aplicador que cobria zero ganchos; a conferencia de shrines que nao
aprovou o formato antigo so porque se recusou a compara-lo).

### Opcoes uteis

```bash
python tools/testes/roda_testes.py --puros        # SO logica pura (e o modo do CI)
python tools/testes/roda_testes.py --jogo         # so o que precisa da lib/
python tools/testes/roda_testes.py --teste tools/testes/testes/puros/t_exemplo_soma_aura.py
python tools/testes/roda_testes.py --lista        # lista o que seria rodado, com requisitos
python tools/testes/roda_testes.py --json         # saida de maquina
python tools/testes/roda_testes.py --lib /caminho/para/lib   # aponta a lib/ do jogo
python tools/testes/roda_testes.py --contra-prova # a prova de fogo do runner (ver abaixo)
```

`--puros` **exclui** os testes de jogo e **mostra** quantos excluiu. Exclusao por
categoria e escolha explicita de quem chamou; nao e teste que sumiu.

---

## O que roda no CI e o que so roda local

* **`categoria: "pura"`** — formula, formatacao, parser, tabela, filtro. Nao toca
  em tipo do jogo: roda em qualquer lugar com Python puro, **inclusive no CI**.
* **`categoria: "jogo"`** — precisa das DLLs do jogo (`lib/`, gitignored: vem da
  instalacao, e a `Assembly-CSharp.dll` e do jogo, proibido distribuir). Roda
  **local**. Declara `requer: ["lib/"]` no META e, sem a lib, sai `NAO RODOU` com
  a lista do que falta.

No CI (`ubuntu-latest`, `.github/workflows/validate.yml`) a `lib/` **nao existe**,
e por isso o CI roda `--puros` (ou o runner inteiro, sabendo que sai 2). O CI deste
projeto tambem **nao compila** nada de proposito (ver o cabecalho do
`validate.yml`): compilar exigiria hospedar DLL do jogo.

> Ainda nao existe passo de testes no `validate.yml`. Quando o dono quiser o
> primeiro, o passo e uma linha: `python tools/testes/roda_testes.py --puros`.
> Nao foi ligado aqui de proposito - esta tarefa nao mexe em CI.

---

## Estrutura

```
tools/testes/
├── roda_testes.py                 o RUNNER (um comando roda tudo)
├── roda.sh                        atalho: escolhe python/python3 e chama o runner
├── arcabouco.py                   biblioteca comum: asserts, fixtures, requisitos, META
├── README.md                      este contrato
├── testes/                        A SUITE (descoberta: t_*.py dentro daqui)
│   ├── puros/                     categoria "pura" - roda sem o jogo
│   │   ├── t_exemplo_soma_aura.py     EXEMPLO de teste puro (usa fixture)
│   │   └── t_prova_de_fogo.py         o teste QUE TESTA O RUNNER
│   └── jogo/                      categoria "jogo" - precisa da lib/
│       └── t_exemplo_referencias_lib.py   EXEMPLO de teste de jogo
├── contra-prova/                  A ISCA: testes que TEM de reprovar (cp_*.py)
│   ├── cp_defeito_soma_aura.py        o defeito plantado  -> REPROVA
│   └── cp_corrigido_soma_aura.py      o mesmo teste, sem o defeito -> PASSA
└── fixtures/                      entradas e saidas esperadas, versionadas
    ├── README.md                  convencao de nome + procedencia
    ├── soma-aura.entrada.json
    ├── soma-aura.esperado.json
    └── geradores/                 como as fixtures foram GERADAS (oraculo C#)
```

Regra de descoberta: sao testes os arquivos `t_*.py` (suite) e `cp_*.py` (isca).
Qualquer outro `.py` na pasta e ignorado **e contado** no relatorio - um nome fora
do padrao nunca vira um teste que desaparece em silencio.

---

## Como escrever um teste

Um arquivo, um META, um `corpo()`. O runner roda cada teste num **subprocesso**
(um teste que estoura nao derruba a suite) e le o resultado de volta.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O que este teste garante, e POR QUE ele existe (o defeito que o motivou)."""
import arcabouco as arc

META = {
    "nome": "meu-teste",          # identificador; e o nome da fixture: <nome>.entrada.json
    "categoria": "pura",         # "pura" (sem o jogo) | "jogo" (precisa da lib/)
    "requer": [],                # requisitos checados ANTES de rodar; hoje: "lib/", "dotnet"
    "descricao": "uma linha do que este teste garante",
    # "esperado": "reprovar",    # so na ISCA (contra-prova) - ver abaixo
}

def corpo():
    dados = arc.ler_json("meu-teste", "entrada")
    arc.igual(minha_formula(dados), 42, "o valor do caso X")

if __name__ == "__main__":
    arc.main(META, corpo)
```

* Devolver `0`/`1`/`2` e responsabilidade do `arc.main` - o `corpo()` so chama
  `arc.igual` / `arc.exigir`. Nao use `assert` do Python como saida: ele funciona
  (vira 1), mas a mensagem nao diz qual caso falhou.
* Requisito desconhecido no META e **erro** (o runner reprova o teste), nao aviso:
  senao um `requer: ["lib"]` com typo viraria um teste "pulado" para sempre.
* Um teste so pode ser dado como visto falhando: plante o defeito, rode
  `--teste <arquivo>`, veja `REPROVOU` (exit 1), tire o defeito, veja `PASSOU`.
  Sem esse passo o teste nao esta pronto - esta decoracao.

### API do `arcabouco`

| o que | para que |
|-------|----------|
| `arc.igual(obtido, esperado, msg)` | comparacao com mensagem que nomeia o caso |
| `arc.exigir(condicao, msg)` | invariante |
| `arc.Falhou(msg)` | reprovar de proposito (exit 1) |
| `arc.NaoRodou(msg, faltando="lib/")` | nao consegui rodar (exit 2) |
| `arc.precisa_lib(dlls=())` | levanta `NaoRodou` se a lib/ faltar, listando o que falta |
| `arc.ler_json(caso, papel)` / `arc.ler_texto(caso, papel, ext)` | fixture versionada |
| `arc.caminho_fixture(caso, papel, ext)` | o caminho, para quem nao le JSON |
| `arc.f32(x)` | arredonda para float de 32 bits (a aritmetica do motor) |
| `arc.raiz_do_repo()` / `arc.dir_lib()` | caminhos |
| `arc.executar_arquivo(caminho)` | roda outro teste como o runner roda (usado pela prova de fogo) |
| `arc.ler_meta(caminho)` / `arc.validar_meta(meta, caminho)` | leitura sem import (o runner usa) |

### Fixtures

Convencao de nome (nao inventar outra):

```
fixtures/<nome-do-teste>.entrada.<ext>     <- a entrada
fixtures/<nome-do-teste>.esperado.<ext>    <- a saida esperada
```

`<ext>`: `json` (padrao), `csv`, `log`, `txt`. O `<nome-do-teste>` e o campo
`nome` do META. Fixture versionada ausente e **defeito** (exit 1), nao dependencia:
ela tem de estar no repositorio.

**A saida esperada precisa ter procedencia.** Fixture gerada pela mesma
implementacao que o teste usa nao prova nada (o teste passaria por construcao). O
padrao esta em `fixtures/soma-aura.*.json`: os valores saem de um **oraculo em C#**
que passa pelo mesmo caminho de conta do motor, e o arquivo declara qual foi. Se
voce precisar de fixture nova, ver `fixtures/README.md`.

### Teste que precisa do `dotnet` (para TST-2..TST-6)

Use `requer: ["dotnet"]` e chame o `dotnet` de dentro do `corpo()` com
`subprocess.run(..., cwd=arc.raiz_do_repo())`. Um `dotnet test` de projeto xunit
fica atras desse wrapper: assim ele continua sob o mesmo contrato (exit 0/1/2) e
nao vira um segundo runner com outra convencao de saida. Traduza o resultado:
build/execucao falhou por falta de dependencia -> `arc.NaoRodou`; teste falhou ->
`arc.Falhou`. Um projeto de teste xunit **nao** deve ser descoberto pelo runner
(nao tem META) - deixe-o em `testes/jogo/<nome>/` como apoio, nao como `t_*.py`.

---

## Prova de fogo (o runner reprova mesmo?)

Duas metades, em `contra-prova/`, que sao **o mesmo teste** (fora do bloco marcado
`BLOCO-DO-DEFEITO` os arquivos sao identicos - e `t_prova_de_fogo.py` confere isso
por comparacao de texto):

* `cp_defeito_soma_aura.py` — o defeito classico do projeto (invariante 1: "todo
  numero exibido e o do MOTOR - nada somado a mao"): o valor esperado foi digitado
  como `40` (20 da base + 20 do Omnism II, esquecendo os +100 do Worship). O motor
  da `44`. **Tem de sair `REPROVOU` (exit 1).** META: `"esperado": "reprovar"`.
* `cp_corrigido_soma_aura.py` — o mesmo teste com o valor vindo da fixture gerada
  pelo oraculo. **Tem de sair `PASSOU` (exit 0).**

```bash
python tools/testes/roda_testes.py --contra-prova
```

O runner **inverte a expectativa** para quem declara `esperado: "reprovar"`: se a
isca reprova, sai `PROVA OK` e o veredito fica VERDE; se a isca **passar**, o
veredito fica `REPROVADO` com `PROVA FALHOU` - ou seja, o runner denuncia a si
mesmo. E `t_prova_de_fogo.py` (que roda na suite normal, no CI) executa as duas
metades nesse mesmo caminho, entao a honestidade do runner e vigiada a cada push.

Para conferir que a prova de fogo **pode** falhar (que ela nao e decoracao): crie
temporariamente um `cp_*.py` que passe com `esperado: "reprovar"` e rode
`--contra-prova` - o veredito tem de ficar vermelho (`PROVA FALHOU`).

---

## Quando um teste acha um defeito de verdade

Nao conserte aqui. O produto deste diretorio sao **testes**. Registre como achado
com prova (comando + saida + arquivo:linha) para o dono decidir o escopo - e, se o
defeito for real, o teste entra na suite com o defeito **ainda presente** e a
tarefa de conserto fica separada. Foi assim que nasceu o `check_patches`: a trava
existe porque o defeito aconteceu, e a trava so vale depois de vista reprovando.

---

## Fora de escopo (de proposito)

* Teste de CENA (o que so aparece em partida) continua roteiro para o dono; o que
  der para capturar em **log**, capture e confira por ferramenta (nao transcreva a
  mao).
* O runner nao instala nada, nao toca no perfil do r2modman, nao compila mod e nao
  muda comportamento de mod nenhum.
