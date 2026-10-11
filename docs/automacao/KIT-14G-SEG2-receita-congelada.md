# KIT-14G-SEG2 — Receita congelada do instrumento AUT4Probe

## Par congelado (fonte + DLL)

| Artefato | sha256 | Caminho no repo |
|----------|--------|-----------------|
| AUT4ProbePlugin.cs | `beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193` | `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` |
| AUT4Probe.dll | `7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee` | `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` |

## Receita de reconstrução

```bash
cd C:/dev/stolen-realm/tools/automacao/runtime/AUT4Probe
dotnet build -c Release
```

A saída é `bin/Release/AUT4Probe.dll`. Verificar o sha256.

## PROBE_SHA para a bancada

```
PROBE_SHA = 7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee
```

## Histórico de receitas

| Versão | Fonte sha256 | DLL sha256 | Data |
|--------|-------------|------------|------|
| Congelado original (perdido) | ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2 | 95069e9cbc5e1e7784f80b34589e54cf19651969cddad86b6a35d9b94c89a865 | — |
| Congelado restaurado (esta receita) | beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193 | 7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee | 2026-10-11 |

## Observações

- A receita original (§5 de KIT-14G-SEG2-parte01.md) tinha um par (ecdcce13… / 95069e9c…) que não
  existe em nenhum lugar da árvore. Foi identificado que a fonte da árvore (beaf965a…) é a que
  carrega os marcos de clique / gate CliqueFisico / SilencioAposClique do run714.
- O rebuild a partir dessa fonte produz a DLL 7f9a4cf1…, que é a DLL já existente na árvore.
- O sandbox run712 tinha fonte 594c8add… e DLL 1d496dbc…, que é o PROBE_SHA atual em roda.py.
- A DLL não é reproduzível byte a byte em princípio (qualquer rebuild muda o hash); este rebuild
  coincidiu porque a árvore já contém a DLL correspondente ao fonte atual.
