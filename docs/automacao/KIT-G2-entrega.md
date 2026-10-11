# KIT-G2 — ENTREGA: registro da autorizacao humana para a sessao MVP com cenarios ativos (ambiente limpo)

> Cartao `t_f19310d3` (KIT-G2) · perfil `default` · run 695 · **2026-10-10 12:2x BRT**
> (Hora oficial do Brasil, UTC-03:00).
> Natureza: **GATE HUMANO**. Este documento **marca a autorizacao** e o **pre-registro da
> rodada** — **nao** e aceite da rodada, **nao** e aprovacao tecnica e **nao** e publicacao do DoD.
> Partes que compoem a prova: `KIT-G2-parte01.md` (autorizacao/escopo/estado),
> `KIT-G2-parte02.md` (inventario, cenarios, controle negativo, congelamento),
> `KIT-G2-parte03.md` (limites de performance + provas de estado).

---

## 1. O que este cartao entrega

O registro formal da **autorizacao do dono** para uma rodada que qualifique, **em jogo**,
pacote + monitor + executor, com **perfil/save DESCARTavel** em **ambiente isolado** e
**separado da sessao pessoal** — precedida do pre-registro de acoes/cenarios, baseline/controle
negativo, limites de performance e congelamento de artefatos. Nada foi instalado, aberto,
encerrado, salvo ou publicado nesta execucao.

## 2. Fonte da autorizacao (nao inferida)

- Mensagem do dono em **09/10/2026 ~18:2x**, conteudo **"autorizo"**, registrada no comentario
  deste cartao (`default`, 09/10 18:19).
- Ficou **represada** enquanto a dependencia logica **KIT-15R** estava aberta e foi **aplicada**
  (unblock) em **10/10/2026** apos KIT-15R fechar (10/10 03:47) — comentario `default` 10/10 12:18.
- Padrao do KIT-G1 respeitado: a autorizacao **nao** foi preenchida por inferencia; o pedido de
  **criar tarefas** (07/10) **nao** foi usado como consentimento. Sem ampliacao do escopo.

## 3. Escopo AUTORIZADO (exatamente o do cartao)

| # | item | conteudo autorizado |
|---|---|---|
| B1 | **Build/pacote** | Construir/empacotar a build identificada (pacote kit-rstv 0.1.0 do KIT-15F + probe AUT-4), `hash conferido antes de instalar`, em copia isolada, sempre `-p:DeployToBepInEx=false`. |
| B2 | **Perfil/save DESCARTavel** | Perfil/save descartavel em area **isolada**, fora do perfil pessoal do dono; perfil/save do dono **preservado**. |
| B3 | **Observacao** | Ler o objeto vivo (tooltip/TMP_Text), PNG pela API do Unity, owners Harmony — **somente leitura**, com as 3 provas de execucao. |
| B4 | **Navegacao** | Navegar a UI para os cenarios ativos (avanco do KIT-G1, que so cobria boot/menu). Handler real; OCR/coordenada so fallback **declarado**. |
| B5 | **Encerramento** | Encerrar **a instancia criada por esta rodada**: gracioso (`CloseMainWindow`) -> forcado **por PID** como fallback; nunca `taskkill /IM`. |
| B6 | **Janela** | A sessao de teste desta frente, jogo do dono **FECHADO**, **frente unica**; teto `OrcamentoSegundos` (default 120 s) + `--timeout`. *(limite minimo implicito — ponto para refutacao)* |

## 4. Escopo NAO autorizado (preservado como proibicao)

Publicacao/distribuicao (KIT-G4) e aceite do DoD · perfil/save do dono · jogo do dono aberto
(preservar + declarar reinicio, sem hot-reload) · `Assembly-CSharp.dll`, Bard/musica, gameplay
e travas · Core/Adapter como dependencia obrigatoria · mudar configuracao/modelo/cron/prioridade
dos mods · `git add -A` · publicar DLL proprietaria ou segredo.

## 5. Estado medido no momento do gate (10/10/2026 ~12:26 BRT)

| item | medido | consequencia |
|---|---|---|
| jogo do dono | nenhum processo `Stolen*` | **FECHADO** — nao precisa declarar reinicio |
| frente unica | `front-unica.sh check` → "lock disponivel" (exit 0) | nenhuma outra frente controla o jogo |
| area isolada residual | `scratch/kit/runtime-iso` **nao existe** | rollback anterior exato |
| perfil do dono | 10 plugins, **sem `AUT4Probe`** | produto limpo do instrumento |
| `lib/Assembly-CSharp.dll` | sha256 `8bb4a7c5…b37855a` | **intacta** |

## 6. Protocolo pre-registrado (o que a rodada vai fazer)

- **Marco RSTV**: clique fisico -> janela -> conteudo/tooltip -> PNG -> relatorio -> marcar
  problema -> exportar.
- **Cenarios do Runner**: `RSTV-6-readonly-personagem`, `RSTV-6-readonly-skills-pontos`,
  `RSTV-21-janela-ciclo`, `RSTV-21-tooltip-restauracao`, `RSTV-26-placeholders`,
  `RSTV-25b-dependencia`, `RSTV-geometria-clipping` + criterios de `tooltips_shrines.py`.
- **Cenarios de coleta AUT-4** (runbook §4): C0–C7.
- **Baseline/controle negativo**: C0 isolado (`NAO_EXERCITADO`, `dados_sinteticos=false`);
  fixtures negativas rotuladas; detector `--detectar` deve dizer NO/AUSENTE/INCOMPLETO;
  perfil/saves do dono identicos por `medir-dono.sh`; medicao com e sem recorder.
- **Congelamento**: sha256 de probe/coletor/cenarios/DLL do jogo antes e depois; JSON com
  `Sessao` desta rodada + `HashFonte`; uma unica frente.
- **Limites de performance**: **LACUNA** — nao existe numero-limite acordado pelo dono em
  nenhum doc (todas as mencoes estao como NAO_EXERCITADO). Metodo de medicao registrado
  (KIT-G2-parte03 §1.1); declarar numero seria inventar. Ponto para o dono fixar antes da rodada.

## 7. Hashes congelados (identidade = hash declarado)

`AUT4Probe.dll` `72928ffa…` · `coletor.py` `159ff2aa…` · `cenarios/rstv.py` `f8d0aad1…` ·
`cenarios/tooltips_shrines.py` `65c0f3b2…` · `lib/Assembly-CSharp.dll` `8bb4a7c5…`
(fonte/componentes/driver conforme runbook AUT-4 §2).

## 8. Veredito do GATE

**AUTORIZADO** — o dono autorizou a sessao MVP isolada com perfil descartavel, observacao e
navegacao, e o pre-registro foi feito com isolamento/rollback/frente unica declarados.

**O que este veredito NAO e**: nao e `ACEITO` da rodada (a rodada ainda **nao foi executada** —
runtime **NAO_EXERCITADO**); nao e aprovacao tecnica; nao e publicacao do DoD (KIT-G4).

## 9. Prova de execucao do gate (comandos reais)

`date` = 2026-10-10 12:26:30 -0300 · `front-unica.sh check` = OK (exit 0) · `sha256sum` dos 5
artefatos = hashes do §7 · nenhum processo `Stolen*` · `runtime-iso` ausente · perfil do dono
sem `AUT4Probe`. Travas do repo: `check_segredos` exit 0, `check_padroes_segredo` exit 0,
`check_dupes` exit 0, `audita_docs` exit 0 (nenhuma inconsistencia).

## 10. Lacunas declaradas (nao sao OK)

- **Limites de performance**: sem numero acordado (LACUNA) — metodo registrado, limiar a fixar.
- **Janela em relogio**: nao nomeada pelo dono — registrada como limite minimo implicito (B6).
- Runtime em jogo (leitura viva, PNG em jogo, owners vivos, navegacao por handler real,
  ida-e-volta, rollback/encerramento em jogo): **NAO_EXERCITADOS** — objeto do KIT-14, que esta
  autorizacao **libera**, nao executa.
- Build/deploy C# e preflight de deploy: **NAO_EXERCITADO** nesta frente (gate de docs/estado).

## 11. Rastreabilidade e hashes desta entrega

- `docs/automacao/KIT-G2-parte01.md`, `KIT-G2-parte02.md`, `KIT-G2-parte03.md`, este
  `KIT-G2-entrega.md` (arquivos **novos**; nenhum arquivo de produto, mod, perfil, `KANBAN` ou
  de outro ciclo editado; sem `git add`/commit/push).
- Dependencia logica satisfeita: **KIT-15R** (done 10/10 03:47) e correcao **KIT-15F**
  (aprovada run691). Handoffs dos pais: `t_effde07f` (KIT-15R), `t_d83f3ef6` (KIT-15F).
- Instrumento/runbook reusados: `docs/automacao/AUT-4-runbook-rodada-autorizada.md`,
  `tools/automacao/runtime/**`, `tools/automacao/cenarios/**`, `scratch/kit/front-unica.sh`,
  `scratch/kit/medir-dono.sh`.
- Libera (ao fechar): **KIT-14** `t_a1f38855`.
