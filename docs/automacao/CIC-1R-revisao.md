# CIC-1R — revisao independente do orquestrador do ciclo (`t_9b3bb1ac`)

Revisor ≠ autor. Somente leitura do produto: a unica escrita no repo e este doc; toda execucao
foi em scratch Hermes (`AppData/Local/hermes/cache/scratch/cic1r/`). Nao toquei board/KANBAN,
nao editei `ciclo.py`/`test_ciclo.py`, bancada, `decisao.py`, cenarios, runtime, produto.
Nenhum build/jogo/save/install/commit/publicacao. Ignorei o diff `runtime/**` (CIC-5 em andamento).

## Estado lido (bytes exatos)

| arquivo | sha256 | linhas |
|---|---|---|
| `tools/automacao/ciclo/ciclo.py` | `2165df50051113dc53bb984317e25c9f5a3f23edcf4d396d6acffed4bf1565f0` | 872 |
| `tools/automacao/ciclo/test_ciclo.py` | `4a29fe9760bfe9f2f7202f35577594f3f68b9b1d7aaf61edf623fe7fe75f4c95` | 329 |

Ambos confereм com `docs/automacao/CIC-1-entrega.md`. Modulo esta **untracked** (`?? tools/automacao/ciclo/`).
`AUT-3-resultado.json` da origem: `9c1aa58244ed…` (gerado **15:47:35**); o da rodada FULL ficou na copia
(`cic1-full/ciclo-copia/…`, `3911a5e4b2b9…`, gerado 18:07:41).

## Veredito: REPROVADO / BLOQUEIO (aceite #2 e #4 nao satisfeitos) — 2 achados bloqueantes + 2 secundarios

---

### ACHADO 1 — BLOQUEANTE (aceite #2). `--aut3-resultado` nao amarra o resultado aos bytes atuais

O reuso carrega o AUT-3 e marca os criterios OK (`ciclo.py:362-478`) com a identidade **de agora**
(`rodada`: `identidade(repo)` em `:683`, gravado em `:750,789`). O ciclo **nunca compara** a identidade
interna que o proprio AUT-3 carrega (`estados_separados.fonte` / `guarda_repo.sha_antes`): a unica
referencia a `guarda_repo` e `.get("intacto")` (`ciclo.py:433`). Logo, resultado velho vira novo.

- **Repro controlada** (mini-repo git + CLI real, scratch): `aut3` com snapshot `guarda_repo.sha_antes={"a.py": <sha V1>}`
  e `estados_separados.fonte={"a.py": V1}`; rodada 1 (a.py=V1) → `APROVADO_OFFLINE` exit 0; muto a.py p/ V999;
  rodada 2 reusando o MESMO aut3 → **`APROVADO_OFFLINE` exit 0** com sha divergente (aut3=V1, fonte=V999). O ciclo ignorou o snapshot.
- **Repro no repo real**: `python tools/automacao/ciclo/ciclo.py --repo C:/dev/stolen-realm --resultado <scratch>/r-reuso.json --aut3-resultado docs/automacao/AUT-3-resultado.json` → exit **0**, `APROVADO_OFFLINE`,
  `fonte_sha=cc346e119c8d` — reusando um AUT-3 de **15:47** (`9c1aa5…`) num repo que mudou bastante desde entao.
- **Contraste que fecha a prova**: `--verificar <r1.json>` contra 1 byte novo → **exit 3** ("fonte mudou … aprovacao anterior INVALIDADA"). O guarda **existe** nesse modo e **falta** no reuso — dois modos, duas respostas.
- **Teste ausente**: a suite so reusa aut3 que casa com a fonte; nunca muta entre gerar e reusar (`test_ciclo.py:275-325`). O defeito e invisivel para os 21 testes.

### ACHADO 2 — BLOQUEANTE (aceite #4). `estado`/exit do ciclo ignora a `decisao.py` embutida e o `dll_sha`

`ciclo.identidade_suficiente` exige **so** `fonte_sha` (`ciclo.py:226-228`), mas `decisao.identidade_suficiente`
exige `fonte_sha` **E** `dll_sha` (`decisao.py:86-94`). Sem `bin/Release` → `dll_sha=None`:
o ciclo diz `APROVADO_OFFLINE` exit **0**, enquanto `decisao.falhas_automaticas=3`, `pronto=False`.
O `_imprimir` (`ciclo.py:836-848`) mostra apenas `origem_decisao` e **esconde** `falhas_automaticas`;
o exit code nao consulta a decisao. Aceite #4 e descumprido ("sem esconder falhas tecnicas").
- Repro (mini-repo, CLI real): `estado=APROVADO_OFFLINE  dec.pronto=False  dec.falhas=3  dll_sha=None`.
- No repo real ha DLLs (`dlls` mapeadas), entao **nao dispara hoje** — mas e alcancavel em clone/repo sem
  build e o defeito de contrato (relatorio curto escondendo falha tecnica) permanece.

### ACHADO 3 — secundario. `sem_progresso` nao escala sozinho e `motivo_escalacao` engana
2ª e 3ª rodada com mesma fonte+mesmas falhas (`limite=5`): `sem_progresso=True`, `escala=False`,
`estado=REPROVADO`, porem `motivo_escalacao` **preenchido** com a mensagem de escalonamento (`ciclo.py:775-781`)
— campo contradiz o flag. Escalonamento por `numero>limite` funciona (`--limite 1` → `ESCALADO` exit 1), mas
"sem progresso" nao aciona escalonamento, so avisa.

### ACHADO 4 — secundario. Fila acionavel aponta o conferidor, nao a causa
`montar_fila` (`ciclo.py:489-511`): `caminhos` = evidencia = o **script conferidor** (ex.: `tools/check_x.py`),
nunca o arquivo-causa; `tarefa_origem` e **sempre** o id do orquestrador (`TAREFA="t_2c3e8182"`, `ciclo.py:58`),
nao a tarefa dona do defeito. Estrutura do contrato existe (caminhos/tarefa/falha/evidencia/criterio) e a
instrucao textual e clara, mas o roteamento nao chega ao dono por `caminhos`/`tarefa_origem`. Itens com
`execucao_automatica=False` e `requer_nova_rodada=True` — **OK** (nenhum comando executado).

### INDETERMINADO — fechamento por fail→fix→revalidate nunca foi demonstrado no caminho completo
Os artefatos do autor confirmam: FULL (`2cfc18484f6a`) e seu reuso rodaram **sobre a mesma fonte**
(`resultado.json` e `resultado-reuso.json` ambos `fonte_sha=2cfc…`) — o reuso **nunca exercitou fonte mutada**.
A demo defeito→correcao terminou R2 com 2 falhas ambientais e a "regressao direta verde" foi rodada **fora** do
ciclo; portanto o `APROVADO_OFFLINE` comprovado veio de (a) arvore limpa com 6 builds e (b) reuso — **nao** do
caminho defeito→correcao. Sob `--sem-build` nao ha atalho: a bancada marca a fase de builds `NAO_EXERCITADO`
(`bancada_aut3.py:276-288`) e conferidores de artefato saem vermelhos (o autor registra isso). Nao rodei builds
(restricao da revisao), entao **nao exercitei** o fechamento por esse caminho: INDETERMINADO, nao OK.

### Lacuna de cobertura (menor). Identidade nao cobre config do perfil nem observa/runtime
A identidade do ciclo = bytes do repo (git tracked+untracked) + DLLs `bin/Release`. Nao ha `config_sha` nem
observacoes runtime no portao; o `guarda_perfil` do AUT-3 so **prova que o perfil nao foi mutado** (nao gata
aprovacao) e cobre `plugins/` e `config/` (`bancada_aut3.py:132-135`). Aceitavel pelo contrato v1
(`fonte_sha`/`dll_sha`), mas "config e observa/runtime quando aplicavel" nao esta ligado ao portao.

### Contexto (nao e defeito). Identidade ampla × trabalho paralelo
A identidade inclui **todo** untracked nao-ignorado (481 arquivos hoje): qualquer escrita de outro agente
(CIC-2/3/4/5) muda `fonte_sha` e derruba aprovacoes anteriores. Fail-closed e coerente, mas explica por que a
aprovacao do autor (`2cfc…`) ja nasceu invalida — e o reuso nao a invalida (liga ao ACHADO 1).

---

## Itens OK (com prova)

- **OK** — Suite real: `python tools/automacao/ciclo/test_ciclo.py` → **21 testes, OK, exit 0** (`Ran 21 tests ... OK`).
- **OK** — Fila declarativa; nada executa comando de correcao (`montar_fila`), `execucao_automatica=False` confirmado em execucao.
- **OK** — CIC-2 agrega residual: 12 lacunas de runtime → **2** itens de autorizacao (BetterTooltips 9, RSTV 3); `pendencias_humanas=12` brutas agregadas em 2 itens; offline nao vai ao dono (`falhas_automaticas=0`). "12 lacunas nao viram 12 tarefas humanas" — satisfeito.
- **OK** — Cobertura runtime e residual e **nunca** OK; sem identidade suficiente nada vira OK (`ciclo.py:379-380,400-401`; `test_sem_identidade_build_nao_vira_ok`).
- **OK** — Exit codes conferem com a doc: `--verificar` valido=0 / mutado=3; aut3 ausente=`INCOMPLETO` exit 2; revalidate fresco=`APROVADO_OFFLINE` exit 0.
- **OK** — Backend: sem LLM proprio; consolidador real `decisao.py` (usa quando existe, cai na minima se ausente/quebra).
- **OK (contra-prova de trava, real)** — Regressao focada em **copia** (produto intacto): duplicar 1 entrada do `LocalizePatch.cs` → `python tools/check_dupes.py` **exit 1**; restaurar → **exit 0**.

## Travas rodadas
`test_ciclo.py` (21 OK), `check_dupes.py` na copia (fail/pass), CLI real nos 4 modos, `decisao.py` via ciclo.
Nao rodei suíte completa/build por restricao da rodada.

## O que NAO consigo confirmar (fica para o dono/runtime)
- Fechamento defect→fix→revalidate no caminho completo (exige 6 builds) — INDETERMINADO acima.
- Prova runtime/em jogo: nenhuma aqui; fixture de runtime nao prova jogo.
- Se a DIVERGENCIA do ACHADO 2 ocorre no fluxo real (hoje ha DLLs) — nao exercitado no repo real.

## Encaminhamento (supervisor, nao dono)
Bloqueantes (1,2) exigem conserto em `ciclo.py` + teste (o guarda do `--verificar` deve valer para o reuso;
`estado` deve reconciliar com `decisao`/`dll_sha`). Secundarios (3,4) e a lacuna de identidade vao ao backlog.
Falhas tecnicas ficam no ciclo; nada aqui e tarefa do dono.

## Evidencia (scratch Hermes)
`AppData/Local/hermes/cache/scratch/cic1r/`: `r-reuso.json`, `mini/` (repro controle), `mini2/aut3-snap.json` +
`snap-r*.json` (snapshot ignorado), `regressao/` (check_dupes fail/fix). Autor: `scratch/cic1-full/resultado*.json`.
