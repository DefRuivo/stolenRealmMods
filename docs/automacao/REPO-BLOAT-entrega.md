# REPO-BLOAT-1 — conteúdo superseded fora do índice: proposta e pacote de decisão

Cartão `t_e8beca3f` (frente REPO-BLOAT). **Status: PROPOSTA — nada foi desindexado.**

Este documento existe para o dono decidir. A desindexação (§5) só roda depois de a autorização
**nominal** dele estar registrada em comentário no cartão; a política ORG-R2 gravada no próprio
`.gitignore` (linhas ~95-110) diz, verbatim, que "a lista aprovada de remoções do índice é VAZIA",
então o padrão é NÃO desindexar até ele dizer o contrário, com escopo citado.

- Base medida: `HEAD = 3643155` (`main`), 16/10/2026 15:12 (-03:00).
- Contexto da medição: no mesmo horário a árvore tinha **73 arquivos modificados por outra frente**
  (REPO-PRIV-1, substituição de caminho de perfil por `%USERPROFILE%` em `docs/`). Por isso as
  contagens canônicas abaixo vêm do **índice** (`git ls-files` + `git cat-file`), não do worktree,
  e nenhum arquivo daquela frente foi tocado, revertido ou commitado aqui.

---

## 0. Números de base

| Medida | Valor |
| --- | --- |
| Arquivos rastreados no HEAD | **1.929** |
| Soma dos blobs do HEAD (tamanho lógico) | **97.993.023 B = 93,45 MB** |
| Checkout no disco (worktree, com CRLF) | 94,05 MB |
| Clone Windows (`core.autocrlf=true`) | checkout ~100 MB + `.git` 67 MB |
| `.git` / pack | 67 MB / 65,8 MB |
| `git ls-files -ci --exclude-standard` | **VAZIO** (invariante ORG-R2 preservado) |

O corpo do cartão cita 87,9 MB / 1.797 arquivos (medição mais cedo do mesmo dia); o repositório
cresceu para 94,05 MB / 1.929 com os relatórios das frentes de 16/10. As duas medições estão certas
em suas datas — a de referência para a decisão é a de cima.

Topo por diretório (blobs do HEAD):

| Área | MB | arq |
| --- | --- | --- |
| `docs/cobertura/EV-R1` | 23,84 | 29 |
| `BetterPortuguese/` | 13,73 | 22 |
| `docs/automacao/AUT-4-evidencias` | 12,57 | 24 |
| `docs/automacao/COR-AUT7-F2-evidencias` | 8,56 | 149 |
| `docs/automacao/COR-AUT7-evidencias` | 7,74 | 79 |
| `tools/` | 5,57 | 548 |
| `docs/img/` | 4,85 | 3 |
| (resto: relatórios, `api/`, mods, `docs/cobertura/revisao`) | ~17 | ~850 |

---

## 1. Achado central: os sete arquivos sem `-v2` (v1) do EV-R1 estão superseded — **com prova**

### 1.1 Tabela

| caminho (a desindexar) | tamanho | superseded por | prova | ação |
| --- | ---: | --- | --- | --- |
| `docs/cobertura/EV-R1/revisao-por-evento.md` | 1.924.497 B | `revisao-por-evento-v2.md` (1.853.674 B) | P1 + P2 + P3 | desindexar |
| `docs/cobertura/EV-R1/lote-Normal.md` | 1.342.507 B | `lote-Normal-v2.md` (1.292.757 B) | P1 + P2 + P4 | desindexar |
| `docs/cobertura/EV-R1/lote-NotInEventPool.md` | 534.297 B | `lote-NotInEventPool-v2.md` (514.868 B) | P1 + P2 + P4 | desindexar |
| `docs/cobertura/EV-R1/lote-SemPoolDeclarado.md` | 40.648 B | `lote-SemPoolDeclarado-v2.md` (39.292 B) | P1 + P2 + P4 | desindexar |
| `docs/cobertura/EV-R1/indice.md` | 28.348 B | `indice-v2.md` (28.355 B) | P1 + P2 + P3 + P5 | desindexar |
| `docs/cobertura/EV-R1/lote-QuestStart.md` | 4.961 B | `lote-QuestStart-v2.md` (4.953 B) | P1 + P2 + P4 | desindexar |
| `docs/cobertura/EV-R1/lote-AfterBattle.md` | 1.899 B | `lote-AfterBattle-v2.md` (1.891 B) | P1 + P2 + P4 | desindexar |
| **total** | **3.877.157 B = 3,70 MB** | | | |

Todos os tamanhos são **tamanho de blob no índice** (`git cat-file -s :<caminho>`). No disco o v1 é
alguns bytes maior porque está em CRLF (ex.: `indice.md` 28.632 B no disco x 28.348 B no blob).

### 1.2 As provas

**P1 — o v2 é superconjunto byte a byte do v1 (não é "mesmo nome, conteúdo diferente").**
Normalizando o CR (que é exatamente o defeito declarado), o corpo dos dois é **idêntico caractere a
caractere**; a única diferença é a linha de título H1 (e, no índice, o cabeçalho de 3 linhas e os 5
ponteiros internos — ver P5). Reprodução:

```
cd docs/cobertura/EV-R1
for p in indice revisao-por-evento lote-Normal lote-NotInEventPool \
         lote-SemPoolDeclarado lote-AfterBattle lote-QuestStart; do
  echo "== $p =="
  diff -u <(tr -d '\r' < "$p.md") <(tr -d '\r' < "$p-v2.md") | head -20
done
```

Resultado literal: os cinco lotes e a revisão integral dão **8 linhas de diff** — todas a linha 1
(`# EV-R1 — Normal (160 eventos)` x `# EV-R1 — Normal (160)`); o índice dá 51 linhas, todas no
cabeçalho/ponteiros.

**Contagem de CR, que fecha a prova de que a única diferença é a tradução de CR/LF** (medida por
`tr -dc '\r' < arq | wc -c` e `tr -dc '\n' < arq | wc -c`):

| arquivo | v1 CR | v1 LF | CR-LF | v2 CR | CR de conteúdo |
| --- | ---: | ---: | ---: | ---: | --- |
| `indice.md` | 284 | 284 | 0 | 0 | iguais |
| `lote-Normal.md` | 49.790 | 49.742 | **48** | **48** | iguais |
| `lote-NotInEventPool.md` | 19.456 | 19.421 | **35** | **35** | iguais |
| `lote-SemPoolDeclarado.md` | 1.356 | 1.348 | **8** | **8** | iguais |
| `lote-AfterBattle.md` | 100 | 100 | 0 | 0 | iguais |
| `lote-QuestStart.md` | 217 | 217 | 0 | 0 | iguais |
| `revisao-por-evento.md` | 70.923 | 70.832 | **91** | **91** | iguais |

Leitura: o v1 tem CR em **100% das linhas** (CR ≥ LF em todos os sete) mais os CRs que fazem parte do
próprio conteúdo; o v2 tem o mesmo número exato de CRs de conteúdo (0, 48, 35, 8, 0, 0, 91) e nenhum
CR de fim de linha. Ou seja, o v2 é o v1 **menos o CRLF** — nada mais.

**P2 — o repositório já declara, por escrito, que o v1 é histórico e que o v2 é o vivo.**
`docs/cobertura/EV-R1/ENTREGA-E-LOCALIZACAO.md:24-25`, verbatim:

> Os Markdown sem sufixo `-v2` são a primeira renderização, **preservados como histórico**; a primeira
> gravação sofreu tradução automática de nova linha no Windows. **Prefira os `-v2`.** Nenhum string de
> dados foi reescrito.

**P3 — os documentos vivos só apontam para o v2.** `docs/cobertura/EV-R1/LEIA-ME.md:7`
("Comece em `docs/cobertura/EV-R1/indice-v2.md`. Para leitura contínua: `revisao-por-evento-v2.md`").

**P4 — o v2 se declara a correção do v1.** `indice-v2.md:7`: "Revisão v2 corrige apenas a tradução
automática CR/LF do gravador Markdown no Windows. Os strings de `eventos.json` e os textos autorais
não foram alterados."

**P5 — os ponteiros internos do v2 apontam para os arquivos `-v2`.**
`indice-v2.md:10,15,179,267,272` citam `lote-*-v2.md`; o `indice.md` (v1) apontava para os v1.

### 1.3 Verificação da exigência do cartão: "se algum v1 tiver informação que o v2 NÃO tem, ele não entra"

Nenhum tem. Como os corpos são idênticos após normalizar o CR (P1), **não existe** string de dado,
tabela, GUID, SHA de objeto, opção, ação ou recompensa presente no v1 e ausente no v2. A única
informação exclusiva do v1 é o próprio CR (o defeito) e a palavra "eventos" no título
("(160 eventos)" x "(160)"). A direção do conjunto é v1 ⊂ v2.

### 1.4 Quem cita os v1 (e o que acontece se saírem do índice)

| documento | linha | o que muda |
| --- | --- | --- |
| `docs/cobertura/EV-R1/ENTREGA-E-LOCALIZACAO.md` | 16-17, 24-25 | doc **vivo**: lista `indice.md` / `indice-v2.md` e `revisao-por-evento.md` / `-v2.md` como pares e explica que o v1 é histórico. Num clone sem os v1, a linha 16-17 fica falsa. → **decisão do dono (§4.3)** |
| `docs/automacao/ORG-R0-parte01.md` | 77-80 | relatório de **medição histórica** (tabela dos maiores arquivos do repo na data). Continua verdadeiro como registro do que foi medido; não é ponteiro. Sem ação. |
| `docs/cobertura/EV-R1/indice.md` | 10,15,179,267,272 | o próprio v1 apontando para os v1. Sai junto. |

Nenhum `tools/`, `api/`, `.github/`, mod ou manifesto referencia os v1.

---

## 2. Varredura ampliada (padrões de duplicata/supersessão no índice)

Padrões procurados: `-final`, `-v2`, `-v3`, `revisao-final`, `-antigo`, `-old`, `revisado`, `(copia)`,
`copia`, `-backup`, `_backup`, `-dup`. Busca por nome **e** por conteúdo (md5 de todos os 1.929
arquivos rastreados). Veredito:

| grupo | MB | veredito |
| --- | ---: | --- |
| `docs/cobertura/EV-R1/*-v2.md` + `indice-v2.md` (7 arq) | 3,70 (v1) + 3,69 (v2) | v1 = **candidato** (§1). Os `-v2` são os **vivos** — ficam. |
| `docs/automacao/KIT-{06F,07F,10,11,12,13,14}-*final*.md` (11 arq) | ~0,08 | **histórico legítimo**. Cada `-entrega-final*.md` é o relatório da rodada que fechou a frente; `KIT-10-entrega-final.md` diz explicitamente que *substitui* `KIT-10-entrega.md`, e `final2` substitui `final`. O valor é a trilha de auditoria ("os registros anteriores não foram alterados" é a convenção do projeto). **Não remover.** |
| `docs/automacao/LEVEL-{R2,R3F1}-evidencias/rodada-final-01.{json,txt}` (4 arq) | 0,07 | **duplicatas byte a byte** de `harness-results.{json,txt}` na mesma pasta (md5 idêntico). Ganho: 0,07 MB. Custo: mexer em evidência de rodada. **Não vale.** |
| `docs/automacao/schemas/*-v1.json`, `tools/automacao/kit13/scenario-v1.schema.json` (5 arq) | 0,01 | `-v1` é **nome de versão de schema**, não cópia de um v2. Não existe v2. **Fica.** |
| `docs/automacao/CIC-3R2-evidencias/*-antigo-atual.txt` (2 arq) | 0,03 | evidências de comparação antigo×atual de uma rodada. **Fica.** |
| `docs/automacao/EV-R2-FORAPOOL-b04-copia-verificada.json` | 0,003 | recibo de verificação: lista `path` + `sha256` + `bytes` dos 15 artefatos da entrega. **Fica** (é a prova da cópia, não uma cópia). |
| `docs/automacao/COR-AUT7-evidencias/*duplicate-same-reading*` (6 arq) | 2,5 | nome do **caso de teste** (leitura duplicada), não arquivo duplicado. **Fica.** |
| `tools/automacao/runtime/testes/contra-prova/cp_aut4rest_isca_backup_log_sem_registro.py` | 0,01 | **isca deliberada** (contra-prova que afirma o falso). Remover quebraria a suíte. **Fica.** |
| `docs/cobertura/revisao/REVISAR-AO-FINAL.md` | 0,01 | nome do marcador de revisão do dono, documento vivo. **Fica.** |
| `AUT-4-evidencias/r3-confirmada/02-final.png` | 2,5 | evidência de run (o "final" é o segundo print da rodada). Ver §3.2. |

Varredura por conteúdo (md5 de 1.929 arquivos): **19 grupos de arquivos byte a byte idênticos,
excedente total 331.493 B = 0,32 MB** — todos em `docs/automacao/*evidencias/` (a mesma suíte/observação
copiada em dois ou três diretórios de rodada: `suite-puros.json`, `suite-contra-prova.json`,
`E-E1-sem-suite-baseline.stdout`, `obs/bct-*.obs.json` etc.). São a mesma peça em rodadas diferentes;
desindexar quebraria a leitura de quem reconfere rodada por rodada, por 0,32 MB. **Não recomendo mexer.**

Outros dois achados de higiene (sem MB, mas ficam registrados):

- **66 arquivos de 0 byte**, quase todos `.stderr` em `docs/automacao/COR-AUT7*-evidencias/`. São
  evidência de "o passo não escreveu em stderr", proposital. **Não mexer.**
- Nenhum arquivo rastreado com nome `.bak`/`.orig`/`.tmp` (as regras defensivas do REPO-HIG estão
  funcionando).

---

## 3. Outras categorias: o que é fonte, o que é derivado, o que pode ser recomprimido

### 3.1 `docs/img/*-icon-fonte.png` — **FONTE: preservar** (não é candidato)

2 arquivos, 1254×1254 RGB, **5.087.987 B = 4,85 MB**:

| arquivo | bytes |
| --- | ---: |
| `docs/img/bettercombattext-icon-fonte.png` | 2.629.779 |
| `docs/img/roguelikedebugger-icon-fonte.png` | 2.458.208 |

- É **fonte declarada** e a decisão de guardar as duas versões está registrada pelo dono:
  `RoguelikeDebugger/CHANGELOG.md:36` — "A arte-fonte continua versionada em `docs/img/` — o
  repositório guarda as duas" (o derivado é o `icon.png` 256×256 que vai ao pacote). Também citado em
  `BetterCombatText/CHANGELOG.md:210` e `docs/cobertura/revisao/CHK-1-shrines-conferencia-mecanica.md:508`.
- O **derivado** são os 9 `icon.png` 256×256 fora de `docs/` (894.973 B = 0,85 MB) que os manifests
  referenciam e que precisam existir no pacote. Nada a fazer.
- **Recompressão medida (PIL 12.3, `optimize=True, compress_level=9`):** perda **zero** de pixel rende
  −3,1% e −2,1% (≈ 80 KB no par) — não justifica um commit que invalide o carimbo da arte. A via
  "PNG indexado 256 cores" rende −56,7% / −54,1% (**2,3 MB**), mas é **lossy**: destrói o gradiente e
  a suavidade do mestre e transformaria uma fonte de arte num arquivo degradado. **RECUSADO.**
- Correção de escopo: o cartão citava "docs/img 4,9 MB (3 arq)"; hoje são 2 PNG (4,85 MB) +
  `LEIA-ME.txt` (5.218 B, o guia de capturas pendentes do README).

### 3.2 Evidências PNG de run em `docs/automacao` — **PROVA: preservar byte a byte**

4 arquivos, 1920×1080 RGB, **10.520.644 B = 10,03 MB** (10,7% do repo):

| arquivo | bytes | recompressão lossless medida |
| --- | ---: | --- |
| `AUT-4-evidencias/r2-incompleto/01-ui.png` | 2.764.203 | −14,2% (2.316.400 B) |
| `AUT-4-evidencias/r3-confirmada/01-ui.png` | 2.506.147 | −17,3% (2.023.600 B) |
| `AUT-4-evidencias/r3-confirmada/02-final.png` | 2.506.159 | −17,3% (2.023.600 B) |
| `AUT-4-evidencias/r4-confirmada-log/01-ui.png` | 2.744.135 | −14,6% (2.289.800 B) |

- **Não são derivados descartáveis: são a prova visual da rodada.** O `sha256` e o `bytes` de cada um
  estão **cravados** no manifesto do instrumento (`AUT-4-evidencias/r3-confirmada/aut4probe.json`,
  campo `manifest.artefatos`), repetidos em `resultado-r{2,3,4}.json` e citados em `AUT-4-parte04.md`.
  Recomprimir muda o blob → invalida o carimbo → vira **reconferência de prova**, não limpeza.
- Se o dono **aceitar re-carimbar** (decisão dele, com reescrita das 3 referências por arquivo, é uma
  frente nova, não este cartão): a única via defensável é a **lossless**, −1,44 MB no conjunto, sem
  perder um pixel. A via indexada (−73% ≈ −7,7 MB) troca texto de UI por borrão e é **inadequada para
  evidência**. Recomendação: **não tocar**.
- O que **não** ajuda: mover para anexo de cartão tira do repo mas quebra os caminhos citados por
  **19 arquivos rastreados** (`AUT-4-parte0{2,3,4}.md`, `KIT-12*`, `INT-R1-C2*`, `ORG-PRE-SEG-parte01.md`,
  `ORG-R0-parte01.md`, `tools/automacao/kit12/*.py`).

### 3.3 `BetterPortuguese/` — 13,73 MB, **nada a desindexar** (é o produto)

`pt-BR.original.json` (4.701,8 KB), `pt-BR.corrigido.json` (4.701,8 KB) e `pendencias.json`
(4.474,2 KB) = 13,88 MB parecem "dados de trabalho", mas são **payload do mod**:
`BetterPortuguese.csproj:28` embute `Data\*.json` como `EmbeddedResource`, e `README.md:46` declara
"JSONs UTF-8 estritos são embutidos na DLL e **distribuídos como cópias auditáveis** em
`plugins/BetterPortuguese/Data/`. SHA-256 de cada recurso é fixado no código". Desindexar quebraria a
entrega auditável. **Fica.**

### 3.4 `tools/` — 5,57 MB em 548 arquivos, **sem alvo**

Maior arquivo: `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` com 106,8 KB. Não há arquivo
grande; o volume é instrumentação, fixtures e provas que o `release-check` usa. **Fica.**

---

## 4. Pacote de decisão

### 4.1 Lista exata a desindexar (7 caminhos, 3.877.157 B = **3,70 MB**)

```
docs/cobertura/EV-R1/indice.md
docs/cobertura/EV-R1/revisao-por-evento.md
docs/cobertura/EV-R1/lote-AfterBattle.md
docs/cobertura/EV-R1/lote-Normal.md
docs/cobertura/EV-R1/lote-NotInEventPool.md
docs/cobertura/EV-R1/lote-QuestStart.md
docs/cobertura/EV-R1/lote-SemPoolDeclarado.md
```

Nada do disco é apagado; nada do histórico é reescrito. Também **não** entram na lista (decisão
fundamentada em §2 e §3): os `docs/img/*-icon-fonte.png`, as 4 evidências PNG do AUT-4, os 11
`KIT-*-final*.md`, os 19 grupos de duplicatas exatas, os 66 arquivos vazios, `BetterPortuguese/Data`
e `tools/`.

### 4.2 O que muda para quem clona (medido, não estimado)

Piloto executado em clone descartável (`scratch/piloto-bloat`, commit `ce22b94`):

| | antes | depois |
| --- | ---: | ---: |
| Arquivos rastreados | 1.929 | **1.922** |
| Soma de blobs do HEAD | 93,45 MB | **89,75 MB** (−3,70 MB, −3,96%) |
| Checkout no disco (clone Windows, CRLF) | 100 MB | **96 MB** (−4 MB) |
| `.git` do clone | 67 MB | **67 MB (não encolhe)** |
| `git ls-files -ci --exclude-standard` | vazio | **vazio** (verificado no clone) |
| Arquivos v1 no disco de quem já tinha clone | presentes | presentes (nada é apagado) |
| Arquivos v1 no clone novo | presentes | **ausentes do checkout** (ficam no histórico) |

O `.git` não encolhe porque **não se reescreve histórico**: os blobs v1 continuam alcançáveis pelo
commit anterior. Medição direta do custo marginal: empacotando todos os objetos alcançáveis de HEAD
com e sem os 7 caminhos — **69.022.563 B → 68.637.499 B (−385.064 B, −0,56%)**, porque o v1 é
comprimido por delta contra o v2 (são quase iguais). Ou seja: o ganho real é de **checkout** e de
**clareza do índice**, não de tamanho do clone.

### 4.3 Dois efeitos colaterais que exigem decisão do dono

1. **`!docs/**/*.md` (`.gitignore:31`) re-inclui `docs/`.** Portanto desindexar sem regra de ignore
   não basta — o arquivo voltaria a ser rastreado no próximo `git add`. A regra de ignore tem de ser
   **nominal, um caminho por linha**, no padrão já usado em `.gitignore:164-165`
   (`/docs/cobertura/EV-R1/catalogo-referencias.json`).
2. **Regra de ignore SEM `git rm --cached` quebra o invariante ORG-R2.** Medido no contra-factual
   (`scratch/piloto-contrafactual`): só acrescentar as 7 linhas de ignore deixa
   `git ls-files -ci --exclude-standard` com **7 linhas** — exatamente o que a política do `.gitignore`
   existe para evitar. As duas mudanças têm de ir **no mesmo commit**. Com as duas, o invariante volta
   a zero (verificado).
3. **Pendência de documentation drift:** `ENTREGA-E-LOCALIZACAO.md:16-17` descreve o par
   `indice.md` / `indice-v2.md`. Num clone sem os v1 a frase fica falsa (§1.4). As travas deste cartão
   proíbem tocar em **doc vivo**, então eu **não** editei. Escolha do dono: (a) autorizar, no mesmo
   commit, o ajuste de 2 linhas (16-17 e 24-25) para citar só os `-v2` e registrar que os v1 saíram do
   índice; ou (b) deixar como está e aceitar que o doc descreve o histórico, não o clone.

---

## 5. Execução proposta — **só após a autorização nominal** (§7)

Passos, na ordem, com verificação em cada um:

```bash
# 1. Confirmar estado de partida
git ls-files -ci --exclude-standard          # tem de sair VAZIO
git ls-files | wc -l                          # 1929

# 2. Acrescentar ao .gitignore o bloco nominal (mesmo padrão das linhas 164-165)
cat >> .gitignore <<'EOF'

# ---------------------------------------------------------------------------
# REPO-BLOAT-1 (autorizado por <dono>, <data>): conteudo SUPERSEDED do EV-R1.
# Os 5 lotes e o indice tem par `-v2` que os substitui (corpo byte-identico;
# o v1 so' carrega o CR/LF do gravador no Windows). Os originais ficam no DISCO
# e no HISTORICO; saem apenas do indice. Regra NOMINAL: um caminho por linha.
# ---------------------------------------------------------------------------
/docs/cobertura/EV-R1/indice.md
/docs/cobertura/EV-R1/revisao-por-evento.md
/docs/cobertura/EV-R1/lote-AfterBattle.md
/docs/cobertura/EV-R1/lote-Normal.md
/docs/cobertura/EV-R1/lote-NotInEventPool.md
/docs/cobertura/EV-R1/lote-QuestStart.md
/docs/cobertura/EV-R1/lote-SemPoolDeclarado.md
EOF

# 3. Desindexar (PRESERVA o arquivo no disco)
git rm --cached docs/cobertura/EV-R1/indice.md \
                docs/cobertura/EV-R1/revisao-por-evento.md \
                docs/cobertura/EV-R1/lote-AfterBattle.md \
                docs/cobertura/EV-R1/lote-Normal.md \
                docs/cobertura/EV-R1/lote-NotInEventPool.md \
                docs/cobertura/EV-R1/lote-QuestStart.md \
                docs/cobertura/EV-R1/lote-SemPoolDeclarado.md

# 4. Commit unico (so' estes caminhos; a arvore tem trabalho de outra frente rodando)
git add .gitignore
git commit -m "REPO-BLOAT-1: desindexa os 7 markdown superseded do EV-R1 (v1; 3,70 MB)" \
  -- .gitignore docs/cobertura/EV-R1/indice.md docs/cobertura/EV-R1/revisao-por-evento.md \
     docs/cobertura/EV-R1/lote-AfterBattle.md docs/cobertura/EV-R1/lote-Normal.md \
     docs/cobertura/EV-R1/lote-NotInEventPool.md docs/cobertura/EV-R1/lote-QuestStart.md \
     docs/cobertura/EV-R1/lote-SemPoolDeclarado.md

# 5. Verificacao
git ls-files -ci --exclude-standard          # TEM de sair VAZIO
git ls-files | wc -l                          # 1922
ls -la docs/cobertura/EV-R1/*.md              # os 7 continuam no disco
git check-ignore -v docs/cobertura/EV-R1/indice.md
git status --porcelain                        # limpo (fora o trabalho da outra frente)
```

Sem push (trava do cartão).

### 5.1 Piloto já executado (o procedimento funciona — em clone descartável, não no repo)

`scratch/piloto-bloat` (clone local, commit `ce22b94`): 1.929 → 1.922 rastreados,
`git ls-files -ci --exclude-standard` = **0 linhas**, os 7 arquivos presentes no disco, `git status`
limpo, `git check-ignore -v` apontando as linhas novas do `.gitignore`.
`scratch/piloto-contrafactual`: só as linhas de ignore, **sem** `rm --cached` → `ls-files -ci` = **7**
(o motivo pelo qual as duas mudanças são um commit só).

Os clones do piloto são **descartáveis** (vivem no scratch do Hermes, que é podado por ociosidade; o do
contra-factual já foi apagado depois da medição). Eles **não** são pré-requisito da execução: os
números da §4.2 se reproduzem com os comandos da §5 num clone novo.

---

## 6. Invariante de verificação obrigatória

```
$ git ls-files -ci --exclude-standard
(VAZIO — 0 linhas, hoje e depois da execução)
```

Hoje: **vazio** (conferido em 16/10/2026 15:12). Depois da execução: **vazio** (conferido no piloto).
O estado tem de sobreviver ao commit; se aparecer qualquer linha, a regra de ignore está sem o
`rm --cached` correspondente e o commit deve ser desfeito antes de sair.

---

## 7. Travas respeitadas nesta rodada

- Nenhum `filter-branch` / `filter-repo` / reescrita de histórico.
- Nenhum arquivo apagado do disco (`git rm --cached` preserva; o piloto provou).
- Nenhuma fonte de mod, `manifest.json`, `CHANGELOG.md`, `package.py`, `api/` ou `tools/` tocada.
- Nenhuma exceção `!` do `.gitignore` alterada; nenhuma linha do `.gitignore` do repo alterada.
- Nenhum doc vivo editado (as 2 linhas de `ENTREGA-E-LOCALIZACAO.md` ficam como pergunta, §4.3).
- Sem push. O único arquivo gravado nesta rodada é este documento (e o commit dele).
- A árvore tinha 73 arquivos modificados por outra frente (REPO-PRIV-1) durante a medição; nada
  daquilo foi tocado, revertido ou incluído em commit.

## 8. O que eu preciso do dono (autorização nominal)

Para o cartão sair da fase de proposta, é preciso, **em comentário neste cartão**:

1. **A autorização, citando o escopo**: desindexar os **7 caminhos da §4.1** (3,70 MB), entendendo que
   `.git` não encolhe sem reescrever histórico (§4.2) — o ganho é de checkout e de clareza.
2. **A decisão da §4.3**: (a) incluir no mesmo commit o ajuste de 2 linhas do doc vivo
   `ENTREGA-E-LOCALIZACAO.md`, ou (b) deixá-lo como está.

Sem essas duas frases, o cartão para aqui: proposta pronta, pacote de decisão pronto, repositório
intacto.
