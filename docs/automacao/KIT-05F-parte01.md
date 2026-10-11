# KIT-05F — parte 01: abertura, baseline e plano por achado

Cartão: `t_467952ea` (KIT-05F) · perfil `default` · implementer run 631 (nova instância,
!= autor 629 e != reviewer 630) · data 2026-10-09 · **frente única OFFLINE**.

Objetivo: corrigir F1–F9 do parecer `docs/automacao/KIT-05R-revisao.md` (t_43675d2e),
preservando histórico KIT-05/KIT-05R, sem implementar KIT-06/07/09, sem jogo, sem
deploy, sem publicação, sem alterar política/modelos/crons/prioridades.

## 1. Fontes vivas de partida (SHA256 medido agora, antes de qualquer edição)

```
e3e89d5b2600a4d495465c55a612d60b48ba8746e59ad61b5a0e4ed6ffaac713  tools/automacao/runtime/observacao_passiva.py
bf7ae0e59901503be7f1a564f88da8bf4dcc4996bd9ee15557370f2ba9d496c6  tools/automacao/kit05/teste_observacao_passiva.py
05bc6a34b233c2c78f7b8e8a073470175b74c6a04a24bf32eb048fb6affd80a3  tools/automacao/kit05/roda_testes_kit05.sh
027e6ee37bcfbfe8f58510f18aadea8002c31b2982a449dc03e5e9b23a8b68a0  scratch/kit/KIT-05/contra_prova.py
8a415edb92693a37f39cebfa92295b5fa9e120fa544bcf2c247c672ba97ce905  tools/automacao/runtime/KIT04Core/CorePlugin.cs
9687dbd4fc81399cf94808a5a14fa955b43e5cb327426da811380c5339662b01  tools/automacao/runtime/KIT04Adapter.SR/SRAdapterPlugin.cs
6802717c901416f826fc5a020485893409871279c1559dd62d4134884f37cf73  tools/automacao/runtime/fixtures/kit05-observacao.entrada.json
```

Comando: `sha256sum <arquivos>` (saída completa em `scratch/kit/KIT-05F/baseline-sha256.txt`).
Os três primeiros conferem byte a byte com os hashes declarados no corpo do cartão.

Ambiente: Windows 11, bash MSYS, `python` = 3.14.7, `dotnet` = 6.0.428,
`E:/SteamLibrary/.../Stolen Realm_Data/Managed` presente (necessário ao build C#).

## 2. Plano por achado (decisão de correção)

| Achado | Correção decidida | Prova planejada (offline) |
|---|---|---|
| F1 captura | Separar **pedido** (`registrar_captura` -> pedido com estado `solicitada`) de **confirmação** (`confirmar_captura` exige evento existente, sessão/evento coincidentes, arquivo PNG real em disco, quadro estritamente posterior ao evento e hash). Pedido **nunca** marca `captura_apos_atualizacao_visual`. | testes novos de F1 + controle de contra-prova |
| F2 pausa | Pausa bloqueia `registrar`, `registrar_captura` e `confirmar_captura`; ao pausar, pendências cujo intervalo perdeu observação são invalidadas com lacuna explícita e **não** viram falha de timeout ao retomar. | testes F2 positivo/negativo |
| F3 dedup | Estado por **fonte** (janela/contexto) e não global; assinatura inclui tipo+dados+janela; cliques seguem discretos; abrir/fechar/reabrir sobrevive. | testes F3 |
| F4 limites | Limite explícito próprio para TODO estado auxiliar (degradações, rejeitados, pendentes, estado de dedup, pedidos de captura), com contadores agregados de descarte/ motivo; evicção/expiração limpam referências órfãs. | testes F4 com 1000 entradas |
| F5 timeout | Resolução só vale dentro do prazo; vencimentos são materializados (motivo+clique_id+janela+timeout reais) **antes** de processar abertura tardia. | testes F5 (fronteira exata, janela errada, tardia, tempestiva, pausa) |
| F6 CLI replay | `_correr_entradas` devolve o **estado retido**, não lista paralela; export do CLI coerente com totais/IDs/limites; rótulos de fixture/offline e `runtime=NAO_EXERCITADO`. | teste F6 + execução real do CLI |
| F7 runner | Resolver raiz pelo **layout** (`BASH_SOURCE`), sem `git rev-parse`; contra-prova durável em `tools/automacao/kit05/`; `PYTHON` configurável; exit 0/1/2 distintos; nenhuma ausência verde. | runner em cópia fora de qualquer `.git` |
| F8 integração | Ponte passiva em C# reusando Core/Adapter: `EventosImpl` com teto/retenção, pipeline passivo compilável sem Unity, transições reais de tela -> `janela_aberta`/`janela_fechada`, opt-in `false`; build em cópia isolada `-p:DeployToBepInEx=false` só após preflight; harness offline próprio. | harness C# executado + build isolado |
| F9 contra-prova | Discriminador estrito: exige `FAIL`/`AssertionError` **do alvo**, exit 1, sem ERROR/skip/timeout; controle adversarial "alvo passa, outro falha" DEVE reprovar a contra-prova. | execução real dos 7+ casos e do controle falso-verde |

## 3. Regras de trabalho desta execução

- Tocar apenas: `tools/automacao/runtime/observacao_passiva.py`,
  `tools/automacao/kit05/*`, `tools/automacao/runtime/KIT04Core/*`,
  `tools/automacao/runtime/KIT04Adapter.SR/*`, docs `KIT-05F-*`, provas novas em
  `scratch/kit/KIT-05F/`.
- Preservar `scratch/kit/KIT-05/` e `scratch/kit/KIT-05R-run630/` como histórico
  (não sobrescrever provas do reviewer).
- Sem `git add` de diretório, sem commit, sem deploy, sem jogo, sem save.
