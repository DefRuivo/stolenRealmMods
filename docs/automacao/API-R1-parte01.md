# API-R1 — parte 01: escopo e isolamento

Tarefa: t_b7f6fc4a. Repo autorizado: C:/dev/stolen-realm. Workspace: C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_b7f6fc4a.

Entrega própria: módulo api/, namespace Gumatos.RealmApi, GUID com.gumatos.realmapi. Não haverá instalação no perfil, alteração dos assemblies do jogo ou publicação. Artefatos de inspeção externa permanecem no scratch privado; nomes externos não entram no código/README do módulo.

Comandos já executados: `dotnet --version` retornou 6.0.428; `ilspycmd --version` retornou 8.2.0.7535; `hermes profile list` mostrou o perfil default. `git -C C:/dev/stolen-realm status --short` mostrou alterações anteriores em README.md, docs e ferramentas; esses arquivos não serão sobrescritos.

O filho t_ecb8f32d (INT-R1) depende desta tarefa e apenas analisa migração. Serão criados cartões especializados para implementação complementar e revisão independente com modelos explícitos. A API não implica migração automática de nenhum mod existente.

NAO_EXERCITADO: carregamento pelo BepInEx e hooks dentro do jogo, pois runtime não foi autorizado. Smoke offline será identificado como offline; não será apresentado como validação em jogo.

Próxima evidência: pacote público baixado em scratch, inventário de tipos e assinaturas, identidade lida da instalação local e plano de reconstrução. Qualquer recurso cuja compatibilidade não seja demonstrada ficará explicitamente sem suporte, não representado por stub silencioso.
