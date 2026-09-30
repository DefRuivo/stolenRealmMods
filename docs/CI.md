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
| 5 | `python tools/check_chave_compartilhada.py` | texto usado por mais de um dono, com correção por texto (BUG-32) |
| 6 | `python .github/scripts/valida_pacotes.py` | manifest, ícone, README e CHANGELOG de cada pacote |
| 7 | `python tools/audita_docs.py` **se existir** | auditoria dos docs (hoje mora em `scratch/`, fora do git) |

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
```

Com `bash`/git-bash dá para parar no primeiro erro como o CI faz:

```bash
for s in check_segredos check_fix_keys check_dupes check_notas_redundantes \
         check_chave_compartilhada; do python "tools/$s.py" || break; done
python .github/scripts/valida_pacotes.py
```

## Armadilhas conhecidas

- **O passo 4 reescreve um arquivo versionado.** O
  `check_notas_redundantes.py` regenera `docs/cobertura/revisao/RV-15-notas-redundantes.md`
  a cada execução. No CI isso não é commitado (é só trava), mas localmente ele deixa o
  arquivo modificado. Se o número do relatório divergir do commit, é porque o relatório
  ficou **velho** em relação ao `LocalizePatch.cs` — rodar o script de novo é o conserto.
- **O passo 5 hoje não reprova nada.** O `check_chave_compartilhada.py` aceita só `-v`;
  ele sempre sai `0` e **lista** as suspeitas. Quando existir `--estrito`, trocar a linha
  no YAML por `python tools/check_chave_compartilhada.py --estrito` e aí sim as suspeitas
  viram reprovação.
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
