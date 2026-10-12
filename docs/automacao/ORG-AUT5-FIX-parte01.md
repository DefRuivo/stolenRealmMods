# ORG-AUT5-FIX — parte 01: correção do contrato de testes AUT5

Tarefa `t_2d9f22b1` (ORG-AUT5-FIX), derivada de `t_ceceef6b` (ORG-AUT5-DIAG, revisado e aprovado). Escopo **TESTES/PARSER**, offline, em 11/10/2026. Nenhum build, nenhum deploy, nenhum `dotnet run`, nenhum jogo, nenhuma publicação. O instrumento congelado (`AUT4Probe`), a receita congelada e o produto RSTV **não foram tocados**.

Fonte de verdade de partida: `docs/automacao/ORG-AUT5-DIAG-parte01.md` e `parte02.md`, mais `diagnostic-evidence.json` e `investigate_aut5.py` no workspace do pai.

## 1. O que foi corrigido, e por quê

Os cinco defeitos demonstrados pelo diagnóstico estavam **no teste**, não no mod nem no probe. Cada um foi corrigido com prova RED-GREEN: o contrato **antigo** reprova o instrumento congelado (RED) e o **novo** fecha (GREEN), com controles negativos que fazem o contrato novo reprovar cópias defeituosas em memória.

### 1.1 Fixture velha contra a fonte (defeito 1)

- Antes: `test_aut5.py` usava `fixtures/log-completo.log` (boot `0.3.2`) como entrada do caso **positivo**, esperando `AUT5-boot-rstv = INDETERMINADO` e `exit 2`; a fonte declara `0.3.3`. Pela regra do avaliador (`aut5.py:308-314`) versão divergente é `REPROVADO` — a premissa do caso positivo é que estava velha.
- Agora: existe uma **fixture de teste hermética** derivada em tempo de execução (`_escreve_fixture_hermetica`), com **apenas a linha de boot realinhada à versão declarada pela fonte desta cópia**. Nenhum hash de DLL é inventado e nenhum campo é acrescentado. A identidade de teste fica **explícita** em `IDENTIDADE_DE_TESTE` (`repositorio`, `versao_da_fonte`, `dll_declarada = None`).
- O log histórico versionado **não foi editado**: virou o controle negativo `caso_velho_boot` (novo caso `velho-boot`), que exige `REPROVADO` + `exit 1` + falha automática na decisão.
- Matriz medida (mesma do diagnóstico, agora como teste): `0.3.2 → REPROVADO/1`; alinhada sem DLL `→ INDETERMINADO/2`; `0.3.2` (antiga) `→ REPROVADO/1`.
- A regra do avaliador `aut5.py:308-322` **não foi tocada** — o arquivo `aut5.py` está byte-idêntico (`02e76929…`).

### 1.2 Extrator preso a assinatura/visibilidade (defeito 2)

- Antes: `_corpo_do_metodo` fazia `fonte.find("private Dictionary<string, object> Leitura(TMP_Text t")`. O membro real é `internal` (`AUT4ProbePlugin.cs:718`, documentado para reuso nas linhas 715–717) → `None` → as mensagens derivadas diziam que os sete campos não eram emitidos.
- Agora: o extrator resolve a assinatura **sem exigir a visibilidade literal**, aceita a visibilidade real (`internal`/`private`, registrada em `info["leitura_visibilidade"]`) e devolve o **corpo verbatim** do método (casamento de chaves com literais/comentários ignorados). Rejeita `public` (membro interno do probe) e falha se a assinatura não existir.
- Os sete campos (`snapshot_antes/depois`, `tooltip_pai_antes/depois`, `tooltip_indice_antes/depois`, `janelas_duplicadas`) são conferidos no corpo real: `7/7` presentes.

### 1.3 Harness C# com duas premissas estruturais obsoletas (defeito 3)

- Antes: `test_snapshot_modal.py:17` exigia `private static Type Tipo(string nome)` (a fonte tem `internal`, `:1879`) e `:97-98` exigia `IniciarSnapshotDoModal();` **inline** no corpo de `Passo`. Corrigir só a visibilidade não basta: a cadeia real é `Passo:469 → PassoLeitura:507 → IniciarSnapshotDoModal:513`.
- Agora: as assinaturas são pedidas **sem visibilidade** e a visibilidade real é registrada; a captura é conferida pela **cadeia de chamadas real** no grafo de métodos do próprio fonte (`Passo → PassoLeitura → IniciarSnapshotDoModal`), mais a **guarda de ordem** (a captura precede `ColetarObservacoes` na fase de leitura) e a alcançabilidade de `Leitura` a partir do driver.
- O preflight **não compila nada** e não spawna processo: roda sempre, no grupo `preflight-snapshot-modal`.
- Controles negativos do próprio preflight, todos em **cópias em memória** do fonte: `visibilidade-publica`, `tipo-renomeado`, `dispatch-do-driver-removido`, `captura-removida`, `captura-depois-da-coleta`.

### 1.4 Verificação de viewport por string (defeito 4)

- Antes: `test_aut5.py:404` usava a condição `leitura and '"tela" in leitura'` — um teste de pertinência do literal `"tela"` no corpo de `Leitura`. O campo é emitido por `Geometria` (`:1943-1963`), não por `Leitura` (`:747`): a condição **reprova** o instrumento congelado (e, com o extrator antigo, nem era avaliada — curto-circuito com `None`).
- Agora: verificação por **dataflow** — `Leitura` tem de **chamar** `Geometria(t)`; `Geometria` tem de emitir `"tela"` e derivá-lo do viewport (`Screen.width`/`Screen.height`), e `Leitura` tem de ser alcançável a partir do driver. Controles negativos removendo campo/sentido **somente em cópia/string de teste**: `campo-removido-do-leitura`, `chamada-de-geometria-removida`, `tela-removida-da-geometria`, `viewport-constante-na-geometria`, `depois-nao-fechado`, `visibilidade-fora-do-contrato`. **Nunca** no probe do repositório.

### 1.5 Integração ambiental rodando incondicionalmente (defeito 5)

- Antes: `CASOS` incluía `log-real` sem condição; o caso lê o `LogOutput.log` **mutável** do perfil e exige DLL do perfil byte-igual à do repo (`:515-518`). A DLL do perfil existe (105 984 bytes, `98f19bd6…`) e difere da do repo — dependência **ambiental demonstrada**, não defeito do mod.
- Agora: a suíte está dividida em **`CASOS_OFFLINE`** (16 grupos, herméticos) e **`CASOS_INTEGRACAO`** (`log-real`, `snapshot-modal-CSharp`), cada um com **autorização própria** (`AUT5_LOG_REAL=1`, `AUT5_AUTORIZA_COMPILACAO=1`) e **pré-requisito registrado**. Sem autorização, o grupo sai declarado `GRUPO|NAO_EXERCITADO|…` e entra no manifesto — **nunca sumindo como PASSOU**. A suíte imprime `RESULTADO|INCOMPLETO|…` e retorna `2`: verde parcial **não** é declarado verde.
- **Trava de spawn**: o harness conta subprocessos (`SPAWNS`); sem autorização de compilação a suíte falha se algum subprocesso tiver saído (`dotnet run` é bloqueado antes de compilar). Nesta entrega: `SPAWNS = 0`.

## 2. O que **não** foi feito

- Não houve `dotnet build`, `dotnet run`, deploy, abertura de jogo, rodada de boot, publicação ou aceite visual.
- Não houve edição/recompilação do probe congelado, da DLL congelada, da receita congelada, da bancada run712/run714 ou do produto RSTV.
- Não houve `git add -A` nem `commit -a`; os arquivos corrigidos ficaram no *working tree*.
- Não foi executada a suíte completa nem declarado o harness C# verde: `snapshot-modal-CSharp` permanece **NAO_EXERCITADO** (compilação vedada neste escopo) e `log-real` permanece **NAO_EXERCITADO** (dependência ambiental sem autorização).
- Rótulos/evidências históricos AUT5-F1, AUT5-F2 e ORG-R1 não foram alterados.

Continua na parte 02 (provas, hashes antes/depois e handoff).
