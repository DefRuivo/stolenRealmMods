# KIT-14 — run1498: driver e segurança antes da campanha

Checagem real em 15/10/2026 12:37 BRT: Get-Process não encontrou Stolen*. Fonte F2/driver.py e expanded.py integralmente lidos: prepara perfil temporário, adquire front-unica, snapshot imediato, junction KIT16, quarentena dos saves pessoais e PlayerPrefs, exige Cloud off antes de lançar Steam; coleta antes de rollback e só restaura com processo fechado. Fechamento limitado ao PID lançado e caminho do executável. Diretório novo por caso, sem sobrescrever evidência anterior.

Reutilização planejada: wrapper da própria campanha em scratch/kit/KIT-14-run1498 importará F2 e usará seus assemblies/fontes congelados, saída própria e sessão nova. Não executar F2/verify.py na origem porque reescreve verification.json histórico; reaproveitar funções puras de inspeção em saída nova. Não promover probe ao principal.

Filhos inspecionados: KIT14R t_9ce7d260 (revisão independente), LEVEL t_fc484826 (runtime depois do kit), BP5 t_49686933 (também depende LEVEL e gate de conteúdo). Nenhum trabalho dos filhos será executado aqui. A eventual conclusão desta fase deve liberar a revisão precriada, sem duplicar revisão same-card; só quando escopo técnico coletável estiver documentado sem falso aceite integral.

Estado anterior F2 distingue corretamente driver técnico verde de árvore não visível no PNG. A rodada nova verificará o efeito observado, não apenas onClick/CONCLUIDO. physical_click continuará false. Se houver falha técnica real, registrar achado em vez de empurrar como residual humano.
