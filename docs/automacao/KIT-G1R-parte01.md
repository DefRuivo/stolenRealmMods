# KIT-G1R — revisão independente do gate KIT-G1 (parte 01: orientação e execuções)

> Cartão revisado: `t_49c93c37` (KIT-G1, implementador run 618, handoff `review_requested`).
> Cartão de revisão: run 620 (perfil `default`, lane `review`), lente da **rodada 1 = ARTEFATO**
> (leitura fria antes do resumo do implementador, depois conferência por execução própria).
> Data: 2026-10-09 ~18:26 BRT. Repo `C:\dev\stolen-realm`.
> **Nenhum arquivo de implementação foi editado por mim** (separação de papéis). Nada de jogo,
> save, perfil do dono, instalação ou publicação foi tocado nesta revisão.

## 1. O que este cartão entregou (o que estou revisando)

Um **gate humano**: o registro da autorização do dono para a rodada mínima AUT-4 em ambiente
isolado, com perfil/build/ações/janela declarados. Entregáveis:
`docs/automacao/KIT-G1-entrega.md` + `KIT-G1-parte01.md` + `KIT-G1-parte02.md`.

## 2. Leitura a frio (antes do resumo)

Li os três documentos inteiros antes de usar o resumo do handoff. Impressão fria: o documento é
explícito sobre a **natureza** do que registra (não é aceite, não é aprovação técnica, não é
publicação), declara as proibições preservadas e — ponto importante — **destaca por conta própria**
que a janela (A4) **não foi nomeada pelo dono** e pede refutação do revisor. Não encontrei
afirmação de execução que o disco não sustente (§3 e §4 abaixo).

## 3. Execuções reais feitas por mim (exit real)

| # | execução | resultado |
|---|---|---|
| E1 | `sha256sum` dos **3 entregáveis** | `KIT-G1-entrega.md` `d302c3d80b536b94a96cdfa8a48137fee53cdd83566fd9a2efebb4e93c7fd092`; `KIT-G1-parte01.md` `138f9407477992a9149df446fe787f8d8c073a6692efc03b2cbd6a800095712a`; `KIT-G1-parte02.md` `d5622b98bb1fbaff80d87a6477069b7c82b951197fd694c4d2283e355fb5a015` — **idênticos** aos declarados no handoff |
| E2 | `sha256sum` das **identidades vivas** citadas | `AUT4ProbePlugin.cs` `48afd3c4…`, `AUT4Probe.dll` `407c5c63…`, `AUT4Probe.csproj` `347770d0…`, `coletor.py` `adb48dca…`, `lib/Assembly-CSharp.dll` `8bb4a7c5…` — **todos batem byte a byte** com o declarado |
| E3 | estado de processo (`tasklist`) | **nenhum** processo `Stolen*`/`BepInEx` ⇒ a declaração "jogo do dono FECHADO" é verdadeira no momento da revisão; **não há reinício a declarar** |
| E4 | `bash scratch/kit/front-unica.sh check` | `[2026-10-09 18:26:01] [default] Pode executar: lock disponivel` / `OK` / exit **0** ⇒ frente única livre, confere com a declaração |
| E5 | existência da área residual | `scratch/kit/runtime-iso` → **No such file or directory** ⇒ rollback anterior exato, área isolada limpa; `scratch/kit/runtime-isolado.sh` existe |
| E6 | perfil do dono | `find <perfil r2modman Default>/BepInEx -iname '*AUT4*'` → **vazio** ⇒ nada instalado no perfil pessoal |
| E7 | escopo (nada de produto tocado) | `find . -newermt '2026-10-09 18:20' -type f` **fora de `scratch/` e `docs/`** → **vazio**; os 3 entregáveis são `??` (untracked, arquivos novos) e têm mtime 18:21–18:22 |
| E8 | dependências do cartão | pais `t_9670452a` (KIT-03R), `t_160668bd` (KIT-03F), `t_0451c587` (KIT-04R), `t_d5c98d36` (KIT-04F) **todos `completed`**; `unsatisfied_parents` **vazio** |

Consequência de E1–E8: **nada foi instalado, aberto, encerrado, salvo, publicado ou commitado**
por esta rodada, e a identidade do instrumento citado é a do disco.

## 4. Verificações de contexto do board

- **Autorização registrada**: comentário do thread de 09/10 18:19 ("AUTORIZADO PELO DONO em
  09/10/2026 18:2x (mensagem 'autorizo')") + evento `unblocked` (18:19). O comentário de
  **criar tarefas** (dono, em `t_b8b9822e`, 07/10) é **anterior** e foi explicitamente **não**
  usado como consentimento — confere com a regra do cartão.
- **Isolamento/rollback revisados primeiro**: rastreei a cadeia — KIT-03R (reprovado) → KIT-03F
  (aprovado, run 611), KIT-04R (reprovado) → KIT-04F (aprovado, run 615) e a prova runtime
  isolada do KIT-03G1 (`t_09e856b1`, aprovada na run 617). As provas citadas existem nos
  handoffs dos pais e nos eventos do board.
- **Cadeia de liberação**: o filho `t_b8b9822e` (AUT-4) declara `unsatisfied_parents:
  [t_49c93c37]` — é **este** cartão que o libera. Portanto o veredito daqui tem efeito prático.

## 5. Ponto sob suspeita (declarado pelo próprio autor) — a JANELA (A4)

Dois pontos de precisão, que trato item a item na parte 02:

- **A4 não foi nomeado pelo dono.** O próprio entregável afirma isso (§3 nota, §9 lacuna 1) e o
  handoff pede refutação. Preciso decidir se isso cabe como caveat limitado ou como defeito.
- **Imprecisão de proveniência em §5**: o texto diz que a prova runtime isolada foi "exercitada e
  aprovada em `t_09e856b1` (KIT-03G1, **run 617**)". A **execução** em jogo está na **run 616**
  (run 614 bloqueou, 616 pediu review, 617 aprovou). O cartão está certo; o número da run
  identifica a **revisão**, não a execução — vale corrigir a redação para não confundir.

## 6. Segue na parte 02

Veredito por item do aceite, caveats limitados, o que AUT-4 pode e não pode herdar deste gate, e
o fechamento com caminhos/hashes.
