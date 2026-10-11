# KIT-09R — parte 04: discriminação e travas

## F7 — cobertura declarada não corresponde aos critérios
Execução independente: python scratch/kit/KIT-09R-run637/prova_controles.py, exit0.
Saída real: own-controls-green Ran 21 tests failures 0 errors 0 skipped 0; 21 execuções individuais own-control-red-00..20 Ran 1 tests failures 1 errors 0 skipped 0; own-controls-restored Ran 21 tests failures 0 errors 0 skipped 0.
Cada defeito em memória neutralizou somente a regra do critério-alvo importada da sandbox. Cada caso caiu em AssertionError específico, não ERROR/skip; restauração em finally. Os 21 controles independentes incluem render ausente (NAO_EXERCITADO), os demais defeitos observáveis (REPROVADO). Provas em own-control*.log e controls-proof.json.

O catálogo do autor tem 21 linhas CONTROLES, mas só 20 IDs únicos: falta KIT09-RSTV26-render-observado; personagem tem dois controles. Defeito funcional ON-DISK na sandbox: remover somente o guard de render ausente (if not render -> if False) mantém suite autor RESULTADO|PASSOU, exit0, mas o critério render-observado passa a OK sem render. SHA do mutante 823e7cda15505ced3efa0a9d1e42019434ac824e96885926663b2a3a56499825. Fonte restaurado byte a byte SHA a4f7587641174960affab6be73590071fe181c86de919dbb87cceb28025f6586; suite autor final exit0. Log render-mutant-author.log. F7 FALHOU: provar um placeholder vermelho não demonstra todos os critérios; a isca global sempre OK não substitui plantio seletivo.

## Travas realmente exercitadas
Executadas no repo vivo em leitura (scripts descobrem raiz/git; sandbox propositalmente não tem .git):
- python tools/check_segredos.py: exit0; 874 versionados, nenhum padrão de credencial.
- python tools/check_padroes_segredo.py: exit0; 874 versionados, nenhum padrão.
- python tools/check_dupes.py: exit0; TextFixes 101/TextAppends 197 sem duplicadas.
- python tools/audita_docs.py: exit0; nenhuma inconsistência encontrada.
Logs íntegros: scratch/kit/KIT-09R-run637/{nome-da-trava}.log; gates-summary.json. Limite: segredo/docs checam versionados, não aprovam os novos arquivos untracked; conferência dirigida de novos artefatos ainda necessária. Travas de pacote/versão/chave de mod, build C# e suite global runtime não aplicáveis a alterações só de revisão Python/docs; não foram marcadas verdes.

## Preservação e rota
Manifesto baseline de 456 arquivos comparado ao vivo: LIVE_CHANGED_OR_REMOVED []. Produto não alterado. test_kit09.py SHA vivo e1b05706f164b4c6a94a87bb7265e7f49942693ea46fb3ffa19a02827d50fd28.
hermes profile list exit0: somente default disponível (deepseek-flash indicado na configuração; não alterado). Correção será roteada para NOVA instância do implementador default, não executada pelo revisor run637; revisão independente obrigatória no handoff do conserto.
Filhos inspecionados: KIT-10 t_bbad760d, KIT-11 t_f2129aea, KIT-13 t_adc1fbfa, KIT-14 t_a1f38855. Nenhum é revisão deste cartão. Todos devem receber gate de correção antes de fechar este parecer REPROVADO; sem liberar entrega reprovada.

## Parecer preliminar
REPROVADO, 7 grupos acionáveis F1–F7. Runtime/desempenho/aceite humano NÃO_EXERCITADO. Conclusão da revisão não equivale a aprovação do KIT-09. Próximo bloco: abrir correção autocontida, ligar gates, entregar parecer final e arquivo de provas verificável.
