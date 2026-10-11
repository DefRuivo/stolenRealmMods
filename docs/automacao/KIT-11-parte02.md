# KIT-11 — parte 02: implementacao, execucao real e prova RED

Cartao `t_f2129aea` (run 649, perfil `default`). Repo `C:/dev/stolen-realm`.

## 1. Arquivos produzidos (novos; nenhum arquivo de mod/produto editado)

| Caminho | Bytes | sha256 |
|---|---|---|
| `tools/automacao/kit11/executor.py` | 24137 | `65284edd248d3bf1117529b366d150b7cb8578c0ae03c64fcd7358cdbb75b6e2` |
| `tools/automacao/kit11/test_kit11_executor.py` | 14998 | `1d72ae071ceea8086c49b7d11523fbda1c908eee7f772e44290d38adbf071a02` |

Reuso (somente leitura): `runtime/coletor.py` (snapshot/rollback/encerramento/`_pid_vivo`),
`controle_acesso.py` (trava do passivo), `tools/testes/arcabouco.py` (framework).
Nao se reusou o `scratch/kit/front-unica.sh` (lock fragil, reprovado no KIT-03).

## 2. Execucao real (terminal, exit codes distintos)

Comando: `python tools/automacao/kit11/test_kit11_executor.py`
Resultado: `12 teste(s), 0 falha(s)` — **exit 0** (`scratch/kit/KIT-11-green-final.log`).

Ordem dos testes e cobertura:
1. positivo-observacao (menu+tela satisfeitos; observacao NAO concede acao)
2. positivo-ativo (autorizacao separada + perfil/save de teste verificados)
3. falha-timeout (relogio falso; TIMEOUT + diagnostico + tentativas>1)
4. cancelamento (flag do chamador durante a espera)
5. neg-versao-incompativel (fail closed, zero passos executados)
6. neg-tipo-condicao-desconhecidos (fail closed)
7. neg-campo-executavel (passo com `argv` recusado)
8. neg-ativo-sem-autorizacao-separada (observacao != acao)
9. neg-perfil-save-de-teste (sem marcadores / divergente)
10. neg-frente-unica (viva RECUSA; pid nao mensuravel RECUSA; lock morto retoma)
11. encerra-so-instancia-criada (so o PID 200; sem medicao -> recusado)
12. rollback-exato (criado some; modificado volta "ANTES")

Modo ISCA: `python .../test_kit11_executor.py --isca` -> **exit 1**
(`scratch/kit/KIT-11-isca.log`, 13 testes, 1 falha) — o defeito plantado NAO passa.

## 3. Prova RED (defeito plantado no FONTE, restaurado byte a byte)

Cada defeito foi plantado em `executor.py`, a suite mostrou REPROVOU (exit 1) e o fonte foi
restaurado para o original; sha conferido apos restauracao = `65284edd...` (identico ao backup
`scratch/kit/KIT-11-executor-original.py`).

| Defeito plantado | Linha alterada | Suite | Log |
|---|---|---|---|
| versao compat. neutralizada (`if False and versao not in ...`) | `validar_plano_execucao` | exit 1: **neg-versao-incompativel** REPROVOU (`esperado FALHOU_FECHADO, obtido OBSERVADO`); 11 PASSOU | `scratch/kit/KIT-11-red-versao.log` |
| frente viva nao recusa (`if False and estado:`) | `FrenteUnica.obter` | exit 1: **neg-frente-unica** REPROVOU (`frente viva deveria RECUSAR`); 11 PASSOU | `scratch/kit/KIT-11-red-frente.log` |
| timeout com teto None dispara (`decorrido >= (limite or 0)`) | `aguardar_passo` | exit 1: **cancelamento** REPROVOU (excecao inesperada no ramo de teto nulo); 11 PASSOU | `scratch/kit/KIT-11-red-timeout.log` |

Depois de cada restauracao o mesmo comando volta a **exit 0 / 12 PASSOU** — a suite DISCRIMINA
(defeito -> vermelho; fonte correto -> verde) e nao e decoracao.

sha256 dos logs: verde `b2c5b5b2...`, red-versao `b0b2ea7f...`, red-frente `e86816bf...`,
red-timeout `0df3e15d...`, isca `b6fdbfb5...`.

## 4. Itens do aceite e onde estao

- espera menu/tela/condicao com handlers reais + diagnostico/timeout: `aguardar_passo`/`_consultar`
- frente unica: `FrenteUnica` (PID+token; viva/nao-mensuravel -> RECUSA)
- cancelamento/rollback: `executar()` (flag `cancelado`; `finally` com `planejar_rollback`/`executar_rollback`)
- encerra so a instancia criada: `coletor.planejar_encerramento`/`encerrar_processos`
- modo ativo com autorizacao separada: `decidir_permissoes`
- perfil/save de teste verificados: `verificar_ambiente_de_teste`
- observacao nao concede acao: `decidir_permissoes` (status FALHOU_FECHADO)
- config/desconhecido/versao falham fechado: `validar_plano_execucao` (`ConfigInvalida`)
- nao executar comando arbitrario: `CAMPOS_EXECUTAVEIS` recusados

## 5. Lacunas (declaradas, nao mascaradas)

- NAVEGACAO REAL e CLIQUE FISICO: NAO_EXERCITADO — qualificados em KIT-14 (apos KIT-G2).
- Leitura de jogo/probe/perfil/save reais: NAO_EXERCITADO (offline). A fonte no teste e um STUB.
- Nada instalado, jogo/save/perfil/publicacao intocados; nenhum commit.
