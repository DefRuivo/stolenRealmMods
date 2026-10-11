# KIT-03R — Revisão independente de KIT-03 (PARECER FINAL)

- Cartão revisado: **KIT-03** (t_5fe44ff0), entregável `docs/automacao/KIT-03-entrega.md`.
- Cartão desta revisão: **KIT-03R** (t_9670452a), run **603**, perfil `default`.
- Implementador do escopo: t_5fe44ff0 (run 599, perfil `default`, encerrado pelo operador em
  `kanban_request_review` com implementer/reviewer vazios — ver "Independência" abaixo).
- Revisor: esta run. **Independência por run/sessão, não por perfil** (só existe o perfil `default`;
  mesma ressalva já registrada nas revisões AUT-4R3/R4 e KIT-04R). Veredito construído por execução
  própria no disco, sem reutilizar o relatório do implementador.
- Modo: **offline**. Nenhum jogo aberto/encerrado, nenhum save/perfil do dono tocado, nada instalado,
  nada publicado, nenhum commit. Build com deploy **não** executado (não autorizado).
- Provas: `docs/automacao/KIT-03R-parte01.md`, `-parte02.md`, `-parte03.md` (comandos + saídas reais).
  Sandbox: `scratch/kit-revisao/sandbox/` (cópia; sem `.git`, sem credenciais, sem perfil do dono).

## Identidade dos arquivos vivos (SHA256 medido nesta sessão — `sha256sum`)

| Arquivo | SHA256 | Bytes |
|---|---|---|
| docs/automacao/KIT-03-entrega.md | d7203e671bfdb4a13b829ff6185f109bc7db330fd6fe3d80077403081b6b9ce5 | 8746 |
| scratch/kit/run-isolation-tests.sh | 9faa67e531571c9306d97855717673226ff154b4a618c474da50808ff2cb62eb | 10105 |
| scratch/kit/detect-env.sh | 996fa18e5a62ea1b42a0a440f10948d4ad0cd30ffe6b99011e84992371b57b8e | 6481 |
| scratch/kit/snapshot.sh | 4f826b1a33964103473192918daa0dd2ac4852f36cd37d9a373952a998a4222a | 6070 |
| scratch/kit/isolacao.sh | de87e727722851dc24d4f45a94045740a68bce79074950e384997de104917c45 | 7568 |
| scratch/kit/front-unica.sh | cddcfd357374f6c90e39f1570a9209969f8aed0b82a34dc20532464e08b2281b | 6140 |
| docs/automacao/KIT-03-entrega.md (declarado dentro dele) | "a preencher" | — |

O entregável **não registra hash algum** (seções "Hashes SHA256: A preencher" / "Hash SHA256 deste
arquivo: (a ser preenchido)") — a identidade exigida pelo cartão foi suprida por esta revisão, não
pelo implementador. `scratch/kit/detect-any.sh`, citado no handoff do cartão-pai, **não existe**.

## Veredito por critério

| # | Critério | Veredito |
|---|---|---|
| C1 | Identidade dos arquivos vivos no entregável | **ACHADO** (A6: hashes "a preencher"; `detect-any.sh` citado e inexistente) |
| C2 | Detecção de ambiente exercitada | **ACHADO** (A14 cwd-dependente + exit 1 fora da raiz; A15 `Player.log` com caminho errado; A16 doc × implementação divergem sobre onde ficam os saves) |
| C3 | Snapshot + rollback "exato", mesmo em falha parcial | **ACHADO** (A11: só apaga o listado na lista global `arquivos-criados.txt`; `hashes-antes.txt` nunca é conferido; sobra silenciosa) |
| C4 | Prova de isolamento de saves | **FALHOU** (A2: tautologia + veredito fixo + exit 0 mesmo com FALHOU) |
| C5 | Front única / PID / sessão do dono | **FALHOU** (A13: o lock nunca recusa — lê `tail -1` como PID e recebe o worker; 2º `acquire` passa por cima) |
| C6 | Ausência de caminhos pessoais fixos | **ACHADO** (A12 `KITS_DIR` ignorado por 4 scripts; A3 `Abyssus`; A15; A17 `C:/Users/Pichau` hardcoded em `isolacao.sh:187`; A18 `detect-env.sh:147` cadeia morta) |
| C7 | Resíduos de instalação | **OK** (nenhum resíduo atribuível a KIT-03 no perfil; nada instalado) |
| C8 | Runner orquestrador fiel (sem falso-verde) | **FALHOU** (A1: morre em `((TOTAL++))` linha 59, **exit 1**, zero testes; A5: `skip` conta como `PASSED` e exit 0) |
| C9 | Reuso de infraestrutura sem duplicar | **ACHADO** (A4 caminhos errados no Teste 6; zero reuso de `roda_testes_runtime.py`/`controle_negativo.py`; runner paralelo reescrito) |
| C10 | Build isolado `-p:DeployToBepInEx=false` + pre-flight | **NÃO_EXERCITADO** (A19: a flag só existe em prosa; nenhum script de build/gate; `scratch/kit/build/` vazio) |
| C11 | Escopo (nada instalado/publicado/produto tocado) | **OK** |

**Parecer: REPROVADO.** 3 critérios FALHOU (C4, C5, C8), 5 ACHADO, 1 NÃO_EXERCITADO, 2 OK.
As afirmações centrais do entregável — "TODOS OS TESTES DE ISOLAMENTO PASSARAM", "Isolamento
comprovado: PASS", "Lock adquirido/release PASS" — **não se reproduzem no disco**: o runner não roda,
a prova de isolamento é uma string fixa e o lock não exclui ninguém. A "prática obrigatória" de
teste-que-reprova não foi exercitada em nenhum ponto: nenhum caminho negativo foi plantado pelo autor.

## Achados com reprodução (comando → observado)

- **A1 GRAVE** — `KITS_DIR=kit bash kit/run-isolation-tests.sh` → só imprime o cabeçalho, **exit 1**.
  Trace: `+ (( TOTAL++ ))` é a última linha executada. `kit/results/` e `kit/logs/` ficam vazios.
  Evidências citadas no entregável `scratch/kit/logs/test001-detect-env.log` e `test004-isolation.log`
  **não existem**; `scratch/kit/backups/20261008_183747/` existe mas está **vazia**.
- **A2 GRAVE** — `SAVES_DIR=kit/isolated-rev bash kit/isolacao.sh prove-isolation` → imprime
  `FALHOU: Save descartavel esta DENTRO de ...` e **mesmo assim** imprime
  `3. Isolamento: SAVE DISCARDABLE ESTA FORA DOS SAVES PRINCIPAIS` com **exit 0**. O runner decide
  esse critério por `grep` dessa linha fixa → "comprovação" sempre verde.
- **A13 GRAVE** — dois `acquire` seguidos: o 2º **não é recusado** ("Lock stale detectado (PID default
  inativo)"); `check` responde `OK (stale)` com lock ativo. O controle de frente única não existe.
- **A11 MÉDIO** — rollback restaura o arquivo alterado (OK), mas arquivo criado **não listado** em
  `arquivos-criados.txt` sobrevive (`new2.dll persiste? SIM`) e nada é reportado.
- **A14/A15/A16 MÉDIOS** — `detect-env.sh` fora da raiz do repo: exit 1, JSON não gravado
  (`SAVES_DIR` default `...\AppData\Local/Abyssus/Saved/SaveGames`, que **existe** no disco com
  `Profile1.sav`); o caminho `Player.log` do script não existe (o real é `AppData\LocalLow\...`); e o
  entregável (linha 91) declara os saves em `%LOCALAPPDATA%Low\Burst2Flame ...\Saved\`, no lugar errado.
- **A12 MÉDIO** — `snapshot.sh`/`isolacao.sh`/`front-unica.sh`/`detect-env.sh` gravam em
  `scratch/kit/...` relativos ao cwd e **ignoram `KITS_DIR`** — com `KITS_DIR` diferente (o próprio
  runner usa `$KITS_DIR/backups`) snapshot e runner apontam para diretórios distintos.
- **A19 MÉDIO** — não existe pre-flight de deploy: `grep -rn DeployToBepInEx scratch/kit/` só acha
  prosa no entregável; nenhum build isolado foi feito (`scratch/kit/build/` = 2 diretórios vazios).

## Correções a levar ao implementador (abrir em cartão de correção)

1. `run-isolation-tests.sh`: trocar `((TOTAL++))` por `TOTAL=$((TOTAL+1))` (ou remover `set -e` do
   bloco); garantir que o runner **chegue** aos 6 testes e que `skip` **não** incremente `PASSED`;
   exit ≠ 0 quando houver skips ou falhas.
2. `isolacao.sh prove-isolation`: remover a conclusão fixa; derivar a conclusão do resultado real;
   implementar verificação com diretório **plantado** dentro do suposto `SAVES_DIR` (controle
   negativo) e **sair ≠ 0** quando o isolamento falhar.
3. `front-unica.sh`: ler o PID da **mesma linha** em que foi escrito (ou usar 1 linha, só o PID);
   o PID deve ser o da sessão de teste (não de um script efêmero) e `acquire` deve **recusar**
   (exit 1) quando houver lock vivo; usar `--force` ou remover a opção.
4. Rollback: apagar arquivos criados por **diff contra o snapshot** (não por lista manual global) e
   conferir `hashes-antes.txt` ao final, falhando se o diretório não voltar exatamente ao estado.
5. `detect-env.sh`: usar `KITS_DIR`/caminhos absolutos derivados do próprio script (`$(dirname "$0")`),
   corrigir `Player.log` para `LocalLow`, e não engolir o `check` de CIC em cadeia morta.
6. Entregável: corrigir o caminho dos saves (`%LOCALAPPDATA%\Abyssus\Saved\SaveGames`) **ou** usar
   explicitamente o caminho que o `detect-env.sh` valida; preencher a seção de hashes com os SHA256
   reais e remover a citação a `detect-any.sh` (inexistente).
7. Reuso: o Teste 6 deve apontar para `tools/automacao/...` (não `scratch/tools/...`) e o runner deve
   reusar `tools/automacao/runtime/roda_testes_runtime.py` / `controle_negativo.py` em vez de inventar
   um runner paralelo incompatível com pytest/exit 0-1-2.
8. Reabrir com **controle negativo plantado** (defeito plantado que deixa o runner vermelho) antes de
   pedir reconferência; e implementar/declarar o pre-flight de build `-p:DeployToBepInEx=false`.

## Lacunas declaradas (não são OK)

- Runtime em jogo (instalar/abrir/save) segue **NÃO EXERCITADO** — exige autorização explícita do dono
  e a frente única; nada nesta revisão o produziu.
- O cartão KIT-G1 (gate humano) e AUT-4 dependem deste parecer; a correção acima deve preceder qualquer
  rodada runtime de isolamento.

## Passo seguinte concreto

Abrir **KIT-03F** (implementador, filho de KIT-03R) com os 8 itens acima; ao fechar, pedir reconferência
por revisor em run separada sem apagar histórico. O gate humano KIT-G1 fica **atrás** do KIT-03F
(isolamento não confiável ⇒ não autorizar rodada runtime).
