# KIT-14 — run1524: produtor comprovado, consumidor pós-render incompleto

Cartão t_a1f38855. Coletor default/run1524, 15/10/2026. ENTREGA PARCIAL / task_accepted=false. Não concluir KIT14, não liberar KIT14R/BP5/LEVEL por falso verde. Não houve build, edição de produto/fontes principais, deploy Default, commit, push ou publicação.

## Resultado principal

Três boots REAIS novos após revisão F3R: ON/OFF/sem-kit, driver exit0 cada. A correção do produtor F3 funciona na retomada: ON registra uma abertura real do painel atual e um PNG correlacionado; OFF não produz passivos. A árvore aparece em PNGs nativos vistos pelo agente. Isto não é clique físico nem aceite humano.

O bloqueio restante é TÉCNICO, não só residual humano: probe congelado lê objetos no frame do handler, retorna texto renderizado vazio e snapshots nulos e atribui owners dos funis, levando o avaliador canônico a excluir o único alvo RSTV. Tooltip/ciclo/Runner/marcação in-game ainda não exercitados. Nenhum critério foi afrouxado nem campo observado inventado.

## Execução e provas

Raiz: C:/dev/stolen-realm/scratch/kit/KIT-14-run1524.

Comandos realmente executados da raiz do repo:

    python scratch/kit/KIT-14-run1524/test_campaign.py --mutant    exit1 / 6 testes / 1 falha
    python scratch/kit/KIT-14-run1524/test_campaign.py             exit0 / 6 testes
    python scratch/kit/KIT-14-run1524/campaign.py --preflight     exit0 / jogo0,Cloud0,sem junction/backup/lock
    python scratch/kit/KIT-14-run1524/campaign.py recorder-on     exit0
    python scratch/kit/KIT-14-run1524/campaign.py recorder-off    exit0
    python scratch/kit/KIT-14-run1524/campaign.py without-kit    exit0
    python scratch/kit/KIT-14-run1524/audit1524.py               exit0 limitado
    python scratch/kit/KIT-14-run1524/test_audit.py --mutant     exit1 / 9 testes / 5 falhas
    python scratch/kit/KIT-14-run1524/test_audit.py              exit0 / 9 testes
    python scratch/kit/KIT-14-run1524/test_campaign.py           exit0 / 6 testes final pós-setattr
    python scratch/kit/KIT-14-run1524/postprocess.py            exit0 conformidade de saídas esperadas, NÃO aceite

Logs *.console.log e test-*.log preservados. São15 testes distintos, não21 por contar rerun; contagem agregada será calculada por finalize.py lendo os logs. Fixture sintética testa somente lógica do detector, nunca prova runtime. O mesmo detector F3/measure-panel.py avaliou ON novo exit0 e mutante REAL HISTÓRICO F3 exit1; não houve boot mutante novo nesta instância.

Sessões:
- ON KIT14-run1524-recorder-on-20261015-163344, PID7092, personagem descartável Tyler, party1/HUD ativo, handler exato RstvRunSkillTreeButton frame497.
- OFF KIT14-run1524-recorder-off-20261015-163545, PID7552, Eden, party1/HUD ativo, handler frame480. Mesmo roteiro de sete etapas.
- Sem-kit KIT14-run1524-without-kit-20261015-163717, PID31576; só carga, não navegação funcional.

Roteiro: Play;Roguelike;Accept;@PartyCharacter;@PartyAccept;Accept;@HudInitialize, alvo por igualdade =RstvRunSkillTreeButton. Button.onClick.Invoke/handlers nativos; physical_click=false. Config histórica CliqueFisico é guarda de prontidão, NÃO prova mouse físico.

## Identidade e ressalva do agregado herdado

Assemblies congelados conferidos antes da cópia, após instalar em perfil TEMPORÁRIO e/ou pelo hash calculado no runtime conforme disponibilidade:
- Probe AUT4Probe.dll ba0f22b2608fc6b548cb12a9db433a51e3e9b0dfa726f0aacee32224c775f012 (hash do próprio assembly no runtime).
- Adapter F3 revisado 010de6a67671f0a2a03654e54aebb3ca7ae64c11d50270c50c73b568e9dc72c9 (entrada/cópia/instalação/log, não cálculo de hash pelo próprio Adapter).
- Core0391f5d69f1bb9fba6cd76edbb44bf9a9447535877298d9e0df8c9786bd0e37d (identidade runtime também).
- RSTV0.3.3 DLL1d0b85e8d0f30d10c4fe7c4e044d30380537e8801a7d39875192459a2e51d5cc (entrada/cópia/log de carga15ganchos; não hash calculado pelo próprio RSTV).
- RealmApi0.1.0 DLL764b72d84a976a534292a518d14177b76fdede070bf9979e649efc5df25d19d7; Core/Hooks nos inputs.json individuais.

RESSALVA detectada e preservada: source_set_sha256 em inputs.json veio herdado de F2 (cc43e91968a584e4b91ca2c6ec95718adaad54bb6525da53de256189e4831f0c), mas inclusão das fontes F3 produz d3c7995b52cf4da33d9c830e3cc1025724afaf23bbaae09ceaee110ae250140d pelo algoritmo json.dumps dos *.cs/sort_keys. Não reescrevi os inputs/result originais nem aleguei correspondência do agregado. Os hashes INDIVIDUAIS de todos os arquivos são a identidade conferida; não houve rebuild para provar source→DLL independente nesta rodada. Suplemento por modo será gravado em final-readback.json; correção da preparação futura encaminhada ao F4 via comentário943. Não confundir HashFonte legado do cfg (DLL do probe) com hash real do conjunto de fontes.

Candidato consumido diretamente da sandbox F3 revisada; patch principal NÃO aplicado. Não reabrir lifecycle resolvido nem atribuir fontes atuais do principal ao candidato.

## Evento real e falha do consumidor

ON: evento75a9300ae430460ebc9f616d8d36a4e2, janela_aberta, motor bf81bd0658b74f3997231bcaa26933f8. Caminho GUI Manager/Character Menu Manager Window/RstvAllSkillTreesPanel, instance_id -416332, frame497. Captura cap-5e309613 confirmada499,1920790bytes, SHA2561bc5191fa931194be507aa8a5f7e50137544df369029a5caa58c5f611ea6bdbb. Arquivos lidos e hashes retidos ANTES de fechar/restaurar. Uma instalação,767callbacks,zero duplicados,271frames com painel,motor final0. Core livro2 eventos gerais/1passivo; probe consumiu1passivo/1captura. Pipeline mantém runtime=NAO_EXERCITADO literal; verdade inferida da trilha real, não rótulo forjado.

PNG passivo ON e final OFF efetivamente carregados pela ferramenta de visão: All Trees selecionada, Fire visível; Tyler/Eden, sem tooltip. Não há afirmação de simultaneidade entre JSON/PNG nem aprovação de design pelo dono.

Falhas reproduzidas:
1. recoleta.frame=497, igual ao handler497. Única observação RSTV é aba RstvAllSkillTreesTab, texto_bruto=All Trees/texto_renderizado="".
2. snapshot_antes e depois: personagem/skills/pontos nulos. AUT4ProbePlugin.cs:818–825 procura ReadOnlySession.Active/Target do caminho antigo;879 root RstvSkillTreesWindow, diferente do host atual observado.
3. owners=[com.gumatos.aut4probe] vem de OwnersDosFunils genérico (699,718,749,1016). Avaliador cenarios/rstv.py:281–283 exclui alvo por "sem owner do mod sob teste". As sete capacidades são NAO_EXERCITADO por esse motivo, não sete defeitos comprovados do produto.

Pós-render real gate exit1; full-rstv histórico SHAca3d859a25fc40415987082f32a3d1e30d06f88c3bbc8ae6d104b4b7f25fa2b4 intacto exit1; bounded0/produtor0 LIMITADOS. Não remover owner/trocar GUID/relaxar gate para ficar verde. postrender_ready é guarda estrutural adicional, não substitui sete capacidades canônicas nem prova funcional completa.

## Cobertura por critério

- PASSOU LIMITADO: rota descartável→party/HUD→handler→painel/PNG, recorder real ON e ausência OFF, evento/frame/sessão/captura, consumo pelo probe, motor removido.
- FALHOU COLETA: pós-render/snapshots/procedência do alvo; origem da falha acima. Não atribuir a gameplay.
- NAO_EXERCITADO: hover/tooltip interpretado/ciclo abrir-fechar/readonly skills-pontos/dependências geométricas completas. Não usar aba ou inventário residual como prova da árvore.
- NAO_EXERCITADO: Runner real positivo/negativo; bootstrap da rota não é Runner. Negativos offline/histórico não substituem esse aceite.
- NAO_EXERCITADO: marcar/exportar pela UI/atalho in-game; JSON offline/CLI exportam evidência, não exercitam essa interface.
- PASSOU SÓ CARGA sem kit: exatamente RealmApi0.1.0+RSTV0.3.3,15ganchos; sem AUT4/Core/Adapter. Funcionamento da árvore sem instrumentos continua não exercitado.
- PASSOU LIMITADO: install/remove/rollback do perfil temporário/registro/dados por efeito. Update/rollback entre versões de pacote não exercitado.
- NAO_EXERCITADO: uso integral com host Hermes desligado, segundo ambiente/instalação/máquina, portabilidade, identidade de pacote release novo/atualidade das fontes RSTV. ZIP desta rodada é evidência local, não distribuição.
- PENDENTE SEPARADO: revisão independente KIT14R, clique físico, juízo UI/UX e aceite final KIT-G4; nenhuma publicação/DoD concedido.

## Coleta exploratória de performance — sem veredito

Limiares dispensados pela decisão B10/10; sem mínimos/p95 inventados. ON/OFF mesmo roteiro/config conceitual, personagens descartáveis diferentes, inclui loading/transições. Play→handler: ON240frames/15.006s=15.99360255897641FPS/62.525ms médios; OFF223frames/12.869000000000002s=17.328463750097132FPS/57.70852017937221ms médios. Recorder ON emite o evento no final desse intervalo: NÃO é comparação causal de overhead em atividade/steady-state. Sem repetição estatística nem distribuição por frame.

Picos durante boot inteiro (inclui loading): ON WorkingSet2672594944/Private4088483840bytes,18amostras/45.16291369998362s; OFF2357932032/3629322240bytes,17amostras/41.512738800025545s. Sem-kit1956188160/3123453952bytes,18amostras/45.65185120003298s, cenário distinto, fora do A/B. Probe persistido ON6170822/OFF6361468bytes; não é I/O total de disco. Dados crus em process-samples.json/verification.json. Coleta ativa comparável permanece lacuna.

## Integridade e restauração

Antes de CADA boot: processo vazio, frente única adquirida, Cloud per-app0 confirmado, snapshot IMEDIATO production/perfil/outro-jogo e registro, junction KIT16 com dados vazios descartáveis, saves pessoais em quarentena fora do caminho do jogo. Nenhum save pessoal como seed.

Depois de CADA boot: shutdown gracioso do PID próprio, coleta antes do rollback, dados115/perfil53/outro jogo5 iguais por conjunto/tamanho/SHA, zero novo/removido/alterado; PlayerPrefs export antes/depois igual. Jogo fechado; sem junction/backup/perfil/dados temporários/lock. Auditor independente do driver recalculou árvores VIVAS iguais. Finalize.py repetirá leitura atual e registrará resultado, não presume sucesso pelo exit do launch.

Cloud app1330000 estava0 e continua0 (toggle inicial preservado, NÃO religado). Steam modificou remotecache; não alegar cache/servidor intocados. Devolução global ao estado desejado do dono permanece operacional na campanha encadeada.

Player.log por padrões explícitos no verification.json: Error/Fatal0 e exceções nomeadas0 nos três boots; Convex Mesh2/2/1, DontDestroyOnLoad1cada,frustum0. Não dizer "log limpo". Alteração tracked EV-R2-NORMAL-b08-parte144.md preexistente preservada; mudanças desta instância são novas docs/scripts/evidências e seção datada de KANBAN.md. Não há baseline recursiva de TODAS as fontes do repo nesta instância; não alego ausência de edição concorrente fora dos arquivos observados.

## Relatório/exportação local

Viewer KIT08 exit2:7NAO_EXERCITADO/aprovação ausente, HTML local com PNG. Problema pós-render marcado por JSON OFFLINE, não UI. KIT07 exit0:4payloads/3852629bytes/1exclusão report.html por formato_binario_desconhecido,sem upload. JSONs exportados reserializados têm igualdade semântica com origem; PNGs têm igualdade binária. Hash/tamanho contra manifest conferidos pelo fechamento. PNGs não são sanitizados automaticamente; imagens vistas mostram personagens descartáveis. Bruto aut4probe.json ficou intacto.

## Encaminhamento aplicado

KIT-14F4 t_5f50371d → KIT-14F4R t_821396a1 → retomada KIT14; cartões/edge lidos de volta. Autorias/NOVAS instâncias separadas do coletor1524 e entre implementação/revisão; só perfil default registrado, sem especialista inventado. Mesma rota/modelo do cartão atual; sem política/cron/prioridade global alterados. Hotspot AUT4ProbePlugin.cs registrado no cartão942, principal intacto. KIT14R t_9ce7d260 existente não duplicado/liberado; filhos BP5/LEVEL inspecionados e mantidos dependentes.

Aguardar dependência TÉCNICA F4R sem concluir KIT14. Não pedir nova autorização automática/limiares. Roteiro residual: docs/automacao/KIT-14-runbook-residual-run1524.md; não é pedido para o dono compensar coleta defeituosa. Marcadores/testes/gates/snapshots/ZIP são material para revisão futura, não autoaprovação.

Fechamento e hashes finais: scratch/kit/KIT-14-run1524/final-readback.json, seal.json, package-readback.json e checkpoint KIT-14-parte81.md. Pacote terá allowlist sem DLL/saves/.reg/baseline privada/decompilado, CRC e leitura de cada entrada por bytes/SHA. Não é release nem publicação; não atribuir resultado antes da execução do selamento.
