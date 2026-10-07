# CIC-3 — cenarios automaticos RSTV para o ciclo (`t_7fdce47f`)

> Reusa AUT-5 (`t_76a41ea7`) e o formato REAL do coletor AUT-4/CIC-5. **Runtime
> NAO_EXERCITADO**: nenhum jogo aberto, nenhum save tocado, nenhum probe
> instalado, nenhum build/deploy/commit/push. Toda leitura de campo aqui e
> **fixture/sintetica rotulada** — fixture testa o avaliador, nao prova runtime.
>
> Rodada de **retomada**: fecha B1-B5 ja registrados no cartao (re-executados com
> as contra-provas do revisor) e **costura a coleta REAL do CIC-5**, corrigindo o
> desalinhamento de hash R-1 do `CIC-5R-revisao.md`.

## Arquivos (so nesta frente)

| arquivo | papel |
|---|---|
| `tools/automacao/cenarios/rstv.py` | adaptador/cenarios RSTV: `avaliar(observacoes, identidade)` + CLI real |
| `tools/automacao/cenarios/test_rstv.py` | teste executavel offline (exit 0/1/2) + `--contra-prova` + integracao CIC-5 |
| `tools/automacao/cenarios/rstv-observacoes.entrada.json` | fixture limpa (campos planos + bloco `campos` normalizado) |
| `tools/automacao/cenarios/rstv-controles.entrada.json` | 10 controles negativos (defeito plantado -> tem de reprovar) |
| `tools/automacao/cenarios/rstv-lacunas.entrada.json` | 12 casos de ausencia/incompletude/malformado -> nunca OK |
| `tools/automacao/cenarios/rstv-ausente.entrada.json` | caso sem leitura -> tudo NAO_EXERCITADO |
| `tools/automacao/cenarios/rstv-identidade.json` | identidade-exemplo (`fonte_sha`/`dll_sha` sinteticos) |
| `tools/automacao/cenarios/rstv-positivo.entrada.json` | artefato SINTETICO que exercita o caminho OK |

Nao editado: produto, probe, `runtime/**` (CIC-5), `tooltips_shrines.py`/`shrines-*.json`
(CIC-4), `ciclo/`/`decisao.py` (CIC-1/2), KANBAN/board. Nenhum arquivo fora de
`tools/automacao/cenarios/` e deste doc.

## Contrato entregue

`avaliar(observacoes, identidade) -> [criterio]`, com
`id, mod, estado, classe, procedencia, esperado, observado, evidencia, motivo, tarefa_origem`.
Campos extras: `prova_runtime`, `sessao`, `fonte_sha`, `dll_sha`, `config_sha`,
`lacuna_probe`, `tipo_pendencia`, `autorizacao_necessaria`.

- **Adaptador le as DUAS formas do AUT-4/CIC-5**: leitura CRUA do probe
  (`objeto`, `texto_bruto`, `texto_renderizado`, `personagem`, `geometria`, `owners`)
  e leitura NORMALIZADA (`campos: {campo: {estado, valor, alvo}}` + `sessao`/`hash_fonte`
  do topo). Nao impoe formato novo ao coletor.
- **Fixture nunca vira OK**: sem `fonte_sha` E `dll_sha` nao existe OK; procedencia
  `fixture` sem defeito sai NAO_EXERCITADO. Defeito plantado continua REPROVADO.
- **AUSENTE/INDETERMINADO/NAO_EXERCITADO nunca sao OK**; incompleto/malformado idem.
- Sempre devolve o **conjunto canonico EXATO das 7 capacidades** (com
  NAO_EXERCITADO quando falta dado): `RSTV-6-readonly-personagem`,
  `RSTV-6-readonly-skills-pontos`, `RSTV-21-janela-ciclo`,
  `RSTV-21-tooltip-restauracao`, `RSTV-26-placeholders`, `RSTV-25b-dependencia`,
  `RSTV-geometria-clipping`.

## B1-B5 (revisao CIC-3R) — fechados e re-executados

| # | defeito (CIC-3R) | correcao | contra-prova |
|---|---|---|---|
| **B1** | ausencia/incompletude fechava OK (`contrib/dados` antes de validar; `_fecha` ignorava `motivos`) | `_fecha` honra `motivos` e **nunca** fecha OK com motivo; cada capacidade so marca `dados` depois de validar completude | `ataca_rstv.py` -> **ACHADOS: 0** (exit 0) |
| **B2** | `skills` string/dict aceitos (escondia `AB`->`BA`) | `_lista_de_str` exige lista de strings; `pontos` exige numerico; snapshot sem chaves = lacuna | `ataca_rstv2.py` 1: `NAO_EXERCITADO` (sem esconder mudanca) |
| **B3** | excecao mapeava id por `split("-")[0]` (`rstv`) e o id canonico sumia | `_CAPS = ((id_canonico, funcao), ...)`; a excecao preserva o id canonico | `ataca_rstv2.py` 1: `pontos 'abc' -> ids: so canonico` |
| **B4** | so `hash_fonte` era conferido; `hash_dll`/`config_sha` ignorados; criterio nao expunha hash | `_checagem_hashes` confronta os hashes declarados; o criterio propaga `fonte_sha`/`dll_sha`/`config_sha`/`prova_runtime`/`sessao` | `ataca_rstv2.py` 3: divergente -> INDETERMINADO; nao-confirmado -> NAO_EXERCITADO; `hashes declarados=['fonte_sha','dll_sha']` |
| **B5** | falso OK propagava a `decisao.py` como `OK_VINCULANTE` | com B1-B4 o falso OK deixou de existir; o criterio carrega os campos que a `decisao.py` consome | `ataca_rstv2.py` 4c: personagem ausente -> `FALHA_AUTOMATICA` (nao mais OK_VINCULANTE) |

## Correcao de integracao — R-1 do CIC-5R (hash do coletor)

**Achado (CIC-5R R-1):** o coletor CIC-5 grava `hash_fonte` = **sha256 da DLL** do
probe (`coletor.derivar_config`/`provar_atualidade`; a propria CIC-5-entrega diz
"a identidade do probe (`hash_fonte`) casa com `dll_sha`"). O adaptador do CIC-3
comparava esse valor com `fonte_sha` (sha da FONTE) -> **toda** observacao runtime
legitima era marcada divergente (falso INDETERMINADO, devolvida para sempre como
falha automatica).

**Conserto (so `rstv.py`):** `hash_fonte` e `hash_dll` passam a casar com o
`dll_sha` da identidade; `fonte_sha`/`dll_sha` explicitos tambem sao conferidos.
`_desempacotar` (CLI) tambem mapeia `hash_fonte`->`dll_sha`.

```python
_ALIAS_HASH = (("hash_fonte", "dll_sha"), ("hash_dll", "dll_sha"))
```

Isso **costura o formato REAL do CIC-5** sem fabricar runtime nem enfraquecer a
trava: um `hash_fonte` que case apenas com a fonte (convencao antiga) **nunca**
fecha OK.

## Costura com a coleta REAL do CIC-5 (teste `_integracao_cic5`)

O teste importa o `coletor.py` REAL (leitura, sem editar) e prova, com output
literal:

1. a fixture real do probe (`probe-saida-exemplo.entrada.json`) e auto-detectada
   como **FIXTURE** (exit 2) — o proprio coletor nao deixa fixture virar runtime;
2. a forma **NORMALIZADA** que o coletor produz (`campos` + `sessao`/`hash_fonte`
   do topo) e lida por `avaliar`: bloco `campos`, fallback `NAO_APLICAVEL` ->
   `texto_bruto`, e **nenhum OK** com procedencia fixture;
3. uma observacao no formato REAL com `hash_fonte == dll_sha` fecha **OK** (R-1),
   e a convencao antiga (`hash_fonte == fonte_sha`) **nao** fecha OK.

## Comandos exercitados (saida real, exit 0/1/2 distintos)

```
python tools/automacao/cenarios/test_rstv.py
  -> RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao
     viram OK, controles reprovam, runtime identifica                        exit 0

python tools/automacao/cenarios/test_rstv.py --contra-prova
  -> CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os 10 controles passarem
     (o REPROVADO real vem da regra)                                          exit 0

# PROVA DE FOGO do proprio teste (RED capturado antes do conserto de R-1):
# com hash_fonte=aa..a (fonte) no artefato positivo e rstv ainda mapeando
# hash_fonte->fonte_sha -> o caminho OK zerava:
python tools/automacao/cenarios/test_rstv.py
  -> RESULTADO|REPROVOU|cic3-rstv|artefato positivo (sintetico) deveria fechar
     TODAS OK; OK=[]: esperado 7, obtido 0                                   exit 1

# RED do teste de INTEGRACAO (monkeypatch do mapeamento antigo):
#   GREEN: _integracao_cic5 PASSOU com o contrato real
#   RED:   _integracao_cic5 REPROVOU com o mapeamento antigo ->
#          Falhou: hash_fonte == dll_sha tem de amarrar a build ...: esperado
#          'OK', obtido 'INDETERMINADO'

# CLI real (exit code por estado):
python tools/automacao/cenarios/rstv.py --observacoes rstv-observacoes.entrada.json \
  --identidade rstv-identidade.json
  -> contagem {'NAO_EXERCITADO': 7}; runtime_exercitado False                  exit 2
# controle com gasto de skills:
  -> contagem {'NAO_EXERCITADO': 6, 'REPROVADO': 1}; reprovado True            exit 1
     "DEFEITO: skills MUDARAM: antes=['A', 'B'], depois=['A']"
```

O caminho OK foi demonstrado com um artefato **SINTETICO persistido**
(`rstv-positivo.entrada.json`, rotulado `sintetico:true`; o teste injeta
procedencia runtime + sessao e usa os hashes declarados como identidade):
**7/7 capacidades OK**. Sem identidade, nenhum OK.

Contra-prova da RETOMADA (sandbox externo ao repo,
`%LOCALAPPDATA%/hermes/cache/scratch/cic3b/prova_rstv.py`): **30 checks, 0 achados,
exit 0** — repete B1-B5 sob o contrato real, cobre placeholders
(`*0`->REPROVADO, `*0.5`/`*2`/`[2]` cru->OK, `@Might@` renderizado->REPROVADO),
a cadeia de hash, a integracao com o coletor real e os 3 exit codes.

> Nota de honestidade: a contra-prova antiga do revisor (`scratch/cic3r/ataca_rstv2.py`)
> reporta 3 itens a mais agora **porque o script assume `hash_fonte == fonte_sha`**
> (premissa antiga). Sob o contrato real do CIC-5 os mesmos casos (`*0.5`/`*2`/`[2]`
> cru) sao OK — provado pelo `prova_rstv.py`. Nao e regressao do avaliador: e o
> script do revisor com a premissa desatualizada. O item 4(b) (lacuna tecnica ->
> FALHA_AUTOMATICA) segue o residual conhecido, por desenho.

## Controles negativos (os 10 reprovam)

gasto de skills · gasto de pontos · personagem errado · placeholder `*0` ·
placeholder `[indice]` · tooltip nao restaurado · janela duplicada · janela que
nao fecha · geometria com clipping · aresta de dependencia inventada. A isca meta
(`--contra-prova`) mostra que um `_fecha` "sempre OK" **nao** pega os controles —
logo o REPROVADO vem da regra, nao de passe livre.

## Lacunas declaradas (NAO sao OK)

O `AUT4Probe`/coletor de hoje emite UMA leitura por `TMP_Text` ativo e o contexto
`personagem = {gui_state, tem_personagem_selecionado, personagem}`. Ele **nao**
emite, por observacao: `skills_antes/depois`/`pontos_antes/depois`; ciclo
`janela {aberta, fechada}`; `tooltip_pai/indice_antes/depois` + `janelas_duplicadas`;
`linhas_dependencia`/`dependency_por_tier`; `tela` junto da bbox;
`personagem_esperado`. Cada lacuna sai NAO_EXERCITADO/INDETERMINADO com
`lacuna_probe` + `tipo_pendencia='tecnica'` (autorizacao_necessaria=False) — vai a
**agentes**, nunca ao dono por default. Ate a rodada runtime autorizada, o maximo
que a coleta real fecha OK e `RSTV-26-placeholders` (com texto renderizado).

## Blocker de contrato compartilhado (reportado, NAO editado)

O campo `hash_fonte` do coletor CIC-5 carrega semantica de **DLL**, mas o
adaptador do **CIC-4** (`tools/automacao/cenarios/tooltips_shrines.py`, L232/L67;
e `test_tooltips_shrines.py`) ainda compara `hash_fonte` com `fonte_sha` — o
**mesmo R-1** do CIC-5R permanece aberto do lado do CIC-4. Nao editei arquivo de
outra frente (escopo). **Acao pedida ao pai:** alinhar o CIC-4 ao contrato real
(`hash_fonte`->`dll_sha`) ou decidir o contrato no coletor. A `decisao.py` (CIC-2)
le `fonte_sha` (ou `hash_fonte`) e exige `dll_sha` no criterio — o criterio do
CIC-3 propaga os dois, entao **nao precisa mudar**.

## Limites desta rodada

- **Runtime NAO_EXERCITADO**: nenhuma leitura de jogo. `@x@` no cru, `*0` real do
  RSTV-26, emissao real dos campos RSTV pelo probe e o rollback contra o perfil
  real continuam so na rodada runtime autorizada (frente unica).
- `RSTV-25b` continua **INDETERMINADO** (o log existe; o marcador `RSTV-25:` nao
  localizado; o probe nao emite as linhas por tier).
- **DoD humano e publicacao sao estados SEPARADOS**: automacao nao substitui a
  verificacao humana em jogo nem a publicacao na Thunderstore.

## Arquivos e hashes (sha256)

```
524f719757977436b843bdceb8337b10db4003cba9da64ff3fea788ef327d320  tools/automacao/cenarios/rstv.py
2dd71104c8b3a81d9ded38ea2e44baa33a30fb4f0df0bfe5c9f64b85161a4969  tools/automacao/cenarios/test_rstv.py
c5d06592a67276359b5f64699dba8452c97b02084efcf02a3fe7e1ad64ab64e0  tools/automacao/cenarios/rstv-positivo.entrada.json
# inalterados (conferidos nesta rodada):
fe3fe9a974f507682235dc5ed64e1ff826cae57b0c1cd9bd2b8f86873d0f975a  rstv-observacoes.entrada.json
90606c3d73203b5cbb6f17fed9b172e9455a90ea50da9f32e2256273f75252fa  rstv-controles.entrada.json
acac25d49acc1e8565fe87555d2264256785cc9f5fef2a9fe76c0de6b66af889  rstv-lacunas.entrada.json
02ba40105f02d0f2f0acb9ec0c6b8b55f85d7b32e9b5019f1f8586506632a61e  rstv-ausente.entrada.json
5cec628c011e5bc5f249fc649401eed20ee65eccaf40aafa33389d7ef2792f86  rstv-identidade.json
2f502e0d4ca45374f7d6a06f751254eb684e962d722ebb260e6324cee8959e83  tools/automacao/runtime/coletor.py   (= CIC-5)
```

HEAD `f526fe9` (branch `ci-validate-test`) · rodada offline `2026-10-05`.
