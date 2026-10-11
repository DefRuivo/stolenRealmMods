# KIT-15R — parte 07: controles completos, paths e encaminhamento

Controle P1 refeito com defeito REAL de bytes no restore em cópia nova, não erro de arquivo inexistente: Ran1 FAIL1 ERROR0/skip0 exit1 (user originalwrong restore != user original). Evidência control-P1-bytes.json e logs/control-P1-bytes.txt. Com P2..P5 e baseline Ran5 OK: 5/5 positivos discriminantes. Preservados resultados da primeira tentativa inválida P1.

python test_extra_kit15.py: Ran3,FAIL3,ERROR0/skip0,EXTRA_EXIT1. Evidência extra-results.json:
- F12 manifesto core.id='../../outside' sobrescreve arquivo sintético fora de destino, rc0. Somente dentro da sandbox temporária, nenhum arquivo alheio real tocado.
- F12 recibo rel='../outside.txt' remove arquivo sintético fora do destino, rc0.
- F2 recibo {garbage:true} produz estado INSTALADO,0 arquivos,pacote/versão null,rc0.
Resultado conjunto próprio:30 testes,25FAIL/5OK,0ERROR/skip. Encaminhar F12 com alta severidade, sem ampliar exploração para perfil real.

hermes profile list (leitura) confirma somente perfil default existente; correção deverá usar esse perfil em NOVA instância implementadora, seguida de revisão nativa independente; run678 não implementará correção. Não alterada política/modelo/cron/prioridade.

Filhos inspecionados por kanban_show: t_a1f38855 KIT-14 (runtime pendente), t_b001720d KIT-G4 (gate bloqueado), t_f19310d3 KIT-G2 (gate bloqueado). Há comentário de autorização do G2 em09/10/2026, condicionado ao KIT-15R; NÃO aplicar como autorização nesta revisão reprovada. Será necessário acrescentar conserto+reconferência como dependência de TODOS os três antes de concluir o parecer, para que done de review não seja interpretado como aprovação do produto. Não executar, desbloquear nem publicar nos gates.

Pendentes somente empacotamento das provas, preservação final/hashes e registro nativo do parecer/reconferência.
