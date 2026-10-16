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
- **Não empacota num runner limpo.** O passo 9 chama `tools/pack-thunderstore.py`
  se encontrar DLL Release; sem DLL chama apenas `--listar-nomes`. Assim, com DLL local
  o workflow pode gerar ZIPs em `dist/`, mas não os constrói. Metadados são conferidos pelo
  [validador](../.github/scripts/valida_pacotes.py) antes desse passo.

O efeito prático: o workflow antecipa no push os checks de repositório compartilhados com
`tools/release-check.sh`. Não executa o mesmo conjunto: o release-check também compila;
ciclo e validação humana continuam separados.

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
[PUBLICACAO.md](PUBLICACAO.md). Os dois YAML **estão no remoto**. Para reconferir isso, compare
**commit com commit, nunca MD5 de disco com MD5 do publicado**: o disco pode estar sujo (edição
não commitada) ou em CRLF — os dois mudam o MD5 sem nada ter mudado no que o GitHub roda — e uma
reescrita de histórico muda os SHAs dos commits. O jeito que não apodrece:

```bash
git ls-remote origin main      # o SHA do main no GitHub
git rev-parse HEAD             # o SHA do commit local: iguais = o remoto tem este commit
git status --short -- .github/workflows/   # vazio = o disco tem o mesmo conteudo do commit
curl https://raw.githubusercontent.com/DefRuivo/stolenRealmMods/main/.github/workflows/validate.yml
```

A última linha traz o arquivo como ele está no GitHub (o que roda de verdade). Na conferência de
30/09/2026 o `main` era o mesmo commit do HEAD local. O envio local pelo
`tools/publish-thunderstore.sh` (dry-run por padrão) continua valendo como caminho alternativo.

## Os passos, na ordem

Ordem efetiva do YAML local em 16/10/2026 (não é prova de execução remota).
O job para no primeiro erro. O passo 0 imprime ambiente; depois:

| # no YAML | comando | o que pega |
|---|---|---|
| 1 | `python tools/check_segredos.py` | credencial versionada |
| 2 | `python tools/check_versoes.py` | espelhos de versão divergentes |
| 3 | `python tools/check_patches.py` | robustez Harmony |
| 4 | `python tools/check_fix_keys.py` | chaves contra o censo |
| 5 | `python tools/check_dupes.py` | chaves duplicadas |
| 6 | `python tools/check_notas_redundantes.py` | redundância/cor; regenera relatório |
| 7 | `python tools/check_chave_compartilhada.py --estrito` | mesma chave nas duas tabelas |
| 7b | `python tools/cobertura_ui_localized.py --prova` | prova offline do instrumento, não cobertura runtime |
| 8 | `python .github/scripts/valida_pacotes.py` | metadados e dependências |
| 9 | `python tools/pack-thunderstore.py` **somente se houver DLL Release**; senão `--listar-nomes` | empacotador guardado; com DLL pode escrever em `dist/` |
| 10 | `python tools/audita_docs.py` | auditoria da documentação |

`python tools/checa_citacoes.py` é uma checagem local complementar: **não está no YAML atual**.
Nenhum desses scripts exige dependência Python externa; isso não torna o empacotamento um build.

## Rodar tudo na sua máquina

Rodar todos os checks do YAML inclui um ramo com escrita de ZIPs. No checkout do dono, use
`--so-conferir` em vez de empacotar sobre entregáveis antigos; reproduza o ramo com escrita em
uma cópia NOVA. Os checks de notas também regeneram relatório: execute em cópia para preservar
`docs/cobertura/` e sua curadoria.

```bash
python tools/check_segredos.py &&
python tools/check_versoes.py &&
python tools/check_patches.py &&
python tools/check_fix_keys.py &&
python tools/check_dupes.py &&
python tools/check_notas_redundantes.py &&
python tools/check_chave_compartilhada.py --estrito &&
python tools/cobertura_ui_localized.py --prova &&
python .github/scripts/valida_pacotes.py &&
python tools/pack-thunderstore.py --so-conferir &&
python tools/audita_docs.py &&
python tools/checa_citacoes.py  # complementar; não está no workflow
```

O encadeamento `&&` para de verdade no primeiro erro. Num clone limpo sem DLL, troque o
pre-flight por `python tools/pack-thunderstore.py --listar-nomes`, como o guard do YAML.
`release-check.sh` também compila e deixa ciclo/runtime pendentes no modo normal; não é
idêntico ao CI. A referência de numeração é a tabela atual acima, não os relatos históricos abaixo.

## A chamada pronta para o `validate.yml` (CI-4)

O `tools/checa_citacoes.py` foi proposto como passo posterior à auditoria, mas **não aparece
no YAML local de 16/10/2026**; a auditoria efetiva é o passo 10. O bloco abaixo fica preservado
como **proposta histórica**, não como instrução de colagem nem diagnóstico de credencial atual.
Não foi verificado o escopo do PAT nem um run remoto nesta revisão. A decisão de incorporar o
check ao workflow exige tarefa própria e execução prévia verde; o número do passo deve acompanhar
o YAML, não a numeração antiga do exemplo.

```yaml
      # 10. Checagem de CITACOES (tools/checa_citacoes.py): toda citacao `arquivo:linha` da doc
      #     aponta para um arquivo que existe e para uma linha DENTRO dele? O dia teve tres provas
      #     versionadas citando linha que nao existe (a varredura em jogo, a fixture de cores e o
      #     documento da varredura do fake null, este ultimo citando 348/361/386 num arquivo de 252).
      #     A ferramenta e o irmao estreito do `audita_docs.py` (passo 9): duas perguntas so, as duas
      #     checaveis a maquina - arquivo existe? linha esta dentro? NAO julga se a linha certa foi
      #     citada (isso e leitura humana). Sai 1 apontando `documento:linha`, e o texto da doc que
      #     quebrou - nao a ferramenta.
      - name: "10. Citacoes da doc (tools/checa_citacoes.py)"
        run: |
          if [ -f tools/checa_citacoes.py ]; then
            python tools/checa_citacoes.py
          else
            echo "tools/checa_citacoes.py nao esta no repo - passo pulado de proposito."
            echo "Ele e versionado em tools/ hoje; se sumiu, foi remocao."
          fi
```

Antes de ligar qualquer check novo vale a regra da seção abaixo (passos 2 e 3): rode a ferramenta
**hoje** e confirme o código de saída. Em 01/10/2026 o `checa_citacoes.py` sai `0` na árvore atual
(83 citações/menções em 65 documentos, 0 pendências) e sai `1` quando uma citação quebrada é
plantada — uma isca de cópia que citava uma **linha fora do arquivo** (99999 num fonte de 1616
linhas) e um **caminho de `.cs` que não existe no repositório** reprovou pelo motivo certo,
apontando o documento e a linha.

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
  - **O `validate.yml` que está no ar já roda a flag.** Conferido em 30/09/2026 lendo o arquivo
    publicado (não o do disco): o `curl` de
    `https://raw.githubusercontent.com/DefRuivo/stolenRealmMods/main/.github/workflows/validate.yml`
    traz a linha `run: python tools/check_chave_compartilhada.py --estrito`. Para reconferir, leia
    o publicado — **não** compare MD5 com o do disco: o disco pode estar sujo (edição não
    commitada) ou em CRLF, e uma reescrita de histórico muda os SHAs. Regra geral desta doc:
    confirme com `git ls-remote origin main` contra `git rev-parse HEAD` antes de assumir.
    Ou seja, o CI **já trava** no caso do `BUG-32`; a versão que falava em "passo 5 sem a flag"
    não é a que está no ar. Editar `.github/workflows/` pela linha de comando continua exigindo o
    escopo `workflow` no PAT (o escopo da credencial atual não foi verificado), mas o que está
    publicado está atualizado.
  - **Comentário desatualizado dentro do YAML (texto fora desta doc).** O passo 7 do
    `validate.yml` ainda diz no comentário que o `tools/audita_docs.py` "vive em `scratch/`,
    gitignored" — não vive: ele é **versionado** em `tools/` (passo 7 do CI) e a auditoria roda de
    verdade a cada push. O passo funciona (a checagem é condicional), mas o comentário mente e é
    texto dentro de `.github/`, não desta doc.
- **O passo 2 tem 4 avisos que não são erro.** Chaves de UI/loading que o censo do RV-7
  ainda não cobre (a frase das lojas, `Resist Divine`/`Resistance Divine`, a dica da
  poção). Isso é esperado e está documentado em
  [`cobertura/README.md`](cobertura/README.md), na seção "O que este censo AINDA não cobre".
- **Pasta de mod sem `manifest.json` não é erro.** O passo 6 a **avisa** e segue: um mod
  em implementação ainda não é pacote, então não há o que validar; assim que o `manifest.json`
  aparecer, ele passa a ser validado sozinho. O `RoguelikeSkillTreeVisualizer` foi esse caso até
  30/09/2026 — hoje ele já tem `manifest.json`, `README.md`, `CHANGELOG.md` e `icon.png` e entra na
  validação normal (`python .github/scripts/valida_pacotes.py` → **6 pacotes validados, 0 com
  problema**, medido em 30/09/2026).

## Adicionar um check novo

1. Escreva a ferramenta em `tools/` (ou em `.github/scripts/` se for específica de CI).
   Ela deve sair com código `!= 0` quando reprovar e dizer **arquivo e linha** do problema.
2. Rode-a contra o repo **hoje** e confirme o código de saída real, antes de ligar no CI —
   ligar um check que já nasce vermelho trava a branch de todo mundo.
3. Adicione o passo em `validate.yml`, na posição certa da ordem, com um comentário do
   tipo de defeito que ele pega.
