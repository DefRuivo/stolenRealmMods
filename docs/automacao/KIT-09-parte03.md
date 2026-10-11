# KIT-09 — parte 03 — implementacao, provas reais e um achado de fronteira

Cartao `t_a4ca00f9` · offline · nenhum jogo/save/build publicavel/publicacao.

## 1. Entregue nesta rodada (arquivos NOVOS, nada de outra frente editado)

| arquivo | papel |
|---|---|
| `tools/automacao/cenarios/kit09.py` | pacote de cenarios: 21 criterios pequenos, `avaliar_cenarios`, `por_capacidade`, `resumir`, CLI |
| `tools/automacao/cenarios/test_kit09.py` | suite executavel (`arcabouco`, exit 0/1/2) + `--contra-prova` + 21 controles + costura com o coletor CIC-5 |
| `tools/automacao/cenarios/kit09-verdade.entrada.json` | artefato SINTETICO que fecha os 21 criterios OK (hashes/sessao batendo) |
| `tools/automacao/cenarios/kit09-la.entrada.json` | casos de ausencia/malformado/fixture — nunca OK |
| `tools/automacao/cenarios/kit09-velho.entrada.json` | DADO VELHO (sessao de outra rodada) — reprova |
| `tools/automacao/cenarios/kit09-identidade.json` | identidade-exemplo (`fonte_sha`/`dll_sha`/`sessao_esperada`) |
| `scratch/kit/k09/prova-red-kit09.py` | prova RED: planta defeito, mostra reprovacao e restaura byte a byte |
| `scratch/kit/k09/cli-*.json` | saidas reais das 3 rodadas de CLI |

Nenhum arquivo de outra frente foi editado: `rstv.py`, `coletor.py`, `aut5/**`,
`tooltips_shrines.py` e `decisao.py` foram apenas LIDOS.

## 2. Provas reais (comandos exercitados com exit code)

```
python tools/automacao/cenarios/test_kit09.py
  -> RESULTADO|PASSOU|kit09-rstv|KIT-09: 21 criterios pequenos rastreaveis RSTV;
     fixture/ausente/malformado nunca OK; 21 controles reprovam; handler != clique;
     ativo nao prova obstrucao; dado velho reprova                        exit 0

python tools/automacao/cenarios/test_kit09.py --contra-prova
  -> CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os 21 controles passarem
     (o REPROVADO real vem da regra)                                      exit 0

python scratch/kit/k09/prova-red-kit09.py
  -> PROVA-RED|sha256 original de kit09.py = a4f75876...
     [verde] exit=0 · [red] exit=1 (controle 'placeholder-no-render' deixa de reprovar:
     "esperado 'REPROVADO', obtido 'OK'") · restauracao byte a byte sha256 identico
     [verde-de-novo] exit=0 · PROVA-RED|PASSOU                        exit 0

CLI (exit code por estado, saidas em scratch/kit/k09/cli-*.json):
  kit09-verdade.entrada.json -> exit 0 (21 OK)
  kit09-velho.entrada.json   -> exit 1 (DADO VELHO reprovado)
  kit09-la.entrada.json      -> exit 2 (sem OK e sem defeito)

travas do repo depois dos arquivos novos:
  check_segredos / check_padroes_segredo / check_dupes / audita_docs    exit 0
```

## 3. ACHADO DE FRONTEIRA (nao consertado aqui — nao e desta frente)

`python tools/automacao/cenarios/test_rstv.py` (suite do **CIC-3**, arquivo que esta
frente NAO editou) esta **VERMELHA** no estado atual do disco:

```
RESULTADO|REPROVOU|cic3-rstv|hash_fonte == dll_sha tem de amarrar a build
(integracao CIC-5/R-1): esperado 'OK', obtido 'NAO_EXERCITADO'          exit 1
```

**Causa medida (nao suposta):** o filtro de ALVO do KIT-R0F (`_selecionar_alvos` em
`rstv.py`) exclui a observacao da fixture real do probe porque ela declara
`owners=com.gumatos.bettertooltips,com.gumatos.betterfont` — modulo que NAO e o alvo do
RSTV:

```
motivo: sem observacao/leitura para esta capacidade (AUSENTE nao e OK)
        | 1 observacao(oes) NAO-alvo excluida(s): 1 x sem owner do mod sob teste
```

Isto e quebra de fronteira entre frentes (`rstv.py` e o `probe-saida-exemplo` mudaram
depois do CIC-3), **nao** regressao do KIT-09: esta frente so ADICIONA arquivo novo e
nao escreve em `rstv.py`/`coletor.py`/`fixtures/**` (hashes no fechamento). Registrar, e
nao editar o artefato de terceiro para deixar a auditoria verde (regra do cartao).

**Passo seguinte concreto (para o controlador rotear, nao para esta frente):** alinhar a
suite `test_rstv.py` (ou a fixture `probe-saida-exemplo.entrada.json`) ao filtro de alvo
do KIT-R0F — ou declarar o `owners` do RSTV na fixture e reexecutar; a suite do KIT-09
usa a mesma costura e continua verde porque alimenta observacao sem `owners` alheio.

## 4. Limites

- Runtime/pixels/desempenho: **NAO_EXERCITADO** (exige rodada autorizada; KIT-G1/G2 pendentes).
- Campos novos (`janela.fechado_x/fechado_esc`, `handler_invocado`, `clique_fisico`,
  `obstrucao`) sao **contrato declarado**: o probe de hoje nao os emite, e a ausencia sai
  `NAO_EXERCITADO` + `lacuna_probe` + `tipo_pendencia='tecnica'`.
- Fixture testa o AVALIADOR: nunca fecha OK; defeito plantado em fixture continua REPROVADO.
- Aprovar tecnicamente nao e aceite humano nem DoD/publicacao.
