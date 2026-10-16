# KIT14G-SEG2-INV — parte01: fatos do board e correção de premissas

Tarefa t_ceda98dd; investigador default/run844. Coleta iniciada em 11/10/2026 às 14:54:13 UTC−03 (terminal). Esta parte é incremental; o fechamento e a matriz MUNDO DO DONO / MUNDO DO AGENTE estarão na parte final. Limites: investigação somente, sem jogo, montagem, deploy, rebuild ou edição de instrumento/perfil.

## 1. O bloqueio que realmente está registrado

Consulta `kanban_show(t_139f714f)` nesta rodada: status BLOCKED, pais t_0e656658 e t_c36c7082, **0 pais não satisfeitos**. Logo, o bloqueio atual não é espera por congelamento no grafo: é o estado needs_input deixado pela rodada de diagnóstico.

O evento blocked de 11/10 tem run_id=720, motivo explícito: instrumentação offline entregue, mas faltam três boots e o orçamento da sessão terminou. O evento seguinte timed_out declara **Iteration budget exhausted (90/90)**, não expiração dos 10.800 segundos de max_runtime. O run720 permanece registrado como blocked. Não há no histórico mostrado evento unblocked posterior ao término do preparo.

Distinção de autoria: **run714 é o A/B anterior do KIT-14G, não a implementação dos novos marcos**. O comentário de 02:13 em SEG2 identifica a implementação como run720. `docs/automacao/KIT-14G-parte08.md:3-5` descreve o A/B; `docs/automacao/KIT-14G-SEG2-parte01.md:3-6,120-139` declara entrega instrumental/offline e nenhum boot nessa rodada.

## 2. A premissa “reiniciar o congelamento” já envelheceu

`kanban_show(t_c36c7082)`: preparo KIT14G-SEG2-P DONE, com implementação run840 e revisão independente run842. O comentário em SEG2 de 14:36 registra fonte beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193 e DLL 7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee. A revisão aprovou o preparo às 14:48 (hora exata será calculada no fechamento).

Isso não comprova runtime. Será feita verificação própria de bytes e pré-flight antes de afirmar que o congelamento atual está íntegro. A receita histórica ecdcce13… / 95069e9c… consta em `KIT-14G-SEG2-parte01.md:98-106`; a nova receita está em `KIT-14G-SEG2-receita-congelada.md:5-8`. Sua linha 38 ainda chama o PROBE_SHA antigo de “atual”: contradição documental a verificar no arquivo executável.

## 3. CliqueFisico não significa clique humano

`KIT-14G-SEG2-parte01.md:31-52` define CliqueFisico como gate para o handler do probe. O script runtime continua invocando o handler; ele não produz input de mouse nem prova o clique do dono. O runbook `KIT-14G-SEG2-runbook-clique-fisico.md:16-24` pede Play → Roguelike → criação → um clique do dono em Accept.

O runbook apresenta inferências categóricas (“é do jogo”, “é clique cedo demais”) que ultrapassam a prova disponível: mesmo se o clique humano sobreviver, a mecânica exata do crash sintético ainda precisa de marcos e comparação controlada. Um crash físico precisa de Event Log da própria janela, configuração identificada e contexto equivalente; relato visual sozinho não estabelece assinatura.

## 4. Dependência circular operacional, ainda sem alterar o board

`kanban_show(t_a41dd22d)`: SEG1-RT TODO depende de SEG2 BLOCKED; seu filho KIT-14 t_a1f38855 depende de SEG1-RT. O `kanban_show(t_a1f38855)` foi preservado pelo runtime em `%USERPROFILE%/AppData/Local/hermes/cache/spillover/call_WufRp2AcLBd1OFYBCLFCF8bj.txt`; leitura por JSON confirmou 1 pai não satisfeito (SEG1-RT). Portanto, exigir que o cartão KIT-14 inteiro rode primeiro para destravar SEG2 cria uma espera circular operacional. O clique diagnóstico pode ser etapa supervisionada separada; os três boots sintéticos são outro caminho e a própria receita prevê fazê-los sem clique de sistema.

## 5. Estado da montagem: ainda não confirmado nesta parte

`scratch/kit/seg2-sessao-isolada.ps1:42-56` ordena snapshot, export PlayerPrefs, cópia, Move-Item do real e só então junction. Existirem snapshot/cópia não comprova que o junction foi criado. O suposto proprietário do handle e a exclusão de Steam/r2modman exigem leitura dos registros da tentativa; até essa leitura são INDETERMINADOS para esta investigação.

NAO_EXERCITADO nesta parte: novos boots, clique físico, montagem/desmontagem, reprodução de falha de rename, build ou correção. Não fazem parte do escopo permitido.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
