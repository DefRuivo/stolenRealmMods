# LEVEL-R3F1 — relatório 01: escopo, fontes lidas e baseline

Cartão: `t_021bdd67` (LEVEL-R3F1, correção da reprovação R3-01). Worktree:
`C:/dev/stolen-realm/.worktrees/level-r2` (branch `wt/t_918314e9`, commit de partida `cd8e4ce`).
Modelo desta rodada: `deepseek-flash` / provider `deepseek`.
Deploy: **nunca** (`-p:DeployToBepInEx=false`); o jogo **não** é aberto; save/perfil do dono **não**
são tocados; `Assembly-CSharp.dll` e assets **não** são modificados.

Este arquivo é **novo** (não sobrescreve nenhum relatório anterior).

## 1. O que foi lido do upstream

- Revisão que reprovou (parent `t_cda5afa8`), workspace
  `C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_cda5afa8`:
  - `R3-parte01.md` (escopo, re-derivação de hashes, bancada do revisor);
  - `R3-parte02-08.md` (auditoria, contra-provas, parecer);
  - `R3-findings.json` (4 achados: R3-01 ALTO, R3-02 MEDIO, R3-03/R3-04 BAIXO).
- `R3-01` é o achado que este cartão corrige. Os outros três (R3-02 constante numérica,
  R3-03 documentação dos 39 leitores, R3-04 guarda de item nulo sem teste) **não** são
  resolvidos aqui: não são defeito funcional de perda de dado e o cartão manda manter o
  restante intocado.

## 2. Defeito a corrigir (R3-01)

Em `Character.Load(int saveIndex)` (corpus.cs:36462; IL real `IL_0883..IL_089a`, ver relatório 02):

```
ExperienceLevel = Mathf.Min(MaxLevel, CharacterSaveFile.ExperienceLevel);   // clamp de carga
```

`MaxLevel` é a **propriedade** `Character.MaxLevel` — exatamente o getter que o mod patcheia com
Postfix (`MaxLevelPatches.Postfix` → `Policy.EffectiveMaxLevel`). No instante do clamp
`ExperienceLevel` ainda não foi atribuído, então `Character.Level`
(`Mathf.FloorToInt(Mathf.Max(ExperienceLevel, 1f))`) é ~1 e a proteção
`bound > current ? bound : current` do getter **não** protege o nível salvo. Consequências:

1. `Progression.MaxLevel = N` (≥ 21) com save acima de `N` → `Mathf.Min(N, salvo) = N` → nível
   rebaixado ao carregar;
2. caminho de fallback do getter (rede indisponível → `GameState.IsMultiplayer()==true`
   fail-closed; grupo não aplicado; `EnsureReady()` falho) devolvia o teto vanilla **30** →
   `Mathf.Min(30, salvo)` trunca saves acima de 30.

O valor clampado é persistido (`CharacterSaveFile.ExperienceLevel = ExperienceLevel`,
corpus.cs:36131), ou seja: perda silenciosa e durável. Fere parte05/B ("reduzir teto voluntário
preserva nível salvo") e o alerta do cartão LEVEL-R3 ("não deixar teto20 virar teto30").

## 3. Baseline técnico

- `dotnet --version` = **6.0.428** (único SDK). Harness mira net6.0.
- DLL de referência `C:/dev/stolen-realm/lib/Assembly-CSharp.dll`, sha256
  `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` — **CONFERE** (o harness
  reprova sozinho com outra DLL).
- Harness de partida (worktree, commit `cd8e4ce`): `RESUMO: PASS=91 FAIL=0 NAO_EXERCITADO=14`,
  exit 0 — reproduzido nesta rodada antes de qualquer mudança.

## 4. Plano (ordem do cartão)

1. Escolher a correção **por medição** entre as opções (a)/(b)/(c) do cartão e justificar.
2. Cobrir o caminho de fallback (não usar o 30 vanilla como teto de carga quando o save é maior).
3. Garantir que `GiveExperience` continua sem rebater abaixo do nível atual.
4. Provar com teste **real que pode falhar**: ancorar na IL real de `Character.Load(int)`,
   reproduzir o clamp com o par (MaxLevel efetivo, nível salvo) e incluir contra-prova
   replantando o defeito (reverter → suíte vermelha).
5. Relatórios numerados **novos**, README/CHANGELOG (v0.1.1), hashes e pacote de revisão
   regenerado (sem DLL de jogo / corpus).

## 5. Regras de operação deste run

- Não sobrescrever relatórios: cada arquivo novo é numerado (`LEVEL-R3F1-relatorio-NN.md`).
- Não usar `execute_code` headless; execução via terminal + harness real.
- Nenhum PASS fabricado: o que não é exercitável permanece `NAO_EXERCITADO` com motivo.
- Manter intocadas as demais decisões de LEVEL-R2 (GUID, escopo, `RewardQueryLevel=20`, um nível
  por vitória, nada de Bard, campanha/IA intactos).
