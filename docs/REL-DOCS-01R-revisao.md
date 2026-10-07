# REL-DOCS-01R — revisão independente da preparação dos patches documentais (BetterFont, BetterStats, BetterCombatText)

Cartão revisado: `t_c002ac7c` (REL-DOCS-01) · Revisão: `t_2b14610d` (REL-DOCS-01R) · Data: **2026-10-07**, ~04:40–05:0x local
Workspace: `C:\dev\stolen-realm` · HEAD na revisão: **88232fe** (inalterado; nada commitado pela preparação)

**Método.** Nada aqui vem do resumo do autor: cada número foi remedido a partir do artefato (ZIP publicado
baixado da plataforma, ZIP novo em `dist/`, DLL do ZIP, DLL do `bin/Release`) e do código-fonte. As quatro
contra-provas mais fortes contra o parecer do autor estão no §4 (byte a byte e decompilação) — duas delas
**elevaram** a prova que ele entregou, e uma **encontrou defeito que ficou de fora**.

**O que esta revisão NÃO fez:** não mudou fonte nem produto, não instalou nada no perfil, não abriu o jogo,
não fez build com deploy, não empacotou (os ZIPs de `dist/` são os do autor, intactos), não fez push/tag/
Release/`workflow_dispatch`/upload e **não aprovou** nada. O único arquivo que esta revisão escreveu é este
documento. Builds foram feitos em **cópia isolada** (ver §4.3), fora da árvore.

---

## 1. Veredito por item

| # | Item | Veredito |
|---|---|---|
| 1 | Consulta fresca de versão antes do bump (§1 do doc) | **OK** |
| 2 | Matriz dos três artefatos, hashes e tamanhos (§2) | **OK** |
| 3 | Layout do ZIP e conteúdo igual à árvore | **OK** |
| 4 | "Só muda o literal de versão" — nenhuma mudança funcional (§3) | **OK, e a prova foi ELEVADA** |
| 5 | Gates e exit codes (§8) | **OK** (com nota no `check_segredos`) |
| 6 | Reconcilição publicado × árvore (§4) | **OK** (defeito do BCT confirmado no fonte) |
| 7 | Aviso "not yet verified in game" do BCT mantido (§5) | **OK** |
| 8 | Dependências não mexidas e resolvendo (§7) | **OK** (também por API fresca) |
| 9 | Escopo: changelogs antigos em PT/jargão não reescritos (§6, §9.5) | **OK** |
| 10 | `release/mods.json` intocado e desatualizado (§9.7) | **OK** |
| 11 | Texto público que viaja no ZIP: sobra alguma afirmação morta? | **ACHADO A1** |
| 12 | Precisão do documento de evidência | **ACHADO A2** (leve) |
| 13 | Fonte citada do vermelho do `check_segredos` | **ACHADO A3** (leve, explicado) |

Nenhum item ficou **INDETERMINADO**. Ressalva única, declarada: a *atribuição* de autoria arquivo a arquivo
não é provável a partir da árvore (outras frentes escrevem nela ao mesmo tempo) — o que **é** provável, e foi
provado, é que existe exatamente 1 arquivo modificado por mod, 5 por pasta, 15 no total, e que o `.cs` de
nenhum deles mudou além do literal de versão (§4.2).

---

## 2. Itens 1–3 — versões, hashes e o pacote

**Versão no ar (API por pacote, medida agora):** `BetterFont 1.0.2` · `BetterStats 1.0.1` (descrição **em
português**) · `BetterCombatText 0.1.1` (com "not yet verified in game"). Os três alvos — **1.0.3 / 1.0.2 /
0.1.2** — estão inéditos, então o bump é válido (versão publicada é imutável).

**Hashes dos ZIP novos** (remedidos, batem com o §2 do autor):

| | BetterFont 1.0.3 | BetterStats 1.0.2 | BetterCombatText 0.1.2 |
|---|---|---|---|
| sha256 | `bc1de51e…e5ea4e73` | `fa26dd0c…9fa4d45f8` | `9b216b88…4a47117d4` |
| bytes | 113920 | 100632 | 157085 |

**Hashes dos ZIP publicados** (baixados de `thunderstore.io/package/download/…`): `b284fabf…e9ecdf`,
`3470dcd4…dc967c`, `bb5bb64d…533d11` — os prefixos/sufixos do documento conferem.

**Layout:** os três ZIPs têm exatamente 5 arquivos, na raiz `manifest.json` + `README.md` + `CHANGELOG.md` +
`icon.png`, mais `plugins/<Mod>/<Mod>.dll` (lido do ZIP, não do disco). `manifest.name` == nome da pasta.
Ícones lidos do cabeçalho PNG: **256×256** (87821 / 91250 / 124954 bytes — iguais aos do documento).
`description` medido: **212 / 178 / 191** caracteres (≤ 250). **`README.md` e `CHANGELOG.md` dentro do ZIP são
byte-idênticos aos da árvore** nos três (`cmp`), e a DLL do ZIP é **byte-idêntica** ao
`<Mod>/bin/Release/netstandard2.1/<Mod>.dll` (`811428ae…`, `e45dc9d7…`, `d3fc0c1b…`).

---

## 3. Itens 6–10 — a reconciliação e as decisões

**Melhor que o `git diff`:** a comparação foi feita contra os **ZIPs no ar**.

- **BetterFont** — `manifest` e `CHANGELOG` diferem da árvore **só pelo bump**; o `README` publicado ensina,
  às linhas 105–108, que "sem a flag o alvo `DeployToBepInEx` também copia a DLL para o perfil" — falso desde
  DEPLOY-2. **Confirmado no artefato publicado**, e corrigido no texto novo.
- **BetterStats** — diverge nos três, como o autor diz: `description` publicada **em português** (lida do
  `manifest.json` do ZIP no ar); `README` publicado **em português com "Versão: 1.0.0"**; e a `1.0.1`/`1.0.0`
  do `CHANGELOG` com exatamente **3** correções de tempo verbal (linha 10 "está"→"estava"; o título da
  subseção; e o bullet "A versão **não** subiu … corrigido antes de qualquer download"). Árvore tem
  `## Português (BR)` no fim do README — a frase do changelog ("a short Portuguese summary stays at the end
  of the README") é verdadeira.
- **BetterCombatText** — o defeito de conteúdo é **real e foi conferido no fonte**: `Configuracao.cs:117-130`
  passa ao nome do inimigo `largura 0.22`, `suavidade 0.05`, `alfa 0.95`, sombra `0.35/-0.35`, `suavidade
  0.05`, `alfaSombra 0.75`, `fundo "escuro"`; `:132-144` (rótulos) trazem `alfa 0.10` — é **o 10%**; `:150-163`
  (dado) trazem `alfa 0.35` e `suavidade 0.60`. A tabela nova do README e a seção de configuração dizem
  exatamente isso.

**Aviso mantido (item 7):** `t_540bcf8e` e `t_e57fe3bf` estão **arquivados, sem `result`**, com a CONDIÇÃO 1
("o dono confirma em combate") aberta; a REV-52 (`t_116521c4`) declara a premissa "o BetterCombatText **NÃO
tem efeito visual confirmado**"; o `release/mods.json` traz, escrito por agente, "Revisado pelo dono em jogo".
O aviso está nos dois lugares onde o autor diz: `manifest.description` **e** `README.md` (linhas 33–36 em
inglês, 128 em português). Manter o aviso é a decisão **correta** — remover seria atribuir aceite a agente.

**Dependências (item 8):** o BCT segue apontando `DefRuivo_StolenRealmMods-BetterFont-1.0.2`, que **está no
ar** — sem restrição de ordem. Além do `--local` do autor, rodei o `check_dependencias.py --api` (fonte
fresca): **exit 0**, 7/7 referências resolvem.

**Escopo e ledger (itens 9–10):** a decisão de escopo citada como "DOC-4" existe e é literal — `t_dccb3f9e`
registra "FORA DE ESCOPO (decisao do dono): a secao em portugues nos READMEs, a ordem da pagina e o 'Build
from source'" e "reescrever 6 changelogs tecnicos e decisao de escopo". E o `release/mods.json` diz
`BetterCombatText.versao_publicada = "0.1.0"` com **0.1.1 no ar** (conferido: os outros dois batem).

---

## 4. Item 4 — "só muda o literal de versão": a prova foi elevada

O autor declarou honestamente o limite do método dele ("compara literais, não IL"). Refiz a pergunta por três
caminhos independentes, e os três fecham.

**4.1 Publicado × novo, por decompilação (prova nova).** Decompilei a DLL **extraída do ZIP publicado** e a
**extraída do ZIP novo** (`ilspycmd` de arquivo inteiro) e diffei os `.cs`. Em BetterFont (206 literais),
BetterStats (39) e BetterCombatText (270) a única diferença é a string de versão: atributos de assembly,
`[BepInPlugin(...)]`, `const Versao` e a linha de log que a interpola. **Todo o resto do código é idêntico.**

**4.2 Tamanho e literais.** Tamanhos iguais (34816 / 10752 / 50176) e conjuntos de literais UTF-16LE de mesmo
tamanho, diferindo só nos literais de versão — reproduzi com limiar de 4 caracteres, que devolve exatamente
os números do documento (**206/206, 39/39, 259/259**; a contagem depende do limiar: com 3 dá 212/270).

**4.3 A árvore reproduz o pacote (prova nova).** Copiei `Directory.Build.props`, `lib/` e as três pastas de mod
para **fora do repositório** e construí lá com `-c Release -p:DeployToBepInEx=false` (0 erro nos três). O
decompilado da build isolada é **idêntico** ao da DLL do ZIP; as diferenças de bytes são só a **caminho do
PDB embutido** no diretório de debug (e, no BetterStats, +512 bytes porque o caminho maior cruzou o
alinhamento de seção). Ou seja: a DLL empacotada **é** a build desta fonte — não há build velha escondida.

> Fecha a limitação que o autor declarou: o que entra no pacote é exatamente o que a árvore de hoje produz, e
> a única diferença para o que está no ar é o número da versão.

Uma checagem negativa que vale registrar: **nenhum outro `.cs` desses três mods foi tocado** — o `git diff`
de `Plugin.cs` é uma linha de versão, e `Configuracao.cs`, `Patches.cs`, `TextStyler.cs`,
`DiagnosticoArranque.cs` (BCT) não aparecem no `git status`. É o que sustenta "sem mudança funcional".

---

## 5. Item 5 — gates

| Gate | Exit medido |
|---|---|
| `python tools/check_versoes.py` | **0** (6 mods, 4 lugares cada) |
| `python tools/check_deploy_optin.py` | **0** (7 alvos com `Condition=… == 'true'`) |
| `python tools/check_dependencias.py --local` | **0** |
| `python tools/check_dependencias.py --api` (extra, fonte fresca) | **0** |
| `python tools/pack-thunderstore.py --config Release --so-conferir …` | **0** |
| `python tools/check_segredos.py` | **1** (vermelho — ver A3) |

O `--so-conferir` foi rodado (read-only); **não** rodei o empacotador de verdade, para não regravar os ZIPs
que são o objeto desta revisão.

---

## 6. Achados

### A1 (material, conserto barato) — sobrou o defeito corrigido, no mesmo arquivo, em português

`BetterCombatText/README.md:117`, **dentro do pacote 0.1.2**:

> Deixa o **texto de combate** mais legível: um **contorno/halo** (padrão **preto a 10%**)
> nos nomes de inimigos e nos rótulos de buff/debuff, mais o **texto do dado** nos eventos de rolagem.

É **exatamente** a afirmação que esta versão conserta no corpo em inglês do mesmo arquivo (o nome do inimigo
recebe contorno **preto duro e opaco a 95%**, 0.22/0.05; o 10% é o rótulo; o dado é 35%). O README do ZIP é
byte-idêntico ao da árvore — então a frase viaja **congelada** numa versão imutável, na página pública em
português que o DOC-4 decidiu manter.

- **Não é mentira do documento de preparação:** o §4 dele afirma só que "a tabela de superfícies e a seção de
  configuração passaram a dizer os defaults reais" — e isso é verdade. É uma correção **incompleta**, não uma
  afirmação falsa.
- **Por que entra no veredito mesmo assim:** a regra do próprio projeto (varredura de arquivo que entra no
  pacote) e a premissa da DOC-4 ("a página foi limpa e o arquivo que o usuário baixa continua com texto
  velho") tratam afirmação morta em arquivo publicado como defeito da mesma família de código velho.
- **Conserto:** uma linha, e **não custa versão nova** se for feito **antes do aceite** — os assets só são
  consumidos depois do gate humano, então repackar e trocar o asset na mesma Release tag é permitido. Se o
  dono preferir, o certo é **declarar a pendência** no checklist do §9 (hoje o item 5 cobre só changelog
  antigo em PT/jargão, não as seções em português dos READMEs).

### A2 (leve) — precisão do documento de evidência

- §8: "Estado da árvore ao fim: **exatamente 15 arquivos tocados**". Verdadeiro **para as três pastas de mod**
  (contei 15, 5 por mod, e a lista bate com o `changed_files` do autor) — mas o `git status --short` da árvore
  tem **176 linhas** (82 ` M`) por causa de outras frentes rodando em paralelo. Como está escrito, quem lê
  pode concluir que a árvore está limpa fora desta tarefa.
- §4: o README do BetterStats "124 linhas de diferença" é o `diff | wc -l` (inclui cabeçalhos/separadores); as
  linhas efetivamente trocadas são **88**. Cosnético.

### A3 (leve, explicado) — o número do `check_segredos` no documento estava certo quando foi medido

O §8 lista **3** achados (URL em `docs/automacao/AUT-3FR-revisao.md:37`; PEM em
`tools/automacao/offline/testes/t_aut3f2_achados.py:237,245`). O script de hoje reporta **6** — somam-se 3
acertos de **entropia** em fixtures (`t_aut3_segredos.py:32,81` e `t_aut3f2_achados.py:44`).

Isso **não** é erro do autor: `tools/check_segredos.py` foi **modificado por outra frente às 03:28:37**, isto
é, ~4 min **depois** de a preparação fechar (03:24:57). Rodei a versão de `HEAD` (a que o autor viu) e ela
devolve **exatamente os 3 achados** listados. Todos os 6 são pré-existentes: os três arquivos estão
**inalterados** na árvore (`git status` vazio para eles), logo o conteúdo é o de `HEAD`. A conclusão do autor
— vermelho pré-existente, fora do escopo, **não commitar/CI até resolver** — se sustenta integralmente.

---

## 7. O que sobra para o dono (o gate `t_91b357f4`)

1. **A1** — decidir: corrigir a linha do `README.md` (PT) do BetterCombatText e **repackar antes do aceite**
   (grátis), ou registrar a pendência como deferida. Sem isso, o 0.1.2 sobe com a afirmação que ele existe
   para corrigir.
2. Ler e aprovar os textos novos dos três (§9 do documento do autor), inclusive a decisão sobre o aviso do
   BCT, que **fica**.
3. Ordem de envio: livre entre os três (a dependência do BCT aponta para uma versão **já publicada**).
4. `release/mods.json` desatualizado (`BCT = 0.1.0` vs 0.1.1 no ar) — é do REL-CI-01, não desta leva.
5. O vermelho pré-existente do `check_segredos` (A3) antes de qualquer CI de publicação.

> **Esta revisão não é aceite nem aprovação de publicação.** Os pacotes estão fiéis à fonte, com hash e
> conteúdo conferidos artefato × artefato; o que falta é decisão humana — e, no A1, uma decisão humana
> tomada **antes** do envio.

---

## 8. Reprodução (sem efeito colateral)

```bash
# versão no ar (fonte fresca)
curl -s -A hermes "https://thunderstore.io/api/experimental/package/DefRuivo_StolenRealmMods/<Mod>/"
# ZIP publicado
curl -sL -o pub/<Mod>.zip "https://thunderstore.io/package/download/DefRuivo_StolenRealmMods/<Mod>/<versao>/"
sha256sum dist/gumatos-Better*-*.zip                       # confere §2
unzip -l dist/gumatos-<Mod>-<v>.zip                        # 5 arquivos, plugins/<Mod>/<Mod>.dll
cmp <zip>/README.md <Mod>/README.md                        # conteúdo igual à árvore
sha256sum <zip>/plugins/<Mod>/<Mod>.dll <Mod>/bin/Release/netstandard2.1/<Mod>.dll   # byte-idênticas
"$HOME/.dotnet/tools/ilspycmd" <dll-publicada> -o dec_pub/<Mod>
"$HOME/.dotnet/tools/ilspycmd" <dll-do-zip>    -o dec_zip/<Mod>
diff -r dec_pub/<Mod> dec_zip/<Mod>                        # só as strings de versão
python tools/check_versoes.py; python tools/check_deploy_optin.py
python tools/check_dependencias.py --local; python tools/check_dependencias.py --api
python tools/pack-thunderstore.py --config Release --so-conferir BetterFont BetterStats BetterCombatText
```

Nenhum desses comandos abre o jogo, instala no perfil ou toca a Thunderstore.
