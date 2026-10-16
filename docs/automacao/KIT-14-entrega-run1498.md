# KIT-14 — run1498: árvore visível, recorder passivo reprovado

Tarefa t_a1f38855. Coletor default/run1498,15/10/2026. Estado: ENTREGA PARCIAL / NÃO CONCLUÍDA, task_accepted=false. Revisão independente da qualificação KIT14R t_9ce7d260 ainda dependente; nenhum aceite humano ou publicação. Esta rodada NÃO reedita provas anteriores.

## Resultado

Três boots reais com isolamento restaurado. O driver corrigido KIT-14F2 seleciona personagem, aceita party/dificuldade, inicializa HUD pelo caminho nativo e invoca RstvRunSkillTreeButton EXATO. Nos dois boots instrumentados, PNG final foi efetivamente inspecionado e mostra All Trees selecionada/Fire visível, não inventário/loading. Isto é efeito novo comprovado.

A qualificação ainda REPROVA tecnicamente: recorder ON com configs habilitadas registra apenas inicialização1/passivo0. Não dizer que só falta clique físico. Leitura dos objetos no frame do handler ainda não comprova árvore pós-render/tooltip/ciclo. Correção e revisão foram abertas no quadro para nova autoria, sem corrigir o instrumento durante a própria coleta para produzir falso verde.

## Execução e identidade

Raiz de evidências: C:/dev/stolen-realm/scratch/kit/KIT-14-run1498.

Comandos reais, da raiz do repo:

    python scratch/kit/KIT-14-run1498/test_campaign.py --mutant : exit1,6tests/1failure
    python scratch/kit/KIT-14-run1498/test_campaign.py : exit0,6tests
    python scratch/kit/KIT-14-run1498/campaign.py recorder-on : exit0
    python scratch/kit/KIT-14-run1498/campaign.py recorder-off : exit0
    python scratch/kit/KIT-14-run1498/campaign.py without-kit : exit0
    python scratch/kit/KIT-14-run1498/test_audit1498.py --mutant : exit1,9tests/2failures
    python scratch/kit/KIT-14-run1498/test_audit1498.py : exit0,9tests
    python scratch/kit/KIT-14-run1498/audit1498.py --output scratch/kit/KIT-14-run1498/verification-final.json : exit0 LIMITADO
    python scratch/kit/KIT-14-run1498/postprocess1498.py : exit0 de conformidade das saídas, não aceite

Logs separados *.console.log e test-*.log na raiz da campanha. Foram15 testes verdes, não a suíte120 do autor F2; não somei nem aleguei reexecução dessa suíte. Mutantes mudam somente cópias/memória dos testes, nunca binário instalado ou prova congelada.

Boots identificados:
- ON: KIT14-run1498-recorder-on-20261015-123958,PID17988,personagem Aspen,party1/HUD ativo. Alvo final no frame515; PNG01 pedido515/concluído522,PNG02 pedido522/concluído529.
- OFF: KIT14-run1498-recorder-off-20261015-124304,PID36528,personagem Bryce,party1/HUD ativo. Alvo final no frame482. Mesmo roteiro de sete etapas.
- Sem kit: KIT14-run1498-without-kit-20261015-124422,PID35188; somente carga/patches, sem navegação automatizada.

Roteiro: Play;Roguelike;Accept;@PartyCharacter;@PartyAccept;Accept;@HudInitialize. Alvo =RstvRunSkillTreeButton (igualdade, não substring). Button.onClick.Invoke, CharacterChoiceItem.MouseDown(0), API nativa de inicialização HUD. physical_click=false em todas as provas; chave histórica CliqueFisico é apenas guarda de prontidão/CanvasGroup/estabilidade, NÃO mouse físico.

Nenhum build nesta execução. Reutilizei fontes/assemblies CONGELADOS em F2/final/inputs, com hash antes da cópia e leitura de volta; sem promover sandbox ao principal. Todos os inputs por cenário têm inputs.json. Probe mede SHA do próprio assembly carregado; Core também fornece identidade runtime. RSTV/API têm identidade de entrada/cópia + log de carga, não SHA calculado pelo próprio RSTV carregado nem comprovação contra todas as fontes atuais.

Identidades principais:
- AUT4Probe.dll ba0f22b2608fc6b548cb12a9db433a51e3e9b0dfa726f0aacee32224c775f012.
- AUT4ProbePlugin.cs de7fb3ab0f3cd6d8a93715e1ad3d76f597bcbedef2a85ff17a6218d2ad26ee84.
- PartyDriver.cs1ce519ba01ac496f5bdf613b1c00d1f735df5434bef0d19711bb2e9d02e26cb4.
- Conjunto fontes F2 cc43e91968a584e4b91ca2c6ec95718adaad54bb6525da53de256189e4831f0c.
- Core0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d.
- Adapter d1b383c6cfeae198e77f96047ead39c1a54678f24888c110fed60a9561dded50.
- RSTV0.3.3 DLL1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc.
- RealmApi0.1.0 DLL764b72d84a976a534292a518d14177b76fdede070bf9979e649efc5df25d19d7 (Core/Hooks hashes em inputs.json).

## Achado técnico e detector que reprova

ON: Core habilitado=true; Adapter habilitado=true/passivoHabilitado=true, configs resultantes preservadas. Livro geral contém só inicialização; passivo.eventos_total=0 e passivo_book_events=0. OFF não produz eventos. Saída do Core realmente lida antes do rollback, não arquivo ausente contado como zero. BINÁRIO Adapter atual na árvore principal tem o mesmo SHA da rodada, portanto não se trata de simplesmente consumir uma cópia atual omitida.

SRAdapterPlugin.cs:158..186 produz a observação em Update do BaseUnityPlugin. AUT4ProbePlugin.cs:1699..1772 lê ResultadoFinal, não garante execução do produtor. Lifecycle é HIPÓTESE DIRIGIDA para o implementador provar, não causa definitiva declarada por esta coleta. Não invoquei AlimentarPassivo com estados inventados para obter contagem.

PipelinePassivo.cs:395 emite runtime="NAO_EXERCITADO" constante. Corrigi SOMENTE o auditor novo desta rodada após ler esse contrato: exigir string hipotética EXERCITADO seria erro do teste. Auditor final usa contagem/livro passivo/identidade/sessão, preservando o campo original; a prova real ON continua reprovada. verification.json inicial preservado, verification-final.json é o final. Nenhum gate de produto/histórico foi enfraquecido.

Gate histórico rstv-full e audit.py foram copiados BYTE A BYTE. rstv-full exit1; bounded exit0. Gate SHA ca3d859a25fc40415987082f32a3d1e30d06f88c3bbc8ae6d104b4b7f25fa2b4. A frase genérica antiga diz que não viu janela; nesta campanha PNG confirma árvore, mas clique físico/tooltip/ciclo continuam ausentes, portanto o gate integral permanece corretamente vermelho. Detector passivo REAL também exit1. Mutante de falso verde do auditor reprovou2 testes; retirar guarda Cloud do driver gerado reprovou1.

## Cobertura real

- Seleção descartável→HUD→handler exato→All Trees/Fire no PNG: PASSOU nesta campanha por handler+inspeção do agente, NÃO clique físico/aceite do dono.
- Recorder passivo habilitado: FALHOU,0 eventos reais. Não substituído por inicialização/fixture.
- Objetos RSTV pós-render/tooltip/abrir-fechar/skills-pontos/anti-duplicação: NAO_EXERCITADO/INDETERMINADO. Coleta no frame515 do handler tem texto All Trees atribuído mas render vazio, snapshots nulos; PNG final está em quadros posteriores. Não usar inventário/Event Window do dump para aprovar janela RSTV.
- Avaliador canônico rstv.py:7 NAO_EXERCITADO, alimentado somente por observação RstvAllSkillTreesTab real. Não fabricados esperado/observado para fechar critérios.
- Runner ativo e caso positivo/negativo de cenário em jogo: NAO_EXERCITADO. Negativos desta rodada são gates/testes de auditoria, não execução de gameplay pelo Runner.
- Marcação/export in-game: NAO_EXERCITADO. Problema marcado por JSON offline do coletor; KIT07 exportou esse dado real, não prova do atalho/UI.
- Mod sem kit: PASSOU apenas carga de exatamente2 plugins RealmApi/RSTV e15/15 patches. Sem AUT4/Core/Adapter carregados. Sem navegação autônoma, não fechar comportamento de árvore sem kit.
- Uso básico sem Hermes/IA/credenciais: relatório/export CLI local não usou IA/rede/segredo, mas host Hermes continuava ativo; campanha independente com host desligado NAO_EXERCITADO.
- Install/remove/rollback: PASSOU perfil temporário/registro/dados por efeito restaurado. Update/rollback de versões do pacote: NAO_EXERCITADO.
- Segundo ambiente runtime: NAO_EXERCITADO (mesma máquina/jogo; perfil descartável não prova portabilidade).
- Identidade de pacote release novo/atualidade de fontes RSTV: NAO_EXERCITADO. ZIP desta rodada é de evidências, não distribuição do kit/mod.
- Revisão técnica independente, design UI/UX humano, aceite final, publicação: pendentes/separados; nenhum verde parcial os substitui.

## Performance: coleta exploratória, sem limiar/causalidade

Decisão B de10/10 permanece. Intervalo comum conceitual Play→handler RSTV inclui menus/transições/loading, não árvore estável nem recorder ativo. ON236 frames/13.664s:17.271662763466043FPS e57.898305084745765ms/frame médios. OFF227 frames/13.501s aproximadamente:16.81356936523221FPS e59.475770925110126ms/frame. Delta real de Time.frameCount/realtime, não ticks do probe. Endpoints no verification-final.json.

Picos Whole boot WorkingSet64:ON2335907840/OFF2336165888 bytes; PrivateMemorySize64:ON3660591104/OFF3661205504. Amostras21/16, durações50.993044700007886/39.983672700007446s. Bytes persistidos probe6401418/6607990. Sem-kit pico WS1982881792/Private3151347712,18amostras/45.915252799983136s; é outro cenário e não entra em comparação ON/OFF.

Sem repetição estatística, personagens/nome diferentes, memória inclui loading, sem distribuição de frame/p95 ou I/O total de disco. Não inferir overhead/custo nulo; não existe comparação de recorder EM ATIVIDADE porque ON0 passivos. Ausência de limite não transforma coleta em aprovação de performance.

## Integridade/restauração

Antes de CADA boot: jogo fechado, Cloud per-app explicitamente0 no sharedconfig, front-unica adquirido, snapshot IMEDIATO de dados/perfil/outro jogo, PlayerPrefs exportado, junction KIT16 e saves pessoais em quarentena fora do caminho do jogo; personagem gerado em diretório vazio descartável, nunca save pessoal como seed.

Depois de cada boot: fechamento gracioso do PID próprio, coleta antes do rollback, PlayerPrefs byte/hash igual, dados115/perfil53/outro jogo5 idênticos por conjunto/tamanho/SHA; zero novo/removido/alterado. Auditor separado do driver recalculou árvores VIVAS contra snapshot da última rodada com o mesmo resultado. Readback12:53 BRT: jogo0,sem junction/backup/perfil temporário,lock livre. Nenhuma força de processo de terceiros.

Cloud0 inicial/durante/final PRESERVADO; não religada nem alterada por esta rodada, campanha encadeada de runtime ainda pendente. Steam alterou remotecache mesmo off; não afirmar servidor/cache intocados. Restauração do toggle inicial não é religamento: retorno global da campanha ao estado desejado pelo dono permanece operacional, sem quebrar próximos cartões que exigem Cloud off.

Player.log por padrões explícitos no verification-final.json: Error/Fatal0 e exceções nomeadas0; Convex Mesh ON2/OFF1/sem-kit1, DontDestroyOnLoad1cada,frustum0. Não chamar log inteiramente limpo. WIP manual preexistente preservado. git diff --check/cached --check exit0; único diff tracked anterior EV-R2-NORMAL-b08-parte144.md, não atribuído ao KIT. Nenhum commit/push/build/deploy Default/alteração de mod/jogo.

## Relatório, marcação e export reais

postprocess/share-input/report.html: HTML local com PNG da árvore,7 NAO_EXERCITADO,aprovação ausente,CLI exit2. report-input.json contém critérios reais; problema-marcado.json registra recorder zero em JSON offline, não UI/atalho.

KIT07 exit0:4 payloads/3851971bytes,1exclusão report.html por motivo EXATO formato_binario_desconhecido (não limite de tamanho). Quatro bytes/SHA lidos de volta com igualdade. PNGs inspecionados mostram personagens descartáveis; exportador não sanitiza imagem e não afirmamos isso. HTML original permanece local, sem upload. Probe bruto ficou imutável.

## Encaminhamento sem falso gate humano

KIT-14F3 t_26bf5ae7: nova instância de implementação do produtor passivo, causa a provar/opt-in/controle negativo/boot real. KIT-14F3R t_59d49835: revisor independente refuta fonte/assembly/efeitos/segurança. Grafo real: correção→revisão→esta retomada KIT14. Somente perfil default disponível; novas instâncias/papéis separados, não revisão do próprio coletor. Não alterei políticas/modelos/crons; cartões usam a mesma rota de pensamento do KIT14.

Ambos lidos de volta no banco: correção ready/revisão todo, assignee default, gpt-6.1-sol/openai-codex. Sem duplicata ativa localizada. Cartão atual aguardará DEPENDÊNCIA TÉCNICA, não precisa de nova autorização de teste/limiares nem do dono clicar para consertar recorder. KIT14R/BP5/LEVEL inspecionados, não liberados por falsa conclusão. Roteiro humano residual separado em KIT-14-runbook-residual-run1498.md; nada para o dono executar agora para corrigir este achado.

Identidade final verification-final.json:0f70bca7e29432a49685c841a9caa42d4f77461d4dd9e9f7e5bc82d194f927bc. Pacote/selo desta entrega serão gerados em KIT-14-run1498 com seleção explícita, leitura por entrada/CRC/SHA e sem DLLs/.reg/saves/baselines privados. Checkpoints65..71 registram progressão; relatório parcial não fecha o aceite integral.
