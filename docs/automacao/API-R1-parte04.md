# API-R1 — parte 04: primeiro build e smoke vermelho

`dotnet build api/Plugin/RealmApi.csproj -c Release -p:DeployToBepInEx=false` compilou RealmApi.dll e RealmApi.Core.dll: 0 avisos, 0 erros. Não existe target de deploy no novo projeto.

Primeira execução: `dotnet run --project api/Smoke/RealmApi.Smoke.csproj -c Release -p:DeployToBepInEx=false -- C:/dev/stolen-realm/lib/Assembly-CSharp.dll`.

Resultado real: Ran 25 tests; failures: 2. Passaram carregamento gerenciado do Core, gate, sinais, acesso, metadados dos quatro hooks no assembly do jogo, identidade/plugin attribute e negativas de alvo ausente/duplicado. Falharam os dois testes que aplicam Harmony no CLR .NET 6: `HarmonyLib.AccessTools` falha no inicializador (`MethodInvoker.GetHandler`, NullReferenceException). Evidência: workspace/scratch/smoke-first.txt.

A DLL Harmony de lib/ e do perfil tem SHA-256 idêntico `1a21cc03424fc82c3dd1346905d16494536b9595ae4162228d99fb7c285c1031`; não trocaremos a dependência para maquiar o resultado. Alternativa: testar com CLR .NET Framework, suportando o Core netstandard2.0 e mantendo a MESMA DLL Harmony. Isso não abre o jogo. Se ainda falhar, registrar bloqueio; não substituir detour por simulação e chamar de hook real.

NAO_EXERCITADO permanece: runtime BepInEx/Unity, gameplay, saves, multiplayer. Base não aprovada ainda; nenhum install/publicação ocorreu.
