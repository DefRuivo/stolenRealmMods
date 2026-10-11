# KIT-13 — checkpoint 09 (run661)

Execuções reais finais:
- prove_offline.py --out scratch/kit/KIT-13-run661-final: exit0 (8 preflights negativos+8 positivos,4 builds,17 testesC#,14 unittest,Standalone/CoreBridge e4 CLIs).
- prove_mutations.py ... --group py: exit0,14/14 casos 0->1->0.
- prove_mutations.py ... --group cs: exit0,17/17 casos 0->1->0, build de cada mutante exit0 antes de exigir FAIL do caso correspondente.
- prove_mutations.py ... --group extra: exit0,2/2 Standalone/CoreBridge 0->1->0.

Total de mutações reais confirmadas por ferramenta:33, todas fontes sandbox restauradas por SHA; testes não foram enfraquecidos para aceitar mutantes. Logs individuais/resultados preservados nos diretórios mutations-{py,cs,extra}. Nenhum código de produto/jogo/perfil alterado.

Próximo bloco: ler saída final/hash das DLLs, inspecionar referências CLR do mod/estado (controle negativo adaptador que depende do SDK), scanners repo+escopo novo, pacote de fonte e entrega/handoff. Runtime/jogo/BepInEx carregado/UX/IL2CPP/publicação seguem NÃO_EXERCITADO.
