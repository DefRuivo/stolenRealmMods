# KIT-13 — checkpoint 05 (run661)

Separação refinada para comprovação independente: ExampleState é biblioteca do estado do mod (sem SDK); ExampleMod plugin só depende dela+BepInEx/Unity. Standalone console só referencia ExampleState, permitindo rodar com SDK fisicamente ausente. OptionalAdapter só referencia SDK+ExampleState. Harness console exercita inscrições/eventos/leitores/validadores. Nenhum fonte pré-existente alterado.

Harness tem 17 casos nomeados incluindo unregister/reinscrição, removal durante Publish, exceção em evento/leitura/validação, ausente, reentrada, limites, Dispose aguardando callback e exemplo adaptado. test_packages.py tem 14 casos (com subcasos de inputs maliciosos/mal tipados). Inputs deliberadamente mal tipados provocam aviso Pyright no teste; não é dado de produção.

Falha segura de construção do adaptador refinada: state/registry null recusados antes da inscrição; sessão validada antes de criar lease. Mod isola listener opcional defeituoso.

Reuso de AUT3 descoberto: offline/aut3_lib.py expõe sanitiza, run_cmd, snapshots/hash. Próximo bloco usa run_cmd sanitizado para evidências e não duplica engines CIC/AUT. Ponte Core será explicitamente opcional e sem runtime presumido. Builds/testes ainda pendentes, sem alegação de PASSOU.
