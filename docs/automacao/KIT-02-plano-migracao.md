# Plano de Migração KIT-02

## 1. Preservação de Formatos Existentes

### Leitor Backward-Compatible
- Leitor deve suportar AUT-4-estado.json v0.x
- Mapeamento de campos antigos → novos
- Logging de warnings para campos deprecados

### Regras de Migração
1. Se schema_version <= 1.0.0: processar normalmente
2. Se schema_version > 1.0.0: usar modo seguro
3. Se schema_version desconhecida: rejeitar com erro claro

## 2. Rejeição de Versão Desconhecida

### Implementação
```csharp
if (schema_version > current_supported_version) {
    Logger.Warn($"Schema {schema_version} não suportado, usando modo seguro");
    return SafeModeResult;
}

if (schema_version < minimum_supported_version) {
    Logger.Error($"Schema {schema_version} obsoleto, migração necessária");
    throw new IncompatibleSchemaException();
}
```

### Comportamento Esperado
- Versão antiga: erro claro, instruções de atualização
- Versão nova: modo seguro, log de warning
- Versão desconhecida: rejeição com hash do schema

## 3. Prevenção de Falsa Aprovação

### Validação Estrita
- JSON Schema Validator para todos os formatos
- Validação de tipos, formatos, enums
- Validação de campos obrigatórios

### Testes de Contra-Prova
- Injetar defeito → ver falhar
- Exemplos válidos → passar
- Exemplos inválidos → falhar claramente

### Logs Detalhados
- Registrar todas as etapas de validação
- Log de schema_version e hash
- Log de campos mapeados ou ignorados

## 4. Estratégia de Rollback

### Pontos de Rollback
1. Antes de aplicar migration
2. Após validação de schema
3. Antes de escrever dados migrados

### Procedimento
1. Detectar falha na migração
2. Reverter para versão anterior
3. Logar detalhadamente o erro
4. Manter dados originais intactos

## 5. Documentação de Migração

### Para Cada Breaking Change
- Descrição da mudança
- Exemplo antes/depois
- Script de migração (se aplicável)
- Prazo de depreciação

### Release Notes
- Listar todas as mudanças de versão
- Indicar breaking changes claramente
- Fornecer guia de migração
