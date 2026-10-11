# EV-R1 — parte 04: cobertura, IDs duplicados e grafo de referências

## Prova adicional

`python scan_catalogo_v9.py > scan-catalogo-v9.txt 2>&1` terminou com exit 0.

- 256/256 eventos fizeram roundtrip byte a byte: os campos extraídos, reserializados apenas em memória pelo leitor offline, reproduziram exatamente os bytes originais de cada objeto. Nenhum asset foi escrito.
- `globalgamemanagers` foi varrido separadamente: 19 objetos nativos, nenhum MonoBehaviour. ResourceManager contém 11.880 caminhos, com external index 4 explicitamente apontando para resources.assets.
- Todos os 256 PartyEvent estão em caminhos `events/`; há 30 outros objetos nesses caminhos, que não são PartyEvent. Não foram contados como eventos narrativos.
- ListHolderEvents declara 256 referências únicas, correspondentes ao inventário de cabeçalhos.

Evidências: `catalogo-v9.json`, `globalgamemanagers-v1.json`, `scan-global.txt`, `scan-catalogo-v9.txt` em `evidencias/assets/` ou na raiz do workspace.

## Identificador duplicado real — não deduplicar por GUID

Existem 256 assets, mas 255 GUIDs únicos. O GUID `5b740c2b-3480-48f2-997b-88c8291db0c0` ocorre em:

- resources.assets:2545539 — Battle.
- resources.assets:2545540 — Battletest Event.

A entrega preservará ambos e fornecerá `chave = arquivo:path_id`, junto ao GUID original `id`. Não será criado GUID substituto nem descartado evento.

## Referências de efeitos/recompensas

O catálogo v9 contém 2.399 registros integralmente lidos, incluindo os 256 eventos, 177 EventStatus, 54 QuestInfo, configurações GlobalSettings/RoguelikeSettings, tabelas inline, ItemInfo e dados de batalhas. Contém 3.214 resumos de referências.

Os erros secundários de CharacterInfo/ActionInfo do v8 foram resolvidos reconstruindo typetrees de SerializeReference a partir das classes do DLL instalado. O gerador inclui um cabeçalho MonoBehaviour também para classes gerenciadas simples; este cabeçalho foi removido apenas dos nós de SerializeReference. A prova de leitura integral permanece ativa.

Restam três objetos auxiliares `ActionInfoTest`: 2543665, 2543666, 2543671. Eles não são referências diretas de nenhum PartyEvent. O leitor acusa discrepância de bytes; nenhum valor deles será inventado. Serão declarados como fora da decodificação, com nomes/PPtrs e razão, e seus bytes originais serão preservados separadamente. Isso não reduz a cobertura 256/256 de definições PartyEvent.

## Não inferir resultados de runtime

`EventOption.Init` no arquivo decompilado, bloco l.150974–151068: XP pode virar ouro no roguelike ou quando ninguém da party está abaixo do nível 30. Ouro usa GetQuestGold, razões e GoldMultiplier; loot depende de tabelas/restrições e sorteio. Portanto flags `giveExperience/giveGold` não provam quantidades finais. A entrega conterá os parâmetros e fontes, e `null` com motivo para resultados dependentes de partida.

Valor efetivamente sorteado, quantidade final de ouro/XP, dados de uma party e localização selecionada: NÃO_EXERCITADO por limite explícito de não usar runtime/jogo.
