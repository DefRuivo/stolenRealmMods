# EV-R1 — parte 05: entrega final validada e reprodução limpa

Errata da parte 04: o método que inicializa as recompensas é **EventOption.InitActions**, declarado na linha 150877 do decompilado, não `EventOption.Init`.

## Cobertura final

- 256 PartyEvent extraídos / 256 cabeçalhos PartyEvent / 256 referências únicas no ListHolderEvents.
- 404 opções e 449 ações; 42 eventos desabilitados mantidos.
- 255 GUIDs únicos: a duplicação Battle/Battletest Event foi preservada.
- 19 eventos têm encounterText vazio no asset. Permanecem strings vazias; não foi criado texto substituto.
- Cinco lotes: Normal 160, NotInEventPool 84, SemPoolDeclarado 10, AfterBattle 1, QuestStart 1.
- Todos os PPtrs não nulos de gameplay diretamente presentes nos PartyEvent resolvem para objetos decodificados; nenhum aponta para os três ActionInfoTest não decodificados.

## Testes executados

`python test_eventos_v3.py > testes-03.txt 2>&1`: **Ran 22 tests in 35.264s — OK**, exit 0.

A primeira renderização Markdown foi preservada, mas um teste encontrou tradução automática de CR/LF pelo gravador do Windows. `render_human_v2.py` cria novos arquivos `*-v2.md` com newline translation desabilitada. Os strings JSON nunca foram reescritos. Os testes iniciais que falharam estão preservados; não foram ocultados.

Os testes aprovados incluem schema, releitura offline fresca dos 256 eventos, roundtrip byte a byte dos 256 PartyEvent e 177 EventStatus, preservação de textos e parâmetros, todas as variantes de efeitos, GUID duplicado, referências, índices e lotes. Há controles negativos reais: remover evento, fabricar quantidade final e remover origem fazem a validação falhar.

## Reprodução limpa, também exercitada

Comando executado:

    python reproduzir_offline.py --out <workspace>/repro-limpa --deps <workspace>/dependencias

Exit 0. A rotina refez a decompilação e o inventário a partir dos arquivos instalados, sem os leitores diagnósticos que falharam. Produziu os dumps em uma pasta NOVA, executou novamente **22 testes em 40.292s — OK**, e comparou os documentos:

`repro-limpa/repro-conferencia.json`: `eventos_identicos_ao_original=true`, `eventos=256`.

`repro-limpa/scan_headers_offline.py.log`: nove arquivos serializados/cenas varridos; 256 PartyEvent; 502 registros de semente íntegros.

## Exceções explícitas do inventário bruto

O inventário limpo encontra 108 MonoBehaviour com **m_Script.m_PathID=0**, todos falhando pelo mesmo motivo `PPtr can't deref with m_PathID == 0!`. Não podem ser classificados por script. Seus path_ids e razões estão em `repro-limpa/evidencias/assets/inventario-limpo.json`. Nenhum está no ListHolderEvents de 256 referências nem no conjunto dos 256 cabeçalhos PartyEvent identificados. A cobertura declarada é das definições PartyEvent identificáveis/declaradas, não uma interpretação inventada desses componentes sem script.

Três ActionInfoTest secundários não foram decodificados: seus bytes `.bin`, SHA-256, nomes e razões estão no manifesto `docs/cobertura/EV-R1/auxiliares-nao-decodificados/manifesto.json`.

Não exercitado: jogo/runtime, resultados aleatórios, quantidade final dependente de party/nível/modo, disponibilidade efetiva e traduções selecionadas. Pools universais foram preservados por regras/tabelas; não alegamos censo integral de ItemInfo nem decodificação universal de bytes Odin dos objetos auxiliares.

## Entrada recomendada

`docs/cobertura/EV-R1/indice-v2.md`; dados canônicos em `eventos.json`; schema formal em `eventos.schema.json`; guia em `schema.md`. Toda documentação e scripts estão no workspace desta tarefa; nenhum arquivo do repo ou da instalação foi modificado. O pacote final será preservado como artefato da tarefa no Kanban, para não depender da vida útil do workspace scratch.
