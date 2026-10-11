# KIT-14 — entrega PARCIAL run702 / runtime readonly real

Cartão t_a1f38855. Autor default/run702, instância implementadora. Data operacional final medida: 10/10/2026 14:01:14 -03. Complementa KIT-14-entrega.md e KIT-14-entrega-final.md sem os sobrescrever. Não conclui KIT-14, não concede aceite humano, não libera publicação nem KIT-14R.

## Resultado

Pela primeira vez nesta frente KIT-14 houve coleta real com AUT4Probe, usando o isolamento local revisado do KIT-16. Foram lidos 24 objetos e gerados 2 PNG pela API Unity. Hash do assembly carregado foi calculado pelo próprio instrumento e coincide com a build sandbox identificada. A sessão foi encerrada pelo PID próprio e o ambiente local restaurado, com leitura dos efeitos no disco.

O escopo efetivamente exercitado foi BOOT/LOADING, sem navegação, clique, demonstrador ativo, janela Skills, mod RSTV ou personagens. O relatório KIT08 corretamente deixa 21 critérios NAO_EXERCITADO (exit 2). Isso não é validação do marco ponta a ponta nem comparação de recorder.

## Autorizações e fronteira de segurança

KIT-G2 B1–B6 já autoriza perfil/save descartável, observação e navegação isoladas; não pedir novamente autorização genérica. Decisão B do dono continua vigente: limiares prévios DISPENSADOS, coleta exploratória sem PASSOU/FALHOU de performance.

KIT-16 resolveu persistentDataPath local, mas declarou risco residual Steam Cloud. Leitura dirigida do localconfig.vdf nesta execução confirmou cloud.last_sync_state=synchronized e autocloud.lastlaunch/lastexit das rodadas anteriores. Não é prova isolada do toggle atual; é prova de participação recente da mesma conta. O harness local não impede sincronização de saves descartáveis modificados para o Cloud pessoal.

Por isso não naveguei/carreguei personagens nem escrevi saves descartáveis. Também não desliguei o Cloud/configurei Steam por conta própria. Nenhuma publicação, modificação de Assembly-CSharp, gameplay/Bard, travas, política/modelo/cron/prioridade ou perfil pessoal.

## Execução real

Harness descartável: scratch/kit/KIT-14-run702/coleta_readonly.py. Reusa KIT16 preparar/verificar/restaurar e KIT03 preparar/rollback, sem editar essas implementações. Config AUT4 gerada pelas APIs derivar_config/escrever_cfg existentes.

- Guardas offline: test_guardas.py Ran 5 tests / OK / exit 0, duas execuções; recusa processo existente, hash errado, raiz reutilizada, fonte alterada. Mutação seletiva em memória remove o guard de processo existente e deixa esse input escapar. Não é prova de jogo.
- Primeira tentativa: exit 1; front-check exit 127 por representação de caminho na chamada de bash. Antes de lock/install/boot. Logs/result originais preservados.
- Correção somente no harness: Git bash explicitamente descoberto, caminho forward-slash, segunda evidência em attempt02 novo.
- Segunda tentativa: exit 0; front-check/acquire, BepInEx preparar, dados preparar, Steam launch, dados verificar/restaurar, BepInEx rollback e front-release todos exit 0.
- Sessão KIT14-run702-readonly-20261010-135444; PID próprio 16064, executável verificado, CloseMainWindow e espera de término; game_closed=true.
- Config explícita: Autorizado=true, Navegar=false, DemostrarTooltip=false, AutorizaEscritaTooltip=false, orçamento 60s, timeout externo 120s, MaxTextos=400.
- Observação terminou após 17.639836500020465s desde lançamento; JSON CONCLUIDO/fase concluido. Log confirma um único plugin AUT4Probe 0.1.0 e motor PlayerLoop/ganchos, 24 observações/2 prints.

## Identidade e correlação

DLL sandbox run699 e assembly carregado: SHA256 679365e2b0496a33b1c9bb77a7e561b40438ae1443d4120f661b2c5f6845dc57, 56320 bytes. Não é o antigo hash congelado do KIT-G2: rebuild sandbox já identificado no run699; cinco fontes/projeto foram reconferidos byte a byte antes de instalação. Nenhum novo build nesta rodada.

Cfg gerada SHA256 a5033b41b4672ce0d2c26b34e3d5429a8ca50aeeb9e548bdd797374f33195635. Probe JSON original SHA256 fe5d834631e0255716cae7f104b5509ba0e8e09378579cadab5ef534a0cb3cb1, preservado imutável pelo pós-processamento.

- Leitura objetos/textos: frame 158.
- 01-ui.png: pedido frame 158, concluído 163; 2493394 bytes; SHA256 a2520d4b807ce7dcb6ec9800baafba54d210fe7bb86a0be0471cb4d840c161ad.
- 02-final.png: pedido 163, concluído 169; 2493318 bytes; SHA256 5b5a9766fc80a0b975f0ddbebcad3b855fadfbbbc552dd714f627e65481c4a66.
- Ambos PNG abertos em ferramenta de visão: LOADING e dica Shrines, sem janela RSTV/nome de personagem/chat/dado pessoal visível. Isso não é revisão visual do mod nem sanitização automática de imagem.
- CurrentGuiState=ChoosingCharacter e cena_ativa vazia são metadados do arranque/componente, não prova de Select Party desenhada. Único TMP ativo/parseado observado: 'Path Chosen!', frame 158, pixel_visivel=NAO_AFIRMADO. Não aparece como tal no PNG: não confundir componente com pixel.
- Owners Harmony vivos: com.gumatos.aut4probe em GUIManager.Update e OptionsManager.Localize; Tooltip.ShowTooltip/ShowSkillTooltip sem owners. Não prova RSTV, ausente nesta rodada.

## Detector, relatório, marcação e exportação

Executados por fechar_coleta.py e verificar_final.py sobre o JSON real preservado; sem nova abertura de jogo.

- Detector campos básicos objeto/caminho/fonte/shader: CONFIRMADA/exit 0. Critério estritamente leitura de objetos, sem expectativa de gameplay.
- Tentativa de negativo por 'personagem ausente': CONFIRMADA/exit 0; hipótese do harness inválida, pois campo contém contexto lido com tem_personagem_selecionado=false/personagem=null. Não contar esse controle como validado nem como personagem presente.
- Controle rotulado fixture sobre cópia: exit 2, não confirma runtime.
- Negativo correto: plano com expectativa fonte deliberadamente incompatível, mesmo JSON real original -> NO/exit 1. Pós-processamento offline de captura runtime, não controle em jogo/Runner nem mod sem kit.
- Viewer KIT08 real: relatorio.html, 37578 bytes, SHA256 41820fd6c5b7f1cad9889336789c8daa8ff74fca9499f9e57d40e6773921a8c6; exit 2, 21 NAO_EXERCITADO, aprovação ausente. Sem IA/servidor/conta usados pelo CLI.
- Problema marcado explicitamente em problema-marcado.json: lacuna BOOT/LOADING sem marco RSTV. Marcação por arquivo no harness; NÃO foi interação de marcação numa UI do jogo/viewer.
- Exportador KIT07: exit 0, 5 payloads, sem upload; 5/5 paths/tamanhos/SHA lidos de volta e coincidentes no manifest. PNGs mantêm os hashes originais; texto sanitizado tem identidade nova, não fingir hash do original.
- relatorio.html foi EXCLUÍDO pelo exportador (formato_binario_desconhecido). O HTML original está separado; o export não contém o report completo. Não enfraqueci política do exportador.
- Manifest export SHA256 3901ca12dd66a9f7010c4659cc64d86925dcc7ac63307548dc40f2245ae5802f; upload=false.

O harness inicial de fechamento terminou exit 1 por comparar listas JSON com tuplas Python, gerando equal=false nas três árvores. Evidência falha conservada. Reconferência nova normaliza somente representação lista/tupla, preservando caminho/tamanho/hash e comprova igual=true. Não somar como execução única verde.

## Preservação e travas

Leitura independente pós-restauração:
- Diretorio real LocalLow 111/111, zero novos/removidos/alterados, igual=true; tipo real, sem backup *.kit16-real.
- Cópia isolada mudou somente Player.log/Player-prev.log e rotação de quatro arquivos analytics. Character/GlobalSaveData/SaveFile não alterados. Isso limita risco desta coleta, não aprova Cloud para navegação futura.
- Três árvores pessoais contra baseline histórica run699: BepInEx 53/53, LocalLow 111/111, Abyssus 5/5, todos caminhos/tamanhos/SHA iguais.
- PlayerPrefs export atual == antes da rodada: 31bb4e1f0530c749817c207d6843b07a2e9e0726c0e703b40d1bc705def0bd7b. Export readonly exit 0; registro não compartilhado.
- BepInEx isolado run702 removido. Área dados-iso run702 fica em scratch como prova; área residual antiga do run700 não alterada.
- 1343 arquivos fontes/baseline run699 conferidos: changed=[]. Alterações manuais preservadas.
- coletor.py 159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d; rstv.py f8d0aad12c4ae326092d29ad5d93e36d8553424332eab627c39b3ebe7357cab7; DLL do jogo/lib 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a, iguais.
- check_segredos/check_padroes_segredo/check_dupes/audita_docs exit 0 cada. Escopo versionado declarado; não aprovação universal dos artefatos novos.
- Estado final 14:01:14 BRT: STOLEN_PROCESS_COUNT=0; frente livre exit 0; HEAD d82894ebe95d97f26b7989a848372c691dcb8ef6, índice vazio, sem add/commit/push.

## Performance exploratória: dados crus, não aceite

7 amostras reais de processo, janela t+3.6880515000084415 a t+17.6329517000122s desde lançamento, PID 16064, somente BOOT/LOADING com AUT4Probe. Config e duração registradas; não foi recorder contínuo/Core/Adapter e não existe baseline comparável sem recorder.

RSS WorkingSet64 mínimo 127168512 bytes/máximo 1671184384; PrivateMemorySize64 mínimo 172507136/máximo 2481307648 bytes. CPU cumulativa bruta também em process-samples.json. São amostras discretas do boot, não pico garantido nem overhead atribuível ao recorder. Não extrapolar para gameplay.

FPS/tempo de quadro média/p95, I/O disco do recorder e delta com/sem recorder: NAO_EXERCITADO. Bytes dos PNG/export não são impacto de disco do recorder. Limiares e veredito passa/falha de performance: nenhum, conforme decisão B.

## Matriz de cobertura

| Critério | Estado real | Fronteira |
|---|---|---|
| Build/pacote/lifecycle local | PASSOU OFFLINE no run699, identidade reconferida | Não repetidos; update mesma versão não upgrade |
| Hash DLL instalada e carregada | PASSOU | AUT4Probe, não mods/recorder |
| Objetos vivos C1 | PASSOU leitura básica | Não tooltip RSTV/seleção de personagem |
| PNG Unity C2 | PASSOU | Loading, não Skills |
| Owners vivos C3 | PASSOU para instrumento | RSTV ausente |
| Rollback/PID C6–C7 | PASSOU local | Cloud remoto não isolado |
| Detector controle negativo | PASSOU pós-coleta offline | Não Runner/mod em jogo |
| Relatório e marcação/export | PARCIAL; critérios RSTV NAO_EXERCITADO | HTML separado/excluído; marcação JSON, não UI |
| Clique físico → janela → conteúdo/tooltip | NAO_EXERCITADO | Nenhum clique/navegação, RSTV não instalado |
| Runner ativo/cenários autorizados | NAO_EXERCITADO | RSTV-6/21/26/25b/geometria/shrines não exercitados |
| Mod funcionando sem kit | NAO_EXERCITADO | Nenhum mod produto carregado |
| Uso básico sem Hermes/IA/credenciais | PASSOU CLI offline histórico/postprocess | Experiência completa em jogo não demonstrada |
| Saves pessoais locais intactos | PASSOU nesta coleta | Não prova nuvem segura para saves divergentes |
| Comparação performance com/sem recorder | NAO_EXERCITADO | Amostras boot com AUT4 não substituem |
| Segundo ambiente/portabilidade | NAO_EXERCITADO | Somente esta máquina/conta |
| Revisão independente técnica/visual | PENDENTE | KIT-14R já existe; não liberado |
| Aceite humano/publicação | PENDENTE/NAO_EXERCITADO | Gates separados |

## Impedimento específico / decisão necessária

Não reabrir o antigo bloqueio de persistentDataPath nem pedir limiares. Falta proteção do Cloud pessoal para os cenários que podem escrever saves descartáveis. Opções operacionais a decidir pelo dono: autorizar explicitamente isolamento temporário da sincronização desse jogo com restauração/verificação da configuração, OU disponibilizar conta/ambiente Steam de teste independente do Cloud pessoal. Não executar alteração Steam/configuração do dono por inferência; não alegar que restauração do diretório local desfaz upload remoto.

Após resolver essa fronteira: retomar somente os cenários faltantes com uma frente, perfil descartável e hashes identificados; depois comparar recorder com/sem no mesmo cenário/janela, deixando medições indisponíveis NAO_EXERCITADO. Não repetir builds/lifecycle offline já entregues nem esta prova readonly sem motivo.

KIT-14R t_9ce7d260 foi inspecionado e continua todo dependente de KIT-14. Não criar revisão duplicada/same-card review nem concluir tarefa incompleta para liberá-lo. A coleta parcial exige revisão independente quando o handoff completo puder ocorrer.

## Artefatos e selamento

Raiz: C:/dev/stolen-realm/scratch/kit/KIT-14-run702/.

- attempt02/probe/aut4probe.json + 01-ui.png/02-final.png; LogOutput-isolado.txt; commands.json; result.json; process-samples.json; provas isolamento (locais/privadas, fora do export).
- pos-coleta/origem-export/relatorio.html: HTML incompleto original; problema-marcado.json.
- pos-coleta/export-sanitizado/: export KIT07 lido de volta; não inclui saves/registro/DLLs/HTML.
- final/verification.json: reconferência real, negativo NO/exit 1, preservação e números crus.
- final/seal.json: 74 arquivos hashados e relidos pelo verificador, SHA256 502339c4f7d5473bc5e164be2c71b372d59f1b39b3d2d02cbfaf2300e848c4e8; não inclui saves/registro nem este documento posterior.
- Checkpoints novos docs/automacao/KIT-14-parte11.md até parte20.md; históricos preservados.

Estado de handoff: PARCIAL, bloqueio necessita decisão específica de isolamento Steam Cloud. Nenhum resultado sintético foi promovido a runtime.
