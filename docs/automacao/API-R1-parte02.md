# API-R1 — parte 02: evidência de extração e decisão de reconstrução

Pacote obtido pela API pública e CDN, apenas no workspace privado `scratch/reference.zip`. A rota de download informada na API respondeu HTTP 403; a CDN pública respondeu e forneceu ZIP de 146.883 bytes (o tamanho exato será conferido no relatório canônico). SHA-256 do ZIP: `86429189e877cb401e8501214e7500b53431139dfa2996ab90e1a8facd431bf8`.

Comandos reproduzíveis, a partir do workspace:

- `ilspycmd -o scratch/decompiled scratch/reference/plugins/*.dll`
- `dotnet build probe/Probe.csproj -o probe/out -p:DeployToBepInEx=false`
- `dotnet probe/out/Probe.dll surface <DLL-inspecionada>`
- `dotnet probe/out/Probe.dll targets C:/dev/stolen-realm/lib/Assembly-CSharp.dll`

A inspeção de metadados encontrou 57 tipos públicos (incluindo aninhados), 271 métodos/construtores públicos, 143 campos, 50 propriedades e 13 eventos. Accessors de propriedade/evento não entram na contagem de métodos. O código decompilado privado tem 8.143 linhas; não será copiado para a API própria. O ZIP não contém arquivo de licença: reconstrução por contratos e observação do jogo, sem copiar implementação nem atribuir a nós o código inspecionado. Publicação continua proibida nesta tarefa.

Identidade local lida de `E:/SteamLibrary/steamapps/appmanifest_1330000.acf`: AppID 1330000, build 25240684. Assembly-CSharp.dll local e lib/ têm SHA-256 idêntico: `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`. AssemblyVersion é 0.0.0.0 e NÃO identifica versão do jogo. `globalgamemanagers` contém Unity 2022.3.62f2 e string length-prefixed 1.3.1; identificação estrutural do PlayerSettings ainda pendente nesta parte.

Achados de compatibilidade, no JSON scratch/game-targets.json:

- O tipo correto do singleton é `Burst2Flame.Game`; resolver simplesmente `Game` é ambíguo.
- `Character.ModifyHealth` tem overloads de 5 e 8 parâmetros e AMBOS são estáticos. Não é correto presumir um `__instance` de alvo para esse hook.
- `OptionsManager.Localize(System.String,LanguageGender,Gender)` é estático e retorna string.
- `Burst2Flame.Game.Awake()`, `SkillTreeManager.UpdateSkillTreeItems()` e `GameLogic.StartNewTurn()` são de instância e retornam void.

Decisão: RealmApi 0.1.0 fornecerá uma base pequena executável (compatibilidade fechada por versão + hash, resolução exata, acesso a propriedades e quatro hooks observacionais). O inventário completo extraído será contrato de planejamento, NÃO promessa de suporte. Skills/actions/status, UI mutante, quests, enemies, persistência e combat modifiers serão cartões de implementação separados. Nada de métodos vazios retornando sucesso. Revisão independente da base precede sua adoção.

NAO_EXERCITADO: BepInEx/Unity dentro do jogo, criação de conteúdo, persistência/save, multiplayer e eventos de combate. Nenhum runtime autorizado.
