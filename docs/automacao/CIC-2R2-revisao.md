# CIC-2R2 — revisão independente da 2ª correção (`decisao.py` / `test_decisao.py`)

Tarefa: `t_fd25da44` (CIC-2, run 369 — revisor). Revisão **read-only** da entrega
`docs/automacao/CIC-2-correcao-2.md` e do contrato de
`docs/automacao/CICLO-VALIDACAO-escopo.md` (seção "Correcoes funcionais da primeira
integracao"). Rodada anterior: `docs/automacao/CIC-2R-revisao.md` (achados 3a/5a/5b e 6).

**Nada foi editado em código, buildado, jogado, instalado, salvo, commitado ou publicado.**
Não toquei em `decisao.py`, `test_decisao.py`, `ciclo.py`, `cenarios/**`, produto, probe,
board ou `KANBAN.md`. Toda evidência é execução offline real (Python 3.14.7) em scratch/`probe/`.

## Veredito

**APROVADO.** Os quatro pontos que o pai mandou fechar nesta reabertura estão fechados e
reproduzidos por execução independente: `prova_runtime=False` nunca vincula, lacuna
técnica/coleta vai à fila de agente (não ao dono), só autorização real/julgamento visual vão
ao dono, e a instrução **específica** entra no roteiro. Ficam **achados não bloqueantes**
(§Achados) — todos em chaves que **nenhum produtor atual emite** (verificado), portanto
*backlog*, e um achado do relatório anterior que **já não existe na árvore atual** (§F4).

## Identidade do que foi revisado (o que revisei é o que foi entregue)

```
d6de959e73a090e43da2b5438a12ba1739d32be2bd9494c0fe9f0d84d9163933  tools/automacao/ciclo/decisao.py
d6a1b1e9a7b987b6e5d18e9b3fe3122afadab77f76707f786f76cb7d33c06205  tools/automacao/ciclo/test_decisao.py
```

shas medidos na árvore de trabalho e **iguais** aos declarados em `CIC-2-correcao-2.md`.
Escopo: só os 2 arquivos + o doc (mtime 20:00/19:57/20:00); `ciclo.py`/`test_ciclo.py`
intocados (18:46/18:45). Nenhum arquivo de scratch no repo.

## O que foi executado (saídas reais desta revisão)

```
$ python tools/automacao/ciclo/test_decisao.py           total: 127 | falhas: 0 | TUDO OK   exit=0
$ python tools/automacao/cenarios/test_rstv.py           exit=0
$ python tools/automacao/cenarios/test_tooltips_shrines.py   rodaram=24 reprovaram=0  exit=0
$ python tools/automacao/ciclo/test_ciclo.py             Ran 38 tests ... OK            exit=0

# CLI real sobre a SAÍDA REAL dos dois produtores (7+7 critérios fixture, identidade real):
$ python tools/automacao/cenarios/rstv.py --observacoes .../rstv-observacoes.entrada.json \
      --identidade .../rstv-identidade.json --out probe/cap-cic3.json          exit=2 (fixture)
$ python tools/automacao/cenarios/tooltips_shrines.py --observacoes .../shrines-observacoes.exemplo.json \
      --identidade .../rstv-identidade.json --out probe/cap-cic4.json --json   exit=2 (fixture)
$ python tools/automacao/ciclo/decisao.py --criterios probe/criterios-14.json \
      --identidade .../rstv-identidade.json --repo C:/dev/stolen-realm --texto   EXIT=1
resumo: {mods: 2, criterios: 14, ok_vinculantes: 0, falhas_automaticas: 2,
         pendencias_humanas: 0, nao_conta_como_prova: 14}
roteiro humano: 0 item(ns)   aceite: NAO_PRONUNCIADO   publicacao: NAO_VERIFICADO

# caminho positivo (offline OK + evidência com sha + identidade suficiente): EXIT=0, pronto=SIM
```

Integração com o CIC-1 exercitada pela decisão **real** (sem rodar o ciclo/AUT-3):

```
carregar_decisao: modulo=True presente=True erro=None
consolidar_decisao: origem=decisao.py pronto=False okv=0 falhas=2 aviso=None
fila_da_decisao: 2 itens, origem=decisao, requer_nova_rodada=True, execucao_automatica=False
```

## Aceite × evidência

| # | critério | evidência |
|---|---|---|
| 1 | comandos/outputs reais, positivos e negativos | suites acima; CLI exit 0 (positivo) / 1 (falha) / 2 (sem critérios, arquivo ausente) |
| 2 | resultado ligado aos bytes atuais, log velho não aprova | runtime `OK` vinculava **antes** de alterar a evidência; com os bytes alterados na mesma rodada → 0 vinculantes + `FALHA_AUTOMATICA` |
| 3 | falha automática volta ao ciclo, não ao usuário | 14 critérios fixture → 2 falhas automáticas, **0 itens** no roteiro humano |
| 4 | relatório humano curto só com o residual | `--texto` mostra roteiro (0 itens no caso real) + "FALHAS AUTOMATICAS (... NAO ao dono)" |
| 5 | sem deploy/jogo/save/publicação | nada disso rodou; `publicacao: NAO_VERIFICADO` (estado separado) |
| 6 | revisão independente | este parecer |

Demandas do pai, verificadas uma a uma por execução: `prova_runtime=False` →
`FALHA_AUTOMATICA`/`prova_vinculante=False` (não ao humano); lacuna de
probe/campo/coleta → fila de agente; `autorizacao_necessaria=true` / `tipo_pendencia` →
pendência humana; instrução específica preservada
(`CONFIRMAR a linha azul do feed na tela` no roteiro, `instrucoes_por_criterio`).
Contrato com os produtores reconciliado: as duas suítes irmãs seguem verdes e os dois limites
(`identidade` sem `sessao`; evidência por caminho do artefato) estão pinados em teste nomeado
`CONTRATO: ...` — confirmei que `test_tooltips_shrines.py::t_runtime_verde_integra_decisao`
realmente consolida com identidade `{fonte_sha, dll_sha, raiz}` (sem `sessao`) esperando 7 OK,
logo apertar ali seria falso vermelho.

## Contra-prova (mutantes) — refeita nesta revisão

Reproduzi o mecanismo: removendo a **fiscalização de fato** o teste reprova e nomeia a trava.

```
remove a deteccao de contradicao manifest criterio x coleta -> exit=1
  REPROVADAS: manifest do criterio nao sobrescreve o da coleta -> falha tecnica (nao OK)
remove o confronto dos hashes declarados com a identidade (cadeia runtime) -> exit=1
  REPROVADAS: hash de cadeia aninhado divergente -> falha tecnica (nao OK)
guarda so a PRIMEIRA instrucao na agregacao -> exit=1
  REPROVADAS: agregacao preserva as DUAS instrucoes no roteiro
```

## Achados (NÃO bloqueantes; nenhum alcançável pelos produtores atuais)

**F1 — docstring/relatório prometem mais do que o código faz no bloco `cadeia` (offline).**
`_declarados_hashes` lê `*_sha` no topo **e** o bloco `hashes`, mas **não** `cadeia`/`artefatos`;
o confronto de bloco aninhado só acontece no caminho runtime (`_cadeia_runtime` via
`_valor_cadeia`). Sondas:

```
offline OK + cadeia={"dll_sha": <outra build>}   -> OK_VINCULANTE   (deveria falhar)
offline OK + artefatos={"fonte_sha": <outra>}    -> OK_VINCULANTE   (deveria falhar)
offline OK + hashes={"dll_sha": <outra>}         -> FALHA_AUTOMATICA  (esta coberto)
```

Latente: nenhum critério real traz `cadeia`/`artefatos` (inspecionei as 21 chaves dos 14
critérios reais dos produtores; `grep` nos dois produtores: zero `"cadeia"`). Correção mínima
quando o pai quiser: `_declarados_hashes` ler os mesmos blocos que `_valor_cadeia`, **ou**
corrigir a frase do docstring/relatório (linhas 45-50 do módulo) para dizer que `cadeia` só é
confrontado no caminho runtime.

**F2 — rota `requer_humano` (visual) perde o texto específico.** `_sinal_humano` aceita
`requer_humano` com "visual", mas `_item` não carrega esse campo e `_instrucao_humana` no item
normalizado só vê `instrucoes_humanas`/`julgamento_humano` → sai a instrução genérica:

```
requer_humano="visual: CONFIRMAR a linha azul do feed" -> item julgamento_visual, instrucao GENERICA
julgamento_humano="CONFIRMAR o layout do tab X"        -> instrucao ESPECIFICA preservada (ok)
```

É a mesma classe do achado 5b (fechado para `julgamento_humano`), numa rota mais estreita;
latente (nenhum produtor emite `requer_humano`).

**F3 — nomes dos mutantes M4/M5 superestimam o que está pinado.** A inversão literal
"manifest do critério sobrescreve o da coleta" (trocar a ordem do `update`) **não** é detectada
pela suíte (exit 0) — a contradição e o hash do arquivo já fecham o caminho; o que a suíte pega,
e está correto, é a remoção da *detecção de contradição*. Idem "ignorar o grupo `cadeia`": essa
mutação falha fechado por outro motivo ("sem fonte_sha"). As travas existem e funcionam; só a
narrativa do mutante precisa do nome certo. Sem efeito de comportamento.

**F4 — o "ACHADO para o pai" do relatório está DESATUALIZADO na árvore atual.** O relatório diz
que os produtores discordam sobre `hash_fonte` (`rstv.py:97` → `dll_sha` ×
`tooltips_shrines.py:389` → `fonte_sha`). Hoje **os dois** usam
`_ALIAS_HASH = (("hash_fonte","dll_sha"), ("hash_dll","dll_sha"))` (`rstv.py:97`,
`tooltips_shrines.py:122`) com a justificativa de R-1/CIC-5R. Não há decisão pendente a tomar
antes da frente runtime; o item pode sair do radar do pai.

## O que esta revisão NÃO confirma

- Nenhuma rodada runtime/build/jogo/save. Os `runtime OK` positivos usam evidência de arquivo
  local plausível — **não** medição de jogo; provar runtime real continua dependendo das frentes
  AUT-4/5/6 autorizadas.
- Comportamento real do probe em jogo (campos que hoje não emite) segue NÃO EXERCITADO.
- Aceite humano e publicação permanecem fora da automação (`NAO_PRONUNCIADO`/`NAO_VERIFICADO`).
