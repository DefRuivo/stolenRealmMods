# API-R1 — parte 05: smoke verde, sem esconder as limitações

Alternativa exercitada: isolar a camada Unity netstandard2.1 do Core e do instalador Harmony netstandard2.0. As DLLs próprias são RealmApi.dll (plugin), RealmApi.Core.dll (contratos/sinais/acesso) e RealmApi.Hooks.dll (detours). O harness usa .NET Framework 4.7.2 e carrega as MESMAS DLLs Core/Hooks destinadas ao plugin. O plugin Unity é inspecionado por metadados; sua instanciação não é reivindicada.

A tentativa intermediária de compilar o plugin inteiro em netstandard2.0 foi rejeitada pelo compilador CS1705 porque UnityEngine.CoreModule exige netstandard 2.1. Não há supressão desse erro. A separação em três assemblies resolveu o conflito.

Comandos executados, com saída 0:

- `dotnet build C:/dev/stolen-realm/api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false` — 0 avisos, 0 erros.
- `dotnet build C:/dev/stolen-realm/api/Smoke/RealmApi.Smoke.csproj -c Release -p:DeployToBepInEx=false` — 0 avisos, 0 erros.
- `C:/dev/stolen-realm/api/Smoke/bin/Release/net472/RealmApi.Smoke.exe C:/dev/stolen-realm/lib/Assembly-CSharp.dll C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll` — Ran 25 tests; failures: 0.

Prova: workspace/scratch/smoke-net472-final.txt; implementação dos testes: api/Smoke/Program.cs. O teste real-harmony-hooks-dispatch-and-cleanup aplica e confirma owner/postfix, chama quatro métodos CLR locais e recebe quatro notificações. Verifica instância vs estático, argumentos/resultados preservados, isolamento de subscriber que lança, descarte idempotente e ausência de owner após remoção. foreign-owner-preserved verifica que patch de outro owner continua instalado.

Os métodos das fixtures são artificiais e explícitos no fonte. Não são resultados de gameplay. Os quatro alvos reais do jogo são conferidos separadamente por metadados e o SHA-256 do assembly local é conferido no teste. Casos negativos demonstram gate fechado, assinatura ausente/errada e alvo duplicado recusado.

NAO_EXERCITADO: BepInEx carregando o plugin, Application.version em execução, chamadas reais dos quatro hooks no Unity, mudanças de cena, saves/multiplayer, demais famílias de criação de conteúdo. Safety.EnableHooks=false por padrão. Nenhum arquivo foi copiado para o perfil do dono e o jogo não foi aberto.
