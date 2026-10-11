# API-R1 — parte 06: fechamento da entrega (README, evidências consolidadas e limites)

Continua `docs/automacao/API-R1-parte05.md`. Rodada atual: run 740 (tarefa t_b7f6fc4a). Esta parte
**não** refaz a extração (partes 02–03) nem a construção da base (partes 04–05): consolida as evidências
do repo, fecha o README do módulo e reconfere build+smoke de ponta a ponta nesta rodada.

## 1. Reconferência completa nesta rodada (build + smoke)

Comando e resultado real (5 projetos, cada um `Release`):

```
dotnet build api/Core/RealmApi.Core.csproj   -c Release   -> 0 Aviso(s), 0 Erro(s)
dotnet build api/Hooks/RealmApi.Hooks.csproj -c Release   -> 0 Aviso(s), 0 Erro(s)
dotnet build api/Plugin/RealmApi.csproj      -c Release   -> 0 Aviso(s), 0 Erro(s)
dotnet build api/Smoke/RealmApi.Smoke.csproj -c Release   -> 0 Aviso(s), 0 Erro(s)
dotnet build api/tools/Inspect/Inspect.csproj -c Release  -> 0 Aviso(s), 0 Erro(s)

api/Smoke/bin/Release/net472/RealmApi.Smoke.exe \
  C:/dev/stolen-realm/lib/Assembly-CSharp.dll \
  C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll
  -> Ran 25 tests; failures: 0   (exit 0)
```

Saída bruta preservada em `api/docs/smoke-output.txt`; resumo estruturado em `api/docs/smoke-result.json`.
`RealmApi.dll` da rodada: sha256 `b52b66e5ce85149a624c8f09e695c3fb2d90ebf3f9746e068e727c68811d822c`.

## 2. Evidências versionadas no repo (todas geradas por comando, nenhuma escrita à mão de número)

| Arquivo | O que prova | Como foi produzido |
|---|---|---|
| `api/docs/contract-inventory.json` | superfície pública a reconstruir, anonimizada: 57 tipos, 271 métodos, 143 campos, 50 propriedades, 13 eventos | `Inspect surface` sobre o pacote em scratch (Mono.Cecil; não executa o alvo) |
| `api/docs/game-targets.json` | pontos do jogo com `isStatic` e overloads | `Inspect targets lib/Assembly-CSharp.dll` |
| `api/docs/target-game.json` | AppID 1330000, versão 1.3.1, build 25240684, Unity 2022.3.62f2, hash do Assembly-CSharp, com a proveniência de cada campo | valores medidos na instalação local + `sha256sum` |
| `api/docs/smoke-result.json` | 25 testes, 0 falhas, exit 0, escopo exercitado vs não exercitado | execução acima |
| `api/docs/smoke-output.txt` | saída bruta da suíte | cópia do log da execução |

Verificação de vazamento do nome do pacote inspecionado em todo o módulo (o padrão literal, com o nome do
pacote, fica somente no scratch privado; aqui ele é omitido de propósito — regra do dono):

```bash
grep -ril -E '<owner-do-pacote>|<nome-do-pacote>' api/   # -> sem resultado (0 arquivos)
```

Os quatro JSONs de `api/docs/` só contêm aliases neutros (`Gumatos.RealmApi.ContractReference.*`), o
nosso próprio namespace e valores medidos do jogo. O código-fonte do pacote inspecionado não foi copiado
e a DLL dele não está no repo (o pacote vive só em scratch, fora do repo).

## 3. README do módulo (entrega pedida)

`api/README.md` (novo nesta rodada) contém, na ordem pedida pelo aceite:

- **versão do jogo** alvo explícita, em tabela, com o comando de medição de cada campo e a regra
  fail-closed (versão **e** hash divergentes => zero hooks);
- **como usar**: `RealmHooks.Observed.Subscribe(...)`, `RealmAccess.ReadProperty(...)`, a tabela dos quatro
  hooks da base 0.1.0 e a config `Safety.EnableHooks` (padrão `false`);
- **como contribuir**: o que é um hook novo, o que exige decisão de arquitetura (formas de postfix além de
  `void`-instância e `string`-estático), proibições (não tocar/redistribuir `Assembly-CSharp.dll`, não
  referenciá-lo no plugin — coberto pelo teste `no-game-assembly-dependency`), exigência de prova por
  caminho/contagem/comando e o marcador `NÃO_EXERCITADO`;
- **como construir** (os cinco `dotnet build`) e a constatação de que **não existe alvo de deploy** em
  nenhum `.csproj` de `api/` — construir não instala nada;
- **como rodar o smoke** e o que ele responde (carrega? expõe? hooks respondem?);
- **como atualizar** quando o jogo mudar: 7 passos com comando reprodutível em cada um (reconferir
  identidade -> regerar `game-targets.json` -> recomparar assinaturas -> ajustar o código próprio, ou
  remover o hook se o ponto desapareceu, sem alvo substituto silencioso -> rebuild -> smoke `failures: 0`
  -> regravar evidências -> runtime só com autorização);
- **NÃO exercitado**: BepInEx carregando o plugin, gameplay, saves, multiplayer, deploy no perfil,
  famílias não implementadas, publicação.

## 4. Limites do aceite — o que fica declarado como não feito

- **Runtime BepInEx/Unity: NÃO_EXERCITADO.** O plugin está desabilitado por padrão (`Safety.EnableHooks=false`)
  e nenhuma execução dele no jogo ocorreu; smoke é offline, com fixtures CLR.
- **Publicação: não feita.** Ato separado e explicitamente autorizado (LIMITES do cartão).
- **Perfil r2modman: intocado.** Nenhum arquivo foi copiado para o perfil do dono e o jogo não foi aberto.
- **Assemblies do jogo: não redistribuídos e não modificados.** `lib/Assembly-CSharp.dll` é lido (hash e
  metadados) e é o mesmo binário já presente no repo; nada de `api/` o referencia em tempo de compilação.
- **Escopo da API 0.1.0: observacional.** Quatro hooks postfix; nenhuma capacidade de cancelar/substituir
  argumento ou resultado, e nenhuma promessa para as outras famílias do inventário.
- **Compilação independente da Unity:** o `RealmApi.Core`/`RealmApi.Hooks` saem em netstandard2.0 e são os
  mesmos carregados pelo smoke; o plugin netstandard2.1 isola a dependência `UnityEngine.CoreModule`
  (o CS1705 do netstandard2.0 não é suprimido, é evitado por separação de assemblies — parte 05).

## 5. Cartões abertos a partir daqui

- **Implementação** (modelo `deepseek-flash` / `deepseek`): a frente de implementação complementar do
  módulo, dependente deste cartão.
- **Revisão** (modelo `gpt-6.1-sol` / `openai-codex`): revisão independente desta API-base, dependente
  deste cartão.
- **INT-R1** (`t_ecb8f32d`), já existente como filho: só destrava com este cartão fechado — é a análise de
  migração/duplicação, não implementação.
