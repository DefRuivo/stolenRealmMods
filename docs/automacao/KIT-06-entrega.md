# KIT-06 — ENTREGA: acesso simples (observar · pausar · marcar problema · exportar)

Cartão `t_66ff87b5` · perfil `default` · implementer **run 633**
Data 2026-10-09 · **offline**: sem instalar, sem deploy, sem publicar, sem gate KIT-G1/G2/G3/G4.

## 0. Veredito por critério de aceite

| Critério do cartão | Situação | Prova principal (execução real) |
|---|---|---|
| UI/atalhos **configuráveis** | PASSOU | `valida_atalhos`/`carrega_atalhos` + `atalhos.exemplo.json`; CLI real exit 0 |
| **Indicador de coleta** | PASSOU | `indicador()`/`texto_indicador()`; CLI `COLETA: observando \| janela=InventoryPanel \| eventos=0 \| marcacoes=2` |
| **Contexto** | PASSOU | `atualizar_contexto` (janela/chat/digitando/remapeando/foco) gravado na marcação e no indicador |
| **Marcação manual** | PASSOU | `marcar_problema` com contexto, severidade e `pausado_no_momento`; teto de problemas |
| **Guards chat/remapeamento** | PASSOU | `guard_chat`/`guard_remapeamento`/`guard_sem_foco` barram o atalho com degradação explícita |
| **Ausência de conflito com input** | PASSOU | validação recusa tecla reservada e conflito; `consome_input=False` (só lê) |
| **Observar nunca autoriza modo ativo** | PASSOU | `habilitar_modo_ativo()` sempre falha; `ACOES_ATIVAS` recusadas; `modo` fica `passivo` |
| **Sem foco forçado** | PASSOU | `foco_forcado=0` (trava); guard de sem-foco bloqueia em vez de puxar foco |
| **Sem encerrar sessão do dono** | PASSOU | `parar_observacao` só para a coleta; `encerrou_sessao=False` (trava) |
| **Exportação acessível sem Hermes/IA** | PASSOU | `exportar()` grava JSON local em pasta padrão; CLI e harness gravam arquivo real |
| **Integrar contrato KIT-07** | PASSOU (contrato) | `contrato_kit07()` → esquema `KIT-07/export/1`, `status_kit07=NAO_IMPLEMENTADO` |
| **Fluxo completo offline** | PASSOU | roteiro offline (`roteiro.exemplo.json`) + CLI + harness (44 verificações) |
| **UI real** | NAO_EXERCITADO | depende de **KIT-G2**; aqui só a lógica/dado do plano de controle |
| **Runtime em jogo / pixels / foco real** | NAO_EXERCITADO | exige rodada autorizada do dono |

## 1. Arquivos entregues (SHA256 medidos por `sha256sum`)

```
2e21f5396628f6141ea3fd66d5e60f815b95c0dfb0ac4a83c37157ee7c787e2f  tools/automacao/runtime/controle_acesso.py
6bfe3db1e50c18e441d266fca00bfba82c527680837a1a22d148455c5db6bbbf  tools/automacao/runtime/KIT04Adapter.SR/PonteControleRSTV.cs
600503b349bdf9ac57ab89cafde82b80aae66a8e08719f470e7ee21d1ec981db  tools/automacao/runtime/harness-controle/Program.cs
d8de16e042f7d531e57969c93890f844720bc51e3c0c30587d8ebaaa3f99d5fb  tools/automacao/runtime/harness-controle/HarnessControle.csproj
e3a310679acb3e67d238c938a85b46af0a80b46f163f96289ad6b0c5d56a6186  tools/automacao/kit06/teste_controle_acesso.py
0374fdfe9fe000aff607f8088defcb24a7b5954af3d9961e4c879bc4e084db0d  tools/automacao/kit06/contra_prova_kit06.py
9c121d12e5772ae7331b74d9d65262c1f20cbb695c4eb5f44d06bb027829551d  tools/automacao/kit06/roda_testes_kit06.sh
d4ad2cb1e0562d6b7ae4fb02dfd2a90266b8e59769c597e4fa4012407e48bc48  tools/automacao/kit06/atalhos.exemplo.json
65ee62fcc74badb3dda441a89601df72488ebc5f0d90add3065cb4ab723a2296  tools/automacao/kit06/roteiro.exemplo.json
```
Lista completa (inclui as partes e logs) em `scratch/kit/KIT-06/hashes-kit06.txt`.
Nenhum arquivo existente foi modificado; `git status` mostra só caminhos **novos**
(nada de `git add`, nada de commit).

## 2. Execuções reais (comando → exit)

| Comando | Resultado |
|---|---|
| `python tools/automacao/kit06/teste_controle_acesso.py` | `Ran 35 tests`, OK, **exit 0** |
| `python tools/automacao/kit06/contra_prova_kit06.py` | 13 iscas, 0 falhas, **exit 0** (logs `scratch/kit/KIT-06/contra-prova/isca-*.log`) |
| `python tools/automacao/kit06/contra_prova_kit06.py --autoteste` | 9/9, **exit 0** |
| `bash tools/automacao/kit06/roda_testes_kit06.sh` | VERDE, **exit 0** (`scratch/kit/KIT-06/runner.log`) |
| `PYTHON=/nao/existe/python bash .../roda_testes_kit06.sh` | **exit 2** (nenhuma ausência verde) |
| `dotnet run --project tools/automacao/runtime/harness-controle` | 44 OK / 0 FALHA, **exit 0** |
| `... --defeito guard` | 3 FALHA detectadas, veredito de controle negativo, **exit 0** |
| `... --defeito ataque` | 2 FALHA detectadas, veredito de controle negativo, **exit 0** |
| `dotnet build .../KIT04Adapter.SR.csproj -c Release -p:DeployToBepInEx=false` (cópia isolada) | 0 Erros, **exit 0**; DLLs dentro da cópia |
| `python tools/automacao/runtime/controle_acesso.py --atalhos ... --roteiro ... --out ...` | **exit 0**; `observando=True`, `modo=passivo`, `foco_forcado=0`, `encerrou_sessao=False`, `guard_chat=1`, 2 marcações |

CLI (medido): `problemas_config=[["voar","acao_desconhecida"],["salvar","acao_ativa_proibida"]]`,
`degradacoes_por_motivo={guard_chat:1, sem_pipeline:2, ja_observando:1}`,
`eventos=[observar, marcar_problema, marcar_problema]` — o F9 com o chat aberto
**não** marcou (guard), exatamente como declarado.

## 3. Discriminador estrito e autoteste (lição F9 do KIT-05R)

A contra-prova exige exit 1 + **conjunto exato** de testes falhando +
`AssertionError` + ausência de `ERROR:`/skip + `Ran N tests` > 0. O autoteste
mostra que o oráculo **recusa 8 saídas enganosas** e **aceita 1 verdadeira**.
Registro honesto: na 1ª execução meu parser leu o token errado de
`FAIL: <teste> (<modulo>.<Classe>.<teste>)` e acusou 13 falsos-negativos; corrigi
o parser (não a expectativa) e reexecutei.

## 4. Integração reusada (sem duplicar infraestrutura)

- Pipeline **KIT-05F** (`observacao_passiva.py` / `PipelinePassivo.cs`) é o ÚNICO
  pipeline: pausar/retomar pelo atalho agem nele, e o indicador lê
  `eventos_total` dele (`TestIntegracaoKit05F`).
- Núcleo C# **sem Unity/BepInEx** (`PonteControleRSTV.cs`) é compilado por LINK
  pelo harness (padrão KIT-05F) e pela build real do Adapter.
- Nada de Core/Adapter virou dependência obrigatória dos mods testados.

## 5. O que NÃO foi feito (limites honestos)

- **UI real/overlay e leitura de teclas do engine**: NÃO implementadas — exigem
  **KIT-G2** (gate humano) e rodada autorizada. O `PonteControleRSTV` ainda não
  é chamado pelo `SRAdapterPlugin.Update`; a ligação é o próximo passo.
- **Runtime/pixels/interferência**: NAO_EXERCITADO. O jogo **estava aberto** na
  rodada (PID 32388) e NÃO foi aberto/fechado por mim; nada foi instalado.
- **KIT-07**: contrato declarado, não acoplado (KIT-07 entregou em paralelo — a
  integração efetiva é passo futuro, sem tornar este módulo dependência dele).
- Nada publicado; `git add`/commit: nenhum. `Assembly-CSharp.dll`, Bard,
  gameplay e travas: intocados.
- A suíte AUT-4 não foi reexecutada; não se alega não-regressão runtime.

## 6. Próximo passo

Revisão independente **KIT-06R** (`t_f9f88c18`, instância ≠ 633): conferir os
hashes acima, refutar permissões misturadas, atalhos invasivos e UI/UX
insuficiente, rodando a suíte/contra-prova/harness por conta própria. Aprovação
técnica não equivale a aceite humano nem à publicação do DoD.
