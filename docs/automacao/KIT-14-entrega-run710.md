# KIT-14 — entrega PARCIAL run710: arranque corrigido, espera real, roteiro/recorder pendentes

Cartão:t_a1f38855. Implementador:default/run710. Revisão independente:PENDENTE,t_9ce7d260 (filho preexistente inspecionado,não duplicado/não liberado). Data local:10/10/2026. Complementa runs anteriores e partes32–40;nenhum produto/mod foi editado,nenhum commit/push/publicação/deploy pessoal.

## 1. Resultado e impedimento específico

Requalificação REAL após KIT-14F revisado (run709 ≠ autor run708). Core agora é carregado ANTES do Adapter;vínculo concluído e a NullReferenceException antiga não aparece nas três capturas de Player.log examinadas. Probe corrigido percorre a fase real de navegação,esgota o teto e encerra corretamente.

Não fecha KIT-14:recorder eficaz sem arquivo/eventos runtime lidos;rota entregue só procura Skills e não chega ao contexto necessário. Dois boots com teto12 capturam loading. Diagnóstico adicional com teto3600 chega ao MENU PRINCIPAL,10 botões ativos,Skills ausente,nenhuma invocação. Mod RSTV não instalado nesses boots diagnósticos;logo,não atribuir ausência de janela a defeito do mod.

Próximo técnico concreto:roteiro revisado menu→personagem descartável→Skills e mod-alvo identificado no perfil TEMPORÁRIO,consumidor/leitura da trilha runtime do recorder,recaptura dos objetos após ação. Não modificar o produto durante a auditoria só para deixá-la verde. Perfil disponível descoberto:apenas default;não inventei especialista nem criei follow-up autoatribuído. Supervisor precisa encaminhar esse escopo a implementação/revisão independentes antes de outra rodada.

Input OS não foi tentado/contornado. Clique físico e Cloud ON residual têm runbook curto separado;isso não é pedido de nova autorização KIT-G2/A/B nem novo limiar.

## 2. Builds/identidades/preflight reais

Sandbox nova conserva fontes tracked/untracked:1385 arquivos (874 tracked,512 untracked,nul excluído),sem .git/remotos/credenciais. Referências proprietárias locais só para compilação. Preflight6 alvos exit0;controle negativo XML sem opt-in exit1;preflight antes de CADA build exit0. Builds isolados com -p:DeployToBepInEx=false e USERPROFILE/APPDATA/LOCALAPPDATA separados:
- AUT4Probe:exit0,1 aviso,0 erros.
- KIT04Adapter.SR/Core:exit0,67 avisos,0 erros.

Hashes das builds usadas:
- AUT4Probe.dll:35e845c0c1a71da83454372dd5452b7463b1edf668d0e59e88eaf17b5240e582.
- KIT04Core.dll:84d911a8a6edaf8b081812ccb92b781e7bbc42553a0fbdfad64056616bdc8040.
- KIT04Adapter.SR.dll:2a4386bde036d15d8fd2c0f814b0af1ca5fd8d8edf73a04114d794f9900796a8.
- Fonte AUT4ProbePlugin.cs:21586beb01063bb2e2a64ca9ad21948397d83282382ddc1a0fc9ab024b058d1d (igual à correção revisada).
- Fonte SRAdapterPlugin.cs:d810464da20ccd88459352ce9b465f9cf12ed0221376080b8367a4d2587b639a.

Probe calcula hash do próprio assembly em runtime:igual à build/instalada em CADA sessão. Core/Adapter têm hash instalado+ordem/log,vinculação observada;NÃO há hash próprio calculado em runtime nem contagem interna lida desses dois assemblies. Configs/sessões/hashes de fonte guardados nos JSONs por condição. HashFonte do driver do probe é o hash da DLL,não confundir com SHA do arquivo-fonte;este está separado.

Pacote HISTÓRICO final reconferido no caminho exato:scratch/kit/KIT-14-run699/pacote-resume/kit-rstv-0.1.0.zip,175059 bytes,SHA256 d5f42854a5f852b813f181d302bdbcc2a90498493e7d0f3da1af0a54bf606bf7. CLI verificar exit0,42 membros,testzip=null,problemas/scan vazios. É pacote fonte/ferramentas do run699,não pacote de DLLs atuais nem novo release;install/update/remove/rollback histórico não foi repetido como novidade. Consulta inicial a pacote/ apontou ZIP de tentativa anterior,explicitado em parte40;não houve drift alegado nem reempacotamento para casar SHA temporal.

## 3. Sessões/cobertura real

Ferramentas de bancada nesta rodada:scripts em scratch/kit/KIT-14-run710,reusando finalmente/isolamento de run702/run704 e KIT03/KIT16. Nenhuma dependência nova dos mods.

| condição | sessão | PID próprio | duração real s | observado |
|---|---|---|---|---|
| without-passive | KIT14-run710-without-passive-readonly-20261010-174951 |31648|61.89812950004125|probe sozinho;PNG loading/Fortunes;12 tentativas,0 botões |
| with-passive | KIT14-run710-with-passive-readonly-20261010-174815 |32660|62.01125480001792|Core→Adapter,vínculo normal;PNG loading/Barrels;12 tentativas,0 botões |
| late-with-passive | KIT14-run710-late-with-passive-readonly-20261010-175251 |21136|60.964099600038026|mesmas DLLs,teto cfg3600;PNG MENU PRINCIPAL;10 botões,Skills ausente |

Todos os PNG01 foram efetivamente abertos/inspecionados:não são Skills/RSTV.6 PNG locais no total,não distribuídos/exportados.72 observações e74 amostras de processo,total agregado por Python. Três instâncias próprias encerradas graciosamente;finally restaurou dados/BepInEx/frente e efeitos foram relidos.

Correlação não simultânea:leitura/pedido PNG em with-passive160→164 e without-passive156→160;diferença calculada4 em ambas. Diagnóstico tardio157→1352,pedido concluído1356;segundo1356→1361. Os3600 incrementos de tentativas cobrem1195 frames entre leitura e pedido:contadores internos não são FPS nem quadros renderizados um-a-um. Observações e CurrentGuiState iniciais NÃO descrevem automaticamente o menu do PNG tardio. Necessária recaptura pós-ação antes de alegar prova visual de texto/tooltip.

## 4. CLIs/controles e exportação

- test_build.py:2 testes OK exit0 (preflight negativo real exit1 antes do build).
- test_guardas.py:11 OK exit0;MESMO mutante --defeito-cloud:11 testes,1FAIL,exit1. Logs green/red conservados;AST mantém finally original.
- Harness KIT14F:10+5+21 verificações OK agregado exit0;estado de UI injetado offline e Harmony offline falha declarada. Adapter e probe da sandbox,mas Core resolvido do bin/Release do repo (não atribuir o agregado exclusivamente às3 DLLs novas). Fonte do harness confirmou CoreBin fixo. Três temporários que o harness criou inadvertidamente em Temp do sistema foram enumerados/hashados,JSON guardado no scratch e SOMENTE esses3 foram removidos;ausência lida de volta. Ressalva não escondida;próxima chamada precisa TEMP/TMP redirecionados.
- Em CADA captura:detector sobre OBJETO real inicial exit0;expectativa de fonte deliberadamente impossível NO/exit1;fixture rotulada exit2. Controle de interpretação offline,não defeito plantado no mod/Runner runtime.
- Avaliador RSTV:exit2,7NAO_EXERCITADO por condição. Viewer:exit2,21NAO_EXERCITADO,aprovação ausente. HTML local não é aceite UI/UX.
- Issue marcado por JSON,não UI. Export KIT07:exit0,4payloads por condição,total12;cada arquivo/hash/tamanho reconferido com manifest.0PNG,sem DLL proprietária/save/registro/config Steam,upload=false. Diretórios:post/<condição>/export-sanitizado.
- Travas gerais versionadas:check_segredos,check_padroes_segredo,check_dupes,audita_docs todos exit0;isso não audita integralmente todos os novos docs locais.

## 5. Números crus: NÃO comparação de recorder

Decisão B aplicada:sem limiares,sem veredito de performance. Recorder eficaz não foi lido e cenários/janelas/telas diferem;nenhum delta de overhead foi calculado. FPS,duração média/p95 de frame e I/O do recorder:NAO_EXERCITADO,não estimado.

| condição | amostras | RSS máximo bytes | privada máxima bytes | CPU acumulada início→fim s | bytes retidos dados isolados |
|---|---|---|---|---|---|
| without-passive |25|1972187136|3144380416|0.890625→26.046875|727698|
| with-passive |25|1979125760|3147030528|0.875→28.03125|727891|
| late-with-passive |24|1991110656|3151167488|0.515625→34.5625|727872|

Amostras/tempos completos em verification.json e process-samples.json. Bytes retidos são arquivos do jogo,não writes ou espaço atribuível ao recorder. A checagem de recorder_path_exists foi realizada APÓS rollback:essa ausência não prova que o diretório nunca existiu durante o jogo. Nenhum arquivo/evento dessa trilha foi preservado/lido;portanto,inexistência runtime e zero eventos internos continuam INDETERMINADOS. ResultadoFinal existe como API no Core,mas nesta rodada não há consumidor que a leia no processo. O próximo executor precisa medir/exportar a trilha ANTES de remover o perfil temporário.

## 6. Preservação/rollback/Cloud — efeito reconferido

verificar_e_selar.py exit0,task_accepted=false:
-111/111 arquivos dos dados Stolen Realm idênticos ao snapshot KIT16;sem novos/removidos/alterados. Nenhum personagem pessoal selecionado,cópia pessoal em quarentena não consumida.
-53/53 arquivos BepInEx pessoais e5/5 outro jogo idênticos à baseline IMEDIATA run710. Não restaurar mudanças históricas do dono para fingir igualdade com run699.
-1385 fontes sem divergência;novos arquivos só partes/docs autorizados. Índice git vazio;nenhum commit/reset.
-Registro no mesmo ramo PAI Burst2Flame Entertainment:SHA25631bb4e1f0530c749817c207d6843b07a2e9e0726c0e703b40d1bc705def0bd7b antes/depois.
-Assembly-CSharp local/instalado:8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a,intacto,não exportado.
-Jogo fechado[],junction ausente,backup real retornado,perfis temporários removidos,frente livre. Outro jogo/Steam não encerrados.
-Cloud app1330000 cloudenabled=[0] antes/antes do boot/fim/fechamento. Mtime remoto mudou apesar do toggle off;não é prova de upload. Cloud remota não inspecionada. Cloud ON restauração pendente do dono conforme runbook;nenhuma edição VDF/input alternativo.

## 7. Veredito por critério

| critério | estado e limite |
|---|---|
| build/probe identificado instalado isolado |PASSOU;identidade própria do probe medida |
| arranque Core→Adapter/NRE anterior |PASSOU nesta observação;recorder eficaz INDETERMINADO |
| fase/retry/teto cfg real |PASSOU;teto12 e3600 real esgotados;não prova handler de alvo |
| clique físico→janela RSTV→conteúdo/tooltip→PNG |NAO_EXERCITADO |
| relatório/issue/export |PASSOU para pós-coleta minimizada;issue JSON,não UI;viewer não aceito |
| Runner ativo positivo/negativo |NAO_EXERCITADO;detector offline não substitui |
| RSTV funcionando sem kit |NAO_EXERCITADO;condição sem Core/Adapter só tem probe |
| básico sem Hermes/IA/credenciais |histórico offline run699;runtime do mod INDETERMINADO |
| install/update/remove/rollback |histórico offline run699 preservado;update era reparo mesma versão;rollback desta rodada PASSOU |
| saves pessoais intactos |PASSOU local;Cloud remota não inspecionada |
| FPS/frame/memória/disco comparáveis com/sem recorder |NAO_EXERCITADO;números de boot separados |
| limiares prévios |DISPENSADOS pelo dono,não bloqueio |
| pacote/hash |histórico final reconferido;nenhum pacote atual publicado |
| segundo ambiente/portabilidade |NAO_EXERCITADO;perfil temporário não é outra máquina/conta |
| revisão técnica/visual/aceite humano/publicação |PENDENTES,separados |

## 8. Evidências/handoff

Raiz:scratch/kit/KIT-14-run710 (não distribuir integralmente:há referências proprietárias/quarentena/registro privados).
- final/verification.json SHA256 da45cd4146f1c7347cbaf36ae2e21fbd971b5d9e751b1286091c811d40258311.
- final/seal.json SHA256 73eaca48fad733eac2f3c886fbaa2706f9997aad43a1a63f17e5de48cfda2e4e:HISTÓRICO239 arquivos. Readback posterior reprovou por1 log autoescrito (final-readback.log,0→312bytes),não por payload. Falha/correção registradas em parte42;usar final/seal-final.json novo para os238 payloads restantes,com comparação estrita. Documentos finais e leitura do pacote têm readback separado,não fingir que entraram no selo histórico.
- build-results.json,binaries.json,preflight-readonly.json,logs/*,guardas-green/red.log.
- with-passive/without-passive/late-with-passive:result.json,commands.json,probe/aut4probe.json,PNG,process-samples.json,LogOutput-isolado.txt e Player.log na área descartável.
- post/postprocessing.json e exports minimizados;package-final-historical-readback.json.
- Runbook humano:docs/automacao/KIT-14-runbook-residual-run710.md.

KIT-14 NÃO concluído. Não liberar/duplicar KIT14R,não solicitar novos limiares/consentimento genérico. Encaminhar roteiro/consumo runtime a escopo de implementação/revisão próprio;depois retomar somente faltantes. Aceite UI/UX e Cloud ON residual pertencem ao humano,sem promover a presente auditoria parcial a DoD.
