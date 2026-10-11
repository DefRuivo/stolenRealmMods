# KIT-14 — run704 / checkpoint 29: achado REAL e reconferência reprovada

PNG 01 das duas condições abertos em visão: LOADING (Barrels/Shrines), não Skills/RSTV/Select Party desenhada. Navegação real do probe registrou 0 botões ativos, achou_skills=false, nenhuma invocação. CONCLUIDO do probe não valida cenário.

ACHADO RUNTIME: Player.log da condição with-passive, linha46, NullReferenceException em KIT04Adapter.SR.SRAdapterPlugin.Awake. Chainloader inicia Adapter ANTES do Core; código do Adapter usa CorePlugin.Instancia e core.Passivo sem guarda/dependência. É causa compatível a confirmar/refutar por especialista, não conserto nesta auditoria. Recorder efetivo NÃO comprovado; não calcular overhead como se estivesse funcionando. Log contém ainda erros GameAnalytics no encerramento (não atribuir todos ao Adapter).

Reconferência independente analisar.py: exit1 REAL, evidência verification.json preservada (SHA256 1e520d0ba6ce090b58c9dbdba4d7495aac7710886836bc9092142bc23da9b45f).
- Produção Stolen Realm 111/111 iguais; BepInEx pessoal 53/53 iguais; fontes1343 sem mudança; jogo fechado/junction ausente/frente livre.
- Árvore Abyssus 5/5 diverge da baseline histórica. Outro jogo já estava ativo segundo operador; não restaurar save dele por inferência. Rollback KIT03 de cada rodada conferiu sua baseline imediata e disse iguais. Investigar hashes/mtime sem expor conteúdos.
- Registro export final hash9e1366… diverge do histórico31bb4e…. Ambas baselines imediatas run704 e exports de restauração KIT16 eram31bb4e…, com readback igual no encerramento de cada rodada. Não declarar preservação final sem esclarecer formato/efeito/ação concorrente. Não escrever ramo do dono automaticamente só para fazer auditoria verde.

Próximo bloco: distinguir divergência serialização de export vs estado do registro; preservar evidência atual, investigar somente metadados de Abyssus/PlayerPrefs; interromper novos boots até esclarecer. Finalização exigirá Cloud ON via clique do dono (runbook), sem contornar bloqueio desktop.

Perfil descoberto via hermes profile list: apenas default. Não inventar assignee nem criar seguimento autoatribuído. Achado de produto será registrado para encaminhamento pelo supervisor.
