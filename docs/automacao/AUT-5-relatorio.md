# AUT-5 — Automatizar cenarios do RSTV e prova de somente leitura (`t_76a41ea7`)

> Rodada **OFFLINE**. Nada de jogo: nenhum probe instalado, nenhum jogo iniciado/encerrado,
> nenhum save carregado, nenhum build/deploy no perfil, nenhum commit/push/publicacao.
> Tudo o que foi exercitado sao **bytes em disco** (fonte do mod, DLL, `.cfg` e o
> `LogOutput.log` da sessao do dono) lidos em **somente leitura** e o pipeline que os julga.
> Runtime continua **NAO EXERCITADO** — pela regra da tarefa, instalar/iniciar/carregar save
> exige **autorizacao explicita do dono para a rodada**.

## 1. O que foi entregue (frente exclusiva: `tools/automacao/aut5/`)

| arquivo | sha256 (16) | papel |
|---|---|---|
| `tools/automacao/aut5/log_rstv.py` | `5586ac86330ab729` | leitor somente-leitura do `LogOutput.log` -> observacoes do contrato (marcadores RSTV-21/24a/24b/23i/25/5/16/2 + confronto Dependency x conectores) |
| `tools/automacao/aut5/aut5.py` | `7a82331fcc099b8a` | condutor: identidade (fonte/DLL/config), criterios de instrumentacao, cenario RSTV via avaliador CIC-3, guardas, aceite visual, e a **decisao** CIC-2 |
| `tools/automacao/aut5/cenarios-rstv.json` | `b2dd7e04a134d07b` | plano de cenarios (S1 modal · S2 inventario-independente · S3 level-up · S4 run · S5 tooltip) + dependencia primaria de cada capacidade |
| `tools/automacao/aut5/test_aut5.py` | `61a29656f8e77029` | suite executavel (7 grupos de caso) + `--contra-prova` |
| `tools/automacao/aut5/fixtures/log-completo.log` | `6d83edfd1fbd732e` | fixture de sessao completa (marcadores consistentes) |

Lidos (e **nao editados** — arquivos de outras frentes): `cenarios/rstv.py` `524f719757977436`,
`ciclo/decisao.py` `d6de959e73a090e4` (**mudou durante a rodada**: outro agente escreve nele),
`runtime/coletor.py` `2f502e0d4ca45374`, `cenarios/test_rstv.py` `2dd71104c8b3a81d`.

## 2. Identidade dos bytes (o que foi medido)

| item | sha256 |
|---|---|
| `fonte_sha` (arvore de fonte do RSTV: 14 arquivos `.cs`/`.csproj`, sha de `"relpath\tsha256"` ordenado) | `7774d11fab0017f9d27227ae8700a353203bdfd8d4d4c63a285f74fbab758612` |
| `dll_sha` (build do repo, `bin/Release/netstandard2.1`) | `454587a031a3e89104ec8535cf4c6328e2a527238138a136adcc773c5617a948` |
| DLL **deployada no perfil do dono** (so leitura) | `454587a031a3e89104ec8535cf4c6328e2a527238138a136adcc773c5617a948` (**== repo**) |
| `config_sha` (`com.gumatos.roguelikeskilltreevisualizer.cfg`, so leitura) | `fa506b724f8af93cd071c2a662f3348072007b0ec06f73c056bc1e872f0233cc` |
| `LogOutput.log` da sessao (1.234.333 B, 05/10 14:32, 3.440 linhas) | `8652cd5833a367c0137e4cca076eaeda6f138e32188aa77a54e1b9588aaef85e` |
| versao (fonte `<Version>` == `Plugin.Version` == log) | `0.3.2` |

`fonte_sha` e uma definicao desta frente (documentada aqui porque e o que a identidade do
cenario usa): sha256 sobre as linhas `"<relpath>\t<sha256>"` das fontes do mod, ordenadas —
mudar qualquer byte de qualquer `.cs` invalida a identidade e derruba toda aprovacao anterior.

## 3. Comandos exercitados (saida real)

```
python tools/automacao/aut5/test_aut5.py                 -> RESULTADO|PASSOU|aut5-rstv|7 casos   exit 0
python tools/automacao/aut5/test_aut5.py --contra-prova  -> CONTRA-PROVA|PASSOU|isca 'sempre OK'
                                                            nao passa                                exit 0
python tools/automacao/aut5/aut5.py --texto --out ...    -> 6 OK / 11 NAO_EXERCITADO · decisao:
                                                            falhas_automaticas=5 · pendencias_humanas=2
                                                            exit 2 (incompleto: runtime nao exercitado)
python tools/automacao/aut5/aut5.py --log fixtures/log-completo.log --texto
                                                         -> 6 OK / 4 INDETERMINADO / 7 NAO_EXERCITADO
                                                            (fixture NAO aprova o que exige rodada)
travas do repo com os arquivos novos no lugar:
  check_segredos / check_padroes_segredo / check_dupes / audita_docs   -> exit 0 (nenhuma vermelha)
```

## 4. Veredito por criterio (rodada real, log do dono)

| id | classe | estado | prova / motivo |
|---|---|---|---|
| `AUT5-obs-marcadores-fonte` | offline | **OK** | 9 marcadores exigidos (RSTV-21 aberta/fechada, 24b, 25, 23i, 24a, 5-recusa, 16-ativo, 2-commit) presentes nos 13 `.cs` da fonte |
| `AUT5-guardas-run-fonte` | offline | **OK** | os 7 motivos literais de `RunTargets.GateOk` + catch com lado seguro, em `RunTargets.cs` |
| `AUT5-travas-readonly` | offline | **OK** | `SkillTreeManagerAcceptSkillChangesPatch` + `SkillTreeManagerResetSkillPointsPatch` na fonte **e aplicados** no boot do log |
| `AUT5-boot-rstv` | offline | **OK** | log de boot da **DLL atual** (`454587a0` == repo == perfil), versao 0.3.2, 15 ganchos aplicados |
| `AUT5-geometria-botao-run` | offline | **OK** | `RSTV-5: botao 'Skills' injetado no HUD (24.2x24.2 px) ... largura da linha 88.6 -> 88.6 px` |
| `AUT5-geometria-botao-modal` | offline | **OK** | `44x44 px`, canto superior direito de `Panel`, clone de `Cancel Button` |
| `AUT5-RSTV-25b-conectores-log` | offline(runtime) | NAO_EXERCITADO | a janela nao foi aberta na sessao: nao ha `RSTV-25` nem `RSTV-24b` |
| `AUT5-geometria-arvore-log` | offline(runtime) | NAO_EXERCITADO | sem `RSTV-24a`/`RSTV-23i` (janela nao renderizada) |
| `RSTV-6-readonly-personagem` | runtime | NAO_EXERCITADO | sem leitura de personagem **e sem alvo declarado** — o alvo e do perfil de teste (nunca do proprio log) |
| `RSTV-6-readonly-skills-pontos` | runtime | NAO_EXERCITADO | ninguem emite snapshot antes/depois de skills/pontos |
| `RSTV-21-janela-ciclo` | runtime | NAO_EXERCITADO | sem rodada: os marcadores existem, o ciclo nao foi exercitado |
| `RSTV-21-tooltip-restauracao` | runtime | NAO_EXERCITADO | pai/indice do tooltip nao sao emitidos por ninguem |
| `RSTV-26-placeholders` | runtime | NAO_EXERCITADO | o texto renderizado do hover so existe com o jogo aberto |
| `RSTV-25b-dependencia` | runtime | NAO_EXERCITADO | `RSTV-25` da o Dependency real; faltam as linhas **por tier** |
| `RSTV-geometria-clipping` | runtime | NAO_EXERCITADO | a `geometria` do probe nao traz a dimensao de tela por observacao |
| `AUT5-guards-run-exercicio` | runtime | NAO_EXERCITADO | o log nao diz em que estado do turno o clique ocorreu: recusa lida no log **nao** prova a cena |
| `AUT5-aceite-visual-design` | runtime | NAO_EXERCITADO | DoD item 4: aceite de design exige olho humano sobre PNG (nao ha PNG desta rodada) |

Nenhum `REPROVADO` na rodada real — o produto **nao** foi exercitado; `AUSENTE`,
`NAO_EXERCITADO` e `INDETERMINADO` **nunca** contam como OK (sao 11 dos 17 criterios).

### Como a decisao (CIC-2) roteia isso

```
pronto_para_decisao = False
falhas_automaticas  = 5   (tecnica: probe/coletor POR CAMPO — fila de agente, nao vai ao dono)
pendencias_humanas  = 2   (1 autorizacao da rodada + 1 julgamento visual)
```

* **fila de agente (5):** `RSTV-6-readonly-skills-pontos` (snapshot antes/depois),
  `RSTV-21-tooltip-restauracao` (pai/indice + duplicatas), `RSTV-25b-dependencia` (linhas por
  tier), `RSTV-geometria-clipping` (`geometria.tela`), `AUT5-RSTV-25b-conectores-log`
  (contagem de linhas POR TIER no `RSTV-24b` do mod).
* **roteiro humano (curto, agregado):** autorizar **UMA** rodada (fecha
  `RSTV-21-janela-ciclo`, `RSTV-26-placeholders`, `RSTV-6-readonly-personagem`,
  `AUT5-geometria-arvore-log`, `AUT5-guards-run-exercicio`) + anexar PNG por cena
  (aceite de design).

## 5. Controles negativos (o que a automacao sabe reprovar)

Defeito plantado -> REPROVADO **com a decisao roteando como falha automatica** (todos na suite):

| # | defeito plantado | criterio que reprova |
|---|---|---|
| 1 | log com versao `0.3.1` | `AUT5-boot-rstv` (log de OUTRA build nao vale) |
| 2 | gancho `SkillTreeManagerAcceptSkillChangesPatch` removido do log | `AUT5-travas-readonly` (risco de escrita no personagem) |
| 3 | `RSTV-24b: 0 linha(s) ...` com 4 nos com Dependency | `AUT5-RSTV-25b-conectores-log` (**conector ausente** = sintoma do RSTV-25b) |
| 4 | `RSTV-24b: 6 linha(s)` com 4 nos com Dependency | `AUT5-RSTV-25b-conectores-log` (conector SEM Dependency = aresta inventada) |
| 5 | `T5:3/4` (T5 passa a ter Dependency) | idem (soma > linhas) |
| 6 | `RSTV-23i: ... reduzida por 1x` | `AUT5-geometria-arvore-log` (excede e nao reduz = clipping) |
| 7 | `largura da linha 88.6 -> 120.4 px` | `AUT5-geometria-botao-run` (linha do HUD cresceu) |
| 8 | marcador `RSTV-25:` renomeado **na fonte** (copia) | `AUT5-obs-marcadores-fonte` |
| 9 | motivo da guarda "nao e o turno do jogador" removido **na fonte** (copia) | `AUT5-guardas-run-fonte` |

Controle de ausencia: log sem leitura do RSTV -> **nenhum** criterio de runtime OK e
`exit != 0`. Controle de rotulo: criterio nao exercitado nunca sai com `prova_runtime=True`;
quem tem classe de prova `runtime` carrega `procedencia_nota` dizendo que **nao** houve rodada
(nao se promove nada a `runtime` por rotulo).

**A suite MOSTRADA reprovando** (regra do projeto): neutralizando a checagem de conector no
produto (`if cons["conector_ausente"]:` -> `if False:`), a suite sai
`RESULTADO|REPROVOU|... defeito 'conector-ausente' nao reprovou` **exit 1**; restaurado
**byte a byte** (sha conferido `7a82331fcc099b8a`), volta a `PASSOU` exit 0.

## 6. RSTV-25b — o que a automacao PODE e NAO PODE afirmar

O `RSTV-25` (fonte `SkillTreesTab.cs:1963`) conta, por tier, quantos nos tem `SkillInfo.Dependency`
— o **Dependency real**. O `RSTV-24b` (l.1938) conta as linhas de dependencia **ativas** (total,
com sprite e cor). Regra aplicada (derivada das duas linhas do codigo, nao inventada): a soma
dos nos com Dependency tem de casar com as linhas ativas — faltando linha, e o proprio sintoma
do RSTV-25b; sobrando, e conector sem Dependency. **T5 sem Dependency e ausencia LEGITIMA**
(nao se inventa aresta).

| o que | veredito |
|---|---|
| confronto no TOTAL (Dependency 4 == linhas 4) | exercitado na fixture -> **INDETERMINADO** (nao aprova: falta o por-tier) |
| confronto POR TIER (linhas por tier) | **NAO EXERCITADO** — o `RSTV-24b` hoje so da o total; precisa de campo/linha por tier (fila de agente) |
| Dependency real na sessao do dono | **ausente do log** (a janela read-only nao foi aberta em 05/10 14:32) — nada foi inferido |

## 7. Guardas de turno/chat/mira (RSTV-6, itens (a)-(g) do dono)

Na **fonte** (offline, OK): `RunTargets.GateOk` recusa por mira de hex (`PingModeActive`),
janela de UI aberta, mira de skill (`HexCellManager.CurrentState=Action`), posicionamento
inicial (`SpawnPlacementActive`), turno do inimigo (`!IsPlayerTurnAndReady`), personagem agindo,
personagem movendo, com `catch` que **nao** abre; o `LevelUpAberto()` suspende so os portoes de
batalha (nao o alvo) e o atalho F10 respeita foco de campo de texto.
Na **execucao**: **NAO EXERCITADO** — o log da sessao nao tem **nenhuma** recusa
(`RSTV-5: abertura RECUSADA`), e ausencia de recusa nao prova nada (o botao pode simplesmente
nao ter sido clicado). A automacao cobra o motivo EXATO de cada cena na rodada autorizada.

## 8. Lacunas declaradas (nunca OK)

> **ATUALIZACAO (AUT5-F1, `t_dd95f8d9`):** itens **2-5** desta secao foram fechados como
> **EMISSAO** (probe/coletor para o snapshot e o tooltip; linha `por tier` no `RSTV-24b` do
> mod). O `geometria.tela` do item 5 ja era emitido pelo probe e foi **conferido**. Depois
> disso, o que resta nos criterios correspondentes **nao e mais campo de probe**: e a rodada
> autorizada (o plano passou esses itens para `pendencia_primaria=autorizacao`). O item 1
> (`personagem_esperado`) segue indefinido de proposito (item do dono). Detalhe, provas e
> controles em `docs/automacao/AUT5-F1-entrega.md`.

> **Adendo apos revisao R1/R2:** o snapshot agora captura o Target da sessao
> read-only, nao o personagem selecionado; marcadores ausentes em arvore exercitada
> geram REPROVADO/tecnica. Provas offline e hashes atuais em
> `docs/automacao/AUT5-F1-reentrega.md`. Emissao nao equivale a leitura em jogo.

1. `personagem_esperado` — o alvo do cenario e do **perfil de teste**; ler o alvo do proprio log
   seria comparar o dado consigo mesmo. Falta o dono declarar o nome.
2. `skills_antes/depois`, `pontos_antes/depois` — nenhum instrumento emite (guarda de leitura
   somente pelo snapshot antes/depois).
3. `tooltip_pai_antes/depois`, `tooltip_indice_antes/depois`, `janelas_duplicadas` — idem.
4. `linhas_dependencia` **por tier** — o `RSTV-24b` so publica o total.
5. `geometria.tela` por observacao (probe AUT-4) — sem viewport nao ha contexto de clipping.
6. `sessao` de rodada + PNG por cena — so existem na rodada autorizada.
7. `@x@` no texto **cru** pode ser negrito legitimo do motor: nao se afirma nada sem o
   renderizado (pendencia herdada da CIC-3R, mantida aberta).

## 9. Pedido ao dono (autorizacao minima, uma unica frente)

> **Autorizar UMA rodada** com o perfil/probe que a frente runtime usa (perfil isolado de
> preferencia; **nao** carregar save de producao automaticamente), **sem combate**, e:
> 1. dizer o **nome do personagem** esperado em cada cena (Party Select, level-up, run) —
>    e o `personagem_esperado` do cenario;
> 2. abrir a janela read-only (modal **e** run) e fechar com **X** e com **Esc**;
> 3. clicar o botao 'Skills' da run em cada cena de risco: turno de inimigo, mira de hex,
>    mira de skill, janela de UI aberta, personagem agindo/movendo, posicionamento inicial;
> 4. abrir duas vezes (anti-duplicacao) e passar o mouse por 2 skills de dano + 1 passiva;
> 5. deixar o log fechar a sessao e **anexar PNG** por cena (janela aberta/fechada, hover por
>    objeto, arvore inteira) para o aceite de design.
>
> O probe e **novo**: exige instalar e **iniciar** o jogo — nao existe recarga a quente, e o
> hot-reload nao esta prometido. A automacao reexecuta sozinha depois e cobra cada item.

## 10. Limites desta rodada (o que NAO foi provado)

* **Runtime NAO EXERCITADO**: nenhuma leitura de objeto em sessao viva, nenhum PNG, nenhum
  snapshot de skills/pontos, nenhuma recusa de guarda. Nenhum criterio de runtime foi aprovado.
* **Automacao nao substitui aceite humano nem a publicacao do DoD.** O aceite visual continua
  sendo do dono, em jogo, com os PNGs.
* O log da sessao e de **05/10 14:32** com a DLL **atual** (sha conferido): vale como prova de
  boot/injecao/geometria, **nao** como rodada desta tarefa (nao tem `sessao`).
* `decisao.py` (CIC-2) e `rstv.py` (CIC-3) foram lidos no estado do disco e **mudaram durante a
  rodada** (outras frentes escrevem neles); as falhas do `coletor.py` apontadas pela CIC-5R
  (`S-1`, `R-2` a `R-5`) sao do CIC-5 (`t_431dba37`) e **nao** foram tocadas aqui.
* Nada de produto/probe/perfil/save/commit/publicacao nesta rodada; o unico arquivo novo no
  repo sao os cinco arquivos da secao 1 e este relatorio.

## 11. Pos-rodada: conserto dos achados A-1/A-2/A-3/A-8 (AUT5-F2, `t_9cee7d21`)

A revisao independente **AUT-5R** (`t_a6bb7f27`, `AUT-5R-revisao.md`) e a da AUT5-F1
(`t_dd95f8d9`) abriram achados de robustez que **nao** invalidam o que esta declarado acima,
mas mudam os bytes desta frente. O conserto esta em **`AUT5-F2-relatorio.md`**: o confronto do
motivo das guardas passou a ser normalizado dos dois lados (A-1), a **falha do proprio mod no
log** virou criterio `AUT5-falhas-produto-log` que REPROVA (A-2), a checagem das guardas passou
a exigir o bloco `if (<condicao>) -> motivo -> return false` (A-3), o item `chat/texto` saiu da
contagem de guardas confrontaveis (A-8) e o probe no formato normalizado do coletor passou a
fechar o trio do tooltip (F-1). Os hashes da secao 1 **nao valem mais** para `aut5.py`,
`log_rstv.py`, `cenarios-rstv.json`, `test_aut5.py` e `fixtures/log-completo.log` — os valores
atuais estao na secao 1 do adendo.
