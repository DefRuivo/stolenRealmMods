# COR-AUT7-F2 — fecho dos achados A1–A9 do parecer COR-AUT7R

Tarefa: `t_cd1332d7` (COR-AUT7-F2), **execução 430** (2ª rodada). Fonte dos achados: parecer
independente `COR-AUT7R-revisao.md` / `COR-AUT7R-resultados.json` / `COR-AUT7R-evidencias.zip`
(t_11839818, execução 408 — distinta do autor da COR-AUT7, execução 387, e do revisor da AUT-7,
381). A 1ª rodada desta correção foi a **execução 415**; a revisão independente dela (execução
**425**) verificou e fechou A1, A2, A3, A4, A5, A7, A8 e A9, e **recusou** o A6: a fotografia do
cache `--sem-suite` cobria os artefatos de build, mas **não** as ENTRADAS que os testes mapeados
leem (`tools/fixtures/**`, lido por `t_bf_diag_orcamento`). Esta rodada fecha esse ponto e regera
a evidência.

Escopo EXCLUSIVO: `tools/automacao/estilo/**`, `tools/automacao/aceite/**` e os docs gerados
por elas. Produto/mods, `docs/cobertura/**` curado, CIC-1/2/3/4/5 e `tools/testes/**` **não**
foram editados. Nenhum build, instalação, abertura de jogo, save, deploy ou publicação.
Nenhuma trava foi enfraquecida: os consertos continuam **fail-closed** (o que era falso-OK
virou lacuna/reprovação, nunca o contrário).

## 0. O que mudou nesta rodada (execução 430) — o ponto que a revisão deixou aberto

| ponto | antes (execução 415) | agora (execução 430) |
|---|---|---|
| **A6/F2** — fotografia do cache `--sem-suite` | cobria fontes dos 4 mods medidos + `tools/testes/**` + `tools/automacao/estilo/**` + `tools/*.py` + artefatos (`dist/*.zip`, `<Mod>/bin/**/*.dll`) ⇒ `tools/fixtures/**`, lido pelos testes mapeados, **não** invalidava o cache | cobre **todas as ENTRADAS que a suíte lê**: os 6 mods, `tools/**`, `lib/**`, `docs/cobertura/**`, `ReloadProbe/**` (projeto de bancada, fora do repositório, não versionado), `scratch/**`, `docs/PLANO-DE-TESTES.md` e os projetos `*.csproj`/`*.props`/`*.targets` da árvore, **+** os artefatos medidos. A cobertura declarada vai no próprio resultado (`medicao.fotografia`) e foi **medida** (não afirmada) com gancho de auditoria sobre a rodada viva |
| **A5 (achado menor)** | o `dump-do-produto.json` trazia `total_com_predicado_estrito: 5` sem declarar o predicado — número não reproduzível pelo rótulo | cada número vem **com o predicado que o produz**: **68** com `' | '`, **5** com `desc=` (e **sem** `' | '`), **73** na união, **0** com `'" | "'` literal, **0** reconhecidas pelo `LINE` |
| regressões | 26 casos na suíte da ferramenta, 15 na do aceite; refutação em duas fases (A1–A9) | **28** casos na suíte da ferramenta (+2: cobertura das ENTRADAS e a regressão ponta a ponta com a fixture apagada) e 15 no aceite; fase nova de refutação `refutar_cor_aut7f2_entradas.py` (E1–E5) |

## 1. O que mudou, achado por achado

| achado | sev | onde estava | conserto | arquivo:linha |
|---|---|---|---|---|
| **A6** | ALTA | a fotografia do cache `--sem-suite` não cobria o artefato que a suíte **mede** (`dist/gumatos-BetterCombatText-*.zip`, `bin/<config>/*.dll`) — e, como a 2ª rodada da revisão mostrou, também **não** cobria as ENTRADAS que ela **lê** (`tools/fixtures/**` etc.) | fotografia em DUAS camadas: (a) **entradas** — `_arquivos_que_a_suite_le` sobre as raízes declaradas (`RAIZES_DA_FOTOGRAFIA`), os arquivos soltos e os padrões de projeto da árvore; (b) **artefatos medidos** — `dist/*.zip` + `<Mod>/bin/**/*.dll`. Tudo com sha256 e conjunto de CAMINHOS (entrar/sair/alterar invalida). Fora de propósito: `bin`/`obj`/`__pycache__` (derivados) e `docs/automacao/**` (saída da própria ferramenta) | `estilo_atributos.py:348` (`MODS_DA_ARVORE`/`RAIZES_DA_FOTOGRAFIA`/`PADROES_DA_FOTOGRAFIA`), `:376` (`_arquivos_que_a_suite_le`), `:434` (`_artefatos_medidos`), `:456` (`fotografia_suite`) |
| **A3** | MÉDIA | superfície do BCT detectada por **substring**: `Healthbar` ⊂ `BossHealthbar` ⇒ 6 leituras marcavam as 7 | casamento por **token** (fronteira dos dois lados), usado nas DUAS ocorrências (superfícies e idempotência) | `estilo_atributos.py:902` (`_superficies_no_alvo`) |
| **A2** | MÉDIA | o hash do config tinha de estar **dentro** da identidade do CIC-1 (que não traz config) ⇒ config legítimo saía REPROVADO e o critério nunca fechava OK | três casos distintos: bytes ≠ sha ⇒ REPROVADO; identidade **sem** hash de config ⇒ **LACUNA** nomeando o próximo passo (anexar `config_sha` no `--identidade`); identidade com hash ⇒ confronta (OK se bate, REPROVADO se é de outra rodada) | `estilo_atributos.py:835` |
| **A1** | LEVE | par BF comparado por **interseção** de chaves — chave de um lado só não era medida | comparação do conjunto **completo** (chaves de um lado só viram erro nomeado; valores da interseção continuam comparados) | `estilo_atributos.py:811` |
| **A7** | MÉDIA | evidência de item de frente só por **presença**; identidade divergente gerava lacuna **sem** rebaixar o item; o adaptador **emprestava** `fonte_sha`/`dll_sha` da rodada ao item | evidência conferida (existência + sha, sha calculado e registrado quando a frente só dá o caminho); item OK de runtime só segue com identidade **própria** conferida; item de rodada divergente é **rebaixado** para `NAO_EXERCITADO` com lacuna canônica `…/item-nao-vinculado`; a rodada entra só como rastro (`identidade_da_rodada`) | `relatorio_aceite.py:244` (`_anotar`), `:249` (`_identidade_do_item`), `:262` (`_refs_de_evidencia`), `:292` (`_rebaixar`), `:302` (`_validar_resultado_frente`) |
| **A8** | MÉDIA | o módulo real do AUT-6 **não carregava** (`aut6/cobertura.py` faz `import prova` no topo e o diretório do pacote não estava no `sys.path`) ⇒ `AUT-6/avaliador-indisponivel`, 0 itens | o diretório `tools/automacao/aut6` entra no `sys.path` do adaptador. A preferência pelo módulo real e a proibição do fallback para `cenarios/tooltips_shrines.py` foram **mantidas** | `relatorio_aceite.py:65` |
| **A5** | LEVE | a doc dizia "73 reconhecidas pelo parser real"; 73 ≠ reconhecidas, e não havia artefato | frase corrigida em `COR-AUT7-correcao.md` (diz agora **o que** mede) + artefato `COR-AUT7-F2-evidencias/dump-do-produto.json` com a lista **completa** e, nesta rodada, **cada total com o seu predicado declarado** | `COR-AUT7-correcao.md` (tabela de verificação), `refutar_cor_aut7f2.py` (bloco A5) |
| **A4** | LEVE | "`\|` dentro de valor ⇒ REPROVADO" só vale **colado** ao valor; com o separador real (`" \| "`) é indetectável | frase qualificada na doc **e** limite declarado no ponto que decide (comentário no aspecto de contrato do dump) | `estilo_atributos.py` (aspecto do dump), `COR-AUT7-correcao.md` (item 7) |
| **A9** | MÉDIA | `COR-AUT7-correcao.md` citava `evidencias/adaptador-aut6.json` e `evidencias/docs-antes.txt` como prova — **nenhum dos dois existia** | as duas provas foram **produzidas e entregues** em `docs/automacao/COR-AUT7-F2-evidencias/` (com `adaptador-aut6.json` = reuso real do AUT-6, 26 critérios; `docs-antes.txt` = sha256 antes/depois dos docs regerados) e a citação da COR-AUT7 foi corrigida | `COR-AUT7-F2-evidencias/` |

## 2. Regressão negativa por achado (defeito plantado reprovando) — CLIs REAIS

Todas as linhas abaixo saem de `refutar_cor_aut7f2.py` (fase 1: A1–A9),
`refutar_cor_aut7f2_entradas.py` (fase 1.5: as ENTRADAS do cache, E1–E5) e
`fechar_cor_aut7f2.py` (fase 2: suítes + docs), com `*.stdout`/`*.stderr` guardados por CLI
(produtor `estilo_atributos.py` → decisor/consolidador `relatorio_aceite.py` + `decisao.py`).

| cenário | esperado | observado | vinculante? | evidência |
|---|---|---|---|---|
| **A3** 6 das 7 superfícies, cadeia de runtime completa | LACUNA nominal | **NAO_EXERCITADO** (`superficies canonicas ausentes: Healthbar`), `superficies_medidas` = 6, sem `Healthbar` | **não** (consolidador: FALHA_AUTOMATICA) | `refutacao-cor-aut7-f2.json#achados.A3` (+ `.estilo.json`/`.aceite.json`) |
| **A3b** as 7 de verdade (controle) | OK | **OK / OK_VINCULANTE** | sim (legítimo) | idem `A3b_controle` |
| **A1** par BF com chave só no lado ligado | REPROVADO | **REPROVADO** (exit 1), com a chave nomeada | não | `achados.A1` |
| **A1b** mesmo par sem a chave extra | não REPROVADO | **NAO_EXERCITADO** (fixture) | não | `achados.A1b_controle` |
| **A2** config legítimo + identidade **sem** hash de config | LACUNA (não REPROVADO) | **NAO_EXERCITADO** com motivo nomeando o `config_sha` | não | `achados.A2.sem_hash_na_identidade` |
| **A2** identidade que **declara** o hash certo | OK | **OK / OK_VINCULANTE** | sim (legítimo) | `achados.A2.com_hash_na_identidade` |
| **A2** identidade com hash de outra config | REPROVADO | **REPROVADO** | não | `achados.A2.hash_errado` |
| **A6** R1 rodada real (suíte) no sandbox | OK + cache | **OK**, cache gravado, fotografia com **3615 arquivos + 33 artefatos** | sim | `achados.A6.R1` |
| **A6** R2 defeito da regra de ouro plantado **só no pacote** | fotografia muda | zip muda, fotografia **muda**, fonte intacta | — | `achados.A6.R2` |
| **A6** R3 rodada viva de novo | REPROVADO | **REPROVADO**, exit 1 | não | `achados.A6.R3` |
| **A6** R4 `--sem-suite` com o **cache anterior** | não reusar | `cache_valido=false`, **0 OK** de suíte | não | `achados.A6.R4` |
| **A6** R4b cache no **formato anterior** (fotografia sem `artefatos`) | não aceitar | não aceito (é o caminho exato do falso-OK antigo) | não | `achados.A6.R4b_controle` |
| **A6** R5 consolidador com o cache anterior | 0 OK_VINCULANTE | **0 vinculante**, exit 1 | não | `achados.A6.R5` |
| **A6** R6 defeito plantado **só em `bin/Release`** | fotografia muda / não reusar | fotografia muda, `cache_valido=false` | não | `achados.A6.R6` |
| **A6** R7 artefatos restaurados byte a byte | cache volta a valer | `cache_valido=true`, fotografia == R1, **49 OK** de suíte | sim | `achados.A6.R7` |
| **A6/F2 E1** cache real: rodada viva grava, `--sem-suite` reusa | reusar prova | `cache_valido=true`, `bf-diag-orcamento` **OK** (idem o controle negativo) | sim | `achados.A6_entradas.E1` |
| **A6/F2 E2** rodada viva do teste que lê a fixture (linha de base) | PASSA | **PASSOU**, exit 0 | — | `achados.A6_entradas.E2` |
| **A6/F2 E3** **apagar `tools/fixtures/bf-efeito-no-boot.json`** | fotografia muda / não reusar | fotografia **muda** (3615 → 3614: sai **exatamente** o caminho da fixture; artefatos intactos); rodada viva **REPROVOU** (exit 1: "a medicao dos textos COM EFEITO no boot nao esta em tools\fixtures\bf-efeito-no-boot.json"); `--sem-suite`: **`cache_valido=false`**, **0 OK** de suíte, critério do teste **ausente**; consolidador: `AUT-7/BetterFont/suite-ausente` **NAO_EXERCITADO**, **0 OK_VINCULANTE** | não | `achados.A6_entradas.E3_*` |
| **A6/F2 E4** fixture restaurada byte a byte | cache volta a valer | sha igual, fotografia igual à de E1, rodada viva exit 0, `--sem-suite` `cache_valido=true`, e no consolidador o item volta a **OK / OK_VINCULANTE** (BetterFont: 12 vinculantes; rodada: 49) | sim (legítimo) | `achados.A6_entradas.E4` |
| **A6/F2 E5** cobertura **auditada** (gancho `sys.addaudithook` na rodada viva) | nenhuma leitura fora da cobertura | **376** arquivos lidos sob o repo; **324** entradas cobertas pelas raízes/padrões/artefatos declarados; **0 não cobertos**; 52 leituras de **derivados** (`__pycache__`) | — | `achados.A6_entradas.E5` |
| **A7** X5a evidência inexistente | inadmissível | lacuna `AUT-6/resultado-malformado`, 0 item | não | `achados.A7.X5a…` |
| **A7** X5b rótulo OK + arquivo qualquer (sem identidade própria) | não OK | **NAO_EXERCITADO / FALHA_AUTOMATICA** + `AUT-6/item-nao-vinculado` | **não** | `achados.A7.X5b…` |
| **A7** X5c identidade divergente no item | não OK | rebaixado | **não** | `achados.A7.X5c…` |
| **A7** X5d/X5e sem evidência / sha divergente | inadmissível | malformado | não | `achados.A7.X5d…`, `X5e…` |
| **A7** X5f resultado de outra rodada | rebaixar | rebaixado + `identidade-divergente` + `item-nao-vinculado` | **não** | `achados.A7.X5f…` |
| **A7** controle: item com identidade própria conferida | OK | **OK / OK_VINCULANTE** | sim (legítimo) | `achados.A7.controle…` |
| **A8** frente real do AUT-6 na árvore entregue | carrega | **carrega**, 26 critérios, sem `avaliador-indisponivel`, sem `tooltips_shrines` | — | `COR-AUT7-F2-evidencias/adaptador-aut6.json` |
| **A5** o número do dump | medida com artefato **e** predicado declarado | **68** com `' \| '` + **5** com `desc=` (todos sem `' \| '`) = **73** na união; **0** com `'" \| "'` literal; **0** reconhecidas pelo `LINE` | — | `COR-AUT7-F2-evidencias/dump-do-produto.json` |
| **A4** `\|` colado vs separador real | limite declarado | colado ⇒ REPROVADO; com `" \| "` a linha passa (limite documentado) | — | `COR-AUT7R-resultados.json` + comentário no aspecto do dump |

**Falso-OK vinculante (A6/A3):** o `bct-regra-de-ouro` do pacote mutado **e** o
`bf-diag-orcamento` com a fixture apagada deixam de poder ser "OK vinculante com prova velha":
a rodada viva reprova (R3 / E3), o `--sem-suite` não reusa nada (R4/R6 / E3) e o consolidador não
emite nenhum OK_VINCULANTE para o item (R5 / E3). No A3, as 6 leituras passam a ser LACUNA
nominal e o consolidador classifica FALHA_AUTOMATICA (antes: OK_VINCULANTE).

## 3. Suítes, docs e hashes

| prova | resultado |
|---|---|
| suíte da ferramenta de estilo | **28/28, exit 0** (era 26/26; +2 casos: cobertura das ENTRADAS e a regressão ponta a ponta com a fixture apagada) |
| suíte do relatório de aceite | **15/15, exit 0** (inalterada nesta rodada) |
| fase 1 (A1–A9) | `refutacao-cor-aut7-f2.json#achados`: A1/A1b/A2/A3/A3b/A4/A5/A6/A7/A8 |
| fase 1.5 (ENTRADAS do cache) | `achados.A6_entradas` (`fechou = true`) + `COR-AUT7-F2-evidencias/entradas-medidas.json` |
| docs gerados regerados pela CLI real | `AUT-7-relatorio.md`: `3c53c2c22620…` → **`2ca2bb08c2c9…`**; `AUT-7-resultado.json`: `eb1a40e6bc02…` → **`a8a2f55250b7…`**. O doc **não é estável** enquanto a árvore tem escritores concorrentes: cada regeração mede o disco do momento (a suíte puros do momento entra no texto) |

Hashes das fontes e dos docs (medidos no fechamento — repetidos em
`COR-AUT7-F2-evidencias/refutacao-cor-aut7-f2.json#hashes`, em `docs-antes.txt` e em
`COR-AUT7-F2-evidencias/hashes-finais.json`):

| arquivo | sha256 |
|---|---|
| `tools/automacao/estilo/estilo_atributos.py` | `49cd80b641bff189f822ca28d89a6c9f659ccf845092a47f468ee82c518cc975` |
| `tools/automacao/estilo/test_estilo_atributos.py` | `67db3f44a99439b3ddb4417da7c7acd72eb59a3c687504dcacb1feb4d3c8bf4b` |
| `tools/automacao/estilo/refutar_cor_aut7f2.py` | `8284b169f2ee0e20b9706372d0fafc93c77e1175e088fbc59d0c34368827d0a9` |
| `tools/automacao/estilo/refutar_cor_aut7f2_entradas.py` (novo) | `c4cc4d983388f4b2505f27b12ce1f0fc52857d68a3ec0df77f0b2927d726493d` |
| `tools/automacao/estilo/fechar_cor_aut7f2.py` | `a43cad62b3f6352f6d5b258040211da9d1a473c811c57eb6cfb2c69f4f44dcc0` |
| `tools/automacao/aceite/relatorio_aceite.py` | `0ea9c942ffc5f7b2ff8f36e49313e1cb133aa1f2e45cf9a26e79b7136e6b01b1` |
| `tools/automacao/aceite/test_relatorio_aceite.py` | `1d253c3820923600ef4ead6df71862a8f80677d8698189c77bb47208e1b38b3b` |
| `docs/automacao/AUT-7-relatorio.md` (regerado) | `2ca2bb08c2c9551db3bff44de1e1e4d9f05e0fe2e79d9c8092789de220173e7b` |
| `docs/automacao/AUT-7-resultado.json` (regerado) | `a8a2f55250b7bc0afcd360493cb4940948be0edaa3566540fd9c226898e47d7c` |
| `docs/automacao/COR-AUT7-F2-evidencias/entradas-medidas.json` | `758f177bb51e94e4de6dde009cb647f36d21ec950d30ea6f5d07aa04089f652e` |
| `docs/automacao/COR-AUT7-F2-evidencias/dump-do-produto.json` | `b88e5d21c0f476e16952c66fd842dbcf43db81a11b94ad3786311c16d3272448` |
| `docs/automacao/COR-AUT7-F2-evidencias/adaptador-aut6.json` | `50ec696f9afc550637c948d089c32cb5b0dc3618ea026922f3b7de84b8a7864e` |
| `docs/automacao/COR-AUT7-F2-evidencias/docs-antes.txt` | `9c87b14454829fad4b0ea7d5d913b0aa8bd3b95448fcd759049e24728ea4c52d` |
| `tools/automacao/aut6/cobertura.py` (reusado, não editado) | `e33fb037ab0303e33765331ba5cd06194bb4e1343d534fcbcab9726290ea8c0d` |

## 4. Ambiente, escopo e restauração

- **Produto intocado**: os 78 arquivos de fonte/asset dos 6 mods seguem presentes byte a byte, e
  os **25** artefatos de build registrados na rodada anterior (`hashes-finais.json`) continuam
  **idênticos** (conferido item a item por sha256, 0 divergência). Nesta rodada a fotografia
  passou a medir **33** artefatos (entram os `bin/Debug` e os mods
  `BetterTooltips`/`RoguelikeSkillTreeVisualizer`): os artefatos novos são medição **adicionada**,
  não divergência.
- A mutação de artefato (R1–R7) e a retirada da fixture (E1–E5) rodaram **só** numa cópia do repo
  (`<TMP>/cor-aut7f2-sandbox`), restaurável byte a byte e conferida por sha256. O `dist/` e o
  `bin/` do repo vivo nunca foram escritos; `docs/automacao/` recebeu apenas os docs/evidências
  desta correção.
- `tools/automacao/**` e `docs/automacao/**` **não são versionados** neste repo (aparecem como
  `??` no `git status`); as entradas `M` do `git status` são de **escritores concorrentes** em
  produto/testes, não desta execução.
- Se a cópia do sandbox (`COR_F2_SANDBOX`) for de uma execução anterior, as fases **recopiam**
  automaticamente: evidência de outro binário seria a mesma classe de falso-OK que este cartão
  conserta.
- Nada de jogo/save/build/deploy/publicação. Nenhuma tarefa de mod fechada, DoD intocado.

## 5. O que esta correção NÃO prova (e limites que ficam declarados)

- **Runtime segue NÃO EXERCITADO**: nenhum número de atributo, bbox, censo real, contraste real
  ou leitura de objeto vivo; `aceite_humano = NAO_PRONUNCIADO`, `publicacao = NAO_VERIFICADO`,
  `consolidacao_final = false`. Nada aqui é prova de jogo.
- **A6/F2 — o que a fotografia cobre agora**: os **6 mods**, `tools/**`, `lib/**`,
  `docs/cobertura/**`, `ReloadProbe/**` (projeto de bancada, fora do repositório, não versionado), `scratch/**`, `docs/PLANO-DE-TESTES.md`, os projetos
  `*.csproj`/`*.props`/`*.targets` da árvore e os artefatos medidos (`dist/*.zip`,
  `<Mod>/bin/**/*.dll`). **Fica fora de propósito**: `bin`/`obj`/`__pycache__` (DERIVADOS — cobrir
  o bytecode faria a própria rodada invalidar a fotografia), `docs/automacao/**` (SAÍDA da
  ferramenta, senão o cache se invalidaria a cada relatório regerado), `release/` e `NuGet/`
  (build/publicação). A cobertura está declarada **no resultado** (`medicao.fotografia`) e foi
  auditada por medição, não por afirmação.
- **A6/F2 — custo assumido**: a fotografia agora é sensível a **qualquer** escrita numa entrada
  coberta. Num repo com escritores concorrentes (o caso desta árvore), o `--sem-suite` quase
  sempre manda rerodar a suíte em vez de reusar prova velha — é o lado fail-closed, e é o
  desejado. Consequência declarada: apontar `--out-dir` para **dentro** de uma raiz coberta
  (ex.: `tools/**`) provoca drift e a ferramenta recusa a prova.
- **A6/F2 — o que a auditoria não cobre**: o gancho registra as leituras de **um** par de
  execuções da suíte nesta árvore; um teste novo que passe a ler um diretório **não** coberto não
  é visto por ela. O que fica garantido é o conjunto declarado de raízes — se a suíte passar a ler
  outra raiz, ela tem de entrar em `RAIZES_DA_FOTOGRAFIA`.
- **Suíte de estilo — flake de ambiente (não é defeito da entrega)**: o caso "medicao offline
  REAL" roda a suíte viva (~100 s); se um escritor concorrente mexer num caminho coberto durante
  a rodada, a guarda de drift (correta) descarta a saída e o caso reprova. Nesta rodada ele ganhou
  **uma repetição** com aviso explícito antes de reprovar; o que o caso exige continua o mesmo
  (suíte verde).
- **A7 — limite que fica**: a evidência de item de frente passa a ter existência + sha conferidos
  e identidade não-emprestada, mas o adaptador **não pode saber** se um arquivo existente é de
  fato a MEDIÇÃO daquele item (isso é a cadeia de prova da própria frente).
- **A4 — limite que fica**: com o separador real (`" | "`), `|` dentro de um valor continua
  indetectável pelo contrato do censo (o `FIELD` trunca em silêncio) — declarado na doc e no
  código; fechar exigiria mudar o contrato do dump no produto (`tools/testes/**`, fora do escopo).
- `checa_citacoes`/`checa_shrines` e travas de C#/build: fora do escopo desta correção; não
  exercitados aqui (nem aprovados por omissão).
- O conserto **exige nova revisão independente** (execução distinta) antes de fechar.

## 6. Como reproduzir

    python tools/automacao/estilo/test_estilo_atributos.py            # 28/28
    python tools/automacao/aceite/test_relatorio_aceite.py            # 15/15
    python tools/automacao/estilo/refutar_cor_aut7f2.py               # fase 1: A1-A9 (CLIs reais)
    python tools/automacao/estilo/refutar_cor_aut7f2_entradas.py      # fase 1.5: ENTRADAS do cache
    python tools/automacao/estilo/fechar_cor_aut7f2.py                # fase 2: suítes + docs regerados
    # evidência: docs/automacao/COR-AUT7-F2-evidencias/
    #   refutacao-cor-aut7-f2.json · entradas-medidas.json · adaptador-aut6.json · docs-antes.txt
    #   · dump-do-produto.json · hashes-finais.json · *.stdout/*.stderr de cada CLI

As três fases existem porque uma execução única passa de 8 minutos e o host Windows derruba o
spawn de processos novos (`0xC0000142`); cada fase roda sozinha e escreve na MESMA evidência
(a 1.5 e a 2 completam o mesmo `refutacao-cor-aut7-f2.json`; reexecutar a fase 1 **não** apaga o
que elas gravaram).

> AUSENTE / NÃO EXERCITADO / INDETERMINADO nunca são OK. Automação não substitui aceite humano
> nem publicação.
