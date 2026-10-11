# EV-R1 — inventário offline completo de PartyEvent

Entrega da tarefa t_48d68679. Não houve jogo/runtime, instalação de plugin, alterações no repo ou publicação.

## Abrir

Comece em `docs/cobertura/EV-R1/indice-v2.md`. Para leitura contínua: `revisao-por-evento-v2.md` nessa pasta. Para IA: `eventos.json` e `eventos.schema.json`. `schema.md` documenta os campos, identidade e limites.

Resultado: 256 eventos / 256 declarados no ListHolderEvents; 404 opções; 449 ações. Foram preservados 42 desabilitados e os eventos sem pool ou fora do pool. Existem 255 GUIDs únicos; Battle e Battletest Event compartilham um GUID real e não foram deduplicados. A identidade única é arquivo:path_id.

Lotes: Normal 160, NotInEventPool 84, SemPoolDeclarado 10, AfterBattle 1, QuestStart 1. Textos são os originais em inglês, não traduções nem propostas de melhoria.

## Verificação

`testes-03.txt`: 22 testes OK. Incluem schema, releitura dos 256 eventos, roundtrip byte a byte de 256 eventos e 177 status, preservação de textos/efeitos/recompensas/overrides, referências, índices, lotes e controles negativos.

`repro-limpa/testes-repro.txt`: outros 22 testes OK. `repro-conferencia.json` registra que os 256 eventos reconstruídos a partir dos assets instalados são idênticos aos originais desta entrega.

Os cinco relatórios `docs/automacao/EV-R1-parte01.md` a `parte05.md` são incrementais. As partes 03 e 05 contêm erratas identificadas durante a verificação; os registros anteriores não foram sobrescritos.

## Limites explícitos

- Ouro/XP/loot finais, RNG, disponibilidade efetiva e tradução selecionada não foram exercitados. NULL tem razão, não é zero. Configurações, tabelas, fórmulas, candidatos e PPtrs permanecem.
- 19 encounterText estão vazios no asset; nenhuma narrativa foi inventada.
- Três ActionInfoTest auxiliares não foram decodificados: os bytes e hashes estão em `auxiliares-nao-decodificados/`. Nenhum é referência direta de PartyEvent.
- 108 MonoBehaviour do inventário bruto têm m_Script.m_PathID=0 e não podem ser classificados; seus IDs/razões estão em `repro-limpa/evidencias/assets/inventario-limpo.json`. Não estão no ListHolderEvents nem nos cabeçalhos identificados de PartyEvent.
- Os 30 outros objetos com Resource paths `events/` não são PartyEvent. Não os contamos como narrativas.
- Não se alega inventário completo de ItemInfo nem decodificação universal das estruturas Odin auxiliares; bytes não interpretados permanecem nos dados originais.

## Reproduzir em pasta nova

Pré-requisitos: Python, ilspycmd 8.2.0.7535 e a instalação local indicada em leitor_offline.py. A reprodução nunca inicia Unity ou o jogo.

    python reproduzir_offline.py --out C:/caminho/nova-pasta

Sem `--deps`, a rotina instala UnityPy 1.25.4, TypeTreeGeneratorAPI 0.0.10 e jsonschema 4.26.0 em dependencias dentro da pasta nova. Para reutilizar dependências existentes, acrescente `--deps C:/caminho/dependencias`. A pasta de destino não pode existir.

Para somente validar a entrega, instale as versões acima em `dependencias` ao lado dos scripts e execute `python test_eventos_v3.py`. O pacote não contém dependências Python nem os assets/DLLs instalados do jogo. Contém dados extraídos, evidências e o decompilado de referência para revisão local.

## Revisão humana criada no Kanban

Todos os cartões estão bloqueados aguardando decisão humana, não autorização para implementação:

- t_004ed4b0 — 160 Normal: texto, escolhas, recompensas e condições dos eventos do pool principal.
- t_8e74c724 — 84 NotInEventPool: eventos encadeados/condicionais, sem presumir que fora do pool significa inútil.
- t_55517882 — 10 SemPoolDeclarado: array de spawn vazio, mantendo protótipos/variantes e fontes.
- t_b10171fa — 1 AfterBattle: revisar o evento autoral pós-batalha, mesmo sendo de teste/desabilitado.
- t_34205427 — 1 QuestStart: revisar a definição de início de quest.

Por evento, o dono registra manter ou melhorar, proposta exata e razão; separa wording, recompensa e condição. Nenhum desses cartões exige testar visualmente no jogo nesta etapa. Mudanças de mod ficam para cartões posteriores com decisão aprovada.
