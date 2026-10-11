# KIT14G-SEG2-INV — parte04: entrega final, timeline e divisão de responsabilidades

Tarefa t_ceda98dd, investigação default/run844; 11/10/2026. **Veredito documental: investigação entregue; correção/runtime SEG2 NÃO concluídos.** Esta é a síntese final das partes01–03, que permanecem como checkpoints. Não equivale a aceite do SEG2/KIT-14 nem à aprovação desta investigação pelo revisor.

## 1. Resposta direta: o que houve

1. **Run714 mediu o gatilho, não corrigiu o crash.** Foram cinco boots A–E, além de oito do run712: o conjunto corrigido tem **13**, não “10” como o título histórico. A/B morreram com ntdll/c0000005/offset 0x4a612; C/D/E sobreviveram, mas não iniciaram uma run com clique físico. Evidência: `KIT-14G-run716/verification.json.ab_causa_do_encerramento`; recontagem independente de Event Log em `supplement-result.json.raw_ab_independent`: duas entradas na janela A/B, zero C/D/E. A causa mecânica permanece **INDETERMINADA**, conforme `KIT-14G-parte10.md:90-109`.
2. **Run720 instrumentou o diagnóstico offline, mas não rodou os três boots.** Entregou arquivo marcos-clique.log com Flush, trilha clique_eventos, gate CliqueFisico/estabilidade e modo SilencioAposClique; declarou suíte 16/16, contra-prova 33/33 e harnesses 10/5/21/14 OK. Fonte original e DLL foram medidas por run721 às 02:24. Não se confunde teste offline com comportamento em jogo. Evidência: `KIT-14G-SEG2-parte01.md:120-150`, comentário SEG2 de 02:13 e `KIT-14-entrega-run721.md:13-21`. Nesta investigação a suíte histórica não foi rerodada; o pré-flight de identidade foi executado separadamente.
3. **O motivo inicial de parada foi orçamento de iterações, não pane misteriosa nem limite de três horas.** SEG2 bloqueou às 02:13:43; timeout às 02:14:00 informa 90/90 iterações. O status atual continua BLOCKED/needs_input, mesmo com seus dois pais DONE. Concluir o preparo não gerou evento unblocked no SEG2; falta retomada operacional pelo operador, não nova implementação do preparo.
4. **Depois, outra frente alterou o mesmo instrumento e a receita ficou histórica.** INT-R1-C2-I1/t_a706b09c alterou o hook de Localize e o csproj e atualizou identidades gerais; sandbox e receita SEG2 ainda apontavam rodadas anteriores. Essa é a origem comprovada da deriva fonte/projeto, não mero CRLF. Evidência: `INT-R1-C2-I1-parte04.md:31-43,146-149`, comparação própria em `source-delta.diff` e parte03 desta investigação.
5. **O par original não desapareceu de todo lugar.** Encontrei fonte e DLL originais juntos no cache `C:/Users/Pichau/AppData/Local/hermes/cache/scratch/int_r1_c4_fora/tools/automacao/runtime/AUT4Probe/`; fonte também está em `docs/automacao/INT-R1-C2-I1-evidencias/AUT4ProbePlugin-pre-edicoes.cs.txt`. É falso dizer perda absoluta. A busca por nomes exatos em três raízes encontrou 52 fontes/7 hashes e 53 DLLs/14 hashes, sem erro. Parte02 detalha limites e hashes.
6. **SEG2-P já resolveu o alinhamento atual.** Foi aprovado às 14:48:56. O par agora é fonte **beaf965a…** / DLL **7f9a4cf1…**; cinco entradas repo/sandbox e PROBE_SHA passam em meu pré-flight exit 0. Não há necessidade de rebuildar de novo só porque o texto original mandava “reiniciar congelamento”. Isso não comprova equivalência em jogo com a versão original: a retirada do hook Localize exige um controle novo.
7. **Ainda há preparo do agente antes do runtime.** Geração offline do driver tem zero ocorrências das três chaves SEG2; os defaults fariam labels diferentes rodarem a mesma condição. Além disso production_diff histórico dá false (111/106; 4 novos/9 removidos/8 alterados). Precisa configurar as condições e usar snapshot imediato por rodada, preservando a proteção, sem restaurar saves históricos. Evidência: `audit-result.json.driver_generation` e `production_diff_historical`.
8. **A sessão para o mouse do dono não foi montada.** O script primeiro errou Local/Low, corrigiu para LocalLow, depois parou no Move-Item:54 por uso concorrente; junction:56 não foi criado. Dono do handle é **INDETERMINADO**. Tentativas de parar Steam/r2modman/worker não liberaram; não houve enumeração positiva de handles; WSearch não pôde ser parado. Reboot é alternativa operacional proposta, não prova de resolução.
9. **Nenhum dano ao conteúdo dos saves foi observado nesta coleta.** Real e cópia têm 106/106 arquivos iguais ao snapshot c51394a2… por SHA256+tamanho, sem junction e sem backup origem-real. Isso prova igualdade nessa comparação; não identifica quem segurava a pasta. Estado registrado em `audit-result.json.real_vs_snapshot`, `iso_vs_snapshot`, `real_path_state`.

## 2. Timeline verificada (BRT / UTC−03)

Fonte: `audit-result.json.board`, com eventos e IDs integrais preservados. Horas absolutas calculadas dos timestamps locais.

| Data e hora | Evento / evidência | O que significa |
|---|---|---|
| 10/10/2026 19:50:23 | SEG2 created 8498; dependency_wait 8499 | Criado a partir do A/B; esperava KIT-14G. |
| 10/10/2026 20:34:34 | promoted 8529 | Pai concluído; elegível. |
| 11/10/2026 01:58:56–01:58:59 | model_override 8580; assigned 8581 | deepseek-flash/default. |
| 11/10/2026 01:59:02 | edited/claimed/spawned 8584–8586, run720 | Cap 10.800s; começou implementação instrumental. |
| 11/10/2026 02:13:43 | commented 8617; blocked 8618 | Offline entregue, runtime não executado, needs_input. |
| 11/10/2026 02:14:00 | timed_out 8621 | Orçamento de iterações 90/90 esgotado. Payload retry_status=ready não é prova de reabertura; task/run continuam blocked. |
| 11/10/2026 02:24:02 | KIT-14-entrega-run721.md:7,19-20 | Par original existia e foi rechecado. |
| 11/10/2026 05:47:33 | t_a706b09c completed (kanban_show) | Migração observacional alterou fonte/projeto/DLL; identidades gerais atualizadas, rodada SEG2 ficou histórica. |
| 11/10/2026 13:55:57–13:56:02 | SEG2-P created 10310; linked em SEG2 10312 | Criado preparo dedicado, sem runtime. |
| 11/10/2026 14:13:51 | state.db 108131 | Erro de caminho Local/Low. |
| 11/10/2026 14:14:01 | state.db 108133 | Caminho corrigido; cópia/snapshot feitos; Move recusado. |
| 11/10/2026 14:14:55–14:20:13 | state.db 108141,108143,108151,108208,108210 | Tentativas de exclusão Steam/r2modman/worker; indexador não pôde ser parado; rename continua recusado. |
| 11/10/2026 14:20:04–14:20:32 | SEG2-P reclaimed 10339, pausa 10340, unblocked 10343, claimed 10344 | Pausa técnica da tentativa de handles, depois retomada run840; não é causa do crash original. |
| 11/10/2026 14:36:32 | SEG2 commented 10366 | Novo par informado ao próximo worker. |
| 11/10/2026 14:38:21–14:48:56 | SEG2-P review_requested 10372; revisão run842; completed 10407 | Preparo concluído e revisado, sem boots. |
| 11/10/2026 14:52:53 | state.db 108440 | Dono recebeu aviso com “NADA que só você possa fazer”. |
| 11/10/2026 14:54–15:01 | ferramentas desta investigação; audit/supplement | Bytes e pré-flight confirmados; par original recuperável; gates runtime ainda pendentes. |

## 3. O que o aviso automático deixou de dizer

`economy_status.py:170` trunca o motivo em 320 caracteres. O texto recebido omitiu detalhes do restante do motivo, e a classificação por “clique” misturou clique sintético, nome CliqueFisico e clique humano. Mensagem velha negava ação do dono; mensagem atual manda “Nada acontece até você executar”, também ampla demais: ainda há trabalho automático de driver, identidade e gates.

A correção de wording já foi feita pelo operador em outra sessão; nesta tarefa **não** alterei Hermes/cron. Extraí a função por AST e medi seu retorno para o motivo real sem executar o cron. Há necessidade de aviso com ação específica por etapa, não apenas palavra-chave. Evidência: `state.db` 108440/108441 e leitura `C:/Users/Pichau/AppData/Local/hermes/scripts/economy_status.py:107-124,169-170`.

## 4. Próximos passos em duas colunas, na ordem segura

Esta tabela é uma proposta de encaminhamento, **não autorização nova de runtime** e não instrução para o dono clicar agora. Respeita as autorizações já registradas em KIT-14 e os limites desta investigação.

| MUNDO DO DONO | MUNDO DO AGENTE |
|---|---|
| **1 — Nenhum clique em save real.** Não precisa reautorizar genericamente KIT-G2/A/B. | Confirmar o preparo aprovado e manter o novo par congelado; preservar referência original recuperável se o operador decidir conservá-la. Reabrir SEG2 operacionalmente na frente correta, sem repetir SEG2-P. Prova: identidade repo/sandbox/config e gate de autorização/frente. |
| **2 — Se houver necessidade de elevação/identificação do handle, agir supervisionadamente.** Pode informar janela/programa segurando a pasta; reboot do Windows é alternativa, não garantia. Só avise que reiniciou se foi o computador, não apenas r2modman. | Preparar driver novo com F-marcadores=false/0/false, F-silencio=false/0/true e F-gate=true/10/false; rota Play;Roguelike;Accept, probe só. Registrar cfg+hash/labels; substituir a comparação histórica por snapshot imediato antes/depois, explicitamente. Resolver/verificar isolamento antes de qualquer lançamento. Não matar processos alheios nem enfraquecer guardas. |
| **3 — Nenhuma ação humana é necessária para o clique sintético da bancada.** | Com frente autorizada, save isolado e identidades/gates verdes, executar primeiro **F-marcadores**. Prova: reproduz (ou refuta) o gatilho na build nova; marcos limitam o caminho e Event Log confirma assinatura na janela. Se não reproduzir, não atribuir a F-gate o desaparecimento do crash antigo. |
| **4 — Ainda não clicar no jogo real.** | Na mesma build e condições controladas, executar **F-silencio** e **F-gate**. Prova: dependência da atividade posterior do probe e do gate/estabilidade; confirmar clique real do handler, ativação da condição e chegada ao HUD. Ausência de crash sem navegação/sem chegada à run é NAO_EXERCITADO, não sucesso. |
| **5 — Quando o agente confirmar sessão isolada montada e coleta pronta:** Play → Roguelike → criação; avisar “na criação”; clicar Accept **uma vez com o mouse**; dizer se chegou ao HUD, fechou ou teve outro sintoma. | Preparar etapa física supervisionada **se necessária ao diagnóstico ou ao aceite visual**, com probe em Navegar=false (se instalado), sem handler sintético competindo. Identificar versão/DLLs/dados/config/tempo. Coletar Player.log e Event Log da própria janela; comparar com boots sintéticos. Esse teste não precisa esperar o KIT-14 inteiro fechar: separar a etapa diagnóstica da fila SEG2 → SEG1-RT → KIT-14 evita espera circular. |
| **6 — Relatar o observado; não precisa colar logs.** Skills/RSTV/legibilidade são a etapa visual posterior do KIT-14, não requisito deste diagnóstico mínimo. | Encerrar/restaurar com dono presente conforme autorização; verificar save real por hashes imediatos, caminho/Cloud/frente/perfil. Declarar classificação e próximo reparo somente sobre provas. Corrigir/revisar SEG2 ou documentar limitação comprovada; depois liberar SEG1-RT e só então KIT-14 completo. |

Os passos 3–4 podem preceder o físico porque são sintéticos e a própria receita os prevê; não dependem do mouse do dono. Ambos os caminhos, porém, dependem de **isolamento efetivo**. O ponto físico é trabalho humano de input, não obrigação de fazer as correções do agente.

## 5. Limites dos discriminadores (não converter hipótese em causa)

- **Silêncio não é zero contato com a engine.** O ramo atual chama QuadroAtual/TempoSilencio a cada marco, que leem Time.frameCount/realtimeSinceStartup (`AUT4ProbePlugin.cs:419-423,1513,1518-1523`), além de gravar JSON. Ele retira trabalho de varredura/leitura/captura principal, não todo código do instrumento. Sobreviver favorece interação pós-clique; morrer não prova sozinho defeito exclusivo do jogo.
- **Gate não é input físico.** Continua invocando `onClick.Invoke()` (:1198), sem demonstrar raycast completo/oclusão/EventSystem. F-gate sobreviver com controle F-marcadores morrendo sustenta dependência do gate/tempo, não substitui aceite humano.
- **Último marco não é stack nativa.** É a última linha registrada; operações posteriores podem não emitir marco, e abertura/escrita do log engolem exceções (:1534-1541). Para atribuir instrução exata, pode faltar dump/stack nativa correlacionada, além dos marcos.
- **Event Log antigo tem campo pid inadequado.** `roda714.py:198` exporta Properties[4] como pid; os exports A/B trazem uma string de versão `10.0.26100.9549`, não created_pid. A correlação antiga por janela continua reproduzível, mas futura correlação estrita por PID exige coletar o campo correto e verificar o schema do evento. Não inventei seu valor correto nem o corrigi aqui.
- **Handle/reboot continuam INDETERMINADOS.** Falta proprietário medido, e rename após intervenção supervisionada não foi exercitado aqui.

## 6. Entrega, validação e encaminhamento

Arquivos novos de relatório: **parte01, parte02, parte03 e parte04**, todos em `C:/dev/stolen-realm/docs/automacao/KIT14G-SEG2-investigacao-parteNN.md`. Evidências e scripts próprios no workspace `C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_ceda98dd/`: audit_seg2.py, audit-result.json, supplement_seg2.py, supplement-result.json e source-delta.diff. Bundle e resultado de verificações finais serão citados no handoff, com hashes medidos.

**PASSOU nesta investigação:** coleta do board readonly; pré-flight (DLL+5 entradas); geração/compilação offline do driver sem executar; comparação real/cópia/snapshot por bytes; varredura ampliada; diff fonte anterior/atual; recontagem temporal independente dos cinco exports A–E; histórico da recusa de Move; reprodução da função de classificação sem executar cron. Scripts da investigação terminaram exit 0.

**NAO_EXERCITADO por proibição do cartão:** jogo/boots novos, clique físico, montagem/desmontagem/retentativa de rename, reboot, handles elevados, build do probe, modificação de driver/cron/perfil, deploy e publicação. A investigação está pronta para revisão; o SEG2 continua sem aceite runtime.

Lacunas novas para o operador encaminhar: identificação segura de handles/montagem supervisionada; aviso semântico por etapa; errata documental aditiva do runbook/receita. Driver e gates dos três boots já pertencem a SEG2, não criar duplicata. `hermes profile list` retornou apenas default; nenhuma autoatribuição ou assignee fictício criado. O grafo de investigação não tem filho de revisão precriado, então o handoff solicitado é **kanban_request_review no mesmo cartão**.
