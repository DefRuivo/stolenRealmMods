# EV-R1 — parte 02: inventário offline e falhas de leitura detectadas

## Corpus medido

`python scan_assets_v2.py` varreu os sete arquivos `.assets` instalados e as três cenas `level0`, `level1`, `level2` (o log contém oito entradas: globalgamemanagers.assets, resources.assets, sharedassets0/1/2.assets e level0/1/2). O assembly instalado e a cópia `C:/dev/stolen-realm/lib/Assembly-CSharp.dll` têm SHA-256 idêntico ao registrado na parte 01.

Evidência: `evidencias/assets/inventario-v2.json` e `scan-assets-v2.txt`.

- `resources.assets`: 2.857.501 objetos; 256 cabeçalhos de script `PartyEvent`.
- Outros arquivos varridos: zero cabeçalhos `PartyEvent`.
- `ListHolderEvents`: um objeto, path_id `2547145` em resources.assets.
- Tipos correlatos no arquivo: 177 EventStatus e 54 QuestInfo.
- O script `scratch/rv28/dump_fortunes.py` do repo navega a UI de Fortunes; não é um extrator de eventos/recompensas reutilizável diretamente.

## Falha registrada, não mascarada

A primeira tentativa sem geração de typetree produziu 312.437 erros de leitura por faltar campos customizados. Seu resultado NÃO serve como dump de eventos.

A segunda tentativa usa UnityPy 1.25.4 + TypeTreeGeneratorAPI local, com os DLLs instalados. Reconheceu 256 eventos, porém só leu 249 integralmente; detectou também divergência no PPtr `m_Script` do cabeçalho (gerado `m_FileID=16777216`, enquanto o cabeçalho nativo do evento 2545531 tem `m_FileID=1`, `m_PathID=1910`). Portanto o resultado v2 é diagnóstico, NÃO a entrega final.

Reprodução: `python scan_assets_v2.py` numa pasta limpa; `ObjectReader.parse_monobehaviour_head()` para comparar cabeçalho nativo com o nó gerado. Novas tentativas usarão novos arquivos numerados, preservando a evidência anterior.

## Fontes no código

Arquivo: `evidencias/codigo/Assembly-CSharp.decompiled.cs`, 371.804 linhas, ilspycmd 8.2.0.7535.

- `PartyEvent` (l.149972): textos, opções, filtros, ChanceRatio e EventSpawnTypes são campos serializados, não uma tabela literal de eventos no DLL.
- `PartyEvent.EventName` (l.150223): usa EventNameOverride não vazio, senão nome do asset.
- `ListHolderEvents.Populate` (l.131811): enumera Resources de Events e Quests.
- `EventAction.GetEventActionEffects` (l.151198): permite override por FullReleaseMode; nenhum override pode ser descartado por inferência offline.
- `EventActionEffects` (l.151214): ouro/XP são flags e razões, itens/fortunes/status são referências; valores finais dependentes de runtime não serão fabricados.

Cobertura integral e textos resolvidos: NÃO_EXERCITADO nesta parte; faltam corrigir o leitor, validar as referências e reconciliar o ListHolderEvents com os 256 cabeçalhos.
