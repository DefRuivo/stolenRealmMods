# CIC-3 correcao — fechamento de B1-B5 do avaliador RSTV (`t_7fdce47f`)

> Correcao funcional da entrega CIC-3 apos o aceite Red da revisao independente (`CIC-3R-revisao.md`,
> contra-provas em `scratch/cic3r/ataca_rstv*.py`). Rodada **offline**: nenhum jogo aberto, probe
> instalado, build/deploy/commit/publicacao, save ou escrita de produto. So leitura de runtime/produto.
> Escopo de escrita: `tools/automacao/cenarios/rstv.py`, `test_rstv.py`, `rstv*.json` novos e este doc.
> **Nao toquei** em `ciclo/`, `decisao.py`, `tooltips_shrines.py`/`shrines-*.json` (outras frentes).

## B1-B5 — fechado

| # | defeito (CIC-3R) | correcao | repro que prova |
|---|---|---|---|
| **B1** | ausencia/incompletude fechava OK porque `contrib.append`/`dados=True` vinha ANTES de validar o campo, e `_fecha` ignorava `motivos` | `_fecha` agora aceita `motivos` e **nunca fecha OK** com motivo (AUSENTE/incompleto -> NAO_EXERCITADO; confronto impossivel -> INDETERMINADO); cada capacidade so marca `dados` apos validar completude | `ataca1` ACHADOS **0** |
| **B2** | `skills` string/dict era aceito (e escondia mudanca `AB`->`BA`) | validacao de TIPO: `skills` tem de ser **lista de strings** (`_lista_de_str`); `pontos` numerico (`_numerico`); snapshot sem `skills`/`pontos` vira lacuna | `ataca2` `skills string/dict` -> NAO_EXERCITADO |
| **B3** | excecao mapeava id por `split("-")[0]` (= `rstv`) e o id canonico SUMIA | `avaliar` usa `_CAPS = ((id_canonico, funcao), ...)`; a excecao preserva o **id canonico** da capacidade | `ataca2` `pontos 'abc' -> ids: so canonico` |
| **B4** | so `hash_fonte` era conferido; `hash_dll`/`config_sha` divergentes eram IGNORADOS; o criterio nao expunha hash nenhum | `_checagem_hashes` confronta **fonte+dll+config** quando declarados; divergente -> INDETERMINADO, nao-confirmado -> NAO_EXERCITADO; o criterio **propaga** `fonte_sha`/`dll_sha`/`config_sha` + `prova_runtime` + `sessao` | `ataca2` `hashes declarados=[fonte_sha,dll_sha]`; divergencia -> INDETERMINADO |
| **B5** | o falso OK propagava a `decisao.py` como `OK_VINCULANTE` | com B1-B4 o falso OK deixou de existir; o criterio agora carrega os campos que a `decisao.py` (CIC-2) consome | `ataca2` personagem ausente -> **FALHA_AUTOMATICA** (nao mais OK_VINCULANTE) |

## Contrato positivo runtime (conforme CICLO-VALIDACAO-escopo.md)

O criterio OK carrega `prova_runtime=true`, `sessao`, `fonte_sha`, `dll_sha`, `config_sha` (quando a
config e relevante) — confrontados com a **identidade da coleta**, nao com rotulo. Ausencia/falha de
cadeia => NAO_EXERCITADO/INDETERMINADO, nunca OK. **Nao se inventou campo de emissao nem prova
criptografica nova**: le-se o formato do coletor CIC-5 (bloco `campos` + `sessao`/`hash_fonte` do topo
injetado por `anexar_contexto`); a **identidade do artefato esperado** e o criterio suficiente contra
dado lido ausente/mismatch.

## Dados vivos ausentes = lacuna TECNICA (nao e do dono por default)

Cada capacidade NAO_EXERCITADO/INDETERMINADO por campo ausente carrega `lacuna_probe` (o que o probe
nao emite) e `tipo_pendencia="tecnica"` com `autorizacao_necessaria=false`. A `decisao.py` (CIC-2,
atualizada) le exatamente essas chaves e roteia a lacuna para **FALHA_AUTOMATICA** (fila de agente),
nunca ao dono. Autorizacao so com `autorizacao_necessaria=true`/`tipo_pendencia=autorizacao`.

## Caminho positivo (artefato SINTETICO, nao prova runtime)

`rstv-positivo.entrada.json` e **claramente sintetico** (`sintetico:true` + aviso + hashes sinteticos).
O teste injeta `procedencia=runtime` + `sessao` e usa os hashes declarados como identidade: fecha
**7/7 OK** (exercita o avaliador). Fixture continua fixture: nenhuma fixture vira OK com procedencia
`fixture`; e a CLI nunca produz OK a partir de arquivo (so leitura de jogo pode ter `runtime`).

## Evidencia (execucao real, offline)

```
python tools/automacao/cenarios/test_rstv.py
  -> RESULTADO|PASSOU|cic3-rstv|...                                   exit 0
python tools/automacao/cenarios/test_rstv.py --contra-prova
  -> CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os 10 controles passarem   exit 0
python scratch/cic3r/ataca_rstv.py    (contra-prova da revisao)
  -> 8 casos deixam de OK; ACHADOS: 0                                  exit 0
python scratch/cic3r/ataca_rstv2.py   (contra-prova da revisao)
  -> malformado/cadeia/hashes OK; personagem ausente = FALHA_AUTOMATICA; 1 achado residual (ver abaixo)
CLI: fixture limpa -> {NAO_EXERCITADO: 7}, prova_runtime=false         exit 2
CLI: controle gasto de skills -> {NAO_EXERCITADO: 6, REPROVADO: 1}      exit 1
     "DEFEITO: skills MUDARAM: antes=['A', 'B'], depois=['A']"
```

Suite pura do projeto intacta: `python tools/testes/roda_testes.py --puros` -> **85/85, VERDE, exit 0**.

## Secundario remanescente (nao bloqueia; herdado da revisao)

`ataca_rstv2.py` item 4(b) acusa "todo criterio sem dado vira FALHA_AUTOMATICA" quando `avaliar([])`
roda com identidade. Isso e a checagem-proxy da revisao (dispara em FALHA independentemente do
motivo). Com a correcao o rotulo deixou de mentir: a `decisao.py` agora classifica como
*"lacuna tecnica de runtime (probe/campo/coleta/preparacao): automatizavel, volta ao ciclo — NAO e
tarefa do dono"*. Como a lacuna tecnica **deve** ir a automacao (correcao do objetivo central), nao ha
como zerar esse proxy sem mandar trabalho indevido ao humano — preservado como esta, com o motivo
correto.

## Limites

- **Runtime NAO_EXERCITADO**: nenhuma leitura de jogo. `@x@` no cru, `*0` real do RSTV-26 e a emissao
  real dos campos RSTV pelo probe continuam so na rodada runtime autorizada (frente unica).
- Nao editei produto/probe/`ciclo/`/`decisao.py`/`shrines`; sem build/jogo/install/save/commit/push.
