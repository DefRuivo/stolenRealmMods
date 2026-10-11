# EV-R1 — schema 1.0.0 e guia de uso

## Comece aqui

- `indice-v2.md`: todos os 256 eventos, particionados pelo campo autoral EventSpawnTypes.
- `revisao-por-evento-v2.md`: todos os textos, opções, ações, condições, efeitos e configurações de recompensa em um documento.
- `lote-*-v2.md`: documentos separados para os cinco lotes humanos.
- `eventos.json`: documento canônico para IA; os strings originais são preservados, inclusive espaços, controles CR/LF e placeholders.
- `eventos.schema.json`: JSON Schema draft 2020-12, versão 1.0.0.
- `eventos-originais.json`: os 256 objetos PartyEvent sem normalização de campos.
- `catalogo-referencias.json`: 2.399 registros de apoio e 3.214 resumos de referências; consulte por `arquivo:path_id`.
- `cobertura.json`, `fontes.json`, `enums.json`, `prova-roundtrip.json`: prova de origem e cobertura.
- `auxiliares-nao-decodificados/`: bytes originais e manifesto dos três ActionInfoTest não decodificados.

Os Markdown sem sufixo `-v2` são a primeira renderização, preservada como histórico. Prefira os `-v2`: desabilitam tradução automática de nova linha na escrita no Windows. Não houve reescrita do inglês ou dos dados JSON.

## Identidade e escopo

`schema_version` é `1.0.0`. A raiz tem `fontes`, `cobertura`, `eventos`.

`eventos[].chave` é a chave única do inventário, no formato `resources.assets:path_id`. `id` é o GUID real do jogo, não um GUID criado pelo extrator. Há uma duplicação real de GUID entre Battle e Battletest Event; ambos ficam no documento. A chave física é estável para os assets desta instalação, identificada pelos SHA-256 de fontes; não é promessa de estabilidade entre atualizações do jogo. Não una nem elimine registros usando apenas `id` ou título.

Todos os PartyEvent encontrados são incluídos, inclusive 42 com `disabled=1`, protótipos, eventos encadeados, sem pool e fora do pool aleatório. `disabled=0` não significa comprovadamente disponível em uma partida: há filtros e overrides adicionais no jogo.

## Evento

- `categoria`: nomes dos valores de EventSpawnTypes unidos por `+`; array vazio usa `SemPoolDeclarado`. Não é classificação temática inferida.
- `titulo`: EventNameOverride quando não é vazio/branco; senão m_Name, conforme PartyEvent.EventName.
- `texto`, `texto_resultados_possiveis`: encounterText e encounterPossibleResultsText, sem tradução ou substituição de tokens.
- `raridade`, `pool`, `modos`, `historia`, `full_release`: enum representado por `{valor, nome}`. Nomes vêm dos enums do assembly decompilado; `enums.json` guarda o dicionário.
- `peso`: ChanceRatio, peso relativo configurado. Não é percentual absoluto de ocorrência. WorldMapGenerator.GetRandomEvent combina peso, deck, filtros, fortuna e fallback.
- `condicoes`: flags originais de disponibilidade, nível, terreno, horário, nó, status, minor/major e manutenção no deck.
- `origem`: arquivo, path_id, caminhos do ResourceManager, hash do objeto e tipos de código que definem/consomem os campos.
- `campos_originais`: objeto serializado inteiro, para recuperar campos não promovidos ao schema de leitura.
- `ausencias`: mapa de caminhos de todos os nulls do evento para sua razão. Strings vazias e arrays vazios existentes no asset NÃO viram null.

## Opção e ação

`opcoes[]` contém índice de base 1, título, descrição, condições, rolagem, efeitos, recompensas e campos originais. Índices são coordenadas de leitura, não IDs novos do jogo.

`opcoes[].efeitos[]` representa cada EventAction, mantendo a ordem original. Contém texto de ativação, EventResultType, RollLimit autoral, textos manuais, EventActionEffects, todos os overrides por FullReleaseMode, batalha e evento encadeado. `opcoes[].recompensas` é uma projeção redundante das mesmas configurações por ação/variante, conveniente para busca por IA; NÃO é recompensa adicional cumulativa.

Cada EventActionEffects mantém saúde/mana, configuração de alvo, remoções de status, recompensas e os campos originais. Alvo default serializado não é necessariamente o alvo calculado na partida. A escolha entre efeitos padrão e overrides depende do modo do jogo; o dump não escolhe uma variante por conta própria.

## Recompensas e referências

- Ouro: flags dar/retirar e razão originais. `quantidade_final=null` com motivo: depende de GetQuestGold(nível), razão e multiplicador roguelike.
- XP: flag e razão originais. O código pode converter XP em ouro no roguelike ou quando todos os personagens alcançaram nível 30; não trate a flag como XP garantido.
- Itens: pool_tipo, quantidade_configurada, LootTable inline, chances autorais e LootRestrictions. `sorteio_final=null`. `itemCount` é parâmetro; não prova que todos os itens finais vêm desse único ramo.
- Status/fortunas: candidatos por PPtr, descrição, duração e modificadores de atributo, com nomes/formulas originais. pickRandomStatus e randomStatusCount são preservados; não escolhemos candidatos.
- Skills: referências mantidas; campos completos e relações adicionais estão no catálogo.
- PPtr nulo tem `chave=null`, `nome=null` e motivo explícito. Referência não nula tem chave, PPtr e nome quando recuperável. Ícones, prefabs e assets nativos têm resumo, não cópia de textura/malha.

Strings como `[o1a1_status]`, `[0]`, tags de cor e fórmulas ficam intactos. Preenchê-los como se fossem o resultado de uma partida seria inventar dados. Os status candidatos ajudam a revisar o significado, mas não autorizam substituir tokens aleatórios pelo primeiro candidato.

## O que não foi exercitado / expandido

- Não houve lançamento do jogo, runtime Unity, plugin, instalação/deploy ou publicação.
- Não foram calculados resultados de RNG, quantidades finais de ouro/XP/loot, disponibilidade efetiva numa party ou tradução selecionada.
- Os pools universais de itens são preservados como configuração/regras/tabelas e referências. Não é um censo de TODOS os ItemInfo do jogo nem uma enumeração de cada item elegível a cada nível.
- Odin: NamedGuid Id/Guid inicial foi decodificado; demais bytes Odin dos objetos de apoio permanecem literais em serializationData. Não declaramos interpretar universalmente todas as estruturas privadas/dicionários Odin.
- Três ActionInfoTest auxiliares falharam na leitura integral. Nenhum é referência direta de PartyEvent; seus bytes originais, nomes, IDs e hashes foram guardados. Não foram inventados campos para eles.
- Os 30 outros objetos com paths `events/` não são PartyEvent e não viraram eventos narrativos. Cenas, UI, fontes, áudio, meshes e assets de apresentação não são opções narrativas extras.

## Reprodução e validação

Use Python 3.14.7 e dependências isoladas no diretório de trabalho:

    python -m pip install --target dependencias UnityPy==1.25.4 TypeTreeGeneratorAPI==0.0.10 jsonschema==4.26.0

A origem instalada é fixa em leitor_offline.py (`ROOT`). Para outra instalação, copie os scripts para uma pasta nova e ajuste ROOT; não sobrescreva resultados existentes.

Os scripts `scan_assets_v2.py`, `scan_assets_v7.py`, `scan_catalogo_v9.py` e `gerar_entrega.py` usam criação exclusiva de arquivos. A cadeia histórica exige os v2/v7 JSON e a varredura de ResourceManager descrita na parte 04; o pacote inclui esses insumos de auditoria selecionados. `reproduzir_offline.py` fornece o caminho consolidado para extração nova, sem as falhas diagnósticas.

Validação contra os assets instalados:

    python test_eventos_v3.py

Resultado real: 22 testes, OK (`testes-03.txt`). Inclui releitura offline independente dos 256 objetos, roundtrip dos 256 PartyEvent e 177 EventStatus, schema, preservação de strings/recompensas/overrides, caminhos, cobertura, lotes e três controles negativos (remover evento, fabricar recompensa final, remover campo obrigatório).

O SHA-256 de Assembly-CSharp.dll permaneceu `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`. Todos os arquivos do jogo e o repo foram somente lidos.
