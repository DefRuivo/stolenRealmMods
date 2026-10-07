REVISAO INDEPENDENTE (revisor != autor; tentar REFUTAR, nao confirmar). Somente leitura do repo C:/dev/stolen-realm. Sem jogo, sem deploy, sem commit, sem publicacao, sem tocar em Assembly-CSharp.dll.

ESCOPO 1 - o conserto do RSTV-27 (rodape da tooltip read-only: mana/cooldown/alcance/blast/duracao):
- RoguelikeSkillTreeVisualizer/Patches.cs (postfix de Tooltip.get_TooltipCharacter, ~l.735-793): o valor do jogo deve VENCER (__result != null -> nao sobrescreve), fallback sem alvo armado, try/catch, log de 1a resolucao.
- RoguelikeSkillTreeVisualizer/SkillTreesTab.cs (hover read-only, ~l.2166-2182): arma ReadOnlySession.Target com ComAlvo/SemAlvo em try/finally.
- Testes: tools/testes/regras_rstv27.py, tools/testes/testes/puros/t_rstv27_rodape_personagem.py, tools/testes/prova-sandbox-rstv27.py, tools/testes/rstv27-rodape-prova-reprovando.log.
Hashes declarados pelo autor: SkillTreesTab.cs ecb75898ba136e9ab13eda9113694153ad6a9703fd0dcf0cf2e08d36b9d53624, Patches.cs 5f0d27f62e0aa0e9a3f5e0b5072c1665a91871c6220c45cf3d0bd64b00455b49.
Perguntas a refutar: (a) o postfix preenche o alvo em TODOS os caminhos read-only e nao vaza para o inventario? (b) o fallback/valor do jogo realmente vence? (c) o teste prende a SAIDA (valor resolvido para o alvo do modal) ou apenas a existencia da chamada? (d) a contra-prova em sandbox demonstra os 4 defeitos plantados reprovando (a)..(d) e o repo intacto? (e) a propriedade do JOGO e get-only (logo o conserto por postfix e o unico caminho)? Rode `python tools/testes/roda_testes.py --puros` voce mesmo e cite a saida; NAO rode dotnet build (build verde ja provado pelo autor - se julgar indispensavel, registre como INDETERMINADO).

ESCOPO 2 - verificar se os cartoes-filho ja podem ser fechados (o trabalho deles existe no disco?):
- t_4db38da9 "Teste que prende o VALOR do rodape resolvido para o alvo do modal" (esta preso em status running; agente nao esta mais vivo).
- t_29871204 "Contra-prova em sandbox fora do repo e build Release".
Diga, com prova, se o criterio de aceite de cada um esta satisfeito no disco atual (SIM/NAO + arquivo+linha+saida), para o pai aplicar a transicao.

FORMATO DO VEREDITO: item por item OK (com prova) / ACHADO (onde, o que) / INDETERMINADO; hash do que leu; o que voce NAO conseguiu exercitar. Escreva o relatorio em docs/cobertura/revisao/RSTV-27R-revisao.md (e so' esse arquivo). Nao crie nem altere cartoes do kanban. Nao commite. Todo numero/linha do jogo tem de vir do decompilado C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cs/Assembly-CSharp.decompiled.cs por `grep -n` com contexto (nunca ler o arquivo inteiro).
