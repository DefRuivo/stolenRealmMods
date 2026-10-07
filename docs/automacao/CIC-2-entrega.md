# CIC-2 — entrega: consolidacao da decisao e roteiro humano RESIDUAL

Tarefa: `t_fd25da44` (CIC-2). Contrato de referencia: `docs/automacao/CICLO-VALIDACAO-escopo.md`
(secao "Contrato de integracao minimo (v1)"), sob `docs/SUPERVISAO.md` e `docs/PROCESSO-REVISAO.md`.

**Escopo entregue (exclusivo):** `tools/automacao/ciclo/decisao.py`, `tools/automacao/ciclo/test_decisao.py`
e este documento. Nao criei `__init__`/README compartilhado, nao toquei em `ciclo.py` nem em `cenarios/`,
nao mutou board/`KANBAN.md`, nao houve build/deploy/install/jogo/save/commit/push/publicacao.

## O que o modulo faz

`consolidar(criterios, identidade, aceite_humano=None) -> dict` classifica CADA criterio e separa
tres estados que nao se misturam:

| classificacao | significado | vai para |
|---|---|---|
| `OK_VINCULANTE` | prova real: nao-fixture + evidencia existente + identidade suficiente/hashes batem | base da decisao |
| `FALHA_AUTOMATICA` | defeito ou lacuna **automatizavel** | `falhas_automaticas` (volta ao ciclo, **nunca** ao dono) |
| `PENDENCIA_HUMANA` | so o dono resolve: `autorizacao` de rodada OU `julgamento_visual` residual | `pendencias_humanas` (curto) |
| `NAO_CONTA_COMO_PROVA` | `fixture`: testa o avaliador, nao o produto | registro (nao decide) |

Saida com as chaves do contrato — `por_mod`, `falhas_automaticas`, `pendencias_humanas`,
`pronto_para_decisao`, `aceite_humano`, `publicacao` — mais `roteiro_humano`, `resumo`,
`motivo_pronto_para_decisao`, `aceite_inconsistente`, `identidade`.

### Regra que nao se dobra: NUNCA OK por rotulo

Um criterio que se **declara** `OK` so conta como prova vinculante quando:

1. `procedencia != "fixture"` (fixture nunca prova o produto);
2. **a evidencia existe** — `evidencia` e lista de caminhos; caminho ausente/ilegivel/hash divergente
   invalida o OK;
3. **a identidade e suficiente** — `fonte_sha` **E** `dll_sha` (mesmo padrao de `cenarios/rstv.py`);
4. **os hashes declarados batem** — hash de bytes antigos = `REPROVADO` (aprovacao anterior invalidada);
   hash `*_sha`/`config`/`cenario` que a identidade **nao conhece** = falha automatica.

`identidade` aceita `{fonte_sha, dll_sha, artefatos:{nome:sha}, hashes:{nome:sha}}` — os dois ultimos
cobrem **config/cenario conhecidos**. Campos extras rastreaveis do criterio reconhecidos:
`hashes`, `julgamento_humano`, `requer_humano`, `instrucoes_humanas`.

### Reduzir o trabalho humano (nao empurrar falha automatizavel)

| estado do criterio | classe | decisao |
|---|---|---|
| `REPROVADO` | qualquer | `FALHA_AUTOMATICA` |
| `NAO_EXERCITADO`/`INDETERMINADO` | **offline** | `FALHA_AUTOMATICA` (automatizavel — **nao** vira tarefa do dono) |
| `NAO_EXERCITADO`/`INDETERMINADO` | runtime, identidade ok | `PENDENCIA_HUMANA` `autorizacao` |
| `OK` + `julgamento_humano` | runtime | prova vinculante **+** `PENDENCIA_HUMANA` `julgamento_visual` |
| `OK` sem evidencia / sem identidade / hash velho | qualquer | `FALHA_AUTOMATICA` (`REPROVADO`) |
| `fixture` `OK` | qualquer | `NAO_CONTA_COMO_PROVA` |
| identidade insuficiente (`NE`/`OK`) | qualquer | `FALHA_AUTOMATICA` (anexar identidade) |
| mod so com criterios nao-vinculantes | — | falha sintetica `"<mod>:sem-prova-vinculante"` |

`pronto_para_decisao` = **sem falha automatica E existe prova vinculante ou pendencia humana**.
`aceite_humano` e `publicacao` ficam em campos **separados**, por padrao `NAO_PRONUNCIADO` e
`NAO_VERIFICADO`; aceite marcado como `aceito` num mod com falha automatica vira `aceite_inconsistente`
(nunca esconde a falha). O roteiro humano e **agregado por `(mod, tipo)`** — no maximo um item por mod+tipo,
com a lista de ids — para nao replicar o checklist inteiro.

## Comandos reais e exit codes

Teste (77 checagens, inclui CLI real em subprocesso):

```
$ python tools/automacao/ciclo/test_decisao.py
total: 77 | falhas: 0
TUDO OK
$ echo $?          # 0 = tudo verde; 1 = reprovou; 2 = nao rodou
```

CLI (caso misto real, 5 criterios: build OK vinculante, conferidor offline NAO_EXERCITADO, runtime
NAO_EXERCITADO, runtime OK com julgamento visual, fixture):

```
$ python tools/automacao/ciclo/decisao.py \
    --criterios criterios.json --identidade identidade.json --repo <DIR> \
    --resultado saida.json --texto
EXIT=1   # 1 = ha falha automatica que volta ao ciclo
```

Trecho real do `--texto` (residual curto; nada do checklist completo):

```
ROTEIRO HUMANO (residual) — 2 item(ns):
- [BetterTooltips] JULGAR visual/UX: Abrir o jogo no alvo do criterio e confirmar a aparencia/UX; registrar aceite humano (o dado tecnico ja esta provado). (criterios: RV-49-aura-perigo)
- [RoguelikeSkillTreeVisualizer] AUTORIZAR rodada runtime: Autorizar UMA frente runtime (AUT-4/5/6) e reexecutar o ciclo; sem autorizacao nada em jogo e lido. (criterios: RSTV-26-hover)

FALHAS AUTOMATICAS (voltam ao ciclo, NAO ao dono) — 1:
- [transversal] check_deploy_optin: criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)

PRONTO PARA DECISAO: NAO — NAO: 1 falha(s) automatica(s) volta(m) ao ciclo; nada disso vai ao dono
ACEITE HUMANO: NAO_PRONUNCIADO (estado separado)
PUBLICACAO: NAO_VERIFICADO (estado separado)
```

`resumo` do JSON: `{mods: 3, criterios: 5, ok_vinculantes: 1, falhas_automaticas: 1,
pendencias_humanas: 2, nao_conta_como_prova: 1}`. Outros exits exercitados nos testes:
sem criterios -> `2`; `--criterios` inexistente -> `2`; criterio REPROVADO -> `1`; tudo vinculante -> `0`.

## Prova de fogo (contra-prova)

O teste carrega o modulo por `CIC2_DECISAO` (default `decisao.py`). Plantei um mutante que **confia no
rotulo** (`identidade_suficiente -> True`, `_verifica_evidencia -> []`):

```
$ CIC2_DECISAO=<scratch>/decisao_mutante.py python tools/automacao/ciclo/test_decisao.py
total: 77 | falhas: 10
REPROVADAS: OK sem evidencia...; evidencia ausente...; identidade insuficiente...; por_mod BetterTooltips com falha
EXIT=1
$ python tools/automacao/ciclo/test_decisao.py     # modulo real
total: 77 | falhas: 0   TUDO OK   EXIT=0
```

Ou seja: os testes **reprovam** quando a verificacao da prova e removida, e passam com ela — nao sao
decoracao. Os tres controles negativos de `test_decisao.py` cobrem exatamente os tres buracos do aceite
(fixture, evidencia, hash/identidade).

## Integracao (para CIC-1 / pai)

- `ciclo.py` chama `consolidar(criterios, identidade={fonte_sha,dll_sha,...})` quando o modulo existir e
  consome `falhas_automaticas` como a **fila de correcao** (cada item traz `id`, `mod`, `motivo_decisao`,
  `problema(s)`, `tarefa_origem`); nova rodada apos correcao.
- O roteiro humano (`roteiro_humano.itens`) e o que se mostra ao dono — autorizar rodada / julgar visual —
  sem reabrir diagnostico tecnico.
- `aceite_humano` e `publicacao` entram como entradas/saidas **separadas**; a automacao nunca as infere.

## Lacunas e limites (honestos)

- **Nenhuma rodada runtime, build ou jogo.** So execucao offline/pura e CLI em scratch. `runtime OK`
  nos testes usa evidencia de arquivo local plausivel, nao medicao de jogo — a prova de runtime real
  depende das frentes AUT-4/5/6 autorizadas.
- A conferencia de evidencia exige que o caminho **exista** no disco (`--repo`); evidencia que seja
  descricao livre (nao-caminho) sera tratada como ausente — fail-closed por desenho.
- `procedencia`/`classe` fora dos enums do contrato viram `FALHA_AUTOMATICA` (malformado), nao silencio.
- `pronto_para_decisao` reflete **so** a automacao; ele nao e aceite nem publicacao (campos separados).
- Nao integrei ao runner `tools/testes/roda_testes.py` (pertence ao pai): `test_decisao.py` roda sozinho
  com exit 0/1/2 e linhas `RESULTADO|...`, como o resto de `tools/automacao/`.
- `docs/automacao/CIC-2-entrega.md` e o unico doc escrito; `decisao.py`/`test_decisao.py` nao referenciam board.

## Hashes SHA-256 dos entregaveis (working tree, branch `ci-validate-test`)

```
836b08c811abef6d9a48d0e6258602d74695c3072d673a82f6d9fd1ea608cd48  tools/automacao/ciclo/decisao.py
699ab82e59154a5e0d5c8970f32dc2018e6c207ef4c48aeda04721fc6a2ff3c7  tools/automacao/ciclo/test_decisao.py
```
