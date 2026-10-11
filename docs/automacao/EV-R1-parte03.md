# EV-R1 — parte 03: leitura íntegra dos eventos

Errata da parte 02: o inventário v2 varreu **cinco arquivos `.assets` e três cenas**, oito arquivos ao todo, não sete `.assets` e três cenas. `globalgamemanagers` (sem extensão) ainda deve ser verificado separadamente; não está implicitamente incluído.

## Resultado offline exercitado

Comando: `python scan_assets_v7.py > scan-assets-v7.txt 2>&1`, exit 0.

Fonte: `evidencias/assets/resources-extraidos-v7.json`.

- PartyEvent: 256 lidos integralmente / 256 cabeçalhos identificados.
- ListHolderEvents: 256 referências / 256 referências únicas.
- EventStatus: 177 lidos / 177 identificados.
- QuestInfo: 54 lidos / 54 identificados.
- SkillInfo: 694 lidos; CharacterAttribute: 321; BattleInfo: 14.
- Erros de leitura desses registros: 0. Cada registro passou pela checagem de consumo integral dos bytes e pela comparação do cabeçalho m_Script/m_Name com o leitor nativo.

A reconciliação final de IDs, as referências e o schema ainda serão validados por testes.

## Correção do leitor (não modifica o jogo)

As tentativas v3 a v6 foram preservadas como diagnóstico. O gerador de typetree fornece um cabeçalho com alinhamento inadequado e identifica algumas coleções de string como strings escalares. Corrigimos o nó apenas em memória: cabeçalho do TPK nativo e coleções identificadas pela estrutura `Array/data string` passam a `vector`.

A implementação Boost mantinha a leitura escalar mesmo após o nó aparecer corrigido no dump textual. A alternativa v7 desabilita `TypeTreeHelper.read_typetree_boost` e exercita o leitor Python; os sete eventos antes ausentes, as duas EventStatus antes ausentes e todas as QuestInfo agora passam pelo consumo integral dos bytes. Evidências: `scan-assets-v5.txt`, `scan-assets-v6.txt`, `scan-assets-v7.txt`, `PartyEvent-typetree-v7.txt`.

## Particionamento proposto, baseado em campo serializado

EventSpawnTypes medido nos 256 eventos:

- Normal `[0]`: 160.
- NotInEventPool `[3]`: 84.
- Array vazio `[]`: 10.
- AfterBattle `[1]`: 1.
- QuestStart `[2]`: 1.

Estes são os lotes técnicos de revisão, não uma categorização temática inventada. Eventos desabilitados continuam no inventário: 42 têm `disabled=1`, 214 têm `disabled=0`. Isso não equivale a provar disponibilidade em qualquer partida: filtros de modo, história, nível e status continuam preservados.

Ouro/XP finais, sorteios, localização ativa e disponibilidade efetiva em partida: NÃO_EXERCITADO, por limite explícito de não usar runtime/jogo. A entrega preservará fórmulas, tabelas e referências sem fabricar resultados.
