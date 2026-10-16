# KIT-14F3 — causa adicional medida: host obsoleto

Boot diagnóstico run1519/on exit0 (somente execução/restauração); detector original exit1, mantido como prova. Engine observada811 frames, ponte habilitada=true/mesmo_pipeline=true/transições0, nenhuma janela conhecida ativa. O problema residual não está no vínculo/opt-in.

PNG02-final realmente aberto pela ferramenta visual: cabeçalho Nevada, Character / Skill Tree / Fortunes / All Trees, Fire selecionado; trata-se da ABA de inventário, não da janela separada. Log real linhas57..73 confirma CharacterMenusManager.OpenCharacterMenu e painel sob Character Menu Manager Window. Fonte SkillTreesTab.cs:13..15 já declara janela separada aposentada; PanelName na linha82 é RstvAllSkillTreesPanel. A constante RstvSkillTreesWindow em SkillTreesWindow é apenas o host alternativo antigo. Decompilação da DLL congelada de SkillTreesTab realizada para frozen-tab.cs antes de corrigir o observador.

Consequência: adicionar ao instrumento o nome REAL do painel. O detector experimental run1502 hardcodifica o host antigo, portanto não poderá ser anunciado verde para esta rota. Ele será preservado; uma medição correlacionada específica do painel atual será adicionada separadamente, com os mesmos requisitos de sessão/frame/hash/captura e mutante obrigatório. Isto não substitui nem afrouxa full-rstv, cujos critérios e lacunas continuam inalterados. Não haverá mudança de produto/driver/probe para fabricar a janela esperada.

Restauração deste boot lida: production115/profile53/other-game5 sem diferenças, PlayerPrefs igual, jogo fechado e nenhum lock/junction/backup/perfil restante; Cloud configuração0 preservada (não implica inspeção do servidor).
