# KIT-13 — checkpoint 06 (run661)

Execução REAL: `python tools/automacao/kit13/prove_offline.py --out scratch/kit/KIT-13-run661` exit0.

Resultados (logs em scratch/kit/KIT-13-run661/logs, comandos estruturados em commands.json):
- 8 projetos: preflight com DeployToBepInEx=true recusado exit1 (alvo só de trava); false permitido exit0. Build só iniciou depois de exercer a trava.
- Builds ExampleMod, Harness, Standalone e CoreHarness: exit0, em sandbox sem .git e perfil do dono, propriedades DeployToBepInEx=false / GameManaged=game-refs local.
- Harness: 17 casos, exit0.
- Standalone com SDK/Adapter/Core fisicamente ausentes: exit0, count=2. Prova lógica offline, não BepInEx em jogo.
- CoreBridge contra serviço ICoreEvento falso: exit0, disabled=0/enabled=1. Compilou com Core vivo copiado; não prova serviço em jogo.
- Python: 14 testes, exit0.
- CLI decisão negada exit2; menu/skills exit0; fonte ausente exit1. Cenário trocado sem recompilar. Todos runtime_exercitado=false.
- Baseline/cópia conferidos pelo runner; detalhes em verification.json.

Próximo bloco obrigatório: provar cada teste reprovando com mutações seletivas reais dos fontes sandbox, não AssertionError artificial. Fonte vivo nunca mutado. Checar cobertura contra falsas negativas do próprio teste (JSON duplicado deve ser pacote de resto válido). Parecer independente segue pendente.
