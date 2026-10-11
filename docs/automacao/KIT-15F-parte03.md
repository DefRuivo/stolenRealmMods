# KIT-15F — parte 03: correção do achado F11 (contra-prova com veredito falso)

Cartão: t_d83f3ef6. Data: 10/10/2026 (UTC-03:00).
Rodada de provas: **run689**. Instância implementadora: `default/run689` (mesma linhagem implementadora
de run686/run687; **não** run678/run685, que são os revisores).
Origem do achado: revisão independente **run688** (revisor ≠ implementador) que devolveu
`changes_requested` com **um** achado bloqueante, de F11, descrito no comentário do cartão.

## O achado (verbatim, resumido)

> A contra-prova depende de ONDE fica o sandbox, e no layout do AUTOR (com TMPDIR definido) reporta
> uma falha que NÃO existe. … o baseline é verde (18/18) mas a contra-prova declara FALHOU: um
> "sinal que não é efeito". … `test_15` mistura DOIS resolvedores … Ex.: `test_15` resolver o layout
> por UMA única fonte (coerente com a resolução usada na verificação).

## Reprodução do falso vermelho (antes da correção) — medição própria

Comando do guia, no repositório do autor, com `TMPDIR` definido:

    python tools/automacao/kit15/contra_prova_kit15.py        -> exit 1
    CONTRA-PROVA|FALHOU|baseline=False|recusados=1/7|sandbox=C:\...\Temp\kit15-contra-050117

O `log-baseline.txt` da sandbox (prova lida do arquivo, não da mensagem):

    FAIL: test_15_descoberta_sem_usuario_fixo (__main__.TesteDescoberta...)
    AssertionError: 'padrao-repo' != 'padrao-home'

A suíte rodava 18/18 OK ao mesmo tempo, e os 6 defeitos restantes apareciam como
`ALVO-DIVERGENTE` (cicatriz do mesmo defeito: em toda cópia mutada havia uma falha extra, a do teste
mal resolvido). Cópia bruta preservada em `scratch/kit/KIT-15F-run689/01-contra-antes.txt` e
`00-suite-antes.txt`.

## Causa raiz

Dentro de `test_15_descoberta_sem_usuario_fixo` a expectativa do padrão era perguntada ao resolvedor
**errado**:

    tem_layout_repo = descoberta.raiz_do_repositorio(descoberta.AQUI) is not None   # local da CÓPIA
    ...
    destino, origem = descoberta.destino_do_kit(ambiente=ambiente)                  # usa raiz_efetiva (env)

`raiz_efetiva` honra `KIT15_RAIZ`/`KIT_RSTV_RAIZ` do processo; `raiz_do_repositorio(AQUI)` só olha o
caminho da cópia. A contra-prova exporta `KIT15_RAIZ=<raiz do repo>` e, por padrão, coloca a sandbox
em `TMPDIR/kit15-contra-*` — **fora** da árvore. Logo os dois resolvedores divergiam exatamente quando
o sandbox saía da árvore: expectativa `padrao-home`, implementação `padrao-repo`.

## Correção (mínima, um único arquivo de produto)

`tools/automacao/kit15/teste_kit15.py` — `TesteDescoberta.test_15_descoberta_sem_usuario_fixo`.
A expectativa passa a ser calculada **das mesmas duas fontes que o contrato define**, e de forma
independente da implementação (o teste não pergunta ao código sob teste qual é o layout):

    raiz_declarada = <KIT15_RAIZ|KIT_RSTV_RAIZ do processo, se for raiz de repo válida>
    raiz_acima_da_copia = descoberta.raiz_do_repositorio(descoberta.AQUI)
    raiz_esperada = raiz_declarada or raiz_acima_da_copia
    destino, origem = descoberta.destino_do_kit(ambiente=ambiente)
    if raiz_esperada:  esperado = <raiz_esperada>/dist/kit-rstv  (origem "padrao-repo")
    else:              esperado = <HOME>/kit-rstv                (origem "padrao-home")

Escolha de projeto registrada: **não** virou `template_layout = descoberta.raiz_efetiva(...)`. Isso
deixaria o teste tautológico (nunca pegaria uma `raiz_efetiva` que deixasse de honrar a env). Com a
expectativa derivada das duas fontes, o teste continua discriminando — prova no controle positivo 6
abaixo. Nenhum outro arquivo de produto mudou (`descoberta.py` intacto, hash igual ao do revisor).

## Prova de que o defeito NÃO se move com o sandbox (matriz de localização)

Mesmo comando, três localizações de sandbox, veredito lido de `contra-prova.json`:

| Invocação (cwd = repositório do autor) | sandbox | veredito | baseline | recusados |
|---|---|---|---|---|
| `python tools/automacao/kit15/contra_prova_kit15.py` (default, `TMPDIR` definido) — **a repro do revisor** | `C:\Users\…\Temp\kit15-contra-*` | **OK** | true | 7/7 |
| `bash tools/automacao/kit15/roda_testes_kit15.sh` (invocação de guia) | idem (default) | **VERDE**, exit 0 | — | 7/7 |
| `python …/contra_prova_kit15.py --saida …/KIT-15F-run689/contra-dentro` | dentro da árvore | **OK** | true | 7/7 |
| `python …/contra_prova_kit15.py` com `TMPDIR` **ausente** (default cai em `./scratch`) | `…\stolen-realm\scratch\kit15-contra-*` | **OK** | true | 7/7 |

E a invocação documentada no repositório do autor:

    bash tools/automacao/kit15/roda_testes_kit15.sh  ->  KIT-15 RESULTADO|VERDE|suite=0 contra-prova=0   (exit 0)

Antes: `FALHOU` / `VERMELHO` exit 1. Agora o veredito é o **mesmo** nas três localizações e verde na
invocação de guia — o sinal voltou a ser efeito.

## Controles de F11 (o que continua reprovando)

1. **Negativo** — isca autossuficiente (`f11-bait/`) que quebra o módulo antes de rodar qualquer
   teste: `veredito=FALHOU`, `baseline_verde=false`, `por_veredito={"FALSO-VERDE": [D1..D7]}`,
   exit **1**. Suite quebrada/0 testes segue **não** sendo RED aprovado.
2. **Positivo (novo nesta rodada)** — cópia **fora** da árvore + `KIT15_RAIZ=<repo>` com
   `raiz_efetiva` mutada para ignorar o ambiente: a suíte roda 18 testes, `failures =
   [test_15_descoberta_sem_usuario_fixo]`, **0 ERROR / 0 skip**, exit 1; a cópia intacta na mesma
   localização volta verde. Ou seja: o teste continua pegando a quebra do contrato (não ficou
   tautológico), e o controle é honesto porque a cópia está fora da árvore — sem isso o mutante
   acertaria por acaso, subindo até o repo.

## Re-execução integral após a correção (run689)

| Prova | Oráculo/origem | Resultado |
|---|---|---|
| Oráculo de revisão | cópia byte a byte de `KIT-15R-run678/test_review_kit15.py` sha `1efb6c18…6a449` | **27 OK / 0 FAIL / 0 ERROR / 0 skip**, exit 0 |
| Oráculo extra | cópia byte a byte de `KIT-15R-run678/test_extra_kit15.py` sha `e68eb481…9d56` | **3 OK**, exit 0 |
| Suíte do autor | `tools/automacao/kit15/teste_kit15.py` | **18 OK**, exit 0 |
| Contra-prova | `contra_prova_kit15.py` | **7/7 recusados**, exit 0 (3 localizações) |
| F1 identidade | `verify_f1_run689.py` | 42 membros, 41 payload, **0 divergentes**, 0 sem origem, 0 sobra, `descoberta.py` no ZIP = `10dd2e62…` = fonte viva |
| F7 | layout extraído, `pacote.py verificar` **sem** `--json` | `PACOTE|OK|{…}` exit 0 (e com `--json` exit 0) |
| F8 | layout **extraído fora da árvore** (nenhum ancestral tem `tools/automacao`) | suíte 18 OK; contra `base=<extraído>` 7/7 OK; shell `KIT-15 RESULTADO|VERDE` — todos exit 0 |
| F4 | CLI no extraído: instalar → status → remover → rollback → status | `INSTALADO 41` → `AUSENTE` → `INSTALADO 41`, rc 0 |
| F10/F12 | oráculos do revisor (imutáveis) | verdes (ver tabela) |

Nota de ambiente (honesta, não é produto): no Windows `subprocess.run(["bash", …])` resolve pelo
`CreateProcess` (`System32` antes do `PATH`) e o bash do WSL não lê `C:\…`. As provas que chamam
`bash` rodaram com o bash do Git/MSYS resolvível pelo **diretório de trabalho** do processo
(`shim/` no run686/687 e neste run689). O mesmo arranjo é declarado na doc do pacote como
não medido.

## Hashes (run689)

| Arquivo | sha256 |
|---|---|
| `tools/automacao/kit15/teste_kit15.py` (corrigido) | `72caddfbffa0538592c7a61ede1494ca4d9215815c0301f684d0a9994e332ef7` |
| `tools/automacao/kit15/teste_kit15.py` (antes, run687) | `57473e60383f48eb7ff3867962e6ccffcab20ce9493a12239ba810f01931310d` |
| `tools/automacao/kit15/descoberta.py` (inalterado) | `10dd2e6275152cd6fd93f49edd86e2e6d7c0ff3dea73326ee7884f0482ad1c86` |
| `tools/automacao/kit15/CHANGELOG.md` (nota da correção) | `ba6c72971b8eff7c1f9e29250ee17626b2638e1ff3970439aa44533e01c9c6c8` |
| Demais arquivos do kit | idênticos ao run687 (ver `scratch/kit/KIT-15F-run689/hashes-produto.json`) |
| Pacote regerado | `scratch/kit/KIT-15F-run689/pacote-proprio/kit-rstv-0.1.0.zip` sha256 `197cb1efeb2ea814a9ccfed9115cda3b956bec5728347fcf24c3fd89cdc1a00b`, 175059 bytes, 42 membros, `testzip` OK, `scan_total=0`, `PACOTE_LIMPO` |

O sha256 do ZIP **não é determinístico** (o zip guarda carimbo de data/hora por membro: builds
seguidas dão shas diferentes com o mesmo conteúdo). Por isso a prova de F1 é a identidade **membro a
membro** contra a origem viva — 0 divergências —, não o sha do arquivo.

## Limites (não medido)

Runtime no jogo/BepInEx/UI, build e deploy C#, segundo host, Linux/macOS, publicação, gates humanos e
DoD. Nesta rodada: nada instalado no perfil do dono, nenhum jogo aberto/fechado, nenhum save tocado,
nenhum push/tag/Release/Thunderstore, build C# não executado. Baselines `KIT-15R-run678/` e
`KIT-15R-run685/` preservados (não sobrescritos). Esta correção **não** é aprovação do produto e
**não** desbloqueia KIT-G2 `t_f19310d3`, KIT-14 `t_a1f38855` nem KIT-G4 `t_b001720d`.
