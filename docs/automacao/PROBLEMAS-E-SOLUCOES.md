# Board do Stolen Realm — problemas e soluções

Registro operacional. Cada item: **o que quebrou → como foi resolvido → como se reconhece de novo**.
Fonte: histórico de `task_events` (9838 `heartbeat`, 915 `respawn_guarded`, 284 `rate_limited`, 112 `blocked`,
40 `block_loop_detected`, 19 `escalated_repeated_failure`), o skill `stolen-realm-kanban-ops` e as rodadas de 09–13/10/2026.

---

## A. Despacho, roteamento e capacidade

1. **Frota ociosa com quadro "cheio".** Pools 0/3, 0/3, 0/1 e nada executável — o gargalo estava na lane de `review`,
   não nas rotas. → Medir na ordem: **review → dependências (`task_links`) → pino/assignee → pools**. Pool é o ÚLTIMO suspeito.
2. **Teto por perfil.** `max_in_progress_per_profile=1` tornava a fila serial mesmo com pools folgados (todos usam o perfil
   `default`). → Elevar junto com `CAPACIDADE` (= 7: 3+3+1 local).
3. **Tier local `fast` (16k) como worker.** Declarava 16k e a sessão de agente cresce até ~105k tokens: o backend recusa, o
   worker rotula **`rate_limited`** e o guard respawna idêntico → laço determinístico (caso `CIC-3F`: 6 mortes, ~14 h, zero artefato,
   heartbeat vivo o tempo todo parecendo saudável). → `fast` NUNCA serve worker; janela **declarada** grande; `RotaJanelaTests` trava isso.
4. **Pinar o cartão no NOME do tier desliga os guardrails** (checkpoint/handoff/vigia exigem `model_override == 'hermes-local'`).
   → Fixar o tier no **provider** (`extra_body.metadata.llm_tier`) e deixar o cartão em `hermes-local`.
5. **Família de cartão nova cai no tier local por padrão** (qualquer prefixo fora do funil não casa o classificador, mesmo com título
   "Revisar"/"Extrair") e nasce `ready` sem dono → é atribuído e spawnado. → Pinar **no `create`** (`--model/--provider`) e escrever
   no corpo que os filhos sejam pinados igual.
6. **Cartão `ready` SEM assignee nunca é despachado** (`admission` recusa `foreign_or_unassigned`, tick devolve `spawned: []` +
   `deferred: []`, que se lê errado como "política de pico"). → `atribuir_prontos()` no tick; e `assign` ANTES do tick em gate autorizado.
7. **Bloqueador de cadeia no tier local** (1 slot, ~2 min/turno) segura a cadeia inteira atrás de si — caso `ORG-R0`: 4 cartões do
   ChatGPT parados por um mecânico gratuito. → Critério: **bloqueador de cadeia → assinatura ou paga; local é para trabalho terminal**.
   Pergunta obrigatória ao pinar no local: *quantos cartões esperam por este?*
8. **Adiamento de pico sobre rota gratuita.** O freio de pico pegava também o `hermes-local` → fila congelada 7 h/dia sem economizar
   um centavo. → `paid()` governa os DOIS freios (`admission()` e `insufficient_runtime_margin`); rota gratuita nunca é adiada.
9. **Orçamento mexido só no `config.yaml`** → `validate_controls()` derruba o dispatcher **falhando fechado**
   (`RuntimeError: Unbounded budget`), ~45 min sem despachar e o quadro parecia parado. → Mudança de orçamento = guard + `test_economy.py`
   no mesmo passo; na dúvida, não mexer.

## B. Cartões presos e lanes travadas

10. **`review` para sempre**: `review_requested` gravado com `implementer=None` → sem proveniência o fechamento nunca aplica
    (a revisão independente reprovou as duas entregas fechadas por `specify`+`complete` e criou ela mesma o cartão de correção).
    → Preencher implementer/reviewer ao pedir revisão; fechar à mão citando parecer e sha256.
11. **`blocker_auth` por ERRO ANTIGO** (guard devolve park lendo `last_failure_error` de horas antes, sem nenhum `rate_limited` novo;
    `respawn_guarded` a cada 5 min por horas). → Limpar `last_failure_error` + `consecutive_failures` (em `review`, `unblock` recusa →
    escrever direto no banco com backup antes). **`rate_limit_cooldown` e `blocker_auth` pedem consertos OPOSTOS** (esperar × limpar).
12. **`review` ciclando não é `review` preso**: o guard tenta de novo a cada 5 min e **não conta falha** (18–21 `respawn_guarded`
    por cartão numa manhã). → Contar as tentativas antes de dizer "preso"; passando de `ESCALADA_APOS=12` (~1 h) a rotina re-fixa.
13. **`block_loop_detected` tira o cartão de `blocked` e joga em `triage` — e aí `unblock` recusa.** → Parquear escrevendo a linha
    (`status='blocked'`, `block_kind='needs_input'`) + evento próprio, **comentar a resposta do dono ANTES de destravar** (senão o worker
    respawnado age com a instrução velha e remonta a bancada).
14. **Cartão `triage` cujo corpo já é spec completa**: o `specify` do CLI chama o specifier LLM, **reescreve o corpo** e deixa em `review`
    (lane terminal) → perder bloco operacional e autorização. → Usar a API nativa `specify_triage_task(..., body=<corpo atual>)`;
    guardar o corpo original ANTES de qualquer `specify`.
15. **Cada lane aceita verbos diferentes** (`complete` recusa `triage`; `promote` só `todo`/`blocked`; `reclaim` só `running`;
    `stats` conta run velho como `running`). → Confiar no status do CARTÃO, não na contagem.
16. **Cartão em `triage` com o trabalho já feito** → `archive` (ou `specify`, se ainda vira spec).
17. **`unblock` zera falhas e erro mas PRESERVA `block_kind`** (recorrência de bloqueio sobrevive de propósito). → Snapshot do banco
    antes de destravar em lote e conferir os gates humanos byte a byte depois.

## C. Bloqueios: classificar antes de mexer

18. **Bloco técnico ≠ gate humano.** `WORKER_STAGNATION` (ou estouro de contexto) **não protege nada** → destravar e deixar re-rodar;
    `needs_input` com aceite/decisão/autorização → **não se solta**. Soltar gate humano gasta um turno: o agente lê, conclui
    "não é automatizável" e re-bloqueia igual.
19. **Três classes de recuperação automática** (não duas): **estagnação**, **infra transiente** (`HTTP 4xx/5xx`, `timed out`,
    `Connection refused` → mesma rota, teto de 3 recuperações) e **laço de falha repetida na mesma rota** (`escalar_laco`: 3 desfechos
    técnicos iguais → sobe UM degrau).
20. **Fila serial sem recuperação = fila parada**: cartão-cabeça bloqueado por motivo técnico → 20+ esperando, quadro ocioso
    (medido: 8 h de nada com o vigia rodando normal e `spawned: []`). → `recover_stagnation()` no ciclo do cron.
21. **Escalar por laço de `rate_limited` desfaz o roteamento do dono** (um cartão voltou ao pago 21 s depois de ter sido designado à
    assinatura). → Skip de laço `rate_limited` (cota não se cura pagando) e `assinatura_funcionando()` contando também runs EM CURSO.
22. **Dois mecanismos de escalada se anulando**: a rotina de cota devolvia à assinatura e o detector de laço re-escalava ao pago lendo
    `rate_limited` antigos → cartão espremido, relato dizendo "cota fora" com o serviço funcionando. → `deve_escalar(laco, assinatura_funcionando)`
    — **nenhum registro de falha vale mais que uma medição de agora**.
23. **Vaivém de rota.** → Anti-vaivém de 45 min (`pode_subir()` lê o `route_reverted`) e a **descida volta ao degrau de ORIGEM** com
    provider explícito — **nunca limpar o override** (cai no default do perfil, que é pago).
24. **Gate que falha por causa de um cartão ordenado DEPOIS dele** = dependência circular. → Inverter com `unlink` + `link`
    (o `link` recusa filho já `running`: reordenar **antes** de despachar).
25. **Dependência cuja finalidade já se cumpriu** (pré-voo de publicação que já saiu) → `unlink` com o motivo no `--result`.

## D. Custo

26. **Vazamento silencioso**: cartão criado por worker **herda o modelo padrão do perfil (pago)** — os guardas agiam na escalada e no
    rebalanceamento, **nunca na criação**. → Sempre `--model/--provider` no `create` **e** uma **sentinela que reverte o estado ilegal**
    (`vigiar_pinos_pagos`): pino pago de frente de baixa prioridade, longa duração ou cap desconhecido volta ao gratuito, com evento.
    **Regra geral: violação de custo não falha alto — ela gasta quieto. Rede de segurança > disciplina de quem escreve.**
27. **Nunca gastar dinheiro para "resolver" cota.** `gpt-6.1-sol` é assinatura (custo fixo; esperar é grátis), `deepseek-flash` é
    medido (~US$ 0,28/cartão fora do pico). → A rotina de cota escala para a rota **gratuita**; limpar erro stale **vale em qualquer rota**
    (não é gasto — a exclusão de rota paga vale só para ESCALAR/re-pinar).
28. **Reversão ingênua de pino** (`set-model <id> none`) volta para `model.default` = pago. → Fixar explicitamente `hermes-local --provider qwen-llm-gui`.
29. **Prova de gasto sem prova falsa**: `model_override` não é reescrito no spawn (fica o valor antigo) → a prova é a **linha de comando do
    processo** + `admission.jsonl` + `session_model_usage`; e **datar o log** antes de acusar (linha de dias atrás é histórico, não regressão).

## E. Infra, concorrência e ambiente

30. **Lock de escrita do quadro travado por deadlock (13/10, 16 min).** `gpt_quota_retry.limpar_stale` fazia UPDATE **dentro** de
    `with con:` e **no mesmo bloco** chamava `hermes kanban comment`: o CLI abre uma **segunda conexão** para o mesmo banco e espera a
    transação externa, que espera ele. Nenhum cartão subia, nenhum worker reportava, `hermes kanban create` pendurou 240 s.
    → **Commit primeiro, CLI depois**; melhor ainda: escrever o efeito por **SQL direto**. E **todo `subprocess.run` de automação precisa
    de `timeout=`** (sem isso o processo pendurado fica vivo segurando lock para sempre — foram os pids 24336/9340).
    **Receita de diagnóstico**: leitura funciona e escrita falha com `database is locked` **instantâneo**; listar
    `Get-CimInstance Win32_Process` (python.exe/hermes.exe) com **CreationDate + CommandLine** — o processo com o horário do último evento
    e linha `hermes kanban ...` é o culpado; `Stop-Process -Id <pid> -Force` resolve em segundos.
31. **Corrida no `controller.lock`** (dois despachos concorrentes; a rotina de cota rodava o despachante por cima do vigia). →
    Uma responsabilidade por script (cota em `gpt_quota_retry.py`, despacho em `economy_dispatcher.py`) e saída silenciosa (`sys.exit(0)`)
    quando o lock está tomado.
32. **Dois `dotnet build` do mesmo csproj colidem no `obj/`.** → Antes de buildar, confirmar que nenhum cartão de build está `running`
    (filtrar `Name` + `StartTime`, **não** `CommandLine` — casa com o próprio PowerShell).
33. **Handle de terceiro segurando a pasta de saves** (`Device or resource busy` no rename, com Steam e r2modman fechados) — o dono era
    o **VS Code** com a pasta de saves no workspace. → `handle64.exe "<caminho>"` para nomear o dono; conserto = tirar a pasta do workspace
    ou fechar a janela (segundos), **não reboot**. O cartão que faz certo declara `BLOQUEADO_POR_HANDLE` com o comando exato do erro.
34. **`persistentDataPath` é `LocalLow`** (irmão de `Local`) → derivar `Split-Path $env:LOCALAPPDATA -Parent`, nunca `Join-Path ... 'Low\...'`.
35. **Desmontar junction com remoção recursiva destrói o ALVO.** → `rmdir` sempre; nunca `rmtree`; hash antes/depois do diretório real como prova.

## F. Critérios de aceite (os que eu escrevi errado)

36. **Aceite exigindo estado GLOBAL limpo** é impossível por desenho num repo com frentes concorrentes: o cartão faz o trabalho, prova que
    fez, e **não fecha** — vira bloqueio falso (3 casos: `ORG-R6-GUARDA` release-check global; `LEVEL-R2-LAND` `git status` global;
    `RLP-RENAME` busca global vazia). → **O aceite nunca pode exigir que o PASSADO mude** (evidência congelada é imutável). Escrever
    "zero no conjunto ATIVO" + "o residual é evidência, listado arquivo por arquivo, sem curinga".
37. **Heurística de detecção**: se o aceite só fecha quando algo **fora do escopo do cartão** mudar, o defeito é a **redação**, não o trabalho.
38. **Aceite misturando condição técnica com aprovação humana** (foi o que travou o `BP-5`) → re-escopar: a aprovação humana é o gate do
    dono (`LANG-C4`/`BP-6`); o cartão técnico prova só o que é técnico.
39. **Licença/legalidade NÃO é gate** (Unlicense/domínio público, decisão do dono 09/10) → não criar critério jurídico; o que permanece, por
    risco real: o pacote não inclui assemblies do jogo.

## G. Runtime e bancada

40. **Duas bancadas brigando pelo mesmo recurso físico** (jogo, junction KIT-16, Steam Cloud) — o segundo boot destrói a evidência do primeiro.
    → **Encadear por `link`** para o grafo ser o mutex (`BP-5 → KIT-14 → LEVEL-RT`).
41. **Janela de ambiente curta demais**: pedir para religar a cloud com outro cartão de runtime já despachado → guard `require_cloud_off`
    recusa o boot e devolve bloqueio de ambiente (um ciclo perdido, culpa da orquestração). → A janela tem de cobrir o bloco INTEIRO de runtime.
42. **O estado de isolamento é cumulativo** (BepInEx → junction → Steam Cloud) e **a prova do toggle da cloud é o `sharedconfig.vdf`**
    (`"cloudenabled"`), não o `remotecache.vdf`. → appid 1330000; desligar → rodar → **religar** ao fim.
43. **Worker sem supervisão NÃO faz clique de sistema** (`block_kind=capability`) — é ambiental, não se contorna reenviando.
    → Navegar por **handlers in-process**; o que depender de clique vira **RUNBOOK** para o dono (humano na borda, agente na evidência).
44. **Autorização de runtime é POR RODADA e se consome** — deixar o próximo subir sozinho é boot não autorizado. → Parquear em
    `blocked/needs_input` e renovar. Hoje: **validação automática é pré-autorizada**; o único gate é **o jogo estar aberto**.
45. **Clique cedo demais** (`activeInHierarchy` ≠ `interactable`) fez o probe clicar o banner errado e o veredito virar "defeito do jogo".
    → Esperar `interactable`; e a tabela de leitura: **jogo fecha/crasha → defeito do jogo; entra na run e chega ao HUD → defeito do INSTRUMENTO**;
    travou/tela preta → pedir descrição e **não concluir**.

## H. Medição, medição e medição

46. **Resultado vazio ≠ objeto ausente**: glob com aspa literal no Windows (`git tag -l 'org-*'`) não casou nada → alarme falso de "tag deletada",
    com cartão desbloqueado e comentário errado já gravados. → Provar o negativo (listar tudo) antes de comunicar; se já comunicou, **registrar a
    correção no próprio cartão**.
47. **O `stats`/`list` do CLI mente PARA BAIXO** (já devolveu `todo 0 | blocked 0` com 30 `todo` + 5 `blocked` vivos). → Contar pelo banco.
48. **`running` no quadro ≠ processo vivo**; e **`running` + heartbeat + nenhum artefato = laço**. → A prova é artefato no disco com mtime recente
    e teste executado.
49. **Banco-isco**: `~/AppData/Local/hermes/kanban/kanban.db` tem ~6 bytes e não tem tabela `tasks`. → O banco real é
    `~/AppData/Local/hermes/kanban.db`; copiar sempre **db + -wal + -shm juntos**.
50. **Resumo humano virou spam** e o dono parou de ler (chave do hash usando `max(id)` de `task_events` — os `heartbeat` mudavam a chave em
    TODO tick). → Chave = último evento **NÃO-heartbeat**; tempo em faixas de 15 min; mensagem de 4 linhas. **Campo que muda a cada tick não entra
    no hash cru nem fica fora dele.**
51. **A frase que o dono vai LER nasce na INSTRUÇÃO do worker, não no relatório**: `reason` de engenheiro → o dono responde legitimamente
    "não entendi o que o cartão pede". → Escrever no `--reason` o texto **literal** que o worker deve usar, em linguagem de jogador, com as opções
    de resposta; e ao repassar, dizer **de qual frente é** (mod × instrumento), o que fazer visualmente e o que resolve.
52. **Aviso de bloqueio separado em três casos** (aguardando / decisão do dono / ação do operador) — chamar o dono para o que não é dele é ruído,
    e "nada a fazer" é mentira quando o passo é DELE. → Uma vez por bloqueio, idempotente, com `PAROU / Por que / Para que serve / Para destravar`.
53. **`Iteration budget exhausted (N/N)` NÃO é `delegation.max_iterations`** (é default de código no spawn; subir o config não muda o N).
    → Ler o N real em `task_runs.outcome`; cartão que morre assim está progredindo em blocos — contar mais um run, não anunciar fracasso.
54. **Prova sem artefato = falso verde**, e o **contador anti-estagnação só zera com `write_file` verificado ou teste real** (`grep`/`ls`/`read_file`
    não contam). → Ao reescrever o corpo para modelo local: artefato-primeiro, **arquivo NOVO numerado** por bloco, nunca sobrescrever.

## I. Repositório e branches

55. **O dia inteiro de trabalho foi para um branch local nunca enviado** (`ci-validate-test`, 11 commits; `main` intacto, nada passou por CI).
    → Conferir `git branch --show-current` antes de despachar frente que commita; mitigar com `git tag` (sobrevive a `branch -D`) e merge
    `--ff-only` **depois** que a frente parar de usar o branch.
56. **Trocar de branch sob worker rodando destrói o trabalho dele.** → Só **worktree temporário** (`git worktree add` + `merge --ff-only` + `remove`).
57. **Artefato dentro de `git worktree` é trabalho órfão**, não entrega (o mod não existe na árvore principal e desaparece se o worktree for removido).
    → Medir `git worktree list` + `git log main..<branch>`; abrir cartão de aterrissagem **sem** remover o worktree (é evidência).
58. **Junção que não pode ser feita agora não vira promessa verbal** → vira **job** (cron que checa "nenhum worker rodando + frente fechada +
    árvore limpa + trabalho ainda fora do `main`", faz o `--ff-only`, **nunca** dá push e responde silêncio quando não é hora).
59. **"Tem várias branches? Cuidado para os arquivos não ficarem para trás" é pergunta de AUDITORIA.** → Cartão de inventário/risco (não de mutação);
    checar `.gitignore` contra arquivos **de projeto** por arquivo (`git ls-files`/`git check-ignore -v`), separando fonte × build/dist × DLL do perfil;
    entregar ITEM → ONDE VIVE → ALCANÇÁVEL DO `main`? → RISCO → AÇÃO, e **criar os cartões das lacunas que achar**.
60. **`git add -A` é proibido** (o dono edita os fontes em paralelo; a edição dele tem prioridade absoluta) → um commit por frente.

## J. Governança (as regras que sobraram de tudo isso)

61. **Três classes de roteamento** (dono, 12/10): **mecânica** → `hermes-local` (sem pressa, janela baixa, custo mínimo);
    **pensamento** → Codex (raciocínio/criticidade, sem pressa, cota reinicia de 5 h); **gargalo** → escada local → Codex → DeepSeek,
    com o degrau pago cercado (cartão CURTO ≤ 3600 s, no máximo 1 pago em voo, nunca a frente de baixa prioridade).
62. **Cartão de PASSO HUMANO não tem classe** ("Revisão humana...", "Aprovar...", "Aceitar o kit"): nenhum worker é despachado nele e
    ele **não se solta para a fila de agentes** — um agente "revisando" no lugar do dono é mentira.
63. **Destrave manual também passa pelos guardas**: um casamento por palavra-chave ("autoriz") soltou o `KIT-G4` (gate humano) para a fila
    de agentes — exatamente o erro que a classe `humano` existe para impedir.
64. **Nada de cartão de agente parado sem input humano pendente** (dono, 10/10): `atribuir_prontos()` + `resgatar_triage_pronta()`,
    com o predicado testado — **cartão que ESPERA HUMANO nunca é resgatado** (o worker respawnado remonta a bancada por cima do teste do dono).
65. **Gate humano grande é matéria-prima, não bloco de leitura**: decompor em lotes de proposta (~20 itens) para o dono **aprovar um inventário**
    em vez de garimpar o bruto; cada lote entra como **PAI** do gate (para o aviso dizer `AGUARDANDO`, não chamar o dono cedo).

---

## O gargalo estrutural que a lista revela (13/10/2026)

A corrente `BP-5 → KIT-14 → LEVEL-RT → BP-6` (todo o pensamento do BetterPortuguese) está parada por um motivo só, e ele
não é técnico:

```
gates de aprovacao do dono (LANG-C1..C5) bloqueados
   -> as correcoes nao sao aprovadas
      -> o dataset "corrigido" (BP-3) tem ZERO mudancas em 9.095 registros
         -> o pacote do mod (BP-4) tem "ZERO mudancas"
            -> o BP-5 recusa o proprio aceite (e esta certo)
               -> a corrente inteira fica em `todo`, gated
                  -> o Codex (3 vagas, cota cheia) fica ocioso
```

O cartao `BP-ENC-1` (criado para "ligar BP-3 no BP-4") **bloqueou dizendo que a premissa estava errada**: o dataset ja esta
embutido byte a byte — o que falta e **conteudo aprovado**, nao encaixe. Ou seja: **o gargalo do quadro e a fila de revisao do dono.**
Instrumentos ja prontos para reduzir isso: o material de decisao `LANG-C4-REVISAO-DONO` (no Codex) e os avisos de bloqueio em
linguagem simples.
