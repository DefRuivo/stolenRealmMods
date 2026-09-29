# RV-8b — lote **Shadow** (41 skills) · revisado em 29/09

> Primeiro lote da revisão de conteúdo das skills. Método: ler a descrição **exata** do
> asset (do `skills.csv`), comparar com as tags/tier/dano do próprio asset e corrigir
> só o que é objetivamente defeito de texto. **Nenhuma afirmação de mecânica foi
> alterada** — mecânica exige verificação no código + triangulação externa.

## 1. Corrigido (4) — `status = corrigido` no `skills.csv`

Gramática e espaçamento. Nenhum muda o sentido, então não precisaram de triangulação.

| Skill | Antes | Depois |
|---|---|---|
| `Poison Cloud` | "creates **an** poison gas cloud **applies**" | "creates **a** poison gas cloud **that applies**" |
| `Raise Undead Wizard` | "Raise **a** Undead Wizard" | "Raise **an** Undead Wizard" |
| `Ghost Armor` | "attack.**··**Lasts until hit.**·**" (espaço duplo + espaço no fim) | "attack. Lasts until hit." |
| `Soul Crush` | "…Max Health.**·**" (espaço no fim) | "…Max Health." |

As chaves foram conferidas por `python tools/check_fix_keys.py`: **53 das 55** chaves das
tabelas do mod existem no censo; as 2 de fora são dicas de loading (uma delas já
confirmada disparando no log). As 4 novas estão entre as que casam.

## 2. Aguardando decisão de wording (não é bug, é escolha sua)

Estas mudam a **redação**, não a correção — e você ajusta wording pessoalmente, então
não mexi:

- **"Summon" vs "Raise"**: os 6 invocadores têm nomes que começam com *Raise*
  (`Raise Skeletal Archer`, `Raise Undead Ranger`…), mas 3 descrições dizem
  *"Summon a skeletal…"* e 3 dizem *"Raise an Undead…"*. Padronizar em **Raise**
  alinharia texto e nome.
- **"to fight for you" vs "to fight by your side"**: o `Raise Iron Golem` usa *"for you"*,
  todos os outros usam *"by your side"*. Só o Iron Golem destoa.
- **`Coin of Chaos`** — `"Flip the Coin of Chaos!"` é a descrição **inteira**: zero
  informação sobre o que a skill faz. Pode ser sabor proposital (é caos), mas vale
  decidir: mantém o mistério ou explica?

## 3. Inconsistência de DADOS encontrada (não dá pra corrigir num mod de texto)

`Raise Skeletal Archer` e `Raise Undead Ranger` **não têm a tag `Beneficial`**, enquanto
os outros quatro invocadores têm (`Beneficial,Ranged`). A tag vem do asset e afeta como
o tooltip é montado/colorido — um mod de texto não alcança isso. **Confirmar no jogo** se
a diferença aparece; se aparecer, é caso pra (a) reportar ao dev ou (b) um mod próprio.

## 4. O que falta para fechar o RV-8b

Duas coisas, nesta ordem:

1. **Enriquecer o dump de skills.** O censo de hoje traz nome, tipo, tier, dano, tags e
   descrição — mas **não** as `DescriptionExpressions`, `ActionsGranted` e
   `AttributeEffects`. Sem elas não dá pra conferir se os **números** do texto batem com
   o que o código calcula (que é o coração da revisão de conteúdo).
2. **Triangular os 37 restantes** com ≥2 fontes externas (wiki, patch notes mais recentes,
   guias Steam, Discord) e marcar `revisado` no `skills.csv`. Os 37 seguem `pendente`
   de propósito — foram lidos, mas ler não é revisar.
