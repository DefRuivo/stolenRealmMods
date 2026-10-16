# EV-R2-FORAPOOL-b04 — parte 01: inventário e escopo

Cartão t_60b05dec. Propostas documentais para aprovação do dono; nenhum veredito constitui aprovação. Não implementar, não abrir o jogo, não alterar recompensas/condições.

Fonte de ordem: C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md, 84 seções `## `; este lote cobre exclusivamente as 21 seções 64–84. Metadados abaixo conferidos em C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json por chave física, sem agrupar títulos repetidos.

| Nº | Chave física | Título | Categoria | Raridade (valor) | Peso relativo | disabled | Opções |
|---:|---|---|---|---|---:|---:|---:|
|64|resources.assets:2545781|The runes of the Ymir|NotInEventPool|Common (0)|1.0|0|2|
|65|resources.assets:2545783|The runes of the Ymir|NotInEventPool|Common (0)|1.0|0|2|
|66|resources.assets:2545747|The Spell Council|NotInEventPool|Common (0)|1.0|0|1|
|67|resources.assets:2545749|The Spell Council|NotInEventPool|Common (0)|1.0|0|2|
|68|resources.assets:2545635|The Sultan|NotInEventPool|Common (0)|1.0|0|0|
|69|resources.assets:2545643|The Witch|NotInEventPool|Common (0)|1.0|0|0|
|70|resources.assets:2545647|Too Late|NotInEventPool|Common (0)|1.0|0|0|
|71|resources.assets:2545760|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|0|2|
|72|resources.assets:2545761|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|0|2|
|73|resources.assets:2545762|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|0|2|
|74|resources.assets:2545763|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|0|2|
|75|resources.assets:2545764|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|0|3|
|76|resources.assets:2545765|Trial of the Ymir|NotInEventPool|Common (0)|1.0|0|1|
|77|resources.assets:2545766|Trial of the Ymir|NotInEventPool|Common (0)|1.0|0|2|
|78|resources.assets:2545570|Unholy Experiments|NotInEventPool|Common (0)|1.0|0|2|
|79|resources.assets:2545768|Unleashed|NotInEventPool|Common (0)|1.0|0|1|
|80|resources.assets:2545769|Unleashed|NotInEventPool|Common (0)|1.0|0|1|
|81|resources.assets:2545772|What Lurks|NotInEventPool|Common (0)|1.0|0|1|
|82|resources.assets:2545775|Witch's Pyre|NotInEventPool|Rare (2)|1.0|0|1|
|83|resources.assets:2545782|Ymir Rune, Honor|NotInEventPool|Common (0)|1.0|1|1|
|84|resources.assets:2545784|Ymir Rune, Strength|NotInEventPool|Common (0)|1.0|1|1|

Inventário inicial: 21/21 eventos identificados. Contagens agregadas de opções/ações/anomalias e propostas finais serão calculadas no fechamento, sem transformar NULL em zero.

Regra de interpretação: NULL de resultado de partida = NAO_EXERCITADO, com motivo do canônico; PPtr serializado com m_PathID=0 = referência nula no asset, não recompensa zero. Peso 1.0 não significa probabilidade 100%. NotInEventPool não significa evento inútil. disabled isolado não comprova disponibilidade efetiva.

Lacuna inicial de fonte: catalogo-referencias.json não está solto na pasta durável EV-R1 consultada; recuperar a fonte preservada antes do fechamento. Não preencher descrições ausentes por inferência. Os arquivos evt_* do workspace são extratos de tentativa anterior, não fonte canônica de propostas.

NAO_EXERCITADO: runtime/UI, disponibilidade numa partida, RNG, ouro/XP/loot finais, aplicação de status e combate — tarefa limitada à análise documental offline. Aprovação humana: PENDENTE em todas as 21 chaves.
