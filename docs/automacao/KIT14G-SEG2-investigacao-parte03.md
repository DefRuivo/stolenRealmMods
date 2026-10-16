# KIT14G-SEG2-INV — parte03: causas da deriva, montagem e mensagem humana

Investigação default/run844; 11/10/2026. Esta parte é aditiva. Evidência de história: `supplement-result.json` no workspace t_ceda98dd, extraído somente-leitura de `%USERPROFILE%/AppData/Local/hermes/state.db`, com IDs e timestamps dos outputs originais. A timeline do board está em `audit-result.json.board` (extração readonly de kanban.db).

## 1. A deriva do instrumento tem uma origem documentada

Não foi necessário inventar “corrupção”, “perda misteriosa” ou culpa do timeout. O cartão **t_a706b09c / INT-R1-C2-I1**, concluído às 05:47:33 em 11/10/2026, alterou fonte e csproj e rebuildou o probe **depois** da implementação SEG2/run720. A sua parte04:31-43 documenta ecdcce13… → beaf965a… e DLL 95069e9c… → 7f9a4cf1…. Atualizou AUT-4-runbook/estado/preparacao, mas a receita histórica SEG2 §5 permaneceu nos hashes anteriores; sandbox/PROBE_SHA run712 ainda eram da rodada anterior até o preparo SEG2-P.

Prova própria complementar: `source-delta.diff` compara cache antigo com fonte vivo e mostra retirada de `GanchoTodos("OptionsManager", "Localize")`, substituição por `LigarPonteOpcional()` e config `PonteApiHook=false`. GUIManager.Update/PlayerLoop permanecem. A correção de SEG2 não foi implementada por essa ponte: o próprio cartão diz que clique/navegação/crash continuam fora de seu escopo.

**Consequência experimental:** mesmo com os controles SEG2 preservados, a build nova não é byte a byte nem tem exatamente o mesmo conjunto de drivers da original. O boot F-marcadores deve primeiro demonstrar se o gatilho antigo ainda reproduz nessa build. Não atribuir sobrevivência futura de F-gate à correção do gate se o controle F-marcadores já sobreviver. Escolha do novo par feita pelo preparo aprovado; esta investigação não troca a build.

A fonte original também existe **dentro do repo**, sob outro nome: `docs/automacao/INT-R1-C2-I1-evidencias/AUT4ProbePlugin-pre-edicoes.cs.txt`, 104.974 bytes, SHA256 ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2. Na parte02, “52 fontes” era a contagem **do nome exato AUT4ProbePlugin.cs**, não de todas as reconstruções com nome distinto. O par original fonte+DLL está no cache int_r1_c4_fora indicado na parte02; sua conservação em cache não é arquivo permanente.

## 2. Montagem: o que falhou, com timestamps e força da prova

Todos os horários abaixo são **11/10/2026, UTC−03**, calculados dos timestamps, não dos rótulos de data imprecisos do buscador de sessões.

| Hora / mensagem state.db | Medição registrada | Conclusão permitida |
|---|---|---|
| 14:13:51 / 108131 | Caminho Local/Low inexistente | Primeiro erro foi do script; abortou antes do snapshot. Corrigido no script atual:18-20 para LocalLow. |
| 14:14:01 / 108133 | Snapshot 106 arquivos; export/cópia; Move-Item:54 falha com “sendo usado por outro processo” | Sharing violation/uso concorrente comprovado naquele instante; junction:56 não atingido. |
| 14:14:28 / 108137 | Real sem LinkType, 91 itens imediatos; backup inexistente; cópia 91 itens; duas tentativas recusadas | 91 entradas no nível superior não contradizem 106 arquivos recursivos. |
| 14:14:55 / 108141 | steam.exe=0; move ainda recusado | steam.exe não era condição suficiente para explicar o bloqueio. |
| 14:15:34 / 108143 | Comando tentou encerrar steam*; move ainda recusado; Steam reaberto (8 processos) | Tentativa ampliada não liberou. Não há contagem steam*=0 entre o encerramento e o rename: “TODOS descartados” é mais forte que esse output. |
| 14:16:10 / 108151 | Comando tentou encerrar r2modman; Directory.Move falha igual | Trocar Move-Item por API .NET e encerrar r2modman não resolveu. Não houve inventário de handles por PID. |
| 14:19:48 / 108208 | Após o dono reiniciar r2modman: 4 processos, jogo fechado; move falha igual | Reinício de r2modman não liberou; não é reboot do Windows. |
| 14:20:13 / 108210 | Worker SEG2-P reclamado/parado; move segue recusado | Worker em execução não era requisito para persistir o bloqueio. |
| 14:20:13 / 108210 | WSearch não pôde ser parado (“Não é possível abrir o serviço…”) | Indexador **NÃO foi descartado**. A linha “após C (WSearch parado)” é um rótulo falso: a própria saída informa falha. |

Esses outputs são de wrappers com **exit_code=0** mesmo quando PowerShell/Move falharam. O helper guardou stdout/stderr, mas não propagou o returncode do subprocesso; portanto “tool success” não comprova montagem. A presença da exceção e o readback do caminho prevalecem.

**Dono do handle: INDETERMINADO.** Não foi apresentada enumeração de handles/kernel por PID/caminho. Steam/r2modman/worker tiveram tentativas de exclusão, não atribuição positiva. SearchIndexer, Explorer, antivírus, backup ou crash handler são hipóteses, não causas provadas. Falta uma captura de handles no instante da recusa (se requerer elevação, ação supervisionada do dono/operador).

**Reboot: proposta, não prova nem garantia.** Não existe nesta evidência um reboot do Windows seguido de rename exitoso. Reiniciar r2modman não equivale a reiniciar o computador. Não prometer “depois nada segura” nem “montagem em 20 segundos”. Esta investigação não retentou rename: NAO_EXERCITADO por limite expresso.

O estado **atual** já foi confirmado na parte02: real e cópia 106/106 iguais ao snapshot por conteúdo; sem junction/backup; jogo fechado. Não lançar o jogo para o teste nesse estado.

## 3. O aviso automático tinha um erro e ainda tem uma simplificação perigosa

Mensagem original copiada pelo dono em state.db **108440**, 11/10/2026 às 14:52:53: a seção Por que termina em “orçamento… acabou”; seção Para destravar diz “NADA que só você possa fazer agora”. Isso ocultou o passo humano e o estado de montagem, além de não distinguir congelamento de medição.

`%USERPROFILE%/AppData/Local/hermes/scripts/economy_status.py:170` corta o motivo em **320 caracteres**. `_como_destravar:107-112` usa palavras genéricas (`clique`, inclusive em “marcos-clique”/“CliqueFisico”) antes de analisar needs_input. O histórico 108441 documenta a troca da mensagem antiga; a leitura atual confirma “VOCE PRECISA AGIR… Nada acontece até você executar”.

Prova própria: executei **somente a função extraída por AST**, sem importar/executar o script de cron (evitando gravação/envio), com o motivo real SEG2. Ela retorna a mensagem de ação exclusiva do dono, apesar de o motivo também conter **três boots sintéticos executáveis pela bancada**. Logo, a correção de wording ainda confunde tipos de clique; não permite concluir que tudo depende do mouse do dono. Nenhum arquivo Hermes foi alterado nesta investigação.

## 4. Lacunas encaminhadas, não implementadas

- SEG2 já tem escopo/receita para driver dos três boots e diagnóstico. Não duplicar a tarefa.
- Montagem/identificação do handle e melhoria semântica do aviso são frentes próprias; também cabe errata aditiva da receita/runbook. Não foram implementadas aqui.
- Descoberta `hermes profile list`, exit 0: **apenas default**. O protocolo desta rodada proíbe autoatribuir follow-up e inventar assignee. Por isso não criei cartão autodespachável para mim; propostas são registradas no handoff/comentário para o operador escolher especialista. Isso não impede entregar a investigação.

NAO_EXERCITADO: parar processos/serviços, instalar ferramenta de handles, reboot, montar/desmontar, abrir jogo, corrigir driver/cron, rebuild, deploy e publicação. Não são falhas do investigador: estão fora do limite autorizado.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
