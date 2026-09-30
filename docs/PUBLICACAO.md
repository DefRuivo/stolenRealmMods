# Publicação na Thunderstore (PUB-4 + CI-3)

O caminho de uma **versão nova** dos mods até a comunidade
[`stolen-realm`](https://thunderstore.io/c/stolen-realm/), com duas travas humanas e
nenhuma etapa "adivinha": quem pode sair está escrito no repositório
([`release/mods.json`](../release/mods.json)) e quem libera o envio é um clique de aprovação
no GitHub ([`.github/workflows/publish.yml`](../.github/workflows/publish.yml)).

**Estado hoje (30/09/2026): nada foi publicado.** Os **6** mods estão com `publicar: false`
(conferido no [`release/mods.json`](../release/mods.json)) e o `team` está vazio de propósito
(decisão pendente). Os dois workflows **já estão no remoto** — conferido com
`git ls-remote origin main` e com o `curl` do YAML publicado (mesmo MD5 do arquivo no disco), ver
[`CI.md`](CI.md) — então o pipeline está **vivo**, não "só no disco": ele **falha antes de tocar
em qualquer coisa** porque o `team` está vazio, e não chuta.

## 1) As regras da plataforma que mandam no desenho

| Regra | Consequência prática |
|---|---|
| **Versão é imutável.** Depois de aceita, não se edita nada — nem o README. | Qualquer mudança, inclusive de texto, exige uma **versão nova**. Não existe "consertei o README". |
| **Atualizar = subir `version_number` e reenviar.** | O `<Version>` do `.csproj` é a fonte (PKG-2); `manifest.json` e `Plugin.cs` são espelhos conferidos. |
| **O `name` do pacote não muda.** | Trocar o `name` cria um pacote **NOVO** (o antigo continua no ar com os downloads). |
| **O TEAM não muda.** | Publicar no mesmo `name` por outro team também cria pacote novo. O team **vem do token**, não do zip: `namespace` no workflow é informativo, quem decide é o token. |
| **Versão é SemVer `X.Y.Z`, comparada por parte.** | `1.0.10 > 1.0.1`. A plataforma exibe sempre a **maior** versão, independente da data do upload — publicar uma versão menor "some" da vitrine. |
| Nome do pacote tem que bater com a pasta dos plugins. | Já coberto pelo pre-flight do empacotador e pelo passo 6 do [CI de validação](CI.md). |

O que o pipeline lê da plataforma é a **API pública da comunidade**:
`https://thunderstore.io/c/stolen-realm/api/v1/package/` → por pacote, a lista de
`versions[].version_number` publicada. Ela é a única prova de "esta versão já existe".

## 2) O gate do que pode sair: `release/mods.json`

O quadro de tarefas do projeto é uma nota local, fora do git — então o CI **não tem como
consultá-lo**. O [`release/mods.json`](../release/mods.json) é o substituto versionado e
revisável no diff:

```json
{ "nome": "BetterFont", "publicar": false, "versao_publicada": null,
  "publicado_em": null, "motivo": "primeira publicacao ainda nao feita - ..." }
```

- **`publicar: true`** é o que libera. O pipeline publica **só** o que estiver `true`.
- **`publicar: false`** nunca é enviado — nem se você escolher o mod a dedo no disparo
  manual: nesse caso o job **falha de propósito** e mostra o `motivo`. Escolher um mod
  travado é pedido explícito, então a resposta é "não" com o porquê, não um run verde.
- **`versao_publicada` / `publicado_em`** são escritos pelo próprio pipeline (job
  `registra`), **depois** de confirmar na API pública — o pipeline não presume que o envio
  funcionou, ele lê o resultado. Se a API não mostrar a versão, o registro não acontece.
- A lista de mods do JSON tem que ser a mesma que o empacotador descobre
  (`python tools/pack-thunderstore.py --listar-nomes`). O gate confere isso a cada run: uma
  segunda lista de mods divergindo é falha, não aviso.

Para liberar um mod: vire `publicar` para `true`, escreva o `motivo` e commite. A decisão
fica no histórico.

## 3) O gate humano: o GitHub Environment `thunderstore`

A aprovação é uma pessoa clicando. Não é variável de ambiente, não é label.

1. **Settings → Environments → New environment** → nome **`thunderstore`**.
2. Marque **Required reviewers** e escolha quem aprova (o dono do repositório).
3. Opcional, recomendado: em **Deployment branches**, restrinja a `main`.
4. Adicione o secret **no Environment** (não no repositório):
   **Environment secrets → `THUNDERSTORE_TOKEN`**, com o token de **service account do team
   escolhido** (PUB-3 — o team define a URL do pacote para sempre).

Quando o workflow chega no job `publica`, ele **para** e aparece em
**Actions → (o run) → Review deployments**. Só o que for aprovado roda. O secret do
Environment é a única fonte do valor: `secrets.THUNDERSTORE_TOKEN` dentro do job com
`environment: thunderstore` — nenhum outro job enxerga.

O token **nunca** aparece em log: os passos só dizem "token presente", o valor vem mascarado
do `secrets` e o próprio YAML não contém credencial nenhuma (`tools/check_segredos.py` roda
como passo 1 do job e reprova se algum token entrar no que seria publicado).

## 4) O que o CI **não** faz — e por quê

**O CI não compila.** Os `.csproj` referenciam as assemblies do *jogo*
(`Assembly-CSharp.dll`, `UnityEngine`, `Sirenix`), que vivem em `lib/` (gitignored) e não
existem num runner limpo. Commitar a DLL do jogo num repositório **público** está fora de
cogitação (é propriedade do jogo). Logo: **quem compila e empacota é a máquina de
desenvolvimento**, e o CI só transporta o `.zip` pronto.

Isso é viável porque a Action
[`GreenTF/upload-thunderstore-package`](https://github.com/GreenTF/upload-thunderstore-package)
aceita o input `file:` e **pula o build** quando recebe um pacote pronto.

Como o zip chega ao runner (escolha uma):

| Caminho | Como | Quando usar |
|---|---|---|
| **GitHub Release (recomendado hoje)** | `gh release create v1.0.0 dist/gumatos-*.zip` e dispare o workflow com o input `release_tag = v1.0.0` | Runner normal (`ubuntu-latest`), sem máquina própria no CI |
| **Runner self-hosted** | O `dist/` já existe na máquina que tem o jogo; trocar `runs-on` para `self-hosted` | Quando quiser um clique só, do commit até a Thunderstore |

Aceitável subir **DLL de mod** (é código nosso). DLL do jogo, nunca.

## 5) Passo a passo de um release

Tudo da raiz do repositório, na máquina com o jogo instalado.

```bash
# 1) A versão é o <Version> do .csproj (fonte). Suba a versão lá primeiro.
#    Depois espelhe nos dois lugares que carregam versão:
python tools/pack-thunderstore.py --sincronizar-versao

# 2) Compile Release SEM instalar no perfil (a flag é obrigatória: sem ela o build
#    sobrescreve a DLL do r2modman antes de empacotar) e empacote:
dotnet build BetterTooltips/BetterTooltips.csproj -c Release -p:DeployToBepInEx=false
python tools/pack-thunderstore.py BetterTooltips     # pre-flight dos 3 lugares da versão + zip

# 3) Prove que a versão ainda não existe (a plataforma é imutável):
curl -s https://thunderstore.io/c/stolen-realm/api/v1/package/ | grep -o 'gumatos-BetterTooltips[^"]*'

# 4) Libere o mod no gate e commite (é isto que o CI lê):
#    release/mods.json -> "publicar": true  e o "motivo" explicando

# 5) Anexe os zips numa Release (ou deixe o dist/ no runner self-hosted):
gh release create thunderstore-1.0.0 dist/gumatos-*.zip --title "Pacotes 1.0.0"

# 6) Dispare o workflow: Actions -> "Publicacao Thunderstore" -> Run workflow
#    input `mod` = BetterTooltips (ou "todos") e `release_tag` = thunderstore-1.0.0

# 7) Aprove no gate humano: Actions -> run -> Review deployments

# 8) Confira o resultado na comunidade e o registro no repositório:
#    https://thunderstore.io/c/stolen-realm/  +  release/mods.json (versao_publicada/publicado_em)
```

**Envio local (sem GitHub)** continua valendo como sempre, e é o caminho mais curto hoje:
`bash tools/publish-thunderstore.sh` (**dry-run** por padrão; só envia
com `--go`). Ele roda a trava de segredo e o `tools/release-check.sh` antes de qualquer coisa
e lê o token de `TCLI_AUTH_TOKEN` / `THUNDERSTORE_TOKEN_FILE` / `~/.thunderstore-token` —
**nunca** de dentro do repositório (se o arquivo estiver dentro, ele recusa).

## 6) O que o pipeline verifica sozinho

| # | Verificação | Recusa quando |
|---|---|---|
| 1 | `tools/check_segredos.py` | entrou token/credencial no que seria publicado |
| 2 | Token do Environment | `secrets.THUNDERSTORE_TOKEN` vazio (environment não configurado) |
| 3 | Gate `release/mods.json` | mod escolhido está `publicar: false`; lista de mods divergiu do empacotador; `team` vazio |
| 4 | Pacote presente | não existe `dist/gumatos-<Mod>-<versao>.zip` → diz o comando exato do build + empacotador |
| 5 | Pacote é deste commit | zip com manifesto diferente do `manifest.json` do repositório, ou zip incompleto (falta DLL/ícone/README/CHANGELOG) |
| 6 | Versão contra a API pública | versão **já publicada** (imutável) ou **não maior** que a que está no ar |
| 7 | Registro no JSON | o JSON diz que uma versão saiu e a API não tem; e só grava o que a API confirmar |

Se qualquer passo falhar, **nada é enviado** e o log diz o arquivo e o comando do conserto.
O pre-flight roda **depois** da aprovação mas **antes** de qualquer envio — aprovar acorda o
job, não publica nada.

## 7) Modo automático (desligado) e o runner self-hosted

No topo do `publish.yml` existe um bloco `push:` **comentado**, com o filtro nativo `paths:`
por pasta de mod (`'BetterTooltips/**'`, …). É assim que se responde "qual mod mudou" sem
script adivinhando: o GitHub só dispara o run se algo entrou naquela pasta, e o
`release/mods.json` continua decidindo se aquele mod **pode** sair.

Ele está desligado por um motivo concreto: **um runner hospedado pelo GitHub não compila**
estes mods (a `lib/` do jogo não está lá). Ligar o modo automático exige um runner
**self-hosted** numa máquina com o jogo instalado, que rode o build + o empacotador antes do
envio. Nesse cenário:

- `runs-on: self-hosted` no job `publica`;
- o `dist/` passa a ser local (dispensa o input `release_tag`);
- o **environment com revisores continua** — automação de build não substitui aprovação humana.

## 8) Estado dos workflows e o escopo `workflow` do PAT

Os dois YAML **já estão publicados** — conferido em 30/09/2026: o `main` do GitHub é o mesmo
commit do HEAD local (`git ls-remote origin main`) e o arquivo publicado tem o **mesmo MD5** do
arquivo no disco. O que continua exigindo credencial é **editar** esse caminho: um push que mexe
em `.github/workflows/` precisa do escopo de workflow no PAT. O escopo da credencial atual **não
foi verificado** (é segredo); se o push desse caminho for recusado, habilite:

| Token | O que habilitar |
|---|---|
| **Fine-grained PAT** | *Repository permissions → **Workflows: Read and write*** (além de `Contents: Read and write`) |
| **Classic PAT** | escopo **`workflow`** (além de `repo`) |

**Conferir o que está publicado, sem credencial** (foi assim que este documento foi corrigido):

```bash
git ls-remote origin main        # o main do GitHub é o mesmo commit daqui?
curl -s https://raw.githubusercontent.com/DefRuivo/stolenRealmMods/main/.github/workflows/validate.yml | md5sum
md5sum .github/workflows/validate.yml     # mesmo hash = o arquivo do disco é o que está no ar
```

A árvore completa da API, também sem credencial:
`curl -s "https://api.github.com/repos/DefRuivo/stolenRealmMods/git/trees/main?recursive=1"`
(procure `publish.yml`; a leitura vem com `\r` no Windows).

> **Correção (30/09/2026):** a versão anterior deste documento dizia que os workflows viviam só
> no disco, por falta do escopo `workflow`. Isso deixou de valer: o commit `d417a81` ("CI: ativa
> os workflows de validacao e de publicacao (escopo workflow no PAT)") subiu os dois, e o
> `validate.yml` que está no ar roda o passo 5 **com** `--estrito`.

## 9) Armadilhas conhecidas (todas vividas ou conferidas na fonte)

- **A API pública responde `403` ao User-Agent padrão do `urllib`.** `curl` passa, o Python
  não. O pipeline manda um `User-Agent` próprio; um script novo que leia a API sem cabeçalho
  vai parecer "API fora do ar".
- **`repo:` é obrigatório na Action.** Sem esse input o script dela monta
  `tcli publish --repository` com valor vazio e o envio quebra. O valor usado é
  `https://thunderstore.io`.
- **`file:` é relativo à raiz do repositório, e o caminho real vira `dist/<file>`.** A Action
  move a raiz do repo para `/dist` e publica `dist/$file` — por isso o valor no YAML começa
  com `dist/` e *não* é engano. Não "conserte" isso.
- **Versão repetida não dá segunda chance.** A plataforma recusa a versão inteira; o
  conserto é subir o `version_number` (e refazer o zip). O pre-flight evita o round-trip.
- **Versão menor que a que está no ar** é aceita pela API e some da vitrine (a plataforma
  mostra a maior). O pre-flight recusa.
- **Zip de outro commit**: se você editar o `manifest.json`/descrição depois de zipar, o
  pre-flight acusa "o zip não é deste commit". Rebuilde e reempacote.
- **`RoguelikeSkillTreeVisualizer` tinha o pacote incompleto** (faltava `CHANGELOG.md`) e por isso
  não podia ser liberado. **Corrigido em 30/09/2026:** os 6 mods têm `manifest.json`, `README.md`,
  `CHANGELOG.md` e `icon.png`, e o `python .github/scripts/valida_pacotes.py` valida os
  **6 pacotes com 0 problemas** — o empacotador não recusa mais nenhum por pacote incompleto.
  O que ainda trava esse mod é só o gate (`publicar: false`).
- **O `[skip ci]` no commit do registro** evita disparar a validação inteira de novo por um
  commit que só escreve a versão publicada.
- **Push do registro pode falhar** (proteção de branch, permissão de escrita). Nesse caso a
  publicação **já aconteceu**: o run diz isso e deixa o bloco JSON no resumo para commitar à
  mão — nunca commite uma versão que a API não mostra (o pre-flight da próxima publicação
  recusa).

## 10) Tarefas relacionadas (ainda abertas)

- **PUB-2** — primeira publicação (aprovação por envio).
- **PUB-3** — decidir o **team**: define a URL do pacote para sempre. É o que segura o
  `team` vazio em `release/mods.json`.
- **SEC-1** — rotacionar os tokens que foram expostos; trocar o arquivo local não revoga nada.

## Arquivos deste pipeline

| arquivo | papel |
|---|---|
| [`.github/workflows/publish.yml`](../.github/workflows/publish.yml) | o workflow: gate, environment, pre-flight, envio, registro |
| [`.github/workflows/validate.yml`](../.github/workflows/validate.yml) | o outro lado da trava: valida a cada `push`/PR (não compila, não publica) — ver [CI.md](CI.md) |
| [`release/mods.json`](../release/mods.json) | o gate versionado: quem pode sair e o que já saiu |
| [`tools/pack-thunderstore.py`](../tools/pack-thunderstore.py) | gera o `.zip` que o pipeline transporta (pre-flight de versão única/ícone/DLL) e dá a lista de mods (`--listar-nomes`) |
| [`tools/publish-thunderstore.sh`](../tools/publish-thunderstore.sh) | publicação pela linha de comando (**dry-run** por padrão; `--go` envia) |
| [`.github/scripts/valida_pacotes.py`](../.github/scripts/valida_pacotes.py) | o que o CI confere do pacote **sem** DLL: manifest, ícone 256x256, README e CHANGELOG |
| [`.github/scripts/`](../.github/scripts) | a pasta das ferramentas que só existem para o CI |
| este documento | o processo, os comandos e as armadilhas |
| [docs/CI.md](CI.md) | onde a validação e a publicação se encontram |
