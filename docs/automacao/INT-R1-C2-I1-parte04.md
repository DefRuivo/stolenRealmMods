# INT-R1-C2-I1 — parte 04: correções da revisão independente (rodada 1) — B1, B2, B3

Cartão `t_a706b09c`. A revisão independente da rodada 1 (comentário de 11/10/2026, 05:31)
pediu **três** correções (B1, B2, B3) e declarou o resto **verificado e aprovado** (a ponte da
parte 01, o harness de 17 testes e as 10 mutações `0→1→0` **não** foram refeitos). Esta parte é
**aditiva**: a parte 02 não foi sobrescrita — onde ela estiver errada, o número vivo está aqui, e
a errata está nomeada no §4.

Todas as provas desta parte são **offline**: nenhum jogo aberto/encerrado, nenhum save, nenhum
`deploy`, nenhuma instalação, nenhum `git add`/`commit`/`push`.

---

## 1. B1 (bloqueia) — a suíte offline do runtime AUT-4 estava VERMELHA

### 1.1 O defeito, medido

```
python tools/automacao/runtime/roda_testes_runtime.py     # antes desta parte
[REPROVOU] testes\t_aut4_estado_docs.py
   | A7: o hash declarado da DLL tem de ser o dos bytes em disco:
     esperado '05b982de…', obtido '95069e9c…'
[REPROVOU] testes\t_aut4_runbook.py
   | o runbook tem de casar com o disco (hashes/chaves/contagens):
     ['hash de DLL do probe nao declarado no runbook (esperado 05b982de…)',
      'hash de fonte do probe nao declarado no runbook (esperado 6d8a3205…)',
      'hash de projeto do probe nao declarado no runbook (esperado 418a559b…)']
VEREDITO: VERMELHO (exit 1)
```

A causa é a mesma classe do achado A7 (`t_b62359c3`): **identidade declarada ≠ bytes em disco**.
A entrega da parte 01/02 mexeu no `AUT4ProbePlugin.cs` e no `AUT4Probe.csproj` e **rebuildou** a
DLL, mas os hashes *frozen* continuaram com os valores anteriores — exatamente a deriva que
`t_aut4_runbook.py` existe para bloquear (o runbook é o documento que o dono lê **antes** de
autorizar a rodada em jogo).

### 1.2 A correção: re-declarar o **medido**

| artefato | valor declarado (antes) | valor medido agora |
|---|---|---|
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2` | `beaf965a162c9452bee8302ecadbcc5ae42322d388c798179911e1660c07c193` |
| `tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj` | `347770d091a6a173cbebb988fb30d2a7a73df4d64e316033812e4220869057f4` | `418a559beb424066633bc4aed604cd5c9cef9825c9ef5d4950b84f6f26ba0ff6` |
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `95069e9cbc5e1e7784f80b34589e54cf19651969cddad86b6a35d9b94c89a865` | `7f9a4cf1f62b721faff3f43e16ecb0e2313e748cf03c0eee5cca543c4e2575ee` |

Comando que mediu (nenhum valor foi copiado de outro documento):

```bash
sha256sum tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs \
          tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj \
          tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll
wc -l tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs     # 2012
```

O build foi refeito (`0 Erro(s)`, `1 Aviso(s)` MSB3277 **pré-existente** — o mesmo `System.Net.Http`
que o `AUT-4-estado.json` já registrava), com `USERPROFILE`/`APPDATA`/`LOCALAPPDATA` redirecionados
para pasta de trabalho e **sem** flag de deploy (o csproj não tem alvo `DeployToBepInEx`):

```bash
dotnet build -c Release --no-incremental -v q -p:DeployToBepInEx=false AUT4Probe.csproj
```

Re-declarado em **três** documentos (os três que afirmavam a identidade):

1. `docs/automacao/AUT-4-runbook-rodada-autorizada.md` §2 — fonte, projeto e DLL;
2. `docs/automacao/AUT-4-estado.json` — `probe_fonte_sha256`, `probe_dll_sha256` e o campo **novo**
   `probe_projeto_sha256` (o estado declarava o **caminho** do csproj mas não o hash dele; o runbook
   declarava o hash — agora os dois declaram o mesmo, medido);
3. `docs/automacao/AUT-4-preparacao.md` (build check do AUT-4) — as duas linhas de hash do probe,
   que repetiam os valores anteriores.

### 1.3 Prova final (exit 0)

```
python tools/automacao/runtime/roda_testes_runtime.py
 VEREDITO: VERDE (exit 0) — 16 teste(s)          # os 16 PASSOU, incluindo t_aut4_runbook.py e t_aut4_estado_docs.py

python tools/automacao/runtime/roda_testes_runtime.py --contra-prova
 VEREDITO: VERDE (exit 0) — 33 teste(s)          # todas as iscas reprovam como devem
```

O `t_aut4_runbook.py` continua **travando** o runbook contra o disco (hash de fonte/csproj/DLL,
chaves vivas de `coletor.CFG_CHAVES`, contagens reais de testes/iscas e as frases de limite): o
verde acima é o `checar(...) == []` para os **novos** valores, e o vermelho do §1.1 é a prova de
que a trava funciona nos valores velhos.

---

## 2. B2 — a reconstrução do pré-edição perdia uma linha de **outro** cartão

### 2.1 O defeito, medido

`docs/automacao/INT-R1-C2-I1-evidencias/AUT4ProbePlugin-pre-edicoes.cs.txt` (a reconstrução do
arquivo **antes** das 5 edições deste cartão) foi gerada por inversão por âncora e **perdeu a
linha de código**:

```
            _dir = _outDir.Value;      # viva hoje em AUT4ProbePlugin.cs:219 (venha de outro cartão)
```

Ela é usada logo depois (`Directory.CreateDirectory(_dir)`, `Path.Combine(_dir, …)`) e **não** é
deste cartão: nenhuma das 5 edições toca essa linha. Efeito: o hunk 2 do diff aparecia como
`+1/−1` a mais, apresentando ao auditor uma linha de outro cartão como se esta entrega a tivesse
adicionado — quem audita não consegue atribuir.

Medições que fecham o caso (executadas nesta rodada):

| arquivo | linhas | sha256 |
|---|---|---|
| reconstrução antiga (sem a linha) | 1956 | `7aa6b99970bec7b756b44f670def5b7bc5f8899a7b6d15157c4bbe71c44c234e` |
| reconstrução + a linha | 1957 | `ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2` |
| `git show HEAD:…/AUT4ProbePlugin.cs` | 1084 | `48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94` |

Ou seja: a reconstrução **com** a linha volta a ser **byte a byte** o arquivo pré-edição real —
o `ecdcce13…` que era o hash declarado no runbook §2 e em `AUT-4-estado.json` **antes** deste
cartão. (O `HEAD` tem 1084 linhas: o arquivo está sujo na árvore de trabalho por vários cartões —
é o hotspot registrado no cartão pai —, então `git diff`/`HEAD` **não** isolam esta entrega.)

### 2.2 A correção

A pré-edição foi **regenerada com a linha presente** e o diff, refeito:

```
docs/automacao/INT-R1-C2-I1-evidencias/AUT4ProbePlugin-pre-edicoes.cs.txt
  linhas 1957 · sha256 ecdcce138a2a7c955023bde0d8da192a1bdf8186422d3ab36a90972a0da67bd2

docs/automacao/INT-R1-C2-I1-evidencias/edicoes-aut4probe.diff
  sha256 eb6ca8b2016f441b9bf18652ff21b44c2529e2eab261f22f6e886ad0a5c8b7b9
  5 hunks · +65 / −10
```

O hunk 2 agora é **só inserção** (`@@ -202,6 +211,11 @@`), com `_dir = _outDir.Value;` como
**contexto**:

```
             + "RESTAURADOS depois, com conferencia explicita da restauracao.");
 
+            _ponteApiCfg = Config.Bind("Geral", "PonteApiHook", false,
+                "OPT-IN (default FALSE): consumir o hook ui.localized entregue pela ponte "
+                + "Gumatos.KitApiBridge.AUT4 (assembly companheiro, carregado por nome EXATO). O patch "
+                + "proprio em OptionsManager.Localize foi REMOVIDO; sem esta ponte o gatilho por "
+                + "localizacao nao existe e restam GUIManager.Update e o PlayerLoop.");
             _dir = _outDir.Value;
             _orcamentoSeg = _orcamento.Value;
```

Os cinco hunks são, na ordem: (1) os dois campos novos (`:77-85`); (2) a config nova — o hunk do
exemplo acima; (3) `GanchoTodos("OptionsManager","Localize")` → `LigarPonteOpcional()`;
(4) `GanchoTodos(...)` → `LigarPonteOpcional()` (corpo); (5) `Finalizar()` desfaz a ponte. Fora
desses cinco pontos o arquivo **não** difere da pré-edição.

---

## 3. B3 — a saída *default* não era literalmente a de hoje

### 3.1 O defeito

Com `PonteApiHook=false` — o **default** — o probe ainda:

* gravava um `Marco(...)` novo no caminho desligado (`:342` de então);
* criava a chave `_passos["ponte_api"]` no `Finalizar()` (`:645-646` de então). Como
  `_res["passos"] = _passos` é atribuído no `Initialize()` (`:242`) e o dicionário é mutado por
  referência, essa chave **virava campo novo do JSON de saída**.

Isso contradizia o critério de aceite 3 do cartão ("com a config em false e sem o companheiro a
saída é a de hoje") e a frase de `INT-R1-C2-I1-parte02.md` §3.3 ("Não há novo campo no JSON de
saída").

### 3.2 A correção (o código passou a cumprir o critério)

| onde (vivo, depois) | antes | agora |
|---|---|---|
| `LigarPonteOpcional()` — `AUT4ProbePlugin.cs:343` | `if (!_ponteApiCfg.Value) { Marco("…PonteApiHook=false…"); return; }` | `if (!_ponteApiCfg.Value) return;` — **silencioso** |
| `Finalizar()` — `AUT4ProbePlugin.cs:646-650` | `try { _ponteApi?.Dispose(); … _passos["ponte_api"] = "encerrada"; } catch { … }` | `if (_ponteApi != null) { try { … } catch { … } }` — sem ponte ligada **nada** é escrito |

Consequência: no caminho default (config `false` **ou** companheiro ausente/recusado) o probe não
emite marco novo nem chave nova — a saída é a de hoje. Os `Marco(...)` que sobraram (`:358`, `:364`)
pertencem ao caminho **opt-in** (`PonteApiHook=true`), que por definição já é "saída nova".

Rodada em jogo comparada com `docs/automacao/AUT-4-evidencias/`: **NAO_EXERCITADO** (este cartão não
abre o jogo — a igualdade foi conferida por leitura de código).

---

## 4. Errata da parte 02 (o texto vivo é este)

* `INT-R1-C2-I1-parte02.md` §2 (:53-56) declara que a reconstrução difere do pré-edição real "em
  **uma linha em branco**" entre `_dir = _outDir.Value;` e `_orcamentoSeg = _orcamento.Value;`.
  **Falso como está escrito**: a divergência era a **própria linha de código**
  `_dir = _outDir.Value;`, ausente da reconstrução. O número vivo está no §2.1 acima; a
  reconstrução foi corrigida (§2.2), então o hunk 2 do diff **não** aparece mais com um `+1/−1`
  a mais. A parte 02 fica como está, por histórico — este § é a errata.
* `INT-R1-C2-I1-parte02.md` §3.3 ("Não há novo campo no JSON de saída") passou a ser
  **verdadeira** por causa do conserto do §3.2 — antes era falsa (o `_passos["ponte_api"]` era um
  campo novo).

---

## 5. Fora do escopo, declarado (não é regressão deste cartão)

`tools/automacao/aut5/test_aut5.py` sai **exit 1** — **antes e depois** deste cartão, com o
**mesmo** conjunto de 14 falhas (10 delas sobre âncoras do probe). A causa é pré-existente:
o teste procura `private Dictionary<string, object> Leitura(TMP_Text t` e
`private static Type Tipo(string nome)`, e a fonte viva tem `internal Dictionary<string, object>
Leitura(TMP_Text t, List<object> ownersFunil)` (`:718`) e `internal static Type Tipo(string nome)`
(`:1879`). **Nenhuma dessas linhas está no diff deste cartão** (0 ocorrências no
`edicoes-aut4probe.diff`).

Prova A/B executada nesta rodada: os `CASOS` do módulo foram rodados duas vezes, com
`SEMENTE_PROBE` apontando (a) para a fonte viva e (b) para a pré-edição reconstruída — as listas de
falhas são **idênticas** (14 totais; as mesmas 10 âncoras). O suíte AUT-5 não faz parte de
`roda_testes_runtime.py` nem do `.github/workflows/validate.yml`; o vermelho dele é declarado aqui
para não virar surpresa.

O mesmo vale para a suíte maior de mods (`python tools/testes/roda_testes.py --puros`): ela sai
**exit 1** com **1** reprovação — `deploy-optin-repo` —, e os únicos arquivos que ela acusa são
`scratch/kit/KIT-14-run699/**` e `scratch/kit/KIT-14-run710/**` (csproj de bancada deixados por
outros cartões; um deles nem é XML válido). Nenhum deles é csproj deste cartão e este cartão **não
criou csproj algum**. Os 94 demais passam. Defeito pré-existente e fora do escopo, declarado aqui
pelo mesmo motivo.

---

## 6. NAO_EXERCITADO desta parte (com motivo)

* **Runtime/jogo**: B1/B2/B3 foram provados offline. Harmony real, BepInEx carregando com
  `EnableHooks=true`, ponte ligada dentro do processo do jogo, PNG/clique/navegação: **NAO_EXERCITADO**
  (exige autorização do dono + jogo aberto — proibido neste cartão).
* **Igualdade byte a byte da saída default do probe** com a rodada de `docs/automacao/AUT-4-evidencias/`:
  **NAO_EXERCITADO** — provada por leitura de código (§3.2), não por execução em jogo.
* **Re-declaração de hash**: por construção, o próximo cartão que editar `AUT4ProbePlugin.cs` **tem**
  de re-declarar (§1.2) — é o que `t_aut4_runbook.py`/`t_aut4_estado_docs.py` exigem.
* **Deploy/instalação/publicação**: 0 (nenhum), por limite do cartão.
