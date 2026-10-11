# KIT-10 — entrega FINAL (correção do KIT-10R, request_changes)

Cartão `t_bbad760d`. Filho de revisão: `t_896796be` (KIT-10R). Rodada do implementador: **run655**
(correção pedida pela revisão independente **run651**, parecer em `docs/automacao/KIT-10R-parte01.md`).
Rodada **OFFLINE**: nenhum jogo, save, perfil, probe, build, install, deploy, commit ou publicação.
**Nenhum mod, gameplay ou arquivo de outra frente foi alterado.**

> Este arquivo SUBSTITUI `docs/automacao/KIT-10-entrega.md` (rodada anterior, run646), que fica no
> histórico com duas declarações a corrigir: (a) a suíte tinha 17 casos, agora tem 24; (b) a tabela
> dizia `test_estilo_atributos.py` **exit 0** — o exit REAL medido é **1** (ver F4 abaixo).

## 1. O que a revisão pediu e o que foi feito

| Achado do KIT-10R | Correção aplicada | Prova |
| --- | --- | --- |
| **F1 (ALTO)** `_asp_por_evento` só tinha blacklist de boot: `estagio="banana"` + `evento_id` fechava `OK/prova_runtime=True` | novo ramo `elif estagio not in ESTAGIOS_DE_EVENTO:` → **NAO_EXERCITADO** (motivos distintos para "sem estágio" e "estágio fora da whitelist"). A whitelist agora vale em TODOS os ramos | caso `C-guarda-estagio-desconhecido`; RED `G1-estagio-desconhecido`; probe do revisor P2 agora NAO_EXERCITADO |
| **F2 (ALTO)** `_asp_worship_dobro` ignorava (`continue`) aura viva sem item: `itens_observados={}` → `defeito=[]` → `OK/prova_runtime=True` | lista `faltando`; estado passa a `REPROVADO` → `NAO_EXERCITADO` (se alguma aura viva não foi medida) → `OK` (só com tudo medido). `observado["sem_observacao"]` nomeia as auras não medidas; `itens_observados` não-mapa também vira "não medido" | casos `B-guarda-itens-ausentes`, `B-guarda-itens-parciais`; RED `G2-itens-ausentes`; probe P3/P3b agora NAO_EXERCITADO. Comportamento confirmado do "dobro" (DWA-2) preservado |
| **F3 (MÉDIO)** `_asp_contexto_dano` não media a tooltip com `aura_buff` fora da tabela e aprovava | `lacuna` cobre (a) buff declarado fora da tabela / sem atributo e (b) `contrib` ausente com esperado independente disponível; ordem `REPROVADO` > `NAO_EXERCITADO` > `OK`; `observado["lacuna"]` documenta | casos `A-guarda-buff-fora-tabela`, `A-guarda-contrib-ausente`; RED `G3-contrib-ausente`; probe P4 agora NAO_EXERCITADO |
| **F4 (handoff)** a entrega declarava `test_estilo_atributos.py exit 0`; na árvore viva o exit é 1 | reconferido nesta rodada: **exit 1** (`total: 28 \| falhas: 1`; `REPROVADAS: medicao offline REAL: roda a suite do projeto e nao deixa mod sem familia de teste`). Causa: mod sem família de teste detectado por escritores concorrentes de outra frente — **não é do KIT-10** (a frente não toca `tools/automacao/estilo/` nem família `t_*`). Declarado como lacuna, não mascarado | log `scratch/kit/KIT-10-run655-estilo.txt`; exit real 1 |

## 2. Provas reais executadas nesta rodada (comando → saída → exit)

| Execução | Saída real | Exit |
| --- | --- | --- |
| `python tools/automacao/kit10/test_kit10_cenarios.py` | `TOTAL\|rodaram=24 reprovaram=0 nao_rodaram=0` (antes 17) | **0** |
| `python tools/automacao/kit10/test_kit10_cenarios.py --isca` | `ISCA\|OK\|defeito plantado detectado: N-A-source: esperado=OK estados=['REPROVADO']` | **0** |
| `python scratch/kit/KIT-10-run/prova_red_kit10.py` (5 guardas originais) | `PROVA-RED\|PASSOU\|5 mutacoes\|todas as guardas load-bearing` | **0** |
| `python scratch/kit/KIT-10-run655/prova_red_kit10_guardas.py` (3 guardas NOVAS) | `PROVA-RED\|PASSOU\|3 mutacoes\|as tres guardas novas sao load-bearing` (cada: original `NAO_EXERCITADO/False` → neutralizada `OK/True`) | **0** |
| `python scratch/kit/KIT-10R-run651/probe_revisor.py` (**probe da própria revisão**, reexecutado contra o fonte corrigido) | P2/P3/P3b/P4/P5 todos `NAO_EXERCITADO False` (antes P2/P3/P3b/P4 = `OK True`) | **0** |
| `python tools/automacao/kit10/kit10_cenarios.py --observacoes scratch/kit/KIT-10-run/fixture.json` | `OK=0, REPROVADO=0, NAO_EXERCITADO=19 ... com prova runtime: 0` | **2** (fixture nunca é verde) |
| `python tools/automacao/cenarios/test_tooltips_shrines.py` (reuso CIC-4) | `TOTAL\|rodaram=28 reprovaram=0 nao_rodaram=0` | **0** |
| `python tools/automacao/estilo/test_estilo_atributos.py` (reuso AUT-7) | `total: 28 \| falhas: 1` (F4, pré-existente, de outra frente) | **1** |
| `check_segredos.py` / `check_padroes_segredo.py` / `check_dupes.py` / `audita_docs.py` | travas do repo | **0** (4/4) |

Saídas guardadas em `scratch/kit/`: `KIT-10-run655-probe-revisor.txt`, `KIT-10-run655-cli-fixture.txt`,
`KIT-10-run655-cic4.txt`, `KIT-10-run655-estilo.txt`.

## 3. Aceite do cartão — veredito por critério

| Critério do cartão | Estado | Prova |
| --- | --- | --- |
| Relacionar tooltip/contexto/dano e fonte/receptor corretos em shrines | PASSOU (offline) | aspecto A: dano do ground effect no eixo `Source` (bonus 0), tooltip de buff no eixo `Target` do receptor; `A-ok-runtime` + 2 controles negativos + RED `A-contexto-fonte`/`A-contexto-dano` |
| Preservar **Worship** confirmado, não remover o dobro para tornar o teste verde | PASSOU (offline) | `B-ok-dobro-preservado` (gatilho 2 / atributo 1), `B-defeito-dobro-removido` REPROVADO, RED `B-dobro` |
| BetterStats base `SavedMap`/final | PASSOU por reuso (offline) | reuso AUT-7 (`AUT-7/BetterStats/*` no conjunto) |
| BetterFont/BetterCombatText material/keywords/cores e **superfícies por evento, não prefab de boot** | PASSOU (offline) | reuso AUT-7 + aspecto C; `C-defeito-boot` REPROVADO; **novo** `C-guarda-estagio-desconhecido` NAO_EXERCITADO (F1) |
| Debugger contrato sem truncar texto | PASSOU (offline) | reuso `regras_debugger` → `tools/census.py`; `D-defeito-pipe-no-valor`, `D-defeito-truncado` REPROVADOS; RED `D-dump` |
| Critérios independentes rastreáveis, várias superfícies e controles negativos | PASSOU | esperado de fonte independente (oráculo/tabelas/censo); 5 defeitos plantados + **5 guardas anti-falso-OK** + 2 iscas; RED 5+3 mutações |
| Completar campos apenas necessários por caso; **runtime ausente não recebe OK** | PASSOU | `fixture-nao-prova-runtime` (exit 2, zero OK) + `guardas-sem-falso-ok` (F1/F2/F3 nunca fecham OK/prova_runtime) |
| Não modificar mods/gameplay nesta tarefa | PASSOU | `git status` só mostra `tools/automacao/kit10/` e `docs/automacao/KIT-10*` |

**NÃO_EXERCITADO:** runtime/UIUX/desempenho/build/deploy/pacote/publicação, gates KIT-G1/G2/G3/G4 e
aceite humano (DoD). Aprovação técnica não é aceite humano nem publicação.

## 4. Arquivos e SHA256 desta rodada

| Arquivo | SHA256 |
| --- | --- |
| `tools/automacao/kit10/kit10_cenarios.py` (corrigido) | a46cf76f011947c58f8ca87c4579c13c8b24ff8b5c6caf674570d83ddaab1414 |
| `tools/automacao/kit10/test_kit10_cenarios.py` (corrigido) | 30ca0c493d2fe018a64818c06555591f3afe7da12e74b9fcb4eb73ebe6feb427 |
| `scratch/kit/KIT-10-run655/prova_red_kit10_guardas.py` (novo) | 84d5601873820f86599244e587f267aee808dc3f1ec7b64f9ed1359b85b27a87 |
| `scratch/kit/KIT-10-run/prova_red_kit10.py` (intocado) | b01919cf6e9588e02da48eedc0e4546e0d093190fad45d3854ddd8162d47f711 |

Reuso (LIDOS, **não editados** por esta frente; hash do disco no momento desta rodada):
`tooltips_shrines.py` CIC-4 `65c0f3b2…`, `estilo_atributos.py` AUT-7 `49cd80b6…`,
`checa_shrines.py` `a000cc17…`, `regras_shrine.py` `1ef67649…`, `regras_debugger.py` `9e1cdd00…`.

Documentos desta rodada: `KIT-10-parte03.md` (plano), `KIT-10-parte04.md` (correção + provas),
este `KIT-10-entrega-final.md`.

## 5. Limites e passo seguinte

- O handoff pede **nova revisão independente** (instância ≠ run655) no mesmo cartão
  (`kanban_request_review`); nada foi autoaprovado.
- `test_estilo_atributos.py` segue **exit 1** por causa pré-existente de outra frente (mod sem
  família de teste) — registrado como lacuna, não corrigido aqui (não é escopo do KIT-10).
- Nenhum `git add`, commit ou publicação foi feito.
