# AUT5-F2 — conserto do confronto de motivo das guardas e consumo da "falha" do produto no log

Adendo ao **AUT-5** (`t_76a41ea7`) e à revisão independente **AUT-5R** (`t_a6bb7f27`).
Card: **`t_9cee7d21`** (filho da AUT-5R e da AUT5-F1 `t_dd95f8d9`). Escopo **offline**:
nenhum jogo aberto, nenhum save carregado, nenhum probe instalado, nenhuma publicação,
nenhum byte escrito no perfil do dono. `git status --porcelain` = **82** antes e depois;
HEAD `f526fe9`.

Os arquivos desta frente **disputam** com a AUT5-F1, por isso a rodada começou reconferindo
as âncoras (§ 1) e refazendo os controles do parecer (§ 6) **antes** de qualquer edição.

## 1. Âncoras: o que eu recebi e o que eu declarei

Hashes do estado **no início desta rodada** (lidos do disco antes de editar — o `md5` é o
que ficou registrado no meu primeiro comando; o `sha256` do estado anterior **não** é
recuperável depois da edição, ver "limite" abaixo):

| arquivo | md5 no início da rodada | sha256 declarado pela AUT5-F1 |
|---|---|---|
| `tools/automacao/aut5/aut5.py` | `336dad83599aa91357fd780aefc62b8d` | `6e5e53eb6c50333f839387a8c0425c06ec111402a9a24cb3e9165698ffc8431c` |
| `tools/automacao/aut5/log_rstv.py` | `8c4384c0c5585947a7c901ee235d6b2e` | `fcf22c95406304c974b474e7d9fcdbbd7acce7634e16f29e791994677e147c22` |
| `tools/automacao/aut5/cenarios-rstv.json` | `eb3f3e373deaf58628699b03233522df` | `7b56e4fc79d8130a3c9f48e931b45ec1f52a8b28da5bf3e357a863690dbe5063` |
| `tools/automacao/aut5/test_aut5.py` | `89c5663ad6746d0a78ad72ea95bcd6a6` | `1b42c8aab126c19894720e726290c35b62004dcaa503c45ff7f81a78e5572dc2` |

**Verificação possível (e feita) das âncoras de terceiros:** todos os arquivos em que esta
rodada **não** mexeu continuam byte a byte iguais ao que a AUT5-F1 declarou —
`tools/automacao/aut5/test_snapshot_modal.py` `054aecb1…` (um dos cinco arquivos da frente,
intocado aqui), `tools/automacao/runtime/coletor.py` `0518634e…`,
`tools/automacao/cenarios/rstv.py` `524f7197…`, `tools/automacao/ciclo/decisao.py`
`d6de959e…`, `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs` `09debb76…`,
`tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` `afa4ee6d…`. O produto
(`RoguelikeSkillTreeVisualizer/*.cs`) **não foi editado** nesta rodada.

Hashes da entrega **depois** do conserto:

| arquivo | sha256 | linhas |
|---|---|---|
| `tools/automacao/aut5/aut5.py` | `3c8cb998abd59edaf40c9fb7bee11f8809d806d0ee5c2708eaaf479aacec6bec` | 908 |
| `tools/automacao/aut5/log_rstv.py` | `262707485e25d26e0b2613eddf4967a39b18bcdf652b0be29ca1f2a136e31a2c` | 579 |
| `tools/automacao/aut5/cenarios-rstv.json` | `efab1207bb9d12105b4824aab108e27dc5efa35935a42cc20c0515c9562ffedd` | 125 |
| `tools/automacao/aut5/test_aut5.py` | `99c40b3ea881f849fc2ff985fa2c414d0bb98e8339fa0a8abd2acc18d80e08d4` | 849 |
| `tools/automacao/aut5/fixtures/log-completo.log` | `5e9672bc36de71b8e8d3355d0910db6fb57c4d7b43daa97c0a11304fbe993dd2` | 33 |
| `tools/automacao/aut5/test_snapshot_modal.py` | `054aecb14eb53700d3f0aa28d9b51e221c82e4f93a972d5a36f15bafcb4c3e96` | 129 (**intocado**) |

Log do dono lido (somente leitura, 1.234.333 B, 05/10 14:32):
`8652cd5833a367c0137e4cca076eaeda6f138e32188aa77a54e1b9588aaef85e`.
DLL do perfil == DLL do repo: `454587a031a3e89104ec8535cf4c6328e2a527238138a136adcc773c5617a948`.

## 2. A-1 (ALTO) — motivo do `mira-skill` truncado no plano vs literal do produto

**Reproduzido antes do conserto** (`repro_achados.py`, controle E1 do parecer): log com a
recusa real de `RunTargets.cs:231` → `AUT5-guards-motivo-fora-do-plano` = **REPROVADO**,
exit **1** — recusa legítima tratada como defeito, e a cena não contava como exercitada.

**Conserto, nos dois lados (o "ou" do parecer virou "e", por robustez):**

1. **literal COMPLETO nas duas listas** — `cenarios-rstv.json` (`guards_run.itens`) e
   `log_rstv.GUARDAS` passaram a declarar
   `mira de skill ativa (HexCellManager.CurrentState=Action): abrir aqui cancelaria o apontar hex`,
   o texto que o produto realmente emite;
2. **normalização idêntica dos dois lados** — `log_rstv.chave_motivo()` (texto até o primeiro
   ` (`) é aplicada tanto ao motivo declarado quanto ao motivo lido do log, a **mesma**
   normalização que a checagem de fonte já usava. Comparar por igualdade exata era a assimetria.

**Guarda estática nova (causa-raiz):** `AUT5-guardas-run-fonte` agora exige que o **plano** e o
**registry** declarem a mesma guarda (mesmo `id` + mesma chave de motivo) e que nenhum motivo
normalizado apareça duas vezes no plano. É a detecção onde o desalinhamento nasce, não só no
confronto do log.

## 3. A-2 (ALTO) — `falha` do produto no log não reprovava nada

**Reproduzido antes do conserto** (`repro_achados.py`): a linha real
`RSTV: falha ao higienizar AcceptSkillChanges …` (`Patches.cs:189`, **sem hífen**) **nem era
capturada** (`falhas=[]`); a linha `RSTV-16: falha …` era capturada e ficava sem consumidor —
em ambos os casos o delta de estados era **ZERO** e `AUT5-travas-readonly` seguia **OK**
(controles E8/E9/E10 do parecer).

**Conserto (a) — regex tolerante.** O marcador `falha` de `log_rstv.MARCADORES` passou a casar:

* qualquer linha `[Error  :Roguelike Skill Tree Visualizer]` (todo `LogError` do mod —
  inclusive `RSTV: FALHA ao aplicar o gancho` e o resumo `… GANCHOS QUE FALHARAM:` de
  `Plugin.cs:260`, que não têm a palavra "falha" na forma exigida antes);
* `RSTV-?[0-9a-zA-Z]*:\s*falha|FALHA` (com **ou sem** hífen, qualquer nível de log) — cobre os
  ~20 `LogError` do produto e eventuais falhas registradas como warning.

**Conserto (b) — a falha passa a reprovar.** Critério novo `AUT5-falhas-produto-log`
(classe `offline`, procedência `execucao`, mod do produto): com **qualquer** falha do mod no
log → **REPROVADO**, exit **1**, e a decisão CIC-2 o roteia como **falha automática**
rastreável. O critério **só existe quando há o que reportar**: "log sem falha" **não** cria
critério novo (não se inventa OK nem se polui a contagem) — o vazio fica registrado em
`relatorio["falhas_produto"] = {total, linhas, criterio, regra}`, para a ausência ser auditável.

## 4. A-3 (MÉDIO) — a checagem das guardas era de presença, não de efeito

Reproduzido (E2 do parecer): com a guarda neutralizada na cópia da fonte
(`if (false && gui.PingModeActive)`) o critério continuava **OK**.

`log_rstv.guarda_ligada()` substituiu a busca por texto: para **cada** guarda o critério exige
o bloco `if (<condição EXATA>) { … motivo = "<texto>"; … return false; … }`
(`_RX_BLOCO_GUARDA` / `_RX_MOTIVO_NO_BLOCO`), com a condição que o produto realmente usa
(`gui.PingModeActive`, `wm != null && wm.AnyUIWindowOpen`,
`hcm != null && hcm.CurrentState == PlayerState.Action`, `root.SpawnPlacementActive`,
`!root.IsPlayerTurnAndReady`, `root.AnyActingCharactersInBattle`,
`root.AnyMovingCharactersInBattle`) — o `run_targets` é lido num único passe com regex sobre
a fonte real. Guarda neutralizada (`false &&`, `&& false`), motivo desligado da condição ou
bloco sem `return false` → **REPROVADO**, com `guardas_sem_bloco` dizendo **qual** guarda caiu.

## 5. A-8 (INFO) e A-4 (declarado) — o que não é confrontável fica DECLARADO, não silencioso

* o item `chat/texto` passa a declarar `"via": "RSTV-11"` e
  `"confrontavel_em_recusas": false`, com a observação de que o produto o registra como
  `RSTV-11: atalho F10 IGNORADO — <motivo>.` (`SkillTreeShortcut.cs:69`) e **nunca** como
  `RSTV-5: abertura RECUSADA`;
* `AUT5-guards-run-exercicio` passou a expor `guards_declaradas` (8),
  `guards_confrontaveis_em_recusas` (7), `guards_fora_desta_via` (`["chat/texto"]`) e
  `guards_exercitadas_no_log` — a contagem deixou de prometer 8 cenas exercitáveis por uma via
  que só cobre 7;
* **A-4 declarado (não consertado):** o marcador de S2
  `RSTV-16: o inventario nao abriu em 5 s` (`SkillTreesTab.cs:746`) continua sem critério e sem
  leitura dedicada — o leitor o registra honestamente como `nao-reconhecido:RSTV-16`. A suite
  agora **cobra** que ele siga assim (nunca virando OK fabricado) e que S2 continue declarando
  o marcador no plano. A-4/A-5 seguem backlog.

## 6. F-1 (MÉDIO, roteado da revisão da AUT5-F1) — probe no formato normalizado do coletor

`_obs_do_probe` prometia "cru ou normalizado", mas o trio do tooltip só era lido no formato
CRU: `rstv._cap_tooltip_restauracao` (`rstv.py:543-575`) usa `k in o`/`o.get(k)` direto,
enquanto as outras capacidades usam `_campo()`. Com o bloco `campos` do coletor
(`coletor.py:152-226`), `RSTV-21-tooltip-restauracao` ficava **NAO_EXERCITADO/tecnica** mesmo
com os campos **PRESENTES**.

Conserto em `aut5._achata_campos()`: a observação normalizada é achatada nas chaves planas com
a **mesma regra de `_campo()`** — `PRESENTE` vira chave plana com o seu valor,
`NAO_APLICAVEL` (objeto inativo) usa o `fallback` declarado, **AUSENTE não vira chave nenhuma**.
`rstv.py` (arquivo do CIC-3) **não** foi tocado.

## 7. Controles negativos plantados

**Na suite (`test_aut5.py`, 16 casos; era 10)** — três casos novos + dois ampliados:

| controle | o que exige |
|---|---|
| `positivo` (ampliado) | a fixture carrega as **3 recusas reais**, inclusive a do `mira-skill` com o sufixo completo: **nenhuma** pode cair em "fora do plano"; contagem 8 declaradas / 7 confrontáveis; as 3 exercitadas reconhecidas; **sem** falha no log **não** existe critério de falha (`falhas_produto.total == 0`) |
| `recusa-fora-do-plano` (novo) | motivo **não** declarado no plano → REPROVADO, exit 1, falha automática; e o motivo **legítimo** (literal completo do produto) → **não** reprova |
| `probe-normalizado` (novo) | observação do **coletor** com os campos do tooltip PRESENTE → OK (runtime); com o bloco sem eles → NAO_EXERCITADO, **nunca OK** |
| `falha-produto` (novo) | as **quatro** formas reais (`RSTV: falha` sem hífen, `RSTV-16: falha` com hífen, `RSTV: FALHA ao aplicar o gancho`, resumo `GANCHOS QUE FALHARAM`) → REPROVADO, exit 1, **falha automática**, `pronto_para_decisao=False`; log limpo → critério **não** existe |
| `guarda-ligada` (novo) | `false &&`, `&& false` e motivo removido do bloco → REPROVADO (com a guarda nomeada); fonte intacta → OK |
| `plano-divergente` (novo) | guarda com **outra** identidade, guarda **ausente** do plano e motivo normalizado **repetido** → REPROVADO; plano real → OK |
| `roteamento-guards` (novo) | `chat/texto` declara a via `RSTV-11` e não é confrontável; S2 mantém o marcador; o marcador de S2 continua `nao-reconhecido:RSTV-16` (nunca OK) |

A fixture ganhou a 3ª recusa (`mira-skill`, literal completo do produto) — é o controle
**positivo** que impede o retorno do falso `REPROVADO`.

**Controles de mutação** (`controles_mutacao_e_f2.py`) — reintroduz o defeito nos arquivos do
repo, roda a suite, **restaura byte a byte** (sha256 conferido no próprio script):

| id | mutação | esperado | obtido |
|---|---|---|---|
| E-F2-1 | plano **truncado** + confronto por **igualdade exata** (os dois lados revertidos) | REPROVOU | REPROVOU (`positivo: exit esperado 2, veio 1`) ✔ |
| E-F2-1b | plano truncado **com** o confronto normalizado | PASSOU | PASSOU (a tolerância segura sozinha) ✔ |
| E-F2-2 | `criterios_falhas_produto` volta a devolver `[]` | REPROVOU | REPROVOU (`falha 'sem-hifen' NAO reprovou`) ✔ |
| E-F2-3 | checagem das guardas volta a ser de presença | REPROVOU | REPROVOU (guarda 'turno do jogador') ✔ |
| E-F2-4 | `_achata_campos` desligado | REPROVOU | REPROVOU (tooltip PRESENTE não fecha) ✔ |
| — | `--contra-prova` com o defeito A-1 reintroduzido | REPROVOU | REPROVOU ✔ |

## 8. Resultado — suite, log real do dono e ambiente

```
python tools/automacao/aut5/test_aut5.py                 -> PASSOU     exit 0 (16 casos)
python tools/automacao/aut5/test_aut5.py --contra-prova  -> PASSOU     exit 0
python tools/automacao/aut5/aut5.py --texto --perfil <Default>
     -> 6 OK / 11 NAO_EXERCITADO  exit 2
        decisao: pronto_para_decisao=True · falhas_automaticas=0 · pendencias_humanas=2
        classe runtime OK: NENHUM (runtime_ok = [])
        falhas_produto.total = 0  (criterio AUT5-falhas-produto-log ausente — nao se inventa)
travas do repo: check_segredos / check_padroes_segredo / check_dupes / audita_docs = exit 0
suites vizinhas: CIC-3 test_rstv PASSOU · CIC-2 test_decisao "TUDO OK" · test_ciclo "OK"
```

Os **6 OK offline são exatamente os mesmos** de antes do conserto (`AUT5-obs-marcadores-fonte`,
`AUT5-guardas-run-fonte`, `AUT5-travas-readonly`, `AUT5-boot-rstv`, `AUT5-geometria-botao-run`,
`AUT5-geometria-botao-modal`); o único texto que mudou no relatório é o `motivo` do critério de
guardas (agora diz que exige o bloco ligado e o plano sem motivo truncado). Nenhum critério de
runtime foi promovido.

**Ambiente na janela da rodada:** **0** arquivos do perfil do dono com mtime na janela (BepInEx
inteiro varrido); nenhum processo do jogo (`tasklist`); nenhum commit, nenhum install, nenhum
publish.

`git status --porcelain` = **83** ao fim da rodada (era **82** na primeira medicao desta frente).
A entrada a mais **nao e desta tarefa**: e `?? docs/cobertura/auditoria-cobertura.md`, arquivo de
**03/10 21:15**, que nenhum script do repo escreve (o `audit_tooltips.py` escreve
`auditoria-tooltips.md`, outro arquivo) — o `??` apareceu porque a primeira chamada de
`git status` atualizou o cache de nao rastreados do indice. Nenhum arquivo desta frente entra
listado no status: `tools/automacao/` e `docs/automacao/` sao diretorios **nao rastreados** e
aparecem como **uma** entrada `?? ...` cada, antes e depois.

## 9. Limites desta rodada (o que NÃO foi provado)

* **Runtime não exercitado**: nenhuma sessão viva, nenhum PNG, nenhuma recusa de guarda em
  jogo. Nenhum critério de runtime foi aprovado; **esta rodada não fecha a AUT-5** e não
  substitui o aceite humano nem o DoD.
* **Âncoras anteriores não recuperáveis**: para os 4 arquivos que eu editei só ficou o `md5`
  do disco no início da rodada — o `sha256` do estado anterior (declarado pela AUT5-F1) não é
  reconferível depois da edição. O que **é** verificável confere: os arquivos intocados da
  frente e das frentes vizinhas batem byte a byte com as âncoras declaradas (§ 1).
* **A-4/A-5 continuam backlog**: S2/S3 seguem sem critério próprio e os flags de config /
  `RSTV DIAG` continuam não conferidos. Ficaram **declarados** (§ 5), não silenciosos.
* **L-1 (limite do contrato CIC-3/CIC-5)** segue de pé: `--probe` aprova runtime por
  autodeclaração de `sessao`/`hash_fonte`. Não é defeito desta entrega e não foi alterado.
* Textos `LACUNA_*` velhos em `rstv.py` (F-2 da revisão da AUT5-F1) são do CIC-3 e **não**
  foram tocados aqui.

## 10. Evidência bruta

`C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_9cee7d21\` —
`evidencia.json` / `resumo.txt` (hashes, resultado da suite, CLI no log real, travas,
suites vizinhas, ambiente), `evidencia_aut5f2.py` (script), `repro_achados.py` +
`baseline/repro-antes.txt` e `repro-depois.txt` (A-1/A-2 antes e depois),
`controles_mutacao_e_f2.py` + `controles-mutacao.txt` (os 5 controles de mutação),
`relatorio-log-real-aut5f2.json` e `log-real-depois.txt`.
