# BetterPortuguese

- **Version:** 0.1.0
- **Author:** gumatos
- **GUID:** `com.gumatos.betterportuguese`
- **Status:** implementação inicial, validação offline; NÃO aprovado para publicação ou instalação automática.

Mod BepInEx independente para Stolen Realm, sem alterar gameplay, arquivos do jogo ou outros plugins. Contém os conjuntos completos **Original** e **Corrigido**, selecionáveis pela configuração. Não precisa de nenhum outro mod do projeto nem de biblioteca de terceiros.

## Estado editorial desta versão — importante

Esta captura contém **ZERO correções aprovadas**. Os gates humanos LANG-C1..C5 ainda estavam pendentes na entrega BP-3. Por isso Corrigido contém os mesmos textos/entradas do Original (a única diferença no JSON é `variant`). O padrão `Corrigido` é a escolha do conjunto, não uma alegação de que o português já foi melhorado.

Os dois snapshots têm 9.095 registros da união das tabelas, 9.090 chaves pt-BR presentes, 8.097 entradas, 1.286 listas vazias e cinco ausências explícitas. Há dois registros manuais preservados, sem pt-BR aprovado. Esses totais descrevem o dataset, não cobertura de toda tela/string do jogo nem 9.090 traduções não vazias.

`pt-BR.mods.json` está vazio. `IntegracaoMods=true` reserva a configuração dessa camada, mas **não ativa nenhum adaptador nesta versão**. Não há tradução/composição aprovada das notas de BetterTooltips, de synergies nem de outros textos de mods. Texto emitido por outro plugin é preservado. Novas traduções precisam de dataset aprovado, binding versionado e testes próprios; não basta acrescentar propostas a pendencias.json.

## Configuração e volta ao original

O arquivo é `BepInEx/config/com.gumatos.betterportuguese.cfg`. O plugin cria este arquivo quando executado no ambiente autorizado; esta entrega NÃO instalou nem abriu o jogo.

```ini
[Geral]
Ativo = true
Conjunto = Corrigido
IntegracaoMods = true
Diagnostico = false
```

- `Conjunto = Original`: deixa o resultado vigente do jogo passar intacto. O snapshot original embarcado continua disponível para auditoria; não impomos um português antigo sobre um jogo atualizado.
- `Conjunto = Corrigido`: aplica somente chaves efetivamente alteradas no snapshot validado, comparando integralmente a lista vigente com a baseline original. Nesta captura não há chaves alteradas.
- `Ativo = false`: desliga as camadas BP; não desliga outros mods.
- `IntegracaoMods = false`: desliga só a camada BP de conteúdo de mods; não muda a escolha do conjunto base.
- `Diagnostico = true`: inclui registro de refresh, sem log por frame.

É possível editar/salvar o `.cfg` enquanto o jogo está aberto. O driver no `GUIManager.Update` verifica o arquivo a cada segundo de tempo real; mudanças são enfileiradas e publicadas na thread principal. Config com valor inválido, como `Conjunto = Corrigdo` ou um ordinal numérico, desativa overrides até o arquivo ser corrigido. A leitura não regrava comentários/textos manuais do `.cfg`. Mudanças feitas por um gerenciador de configuração também passam pela fila.

O refresh é dirigido: somente textos já registrados pelo jogo cuja chave original pertence às correções aprovadas são enviados a `OptionsManager.LocalizeUIText`. Ele roda na thread principal quando a camada efetiva entra ou sai de Corrigido; mudanças apenas de diagnóstico/integração (registro vazio) não refazem a UI. Não chama `LocalizeUI(force: true)` nem relocaliza componentes manuais/objetos de idioma que o BP não altera. Isso evita repetir diagnósticos nativos Screen/Window a cada troca de configuração, sem suprimir logs nem remendar o parser do jogo. Se o registro privado nativo mudar de assinatura, o refresh automático falha com aviso; o lookup segue preservado e a UI pode ser reaberta. Tooltips/dados dinâmicos precisam de próximo hover/refresh. **Não foi testada atualização visual de toda janela aberta**, nem renderização/fontes em português. Original remove alterações BP, mas não remove notas/alterações dos outros mods: para o jogo totalmente vanilla é preciso desativá-los separadamente.

## Arquitetura e limites de segurança

O postfix usa a assinatura exata de `OptionsManager.GetLocalizationEntryList(string original, LanguageChoice languageChoice, bool fallbackToTranslatorKey)`, retorno `List<LocalizationEntry>`. Consulta e idioma efetivo precisam ser PortugueseBrazil. Chaves são comparadas com `StringComparer.Ordinal`: sem trim, mudança de caixa ou remoção de tags. O jogo continua processando destaque/gênero, escolhendo a primeira entrada não branca e resolvendo placeholders/números.

O core não muta listas/objetos do asset: cria uma lista e objetos próprios somente no override. Uma chave alterada por update ou plugin desconhecido não é sobrescrita; conflito é registrado por ID com teto de logs. Outro postfix posterior continua podendo mudar a saída: não há promessa de precedência sobre plugins desconhecidos.

JSONs UTF-8 estritos são embutidos na DLL e distribuídos como cópias auditáveis em `plugins/BetterPortuguese/Data/`. SHA-256 de cada recurso é fixado no código. Membros JSON/IDs/chaves duplicados, schema inválido, drift de identidade, diff sem aprovação ou perda de tokens recusam o catálogo. Propostas de `pendencias.json` NÃO são carregadas como correções.

O loader 0.1.0 suporta alterações aprovadas de Value/Feminine/Masculine/Neutral em entradas existentes. Mudança de lista/ausência, tradução manual, alteração de tags/tokens ou adaptador de mods requer implementação/validação nova e falha de modo seguro nesta versão. Esse limite não perde registros do snapshot; restringe operações aplicáveis no runtime atual.

Nenhum material, fonte, cor, número, mecânica, PlayerPrefs ou dicionário global é escrito pelo BP. Assembly-CSharp.dll/resources.assets permanecem intactos. O refresh nativo do jogo pode executar os seus próprios mecanismos de UI; isso não é um patch de estilo do BP.

## Compilar e verificar — sem instalar

Referências locais privadas devem existir na `lib/` da raiz. Nunca distribuir DLLs do jogo/Unity/BepInEx nem carregá-las como plugins.

```bash
dotnet build BetterPortuguese/BetterPortuguese.csproj -c Debug -p:DeployToBepInEx=false
dotnet build BetterPortuguese/BetterPortuguese.csproj -c Release -p:DeployToBepInEx=false
python tests/BetterPortuguese.Offline/run.py
```

O runner usa o SDK .NET 6 para o core/binding e o CLR desktop do Windows para executar HarmonyX local com o mesmo core de produção. A DLL HarmonyX 2.9.0.0 desta bancada não funcionou no host net6 (`AccessTools/MethodInvoker`); a alternativa CLR desktop foi executada, não um mock do Harmony. Fixtures são explicitamente sintéticas e não entram nos snapshots distribuídos.

As verificações incluem corpus lossless, aprovação/diff, parser negativo, clones/rollback/conflito, fila/config, metadata da API real e bytes de cada recurso nas DLLs Debug e Release, além de execução de postfixes-isca reais em duas ordens de registro, owner ausente/desconhecido e ciclo. Isso **não** testa o plugin em Mono/Unity, a UI ou notas dos mods. Os builds têm um warning MSB3277 de System.Net.Http pela referência Assembly-CSharp; nenhum erro de compilação.

## Pacote auditável

Após build/testes, use o empacotador específico, que reutiliza a validação de metadados do repositório e inclui os JSONs externos exigidos por BP-1:

```bash
python BetterPortuguese/package.py --output dist/gumatos-BetterPortuguese-0.1.0-auditado.zip
```

Ele recusa substituir um ZIP já existente e não instala/publica. O empacotador genérico do repositório produz DLL com recursos embutidos, mas não acrescenta as cópias Data; **para a entrega auditável use este comando**. `Data/manifest.json` descreve os snapshots, não é o manifest Thunderstore da raiz.

Para remover uma futura instalação autorizada, desative o mod no perfil ou remova somente `BepInEx/plugins/BetterPortuguese/`. O jogo original não precisa de restauração porque nenhum asset é editado. A configuração pode ser mantida. Não colocar backups de DLL dentro de plugins: o loader é recursivo.

## Proveniência

Decisão de arquitetura BP-1; Original lossless BP-2; captura Corrigido sem aprovações BP-3. Fonte canônica: LANG-R1 `entrega02/localizacao-ptbr.json`. Os hashes completos e as pendências acompanham Data/; o assembly de referência é identificado pela fonte dos snapshots, não redistribuído. Aprovações editoriais e runtime autorizado BP-5 ainda são gates separados; build verde não libera publicação.
