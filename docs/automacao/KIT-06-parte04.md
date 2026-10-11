# KIT-06 — parte 04: contra-prova adversarial, runner e build isolado

Cartão `t_66ff87b5` · run 633 · 2026-10-09 · offline (sem instalar/deploy/publicar).

## 1. Produzido neste bloco

| Arquivo | O quê |
|---|---|
| `tools/automacao/kit06/contra_prova_kit06.py` | Contra-prova durável: 13 defeitos plantados + discriminador estrito + autoteste adversarial |
| `tools/automacao/kit06/roda_testes_kit06.sh` | Runner (raiz pelo layout, sem `.git`), exit 0/1/2 |

## 2. Contra-prova: cada defeito REPROVA exatamente o alvo declarado

```
$ python tools/automacao/kit06/contra_prova_kit06.py
[OK ] acao_ativa_permitida            [OK ] conflito_de_atalho_aceito
[OK ] encerrou_sessao_ligado          [OK ] export_sem_dados_permitido
[OK ] foco_forcado_ligado             [OK ] guard_chat_removido
[OK ] guard_remapeamento_removido     [OK ] guard_sem_foco_removido
[OK ] indicador_pausado_errado        [OK ] marcar_sem_observacao_permitido
[OK ] pausa_nao_delega_pipeline       [OK ] tecla_reservada_aceita
[OK ] trava_modo_ativo_removida
 iscas: 13, falhas: 0                                             EXIT=0
```

Cada isca muta uma CÓPIA temporária do módulo (o original nunca é tocado) e o
discriminador exige: exit 1 + **conjunto exato** de testes falhando +
`AssertionError` + ausência de `ERROR:`/skip + execução real (`Ran N tests`).

Registro honesto de um erro MEU, corrigido: a 1ª execução acusou 13/13 iscas
"não declaradas" porque o parser do discriminador lia o token errado do formato
`FAIL: <teste> (<modulo>.<Classe>.<teste>)`. Corrigi o parser (não a expectativa)
e reexecutei — é exatamente o tipo de falso-negativo que o achado F9 do KIT-05R
apontou, e por isso existe o autoteste abaixo.

## 3. Autoteste do discriminador (o oráculo não pode ser enganado)

```
$ python tools/automacao/kit06/contra_prova_kit06.py --autoteste
 autoteste do discriminador: 9/9                                  EXIT=0
```

8 saídas enganosas são recusadas (falha de teste NÃO-alvo, exit 0 com texto de
FAIL, ERROR de setup, skip, sem AssertionError, `Ran 0`, conjunto parcial,
saída limpa) e 1 caso verdadeiro é ACEITO (o oráculo não é sempre-nega).

## 4. Runner (exit 0/1/2 distintos)

```
$ bash tools/automacao/kit06/roda_testes_kit06.sh
 Ran 35 tests ... OK
 iscas: 13, falhas: 0
 autoteste do discriminador: 9/9
 VEREDITO KIT-06: VERDE (exit 0)                                  EXIT=0
 log: scratch/kit/KIT-06/runner.log

$ PYTHON=/nao/existe/python bash tools/automacao/kit06/roda_testes_kit06.sh
 ERRO KIT-06: interpretador '/nao/existe/python' nao encontrado   EXIT=2
```

Exit 1 acontece nas iscas (cada `scratch/kit/KIT-06/contra-prova/isca-*.log`
tem `FAILED (failures=N)`).

## 5. Build isolado (`-p:DeployToBepInEx=false`)

Cópia isolada em `scratch/kit/KIT-06/isolated/` (lib + tools/automacao/runtime).

```
$ dotnet build tools/automacao/runtime/KIT04Adapter.SR/KIT04Adapter.SR.csproj \
      -c Release -p:DeployToBepInEx=false
    6 Aviso(s)
    0 Erro(s)                                                    EXIT=0
# DLLs geradas DENTRO da cópia: KIT04Adapter.SR.dll, KIT04Core.dll
log: scratch/kit/KIT-06/build-isolado.log
```

A ponte nova entra no projeto real do Adapter (compila com `#nullable disable`
local; **0 novas** advertências CS8625/CS8603) e o harness offline continua
compilando os MESMOS fontes.

### Invariante do perfil do dono

O JOGO ESTAVA ABERTO durante esta rodada (`Stolen Realm` PID 32388, iniciado
20:14) — **não fechei e não abri nada**. O único arquivo do perfil que mudou foi
`BepInEx/LogOutput.log`, escrito **pelo jogo em execução** (mtime acompanhando o
`date` da rodada), não pelo build. Excluindo o log:

```
perfil-antes-sem-log.txt 97f04c7c86d7eb879a75662e6df306614036b73f62a27aa5465e0a5a68282ce6
perfil-depois-sem-log.txt 97f04c7c86d7eb879a75662e6df306614036b73f62a27aa5465e0a5a68282ce6
PERFIL_SEM_LOG_INALTERADO=OK
```

## 6. Limites desta rodada (honestos)

- **Runtime/pixels/foco real/teclado do engine: NAO_EXERCITADO.** Havia jogo
  aberto, mas NÃO integramos a ponte ao `SRAdapterPlugin` nem geramos a UI —
  isso é KIT-G2 + rodada autorizada. Não se alega interferência zero em jogo.
- KIT-07 segue **não implementado**; só o contrato foi declarado.
- Nada instalado/publicado; nenhum `git add`/commit.

## 7. Progresso

- [x] parte01 · [x] parte02 · [x] parte03
- [x] parte04 (contra-prova 13/13 + autoteste 9/9 + runner + build isolado)
