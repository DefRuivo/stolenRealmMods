# KIT-06R — parte 07: auditoria final e dependências lidas de volta

Complemento do parecer imutável docs/automacao/KIT-06R-revisao.md; não sobrescreve partes anteriores.

## Estado vivo final

Comando de comparação de SHA256 dos 188 arquivos da baseline: drift final=[tools/automacao/cenarios/kit09.py]. O checkpoint anterior tinha DRIFT=[]; outra frente alterou cenário KIT-09 durante esta revisão. Esse arquivo NÃO foi editado pelo reviewer638 nem usado para decidir os achados KIT-06. Hashes KIT-06 continuam os revisados; não alegar preservação absoluta final de todos188. Snapshot sandbox mantém a identidade original. Relatório anterior refere-se expressamente ao checkpoint, não à situação concorrente final.

Referências qualificadas parseadas no parecer: 3, todas apontam a arquivos/linhas existentes. verificacao-final.json guarda resultados e hashes:
- parecer KIT-06R-revisao.md ddcf019696e34df957ca092756c47192db58eccc5924cc24d456b02ee6532b36
- test_revisao_kit06.py 68d6283d2222260ca4792db7f84e5a2254d4d1ef8fb35b8d66d4aaa9b5b5cc7a
- harness-reviewer/Program.cs 1035cd9e8213a95436138cbabd3225225d1bc07ea7ab172629d34ddf913cd341

## Verificação externa do encaminhamento

kanban_show(t_73f0779f): KIT-06F existe, status todo, parent=t_f9f88c18, child=t_10584ca5, autoria desta revisão e nova instância requerida. kanban_show(t_10584ca5): KIT-15 inclui t_73f0779f entre pais e insatisfeitos, status todo. Gate de correção real confirmado.
Mesmo readback trouxe handoff KIT-07R t_96d0c463: REPROVADO; correção KIT-07F t_a7318a33 ativa e também gate de KIT-15. Consequentemente F8 deve usar disponibilidade condicionada à aprovação do exportador corrigido; API nominal acessível não autoriza pacote privado com exportador reprovado.

## Empacotamento das provas

Script novo finaliza_provas.py reusa FORMATOS/PADROES e heurística de entropia dos scanners do repo, apenas sobre arquivos explícitos desta revisão (não git ls-files, que ignoraria os untracked). Controle negativo em memória, sem valor de credencial gravado/impresso; saída só registra booleans. Gerará ZIP de relatórios/scripts/logs/evidência sintética, nunca sandbox/lib/DLL proprietária/build. Este item ainda depende da execução real do script; seus resultados estarão em handoff-verificado.json e handoff nativo. Não é pacote de mod nem publicação.

Parecer permanece REPROVADO com oito achados; UI/runtime NAO_EXERCITADO; correções NÃO executadas pelo reviewer. A conclusão do cartão encerra a revisão, não aprova entrega ou DoD e não libera KIT-15 sem KIT-06F.
