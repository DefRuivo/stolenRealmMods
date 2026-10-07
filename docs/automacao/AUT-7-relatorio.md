# AUT-7 — relatorio de aceite por mod (provisorio)

> Gerado por `tools/automacao/aceite/relatorio_aceite.py` (offline). Status TECNICO, ACEITE HUMANO e PUBLICACAO sao estados SEPARADOS. Nenhum "carregado" aqui vira "eficaz".

## Status tecnico (automacao)

| criterios | OK vinculantes | falhas automaticas | pendencias humanas | nao contam como prova |
|---|---|---|---|---|
| 118 | 49 | 65 | 4 | 0 |

- **pronto_para_decisao**: False — NAO: 65 falha(s) automatica(s) volta(m) ao ciclo; nada disso vai ao dono
- **consolidacao final**: NAO (PROVISORIA) — revisao(oes) pendente(s)/nao-OK: AUT-3R, AUT-5R, AUT-6R
- **aceite humano**: NAO_PRONUNCIADO (estado separado)
- **publicacao**: NAO_VERIFICADO (estado separado; online NAO e consultado aqui)
- **ATENCAO AUT-3**: o resultado de `2026-10-05 15:47:35` NAO corresponde aos bytes atuais — snapshot do AUT-3 diverge dos bytes atuais: 4 alterado(s), 0 removido(s), 771 criado(s) (snapshot=78, atual=849); resultado NAO prova a fonte atual, nova rodada necessaria. **Todos** os criterios do AUT-3 saem `NAO_EXERCITADO` ate uma nova rodada da bancada sobre a arvore atual (falha AUTOMATIZAVEL: nova rodada, nao tarefa do dono).

## BetterTooltips — estado tecnico: `NAO_EXERCITADO`

### Provas (0)
- nenhuma

### Regressao / falha automatica (17)
- `build_BetterTooltips` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterTooltips` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_dupes` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_chave_compartilhada` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_notas_redundantes` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_fix_keys` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M4` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:S-RV-26` — tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-27` — tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-28` — tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-29` — aura viva x fora da aura — leitura em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-30` — aura de perigo com Source=null — medicao em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-31` — agregado por atributo — leitura em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-33` — flame/decay por alvo — leitura em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-34` — defeito do proprio mod superado por RV-30 — revalidacao em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:BUG34` — aceite humano ja dado (KANBAN l.506); regressao de feed exige jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `AUT-6/nao-exercitado` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)

### Lacunas (17)
- `build_BetterTooltips` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterTooltips` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_dupes` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_chave_compartilhada` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_notas_redundantes` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `check_fix_keys` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M4` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:S-RV-26` [NAO_EXERCITADO] — tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-27` [NAO_EXERCITADO] — tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-28` [NAO_EXERCITADO] — tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-29` [NAO_EXERCITADO] — aura viva x fora da aura — leitura em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-30` [NAO_EXERCITADO] — aura de perigo com Source=null — medicao em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-31` [NAO_EXERCITADO] — agregado por atributo — leitura em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-33` [NAO_EXERCITADO] — flame/decay por alvo — leitura em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:S-RV-34` [NAO_EXERCITADO] — defeito do proprio mod superado por RV-30 — revalidacao em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:BUG34` [NAO_EXERCITADO] — aceite humano ja dado (KANBAN l.506); regressao de feed exige jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `AUT-6/nao-exercitado` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)

### Roteiro humano minimo
- nada: nenhuma pendencia humana deste mod.

## BetterFont — estado tecnico: `REPROVADO`

### Provas (12)
- `AUT-7/BetterFont/puro/bf-decisao-texto` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-defaults` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-diag-orcamento` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-falha-segura` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-gate-material` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-nao-regride` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-preservacao` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-sem-acoplamento` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/puro/bf-sombra-inerte` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterFont/controle-negativo/contra-prova-bf-diag-orcamento` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterFont/controle-negativo/contra-prova-bf-gate-shader` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterFont/controle-negativo/contra-prova-bf-sombra-por-alfa` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`

### Regressao / falha automatica (5)
- `build_BetterFont` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterFont` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M2` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterFont/runtime-preservacao-estilo` — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')
- `AUT-7/BetterFont/runtime-config` — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')

### Lacunas (6)
- `build_BetterFont` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterFont` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M2` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterFont/runtime-preservacao-estilo` [NAO_EXERCITADO] — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')
- `AUT-7/BetterFont/runtime-config` [NAO_EXERCITADO] — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')
- `AUT-7/BetterFont/runtime-visual` [NAO_EXERCITADO] — o DoD exige revisao de UI/UX para alteracao de fonte: o dado tecnico nao substitui o olho no jogo

### Roteiro humano minimo
- **[JULGAR visual/UX]** criterios: AUT-7/BetterFont/runtime-visual
  - Abrir o jogo com o BetterFont ativo e conferir, em tooltip, texto de combate e UI, se a fonte ficou legivel e sem corte; registrar o aceite.

## BetterCombatText — estado tecnico: `REPROVADO`

### Provas (27)
- `AUT-7/BetterCombatText/puro/bct-aplicador` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-caminho-legado` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-defaults` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-desligar-inerte` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-diagnostico` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-idempotencia` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-precondicao-shader` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-regra-de-ouro` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-sem-acoplamento` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-sem-vazamento-no-levelup` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-sombra-adaptativa` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-sombra-contraste-letra` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-sombra-polaridade-fonte` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/puro/bct-sombra-visivel-fundo-escuro` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-composicao-idem` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-composicao-ordem` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-composicao-ok` — estado no runner=PASSOU | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-guard` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-guard-ok` — estado no runner=PASSOU | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-substituicao` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-substituicao-ok` — estado no runner=PASSOU | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-texto-ausente` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-texto-ausente-ok` — estado no runner=PASSOU | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-token` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-token-ok` — estado no runner=PASSOU | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-uma-entrada` — estado no runner=PROVA_OK | evidencia: `suite-contra-prova.json`
- `AUT-7/BetterCombatText/controle-negativo/contra-prova-bt-uma-entrada-ok` — estado no runner=PASSOU | evidencia: `suite-contra-prova.json`

### Regressao / falha automatica (6)
- `build_BetterCombatText` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterCombatText` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M1` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterCombatText/runtime-superficies-contraste` — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')
- `AUT-7/BetterCombatText/runtime-idempotencia` — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')
- `AUT-7/BetterCombatText/runtime-sem-vazamento-levelup` — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')

### Lacunas (6)
- `build_BetterCombatText` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterCombatText` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M1` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterCombatText/runtime-superficies-contraste` [NAO_EXERCITADO] — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')
- `AUT-7/BetterCombatText/runtime-idempotencia` [NAO_EXERCITADO] — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')
- `AUT-7/BetterCombatText/runtime-sem-vazamento-levelup` [NAO_EXERCITADO] — criterio incoerente: classe runtime exige procedencia runtime (veio 'execucao')

### Roteiro humano minimo
- nada: nenhuma pendencia humana deste mod.

## BetterStats — estado tecnico: `NAO_EXERCITADO`

### Provas (6)
- `AUT-7/BetterStats/estrutural/base-do-savedmap` — estrutura encontrada no fonte | evidencia: `Plugin.cs`
- `AUT-7/BetterStats/estrutural/final-do-motor` — estrutura encontrada no fonte | evidencia: `Plugin.cs`
- `AUT-7/BetterStats/estrutural/sem-gameplay` — estrutura encontrada no fonte | evidencia: `Plugin.cs`
- `AUT-7/BetterStats/estrutural/geometria-deslocada-uma-vez` — estrutura encontrada no fonte | evidencia: `Plugin.cs`
- `AUT-7/BetterStats/estrutural/falha-segura` — estrutura encontrada no fonte | evidencia: `Plugin.cs`
- `AUT-7/BetterStats/estrutural/formato-base-combinado` — estrutura encontrada no fonte | evidencia: `Plugin.cs`

### Regressao / falha automatica (6)
- `build_BetterStats` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterStats` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M3` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterStats/suite-ausente` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterStats/runtime-base-vs-final` — lacuna tecnica de runtime (probe/campo/coleta/preparacao): automatizavel, volta ao ciclo — NAO e tarefa do dono — valores de atributo do personagem (SavedMap + final) por atributo, para confrontar com
- `AUT-7/BetterStats/runtime-geometria` — lacuna tecnica de runtime (probe/campo/coleta/preparacao): automatizavel, volta ao ciclo — NAO e tarefa do dono — caixa (bbox) do painel de atributos, alem da do texto

### Lacunas (7)
- `build_BetterStats` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_BetterStats` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M3` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterStats/suite-ausente` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/BetterStats/runtime-base-vs-final` [NAO_EXERCITADO] — lacuna tecnica de runtime (probe/campo/coleta/preparacao): automatizavel, volta ao ciclo — NAO e tarefa do dono — valores de atributo do personagem (SavedMap + final) por atributo, para confrontar com o texto medido
- `AUT-7/BetterStats/runtime-geometria` [NAO_EXERCITADO] — lacuna tecnica de runtime (probe/campo/coleta/preparacao): automatizavel, volta ao ciclo — NAO e tarefa do dono — caixa (bbox) do painel de atributos, alem da do texto
- `AUT-7/BetterStats/runtime-visual` [NAO_EXERCITADO] — so a estrutura foi medida offline; numeros/geometria runtime seguem nao comprovados; aceite visual separado

### Roteiro humano minimo
- **[JULGAR visual/UX]** criterios: AUT-7/BetterStats/runtime-visual
  - Com o BetterStats ativo, abrir a ficha de personagem (painel Attributes) e a tela de level-up: conferir que `base (final)` cabe no painel, sem vazar a borda e sem quebra de linha.

## RoguelikeSkillTreeVisualizer — estado tecnico: `NAO_EXERCITADO`

### Provas (0)
- nenhuma

### Regressao / falha automatica (8)
- `build_RoguelikeSkillTreeVisualizer` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_RoguelikeSkillTreeVisualizer` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M6` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:T-RSTV6` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:T-RSTV21` — janela read-only abre/navega/fecha e publicacao — exige jogo/dono (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:T-RSTV25B` — precisa do LogOutput.log do proximo boot (INDETERMINADO) (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:T-RSTV26` — hover com numeros resolvidos — revalidacao visual em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `AUT-5/nao-exercitado` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)

### Lacunas (8)
- `build_RoguelikeSkillTreeVisualizer` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_RoguelikeSkillTreeVisualizer` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M6` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:T-RSTV6` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:T-RSTV21` [NAO_EXERCITADO] — janela read-only abre/navega/fecha e publicacao — exige jogo/dono (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:T-RSTV25B` [NAO_EXERCITADO] — precisa do LogOutput.log do proximo boot (INDETERMINADO) (automatizavel: lacuna tecnica, nao vai ao dono)
- `cobertura:T-RSTV26` [NAO_EXERCITADO] — hover com numeros resolvidos — revalidacao visual em jogo (automatizavel: lacuna tecnica, nao vai ao dono)
- `AUT-5/nao-exercitado` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)

### Roteiro humano minimo
- nada: nenhuma pendencia humana deste mod.

## RoguelikeDebugger — estado tecnico: `NAO_EXERCITADO`

### Provas (4)
- `AUT-7/RoguelikeDebugger/puro/debugger-estabilidade` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/RoguelikeDebugger/puro/debugger-parser-contrato` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/RoguelikeDebugger/puro/debugger-reflexao-cast` — estado no runner=PASSOU | evidencia: `suite-puros.json`
- `AUT-7/RoguelikeDebugger/puro/debugger-saneamento` — estado no runner=PASSOU | evidencia: `suite-puros.json`

### Regressao / falha automatica (4)
- `build_RoguelikeDebugger` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_RoguelikeDebugger` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M5` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/RoguelikeDebugger/controle-negativo-ausente` — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)

### Lacunas (6)
- `build_RoguelikeDebugger` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `fonte_dll_RoguelikeDebugger` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `cobertura:M5` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/RoguelikeDebugger/controle-negativo-ausente` [NAO_EXERCITADO] — criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)
- `AUT-7/RoguelikeDebugger/runtime-contrato-dump` [NAO_EXERCITADO] — rodada runtime ainda nao autorizada: log de sessao anterior NAO prova os bytes atuais (precedente AUT-4R: log velho nao assina fonte nova). O contrato e o saneamento ja tem prova ESTRUTURAL na suite pura (t_debugger_*)
- `AUT-7/RoguelikeDebugger/runtime-censo` [NAO_EXERCITADO] — rodada runtime ainda nao autorizada (mesmo log do boot do criterio de contrato); o `census.py` NAO e executado nesta frente porque reescreve doc curada

### Roteiro humano minimo
- **[AUTORIZAR rodada runtime]** criterios: AUT-7/RoguelikeDebugger/runtime-censo, AUT-7/RoguelikeDebugger/runtime-contrato-dump
  - Autorizar UMA rodada de boot com os mods atuais (SEM carregar save): abrir o jogo ate o menu com o RoguelikeDebugger ativo e encerrar; o LogOutput.log dessa sessao e a evidencia.
  - Autorizar UMA frente runtime (AUT-4/5/6) e reexecutar o ciclo; sem autorizacao nada em jogo e lido.

## Hashes do insumo (medicao desta rodada)

- suite `puros`: `suite-puros.json` (exit do runner=0, sha256=`95d9dd5fe6c3274a`)
- suite `contra_prova`: `suite-contra-prova.json` (exit do runner=0, sha256=`275e6da19ac33c1a`)

> Automacao NAO substitui aceite humano nem publicacao do DoD. AUSENTE/NAO_EXERCITADO/INDETERMINADO nunca sao OK.
