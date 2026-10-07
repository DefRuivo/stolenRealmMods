# AUT-7 — entrega: medicao de estilo/atributos/dump + relatorio de aceite do DoD

Tarefa `t_674c5976`. Escopo exclusivo desta entrega (nada de outro dono foi tocado):

```
tools/automacao/estilo/estilo_atributos.py        (novo)
tools/automacao/estilo/plano-estilo.entrada.json  (novo)
tools/automacao/estilo/test_estilo_atributos.py   (novo)
tools/automacao/aceite/relatorio_aceite.py        (novo)
tools/automacao/aceite/test_relatorio_aceite.py   (novo)
docs/automacao/AUT-7-relatorio.md                 (gerado)
docs/automacao/AUT-7-resultado.json               (gerado)
docs/automacao/AUT-7-evidencias/                  (gerado: 2 JSON do runner)
docs/automacao/AUT-7-revisoes.json                (novo: estado das revisoes AUT-3R/5R/6R)
docs/automacao/AUT-7-entrega.md                   (este)
```

Nao toquei em `tools/automacao/ciclo/**` (CIC-1/2), `tools/automacao/cenarios/**` (CIC-3/4),
`tools/automacao/runtime/**` (CIC-5), `tools/automacao/offline/**` (AUT-3), produto,
`KANBAN.md` nem no board. Nenhum build, deploy, install, jogo, save, commit, push ou publicacao.

## 1. Os dois comandos

### 1.1 Medicao da frente (estilo, atributos e dump)

```bash
python tools/automacao/estilo/estilo_atributos.py --repo C:/dev/stolen-realm \
    --out-dir <dir-de-evidencia> [--observacoes obs.json] [--validar-plano plano-estilo.entrada.json]
```

* **Offline REAL**: roda a suite do projeto (`roda_testes.py --puros` e `--contra-prova`) e
  converte **cada teste** dos quatro mods em UM criterio do contrato do ciclo, com a saida do
  runner gravada e hasheada (`suite-puros.json`, `suite-contra-prova.json`). **Nao reimplementa**
  build, suite nem conferidor.
* **BetterStats nao tem familia `t_bs_*` na suite**: e medido por **recorte estrutural**
  (`tools/testes/recorte.py`, casamento de chaves) contra o `BetterStats/Plugin.cs` vivo — base
  PURA do `SavedMap`, valor FINAL do motor, formato `base (final)`, geometria deslocada UMA vez
  (idempotente), falha-segura e ausencia de escrita no personagem. A ausencia de familia de teste
  fica **declarada** (`suite-ausente`), nunca escondida.
* **Runtime**: 11 aspectos (BetterFont troca+preservacao+config+visual, BetterCombatText
  superficies/contraste-pola­ridade/idempotencia/sem-vazamento no level-up, BetterStats
  base-vs-final/geometria/visual, Debugger contrato do dump/censo). Le o formato REAL do probe
  AUT-4 (`fonte`, `cores`, `keywords`, `geometria`, `personagem`) e o normalizado do coletor CIC-5;
  o modelo de sombra/luminancia/superficies alvo vem de `tools/testes/regras_bct.py` e a lista de
  preservacao de `tools/testes/regras_bf_estilo.py` — **nenhuma formula copiada**.
* **Plano de coleta** (`plano-estilo.entrada.json`), no schema `AUT-4/1` e validado pelo proprio
  contrato do coletor (`validar_plano` + `planejar_rodada`), com alvos NOMEADOS por cenario e
  `coleta_autorizada=false`.

Exit: `0` ha criterio OK e nenhum REPROVADO · `1` algum REPROVADO · `2` nada exercitado.

### 1.2 Relatorio de aceite do DoD (consolidacao offline)

```bash
python tools/automacao/aceite/relatorio_aceite.py --repo C:/dev/stolen-realm \
    --out-dir docs/automacao/AUT-7-evidencias \
    --relatorio docs/automacao/AUT-7-relatorio.md \
    --out docs/automacao/AUT-7-resultado.json \
    [--aut3-resultado ...] [--rstv-observacoes|--rstv-criterios ...] \
    [--shrines-observacoes|--shrines-criterios ...] [--estilo-observacoes ...] \
    [--aceite aceite.json] [--revisoes docs/automacao/AUT-7-revisoes.json]
```

Consolida as QUATRO frentes — AUT-3 (via o orquestrador CIC-1, que confronta o snapshot do
resultado com os bytes ATUAIS), AUT-5 (`cenarios/rstv.py`), AUT-6 (`cenarios/tooltips_shrines.py`)
e AUT-7 (esta frente) — e emite um relatorio **por mod** com **provas, regressao, lacunas e roteiro
humano minimo**. A classificacao NAO e reimplementada: quem decide prova vinculante / falha
automatica / pendencia humana e o `tools/automacao/ciclo/decisao.py` (CIC-2). Faltando o modulo de
decisao, o comando sai INCOMPLETO (exit 2) em vez de improvisar veredito.

**Tres estados separados, sempre:**

| estado | de onde sai | valor nesta rodada |
|---|---|---|
| `tecnico` | decisao CIC-2 (falhas automaticas, pronto_para_decisao) | ver abaixo |
| `aceite_humano` | `--aceite` (declaracao do dono) | `NAO_PRONUNCIADO` |
| `publicacao` | `--aceite` (Thunderstore e imutavel) | `NAO_VERIFICADO` (online nao e consultado) |

E `revisoes` (AUT-3R/5R/6R): enquanto houver revisao pendente, `consolidacao_final=false` — o
relatorio e **PROVISORIO** por declaracao, nao por omissao.

## 2. Resultado real desta rodada (exit 1)

```
criterios=118  OK vinculantes=49  falhas automaticas=64  pendencias humanas=5
frentes: AUT-3=54  AUT-5=1  AUT-6=1  AUT-7=62
pronto_para_decisao=False
consolidacao final: NAO (PROVISORIA) — pendente: AUT-3R, AUT-5R, AUT-6R
```

| mod | estado tecnico | provas | regressao | lacunas | roteiro humano |
|---|---|---|---|---|---|
| BetterTooltips | NAO_EXERCITADO | 0 | 17 | 17 | — |
| BetterFont | NAO_EXERCITADO | 12 | 5 | 6 | 1 (visual/UX) |
| BetterCombatText | NAO_EXERCITADO | 27 | 5 | 6 | 1 (autorizar rodada) |
| BetterStats | NAO_EXERCITADO | 6 | 6 | 7 | 1 (visual/UX) |
| RoguelikeSkillTreeVisualizer | NAO_EXERCITADO | 0 | 8 | 8 | — |
| RoguelikeDebugger | NAO_EXERCITADO | 4 | 4 | 6 | 1 (autorizar boot) |

As provas de BetterFont/BetterCombatText/RoguelikeDebugger sao os **testes puros do projeto**
(9 + 11 + 4) mais as **iscas** (`cp_bf_*`, `cp_bt_*`) que sairam `PROVA_OK` (reprovaram como deviam).
As de BetterStats sao as 6 checagens estruturais desta frente.

## 3. O achado que MANDA nesta consolidacao

**O `AUT-3-resultado.json` do repositorio (15:47, veredito VERDE, sha256 `9c1aa582…`) NAO
corresponde aos bytes atuais**: `snapshot=78, atual=532 arquivos` (454 criados desde entao).
O CIC-1 confere isso e, como manda a regra, **todos os 54 criterios do AUT-3 sairam
`NAO_EXERCITADO`** — nunca OK. E por isso que a tabela acima tem 64 falhas automaticas: a maior
parte e a bancada AUT-3 **stale**, nao defeito de mod.

Acao (para o pai/revisor, **falha AUTOMATIZAVEL — nao vai ao dono**): quando a arvore parar de
mudar, rodar a bancada **uma vez** sobre os bytes atuais e reexecutar este relatorio:

```bash
python tools/automacao/ciclo/ciclo.py --repo C:/dev/stolen-realm --trabalho <scratch> --resultado <saida.json>
python tools/automacao/aceite/relatorio_aceite.py --repo C:/dev/stolen-realm --aut3-resultado <saida.json> ...
```

Sem isso o relatorio nao pode ficar verde — e nao fica "verde" por rotulo.

## 4. Roteiro humano minimo (o residual, agregado por mod+tipo)

1. **BetterCombatText — AUTORIZAR UMA rodada runtime** (superficies alvo/contraste): plano
   `tools/automacao/estilo/plano-estilo.entrada.json`, alvos nomeados (boss healthbar, janela do
   jogador, icone de status, dado). O probe ja le esses objetos; falta a autorizacao da rodada.
2. **RoguelikeDebugger — AUTORIZAR UM boot** com os mods atuais, **sem carregar save**; o
   `LogOutput.log` dessa sessao prova o contrato do dump e alimenta o censo (o `census.py` nao e
   executado aqui porque reescreve doc curada).
3. **BetterFont — JULGAR visual/UX** (fonte legivel/sem corte em tooltip, texto de combate e UI).
   O DoD exige revisao de UI/UX para alteracao de fonte; o dado tecnico ja esta medido.
4. **BetterStats — JULGAR visual/UX** (BS-1a: `base (final)` cabendo no painel na ficha e no
   level-up). Idem: medicao feita, aceite e visual.

Nada alem disso foi empurrado ao dono: lacuna de probe/coleta vira fila tecnica (falha automatica).

## 5. O que NAO foi exercitado e o que o probe ainda nao emite (lacunas ditas)

* **Runtime inteiro**: `NAO_EXERCITADO` — nenhuma rodada autorizada nesta tarefa (jogo, save e
  publicacao proibidos pela tarefa; nenhuma frente runtime iniciada).
* **BetterFont**: a preservacao de cor/contorno/underlay so fecha com o **par ligado/desligado no
  mesmo objeto** (o probe le `fonte`/`cores`/`keywords`, mas nao tem sessao de controle) e a
  **config** do mod nao e emitida por rodada.
* **BetterCombatText**: idempotencia em jogo exige **duas leituras do mesmo objeto** (o probe le
  cada TMP uma vez por passada); o vazamento no level-up exige a marca `nao_deve_exibir_efeito` por
  objeto no plano de coleta.
* **BetterStats**: o probe emite a caixa do TEXTO, mas nao os **valores de atributo do personagem**
  (SavedMap x final) nem a **bbox do painel** — sem eles, base-vs-final e clipping ficam
  `INDETERMINADO`/`NAO_EXERCITADO` mesmo com o texto certo na tela.
* **Debugger censo**: conferir categorias/colunas exige regenerar o censo (escreve doc curada) —
  passo separado e autorizado.
* **AUT-5/AUT-6**: as frentes nao entregaram observacoes/resultado nesta rodada; elas entram como
  `NAO_EXERCITADO` (uma lacuna dita cada), nunca como OK.

## 6. Regras respeitadas (checagens feitas)

* **"Carregado" != "eficaz"**: todo OK desta entrega vem de execucao real (runner/suite/recorte) com
  evidencia em arquivo; nenhum criterio aprova mod por ter carregado.
* **Fixture nao aprova**: com `procedencia=fixture` a ausencia de defeito sai `NAO_EXERCITADO`; um
  DEFEITO plantado continua `REPROVADO` (ha teste para os dois lados).
* **Nunca OK por rotulo**: a cadeia `sessao` + `fonte_sha` + `dll_sha` tem de estar NA OBSERVACAO e
  bater com a identidade da rodada; sem ela, runtime nao fecha OK.
* **Sem auto-assinatura**: identidade desta rodada `fonte_sha=cea9876d3491…`,
  `dll_sha=bca54d2b5545…` (DLL inalterada em relacao a AUT-3/CIC-1).
* **Efeitos colaterais**: perfil do dono **intacto** (plugins+config sem escrita nesta sessao;
  mtime mais recente 14:25), nenhum build/deploy, nenhum jogo, nenhum save, nenhum commit/push,
  nenhuma publicacao, board e `KANBAN.md` intocados.
* **Doc curada nao regerada**: `census.py`, `gera_shrines_esperado`, `grava_shrines_esperado` e
  afins **nao** foram executados.

## 7. Testes desta entrega (16 + 10 = 26 casos, todos verdes)

```
$ python tools/automacao/estilo/test_estilo_atributos.py     -> total: 16 | falhas: 0   TUDO OK  (exit 0)
$ python tools/automacao/aceite/test_relatorio_aceite.py     -> total: 10 | falhas: 0   TUDO OK  (exit 0)
```

Incluem os **controles negativos** (defeito plantado, tem de reprovar):
sombra do BCT igual a letra do texto; par ligado/desligado com cor divergente; fonte que nao troca;
`OUTLINE_ON` em objeto marcado como "nao pode receber o efeito"; `|` antes do `desc=` no log;
BetterStats lendo a base do valor FINAL; geometria sem o deslocamento guardado; rotulo OK sem
evidencia; aceite humano sobre mod com falha automatica (fica INCONSISTENTE e nao esconde a falha).

## 8. Hashes (sha256) desta entrega

```
d34509723514a4263b20eda9eb913ad8f0b9600e0808d3509cce30740404c3dc  tools/automacao/estilo/estilo_atributos.py
ee2e39b7261b73860de779b758242e5c0876234192e358b396856726919c860f  tools/automacao/estilo/plano-estilo.entrada.json
2e35e30f8539375dc0c8b42bfc6317a842fd2928ab0de9b74cfc743e04aeed50  tools/automacao/estilo/test_estilo_atributos.py
01eefefff1dc62d80b8f28fe031105433682efe791b5a1d716c8487887d77e3d  tools/automacao/aceite/relatorio_aceite.py
2baf1e8da27addb99925c6807907d092461ea33b234f6f956768133c21b83d3d  tools/automacao/aceite/test_relatorio_aceite.py
f16b4f39ab11e81aced30048374806547b7ff879944333e9548ebad4d9307808  docs/automacao/AUT-7-relatorio.md
a4dbdc04ac9d8f909c2f595a78525476f3ccf60302490e5ae7cb2a202e134d95  docs/automacao/AUT-7-resultado.json
df9039c26ede3d9b25d4ae31a6ebbdd23ba1f99d373098cc262c2835be32ba8c  docs/automacao/AUT-7-revisoes.json
7058c69c598f18b425fa09460bc7a209fdf7466fc2bccdcf7091487d913a45fa  docs/automacao/AUT-7-evidencias/suite-puros.json
275e6da19ac33c1aa18b725ec51d712c313a013041c610a58ae4cb071eb4320e  docs/automacao/AUT-7-evidencias/suite-contra-prova.json
```

## 9. Limites (honestos)

* **Este relatorio NAO substitui aceite humano nem publicacao do DoD** — e a camada tecnica que
  deixa o residual humano explicito e curto.
* **Consolidacao PROVISORIA**: depende de AUT-3R/5R/6R (e de uma rodada fresca do AUT-3).
* Os testes desta entrega sao de **ferramenta** (nao entram no runner `tools/testes/`), como os das
  frentes CIC; rodam sozinhos com exit 0/1/2.
* `--sem-suite` reusa os JSON ja gravados: serve para reexecutar o relatorio barato, mas um JSON
  ausente vira `NAO_EXERCITADO` (nunca OK).
