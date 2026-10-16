# KIT-14F4 — entrega (implementação)

Tarefa: `t_5f50371d` (KIT-14F4) · run **1533** · perfil `default` · 15/10/2026
Escopo: corrigir **somente o instrumento/coleta** (consumidor AUT4Probe) e a costura ao avaliador
RSTV existente, em sandbox, com identidade de fonte/DLL/config. Produtor F3 **não** foi reaberto.

## 1. O que foi entregue

1. **Consumidor corrigido** em cópia congelada F2 na sandbox
   `scratch/kit/KIT-14F4-run1525/sandbox/tools/automacao/runtime/AUT4Probe/RstvPostRender.cs`
   (novo sha256 `e3f58b31d8f2792ccb6af563b1bc898e97eaa2aaecac1ef6fc3559fd58ea4d16`).
2. **Patch de integração identificado e NÃO aplicado** no principal:
   `scratch/kit/KIT-14F4-1533/patch-integracao.diff` (479 linhas, contra a fonte base F2
   `RstvPostRender-baseline1525.cs`, sha `048b6a6f69d844542e584fc201e670a54f61838b99b20d40bca60438a2adce4f`).
   `tools/automacao/runtime/AUT4Probe/RstvPostRender.cs` do repositório **não foi tocado**.
3. **Evidência runtime** de boot isolado novo: `scratch/kit/KIT-14F4-1533/on5`, `on6`
   (campanha `recorder-on`, mesmo arnês do KIT14 com isolamento KIT16, frente única, Cloud OFF,
   snapshots IMEDIATOS e restauração — ver `isolamento/` e o readback final de cada boot).
4. **Avaliador canônico alimentado com saída REAL** (`tools/automacao/cenarios/rstv.py`, intacto):
   4 das 7 capacidades **exercitadas** (OK) por dado de runtime, 2 pendências técnicas concretas
   e 1 achado real de geometria (seção 4).
5. Docs novas: `docs/automacao/KIT-14F4-entrega.md` + partes desta rodada
   (`KIT-14F4-1533-parte01.md`, `KIT-14F4-1533-parte02.md`, `KIT-14F4-parte03.md`,
   `KIT-14F4-parte04.md`, `KIT-14F4-parte05.md`). Os antigos `KIT-14F4-parte01.md`/`parte02.md`
   (rodada 1525) foram **preservados sem alteração**.

## 2. Causa-raiz (medida, não deduzida)

O consumidor travava em **TIMEOUT** sem nenhuma amostra. O diagnóstico por guarda
(`rstv_diagnostico` no JSON do probe) mostrou, quadro a quadro:

* `painel_encontrado=true`, `painel_origem="RoguelikeSkillTreeVisualizer.SkillTreesTab._painel"`,
  `painel_ativo=true`, `caminho=GUI Manager/Character Menu Manager Window/RstvAllSkillTreesPanel`;
* `hover_candidatos=30`, `hover_casou="Fireball"` (o hover nativo **era** resolvido);
* `textos_no_painel=0` → travava em "painel vivo sem TMP_Text ATIVO com texto renderizado".

Causa: o host do RSTV rotula a barra de classes com o componente de texto **do próprio jogo**
(`SkillTreeTab.treeName`, tipo `UnityEngine.UI.Text` — confirmado por decompilação de
`lib/Assembly-CSharp.dll`), e os nós da árvore só têm ícone. Ler **somente TMP** devolvia
"render vazio" com a árvore inteira na tela (PNG `on4`/`on5`). Segunda causa da rodada anterior:
teto de espera de 120 s estourava a janela de 120 s do arnês de boot → processo fechado sem prova
(`cases/on3`, sem `rstv_coleta`).

Correção (sem afrouxar critério): leitor de texto nas **duas famílias vivas** (TMP e
`UnityEngine.UI.Text`), painel por objeto vivo com controle próprio (nome de contrato
`RstvAllSkillTreesPanel` quando o estático não está disponível), hover pelo **nome de tipo do
componente vivo**, teto de espera 40 s (abaixo da janela do arnês), gravação incremental do JSON
durante a espera e captura do alvo efetivo quadro a quadro.

## 3. Provas

RED (antes da correção, mesmo detector):

| prova | detector | exit |
|---|---|---|
| `on1-detect.json` (boot run1525, consumidor anterior) | `detect.py` | 1 |
| `red-historical.json` (saída histórica congelada) | `detect.py` | 1 |
| gate full-rstv (`ca3d859a…`) | avaliador canônico | 1 (não enfraquecido) |

GREEN (depois, `on6`): status **CONCLUIDO** em 2,1 s com ciclo nativo completo —
`before_open 451 → open_observed 453 → hover_handler 453 → tooltip_observed 455 →
tooltip_png 461 → close_handler 461 → close_observed 465 → reopen_handler 465 →
reopen_observed 467 → close_handler 467 → close_observed 469`, 32 amostras.

Critérios canônicos com a saída real (`on6-detect.json`):

| capacidade | estado | prova |
|---|---|---|
| RSTV-6-readonly-skills-pontos | **OK** | `snapshot_antes/depois` do MESMO objeto (`identidade_clr` igual), skills `[Fracture,Bash,Charge]`, pontos 0 |
| RSTV-21-janela-ciclo | **OK** | `janela={aberta:true, fechada:true, reaberta:true}` |
| RSTV-21-tooltip-restauracao | **OK** | pai `GUI Manager/Tooltips / Popups` 8→8, índice 8→8, `janelas_duplicadas=0` |
| RSTV-26-placeholders | **OK** | texto RENDERIZADO da tooltip sem `*0`/`[N]`/`@atributo@` |
| RSTV-6-readonly-personagem | NAO_EXERCITADO | `ReadOnlySession.Active/Target` não é legível por reflexão (ver parte05) |
| RSTV-25b-dependencia | NAO_EXERCITADO | o consumidor não emite `dependency_por_tier` (fora do escopo coberto) |
| RSTV-geometria-clipping | REPROVADO | tooltip com x negativo sob hover **sem ponteiro físico** (ver seção 4) |

Owners: `['com.gumatos.roguelikeskilltreevisualizer']` obtidos de patches Harmony **reais**
(`CharacterMenusManager.OpenWindow` → `CharacterMenusManagerOpenWindowPatch`) no componente vivo —
procedência de origem, não herdada do funil de localização.

## 4. Achado real de geometria (não mascarado)

Sob hover **por handler** (sem clique/ponteiro físico, `physical_input=false`), o tooltip do jogo
ancora fora da tela: `Title` x=−333,3 e `Description` x=−419,7 (tela 1920×1080). O dado foi
**mantido e classificado**, não removido nem filtrado. É consequência do caminho não-físico
(a posição da tooltip vem do ponteiro ausente), e o aceite de UIUX/clique físico é campanha
separada (KIT-G4). Registrado aqui para não virar verde por omissão.

## 5. Limites desta entrega

* Não fecha o KIT14: Runner, marcação/export in-game, mod sem kit funcional, performance comparável
  e update/rollback continuam campanha do KIT14.
* Nenhum deploy no perfil Default, nenhuma publicação, `Assembly-CSharp.dll` e RSTV/gameplay/assets
  intactos; nada de Bard.
* Revisão independente: filha `t_821396a1` (pré-criada) — esta entrega conclui **somente a fase de
  implementação**.
* Ressalva de identidade herdada: `inputs.json` preserva `source_set_sha256` agregado F2
  (`cc43e919…`); o conjunto atual com as fontes F3 recalcula `d3c7995b…`. Hashes individuais
  conferidos; guardas devem rejeitar agregado incoerente (detalhe na parte05).
