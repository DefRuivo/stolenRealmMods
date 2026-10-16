# INT-R1-C4 — parte 03: a suíte, o vermelho→verde fora do repo, o risco do commit e os limites

Cartão `t_84ca88d4`. Continuação de `INT-R1-C4-parte01.md` (reconhecimento) e `-parte02.md` (a migração).

## 1. O que foi acrescentado à suíte do mod

Padrão do projeto (regras em `tools/testes/regras_*.py`, teste em `tools/testes/testes/puros/t_*.py`,
run único `python tools/testes/roda_testes.py`):

| Arquivo (novo) | O que é |
|---|---|
| `tools/testes/regras_int_r1_c4.py` | as regras: pontos migrados, contagem do escopo, pontos presos, a ponte (vínculo + delegação + entrada única), a guarda do commit, a dependência (csproj/plugin/README), o ponto de observação da API e **8 plantadores de defeito** |
| `tools/testes/testes/puros/t_int_r1_c4_familia_ui.py` | o teste `int-r1-c4-familia-ui` (categoria `pura`), que roda as regras e exige que **cada um dos 8 defeitos plantados reprove** |

## 2. A suíte: medido (não estimado)

```
cd C:/dev/stolen-realm && python tools/testes/roda_testes.py --puros
```

| | linha de base (parte 01) | depois desta entrega |
|---|---|---|
| rodaram | 94 | **95** |
| passaram | 93 | **94** |
| reprovaram | 1 | **1** (o MESMO de base) |
| excluídos (`jogo`) | 1 | 1 |

O único vermelho continua sendo `deploy-optin-repo`, **pré-existente e alheio a este cartão**: ele
varre TODO `.csproj` do repositório (inclusive `scratch/`) e reprova por sobras de outro cartão em
`scratch/kit/KIT-14-run699/…` e `scratch/kit/KIT-14-run710/…`. Comparação literal da linha de base
está em `INT-R1-C4-parte01.md` secção 2; a saída desta rodada, em
`docs/automacao/INT-R1-C4-evidencias/04-suite-puros.txt` e `04b-suite-reprovados.txt`.
**Nada disso foi tocado por mim.**

Os três checks read-only do CI, rodados localmente depois da entrega:
`python tools/check_segredos.py` exit 0; `python tools/check_versoes.py` exit 0;
`python tools/check_patches.py` exit 0. `python tools/check_dependencias.py` exit 0
("todas as dependencias resolvem").

## 3. Vermelho→verde NUMA CÓPIA FORA DO REPOSITÓRIO

Regra do projeto: um teste que nunca falhou não é teste. A prova foi feita fora do repositório, para
que o resultado não dependa da árvore viva:

* cópia em `%USERPROFILE%/AppData/Local/hermes/cache/scratch/int_r1_c4_fora` (raiz própria com
  `.git/` + `tools/`, `RoguelikeSkillTreeVisualizer/`, `api/Core/Contracts.cs`, `docs/`);
* com a migração: **VERDE** (`06-fora-do-repo-verde.txt`);
* plantando de volta o `Instantiate` à mão em `RunButton.cs` da CÓPIA: **VERMELHO**
  (`05-fora-do-repo-vermelho.txt`), com o motivo certo:

```
[REPROVOU] int-r1-c4-familia-ui  a migracao regrediu em 2 ponto(s):
 RunButton.cs: o ponto que substituiu `Instantiate(molde.gameObject, parent) + clone.name =
 ButtonName` nao chama a familia UI da API (esperado `RstvApiUi.Clonar(molde.gameObject, parent,
 ButtonName)`)  |  RunButton.cs: `RstvApiUi.Clonar(` aparece 0 vez(es); o esperado e 1
```

* desfazendo o plantio: **VERDE** de novo. Logo, o teste lê a árvore em que está e **mede** a
  migração — não passa por acidente.

Os 8 defeitos plantados **em memória** (dentro do próprio teste, que exige a reprovação de cada um):
(1) clone do HUD à mão, (2) clone da janela à mão, (3) clique do modal à mão, (4) vínculo sem
`allowMutation: true`, (5) ponte voltando a fazer a chamada crua, (6) `[BepInDependency]` apagado,
(7) os ganchos citando a ponte, (8) README sem a dependência. O nono caso de prova é em DISCO: o
teste copia `api/docs/{contract-inventory,ui-contract-diff}.json` para uma pasta temporária, troca o
veredito para `DIVERGENTE` e exige a reprovação pela mensagem certa.

## 4. O risco conhecido do cartão: fechar o viewer nativo COMMITA

Fato do levantamento RSTV-1 (`docs/cobertura/revisao/RSTV-1-investigacao.md`): o fechamento nativo
commita — `CharacterMenusManager.CloseSkillTreeMenu()` (l.48490) chama
`AcceptSkillChanges(closeMenu: true)` (l.48494); e há o segundo caminho em l.108137. O ponto de
observação desse risco na API é o hook `ui.skill-tree.updated` ->
`SkillTreeManager::UpdateSkillTreeItems`, que existe no catálogo do provedor:
`api/Core/Contracts.cs:62`.

**A prova de não-regressão, por estrutura (offline):**

1. a defesa do mod contra esse commit **não está na plumbing de UI**: está nos ganchos — o patch de
   `SkillTreeManager.AcceptSkillChanges` (`Patches.cs:118-119`) e o postfix de
   `CharacterMenusManager.CloseSkillTreeMenu` (`Patches.cs:468`);
2. `Patches.cs` **não aparece no diff** desta entrega (`git diff --stat`, parte 02 secção 8) — os
   ganchos ficaram byte a byte como estavam;
3. o teste exige as duas coisas: a guarda do commit continua no arquivo dos ganchos **e** os ganchos
   não citam `RstvApiUi`/`UIFactory.`/`UiFamily.` — assim a plumbing da API não pode ter aberto
   caminho para dentro da janela que grava;
4. o ponto de observação para um futuro smoke em jogo existe e é exigido pelo teste
   (`regras_int_r1_c4.falhas_do_ponto_de_observacao`).

**O que NÃO foi provado:** a observação EM JOGO pelo hook (o hook disparar no fechamento e a leitura
dos argumentos/estado) — **NAO_EXERCITADO**, porque este cartão proíbe abrir o jogo. É exatamente o
ato que o dono autoriza depois.

## 5. Limites respeitados (cada um com a prova)

| Limite do cartão | Situação |
|---|---|
| não instalar | nada foi copiado para o perfil: build com `-p:DeployToBepInEx=false` (o alvo tem `Condition` de opt-in) |
| não abrir o jogo | nenhum processo do jogo foi iniciado nesta rodada |
| não publicar | nenhum pacote/zip gerado, nenhum upload |
| não editar `Assembly-CSharp.dll` | intacto; o mod só o referencia (`lib/Assembly-CSharp.dll`, `Private=false`) |
| não alterar `BetterTooltips`/`BetterCombatText` | `git status` deles: sem alteração minha (o build do BetterTooltips foi usado só para medir o aviso pré-existente) |
| não reabrir aceites anteriores do RSTV | os literais presos continuam presos — o teste reprova se algum sumir (parte 02 secção 4) |
| não reintroduzir o botão da tela Select Party / não tocar no F10 | `regras_rstv28.py` (superfície removida) e `regras_rstv11.py` (atalho) continuam verdes |

## 6. NAO_EXERCITADO (declarado, nunca estimado)

* **Runtime**: o `UiFamily.Bind` dentro do processo BepInEx, a criação visual dos clones (o
  `Instantiate` real da Unity), o clique dos botões, o vínculo em jogo com `GUIManager.instance`
  disponível — tudo **NAO_EXERCITADO**. A validação visual é do dono (aceite do cartão).
* **Observação do commit em jogo** pelo hook `ui.skill-tree.updated` — **NAO_EXERCITADO** (secao 4).
* **Carga do plugin sem a API**: o comportamento "BepInEx recusa carregar o mod" é o contrato do
  `[BepInDependency]` hard do BepInEx; não foi exercitado num processo real (nem com a API ausente
  nem com versão antiga) — **NAO_EXERCITADO**.
* **Dependência no `manifest.json`** (Thunderstore): deliberadamente NÃO declarada enquanto a API
  não estiver publicada — `tools/check_dependencias.py` recusaria o pacote inteiro
  (`No matching package found for reference`). Follow-up de publicação.
* **`CHANGELOG.md`/versão do mod**: NÃO alterados. O cartão pede build + suíte + README; subir a
  versão (0.3.3 -> 0.4.0, por ser dependência nova) mexe em TRÊS lugares sincronizados
  (`csproj`/`manifest.json`/`Plugin.cs`, PKG-2) e é decisão de release, não desta migração.
  Registrado aqui para não passar em branco.

## 7. Artefatos e evidências

* Artefatos desta entrega: `docs/automacao/INT-R1-C4-parte01.md`, `-parte02.md`, `-parte03.md`.
* Evidências medidas em `docs/automacao/INT-R1-C4-evidencias/`:
  `01-diff-stat.txt`, `02-diff-completo.txt`, `03-build-release.txt`, `04-suite-puros.txt`,
  `04b-suite-reprovados.txt`, `05-fora-do-repo-vermelho.txt`, `06-fora-do-repo-verde.txt`,
  `07-ilspy-equivalencia.txt`.
* Código: `RoguelikeSkillTreeVisualizer/RstvApiUi.cs` (novo) + 6 arquivos editados
  (`Plugin.cs`, `RunButton.cs`, `RemovalWindowSkillsButton.cs`, `SkillTreesTab.cs`,
  `SkillTreesWindow.cs`, `RoguelikeSkillTreeVisualizer.csproj`) e o `README.md` do mod.
* Suíte: `tools/testes/regras_int_r1_c4.py` e `tools/testes/testes/puros/t_int_r1_c4_familia_ui.py`.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
