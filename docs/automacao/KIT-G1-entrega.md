# KIT-G1 — ENTREGA: registro da autorização humana para a rodada mínima AUT-4 (ambiente isolado)

> Cartão `t_49c93c37` · perfil `default` · run 618 · **2026-10-09 18:2x BRT** (Hora oficial do Brasil, UTC-03:00).
> Natureza: **GATE HUMANO**. Este documento **marca a autorização** — **não** é aceite da rodada,
> **não** é aprovação técnica e **não** é publicação do DoD.
> Partes que compõem a prova deste gate: `KIT-G1-parte01.md` (escopo/checklist/base normativa),
> `KIT-G1-parte02.md` (isolamento/rollback revisados + estado medido + hashes).

---

## 1. O que este cartão entrega

O registro formal da **autorização do dono** para a **rodada mínima do instrumento AUT-4 em
ambiente isolado**, com **perfil, build, ações e janela** declarados, precedido da verificação de
que **isolamento e rollback foram revisados primeiro**. Nada foi instalado, aberto, encerrado,
salvo ou publicado nesta execução.

## 2. Fonte da autorização (não inferida)

- **Fato**: mensagem do dono em **09/10/2026, ~18:2x**, conteúdo **"autorizo"**, vinculada ao
  pedido de decisão escalado pelas revisões AUT-4R3/AUT-4R4 e à pendência de gate deste cartão.
- **Registro**: thread deste cartão, comentário de 09/10/2026 18:19
  ("AUTORIZADO PELO DONO em 09/10/2026 18:2x (mensagem 'autorizo')…") seguido do `UNBLOCK`
  pelo mesmo motivo (18:19).
- **Regra respeitada**: a autorização **não** foi preenchida por inferência; o pedido de **criar
  tarefas** (comentário do dono em `t_b8b9822e`, 07/10) **não** foi usado como consentimento.
  Este documento **não amplia** o que o dono escreveu.

## 3. Escopo AUTORIZADO (exatamente o do cartão)

| # | item | conteúdo autorizado |
|---|---|---|
| A1 | **Perfil** | Perfil **ISOLADO** (área `scratch/kit/runtime-iso/BepInEx`, cópia de `core/`+`plugins/`+`config/`), **fora** do perfil pessoal do dono (`r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx`). O perfil do dono é **preservado**. |
| A2 | **Build** | O **probe identificado** desta frente: `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll`, sha256 **`407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7`** (fonte `AUT4ProbePlugin.cs` `48afd3c4…`, projeto `AUT4Probe.csproj` `347770d0…`, driver `coletor.py` `adb48dca…`). Identidade = **hash declarado**, conferido antes de instalar; a DLL **não** é reproduzível byte a byte. |
| A3 | **Ações** | **instalar o probe identificado** na área isolada; **iniciar** a instância de **teste** do jogo; **encerrar** essa instância (**somente o PID próprio**, `CloseMainWindow`); **coletar UI** (leitura do objeto vivo, JSON e PNG pela API do Unity) — **somente leitura**. |
| A4 | **Janela** | A **sessão de teste desta frente**, em **09/10/2026**, com o **jogo do dono FECHADO** e **uma única frente** controlando o jogo. Teto técnico por rodada: `OrcamentoSegundos` (default **120 s**) e o `--timeout` do driver; encerramento imediato ao fim da coleta. |

> **A4 é interpretação limitada do executor**: o dono **não** nomeou uma janela em relógio. O que
> está declarado acima é o **limite mínimo** que a própria autorização implica (instância de
> **teste**, jogo fechado, frente única, ambiente isolado). Se o dono pretendia outra janela, esta
> linha precisa ser corrigida — está aqui destacada para o revisor poder refutar.

## 4. Escopo NÃO autorizado (preservado como proibição)

- **Save**: carregar save **não** está autorizado (a rodada vai só até o boot/menu).
- **Navegação**: navegar por UI **não** está autorizado.
- **Publicação**: nada é publicado; **aceite humano** e **DoD** são passos separados.
- **Perfil do dono**: nada é instalado, movido ou apagado no perfil pessoal; a DLL do dono não é tocada.
- **Jogo do dono aberto**: se estiver aberto, **preservar a sessão** e **declarar reinício** em vez de
  interferir (**sem hot-reload** presumido).
- **Produto**: `Assembly-CSharp.dll`, Bard/música, gameplay e travas — **intocados**.
- **Dependências**: Core/Adapter do kit são **ferramentas**, nunca dependência obrigatória dos mods.

## 5. "Isolamento/rollback revisados primeiro" — satisfeito

Cadeia de revisão **independente**, concluída **antes** deste gate (detalhe e provas em
`KIT-G1-parte02.md` §1):

- **KIT-03** → revisado (`t_9670452a`, REPROVADO) → **corrigido e aprovado** (`t_160668bd` KIT-03F).
- **KIT-04** → revisado (`t_0451c587`, REPROVADO) → **corrigido e aprovado** (`t_d5c98d36` KIT-04F).
- **Prova runtime isolada em jogo** já exercitada e aprovada em `t_09e856b1` (KIT-03G1, run 617):
  jogo lançado a partir da **cópia**, probe no `LogOutput` **da cópia**, perfil/saves do dono
  **bit-a-bit idênticos**, fechamento só do PID próprio, rollback exato.

Dependências lógicas do cartão (**KIT-03R**, **KIT-04R**) estão `completed`; `unsatisfied_parents`
do cartão: **vazio**.

## 6. Estado medido no momento do gate (18:22 BRT)

| item | medido | consequência |
|---|---|---|
| jogo do dono | **FECHADO** (nenhum `Stolen*` em `tasklist`) | **não** é necessário declarar reinício |
| frente única | `front-unica.sh check` → "lock disponivel" | nenhuma outra frente controla o jogo |
| área isolada residual | `scratch/kit/runtime-iso` **não existe** | rollback anterior foi exato |
| perfil do dono | sem `AUT4Probe` | produto limpo |
| `lib/Assembly-CSharp.dll` | `8bb4a7c5…` | **intacta** |

## 7. Veredito do GATE

**AUTORIZADO** — o dono autorizou a rodada mínima isolada com perfil (A1), build (A2), ações (A3) e
janela (A4) declarados, e isolamento/rollback foram revisados primeiro (§5).

**O que este veredito NÃO é:**

- **não** é `ACEITO` da rodada — a rodada ainda **não foi executada** (runtime **NÃO EXERCITADO**
  no nível do instrumento AUT-4);
- **não** é aprovação técnica de nenhuma entrega;
- **não** é publicação do DoD.

## 8. O que a rodada (cartão AUT-4, `t_b8b9822e`) deve respeitar ao ser executada

1. Rodar **com o jogo fechado** e **uma única frente** (gate G4).
2. Instalar a build de **hash conferido** (§3/A2) na área **isolada** (gate G5/G7).
3. **Somente leitura**: sem save, sem navegação, sem combate (gate G8).
4. **Encerrar** em duas etapas (gracioso → forçado **por PID**, nunca `taskkill /im`).
5. **Rollback exato** e `restauracao.limpo == true`; resíduo ⇒ perfil sujo declarado.
6. Evidência válida só com **sessão da rodada**, JSON mais novo que o lançamento, log com
   chainloader + linha de vida do probe e `prints` com `bytes > 0`.
7. `AUSENTE`/`NAO_EXERCITADO`/`INDETERMINADO` **nunca** são OK; `dados_sinteticos=false` e
   `hot_reload=false` sempre.

## 9. Lacunas declaradas (não são OK)

- A **janela em relógio** não foi nomeada pelo dono — registrada em §3/A4 como limite mínimo
  implícito (ponto explícito para refutação).
- **Leitura viva, PNG em jogo, owners Harmony vivos, navegação por handler real, ida-e-volta e
  rollback contra o perfil real**: **NÃO EXERCITADOS** — objeto da rodada que esta autorização
  libera; a rodada **não** foi executada por este gate.
- **Ordem de carga** entre plugins BepInEx (Core/Adapter) em runtime: sem prova offline (herdado
  do KIT-04F).

## 10. Rastreabilidade e hashes desta entrega

- `docs/automacao/KIT-G1-parte01.md`, `docs/automacao/KIT-G1-parte02.md`, este
  `docs/automacao/KIT-G1-entrega.md` (arquivos **novos**; nenhum arquivo de produto, mod, perfil,
  `KANBAN` ou de outro ciclo foi editado).
- Handoffs dos pais: `t_9670452a` (KIT-03R), `t_160668bd` (KIT-03F), `t_0451c587` (KIT-04R),
  `t_d5c98d36` (KIT-04F).
- Instrumento e runbook: `docs/automacao/AUT-4-runbook-rodada-autorizada.md`,
  `docs/automacao/AUT-4-preparacao.md`, `tools/automacao/runtime/**`,
  `scratch/kit/runtime-isolado.sh`.
- Nada publicado, instalado no perfil do dono, aberto/encerrado ou commitado nesta execução
  (nenhum `git add`).
