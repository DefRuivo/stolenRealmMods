# KIT-13R — leitura fria e readback independente

Comando Python dirigido executado no terminal, exit0: rehash de baseline.json em arquivos vivos (207 arquivos, mismatch=[]); leitura csproj/Directory.Build.props/CounterState/ExamplePlugin; listagem bare-mod, JSONs CLI e caudas dos logs.

Identidade real:
- SDK/RegistryV1.cs SHA256 9f2eabdd5da1a3796e7c191f241ff5687d9fb876d51a0bd03117ed1789187700
- packages.py SHA256 60f65437a167d5c08ba09647e1d45a265a1c7d28463793f57bb432546b5ea3c6
- lib/Assembly-CSharp.dll SHA256 8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a
Hashes iguais aos declarados no handoff do autor. Demais27 e ZIP ainda pendentes.

Logs lidos pelo reviewer: Ran17 tests; failures=0; OFFLINE_ONLY; Ran14 tests in0.452s OK. Standalone count=2; kit absent; CoreBridge disabled=0 enabled=1 ICoreEvento fake. Bare-mod só contém Standalone e Gumatos.KitExampleState, respectivos pdb/exe/json; sem SDK/Adapter/Core.

CLI readback: denied NAO_EXERCITADO false, menu OBSERVADO false, missing FALHOU false, skills OBSERVADO false (último campo runtime_exercitado). Não foi usado print de sucesso como prova de estado.

C5 dependência obrigatória REFUTADA para CounterState/Standalone, csproj ExampleMod e BepInDependency ausente. Plugin ainda não foi carregado no jogo; NAO_EXERCITADO. CounterAdapter é biblioteca opcional independente. CoreBridge usa ICoreEvento e guard hostObservationAuthorized && EstaHabilitado; não limpa auditoria. Erros C# de extensão são trusted-code, não sandbox de segurança.

Hipóteses a atacar sem assumir defeito: ciclo dispose/reinscrição durante Publish, read/validate de callbacks reentrantes; ponte disabled/null, perda de dado de evento; schema vs Python em tipos/limites; pacote hostil não importar código nem autorizar observação; lock ocupado e erro de fonte nunca verdes. Novos testes apenas em scratch, não produto. Nenhum achado fechado até executar.
