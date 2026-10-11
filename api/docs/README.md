# RealmApi — documentação

Esta pasta contém os contratos extraídos e as evidências da API-base. Não contém código decompilado nem DLL de terceiros/jogo.

- contract-inventory.json: 57 tipos públicos e seus métodos, campos, propriedades e eventos, com aliases neutros de namespace/host. É inventário para planejar reconstrução; não é API compilável nem suporte prometido.
- game-targets.json: metadados dos pontos relevantes do assembly instalado, incluindo static/instance e overloads.
- target-game.json: AppID/build, hash e versão medida no objeto PlayerSettings da instalação local.
- smoke-result.json: resultado e escopo do smoke offline; as chamadas são em fixtures CLR e os alvos Unity são verificados apenas por metadados.
- smoke-output.txt: saída literal da última execução do smoke (exit code e linhas PASS/FAIL).
- ui-contract.json: superfície IMPLEMENTADA da família UI, gerada por metadados (`Inspect ui`) a partir de `RealmApi.dll` + `RealmApi.Core.dll` (API-R1-I2).
- ui-contract-diff.json: veredito da conformidade entre a superfície implementada e o contrato do inventário, com o controle negativo que prova que a comparação não passa por omissão (API-R1-I2).

Comando reprodutível das duas últimas (API-R1-I2):

    dotnet build api/tools/Inspect/Inspect.csproj -c Release
    dotnet run --project api/tools/Inspect/Inspect.csproj -c Release --no-build -- ui \
      api/Plugin/bin/Release/netstandard2.1/RealmApi.dll \
      api/Core/bin/Release/netstandard2.0/RealmApi.Core.dll > api/docs/ui-contract.json
    python api/tools/check_ui_contract.py     # -> CONFORME; exit 0

O módulo implementado hoje é descrito em ../README.md. A atualização segue recomparar superfície -> reconstruir código próprio -> build -> smoke offline -> autorização explícita de smoke Unity. Nenhum documento nesta pasta declara suporte às famílias ainda não implementadas — a partir da API-R1-I2 a família **UI** é a exceção declarada (implementada com alvo verificado por metadados, mutação por opt-in e runtime NÃO_EXERCITADO).
