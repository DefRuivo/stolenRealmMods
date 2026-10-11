# KIT-12 — ENTREGA: costura alteracao -> cenarios pertinentes -> coleta -> avaliadores -> relatorio

Cartao: `t_0a434c97` · Run: 667 · Autor: `default` (implementador) · Worktree: `C:/dev/stolen-realm`
Escopo: `tools/automacao/kit12/**` + `docs/automacao/KIT-12-*.md` + provas em `scratch/kit/KIT-12-run667/**`.
Rodada **OFFLINE**: nenhum build, nenhum jogo, nenhum save, nenhum probe instalado, nenhum commit/push,
nenhuma publicacao, nenhuma DLL proprietaria.

## 1. O que foi entregue (arquivos + sha256)

```
f49a0d4059af33002ce52b463ad6be7091063ee6d661d746498072545c1a3599  tools/automacao/kit12/integracao.py
b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320  tools/automacao/kit12/pertinencia.json
c57ad7980754ab53c2bbc18368ced23acda0bf6b6649a35d4bf8955814870b77  tools/automacao/kit12/test_kit12_integracao.py
1748f7c5da3180540f18562d99ab72004839ed04e1581bb9abbb03912175e64b  tools/automacao/kit12/prove_ciclo.py
8a6f165c3225a2e9469be6d22047165c75aac376f9219b96bb8a22f1f5ca9bc4  scratch/kit/KIT-12-run667/prova.json
```

| arquivo | papel |
|---|---|
| `kit12/pertinencia.json` | DADO declarativo: `mod -> cenarios/frentes/fonte`. Trocar pertinencia nao exige codigo. |
| `kit12/integracao.py` | A costura (reuso por caminho de CIC-1/CIC-2/KIT-10/AUT-7) + CLI. |
| `kit12/test_kit12_integracao.py` | Suite offline (unittest) + `--isca` (mutacao seletiva do fonte). |
| `kit12/prove_ciclo.py` | Demonstracao real da CLI em sandbox: fixture marcada -> defeito -> correcao -> revalidacao. |

## 2. Contrato da costura (`integracao.cadeia()`)

- **IDENTIDADE UNICA** `fonte_sha` + `dll_sha` + `config_sha` + `versao` + `sessao`, agregados em
  `cadeia_sha`; os cinco campos e o `cadeia_sha` sao ANEXADOS a **cada criterio**, a **cada item da fila**
  e ao **relatorio**. A mesma identidade atravessa pertinencia -> coleta -> avaliadores -> decisao -> fila.
- **PERTINENCIA**: `mods_alterados()` (git status + `--base`; ou `--alterados`/`--mod` explicito) ->
  `mapear()` -> `{mod: cenarios/frentes/fonte}` + `nao_mapeados`. Arquivo alterado SEM mapa, mod sem
  observacao coletada e observacao de mod nao pertinente **nao desaparecem**: viram lacuna/registro declarado.
- **AVALIACAO**: `kit10_cenarios.avaliar(observacoes_pertinentes, identidade)` (avaliador REAL, reusado).
  Criterios de mod CONHECIDO nao alterado saem em `fora_da_pertinencia` (declarados, nao somados ao mod);
  `transversal`/mod desconhecido FICA (lacuna da avaliacao nao some).
- **LACUNA x DEFEITO**: `REPROVADO` -> exit 1; lacuna tecnica (`NAO_EXERCITADO`/`INDETERMINADO`) -> exit 2
  (volta ao AGENTE). Humano so recebe o que o criterio declarar como `autorizacao`/`julgamento_visual`
  (regra do `decisao.py`, nao reimplementada).
- **FILA DECLARATIVA**: reusa `ciclo.montar_fila` + `ciclo.fila_da_decisao`; cada item com
  `criterio`, `causa`, `caminhos`, `prova`, `instrucao`, `tarefa_origem`, `requer_nova_rodada`,
  `execucao_automatica: false`. Qualquer campo executavel (`comando/argv/shell/exec/cmd/subprocess/...`)
  e MOVIDO para `propostas_nao_executadas`; **nao existe caminho de execucao neste modulo**.
- **TENTATIVAS**: `ciclo.avaliar_tentativas` (numero, limite, sem-progresso) + `avaliar_escalonamento`
  (destino `supervisor`, nunca o dono).
- **INVALIDACAO**: `invalidar_anterior` compara `fonte_sha/dll_sha/config_sha/versao` guardados com os
  atuais -> exit 3 (`--verificar`).
- **ESTADO/EXIT**: 0 `APROVADO_OFFLINE` · 1 `REPROVADO`/`ESCALADO` · 2 `INCOMPLETO` · 3 `INVALIDADO_POR_MUDANCA`.
  Avaliacao VAZIA (zero criterios) **nao** aprova: INCOMPLETO/2.

## 3. Provas reais (comandos, exits e arquivos lidos de volta)

### 3.1 Suite offline (sandbox propria, fora do repo)

```
python tools/automacao/kit12/test_kit12_integracao.py
-> Ran 18 tests ... OK   (exit 0)
```

18 testes: 4 positivos (cadeia completa com identidade anexada; APROVADO_OFFLINE com criterio OK offline
e evidencia REAL; determinismo do JSON canonico entre duas rodadas) e 14 controles negativos:
arquivo sem mapa; observacao fora da pertinencia; coleta ausente; fixture REPROVADA com causa na fila;
correcao controlada revalidando; sem-progresso; limite de tentativas escalando ao supervisor;
campo executavel nao executado; config/versao invalidando; identidade insuficiente derrubando OK;
avaliacao vazia; avaliador que levanta excecao virando lacuna transversal preservada; pertinencia por mapa;
declaracao incoerente do avaliador virando lacuna nomeada.

### 3.2 Isca (mutacao SELETIVA do fonte, nao `AssertionError` artificial)

```
python tools/automacao/kit12/test_kit12_integracao.py --isca
ISCA|fixture_pode_aprovar|test_neg_identidade_insuficiente|exit=1
ISCA|fila_executa_campo|test_neg_campo_executavel|exit=1
ISCA|invalidacao_desligada|test_neg_config_mudou|exit=1
ISCA|nunca_incompleto|test_neg_correcao_controlada|exit=1
ISCA|sem_progresso_desligado|test_neg_limite|exit=1
ISCA|sem_anexar_cadeia|test_positivo_cadeia_completa|exit=1
ISCA|controle_restaurado|test_positivo|exit=0
ISCA|mutacoes_discriminadas=6/6|falhas=0        (exit 0)
```

Cada mutante derruba EXATAMENTE o teste-regressao do guard mutado; o controle restaurado volta verde.
Os mutantes rodam numa arvore `tools/` ESPELHADA em area externa (o modulo resolve os irmaos por
`__file__`; mutar num diretorio solto quebraria por ausencia de irmao, nao pela mutacao).

### 3.3 CLI integrada em SANDBOX (copia de `tools/` + mod de fixture + `git init`)

```
python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12-run667
1-fixture-marcada                    | exit=2 | estado=INCOMPLETO
2-defeito-plantado                   | exit=1 | estado=REPROVADO
3-correcao-controlada                | exit=2 | estado=INCOMPLETO
4-verificar-apos-mudanca-de-config   | exit=3 | (resultado guardado INVALIDADO)
PROVA|PASSOU|C:\dev\stolen-realm\scratch\kit\KIT-12-run667\prova.json      (exit 0)
```

Itens lidos de `prova.json` e dos resultados JSON:

- **defeito** (`fonte`/`texto_renderizado` "10 (99)"): criterio `KIT-10/atributos/base-vs-final/Attributes_Text`
  = `REPROVADO`, e o item da fila traz `causa: BetterStats/Plugin.cs`, `caminhos: [BetterStats/Plugin.cs]`,
  `prova: [coleta-fixture-defeito.json, BetterStats/Plugin.cs]`, `roteamento: causa`,
  `execucao_automatica: false`, `instrucao: "corrigir a CAUSA em BetterStats/Plugin.cs ... o ciclo NAO
  executa comando de correcao"`.
- **correcao controlada** (observacao regravada "10 (15)"): `REPROVADO=0`, `OK=0`, `com_prova_runtime=0`,
  criterio volta a `NAO_EXERCITADO` -> a fixture continua fixture; nada foi promovido a verde.
- **invalidacao**: com a config mudada, `--verificar` sai 3 com motivo `config mudou desde a rodada anterior`.

Provas em `scratch/kit/KIT-12-run667/`: `prova.json`, `ciclo-resultado{,-defeito,-corrigido}.json`,
`coleta-fixture-{ok,defeito}.json`, `com.gumatos.betterstats.cfg`, 4 arquivos `*-saida.txt` (stdout real da CLI).

### 3.4 Travas do repo

```
python tools/check_segredos.py         -> exit 0
python tools/check_padroes_segredo.py  -> exit 0
python tools/check_dupes.py            -> exit 0
python tools/audita_docs.py            -> exit 0 ("nenhuma inconsistencia encontrada")
```

## 4. Aceite, item por item

| criterio do cartao | veredito | prova |
|---|---|---|
| hash/versao/config/sessao atravessam toda a cadeia | PASSOU | `test_positivo_cadeia_completa_*` (cadeia_sha/fonte/dll/config/versao/sessao em cada criterio; `cadeia_sha` na fila e no relatorio) |
| mudanca invalida aprovacao anterior | PASSOU | `test_neg_config_mudou_*`, `test_neg_versao_diferente_invalida`, etapa 4 da CLI (exit 3) |
| lacuna tecnica volta ao agente; humano so residual | PASSOU | `NAO_EXERCITADO` -> exit 2 e item na fila com `quem_executa: agente`; humano so com `tipo_pendencia` explicito (na CLI: 1 item de `julgamento_visual`) |
| fila declarativa com paths/criterio/prova, limite e sem-progresso | PASSOU | `test_neg_fixture_reprovada_*`, `test_neg_sem_progresso_*`, `test_neg_limite_de_tentativas_*` (destino `supervisor`) |
| nao executar comando LLM arbitrario | PASSOU | `test_neg_campo_executavel_*` (com `subprocess.run` instrumentado para explodir; campos movidos p/ `propostas_nao_executadas`); a isca derruba o guard |
| validacao/relatorio deterministicos sem IA | PASSOU | `test_determinismo_duas_rodadas_*`; stdlib apenas, sem rede/IA; relatorio via `relatorio_aceite.montar_relatorio`/`texto_do_relatorio` |
| integracao Hermes opcional | PASSOU | nenhum caminho do modulo depende de Hermes/IA; corre por `python ... integracao.py`/`prove_ciclo.py` |
| CLI integrada em sandbox com fixture marcada | PASSOU | secao 3.3 (sandbox externa ao repo, `git init`, DLL de fixture DECLARADA) |
| erro -> correcao controlada -> revalidacao | PASSOU | secao 3.3, passos 2 e 3 (exit 1 -> exit 2, defeito some, nada vira OK) |
| sem fingir runtime | PASSOU | fixture marcada -> `rebaixar_ok` + `com_prova_runtime=0` em todos os passos; nenhuma observacao runtime foi fabricada |

## 5. Achados e lacunas (registrados, NAO maquiados)

1. **`kit10_cenarios._criterio(..., obs=None, ...)` quebra** quando um aspecto levanta: o caminho de
   erro chama `est._procedencia(None)` -> `AttributeError`, e a excecao escapa de `avaliar()` em vez de
   devolver o criterio `INDETERMINADO` previsto. Latente no repo (os oraculos carregam), exposto quando
   um oraculo de `tools/testes` nao importa. **Nao corrigido** (produto de outro cartao/rodada ja
   aprovada): a costura apenas garante o pre-requisito (`tools/testes` no `sys.path`) e, se ainda
   assim falhar, declara `avaliador/erro` transversal em vez de silenciar.
2. **Declaracao incoerente do AUT-7**: `estilo_atributos` emite criterios `classe=runtime` com
   `procedencia=execucao` (ex.: `AUT-7/BetterStats/runtime-base-vs-final`) quando ha observacao do tipo.
   O CIC-2 classifica isso como `REPROVADO` ("criterio incoerente") — um FALSO VERMELHO do produto.
   A costura normaliza: vira lacuna nomeada `avaliador/declaracao-incoerente/<id>` (agente), e o
   criterio ORIGINAL fica preservado em `declaracoes_incoerentes`. Acao recomendada: cartao de correcao
   no AUT-7 (fora do escopo deste cartao).
3. **Oraculos do avaliador**: `tools/testes/regras_*.py` fazem `import arcabouco`; a costura insere
   `tools/testes` e `tools/automacao` no `sys.path` antes de avaliar (pre-requisito do avaliador).
4. **Config dentro do repo entra no `fonte_sha`** (untracked). Para separar os campos, a prova usa
   config FORA do repo; comportamento declarado, nao escondido.
5. **Sandbox**: `tools/` e copiado para area externa (`%LOCALAPPDATA%/hermes/cache/scratch`), com
   `git init` local, sem `.git` remoto, sem perfil/credenciais/save do dono. Nenhum arquivo de `tools/`
   ou de mod foi editado.

## 6. NAO_EXERCITADO (declarado)

Jogo/probe/save/perfil real, runtime AUT-4, UI/UX e pixels, build C#/preflight de deploy, instalacao,
publicacao e aceite humano/DoD — **nada disso foi exercitado** (nem autorizado). Fixture testa o
avaliador; fixture NAO comprova runtime. Aprovacao tecnica **nao** e aceite humano nem publicacao.

## 7. Reuso (nada duplicado)

`ciclo.py` (CIC-1: identidade, snapshot, `montar_fila`, `fila_da_decisao`, tentativas, escalonamento,
invalidacao) · `decisao.py` (CIC-2: classificacao "nunca OK por rotulo", roteiro humano) ·
`kit10_cenarios.avaliar` (avaliador) · `relatorio_aceite.montar_relatorio`/`texto_do_relatorio`/`_revisoes`
(AUT-7) · vocabulario de `CAMPOS_EXECUTAVEIS` do KIT-11. Nenhum backend LLM novo; nenhuma engine de
avaliacao reimplementada.

## 8. Proximo passo sugerido

1. Revisao independente (cartao R `t_811b1717` / handoff nativo) refutando: fixture promovida a verde,
   fila executando campo de comando, invalidacao ignorada, criterio transversal sumindo na pertinencia.
2. Cartao de correcao no AUT-7 para a declaracao `classe=runtime`/`procedencia=execucao` (achado 2).
3. Cartao de correcao no KIT-10 para o caminho de erro com `obs=None` (achado 1).
4. Gate humano: autorizacao de UMA frente runtime (AUT-4) para sair do residual.
