# AUT-5R — revisão independente da AUT-5 (`t_76a41ea7`)

Revisor **não-autor** (nenhuma linha de `tools/automacao/aut5/**` nem de `docs/automacao/AUT-5-relatorio.md`
foi escrita por mim). Escopo: a entrega da AUT-5 — leitor `log_rstv.py`, condutor `aut5.py`, plano
`cenarios-rstv.json`, suíte `test_aut5.py`, fixture `fixtures/log-completo.log` e o relatório — confrontada
com o **produto** (`RoguelikeSkillTreeVisualizer`) e com o log real do dono.

**Nada de jogo, save, probe, install, build com deploy, commit, push ou publicação.** O perfil do dono foi
lido **por hash** (DLL, `.cfg`, `LogOutput.log`) — nenhum byte escrito nele. O produto **não foi editado**;
os defeitos foram plantados em **cópias** (tempdir). HEAD `f526fe9`,
`git status --porcelain` = **82** (antes e depois). O único arquivo novo no repo é **este** `.md`.

Método: execução real do CLI e da suíte (não leitura), com controles negativos **próprios** (E1–E11), escritos
sem reaproveitar os da AUT-5 nem os de outras revisões. Evidência bruta:
`C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_a6bb7f27\` — `evidencia_aut5r.py` (script),
`evidencia.json`, `resumo.txt`, `relatorio-log-real.json`, `relatorio-fixture.json`,
`relatorio-log-real-pos-AUT5F1.json`.

## 1. Âncora: hashes do que foi revisado e do que foi lido

Todos os hashes declarados pela AUT-5 foram **reconferidos por mim, byte a byte**, e conferem:

| item | sha256 | declaração da AUT-5 |
|---|---|---|
| `tools/automacao/aut5/aut5.py` | `7a82331fcc099b8ad413a2697d2e1dd3f6794aad678d748f8dd459dc9614e7f4` | ✔ |
| `tools/automacao/aut5/log_rstv.py` | `5586ac86330ab7293b789ec3b275f023a86b3d64bdc89ce1ce0a9cd9126a091c` | ✔ (mudou depois — § 7) |
| `tools/automacao/aut5/cenarios-rstv.json` | `b2dd7e04a134d07b9074895d7b6ab3042114ee95917842dabf2654b05377d667` | ✔ |
| `tools/automacao/aut5/test_aut5.py` | `61a29656f8e77029868e415129de69d71727afd34a8ec4dc6bf17697a931f12e` | ✔ |
| `fixtures/log-completo.log` | `6d83edfd1fbd732ebb5b6afb448fd6f9c2483f5785600162cf12e770d1948841` | ✔ |
| `fonte_sha` (14 fontes do RSTV, **recalculado por mim**) | `7774d11fab0017f9d27227ae8700a353203bdfd8d4d4c63a285f74fbab758612` | ✔ (mudou depois — § 7) |
| `dll_sha` (repo `bin/Release`) | `454587a031a3e89104ec8535cf4c6328e2a527238138a136adcc773c5617a948` | ✔ |
| DLL **do perfil do dono** (só leitura) | `454587a031a3e89104ec8535cf4c6328e2a527238138a136adcc773c5617a948` (**== repo**) | ✔ |
| `config_sha` (`com.gumatos.roguelikeskilltreevisualizer.cfg`) | `fa506b724f8af93cd071c2a662f3348072007b0ec06f73c056bc1e872f0233cc` | ✔ |
| `LogOutput.log` lido (1.234.333 B, 05/10 14:32) | `8652cd5833a367c0137e4cca076eaeda6f138e32188aa77a54e1b9588aaef85e` | ✔ |
| `cenarios/rstv.py` (CIC-3, só leitura) | `524f719757977436b843bdceb8337b10db4003cba9da64ff3fea788ef327d320` | ✔ |
| `ciclo/decisao.py` (CIC-2, só leitura) | `d6de959e73a090e43da2b5438a12ba1739d32be2bd9494c0fe9f0d84d9163933` | ✔ |

O `fonte_sha` foi **recalculado com o algoritmo reescrito por mim** (§ 4 do relatório da AUT-5), não chamando o
runner: bate exatamente. Os `*_sha` das frentes vizinhas **não foram editados** — os valores de hoje são os
mesmos que o relatório declarou ter lido, então a alegação "mudaram durante a rodada" não é verificável pelo
disco de agora (registrado como limite, não como reprovação).

## 2. Reprodução dos números (execução real)

```
python tools/automacao/aut5/test_aut5.py                 -> PASSOU  exit 0   (7 casos)
python tools/automacao/aut5/test_aut5.py --contra-prova  -> PASSOU  exit 0   (isca 'sempre OK' nao passa)
python tools/automacao/aut5/aut5.py --texto (log do dono)-> 6 OK / 11 NAO_EXERCITADO  exit 2
   decisao: pronto_para_decisao=False · falhas_automaticas=5 · pendencias_humanas=2 · ok_vinculantes=6
   falhas automaticas = AUT5-RSTV-25b-conectores-log, RSTV-6-readonly-skills-pontos,
                        RSTV-21-tooltip-restauracao, RSTV-25b-dependencia, RSTV-geometria-clipping
   roteiro humano     = [autorizacao: 5 criterios] + [julgamento_visual: AUT5-aceite-visual-design]
python tools/automacao/aut5/aut5.py --log fixture/...    -> 6 OK / 4 INDETERMINADO / 7 NAO_EXERCITADO
travas do repo: check_segredos / check_padroes_segredo / check_dupes / audita_docs = exit 0
```

Bate **exatamente** com o § 3 e o § 4 do relatório (contagens, exit, listas da decisão e agrupamento do
roteiro humano). Reproduzi também a "prova mostrada reprovando": neutralizando a checagem de conector
**numa cópia** do condutor e plantando `0 linha(s)` com 4 nós com Dependency, sai `INDETERMINADO/exit 2`
(E11) contra `REPROVADO/exit 1` (E3) — a reprovação vem da **regra**, não de passe livre.

## 3. Veredito por item (17 critérios)

Legenda: **OK** = a alegação se sustenta, com prova minha; **NÃO-OK** = o estado declarado (não aprovado)
está correto para a rodada; **ACHADO** = defeito/limite encontrado (numeração em § 4).

| # | critério (estado declarado) | meu veredito | prova / observação |
|---|---|---|---|
| 1 | `AUT5-obs-marcadores-fonte` OK | **OK** | os 9 marcadores exigidos existem na árvore (7 dos 13 `.cs`); recalculado sobre a árvore atual: **nenhum** faltando; controle da suíte (marcador renomeado em cópia) → REPROVADO |
| 2 | `AUT5-guardas-run-fonte` OK | **OK (afirmação "existem") + ACHADO A-3** | os 7 motivos literais estão em `RunTargets.cs` (l.203–257), **cada um dentro de um `if` real**, + `catch (Exception` (l.264) com lado seguro; E2: guardas neutralizadas (`if (false && …)`) → **continua OK** |
| 3 | `AUT5-travas-readonly` OK | **OK (afirmação declarada) + ACHADO A-2** | os 2 patches estão em `Patches.cs` e os 2 nomes aparecem na lista de ganchos do boot (15 ganchos, conferido no log); E9/E10: `falha` real do próprio gate no log → **nada muda** |
| 4 | `AUT5-boot-rstv` OK | **OK** | log `0.3.2` == `<Version>` da fonte; DLL do log (perfil) **==** DLL do repo (sha meu); E5 (`0.3.1`) → REPROVADO; E4 (perfil com DLL divergente) → INDETERMINADO (a porteira de identidade funciona nos dois sentidos) |
| 5 | `AUT5-geometria-botao-run` OK | **OK** | log real l.3224: `24.2x24.2 px … largura da linha 88.6 -> 88.6 px`; E: `88.6 -> 120.4` → REPROVADO. Nota: a prova é o **texto do próprio mod** |
| 6 | `AUT5-geometria-botao-modal` OK | **OK** | log real l.3215: `(44x44 px, canto superior direito de 'Panel' …)`; E6 (sem "canto superior direito") → REPROVADO. Mesma nota do item 5 |
| 7 | `AUT5-RSTV-25b-conectores-log` NÃO_EXERCITADO | **NÃO-OK correto** | a janela não foi aberta na sessão (sem `RSTV-24b`/`RSTV-25`); E3 → REPROVADO, E11 → volta a não reprovar = a regra é que reprova |
| 8 | `AUT5-geometria-arvore-log` NÃO_EXERCITADO | **NÃO-OK correto** | sem `RSTV-24a`/`RSTV-23i` no log (lista `marcadores_ausentes` do meu JSON); roteado ao dono |
| 9 | `RSTV-6-readonly-personagem` NÃO_EXERCITADO (runtime) | **NÃO-OK correto** | nenhuma leitura de personagem no log **e** o alvo é do cenário (nunca do próprio log) — o relatório declara isso no § 8.1 |
| 10 | `RSTV-6-readonly-skills-pontos` NÃO_EXERCITADO | **NÃO-OK correto** | nenhum instrumento emite snapshot antes/depois (campo ausente → nunca OK) |
| 11 | `RSTV-21-janela-ciclo` NÃO_EXERCITADO | **NÃO-OK correto** | mesmo com o ciclo presente **na fixture** o critério sai NÃO_EXERCITADO ("runtime sem sessão/hash_fonte") = fixture não aprova runtime; E7 mostra que só um **probe** autodeclarado promove (limite L-1) |
| 12 | `RSTV-21-tooltip-restauracao` NÃO_EXERCITADO | **NÃO-OK correto** | pai/índice não são emitidos por ninguém |
| 13 | `RSTV-26-placeholders` NÃO_EXERCITADO | **NÃO-OK correto** | texto renderizado do hover só existe com o jogo aberto (não houve PNG) |
| 14 | `RSTV-25b-dependencia` NÃO_EXERCITADO | **NÃO-OK correto** | `RSTV-24b` da sessão só dá o total; sem linhas por tier, INDETERMINADO/NÃO_EXERCITADO (AUT5-F1 trata) |
| 15 | `RSTV-geometria-clipping` NÃO_EXERCITADO | **NÃO-OK correto** | `geometria.tela` por observação não existe no probe/coletor |
| 16 | `AUT5-guards-run-exercicio` NÃO_EXERCITADO | **NÃO-OK correto** | o log real **não tem nenhuma recusa**; ausência de recusa não prova cena — o relatório diz isso no § 7 |
| 17 | `AUT5-aceite-visual-design` NÃO_EXERCITADO | **NÃO-OK correto** | DoD item 4: exige olho humano sobre PNG; nenhum PNG nesta rodada |

**Nenhum critério de classe `runtime` saiu OK** (conferido em código e em execução: `rstv._fecha` só fecha OK com
`procedencia=runtime` + `sessao` + `hash_fonte` + identidade, e o leitor do log **nunca** emite `procedencia`
runtime). Nenhum OK veio de `AUSENTE`. Os 6 OK são todos de classe offline, ancorados em bytes de disco.

## 4. Controles negativos independentes (cópias / logs plantados; CLI real)

| id | o que plantei | resultado literal |
|---|---|---|
| **E1** | recusa com o **literal real** de `RunTargets.cs:231` (mira-skill), na fixture | `AUT5-guards-motivo-fora-do-plano` = **REPROVADO**, exit **1** — **defeito falso** (A-1) |
| **E2** | 2 guardas **neutralizadas** na cópia da fonte (`if (false && …)`), literal mantido | `AUT5-guardas-run-fonte` = **OK** (A-3) |
| **E3** | `4 linha(s)` → `0 linha(s)` (conector ausente) | `AUT5-RSTV-25b-conectores-log` = **REPROVADO**, exit 1 ✔ |
| **E4** | perfil falso com a DLL alterada em 1 byte | `AUT5-boot-rstv` = **INDETERMINADO**, `dll_perfil_igual_repo=false` ✔ |
| **E5** | log `0.3.1` | `AUT5-boot-rstv` = **REPROVADO**, exit 1 ✔ |
| **E6** | `canto superior direito de` → `em algum lugar de` no marcador do modal | `AUT5-geometria-botao-modal` = **REPROVADO**, exit 1 ✔ |
| **E7** | `aut4probe.json` **fabricado** (`procedencia=runtime`, `sessao="rodada-fabricada-1"`, `hash_fonte=dll_sha`) | `RSTV-21-janela-ciclo` = **OK** sem nenhuma rodada (limite L-1) |
| **E8** | linha real `RSTV-21: falha ao abrir a janela read-only: …` (`SkillTreesTab.cs:549`) | capturada em `leitura["falhas"]`, **delta de estados = NENHUM** (A-2) |
| **E9** | linha real `RSTV: falha ao higienizar AcceptSkillChanges — o original NAO vai rodar…` (`Patches.cs:189`) | **nem capturada** (`falhas=[]`) e **delta = NENHUM**; `AUT5-travas-readonly` segue **OK** (A-2) |
| **E10** | linha real `RSTV-16: falha no postfix de CharacterMenusManager.OpenWindow: …` (`Patches.cs:440`) | capturada, **delta = NENHUM**; `AUT5-travas-readonly` segue **OK** (A-2) |
| **E11** | checagem `conector_ausente` neutralizada numa **cópia do condutor** + E3 | deixa de reprovar (`INDETERMINADO`/exit 2) = a suíte reprova pela REGRA ✔ |

## 5. Achados

- **A-1 · ALTO · falso `REPROVADO` garantido na cena "mira de skill" da rodada autorizada.**
  `RunTargets.cs:231` emite o motivo **completo** — `mira de skill ativa (HexCellManager.CurrentState=Action):
  abrir aqui cancelaria o apontar hex` — enquanto `cenarios-rstv.json` (`guards_run.itens`) e
  `log_rstv.GUARDAS` declaram o motivo **truncado** (sem o sufixo `: abrir aqui cancelaria o apontar hex`).
  `aut5.criterios_guards` compara o motivo lido do log com o declarado por **igualdade exata**: a recusa
  legítima entra em "fora do plano" → `AUT5-guards-motivo-fora-do-plano` = REPROVADO, exit 1, e a cena **não
  conta** como exercitada em `AUT5-guards-run-exercicio`. Prova: E1 (três estados do leitor: `5586ac86`,
  `80e2ac02`, `b1c1556c` — a assimetria mora no **plano**, que não mudou, e no **produto**). Assimetria de
  critério: a checagem de fonte tolera o sufixo (`motivo.split(" (")[0]`), a do log não.
  **Conserto**: usar o literal completo nas duas listas, ou normalizar os dois lados pelo mesmo prefixo.
- **A-2 · ALTO · `falha` do próprio mod no log não reprova nada — e a maioria nem entra na leitura.**
  O leitor coleta `RSTV-<n>: falha…` em `leitura["falhas"]`, mas **nenhum critério e nenhuma rota da decisão
  consome o campo** (fica só no JSON). Pior: o regex exige hífen (`RSTV-[0-9a-zA-Z]*: falha`), e a maioria dos
  ~20 `LogError` do produto é `RSTV: falha …` (sem hífen) — **não é nem capturada**. Provas E8/E9/E10: com o
  literal real de falha do gate de leitura-somente no log, o delta de estados é **zero** e
  `AUT5-travas-readonly` continua **OK**. É o padrão "trava que passa a proteger menos continua verde".
  **Conserto**: (a) regex tolerante a `RSTV:` sem hífen/captura de `LogError`; (b) transformar falha do produto
  em REPROVADO (ou, no mínimo, em falha automática rastreável) em vez de campo morto.
- **A-3 · MÉDIO · a checagem das guardas é de PRESENÇA de texto, não de efeito.**
  `criteria_instrumentacao` procura o prefixo do motivo no texto da fonte; E2 prova que a guarda pode estar
  neutralizada e o critério seguir **OK**. A frase declarada ("existem na fonte") é fiel — o problema é usar o
  critério como pré-aprovação do risco do RSTV-6. **Conserto sugerido**: exigir que cada motivo esteja ligado a
  um `if (<símbolo esperado>)`/`return` no mesmo bloco, ou exercitar `GateOk` por reflexão num teste offline.
- **A-4 · BAIXO · cobertura: o cenário S2 ("inventário fechado") não tem critério, e o marcador que ele declara
  não é lido.** O plano declara S2 com `RSTV-16: o inventario nao abriu em 5 s` (literal real em
  `SkillTreesTab.cs:746`), e o leitor não tem entrada para esse marcador — ele cai em `nao-reconhecido:RSTV-16`.
  Nada julga "a janela abriu **com o inventário fechado**": a única evidência é o texto que o próprio mod
  escreve (`… — sem depender do inventario`), que a automação não inspeciona. S3/S5 idem, cobertos só
  indiretamente. Efeito: uma sessão em que a janela abrisse **depois** do inventário abrir passaria igual.
- **A-5 · BAIXO · flags de configuração não são conferidos.** O relatório registra `config_sha` mas não lê
  `AtivarBotao`/`AtivarBotaoNaRun`/`AtivarBotaoNaRemocao`/`AtalhoSkillTree` (hoje **todos true**, conferido por
  mim no `.cfg`) nem a linha `RSTV DIAG` do log. Se um flag estivesse `false`, o critério de geometria sairia
  "marcador ausente → NÃO_EXERCITADO" e a automação **não** distinguiria "desligado por config" de "regressão".
- **A-6 · BAIXO · efeito colateral não declarado.** O § 10 diz que os únicos arquivos novos são os 5 + o
  relatório, mas a rodada também gravou `scratch/aut5/relatorio.json` (mtime 20:03:49, esquema
  `AUT5/relatorio/1`). Não é produto nem dependência — é só rastreabilidade do que a rodada escreveu fora do
  próprio diretório.
- **A-7 · INFORMATIVO · redação do handoff.** "nenhum OK proveniente de AUSENTE ou de log" é ambíguo: **4 dos 6
  OK vêm de log** (`AUT5-boot-rstv`, `AUT5-geometria-botao-run`, `AUT5-geometria-botao-modal` e a metade
  "aplicado no boot" de `AUT5-travas-readonly`). O que é exato é a afirmação do metadata
  (`classe_runtime_nunca_vem_de_log=true`) e o § 4 do relatório, que nomeia a prova de cada linha. Não canonizar
  a versão curta.
- **A-8 · INFORMATIVO · plano com 8 itens de guarda, 7 confrontáveis.** O item `chat/texto` ("atalho F10
  ignorado com campo de texto em foco") não pode aparecer em `recusas`: o produto loga
  `RSTV-11: atalho F10 IGNORADO — <motivo>` (`SkillTreeShortcut.cs:69`), não a forma
  `RSTV-5: abertura RECUSADA — …`. `AUT5-guards-run-exercicio` conta "declaradas no plano: 8" → uma cena que
  nunca será exercitada por essa via.
- **L-1 · LIMITE (não é defeito desta entrega) · `--probe` aprova runtime por autodeclaração.** E7: um JSON
  escrito à mão com `procedencia=runtime`, `sessao` e `hash_fonte = dll_sha` promove `RSTV-21-janela-ciclo` a
  **OK** ("leitura runtime completa com identidade suficiente"). É propriedade do contrato CIC-3/CIC-5, e o
  condutor só a expõe; **nesta rodada nenhum probe foi passado** e nenhum critério runtime foi aprovado. Quem
  rodar com probe precisa saber que o OK de runtime vale o que vale o `sessao`/`hash_fonte` autodeclarado.

## 6. Cobertura e restauração do ambiente

- **Cobertura dos critérios**: as 7 capacidades do plano têm critério (7/7) e os 17 critérios são contados e
  roteados (6 OK · 11 não-OK · 0 REPROVADO na rodada real; nenhum AUSENTE virou OK). Lacuna de cobertura: S2/S3
  sem critério próprio (A-4).
- **Restauração**: **0 de 51** arquivos do perfil (plugins+config+core) com mtime na janela da AUT-5
  (20:00–20:12) — e 0 na minha janela também; DLL e `.cfg` do perfil com sha idêntico ao declarado;
  `LogOutput.log` **truncado em 14:32** (anterior à rodada, não foi reescrito); `Player.log` idem;
  **nenhum processo** do jogo em execução (`tasklist`); nenhum probe/plugin novo na árvore de plugins
  (a pasta do RSTV é de 04/10 19:09); `git status` = 82 antes/depois; HEAD `f526fe9`.
- **Produto intocado pela rodada**: as 13 fontes `.cs` do mod não têm mtime entre 19:50 e 20:09 (a DLL de
  `bin/Release` é de 19:55, de frente anterior) e o `fonte_sha` que recalculei **bate** com o declarado.

## 7. Hotspot — a árvore se moveu durante a revisão (o que NÃO é desta entrega)

Durante a minha janela, **outra frente** (`AUT5-F1`, `t_dd95f8d9`, em execução paralela) escreveu na mesma
árvore que eu estava revisando:

| arquivo | mtime | efeito |
|---|---|---|
| `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs` | 20:14:10 | `fonte_sha` deixou de ser `7774d11f…` → hoje `051f0f58…` (+38/−5 linhas: linha "por tier" no `RSTV-24b`) |
| `tools/automacao/aut5/log_rstv.py` | 20:15:11 (e de novo depois) | `5586ac86…` → `80e2ac02…` → `b1c1556c…` (parse do `por tier`) |
| `tools/automacao/runtime/coletor.py` | na janela | `2f502e0d…` (declarado pela AUT-5) → `0518634e…` |

Consequências, declaradas para não canonizar nada errado: (a) os meus **2 critérios de fonte** foram verificados
para a árvore `7774d11f` e **reexecutados na árvore atual** (`051f0f58`) — continuam OK, nenhum marcador faltando;
(b) os critérios ancorados no **log/DLL** seguem válidos porque a DLL é byte-idêntica (`454587a0` — a árvore
mudou **depois** da rodada e não foi rebuildada: a fonte está à frente do `bin`); (c) o estado de
`log_rstv.py` **em edição agora** não é objeto desta revisão — o que revisei é o hash declarado, e o A-1 se
mantém nos três estados que vi. Reexecutada a suíte com o leitor **atual**: `PASSOU` + contra-prova `PASSOU`.
`hotspot: tools/automacao/aut5/log_rstv.py — AUT5-F1 edita o mesmo arquivo enquanto a revisão roda`.

**Snapshot do fim da minha janela (20:16:38)** — a frente paralela já havia reescrito **quatro** dos cinco
arquivos da entrega: `aut5.py 67f1dae4…`, `log_rstv.py b1c1556c…`, `cenarios-rstv.json 7b56e4fc…`,
`fixtures/log-completo.log bcbda70f…` (a fixture ganhou o `por tier`), `test_aut5.py 8ca3f273…`. Nesse estado a
suíte sai **REPROVOU** (`positivo: AUT5-RSTV-25b-conectores-log esperado INDETERMINADO, veio OK` e
`+ positivo: RSTV-2`): é o front **alheio no meio da edição**, não a entrega da AUT-5 — que foi medida com a
suíte **verde** nos bytes que ela declarou —, e quem julga isso é a revisão da AUT5-F1. O **A-1 continua de pé
nesse estado**: com o plano `7b56e4fc`, a recusa real do `mira-skill` segue saindo `REPROVADO` (exit 1).
Os vereditos desta revisão valem para os hashes da § 1; a árvore de agora é de outra frente.

## 8. Lacunas — o que esta revisão NÃO confirma

- **Runtime de jogo**: nada exercitado em sessão viva — sem ciclo de janela, sem PNG, sem snapshot de
  skills/pontos, sem recusa de guarda, sem tooltip renderizado. Os 11 critérios não aprovados continuam não
  aprovados; **esta revisão não promove nenhum deles**.
- **Aceite humano, UI/UX e DoD**: não avaliados. Não há publicação, não há versão nova, não há verificação do
  dono — nada disso muda com esta rodada.
- **O log do dono é de 05/10 14:32** e vale como prova de **boot/injeção/geometria da DLL atual**; não é a
  rodada desta tarefa (não tem `sessao`) e não prova comportamento de cena.
- **Valores de frentes vizinhas**: `rstv.py`/`decisao.py`/`coletor.py` são de outras tarefas; verifiquei apenas
  que os hashes de hoje batem com o que o relatório declarou ter lido. A alegação "mudaram durante a rodada"
  não é decidível pelo disco de agora.
- **Mudança de bytes invalida os vereditos**: os itens de fonte valem para `fonte_sha 7774d11f` (declarado) e
  foram reexecutados em `051f0f58`; um novo build/edição derruba a reexecução.

## 9. Veredito

**APROVADO COM ACHADOS no escopo que a entrega se propõe (offline).** As 6 aprovações offline são legítimas e
rastreáveis (identidade byte a byte, nenhuma veio de AUSENTE, nenhuma classe `runtime` promovida); os 11
critérios não aprovados estão corretamente não aprovados; a decisão CIC-2 foi reproduzida linha a linha
(`pronto_para_decisao=False`, 5 falhas automáticas = fila de agente, 2 pendências humanas); o ambiente do dono
está intacto e o produto não foi editado.

Dois achados precisam ser corrigidos **antes** da rodada runtime autorizada, senão a rodada sai contaminada:
**A-1** (falso REPROVADO na cena "mira de skill") e **A-2** (falha do próprio mod no log não reprova — inclusive
a do gate de leitura-somente). A-3..A-8 são de robustez/rastreabilidade e não bloqueiam a rodada.

Esta revisão **não** fecha a AUT-5, **não** aprova runtime, **não** substitui o aceite humano e **não** publica.
