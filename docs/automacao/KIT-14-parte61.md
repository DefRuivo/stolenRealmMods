# KIT-14 — run1471 — montagem e rota não equivalem

Código vivo Plugin.cs:49..67 confirma dependência hard RealmApi>=0.1.0 e versão RSTV0.3.3. Dependência faltante será corrigida apenas na bancada, sem editar mod. Binários candidatos existentes encontrados em api/Plugin/bin/Release/netstandard2.1 (RealmApi.dll/Core/Hooks); seus contratos/hashes serão conferidos antes de usar.

Outra lacuna concreta: fonte RSTV Plugin.cs:22..25 declara botão Select Party REMOVIDO desde06/10. O alvo RstvRunSkillTreeButton é HUD da RUN, não party vazia. A rota Play;Roguelike;Accept só chega Select Party, portanto não comprova a janela mesmo com dependência corrigida. Não inventar que Choose Powerups abre o modal nem usar save do dono como atalho.

Necessário separar: boot de carregamento com dependência correta e básico sem kit são automatizáveis agora; acesso à superfície RSTV da run exige rota real de seleção/partida descartável, verificável pelo driver, não suposição. Coleta comparável poderá ser limitada ao mesmo menu/tela nativa e declarada como tal, sem prometer medir janela RSTV.

Zero alterações de produto/builds/novos boots até este checkpoint. Artefatos históricos preservados, não sobrescritos. Próximo bloco identifica dependências e extensão mínima do driver de bancada para cenários delimitados; negativa continuará reprovando cenário RSTV ausente.
