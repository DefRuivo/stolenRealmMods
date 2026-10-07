# COR-AUT7 — correção dos falsos OK, do cache stale e das lacunas omitidas

Tarefa: `t_d0ece0eb` (COR-AUT7), execução 387, sessão distinta do autor (367) e do revisor
(381). Fonte dos achados: parecer independente `AUT-7R-revisao.md` (t_c718923e).

Escopo EXCLUSIVO: `tools/automacao/estilo/**` e `tools/automacao/aceite/**` (as duas
ferramentas e os dois testes da própria entrega) e os documentos gerados por elas. Produto,
mods, `docs/cobertura/**` curado, CIC-1/2/3/4/5 e trabalhos concorrentes **não** foram
editados. Nenhum build, instalação, abertura/encerramento de jogo, save ou publicação.

Esquema preservado: `AUT-7/estilo/1` e `AUT-7/aceite/1`; IDs canônicos dos 11 aspectos de
runtime e dos 4 mods inalterados.

## Ambiente e integridade

| item | resultado |
|---|---|
| produto (`identity-full.json` do AUT-7R: 25 fontes/DLLs) | 25 conferidos, **0 drift**, 0 ausentes |
| `BetterFont/Plugin.cs` mutado em sandbox (teste de cache) | restaurado **byte a byte** (sha256 igual) |
| jogo / save / build / deploy / publicação | **não executados** |
| runtime | **NÃO EXERCITADO** (censo, painel de atributos e números seguem INDETERMINADO) |

## Achado por achado

1. **BetterFont — propriedades efetivas do material.** Antes a preservação só comparava os
   campos presentes na observação. Agora o critério só fecha OK com **todas** as propriedades
   de `regras_bf_estilo.PRECISA_COPIAR` presentes e tipadas (`Float` numérico finito, `Cor`
   com hex+alfa, `_ClipRect` com 4 números), `keywords` de `PRECISA_LIGAR` booleanos e
   `shader_keywords` não vazio. Campo ausente ⇒ **NAO_EXERCITADO** com `lacuna_probe`, nunca OK.
2. **BetterFont — todos os controles/objetos.** O par ligado/desligado agora exige: mesma
   chave de objeto, exatamente um ligado e um desligado, **mesma sessão**, procedência e
   evidência válidas em ambos, e compara *todos* os campos (cores, keywords, material,
   `shader_keywords`). Controle `fixture`, sem material completo, de outra sessão ou ambíguo
   ⇒ lacuna. `rotulo_fixture=true` e `evidencia_runtime=false` **sobrepõem** `procedencia`.
3. **BetterFont — configuração.** O `config_sha` sozinho não aprova mais: é preciso o
   arquivo real, o hash conferido contra os bytes **e** contra a identidade da rodada, as
   chaves lidas do `.cfg` confrontadas com `defaults_com_linha` do fonte vivo, e igualdade
   valor-a-valor. Chave ausente/ambígua ⇒ lacuna; valor divergente ⇒ **REPROVADO**.
4. **BetterCombatText — superfícies/cores/alfa/contraste.** Só fecha OK com **todas** as
   superfícies de `SUPERFICIES_DO_BCT` (7), cada uma com letra, sombra e alfa completos,
   polaridade igual à esperada por `sombra_para`, contraste ≥ `CONTRASTE_MINIMO` e alfa ≥
   `ALFA_SOMBRA_MINIMA`. Uma única surface (ou sem cores) ⇒ lacuna nominal com a lista das
   superfícies ausentes.
5. **BCT — idempotência.** Duas observações copiadas da mesma leitura não valem: exige ≥2
   leituras do mesmo alvo/sessão com `estagio`, `leitura_id`, `evento_id` e `timestamp`
   **distintos**; valores iguais ⇒ OK, valores divergentes ⇒ REPROVADO; sessões diferentes,
   identidades repetidas ou cor incompleta ⇒ lacuna.
6. **BCT — sem vazamento no level-up.** Exige contexto `level-up`, `tipo_levelup` dentro de
   `TIPOS_DO_LEVELUP` e alvo Title/Description com campos completos. O veredito sai da
   **comparação com o controle nativo** (`controle_nativo`, BCT desligado, mesmo alvo e
   sessão, com prova própria): estilo **igual** ao nativo não é vazamento (lacuna/OK conforme
   o resto), estilo **diferente** é REPROVADO. Marca isolada de texto alheio ⇒ lacuna.
7. **Debugger — contrato/saneamento do dump.** Passa a usar o parser REAL do censo
   (`regras_debugger.carrega_censo` + `confere_linha` + `contrato_da_linha`), como a tarefa
   pediu. Log vazio ou **sem nenhuma linha reconhecida** ⇒ lacuna (nunca OK); linha
   "declarada dump" que o parser não reconhece ⇒ REPROVADO; campo **depois** do `desc=`,
   `|` **colado** ao valor e quebra de linha ⇒ REPROVADO; **os `|` separadores ANTES do `desc=`
   são o contrato e não reprovam mais**. **LIMITE (qualificado na COR-AUT7-F2, achado A4)**:
   o `|` DENTRO de um valor só é detectado quando vem colado (`tags=fogo|gelo`); com o
   separador real (`" | "`) o `FIELD = [^|]+` trunca em silêncio e a linha passa — o limite
   está comentado no ponto que decide e no censo (`tools/census.py:53`). Cobertura canônica de
   categorias e das colunas que o `FIELD` realmente lê é exigida (as derivadas — `arvore`/
   `status` — não vêm da linha).
8. **Cache `--sem-suite`.** O cache agora carrega a **fotografia** da suíte: hash de todos os
   fontes dos 4 mods, de `tools/testes/**`, de `tools/automacao/estilo/**` e de `tools/*.py`
   (conjuntos de caminhos: entrar/sair arquivo invalida), mais o comando e a versão do Python.
   Na releitura, o cache é revalidado: fotografia diferente ou JSON removido ⇒ **não reusa nada**
   (`cache_valido=false`, 0 OK de suíte). Drift durante a rodada descarta o resultado da suíte.
   **AMPLIAÇÃO na COR-AUT7-F2 (achado A6, 2ª rodada da revisão independente):** a fotografia
   passou a cobrir TODAS as ENTRADAS que a suíte lê — os 6 mods, `tools/**`, `lib/**`,
   `docs/cobertura/**`, `ReloadProbe/**`, `scratch/**`, `docs/PLANO-DE-TESTES.md` e os projetos
   `*.csproj`/`*.props`/`*.targets` da árvore (as guardas varrem a raiz inteira) — além dos
   artefatos de build que ela MEDE (`dist/*.zip` e `<Mod>/bin/**/*.dll`, bloco `artefatos`).
   Ficam fora de propósito: `bin`/`obj`/`__pycache__` (DERIVADOS) e as SAÍDAS da própria
   ferramenta (`docs/automacao/**`, senão o cache se invalidaria a cada relatório regerado).
   A cobertura declarada vai em todo resultado (`medicao.fotografia`) e foi MEDIDA com gancho de
   auditoria sobre a rodada viva (0 leituras fora dela). Prova:
   `COR-AUT7-F2-evidencias/entradas-medidas.json` (E1–E5) e `achados.A6_entradas` no
   `refutacao-cor-aut7-f2.json`.
9. **AUT-5/6 — resultado vazio/malformado.** `--rstv-criterios`/`--shrines-criterios` com
   `{"criterios":[]}`, fora do schema ou sem nenhum item utilizável geram **critério de
   lacuna canônico** (`AUT-5/resultado-vazio`, `AUT-6/resultado-malformado`, …) em vez de
   frente=0; item sem `id`/`estado`/`evidência` é descartado com lacuna nomeada; identidade
   divergente da rodada gera `identidade-divergente`. O adaptador injeta
   `fonte_sha`/`dll_sha` e registra qual módulo produziu cada critério.
10. **Reuso real do AUT-6.** O adaptador usa `tools/automacao/aut6/cobertura.py::avaliar`
    (frente COR-AUT6, sha256 `a935f573…`) — 21 critérios recebidos e anotados nas observações
    sintéticas, cada um com `fonte_sha`/`dll_sha` e o adaptador que o produziu. Se esse módulo
    não carregar (foi observado durante a edição concorrente do COR-AUT6 `t_6fcb39da`), a
    frente **não** é medida por outro avaliador: sai o critério canônico
    `AUT-6/avaliador-indisponivel`. O antigo `cenarios/tooltips_shrines.py` (hotspot de outro
    trabalho) **não** substitui a frente real — mediria por outras regras e poderia passar por
    integração do AUT-6. Nada do AUT-6 foi duplicado ou editado.
    **CORREÇÃO na COR-AUT7-F2 (achado A8):** essa preferência estava certa, mas na árvore
    entregue o módulo **não carregava** (`import prova` no topo de `aut6/cobertura.py` sem o
    diretório do pacote no `sys.path`), e a frente saía `AUT-6/avaliador-indisponivel` com
    **0 itens**; o número "21" também não era verificável (o arquivo mudou depois). Com o
    pacote no `sys.path` a frente real responde — **26 critérios** hoje
    (`COR-AUT7-F2-evidencias/adaptador-aut6.json`) — e a proibição do fallback foi mantida.
11. **Linguagem.** A frase "o número e a geometria estão medidos" saiu: o texto agora diz
    que **só a estrutura foi medida offline** e que números/geometria de runtime seguem
    **não comprovados**. `AUT-7-relatorio.md` e `AUT-7-resultado.json` foram regerados com o
    texto honesto (hashes antes/depois abaixo).

## Verificação (execução 387, CLIs reais)

| prova | resultado |
|---|---|
| suíte da ferramenta de estilo | **22/22, exit 0** (era 16/16) |
| suíte do relatório de aceite | **14/14, exit 0** (era 10/10) |
| 8 variantes insuficientes do revisor (produtor→consolidador) | **0 OK**, **0 OK_VINCULANTE** (antes: 6 vinculantes) |
| contrato real com `\|` antes do `desc=` | **não reprovado** (antes: falso REPROVADO) |
| cache com suíte real | 12 OK de BetterFont |
| cache após trocar `BetterFont/Plugin.cs` por fonte inválida | `cache_valido=false`, **0 OK**, **0 vinculante**, fonte restaurada |
| frentes vazias | `por_frente` AUT-5=1, AUT-6=1 com lacunas `AUT-5/resultado-vazio`, `AUT-6/resultado-vazio` (antes: 0) |
| linhas do FONTE do produto (`.cs`) com ` | ` ou `desc=` | **73 medidas** (predicado `' | ' in linha or 'desc=' in linha`, 2 patches do RoguelikeDebugger); reconhecidas pelo `LINE` do censo: **0** — é fonte C#, não log. Cada número agora vem com o predicado que o produz: **68** têm `' | '`; **5** têm `desc=` **sem** `' | '` (era este o número que a 2ª rodada da revisão não conseguia reproduzir pelo rótulo "predicado estrito" — com `'" | "'` literal dá **0**). Lista completa e predicados em `COR-AUT7-F2-evidencias/dump-do-produto.json`. **Frase corrigida na COR-AUT7-F2 (achado A5): antes dizia "73 reconhecidas pelo parser real", que era falso.** |

Prova completa: `evidencias/refutacao-cor-aut7.json` (+ `*.stdout`/`*.stderr` de cada CLI).

> **Nota da COR-AUT7-F2 (achados A9/A5):** este relatório citava `evidencias/adaptador-aut6.json`
> e `evidencias/docs-antes.txt` como prova — **nenhum dos dois foi entregue** (nem no repo, nem no
> ZIP). As provas faltantes foram produzidas e entregues pela COR-AUT7-F2 em
> `docs/automacao/COR-AUT7-F2-evidencias/adaptador-aut6.json` (reuso real do AUT-6, 26 critérios)
> e `docs/automacao/COR-AUT7-F2-evidencias/docs-antes.txt` (hashes antes/depois dos docs
> regerados); o artefato do número das 73 linhas é
> `docs/automacao/COR-AUT7-F2-evidencias/dump-do-produto.json`.

## Hashes

| arquivo | antes (AUT-7/AUT-7R) | depois (COR-AUT7) |
|---|---|---|
| `tools/automacao/estilo/estilo_atributos.py` | `d3450972…c3dc` | `17066cfa…8c22` |
| `tools/automacao/estilo/test_estilo_atributos.py` | `2e35e30f…ed50` | `3ef52c20…9bf1` |
| `tools/automacao/aceite/relatorio_aceite.py` | `01eefeff…7e3d` | `13bc565c…9767` |
| `tools/automacao/aceite/test_relatorio_aceite.py` | `2baf1e8d…3d3d` | `29ce8d33…41d8` |
| `docs/automacao/AUT-7-relatorio.md` | `f16b4f39…7808` | `6ef85b4d…5849` |
| `docs/automacao/AUT-7-resultado.json` | `a4dbdc04…4d95` | `af5b1279…728c` |

Os dois fontes batiam exatamente com os hashes do parecer AUT-7R antes desta correção
(nenhum drift concorrente nas ferramentas). Os documentos gerados foram **regerados** pela
ferramenta corrigida; os hashes antigos ficaram registrados **apenas no texto deste relatório** —
o arquivo `evidencias/docs-antes.txt` citado aqui nunca foi entregue (achado A9, fechado na
COR-AUT7-F2 com o artefato `docs/automacao/COR-AUT7-F2-evidencias/docs-antes.txt`).

## O que esta correção NÃO prova

Nada de runtime: nenhum critério de jogo foi aprovado, o censo não foi regenerado, o painel
de atributos e os números `base (final)` seguem **INDETERMINADO/LACUNA**, e o aceite humano
de UI/UX permanece `NAO_PRONUNCIADO`. `consolidacao_final` segue **PROVISORIA** (AUT-3R/5R/6R
pendentes). Mods não foram fechados.

## Como reproduzir

    python tools/automacao/estilo/test_estilo_atributos.py
    python tools/automacao/aceite/test_relatorio_aceite.py
    python tools/automacao/estilo/refutar_cor_aut7.py
    # evidencias: docs/automacao/COR-AUT7-evidencias/ (+ relatorio refutacao-cor-aut7.json)

O `refutar_cor_aut7.py` também é entregue em `tools/automacao/estilo/refutar_cor_aut7.py`
(sha256 `fdc3456f…a356`), dentro do escopo desta correção.

Refutação e testes são offline (`--sem-suite` ou suíte real do projeto); nenhum passo toca o
jogo, o perfil, o save ou a Thunderstore.
