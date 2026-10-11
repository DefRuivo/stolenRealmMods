# KIT-10R — run663 — parte07: preservação e higiene

`python scratch/kit/KIT-10R-run663/verify_evidence.py` executou em leitura:
- baseline1156 arquivos: live_changed=[] e sandbox_changed=[];
- no_git=true, no_dll=true;
- hashes dos sete arquivos principais conferidos, sem drift;
- SHA suite própria: e7eddb6f366213fe09d296f1de74cd4fdbc6d3e7d23c252bc1774129729dd71e;
- SHA suite envelope: 2d3a40b5f6099dc2d954bb4222953bcfe5a8946486bd625540a181da90a51799;
- SHA driver controles: 582c50d22dd6209923cdf7fa594ae98f84a87452796c7fc1d4ff380a328de078.

Scanner dirigido nos203 arquivos do escopo novo (não só Git): formatos conhecidos0; heurístico2 candidatos, exit1 BRUTO mantido. Um é texto público `RESTORED_SHA=` seguido do SHA da fonte na parte06 (falso positivo pela concatenação do rótulo+hash); outro era literal sintético de controle de entropia no próprio harness. Não é credencial real. Mudei apenas o harness próprio para montar o segundo controle em memória por fragmentos e classificar primeiro candidato por igualdade EXATA com SHA computado. Nenhuma trava do repo modificada/enfraquecida. O scanner continuará com exit1 se restar candidato; classificação independente não converte saída bruta em verde. Controle em memória foi detectado por formato e entropia (dois true).

A próxima passagem --package terá resultado próprio distinto em verification-package.json, sem apagar verification.json inicial. ZIP conterá fontes sandbox semDLL/.git, resultados simulados e parecer; não é pacote de mod para instalação/publicação.

Comparação Git (não executada na primeira sequência por short-circuit após exit1 do scanner) será executada separadamente; não inferir resultado do comando pulado. Build/versões/pacotesMod/UIUX/runtime: NAO_EXERCITADO.
