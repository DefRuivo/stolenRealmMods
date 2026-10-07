# AUT-4R — revisão do coletor para integração ao ciclo (t_e577eedf)

Revisor: agente independente (não é o autor) · tarefa `t_e577eedf` · 2026-10-05
Escopo: **revisar o coletor AUT-4 existente (SOMENTE LEITURA)** e apontar o que falta para **integrá-lo
ao ciclo** (CIC-1..4). Foco: **campos que o probe REAL emite**, como alimentar RSTV/shrines/materials e o
**menor próximo passo de coleta real autorizada** para reduzir carga humana — **não** auditoria expansiva
de segredos/hardening. Nada foi executado em jogo: sem build no perfil, sem instalar probe, sem abrir/
encerrar jogo, sem save, sem commit/board/publicação. Rodada **OFFLINE**.

> A revisão anterior (mesma tarefa, foco segurança) estava neste arquivo; os achados A1–A9 dela estão
> preservados no apêndice ao fim e a cópia em `scratch/aut4r-ciclo/AUT-4R-revisao-previa-15h57.md`.

## Método e estado medido no disco (hashes reais)

| artefato | sha256 |
|---|---|
| `tools/automacao/runtime/coletor.py` | `cab67bc175c045b2ec816a1407048ff332b134aef2d00eef7a986f612db49b15` |
| `tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs` | `5605b1fa52f3443a0f2efa6dbfa953fe8d0dbf24e915b14d61d2fd4d2e723d18` |
| `tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll` | `e8ee229b38fdc3d7f8800fe06606e197528ab7a112f439e2ae2665fbb47ba62d` (= `AUT-4-estado.json`) |
| `docs/automacao/AUT-4-estado.json` | `91bfe7bd739a4c967bb331b631e2bdd0481a6224bbf77b1fd3437da1df0ac6d7` |

Comandos exercitados (offline, sem jogo):

```
python tools/automacao/runtime/roda_testes_runtime.py               -> VERDE, 6/6, exit 0
python tools/automacao/runtime/roda_testes_runtime.py --contra-prova -> VERDE, 2/2 iscas reprovam, exit 0
python tools/automacao/runtime/coletor.py --plano .../plano-exemplo.entrada.json -> exit 2 / NAO_EXERCITADO
```

Leitura do **binário** (não só do fonte): `ilspycmd -t Aut4Probe.Aut4ProbePlugin <dll>` decompilou 1188
linhas e confirma que as chaves emitidas na DLL batem com o fonte. Evidência em
`scratch/aut4r-ciclo/plugin.decompiled.cs` e simulação em `scratch/aut4r-ciclo/sim_integracao.*`.

## Mapa de campos — o que o probe REAL emite × o que a integração consome

`Leitura()` (`AUT4ProbePlugin.cs:360-395`) emite **18 chaves por observação** (confirmado no IL, l.552):

| campo emitido | no schema de `coletor.py` (`CAMPOS`) | utilidade na integração |
|---|---|---|
| `objeto`, `caminho` | ✅ | identifica o alvo (título/descrição/tela) |
| `ativo_na_hierarquia` | ✅ | controla o fallback de texto |
| `texto_bruto`, `texto_renderizado` | ✅ | **texto renderizado** = o que o jogador vê (RSTV/tooltips) |
| `fonte`, `material`, `shader` | ✅ | **materials** / BetterFont (fonte/material) |
| `keywords` (OUTLINE_ON/UNDERLAY_ON/UNDERLAY_INNER/GLOW_ON/BEVEL_ON) | ✅ | estilo de material |
| `cores` (texto/face/contorno/sombra) | ✅ | contraste/estilo (design) |
| `geometria` (caixa_na_tela_px{x,y,largura,altura}, tamanho_do_rect_px, escala, tela) | ✅ | **RSTV** (posição/tamanho na tela) |
| `owners` (Harmony.GetPatchInfo dos funis) | ✅ | quais mods patcheiam o quê |
| `personagem` (gui_state, tem_personagem_selecionado, personagem) | ✅ | contexto de tela/personagem (não é o save) |
| `componente` (TextMeshProUGUI/…) | ❌ **descartado** | distingue o componente |
| `visivel_na_tela` (isActiveAndEnabled && activeInHierarchy) | ❌ **descartado** | distingue "ativo" de "visível" |
| `shader_suportado` | ❌ **descartado** | integridade do material (shader quebrado) |
| `tamanho_fonte` | ❌ **descartado** | tamanho de fonte (design/BetterFont) |
| `nota_texto_renderizado` | ❌ **descartado** | fallback declarado p/ objeto inativo |

**Topo do JSON do probe** (fora da observação): `sessao`, `hash_fonte`, `aplicacao` (produto/versão/unity/
cena/resolução/plataforma/frame/timeScale), `owners_harmony`, `mods_carregados`, `estado_da_tela`,
`rollback`, `manifest`, `prints`, `marcos`, `total_observacoes`, `duracao_s`.

### Cobertura por consumidor

- **RSTV (AUT-5):** `texto_renderizado` + `geometria` + `fonte/material/shader/cores/keywords` + `owners`
  — **o probe cobre** (na fonte). Limite: a `geometria` é a caixa do `TMP_Text`, **não** o id do nó de
  skill; o adaptador casa por `objeto`/`caminho`. Chegar à árvore exige `Navegar=true` + tela Select Party
  (carrega o save) → **autorização específica**.
- **Materials / BetterFont:** `material`, `shader`, `keywords`, `cores` presentes; **`shader_suportado` e
  `tamanho_fonte` são descartados** pelo schema canônico → hoje não atravessam a normalização.
- **Shrines (AUT-6 / RV-26..34):** verificação é **offline por log** (`tools/checa_shrines.py` lê
  `LogOutput.log`, exit 0/1/2/3). O probe **não emite** número/aura de shrine. Portanto **não** usar AUT-4
  como prova de shrine; ele só acrescenta o texto renderizado se aquela tela estiver aberta.

## Costura probe → coletor: o que quebra hoje (medido, não opinião)

Simulação offline alimentando o coletor com observações no formato exato do probe
(`scratch/aut4r-ciclo/sim_integracao.saida.json`):

- **B1 — GRAVE — observação do probe não tem `sessao`/`hash_fonte` por item.** O probe guarda os dois só
  no topo (`AUT4ProbePlugin.cs:105-106`); `normalizar_observacao(...,"runtime")` os **exige por observação**
  (`coletor.py:130-134`). Resultado real: `A_sem_hash_por_obs = RECUSOU: procedencia=runtime exige sessao,
  hash_fonte nao vazio`. **Não há glue** que copie o topo para cada item (`grep` não acha consumidor de
  `aut4probe.json`). ⇒ alimentar o JSON do probe direto no ciclo **falha**.
- **B2 — MÉDIO — 5 campos do probe são descartados.** `normalizar_observacao` só monta `campos` a partir
  de `CAMPOS` (13, `coletor.py:37`); a simulação mostrou `B_extras_do_probe_preservados = [componente,
  nota_texto_renderizado, shader_suportado, tamanho_fonte, visivel_na_tela]`. Para design/material, 2 deles
  importam.
- **B3 — MÉDIO — "todos os 13 campos" torna a consolidação sempre INCOMPLETA.** O probe inclui objetos
  **nomeados inativos** (Title/Description/…), cujo `texto_renderizado` é `null`. A simulação deu
  `C_inativa_lacunas=[texto_renderizado]` → `consolidar` = **INCOMPLETO / exit 1**. Como o ciclo deve
  *reduzir* carga humana, o critério tem de ser **por campo-alvo** (cada cenário diz o que importa), não
  "os 13 de todo TMP_Text".

## Veredito por critério

| # | critério | veredito | prova |
|---|---|---|---|
| 1 | contrato offline do coletor (opt-in; AUSENTE nunca OK; fixture≠runtime; manifest/rollback) | **OK** | suite 6/6 exit 0; contra-prova exit 0; default exit 2; hashes acima |
| 2 | probe compila e as chaves estão no binário | **OK (fonte/binário)** | IL `Leitura` (l.552) emite as 18 chaves; csproj netstandard2.1 sem `DeployToBepInEx` |
| 3 | **probe REAL emite campos em sessão viva** | **INDETERMINADO** | nada rodou em jogo; nenhum tick medido. Fonte ≠ execução |
| 4 | costura probe→coletor pronta para o ciclo | **ACHADO (B1, B2, B3)** | simulação acima; sem glue |
| 5 | driver sobrevive à destruição do GameObject do plugin | **ACHADO** | IL l.287 `if (!((Object)(object)instancia == (Object)null))` = operador Unity → **fake-null**; `gancho` (fonte l.216) e `motor` (l.758) mortos; só `DelegadoDeQuadro` (IL l.209, sem check) sobrevive; **sem fallback** |
| 6 | integração RSTV / materials / shrines | **PARCIAL** | RSTV/materials cobertos na fonte; shrines **não** é caso de AUT-4 (é log) |
| 7 | reduz carga humana já nesta rodada | **NÃO AINDA** | depende de B1–B3 + 1 rodada autorizada |

**Não aprovo runtime não exercitado.** O que está OK é a camada **offline**; o probe em jogo segue
**NÃO EXERCITADO**.

## Menor próximo passo de coleta real autorizada

Pré-condição (offline, sem jogo — é o que torna a rodada útil):
1. **B1/B2/B3** na costura: ao carregar `aut4probe.json`, injetar `sessao`/`hash_fonte` do topo em cada
   observação, **carregar** os 5 campos extras e marcar **campos-alvo por cenário** (não-alvo vira
   "não-aplicável", não "lacuna").
2. Escrever o `.cfg` com `Autorizado=true`, `HashFonte=<sha do fonte/DLL>` e `PerfilDir` (não há rotina que
   o faça hoje — A8).
3. Build `-p:DeployToBepInEx=false` em **cópia isolada**.

Rodada mínima (uma frente):
4. Instalar o probe em perfil **isolado** (ou perfil do dono com autorização explícita + rollback), lançar
   **pelos argumentos de doorstop** (não o `.exe`), esperar **estado** de UI com texto renderizado — a tela
   de loading/menu, onde o CAP-1 já provou tooltip ("Barrels"), serve. `Navegar=false`.
5. Deixar finalizar `aut4probe.json`; consumir `manifest` + `rollback` e restaurar/remover **exato**.
   Prova o essencial: o **PlayerLoop tickou**, os campos **saíram vivos** e o PNG saiu pela API do Unity.
   **Não abre save, não vai à árvore de skills, não combate.**

## Roteiro do usuário (só autorização/instrumentação — sem fingir hot-reload)

- Precisa do dono apenas: **(a)** autorizar **uma** frente runtime (instalar probe + iniciar o jogo, **sem
  save/combate**); **(b)** dizer se usa **perfil isolado** ou o perfil dele (com rollback exato).
- **O probe é NOVO: exige instalar e INICIAR o jogo.** Não há recarga a quente; **não** prometer reload.
- Só para chegar à **árvore de skills** (RSTV) numa 2ª rodada: aí sim exige carregar o save → autorização
  específica. Isso **não** faz parte do menor passo.

## Limites desta revisão

- **Nada em jogo**: emissão real de campos, PNG, owners vivos e rollback **executado** são **NÃO
  EXERCITADOS**. A afirmação "o probe emite X" é sobre a **fonte/binário**, não sobre uma rodada.
- Cobertura: **offline** (suite + contra-prova + simulação da costura) e leitura do binário. Não rebuildei
  o probe (a DLL do repo foi decompilada e confere com o fonte; hash declarado em `AUT-4-estado.json`).
- Não toquei em produto, probe, cenários (CIC-1..4 em andamento) nem em board. **Único arquivo escrito:**
  `docs/automacao/AUT-4R-revisao.md`.

## Apêndice — achados A1–A9 da rodada anterior (foco segurança), preservados

A1 grave: `planejar_rodada` só imprime plano (lista de strings), não dirige/instala/lança — a orquestração
do CAP-1 não foi portada. A2 grave: rollback declarativo (lista), `planejar_rollback` órfão. A3 grave:
igual ao critério 5 acima (guarda fake-null derruba gancho e motor). A4 médio: `manifest` auto-referente
fica stale (hash do próprio JSON não confere). A5 médio: teste de contrato do probe é token-only (aceita
stub). A6 médio: procedência por observação não fecha (== B1). A7 baixo: PNG não finalizado entra no
manifest sem flag `existe`. A8 baixo: nenhuma rotina deriva `HashFonte`/`PerfilDir`/`.cfg` (== pré-item
2). A9 baixo: hash da DLL não é auto-verificável sem `-p:PathMap`. **Secundários (A4/A5/A7/A9) vão para
backlog; A1/A2/A3 são bloqueadores antes de autorizar a rodada.**
