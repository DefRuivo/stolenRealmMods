# AUT-6 — automatizar tooltips e conferencia de shrines por personagem (`t_775eb4ae`)

> **Rodada OFFLINE.** Nenhum jogo aberto/encerrado, nenhum save, nenhum install, nenhum build,
> nenhum commit, push ou publicacao. O caminho **runtime continua NAO EXERCITADO** e assim esta
> declarado em todo criterio. Automacao **nao** substitui aceite humano nem publicacao do DoD.

## 1. O que foi entregue

| arquivo | papel |
|---|---|
| `tools/automacao/aut6/cobertura.py` | **avaliador** `avaliar(observacoes, identidade) -> criterios` (contrato v1) + CLI com exit 0/1/2 |
| `tools/automacao/aut6/casos-aut6.json` | os **cenarios** (o esperado **nao** e digitado: o modulo o calcula das fontes) |
| `tools/automacao/aut6/observacoes_fixture.py` | monta as observacoes de FIXTURE a partir do **conteudo real** das fixtures versionadas |
| `tools/automacao/aut6/observacoes-fixture.json` | as observacoes rotuladas `fixture` (gerado; `--gravar`) |
| `tools/automacao/aut6/test_cobertura_aut6.py` | suite offline (24 casos) + ISCA (`--isca`) |
| `tools/automacao/aut6/fixtures/globule-rv28.txt` | fixture NOVA do globule (RV-28/32), no formato do `Marca` do `GlobulePatch` (`.txt` de proposito: o repo ignora `*.log` no git) |
| `tools/automacao/aut6/fixtures/armor-bug34-superficies.txt` | fixture NOVA das duas superficies do Armor (feed x corpo) |
| `tools/automacao/aut6/fixtures/tooltip-shrine-corpo.txt` | fixture NOVA do corpo renderizado da tooltip de shrine (linha + nota) |

Escrita exclusiva desta rodada: `tools/automacao/aut6/**` e este documento. **Nada mais foi
editado** — em particular `tools/checa_shrines.py`, `tools/gera_shrines_esperado.py`,
`tools/dados/*.csv`, `tools/fixtures/*` (so LEITURA), produto, `tools/automacao/runtime`,
`tools/automacao/ciclo` e `tools/automacao/cenarios`.

## 2. Cobertura por tarefa (RV) — o que cada criterio exercita

| tarefa | casos no avaliador | o que e conferido | fonte do esperado |
|---|---|---|---|
| **RV-26** | `S-rv26-receptor-duas-pessoas`, `S-rv33-decay-portador`, `S-rv33-flame-atacante`, `S-rv26-corpo-linha-nota` | receptor x source (a linha e POR personagem), o numero dinamico da linha (Flame por alvo; a `[0]` do Decay) e o corpo renderizado com linha+nota | tabela gerada + percentuais + asset |
| **RV-27** | `S-rv26-corpo-linha-nota` | a LINHA azul presente no corpo renderizado (posicao/cor sao da leitura visual; o offline fica com `regras_cor.py`, ja no gate) | contrato do fonte (`ShrineAuraPatch`/`LocalizePatch`) |
| **RV-28** | `S-rv28-dwarven-duas-pessoas`, `S-rv26-receptor-duas-pessoas`, `S-rv28-globule-sustenance` | item proprio da aura de gatilho (Dwarven), receptor/source e a **cura dinamica do globule por personagem** | tabela gerada (Dwarven) + **`docs/cobertura/acoes.csv`** (Sustenance I `.08f` / II `.20f`) |
| **RV-29** | `S-rv29-dentro-da-aura`, `S-rv29-fora-da-aura` | DENTRO a linha aparece; FORA nao aparece — a observacao tem de **declarar** entrar/sair | contrato do fonte (`AurasVivas`, lista viva) |
| **RV-31** | `S-rv28-omnism-horn-cadeia`, `S-rv29-*`, `S-rv31-dedupe-stacking` | agregado por atributo + a cadeia do bonus (0/20/100) + **dedupe** da aura repetida | tabela gerada |
| **RV-33** | `S-rv33-decay-portador`, `S-rv33-flame-atacante` | Decay = % da vida do PORTADOR; Flame = % da vida do ATACANTE projetado, eixo `Source` (RV-30) | `shrines-percentuais.csv` + `round_half_even` (mesma conta do `checa_shrines`) |
| **RV-34** | idem + `S-rv49-divergencia-perigo` | o defeito do proprio mod superado pelo RV-30; a **divergencia do RV-49 registrada** | tabela gerada (coluna `eixo=Source`) |
| **RV-46** | `S-rv31-dedupe-stacking`, `S-rv46-teto-*`, `S-rv50-piso-*` | `instancias=[X xN]` (1x, nunca Nx), **TETO/PISO** do atributo e o `cru` | `resources.assets@1519603860` (Max=50) e `@1519616544` (Min=-75) |
| **BUG-34** | `S-bug34-armor-feed-e-corpo` | **as duas superficies**: feed/texto flutuante SEM a nota e corpo da tooltip COM a nota (`reabre_bug=false`) | contrato do fonte (`EmTextoDeFeed`/`BuildArmorNote`) |

Cada criterio carrega: `id`, `mod`, `estado`, `classe`, `procedencia`, `prova_runtime`,
`esperado` (**com a fonte citada**), `observado`, `evidencia`, `motivo`, `tarefa_origem`,
`tarefas_rv` e, da rodada, `identidade_rodada` (`fonte_sha`/`dll_sha`/`config_sha`,
`observacoes`, `casos_sha256`); o criterio de runtime aprovado tambem leva `sessao` + os hashes
confrontados (contrato positivo do ciclo).

## 3. Regras duras exercitadas (todas com teste)

- **AUSENCIA NAO E APROVACAO.** Sem observacao: `OK=0`, `NAO_EXERCITADO=20`,
  `INDETERMINADO=1` (so a divergencia do RV-49), **exit 2**.
- **Fixture nao prova runtime.** No caminho so-fixture `prova_runtime=False` em TODOS os 21
  criterios e o exit continua **2**.
- **Runtime sem cadeia nao aprova**: sem identidade, sem `sessao`, sem hash declarado, hash de
  **outra build** (`INDETERMINADO`) ou sem **evidencia de artefato que existe no disco** —
  qualquer um dos cinco derruba para `NAO_EXERCITADO`/`INDETERMINADO`.
- **O caminho verde existe** (nao e um avaliador que nunca aprova): com observacao de RUNTIME
  completa os 20 casos fecham `prova_runtime` e, **removida a divergencia do RV-49**, o exit e 0.
- **Lacuna tecnica nao vira pedido humano**: so a decisao do **RV-49** sai como
  `tipo_pendencia=decisao_dono`; o resto e `coleta_tecnica`.

## 4. Evidencia (execucao real, offline)

```
$ python tools/automacao/aut6/cobertura.py --offline
AUT-6 offline (nenhuma observacao): {"total": 21, "OK": 0, "REPROVADO": 0,
  "NAO_EXERCITADO": 20, "INDETERMINADO": 1, "com_prova_runtime": 0}
exit esperado: 2 (ausencia NAO e aprovacao) -> obtido 2                       exit 2

$ python tools/automacao/aut6/observacoes_fixture.py --gravar
gravado: tools/automacao/aut6/observacoes-fixture.json (9 observacoes)        exit 0

$ python tools/automacao/aut6/cobertura.py --observacoes .../observacoes-fixture.json
por estado: OK=20 REPROVADO=0 NAO_EXERCITADO=0 INDETERMINADO=1 (com prova runtime: 0)
                                                                              exit 2

$ python tools/automacao/aut6/test_cobertura_aut6.py
TOTAL|rodaram=24 reprovaram=0                                                 exit 0

$ python tools/automacao/aut6/test_cobertura_aut6.py --isca
ISCA OK: defeito plantado detectado (11 criterio(s) reprovados)
TOTAL|rodaram=25 reprovaram=0                                                 exit 0

$ python tools/testes/roda_testes.py --puros        -> VERDE (exit 0)  (suite do projeto intacta)
$ python tools/audita_docs.py                       -> nenhuma inconsistencia (exit 0)
$ check_dupes / check_notas_redundantes / check_segredos / check_versoes /
  check_chave_compartilhada --estrito               -> exit 0
```

Controle negativo (cada defeito plantado na fixture/observacao, estado exigido pelo teste):

| defeito plantado | criterio | estado exigido | resultado |
|---|---|---|---|
| `%` do Sustenance (8 -> 9) | `S-rv28-globule-sustenance/so-tier1` | REPROVADO | OK |
| frase nao fecha com o pool (4 -> 9 mana) | `S-rv28-globule-sustenance/so-tier1` | REPROVADO | OK |
| contribuicao multiplicada (40 -> 120) | `S-rv31-dedupe-stacking` | REPROVADO | OK |
| repeticao da aura nao exercitada | `S-rv31-dedupe-stacking` | NAO_EXERCITADO | OK |
| linha presente FORA da aura | `S-rv29-fora-da-aura` | REPROVADO | OK |
| DENTRO da aura sem a linha | `S-rv29-dentro-da-aura` | REPROVADO | OK |
| observacao sem declarar dentro/fora | `S-rv29-*` | NAO_EXERCITADO | OK |
| nota de Armor no FEED/texto flutuante | `S-bug34-.../feed` | REPROVADO | OK |
| corpo da tooltip SEM a nota | `S-bug34-.../corpo` | REPROVADO | OK |
| regressao sem as superficies declaradas | `S-bug34-...` | NAO_EXERCITADO | OK |
| corpo de shrine sem a LINHA azul | `S-rv26-corpo-linha-nota` | REPROVADO | OK |
| `MaxValue` do log != asset (50 -> 60) | `S-rv46-teto-damage-reduction` | REPROVADO | OK |
| asset ausente no limite | `S-rv46-teto-damage-reduction` | NAO_EXERCITADO | OK |
| runtime sem identidade / hash de outra build / sem evidencia | varios | NAO_EXERCITADO / INDETERMINADO | OK |

## 5. Fontes do esperado (independentes, rastreaveis) e hashes dos bytes lidos

Nenhum esperado mora no avaliador nem no log do mod: o modulo **importa** `tools/checa_shrines.py`
e le as tabelas GERADAS, o censo de acoes e o asset.

```
a000cc178b2f93007dbf8c948ca553a1c8e9593e37aca52177bcde82e6900296  tools/checa_shrines.py        (reusado, NAO editado)
d58ee0c931fb5efdff08189f48cbb4085a06c0fc03072c9f3fb9dcae83de5dcc  tools/gera_shrines_esperado.py (reusado, NAO editado)
836f2833d2ef50e0ee14aaebe17b551f9ed7f6a09fc029771ffced5c048824ce  tools/dados/shrines-esperado.csv    (gerada)
99174e006dd7d70560142012d1d752ce7b43113d68751c7b47f7836929e549b2  tools/dados/shrines-percentuais.csv (gerada)
077f69edc600a7e8eb25028cb221863b09144c9a7efe8ee2e5b8463206a22ab4  docs/cobertura/acoes.csv      (acao do motor - Sustenance)
c192ad94b06db685d3a8308055acbd8ff3eeee8d57ea9c66f77b4243edb8ac9f  docs/cobertura/status.csv     (censo - base das auras)
29ff26a77c0722432196794a50fc242a8fef24f97926c6ba134c38257c4d309c  BetterTooltips/Patches/LocalizePatch.cs
7e3bd18ac737edc8954e84fa78f103aca0a74e4281a70b586ee1eb142fce8173  BetterTooltips/Patches/ShrineAuraPatch.cs
771dec0f01d64a17aca9f438e7d14fd053a8094028d2f87197b2b285c40cf0fd  BetterTooltips/Patches/GlobulePatch.cs
3d9d5a2031e4c5b74d4a15726e43154f14fcfbac309d66099091a5839f971f1b  tools/fixtures/shrines-exemplo.log
06696792855f487a1ce2662b8f82c627aa49268511ec8d945a96066adf17b4b6  tools/fixtures/shrines-rv46-dedupe.log
641a5a775d5b7f54c982890518892d654d48b3b46574ecef66d41ccc3288d817  tools/fixtures/shrines-piso-cru.log
```

**DLL do mod em uso (identidade da rodada, leitura):** perfil do owner
`.../profiles/Default/BepInEx/plugins/BetterTooltips/BetterTooltips.dll`
sha256 `270f311b0f7bb5cca5a61f42e6adb56cbadcb7e8965a49bd5bb940c61c3cbe6b` (mtime 05/10 13:36 -
o MESMO `270f311b…` do inventario AUT-2). O binario do repo e o do perfil nao foram alterados.

Entregaveis desta rodada:

```
a935f573ebf1fda914c7684d092b995833c2330c82914f06808e9c3bbfc11f4d  tools/automacao/aut6/cobertura.py
ade76e34a3456c2e7000d49c8db2a8bceba1c0ff0a37b8ae892acdf2d6225da1  tools/automacao/aut6/casos-aut6.json
867a098c61eb4f1e2f25e4ac359f4bfb72f0c2a399c58f026d4b35bba1d48ec4  tools/automacao/aut6/test_cobertura_aut6.py
52a299aecf20af9b3466a57810ed9285db5274d242fae65c8c4f6510c92ceff8  tools/automacao/aut6/observacoes_fixture.py
78c446e54bd66709050978a16999641accfa3e8c05bbee6f53819e49711133c6  tools/automacao/aut6/observacoes-fixture.json
4ce54eef44707ea1e93446be220445bdb6481e302f13fdb92bb353ecd40234cb  tools/automacao/aut6/fixtures/armor-bug34-superficies.txt
d258f9cda92a260597c4e9eb6ce8c61787bc28bc99ae5e22f927376b241ed668  tools/automacao/aut6/fixtures/globule-rv28.txt
e7a0f8af190db9dc91e822441328dc558f028466702c0805c4e058949f677043  tools/automacao/aut6/fixtures/tooltip-shrine-corpo.txt
```

## 6. LACUNAS (nunca OK) e o roteiro humano RESIDUAL

**NAO EXERCITADO nesta rodada** (nao houve autorizacao para jogo/install/save):

1. A leitura do **objeto vivo** (texto renderizado, posicao/cor) — corpo da tooltip, linha azul e
   `[Globule RV-28]` de uma sessao real saem `NAO_EXERCITADO` sem uma observacao do coletor.
2. Os **marcadores em sessao viva**: `RV-31 acumulado` / `RV-44 item` / `RV-46 teto|piso` /
   `RV-34 linha do Decay` / `RV-34 Flame alvo` / `[Globule RV-28]` com o build instalado.
3. A **medicao em jogo com/sem Omnism/Horn** das auras de PERIGO (o dado que fecha o **RV-49**).
4. O dano de **RETORNO** do Flame (atacante x portador) — segue como experiencia em jogo (RV-19 §9).

**Roteiro humano residual (so o que nao da para automatizar)** — uma unica frente controlando o
jogo, com autorizacao explicita do owner:

1. Autorizar a rodada e **reiniciar o jogo** com o probe/coletor instalado (probe novo = exige
   instalacao e boot; **nao ha hot-reload** — declarado, nao prometido).
2. Coletar, por personagem (sem bonus / `Omnism II` / `Horn of Devotion`), DENTRO e FORA da aura:
   o `LogOutput.log` do perfil (marcadores da §6.2) + o objeto vivo da tooltip (texto renderizado).
3. A unica **decisao humana**: o **RV-49** — medir o dano de Decay/Flame com/sem o bonus e decidir
   qual versao fica (a automacao registra a divergencia, **nao** altera formula para ficar verde).
4. Leitura visual final (cor/posicao/sobreposicao) do bloco azul — o passo do DoD que e do owner.

## 7. Hotspot e integracao (para o pai)

- **`hotspot: tools/automacao/cenarios/tooltips_shrines.py`** — o arquivo estava sendo ESCRITO por
  outro agente durante esta rodada (bytes mudaram as 19:59:28; sha `a801debe…` contra o
  `c4e0a837…` declarado no CIC-4). Por isso o AUT-6 **nao** importa nem edita o modulo do CIC-4:
  ele reusa a infraestrutura ESTAVEL (`checa_shrines` + tabelas + oracle) e emite o **mesmo
  contrato v1**. Se os dois conjuntos divergirem, o achado e do pai (decisao, nao conserto local).
- **Integracao no ciclo**: `decisao.consolidar(criterios, identidade)` consome a saida direto
  (mesmos campos). O AUT-6 **nao** foi adicionado a `tools/testes/roda_testes.py` de proposito:
  a suite do projeto tem contagem publicada (85/85) e mexer nela altera documentos auditados —
  decisao do pai. A suite roda sozinha (`test_cobertura_aut6.py`, exit 0/1).
- `.cfg`/perfil/`LogOutput.log` **nao** foram tocados; nenhuma DLL foi construida ou copiada.

## 8. O que NAO foi feito

- Nao abri/fechei o jogo, nao carreguei save, nao instalei probe, nao publiquei, nao commitei.
- Nao rodei build (`dotnet build`) — nao era necessario e nada de produto foi alterado.
- Nao reabri o BUG-34: o criterio e **so regressao** (`reabre_bug=false`), com o aceite de 05/10
  preservado.
- Nao alterei `KANBAN.md`, `tools/checa_shrines.py`, `tools/gera_shrines_esperado.py`,
  `tools/dados/**`, `tools/fixtures/**`, `tools/automacao/ciclo/**`, `tools/automacao/cenarios/**`
  nem qualquer arquivo de mod.
