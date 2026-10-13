# EV-R2-FORAPOOL-b02 — inventário e limites da proposta

Cartão: t_cf917982. Escopo: seções 22–42, inclusive, das 84 seções `## ` de `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`. Identidades cruzadas com `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json`; contrato em `eventos.schema.json` e `schema.md`; referências em `catalogo-referencias.json`, no mesmo diretório.

Contagem verificada por `inspecionar.py`: 21 eventos e 21 chaves físicas distintas. Este inventário não é aprovação: todas as decisões do dono estão PENDENTES. As propostas detalhadas e o fechamento ficam nas partes seguintes, novas e numeradas; este arquivo não será sobrescrito.

## Inventário do escopo

| Nº da seção | Chave física | Título | Categoria | Raridade (valor) | Peso relativo | disabled | Opções |
|---:|---|---|---|---|---:|---:|---:|
| 22 | resources.assets:2545613 | Jack in the Box | NotInEventPool | Common (0) | 1.0 | 0 | 2 |
| 23 | resources.assets:2545615 | Jack in the Box | NotInEventPool | Common (0) | 1.0 | 0 | 2 |
| 24 | resources.assets:2545614 | Jack in the Box - Victory | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 25 | resources.assets:2545633 | King Under the Mountain | NotInEventPool | Common (0) | 1.0 | 0 | 0 |
| 26 | resources.assets:2545620 | Lady of the Well | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 27 | resources.assets:2545617 | Lesser Mimic | NotInEventPool | Common (0) | 1.0 | 0 | 3 |
| 28 | resources.assets:2545625 | Magic Mirror | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 29 | resources.assets:2545650 | Master of Rage | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 30 | resources.assets:2545754 | Mimic | NotInEventPool | Common (0) | 1.0 | 0 | 3 |
| 31 | resources.assets:2545657 | Ogre Debt Collector | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 32 | resources.assets:2545658 | Ogre Debt Collector | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 33 | resources.assets:2545661 | Party like a Pirate | NotInEventPool | Common (0) | 1.0 | 0 | 2 |
| 34 | resources.assets:2545662 | Party like a Pirate | NotInEventPool | Common (0) | 1.0 | 0 | 2 |
| 35 | resources.assets:2545663 | Party like a Pirate | NotInEventPool | Common (0) | 1.0 | 0 | 2 |
| 36 | resources.assets:2545667 | Pirate's Treasure | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 37 | resources.assets:2545669 | Poacher's Demise | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 38 | resources.assets:2545629 | Red Dragon | NotInEventPool | Common (0) | 1.0 | 0 | 0 |
| 39 | resources.assets:2545679 | Scent of Blood | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 40 | resources.assets:2545695 | Strange Crystal | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 41 | resources.assets:2545698 | Strange Crystal | NotInEventPool | Common (0) | 1.0 | 0 | 1 |
| 42 | resources.assets:2545701 | Strange Crystal | NotInEventPool | Common (0) | 1.0 | 0 | 1 |

## Regras da análise

- Texto atual é preservado literalmente em strings JSON: `\n` e `\r` representam os controles reais; `""` é texto vazio, não NULL. Redações propostas permanecem em inglês, com tags e placeholders preservados.
- Naturezas separadas: wording, recompensa e condição. Nenhum veredito proposto autoriza implementação. Não adicionar recompensas nem modificar pesos, flags, encadeamentos ou variantes FullReleaseMode.
- NULL de resultado final significa NAO_EXERCITADO, com o motivo do canônico. Não calcular ouro/XP/loot, não preencher tokens e não escolher um status ou variante arbitrariamente.
- Uma referência nula de PPtr é ausência estrutural explicitada, não resultado runtime. Combate com referência nula não prova combate quebrado: consultar `batalha.override`, `manual` e inimigos forçados.
- `disabled=0` nestes 21 eventos é somente o valor autoral. Não prova disponibilidade. `NotInEventPool` não significa inútil: encadeamentos e eventos pós-combate devem permanecer.
- Não unir títulos iguais: as variantes dos eventos 22/23, 31/32, 33/34/35 e 40/41/42 são chaves distintas.
- NAO_EXERCITADO: jogo/runtime, UI, disponibilidade efetiva, seleção de personagem, RNG, combate e aplicação final de recompensas/status. Motivo: tarefa estritamente documental/offline, sem abrir o jogo.

## Roteamento da revisão

O filho pré-criado `t_8e74c724` é a revisão HUMANA dos 84 eventos e depende deste lote. Ao terminar a fase documental, o lote será concluído para liberar essa dependência, sem revisar no lugar do dono e sem abrir uma segunda revisão no mesmo cartão. A aprovação de cada chave permanece PENDENTE.
