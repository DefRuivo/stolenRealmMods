# KIT-06R — parte 03: resultados próprios reproduzidos e obstáculo de console

Sandbox própria: scratch/kit/KIT-06R-run638/sandbox. `python scratch/kit/KIT-06R-run638/prepara_revisao.py` copiou 188 arquivos vivos de tools/automacao + lib + props + entrega, tracked/untracked do escopo preservados, sem .git, bin/obj/caches/credenciais. Identidade: identidade-inicial.json; 9 hashes publicados conferem (hashes-entrega.json).

SHA256 medidos:
- controle_acesso.py 2e21f5396628f6141ea3fd66d5e60f815b95c0dfb0ac4a83c37157ee7c787e2f
- PonteControleRSTV.cs 6bfe3db1e50c18e441d266fca00bfba82c527680837a1a22d148455c5db6bbbf
- KIT-06-entrega.md a9cdca3b97e2bc7278bb6ffaaf597aba015f1dc0bb48be2c1954404105a3b8c3

## Preflight de deploy PASSOU

Projeto sentinela usa Directory.Build.props copiado. Execuções dotnet msbuild preflight.proj -t:Build:
- -p:DeployToBepInEx=true: exit 0, sentinela=True (controle negativo detecta efeito de deploy dentro da sandbox).
- default: exit 0, sentinela=False.
- -p:DeployToBepInEx=false: exit 0, sentinela=False.
Logs preflight-negativo/default/explicito.log; nenhum alvo aponta ao perfil do dono.

## Reexecuções do autor PASSOU no escopo nominal

Com cwd=sandbox, subprocessos reais:
- python tools/automacao/kit06/teste_controle_acesso.py: Ran 35 tests, OK, exit 0 (suite.log).
- python tools/automacao/kit06/contra_prova_kit06.py: 13 iscas, falhas 0, exit 0 (contra.log + logs em sandbox/scratch/kit/KIT-06/contra-prova).
- python .../contra_prova_kit06.py --autoteste: 9/9, exit 0 (autoteste.log).
- dotnet run --project tools/automacao/runtime/harness-controle -p:DeployToBepInEx=false: 44 OK, 0 FALHA, exit 0 (harness.log); export local realmente lido pelo harness.

## Build INDETERMINADO nesta tentativa

dotnet build sandbox/.../KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false chegou a executar, mas coleta de stdout via subprocess text=True falhou com UnicodeDecodeError byte 0xc6 e depois TypeError por stdout=None. Comando agregado exit 1; resultado de build não é verde. Arquivos do repo são UTF-8; este obstáculo é encoding do console nativo, não do fonte. Próxima abordagem: capturar bytes e conservar output binário, decodificar apenas cópia para inspeção. Não repetir text=True.

Inspeção adicional: SRAdapterPlugin.cs integralmente lido; Update apenas usa PontePassivaRSTV e Input.GetMouseButtonDown; nenhuma instância/chamada de PonteControleRSTV. Não há UI/engine input entregue. Nenhuma instalação, jogo/save, foco ou encerramento executado.
