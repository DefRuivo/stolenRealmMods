# CIC-4R2 — revisão independente, rodada 3 (lente de CONTRATO) — `t_fa36c892`

Revisor: **run 371, lane `review`** (não-autor: a rodada 1 é do run 341). Leitura **read-only** do
produto: não editei `tooltips_shrines.py`, `test_tooltips_shrines.py`, os `shrines-*.json`, o
oráculo, as tabelas geradas, `checa_shrines.py`, `decisao.py` nem `ciclo.py`. Nada de build, jogo,
install, save, commit, push ou publicação; **nenhuma tarefa criada no board** (achado vai ao pai).

Escritas desta rodada: **este documento**, a nota de superação no topo do parecer da rodada 1
(`docs/automacao/CIC-4R-revisao.md`, só o aviso — os vereditos da rodada 1 ficam intactos) e o
scratch de evidência
`…/hermes/kanban/workspaces/t_fa36c892/cic4r_r3/` (`cic4r_r3.py`, `cic4r_r3_v2.py`, `cic4r_r3_e.py`
e as saídas literais `cic4r_r3_evidence_pre.txt`, `cic4r_r3_evidence_v2.txt`,
`cic4r_r3_evidence_esperado.txt`, `cic4r_r3_travas.txt`).

Método (rodada 3 = contrato): reli o corpo **original** da tarefa e os critérios declarados do
CIC-4 **antes** de rodar, e auditei o que foi entregue contra eles; as variantes novas usam o
**mesmo construtor do caso verde da própria suíte** (`test_tooltips_shrines._rodada_runtime_completa`)
para que a identidade da rodada seja a mesma e nada seja atribuído a uma construção diferente.

## Por que uma rodada 3

A rodada 2 (run 363) deu veredito **mudanças necessárias** com dois itens mínimos — (1) reancorar o
parecer nos bytes atuais e (2) acrescentar as variantes que falsificam um critério declarado — e
**não conseguiu roteá-los**: `kanban_request_changes` foi recusado pelo kernel (*"review handoff has
no valid implementer provenance"*, handoff da run 341 com `implementer=null`), então não havia
implementador para devolver o card. Reancorar é **documento**, não produto: é o que esta rodada faz,
e ela registra o veredito por item contra os bytes que leu.

## Identidade do que foi revisado (sha256 medido 2026-10-05 ~20:07–20:09)

```
df3258e841f7ca9f3f81f41b277f69c63c08b0d4308dcd7c4412afff9b2ddbef  tools/automacao/cenarios/tooltips_shrines.py
0b6436783a9c779d37c970a88af34b3af4d5d365b73b70f88e74bb698b1ced95  tools/automacao/cenarios/test_tooltips_shrines.py
6ef205481d874a3587d07ca433b41565eef29f3323a14259c978cde263f77c52  tools/automacao/cenarios/shrines-casos.json
969b1c693956ee1c3f2de4a3ccb42a9724f502f623d91bd71030867a5e23cdec  tools/automacao/cenarios/shrines-observacoes.exemplo.json
0d60f709d4252d9ff59a08bb1f5e2d4c0697b128601c60f0e538bde57ea6857a  tools/automacao/cenarios/shrines-controle-negativo.json
d6de959e73a090e43da2b5438a12ba1739d32be2bd9494c0fe9f0d84d9163933  tools/automacao/ciclo/decisao.py            (CIC-2, consumidor; não editado)
d6a1b1e9a7b987b6e5d18e9b3fe3122afadab77f76707f786f76cb7d33c06205  tools/automacao/ciclo/test_decisao.py       (não editado)
169c8084388d47a30b0146dd0aa385b808b7d604950f3aaab9a88475911c8288  tools/automacao/ciclo/ciclo.py              (CIC-1; não editado)
a000cc178b2f93007dbf8c948ca553a1c8e9593e37aca52177bcde82e6900296  tools/checa_shrines.py      (fonte/oráculo reusado, intacto)
1ef67649463eeab2b113f1423c8c6667ff24b9162c89633608e6c2a51bf9c562  tools/testes/regras_shrine.py (oráculo, intacto)
d58ee0c931fb5efdff08189f48cbb4085a06c0fc03072c9f3fb9dcae83de5dcc  tools/gera_shrines_esperado.py (fonte, intacta)
836f2833d2ef50e0ee14aaebe17b551f9ed7f6a09fc029771ffced5c048824ce  tools/dados/shrines-esperado.csv   (gerado; fonte do esperado)
99174e006dd7d70560142012d1d752ce7b43113d68751c7b47f7836929e549b2  tools/dados/shrines-percentuais.csv (gerado)
6467698a6a893f16663ab2a725f1775e8c32edd609c8c45c89f5c32656acb0c1  docs/automacao/CIC-4-entrega.md     (supersede CIC-4-correcao.md)
7a41785bf04626d1ece6ca00c1c100362648f9c76c300ec8db477173edffe15d  docs/automacao/CIC-4-correcao.md
35cdaf40a7235b32f5a959356c21fb41d9168338e6563a0a1f53bc1678511aa0  docs/automacao/CIC-4R-revisao.md    (parecer da rodada 1 — intacto)
```

Nada mudou de sha durante a rodada (módulo com mtime 19:59:36, `decisao.py`/`test_decisao.py`
20:00) — diferente da janela de 19:52, quando os arquivos estavam em movimento.

## Veredito por item

| # | item | veredito | prova |
|---|---|---|---|
| R1 | **Âncora do parecer da rodada 1** | **CONFIRMADO (vencido)** | a rodada 1 declara `c5be25b4…`/`73e04315…`; o disco tem `df3258e8…`/`0b643678…` e o `CIC-4-entrega.md` já declara os bytes novos. Pelo aceite #2 de `CICLO-VALIDACAO-escopo.md` ("mudança invalida aprovações anteriores") os 12 vereditos da rodada 1 **não** podem ser usados como âncora |
| R2 | Itens **#8/#9** da rodada 1 | **SUPERADOS** | o `CIC-4-correcao.md` corrigiu ambos; reconfirmado por execução: rótulo runtime sem cadeia ⇒ `NAO_EXERCITADO`; rodada sem artefato ⇒ 0 OK |
| R3 | Item 12 da rodada 1 (fonte/oráculo intactos) | **OK** | hashes de `checa_shrines.py`/`regras_shrine.py`/`gera_shrines_esperado.py`/CSVs idênticos aos da rodada 1 |
| E1–E3 | Item 2 da rodada 1 (esperado **independente e rastreável**) | **OK** | refeito nesta rodada por execução própria (seção abaixo): 99 → `REPROVADO`, oráculo do Flame 40 → `REPROVADO` / 14 → `OK` |
| G1 | Suíte CIC-4 (bytes atuais) | **OK** | `test_tooltips_shrines.py` → **24/24, exit 0** |
| G2 | Isca (prova de fogo do próprio teste) | **OK** | `--isca` → `ISCA|OK|defeito plantado detectado: N1…`, **exit 0** |
| G3 | Fixture nunca verde | **OK** | CLI só-fixture → `OK=7 … com prova runtime: 0`, **exit 2** |
| G4 | Consumidor CIC-2 | **OK** | `test_decisao.py` → `total: 127 | falhas: 0`, **exit 0** |
| G5 | Orquestrador CIC-1 | **OK** | `test_ciclo.py` → `Ran 38 tests … OK`, **exit 0** |
| **A** | **Superfície TOOLTIP ausente não vira `NAO_EXERCITADO`** | **ACHADO (bloqueante — falso verde)** | V1/V1b abaixo: 7 OK, `com_prova_runtime=7`, `exit 0` e `decisao` → `por_mod OK`, `ok_vinculantes=7`, `pronto_para_decisao=True` |
| **B** | **A superfície de contra-prova (tooltip) não é autenticada** | **ACHADO (mesma família)** | V3/V3b abaixo: tooltip `fixture` ou de **outra build** ainda dá `feed_vs_tooltip=IGUAL` e fecha 7 OK/exit 0 |
| C | Evidência **declarada** não é validada | **ACHADO (menor / backlog)** | V2/V2c/V2d abaixo; o consumidor CIC-2 contém o caminho inexistente, mas o **módulo** sai verde |
| D | Ausência de **FEED** é pega | **OK** | V4: só tooltip → 6 `NAO_EXERCITADO`, `exit 2` (a assimetria com o item A é o achado, não a falta desta trava) |

## ACHADO A — sem a superfície TOOLTIP, o módulo fecha verde (e o ciclo também)

O critério declarado é explícito: `tools/automacao/cenarios/tooltips_shrines.py:42-43` —
*"Se so houver uma das duas superficies, o que faltar sai NAO_EXERCITADO (nunca OK)"* — e
`docs/automacao/CIC-4-entrega.md:81` — *"Faltando uma superfície, o que falta sai
`NAO_EXERCITADO`"*. No código, em `_caso_atributo` (l.609-615) a comparação começa com
`if tooltip is not None:`: **não existe o ramo do "faltou a tooltip"**. Sem observação de tooltip o
critério simplesmente pula a comparação e segue para `_decisao_runtime(obs_do_feed, …)`.

Variante **V1** — só o FEED (a observação de tooltip é retirada da rodada); a observação do feed é
byte-idêntica à do caso verde da suíte:

```
{"resumo": {"OK":7,"NAO_EXERCITADO":0,"com_prova_runtime":7,"total":7}, "exit": 0,
 "crit": {"id":"S-dois-personagens-rogue/receptor/bonus=0","estado":"OK","prova_runtime":true,
          "feed_vs_tooltip":null,"superficie_tooltip":null,"superficie_feed":"observacoes[0]"},
 "decisao": {"por_mod":{"BetterTooltips":"OK"},"ok_vinculantes":7,"falhas_automaticas":[],
             "pendencias_humanas":0,"pronto_para_decisao":true}}
```

Variante **V1b** — as tooltips **existem**, mas sem o campo `personagem` (que é o que a l.612 do
módulo usa para casar): mesmo resultado — 7 OK, `com_prova_runtime=7`, `exit 0`, `feed_vs_tooltip=null`.

Consequência: o cenário 2 do CIC-4 ("**feed vs tooltip**", `CIC-4-entrega.md:79-81`) é vendido como
comparação das duas superfícies, e o módulo fecha **verde** sem a segunda superfície existir — com
`prova_runtime=True` e sem nenhuma pendência no ciclo. É exatamente a classe de defeito que o
`CICLO-VALIDACAO-escopo.md` existe para matar ("falso verde"). O consumidor CIC-2 **não** tem como
pegar isso: o critério chega com cadeia completa e `prova_runtime=True`; quem tem de marcar
`NAO_EXERCITADO` é o módulo.

**Rota:** é produto (CIC-4), e a decisão de projeto — marcar `NAO_EXERCITADO` quando falta a
superfície **ou** declarar feed-only como aceitável e corrigir os dois documentos — é do **pai**.
Este revisor não edita produto e não cria tarefa no board (regra do card).

## ACHADO B — a contra-prova de tooltip não é autenticada

O item declarado é "o valor do FEED **e** o da TOOLTIP têm de bater **entre si**" (`CIC-4-entrega.md:79-81`).
A cadeia de runtime (`_cadeia_runtime`) é exigida **só** da observação do feed; a observação de
tooltip entra por `o.get("personagem") == nome and o.get("texto_renderizado")` (l.612) e nada mais é
conferido dela.

Variante **V3** — feed runtime completo (sessão + hash + evidência) e as **tooltips declaradas
`fixture`** (sem sessão, sem hash, sem evidência):

```
{"resumo": {"OK":7,"com_prova_runtime":7,"total":7}, "exit": 0,
 "crit": {"estado":"OK","prova_runtime":true,"feed_vs_tooltip":"IGUAL",
          "superficie_tooltip":"observacoes[1]"},
 "decisao": {"por_mod":{"BetterTooltips":"OK"},"ok_vinculantes":7,"pronto_para_decisao":true}}
```

Variante **V3b** — a tooltip traz `hash_fonte` de **outra build** (`ff…`) e sessão de outra rodada:
mesmo resultado — `feed_vs_tooltip=IGUAL`, 7 OK, `exit 0`, decisão `OK`/`pronto_para_decisao=True`.

Ou seja: uma superfície `fixture` (ou de outra build) satisfaz a comparação que o documento
apresenta como prova de campo. Não é um caso de borda — é o **único** lugar onde a segunda
superfície é exigida.

**Rota:** produto (CIC-4), mesma família do achado A (a correção de A provavelmente fecha B, se a
tooltip passar a exigir a mesma cadeia do feed).

## ACHADO C (menor) — a `evidencia` declarada não é validada

`_evidencia_obs` (l.534-546) devolve os caminhos declarados em `evidencia` **crus**; só `objeto` é
verificado contra o disco. Como a cadeia só testa "lista vazia?" (l.470), qualquer caminho declarado
satisfaz o passo de evidência (o texto do módulo — l.74-76 — e `CIC-4-correcao.md:21` prometem
"`evidencia` só do artefato realmente lido"). Três variantes, com **o caso de regressão presente**
para que o resto da rodada feche:

```
V2  evidencia=["tools/dados/shrines-esperado.csv"]      (o CSV do esperado)   -> 7 OK · exit 0 · decisao OK/pronto_para_decisao=True
V2d evidencia=["tools/automacao/cenarios/tooltips_shrines.py"] (o produto)    -> 7 OK · exit 0 · decisao OK/pronto_para_decisao=True
V2c evidencia=["tools/dados/nao-existe.log"]  (NÃO existe)                    -> módulo 7 OK · exit 0
                                                                                 decisao: por_mod REPROVADO · ok_vinculantes=1 · 6 falhas automáticas
```

Duas leituras, ditas com precisão:

- **V2/V2d**: o consumidor CIC-2 aceita a rodada como `OK_VINCULANTE ×7`. O valor comparado continua
  sendo o esperado independente (não há falso verde **de número** aqui), mas o campo `evidencia` fica
  apontando para a tabela do esperado ou para o próprio produto — o rótulo "artefato lido" não vale.
- **V2c**: aqui há **divergência módulo × ciclo** — o módulo devolve `exit 0` (verde) e o
  `decisao.py` devolve `REPROVADO` (fail-closed, correto). O consumidor contém o defeito, mas o
  produto sozinho mente na mesma rodada.

O teste `evidencia-vem-do-artefato-lido` pina **só** o caso positivo (observação que declara o
artefato real); o caso negativo não está pinado. **Rota:** secundário — só a metade do V2c
(módulo verde × ciclo reprovado) merece entrar na correção do CIC-4; o resto é backlog, e nada
disso é pedido ao dono.

## Prova do item 2 (esperado independente) — refeita nesta rodada

As provas B1/M/N da rodada 1 foram em bytes antigos; refiz as três no módulo atual, mudando **só** o
número do FEED e mantendo a cadeia completa do caso verde:

```
E1  feed Dodge +99% (personagem certo, bonus certo)
    -> REPROVADO · esperado=20.0 · fonte="tools/dados/shrines-esperado.csv (Rogue Aura/DodgeChance bonus=0)
       <- docs/cobertura/status.csv:402" · observado=99.0      (o esperado NÃO vem do log)
E2  Flame MaxHealth=100 dano=40  -> REPROVADO · esperado=14.0 (oráculo) · fonte="shrines-percentuais.csv
       (Flame Shrine Aura/Fodder) + regras_shrine.dano (eixo Source=0)"
E3  Flame MaxHealth=100 dano=14  -> OK · esperado=14.0
```

O esperado continua saindo da tabela gerada + oráculo, com fonte citável, e o eixo do Flame continua
`Source` (RV-30). Item 2 reconfirmado nos bytes atuais.

## Travas rodadas (saída literal, 2026-10-05 ~20:08–20:10)

```
python tools/automacao/cenarios/test_tooltips_shrines.py         TOTAL|rodaram=24 reprovaram=0 nao_rodaram=0   exit 0
python tools/automacao/cenarios/test_tooltips_shrines.py --isca   ISCA|OK|defeito plantado detectado: N1-...   exit 0
python tools/automacao/cenarios/tooltips_shrines.py --observacoes .../shrines-observacoes.exemplo.json
                                                                  OK=7 ... com prova runtime: 0               exit 2
python tools/automacao/ciclo/test_decisao.py                      total: 127 | falhas: 0 · TUDO OK            exit 0
python tools/automacao/ciclo/test_ciclo.py                        Ran 38 tests ... OK                          exit 0
python tools/audita_docs.py                                       "nenhuma inconsistencia encontrada"          exit 0
python tools/checa_citacoes.py                                    117 conferidas, 1 pendencia (em CIC-5R)      exit 1
```

As 5 primeiras são as travas do CIC-4 e dos consumidores; as 2 últimas são as travas de documento
do repo. A única pendência do `checa_citacoes` é **pré-existente e fora desta frente**:
`docs/automacao/CIC-5R-revisao.md:18` cita um arquivo do probe AUT-4 que não existe no repo (caminho
citado lá, não aqui). Nenhuma citação deste documento ficou pendente.

## O que esta rodada NÃO confirma

- **Runtime real (AUT-4/AUT-6) continua NÃO EXERCITADO.** Nenhum objeto vivo lido, nenhuma
  `fonte_sha`/`dll_sha` de sessão em jogo, nenhum artefato de runtime criado. Toda evidência acima é
  **offline/sintética, ancorada por construção nos bytes** — e `fixture ≠ runtime`: nada aqui é
  conclusão de campo.
- Não revisei mérito de CIC-1 (`ciclo.py`), CIC-2 (`decisao.py`) nem CIC-5 — eles foram usados como
  **consumidores** do contrato e rodados como travas (G4/G5), com veredito próprio em outra tarefa.
- A leitura visual final (auras de perigo em campo, RV-49) continua do dono — limitação já declarada
  em `tools/checa_shrines.py`.

## Veredito

**NÃO APROVADO como âncora de ciclo completo.** O parecer da rodada 1 fica **superado por este
documento** (ver a nota no topo dele): era fiel aos bytes de 18:29, mas esses bytes não são mais os
do disco, e os dois achados que ele registrou (#8/#9) já foram corrigidos. Contra os bytes atuais
(`df3258e8…`/`0b643678…`) as travas do CIC-4 estão verdes (G1–G5) e os itens declarados 1, 2, 3, 4,
5, 6, 7, 10, 11 continuam válidos — **a rodada 1 pode ser reconfirmada nesses itens**. O que **não**
passa é o critério declarado da superfície TOOLTIP (achados A e B): o módulo fecha verde — e o ciclo
com ele — sem a segunda superfície existir e sem autenticar a que serviria de contra-prova.

Pelo aceite #6 do `CICLO-VALIDACAO-escopo.md` ("secundário vai backlog sem bloquear"), só A e B
bloqueiam o critério de ciclo completo; C vai para backlog. A rota é do **pai**: correção do CIC-4
(itens A/B/C), e a decisão de projeto é dele/dono — este documento apenas registra, com repro, onde
o declarado e o código divergem.
