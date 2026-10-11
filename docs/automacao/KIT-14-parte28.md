# KIT-14 — run704 / checkpoint 28: duas execuções reais

Preflight novo scratch/kit/KIT-14-run704/preflight.json, exit0, SHA256 b051a6e849e74a72c9ac63fdbb0dfa69b5138a7efe7334854feb106fedac6a77: app cloudenabled=0; produção 111/111 sem diferença contra KIT16.

Guardas novas do harness: Ran 7 tests/OK/exit0; mutante seletivo removendo guarda Cloud resultou Ran 7 tests/1 FAIL/exit1. AST comprova que finally histórico foi preservado, exceto leitura adicional de Cloud; não equivale a revisão independente. Logs test-green.log/test-red.log preservados.

Duas rodadas autorizadas reais, sem clique OS:
- without-passive: sessão KIT14-run704-without-passive-readonly-20261010-151314, PID21736, janela externa 60.81786050001392s, AUT4 Navegar=true, Core/Adapter ausentes.
- with-passive: sessão KIT14-run704-with-passive-readonly-20261010-151528, PID19004, janela 60.83437729999423s, AUT4 Navegar=true, Core/Adapter opt-ins true/passivo true.
- Diretório consumido pelo jogo comprovado junction para área própria VAZIA antes de boot; cópia pessoal mantida fora desse caminho e não usada/selecionada. Produto RSTV não instalado nessas rodadas.
- Ambas terminaram harness exit0, probe CONCLUIDO, 2 PNG por rodada, game_closed=true; comandos de restauração registrados. Ainda conferir efeitos independentemente.
- AUT4 instalada SHA256 679365e2…; Core 4b318522…; Adapter ab2da758… são builds sandbox run699, sem build/deploy pessoal novo.

Cloud ficou cloudenabled=0 antes/depois de cada boot. ATENÇÃO: remotecache.mtime mudou apesar do toggle off (novo mtime 15:13:43 e 15:15:40). Isso refuta a heurística 'mtime mudou = necessariamente sync ativo'. Não é prova de upload remoto; investigar/registrar com estado específico do app, sem alegar nuvem inspecionada. Não editar Steam/VDF para forçar interpretação.

Próximo bloco: ler JSON/PNG/logs reais, verificar navegação e eventos passivos, consolidar números crus sem atribuir overhead efetivo quando recorder não comprovado, e preparar runbook para passos físicos/restauração Cloud pelo dono. Harness reutiliza scripts KIT03/KIT16; nenhum produto alterado.
