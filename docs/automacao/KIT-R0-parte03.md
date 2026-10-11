# KIT-R0 — checkpoint 03: identidade cruzada e sandbox

Run 623. Sandbox criada por cópia recursiva dos caminhos tracked/untracked enumerados por git, preservando conteúdos e sem .git/remotos: scratch/kit/KIT-R0-run623/sandbox. 1025 arquivos copiados. Exclusões explícitas scratch/, .git/, nul e nomes reservados de credenciais; inventário completo em scratch/kit/KIT-R0-run623/sandbox-inventory.json. Snapshot de hashes do workspace anterior aos testes em snapshot-before.json. Terminal exit 0. DLL/lib ignoradas pelo git não foram copiadas; nenhum build será feito nesta revisão, portanto pré-flight de deploy não será contornado.

Hashes recalculados diretamente do disco (exit 0):
- AUT4Probe.dll: 407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7.
- AUT4ProbePlugin.cs: 48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94.
- coletor.py: adb48dca024120db91b65e28b8842b7f303ca1725359cdaf4deab5530ae1dd46.
- controle_negativo.py: 053c0026f97c8541294c81e9d0011df4f3d970756f6ab8bc1d96a98fa9296659.
- roda_testes_runtime.py: 7906c1692bf349aff006039f73bbc8c59ef4e2a7a588210c348227be4dfb157e.
- Assembly-CSharp.dll: 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a.

Cruzamento bruto independente: LogOutput-copia.log de r4 contém Chainloader started, Loading AUT-4 Probe 0.1.0, linha de vida, dois ganchos e motor PlayerLoop ativo. Uma única carga de plugin, sem linhas de Error/Fatal no arquivo de 19 linhas. Isso corrobora identidade e carregamento, não prova por si eficácia visual.

KIT-G1-revisao distingue teto do executor e permissão humana; restringe somente leitura até boot/menu. Nenhum caveat ali cobre explicitamente a escrita do demonstrador ShowTooltip. A avaliação final deve separar prova bruta de ida-e-volta de autorização para intervenção UI e de renderização.

Localizados runner de 15 testes e 31 contra-provas, costura real do coletor e APIs dos avaliadores AUT-5/6/7. Suítes ainda NÃO executadas por esta instância. Próximo bloco: executar em sandbox e refutar por CLI sobre evidência real preservada; resultado positivo com expectativa independente e negativo divergente, sem nova rodada runtime.
