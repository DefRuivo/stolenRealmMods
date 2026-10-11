# KIT-06F — ENTREGA: correcao dos achados F1-F8 do KIT-06R

Cartao t_73f0779f. Rodada 641 (F1-F8) + rodada 650 (retorno do revisor: F6 no
caminho ANINHADO — ver `KIT-06F-parte07.md`). Perfil default. Offline: sem
instalar, sem jogo/save, sem publicar, sem Assembly-CSharp.dll, sem Bard, sem
gameplay.

## 1. Arquivos entregues (SHA256 medidos por sha256sum, rodada 650)
```
379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457  tools/automacao/runtime/controle_acesso.py
cad1bcc26cf10d4d754e8e96c076fc39c6dd13ca05486dbe73581e0163cc9084  tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs
e864ac9dbf86dba3403986b8bd6d5adfc43f9caf80a5f0672a927df1a9aebe81  tools/automacao/runtime/harness-controle/Program.cs
375edb6f28c1de10b2346ebc3aab248abc2f5be36caf9771e9b0eaff32e2b1fa  tools/automacao/kit06/teste_controle_acesso.py
d4a2cbb77313e3d63ceb7fb41869cc006e4eaa16375d53e27d77287321a7fbc4  tools/automacao/kit06/contra_prova_kit06.py
```

## 2. Execucoes reais (comando -> exit; rodada 650 em scratch/kit/KIT-06F-run650)
- oraculo Python do reviewer p/ fontes vivos: 14 testes, 0 FAIL, exit0
- oraculo C# do reviewer p/ fontes vivos: 12 OK / 0 FAIL, exit0
- suite do autor: Ran 46 tests OK exit0 (35 originais + 10 de contrato + 1 F6-aninhado)
- contra-prova por regra: 38 iscas, 0 falhas, exit0; cobertura AST 46/46, 0 fantasma
- autoteste do discriminador: 9/9 exit0; runner shell: VERDE exit0
- probe do revisor (F6 aninhado), PY e C#: ANTES (fonte pre-correcao) exit1
  contaminado; DEPOIS (fonte vivo) exit0 — `probe-antes/depois.log`, `csprobe-*.log`
- harness normal: 46 OK / 0 FALHA exit0; --defeito guard 3 falhas EXATAS exit0;
  --defeito inventado exit2; isca C# (harness vs adapter pre-correcao) normal
  exit1 com os 2 IDs novos e --defeito guard exit1 (falha EXTRA recusada)
- preflight deploy true/default/false: exit0 cada; sentinela true/false/false
- build sandbox -c Release -p:DeployToBepInEx=false: exit0, 0 Erros, 65 Avisos;
  perfil do dono (plugins+scripts) hash IDENTICO antes/depois

## 3. Limites honestos
- UI real/overlay, input do engine, runtime/pixels/foco: NAO_EXERCITADO (KIT-G2);
  PonteControleRSTV ainda nao e chamada por SRAdapterPlugin.Update.
- KIT-07: sem integracao efetiva (gate nao satisfeito); nao se chama o exportador
  reprovado nem se duplica sanitizacao.
- Nada commitado/add/pushado; sem deploy/instalacao/jogo/save/foco/publicacao.
- TEMP/TMP/TMPDIR direcionados ao scratch da tarefa; nenhuma escrita externa.

## 4. Proximo passo
Revisao independente em NOVA instancia (kanban_request_review no mesmo cartao),
reconferindo hashes/provas antes de conclusao e do gate KIT-15 (t_10584ca5).
