# ORG-AUT5-FIX — parte 02: provas, hashes e handoff

Continuação de `docs/automacao/ORG-AUT5-FIX-parte01.md` (tarefa `t_2d9f22b1`). Tudo abaixo é execução **offline**; nenhum `dotnet run`, nenhum build, nenhum deploy, nenhum jogo.

## 1. Arquivos da entrega e hashes antes/depois

Hash físico (SHA-256 do arquivo em disco, LF), medido antes e depois da correção:

| Arquivo | Antes | Depois | Linhas |
|---|---|---|---|
| `tools/automacao/aut5/test_aut5.py` | `b624c5785ff5d44e9071317d14c4c7aa5f674287e3492fa189add8f614192062` | `01a57737b9208073b640859904937c49b7feb343b4cb6e5968fa58d2807e7b78` | 850 → 1383 |
| `tools/automacao/aut5/test_snapshot_modal.py` | `054aecb14eb53700d3f0aa28d9b51e221c82e4f93a972d5a36f15bafcb4c3e96` | `9fac95e50bd9f2b6cb6e0fabb3399b9e12736058e7d8fb4abc97afea094fce90` | 129 → 214 |

**Intocados** (byte-idênticos ao baseline e ao diagnóstico):

| Arquivo | SHA-256 |
|---|---|
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193` |
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee` |
| `tools/automacao/aut5/aut5.py` (avaliador) | `02e76929f1aa7c931863d6149902125d91132fdd0fd064fbc0d533480eb89c7b` |
| `tools/automacao/aut5/fixtures/log-completo.log` | `574f8f7b9fd4bbbd119ea78d17017153e17a5aff4b06694f0fc1fd85ea633094` |
| `RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj` | `5d8bb0c12835e5d6f9c5fa64d924cd4407b52149eb984983232025c174e345cb` |

O par congelado foi conferido **antes e depois** da instalação e o censo da cópia isolada confirma que **só** os dois arquivos de teste mudaram (254 arquivos conferidos, nenhum ausente). Nenhum `git add`/`commit`.

## 2. RED-GREEN de cada defeito (executado)

Bancada: `prova_contrato_aut5.py` (workspace da tarefa), que lê a cópia isolada, monta as cópias negativas **em memória** e usa os **originais** `test_aut5.py`/`test_snapshot_modal.py` como referência do contrato velho. Resultado: **26 verificações, 0 falhas**.

| Defeito | RED (contrato velho × instrumento congelado) | GREEN (contrato novo) |
|---|---|---|
| 1 fixture | log histórico `0.3.2` × fonte `0.3.3` → `AUT5-boot-rstv=REPROVADO`, `exit 1` (o caso positivo velho esperava `INDETERMINADO/2`) | fixture de teste `0.3.3` sem hash de DLL → `INDETERMINADO`, `exit 2`; controle negativo `0.3.2` → `REPROVADO/1` |
| 2 extrator | assinatura literal `private … Leitura(` → `corpo=None`; 7/7 campos "não emitidos" | visibilidade real `internal` aceita, corpo preservado, 7/7 campos presentes |
| 3 harness | `probe sem metodo real: private static Type Tipo(string nome)`; com `Tipo` privatizado **só na cópia**: `Passo nao captura o alvo do modal` | preflight limpo; cadeia real `['Passo','PassoLeitura','IniciarSnapshotDoModal']`; visibilidades `{internal, private}`; 5 controles negativos reprovam |
| 4 viewport | `"tela" in leitura` → `False` no instrumento congelado (o campo sai de `Geometria`) | dataflow `Leitura → Geometria(t)` com `'tela'` e `Screen.width/height` conferidos; 6 controles negativos reprovam |
| 5 integração | `log-real` rodava incondicionalmente em `CASOS`; DLL do perfil `98f19bd6…` (105 984 B) ≠ DLL do repo | `log-real` em `CASOS_INTEGRACAO` com pré-requisito; sem `AUT5_LOG_REAL=1` sai `NAO_EXERCITADO` |
| trava | — | `SPAWNS = 0`: nenhum subprocesso disparado em nenhuma verificação |

Comandos (cópia isolada, e depois no repositório):

```
python tools/automacao/aut5/test_aut5.py
    GRUPO|NAO_EXERCITADO|log-real|perfil r2modman Default desta maquina …
    GRUPO|NAO_EXERCITADO|snapshot-modal-CSharp|compilacao/execucao do harness C# …
    RESULTADO|INCOMPLETO|aut5-rstv|suite OFFLINE (identidade de teste declarada) PASSOU em 16
    grupos; integracao NAO_EXERCITADA: log-real, snapshot-modal-CSharp — isto NAO e a suite
    completa verde                                        -> exit 2

python tools/automacao/aut5/test_aut5.py --contra-prova
    CONTRA-PROVA|PASSOU|aut5-rstv|isca 'sempre OK' nao passa … -> exit 0

AUT5_MANIFESTO=<arquivo> python tools/automacao/aut5/test_aut5.py
    → manifesto com grupos_executados (16) e grupos_nao_exercitados (2 + pré-requisito)
```

Os **16 grupos offline** passam, incluindo o caso positivo (boot `INDETERMINADO`), o novo `velho-boot` (`REPROVADO/1`), os defeitos plantados e o `preflight-snapshot-modal`. A contra-prova continua provando que o `REPROVADO` vem da **regra**, não de passe livre.

## 3. Contrato do contrato (o que a suíte garante agora)

1. Teste offline hermético tem **identidade de teste explícita e declarada** (`IDENTIDADE_DE_TESTE`): repositório, versão da fonte e **ausência** de identidade de DLL.
2. Grupo de integração (ambiental ou compilado) **nunca** roda por omissão e **nunca** some como PASSOU: sai `GRUPO|NAO_EXERCITADO|…` com pré-requisito, e a suíte retorna `2` (`INCOMPLETO`).
3. Ausente, `null` e não identificado **nunca** são OK; versão divergente **continua** `REPROVADO` (`aut5.py:308-322` intacto).
4. Nenhum hash é inventado; nenhuma fixture/sintética é promovida a runtime; nenhum número de versão é inventado no teste (a versão antiga plantada vem do log histórico da baseline).
5. Nenhuma cópia de controle negativo chega ao probe do repositório: as mutações vivem em memória, no teste.
6. Sem autorização de compilação, **nenhum** subprocesso pode sair (trava de spawn), inclusive por caminho indireto.

## 4. NAO_EXERCITADO (declarado, não presumido)

- `snapshot-modal-CSharp` — execução do harness C#: **NAO_EXERCITADO** (compilação vedada neste escopo). O que existe é o contrato **estático** do harness, com RED-GREEN e controles negativos.
- `log-real` — integração ambiental: **NAO_EXERCITADO** (perfil da máquina, DLL do perfil ≠ DLL do repo). Não autoriza deploy corretivo nem reinstalação de DLL.
- Suíte completa e CI remoto: não executados. `tools/automacao/aut5/test_aut5.py` continua **fora** de `.github/workflows/validate.yml`; este trabalho não é gate de ORG-R2/R3/R4.

## 5. Handoff

- Entrega revisada via `kanban_request_review` no cartão `t_2d9f22b1`.
- Artefatos da prova (workspace da tarefa): `prova_contrato_aut5.py`, `prova-aut5fix.json`, `editor_aut5b.py` (receita da edição por âncoras), `originais/` (contrato velho de referência), `manifesto-repo.json`, `baseline-hashes.json`.
- `hotspot: tools/automacao/aut5/` — `test_aut5.py` e `aut5.py` concentram as frentes AUT5-F1/F2 e esta correção; qualquer trabalho novo nesse diretório deve reler o contrato antes de mexer.
- Nenhum cartão novo foi criado: não há dependência das frentes ORG-R2/R3/R4 nem autorização nova indispensável neste escopo.
