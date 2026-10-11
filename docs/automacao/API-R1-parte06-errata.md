# Errata — API-R1-parte06.md (seção 3)

**Referência:** `docs/automacao/API-R1-parte06.md`, §3 "README do módulo (entrega pedida)".

## D2-1: "não existe alvo de deploy" — incorreto

**Texto original (§3, item "como construir"):**

> como construir (os cinco `dotnet build`) e a constatação de que **não existe alvo de deploy** em
> nenhum `.csproj` de `api/` — construir não instala nada;

**Problema:** `api/Plugin/RealmApi.csproj` contém um alvo `DeployToBepInEx` (API-R1-I1). A constatação
está incorreta — existe um alvo de deploy, mas ele é condicional (opt-in via `-p:DeployToBepInEx=true`)
e o build padrão (sem a flag) não copia nada.

**Correção:** substituir por:

> como construir (os cinco `dotnet build`), a presença do alvo `DeployToBepInEx` no `RealmApi.csproj`
> (opt-in via `-p:DeployToBepInEx=true`) e a constatação de que o build padrão (sem a flag) não instala nada.

## D2-2: "versão do jogo alvo explícita, em tabela" — tabela superdeclara o gate

**Texto original (§3, primeiro item):**

> versão do jogo alvo explícita, em tabela, com o comando de medição de cada campo e a regra
> fail-closed (versão **e** hash divergentes => zero hooks);

**Problema:** a tabela original listava 5 campos sem distinguir quais são verificados em runtime
versus identidade documentada. A regra fail-closed (`ApiIdentity.Matches`) compara **apenas**
`Application.version` e SHA-256 do `Assembly-CSharp.dll` — os outros 3 campos (AppID, Build Steam,
Unity) são **identidade documentada** usados apenas na etapa de atualização. A tabela original
sugeria erroneamente que todos os 5 campos são gates em runtime.

**Correção:** a tabela deve incluir uma coluna "Verificado em runtime?" diferenciando os 2 campos
verificados em runtime (`Application.version`, SHA-256) dos 3 campos de identidade documentada
(AppID, Build Steam, Unity). Ver `api/README.md` versão corrigida (D3).

## D2-3: evidências listadas usam nome antigo `game-targets.json`

**Texto original (§2, tabela de evidências):**

| `api/docs/game-targets.json` | pontos do jogo com `isStatic` e overloads | `Inspect targets lib/Assembly-CSharp.dll` |

**Problema:** o arquivo foi renomeado para `api/docs/target-game.json` nas rodadas posteriores.
A menção em §2 é de uma rodada anterior; em §3, o texto descreve o README como se a tabela já
tivesse o gate correto (o que não era verdade naquela rodada).

**Correção:** não há ação de código — apenas registrar que `game-targets.json` foi renomeado
para `target-game.json` e que o §2 refere-se à rodada run 740, enquanto o README atualizado
reflecte a correção D3.

## D2-4: §3 omite que a seção "como atualizar" já menciona runtime como NÃO_EXERCITADO

**Texto original (§3, oitava bullet):**

> como atualizar quando o jogo mudar: 7 passos com comando reprodutível em cada um (...)
> -> regravar evidências -> runtime só com autorização);

**Problema:** o texto original contava "7 passos", mas a versão atual tem 8 passos (o runtime
com autorização foi separado no passo 8). A descrição "runtime só com autorização" está correta,
mas omite que o passo adicional foi adicionado para deixar mais explícito que o BepInEx real
é um ato separado.

**Correção:** ajustar de "7 passos" para "8 passos" e manter "runtime só com autorização".
