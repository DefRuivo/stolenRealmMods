# BetterTooltips

Mod para **Stolen Realm** que melhora textos, descrições e tooltips — sem alterar gameplay.

- **GUID:** `com.gumatos.bettertooltips`
- **Versão:** 0.1.0
- **Dependências:** BepInEx 5 (instalado no perfil do r2modman)

## Compilar

```powershell
cd C:\dev\stolen-realm\BetterTooltips
dotnet build
```

Saída: `bin\Debug\netstandard2.1\BetterTooltips.dll`

## Instalar (manual)

Copiar a DLL para:

```text
C:\Users\<usuario>\AppData\Roaming\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\BetterTooltips\
```

## Testar

1. Abrir o r2modman → perfil **Default** → **Start modded**
2. Conferir `LogOutput.log` (na pasta `BepInEx\` do perfil): deve aparecer `[Info :Better Tooltips] Better Tooltips carregado.`

## Remover

Apagar a pasta `BetterTooltips` dentro de `BepInEx\plugins\` (ou desabilitar no r2modman).
