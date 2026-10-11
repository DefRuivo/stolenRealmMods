# Schemas KIT-02

Esta pasta contém os schemas JSON versionados definidos pelo KIT-02.

## Schemas Disponíveis

### evento-v1.json
Schema para eventos de observação passiva. Versão 1.0.0.
- Hash SHA256: `77e26af5d412257833a0e4b9c4e473b73eaf14e6048be418e41e22b9d51a3998`

### cenario-v1.json
Schema para cenários executáveis. Versão 1.0.0.
- Hash SHA256: `c6f0724232b8f8a3956c71b3701d7f5f2374fb44ce46d4cb3b7d6b119adc7c52`

### sessao-v1.json
Schema para sessões de observação. Versão 1.0.0.
- Hash SHA256: `ce896f91c69910bf8ff60bfcf6b17dd6d01a947854c782fd5ec0d76517adbbf7`

### exemplo-cenario-001.json
Exemplo prático de cenário JSON seguindo o schema cenario-v1.json.
- Hash SHA256: `f93670cfd99f32942f45225ae1294918d416612cefe161267304a2e9b7723f0a`

## Uso

Todos os schemas seguem JSON Schema Draft-07. Para validar:

```bash
# Usando jq + jsonschema (exemplo)
jsonschema -i evento-v1.json -s docs/automacao/schemas/evento-v1.json
```

## Versionamento

- **MAJOR**: breaking changes no schema
- **MINOR**: novas features (backward compatible)
- **PATCH**: correções de bugs

## Referências

- Documento principal: [KIT-02-entrega.md](../KIT-02-entrega.md)
- Matriz de compatibilidade: [KIT-02-matriz-compatibilidade.md](../KIT-02-matriz-compatibilidade.md)
- Plano de migração: [KIT-02-plano-migracao.md](../KIT-02-plano-migracao.md)
