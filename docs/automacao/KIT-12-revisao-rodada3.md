# KIT-12 — revisao independente da rodada 3 (run672, lente CONTRACT + execucao propria)

Cartao: `t_0a434c97` · revisor: `default run672` ≠ implementador `default run671` ≠ revisores
`run668` (rodada 1) e `run670` (rodada 2) · HEAD `d82894e` · repo `C:/dev/stolen-realm`.
Produto conferido byte a byte e **NAO editado pelo revisor**:

| arquivo | sha256 conferido |
|---|---|
| `tools/automacao/kit12/integracao.py` | `7785d8c1f624ff263b4ac89ad36e3ab9952db17d5a233d12affada091da8af87` (bate com o handoff) |
| `tools/automacao/kit12/test_kit12_integracao.py` | `25284c7075633042efc6445a5856d5a24e40d152ccdb593d6cb94d661e96da8c` |
| `tools/automacao/kit12/prove_ciclo.py` | `4fc01b81572bdfbbea4cc3af33f1fb845659f23bc689cc94068e2d85b973b750` |
| `tools/automacao/kit12/pertinencia.json` | `b77ca4b540c65fb0221412af5195d444844ec3f8915a45277e4c52d35602d320` |

Provas do revisor: `scratch/kit/KIT-12H-run672-rev/` (`suite-run672.txt`, `isca-run672.txt`,
`prove-672.txt`, `cli/`, `sondas_run672.py` + `sondas-run672.json`,
`sondas_run672b.py` + `sondas-run672b.json`, `verify-apos-mudanca-de-fonte.txt`,
`trava-*.txt`). Nenhum diretorio de rodada anterior foi sobrescrito.

## 1. Criterios de aceite do cartao (lente CONTRACT)

| criterio do corpo do cartao | verificacao REAL (comando/saida) | veredito |
|---|---|---|
| hash/versao/config/sessao atravessam toda cadeia | `integracao.py … --config <abs>` (det4): **25/25** criterios com `fonte_sha`, `dll_sha`, `config_sha`, `versao`, `sessao`, `dll_probe_sha`, `cadeia_sha`; itens da fila com o MESMO `cadeia_sha` da identidade (`True` nos 3 primeiros) | PASSOU |
| mudanca invalida aprovacao anterior | rodada A (exit 2) -> `--verificar` sem mudanca: **exit 0** ("resultado corresponde aos bytes atuais"); depois de alterar os bytes de `BetterStats/Plugin.cs` na sandbox: **exit 3**, `"fonte mudou … (antes=cda27009cf2f agora=ea0cc3cfd181): aprovacao anterior INVALIDADA"` (`verify-apos-mudanca-de-fonte.txt`) | PASSOU |
| lacuna tecnica volta ao agente; humano so autorizacao/julgamento residual | com envelope REAL: `pendencias_humanas=0`, `pronto_para_decisao=false` com motivo "25 falha(s) automatica(s) volta(m) ao ciclo"; no caso com defeito, `pendencias_humanas=1` e e **julgamento visual** (`tipo=julgamento_visual`), criterios tecnicos com `tipo_pendencia=coleta_tecnica`/`autorizacao_necessaria=false` | PASSOU |
| fila declarativa com paths/criterio/prova + limite + sem progresso | item da fila traz `criterio`, `caminhos`, `prova`, `evidencia`, `instrucao`, `execucao_automatica=false`, `quem_executa=agente`; R7 (4 rodadas, `--limite 2`): `numero` 1->2->3->4, `sem_progresso=true` na 2a com motivo ("mesma fonte … e mesmas falhas … nenhuma correcao mudou os bytes"), `ESCALADO/exit 1` ao exceder o limite | PASSOU |
| nao executar comandos LLM arbitrarios | `grep -nE "subprocess\|os.system\|eval(\|exec(\|requests\|urllib\|openai"` em `integracao.py`: so `subprocess.run(["git","status"/"diff", …])` com argv FIXO (sem `shell=True`, sem `check=True`, sem `git add/commit/push`); nenhuma primitiva de execucao de comando do agente; R9: campo executavel injetado em criterio nos 4 estados (OK/NAO_EXERCITADO/INDETERMINADO/REPROVADO) sai do criterio e e registrado em `propostas_nao_executadas` (`criterio_sanitizado=true`, `residuais=[]`) | PASSOU |
| validacao/relatorio deterministas, sem IA permanente | duas execucoes com a MESMA entrada: `det1.json` == `det2.json` byte a byte (descontado `gerado_em`), incluindo `relatorio_texto` (1745 chars) identico; relatorio vem de `relatorio_aceite.py` (AUT-7) reusado; nenhum cliente de rede/LLM no modulo | PASSOU |
| CLI integrada em sandbox com fixture marcada e erro->correcao->revalidacao | `prove_ciclo.py --out scratch/kit/KIT-12H-run672-rev/cli`: exits **2 -> 1 -> 2 -> 2 -> 2 -> 2 -> 3**, `veredito=PASSOU`, `problemas=[]`; todas as coletas `procedencia=fixture`/`rotulo_fixture`/`evidencia_runtime=false` e `com_prova_runtime=0`; etapa 4 = revalidacao (exit 3) | PASSOU |
| reuso de CIC-1/CIC-2/CIC-5 + `relatorio_aceite.py`, sem backend LLM novo | modulo carrega `ciclo.py`/`decisao.py`/`kit10_cenarios.py`/`relatorio_aceite.py` via `_modulo` e chama `c.identidade`, `c.montar_fila`, `c.fila_da_decisao`, `c.avaliar_tentativas`, `c.avaliar_escalonamento`, `dec.consolidar`, `a.montar_relatorio` — nenhuma copia de avaliacao/fila/relatorio | PASSOU |
| dependencias KIT-08R/KIT-10R/KIT-11R | `kanban_show`: pais `t_2a38d1d3/t_48b78ecb/t_70608c71/t_79c1525f/t_896796be/t_ac0f78f7` completos, `unsatisfied_parents=[]` | PASSOU |

## 2. Itens pedidos nas rodadas anteriores (reconferencia obrigatoria)

| item pedido | onde foi pedido | medicao do revisor run672 | veredito |
|---|---|---|---|
| F1 — procedencia confrontada, nada sobrescrito em silencio | run668 | R5: criterio declarando `fonte_sha`/`dll_sha` de OUTROS bytes -> criterio rebaixado a `NAO_EXERCITADO`, `declaracoes_contraditorias` com os dois campos, valor declarado PRESERVADO, lacunas `cadeia/declaracao-contraditoria/<id>/fonte_sha|dll_sha` | CORRIGIDO |
| F2 — campo executavel sai tambem do CRITERIO | run668 | R9 pelo caminho REAL (`cadeia()` com avaliador injetado, nos 4 estados): `campos_executaveis_que_sobrevivem_no_criterio=[]`, `criterio_sanitizado=true`, 3 propostas registradas por criterio | CORRIGIDO |
| F5 — confronto ligado ao campo canonico do INSTRUMENTO, nao a `fonte_sha` | run670 | R2 instrumento MEDIDO (`--probe-dll`): `confere` / `dll_probe_sha(medido)` / **zero** lacuna `cadeia/coleta-*`; R1 armadilha (`hash_fonte = fonte_sha` DA RODADA): `contraditoria` + `cadeia/coleta-contraditoria/hash_fonte`; R4 incoerente: `incoerente` + `cadeia/coleta-incoerente/hash_fonte`; fallback `hash_fonte or fonte_sha` ausente de `carregar_coleta` (l.483) | CORRIGIDO |

**Regressao exata do F5 (a prova mais forte desta rodada).** A evidencia REAL do produtor,
`docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json` (sha256
`5bef1c67e21365ccf84d02ff645715e254a4e1140aec77d62c6b12de689a158d`), copiada SEM ALTERACAO e
passada pela CLI (**R3** e `cli/ciclo-resultado-real.json`): `hash_fonte_confronto="confere"`,
`instrumento_origem="declarado-coleta"`, `instrumento_sha=407c5c63d9d7…`,
`lacunas_coleta=[]`. Isto e, o envelope que o produtor vivo escreve **nao e mais rebaixado** —
que era o defeito medido em run670 (S11 -> INCOMPLETO/2 em toda coleta legitima).

## 3. Reproducao das provas entregues (execucao do revisor)

| prova | comando | resultado |
|---|---|---|
| suite | `python tools/automacao/kit12/test_kit12_integracao.py` | `Ran 30 tests`, **OK, exit 0** |
| isca | `... --isca` | **14/14** mutacoes discriminadas, `controle_restaurado exit=0`, `falhas=0` |
| CLI sandbox | `python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12H-run672-rev/cli` | exits **2->1->2->2->2->2->3**, `PROVA\|PASSOU` |
| travas | `check_segredos.py`, `check_padroes_segredo.py`, `check_dupes.py`, `audita_docs.py` | **exit 0** cada |

## 4. Achados

Nenhum achado bloqueante. Dois achados **nao bloqueantes**, ambos pre-declarados pelo
implementador em `KIT-12G-entrega.md` secao 5:

1. **F3/F4 (divida declarada, fail-closed):** REPROVADO com par classe/procedencia incoerente vira
   lacuna (um vermelho real nao fica vermelho); `--verificar` sem `--config` da exit 3 sem mudanca
   real. Nao tocados nesta rodada; nao afetam os criterios de aceite (medido: sem `--config` o
   produto declara motivo, nao finge verde).
2. **Instrumento apenas DECLARADO:** sem bytes do probe em disco, a procedencia e aceita como
   DECLARACAO (`coleta.instrumento_origem=declarado-coleta`, em `resultado["limites"]`). Medicao
   independente exige `--probe-dll` ou `identidade.arquivo_dll_do_probe` presente. Limitacao real
   e honestamente declarada; sem ela o envelope real do produtor voltaria a ser impossivel de
   aprovar (e o F5).

### Nota de metodo (sonda minha que foi REFUTADA por mim mesmo)

A sonda `R6`, rodada contra `montar_fila(criterios, {}, ident)` com decisao VAZIA, mediu campos
executaveis residuais no criterio — **artefato da sonda**, nao defeito: em `cadeia()` a decisao
CIC-2 sempre popula `falhas_automaticas` e a fila, e `R9` (caminho real, 4 estados) mediu
`residuais=[]` em todos. Registrado para nao virar falso achado.

## 5. Limites desta revisao (NAO_EXERCITADO)

Jogo/probe/save/perfil real, runtime AUT-4 (coleta real), UI/UX/pixels, build C#,
pre-flight de deploy, instalacao, publicacao, gates KIT-G1..G4 e aceite humano/DoD: **NAO
EXERCITADO** por esta revisao. Fixture nao comprova runtime; aprovacao tecnica nao e aceite
humano nem DoD.

## 6. Parecer

**APROVADO** no escopo OFFLINE entregue (rodada 3). As tres correcoes pedidas nas rodadas
anteriores (F1, F2, F5) estao presentes nos bytes vivos e foram medidas por sondas proprias do
revisor — inclusive a regressao exata do F5 contra a evidencia real do produtor. Os criterios de
aceite do cartao mapeiam para execucao real (suite 30 OK, isca 14/14, CLI 7 etapas, travas exit 0,
determinismo byte a byte, invalidacao por mudanca de fonte exit 3). Sem `git add/commit/push`;
HEAD `d82894e`; nenhum arquivo de produto editado pelo revisor.
