# KIT-10 — entrega: cenários de tooltips, shrines, estilo e atributos

Cartão `t_bbad760d`. Pai de gate: `t_01f65801` (KIT-09F, aprovado). Revisão: `t_896796be` (KIT-10R).
Perfil `default`, instância nova, contexto pequeno. Rodada **OFFLINE**: nenhum jogo, save, perfil,
probe, build, install, deploy, commit ou publicação. **Nenhum mod nem gameplay foi alterado.**

Esta entrega é o pedido de revisão (`kanban_request_review`). Não há autoaprovação; o revisor deve
tentar refutar os 4 aspectos e os guardas por conta própria.

## Resultado executivo

O KIT-10 **completa os cenários** que faltavam sem duplicar infraestrutura: `kit10_cenarios.avaliar`
**reusa pela importação** o avaliador CIC-4 (`tooltips_shrines.py`) e o AUT-7
(`estilo_atributos.py`) — que por sua vez trazem BetterStats `SavedMap`/final, BetterFont e
BetterCombatText e o contrato do Debugger — e **acrescenta 4 aspectos** com o esperado independente
(O oráculo `regras_shrine`, as tabelas geradas, `regras_debugger`→`tools/census.py`, `regras_bct`) e
**um controle negativo por aspecto**.

| Execução real | Resultado |
| --- | --- |
| `python tools/automacao/kit10/test_kit10_cenarios.py` | `TOTAL\|rodaram=17 reprovaram=0 nao_rodaram=0` · **exit 0** |
| `python tools/automacao/kit10/test_kit10_cenarios.py --isca` | `ISCA\|OK\|defeito plantado detectado` · **exit 0** |
| `python scratch/kit/KIT-10-run/prova_red_kit10.py` | `PROVA-RED\|PASSOU\|5 mutacoes\|todas as guardas load-bearing` · **exit 0** |
| `python tools/automacao/kit10/kit10_cenarios.py --observacoes scratch/kit/KIT-10-run/fixture.json` | `OK=0 ... com prova runtime: 0` · **exit 2** (fixture não é verde) |
| `test_tooltips_shrines.py` (reuso) | **exit 0** |
| `test_estilo_atributos.py` (reuso) | **exit 0** |
| `check_segredos.py` / `check_padroes_segredo.py` / `check_dupes.py` / `audita_docs.py` | **exit 0** (4/4) |

## Aceite — veredito por critério (do corpo do cartão)

| Critério do cartão | Como foi cumprido | Prova |
| --- | --- | --- |
| Relacionar tooltip/contexto/dano e fonte/receptor corretos em shrines | aspecto A: ground effect lê o dano no eixo `Source` (bonus 0); a tooltip de BUFF lê o bonus do RECEPTOR (`Target`). Esperado do ORÁCULO | `A-ok-runtime` (OK/prova_runtime) + 2 controles negativos |
| Preservar comportamento **Worship** confirmado; **não remover o dobro** para tornar teste verde | aspecto B: gatilho (Dwarven/Decay/Flame) conta por INSTÂNCIA (DWA-2); atributo 1× (RV-46). O defeito "dobro removido" REPROVA | `B-ok-dobro-preservado`, `B-defeito-dobro-removido`, RED `B-dobro` |
| BetterStats base `SavedMap` / final | reuso do AUT-7 (`estilo_atributos.avaliar` → `AUT-7/BetterStats/*`), presente no conjunto | `reuso-cic4-aut7` (id `AUT-7/BetterStats/`) |
| BetterFont e BetterCombatText material/keywords/cores e superfícies **por evento**, não prefab de boot | reuso do AUT-7 (material/cores/keywords/superfícies) + aspecto C (leitura por EVENTO; `estagio=boot` REPROVA) | `C-ok-evento`, `C-defeito-boot`, `C-sem-evento-nao-ok`, RED `C-evento` |
| Debugger contrato sem truncar texto | reuso do AUT-7 (`RoguelikeDebugger/runtime-*`) + aspecto D (contrato do dump: `desc=` último, `\|` em valor e desc truncada REPROVAM) | `D-ok-sem-truncar`, `D-defeito-pipe-no-valor`, `D-defeito-truncado`, RED `D-dump` |
| Critérios independentes rastreáveis, várias superfícies e controles negativos | esperado de fonte independente (oráculo/tabelas/censo); reuso de DUAS camadas (CIC-4+AUT-7); 5 defeitos plantados + isca | `esperado-rastreavel-kit10`, `controle-negativo`, `isca-teste-deve-reprovar` |
| Completar campos apenas necessários por caso; **runtime ausente não recebe OK** | cada aspecto lê só os campos do seu caso; o fechamento (AUT-7 `_fecha`/`_vinculo_obs`) rebaixa a `NAO_EXERCITADO` sem cadeia | `fixture-nao-prova-runtime` (exit 2, zero OK) |
| Não modificar mods/gameplay nesta tarefa | só 3 arquivos novos de ferramenta/teste + docs; nenhum mod/probe/produto tocado | `git status` + hashes abaixo |

## Contrato de prova (herdado, aplicado)

- **Runtime ausente não recebe OK:** sem identidade suficiente (`fonte_sha`+`dll_sha`), sem `sessao`,
  sem hash confrontado e sem evidência do artefato lido, o melhor estado é `NAO_EXERCITADO`
  (`prova_runtime=False`); fixture nunca é verde (exit 2).
- **Defeito é defeito em qualquer procedência:** um defeito plantado sai `REPROVADO` mesmo em fixture
  — é assim que o controle negativo prova a regra.
- **Lacuna técnica ≠ pedido humano:** `NAO_EXERCITADO` carrega `tipo_pendencia=coleta_tecnica` e
  `autorizacao_necessaria=False`, com o próximo passo TÉCNICO nomeado.
- **Guarda load-bearing:** o driver RED neutraliza cada guarda e mostra o defeito escapando
  (`prova_red_kit10.py`), e o fonte original nunca é tocado (mutante temporário removido).

## Arquivos e SHA256

| Arquivo | SHA256 |
| --- | --- |
| `tools/automacao/kit10/kit10_cenarios.py` (novo) | e74771d461a78882f1b614dc8d812703768ae7e0e1d7f16e69cb3fee09a8c4be |
| `tools/automacao/kit10/test_kit10_cenarios.py` (novo) | dd9a5c25cdb37da675f6d98b1143c5f930ddc591b6f60d07987103db56f0e98f |
| `scratch/kit/KIT-10-run/prova_red_kit10.py` (novo) | b01919cf6e9588e02da48eedc0e4546e0d093190fad45d3854ddd8162d47f711 |

Reuso (LIDOS, **não editados** por esta frente) — hashes do estado atual no disco:

| Arquivo | SHA256 |
| --- | --- |
| `tools/automacao/cenarios/tooltips_shrines.py` (CIC-4) | 65c0f3b226fde23401131028f603bf01577d99896a3cae1244b632c20e673199 |
| `tools/automacao/estilo/estilo_atributos.py` (AUT-7) | 49cd80b641bff189f822ca28d89a6c9f659ccf845092a47f468ee82c518cc975 |
| `tools/checa_shrines.py` | a000cc178b2f93007dbf8c948ca553a1c8e9593e37aca52177bcde82e6900296 |
| `tools/testes/regras_shrine.py` | 1ef67649463eeab2b113f1423c8c6667ff24b9162c89633608e6c2a51bf9c562 |
| `tools/testes/regras_debugger.py` | 9e1cdd00b142a8b28aa0f06e8a129229a37702c381e30627054d223f6d1e30e7 |

> Observação de rastreabilidade: o hash de `tooltips_shrines.py` no disco **difere** do declarado na
> entrega CIC-4 (`df3258e8…`) — o arquivo foi alterado por OUTRA frente depois do CIC-4. Esta frente
> não o editou; o reuso é por import e os testes do CIC-4 continuam verdes.

## Preservação e limites

- Nada de parecer anterior foi reescrito. Alterações manuais do dono não foram tocadas.
- Os arquivos desta frente são artefatos de FERRAMENTA; não entram no runner `tools/testes/` (sem
  família `t_*`), como as demais frentes CIC/AUT/KIT. Rodam sozinhos com exit 0/1/2.
- **Runtime/UIUX/desempenho/build/deploy/pacote/publicação: NÃO_EXERCITADO.** Isto não substitui
  KIT-G1/G2, o aceite humano (DoD) nem os gates de publicação.
- A prova de `exit 2` da CLI está em `scratch/kit/KIT-10-run/` (volume/scratch, não versionado).
- Este trabalho NÃO conclui o DoD: segue para revisão independente (`kanban_request_review`).
