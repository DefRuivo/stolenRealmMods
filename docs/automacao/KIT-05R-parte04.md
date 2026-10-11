# KIT-05R — parte 04: resultados na sandbox realmente isolada

## Isolamento confirmado

A cópia definitiva está em C:/Users/Pichau/AppData/Local/hermes/cache/scratch/kit/KIT-05R-run630-sandbox, FORA do repo. O driver verifica ausência de .git na sandbox e em TODOS os ancestrais, usa PYTHON explícito e tmp separado. Cópia dirigida dos 24 arquivos vivos: hashes origem=cópia em todos; inclui fontes tracked/untracked do escopo, sem Git/credenciais/perfil/bin/obj. Manifest completo: scratch/kit/KIT-05R-run630/isolated/manifest.json.

## Comando e resultados reais

`PYTHONDONTWRITEBYTECODE=1 python scratch/kit/KIT-05R-run630/preparar_e_executar.py`, exit 0 do driver de coleta (não do aceite). Todos os subprocessos e logs persistidos em scratch/kit/KIT-05R-run630/isolated/:

- suite-autores.log: python tools/automacao/kit05/teste_observacao_passiva.py -> Ran 19 tests, OK, exit 0.
- contra-prova-autores.log: python scratch/kit/KIT-05/contra_prova.py -> VERDE 7 iscas, exit 0.
- mutation-A…G.log: cada mutação executada novamente e inspecionada pelo reviewer; 7 casos exit 1, FAIL específico do teste esperado e zero ERROR. Defeito F também derruba test_captura_apos_atualizacao_visual.
- cli-fixture.log: CLI original -> exit 0, capturas=0, simultaneidade_afirmada=false. Só replay de fixture.
- suite-reviewer.log: python test_revisao_kit05.py -v -> Ran 16 tests, FAILED (failures=10), exit 1. Os MESMOS F1–F6 da parte03 reaparecem no isolamento correto. 6 positivos OK; nenhuma exceção/skip/timeout.
- runner-sem-git.log: bash tools/automacao/kit05/roda_testes_kit05.sh -> exit 2, `fatal: not a git repository`. A indisponibilidade do runner sem .git é real e agora separada da falha de PATH da primeira execução. Não foi fabricado .git para passar.

## SHA256 vivos conferidos

observacao_passiva.py = e3e89d5b2600a4d495465c55a612d60b48ba8746e59ad61b5a0e4ed6ffaac713
teste_observacao_passiva.py = bf7ae0e59901503be7f1a564f88da8bf4dcc4996bd9ee15557370f2ba9d496c6
runner = 05bc6a34b233c2c78f7b8e8a073470175b74c6a04a24bf32eb048fb6affd80a3
fixture = 6802717c901416f826fc5a020485893409871279c1559dd62d4134884f37cf73
contra_prova.py = 027e6ee37bcfbfe8f58510f18aadea8002c31b2982a449dc03e5e9b23a8b68a0
KIT-05-entrega.md = bf4c18e8c0fad79c3ebec75ef12853e0d2f0a6e9285516630277dc59228b505d
CorePlugin.cs = 8a415edb92693a37f39cebfa92295b5fa9e120fa544bcf2c247c672ba97ce905
SRAdapterPlugin.cs = 9687dbd4fc81399cf94808a5a14fa955b43e5cb327426da811380c5339662b01

## Parecer provisório

REPROVADO para aceite KIT-05. Lógica nominal passa, mas captura é afirmação sem efeito, pausa é parcial, dedup perde janela/gera spam, memória auxiliar e payload de replay são ilimitados, janela tardia apaga falha. Confirmar integração e formular correção única ao implementador, com gate nas dependências; sem implementar correções pelo reviewer. Runtime e desempenho NAO_EXERCITADO, não usados como justificativa para os defeitos offline.
