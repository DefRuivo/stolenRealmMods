# CI

Automacao de GitHub Actions do repositorio. Hoje existe **um** workflow:

| arquivo | quando roda | o que faz |
|---|---|---|
| [`.github/workflows/validate.yml`](../.github/workflows/validate.yml) | `push` e `pull_request` na `main` | só **valida**: reprova o commit se um dos checks do projeto falhar |

## Escopo A: só validação (decidido)

O CI **não compila** e **não publica**. Isso é decisão, não pendência:

- **Não compila.** Os `.csproj` dependem das assemblies do *jogo*, que ficam em
  `lib/` (gitignored) e não existem num runner limpo. Colocar essa `lib` no CI
  significaria hospedar arquivo de terceiro num repositório **público** — fora de
  cogitação. Quem compila é a máquina de desenvolvimento, com o jogo instalado.
- **Não publica.** Nenhum segredo é lido, nenhum upload acontece. O job declara
  `permissions: contents: read`, então nem se quisesse daria para escrever no repo.
- **Não empacota.** O `tools/pack-thunderstore.py` exige a DLL buildada, então fica
  fora. A parte dele que só olha metadado virou
  [`.github/scripts/valida_pacotes.py`](../.github/scripts/valida_pacotes.py), que lê
  apenas arquivos versionados.

O efeito prático: o workflow é a mesma trava do `tools/release-check.sh`, mas **cedo**
— no push, e não na hora de publicar.

## Os passos, na ordem

O job para no primeiro erro (o GitHub corta o job no primeiro `run` que sai `!= 0`).
A ordem vai do mais barato/mais grave para o mais caro.

| # | comando | o que pega |
|---|---|---|
| 1 | `python tools/check_segredos.py` | token/credencial nos arquivos **versionados** — o que seria publicado |
| 2 | `python tools/check_fix_keys.py` | chave das tabelas do `LocalizePatch` que não existe no censo |
| 3 | `python tools/check_dupes.py` | chave **duplicada** → `ArgumentException` derruba o `LocalizePatch` inteiro (INC-1) |
| 4 | `python tools/check_notas_redundantes.py` | nota que repete o próprio texto (RV-15) |
| 5 | `python tools/check_chave_compartilhada.py` | texto usado por mais de um dono, com correção por texto (BUG-32). A flag `--estrito` **existe**, mas o CI **não** a usa de propósito — ver "Armadilhas conhecidas" (1 caso real ainda aberto) |
| 6 | `python .github/scripts/valida_pacotes.py` | manifest, ícone, README e CHANGELOG de cada pacote |
| 7 | `python tools/audita_docs.py` | auditoria das docs contra o disco: contagens, versões, ferramentas citadas, links e caminhos que saíram do repo (promovido de `scratch/` em 30/09/2026) |

Nenhum passo instala dependência: todos usam só a biblioteca padrão do Python
(`csv`, `json`, `re`, `struct`, `zlib`, `subprocess`).

## Rodar tudo na sua máquina

Da raiz do repo, na mesma ordem:

```bash
python tools/check_segredos.py
python tools/check_fix_keys.py
python tools/check_dupes.py
python tools/check_notas_redundantes.py
python tools/check_chave_compartilhada.py
python .github/scripts/valida_pacotes.py
python tools/audita_docs.py
```

O passo 5 tem a flag `--estrito` (o modo do `release-check.sh`); troque a linha por
`python tools/check_chave_compartilhada.py --estrito` para ver **hoje** o caso que mantém a flag
fora do CI — ele vai apontar a chave `Devour...`, e sai `1` (ver "Armadilhas conhecidas").

Com `bash`/git-bash dá para parar no primeiro erro como o CI faz:

```bash
for s in check_segredos check_fix_keys check_dupes check_notas_redundantes \
         check_chave_compartilhada; do python "tools/$s.py" || break; done
python .github/scripts/valida_pacotes.py
python tools/audita_docs.py
```

## Armadilhas conhecidas

- **O passo 4 reescreve um arquivo versionado.** O
  `check_notas_redundantes.py` regenera `docs/cobertura/revisao/RV-15-notas-redundantes.md`
  a cada execução. No CI isso não é commitado (é só trava), mas localmente ele deixa o
  arquivo modificado. Se o número do relatório divergir do commit, é porque o relatório
  ficou **velho** em relação ao `LocalizePatch.cs` — rodar o script de novo é o conserto.
- **O passo 5 é a única trava ainda DESLIGADA — de propósito, e o que falta é UM caso.**
  O `check_chave_compartilhada.py` **já tem** a flag `--estrito` (existe desde 30/09/2026 e é a
  mesma que o `tools/release-check.sh` usa como passo 5). Sem a flag ele é relatório: sai `0`
  sempre e **lista** as suspeitas. Com `--estrito` ele sai `1` quando a **mesma chave** está em
  `TextFixes` **e** em `TextAppends` — caso em que o lookup `if/else if` executa o de `TextFixes`
  e a entrada de `TextAppends` **nunca roda** (a nota não existe em jogo, sem erro no log). As 12
  *suspeitas* de texto compartilhado seguem aviso que não reprova **nos dois modos** — ali a
  decisão é humana (se a nota mente para o outro dono depende da mecânica que ela cita).
  - **HOJE (o CI roda sem a flag, de propósito):** rodando `--estrito` na árvore atual ele sai
    `1` por **1 caso real** — a chave `Devour the life force of all enemies within 2 hexes
    dealing *0 Shadow Damage and giving you 10% @Maximum Health@ for each enemy effected.` está
    nas duas tabelas (`TextAppends` l.431, nota de *stack* da skill `Consumption`, e `TextFixes`
    l.907, o fix de terminologia `maximum health`→`max health` que é quem executa). Enquanto esse
    caso existir, ligar a flag no CI deixaria a `main` vermelha para todo mundo **sem ganho
    imediato** — e nada fica encoberto: o mesmo caso já reprova o `release-check.sh` na hora de
    publicar (o CI é uma trava cedo, não a única).
  - **DEPOIS (quando o caso for corrigido no `LocalizePatch.cs` — 1 entrada por texto, fundindo
    o valor da `TextAppends` no da `TextFixes`):** trocar a linha do passo 5 no YAML por
    `python tools/check_chave_compartilhada.py --estrito` e conferir antes, na sua máquina, com
    `python tools/check_chave_compartilhada.py --estrito; echo $?` → **`0`**. Só então a flag
    entra no CI e as chaves repetidas nas duas tabelas passam a reprovar no push, que é o
    objetivo. (No `release-check.sh` esse já é o modo do **passo 5/6** dele hoje: é só o CI que
    ainda não ligou a flag.)
- **O passo 2 tem 4 avisos que não são erro.** Chaves de UI/loading que o censo do RV-7
  ainda não cobre (a frase das lojas, `Resist Divine`/`Resistance Divine`, a dica da
  poção). Isso é esperado e está documentado em
  [`cobertura/README.md`](cobertura/README.md), na seção "O que este censo AINDA não cobre".
- **Pasta de mod sem `manifest.json` não é erro.** O passo 6 a **avisa** e segue: um mod
  em implementação (hoje o `RoguelikeSkillTreeVisualizer`) ainda não é pacote, então não
  há o que validar. Assim que o `manifest.json` aparecer, ele passa a ser validado sozinho.

## Adicionar um check novo

1. Escreva a ferramenta em `tools/` (ou em `.github/scripts/` se for específica de CI).
   Ela deve sair com código `!= 0` quando reprovar e dizer **arquivo e linha** do problema.
2. Rode-a contra o repo **hoje** e confirme o código de saída real, antes de ligar no CI —
   ligar um check que já nasce vermelho trava a branch de todo mundo.
3. Adicione o passo em `validate.yml`, na posição certa da ordem, com um comentário do
   tipo de defeito que ele pega.
