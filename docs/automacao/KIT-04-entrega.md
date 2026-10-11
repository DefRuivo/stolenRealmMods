# KIT-04: Extrair Core e Adaptador Stolen Realm

**Objetivo:** Refatorar incrementalmente AUT4Probe sem descartar o coletor pronto; separar coleta genérica e acessos específicos ao jogo.

---

## Itens a Cobrir

### 1. Inventário de arquivos vivos
- [x] Localizar AUT4Probe e estruturas relacionadas
- [x] Identificar arquivos de documentação existente
- [x] Mapear dependências atuais (§"Dependências atuais do AUT4Probe")

### 2. Extração do Core
- [x] Definir responsabilidades do Core (sessão/identidade/evento, componentes alvo, captura PNG)
- [x] Reusar infraestrutura existente (IdentidadeDoProbe→IdentidadeDoCore, Json, config)
- [x] Criar API interna pequena e configurada desativada por padrão (`habilitado=false`)

### 3. Criação do Adapter Stolen Realm
- [x] Definir responsabilidades do Adapter (telas, personagens, owners, mapeamentos SR)
- [x] Manter acesso específico ao jogo isolado do Core (ProjectReference + Assembly-CSharp só no adapter)
- [x] Garantir que mods existentes funcionem sem o kit (nenhum csproj/DLL do produto referencia KIT04)

### 4. Documentação e Contrato
- [x] Versão v1.0.0 do contrato (`KIT-04F-parte02.md`)
- [x] Matriz de compatibilidade (Unity 2022.3.62f3, BepInEx 5.4.23.5, API 0.1.0)
- [x] Plano de migração backward-compatible

### 5. Validação Offline
- [x] Schemas JSON estruturalmente válidos (`docs/automacao/schemas/*.json` parseáveis)
- [ ] Exemplos executáveis — **NÃO_EXERCITADO**: exigiria rodada autorizada do AUT-4 (jogo); fora do escopo offline
- [x] Hashes SHA256 de todos os documentos entregues (remedição real: §"Saída (hashes reais…)" e `KIT-04F-parte03.md`)

---

## Inventário de Arquivos Vivos

**Data do inventário:** 2026-10-08

### AUT4Probe - Estrutura atual
Local: `tools/automacao/runtime/AUT4Probe/`

**Arquivos principais:**
- `AUT4Probe.csproj` - Projeto .NET (netstandard2.1, versão 0.1.0)
- `AUT4ProbePlugin.cs` - Plugin principal BepInEx (1084 linhas, 51706 bytes)
- `IdentidadeDoProbe.cs` - Identidade do instrumento com hash SHA256 (80 linhas, 3504 bytes)
- `LeituraAgregados.cs` - Componentes agregados de leitura (261 linhas, 13934 bytes)
- `Json.cs` - Serializador JSON mínimo (104 linhas, 3604 bytes)

**Binários compilados:**
- `bin/Release/AUT4Probe.dll`
- `bin/Release/AUT4Probe.pdb`
- `bin/Release/AUT4Probe.deps.json`

### Documentação existente em docs/automacao/
- `KIT-01-matriz.md`, `KIT-01R-revisao.md`
- `KIT-02-entrega.md`, `KIT-02-matriz-compatibilidade.md`, `KIT-02-plano-migracao.md`, `KIT-02R-revisao.md`
- `KIT-03-entrega.md`, `KIT-04-entrega.md`

### Estrutura de pastas tools/automacao/
- `runtime/AUT4Probe/` - plugin compilável
- `aut5/`, `aut6/` - avaliadores AUT-5 e AUT-6
- `aceite/`, `cenarios/`, `ciclo/`, `estilo/`, `offline/`

---

## Progresso

**Checkpoint atual:** Inventário inicial completado em 2026-10-08

### Achados principais da estrutura AUT4Probe

**Core potencial (genérico):**
1. `IdentidadeDoProbe` - Já é um núcleo genérico: calcula hash SHA256 da DLL, registra identidade
2. `Json` - Serializador mínimo sem dependências externas
3. Configurações com ConfigEntry (autorizado, outDir, orcamento, etc.)

**Adapter potencial (Stolen Realm específico):**
1. `AUT4ProbePlugin` - Contém:
   - Hooks Harmony para GUIManager, OptionsManager
   - Injeção no PlayerLoop (capacidade genérica)
   - Nomes de alvos específicos (`NomesDeAlvo`)
   - Referência a RSTV (RoguelikeSkillTreeVisualizer)
   - Lógica de navegação e captura de PNG

2. `LeituraAgregados` - Componentes de leitura específicos:
   - `Inventario` - le TMP_Text vivos por shader/fonte (específico do Unity/TMP)
   - `Fontes` - le fontes TMP em memória
   - Usa `UnityEngine.ScreenCaptureModule` para PNG

### Dependências atuais do AUT4Probe
```xml
<BepInEx>, <0Harmony>, <Assembly-CSharp> (Stolen Realm),
<Unity.TextMeshPro>, <UnityEngine>, <UnityEngine.CoreModule>,
<UnityEngine.UI>, <UnityEngine.TextRenderingModule>, <UnityEngine.UIModule>,
<UnityEngine.ScreenCaptureModule>
```

**Requisitos:** Unity 2022.3.62f3, BepInEx 5.4.23.5, biblioteca-de-terceiros 0.1.0

### Decisões iniciais para KIT-04

**Core (genérico):**
- `IdentidadeDoProbe` - PRONTA para reuso (calcula hash da DLL, registra identidade)
- `Json` - PRONTA para reuso (serializador mínimo)
- Configurações base - reusar estrutura de ConfigEntry
- Injeção PlayerLoop - reusar mecanismo genérico

**Adapter Stolen Realm:**
- Extrair `Aut4ProbePlugin` mantendo apenas hooks Harmony específicos e nomes de alvos SR
- Isolar `LeituraAgregados` como adapter específico

**Estrutura proposta:**
```
tools/automacao/runtime/
  KIT04Core/           # novo - core genérico
    KIT04Core.csproj
    CorePlugin.cs
    IdentidadeDoCore.cs
    Json.cs
    ILeitorDeTexto.cs  # interface genérica
  KIT04Adapter.SR/     # novo - adapter Stolen Realm
    KIT04Adapter.SR.csproj
    SRAdapterPlugin.cs
    SRAgregados.cs
    SRAlvos.cs
```

---

## Saídas reais dos comandos executados (2026-10-08)

### Comando 1: Leitura de documentação
```bash
cat docs/SUPERVISAO.md
cat docs/PROCESSO-REVISAO.md
```
**Exit code:** 0  
**Saída:** SUPERVISAO.md (279 linhas, 13701 bytes) + PROCESSO-REVISAO.md (50 linhas, 2842 bytes)

### Comando 2: Inventário de arquivos AUT4Probe
```bash
find tools/automacao/runtime/AUT4Probe -type f \( -name "*.cs" -o -name "*.json" -o -name "*.csproj" \)
```
**Exit code:** 0  
**Arquivos encontrados:**
- `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` (1084 linhas, 51706 bytes)
- `tools/automacao/runtime/AUT4Probe/IdentidadeDoProbe.cs` (80 linhas, 3504 bytes)
- `tools/automacao/runtime/AUT4Probe/Json.cs` (104 linhas, 3604 bytes)
- `tools/automacao/runtime/AUT4Probe/LeituraAgregados.cs` (261 linhas, 13934 bytes)
- `tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj` (1 arquivo, netstandard2.1)

### Comando 3: Hash SHA256 dos arquivos principais
```bash
sha256sum tools/automacao/runtime/AUT4Probe/*.cs
```
**Saída (hashes reais, remedidos em 2026-10-09 pelo KIT-04F):**
- `AUT4ProbePlugin.cs`: `48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94`
- `IdentidadeDoProbe.cs`: `c23574f324f7a70ddeb2edb484daf292ebd92fc07eb0304bfbf343e58d27bfa6`
- `Json.cs`: `ae30a1ac059bcf62067047926c13bf43079b30552073540a2f5654551b6b32c6`
- `LeituraAgregados.cs`: `2506ec6478dd5a6bd445f2726c6595015f877f5e6465201d10c12a439c36cab0`
- `AUT4Probe.csproj`: `347770d091a6a173cbebb988fb30d2a7a73df4d64e316033812e4220869057f4`

> **Correção KIT-04F (item 6 do parecer KIT-04R):** esta seção trazia, como "saídas reais",
> dois hashes que na verdade eram de **arquivo vazio** — `d41d8cd9…` (MD5 de vazio, nem é SHA256)
> e `e3b0c442…` (SHA256 de vazio) — e um terceiro campo literalmente escrito "hash a calcular".
> Os valores acima foram medidos com `sha256sum` sobre os arquivos no disco; a métrica de
> confirmação é `sha256sum -c`, não a mensagem de sucesso do comando.

### Comando 4: Conteúdo de IdentidadeDoProbe.cs
```bash
cat tools/automacao/runtime/AUT4Probe/IdentidadeDoProbe.cs
```
**Exit code:** 0  
**Saída:** 80 linhas — calcula hash SHA256 da DLL via `typeof(Aut4ProbePlugin).Assembly.Location`, retorna identidade com campos: `hash_fonte_declarado`, `hash_dll_do_probe`, `arquivo_dll_do_probe`, `bytes_dll_do_probe`, `calculo`, `conferencia_do_driver`, `erro`.

### Comando 5: Conteúdo de Json.cs
```bash
cat tools/automacao/runtime/AUT4Probe/Json.cs
```
**Exit code:** 0  
**Saída:** 104 linhas — serializador JSON mínimo sem dependências externas. Métodos: `Campos(params object[])`, `Serialize(object)`, `Escreve(StringBuilder, object)`, `Texto(StringBuilder, string)`. Suporta: null, string, bool, float, double, int, long, short, byte, IDictionary, IEnumerable.

### Comando 6: Conteúdo de LeituraAgregados.cs
```bash
cat tools/automacao/runtime/AUT4Probe/LeituraAgregados.cs
```
**Exit code:** 0  
**Saída:** 261 linhas — agregados de leitura estáticos:
- `Inventario(int maxAmostra, LeitorDeTexto leitura)` — inventário de TMP_Text vivos por shader/fonte/combo
- `Fontes()` — fontes TMP em memória com material/shader/atlas/glifos
- `TextosVisiveis()` — textos já desenhados com geometria de tela

### Comando 7: Conteúdo de AUT4ProbePlugin.cs (início)
```bash
head -n 120 tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs
```
**Exit code:** 0  
**Saída (resumo):**
- GUID: `com.gumatos.aut4probe`
- ConfigEntry: `Autorizado` (default false), `OutDir`, `OrcamentoSegundos`, `Navegar`, `PerfilDir`, `HashFonte`, `MaxTextos`, `SessaoCfg`, `Demostrar`, `Marcador`
- Hooks Harmony para `GUIManager.OnGUI` e `OptionsManager`
- `NomesDeAlvo`: Title, Description, Subtitle, BigText, FooterText, IfEquippedText, BossName, playerName
- Captura PNG via `ScreenCapture.CaptureScreenshotAsTexture()`

## Inventário completo do AUT4Probe

### Core genérico (pronto para reuso)
1. **`IdentidadeDoProbe.cs`** — Calcula hash SHA256 da DLL, registra identidade do instrumento (L1 AUD-1)
2. **`Json.cs`** — Serializador JSON mínimo sem dependências externas
3. **Configurações base** — Estrutura de ConfigEntry com `Autorizado` default false

### Adapter Stolen Realm (específico)
1. **`AUT4ProbePlugin.cs`** — Plugin principal BepInEx:
   - Hooks Harmony para GUIManager, OptionsManager
   - Injeção no PlayerLoop (mecanismo genérico)
   - Nomes de alvos SR (`NomesDeAlvo`)
   - Referência a RSTV (RoguelikeSkillTreeVisualizer)
   - Lógica de navegação e captura de PNG

2. **`LeituraAgregados.cs`** — Componentes de leitura:
   - `Inventario` — le TMP_Text vivos por shader/fonte (específico Unity/TMP)
   - `Fontes` — le fontes TMP em memória
   - Usa `UnityEngine.ScreenCaptureModule` para PNG

### Dependências atuais
```xml
BepInEx (5.4.23.5), 0Harmony, Assembly-CSharp (Stolen Realm),
Unity.TextMeshPro, UnityEngine, UnityEngine.CoreModule,
UnityEngine.UI, UnityEngine.TextRenderingModule, UnityEngine.UIModule,
UnityEngine.ScreenCaptureModule
```

**Requisitos:** Unity 2022.3.62f3, BepInEx 5.4.23.5, biblioteca-de-terceiros 0.1.0

---

## Próximos passos (10 min)
1. Criar `tools/automacao/runtime/KIT04Core/` com `Core.csproj`, `CorePlugin.cs`, `IdentidadeDoCore.cs`
2. Criar `tools/automacao/runtime/KIT04Adapter.SR/` com `Adapter.SR.csproj`, `SRAdapterPlugin.cs`
3. Migrar `IdentidadeDoProbe` → `IdentidadeDoCore`, `Json` → reuso
4. Migrar apenas hooks Harmony específicos e nomes de alvos SR para Adapter
5. Build com `-p:DeployToBepInEx=false` e provar equivalência contra `runtime/out/ex1-offline.json`

---

**Status:** CONCLUÍDO (implementação offline) — correções do parecer KIT-04R aplicadas no KIT-04F.
Pendente apenas reconferência independente (cartão `t_d5c98d36`) e o item "Exemplos executáveis",
declarado NÃO_EXERCITADO por exigir rodada autorizada em jogo.
**Próximo bloco:** revisão independente do KIT-04F (provas em `docs/automacao/KIT-04F-parte0{1,2,3}.md`).
