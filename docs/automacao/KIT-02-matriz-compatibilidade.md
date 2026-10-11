# Matriz de Compatibilidade KIT-02

## Versões Suportadas

| Componente | Versão Mínima | Versão Testada | Notas |
|------------|---------------|----------------|-------|
| Unity | 2022.3.62f3 | 2022.3.62f3 | Versão atual do jogo |
| BepInEx | 5.4.23.5 | 5.4.23.5 | Compatível com Mono |
| biblioteca-de-terceiros | 0.1.0 | 0.1.0 | API oficial do jogo |
| Harmony | 2.10.2+ | 2.10.2 | Usado por BepInEx |

## Depreciações e Migrações

### Política de Versionamento
- **Semântico (MAJOR.MINOR.PATCH)**
  - MAJOR: breaking changes no schema
  - MINOR: novas features (backward compatible)
  - PATCH: correções de bugs

### Depreciações Planejadas
- **Nenhuma depreciação imediata**: Core é projetado para ser forward-compatible

## Regras de Compatibilidade

### Rejeição de Versão Desconhecida
```
if (schema_version > current_version) {
    Log.Warn("Schema {schema_version} não suportado, usando modo seguro");
    return SafeModeResult;
}
```

### Prevenção de Falsa Aprovação
- Validação estrita de schema (JSON Schema Validator)
- Testes de contra-prova (injetar defeito → ver falhar)
- Logs detalhados de todas as etapas

## Plano de Migração

### Preservação de Formatos Existentes
- Leitor backward-compatible para AUT-4-estado.json v0.x
- Mapeamento de campos antigos → novos
- Logging de warnings para campos deprecados

### Estratégia de Upgrade
1. Versão v1.0.0: MVP inicial (sem breaking changes)
2. Versão v1.x.0: Novos recursos (backward compatible)
3. Versão v2.0.0: Breaking changes (documentar migração)

## Dependências Opcionais

### Não Dependências Obrigatórias
- Core/Adapter nunca dependência obrigatória dos mods testados
- Uso básico funciona sem Hermes, IA, credenciais ou assinatura
- SDK posterior não pode bloquear MVP inicial

### Extensões Opcionais
- Agent IA: leitura de dados, análise (não requerido para funcionamento básico)
- Report Viewer: exportação HTML/Markdown (opcional)
- Scenario Runner: execução automatizada (opcional)
