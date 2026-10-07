# CIC-1 — correção dos bloqueios (revisão `CIC-1R-revisao.md`, tarefa `t_2c3e8182`)

Escopo exclusivo desta rodada: `tools/automacao/ciclo/ciclo.py`, `tools/automacao/ciclo/test_ciclo.py`
e **este** documento. Não toquei em `decisao.py`/`test_decisao.py` (CIC-2), em `cenarios/` (CIC-3/4),
na bancada offline, no coletor, em produto, `runtime`, `KANBAN.md` nem no board. O parecer anterior
(`CIC-1R-revisao.md`) segue intacto. Nada foi executado no repo de origem: toda a demonstração rodou
em **cópia congelada** sob o scratch do Hermes. Sem jogo, save, instalação, commit ou publicação.

## 1. O que foi corrigido (aceite + "Correções funcionais" do escopo)

### ACHADO 1 (bloqueante) — reuso de AUT-3 não amarrava o resultado aos bytes atuais
O ciclo carregava o AUT-3 e assinava os critérios com a identidade **de agora**, sem comparar o
**snapshot de fonte** que o próprio AUT-3 carrega (`guarda_repo.sha_antes` / `estados_separados.fonte`).
Resultado velho virava verde para fonte nova.

Correção: `confrontar_snapshot(aut3, repo)` recomputa o universo do AUT-3 (tracked+untracked, exceto
`scratch/`, `dist/` e os outputs `AUT-3-resultado.json`/`AUT-3-resumo.md`) e compara **conjunto de
hashes** — alterado/removido/**criado** = divergência. Snapshot ausente/vazio/divergente ⇒ o AUT-3
**não prova os bytes atuais**: todos os critérios OK caem para `NAO_EXERCITADO`, entra um critério
`reuso_snapshot_aut3`, e a rodada sai `INCOMPLETO`/nova rodada (nunca APROVADO). O bloco `reuso`
(`snapshot_ok`, `snapshot_motivo`, `snapshot_detalhe`, `n_snapshot`/`n_atual`) é gravado no resultado.

**Antes × depois (mesmo AUT-3 de origem, `gerado_em 15:47`, sobre a cópia congelada):**

| código | comando | estado | exit |
|---|---|---|---|
| **antigo** (`ciclo.py` pré-correção) | `--aut3-resultado docs/automacao/AUT-3-resultado.json` | `APROVADO_OFFLINE` | **0** (falso verde) |
| **novo** | idem | `INCOMPLETO` (snapshot=78, atual=498, **420 criados**) | **2** |

Provas em `scratch/cic1-corr/`: `old-antigo.out` (exit 0, `fonte_sha=d31740d7` assinando log velho) e
`r-old.json` / `r-old.out` (exit 2, `reuso.snapshot_ok=false`, **0 critérios OK**, fila com
`reuso_snapshot_aut3`).

### ACHADO 2 (bloqueante) — estado/exit do ciclo não incorporavam a decisão nem o `dll_sha`
`identidade_suficiente` exigia só `fonte_sha` (a `decisao.py` exige `fonte_sha` **E** `dll_sha`), e o
resumo escondia `falhas_automaticas`; o exit não consultava a decisão.

Correção:
- `identidade_suficiente` agora exige **`fonte_sha` E `dll_sha`** (mesmo critério da decisão) — sem DLL
  (clone sem build) **nada** vira OK;
- o estado final é reconciliado com a decisão: `REPROVADO` se houver severidade `REPROVADO`,
  `INCOMPLETO` se houver falha automática/offline não exercitado — **nunca APROVADO paralelo a falha
  automática**;
- a fila recebe também as falhas da decisão que o ciclo não cobria (`fila_da_decisao`);
- o resumo curto passa a imprimir `falhas_automaticas`, `pendencias_humanas`, `pronto`,
  `motivo_pronto`, `escala`, `motivo_escalacao` — nada de falha técnica escondida.

**Contraste que fecha a prova** (cópia congelada, sem `bin/Release` → `dll_sha=None`): antes o ciclo
podia sair APROVADO enquanto a decisão reprovava; agora o `--limite` e a cópia sem DLL saem
`INCOMPLETO`/`REPROVADO`, `pronto_para_decisao=false`, fila preenchida (testes
`test_cli_sem_dll_nao_aprova_e_mostra_falhas`, `test_cli_decisao_discorda_do_ciclo_e_rebaixa_aprovado`).

### ACHADO 3 (secundário) — `sem_progresso` não escalava e `motivo_escalacao` mentia
`motivo_escalacao` era preenchido com a mensagem de escalonamento enquanto `escala=False`.

Correção: `avaliar_escalonamento(tem_falha, tent, limite)` decide escalonamento e preenche o motivo
**só quando escala**. Escala quando `numero > limite` **ou** `sem_progresso_seguidas >= limite`. O
motivo diz explicitamente o destino: **supervisor/agente técnico (NÃO ao dono)**. Campo novo
`destino_escalonamento` (`supervisor`/`ciclo`). Se não escala, `motivo_escalacao` sai vazio
(testes `TestEscalonamento`, `test_cli_escalona_por_sem_progresso` → `ESCALADO` exit 1).

### ACHADO 4 (secundário) — fila apontava o conferidor, não a causa
`montar_fila` reusava a evidência como `caminhos` e carimbava `tarefa_origem` com o id do
orquestrador para tudo.

Correção: cada critério pode declarar `causa`; a fila expõe `causa`, `causa_desconhecida`,
`roteamento` (`causa`/`desconhecido`), `caminhos` = a causa, `evidencia` separada, e `tarefa_origem`
= a tarefa do critério **ou `"desconhecido"` explícito** (nunca o id do orquestrador por omissão). No
demo real, `cp_dupes` (contra-prova) roteia para **`BetterTooltips/Patches/LocalizePatch.cs`**; falhas
de conferidor sem arquivo-fonte declaram `causa_desconhecida=true`.

### Erro oculto no fallback da decisão
`carregar_decisao` agora devolve também `presente`. `decisao.py` **ausente** = fallback mínimo legítimo
(pré-integração); `decisao.py` **presente e quebrada** = falha técnica, vira critério `decisao_consolidacao`
`REPROVADO`, entra na fila e impede APROVADO (`d["decisao_erro"]`). Nunca cai calado no fallback.

## 2. Prova real

### 2.1 Testes (TDD, verdes)
`python tools/automacao/ciclo/test_ciclo.py` → **38 testes, OK, exit 0**.

Fluxo TDD: os 26 testes novos/ajustados foram escritos primeiro e rodaram **vermelhos** (4 `FAIL` +
22 `ERROR` — funções ainda inexistentes), depois a implementação os deixou verdes. Cobrem: snapshot
confere/divergente/ausente/arquivo-novo; identidade exige fonte+dll; fila causa vs desconhecido;
reuso divergente ⇒ `INCOMPLETO`; decisão discorda do ciclo ⇒ rebaixa APROVADO; escalonamento por
limite e por sem-progresso; decisão quebrada não esconde erro; `--verificar` válido/mutado.

### 2.2 Ciclo fechado defeito → fail → correção → revalidação (cópia congelada)
Identidade da cópia congelada (`cic1-demo/repo-frozen`), 498 arquivos de fonte + `bin/Release`:
- estado corrigido: `fonte_sha=d31740d740c6bc4fb67a2c18ddc18ec9fb23acb1b04e9a7fdd0e47dc601b3674`, `dll_sha=bca54d2b55455e09…`
- estado com defeito: `fonte_sha=3fe3b74cc6ce517ce7acffcf75cff7546d2e2eeb8aa6a061d707f2745669aedb`

Defeito plantado **em bytes** (CRLF preservado): duplicação da linha `{ "Resist Divine", "Resist Holy" },`
em `BetterTooltips/Patches/LocalizePatch.cs`. Reversão **byte-exata** (sha do arquivo volta a
`29ff26a77c07…`, igual ao original).

| rodada | fonte | AUT-3 | estado | exit | `REPROVADO` | `OK` |
|---|---|---|---|---|---|---|
| **R1** | com defeito | REPROVADO (6/6 builds) | `REPROVADO` | **1** | 5 | — |
| **R2** | corrigida | VERDE (6/6 builds) | `INCOMPLETO` | **2** | **0** | 29 |

R1 falhou **5 critérios** pelo único defeito: `check_dupes`, `cp_dupes`, `audita_docs`, `suite_puros`,
`suite_contra_prova`. Após a correção byte-exata, **os 5 voltaram a `OK`** (delta por id entre `r1.json`
e `r2.json`). Os 6 builds de cada rodada usaram `-p:DeployToBepInEx=false` em cópia isolada (≤6/rodada);
a fonte→DLL ficou `NAO_EXERCITADO` na cópia isolada (o `bin/Release` da cópia foi buildado ancorado no
repo de origem, e o anchor do sandbox é a cópia) — é o comportamento *fail-closed* correto, **reportado**
e não escondido.

R2 não é APROVADO porque restam **24 falhas automáticas**: 6 `fonte_dll_*` + 6 `cobertura:M*`
(primeiras causadas pelo anchor da cópia isolada) + 12 residuais de **runtime** (AUT-4/5/6 + jogo).
Todas ficam **no ciclo** (`falhas_automaticas`, `pronto_para_decisao=false`), nenhuma virou tarefa
humana (`pendencias_humanas=0`).

`--verificar r2.json`: válido → exit **0**; após 1 byte novo na fonte → exit **3**
(`aprovacao anterior INVALIDADA`). Controle negativo real.

### 2.3 Caminho barato de revalidação (reuso), sem builds
- AUT-3 da **R2** reusado (snapshot confere: 498==498, 0 divergências) → `INCOMPLETO` exit 2, **29 OK**,
  mesmo estado da R2 (o guarda **não** bloqueia reuso legítimo).
- AUT-3 da **R1** (cópia com defeito) reusado contra a fonte corrigida → snapshot divergente (1 alterado),
  `REUSO` exit **1**, **0 critérios OK**, fila com `reuso_snapshot_aut3`.
- AUT-3 **velho do repo** (15:47) reusado → `INCOMPLETO` exit 2, 0 OK (contra 420 criados).

## 3. Integração com `decisao.py` (CIC-2) — contrato fixo, sem polling
A `decisao.py` **mudou em voo** durante esta rodada (sha `b95ddc382ce46bb1…` no momento da cópia;
eu havia lido a versão anterior). O ciclo consome apenas o contrato documentado
`consolidar(criterios, identidade) -> {por_mod, falhas_automaticas, pendencias_humanas,
pronto_para_decisao, aceite_humano, publicacao}` e os campos de item `id/mod/classe/severidade/
motivo_decisao/evidencia/tarefa_origem` — os testes de CLI rodaram **contra a versão atual** e
passaram. **Não** escrevi em `decisao.py`/`test_decisao.py` nem fiz polling. O pai roda a validação
final depois de todas as entregas.

## 4. Limites e cobertura (honestos)
- Sem jogo/save/instalação/publicação; nenhuma prova de runtime aqui (os 12 residuais de runtime
  continuam `NAO_EXERCITADO` e vão ao backlog/AUT-4/5/6 e ao dono só como **autorização** de rodada).
- A demonstração rodou em cópia congelada; `fonte→DLL` não é provável em cópia isolada (anchor do
  `bin/Release`), portanto **nao** se atribui esse FULL à fonte atual mutada — o número que vale é o
  delta R1→R2 (defeito) e o reuso com snapshot confrontado.
- O merge/commit final é do pai; a árvore do repo tem edições concorrentes (CIC-2/3/4/5) — qualquer
  escrita de outro agente muda `fonte_sha` e derruba aprovações anteriores (fail-closed por desenho).

## 5. Arquivos e hashes (working tree)

| arquivo | sha256 | linhas |
|---|---|---|
| `tools/automacao/ciclo/ciclo.py` | `169c8084388d47a30b0146dd0aa385b808b7d604950f3aaab9a88475911c8288` | 1110 |
| `tools/automacao/ciclo/test_ciclo.py` | `783652d6cee8f3feecbc6fc6e8a313e49194c90c9213f8366f123e2ccc50c12f` | 539 |
| `docs/automacao/CIC-1-correcao.md` | (este) | — |

Evidência em `AppData/Local/hermes/cache/scratch/cic1-corr/`: `r1.json`, `r2.json`, `r1.out`, `r2.out`,
`verif-ok.json`, `verif-mut.json`, `r-reuso-r2.json`, `r-reuso-r1.json`, `r-old.json`, `old-antigo.*`,
`log.txt`, `demo.sh`; cópia congelada em `…/scratch/cic1-demo/repo-frozen`.

Sem deploy, sem jogo, sem save, sem instalação, sem commit/push/publicação nesta rodada.
