# KIT-10F (t_48b78ecb) — parte02: correcoes F8–F12 e provas por execucao

Run665 (implementador, instancia nova != run663/revisor). Fonte corrigido:
`tools/automacao/kit10/kit10_cenarios.py` SHA256
`899e47595d2e86ed2dda1e5bc6c425c3a0f9a70db3974f899480fde64620507c` (baseline antigo
`8d3763a6944e7973549e908d63c04bcbf20ac70db6527bd681f2b6ecdc66d092`).

## O que mudou (tudo LOCAL, em `kit10_cenarios.py`; nenhuma dependencia compartilhada editada)

### F8 — medicao numerica invalida nunca OK (aspecto A)
Nova pre-guarda `_numero_finito` roda ANTES das comparacoes sobre `fonte_bonus`, `receptor_bonus`,
`maxhealth`, `dano_observado` e `contrib_observada`. NaN/inf/bool/string nao numerica -> **REPROVADO**
(valor presente, porem nao comparavel); AUSENTE continua **NAO_EXERCITADO** (lacuna de coleta).
Motivo: `abs(float('NaN') - esperado) > 1e-9` e False, entao a finitude/tipo tem de ser checada
explicitamente. Os ramos de ausencia (`if fonte is None`, `if dano is None`, `if not
receptor_exercitado`, `if contrib is None`) ficaram INTACTOS - inclusive para preservar o RED das
guardas antigas que muta esses trechos literais.

### F9 — contagem medida, aura canonica, dobro exercitado (aspecto B)
Novo `_inteiro_contagem` (sem default, sem coercao, sem truncamento): `instancias` exige inteiro
>= 1 MEDIDO; itens exigem inteiro >= 0. Aura tem de ser CANONICA (`regras_shrine.AURAS_DA_FAMILIA`
+ `auras_da_tabela()`). Sem um gatilho repetido (instancias >= 2) o "dobro" NAO foi exercitado ->
**NAO_EXERCITADO** declarado. Preservado o comportamento confirmado: 2 itens para 2 instancias de
gatilho e 1 item para aura de atributo (positivo com Dwarven 2/2 + Rogue 2/1 continua OK).

### F10 — toda linha DECLARADA do dump conferida (aspecto D)
O aspecto passou a iterar TODAS as linhas do log (nao so as que `censo.LINE` reconhece): linha
declarada do dump que o parser real nao reconhece (`[Status] Foo | desc="..."` sem as aspas do
`'nome'`) -> **REPROVADO** (o defeito nao pode ser descartado antes de avaliar). `|` DENTRO do
`desc` tambem reprova (o `contrato_da_linha` pula `desc`; o AUT-7 ja detecta essa classe).
Linhas nao-dump (sem `desc=`) seguem neutras; `linhas_reconhecidas` preservado.

### F11 — marca de fixture do envelope propagada failclosed
`avaliar` marca cada observacao (COPIA; input do dono intacto) quando o ENVELOPE ou a propria
observacao declara `procedencia=fixture`/`rotulo_fixture=true`/`sintetico=true`/`evidencia_runtime
=false`. A marca ja era honrada em `_fecha`; agora o envelope nao a perde. Vale tambem para os
avaliadores reusados CIC-4/AUT-7 (recebem a mesma lista marcada).

### F12 — aspecto E `KIT-10/atributos/base-vs-final` (cobertura)
Adaptacao OFFLINE minima e local: confronta o texto `base (final)` do BetterStats com os valores
MEDIDOS independentes `saved_map` (base pura do SavedMap) e `atributos_final` (final do motor) por
atributo+personagem. O `esperado` sai SEMPRE das medicoes, NUNCA do display. Positivo completo
exercitavel; negativos base errada / final errado / personagem troca / valor invalido; falta de
campos -> NAO_EXERCITADO. LACUNA TECNICA declarada: o probe/coletor ATUAL nao emite esses campos
(nada de probe/mod editado aqui). Nao foi criado mecanismo de coleta redundante.

## Provas reais (exit codes reais; resultados lidos de arquivo)

| prova | comando | saida real |
|---|---|---|
| Suite imutavel revisor (ANTIGO) | `python test_review_kit10.py` em `antigo/sandbox` | `Ran 45 ... FAILED (failures=10)` / exit 1 |
| Wrapper revisor (ANTIGO) | `python test_wrapper_metadata.py` em `antigo/sandbox` | `Ran 4 ... FAILED (failures=4)` / exit 1 |
| Suite imutavel revisor (CORRIGIDO) | idem em `novo/sandbox` | `Ran 45 ... OK` / exit 0 |
| Wrapper revisor (CORRIGIDO) | idem em `novo/sandbox` | `Ran 4 ... OK` / exit 0 |
| Autor | `python tools/automacao/kit10/test_kit10_cenarios.py` | `rodaram=28 reprovaram=0 nao_rodaram=0` / exit 0 |
| CIC-4 | `python tools/automacao/cenarios/test_tooltips_shrines.py` | `rodaram=28 reprovaram=0` / exit 0 |
| RED guardas antigas | `python scratch/kit/KIT-10-run659/prova_red_kit10_guardas2.py` | `PROVA-RED\|PASSOU\|7 mutacoes` / exit 0 |
| RED durável KIT-10F (F13) | `python scratch/kit/KIT-10F-run665/prova_red_kit10f.py` | `RESUMO\|PASSOU\|controles=13 guardas=9` / exit 0 |
| CLI lista fixture | `kit10_cenarios.py --observacoes scratch/kit/KIT-10-run/fixture.json` | exit 2, OK 0, NAO_EXERCITADO 19 |
| CLI envelope fixture (F11) | `--observacoes observacoes-envelope-fixture.json` | exit 2, OK 0, NAO_EXERCITADO 19 |
| Travas git | `check_segredos` / `check_padroes_segredo` / `check_dupes` / `audita_docs` | todos exit 0 |

### Driver obsoleto superado (F13)
`scratch/kit/KIT-10-run/prova_red_kit10.py` continua OBSOLETO (exit1: trechos de fonte/dano nao
existem mais) - declarado SUPERADO e NAO contado verde. O driver duravel vigente e
`scratch/kit/KIT-10F-run665/prova_red_kit10f.py`, que cobre A/B/C/D+E (positivos e negativos) e as
guardas novas F8/F9/F10/F11/F12, com restauracao byte-exata verificada por SHA.

### Guardas load-bearing (neutralizacao seletiva -> defeito escapa; restauracao byte-exata passa)
`prova_red_kit10f.json` registra, por guarda, `original=NAO-OK` e `neutralizado=OK/True`. 9 guardas
novas: F8 (NaN), F9 aura inventada / sem gatilho repetido / itens fracionario / instancias default,
F10 pipe no desc / linha nao reconhecida, F11 envelope fixture, F12 base errada. SHA do fonte vivo
reconferido byte-a-byte ao final do driver (nenhum `.pyc`/mutante deixado em disco).

### F4 (ressalva)
O teste de estilo historicamente variavel continua INDETERMINADO; nao foi tocado nem
"auditado" com mudanca no BetterFont, conforme o cartao.

## Preservacao
Sandboxes `antigo/sandbox` e `novo/sandbox` (1156 arquivos cada), SEM `.git`/DLL/PDB/
segredo/perfil (`inventario.json`, `perigos: []`). Suites do revisor copiadas intactas (SHA
e7eddb6f... / 2d3a40b5...). Nenhum `git add`/`commit`/`push`. Nenhuma alteracao em mod, gameplay,
probe ou runtime. Runtime real/jogo/save/perfil/UIUX/pixels/desempenho/build/preflight/deploy/
publicacao: NAO_EXERCITADO.
