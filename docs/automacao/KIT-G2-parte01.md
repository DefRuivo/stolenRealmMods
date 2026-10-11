# KIT-G2 — parte01: registro do escopo autorizado e estado medido no gate

> Cartao `t_f19310d3` (KIT-G2) · perfil `default` · workspace `C:/dev/stolen-realm`.
> Natureza: **GATE HUMANO**. Este documento **registra a autorizacao do dono** e o
> pre-registro da rodada (acoes/cenarios, controle negativo, congelamento de artefatos).
> **Nao** e aceite da rodada, **nao** e aprovacao tecnica e **nao** e publicacao do DoD.
> O entregavel final e `docs/automacao/KIT-G2-entrega.md` (gravado uma unica vez, arquivo novo).

## 0. Objetivo do gate

Liberar (autorizacao humana) UMA rodada que qualifique, **em jogo**, pacote + monitor +
executor, em **ambiente isolado** e **escopo separado da sessao pessoal do dono** — antes
de KIT-14 executar runtime. Sem esta autorizacao explicita, KIT-14 nao executa runtime.

## 1. Fonte da autorizacao (fato, nao inferencia)

- Mensagem do dono em **09/10/2026 ~18:2x**, conteudo **"autorizo"**, registrada no
  comentario deste cartao (`default`, 09/10 18:19):
  "AUTORIZADO PELO DONO em 09/10/2026 18:2x (mensagem 'autorizo')...".
- A autorizacao ficou **represada** enquanto a dependencia logica **KIT-15R** estava
  aberta; foi **aplicada** (unblock) em **10/10/2026** apos KIT-15R fechar (10/10 03:47):
  comentario `default` de 10/10 12:18 ("UNBLOCK: ... agora APLICADA ...").
- A autorizacao vale **exatamente** para o escopo escrito neste cartao, **sem ampliacao**.
  O pedido do dono de **criar tarefas** (07/10) **nao** foi usado como consentimento.

## 2. Escopo AUTORIZADO (exatamente o do cartao)

| # | item | conteudo autorizado |
|---|---|---|
| B1 | **Build/pacote** | Construir e empacotar a build identificada da frente (pacote kit-rstv 0.1.0 do KIT-15F + probe AUT-4), com **hash conferido antes de instalar**, em **copia isolada**, sempre com `-p:DeployToBepInEx=false`. |
| B2 | **Perfil/save DESCARTavel** | Criar e usar um **perfil/save DESCARTavel**, em **area isolada** fora do perfil pessoal do dono (`%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx`). O perfil/save do dono e **preservado**. |
| B3 | **Observacao** | **Ler** o objeto vivo (tooltip/TMP_Text), PNG pela API do Unity, owners Harmony — **somente leitura**, com as 3 provas de execucao (sessao + log + prints posteriores ao lancamento). |
| B4 | **Navegacao** | **Navegar** a UI para chegar aos cenarios ativos desta rodada (avanco de KIT-G1, que so autorizava boot/menu sem navegacao). Handler real de UI; OCR/coordenada so fallback **declarado**. |
| B5 | **Encerramento** | **Encerrar a instancia CRIADA por esta rodada** — gracioso (`CloseMainWindow`) -> forcado **por PID** como fallback; nunca `taskkill /IM` cego. |
| B6 | **Janela** | A **sessao de teste desta frente**, com o **jogo do dono FECHADO** e **uma unica frente** controlando o jogo. Teto tecnico por rodada: `OrcamentoSegundos` (default **120 s**) + `--timeout` do driver; encerramento ao fim. |

> B6 e interpretacao limitada do executor, como no KIT-G1: o dono **nao** nomeou janela em
> relogio. O declarado e o **limite minimo** que a autorizacao implica (instancia de teste,
> jogo fechado, frente unica, ambiente isolado). Ponto explicito para refutacao.

## 3. Escopo NAO autorizado (preservado como proibicao)

- **Publicacao / distribuicao / aceite**: NADA e publicado; DoD e aceite humano sao passos
  separados (owner: KIT-G4). Aprovar tecnicamente != aceite humano.
- **Perfil/save do dono**: nada e instalado, movido ou apagado no perfil pessoal; a DLL do
  dono nao e tocada. save de producao fica intocado.
- **Jogo do dono aberto**: se estiver aberto, **preservar a sessao** e **declarar reinicio**
  em vez de interferir (**sem hot-reload** presumido).
- **Produto**: `lib/Assembly-CSharp.dll`, Bard/musica, gameplay e travas — **intocados**.
- **Dependencias**: Core/Adapter do kit sao **ferramentas**, nunca dependencia obrigatoria
  dos mods testados.
- **Configuracao/modelo/cron/prioridade dos mods**: nao mudar. Sem `git add -A`.
- **Segredo/DLL proprietaria do jogo**: nao publicar.

## 4. Estado medido no momento do gate (10/10/2026 BRT)

| item | medido | consequencia |
|---|---|---|
| jogo do dono | nenhum processo `Stolen*` | **FECHADO** — nao e necessario declarar reinicio |
| area isolada residual | `scratch/kit/runtime-iso` **nao existe** | rollback anterior foi exato |
| perfil do dono (plugins) | BetterCombatText, BetterFont, BetterStats, BetterTooltips, CapProbe, HybridSR-Roguelike_Scaling, RoguelikeClassesMod, RoguelikeDebugger, RoguelikeSkillTreeVisualizer, ScriptEngine — **sem `AUT4Probe`** | perfil do dono limpo do instrumento |
| `lib/Assembly-CSharp.dll` | sha256 `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` | **intacta** |
| frente unica | (a confirmar no fechamento deste gate — parte02) | nenhuma outra frente pode controlar o jogo |

## 5. O que a rodada DEVE respeitar (herdado do runbook AUT-4)

1. Rodar com o jogo fechado e frente unica; probe novo ⇒ **instalar + iniciar** (sem hot-reload).
2. Instalar a build de **hash conferido** na area isolada; perfil DESCARTavel.
3. Somente leitura + navegacao autorizada (B3/B4); sem combate.
4. Encerrar so o PID nascido nesta rodada (gracioso -> forcar por PID).
5. Rollback exato; `restauracao.limpo == true`; residuo ⇒ perfil sujo declarado.
6. Evidencia valida so com sessao da rodada + JSON posterior ao lancamento + LogOutput com
   chainloader e linha de vida do probe + prints com `bytes > 0` posteriores.
7. `AUSENTE`/`NAO_EXERCITADO`/`INDETERMINADO` nunca sao OK; `dados_sinteticos=false` e
   `hot_reload=false` sempre.

## 6. Itens a cobrir nas partes seguintes

- (p2) Inventario de artefatos/ferramentas a reusar + hashes congelados (pacote, probe, coletor, runner, cenarios).
- (p2) Acoes/cenarios ativos pre-registrados (lista, observado/esperado por cenario).
- (p2) Controle negativo e baseline (como o "nao" e provado), congelamento de artefatos.
- (p3) Limites de performance: origem dos numeros, o que existe e o que e lacuna.
- (entrega) Veredito do gate, lacunas declaradas, rastreabilidade e hashes desta entrega.
