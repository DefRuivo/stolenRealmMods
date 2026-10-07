# COR-CIC3 — fechar F1-F7 do parecer CIC-3R (`t_7bec518b`)

> Herança: o parecer independente `docs/automacao/CIC-3R-revisao.md` deixou **F1-F7 em aberto no
> produto** e o adendo A3 mostrou que o mesmo funil entrega **verde GLOBAL, sem pendência humana,
> quando a dimensão não foi lida ou a contagem veio `null`**. Este documento entrega o fechamento
> desses sete achados **no produto** (`tools/automacao/cenarios/rstv.py`) com prova executada.
>
> **Nada de jogo, save, probe, build, instalação, deploy ou publicação nesta rodada.** Runtime
> continua **NAO_EXERCITADO**; todo dado abaixo é fixture/sintético rotulado. Escopo estrito: os
> arquivos desta frente (`tools/automacao/cenarios/rstv.py`,
> `tools/automacao/cenarios/test_rstv.py`) e este doc. Nenhum critério de trava foi enfraquecido —
> toda mudança **endurece** (nenhuma capacidade passou a fechar OK com menos leitura).

## 1. O que mudou, por achado

| # | regra que passou a valer | onde (arquivo:linha) |
|---|---|---|
| **F1** | `RSTV-6-readonly-skills-pontos` anuncia **skills E pontos**: a dimensão que nunca teve par antes/depois completo vira lacuna declarada (`NAO_EXERCITADO` + motivo nomeando a dimensão), em vez de "ambas inalteradas" afirmado com metade da leitura | `tools/automacao/cenarios/rstv.py:528`, motivo em `:600-607` |
| **F2** | `RSTV-21-tooltip-restauracao` só prova AUSÊNCIA de duplicata com **contagem observada válida** (número finito ≥ 0) — `null`/negativo/bool/lista é leitura malformada; `duplicata` tem de ser booleano | `rstv.py:666-686` (helper em `:516`) |
| **F3** | `RSTV-25b-dependencia`: valor por tier tem de ser **contagem válida dos dois lados** (`'abc'`/`-2` → lacuna) e a contagem tem de **condizer** com a `Dependency` real (o `esperado` declarado é "linhas == Dependency"); truthiness deixou de valer como confronto | `rstv.py:776-807` |
| **F4** | `RSTV-geometria-clipping` exige **número finito** em x/y/largura/altura (`'NaN'`/infinito = malformado) e `tela` bem formada; dado não mensurável nunca fecha OK | `rstv.py:823-880`, `:882` |
| **F5** | Cadeia de hash: `hash_fonte`/`hash_dll`/`dll_sha` na **mesma** observação com valores diferentes é **contradição declarada** (o alias do coletor não sobrescreve o valor explícito) → `INDETERMINADO` | `rstv.py:253`, `:278`, `:283`, `:438-445` |
| **F6** | `RSTV-26-placeholders`: o OK passa a exigir o **texto renderizado observado** — sem render não se afirma "placeholder resolvido" (não observado ≠ resolvido); o template CRU continua **não** sendo defeito | `rstv.py:725-745` (motivo em `:740`) |
| **F7** | Sessões: observações de **sessões diferentes** na mesma capacidade não são prova de um único ciclo (`INDETERMINADO`), e nenhuma sessão é copiada ao critério como se fosse a do conjunto | `rstv.py:425-432` |

O cabeçalho do módulo ganhou a seção "FECHAMENTO F1-F7" (`rstv.py:51-76`) e o docstring de `_fecha`
registra as regras F5/F7 (`rstv.py:402-408`). Correção **sem ampliação**: as capacidades
`RSTV-6-readonly-personagem` e `RSTV-21-janela-ciclo`, o achado secundário S1 (índice negativo) e o
`@x@` bruto ficaram **como estavam** (o parecer não os pede).

## 2. Decisão de semântica em F3 (registrada para o pai)

O parecer (§4/§5 e §9.4) diz que a **equivalência de contagens** de F3 depende de decisão explícita
do pai *caso* o desenho de produto exija apenas presença. O produto **declara** a semântica de
igualdade no próprio critério (`esperado = "linhas == Dependency real; T5 sem Dependency e
legitimo"`, `rstv.py:814`) — então esta correção **executa o confronto que o critério anuncia** (e
mantém `T5` sem Dependency como ausência legítima). Se o pai fixar a semântica como "só presença",
a linha a relaxar é **uma só**: o `elif` de igualdade em `rstv.py:805-807`. Nada mais depende dela.

## 3. Prova: o teste REPROVA nos bytes antigos e PASSA nos novos

`tools/automacao/cenarios/test_rstv.py` ganhou o bloco **F1-F7** (`:270-386`): uma leitura runtime
COMPLETA fecha as 7 capacidades OK (`:308-311`, `_obs_completa` em `:270`) e, para cada achado, o defeito é **plantado** na
dimensão que ele ataca; o critério alvo tem de sair do OK **nomeando o defeito** no motivo. O mesmo
teste foi rodado contra os **bytes antigos do produto** (cópia congelada, sem editar nada) com
`f1f7/prova_red_f1f7.py` (coletor que acumula as falhas em vez de abortar na primeira):

```
$ python -B f1f7/prova_red_f1f7.py --modulo f1f7/rstv_524f7197.py --lente red
MODULO .../rstv_524f7197.py sha256=524f719757977436b843bdceb8337b10db4003cba9da64ff3fea788ef327d320
TESTE _fixture_nao_vira_ok   SEM_FALHA falhas=0
TESTE _ausente               SEM_FALHA falhas=0
TESTE _lacunas               SEM_FALHA falhas=0
TESTE _controles             SEM_FALHA falhas=0
TESTE _caminho_ok            SEM_FALHA falhas=0
TESTE _cadeia                SEM_FALHA falhas=0
TESTE _fechamento_f1_f7      SEM_FALHA falhas=56
   FALHA F1-skills-sem-pontos: esperado NAO_EXERCITADO, obtido OK (motivo='leitura runtime completa com identidade suficiente')
   ...
   FALHA F2-duplicadas-null: esperado NAO_EXERCITADO, obtido OK
   FALHA F3-contagem-diferente: esperado REPROVADO, obtido OK
   FALHA F3-valores-invalidos: esperado INDETERMINADO, obtido OK
   FALHA F4-nan-x: esperado NAO_EXERCITADO, obtido OK
   FALHA F4-nan-largura: esperado NAO_EXERCITADO, obtido OK
   FALHA F5-hash-contraditorio: esperado INDETERMINADO, obtido OK
   FALHA F6-cru-sem-render: esperado NAO_EXERCITADO, obtido OK
   FALHA F7-sessoes-misturadas: esperado INDETERMINADO, obtido OK
TESTE _adaptadores           SEM_FALHA falhas=2
TOTAL falhas=58
RED CONFIRMADO: o modulo sob prova NAO satisfaz os testes (defeito presente)
```

Os **sete** achados reproduzem `OK` nos bytes antigos (o defeito não foi inventado no teste: ele
existia no produto). Nos bytes corrigidos, o mesmo teste sai limpo:

```
$ python -B f1f7/prova_red_f1f7.py --modulo tools/automacao/cenarios/rstv.py --lente green
MODULO tools/automacao/cenarios/rstv.py sha256=2fad23a3bc3dc48c7b2dd5cda3feda64a18d9e3d802c54dbef63696a8a032252
...
TOTAL falhas=0
GREEN CONFIRMADO: 0 falhas no modulo atual
```

Suíte do próprio produto e isca meta (inalteradas na regra, reexecutadas):

```
$ python -B tools/automacao/cenarios/test_rstv.py
RESULTADO|PASSOU|cic3-rstv|avaliador RSTV: fixture nao vira OK, lacunas nao viram OK,
controles reprovam, runtime identifica                                        exit 0

$ python -B tools/automacao/cenarios/test_rstv.py --contra-prova
CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os 10 controles passarem
(o REPROVADO real vem da regra)                                              exit 0
```

## 4. O verde GLOBAL: o buraco do adendo A3 está fechado

Ciclo sintético coerente (uma sessão, hashes da identidade) com **F1** (`pontos` nunca lidos) e
**F2** (`janelas_duplicadas: null`) plantados, submetido às **duas CLIs reais** (`rstv.py` e
`decisao.py`) — a variante N1 do parecer, reconstruída (`f1f7/n1_verde_global.py`):

```
== antigo (rstv=rstv_524f7197.py)
   rstv exit=0 contagem={'OK': 7}
   decisao exit=0 pronto_para_decisao=True
   ok_vinculantes=7 falhas_automaticas=0 pendencias_humanas=0
   motivo=SIM: automacao sem falhas e sem pendencia humana; resta aceite/publicacao

== atual (rstv=rstv.py)
   rstv exit=0 contagem={'OK': 5, 'NAO_EXERCITADO': 2}
   criterio  RSTV-6-readonly-skills-pontos: NAO_EXERCITADO | campo AUSENTE/incompleto nao vira OK —
             pontos: dimensao NUNCA lida (nenhum par antes/depois completo) ...
   criterio  RSTV-21-tooltip-restauracao: NAO_EXERCITADO | campo AUSENTE/incompleto nao vira OK —
             janelas_duplicadas MALFORMADA (None): contagem observada valida ...
   decisao exit=1 pronto_para_decisao=False
   ok_vinculantes=5 falhas_automaticas=2 pendencias_humanas=0
   motivo=NAO: 2 falha(s) automatica(s) volta(m) ao ciclo; nada disso vai ao dono
```

Leitura: o verde global deixou de sair de leitura incompleta; a lacuna **volta ao ciclo** como
falha automática (**0 pendências humanas** — não foi empurrada ao dono) e a decisão humana segue
exigida. É o "PRONTO QUANDO" do cartão: *o verde global passa a exigir leitura completa e bem
formada de cada dimensão do critério*.

## 5. Regressões: o que foi rodado e o que já estava vermelho

| comando | resultado |
|---|---|
| `python tools/automacao/cenarios/test_rstv.py` | PASSOU (exit 0) |
| `python tools/automacao/cenarios/test_rstv.py --contra-prova` | PASSOU (exit 0) |
| `python tools/automacao/ciclo/test_decisao.py` | 127 checks, 0 falhas (exit 0) |
| `python tools/automacao/aceite/test_relatorio_aceite.py` | total: 14, falhas: 0 (exit 0) |
| `python tools/automacao/ciclo/test_ciclo.py` | exit 0 |
| `python tools/automacao/offline/testes/t_aut3_lib.py` | exit 0 |
| `python tools/automacao/aut6/test_cobertura_aut6.py` | rodaram=24 reprovaram=0 (exit 0) |
| `python tools/automacao/aut6/test_regressoes_cor_aut6.py` | 26 tests, OK (exit 0) |
| `python tools/automacao/runtime/testes/t_aut4_autorizacao.py` · `t_aut4_controle_negativo.py` · `t_aut4_manifest_rollback.py` · `t_aut4_observacao.py` | PASSOU (exit 0) |
| `bash tools/testes/roda.sh --puros` (trava do projeto) | 87 rodaram, 87 passaram, 0 reprovaram, **VERDE (exit 0)** |

**Já estava vermelho antes desta rodada** (não é regressão; nada aqui importa `rstv.py`):

* `tools/automacao/runtime/testes/t_aut4_costura_probe.py` (A2) e `t_aut4_plano.py` — REPROVOU;
  `t_aut4_probe_contrato.py` — NAO_RODOU. Os três são da frente AUT-4/probe e dependem do
  `AUT4ProbePlugin.cs`, que **derivou depois do congelamento** — é o risco residual A4 do próprio
  parecer. Nenhum deles importa o avaliador desta frente.
* `tools/automacao/aut5/test_aut5.py` — exit 1, todas as 6 falhas no caso `log-real`:
  * 4 falhas **pré-existentes** (`RSTV-25b-dependencia` e `AUT5-RSTV-25b-conectores-log` voltando à
    fila de agente em vez do roteiro humano — o log do perfil é de build anterior ao AUT5-F1);
  * 2 falhas de **identidade de DLL** (`a DLL do perfil deveria casar com a build do repo`,
    `AUT5-boot-rstv`), porque a DLL Release do mod **foi recompilada no disco às 13:46 de hoje**
    (mtime) enquanto a DLL do perfil do dono segue de 05/10 13:32 — **nada foi deployado no
    perfil**; nada disso passa pelo avaliador.
  * **Prova de independência (A/B, `f1f7/ab_log_real.py`)**: rodando o MESMO caso `log-real` com o
    avaliador antigo e com o novo, os 7 estados de critério RSTV e as falhas RSTV são **idênticos**
    (`estados iguais=True; falhas RSTV iguais=True`).

## 6. Arquivos e sha256 (do que foi escrito nesta rodada)

```
2fad23a3bc3dc48c7b2dd5cda3feda64a18d9e3d802c54dbef63696a8a032252  tools/automacao/cenarios/rstv.py
51f7100791fbe3d179be7f88234f88e545a9f5831d8bdafcdfc6fd4f26b1c073  tools/automacao/cenarios/test_rstv.py
```

Bytes de partida (cópia congelada usada na prova RED, sha256 declarado no parecer):
`524f719757977436b843bdceb8337b10db4003cba9da64ff3fea788ef327d320` — o sha256 registrado em
`docs/automacao/CIC-3-entrega.md` para `rstv.py` passa a ser **histórico** (aquela entrega é o
estado anterior a esta correção; nada foi reescrito lá).

## 7. Evidência bruta (anexada ao cartão `t_7bec518b`)

Os bytes antigos do produto **não estão no git** (`tools/automacao/` está untracked), então a
evidência desta rodada fica em anexos do cartão, para o revisor reproduzir por execução própria:

| anexo | o que é |
|---|---|
| `rstv_524f7197.py` | os bytes ANTIGOS de `tools/automacao/cenarios/rstv.py` (sha256 `524f7197…`), usados na prova RED |
| `prova_red_f1f7.py` | a bancada RED/GREEN (roda os testes do produto contra um `rstv.py` escolhido, acumulando todas as falhas) |
| `prova_red_final.txt` | saída literal da lente RED (58 falhas nos bytes antigos) |
| `n1_verde_global.txt` | saída literal da variante N1 (verde global antes × depois) |

Reprodução do revisor (na raiz do repo, com os anexos baixados):

```
python -B prova_red_f1f7.py --modulo rstv_524f7197.py --lente red      # espera-se RED (58 falhas)
python -B prova_red_f1f7.py --modulo tools/automacao/cenarios/rstv.py --lente green
```

## 8. Limites e o que continua aberto

* **Runtime NAO_EXERCITADO**: nenhuma leitura de jogo; as fixtures F1-F7 são sintéticas e rotuladas.
  Fechar F1-F7 não atesta DoD de mod nem substitui a rodada autorizada.
* **Independência nominal do revisor**: continua INDETERMINADO no parecer; quem revisa esta correção
  é outra tarefa (CIC-3R2), criada pelo pai.
* Não tocados (fora do escopo pedido): `RSTV-6-readonly-personagem`, `RSTV-21-janela-ciclo`, o
  achado secundário S1, a hipótese de `config_sha` relevante, o probe C# e o CIC-4 (`hash_fonte`).
* Nenhum build, instalação, deploy, save, commit ou publicação. O perfil do dono não foi tocado.
