# KIT-11 — parte 01: inventario, desenho e contrato

Cartao `t_f2129aea` (run 649, perfil `default`). Repo `C:/dev/stolen-realm`.
Este arquivo e um checkpoint de bloco; o entregavel final e `docs/automacao/KIT-11-entrega.md`.

## 1. Inventario (arquivos vivos, so LEITURA)

Reuso obrigatorio (nao duplicar infraestrutura entregue):

| Arquivo | Papel | Reuso em KIT-11 |
|---|---|---|
| `tools/automacao/runtime/coletor.py` | driver opt-in AUT-4 | `validar_plano`, `decidir_autorizacao`, `planejar_encerramento`, `encerrar_processos`, `snapshot_arquivos`/`snapshot_dirs`, `planejar_rollback`/`executar_rollback`, `verificar_sem_residuo` |
| `tools/automacao/runtime/controle_acesso.py` | KIT-06 | `ACOES_ATIVAS` (trava dura do passivo) |
| `tools/automacao/runtime/roda_testes_runtime.py` | runner | convencao exit 0/1/2 + `--contra-prova` |
| `tools/testes/arcabouco.py` | framework | `main/META/corpo`, `RESULTADO|...` |
| `tools/automacao/cenarios/kit09.py`, `kit10_cenarios.py` | avaliadores | cenarios CONHECIDOS (nao reimplementar) |

## 2. Lacuna que KIT-11 fecha

O `coletor.py` ja tem espera de ESTADO (`_esperar_estado`) e rollback, mas o que falta e um
EXECUTOR DETERMINISTICO de cenarios conhecidos:

- maquina de estados que ESPERA menu/tela/condicao (nao sleep cego) com HANDLERS por tipo;
- diagnostico do que faltou + TIMEOUT explicito por passo;
- FRENTE UNICA confiavel (o `front-unica.sh` do KIT-03 foi reprovado — lock por PID fragil);
- CANCELAMENTO/ROLLBACK exatos;
- encerra APENAS a instancia que a propria execucao criou;
- MODO ATIVO com AUTORIZACAO SEPARADA + perfil/save de TESTE verificados;
- observacao NAO concede acao;
- config/desconhecido/versao incompativel FALHAM FECHADO;
- NAO executar comandos arbitrarios de cenario.

## 3. Contrato do modulo `tools/automacao/kit11/executor.py`

Esquema do plano: `"KIT-11/executor/1"`, `versao` inteira (compativel somente as declaradas).

Passos: `{"nome", "tipo" em {menu,tela,condicao}, "alvo", "timeout_s"?, "requer_acao"?}`.
- `tipo` fora do conjunto -> FALHA FECHADA (`tipo_desconhecido`).
- `condicao` cujo alvo nao esta na whitelist `CONDICOES_CONHECIDAS` -> FALHA FECHADA.
- passo com campo executavel (`comando`/`argv`/`shell`/`exec`) -> FALHA FECHADA
  (`comando_arbitrario`) — o executor so ESPERA condicoes conhecidas, nunca roda comando de cenario.

Permissoes separadas:
- `autorizacao.observacao_autorizada` libera apenas OBSERVAR;
- `autorizacao.ativa_autorizada` (SEPARADA) e obrigatoria para passo `requer_acao`;
- passo ativo com **somente** observacao autorizada -> FALHA FECHADA (`autorizacao_ativa_ausente`).
- modo ativo exige perfil/save de TESTE verificados; falta -> FALHA FECHADA antes de agir.

Maquina de estados: `INATIVO -> VALIDANDO -> (FALHOU_FECHADO) | PERMISSOES -> AMBIENTE ->
FRENTE -> AGUARDANDO(passo) -> CONCLUIDO|TIMEOUT|CANCELADO -> ROLLBACK -> ENCERRAMENTO -> fim`.

Handlers REAIS: `FonteDeArquivo` (le um JSON de estado — caminho real, offline) e contrato
`Fonte.ler(tipo, alvo) -> {"satisfeito","observado","diagnostico"}`. Stubs vivem nos TESTES.

Fonte injetavel (`relogio`/`dormir`/`pid_vivo`/`executar`) para o teste provar timeout, cancelamento e
encerramento SEM tocar em processo, jogo ou perfil.

## 4. Prova exigida

Testes offline com stubs: positivo, falha (timeout) e cancelamento, mais CONTROLES NEGATIVOS
(versao incompativel, tipo/condicao desconhecidos, comando arbitrario, ativo sem autorizacao,
perfil/save nao verificados, segunda frente, encerrar so a instancia criada, observacao != acao) e
uma ISCA de contra-prova. Navegacao real/clique fisico ficam em KIT-14 (apos KIT-G2).

## 5. Limites

Offline. Nao abre/fecha jogo, nao instala probe, nao carrega save, nao publica, nao edita
Assembly-CSharp/Bard/gameplay. Runtime NAO_EXERCITADO.
