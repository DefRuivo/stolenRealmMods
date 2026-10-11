# KIT-09 — entrega: pacote de cenarios RSTV em criterios pequenos e rastreaveis

Cartao `t_a4ca00f9` · perfil `default` · run 635 · **offline**.

> Nada de jogo: nenhum probe instalado, nenhum jogo aberto/encerrado, nenhum save
> carregado, nenhum build/deploy no perfil do dono, nenhum commit/push/publicacao.
> Tudo o que foi exercitado sao **bytes em disco deste repo** e o proprio avaliador.
> **Runtime NAO_EXERCITADO** (exige KIT-G1/G2 e autorizacao do dono).

## 1. Objetivo

Reusar AUT-5 (`t_76a41ea7`, plano `tools/automacao/aut5/cenarios-rstv.json`) e CIC-3
(`t_7fdce47f`, avaliador `tools/automacao/cenarios/rstv.py`) para cobrir observacao e teste
do Skill Tree Visualizer com criterios **pequenos e rastreaveis**, sem reabrir o aceite
funcional anterior dos mods e sem duplicar infraestrutura.

## 2. O que foi entregue (arquivos NOVOS; nenhum artefato de outra frente editado)

| arquivo | papel | sha256 (64) |
|---|---|---|
| `tools/automacao/cenarios/kit09.py` | 21 criterios pequenos, `avaliar_cenarios`, `por_capacidade`, `resumir`, CLI | `a4f7587641174960affab6be73590071fe181c86de919dbb87cceb28025f6586` |
| `tools/automacao/cenarios/test_kit09.py` | suite executavel + `--contra-prova` + 21 controles + costura CIC-5 | `e1b05706f164b4c6a94a87bb7265e7f49942693ea46fb3ffa19a02827d50fd28` |
| `tools/automacao/cenarios/kit09-verdade.entrada.json` | artefato SINTETICO que fecha os 21 OK | `596681293039face875a14ca0a25f573c8623fe26f94553778910eebe9c0ad9c` |
| `tools/automacao/cenarios/kit09-la.entrada.json` | ausencia/malformado/fixture — nunca OK | `95fd09336b179c04ce9af4ba95fea25a6bf9340f84d0f7e73e95d8b7e23923f0` |
| `tools/automacao/cenarios/kit09-velho.entrada.json` | DADO VELHO (outra sessao) — reprova | `218dd5018516de1a854d201310921464cfd6bd882ca07c3930eb4935a14686e0` |
| `tools/automacao/cenarios/kit09-identidade.json` | identidade-exemplo (+`sessao_esperada`) | `9c7983b0a061106b565f2caee3cdd753549f6fb9a1016e4ef4d76d29dac1c7b3` |
| `scratch/kit/k09/prova-red-kit09.py` | prova RED (defeito plantado + restauracao byte a byte) | `3b6348791c8a6aa7c8972f9842a6057603dfae88b3ca838903fa9dd9e6410543` |
| `scratch/kit/k09/cli-{verdade,velho,la}.json` | saidas reais das 3 rodadas de CLI | ver `scratch/kit/k09/` |

Lidos e **nao editados** (hashes no momento desta rodada):
`rstv.py` = `f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7`,
`runtime/coletor.py` = `159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d`,
`runtime/fixtures/probe-saida-exemplo.entrada.json` =
`bb37d9a2e4fddec8d955aa5b1354e6672d45063fe8256fb616b25c17d7262754`.

## 3. Contrato entregue

`kit09.avaliar_cenarios(observacoes, identidade) -> [criterio]` com TODOS os campos do
ciclo (`id`, `mod`, `estado`, `classe`, `procedencia`, `esperado`, `observado`, `evidencia`,
`motivo`, `tarefa_origem`) **mais** os campos de rastreabilidade do KIT-09:

- `capacidade_pai` — uma das 7 capacidades macro do CIC-3, ou `KIT09-RSTV5-botao-run`;
- `cenario_origem` — `S1`..`S5` do plano AUT-5;
- `esperado_origem` — **origem do esperado independente** (nunca o valor observado);
- `tarefa_kit` = `t_a4ca00f9`; `tarefa_origem` = `t_76a41ea7` (rastreabilidade AUT-5);
- `por_capacidade(criterios)` faz o **roll-up do pior estado** para a decisao existente (CIC-1/2);
- `resumir` preserva o formato do CIC-3 (`contagem`, `reprovado`, `runtime_exercitado`) e
  acrescenta `por_capacidade` + `criterios_total`.

## 4. Os 21 criterios pequenos

| criterio | capacidade_pai | cenario | esperado (independente) |
|---|---|---|---|
| KIT09-RSTV21-abre | RSTV-21-janela-ciclo | S1/S4 | janela ABERTA |
| KIT09-RSTV21-fecha | RSTV-21-janela-ciclo | S1/S4 | janela FECHADA |
| KIT09-RSTV21-fecha-x | RSTV-21-janela-ciclo | S1/S4 | fechamento pelo X |
| KIT09-RSTV21-fecha-esc | RSTV-21-janela-ciclo | S1/S4 | fechamento pelo Esc |
| KIT09-RSTV6-personagem | RSTV-6-readonly-personagem | S1/S3/S4 | personagem == alvo declarado antes da leitura |
| KIT09-RSTV6-skills-sem-mutacao | RSTV-6-readonly-skills-pontos | S1/S4 | skills antes == depois |
| KIT09-RSTV6-pontos-sem-mutacao | RSTV-6-readonly-skills-pontos | S1/S4 | pontos antes == depois |
| KIT09-RSTV26-render-observado | RSTV-26-placeholders | S5 | texto RENDERIZADO observado |
| KIT09-RSTV26-sem-placeholder | RSTV-26-placeholders | S5 | nenhum literal no render |
| KIT09-RSTV21-tooltip-pai | RSTV-21-tooltip-restauracao | S1 | pai restaurado |
| KIT09-RSTV21-tooltip-indice | RSTV-21-tooltip-restauracao | S1 | indice restaurado |
| KIT09-RSTV21-sem-duplicata | RSTV-21-tooltip-restauracao | S1/S4 | `janelas_duplicadas == 0` (contagem valida) |
| KIT09-RSTV25b-arestas | RSTV-25b-dependencia | S5 | linhas por tier == Dependency REAL |
| KIT09-RSTV25b-sem-aresta-inventada | RSTV-25b-dependencia | S5 | nenhuma linha sem Dependency |
| KIT09-RSTV25b-ausencia-legitima | RSTV-25b-dependencia | S5 | tier com Dependency 0 e 0 linhas segue sem conector |
| KIT09-RSTV-geo-medida | RSTV-geometria-clipping | S5 | bbox finita, dimensoes > 0 |
| KIT09-RSTV-geo-clipping | RSTV-geometria-clipping | S5 | bbox dentro da tela |
| KIT09-RSTV5-handler | KIT09-RSTV5-botao-run | S4 | handler do botao da run INVOCADO |
| KIT09-RSTV5-clique-fisico | KIT09-RSTV5-botao-run | S4 | clique FISICO recebido, alvo nomeado |
| KIT09-RSTV5-sem-obstrucao | KIT09-RSTV5-botao-run | S4 | obstrucao AVALIADA e ausente |
| KIT09-sessao-atual (meta) | — | todas | sessao == `sessao_esperada` da identidade |

Destaques pedidos pelo cartao, e como ficaram:
**handler != clique fisico** (criterios separados: um nao fecha o outro);
**"ativo" nao prova ausencia de obstrucao** (`ativo_na_hierarquia` sem o bloco `obstrucao`
sai NAO_EXERCITADO nomeando a falacia);
**dependency real governa as arestas** e **ausencia legitima nao inventa conector**;
**dado velho reprova**; **esperado independente rastreavel** (campo `esperado_origem`).

## 5. Comandos exercitados (saida real)

```
python tools/automacao/cenarios/test_kit09.py
  RESULTADO|PASSOU|kit09-rstv|KIT-09: 21 criterios pequenos rastreaveis RSTV; fixture/
  ausente/malformado nunca OK; 21 controles reprovam; handler != clique; ativo nao prova
  obstrucao; dado velho reprova                                            exit 0

python tools/automacao/cenarios/test_kit09.py --contra-prova
  CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os 21 controles passarem
  (o REPROVADO real vem da regra)                                          exit 0

python scratch/kit/k09/prova-red-kit09.py
  [verde] exit=0 | defeito plantado (laco do placeholder neutralizado) | [red] exit=1:
  "controle 'placeholder-no-render' tem de REPROVAR KIT09-RSTV26-sem-placeholder
   (obtido OK: leitura runtime completa com identidade suficiente): esperado
   'REPROVADO', obtido 'OK'" | sha256 restaurado == sha256 original (byte a byte)
  | [verde-de-novo] exit=0 | PROVA-RED|PASSOU                               exit 0

python tools/automacao/cenarios/kit09.py --observacoes kit09-verdade.entrada.json \
       --identidade kit09-identidade.json --out scratch/kit/k09/cli-verdade.json   exit 0
python tools/automacao/cenarios/kit09.py --observacoes kit09-velho.entrada.json \
       --identidade kit09-identidade.json --out scratch/kit/k09/cli-velho.json     exit 1
python tools/automacao/cenarios/kit09.py --observacoes kit09-la.entrada.json \
       --identidade kit09-identidade.json --out scratch/kit/k09/cli-la.json        exit 2

travas do repo (com os arquivos novos no lugar):
  check_segredos exit 0 · check_padroes_segredo exit 0 · check_dupes exit 0 · audita_docs exit 0
```

O que a suite cobre (com grupos nomeados no arquivo): contrato/schema dos 21 criterios +
`esperado_origem` independente; fixture do CIC-3 nunca OK; ausente -> tudo NAO_EXERCITADO;
12 casos de ausencia/malformado nunca OK; **21 controles negativos** (um por criterio,
inclusive o mesmo defeito dentro de uma fixture: defeito continua REPROVANDO); caminho OK
dos 21 no artefato sintetico; handler x clique (dois sentidos); "ativo" sem obstrucao;
dado velho e ausencia de `sessao_esperada`; conector ausente x aresta inventada x ausencia
legitima; roll-up do pior estado; adaptador lendo o bloco `campos` NORMALIZADO do coletor
CIC-5 REAL (inclusive os campos novos do contrato) e a CLI nos 3 exit codes.

## 6. ACHADO DE FRONTEIRA — `test_rstv.py` (CIC-3) vermelho no disco atual

`python tools/automacao/cenarios/test_rstv.py` -> `RESULTADO|REPROVOU|cic3-rstv|hash_fonte ==
dll_sha tem de amarrar a build (integracao CIC-5/R-1): esperado 'OK', obtido
'NAO_EXERCITADO'` **exit 1**. Causa MEDIDA: o filtro de alvo do KIT-R0F exclui a fixture
real do probe porque ela declara `owners=com.gumatos.bettertooltips,com.gumatos.betterfont`
(modulo que nao e o alvo do RSTV). Nao e regressao desta frente: `kit09.py` e arquivo NOVO e
`rstv.py`/`coletor.py`/`fixtures/**` nao foram escritos aqui (hashes na secao 2). Nao se
edita artefato de terceiro para deixar a auditoria verde; o passo seguinte (alinhar a suite
do CIC-3 ou o `owners` da fixture ao filtro do KIT-R0F) e do controlador.

## 7. Limites (o que NAO foi provado)

- **Runtime/pixels/desempenho NAO_EXERCITADO**: nenhuma leitura de objeto em sessao viva.
  A suite NAO e prova de produto; fixture testa o AVALIADOR.
- Contrato NOVO declarado e nao emitido pelo probe de hoje:
  `janela.fechado_x`/`fechado_esc`, `handler_invocado`, `clique_fisico`, `obstrucao`
  (e `janela.aberta/fechada` por criterio pequeno). Ausentes -> `NAO_EXERCITADO` +
  `lacuna_probe` + `tipo_pendencia='tecnica'` (nunca OK, nunca maquiado como emitido).
- Automacao NAO substitui o aceite humano em jogo (DoD item 1) nem a publicacao
  (DoD item 3/4): a rodada com PNG por cena continua sendo do dono.
- Nada instalado, nada publicado, nada commitado.

## 8. Handoff

Implementador: perfil `default`, run 635 (cartao `t_a4ca00f9`). Filho de revisao
independente ja existente: `t_0564b789` (KIT-09R) — liberado por esta conclusao.
Caminhos de prova: secao 2 (artefatos + hashes) e `scratch/kit/k09/` (prova RED + 3 saidas
de CLI). Autoria do implementador != revisao: nao houve autoaprovacao.
