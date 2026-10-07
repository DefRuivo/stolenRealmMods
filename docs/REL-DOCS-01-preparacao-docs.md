# REL-DOCS-01 — preparação local dos patches documentais (BetterFont, BetterStats, BetterCombatText)

Cartão: `t_c002ac7c` · Data da medição: **2026-10-07** (madrugada) · Workspace: `C:\dev\stolen-realm`

**O que este documento é:** a prova de que os três pacotes abaixo estão prontos para upload, com o
hash de cada artefato, o que cada um leva, e a lista do que o **dono** ainda tem de decidir/assinar.
**O que ele não é:** um aceite. Publicar não aconteceu e não acontece aqui — sem push, sem tag, sem
Release, sem `workflow_dispatch`, sem upload, sem `publicar:true` tocado, sem jogo aberto, sem
`dotnet build` com deploy, sem `Assembly-CSharp.dll` e sem nada de Bard.

---

## 1. Consulta fresca antes do bump (a fonte é a API pública, não a memória)

| Pacote | Última versão publicada (API) | Descrição **no ar** | Alvo deste patch |
|---|---|---|---|
| DefRuivo_StolenRealmMods/BetterFont | **1.0.2** | inglês (igual à da árvore) | **1.0.3** |
| DefRuivo_StolenRealmMods/BetterStats | **1.0.1** | **português** (diverge da árvore) | **1.0.2** |
| DefRuivo_StolenRealmMods/BetterCombatText | **0.1.1** | inglês, com o aviso "not yet verified in game" | **0.1.2** |

Endpoint usado (por pacote, o único fresco): `https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/<Mod>/`.
Os três números-alvo do cartão batem com o que a API serve. Nenhum deles existe no ar ainda (o bump é
válido — versão publicada é imutável).

---

## 2. Matriz dos três artefatos

ZIP publicado baixado da plataforma (para comparação artefato × artefato):
`https://thunderstore.io/package/download/DefRuivo_StolenRealmMods/<Mod>/<versão>/`

| | BetterFont | BetterStats | BetterCombatText |
|---|---|---|---|
| Publicado (no ar) | 1.0.2 | 1.0.1 | 0.1.1 |
| ZIP publicado (sha256) | `b284fabf…e9ecdf` | `3470dcd4…dc967c` | `bb5bb64d…533d11` |
| DLL dentro do ZIP publicado | `2c07f5e959afbf39…` | `5a3c001ad424f0de…` | `06dae5aa7b5e345a…` |
| **Novo** pacote | **1.0.3** | **1.0.2** | **0.1.2** |
| Caminho do pacote | `dist/gumatos-BetterFont-1.0.3.zip` | `dist/gumatos-BetterStats-1.0.2.zip` | `dist/gumatos-BetterCombatText-0.1.2.zip` |
| **ZIP novo (sha256)** | `bc1de51e3da81e5736fe51f20ab7a30d5b9c875f5cb5c07d2844b017e5ea4e73` | `fa26dd0ce993d74b4d50e05516d978f86b82d6c0bf67f7c7ce9e4d99fa4d45f8` | `9b216b88fbbe7b21cf785846cd695a764cddb44d4ce95b470a674584a47117d4` |
| ZIP novo (bytes) | 113920 | 100632 | 157085 |
| **DLL nova (sha256)** | `811428ae5b2af6337bff66dccd2ced7ff954729d41a1c58cf93196156415f06e` | `e45dc9d7007e5b4d7c74fb3a8df8aa90d630071f8305684de1b88a8ab85c9e08` | `d3fc0c1ba8d710edaa0be9f4d311202c41bc6abb6e814957c990f3fce34009e1` |
| DLL bytes | 34816 (=) | 10752 (=) | 50176 (=) |
| Arquivos no ZIP | 5 | 5 | 5 |
| `manifest` version / nome | 1.0.3 / BetterFont | 1.0.2 / BetterStats | 0.1.2 / BetterCombatText |
| Dependências | `BepInEx-BepInExPack-5.4.2305` | `BepInEx-BepInExPack-5.4.2305` | `BepInEx-BepInExPack-5.4.2305`, `DefRuivo_StolenRealmMods-BetterFont-1.0.2` |
| `description` (chars ≤250) | 212 | 178 | 191 |
| Ícone | 256×256, 87821 B | 256×256, 91250 B | 256×256, 124954 B |

Cada ZIP leva, na raiz, `manifest.json` + `README.md` + `CHANGELOG.md` + `icon.png` e
`plugins/<Mod>/<Mod>.dll` — conferido lendo o ZIP, não o disco.

---

## 3. Prova de que a DLL nova é a fonte de hoje (e só muda a versão)

**Método (artefato × artefato).** As duas DLLs (a extraída do ZIP publicado e a recém-buildada em
`<Mod>/bin/Release/netstandard2.1/`) foram abertas e **todo o conjunto de literais UTF-16LE** foi
extraído e comparado. Resultado:

| Mod | strings só na publicada | strings só na nova | literais (pub/nova) | tamanho do arquivo |
|---|---|---|---|---|
| BetterFont | `1.0.2`, `1.0.2.0` | `1.0.3`, `1.0.3.0` | 206 / 206 | 34816 = 34816 |
| BetterStats | `1.0.1`, `1.0.1.0` | `1.0.2`, `1.0.2.0` | 39 / 39 | 10752 = 10752 |
| BetterCombatText | `0.1.1`, `0.1.1.0`, `Better Combat Text 0.1.1 carregado (GUID …)` | `0.1.2`, `0.1.2.0`, `… 0.1.2 carregado …` | 259 / 259 | 50176 = 50176 |

Ou seja: **a única diferença entre a DLL publicada e a nova é o literal de versão** (e a linha de log
que o interpola). Não houve mudança funcional — que é o que o cartão pede. Prova mecânica de que a
versão nova viaja no binário: o literal novo aparece dentro da DLL **extraída do ZIP novo**.

> Limite honesto deste método: ele compara **literais**, não IL/metadata. Ele não prova byte-identidade
> de código; prova que nenhum texto do assembly mudou. A garantia complementar é a de §4 (o ZIP novo
> contém exatamente os arquivos da árvore) e a de que os `.cs` dos três mods não foram editados aqui
> além do literal de versão (o `--sincronizar-versao` do empacotador é o único que mexeu).

**Build.** `dotnet build <Mod>/<Mod>.csproj -c Release -p:DeployToBepInEx=false` nos três:
`0 Erro(s)` em cada (BetterStats com 1 aviso CS0618 pré-existente; os três com o MSB3277 do
`Assembly-CSharp` pré-existente). Nada foi instalado — o deploy é opt-in e a flag foi passada.

---

## 4. Reconciliação: publicado × árvore (o que cada patch corrige)

Comparação **arquivo por arquivo** entre o ZIP no ar e a árvore. Isto é o "reconciliar todas as
mudanças desde o release", independente do `git diff` de hoje.

**BetterFont 1.0.2 (no ar) × árvore** — `manifest.json` igual, `CHANGELOG.md` igual, **`README.md`
difere**: o texto publicado ensina que um `dotnet build` "também copia a DLL para o perfil" — falso
desde DEPLOY-2. → corrigido no 1.0.3.

**BetterStats 1.0.1 (no ar) × árvore** — diverge nos **três**:
- `manifest.json`: a `description` publicada está **em português**; a da árvore está em inglês.
- `README.md`: o publicado é o texto **antigo, em português, com `Version: 1.0.0`** (124 linhas de
  diferença); a árvore tem o README em inglês.
- `CHANGELOG.md`: 3 correções de tempo verbal (a 1.0.0 afirmava que a versão "não subiu" e que o
  defeito foi corrigido "antes de qualquer download").
→ tudo isso viaja no 1.0.2.

**BetterCombatText 0.1.1 (no ar) × árvore** — `manifest.json` igual, `CHANGELOG.md` igual,
**`README.md` difere** em dois pontos: (a) a mesma frase errada do deploy; (b) **defeito de conteúdo
achado nesta tarefa** — o README dizia "soft outline/halo, default black at 10% alpha" para os nomes
de inimigo, mas desde a 0.1.1 o nome recebe **contorno duro e opaco** (`LarguraContorno` 0.22,
`SuavidadeContorno` 0.05, `AlfaContorno` 0.95) e o 10% é o contorno dos **rótulos**; a sombra do nome
é curta e visível (`AlfaSombra` 0.75, offset ±0.35). Conferido no fonte: `BetterCombatText/Configuracao.cs:117-130`
(nomes) contra `:132-144` (rótulos) e `:150-163` (dado). A tabela de superfícies e a seção de
configuração passaram a dizer os defaults reais. → viaja no 0.1.2.

---

## 5. O aviso "not yet verified in game" do BetterCombatText — **MANTIDO**

O cartão manda consultar o aceite histórico arquivado **antes** de remover o aviso, e não inventar
aceite. Consulta feita, e o resultado é **não há aceite registrado**:

- `t_540bcf8e` (ENTREGA-BCT-011, arquivado): a CONDIÇÃO 1 é "o dono confirma em combate os efeitos…";
  o cartão tem **1 comentário, sobre ordem de envio, e nenhum `result`** — foi arquivado com a
  condição **aberta**. `t_e57fe3bf` (ENTREGA-BF-102) está no mesmo estado.
- A revisão independente REV-52 (`t_116521c4`) registra o ponto sensível do projeto com estas
  palavras: "o BetterCombatText **NAO tem efeito visual confirmado**".
- O AUT-7 mede o estado geral: `ACEITE HUMANO: NAO_PRONUNCIADO`.
- A única afirmação em contrário é **uma linha escrita por agente** em `release/mods.json`
  ("Revisado pelo dono em jogo") — e o gate do lote (`t_91b357f4`) diz literalmente
  "**nunca atribuir aceite a agente**".

Consequência: o aviso **fica** no `description` e no README, e o CHANGELOG 0.1.2 diz isso em uma
linha. Nuance registrada para não exagerar o outro lado: em 02/10 o dono **olhou a tela** e relatou um
defeito ("não vejo sombra nos nomes", BCT-5) — houve olhar, não houve **aceite**. Quem fecha essa
questão é o dono, olhando a 0.1.2 em combate; aí sim um bump futuro pode tirar a frase.

---

## 6. O que o patch entrega, em texto (resumo editorial)

Os três `CHANGELOG.md` ganharam uma seção nova no topo, **em inglês, escrita para o jogador**, dizendo
sem rodeios que é **release de documentação, sem mudança de código**:

- **BetterFont 1.0.3** — instrução de build corrigida (deploy é opt-in) + por que um conserto de texto
  custa uma versão nova (versão publicada é imutável).
- **BetterStats 1.0.2** — página em inglês (descrição + README), instrução de build corrigida e as
  duas notas que mentiam sobre a própria versão.
- **BetterCombatText 0.1.2** — instrução de build corrigida, a tabela de superfícies com os defaults
  reais do contorno, e a linha dizendo que o resultado visual **continua** não confirmado.

Nada de `description`, README ou CHANGELOG foi traduzido/reescrito além disso: as **seções antigas dos
CHANGELOGs continuam em português e com jargão interno** (IDs de tarefa, hashes, linhas do
decompilado). Isso já tinha sido registrado como **decisão de escopo do dono** na DOC-4
("reescrever 6 changelogs técnicos é decisão de escopo") e **não** foi feito aqui por conta própria —
está no checklist do §8. O `README` do BetterStats, que era o pior caso (português e `Version: 1.0.0`),
**está** resolvido porque a árvore já tinha a versão em inglês e ela agora entra no pacote.

---

## 7. Dependências: nada foi mexido

- `BetterFont` e `BetterStats` seguem só com `BepInEx-BepInExPack-5.4.2305`.
- `BetterCombatText` continua apontando **`DefRuivo_StolenRealmMods-BetterFont-1.0.2`** — que **já está
  no ar**. **Não** foi bumpada para 1.0.3 de propósito: o cartão proíbe atualizar dependência sem
  necessidade, e apontar para uma versão inédita criaria a restrição de ordem de envio (dependente
  depois da dependência). Como está, **os três podem subir em qualquer ordem**.
- `python tools/check_dependencias.py --local`: **todas as dependências resolvem** (exit 0).

---

## 8. Gates e exit codes (medidos agora, não herdados)

| Gate | Comando | Exit | Observação |
|---|---|---|---|
| Versão única em 4 lugares | `python tools/check_versoes.py` | **0** | os 6 mods batem (csproj = manifest = Plugin.cs = README) |
| Deploy opt-in | `python tools/check_deploy_optin.py` | **0** | 7 alvos com `Condition="'$(DeployToBepInEx)' == 'true'"` |
| Dependências | `python tools/check_dependencias.py --local` | **0** | 7 referências resolvem |
| Pre-flight do empacotador | `python tools/pack-thunderstore.py --config Release --so-conferir …` | **0** | artefato × fonte + versão única + manifest + ícone, nos 3 |
| Build Release sem deploy | `dotnet build … -c Release -p:DeployToBepInEx=false` | **0** | 0 erro nos 3 |
| Empacotamento | `python tools/pack-thunderstore.py --config Release …` | **0** | 3 pacotes |
| Segredos | `python tools/check_segredos.py` | **1** | **VERMELHO PRÉ-EXISTENTE**, fora do escopo — ver abaixo |

**O vermelho do `check_segredos` é anterior a esta tarefa e não é meu.** Os três achados estão em
`docs/automacao/AUT-3FR-revisao.md:37` e `tools/automacao/offline/testes/t_aut3f2_achados.py:237,245`
(fixtures de teste com URL de push e chaves privadas **falsas**). Prova de preexistência: os marcadores
**já estão em `HEAD`** (`git show HEAD:<arquivo>` devolve 1 e 4 ocorrências) e nenhum dos dois arquivos
aparece em `git status` como tocado por mim. **Não commitar enquanto não for resolvido** — e não é
resolvido às escondidas por esta tarefa (decisão de quem cuida do CIC).

Estado da árvore ao fim: **exatamente 15 arquivos** tocados, todos dentro das três pastas de mod
(5 por mod: `.csproj`, `Plugin.cs`, `manifest.json`, `README.md`, `CHANGELOG.md`). Nenhum
`git add -A`, nenhum diretório, nada commitado, nada empurrado. `dist/` é gitignored.

---

## 9. Checklist de aprovação editorial humana (o que só o dono decide)

Os pacotes estão **prontos e verificados**; o que falta é decisão humana, item por item:

- [ ] **1. BetterFont 1.0.3 — ler o CHANGELOG novo e o trecho de build do README.** Aprovar o texto.
- [ ] **2. BetterStats 1.0.2 — ler a `description` em inglês e o README inteiro** (era o pacote em
      português; é a mudança mais visível da leva). Aprovar.
- [ ] **3. BetterCombatText 0.1.2 — ler o CHANGELOG novo e a tabela de superfícies do README.**
      Aprovar a redação dos defaults (contorno duro nos nomes).
- [ ] **4. O aviso "not yet verified in game" FICA** (§5). Se o dono já tiver confirmado em jogo, diga
      — aí a remoção é um bump futuro, com o aceite registrado no cartão.
- [ ] **5. Changelogs antigos em português/jargão** (§6): manter como estão, ou autorizar a
      reescrita (é decisão de escopo do dono, não foi feita).
- [ ] **6. Escolher a ordem de envio.** Não há restrição entre os três. Sugestão (menor → maior
      impacto de página): BetterFont → BetterStats → BetterCombatText.
- [ ] **7. `release/mods.json` está desatualizado e não foi tocado aqui:** ele diz
      `BetterCombatText.versao_publicada = "0.1.0"` enquanto a **API serve 0.1.1**. Quem reconciliar o
      ledger é o `t_79efef8c` (REL-CI-01), não esta preparação.
- [ ] **8. Resolver o vermelho pré-existente do `check_segredos`** antes de qualquer CI de publicação.

> **Fechar esta preparação não é o DoD do mod e não é aprovação de publicação.** O DoD exige aceite
> humano da versão exata, upload real e confirmação pela API — é o que o cartão `t_91b357f4`
> (ENTREGA-DOCS-01) executa, e ele segue bloqueado até a aprovação do dono.

---

## 10. Prova por decompilação (DLL **extraída do ZIP novo**, não a do `bin`)

`ilspycmd -t <Mod>.Plugin <dll do ZIP>` — o atributo lido:

```
BetterFont        [BepInPlugin("com.gumatos.betterfont", "Better Font", "1.0.3")]
BetterStats       [BepInPlugin("com.gumatos.betterstats", "Better Stats", "1.0.2")]
BetterCombatText  [BepInPlugin("com.gumatos.bettercombattext", "Better Combat Text", "0.1.2")]
                  public const string Versao = "0.1.2";
```

As DLLs foram extraídas dos ZIPs de `dist/` num diretório de trabalho **fora do repositório**, para
que a prova seja do **artefato empacotado** e não do `bin/Release`.

---

## 11. Como reproduzir a verificação (sem efeito colateral)

```bash
# pré-requisito: os 3 zips publicados, baixados para uma pasta fora do repo
#   https://thunderstore.io/package/download/DefRuivo_StolenRealmMods/<Mod>/<versao>/
for m in BetterFont BetterStats BetterCombatText; do
  dotnet build $m/$m.csproj -c Release -p:DeployToBepInEx=false
done
python tools/check_versoes.py && python tools/check_deploy_optin.py && python tools/check_dependencias.py --local
python tools/pack-thunderstore.py --config Release --so-conferir BetterFont BetterStats BetterCombatText
python tools/pack-thunderstore.py --config Release BetterFont BetterStats BetterCombatText
```

Os hashes deste documento saem de: `sha256sum dist/gumatos-Better*-*.zip` e `sha256sum
<Mod>/bin/Release/netstandard2.1/<Mod>.dll`. Nenhum dos comandos abre o jogo, instala no perfil ou
toca a Thunderstore.
