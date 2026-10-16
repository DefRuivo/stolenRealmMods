# BetterPortuguese — arquitetura decidida antes da implementação

BP-1 / `t_2c27e3f8`. Medição offline em 12/10/2026, UTC−03:00. Plugin futuro: `com.gumatos.betterportuguese`.

## 1. Decisão executiva

O BetterPortuguese será um plugin BepInEx separado, com dois datasets completos e imutáveis: original e corrigido. A substituição principal será um **postfix de `OptionsManager.GetLocalizationEntryList(string, LanguageChoice, bool)`**, devolvendo uma lista própria de `LocalizationEntry` para a chave exata e somente em português brasileiro. O jogo continuará escolhendo o gênero, fazendo os fallbacks e resolvendo os valores dinâmicos. Não modificar o asset, o dicionário global nem `Assembly-CSharp.dll`.

Não escolher como gancho principal um postfix que substitui cegamente `OptionsManager.Localize.__result`: isso perde a seleção de campos/entradas e pode apagar notas de outros mods. `Localize` permanece um ponto auxiliar para diagnóstico/contexto e integrações conhecidas, não um tradutor universal do texto final.

Config: `Conjunto = Corrigido` por padrão; `Original` volta à localização nativa vigente. `IntegracaoMods = true` por padrão, mas somente ativa adaptadores com versão/fingerprint e textos aprovados. O conteúdo de mods pertence a um namespace próprio; não contaminar a tabela original com notas de BetterTooltips. Os adaptadores não alteram fonte, materiais, cores existentes, números ou mecânicas.

Esta tarefa entrega decisão e evidência; **não implementa o mod**. A bancada C# incluída só executa o ordenador real do Harmony. Nenhum patch foi aplicado, nenhum jogo foi aberto, nada foi instalado/publicado.

## 2. Fontes, proveniência e cobertura realmente medida

### 2.1 Binário e arquivos

Os hashes abaixo foram medidos nesta rodada; os demais estão em `evidence/audit-report.json` no pacote BP-1.

| Fonte | SHA-256 |
|---|---|
| `C:/dev/stolen-realm/lib/Assembly-CSharp.dll` e DLL instalada em `Stolen Realm_Data/Managed/` — iguais | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` |
| `Stolen Realm_Data/resources.assets` — igual ao asset inventariado no LANG-R1 | `cbdfcd0fa8ecc338029024acfeb6f939593aa99a1f291ae65f4776fcb0dbc012` |
| `lib/0Harmony.dll`, assembly `0Harmony, Version=2.9.0.0` | `1a21cc03424fc82c3dd1346905d16494536b9595ae4162228d99fb7c285c1031` |
| `BetterTooltips/Patches/LocalizePatch.cs`, 214262 bytes, 2957 linhas | `a61987a46d63efa46e16df43c4859f29c914a07b5819f3e4c7b2167482bc3a69` |
| Anexo `LANG-R1-entrega-final.zip` de `t_2a6474ff` | `4d509f13280cd9e210593cfce08420dd8e48a75b4261f9faefee2e6afb6bf161` |
| Dentro desse ZIP: `entrega02/localizacao-ptbr.json`, fonte canônica | `dbc7d03f2ebe1e9b8bda33a22aaf577475eae0bad84c009b8979184e3a1411a2` |
| Dentro desse ZIP: `evidencias/odin-decodificado01/2547158-tabela.json` | `4561b71d673fbb7678fb9316e29e21408faeb9e4c98f29d16a8fe5ee42e2de0b` |

O ZIP está em `%USERPROFILE%/AppData/Local/hermes/kanban/attachments/t_2a6474ff/LANG-R1-entrega-final.zip`. **Usar `entrega02`, não tentativas anteriores.** O CSV é a interface editorial, separado por ponto e vírgula; a fonte lossless é o JSON. `chave_json`/`ptbr_json` servem para conferir escapes sem tratar proteção de planilha como parte do texto.

Decompilador usado: ILSpy CLI 8.2.0.7535. Artefato C#: 496226 linhas, SHA-256 `873a2d1dc153fcd7191100bb481f4bd681374f68e38c8241c0172e7c91465407`. As linhas neste documento se referem a **esse** artefato, não às numerações antigas de LANG-R1 ou dos comentários dos mods. As referências sempre nomeiam o símbolo; recortes com os números originais ficam em `evidence/game-symbols.txt` e `evidence/game-il.txt`.

### 2.2 Reconciliação chave a chave

`evidence/audit_sources.py` leu o dump existente, comparou as listas com Odin e recontou o corpus; não gerou um dataset de implementação.

| Medida | Resultado |
|---|---:|
| União das chaves dos idiomas no dump canônico | 9095 |
| Chaves efetivamente presentes no dicionário pt-BR | 9090 |
| Chaves da união ausentes no pt-BR | 5 |
| Objetos `LocalizationEntry` pt-BR | 8097 |
| Listas pt-BR vazias | 1286 |
| Chaves com algum texto utilizável | 7804 |
| Listas com mais de uma entrada | 191 |
| Chaves com campos Feminine/Masculine/Neutral preenchidos neste corpus | 0 |
| Componentes `ManualLocalization` adicionais | 2, com 14 entradas, sem pt-BR |
| Chaves pt-BR com espaço/quebra ao final | 391 |
| Chaves pt-BR contendo newline | 731 |

Provas executadas: 9095 registros CSV ↔ JSON iguais nos campos literais conferidos; 9090 listas canônicas ↔ listas Odin integralmente iguais, incluindo ordem e os nove campos; payload Odin declarado e consumido = 5508431 bytes; hash do asset instalado igual ao LANG-R1. A auditoria verifica essas relações e falha se divergem. A lista exata das cinco ausências, incluindo o espaço inicial de `LANG-00020`, está em `audit-report.json` (`LANG-00020`, `LANG-01365`, `LANG-02429`, `LANG-08194`, `LANG-08548`).

**9090/9090 significa cobertura das chaves da tabela, não 9090 traduções não vazias nem toda string do jogo.** Os 7804 textos de `AutomaticLocalization` isoladamente não bastam para reconstruir a localização original completa.

## 3. Onde vive o português e como o jogo o lê

### 3.1 Asset real, não uma biblioteca de localização presumida

`LocalizationData` herda `SerializedScriptableObject` (Sirenix/Odin), expondo:

    Dictionary<LanguageChoice, Dictionary<string, List<LocalizationEntry>>> LocalizationDictionary

Fonte: `LocalizationData.LocalizationDictionary`, C# l.24531–24535. O objeto aparece como MonoBehaviour no arquivo serializado Unity, mas a classe de código é um ScriptableObject serializado por Odin. Não é uma tabela I2, Unity Localization ou um hipotético `LanguageData`: o `LanguageData` do decompilado pertence ao Control Mapper e não é o proprietário deste dicionário.

O mapeamento real de Resources aponta `localization/localizationdataportuguesebrazil` para `resources.assets`, path ID **2547158**. A prova está no membro `evidencias/resource-map-localization-recorte.json` do ZIP LANG-R1; o payload é identificado como `LocalizationDataPortugueseBrazil` em `2547158-prova.json` (raw SHA-256 `b07006970f6dd8279c6347968cc8375b06317ca4a140c32f73a51eb142eeae1f`).

`LocalizationDataPathByLangauge.LocalizationDataPath` concatena `Localization/LocalizationData` + enum. `LocalizationDataHolder.GetLocalizationData` carrega com `Resources.Load<LocalizationData>`, mantém cache e descarrega o asset quando muda idioma; English retorna null. Fontes: C# l.137271–137319. `LanguageChoice.PortugueseBrazil` é a entrada enum de valor 10 neste binário (l.154352–154370); usar o **nome** no código, não cravar esse ordinal no patch.

### 3.2 Fluxo e motivo do gancho escolhido

`OptionsManager.Localize`, l.153253–153312, faz:

1. English ou string sem necessidade de localização: retorna a entrada.
2. Processa `@...@` em destaque; `Tooltip.ApplyAttributeTextTags` processa `[[...]]`.
3. Se recebeu `characterGender`, aplica `GetGenderizedText` antes da consulta.
4. Consulta o campo de gênero solicitado quando aplicável.
5. Fallback: Value → Feminine → Masculine → Neutral; cada getter seleciona a primeira entrada com o campo não branco.
6. Sem tradução: devolve a string já processada, não necessariamente o argumento original.

Fontes: `GetStringWithProcessedHighlightedText`, l.153314–153360; `GetLocalizationEntryList` e getters, l.153362–153408; `GetGenderizedText`, l.153416–153424; `Tooltip.ApplyAttributeTextTags`, l.335631–335650. O IL confirma a assinatura de três parâmetros de `GetLocalizationEntryList` e o `TryGetValue` literal, sem normalização (IL l.677850–677902; Localize l.677544–677577).

**A chave de runtime é o texto inglês processado pelo jogo no ponto da consulta**, não o ID editorial LANG, o GUID do asset, TranslatorKey ou o texto pt-BR exibido. O postfix da lista recebe justamente essa chave. Preservar bytes/caracteres, caixa, tags e espaços; nunca usar trim/casefold/remover HTML para lookup. Uma variante de entrada deve ser adicionada explicitamente com prova do call-site, não por casamento aproximado.

O parâmetro `fallbackToTranslatorKey` existe, mas nesta implementação não é consultado pelo corpo de `GetLocalizationEntryList`. Não criar um fallback imaginário por TranslatorKey.

### 3.3 Limites comprovados e uma divergência importante

`ManualLocalization.SetManualLocalization` seleciona sua própria `Entries` e escreve diretamente em Text/TMP (l.140188–140211). Portanto não é coberto pelo gancho da lista; os dois componentes do dump ficam em uma coleção separada. `LocalizedObject.SetObject` seleciona objetos por idioma (l.137343–137357): traduzir uma string não traduz sprites/imagens.

O documento anterior `DUMP-CHAVEADO-LANG-R1.md` classifica status como asset cru e afirma que a descrição não passa pelo dicionário. **Não transportar essa generalização para BP.** No binário conferido, `Tooltip.ShowActionStatusTooltip(ActionStatusInfo, ...)` chama `OptionsManager.Localize(actionStatusInfo.Description)` em l.334326 e localiza o nome em l.334369. Asset cru é a origem do texto; não prova bypass da consulta nessa tela. Outras telas continuam exigindo prova individual.

Depois da localização, esse tooltip processa `{...}` por `ParseBracketedNodeData` e `[0]` por `ApplyDescriptionExpressions` (l.334328, l.334352; definição l.335653–335678). `GetDamageTypeLabel` compõe template localizado e depois substitui `[damage type]` (l.335681–335684). Isso sustenta traduzir **templates**, nunca reavaliar números no tradutor.

## 4. Contrato dos datasets — decisão para BP-2 e BP-3

### 4.1 Arquivos e schema fechado

Pacote/projeto futuro:

    Data/pt-BR.original.json
    Data/pt-BR.corrigido.json
    Data/pt-BR.mods.json
    Data/manifest.json
    Data/correcoes.diff.json
    Data/pendencias.json

Os dois primeiros são snapshots completos de registros, não somente patches esparsos. O terceiro contém somente traduções/adaptações de conteúdo emitido por mods; não altera a alegação de original. Embutir os JSONs como recursos na DLL e manter cópias auditáveis no pacote, com hashes de equivalência. Falha de parse/integridade desliga a camada afetada, sem derrubar o jogo.

Formato obrigatório de original e corrigido (`schemaVersion = 1`, UTF-8, JSON estrito):

    raiz: schemaVersion, locale, variant, source, records, manualRecords
    locale: "pt-BR"
    variant: "Original" ou "Corrigido"
    source: taskId, artifactSha256, resourcePath, resourcePathId,
            resourceAssetSha256, assemblySha256, canonicalMemberSha256
    records: array de registros, ordenado por id editorial
    registro: id, key, presentInSource, entries
    entries: null para chave ausente no original;
             [] para lista existente e vazia;
             array ordenado de entradas nos demais casos
    entrada: Value, Key, TranslatorKey, Feminine, Masculine, Neutral,
             LanguageGender, CanBeGendered, NeedsGenderInfo

`key` é a chave literal; `id` é referência humana. Campos string aceitam null e string vazia, sem converter um no outro. `LanguageGender` é o inteiro serializado do enum, preservado/validado; os outros dois campos são booleanos. Os nove campos da entrada são obrigatórios. Não reduzir a lista a `ptbr`/primeiro Value, não descartar entradas secundárias nem preenchê-las artificialmente.

Os **9095 registros** da união ficam nos dois arquivos; `presentInSource = true` nos 9090 pt-BR. As cinco ausências ficam `false` com `entries = null` no original. No corrigido, uma ausência ou lista vazia só ganha tradução aprovada; `presentInSource` continua descrevendo o original. Conjunto de `id/key` é igual nos dois arquivos. Um update que traga nova chave requer nova versão do snapshot, não truncamento silencioso.

`manualRecords`: preservar `id`, `sourceFile`, `sourcePathId`, `englishText`, `originalEntries` (Language/Text) e `ptBRText`. No original, os dois casos medidos têm `ptBRText = null`; isso não significa um português a inventar. No corrigido, só preencher após aprovação. Path ID é identidade **offline** de proveniência, não `GetInstanceID()` de runtime. Um adaptador manual deve casar referência/contexto/texto inglês com prova, não só um número do dump.

`correcoes.diff.json` usa `(id, key, entryIndex, field, before, after, approvalTaskId)`; mudanças de ausência/lista têm operação explícita e aprovação. `pendencias.json` registra `(id, key, field, gateTaskId, reason)` e não alimenta runtime. Bard/música continuam preservados no snapshot e fora das correções.

BP-2: converter dados originais e provar igualdade de todos os campos, não corrigir. BP-3: copiar o original inteiro e aplicar apenas decisões aceitas da frente LANG; pendência mantém original. O grafo foi alinhado à entrada exigida pelo próprio cartão BP-3: acrescentada a dependência BP-2 → BP-3 (sem remover BP-1 → BP-3). Assim o corrigido aguarda o original final e não reconstrói um baseline alternativo.

### 4.2 Namespace de mods

`pt-BR.mods.json` tem raiz `schemaVersion`, `locale`, `records`; cada registro possui:

    id, ownerGuid, ownerVersion, ownerAssemblySha256,
    route, kind, sourceKey, sourceTemplate,
    portugueseTemplate, tokens, approvalTaskId

`route` identifica emissor/método e slot por nome, com assinatura exata no binding do adaptador. `kind` é `Replacement`, `Append` ou `DynamicTemplate`. `tokens` lista nome e tipo (por exemplo, número já formatado, nome localizado, rich-text opaco) e cada token deve existir com a mesma multiplicidade em ambos os templates. Não procurar/alterar dígitos já renderizados por regex genérica.

Uma nota nova de BetterTooltips não tem "pt-BR original do jogo". Seu baseline é `sourceTemplate` do mod e o texto aprovado é `portugueseTemplate`. Não fabricar uma tradução original para preencher a lacuna. O registry pode nascer vazio se não houver aprovação, mas a entrega não pode então alegar "todos os textos dos mods traduzidos"; informar a cobertura por emissor. BetterFont e BetterCombatText não necessitam linhas traduzidas só por estarem instalados: no código inspecionado alteram apresentação, não a localização semântica (§6).

## 5. Algoritmo de runtime e volta ao original

### 5.1 Overlay da lista

Resolver alvo pela assinatura explícita `(string, LanguageChoice, bool)` e confirmar retorno `List<LocalizationEntry>`. Entradas do patch por nome: `original`, `languageChoice`, `fallbackToTranslatorKey`, `ref __result`; nunca `ref __0` para contornar uma assinatura desconhecida.

Sequência decidida:

1. Ler um snapshot de configuração/dataset já validado. Se desativado, falha, chave null ou idioma de consulta diferente de `PortugueseBrazil`, não tocar.
2. Exigir também `OptionsManager.CurrentLanguage == PortugueseBrazil` no caminho em jogo. Não mudar idioma global, PlayerPrefs ou configuração dos outros mods.
3. Em `Original`, não substituir `__result`: a localização original vigente já foi obtida pelo jogo. O dataset original embarcado é a baseline lossless de comparação/exportação e permite demonstrar a reversão na versão suportada. Não impor um original antigo sobre um jogo atualizado.
4. Em `Corrigido`, localizar `key` com `StringComparer.Ordinal`. Registro inalterado em relação ao original não exige override.
5. Comparar a lista recebida com a baseline original dessa chave, campo a campo, incluindo null/[] e ordem. Se divergiu por update ou outro mod desconhecido, preservar recebida e registrar conflito uma vez por chave/motivo. Nunca apagar um acréscimo desconhecido.
6. Se igual e há correção aprovada, substituir **a referência do retorno** por uma lista própria e objetos próprios contendo os campos corrigidos. Não editar a lista do asset. Para uma tradução nova aprovada, null original ou [] original continuam sendo baselines distintas.
7. Exceção: manter o retorno capturado intacto; não retornar texto/lista parcialmente processados.

O jogo faz o restante da seleção. Não chamar `OptionsManager.Localize` dentro do postfix da lista para "traduzir o resultado": isso cria recursão. O core usa DTOs/strings; só o adaptador cria objetos da API do jogo. Não compartilhar listas mutáveis do dataset cacheado com o asset/outros consumidores: primeira implementação prefere clones no caminho de override, deixando otimização para medição posterior.

**Voltar a Original remove as alterações do BetterPortuguese; não desliga BetterTooltips ou outros plugins.** Se o dono quiser jogo inteiro vanilla, precisa desativar esses outros mods separadamente. Os originais do snapshot seguem disponíveis no pacote; runtime usa a versão vigente por segurança.

### 5.2 Carregamento e atualização de telas

No Awake do plugin: carregar/validar recursos e Bind de config; registrar patches individualmente, com contagens reais e motivo de falha. Não pedir o singleton/localização nem criar objetos de UI antes da primeira cena. A consulta original carrega o asset quando necessário; o overlay não depende de rodar "depois de Resources.Load" no boot.

`Conjunto` é enum Original/Corrigido (default Corrigido); `Ativo = true`; `IntegracaoMods = true`; `Diagnostico = false`. Config inválida desativa overrides com log; não tratar erro como autorização para aplicar o corrigido. Para alteração em runtime, SettingsChanged enfileira atualização para a thread principal, troca o snapshot de forma atômica e invalida caches de adaptadores/contextos.

Na thread principal, com OptionsManager e cena vivos, chamar `OptionsManager.LocalizeUI(force: true)` e o refresh manual suportado; `force` é indispensável porque sem ele o método retorna quando o idioma não mudou (C# l.153427–153461). Tooltips e textos dinâmicos são reconstruídos no próximo hover/refresh. Não prometer atualização de toda janela já aberta sem teste por rota. Original→Corrigido→Original repetido não deve empilhar notas nem registrar "original" a partir de uma string que BP já traduziu.

## 6. BetterTooltips: o que reaproveitar e o que NÃO copiar

Leitura do arquivo completo para inventário; trechos decisivos confrontados com código/IL:

| Símbolo/trecho de `LocalizePatch.cs` | Uso para BetterPortuguese |
|---|---|
| `Postfix` l.2482–2496 | snapshot + try/catch + devolução intacta; diagnóstico limitado por motivo |
| `AplicarNotasDoFunil` l.2525–2559 | chave inglesa literal; `TextFixes` substitui, `TextAppends` anexa; não copiar o gate como detector de idioma |
| `TextAppends` l.711; `TextFixes` l.1440 | corpus de templates/notas de mods para curadoria separada; não são o dataset pt-BR original |
| `AnexarNota` l.2056–2064 | uma linha em branco como composição de notas; não aplicar TrimEnd a chaves |
| regras e builders l.2565–2728, l.2759–2952 | há texto calculado em runtime: snapshots não substituem builders/valores |
| `CorEOrdemDoTooltip.TargetMethod` l.101–122 | resolução de assinatura explícita e recusa de alvo ambíguo |
| `CorEOrdemDoTooltip.Prefix` l.165–214 | organização final e identidade das notas pelo conteúdo, não pela cor |
| `ComACorDoJogo`, `_conteudosDeNota`, marcadores de nível 3 | traduzir no estágio errado pode quebrar reconhecimento e posição; cores também pertencem a valores do motor |

O gate real é `if (__result != original) return;` (l.2532–2537), **não** `CurrentLanguage == English`. Portanto BetterTooltips normalmente não insere suas notas quando existe uma tradução pt-BR diferente do inglês, mas pode atuar em fallback ou texto idêntico ao inglês. A igualdade não basta para identificar idioma. A normalização de espaços fica depois do gate (l.2739), portanto não é uma regra indiscriminada de todos os idiomas.

O comentário inicial chama Localize de funil de TODO texto; ManualLocalization e LocalizedObject refutam a abrangência literal. A decisão usa o binário, não esse comentário.

## 7. Conflitos e versão com mods — quem vence e em qual estágio

### 7.1 Responsabilidades e composição

| Camada | Dono e política |
|---|---|
| Template pt-BR do jogo | BP overlay na lista; somente chave corrigida com baseline compatível |
| Notas/reformulações mecânicas do BetterTooltips | pertencem ao mod; adaptador BP traduz/compõe somente itens registrados, preservando o restante |
| Fonte/atlas/fallback/material | BetterFont; BP não escreve essas propriedades |
| Halo/contorno/estilo de combate | BetterCombatText; BP não escreve essas propriedades |
| Outro tradutor desconhecido | preservar mudança detectada e logar conflito; não alegar que BP sempre vence |

BetterFont (`com.gumatos.betterfont`) tem postfix de Localize sem argumentos/retorno, apenas `FontUpdater.Ensure` (`Plugin.cs` l.302–315). BetterCombatText (`com.gumatos.bettercombattext`) estiliza componentes via TextStyler nos patches de boss/hover/status/dado/tooltip (`Patches.cs`); não disputa `ref string __result` na localização. Há interação visual a verificar, não duas traduções concorrentes a ordenar.

Se dois postfixes conhecidos escrevem a **mesma** string sem composição, o último que a sobrescreve determina a saída. A regra proposta para os adaptadores finais BP é `HarmonyAfter("com.gumatos.bettertooltips", "com.gumatos.betterfont", "com.gumatos.bettercombattext")`, com prioridade normal e assinatura explícita, **no mesmo método e mesma categoria**. IDs são owners Harmony, não nomes de pastas. O overlay principal em GetLocalizationEntryList acontece **dentro** de Localize e não é ordenado contra postfixes externos daquele método por um atributo Before/After.

Dependências BepInEx opcionais podem ordenar inicialização/detecção quando presentes; não fazem BetterPortuguese exigir esses mods nem determinam a ordem de execução Harmony. Não confiar em nome de DLL, PatchAll primeiro/último ou somente Priority.Last.

### 7.2 Prova de ordenação, não uma regra decorada

Foi executado o **PatchSorter da DLL local**, via reflexão, sem aplicar patches. Resultado `evidence/sorter-probe/result.json`: **9/9 verificações passaram**:

- prioridade 600 vem antes de 200;
- nas seis permutações de registro BT/BF/BP, BP com After de BT/BF fica por último;
- owners ausentes não impedem BP sozinho;
- controle negativo sem After deixa BP antes de BT quando seu índice de registro é anterior.

Fonte adicional do comportamento: `HarmonyLib.PatchSorter` l.105–114, l.135–150 e `PatchInfoSerialization.PriorityComparer` l.48–57 nos decompilados incluídos. Um comentário antigo do patch menciona inversão de prioridade; **esta DLL ordena prioridade descendente e desempata pelo índice**. Não repetir a regra de memória. A bancada mede o sorter, não comprova execução de wrappers Mono, renderização nem compatibilidade de qualquer Harmony instalado diferente.

Na implementação/QA: inspecionar `Harmony.GetPatchInfo` para owners, índices, before/after e prioridades em cada alvo; testar execução com sentinelas no retorno e os dois registros de ordem; detectar ciclos e terceiros. `PatchSorter.CullDependency` quebra dependência cíclica (l.174–192): uma relação declarada não é garantia em grafo conflitante. Comparar hash/version da DLL usada no teste com a carregada em runtime.

### 7.3 Adaptação de texto de mods: decisão e limite estrutural

A versão com mods **não** consiste em fazer BP substituir toda a string depois de BetterTooltips. A camada base pt-BR permanece; notas e linhas dinâmicas são compostas como conteúdo separado. Duas rotas:

1. Mod emite template pelo lookup central: registro de chave/entries e owner conhecido, aprovado e compatível; o jogo resolve tokens.
2. Mod escreve texto após a localização: adaptador versionado na rota emissora/apresentação, aplicando templates registrados apenas ao bloco/linha de origem comprovada. Não fazer varredura global de `TMP_Text.text` nem regex de números/dano.

Para BetterTooltips, realizar tradução de blocos já emitidos **depois de `CorEOrdemDoTooltip.Prefix` no `Tooltip.ShowTooltip`**, ou manter explicitamente os marcadores internos do mod. Traduzir antes e esquecer que `_conteudosDeNota`/`Your skills on this status:`/`Your active shrine auras` são identidades quebra a movimentação. A assinatura ShowTooltip de 13 tipos está em `AssinaturaDoShowTooltip` l.75–90 do patch: resolver exatamente essa assinatura e escrever somente `description`. Texto/valores do jogo com a mesma cor ficam intocados. Dados e templates do adaptador devem preservar todos os tokens e o conjunto de blocos antes/depois.

**Ordenação não reativa notas que BetterTooltips não produziu em português.** Para oferecer equivalentes pt-BR das notas inglesas quando a base já está traduzida, o adaptador BP deverá compor as notas aprovadas a partir da chave/contexto original e de parâmetros do produtor mecânico correspondente, quando esse mod estiver presente e for compatível. A composição pertence ao BetterPortuguese, em rotas específicas; não alterar o gate inglês do BetterTooltips globalmente nem chamar seu funil com um resultado inglês fictício. Para valores dinâmicos, aproveitar a fonte de dados/avaliador comprovado do produtor, nunca extrair uma fórmula do texto traduzido ou cravar números.

`StatusSkillSynergyPatch.AcrescentaLinhaDeSinergia` acrescenta texto no postfix de `Tooltip.ApplyDescriptionExpressions`, **fora** do Localize (`StatusSkillSynergyPatch.cs` l.91–128, marcador l.143). Ele exige adaptador final próprio, incluindo identificação/contexto; o registro do último postfix de Localize sozinho não o alcança. As rotas do mod precisam ter inventário de cobertura: estática, dinâmica, suportada, pendente. Até esse inventário e os testes existirem, não anunciar compatibilidade completa nem que todos os recursos de BetterTooltips em inglês aparecerão em português.

O modo Original desativa overrides e composição BP de mods; não remove blocos gerados pelos próprios mods. `IntegracaoMods=false` desativa somente essa camada BP, mantendo o conjunto base escolhido. Um adaptador cujo fingerprint não casa é desligado sozinho, com texto já emitido preservado. Não há reflexão especulativa de "primeiro método que parece servir".

## 8. Riscos e mitigação verificável

| Risco | Mitigação decidida | Prova requerida |
|---|---|---|
| Chave faltando, null, vazia ou só números | não tocar; distinguir null/[]/ausência; registrar ausências sem spam | casos do dump e controles; jogo mantém seus fallbacks |
| Nova chave ou tradução alterada por update | lookup exato e comparação per-key da baseline; preservar chave nova/alterada; reextrair snapshot | corpus vNext com chave adicional, removida e lista diferente |
| Colisão de chave/JSON duplicado | parser estrito recusa duplicatas antes da construção de Dictionary; um registro por chave | duplicata-isca rejeitada; não aceitar contagem como teste de duplicidade |
| Chave pré-processada/gênero/@/[[...]] | interceptar ponto da lista, não normalizar por tentativa | fixtures por etapa e por gênero, incluindo ausência de variante |
| Placeholder/expressão/tags danificados | validar tokens por multiplicidade e estágio; correção de tag aprovada tem exceção explícita no diff | `[0]`, `*0`, `[name]`, `{STA=...}`, `{a,b}`, `[he]`, sprite, color, b/i/size e escapes |
| Texto montado depois do lookup | tratar fragmentos/templates na rota real, adaptador identificado e contexto | exemplos `GetDamageTypeLabel` e synergies; não confundir tabela com cobertura de UI |
| Idioma não pt-BR, inclusive Default | usar CurrentLanguage efetivo + parâmetro languageChoice; não alterar estado global | todos os outros idiomas retornam entrada idêntica; Default resolvido para pt/English |
| Outro mod muda a lista | comparação integral com original; em conflito preservar/logar | mudança-sentinela não é apagada; matriz de ordens |
| Traduzir nota antes do remanejamento | adaptação final após mover blocos ou marcadores preservados | nota após custos/alcance, nível 3 último, números coloridos não movidos |
| Config/catálogo inválido ou alvo removido | desligar camada, log limitado; registrar patches individualmente | parse errado, config enum inválido, assinatura incompatível, exception-isca |
| Reload fora da thread principal ou cache antigo | snapshot atômico + fila main-thread + LocalizeUI(force) | toggle repetido sem duplicata, tradução antiga ou mutação no asset |
| Material/glyph/layout em pt-BR | BP não escreve estilo; testes visuais posteriores com BF/BCT | acentos, fallback, quebra de linha e combate; não cobertos pela bancada offline |

Corrigir tags pode legitimamente mudar o inventário de tags original: não impor igualdade cega quando o próprio defeito é uma tag quebrada. Exigir aprovação por campo + validação do resultado e ausência de alteração de tokens funcionais. Igualdade pt-BR/inglês, presença de placeholders e lista vazia são achados de curadoria, não autorizações automáticas de tradução.

## 9. Testes offline com que o mod precisa nascer

BP-4/QA deve separar core puro (DTOs e composição), binding (tipos/assinaturas) e integração. Nenhum teste deve abrir jogo ou instalar DLL.

1. **Cobertura lossless:** original e corrigido têm o mesmo conjunto de 9095 id/key; 9090 presentes no original; listas/ordem/campos originais idênticos ao dump; cinco ausências e dois manuais explícitos. Fonte/hash declarados batem; source key imutável.
2. **Dupla de snapshots:** corrigido sem decisão fica igual; diff contém somente decisões aceitas, índices/campos/before corretos; propostas pendentes não entram. Originais não podem ser reescritos por exportação editorial.
3. **Parser e serialização:** duplicatas em JSON/records/key rejeitadas com controle positivo; roundtrip UTF-8 e null/empty/newline/quotes/backslash; chaves com espaços iniciais/finais e caixa distintos não colidem.
4. **Escolha de campo:** primeira entrada não branca por Value/Feminine/Masculine/Neutral; falha de variante segue o fallback do jogo; lista secundária vazia não mascara a anterior. O corpus tem zero campos de gênero preenchidos: usar fixtures explicitamente sintéticas para esses ramos, sem afirmar que são dados do jogo.
5. **Preprocessing e template:** string raw versus chave processada, gênero, @ e [[...]]; tokens numéricos e nominais preservados na etapa correta; exemplos reais de status/dano e `{...}`. Não testar apenas que a chave existe no arquivo.
6. **Modo/idioma:** default Corrigido; Original não modifica retorno; Ativo=false/idioma errado são no-op; Original→Corrigido→Original; novo snapshot de config sem patch duplo. Todo estado não pt-BR fica byte/caractere idêntico.
7. **Compatibilidade de update/conflito:** retorno original incompatível, chave ausente/nova e mutação por plugin-isca preservados; retorno/objetos do asset não sofrem mutation; erro mantém retorno de entrada intacto.
8. **Harmony real:** bancada do sorter local e teste de execução de métodos-isca com postfixes reais, sentinelas, duas ordens de registro, owners ausentes/desconhecidos/ciclo; testar assinatura perdida e não usar jogo como alvo de patch offline. Inspeção de metadados sozinha não comprova resultado final.
9. **Mods:** composição com e sem BT, versão desconhecida, nota estática e nota dinâmica, status synergy emitida depois de Localize, nota que não foi produzida pelo gate inglês, feed sem notas, slots de nomes versus descrição; notas traduzidas não eliminam corpo/valores; modo Original/IntegracaoMods=false preserva saída de outros mods. Registro sem aprovação não aplica.
10. **Formatação e binding:** tags/tokens antes/depois; ordem descrição→custos→notas→nível 3; componentes BF/BCT não tocados; targets resolvem pelo tipo, nomes e retorno; build Debug/Release com `-p:DeployToBepInEx=false` e nenhuma escrita no perfil/jogo.

Teste de perf/alocação do lookup e log limitado deve acompanhar o core. Testes de renderização e de atualização de janelas não são substituídos por asserts de string; serão validação posterior autorizada. Esta BP-1 não declara esses dez grupos implementados/passando: executou somente a auditoria de fontes e a prova do sorter abaixo.

## 10. Resultado desta tarefa e handoff

Executado, com exit 0:

    ilspycmd -o <workspace>/evidence/decompiled C:/dev/stolen-realm/lib/Assembly-CSharp.dll
    ilspycmd -t OptionsManager -il C:/dev/stolen-realm/lib/Assembly-CSharp.dll
    ilspycmd -t HarmonyLib.PatchSorter -o <workspace>/evidence/decompiled C:/dev/stolen-realm/lib/0Harmony.dll
    dotnet build <workspace>/evidence/sorter-probe/SorterProbe.csproj
    dotnet <workspace>/evidence/sorter-probe/bin/Debug/net6.0/SorterProbe.dll
    python <workspace>/evidence/audit_sources.py

Bancada compilou com zero erros/avisos; 9/9 checks do sorter passaram. Auditoria conferiu o corpus real, oito âncoras por conteúdo, igualdade de CSV/JSON/listas e hash dos assets. `evidence/verification-final.json` registra o readback final das fontes e artefatos.

Entregáveis: este documento; `BETTERPORTUGUESE-BP1-EVIDENCIAS.zip` contendo relatório/hash, recortes C#/IL, declaração de símbolos BT, bancada/reprodução e saídas. O dump canônico grande permanece no anexo LANG-R1; não duplicar a extração como se fosse o dataset BP-2.

BP-2 e BP-3 devem adotar o schema da seção 4. BP-4 deve implementar a estratégia da seção 5 e os testes da seção 9; a cobertura de mods é separada da cobertura do jogo e depende dos adaptadores/aprovações da seção 7. Nenhuma alteração em BetterTooltips/BetterFont/BetterCombatText foi feita aqui. Tentativa de obter documentação web complementar foi recusada pelo backend/HTTP; não foi usada como evidência. Decisões de lookup e ordem estão fundamentadas no código/IL e execução da DLL local.

**NAO_EXERCITADO:** plugin BetterPortuguese, aplicação de patches em Mono/jogo, UI, seleção efetiva de gênero em runtime, reload de telas, layout, acentos/fallback de fonte, compatibilidade instalada entre todos os mods, novas versões do jogo, revisão/aprovação de traduções. Sem deploy, instalação de BepInEx, publicação ou modificação de Assembly-CSharp.dll.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
