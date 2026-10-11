# KIT-14 — run704 / checkpoint 30: divergências esclarecidas sem alterar dados

Investigação readonly:
- Export histórico KIT16 era do ramo PAI HKCU/Software/Burst2Flame Entertainment, incluindo subramo Stolen Realm. analisar.py exportou somente Stolen Realm: diferença de escopo, não perda de PlayerPrefs.
- Novo export do mesmo ramo pai (reg export exit0) SHA25631bb4e1f… == ambas baselines antes e readbacks de restauração. Seção Stolen Realm também igual byte/texto ao export inicial de escopo menor. Nenhuma escrita corretiva em registro feita.
- Abyssus: 2 arquivos divergentes contra baseline histórica têm mtimes 14:49:42 -03, antes dos boots run704 (15:13+). Não atribuir ao Stolen Realm nem restaurar alterações do dono. Rollbacks imediatos mediram iguais ao início de cada rodada. Manifestos imediatos foram removidos pelo rollback; não há quatro arquivos preservados para comparação independente posterior.

reconferir.py resolveu corretamente registro/dados, mas saiu exit1 por exigir 4 manifestos imediatos que já não existem. Evidência reprovada preservada em reverification.json (SHA2567d428aec…). Não chamar essa execução verde nem repetir a mesma leitura. Fechamento terá verificação nova com escopo correto e lacuna de manifesto explicitada, mantendo histórico inicial.

ACHADO funcional do Adapter continua real: NullReferenceException no Awake antes de Core carregado. Não consertado nesta auditoria. Nada prova recorder ativo; os números medidos representam somente dois boots com plugins ausentes/presentes, telas de loading diferentes, sem delta de overhead válido.

Cloud permanece off em configuração; restauração ON depende de clique do dono e terá instrução curta no runbook. Nenhuma tentativa de input OS/contorno. Restante automatizável agora: relatório/avaliação da captura real, selamento e registro de cobertura; não reabrir jogo para repetir loading.
