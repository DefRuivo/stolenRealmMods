# BetterTexts

Mod para **Stolen Realm** que melhora textos, descrições e tooltips — sem alterar gameplay.

- **GUID:** `com.gumatos.bettertexts`
- **Versão:** 0.1.0
- **Dependências:** BepInEx 5 (instalado no perfil do r2modman)

## Compilar

```powershell
cd C:\dev\stolen-realm\BetterTexts
dotnet build
```

Saída: `bin\Debug\netstandard2.1\BetterTexts.dll`

## Instalar (manual)

Copiar a DLL para:

```text
C:\Users\<usuario>\AppData\Roaming\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\BetterTexts\
```

## Testar

1. Abrir o r2modman → perfil **Default** → **Start modded**
2. Conferir `LogOutput.log` (na pasta `BepInEx\` do perfil): deve aparecer `[Info :Better Texts] Better Texts carregado.`

## Remover

Apagar a pasta `BetterTexts` dentro de `BepInEx\plugins\` (ou desabilitar no r2modman).
