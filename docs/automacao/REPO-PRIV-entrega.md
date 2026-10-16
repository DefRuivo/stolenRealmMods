# REPO-PRIV-1 - vazamento do caminho do perfil do dono nos arquivos rastreados: entrega

Cartao `t_f571f9c0`. Objetivo: tratar (nao esconder) o vazamento de identidade do dono
no repositorio PUBLICO, separando por CLASSE - documento vivo pode normalizar; ferramenta
precisa de resolucao em tempo de execucao; evidencia congelada NAO pode ser reescrita.

Esta e' a **rodada 3**: fecha o achado **B7** da revisao da rodada 2 - a prova de
nao-regressao do gate de docs aqui nesta pagina nao reproduzia no estado ENTREGUE - e o nit
de durabilidade. O que mudou esta na secao 0.1; o corpo abaixo ja' e' o estado corrigido.
(A rodada 2 tinha fechado os 6 achados B1-B6 da rodada 1.)

## 0. Resumo

### 0.1 O que as rodadas 2 e 3 mudaram (achados B1-B7 da revisao)

| achado | o que era | o que ficou |
|---|---|---|
| **B1** bloqueante | `docs/automacao/LANG-C4-REVISAO-DONO.md` foi normalizado como (a), mas o sha256 dele esta registrado em `LANG-C4-REVISAO-DONO-verificacao.json`; a normalizacao quebrou o auto-teste (`test_13`) do `tools/preparar_revisao_dono.py` (`Ran 13 tests ... FAILED`) | documento **revertido** para o HEAD e reclassificado como (c). Prova in-place agora: `Ran 13 tests ... OK` (secao 5.1) |
| **B2** | outros 9 documentos com sha256 de HEAD registrado em artefatos vivos (11 registros) passaram a divergir | **todos os 9 revertidos** para o HEAD e reclassificados como (c) - regra 1 da secao 2 aplicada sem excecao. `git diff HEAD` dos registros e dos documentos cobertos: **vazio** (secao 3) |
| **B3** | numeros do relatorio misturavam o censo de HEAD com o estado final, e 4 linhas da tabela nao fechavam | censo **separado por estado** (HEAD x arvore entregue) na secao 1, tabelas geradas por script, `(a)+(b)+(c) == HEAD` conferido (secao 9) |
| **B4** | dois campos de template vazios (chaves literais sem valor) no entregavel | o entregavel passou a ser **gerado por script** (`scratch/repopriv/gera_entrega3.py`): nao ha mais buraco |
| **B5** | 22 linhas com placeholder DENTRO de bloco de codigo/log/JSON | **16 tokens corrigidos** por semantica: bloco de COMANDO -> `$HOME` (expande no git-bash); bloco de SAIDA/LOG/JSON -> `<PERFIL-DO-DONO>` (nao afirma expansao que nao houve). Criterio e lista na secao 4.2 |
| **B6** | nada commitado (74 arquivos + entregavel apenas na arvore) | commit da rodada 2 (secao 9) |
| **B7** bloqueante (rodada 3) | a linha do gate nesta pagina afirmava `!! 11 PENDENCIAS` ("byte-identico ao baseline"), mas a prova foi tirada com o entregavel ainda NAO RASTREADO: o gate varre os `.md` de `git ls-files`, e o commit o trouxe para dentro da varredura - e o texto citava o nome de um projeto de bancada que saiu do repo, que e' justamente o que o passo 7 do gate reprova | a citacao literal saiu do texto; o gate passou a ser **executado pelo gerador desta pagina** e a saida integral ficou versionada (secao 5.2) |
| **nit** (rodada 3) | a secao 8 dizia que as ferramentas ficam em `scratch/` "fora do versionado" e a ultima linha falava em "script versionado" | as duas dizem a mesma coisa agora: os geradores sao de bancada, em `scratch/` (gitignored) |

### 0.2 Numeros finais (medidos, nao estimados)

| classe | arquivos | ocorrencias do token | acao |
|---|---|---|---|
| (a) documento/relatorio vivo | 61 | 95 | **normalizado** (placeholder declarado + nota no documento) |
| (b) ferramenta/script | 3 (+1, ver 5) | 3 | **resolucao em tempo de execucao** + prova |
| (c) evidencia congelada / registro pinado | 88 | 1084 | **intocada** - permanece como esta, por ser prova |
| **soma** | **152** | - | = arquivos com o token no commit-base do trabalho (secao 1) |

## 1. O censo (medido, nao estimado)

O cartao falava em 98 arquivos. **O censo no commit-base do trabalho (`96a6d60`) nao
reproduz 98** (1923 arquivos rastreados): o numero real e' maior, e o comando fica aqui para
ser refeito. Os numeros desta secao sao MEDIDOS pelo gerador desta pagina a cada execucao.

```
python scratch/repopriv/mede3.py --json      # censo HEAD x arvore (todas as formas)
python scratch/repopriv/classifica4.py       # classes (a)/(b)/(c) + linhas em bloco
```

Token de CAMINHO = `Users` + separador + `<nome>` (cobre `C:/`, `C:\`, `C:\\`,
`/c/`, `../../`).

| estado | arquivos com o token | ocorrencias |
|---|---|---|
| **antes do trabalho** = commit-base do trabalho `96a6d60` | 152 | 1182 |
| **arvore entregue** (`git ls-files` + disco) | 92 | 1111 |
| removidas por este trabalho | 64 | 98 |
| restantes que JA' existiam no commit-base | 88 | 1084 |
| NOVOS, de cartoes PARALELOS (nao deste trabalho) | 4 | 27 |

O rotulo do commit-base e' FIXO (`96a6d60`): cartoes paralelos commitam durante a rodada e o
ponto de partida do trabalho nao se move. `HEAD` no fechamento desta rodada era
`cfcb3f0 REPO-PRIV-1 rodada 3: prova do gate de docs medida na arvore entregue (fecha o achado B7)`.

Os 4 arquivos que apareceram com o token DEPOIS do commit-base nao sao deste trabalho -
vieram de cartoes paralelos:

| arquivo novo (cartao paralelo) | ocorrencias |
|---|---|
| `docs/automacao/LANG-DECISOES/LANG-C1-DECISAO.md` | 9 |
| `docs/automacao/LANG-DECISOES/LANG-C2-DECISAO.md` | 7 |
| `docs/automacao/LANG-DECISOES/LANG-C3-DECISAO.md` | 3 |
| `docs/automacao/LANG-DECISOES/LANG-C5-DECISAO.md` | 8 |

Formas textuais no commit-base `96a6d60`, medidas (mesmo token, escrita diferente):

| forma | arquivos | ocorrencias |
|---|---|---|
| barra invertida: `C:\Users\<nome>` | 37 | 64 |
| escapado em JSON/Python: `C:\\Users\\<nome>` | 34 | 976 |
| barra normal: `C:/Users/<nome>` | 78 | 113 |
| formato MSYS/git-bash: `/c/Users/<nome>` | 15 | 24 |

O grosso das ocorrencias (976 de 1182) vem de **evidencia congelada**:
os `.stdout` de `COR-AUT7-F2-evidencias/` repetem o caminho de 113 em 113 linhas.

**Nota de honestidade sobre o 98:** nao existe combinacao de formas que dê exatamente 98
arquivos (`fwd+msys`=90, `fwd+bks1`=108, uniao de todas=152). O numero do cartao nao foi
reproduzido; o que esta aqui e' o que o repositorio tem, com o comando que mede. Nao
inventei ocorrencia para casar com 98.

**Nenhum arquivo novo com o token entrou por este trabalho** - as 4 entradas novas
da tabela acima sao de cartoes paralelos. A conferencia e' por CONJUNTO: `purgados`
(commit-base menos arvore) = 64 arquivos, `novos` (arvore menos commit-base) = 4
arquivos, e nenhum arquivo deste trabalho esta na lista de novos. Esta entrega so' removeu o
token, nunca introduziu.

## 2. A regra de classe (e por que ela nao e' arbitraria)

Ordem de decisao do classificador - a primeira que casa vence:

1. **sha256 do arquivo registrado E AINDA VALIDO num artefato vivo** -> (c).
   Reescrever o documento faria o registro (que e' prova de uma rodada) passar a mentir.
   Na rodada 2 esta regra foi aplicada **sem excecao**, inclusive sobre os documentos que
   eu ja' tinha normalizado (foi exatamente o que a revisao pegou: B1 e B2).
2. **documento PINADO em `tools/audita_docs_proveniencia.json`** -> (c).
   O projeto mantem esse registro imutavel com `sha256` da LINHA e do DOCUMENTO INTEIRO, e
   o passo 10 do `validate.yml` reprova quando o documento muda.
3. caminho em pasta `*evidencias*`, nome de artefato de prova (`.stdout`, `.log`,
   `hashes*.txt`, `*-resultado.json`, `*-verificacao.json`, `suite-vinculo.json`,
   `rodada-final-*`, `harness-results.*`, `DUMP-CHAVEADO-*`...) -> (c).
4. codigo funcional (`.py`/`.sh`/`.ps1`) -> (b).
5. resto (`.md`/`.txt` de prosa) -> (a).

Na rodada 2 entrou uma regra de SEMANTICA dentro da (a):

6. dentro de **bloco de comando** (fence `bash`/shell) -> `$HOME` (expande de verdade);
   dentro de **bloco de saida/log/JSON** (transcricao do que uma rodada imprimiu) ->
   `<PERFIL-DO-DONO>` (nao pode afirmar uma expansao que nunca houve). Fora de bloco,
   prosa -> `%USERPROFILE%`.

## 3. Documentos que ficaram na classe (c) por REGISTRO de sha256

A rodada 1 tinha normalizado documentos cujo sha256 esta registrado como prova em outro
arquivo do proprio repo. A rodada 2 reverteu todos: editar o documento invalida o registro
(e, no caso do B1, quebra o auto-teste da ferramenta que o gerencia).

**14 documentos revertidos** (sha256 da versao HEAD ainda citado por
15 registros distintos):

| documento (classe c) | sha256 (versao HEAD) | registrado em |
|---|---|---|
| `docs/automacao/LANG-C4-REVISAO-DONO.md` | `40d776c47854...` | `docs/automacao/LANG-C4-REVISAO-DONO-verificacao.json`, `docs/automacao/LANG-DECISOES/LANG-C4-DECISAO-verificacao.json`, `docs/automacao/LANG-DECISOES/LANG-C4-DECISAO.md` |
| `docs/automacao/AUT-3F2-relatorio.md` | `abbd1c23a8e9...` | `docs/automacao/AUT-3F2R-revisao.md` |
| `docs/automacao/CIC-3-L2-entrega.md` | `f8ccfbe86853...` | `docs/automacao/CIC-3-L2-revisao.md` |
| `docs/automacao/KIT-16-parte01.md` | `bceab0c43e40...` | `docs/automacao/KIT-16-revisao.md` |
| `docs/automacao/LEVEL-R2-relatorio-01.md` | `983c08a33fdf...` | `docs/automacao/LEVEL-R2-hashes.txt`, `docs/automacao/LEVEL-R2-pacote-revisao-MANIFEST.json` |
| `docs/automacao/LEVEL-R3F1-relatorio-01.md` | `ea67a7c37a10...` | `docs/automacao/LEVEL-R3F1-hashes.txt`, `docs/automacao/LEVEL-R3F1-pacote-revisao-MANIFEST.json` |
| `docs/cobertura/revisao/CHK-1-shrines-conferencia-mecanica.md` | `6b27b4b61bf4...` | `docs/automacao/AUT-2-matriz.json`, `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json` |
| `docs/cobertura/revisao/RSTV-27R-body.md` | `f2b128e43d52...` | `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json` |
| `docs/cobertura/revisao/RSTV-27R-revisao.md` | `47daa9a4cb5d...` | `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json` |
| `docs/automacao/EV-R2-FORAPOOL-b04-parte06.md` | `1a96d89bb5ef...` | `docs/automacao/EV-R2-FORAPOOL-b04-copia-verificada.json`, `docs/automacao/EV-R2-FORAPOOL-b04-validacao-repro-final.json` |
| `docs/automacao/INT-R1-parte01.md` | `95b23b0198a7...` | `tools/audita_docs_proveniencia.json` |
| `docs/automacao/INT-R1-parte06.md` | `701a3a803e08...` | `tools/audita_docs_proveniencia.json` |
| `docs/automacao/KIT-03F-entrega.md` | `92a5abbeef5f...` | `tools/audita_docs_proveniencia.json` |
| `docs/automacao/KIT-16-entrega.md` | `0ce08822d98d...` | `tools/audita_docs_proveniencia.json` |

**Documentos PINADOS no auditor de proveniencia (passo 10 do CI):**

| documento (classe c) |
|---|
| `docs/automacao/INT-R1-parte01.md` |
| `docs/automacao/INT-R1-parte06.md` |
| `docs/automacao/KIT-03F-entrega.md` |
| `docs/automacao/KIT-16-entrega.md` |

Prova de que nada divergiu: `git diff HEAD` do CONJUNTO de 15 registros +
CONJUNTO de 14 documentos cobertos sai **vazio** (os registros nunca foram
editados; os documentos cobertos estao identicos a HEAD). A prova completa, com a saida, esta
em `scratch/repopriv/provas2/prova_b2_full.out` (secao 0). Os manifestos de hash que cobrem
arquivos com o token seguem batendo: **11 OK / 0 STALE**
(`scratch/repopriv/provas2/manifestos.out`).

**Excecao declarada (transparencia):** `docs/automacao/KIT-16-revisao.md` e' um REGISTRO
(cita o sha256 de `KIT-16-parte01.md`, linha da tabela acima) e ao mesmo tempo carregava o
token - por isso ele esta na classe (a) e nao foi revertido: o sha256 DELE nao esta
registrado em lugar nenhum, ou seja, nada o trata como prova congelada. O cuidado que isso
exige foi tomado e provado: **nenhum dos 10 hashes de 64 caracteres dentro dele mudou**
(diff de HEAD x disco vazio: `scratch/repopriv/provas2/kit16rev_hex.diff`), e o documento
que ele registra foi revertido. As unicas alteracoes nele sao a linha citada do achado B5 e a
nota de rodape que declara o placeholder (secoes 4.2 e 4).

## 4. Classe (a) - documentos vivos: o que foi trocado e por que

Placeholder **declarado**, com nota acrescentada NO PROPRIO documento
(61 dos 61 arquivos da classe (a)):

| forma original | placeholder | por que esse |
|---|---|---|
| `C:/Users/<nome>`, `C:\Users\<nome>`, `C:\\Users\<nome>` | `%USERPROFILE%` | variavel do Windows: **expande de verdade** no cmd/PowerShell |
| `/c/Users/<nome>` | `$HOME` | variavel do bash: expande de verdade no git-bash |
| mencao AO VAZAMENTO / transcricao de run | `<PERFIL-DO-DONO>` | aqui a substituicao expansivel seria MENTIRA: o texto acusa um literal fixo, ou registra o que uma rodada imprimiu |

```text
> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) - e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` - substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
```

### 4.1 Mencoes metalinguisticas (3 linhas, 3 arquivos)

Linha que fala DO caminho fixo como defeito: `<PERFIL-DO-DONO>` (um `<...>` nao pode ser
confundido com caminho valido).

| arquivo | linha | texto |
|---|---|---|
| `docs/automacao/KIT-03F-parte03.md` | 14 | `| C6 | `isolacao.sh` | removido `<PERFIL-DO-DONO>/...` | grep vazio |` |
| `docs/automacao/KIT-03R-parte02.md` | 83 | `- `isolacao.sh` linha 187: fallback **hardcoded** `<PERFIL-DO-DONO>/AppData/Roaming/...` (usuário fixo).` |
| `docs/automacao/KIT-03R-revisao.md` | 40 | `| C6 | Ausência de caminhos pessoais fixos | **ACHADO** (A12 `KITS_DIR` ignorado por 4 scripts; A3 `Abyssus`; A15; A17 `<PERFIL-DO-DONO>` hardcoded em` |

### 4.2 Placeholders DENTRO de bloco de codigo/log (achado B5)

22 linhas da classe (a) tem um placeholder dentro de bloco. Todas conferidas uma a uma:

| bloco | placeholder correto | por que |
|---|---|---|
| ```bash (comando a copiar) | `$HOME` | `%USERPROFILE%` NAO expande em bash |
| ```diff (trecho de shell) / sessao com prompt `$` | `$HOME` | e' codigo de shell |
| bloco sem linguagem com comando (`python ...`) | `$HOME` | idem |
| bloco de SAIDA de run (`[FAIL] Player.log: ...`, `mv: cannot move ...`, listagem de processos) | `<PERFIL-DO-DONO>` | transcricao: `%USERPROFILE%` afirmaria expansao que nao houve |
| bloco ```json com `"path"` de um harness | `<PERFIL-DO-DONO>` | idem |

Resultado medido: **0** linhas de bloco com `%USERPROFILE%`; 9 com `$HOME` (4 em `bash`,
2 em `diff`, 3 em bloco de comando) e 13 com `<PERFIL-DO-DONO>` (12 em bloco de saida,
1 em `json`). Checagem mecanica: `scratch/repopriv/checa3.py` (item 1 = 0).

A linha de prosa que cita um COMANDO EXECUTADO (`KIT-16-revisao.md:24`,
`python tree_snapshot.py ... "C:/Users/<nome>/..."`) tambem virou `$HOME`: varredura em
`scratch/repopriv/varre_cmd.py` (restou so' `ls $HOME/.hermes`, ja' correto).

### 4.3 Os 61 documentos normalizados

| documento | ocorrencias removidas | acao |
|---|---|---|
| `docs/BETTERPORTUGUESE-ARQUITETURA.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/DBG-PROVENIENCIA.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/API-R1-I1-parte02.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/API-R1-I1-parte03.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/API-R1-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/API-R1-runbook-runtime.md` | 3 | normalizado (placeholder declarado + nota) |
| `docs/automacao/AUT-3F-relatorio.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/AUT-3FR-revisao.md` | 4 | normalizado (placeholder declarado + nota) |
| `docs/automacao/AUT-3R2-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/AUT-3R3-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/AUT-5R-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/AUT5-F2-relatorio.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/CIC-3F-entrega.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/CIC-3F-parte03.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/CIC-3F-revisao.md` | 2 | normalizado (placeholder declarado + nota) |
| `docs/automacao/COR-AUT4-F2R-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/COR-AUT4-F4R-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/DBG-R2-parte01.md` | 2 | normalizado (placeholder declarado + nota) |
| `docs/automacao/DBG-R2-parte03.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/DBG-R2-parte04.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/EV-R1-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/EV-R2-NORMAL-b05-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/INT-R1-C4-parte03.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/INT-R1-C6-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-03F-parte03.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-03R-parte02.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-03R-parte03.md` | 4 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-03R-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-04R-parte02.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-04R-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-05F-parte02.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-05R-parte04.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-05R-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-06R-parte06.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-14-entrega-run1014.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-14-entrega-run703.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-14-entrega-run916.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-14-parte23.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-14-parte65.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-14F-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-14G-SEG2-parte02.md` | 11 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-16-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-G4-PREP-entrega.md` | 5 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT-G4-PREP-runbook-dono.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT14G-SEG2-investigacao-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT14G-SEG2-investigacao-parte02.md` | 4 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT14G-SEG2-investigacao-parte03.md` | 2 | normalizado (placeholder declarado + nota) |
| `docs/automacao/KIT14G-SEG2-investigacao-parte04.md` | 3 | normalizado (placeholder declarado + nota) |
| `docs/automacao/LEVEL-PACOTE-CONTRATO-parte01.md` | 2 | normalizado (placeholder declarado + nota) |
| `docs/automacao/ORG-AUT5-DIAG-parte02.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/ORG-R1-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/ORG-R1-parte03.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/ORG-R1-parte04.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/ORG-R3-EXEC-parte01.md` | 2 | normalizado (placeholder declarado + nota) |
| `docs/automacao/ORG-R3-GATE-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/ORG-R4-DOC-parte01.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/PKG-API-entrega.md` | 2 | normalizado (placeholder declarado + nota) |
| `docs/automacao/PUB-API-1-entrega.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/automacao/REPO-WIP-entrega-run923.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/cobertura/revisao/RSTV-28R-revisao.md` | 1 | normalizado (placeholder declarado + nota) |
| `docs/cobertura/revisao/RSTV-29R-revisao.md` | 2 | normalizado (placeholder declarado + nota) |

## 5. Classe (b) - ferramentas: resolucao em tempo de execucao + PROVA

| arquivo | ocorrencias removidas |
|---|---|
| `docs/automacao/EV-R2-NORMAL-b03-gerar-propostas.py` | 1 |
| `docs/automacao/EV-R2-NORMAL-b03-validar.py` | 1 |
| `tools/preparar_revisao_dono.py` | 1 |

`tools/automacao/kit15/teste_kit15.py` entra como **quarto** item da classe (b), mas com
**0 ocorrencias do token de caminho**: o que ele tinha era o NOME SOLTO do perfil como
fallback de `os.environ.get("USERNAME")`. Por isso ele nao aparece na tabela acima (que
conta o token de caminho) nem na soma da secao 0.2 - declarado aqui para nao sumir.

### 5.1 Provas de execucao (saida real, em `scratch/repopriv/provas2/`)

| ferramenta | prova | saida |
|---|---|---|
| `tools/preparar_revisao_dono.py` | **IN-PLACE** `python tools/preparar_revisao_dono.py --verify-only` | `Ran 13 tests in 0.055s` / `OK`; `tests_run: 13`, `tests_passed: true` (`prep_inplace.out`). `ATT` resolvido em tempo de execucao: `%USERPROFILE%\AppData\Local\hermes\kanban\attachments` (existe: `True`) |
| `docs/automacao/EV-R2-NORMAL-b03-gerar-propostas.py` | versao de HEAD x disco, saida comparada | **byte-identica** (diff vazio), `MANTER 13 / MELHORAR 7`; artefato rastreado com o MESMO sha256 `cfbb3643...` |
| `docs/automacao/EV-R2-NORMAL-b03-validar.py` | idem | **byte-identica**; `PASS SOURCES_11_UNCHANGED` (11/11), `TOTAL 28 PASS 28 FAIL 0`; artefato com o mesmo sha256 `9280b0a3...` |
| suite kit15 | `python tools/automacao/kit15/teste_kit15.py` | `KIT15-SUITE|tests=21|failures=0|errors=0|skipped=0|ok=True`; unica diferenca para a rodada 1 e' o tempo decorrido (`6.994s` x `7.251s`) |
| gate de docs | `python tools/audita_docs.py` **executado na arvore entregue** | `!! 12 PENDENCIAS`, exit `1` - **1 linha(s) nova(s)** contra o baseline de 11 pre-existentes, e ela e' do cartao PARALELO PKG-EN (`docs/automacao/LANG-PKG-entrega.md`). **0 pendencia deste cartao**. Saida integral versionada em `docs/automacao/REPO-PRIV-prova-audita.txt` (secao 5.2) |

**Rodada 3: tudo reconferido IN-PLACE, no repo, com a saida integral em
`scratch/repopriv/provas3/prova_b3_full.out`.** `preparar_revisao_dono.py --verify-only`
terminou em `Ran 13 tests in 0.054s / OK`, `tests_passed: true` (o recibo reescrito foi
restaurado com `git checkout --`, `git diff` dele vazio); suite kit15
`tests=21|failures=0|errors=0|ok=True`; `gerar-propostas` `MANTER 13 / MELHORAR 7` com o
artefato no MESMO sha256 `cfbb3643...` e arvore limpa; `validar` `TOTAL 28 PASS 28 FAIL 0`
(`SOURCES_11_UNCHANGED` 11/11) com `EV-R2-NORMAL-b03-validacao.json` no MESMO sha256
`9280b0a3...`; os 11 hashes de manifesto que cobrem arquivos com o token seguem
**11 OK / 0 STALE**. Esta rodada nao tocou em nenhum dos 4 arquivos da classe (b): o diff
deles contra o commit-base continua sendo so' resolucao de caminho.

Correcao de metodo em relacao a rodada 1: a prova do `preparar_revisao_dono.py` agora roda
**no lugar**, no repo. A rodada 1 rodava uma copia em sandbox, onde `ROOT`/`SOURCE` nao
resolviam - a saida terminava em `FAILED (errors=4)` e nao provava nada. Os arquivos
antigos (`provas/prep_antes.out`, `prep_depois.out`, `prep_diff.txt`) foram mantidos, mas
**nao sao mais a prova**; a prova e' `provas2/prep_inplace.out`.

Nota de transparencia: `--verify-only` **reescreve** `LANG-C4-REVISAO-DONO-verificacao.json`
(o recibo guarda o sha256 do documento calculado sobre o disco; como o repo usa
`core.autocrlf=true`, disco=CRLF e blob=LF, o valor regravado difere do versionado). Isso
ja' acontecia em HEAD - nao e' regressao desta tarefa. Depois da prova o recibo foi
restaurado com `git checkout --` e o `git diff` dele esta **vazio** (provado no script).

Mixagem declarada, como o cartao pediu: `EV-R2-NORMAL-b03-validar.py` e' **codigo
funcional COM registro de hash congelado dentro**; tratei as duas partes separadamente - o
caminho virou resolucao de execucao, o sha256 medido ficou intacto.

### 5.2 Gate de docs: a saida INTEGRAL, medida na arvore entregue (achado B7)

O gate do passo 10 do CI e' `python tools/audita_docs.py` (sai diferente de 0 quando alguma
doc afirma algo que nao bate com o disco). A rodada 2 afirmou nesta pagina "bloco de
pendencias byte-identico ao baseline, 11 pre-existentes" - e aquela afirmacao NAO reproduzia,
por dois motivos encadeados:

1. o script monta a lista de arquivos com `git ls-files` filtrado por `.md`, ou seja so' varre
   o que esta RASTREADO. Quando a prova foi tirada, o entregavel ainda estava fora do indice;
   o commit o trouxe para dentro da varredura;
2. o texto do proprio entregavel citava o nome de um projeto de bancada que saiu do repo, e o
   passo 7 do gate reprova exatamente essa citacao. A prova acendeu uma pendencia nela mesma -
   e ninguem remediu depois do commit, que e' quando o arquivo passou a ser varrido.

Correcao: (i) a citacao literal saiu do texto; (ii) o gate passou a ser EXECUTADO pelo gerador
desta pagina a cada execucao, e a saida integral fica versionada em
`docs/automacao/REPO-PRIV-prova-audita.txt` (LF; no Windows o gate imprime CRLF, por isso o
`tr -d '\r'` nas duas pontas). Reproducao por dois comandos:

```
python tools/audita_docs.py | tr -d '\r' > /tmp/agora.txt
tr -d '\r' < docs/automacao/REPO-PRIV-prova-audita.txt | diff /tmp/agora.txt - && echo IGUAL
```

Estado medido na arvore entregue: `!! 12 PENDENCIAS`, exit `1`.

| pendencia | de quem e' |
|---|---|
| 11 pre-existentes (ferramenta citada que nao existe; dependencia do Thunderstore fora do padrao em 2 mods; versao da api; 7 citacoes do nome de um projeto de bancada em `KIT-G4-PREP-entrega.md` e `PKG-API-entrega.md`) | anteriores a este cartao: presentes e identicas no baseline `scratch/repopriv/provas2/a_pend.txt` |
| 1: `docs/automacao/LANG-PKG-entrega.md` cita o nome de um projeto de bancada que saiu do repo | cartao PARALELO PKG-EN (commit `c43b78d`), que trouxe esse `.md` para o indice. Nao e' arquivo deste cartao e nao foi tocado aqui |
| **0** | **deste cartao** |

A comparacao e' por CONJUNTO, nao por contagem: as 11 linhas do baseline continuam presentes e
identicas, e a unica linha nova e' a do cartao paralelo. Como esse numero muda se outro cartao
commitar, a prova e' o arquivo versionado - nao um numero digitado.

## 6. Classe (c) - evidencia congelada: NAO reescrita

Estes 88 arquivos **permanecem como estao, por serem prova**
(1084 ocorrencias do token). Reescrever o caminho dentro deles seria
falsificar o artefato: eles sao o registro do que uma rodada viu.

| arquivo | ocorrencias | motivo (medido) |
|---|---|---|
| `docs/automacao/COR-AUT7-F2-evidencias/A6-R1-suite-real.stdout` | 113 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/A6-R3-suite-real-com-defeito.stdout` | 113 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/A6-R7-sem-suite-restaurado.stdout` | 113 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E1-rodada-viva-grava-o-cache.stdout` | 113 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E1-sem-suite-baseline.stdout` | 113 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E1b-sem-suite-baseline.stdout` | 113 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E4-sem-suite-restaurado.stdout` | 113 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/AUT-3-resultado.json` | 32 | sha256(HEAD) registrado em `docs/automacao/AUT-7-resultado.json`, `docs/automacao/COR-AUT4R-evidencias/hashes.txt`, `docs/automacao/COR-AUT7-F2-evidencias/A1-bf-par-chave-de-um-lado.aceite.json`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/A6-R4-sem-suite-cache-anterior.stdout` | 25 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/A6-R4b-sem-suite-formato-anterior.stdout` | 25 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/A6-R6-sem-suite-dll-de-bin-mutada.stdout` | 25 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E3-sem-suite-com-a-prova-velha.stdout` | 25 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/API-R1-I1-evidencias/06-ensaio-arena-isolada.txt` | 9 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/refutacao-cor-aut7-f2.json` | 8 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LANG-C4-REVISAO-DONO-verificacao.json` | 8 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-3R2-evidencias/09-hashes.txt` | 7 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E4-consolidador-restaurado.stdout` | 7 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/entradas-medidas.json` | 7 | sha256(HEAD) registrado em `docs/automacao/COR-AUT7-F2-evidencias/hashes-finais.json`, `docs/automacao/COR-AUT7-F2-relatorio.md`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/A6-R5-consolidador-cache-anterior.stdout` | 5 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E3-consolidador-sem-a-fixture.stdout` | 5 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-3R2-evidencias/03-bancada-red-green-do-autor.txt` | 4 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-4R3-evidencias/07-negativo-obrigatorio.txt` | 4 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/API-R1-I1-evidencias/09-tentativa-userprofile-descartada.txt` | 3 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/cobertura/revisao/RSTV-27R-revisao.md` | 3 | sha256(HEAD) registrado em `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json` |
| `docs/automacao/API-R1-I1-evidencias/05-antes-x-depois.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/API-R1-I1-evidencias/07-perfil-intacto-e-destino-padrao.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-3R-revisao.md` | 2 | sha256(HEAD) registrado em `docs/automacao/CIC-3R2-evidencias/09-hashes.txt`, `docs/automacao/CIC-3R2-revisao.md` |
| `docs/automacao/CIC-3R2-evidencias/04-plantio-revisor-atual.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-3R2-evidencias/05-dupla-lente-antigo-atual.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-3R2-evidencias/11-checagens-de-doc.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-4R3-evidencias/12-travas-documento.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT4-F2-relatorio.md` | 2 | sha256(HEAD) registrado em `docs/automacao/COR-AUT4-F2R-evidencias/hashes_revisor.txt`, `docs/automacao/COR-AUT4-F2R-revisao.md` |
| `docs/automacao/COR-AUT4-F2R-evidencias/hashes_revisor.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT4R-revisao.md` | 2 | sha256(HEAD) registrado em `docs/automacao/COR-AUT4-F2R-evidencias/hashes_revisor.txt`, `docs/automacao/COR-AUT4-F2R-revisao.md` |
| `docs/automacao/INT-R1-C4-evidencias/05-fora-do-repo-vermelho.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/INT-R1-C4-evidencias/06-fora-do-repo-verde.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/KIT-03-entrega.md` | 2 | sha256(HEAD) registrado em `docs/automacao/KIT-03F-entrega.md` |
| `docs/automacao/KIT-03F-entrega.md` | 2 | PINADO em `tools/audita_docs_proveniencia.json`; sha256(HEAD) registrado em `tools/audita_docs_proveniencia.json` |
| `docs/automacao/LANG-C4-REVISAO-DONO.md` | 2 | sha256(HEAD) registrado em `docs/automacao/LANG-C4-REVISAO-DONO-verificacao.json` |
| `docs/automacao/LEVEL-R2-evidencias/harness-results.json` | 2 | sha256(HEAD) registrado em `docs/automacao/LEVEL-R2-hashes.txt`, `docs/automacao/LEVEL-R2-pacote-revisao-MANIFEST.json`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R2-evidencias/harness-results.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R2-evidencias/rodada-final-01.json` | 2 | sha256(HEAD) registrado em `docs/automacao/LEVEL-R2-hashes.txt`, `docs/automacao/LEVEL-R2-pacote-revisao-MANIFEST.json`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R2-evidencias/rodada-final-01.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R2-relatorio-01.md` | 2 | sha256(HEAD) registrado em `docs/automacao/LEVEL-R2-hashes.txt`, `docs/automacao/LEVEL-R2-pacote-revisao-MANIFEST.json` |
| `docs/automacao/LEVEL-R3F1-evidencias/defeito-replantado-01.json` | 2 | sha256(HEAD) registrado em `docs/automacao/LEVEL-R3F1-hashes.txt`, `docs/automacao/LEVEL-R3F1-pacote-revisao-MANIFEST.json`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R3F1-evidencias/defeito-replantado-01.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R3F1-evidencias/harness-results.json` | 2 | sha256(HEAD) registrado em `docs/automacao/LEVEL-R3F1-hashes.txt`, `docs/automacao/LEVEL-R3F1-pacote-revisao-MANIFEST.json`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R3F1-evidencias/harness-results.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R3F1-evidencias/rodada-final-01.json` | 2 | sha256(HEAD) registrado em `docs/automacao/LEVEL-R3F1-hashes.txt`, `docs/automacao/LEVEL-R3F1-pacote-revisao-MANIFEST.json`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/LEVEL-R3F1-evidencias/rodada-final-01.txt` | 2 | evidencia congelada (caminho/nome de artefato de prova) |
| `tools/fixtures/bf-shaders-em-jogo.log` | 2 | sha256(HEAD) registrado em `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/API-R1-I1-evidencias/01-perfil-antes.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/API-R1-I1-evidencias/10-correcoes-revisao-rodada1.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/AUT-3F2-relatorio.md` | 1 | sha256(HEAD) registrado em `docs/automacao/AUT-3F2R-revisao.md` |
| `docs/automacao/AUT-4F-evidencias/planta-defeitos-resultados.json` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/AUT-7-evidencias/cor-aut7/suite-vinculo.json` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-3-L2-entrega.md` | 1 | sha256(HEAD) registrado em `docs/automacao/CIC-3-L2-revisao.md` |
| `docs/automacao/CIC-3R2-evidencias/06-n1-verde-global.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-3R2-evidencias/07-trava-ok-novo.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-4R3-evidencias/04-bench-antes-RED.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-4R3-evidencias/11-diff-antes-depois.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/CIC-4R3-evidencias/neutro.py` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT4-F2R-evidencias/adv_borda.py` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT4-F2R-evidencias/adv_rev.py` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT4-F3-evidencias/hashes.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT4-F3-evidencias/planta_defeito.py` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT4-F3-relatorio.md` | 1 | sha256(HEAD) registrado em `docs/automacao/COR-AUT4-F3-evidencias/hashes.txt` |
| `docs/automacao/COR-AUT4-F3R-revisao.md` | 1 | sha256(HEAD) registrado em `docs/automacao/COR-AUT4-F4R-revisao.md` |
| `docs/automacao/COR-AUT4-F4-entrega.md` | 1 | sha256(HEAD) registrado em `docs/automacao/COR-AUT4-F4R-revisao.md` |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E2-rodada-viva-com-a-fixture.stdout` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E3-rodada-viva-sem-a-fixture.stdout` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E-E4-rodada-viva-restaurada.stdout` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E5-rodada-viva-contra-prova-auditada.stdout` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/E5-rodada-viva-puros-auditada.stdout` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json` | 1 | sha256(HEAD) registrado em `docs/automacao/ORG-R3-EXEC-parte01.md`, `docs/automacao/ORG-R3-GATE-parte01.md`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/COR-AUT7-evidencias/suite-vinculo.json` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/EV-R2-FORAPOOL-b04-parte06.md` | 1 | sha256(HEAD) registrado em `docs/automacao/EV-R2-FORAPOOL-b04-copia-verificada.json`, `docs/automacao/EV-R2-FORAPOOL-b04-validacao-repro-final.json` |
| `docs/automacao/EV-R2-FORAPOOL-b04-repro-recibo.json` | 1 | sha256(HEAD) registrado em `docs/automacao/EV-R2-FORAPOOL-b04-copia-verificada.json`, `docs/automacao/EV-R2-FORAPOOL-b04-validacao-repro-final.json` |
| `docs/automacao/INT-R1-C5-evidencias/10-release-check.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/automacao/INT-R1-parte01.md` | 1 | PINADO em `tools/audita_docs_proveniencia.json`; sha256(HEAD) registrado em `tools/audita_docs_proveniencia.json` |
| `docs/automacao/INT-R1-parte06.md` | 1 | PINADO em `tools/audita_docs_proveniencia.json`; sha256(HEAD) registrado em `tools/audita_docs_proveniencia.json` |
| `docs/automacao/KIT-16-entrega.md` | 1 | PINADO em `tools/audita_docs_proveniencia.json`; sha256(HEAD) registrado em `tools/audita_docs_proveniencia.json` |
| `docs/automacao/KIT-16-parte01.md` | 1 | sha256(HEAD) registrado em `docs/automacao/KIT-16-revisao.md` |
| `docs/automacao/LEVEL-R3F1-relatorio-01.md` | 1 | sha256(HEAD) registrado em `docs/automacao/LEVEL-R3F1-hashes.txt`, `docs/automacao/LEVEL-R3F1-pacote-revisao-MANIFEST.json` |
| `docs/automacao/PUB-ALL-evidencias/release-check-saida.txt` | 1 | evidencia congelada (caminho/nome de artefato de prova) |
| `docs/cobertura/DUMP-CHAVEADO-LANG-R1-contagens.json` | 1 | sha256(HEAD) registrado em `docs/automacao/INT-R1-C6-parte03.md`; evidencia congelada (caminho/nome de artefato de prova) |
| `docs/cobertura/revisao/CHK-1-shrines-conferencia-mecanica.md` | 1 | sha256(HEAD) registrado em `docs/automacao/AUT-2-matriz.json`, `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json` |
| `docs/cobertura/revisao/RSTV-27R-body.md` | 1 | sha256(HEAD) registrado em `docs/automacao/COR-AUT7-F2-evidencias/suite-vinculo.json` |

Motivo de fundo, em uma frase: um log de run que mostra o caminho do perfil esta
registrando o que ACONTECEU; trocar o texto por `%USERPROFILE%` produziria um documento que
nunca foi verdade.

Um caso merece nota: `docs/cobertura/DUMP-CHAVEADO-LANG-R1-contagens.json` e' um dump
GERADO (`gerado_em`, `script`) e o caminho dentro dele vem da INVOCACAO de
`tools/gera_dump_chaveado.py` (que nao tem caminho de usuario fixo). Editar o JSON a mao
seria mentir sobre o que foi gerado; a correcao real, se o dono quiser, e' regerar passando
um caminho relativo ao repo.

## 7. O que NAO da' para desfazer (e o que exige decisao separada)

**Limpar a arvore nao apaga o passado.** O conteudo ja' esta no HISTORICO do repositorio
PUBLICO: cada commit que tocou esses arquivos guarda o texto antigo, e qualquer pessoa que
clone o repo (ou olhe o historico/forks/mirrors) ve o nome do perfil do dono. Esta entrega
**nao** reescreveu historico, **nao** fez push e **nao** reescreveu commit algum - esta
escrito no cartao e foi respeitado.

Se o dono quiser apagar o passado, e' **reescrita de historico** (por exemplo
`git filter-repo`), o que muda SHAs, quebra clones de terceiros, invalida hashes citados em
documentos do proprio repo (varios deles listados na secao 3) e exige coordenar quem ja'
clonou. **Nao fiz, e nao estou sugerindo como rotina** - e' decisao separada, com cartao
proprio, se e quando o dono decidir. Registro aqui apenas porque o cartao pede que eu diga
o que nao da' para desfazer.

Limitacao tecnica que vale declarar: os 88 arquivos da classe (c)
continuam publicando o nome enquanto a decisao de reescrever historico OU de reemitir a
prova nao existir. Eles sao prova, nao descuido.

## 8. Ferramentas que ficam para conferencia

| arquivo | o que faz |
|---|---|
| `scratch/repopriv/mede3.py` | censo proprio HEAD x arvore (todas as formas) -> `mede3.json` |
| `scratch/repopriv/cruza3.py` | cruza sha256(HEAD) dos arquivos tocados com todo hex de 64 do repo -> `amarrados3.json` |
| `scratch/repopriv/classifica4.py` | classes (a)/(b)/(c) + linhas com placeholder em bloco -> `final4.json`, `b5.json` |
| `scratch/repopriv/fixa_b5.py` | corrige a semantica do placeholder dentro de bloco (dry-run sem `--aplicar`) |
| `scratch/repopriv/checa3.py` | 4 checagens de consistencia antes de fechar |
| `scratch/repopriv/varre_inline.py`, `varre_cmd.py` | procuram placeholder em codigo inline e comandos executados |
| `scratch/repopriv/gera_tabelas.py`, `gera_entrega3.py` | geram as tabelas e ESTE documento |
| `scratch/repopriv/prova_b2.sh` | prova de execucao das ferramentas (b) + nao-divergencia dos registros |
| `scratch/repopriv/prova_b3b.sh` | **rodada 3**: reconfere as ferramentas (b) in-place + o gate de docs, saida em `provas3/prova_b3_full.out` |
| `scratch/repopriv/edita_rodada3b.py` | **rodada 3**: aplica as edicoes do achado B7 (citacao literal fora, gate executado pelo gerador) |
| `scratch/repopriv/checa_manifestos.py` | confere se os hashes registrados ainda batem hoje |

Estao em `scratch/` (bancada, fora do versionado) de proposito: promover a `tools/` e'
decisao do dono, nao desta rodada.

## 9. Estado final medido

* **medicao POS-COMMIT** (medida na arvore entregue): **92** arquivos / **1111**
  ocorrencias do token, dos quais **4** arquivos / **27** ocorrencias vieram de
  cartoes PARALELOS depois do commit-base (secao 1). Nenhum arquivo desta entrega carrega o
  token - o entregavel nao reintroduz a identidade que ele trata.
* **commit desta rodada:** o commit FILHO de `cfcb3f0 REPO-PRIV-1 rodada 3: prova do gate de docs medida na arvore entregue (fecha o achado B7)` (rodada 3: fecha o
  achado B7 e o nit de durabilidade da revisao da rodada 2). Nada foi empurrado (sem `push`) e
  o historico nao foi reescrito.
* commit-base do TRABALHO (ancora deste censo): `96a6d60` - FIXO de proposito, porque cartoes
  paralelos commitam durante a rodada e o ponto de partida nao se move.
* arquivos com o token de caminho: **152** em `96a6d60` -> **92** na arvore
  entregue, dos quais **88** sao o resto do commit-base e **4** sao de cartoes
  paralelos
* removidos por este trabalho: **64 arquivos / 98 ocorrencias** - `(a)`
  61 + `(b)` 3 + `(c)`
  88 = **152**
  = arquivos com o token no commit-base (**152**) - a soma fecha
* classe (c) intocada: nenhum dos 88 aparece em `git diff`
  (`checa3.py`, item 3 = 0)
* `python tools/audita_docs.py`: `!! 12 PENDENCIAS` na arvore entregue -
  1 linha nova e ela e' do cartao PARALELO PKG-EN, **0 deste cartao**;
  saida integral versionada em `docs/automacao/REPO-PRIV-prova-audita.txt` (secao 5.2)

*Nao reescrevi historico, nao dei push, nao toquei em codigo de mod (so' na resolucao de
caminho dos 4 scripts da classe (b) e no fallback de nome do kit15), nao alterei evidencia
congelada e nao inventei ocorrencia: toda contagem desta pagina sai de
`scratch/repopriv/*.json`, gerados pelos scripts de BANCADA de `scratch/` (pasta
gitignored, fora do versionado - secao 8), e este documento e' ele proprio gerado por
`scratch/repopriv/gera_entrega3.py`, que roda o gate de docs a cada execucao.*
