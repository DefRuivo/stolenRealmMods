# DOCS-CI-1R — Revisão independente do conserto do índice de revisões em `docs/README.md`

Revisor ≠ autor, por execução. Cartão `t_f02e78be` (revisão independente) do pai `t_97df8c14`
(DOCS-CI-1). Trabalho 100% local de leitura/medição: **não** publiquei, instalei, buildei mod,
abri o jogo ou commitei. Nenhum `git add` de diretório/`-A`. Nenhum token/PAT em arquivo, log
ou resumo. Repo medido: `C:/dev/stolen-realm`.

Data da medição: 06/10/2026. Cabeça do git no momento: `34f929a` (`git log -1`).

---

## 0. Verdito global

**APROVADO.** Os 6 itens do cartão fecham: o índice de `docs/cobertura/revisao/` bate item a
item com a pasta (53), a trava (`tools/audita_docs.py`) está **byte-idêntica** ao versionado e
continua estrita (contra-prova vermelho/verde), e o parágrafo § Publicar não afirma mais
recência. Fica **1 ressalva de dono** (não bloqueio): os 5 relatórios novos estão UNTRACKED —
têm de entrar no commit junto do `docs/README.md`, senão o CI em checkout reprova no sentido
inverso.

---

## 1. Medição do zero (índice x pasta) — **OK**

Comandos:

```
$ ls docs/cobertura/revisao/*.md | wc -l
53
$ git ls-files docs/cobertura/revisao/ | grep -c '\.md$'
48
```

O auditor, na seção 3b, deu:

```
== 3b) docs/README.md x docs/cobertura/revisao ==
   pasta: 53 relatorios .md | titulo declara 53 | tabela lista 53
```

Contagem independente da tabela (linhas 85..89 de `docs/README.md`), parseando cada célula de
nomes e o `Nº` declarado por linha (`scratch/docci1r_mede.py`):

```
== linhas 85..89 ==
  '**Fichas por árvore** (texto × código, uma por árvore) | `'   declara=13 nomes_na_celula=13
  '**RV-8b** (auditoria de skills) | `RV-8b-0f-propriedades`,'   declara=5  nomes_na_celula=5
  '**RV-9** (buffs/debuffs/status) | `RV-9-censo`, `RV-9-buff'   declara=14 nomes_na_celula=14
  '**Relatórios de caso e de fechamento** | `ANTES-E-DEPOIS.m'   declara=16 nomes_na_celula=17
  '**Revisões independentes** (revisor ≠ autor; `RSTV-27R-bod'   declara=5  nomes_na_celula=5
soma declarada: 53
total nomes citados na tabela: 54
arquivos .md na pasta: 53

== citados na tabela mas AUSENTES na pasta ==
  AUSENTE: tools/review_ledger.py.md
== na pasta mas NAO citados na tabela ==
  (vazio)

== titulo (linha 75) ==
  ### `cobertura/revisao/` — 53 relatórios de revisão
```

O único "extra" (`tools/review_ledger.py`) é **prosa** da célula de descrição (o livro
`ANTES-E-DEPOIS.md` é gerado por essa ferramenta), não um nome de relatório — falso positivo do
meu parser, não do índice. Somadas as linhas: 13+5+14+16+5 = **53** = título = pasta. Cada um
dos 53 arquivos da pasta está citado; nenhum citado está ausente. `git status --short
docs/cobertura/revisao/` confirma os 5 nomes que entraram (ver §6).

Índice da pasta (53 nomes, extraído do disco para bater item a item): fichas-13 (`ficha-basic`,
`ficha-chaos`, `ficha-cold`, `ficha-fire`, `ficha-innate`, `ficha-light`, `ficha-lightning`,
`ficha-monk`, `ficha-nature`, `ficha-ranger`, `ficha-shadow`, `ficha-thief`, `ficha-warrior`);
RV-8b-5; RV-9-14 (`RV-9-censo`, `RV-9-buffs`, `RV-9-buffs-1..6`, `RV-9-debuffs`,
`RV-9-debuffs-1..4`, `RV-9-numeros`); caso/fechamento-16; revisões independentes-5.

---

## 2. A trava não foi afrouxada — **OK**

```
$ sha256sum docs/README.md
4ba2d13fc6581392013f777d775115b17fbb2508b54fffe5b73107e1b18c7054 *docs/README.md
$ sha256sum tools/audita_docs.py
731539a9a6a99c12ededbe001be2acbcc7f071dddd9dd22cec9075ab723b030f *tools/audita_docs.py
$ git status --short tools/audita_docs.py
(vazio)
$ git diff HEAD -- tools/audita_docs.py
(vazio)
```

`tools/audita_docs.py` **confere byte a byte** com o versionado: nem linha modificada nem
untracked. O critério continua o mesmo: procurei no próprio script — seção `3b` mantém a
checagem `total do título` **e** `Nº` de cada linha **e** `todo nome citado existe` **e** `todo
.md da pasta está citado` (`tools/audita_docs.py:177-242`). A contra-prova (§3) prova por
execução que o critério segue **estrito** (não afrouxado). Se o autor tivesse "consertado"
afrouxando o auditor, o diff/`git status` acima estaria sujo — está limpo.

O `sha256` do `docs/README.md` bate com o registrado pelo pai (4ba2d13…).

---

## 3. Contra-prova em execução (vermelho → verde) — **OK**

Método: backup byte a byte de `docs/README.md` em `scratch/`, plantei a REMOÇÃO de
`RSTV-29R-revisao.md` do índice (mantendo o `Nº` da linha = 5), rodei o auditor, restaurei do
backup e conferi o `sha256` de volta. Repo restaurado ao mesmo sha.

**VERMELHO (nome removido do índice):**

```
$ python tools/audita_docs.py
== 3b) docs/README.md x docs/cobertura/revisao ==
   VER linha diz 5 e lista 4 nome(s): | **Revisões independentes** (revisor ≠ autor; `RSTV-27R-body` é o cor
   pasta: 53 relatorios .md | titulo declara 53 | tabela lista 52
   VER esta na pasta e nao esta no indice: RSTV-29R-revisao.md
...
!! 2 PENDENCIAS:
   - docs/README.md: a tabela de docs/cobertura/revisao diz 5 em uma linha que lista 4 nome(s)
   - docs/README.md: o relatorio docs/cobertura/revisao/RSTV-29R-revisao.md nao esta listado no indice
EXIT=1
```

**VERDE (restaurado do backup):**

```
$ sha256sum docs/README.md
4ba2d13fc6581392013f777d775115b17fbb2508b54fffe5b73107e1b18c7054 *docs/README.md
$ python tools/audita_docs.py
   pasta: 53 relatorios .md | titulo declara 53 | tabela lista 53
== nenhuma inconsistencia encontrada ==
EXIT=0
```

Saídas completas gravadas em `scratch/docci1r_contraprova_vermelho.txt` (EXIT=1) e
`scratch/docci1r_contraprova_verde.txt` (EXIT=0). A trava **reprova de verdade** — não é exit 0
por vacuidade.

---

## 4. Parágrafo datado § Publicar — **OK**

O texto antigo afirmava recência (`hoje com **6** entradas … publicadas na leva de 01/10/2026`
e a lista de versões aparentando ser a corrente). O texto no disco agora diz:

> … (**6** entradas, todas com `publicar: true`); a **leva de 01/10/2026** é que subiu BetterFont
> **1.0.1**, … e BetterCombatText **0.1.0** — são as versões **daquela leva**, não as correntes
> (a versão publicada corrente de cada mod é o `versao_publicada` do próprio `release/mods.json`); …

Não há mais "hoje" nem implicação de que essas sejam as versões correntes — a atribuição é
datada e o texto remete ao `versao_publicada` como fonte do corrente. **Robustecido.** (O
"6 entradas" continua verdadeiro: o gate `release/mods.json` tem 6; e o "6 mods" é o número do
projeto, não uma contagem de relatórios.)

---

## 5. Varredura de mentira residual (contagem 48) — **OK**

```
$ grep -rn "48 relatóri\|48 relator\|48 .md\|48 revis\|48 reports" --include=*.md .
./docs/automacao/CIC-4R3-revisao.md:345:   - docs/README.md: o titulo de docs/cobertura/revisao diz 48 relatorios, a pasta tem 51
$ grep -n "48" docs/README.md
(vazio — nenhuma ocorrência)
```

A única menção a "48" é **histórica**: está dentro de um bloco de saída literal citado por um
parecer de revisão anterior (`CIC-4R3`), registrando o estado **de então** (48 com 51 na pasta).
Não é uma declaração corrente do índice, e `docs/automacao/` é **untracked** (não vai ao CI).
O arquivo corrigido (`docs/README.md`) não contém mais "48" em nenhum lugar.

---

## 6. Ressalva de dono — os 5 relatórios estão UNTRACKED (não é bloqueio do cartão) — registrado com prova

```
$ git ls-files docs/cobertura/revisao/ | grep -c '\.md$'
48
$ ls docs/cobertura/revisao/*.md | wc -l
53
$ git status --short docs/cobertura/revisao/
 M docs/cobertura/revisao/ANTES-E-DEPOIS.md
 M docs/cobertura/revisao/CHK-1-shrines-conferencia-mecanica.md
 M docs/cobertura/revisao/RV-19-shrines.md
 M docs/cobertura/revisao/RV-35-40-shrines-conferencia.md
 M docs/cobertura/revisao/RV-9-censo.md
?? docs/cobertura/revisao/RSTV-26R-revisao.md
?? docs/cobertura/revisao/RSTV-27R-body.md
?? docs/cobertura/revisao/RSTV-27R-revisao.md
?? docs/cobertura/revisao/RSTV-28R-revisao.md
?? docs/cobertura/revisao/RSTV-29R-revisao.md
```

O fix é **correto e coerente com o disco**, mas num checkout do CI só existe o versionado (48).
Se `docs/README.md` (declarando 53) for commitado **sem** os 5 arquivos `??`, o CI acusa o
inverso (53 declarados x 48 na pasta). O commit precisa levar os 5 relatórios **junto** com o
`docs/README.md`. É aviso ao dono — não invalida o conserto.

Confirmei também que o portão existe no CI:

```
$ grep -n "audita_docs" .github/workflows/validate.yml
187:      - name: "10. Auditoria dos docs (tools/audita_docs.py)"
189:          if [ -f tools/audita_docs.py ]; then
190:            python tools/audita_docs.py
```

(o cartão diz "passo 7"; no YAML a etapa aparece numerada como "10." — mesmo passo do auditor
`tools/audita_docs.py`. Não é divergência de conteúdo, só de rótulo de numeração.)

---

## 7. Limites do que NÃO verifiquei (INDETERMINADO)

- **INDETERMINADO — outras afirmações envelhecidas fora do § Publicar.** O cartão pediu o §
  Publicar; varri o arquivo em busca da contagem "48" (§5) e nada. Não fiz auditoria semântica
  de *toda* afirmação datada do arquivo (ex.: a nota de rodapé §8 cita "verificado em 30/09/2026").
  São medições datadas explícitas, não recência disfarçada, mas não as reavaliei uma a uma.
- **INDETERMINADO — o diff `docs/README.md` vs HEAD inclui mudanças de outros cartões**
  (DEPLOY-2 nos passos 0/6/8, linha do RSTV-30). Elas **não** fazem parte do DOCS-CI-1: o diff
  do autor (`t_97df8c14/prova/docs-README.diff`) tem só as 3 mudanças do fix. Não revisei o
  mérito dessas outras mudanças — estão fora do escopo deste cartão.

---

## 8. Verdito por item

| # | Item | Veredito |
|---|------|----------|
| 1 | Medição do zero (índice x pasta = 53, item a item) | **OK** |
| 2 | Trava não afrouxada (`audita_docs.py` byte-idêntico) | **OK** |
| 3 | Contra-prova em execução (vermelho EXIT=1 / verde EXIT=0, repo restaurado) | **OK** |
| 4 | Parágrafo datado § Publicar sem afirmar recência | **OK** |
| 5 | Varredura de "48" residual | **OK** (só menção histórica em doc untracked) |
| 6 | Registrar o não-verificado | **OK** (§7) |

**Verdito global: APROVADO** — auditor fecha EXIT=0 de verdade, sem afrouxar a trava. Ressalva
de dono registrada no §6 (commit tem de levar os 5 relatórios untracked junto do `docs/README.md`).
