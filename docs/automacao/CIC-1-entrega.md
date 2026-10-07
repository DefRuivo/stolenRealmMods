# CIC-1 — orquestrador do ciclo validação → fila → revalidação (t_2c3e8182)

Escopo exclusivo desta entrega: `tools/automacao/ciclo/ciclo.py`, seu teste `test_ciclo.py` e este doc.
Não toquei em `decisao.py`/`test_decisao.py` (CIC-2), em `cenarios/*` (CIC-3/4), na bancada offline, no
coletor, em produto, `KANBAN.md` nem no board. Nenhum deploy, nenhum jogo, nenhum save, nenhum
commit/push/publicação. As rodadas reais do ciclo rodaram em área externa (scratch) — a árvore do repo
só recebeu os dois arquivos desta entrega e este doc.

## O que o `ciclo.py` faz

Reusa a bancada offline **AUT-3** como motor de validação (não reimplementa build/suite/conferidores) e
acrescenta o que faltava para fechar o ciclo:

- **Identidade de fonte e DLL**: `fonte_sha` = sha256 canônico da árvore de trabalho atual (tracked +
  untracked via `git ls-files`, fail-closed sem git) menos `scratch/`, `dist/` e os outputs do próprio
  AUT-3; `dll_sha` = sha256 canônico das DLLs `bin/Release`. Identidade só é **suficiente** com as duas
  (mesmo critério do `decisao.py`); sem ela nenhum critério pode ficar OK.
- **Resultado válido só para os bytes atuais**: (a) o resultado AUT-3 tem de ter sido **reescrito nesta
  rodada** (mtime muda; senão `STALE`, ignorado — nunca falso verde); (b) mudança de fonte **durante** a
  rodada ⇒ `INVALIDADO_POR_MUDANCA_DE_FONTE` (exit 3); (c) o **reuso** de um AUT-3 confronta o *snapshot*
  de fonte que o próprio AUT-3 carrega (`guarda_repo.sha_antes` / `estados_separados.fonte`) contra os
  bytes de agora — snapshot ausente ou divergente ⇒ `INCOMPLETO`/nova rodada; (d) `--verificar <resultado>`
  reconfere **fonte e DLL** de um resultado guardado contra os bytes atuais.
- **Fila de correção declarativa** para supervisor/agentes: cada falha vira item com `criterio, mod,
  classe, falha, causa|causa_desconhecida, caminhos, evidencia, tarefa_origem, fonte_sha,
  requer_nova_rodada, execucao_automatica: false` e instrução textual. **Nada é executado automaticamente.**
- **Limite e sem progresso**: `numero`, `limite` (padrão 5), `sem_progresso` (mesma fonte **e** mesmas
  falhas), `sem_progresso_seguidas`; acima do limite ⇒ `ESCALADO` com motivo apontando o **supervisor
  técnico** (nunca o dono).
- **Estado/exit incorporam a decisão**: `falhas_automaticas` sai da consolidação (`decisao.py` quando
  presente; no seu lugar, uma consolidação mínima do contrato quando o módulo ainda não existir) e **não há
  `APROVADO_OFFLINE` convivendo com falha automática**; identidade insuficiente nunca aprova; erro de
  consolidação do `decisao.py` nunca é escondido pelo fallback.
- **Escopo explícito**: rodada de regressão delimitada (`--checagem ID`) aprova como `APROVADO_REGRESSAO` —
  nunca como FULL. Só a rodada FULL (AUT-3 completo, `--jogo`, ≤6 builds) pode dizer `APROVADO_OFFLINE`.
- **Área externa serializada**: `ciclo.lock` na área de trabalho impede duas rodadas concorrendo na mesma
  área (lock de pid morto é retomado). Área ocupada ⇒ a rodada **não começa**, sai `INCOMPLETO`/2 e nem
  cria a cópia.
- **`--ancora`**: valida um **congelamento** byte-exato do repo (`--repo <cópia congelada> --ancora <repo
  real>`), preservando o PathMap da prova fonte→DLL quando o repo compartilhado tem outros agentes
  escrevendo durante a rodada.
- **Criterios** no contrato: `id, mod, estado(OK/REPROVADO/NAO_EXERCITADO/INDETERMINADO),
  classe(offline/runtime), procedencia(execucao/runtime/fixture), esperado, observado, evidencia[caminhos
  reais], motivo, tarefa_origem` + `comando`. A cobertura da matriz AUT-2 entra como residual de
  **runtime** (pendência), nunca OK.

### CLI

```bash
# rodada real: copia o repo p/ area externa e roda AUT-3 --ancora origem --jogo (OFFLINE, sem deploy)
python tools/automacao/ciclo/ciclo.py --repo <repo> --trabalho <area> --resultado <saida.json>
# regressao delimitada (0 builds): um --checagem por ID de CHECAGENS do AUT-3
python tools/automacao/ciclo/ciclo.py --repo <repo> --trabalho <area> --resultado <saida.json> --checagem check_dupes
# congelamento: mesma rodada, com a ancora no repo real
python tools/automacao/ciclo/ciclo.py --repo <congelado> --ancora <repo real> --trabalho <area> --resultado <saida.json>
# revalidacao barata: reusa um AUT-3 ja gerado (sem copia, sem build; exige snapshot coerente)
python tools/automacao/ciclo/ciclo.py --repo <repo> --resultado <saida.json> --aut3-resultado <AUT-3-resultado.json>
# confere se um resultado guardado ainda corresponde aos bytes atuais (fonte + DLL)
python tools/automacao/ciclo/ciclo.py --repo <repo> --verificar <saida.json>
```

Exit: `0` APROVADO_OFFLINE / APROVADO_REGRESSAO · `1` REPROVADO ou ESCALADO · `2` INCOMPLETO ·
`3` INVALIDADO_POR_MUDANCA_DE_FONTE. Esquema do resultado: `CIC-1/1`, com `identidade`, `identidade_depois`,
`escopo`, `aut3_meta`, `criterios`, `fila_correcao`, `pendencias_offline`, `pendencias_runtime`,
`tentativas`, `escala`, `decisao`, `estado`, `historico`.

## Correções desta rodada (o que a revisão bloqueou e o que mudou)

A revisão da 1ª tentativa apontou três bloqueios — os três foram corrigidos e provados:

1. **Reuso de AUT-3 antigo não vinculava snapshot à fonte atual.** Agora `confrontar_snapshot` compara o
   `sha_antes` do AUT-3 com os bytes de agora (alterados/removidos/criados) e baixa qualquer OK; snapshot
   ausente também não aprova.
2. **Estado/exit ignoravam falhas da decisão e o `dll_sha`.** Agora o estado final deriva das falhas
   automáticas consolidadas, exige identidade suficiente (fonte **e** DLL) para aprovar, e `--verificar`
   invalida quando a DLL mudou mesmo com a fonte igual (caso da DLL fora do git — há teste).
3. **O ciclo não fechava falha→correção→revalidação aprovada dentro do próprio orquestrador, sem falha
   ambiental escondida.** Resolvido: `--checagem` roda a **regressão delimitada real** pelo motor do AUT-3,
   e as causas ambientais da 1ª entrega foram eliminadas (`dist/` entra na cópia; a evidência dos guardas é
   o artefato da rodada, não um caminho que pode não existir; rodada bloqueada por lock não escreve nada).

Achados reais desta rodada (cada um com correção ou registro):

- **Concorrência na área externa** — duas instâncias do ciclo na mesma área se destroem (uma apaga
  `aut3/sandbox` e o `ciclo-copia` da outra; a sobrevivente reprova por sandbox vazio, **falso vermelho de
  ambiente**). Corrigido com `ciclo.lock` (obsoleto por pid morto é retomado) + 3 testes.
- **Evidência do guarda** — `guarda_perfil`/`guarda_repo` intactos saíam OK sem artefato de evidência
  persistido, e o `decisao.py` os reprovava por "sem evidência". Agora o OK exige o artefato da rodada como
  evidência; sem ele o critério sai `NAO_EXERCITADO` (honesto).
- **`dist/` fora da cópia** — a contra-prova do BCT depende do artefato de build; sem `dist/` ela saía como
  falha ambiental. `dist/` passa a ser copiado.
- **Sobra de teste no scratch** — `rmtree(ignore_errors=True)` falha com objetos `.git` read-only no Windows
  e deixava centenas de pastas; o `tearDown` usa o removedor com tratamento de read-only.
- **Achado no AUT-3 (não editado, fora do escopo)**: `construir_sandbox` faz `shutil.rmtree` sem tratar
  read-only e crasheia se sobrar `sandbox/` de rodada anterior; e `--sem-build` reprova conferidores que
  dependem de artefato buildado (`pacotes_preflight`, `audita_docs` em alguns estados). O ciclo contorna o
  primeiro limpando `<area>/aut3/sandbox` com tratamento de read-only; o segundo fica registrado.

## Prova real (comandos exercitados, saídas verdadeiras)

**Testes** — `python tools/automacao/ciclo/test_ciclo.py` → **45 testes, OK, exit 0** (rodado no repo e na
cópia). Cobrem identidade estável/sensível a 1 byte, untracked e DLL ignorada pelo git; fail-closed sem git;
reuso com snapshot fiel/divergente/ausente; fila com causa × causa desconhecida explícita; guarda violada;
sem identidade ⇒ nunca OK; contra-prova OK/REPROVADA; cobertura runtime como residual; sem progresso × fonte
nova; invalidação durante a rodada; `--verificar` válido/inválido/DLL trocada; resultado stale; `decisao.py`
opcional (usa, cai para a mínima se ausente, **reporta** se quebrada); lock (vivo bloqueia, obsoleto retoma,
área ocupada não cria cópia); e **regressão delimitada real pelo motor do AUT-3**
(falha → correção → `APROVADO_REGRESSAO`).

**Rodada FULL real (AUT-3 completo, cópia isolada, 6/6 builds)** — sobre cópia congelada do repo com
`--ancora C:/dev/stolen-realm`: `AUT-3 VERDE`, `6/6` builds `-p:DeployToBepInEx=false` com
**`fonte=Release=perfil` provado nos 6 mods**, `11/11` conferidores OK, suite `85 puros` +
`49 PROVA_OK + 14` + `1 jogo`, `5/5` contra-provas `PROVA_OK`, `guarda_perfil=True`, `guarda_repo=True`,
`fases_puladas=[]`.
Ciclo: **41 critérios OK**, **12 `NAO_EXERCITADO`** (residual de runtime da matriz AUT-2), fila com
**12 itens `classe=runtime`**, `pendencias_offline=0`, `falhas_automaticas=12`, `pronto_para_decisao=False`,
estado `INCOMPLETO`. `fonte_sha 30b3e25e4a2f…` · `dll_sha bca54d2b5545…` (dlls por mod: bct `06dae5aa7b5e`,
bf `2c07f5e959af`, bs `5a3c001ad424`, bt `270f311b0f7b`, rd `99c156799380`, rstv `454587a031a3`).

**Ciclo defeito → correção → revalidação, com o `ciclo.py` do repo, sobre cópia do repo real** (0 builds):

| rodada | exit | estado | fila |
|---|---|---|---|
| R0 baseline | 0 | APROVADO_REGRESSAO | — |
| R1 (credencial plantada + versão divergente, **na cópia**) | 1 | REPROVADO | `check_segredos`, `check_versoes` |
| R1b (mesma fonte, mesmas falhas, `--limite 2`) | 1 | **ESCALADO** ao supervisor técnico | idem |
| R2 após correção byte-exata | 0 | APROVADO_REGRESSAO | — (fila vazia, 0 falhas automáticas) |

`--verificar`: **exit 0** nos bytes atuais; com 1 byte novo na fonte: **exit 3** ("fonte mudou desde a
rodada … aprovacao anterior INVALIDADA"); após reverter: **exit 0**. A cópia voltou byte-exata e a origem do
repo não foi tocada.

**Invalidação por concorrência, observada numa rodada real**: uma FULL no repo compartilhado executou o
AUT-3 `VERDE` 6/6 e o ciclo recusou a captura (`INVALIDADO_POR_MUDANCA_DE_FONTE`, `b0aa01aeb792 →
329250e7dc6a`) porque outro agente escreveu no repo durante a rodada — exatamente o comportamento exigido, e
o motivo de existir o `--ancora`.

## Integração (para CIC-2/3/4 e o supervisor)

- O ciclo consome `decisao.consolidar(criterios, identidade, aceite_humano=None)` e nada mais. A identidade é
  `{fonte_sha, dll_sha, …}` + `raiz` (para a decisão resolver os caminhos de evidência).
- Módulos de cenário expõem `avaliar(observacoes, identidade) -> [criterios]`, no formato do contrato.
- **Achado de integração para o CIC-2/pai**: com o `decisao.py` atual, os **12 itens de runtime** (cobertura
  AUT-2, `classe=runtime`, sem `tipo_pendencia`) são classificados como **falha automática** — fila de agente,
  não roteiro humano. É coerente com o contrato ("não mandar todo runtime ausente ao dono"), mas implica que a
  rodada FULL termina `INCOMPLETO` enquanto esses itens não vierem dos adaptadores de cenário (CIC-3/4) com o
  sinal explícito de autorização/julgamento visual. A decisão é do CIC-2, não do orquestrador — o ciclo só
  reporta, nunca esconde.
- A fila é a **única** saída acionável: supervisor/agente corrige e pede **nova rodada**. Sem backend LLM
  próprio, sem comando de correção executado pelo ciclo.

## Arquivos e hashes

| arquivo | sha256 | linhas |
|---|---|---|
| `tools/automacao/ciclo/ciclo.py` | `241a90f2248445ed8d90bc295146f1237b2a25fa3d1291630519d10f22700950` | 1303 |
| `tools/automacao/ciclo/test_ciclo.py` | `b4d28cb0e440fec79761585b06de013f4106042fb6cd5ce3d5394c180d1d5198` | 641 |

Sem deploy, sem jogo, sem save, sem instalação, sem commit/push/publicação nesta rodada.
