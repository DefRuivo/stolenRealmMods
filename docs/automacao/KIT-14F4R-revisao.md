# KIT-14F4R — revisão independente (runtime/contrato) da coleta pós-render RSTV

Tarefa: `t_821396a1` (filha de `t_5f50371d`) · run **1538** · perfil `default` · 15/10/2026
Revisor: instância nova, autoria independente do implementador (run 1533 / coletor run1524).
Escopo: revisar **somente evidência**, sem tocar produto, sem build, sem deploy, sem publicar, sem
afrouxar gate. Nada foi executado no jogo nesta revisão; nenhum arquivo de produto foi alterado.

**VEREDITO GERAL: NÃO APROVADO para liberar KIT14.** 3 achados que exigem correção, 1 achado de
rastreabilidade, 3 ressalvas. Devolvido pela transição nativa (rework), sem revisão duplicada.
O que o implementador **declarou aberto** continua aberto (não é omissão dele); o que **não** foi
declarado está listado aqui como achado.

## 0. Fontes efetivamente lidas (não só o relatório)

| objeto | caminho | sha256 / identificação |
|---|---|---|
| consumidor F4 (corrigido) | `scratch/kit/KIT-14F4-run1525/sandbox/.../AUT4Probe/RstvPostRender.cs` | `e3f58b31…a4d16` |
| "fonte base F2" do patch | `scratch/kit/KIT-14F4-1533/RstvPostRender-baseline1525.cs` | `048b6a6f…ce4f` |
| patch de integração | `scratch/kit/KIT-14F4-1533/patch-integracao.diff` | 479 linhas, **1 arquivo** |
| saída real do boot (on6) | `scratch/kit/KIT-14F4-1533/on6/recorder-on/boot01/probe/aut4probe.json` | `5e5ad017…2139` |
| saída real do boot (on5) | `scratch/kit/KIT-14F4-1533/on5/recorder-on/boot01/probe/aut4probe.json` | `82ca6ca8…978d` |
| detector do importador | `scratch/kit/KIT-14F4-1533/detect.py` | importa o avaliador canônico |
| avaliador canônico | `tools/automacao/cenarios/rstv.py` | `f8d0aad1…cab7`; blob git `02095c4f…` = HEAD |
| DLL do boot | `installed_dll_sha256` em `boot01/result.json` | `c5fadede…6040` |
| DLL RSTV do boot | `input_identity.files.RoguelikeSkillTreeVisualizer.dll` | `1d0b85e8…d5cc` |
| DLL RSTV congelada F2 (medi na origem) | `…/workspaces/t_ace7f7f2/final/inputs/RoguelikeSkillTreeVisualizer.dll` | `1d0b85e8…d5cc` (**igual**) |
| `Assembly-CSharp.dll` do sandbox vs repo | `scratch/kit/KIT-14F4-1533/sandbox-final/lib/…` e `lib/…` | `8bb4a7c5…855a` (**iguais**) |
| plugin do produto (hotspot) | `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `beaf965a…c193`; `git status` limpo |

Metadados do predecessor **conferidos item a item** e batendo: `source_sha256`=`e3f58b31…`,
`source_base_sha256`=`048b6a6f…`, `guard_red_exit=1`, `guard_green_exit=0` (é o controle do
`tools/check_deploy_optin.py`, **não** o detector RSTV), `detect_exit=1`, `physical_click=false`,
`published=false`, `product_modified=false`, `human_acceptance=false`.

## 1. Veredito por requisito

### R1. Objeto atual é o alvo REAL `RstvAllSkillTreesPanel` — **OK**
`rstv_coleta.counts` (4 estágios: quadros 484/494/496/498) todas com `host=RstvAllSkillTreesPanel`,
`all_scene_instances=1`, `active_instances` 1→0→1→0. Eventos com caminho real
`GUI Manager/Character Menu Manager Window/RstvAllSkillTreesPanel…` e
`…/RstvTreeArea/RstvNodeContainer/RstvItem_Fire_T2_1` (hover). Diagnóstico:
`painel_encontrado=true`, `painel_origem="…SkillTreesTab._painel (campo estatico do produto, objeto vivo)"`
— o fallback por nome de contrato **não** foi usado no verde. "Aba ativa" não sustenta nada aqui: o
objeto é medido por instância de cena em 4 quadros distintos.

### R2. Seleção/identidade e "snapshots no personagem correto" — **ACHADO**
- Par antes/depois: `personagem="Cree"`, `skills=[Fracture,Bash,Charge]`, `pontos=0`,
  `identidade_clr=466192896`, quadros 482/498, `fonte` = `Character.SkillsFromPoints` /
  `Character.UnspentSkillPoints`, `selecao_fonte="GameLogic.instance.CurrentlySelectedCharacter
  before final handler"` → o par **está** pinado no personagem do modal (não na seleção global).
- Mas a identidade **por observação** não existe: em 32/32 amostras
  `personagem={personagem:null, identidade_clr:null, frame_observado:null}` e
  `mesma_referencia_alvo=false`; o próprio consumidor publica `same_character_reference=false`.
- Avaliador canônico (não modificado): `RSTV-6-readonly-personagem = NAO_EXERCITADO`,
  `prova_runtime=false`, motivo "personagem observado AUSENTE (nada selecionado?)" ×32.
- Consequência medida: `detect.py` → `exit 1`, falhas `["same_character_reference",
  "RSTV-6-readonly-personagem"]`. **Não existe execução verde (exit 0) deste detector em nenhuma
  evidência da rodada** — os 6 `*-detect.json` (on1/on5/on6 em run1525 e 1533) todos `exit 1`.
- Valores são honestos (campo ausente **não** virou OK; nada foi fabricado). Ainda assim o requisito
  nomeado "personagem correto / não o personagem errado" segue **não medido**, e é o item T1 que o
  próprio implementador roteou.

### R3. Leitura posterior ao render (quadros estritos) — **OK** (com achado de rastreabilidade)
`before_open 482 < open_observed 484 = hover_handler 484 < tooltip_observed 486`;
`tooltip_png_requested 486 < tooltip_png_completed 492`; `close_handler 492 < close_observed 494`;
`reopen_handler 494 < reopen_observed 496`; `close_handler 496 < close_observed 498`.
Textos renderizados: 15 amostras em `tree_after_open` — 11 rótulos de classe
(`…/RstvClassBar/RstvClassButton_*/Text`, `UnityEngine.UI.Text`) **e 4 nós reais**
(`…/RstvTreeArea/RstvNodeContainer/RstvItem_Fire_T1_5|T2_5|T3_5|T4_4/Upgraded Version Text` = "I"/"II");
tooltip TMP real `Title="Fireball"` e `Description="Hurls a ball of flame dealing 20-27 fire damage…"`;
PNG `03-rstv-tooltip.png` 1.923.336 bytes, `d19e51f4…733f`.

**ACHADO (rastreabilidade):** a entrega §3 e o `metadata` do handoff citam o ciclo verde como
`451 → 453 → 455 → 461 → 465 → 467 → 469` e "2,1 s". Esses quadros são do boot **on5**
(`82ca6ca8…`, `duracao_s=32.199`), não do **on6** citado (`5e5ad017…`, quadros 482–498,
`duracao_s=21.607`). O artefato não sustenta os números como rotulados.

### R4. Ausência de mutação de skills/pontos — **OK (limite declarado)**
Antes/depois idênticos no objeto pinado (`skills_unchanged`, `points_unchanged` verdadeiros no
detector; `identidade_clr` igual). **Ressalva:** `pontos 0→0` é asserção fraca e **não há caso mutante
do par skills/pontos** nesta rodada (nenhum caso com gasto/ponto injetado) — a sensibilidade do leitor
a uma mutação real não foi provada para este consumidor.

### R5. Pai/índice do tooltip e zero duplicado — **OK (medido), ressalva de gate**
Em 32/32 amostras `tooltip_pai_antes == tooltip_pai_depois == "GUI Manager/Tooltips / Popups"`,
`tooltip_indice_antes == depois == 8`, `janelas_duplicadas = 0`, `janela={aberta:true, fechada:true,
reaberta:true}`. **Ressalva:** `janelas_duplicadas` é derivado do contador interno do consumidor
(`max(0, _rstvMaxCount-1)`) e `detect.py` **não tem check independente** para pai/índice/duplicata —
o veredito canônico `RSTV-21-tooltip-restauracao=OK` herda o campo, não o refuta.

### R6. Procedência confiável para o avaliador canônico — **OK**
`owner_provenance`: `owner="com.gumatos.roguelikeskilltreevisualizer"`, `target_method=
"CharacterMenusManager.OpenWindow"`, `patch_method="RoguelikeSkillTreeVisualizer.
CharacterMenusManagerOpenWindowPatch.Postfix"`, `live_component_type="…RstvSkillHover"`,
`live_component_id=-297952`, `live_path=…/RstvItem_Fire_T2_1`, `assembly="RoguelikeSkillTreeVisualizer,
Version=0.3.3.0…"`, `assembly_sha256=1d0b85e8…` (**= DLL congelada F2 que eu medi na origem**),
`same_assembly=true`; `owners` sem o genérico `com.gumatos.aut4probe`. Sem reclassificação de GUID e
sem filtro afrouxado: `tools/automacao/cenarios/rstv.py` é **byte-idêntico ao HEAD** (blob
`02095c4f…`), logo o gate não foi enfraquecido por esta rodada.

### R7. Negativo do MESMO leitor (sem produto / snapshot-render ausentes) — **ACHADO**
Existem negativos parciais: `on1-detect.json` (mesmo detector, consumidor anterior) `exit 1` e
`red-historical.json` `exit 1`. **Falta o negativo exigido com o produto ausente para ESTE leitor:**
`campaign.py` implementa `case=='absent'` (remove `RoguelikeSkillTreeVisualizer.dll`) e
`AUT4ProbePlugin.cs` tem o ramo `ALVO_AUSENTE` (com `detect.py` devolvendo `exit 2`), mas
`grep -rl ALVO_AUSENTE scratch/kit/` encontra **apenas arquivos-fonte, nenhum JSON produzido**;
os casos executados foram `on1,on3,on4,on5,on6` — **nenhum `absent`**. Sem produto, ausência,
timeout e fixture nunca podem aprovar runtime — e o caminho de recusa não foi exercitado nesta rodada.

### R8. Preflight de deploy e build sandbox — **OK**
`build/candidate6/commands.json`: `guard-red` (csproj insegura inerte) `exit 1`; `guard-green`
`sandbox` `exit 0`; build `dotnet build -c Release -p:DeployToBepInEx=false --no-incremental`
`exit 0`. `installed_dll_sha256=c5fadede…` = DLL do candidato → o binário bootado é o construído.
Nenhum deploy: o boot roda em `bepinex-iso` (o próprio `assembly_path` da procedência aponta para
`…/cases/on6/recorder-on/boot01/bepinex-iso/BepInEx/plugins/Kit1442/…`). Nada publicado,
`physical_click=false`, nenhum aceite humano reivindicado.

### R9. Produto intocado / hotspot preservado / patch de integração — **OK no produto, ACHADO no artefato de integração**
OK (verificado por mim):
- `git status --porcelain -- tools/ RoguelikeSkillTreeVisualizer/` limpo (só um não-rastreado alheio
  `tools/preparar_revisao_dono.py`, de 13/10) → `AUT4ProbePlugin.cs`, `PartyDriver.cs`,
  `IdentidadeDoProbe.cs`, `Json.cs`, `LeituraAgregados.cs` e o mod RSTV **sem alteração pendente**.
- `PartyDriver.cs`=`1ce519ba…`, `Json.cs`=`ae30a1ac…`, `IdentidadeDoProbe.cs`=`c23574f3…`,
  `LeituraAgregados.cs`=`f3985436…` — **idênticos aos hashes F2** (ponte/identidade/F3 mantidos).
- Delta do `AUT4ProbePlugin.cs` do sandbox contra a fonte F2 = **18 linhas** de costura RSTV
  (`ConfigurarRstv();`, `if (_rstvCiclo…)/PassoRstv()`, guarda do refresh legado) — o conteúdo
  manual/hotspot (bloco `KIT14G-SEG2-FIX`, `EsperarInteractable`, `ConfigurarClique`) está preservado.
- `lib/Assembly-CSharp.dll` do sandbox == do repo (`8bb4a7c5…`) → nenhum gameplay/assembly tocado.

ACHADO:
- A entrega §1.2 afirma "`tools/automacao/runtime/AUT4Probe/RstvPostRender.cs` do repositório **não foi
  tocado**". Esse caminho **não existe**: 0 ocorrências fora de `scratch/`, e
  `git log --all --diff-filter=A -- *RstvPostRender*` não retorna commit. O instrumento é artefato de
  scratch, e a "fonte base F2" `RstvPostRender-baseline1525.cs` (`048b6a6f…`) é um snapshot criado às
  17:46 **na mesma sessão** — não um artefato F2 pré-existente.
- `patch-integracao.diff` cobre **1 arquivo** e **não** contém `AUT4ProbePlugin.cs` nem `RstvCiclo`
  (0 ocorrências). Aplicado sozinho sobre a fonte F2, ele adiciona a `partial class` com
  `ConfigurarRstv/RstvAntesDeAbrir/PassoRstv`, mas deixa os **call sites** de fora → coletor morto
  (nunca invocado) e base inexistente no produto. O "patch de integração identificado" não é
  auto-suficiente para integrar.

### R10. Ambiente da campanha — **OK**
`immediate_baseline_at_boot` == `immediate_baseline_after` == `baseline-at-boot/after`:
`production 115→115`, `profile 53→53`, `other-game 5→5`, `novos/removidos/alterados` vazios,
`equal=true`. `restauracao.json`: `rc=0`, `falhas=0`; `registro_antes_sha256 == registro_depois_sha256`
(`ce6049dd…`); `playerprefs_export_equal=true`; `empty_data_check: empty=true`,
`personal_copy_used=false`; `personal_save_selected=false`; `game_closed=true`;
`final_state.game_processes=[]`, `production_junction=false`, `production_backup_exists=false`,
`isolated_profile_exists=false`, `own_lock_released=true`; Cloud: `app_cloudenabled=["0"]` e
`configuration_off=true` no início e no fim (leitura de `sharedconfig.vdf` por app — **não** inferi
servidor Cloud, e o próprio artefato declara "not remote-server inspection").

### R11. Gate full-rstv histórico — **OK**
Hash `ca3d859a25fc40415987082f32a3d1e30d06f88c3bbc8ae6d104b4b7f25fa2b4` inalterado em
`run1471/run1498/run1524` (`seal.json`/`postprocess/summary.json`, `weakened=false`). **Ressalva:**
esta rodada **não** re-executou o gate (nenhum `*full-rstv*` novo); o que eu verifiquei por conta
própria é o que sustenta "não enfraquecido": `rstv.py` idêntico ao HEAD.

## 2. O que continua residual na retomada (não desaparece por esta revisão)

Runner; marcação/export in-game; performance comparável; update/rollback; mod sem kit funcional;
`RSTV-25b-dependencia` (o consumidor não emite `dependency_por_tier`); geometria de tooltip sob hover
não-físico (KIT-G4 / ponteiro físico); `RSTV-6-readonly-personagem` (leitura do alvo vivo da sessão
read-only por reflexão). Nada aqui é KIT14 fechado, DoD, aceite humano ou publicação.

## 3. Correções exigidas (devolvido por rework)

1. **Identidade do personagem por observação (R2).** Fazer a leitura do alvo do ciclo
   (`ReadOnlySession.Target`) devolver identidade, ou reduzir explicitamente a alegação: com
   `same_character_reference=false` e `mesma_referencia_alvo=false` em 32/32, o avaliador canônico
   mantém `RSTV-6-readonly-personagem=NAO_EXERCITADO` e o detector do importador fecha `exit 1`.
2. **Negativo do MESMO leitor com o produto ausente (R7).** Executar o caso `absent` já suportado por
   `campaign.py` (e a variante com snapshot/render ausentes), registrando os exit codes distintos
   `0/1/2` como artefato — hoje `ALVO_AUSENTE` só existe em código.
3. **Patch de integração completo (R9).** Incluir os 18 linhas de costura em `AUT4ProbePlugin.cs` e
   ancorar o patch na fonte viva (a base `048b6a6f…` só existe em scratch). Ajustar a frase sobre
   `tools/.../RstvPostRender.cs`: esse caminho não existe no repositório.
4. **Rastreabilidade (R3).** Rotular na entrega/metadata os quadros do artefato certo
   (on5 = 451–469 / 32,2 s; on6 = 482–498 / 21,6 s) — hoje o doc diz "on6" com os quadros do on5.
5. **Opcional (endurecer, não bloquear):** check independente de pai/índice/duplicata no detector em
   vez de herdar o campo do consumidor; caso mutante de skills/pontos para provar sensibilidade.

## 4. Declaração de limites desta revisão

Revisão **técnica de evidência**, somente leitura. Não executei jogo, build, deploy ou publicação;
não alterei produto, gate, configuração nem artefato do implementador (só criei este relatório).
Não aprovo clique físico, ponteiro humano, UI/UX, campanha integral, DoD ou publicação — e não os
avaliei. Não reivindico estado de servidor Cloud nem uso manifest antigo como baseline de rodada nova.
