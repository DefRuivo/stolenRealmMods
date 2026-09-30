# RV-15 - Notas redundantes / duplicadas nos tooltips

Gerado por `tools/check_notas_redundantes.py` a partir de `BetterTooltips/Patches/LocalizePatch.cs`.

Uma nota existe para dizer o que o texto **nao** diz. Quando ela repete o proprio texto,
o jogador le a mesma frase duas vezes e a explicacao perde credito - foi o que o usuario
reportou em 30/09 (`Blinding Lights` duplicado, `Blind`/`Sleep` redundantes,
`Praying Shot`/`Chok` na mesma familia).

## Resumo

| caso | quantas | o que significa |
|---|---|---|
| nota == chave | **0** | texto e nota sao a MESMA frase: aparece duplicado na tela |
| nota contida na chave | **0** | a nota inteira ja esta no texto: nao acrescenta nada |
| nota ecoa >= 6 palavras da chave | **0** | repete o inicio do texto em sequencia |
| notas unicas (OK) | 205 | dizem algo que o texto nao diz |

Total de notas analisadas: **205**.

## 1. Nota identica a chave (DUPLICADO na tela)

Nenhum caso. 

## 2. Nota inteiramente contida na chave (redundante)

Nenhum caso. 

## 3. Nota que ecoa o texto

Nenhum caso. 
