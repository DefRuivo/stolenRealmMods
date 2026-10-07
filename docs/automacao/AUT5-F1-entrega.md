# AUT5-F1 — emitir os campos que faltavam para os cenarios RSTV (`t_dd95f8d9`)

> **REENTREGA apos revisao:** R1 (alvo do snapshot) e R2 (marcador faltante)
> foram corrigidos. Evidencias atuais, hashes e limites em
> `docs/automacao/AUT5-F1-reentrega.md`. Os resultados/hashes abaixo sao historicos
> da primeira entrega e nao aprovam a reentrega nem runtime.

> Rodada **OFFLINE**. Nenhum jogo aberto/encerrado, nenhum save carregado, nenhum probe
> instalado, nenhum deploy no perfil, nenhum commit/push/publicacao. A **EMISSAO** e provada
> por **build + testes offline** (contrato estatico + formato sintetico rotulado); a
> **LEITURA em jogo** e a rodada autorizada do dono e **NAO** foi feita aqui.

Origem: achado da AUT-5 (`t_76a41ea7`) — 5 criterios ficaram como `falha_automatica`
(fila de agente) porque dependiam de campo que **ninguem emitia**. Este card e essa fila.

## 1. Item por item (o que faltava emitir e como ficou)

| # | item do card | onde | como ficou | formato emitido |
|---|---|---|---|---|
| 1 | `snapshot_antes`/`snapshot_depois` (skills + pontos) | `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` (`Leitura`) + `runtime/coletor.py` (`CAMPOS_RSTV`) | `SnapshotDoPersonagem()` le `Character.SkillsFromPoints` (`SkillInfo.SkillName`) e `Character.UnspentSkillPoints` por reflexao; o "antes" e tirado no inicio da leitura e o "depois" e FECHADO no fim (`AtualizarGuardasDepois`) | `{"personagem": str|null, "skills": [str]|null, "pontos": numero|null, "fonte_skills"/"fonte_pontos": str}` |
| 2 | `tooltip_pai_antes/depois`, `tooltip_indice_antes/depois`, `janelas_duplicadas` | idem (`Leitura` + `LembrarTooltip`/`AtualizarGuardasDepois`/`JanelasDuplicadas`) | pai = caminho do **transform PAI** do `GUIManager.instance.tooltip`; indice = `GetSiblingIndex()`; antes = **primeiro** estado observado (UI acabou de existir, antes de qualquer clique); janelas = quantas janelas do RSTV **ativas alem da primeira** | `pai`: `str` · `indice`: `int` · `janelas_duplicadas`: `int >= 0` |
| 3 | `linhas_dependencia` **POR TIER** | `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs` (linha do `RSTV-24b`, **so a linha de log**) + `aut5/log_rstv.py` + `aut5/aut5.py` | o `RSTV-24b` passou a publicar `; por tier: T1:n, ...` (contagem de linhas ATIVAS por tier) ao lado do `RSTV-25` (Dependency real por tier); o leitor faz o **confronto TIER A TIER** | `RSTV-24b: N linha(s) ... ; cor da 1a = <cor>; por tier: T1:0, T2:1, ...` |
| 4 | `geometria.tela` (viewport) por observacao | `AUT4ProbePlugin.cs` (`Geometria`) | **JA era emitida** (`"tela", Screen.width + "x" + Screen.height`) e **ja era consumida** (`cenarios/rstv.py::_bbox`); conferido no fonte e agora coberto por teste — **nao** houve emissao nova | `geometria: {"caixa_na_tela_px": {...}, "tela": "1920x1080", ...}` |
| 5 | `personagem_esperado` | — | **NAO TOCADO**: e do PLANO/perfil de teste (`aut5/cenarios-rstv.json` → `perfil_de_teste.personagem_esperado: null`), item do dono. Continua INDETERMINADO de proposito | — |

**Armadilha do card (campo novo nao pode nascer `null` virando OK):** respeitada em duas
camadas — (a) no coletor os campos entram em `CAMPOS_EXTRAS`/`CAMPOS_RSTV` (atravessam a
costura e **nao** viram lacuna generica de todo objeto TMP), e (b) quem julga ausencia e o
avaliador, **por capacidade**: `None`/AUSENTE nao monta o par antes/depois e sai
NAO_EXERCITADO/INDETERMINADO — nunca OK. Sem `sessao`/`hash_fonte` valendo, tambem nao sai OK.

## 2. Mudanca de PRODUTO (so a linha de log) e a identidade dos bytes

* Unica alteracao de produto: a string do `RSTV-24b` ganhou o sufixo `por tier`, com um
  `int[6]` de contagem por tier dentro do laco que JA contava as linhas ativas. **Nenhum
  comportamento mudou** (nada e escrito no personagem; nenhum caminho novo).
* A DLL do repo (`RoguelikeSkillTreeVisualizer/bin/Release/netstandard2.1`, `454587a0...`)
  **NAO foi reconstruida**: a identidade fonte/DLL que o AUT-5 usa ficou **intacta** (a DLL
  do perfil do dono continua `==` a do repo). O fonte agora esta **a frente** da DLL.
* Consequencia declarada: o `LogOutput.log` do dono e de build **anterior** ao AUT5-F1 — o
  `RSTV-24b` dele **nao** tem o `por tier` → o confronto por tier segue INDETERMINADO ate
  **rebuild + deploy + rodada**. Existe teste dedicado para esse caso (`log-build-anterior`).
* Build do mod feito com `-o <pasta temporaria>` so para provar compilacao, sem tocar em
  `bin/` nem no perfil.

## 3. Comandos exercitados (saida real)

```
dotnet build -c Release AUT4Probe.csproj -p:DeployToBepInEx=false   -> 0 Erro(s)
    DLL nova do probe: 1769198cb07a7242773ec59a4ddcc0fa0b04b6e8d983223b3b22a0091c952c1f
dotnet build -c Release RoguelikeSkillTreeVisualizer.csproj -o <scratch> -> 0 Erro(s)
    (bin/Release do repo INTACTO: 454587a031a3e891...)

python tools/automacao/aut5/test_aut5.py
  -> RESULTADO|PASSOU|aut5-rstv|9 casos (positivo, log-real, ausente, 9 defeitos
     plantados, 2 fontes mutadas, rotulos, log de build anterior, emissao dos campos, isca)
python tools/automacao/aut5/test_aut5.py --contra-prova   -> CONTRA-PROVA|PASSOU      exit 0

python tools/automacao/aut5/aut5.py --texto                (log REAL do dono)
  -> resumo {"OK": 6, "NAO_EXERCITADO": 11}
     decisao: pronto_para_decisao=True | falhas_automaticas=0 | pendencias_humanas=2     exit 2
python tools/automacao/aut5/aut5.py --log fixtures/log-completo.log --texto
  -> resumo {"OK": 7, "INDETERMINADO": 2, "NAO_EXERCITADO": 8}                            exit 2

python tools/automacao/runtime/roda_testes_runtime.py      -> VERDE 8/8   exit 0
python tools/automacao/cenarios/test_rstv.py               -> PASSOU       exit 0
python tools/testes/roda_testes.py                         -> VERDE 86/86  exit 0
check_segredos / check_padroes_segredo / check_dupes / audita_docs -> exit 0
```

## 4. Controles negativos (o que a suite sabe reprovar)

Os 9 defeitos plantados anteriores continuam, mais os **novos** deste card:

| # | defeito plantado | criterio que reprova |
|---|---|---|
| 10 | `RSTV-24b` com `T4:1` para Dependency=2 (**linha do tier faltando** = conector ausente por tier) | `AUT5-RSTV-25b-conectores-log` |
| 11 | `RSTV-24b` com `T1:1` para Dependency=0 (**linha sobrando** = aresta inventada por tier) | `AUT5-RSTV-25b-conectores-log` |
| 12 | log de build **anterior** (sem `por tier`) | `AUT5-RSTV-25b-conectores-log` -> **INDETERMINADO** com lacuna declarada (nunca OK) |
| 13 | campo **AUSENTE** na observacao sintetica | `RSTV-6-readonly-skills-pontos`, `RSTV-21-tooltip-restauracao`, `RSTV-geometria-clipping` -> nunca OK |
| 14 | **gasto** de pontos no snapshot / tooltip nao restaurado + duplicado / bbox passando da tela | idem -> **REPROVADO** |

E a regra de ouro continua exercitada: `AUT5-RSTV-25b-conectores-log` so sai **OK** com o
confronto **total E por tier** consistente; `T5` sem Dependency segue ausencia LEGITIMA.

## 5. Suite MOSTRADA reprovando (regra do projeto)

Quatro mutacoes, cada uma verificada com `RESULTADO|REPROVOU` — cada uma restaurada
**byte a byte** (sha reconferido):

| mutacao | resultado |
|---|---|
| `"janelas_duplicadas", _janelasDuplicadas,` removido do `Leitura` | RED exit 1 — "probe nao emite o campo 'janelas_duplicadas' POR OBSERVACAO" |
| `d["tooltip_indice_depois"] = _tooltipIndiceDepois;` removido do fim da leitura | RED exit 1 — "probe nao fecha o 'depois' (d[\"tooltip_indice_depois\"])" |
| `"tela", Screen.width + "x" + Screen.height` removido da `Geometria` | RED exit 1 — "probe nao emite geometria.tela como dimensao do viewport" |
| `"tooltip_indice_antes", "tooltip_indice_depois",` removido do `coletor.CAMPOS_RSTV` | RED exit 1 — "coletor descarta o campo 'tooltip_indice_antes'" |

Restaurados: probe `a2bd3d49ceab1ddf...`, coletor `0518634edaa70930...` → suite volta a
`PASSOU` exit 0.

## 6. Efeito na decisao (CIC-2) — o que muda e o que NAO muda

| | antes (relatorio AUT-5) | agora |
|---|---|---|
| fila de agente (lacuna tecnica de probe/campo) | 5 | **0** |
| roteiro humano | 2 (1 autorizacao agregada + 1 visual) | 2 (autorizacao **com instrucao por criterio** + visual) |
| `pronto_para_decisao` (log real) | False | **True** |

As 5 lacunas tecnicas viraram **AUTORIZACAO** no roteiro humano (o plano
`aut5/cenarios-rstv.json` foi atualizado: `pendencia_primaria` de `tecnica` -> `autorizacao`,
com `campos_necessarios` e `instrucoes_humanas` concretas), porque **o que falta agora nao e
instrumento: e a rodada runtime**.

> **`pronto_para_decisao=True` NAO e aprovacao e NAO fecha o DoD.** Significa apenas
> "automacao sem falha: resta a decisao humana". Nenhum criterio runtime foi aprovado, nao ha
> PNG, nao ha aceite visual e nao ha publicacao — os estados seguem separados.

## 7. Limites (o que NAO foi provado)

* **Runtime NAO EXERCITADO**: os campos novos nao foram lidos em sessao viva; nenhum PNG;
  nenhum criterio runtime aprovado; nenhuma recusa de guarda exercitada.
* O probe C# novo **nao foi instalado nem executado** — a prova e build (0 erros), contrato
  estatico do fonte e uma observacao **sintetica** (rotulada) que prova o FORMATO contra o
  avaliador; a leitura real e a rodada autorizada.
* O `RSTV-24b` com `por tier` so aparece depois de **rebuild+deploy** do mod (o log atual e
  de build anterior).
* Itens fora do escopo e intocados: `personagem_esperado` (item 5, do dono), os bloqueadores
  S-1/R-2..R-5 do coletor (CIC-5, `t_431dba37`), o resto da rodada runtime.

### Achado secundario (nao bloqueia; nao era meu escopo)

`docs/automacao/AUT-4-estado.json` e um **snapshot congelado da rodada do AUT-4**
(`t_b8b9822e`): o `artefatos.probe_dll_sha256` dele (`e8ee229b...`) ja estava **stale** antes
desta rodada (a CIC-5 ja registrou o mesmo achado com o valor `3c32f026...`; agora a DLL do
probe e `1769198c...`) e os contadores de teste (6) tambem sao daquele momento (a suite
runtime esta em **8**). Nao reescrevi o arquivo — ele e o retrato de uma rodada de outra
frente; a atualizacao segue com o pai/supervisor, como a `CIC-5-entrega.md` ja pedia.

## 8. Arquivos e hashes (sha256)

```
a2bd3d49ceab1ddfe31bdbdb8fa9d56b86003f8b529d2da22ad0042700718254  tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs
1769198cb07a7242773ec59a4ddcc0fa0b04b6e8d983223b3b22a0091c952c1f  tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll
0518634edaa70930a8f8173151d84aee8c20a5523fcffd9ad5842b6d5ff1faca  tools/automacao/runtime/coletor.py
dddd8672b1594036c8943118bde820d653c923138c529ab449ea6664a49baf66  tools/automacao/aut5/aut5.py
fcf22c95406304c974b474e7d9fcdbbd7acce7634e16f29e791994677e147c22  tools/automacao/aut5/log_rstv.py
aad84ee41f7d5742f6d096d68aedd0a8bc77b05b89defb37b7e48ebeab2c7cb2  tools/automacao/aut5/test_aut5.py
7b56e4fc79d8130a3c9f48e931b45ec1f52a8b28da5bf3e357a863690dbe5063  tools/automacao/aut5/cenarios-rstv.json
bcbda70fb7082442f87a3643ebcba05a65a6113b3a3bb4ef6f4be4c80f67ec9d  tools/automacao/aut5/fixtures/log-completo.log
09debb76cec83c6341a177268add820dbca5bbeb5bf44c101c55619b6f179b9f  RoguelikeSkillTreeVisualizer/SkillTreesTab.cs
# INTACTOS (identidade preservada nesta rodada):
454587a031a3e89104ec8535cf4c6328e2a527238138a136adcc773c5617a948  RoguelikeSkillTreeVisualizer/bin/Release/netstandard2.1/RoguelikeSkillTreeVisualizer.dll
```

Rodada offline `2026-10-05` · branch `ci-validate-test`.

> **Correcao de citacao** (`t_1e7a19aa`, 2026-10-05): a tabela do item 1 citava o fonte do probe
> **sem o prefixo `tools/automacao/`** — caminho que nao existe no repositorio (pendencia acusada
> pelo `tools/checa_citacoes.py`). A citacao passou a
> `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs`. Nada mais mudou: a rodada continua a
> descrita acima, offline, com os mesmos hashes.
