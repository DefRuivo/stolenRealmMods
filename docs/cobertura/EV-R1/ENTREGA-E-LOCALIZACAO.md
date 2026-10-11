# EV-R1 — onde está a entrega (localização durável)

Nota de fechamento da tarefa `t_48d68679`. Não houve sobrescrita de artefatos anteriores:
todos os arquivos abaixo são NOVOS no repositório e foram copiados byte a byte do workspace da tarefa.

## 1. Dados extraídos (revisão humana e IA)

    C:/dev/stolen-realm/docs/cobertura/EV-R1/

- `LEIA-ME.md` — porta de entrada; limites explícitos e como reproduzir.
- `eventos.json` — documento canônico (256 eventos, 404 opções, 449 ações).
- `eventos.schema.json` — JSON Schema draft 2020-12, versão 1.0.0.
- `eventos-originais.json` — 256 objetos PartyEvent sem normalização.
- `catalogo-referencias.json` — 2.399 registros de apoio; 3.214 resumos de referências.
- `cobertura.json`, `fontes.json`, `enums.json`, `prova-roundtrip.json` — prova de origem e cobertura.
- `indice.md` / `indice-v2.md` — índice humano dos 256 eventos por EventSpawnTypes.
- `revisao-por-evento.md` / `-v2.md` — leitura contínua de textos, opções, efeitos e recompensas.
- `lote-Normal-v2.md` (160), `lote-NotInEventPool-v2.md` (84), `lote-SemPoolDeclarado-v2.md` (10),
  `lote-AfterBattle-v2.md` (1), `lote-QuestStart-v2.md` (1) — insumo dos cinco cartões de revisão humana.
- `auxiliares-nao-decodificados/` — bytes originais e manifesto dos três ActionInfoTest não decodificados.
- `EV-R1-entrega.zip` — pacote completo (44 MB): dados, evidências de asset, decompilado de referência,
  rotina de reprodução e testes.

Os Markdown sem sufixo `-v2` são a primeira renderização, preservados como histórico; a primeira gravação
sofreu tradução automática de nova linha no Windows. Prefira os `-v2`. Nenhum string de dados foi reescrito.

## 2. Relatórios incrementais

    C:/dev/stolen-realm/docs/automacao/EV-R1-parte01.md ... EV-R1-parte05.md

Partes 03 e 05 contêm erratas identificadas durante a verificação; os registros anteriores não foram alterados.

## 3. Contagem de cobertura entregue

- 256 PartyEvent extraídos / 256 cabeçalhos PartyEvent / 256 referências únicas no ListHolderEvents.
- 404 opções, 449 ações, 42 eventos com `disabled=1` mantidos.
- 255 GUIDs únicos; a duplicação real Battle/Battletest Event foi preservada.
- Chave única do inventário: `arquivo:path_id` (GUID e título podem repetir).

## 4. Como reconferir

A entrega no workspace `.../workspaces/t_48d68679` foi validada por `python test_eventos_v3.py`:
**Ran 22 tests in 45.784s — OK**. A cópia do repositório é idêntica byte a byte à do workspace
(33 arquivos comparados por SHA-256, 0 divergências).

Para validar esta pasta:

    python -m pip install --target dependencias UnityPy==1.25.4 TypeTreeGeneratorAPI==0.0.10 jsonschema==4.26.0
    python test_eventos_v3.py

Os scripts de validação não foram copiados para o repositório; eles estão dentro de `EV-R1-entrega.zip`
e no workspace da tarefa. A reconstrução independente (`repro-limpa/`) registrou
`eventos_identicos_ao_original=true` para os 256 eventos.

## 5. Declarado fora

Jogo/runtime, RNG, quantidades finais de ouro/XP/loot, disponibilidade efetiva numa party e tradução
selecionada NÃO foram exercitados; nesses campos `null` tem motivo, não é zero. Não há censo integral de
ItemInfo, nem decodificação universal dos bytes Odin auxiliares. Cenas, UI, áudio e apresentação não viram
opções narrativas. Detalhes em `LEIA-ME.md` e `schema.md`.
