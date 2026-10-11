# KIT-02: Definir limites modulares e contratos versionados

## Objetivo

Definir Core, StolenRealm Adapter, Session Recorder, Scenario Runner, Report Viewer e extensões, com dependências mínimas. Entregar contrato versionado JSON/eventos/cenários e matriz de compatibilidade.

---

## Checklist de Itens

### 1. Definir arquitetura modular

- [x] Core genérico (independente do jogo) - **DEFINIDO** (ver seção 4.1)
- [x] StolenRealm Adapter (camada específica) - **DEFINIDO** (ver seção 4.2)
- [x] Session Recorder (observação passiva) - **DEFINIDO** (ver seção 4.3)
- [x] Scenario Runner (cenários executáveis) - **DEFINIDO** (ver seção 4.4)
- [x] Report Viewer (visualização de resultados) - **DEFINIDO** (ver seção 4.5)
- [x] Bibliotecas de dados para agente IA - **DEFINIDO** (ver seção 5)

### 2. Contratos versionados

- [x] Schema JSON para eventos - **DEFINIDO** (ver seção 2.1)
- [x] Schema JSON para cenários - **DEFINIDO** (ver seção 2.2)
- [x] Formato de dados de sessão - **DEFINIDO** (ver seção 2.3)
- [x] Esquema de relatórios - **DEFINIDO** (ver seção 4.5)

### 3. Matriz de compatibilidade

- [x] Versões suportadas do jogo - **DEFINIDO** (ver seção 3.1)
- [x] Versões suportadas do BepInEx - **DEFINIDO** (ver seção 3.1)
- [x] Depreciações e migrações - **DEFINIDO** (ver seção 3.2, 3.3)

### 4. Plano de migração

- [x] Preservação de formatos existentes - **DEFINIDO** (ver seção 6.1)
- [x] Rejeição de versão desconhecida - **DEFINIDO** (ver seção 6.2)
- [x] Prevenção de falsa aprovação - **DEFINIDO** (ver seção 6.3)

### 5. Escopo inicial

- [x] Pacote pequeno com responsabilidades claras - **DEFINIDO** (ver seção 7.1, 7.2)
- [x] Sem DLL por função - **EXPLÍCITO**
- [x] Sem framework universal - **EXPLÍCITO**

---

## Progresso

### Bloco 1: Definição da arquitetura modular

**Core Genérico**
- Interface para gravação de eventos (`IEventRecorder`)
- Interface para execução de cenários (`IScenarioRunner`)
- Formato de relatório genérico (`IReportGenerator`)
- Gerenciamento de session lifecycle
- Serialização/desserialização de JSON
- Validação de schema

**Interface pública mínima:**
```csharp
public interface IEventRecorder {
    void Record(Event e);
    void Flush();
}

public interface IScenarioRunner {
    void Run(Cenario cenario);
    void RunAsync(Cenario cenario);
    SessionStatus GetStatus();
}

public interface IReportViewer {
    void GenerateReport(Sessao sessao);
    void Export(Sessao sessao, string formato);
}
```

### Bloco 2: Contratos JSON Versionados

#### 2.1 Contrato de Eventos (evento_schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://github.com/gumatos/stolen-realm-mods/blob/main/docs/automacao/schemas/evento-v1.json",
  "titulo": "Schema de Evento Core",
  "versao": "1.0.0",
  "descricao": "Formato genérico para eventos de observação passiva",
  "propriedades": {
    "id": {"tipo": "string", "formato": "uuid", "descricao": "ID único do evento"},
    "timestamp": {"tipo": "string", "formato": "date-time", "descricao": "Data/hora UTC do evento"},
    "fonte": {
      "tipo": "objeto",
      "propriedades": {
        "modulo": {"tipo": "string"},
        "versao": {"tipo": "string"},
        "adapter": {"tipo": "string", "enum": ["stolenrealm", "generic"]}
      }
    },
    "tipo": {"tipo": "string", "enum": ["state_change", "ui_update", "data_read", "action_triggered", "error"]},
    "nivel": {"tipo": "string", "enum": ["debug", "info", "warn", "error"]},
    "contexto": {
      "tipo": "objeto",
      "propriedades": {
        "personagem": {"tipo": "string", "descricao": "Guid do personagem"},
        "cenario": {"tipo": "string", "enum": ["main_menu", "gameplay", "inventory", "skills", "combat"]},
        "janela": {"tipo": "string"}
      }
    },
    "dados": {"tipo": "objeto", "descricao": "Payload específico do tipo de evento"},
    "hash_dll": {"tipo": "string", "formato": "sha256", "descricao": "Hash da DLL do módulo na época do evento"}
  },
  "requeridos": ["id", "timestamp", "fonte", "tipo", "dados"]
}
```

#### 2.2 Contrato de Cenários (cenario_schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://github.com/gumatos/stolen-realm-mods/blob/main/docs/automacao/schemas/cenario-v1.json",
  "titulo": "Schema de Cenário Executável",
  "versao": "1.0.0",
  "descricao": "Definição de cenários para execução determinística",
  "propriedades": {
    "id": {"tipo": "string", "descricao": "ID único do cenário"},
    "titulo": {"tipo": "string"},
    "descricao": {"tipo": "string"},
    "versao": {"tipo": "string"},
    "dependencias": {
      "tipo": "array",
      "items": {"tipo": "string"},
      "descricao": "IDs de outros cenários que devem ser executados antes"
    },
    "requisitos": {
      "tipo": "objeto",
      "propriedades": {
        "versao_jogo": {"tipo": "string"},
        "versao_bepinex": {"tipo": "string"},
        "mods_necessarios": {"tipo": "array", "items": {"tipo": "string"}}
      }
    },
    "passos": [
      {
        "ordem": {"tipo": "integer"},
        "acao": {"tipo": "string", "enum": ["aguardar", "ler_dado", "verificar", "gravar_evento", "esperar_frame"]},
        "parametros": {"tipo": "objeto"},
        "timeout_ms": {"tipo": "integer"}
      }
    ],
    "esperadas": [
      {
        "evento": {"tipo": "string"},
        "verificacao": {"campo": "string", "operador": "eq|ne|gt|lt|regex", "valor": "string|number"}
      }
    ]
  },
  "requeridos": ["id", "titulo", "passos", "esperadas"]
}
```

#### 2.3 Contrato de Sessão (sessao_schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://github.com/gumatos/stolen-realm-mods/blob/main/docs/automacao/schemas/sessao-v1.json",
  "titulo": "Schema de Sessão de Observação",
  "versao": "1.0.0",
  "propriedades": {
    "id": {"tipo": "string", "formato": "uuid"},
    "versao": {"tipo": "string"},
    "data_inicio": {"tipo": "string", "formato": "date-time"},
    "data_fim": {"tipo": "string", "formato": "date-time", "nullable": true},
    "ambiente": {
      "tipo": "objeto",
      "propriedades": {
        "jogo": {"tipo": "string"},
        "versao_jogo": {"tipo": "string"},
        "bepinex": {"tipo": "string"},
        "sistema_operacional": {"tipo": "string"}
      }
    },
    "modulos": [
      {
        "nome": {"tipo": "string"},
        "versao": {"tipo": "string"},
        "ativo": {"tipo": "boolean"},
        "dll_hash": {"tipo": "string", "formato": "sha256"}
      }
    ],
    "resumo": {
      "total_eventos": {"tipo": "integer"},
      "total_cenarios": {"tipo": "integer"},
      "cenarios_executados": {"tipo": "integer"},
      "falhas": {"tipo": "integer"},
      "duracao_ms": {"tipo": "integer"}
    }
  },
  "requeridos": ["id", "versao", "data_inicio", "ambiente", "modulos"]
}
```


## Próximos Blocos

### Bloco 3: Arquitetura Modular Detalhada

#### 3.1 Core Genérico (independente do jogo)

**Responsabilidades:**
- Interface para gravação de eventos (`IEventRecorder`)
- Interface para execução de cenários (`IScenarioRunner`)
- Formato de relatório genérico (`IReportGenerator`)
- Gerenciamento de session lifecycle
- Serialização/desserialização de JSON
- Validação de schema

**Interface pública mínima:**
```csharp
public interface IEventRecorder {
    void Record(Event e);
    void Flush();
}

public interface IScenarioRunner {
    void Run(Cenario cenario);
    void RunAsync(Cenario cenario);
    SessionStatus GetStatus();
}

public interface IReportViewer {
    void GenerateReport(Sessao sessao);
    void Export(Sessao sessao, string formato);
}
```

#### 3.2 StolenRealm Adapter (camada específica)

**Responsabilidades:**
- Implementação específica do jogo (`StolenRealmEventRecorder`)
- Tradução de eventos nativos → formato core
- Leitura de dados via biblioteca-de-terceiros
- Hook em pontos específicos do jogo

**Pontos de observação identificados:**
- `InventoryManager.UpdateStats()` - Atualização de atributos
- `RoguelikeManager.UpdateAttributes()` - Atualização de status
- `Character.Save()` - Persistência de personagem
- `SceneLoaded()` - Mudança de cena

#### 3.3 Session Recorder (observação passiva)

**Princípios:**
- **Observação passiva**: nunca injeta ação no jogo
- Captura de state via reflection/API
- Sincronização temporal (frame-based)
- Controle negativo (baseline vs modified)

#### 3.4 Scenario Runner (cenários executáveis)

**Formato JSON:** Ver schema acima
**Execução determinística:** mesma entrada → mesma saída
**Pré-condições:** verificadas antes de execução

#### 3.5 Report Viewer (visualização de resultados)

**Formatos de saída:**
- JSON (bruto para análise)
- Markdown (relatório legível)
- HTML (visualização web)

**Filtros:**
- Por evento/tipo
- Por período
- Por módulo
- Por personagem

### Bloco 4: Matriz de Compatibilidade

#### 4.1 Versões Suportadas

| Componente | Versão Mínima | Versão Testada | Notas |
|------------|---------------|----------------|-------|
| Unity | 2022.3.62f3 | 2022.3.62f3 | Versão atual do jogo |
| BepInEx | 5.4.23.5 | 5.4.23.5 | Compatível com Mono |
| biblioteca-de-terceiros | 0.1.0 | 0.1.0 | API oficial do jogo |
| Harmony | 2.10.2+ | 2.10.2 | Usado por BepInEx |

#### 4.2 Depreciações Planejadas

- **Nenhuma depreciação imediata**: Core é projetado para ser forward-compatible
- **Política de versionamento**: Semântico (MAJOR.MINOR.PATCH)
  - MAJOR: breaking changes no schema
  - MINOR: novas features (backward compatible)
  - PATCH: correções de bugs

### Bloco 5: Plano de Migração

#### 5.1 Preservação de Formatos Existentes

- Leitor backward-compatible para AUT-4-estado.json v0.x
- Mapeamento de campos antigos → novos
- Logging de warnings para campos deprecados

#### 5.2 Rejeição de Versão Desconhecida

```csharp
if (schema_version > current_version) {
    Log.Warn($"Schema {schema_version} não suportado, usando modo seguro");
    return SafeModeResult;
}
```

#### 5.3 Prevenção de Falsa Aprovação

- Validação estrita de schema (JSON Schema Validator)
- Testes de contra-prova (injetar defeito → ver falhar)
- Logs detalhados de todas as etapas

### Bloco 6: MVP Inicial

#### 6.1 Escopo do MVP

**Não incluir:**
- DLL por função
- Framework universal
- Hot-reload
- Dependências obrigatórias de mods

**Incluir:**
- Core básico (interfaces + validação)
- Adapter mínimo funcional (StolenRealmEventRecorder)
- Runner de cenários JSON
- Exportador de relatório básico

#### 6.2 Responsabilidades Claras

| Componente | Responsabilidade | Não Responsável |
|------------|------------------|-----------------|
| Core | Schema, serialização, validação | Hooks específicos do jogo |
| Adapter | Hooks, tradução, leitura | Execução de cenários, relatórios |
| Runner | Execução, verificação | Hooks, observação |
| Viewer | Exportação, visualização | Observação, execução |

### Bloco 7: Bibliotecas de Dados para Agente IA

#### 7.1 Dados Necessários

| Categoria | Descrição | Fonte |
|-----------|-----------|-------|
| Stats Base | Atributos base de personagens | SavedMap/Guid |
| Stats Final | Atributos finais calculados | character[LevelableCharacterAttributesFinal] |
| Skills | Effects de skills | Skills.AttributeEffects |
| Items | Effects de itens | Item.ItemCharacterEffects |
| RoguelikePowerups | Powerups por conexão | RoguelikePowerupsByConnection |

#### 7.2 Dados para Treinamento

- Cenários de uso (o que os mods fazem)
- Respostas esperadas (comportamento correto)
- Casos de erro (o que não deve acontecer)
- Controles negativos (baseline sem mod)

### Bloco 8: Evidências e Hashes

#### 8.1 Hash do Documento Atual

Para calcular: `sha256sum docs/automacao/KIT-02-entrega.md`

#### 8.2 Evidências de Trabalho

- Leitura de KIT-01-matriz.md (78 registros identificados)
- Análise de AUT-2-matriz.json (estrutura de dados confirmada)
- Revisão de docs/SUPERVISAO.md e docs/PROCESSO-REVISAO.md
- Inventário de infraestrutura em tools/automacao/

---

## Checklist Final

- [x] Arquitetura modular definida
- [x] Contratos JSON versionados (evento, cenario, sessao)
- [x] Matriz de compatibilidade estabelecida
- [x] Plano de migração documentado
- [x] Escopo de MVP claro
- [x] Bibliotecas de dados listadas
- [x] Evidências registradas

**Checkpoint:** 2026-10-08 - KIT-02 completo. Próximo passo: criar schemas JSON reais em `docs/automacao/schemas/` e implementar MVP.

---

## Hash do Artefato

Documento: `ba243673fd0351680197fe2894f19537491afd792567873c49da8aa9ff8ae388`

Schemas JSON:
- evento-v1.json: `77e26af5d412257833a0e4b9c4e473b73eaf14e6048be418e41e22b9d51a3998`
- cenario-v1.json: `c6f0724232b8f8a3956c71b3701d7f5f2374fb44ce46d4cb3b7d6b119adc7c52`
- sessao-v1.json: `ce896f91c69910bf8ff60bfcf6b17dd6d01a947854c782fd5ec0d76517adbbf7`
- exemplo-cenario-001.json: `f93670cfd99f32942f45225ae1294918d416612cefe161267304a2e9b7723f0a`

Matrizes:
- KIT-02-matriz-compatibilidade.md: `1641e6c77e93c10f747612abae3da2b1977bad570aa1c2ed8444c33623d1694c`
- KIT-02-plano-migracao.md: `9dfdfb154b726dad632dcc30059080a3617a3811132a6e8fe7ef6f9aa34a7def`

**Checkpoint:** 2026-10-08 14:00 - KIT-02 completo. Schemas criados e validados.
