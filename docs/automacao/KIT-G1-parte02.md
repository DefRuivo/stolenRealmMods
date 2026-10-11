# KIT-G1 — Gate de autorização humana para a rodada mínima AUT-4 (parte 02)

> Cartão `t_49c93c37` · run 618 · 2026-10-09 18:22 BRT. Segue `KIT-G1-parte01.md`.
> Esta parte registra a **verificação de isolamento/rollback** exigida como pré-condição
> ("Isolamento/rollback revisados primeiro") e o **estado medido** no momento do gate.

## 1. Isolamento/rollback revisados PRIMEIRO — cadeia de revisão independente

| elo | cartão | veredito | prova |
|---|---|---|---|
| revisão do isolamento (KIT-03) | `t_9670452a` KIT-03R | REPROVADO (3 FALHOU: isolamento falso-verde, lock inoperante, runner morto) | execução offline com controle negativo |
| correção do isolamento | `t_160668bd` KIT-03F | **APROVADO** | revisor reproduziu por execução: runner 6/6 exit 0; controle negativo próprio 5/5; skip plantado ⇒ exit 1; `prove-isolation` legítimo exit 0 e negativo exit 1; 2º acquire recusado + `--force`; rollback exato; build isolado com `-p:DeployToBepInEx=false` |
| revisão do core/adapter (KIT-04) | `t_0451c587` KIT-04R | REPROVADO (build do Core exit 1; Adapter vazio) | build em cópia isolada |
| correção do core/adapter | `t_d5c98d36` KIT-04F | **APROVADO** | build independente exit 0 (Core 17408 B, Adapter 2 DLLs); 45/45 hashes conferidos; controle negativo 6/6; `Assembly-CSharp.dll` intacta |
| prova runtime ISOLADA em jogo | `t_09e856b1` KIT-03G1 | **APROVADO** (run 617) | `runtime-isolado.sh run` executado 2× com o jogo fechado: jogo abriu a partir da **cópia**, probe apareceu no `LogOutput` **da cópia**, perfil/saves do dono com hash idêntico, fechamento só do PID próprio, rollback exato |

Conclusão: o isolamento e o rollback estão **revisados e provados por execução** antes deste
gate — não é isolamento presumido.

## 2. O que é o "ambiente isolado" desta rodada (concreto)

- **Base do kit**: `scratch/kit/` (`KITS_DIR`). Script de prova: `scratch/kit/runtime-isolado.sh`.
- **Área isolada**: `scratch/kit/runtime-iso/BepInEx` — **cópia** de `core/` + `plugins/` +
  `config/` do perfil do dono. O jogo é lançado com
  `--doorstop-target-assembly .../runtime-iso/BepInEx/core/BepInEx.Preloader.dll`, isto é, o
  BepInEx carregado é **o da cópia**.
- **container/containment**: a área isolada tem de ficar **fora** de
  `...\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx` — o script recusa (fail-closed)
  se apontar para dentro do perfil do dono.
- **Log**: lê/escreve **somente** `runtime-iso/BepInEx/LogOutput.log` (o log do dono não é lido
  nem escrito).
- **Saves**: nenhum save é carregado; hash da árvore de saves medido antes/depois; drift ⇒
  veredito derrubado.
- **PID**: fecha **somente** o PID que a própria prova abriu (`CloseMainWindow`); nunca
  `taskkill /im` contra o processo do dono.
- **Totalidade das pontas medidas antes/depois** (KIT-03G1 §4): `core/` do dono, `plugins/` do
  dono, `LogOutput.log` do dono e árvore de saves — **idênticos** (hash `b1594200…`/`6eae7a3c…`/
  `9bedadac…`/`04ef12fa…`), com `find <perfil> -newermt <pós-sessão> -type f` VAZIO.

Rollback: `runtime-isolado.sh rollback` remove a área isolada exatamente e prova que o perfil e
os saves do dono não mudaram (KIT-03F, Teste 2/3 + caso negativo com hash divergente ⇒ exit 1).

## 3. Estado MEDIDO no momento deste gate (2026-10-09 18:22 BRT)

| item | medido |
|---|---|
| jogo do dono | **FECHADO** — nenhum processo `Stolen*` (`tasklist` vazio) ⇒ **não há necessidade de reinício declarado** |
| frente única | `front-unica.sh check` ⇒ **"lock disponivel"**, nenhuma outra frente controlando o jogo |
| área isolada residual | `scratch/kit/runtime-iso` **NÃO existe** (rollback do KIT-03G1 foi exato) |
| perfil do dono | **sem** `AUT4Probe` (busca `*AUT4*` em `plugins/` ⇒ vazia) |
| `lib/Assembly-CSharp.dll` (DLL do jogo) | `8bb4a7c5…` — **intacta** |

## 4. Identidade reconferida contra o disco (byte a byte, agora)

| artefato | esperado | medido | veredito |
|---|---|---|---|
| `AUT4Probe/AUT4ProbePlugin.cs` | `48afd3c4…` | `48afd3c4…` | OK |
| `AUT4Probe/bin/Release/AUT4Probe.dll` | `407c5c63…` | `407c5c63…` | OK |
| `AUT4Probe/AUT4Probe.csproj` | `347770d0…` | `347770d0…` | OK |
| `runtime/coletor.py` | `adb48dca…` | `adb48dca…` | OK |
| `lib/Assembly-CSharp.dll` | `8bb4a7c5…` | `8bb4a7c5…` | OK |

## 5. Proibições preservadas nesta execução

- Nada foi aberto/encerrado (o jogo **já estava fechado**, por decisão do dono, não minha).
- Nada foi instalado no perfil do dono, nenhum save carregado, nada publicado, nenhum `git add`.
- `Assembly-CSharp.dll`, Bard, gameplay e travas: **intocados**. Só arquivos novos em
  `docs/automacao/` (este par de partes e a entrega).

## 6. Frentes ainda NÃO exercitadas (declaradas, não são OK)

- A leitura **real** do objeto vivo pelo AUT4Probe, o PNG pela API do Unity, os owners Harmony
  vivos, a navegação por handler real, a ida-e-volta em jogo e o rollback **contra o perfil
  real** seguem **NÃO EXERCITADOS** — são exatamente o objeto da rodada que esta autorização
  libera, e serão exercitados sob o cartão **AUT-4 (`t_b8b9822e`)**, não aqui.
- Este gate **não** executa a rodada: marca a autorização (regra do próprio cartão:
  "Marcar somente esta autorização, não aceite/publicação").
