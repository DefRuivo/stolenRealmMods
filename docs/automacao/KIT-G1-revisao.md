# KIT-G1R — REVISÃO INDEPENDENTE do gate KIT-G1 (fechamento)

> Cartão revisado: **`t_49c93c37` — "KIT-G1: Autorizar rodada mínima AUT-4 em ambiente isolado"**
> (implementador: run 618, perfil `default`; handoff `review_requested`).
> Revisão: **run 620** (perfil `default`, lane `review`), **rodada 1**, lente **ARTEFATO**
> (leitura fria antes do resumo + conferência por execução própria).
> Data: 2026-10-09 ~18:30 BRT (UTC-03:00). Repo `C:\dev\stolen-realm`.
> Partes: `KIT-G1R-parte01.md` (execuções), `KIT-G1R-parte02.md` (veredito por item). Este arquivo é
> o fechamento — não repete as partes, consolida.

---

## 1. VEREDITO

**APROVADO** — com **um caveat limitado que não bloqueia o aceite**.

O gate registra corretamente a **autorização do dono** para a rodada mínima AUT-4 **em ambiente
isolado**, com perfil, build e ações **fundados** (perfil isolado; build por hash declarado;
ações = as do corpo do cartão), e com **isolamento/rollback revisados primeiro** (cadeia de
revisão independente concluída: KIT-03F e KIT-04F aprovados; prova runtime isolada em jogo
aprovada no KIT-03G1). Nada foi instalado, aberto, encerrado, salvo, publicado ou commitado —
verificado por mim no disco e no processo.

**Caveat limitado (AC-4 + AC-6):** a **JANELA (A4)** é **teto declarado pelo executor**, **NÃO**
autorização nomeada pelo dono. Está declarada como tal em §3/A4, §9 e nos metadados (`lacunas`),
não expande escopo (é restrição: instância de teste, jogo fechado, frente única, teto de 120 s,
encerramento imediato, somente leitura até boot/menu). Aprovo o aceite **com A4 lido assim** — e
isso vincula o AUT-4 (ver §4).

**O que este veredito NÃO é:** não é aceite da rodada (o runtime do instrumento AUT-4 segue **NÃO
EXERCITADO**), não é aprovação técnica de entrega e não é publicação do DoD.

## 2. O que executei para decidir (exit real; detalhe em `KIT-G1R-parte01.md` §3)

- `sha256sum` dos 3 entregáveis → **idênticos** aos declarados
  (`KIT-G1-entrega.md d302c3d8…`, `-parte01.md 138f9407…`, `-parte02.md d5622b98…`).
- `sha256sum` das identidades vivas → **batem byte a byte** (`AUT4ProbePlugin.cs 48afd3c4…`,
  `AUT4Probe.dll 407c5c63…`, `AUT4Probe.csproj 347770d0…`, `coletor.py adb48dca…`,
  `lib/Assembly-CSharp.dll 8bb4a7c5…`).
- `tasklist` → **nenhum** processo `Stolen*`/`BepInEx` (jogo fechado; sem reinício a declarar).
- `bash scratch/kit/front-unica.sh check` → "lock disponivel", **exit 0**.
- `scratch/kit/runtime-iso` → **ausente** (rollback anterior exato).
- perfil do dono (`r2modman Default`) → **0** ocorrências de `AUT4*`.
- escopo: `find . -newermt '2026-10-09 18:20'` fora de `scratch/`+`docs/` → **vazio**; os 3
  entregáveis são untracked (`??`).
- board: pais `t_9670452a`/`t_160668bd`/`t_0451c587`/`t_d5c98d36` `completed`;
  `unsatisfied_parents` do cartão **vazio**; o filho `t_b8b9822e` (AUT-4) tem este cartão como
  pai pendente (é a liberação que este veredito cumpre).

## 3. Achados registrados (não bloqueantes)

1. **F1 — A4 rotulado dentro do "escopo autorizado".** Correção documental sugerida: tirar a
   janela do bloco autorizado e do campo `escopo_autorizado`, mantendo-a como "teto do executor".
   **O dono pode fechar o item nomeando a janela em comentário.**
2. **F2 — imprecisão de proveniência (§5 do entregável):** a execução em jogo do KIT-03G1 é a
   **run 616**; a **run 617** é a revisão que aprovou. Ajustar a redação.
3. **F3 — informativo:** a fonte da autorização é comentário do próprio worker; recomendo citar a
   mensagem bruta do dono e onde foi recebida.

Nenhum dos três exige retorno ao implementador para eu manter o veredito: F1 está resolvido por
este parecer (o caveat vincula o AUT-4 e o registro daqui), F2/F3 são precisão documental.

## 4. Consequência para o AUT-4 (`t_b8b9822e`) — vinculante

1. Este gate libera a rodada **isolada, de teste, somente leitura** (instalar o probe identificado
   na **cópia**, iniciar/encerrar a **instância própria**, coletar UI). **Não** libera: save,
   navegação, combate, perfil do dono, publicação.
2. **A janela é teto, não permissão do dono.** O AUT-4 tem de registrar a janela **efetiva** da
   sua sessão (início/fim, PID, sessão/hashes) e **não** citar A4 como autorização do dono.
3. Se a rodada do AUT-4 precisar de algo além de boot/menu somente leitura (ou de salvar/carregar
   save), **isso exige autorização nova e explícita do dono** — não está coberto aqui.
4. Gates do runbook seguem valendo (G1–G8): frente única, hash conferido antes de instalar,
   `AUSENTE`/`NAO_EXERCITADO`/`INDETERMINADO` nunca são OK, sem hot-reload presumido.

## 5. Limites desta revisão (declarados)

- **Não** abri/encerrei jogo, **não** instalei nada, **não** carreguei save, **não** movi DLL do
  perfil do dono, **não** publiquei, **não** fiz `git add`/commit/stash.
- **Não** editei nenhum arquivo de implementação (separação de papéis): só criei
  `docs/automacao/KIT-G1R-*.md` e este arquivo.
- **Não** reexecutei a rodada runtime (fora do escopo do cartão e da minha alçada).
- A fonte da autorização do dono é o registro em comentário do thread; **não** há artefato com
  autoria do dono no cartão (F3). Se o dono pretendeu outra janela, este parecer é o ponto onde a
  correção entra.

## 6. Rastreabilidade (hashes desta revisão)

| artefato | sha256 |
|---|---|
| `docs/automacao/KIT-G1R-parte01.md` | `f14590f77f386f30e63a92066b27d88dc9eb5d76621bc2076a8cf598986a0df5` |
| `docs/automacao/KIT-G1R-parte02.md` | `5db06fd12781fadeb8a9d96a9ba8068f9fa8d8e2d53e5ef0031c9000f84397e2` |
| `docs/automacao/KIT-G1-revisao.md` (este) | re-derivar com `sha256sum` no disco |

Revisado a frio antes de usar o resumo do implementador; veredito por item em
`KIT-G1R-parte02.md` §1; refutações tentadas e não sustentadas em §3 da mesma parte.
