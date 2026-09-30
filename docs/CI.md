# CI

Automacao de GitHub Actions do repositorio. Existem **dois** workflows, em escopos
diferentes:

| arquivo | quando roda | o que faz |
|---|---|---|
| [`.github/workflows/validate.yml`](../.github/workflows/validate.yml) | `push` e `pull_request` na `main` | escopo **A** — só **valida**: reprova o commit se um dos checks do projeto falhar |
| [`.github/workflows/publish.yml`](../.github/workflows/publish.yml) | **manual** (`workflow_dispatch`) + aprovacao num Environment | escopo **B** — **publica**: manda um `.zip` já empacotado para a Thunderstore, só dos mods liberados em [`release/mods.json`](../release/mods.json) |

Nenhum dos dois compila e nenhum toca na `lib/` do jogo. O escopo B tem documento próprio:
[PUBLICACAO.md](PUBLICACAO.md) — regras da Thunderstore, o gate, o setup do environment, o
passo a passo e as armadilhas.

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

## Escopo B: publicação (decidido em 30/09/2026)

O "não publica" do escopo A continua valendo **para o `validate.yml`**. A publicação é um
segundo workflow, **separado e manual**, porque não dá para automatizá-la sem quebrar duas
regras do projeto: não hospedar DLL do jogo num repositório público, e não publicar sem
revisão humana.

| | escopo A (`validate.yml`) | escopo B (`publish.yml`) |
|---|---|---|
| disparo | `push`/`pull_request` na `main` | **manual** (`workflow_dispatch`), com input de mod |
| segredo | nenhum | `THUNDERSTORE_TOKEN`, **secret do environment** `thunderstore` |
| permissão | `contents: read` | `contents: read`; o job `registra` usa `contents: write` só em `release/mods.json` |
| compila | não | **não** — envia o `.zip` do `dist/` pelo input `file:` da Action |
| aprovação | — | **Environment com revisores obrigatórios** (a aprovação é o clique) |
| efeito | trava o commit | publica uma versão **nova** na comunidade |

O que o escopo B não negocia:

- **Sem `lib/` não há build no CI.** O `publish.yml` não compila: o zip chega pronto de fora
  (GitHub Release + input `release_tag`, ou runner self-hosted com o jogo instalado). Se o
  pacote não estiver lá, o job **falha** dizendo o comando exato a rodar na máquina local —
  pacote incompleto é pior que pacote nenhum.
- **Mod travado não sai.** Quem decide é o `release/mods.json`, e a lista de mods dele é
  conferida a cada run contra o `tools/pack-thunderstore.py --listar-nomes` (uma fonte só
  para "o que é um mod"). Escolher à mão um mod com `publicar: false` **reprova** o run.
- **Versão repetida nunca.** Versão na Thunderstore é **imutável**: o pre-flight lê a lista
  pública da comunidade e recusa versão que já existe — ou que não seja maior que a que está
  no ar (a plataforma exibe sempre a maior).
- **O token nunca entra em log.** `tools/check_segredos.py` roda como passo do job (a mesma
  trava que o `publish-thunderstore.sh` faz localmente) e o valor só existe dentro do job que
  declara o environment.
- **O registro é conferido, não presumido.** O job `registra` só escreve `versao_publicada` /
  `publicado_em` no `release/mods.json` **depois** de a API pública confirmar a versão, e
  commita com `[skip ci]`.

O passo a passo, o setup do environment `thunderstore` e o troubleshooting estão em
[PUBLICACAO.md](PUBLICACAO.md). Enquanto `.github/workflows/` não subir (falta o escopo
`workflow` no PAT — ver a seção de armadilhas abaixo), o escopo B existe **no disco** e o
envio continua saindo pelo `tools/publish-thunderstore.sh` local (dry-run por padrão).

## Os passos, na ordem

O job para no primeiro erro (o GitHub corta o job no primeiro `run` que sai `!= 0`).
A ordem vai do mais barato/mais grave para o mais caro.

| # | comando | o que pega |
|---|---|---|
| 1 | `python tools/check_segredos.py` | token/credencial nos arquivos **versionados** — o que seria publicado |
| 2 | `python tools/check_fix_keys.py` | chave das tabelas do `LocalizePatch` que não existe no censo |
| 3 | `python tools/check_dupes.py` | chave **duplicada** → `ArgumentException` derruba o `LocalizePatch` inteiro (INC-1) |
| 4 | `python tools/check_notas_redundantes.py` | nota que repete o próprio texto (RV-15) |
| 5 | `python tools/check_chave_compartilhada.py --estrito` | **a mesma chave** em `TextFixes` **e** em `TextAppends`: o lookup é `if/else if` na mesma chave, então a entrada de `TextAppends` **nunca roda** e a nota não existe em jogo, sem erro no log (BUG-32). As *suspeitas* (texto usado por 2+ donos) seguem **aviso que não reprova**, nos dois modos |
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
python tools/check_chave_compartilhada.py --estrito
python .github/scripts/valida_pacotes.py
python tools/audita_docs.py
```

O passo 5 roda **com** `--estrito` aqui e no CI (o modo do `release-check.sh`): sem a flag o
script é relatório puro e sai `0` sempre, listando as suspeitas — foi assim enquanto o único
caso real (a nota de *stack* da `Consumption`, chave nas duas tabelas) existia. Ele foi
corrigido, então a flag entrou.

Com `bash`/git-bash dá para parar no primeiro erro como o CI faz:

```bash
for s in check_segredos check_fix_keys check_dupes check_notas_redundantes \
         check_chave_compartilhada; do python "tools/$s.py" || break; done
python tools/check_chave_compartilhada.py --estrito   # a flag que o loop nao passa
python .github/scripts/valida_pacotes.py
python tools/audita_docs.py
```

## Armadilhas conhecidas

- **O passo 4 reescreve um arquivo versionado.** O
  `check_notas_redundantes.py` regenera `docs/cobertura/revisao/RV-15-notas-redundantes.md`
  a cada execução. No CI isso não é commitado (é só trava), mas localmente ele deixa o
  arquivo modificado. Se o número do relatório divergir do commit, é porque o relatório
  ficou **velho** em relação ao `LocalizePatch.cs` — rodar o script de novo é o conserto.
- **O passo 5 roda com `--estrito` (ligado em 30/09/2026).** É a mesma ferramenta do **passo 5
  do `tools/release-check.sh`**, agora no mesmo modo. Sem a flag ela é relatório puro: sai `0`
  sempre e **lista** as suspeitas. Com `--estrito` ela sai `1` quando a **mesma chave** está em
  `TextFixes` **e** em `TextAppends` — o lookup é `if/else if` na mesma chave, então a entrada de
  `TextAppends` **nunca roda** e a nota não existe em jogo, sem erro no log (BUG-32). As
  *suspeitas* (texto com nota usado por 2+ donos — 12 em 30/09) seguem **aviso que não reprova nos
  dois modos**: ali a decisão é humana (se a nota mente para o outro dono depende da mecânica que
  ela cita).
  - **O caso que segurava a flag fora do CI foi corrigido:** a chave `Devour the life force of
    all enemies within 2 hexes dealing *0 Shadow Damage...` estava nas duas tabelas
    (`TextAppends` l.431, nota de *stack* da `Consumption`; `TextFixes` l.907, o fix de
    terminologia `maximum health`→`max health`, que é quem executava) e virou **uma entrada por
    texto**, com o valor da `TextAppends` fundido no da `TextFixes`. Conferido antes de ligar:
    `python tools/check_chave_compartilhada.py --estrito; echo $?` → **`0`**.
  - **Se voltar a sair `1`,** o conserto é no `LocalizePatch.cs` (**uma entrada por texto**) —
    nunca afrouxar a flag: a falha é silenciosa em jogo e não aparece em log nenhum.
  - **A mudança vale a partir do commit em que o `validate.yml` subir.** O arquivo está em
    `.github/workflows/`, e o push automático do harness **não** tem o escopo `workflow` do PAT:
    editar o YAML no disco funciona, subir não. Enquanto ele não for commitado, o CI continua
    rodando o passo 5 **sem** a flag (relatório); o `release-check.sh` local, esse já trava.
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
