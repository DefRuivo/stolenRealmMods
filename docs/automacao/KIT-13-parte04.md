# KIT-13 — checkpoint 04 (run661)

Arquivos novos escritos em tools/automacao/kit13:
- SDK/KitSdk.csproj e RegistryV1.cs (API v1, IDisposable, limites, falha isolada).
- ExampleMod/{ExampleMod.csproj,CounterState.cs,ExamplePlugin.cs}: plugin independente.
- OptionalAdapter/{OptionalAdapter.csproj,CounterAdapter.cs}: código opcional, não requerido pelo mod.
- packages.py, scenario-v1.schema.json, examples/{menu,skills,state}.json.

Correção durante escrita: linter identificou fechamento de list comprehension errado em packages.py; patch aplicado e lint OK. Não foi ignorado nem alegado teste verde antes de executar.

Pacotes têm schema fechado em todos os objetos, API exata, IDs/targets limitados, allowlist 3 operações, duplicatas JSON recusadas, até 32 passos/64KiB/120s total e condições consumidas do KIT11. Nenhum campo de autorização/código/import é aceito. CLI só arquivo offline, resultado explicitamente runtime_exercitado=false.

API C# mantém snapshot de assinantes com identidade da inscrição, permite unregister no callback, rejeita reentrada de Publish, limite 64 inscrições/diagnósticos. Diagnóstico omite mensagens/stack de exceção; leitura/validação defeituosa não verde. Extensões em código são confiáveis, não sandbox de segurança.

Estado: ainda EM_ANDAMENTO, build/testes não executados. Próximo bloco: ponte Core opcional, harness e runner de provas.
