# KIT-04: Especificação do Core Genérico

## Objetivo
Definir o núcleo genérico do kit de automação — independente de jogo, reutilizável para qualquer Unity.

## Arquitetura proposta

```
tools/automacao/runtime/
├── KIT04Core/              # Core genérico (sem dependência do jogo)
│   ├── KIT04Core.csproj
│   ├── CorePlugin.cs
│   ├── ICoreSession.cs
│   ├── ICoreIdentidade.cs
│   ├── ICoreEvento.cs
│   ├── IComponentReader.cs
│   └── IPictureCapture.cs
└── KIT04Adapter.SR/        # Adapter Stolen Realm (específico)
    ├── KIT04Adapter.SR.csproj
    ├── SRAdapterPlugin.cs
    ├── SRTelas.cs
    ├── SRPersonagens.cs
    ├── SROwners.cs
    └── SRMapeamentos.cs
```

## Contratos do Core

### 1. ICoreSession
```csharp
public interface ICoreSession
{
    void Registrar(string idSessao, string data, string ambiente);
    string ObterIdSessao();
    bool EstaAtiva();
}
```

**Responsabilidades:**
- Registrar sessão com ID único, data/hora e ambiente (dev/teste/prod)
- Manter estado de sessão ativa
- Validar que sessão existe antes de permitir eventos

### 2. ICoreIdentidade
```csharp
public interface ICoreIdentidade
{
    Dictionary<string, object> CalcularIdentidade(string hashFonteDeclarado);
    string CalcularHashSha256(string caminhoArquivo);
}
```

**Responsabilidades:**
- Calcular hash SHA256 do assembly/plugin
- Registrar identidade com campos: `hash_fonte_declarado`, `hash_dll_do_probe`, `arquivo_dll_do_probe`, `bytes_dll_do_probe`
- Manter erro em caso de falha (null safe)

**Reúso:** `IdentidadeDoProbe.cs` já implementa esta interface — apenas renomear para `IdentidadeDoCore`.

### 3. ICoreEvento
```csharp
public interface ICoreEvento
{
    void RegistrarEvento(string tipo, string detalhe, Dictionary<string, object> dados);
    List<Dictionary<string, object>> ObterEventos();
    void LimparEventos();
}
```

**Responsabilidades:**
- Registrar eventos com tipo, detalhe e dados adicionais
- Listar todos os eventos registrados
- Limpar eventos após processamento

### 4. IComponentReader<T>
```csharp
public interface IComponentReader<T> where T : MonoBehaviour
{
    T[] LerTodos();
    T[] LerPorNome(string nome);
    T[] LerPorTag(string tag);
    Dictionary<string, object> Inventariar(int maxAmostra);
}
```

**Responsabilidades:**
- Ler componentes do tipo genérico `T`
- Filtrar por nome, tag, ou inventariar por shader/material/fonte
- Retornar `null` se componente não existir (AUSENTE, não inventar valor)

**Reúso:** `LeituraAgregados.Inventario()` já implementa lógica similar — adaptar para interface genérica.

### 5. IPictureCapture
```csharp
public interface IPictureCapture
{
    bool CapturarPNG(string caminhoSaida, int largura, int altura);
    bool EstaDisponivel();
}
```

**Responsabilidades:**
- Capturar screenshot do frame atual
- Salvar em PNG (caminho absoluto)
- Verificar disponibilidade do módulo de captura

**Reúso:** `ScreenCapture.CaptureScreenshotAsTexture()` do Unity — já existe em `LeituraAgregados`.

## Configuração

**Default desabilitada** (opt-in):
```csharp
private ConfigEntry<bool> _habilitado;
private ConfigEntry<string> _caminhoSaida;
private ConfigEntry<float> _orcamentoSegundos;
```

**Regra:** Sem `_habilitado == true`, o core não executa nenhum método — apenas retorna `{ "status": "NAO_EXERCITADO" }`.

## Dependências do Core

- `BepInEx` (5.4.23.5) — configurações base
- `0Harmony` — hooks opcionais
- `UnityEngine` — captura de PNG, recursos
- `Unity.TextMeshPro` — leitura de textos (opcional, depende do jogo)

**NÃO depende:**
- `Assembly-CSharp` (Stolen Realm)
- Scripts específicos de qualquer jogo
- `biblioteca-de-terceiros`

## Exemplo de uso (pseudocódigo)

```csharp
// Inicialização
var core = new CorePlugin();
core.RegistrarSessao("sessao-001", DateTime.Now, "dev");

// Verificar habilitação
if (!core.EstaHabilitado())
    return Json.Campos("status", "NAO_EXERCITADO");

// Registrar identidade
var identidade = core.CalcularIdentidade(hashFonteDeclarado);

// Ler componente alvo
var inventario = core.LerComponente<T>(10);

// Capturar PNG
var pngSucedido = core.CapturarPNG("scratch/captura.png", 1920, 1080);

// Registrar evento
core.RegistrarEvento("leitura_concluida", "inventario", new { total = 42 });

// Retornar JSON consolidado
return Json.Campos(
    "sessao", core.ObterIdSessao(),
    "identidade", identidade,
    "inventario", inventario,
    "capture_png", pngSucedido,
    "eventos", core.ObterEventos()
);
```

## Critérios de aceitação

- [ ] Core compila separadamente do Adapter (sem `Assembly-CSharp`)
- [ ] Configuração default false (`_habilitado`)
- [ ] Retorna `{ "status": "NAO_EXERCITADO" }` se desabilitado
- [ ] Identidade calcula hash SHA256 da própria DLL
- [ ] Ler componentes genéricos retorna `null` se não existir
- [ ] Captura PNG retorna `false` se módulo indisponível
- [ ] Todos os eventos registrados em lista estruturada
- [ ] Serialização JSON sem dependências externas (reusar `Json.cs`)

## Equivalência provada

**Antes:** AUT4ProbePlugin.cs (1084 linhas)  
**Depois:** Core (~400 linhas) + Adapter SR (~684 linhas)

**Prova de equivalência:**
1. Comparar saída de `ex1-offline.json` antes/depois da refatoração
2. Hash SHA256 do Adapter SR deve bater com parte específica do AUT4Probe original
3. Core deve gerar mesma identidade que `IdentidadeDoProbe`
4. Testes offline (`testes/t_aut4_probe_contrato.py`) devem passar

## Próximos passos

1. Criar `tools/automacao/runtime/KIT04Core/`
2. Copiar `Json.cs` para Core (namespace `KIT04Core`)
3. Renomear `IdentidadeDoProbe.cs` → `IdentidadeDoCore.cs` (namespace `KIT04Core`)
4. Criar interfaces: `ICoreSession.cs`, `ICoreIdentidade.cs`, `ICoreEvento.cs`, `IComponentReader.cs`, `IPictureCapture.cs`
5. Implementar `CorePlugin.cs` (baseado em `Aut4ProbePlugin.cs` mas sem hooks Harmony específicos)
6. Build com `dotnet build -c Release KIT04Core.csproj -p:DeployToBepInEx=false`
7. Validar equivalência contra `runtime/out/ex1-offline.json`

**Data:** 2026-10-08  
**Status:** Especificação definida — aguarda implementação
