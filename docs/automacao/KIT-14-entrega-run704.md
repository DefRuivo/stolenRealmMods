# KIT-14 — entrega PARCIAL run704: runtime real, falha do Adapter e cobertura limitada

Cartão t_a1f38855; implementador default/run704; revisão independente PENDENTE (filho já existente t_9ce7d260, inspecionado em todo). Complementa runs698/699/702/703 e partes24–31 sem sobrescrever. Nenhuma implementação de produto foi modificada, nenhum commit/publicação/novo build/deploy no perfil pessoal.

## Resultado

Duas sessões reais de 60s planejados, com área de dados inicialmente VAZIA comprovada como alvo da junction, sem selecionar personagem pessoal. Harness run702 reaproveitado com mudanças controladas/guardas, sem reiniciar offline run699. Core/Adapter somente no perfil temporário da segunda condição; probe nas duas. Cloud específica app1330000 off comprovada por cloudenabled=0 antes de cada boot, depois e no fechamento. Decisão B aplicada: números exploratórios crus, sem tolerâncias nem aceite de performance.

Resultado funcional: PNG01 de ambas aberto/inspecionado em visão = LOADING (Barrels/Shrines), NÃO Skills/RSTV. Probe leu 0 botões ativos, achou_skills=false, nenhuma invocação. GuiState e texto de objeto não foram promovidos a pixels visíveis. CONCLUIDO/exit0 do harness não valida o marco.

ACHADO REAL: Player.log da condição with-passive, linha46, NullReferenceException em KIT04Adapter.SR.SRAdapterPlugin.Awake. Chainloader lista Adapter antes de Core (LogOutput-isolado.txt linhas19–20). Código vivo SRAdapterPlugin.cs:40 lê CorePlugin.Instancia e :55 acessa core.Passivo sem dependência declarada/guarda. Hipótese de causa compatível com a ordem observada, não conserto nem prova causal isolada. Recorder não inicializado efetivamente/com saída comprovada; NÃO apresentar comparação como overhead de recorder. CorePlugin/Adapter podem constar no roster mesmo após falha de Awake.

## Sessões, identidade e eventos

- without-passive: KIT14-run704-without-passive-readonly-20261010-151314; PID21736; duração real60.81786050001392s; Core/Adapter ausentes; 24 observações/23 amostras processo/2 PNG. Leitura180; PNG solicitados180/188, concluídos188/194.
- with-passive: KIT14-run704-with-passive-readonly-20261010-151528; PID19004; duração real60.83437729999423s; Core/Adapter presentes, opt-ins true; 24 observações/24 amostras processo/2 PNG. Leitura165; PNG solicitados165/173, concluídos173/179.
- Total agregado por Python: 2 sessões, 48 observações, 47 amostras processo, 4 PNG locais. Nenhum PNG distribuído/exportado nesta rodada, pois falta revisão humana de privacidade.
- AUT4Probe DLL calculada em runtime nas duas sessões = congelada679365e2b0496a33b1c9bb77a7e561b40438ae1443d4120f661b2c5f6845dc57. Fonte/config/identidades de harness e hashes estão nos JSONs por condição; não confundir hash declarado com cálculo no assembly.
- Core instalado e reconferido4b318522f51b2ec4ed212f24a15861a0fd907104e561a07e27f300c3fc714eb3; Adapterab2da7587436b9457d152b110ef50014567d430747f85794678e0ab08456f3b0. Esses são hashes de arquivos instalados, NÃO medições pelo próprio assembly Core/Adapter carregado.
- Assembly-CSharp.dll local e instalado reconferidos8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a; não modificados/exportados.

## Execuções e controles reais

Ferramentas de bancada desta rodada são scripts em scratch/kit/KIT-14-run704; não dependências dos mods. Infraestrutura de produto tools/automacao reutilizada sem alteração.

- test_guardas.py:7/7 exit0; mutação --defeito-cloud:7 testes,1FAIL/exit1. Guarda Cloud ligada reprova; AST compara cleanup histórico preservado (única inserção finally é leitura Cloud).
- coleta.py without-passive e with-passive:exit0. PID próprio fechado graciosamente; comandos restaurar dados/BepInEx/liberar frente com exit0 e efeitos reconferidos no final, não só mensagens.
- Em CADA captura: detector campos básicos exit0/CONFIRMADA; expectativa impossível exit1/NO; fixture explicitamente rotulada exit2. Controle offline de interpretação sobre captura real, NÃO defeito plantado no mod ou Runner runtime.
- Em CADA captura: avaliador RSTV exit2/7NAO_EXERCITADO; viewer exit2. HTML existe em post/<condição>/report.html, mas não constitui aceite UI/UX.
- KIT07 export:exit0/4 payloads por condição; total8. Leitura de volta de cada bytes/hash, manifest incluídos4, upload=false; sem PNG/save/REG/config Steam/DLL proprietária. Origem é seleção minimizada (identidade, critérios, issue, números processo), não dump indiscriminado do perfil. Pacotes locais em post/<condição>/export-sanitizado; não enviados a serviço externo.
- Primeiro postprocessar.py exit1 após seis comandos reais da primeira condição por usar nomes errados do manifest KIT07 (destino vs caminho). Fonte/artefatos/falha preservados. retomar_post.py corrigiu somente interpretação e executou apenas segunda condição + readback faltante; exit0. Não repetiu boots ou seis comandos prontos.

## Performance: somente números observados

Sem recorder efetivo, sem mesmo cenário interativo e sem contadores FPS/tempo-frame/I/O: overhead NAO_EXERCITADO. Nenhum delta/limiar/veredito passa–não-passa calculado. Frames do probe são marcos, não medições de FPS ou duração de frame.

- without-passive: RSS mínimo56729600/máximo2339774464bytes; memória privada mínimo89616384/máximo3112812544bytes; CPU acumulada processo0.546875→22.671875s; amostras iniciam4.897999s e terminam58.808074s. Arquivos retidos do jogo isolado727741bytes.
- with-passive: RSS mínimo413212672/máximo2440499200bytes; memória privada mínimo454152192/máximo3120693248bytes; CPU acumulada1.546875→27.828125s; amostras iniciam3.7553505s e terminam58.8263282s. Arquivos retidos747770bytes.

Bytes retidos NÃO são I/O do recorder nem impacto de disco; buffers/Player.log/arquivos de jogo têm outras causas. Duas telas loading com dicas diferentes e janelas de amostragem diferentes não são base comparável de overhead.

## Preservação/rollback: readback final

verificar_e_selar.py exit0 (somente preservação/selamento, task_accepted=false):
- Produção Stolen Realm111/111, nenhum novo/removido/alterado vs manifesto prévio KIT16; BepInEx pessoal53/53 iguais.
- Fontes baseline run699:1343 sem divergência. Alterações manuais preexistentes mantidas; somente novos scripts/provas/docs desta rodada.
- Registro: mesmo ramo PAI Burst2Flame Entertainment, SHA25631bb4e1f0530c749817c207d6843b07a2e9e0726c0e703b40d1bc705def0bd7b antes/depois. Nenhuma escrita corretiva automática para deixar auditoria verde.
- Jogo fechado ([]), perfil temporário removido em ambas, diretório real sem junction, frente única disponível, índice git vazio. Outro jogo/Steam não encerrados.
- Abyssus: divergência histórica em2 arquivos com mtime14:49:42 -03, anterior aos boots15:13+. Alterações do dono preservadas, não restauradas. Rollbacks KIT03 conferiram suas baselines imediatas, mas manifestos foram removidos pelo cleanup; conferência independente posterior desses manifestos NAO_DISPONIVEL. Não alego que toda árvore de outro jogo permaneceu igual desde run699.

Falhas de auditoria preservadas: analisar.py exit1 (comparou árvore histórica de outro jogo e exportou REG de escopo menor); reconferir.py exit1 (registro já corretamente conferido, mas exigiu4 manifestos imediatos removidos). REG menor não era prova de perda: seção Stolen Realm também foi comparada e é igual. Não chamar essas execuções verdes; novo verificador usa escopo correto e explicita a lacuna.

Cloud: sharedconfig.vdf bloco1330000 cloudenabled=0 no fechamento. Remotecache foi atualizado pelo Steam durante os boots mesmo com toggle off; mtime por si não prova sincronização nem upload. Não houve inspeção de servidor remoto. Cloud ainda OFF; religamento ON é pendência do runbook, não executado por input alternativo.

## Cobertura por critério do cartão

1. Instalar build identificada: PASSOU para probe e plugins temporários; pacote RSTV não instalado nesta rodada.
2. Clique físico→janela RSTV→conteúdo/tooltip→PNG: NAO_EXERCITADO. PNG de loading não fecha marco.
3. Relatório/issue/export: PASSOU para pós-coleta real minimizada; issue é JSON, não marcação via UI; viewer sem cobertura aceita.
4. Runner cenários ativos/controle negativo em jogo: NAO_EXERCITADO. Controles do detector offline não substituem.
5. Mod funcionando sem kit: NAO_EXERCITADO nesta rodada; condição sem Core/Adapter é jogo+probe, não RSTV.
6. Uso básico sem Hermes/IA/credenciais: INDETERMINADO como runtime do mod; nenhuma credencial/assinatura necessária aos scripts executados, não confundido com teste de jogador independente.
7. Install/update/remove/rollback pacote: histórico run699 preservado, não reexecutado. Update histórico era reparação mesma versão, não upgrade; perfis/rollback temporários run704 reconferidos.
8. Saves de produção intactos: PASSOU local111/111; Cloud remota não observada.
9. FPS/tempo/frame/memória/disco com/sem recorder mesmo cenário: NAO_EXERCITADO; números crus de processo anexados com limitações.
10. Limiares: DISPENSADOS explicitamente por decisão B, não bloqueio novo nem tolerância inventada.
11. Hash DLL carregada/pacote: PASSOU para AUT4Probe medido no runtime; Core/Adapter só hashes de instalação/roster, estado funcional ACHADO.
12. Segundo ambiente limpo/portabilidade: NAO_EXERCITADO; perfil isolado local não é segunda máquina/conta.
13. Revisão técnica/visual independente: PENDENTE KIT14R. Implementador não autoaprova.
14. Aceite humano/Cloud ON/publicação: PENDENTE; nenhum gate consumido por inferência, nenhuma publicação.

## Runbook curto do dono (input OS não tentado novamente)

Agora, com Stolen Realm FECHADO e111 dados/restauração local conferidos:
1. Steam → Biblioteca → Stolen Realm → Propriedades → Geral → ligar sincronização Steam Cloud APENAS desse jogo (não Cloud global/conta inteira).
2. Confirmar visualmente que ficou ligada e avisar “Cloud religada”. O próximo worker fará leitura dirigida do toggle/estado sem exportar config integral. Não declarar Cloud restaurada antes desse readback.
3. Não abrir agora o jogo real para produzir prova em personagem pessoal. O marco UI seguinte precisa de nova sessão isolada/Cloud protegida e mod RSTV identificado; personagem descartável deve existir/ser criado somente na área vazia de teste. Clique OS/clique físico vira roteiro humano específico nessa sessão, nunca suposta invocação de Skills em loading.

Encaminhamento técnico necessário: especialista reparar/refutar ordem/lifecycle Adapter/Core e produzir build identificada/revisada, mantendo evidência defeituosa; prover roteiro/handler autorizado que alcance o menu/personagem descartável/Skills. Só perfil default foi descoberto; não inventei assignee nem criei follow-up autoatribuído. Não corrigi produto dentro da auditoria.

## Evidência selada

Raiz local: scratch/kit/KIT-14-run704 (não distribuir a raiz inteira: contém REG/quarentena privada).

- final/verification.json SHA256417410553ff9384ff7fa38ec0287433109289c7d4a0551663ffd542fd8365a39.
- final/seal.json SHA25603df410f090d62b97a4b14e28bff228c2a2629001193c8452633869f55c7beac:152 arquivos selecionados, lidos de volta bytes/hash, zero divergentes. Selo não inclui REG/save/quarentena/config Steam/DLL proprietária e não é upload.
- post/postprocessing-with-passive.json SHA2561e88b36738f1bd0a8d659439a5a1e06de4ce79517bc00c55e08fcc30cc731ac3.
- verification.json/reverification.json/analysis.log/reverification.log preservam tentativas reprovadas, sem mascarar.

KIT-14 NÃO concluído: há ACHADO funcional e critérios runtime faltantes. KIT14R não liberado nem duplicado; próximo encaminhamento precisa resolver o produto/roteiro, sem repetir autorizações A/B nem solicitar limiares novamente. Clique OS não é nova falha: é ação explícita do runbook; o impedimento técnico remanescente é recorder/roteiro funcional.
