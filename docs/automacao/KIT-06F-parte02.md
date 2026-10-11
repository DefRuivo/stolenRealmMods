# KIT-06F — parte 02: metodo e alvo de aceitacao

Alvo binario de aceitacao (senao a correcao nao vale):
- oraculo Python do reviewer: 14 testes, 0 FAIL, exit0 (antes 10 FAIL);
- oraculo C# do reviewer: 12 OK / 0 FAIL, exit0 (antes 8 FAIL);
- suite do autor: OK (35 testes originais + 10 novos de contrato), exit0;
- contra-prova: TODOS os 45 testes com prova negativa (37 defeitos, conjunto exato);
- harness C#: 44 OK/0 FALHA no normal; --defeito com CONJUNTO EXATO; defeito
  inventado recusado (exit2);
- build isolada -p:DeployToBepInEx=false, preflight deploy exercitado.

Oráculos do reviewer copiados para scratch/kit/KIT-06F-run641 (oraculo_revisor_py.py,
oraculo-cs/) apontando aos FONTES VIVOS; o fonte ORIGINAL do reviewer em
scratch/kit/KIT-06R-run638 foi PRESERVADO para reconferencia independente.
