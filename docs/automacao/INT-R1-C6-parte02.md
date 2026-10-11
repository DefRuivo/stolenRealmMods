# INT-R1-C6 — parte 02: como a chave é casada (método e o que foi medido)

O casamento é **por texto**: o dump de origem traz a descrição do jogo em inglês e a tabela do
LANG-R1 traz, na coluna `chave`, exatamente esse texto em inglês (o inglês **é** a chave do
dicionário — fato já registrado na revisão do LANG-R1). Então o join é
`desc do dump` → `chave da tabela` → `pt-BR`, `alertas`, `contextos`.

O dumper de boot do `RoguelikeDebugger` (`tools/census.py` lê o `LogOutput.log`) imprime o texto
com **três diferenças conhecidas** em relação ao que está na tabela. Elas não são erro de um lado
nem do outro; são a forma como cada instrumento serializa o mesmo campo:

| Eixo | No dump de boot | Na tabela do LANG-R1 |
|---|---|---|
| realce inline | `@Armor@` | `<b>Armor</b>` |
| quebra de linha interna | espaço (`\n\n` virou espaço) | `\n\n` literal |
| caixa do nome do atributo | `@magic armor@` (forma de exibição) | `<b>Magic Armor</b>` |

Por isso o casamento tem **três tiers**, e o tier fica **declarado em cada item** do dump novo:

1. `exato` — o texto é byte a byte igual à chave (nenhuma transformação aplicada);
2. `normalizado` — igual depois de `<b>X</b>`→`@X@`, remover `<i>`/`<color>`, colapsar
   espaço/quebra de linha e tirar espaços das pontas (caixa preservada);
3. `casefold` — igual ao anterior **e** igual ignorando maiúscula/minúscula.

Eixo a eixo, nos 650 itens chaveados (medido nesta rodada, contando a diferença de cada eixo de
forma independente):

| Diferença em relação à chave | Itens |
|---|---:|
| nenhuma (`exato`) | **551** |
| só espaço/quebra de linha | 40 |
| só realce (`<b>`/`<i>`/`<color>`) | 7 |
| realce + espaço/quebra | 10 |
| realce + espaço/quebra + caixa do atributo | **42** |
| **total chaveado** | **650** |

Exemplos reais, tirados do dump novo:

- `casefold` — Challenger (T1, passiva): o dump traz
  `For every enemy within 1 hex of your character gain 5% to @Armor@ and @magic armor@.`
  e a chave é `... gain 5% to <b>Armor</b> and <b>Magic Armor</b>.` (`LANG-03424`);
- `normalizado` — ataque básico: o dump traz
  `Deals *0 weapon damage to target.   When targeting an ally, heals for *0.` e a chave casada é
  `Deals *0 weapon damage to target. \n\nWhen targeting an ally, heals for *0.` (`LANG-02568`;
  no dump novo a quebra de linha aparece escapada como `\n`). A variante irmã sem o `\n\n` também
  existe na tabela: `LANG-02567` = `Deals *0 weapon damage to target. `.

## Por que o casamento aceitar 3 tiers e ainda ser seguro

A tabela tem 9.095 chaves. Depois da normalização **sem** casefold há **122** chaves que
colidem com outra chave (mesmo texto normalizado, chaves distintas); depois do casefold há
**231**. O script **não escolhe** quando há colisão: se o tier encontra mais de uma chave
distinta, o item vira `ambiguo` e vai para a lista de conferência manual, em vez de o script
adivinhar. Neste corpus houve **0** casamento ambíguo — ou seja, para cada item deste dump havia
exatamente **uma** chave candidata em cada tier. O `casefold`, portanto, não aproximou textos
diferentes: só absorveu a troca de caixa do nome do atributo.

Prova por comando (a contagem de colisões da tabela está no JSON gerado):

```bash
python -c "import json;d=json.load(open('docs/cobertura/DUMP-CHAVEADO-LANG-R1-contagens.json',encoding='utf-8'));print(d['tabela'], d['total']['ambiguo'])"
```

## O que este método **não** prova (dito antes de alguém concluir demais)

- Casar texto **não** prova que a tela que usa aquela chave é a tela do item. A tabela tem
  variantes irmãs do mesmo texto (o caso `Deals *0 weapon damage to target. ` acima: existem as
  versões com e sem o `\n\n`), e o dumper de boot perde a informação de qual asset apontava
  para qual variante. Esse é o risco residual registrado na parte 04.
- O tier `casefold` casa a **variante de exibição** do texto. O pt-BR mostrado no dump vem da
  chave daquela variante (ex.: o pt-BR de `Challenger` sai da chave com `<b>Armor</b>`), não de
  uma chave com `@Armor@`, que pode nem existir.
- Nada foi corrigido, reescrito ou normalizado **na saída**: a normalização vive só dentro do
  `casa()` e não toca uma letra do que vai para o arquivo.
