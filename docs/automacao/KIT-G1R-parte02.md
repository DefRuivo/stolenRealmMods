# KIT-G1R — revisão independente do gate KIT-G1 (parte 02: veredito por item)

> Segue `KIT-G1R-parte01.md`. Veredito da **rodada 1** (lente ARTEFATO + conferência por
> execução). Critérios do cartão `t_49c93c37`, um por um. Nenhuma edição de implementação.

## 1. Verdicto por item do aceite

| # | item do aceite | veredito | base |
|---|---|---|---|
| AC-1 | **Dono autoriza o PERFIL** da rodada | **OK** | Escopo autorizado = perfil **isolado** (`scratch/kit/runtime-iso/BepInEx`), fora do perfil pessoal. Coerente com o corpo do cartão ("ambiente isolado") e com a autorização registrada; não amplia nada. Verifiquei o perfil do dono **sem** `AUT4Probe` (parte 01/E6). |
| AC-2 | **Dono autoriza a BUILD** | **OK** | Identidade = hash **declarado** (`AUT4Probe.dll 407c5c63…`, fonte `48afd3c4…`, csproj `347770d0…`, driver `adb48dca…`). Conferi os cinco hashes **byte a byte** contra o disco (parte 01/E2) — batem. A não-reprodutibilidade byte a byte da DLL está explicitada. |
| AC-3 | **Dono autoriza as AÇÕES** | **OK** | Ações declaradas = exatamente as do corpo do cartão: instalar o probe identificado, iniciar/encerrar a **instância de teste**, coletar UI **somente leitura**. Nada além; save e navegação listados como **não** autorizados. |
| AC-4 | **Dono autoriza a JANELA** | **CAVEAT LIMITADO — não é autorização do dono** | O dono **não** nomeou janela em relógio (o autor declara isso em §3/A4, §9 e no handoff). O que está registrado é o **teto operacional mínimo** (instância de teste, jogo fechado, frente única, `OrcamentoSegundos`=120 s, encerramento imediato). Confere com os gates do runbook (G1 exige autorização do dono para a rodada; G4 frente única; G8 somente leitura) — é **restrição**, não permissão nova. Registro isto como **A4 = interpretação declarada do executor, NÃO autorização do dono**; qualquer coisa acima de boot/menu somente leitura **não** está coberta por este gate. |
| AC-5 | **Isolamento/rollback revisados PRIMEIRO** | **OK** | Cadeia rastreada no board: KIT-03R reprovado → KIT-03F **aprovado** (run 611); KIT-04R reprovado → KIT-04F **aprovado** (run 615); prova runtime isolada em jogo do KIT-03G1 **aprovada** (run 617). Pais do cartão `completed`, `unsatisfied_parents` vazio (parte 01/E8). A ordem exigida foi respeitada de fato. |
| AC-6 | **Não preencher autorização por inferência; não usar "criar tarefas" como consentimento** | **OK com ressalva** | O comentário de *criar tarefas* (dono, `t_b8b9822e`, 07/10) é anterior e foi explicitamente **não** usado como consentimento. A fonte é a mensagem "autorizo" registrada no thread. **Ressalva:** A4 (AC-4) foi preenchido por interpretação — porém **declarado em três lugares** (§3 nota, §9, metadados `lacunas`) e **sem expandir** o escopo. Não é falso-verde nem inferência oculta. |
| AC-7 | **Jogo do dono aberto ⇒ preservar sessão e declarar reinício** | **OK** | Medido **FECHADO** na entrega e reconfirmado por mim agora (`tasklist`: nenhum `Stolen*`) ⇒ **não há reinício a declarar**. A regra está escrita como proibição (§4) e o evento do KIT-03G1 mostra que a frente respeitou isso quando o jogo **estava** aberto (bloqueou em vez de interferir). |
| AC-8 | **Marcar SOMENTE a autorização — não aceite/publicação** | **OK** | §1 e §7 dizem literalmente o que o veredito **não é** (não é `ACEITO` da rodada, não é aprovação técnica, não é publicação do DoD); metadados trazem `nao_e`. O runtime do AUT-4 segue declarado **NÃO EXERCITADO**. |
| AC-9 | **Nada instalado/aberto/encerrado/salvo/publicado/commitado** | **OK** | `find` pós-18:20 fora de `scratch/`+`docs/` = **vazio**; os 3 entregáveis são `??` untracked; nenhum `Stolen*`; perfil do dono sem `AUT4Probe`; `Assembly-CSharp.dll` `8bb4a7c5…` intacta (parte 01/E2–E7). |
| AC-10 | **Identidade dos arquivos vivos antes de editar; reuso de infraestrutura** | **OK** | Os 5 hashes de identidade conferem; o cartão reusa AUT-4Probe/runbook/`scratch/kit` e não duplica infraestrutura entregue. |

## 2. Achados (não bloqueantes)

- **F1 (caveat, ligado a AC-4/AC-6):** a linha A4 aparece sob o título **"Escopo AUTORIZADO"** e o
  campo `escopo_autorizado` dos metadados inclui a janela; a ressalva vive em §3/§9/`lacunas`.
  Risco: um leitor futuro (ou o próprio AUT-4) citar a janela como autorizada **pelo dono**.
  Correção sugerida (documental, sem depender de nova decisão): mover A4 para fora do bloco
  "autorizado" — rotular como *"teto declarado pelo executor; NÃO nomeado pelo dono"* — e deixar
  `escopo_autorizado` sem o campo de janela. **O dono pode fechar o item nomeando a janela em
  comentário no cartão.**
- **F2 (precisão de proveniência, §5):** "exercitada e aprovada em `t_09e856b1` (KIT-03G1, run 617)"
  — a **execução** em jogo foi a **run 616**; a **run 617** é a revisão que aprovou. Redação a
  corrigir para não atribuir execução à run de revisão.
- **F3 (informativo):** a fonte da autorização é um comentário **escrito pelo próprio worker**
  (`default`) no thread; não há artefato com autoria do dono no cartão. Recomendo citar a mensagem
  bruta do dono e onde ela foi recebida, para a auditoria não depender da paráfrase.

## 3. Refutações que tentei e NÃO se sustentam

- "A prova runtime isolada do KIT-03G1 foi só offline" → **refutado**: a run 616 registra duas
  rodadas `runtime-isolado.sh run` com jogo aberto a partir da **cópia** (log bruto preservado,
  `BepInEx 5.4.23.5` → `1 plugin to load` → `ReloadProbe v1 carregado.`), perfil do dono idêntico
  em 4 superfícies; a run 617 conferiu os hashes e o log bruto.
- "O gate liberou a rodada sem nunca ter exercitado nada" → **refutado**: a rodada isolada **já foi
  exercitada** no KIT-03G1; o que segue NÃO EXERCITADO é o **instrumento AUT-4** (leitura viva/PNG/
  owners/navegação/ida-e-volta/rollback contra o perfil real), que é o objeto do AUT-4.
- "Houve instalação no perfil do dono" → **refutado** (E6/E7).
- "Os artefatos citados não existem / hash não bate" → **refutado** (E1/E2/E5).

## 4. Veredito

**APROVADO**, com **um caveat limitado que não bloqueia o aceite**: **A4 (janela) não é
autorização do dono — é teto declarado pelo executor**, e assim deve ser lido pelo AUT-4 e por
quem auditar depois. O gate satisfaz o que o cartão pede de substância: a autorização do dono para
a rodada mínima **isolada e somente leitura** está registrada, isolamento/rollback foram revisados
**primeiro**, nada foi executado, e o documento é explícito sobre o que **não** é.

**O que este gate NÃO é** (mantido do entregável, e concordo): não é aceite da rodada, não é
aprovação técnica, não é publicação do DoD. O runtime do instrumento AUT-4 segue **NÃO EXERCITADO**.
