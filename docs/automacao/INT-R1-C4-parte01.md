# INT-R1-C4 — parte 01: reconhecimento (o que existe hoje, medido)

Cartao: `t_84ca88d4` (INT-R1-C4). Consumidor do provedor `t_9fa61e7e` (INT-R1-C1, familia `UI` da API).
Data da rodada: 2026-10-11. Modelo do worker: `deepseek-flash` / `deepseek`.

REGRA DESTE ARTEFATO: todo numero aqui tem comando ou caminho de arquivo. O que nao foi exercitado
esta declarado `NAO_EXERCITADO`.

## 1. Onde esta o trabalho

* Repositorio real: `C:/dev/stolen-realm` (o `api/` esta UNTRACKED: `git status --short` ->
  `?? api/`, logo um worktree novo nasce sem a API — mesmo achado do cartao provedor
  `t_9fa61e7e`, registrado no handoff dele em `repo_note`).
* Mod consumidor: `C:/dev/stolen-realm/RoguelikeSkillTreeVisualizer/` — 16 arquivos `.cs` na raiz
  (`find RoguelikeSkillTreeVisualizer -maxdepth 1 -name '*.cs' | wc -l` -> 16).
* Suite do mod (o que o aceite chama de "suite"): `python tools/testes/roda_testes.py --puros`
  (runner unico do repo; contrato em `tools/testes/README.md`).

## 2. LINHA DE BASE DA SUITE (antes de qualquer alteracao minha)

Comando:

```
cd C:/dev/stolen-realm && python tools/testes/roda_testes.py --puros
```

Resultado medido (rodada inicial, ANTES de qualquer edicao):

```
   rodaram:    94
   passaram:   93
   reprovaram: 1
   nao rodaram:0
   EXCLUIDOS por categoria (1): jogo=1
 VEREDITO: REPROVADO (exit 1)
```

O unico vermelho de base e `deploy-optin-repo`, e ele NAO tem relacao com o RSTV: o teste varre
TODO `.csproj` do repositorio (inclusive `scratch/`) e reprova por sobras de outro cartao:

* `scratch/kit/KIT-14-run699/deploy-negative/ruim.csproj` (alvo de deploy sem a Condition de opt-in);
* `scratch/kit/KIT-14-run699/instalacao-local-resume/.kit-rstv-backups/…/KIT04Adapter.SR.csproj` (XML invalido);
* `scratch/kit/KIT-14-run710/deploy-negative/ruim.csproj` (mesmo defeito do primeiro).

Isto e PRE-EXISTENTE e anterior a esta rodada; esta linha de base fica registrada para que o aceite
"suite verde" seja lido contra ela (o verde que eu preciso provar e o da familia RSTV + os testes
novos desta migracao). NAO removi os arquivos de `scratch/`: nao sao meus e nao sao deste cartao.

## 3. O que o mod escreve a mao (plumbing de UI) — medido por grep

Comando:

```
cd C:/dev/stolen-realm/RoguelikeSkillTreeVisualizer
grep -n -E "Instantiate|onClick|GetComponent<Text>|GetComponent<Image>|\.sprite|\.Find\(|GetComponentsInChildren|LayoutGroup|Destroy\(|AddListener|Localiz|TextMeshPro" *.cs
```

Superficie de plumbing encontrada (resumo; 8 arquivos com ocorrencia):

| Arquivo | Plomberia de UI que escreve a mao |
|---|---|
| `NativeUiHelpers.cs` | `DescribeGroup` (diagnostico de LayoutGroup), `DisableLocalizers` (varre componentes por nome), `ClearClickListeners` (troca a INSTANCIA do `Button.onClick`) |
| `RunButton.cs` | `Instantiate(molde.gameObject, parent)` + nome, `LayoutElement.ignoreLayout`, `ClearClickListeners`, `onClick.AddListener`, leitura de `Skillbar Buttons`, medicao de posicao (`GetWorldCorners`/`InverseTransformPoint`) |
| `RemovalWindowSkillsButton.cs` | `Instantiate(molde.gameObject, pai)`, `DisableLocalizers`, `ClearClickListeners`, `onClick.AddListener`, `GetComponentsInChildren<TextMeshProUGUI>` |
| `LevelUpWindowButton.cs` | `Instantiate(original.gameObject, janela.transform)`, `DisableLocalizers`, `ClearClickListeners`, `onClick.AddListener`, `TextMeshProUGUI` |
| `SkillTreesTab.cs` | clone da ABA (`Instantiate(menu.TabSkillTree.gameObject, pai)`), `TextMeshProUGUI`, `onClick.AddListener`, `HorizontalLayoutGroup`, clone de botao de classe, `Instantiate(gui.skillTreeItemActivePrefab, …)` |
| `SkillTreesWindow.cs` | clone de titulo/botao de fechar (`Instantiate(molde, cabecalho)`), `Image.sprite` de fundo/moldura/divisor, `onClick.AddListener` |

## 4. O que a familia `UI` da API OFERECE (contrato, lido do fonte)

Prova do contrato: `api/docs/contract-inventory.json` (familia `UI`) e a implementacao
`api/Plugin/Ui/*.cs` + `api/Core/Ui/UiFamily.cs`. Os 5 tipos e as 21 assinaturas:

* `UIFactory`: `Clone(template)`, `Clone(template,parent,name)`, `CloneComponent`, `CopyRectLayout`,
  `FindChild`, `BindClick`, `SetText`, `SetIcon`, `DisableAllText`, `DisableChildLayouts`, `Destroy`;
* `ActionBarUI`: `AddButton`, `RemoveButton`, `UpdateIcon`;
* `SkillTreeUI`: `AddTab`, `RemoveTab`, `HasTab`;
* `MenuUI`, `TooltipHelper`.

Guardas (medidas em `api/Core/Ui/UiFamily.cs:174-235`): exigem `UiFamily.Bind(assembly, hosts,
allowMutation)` previo; `Require` lanca sem vinculo / sem `allowMutation` / fora do thread do vinculo;
os 4 hospedeiros (`GUIManager`, `CurrentCharacterUI`, `SkillTreeManager`, `MenuTabManager`) vem do
consumidor em `UiHosts` e hospedeiro nulo = aquela familia falha fechado.

## 5. A TENSAO MEDIDA (por que a migracao nao pode ser "trocar tudo")

As regras de aceite ANTERIORES do RSTV prendem, no FONTE, o TEXTO das chamadas de plumbing. Medido:

| Regra | Exige o literal | Arquivo |
|---|---|---|
| `tools/testes/regras_rstv11b.py:214` | `Instantiate(original.gameObject, janela.transform)` | `LevelUpWindowButton.cs` |
| `tools/testes/regras_rstv11b.py:235,243` | `NativeUiHelpers.ClearClickListeners(button)` e `AddListener(new UnityAction(RunButton.OpenForTarget))` | `LevelUpWindowButton.cs` |
| `tools/testes/regras_rstv12.py:221-233` | `ClearClickListeners(button)` ANTES de `.onClick.AddListener` | `RunButton.cs` + `LevelUpWindowButton.cs` |
| `tools/testes/regras_rstv16.py:69,73,74` | `Instantiate(menu.TabSkillTree.gameObject`, `ClearClickListeners(botao)`, `AddListener(new UnityAction(SelecionarEMostrar))` | `SkillTreesTab.cs` |
| `tools/testes/regras_rstv21.py:598` | `AddListener(new UnityAction(Fechar))` | `SkillTreesWindow.cs` |
| `tools/testes/regras_rstv30.py:116,426-430` | `NativeUiHelpers.ClearClickListeners(button)` + `.onClick.AddListener` | `RunButton.cs` |

Logo: o cartao pede migrar a plumbing, e o proprio acervo de aceites anteriores do RSTV REPROVA a
troca do texto dessas chamadas. Isso NAO e um impedimento: e' o mapa do escopo REAL. As duas coisas
convivem — a migracao vai para os pontos que a API cobre de forma EQUIVALENTE e que nao sao o texto
preso por um aceite anterior; o que a API NAO cobre de forma equivalente fica como estа e e
declarado com motivo (secao 6).

## 6. O que a API NAO cobre de forma equivalente (medido, com motivo)

1. **Texto**: `UIFactory.SetText` usa `UnityEngine.UI.Text` e FALHA FECHADO com
   `MissingComponentException` em TextMeshPro (`api/Plugin/Ui/UIFactory.cs:81-87`). O mod rotula com
   `TextMeshProUGUI` (`LevelUpWindowButton.cs:280`, `RemovalWindowSkillsButton.cs:358`,
   `SkillTreesTab.cs:243`, `SkillTreesWindow.cs:433`). Trocar seria MUDANCA DE COMPORTAMENTO.
2. **Clone**: **EQUIVALENTE — e por isso o clone foi migrado** (corrigido na revisao da rodada 1;
   ver `INT-R1-C4-parte04.md`). `UIFactory.Clone` clona com `Instantiate(template, parent, false)`
   (`api/Plugin/Ui/UIFactory.cs:33`); o mod usava `Instantiate(obj, parent)`, e o overload de DOIS
   argumentos do jogo cai em `Instantiate(original, parent, instantiateInWorldSpace: false)` —
   MEDIDO em `lib/UnityEngine.CoreModule.dll` (SHA-256
   `80d43e5f8d52964e3ec0ac514076c3e2ee032af8d9c0c3ef511dfdd9067eee8e`,
   `ilspycmd -t UnityEngine.Object`, linhas 321-324 e 363-366; saida em
   `INT-R1-C4-evidencias/07-ilspy-equivalencia.txt`). Ou seja: **a MESMA chamada, para QUALQUER pai**
   — nao so para o mesmo pai (prova em `INT-R1-C4-parte02.md` §1). As duas diferencas REAIS do
   primitivo, tambem medidas, e sem efeito nos 7 pontos migrados: (a) `UIFactory.Clone` lanca
   `ArgumentNullException` em `template`/`parent` nulo (`UIFactory.cs:31-32`), enquanto
   `Instantiate(Object, Transform)` com pai nulo cai em `Instantiate(original)`
   (`CoreModule.dll`: o overload de 3 argumentos, l.329-332) — os 7 pontos checam pai/molde antes de
   clonar, entao nunca chegam ao caso nulo; (b) o nome do clone, que `UIFactory.Clone` aplica pelo
   parametro `name` e o mod fazia logo depois com `clone.name = ...` (parte 02 §1).
3. **`FindChild`**: falha fechado (lanca) quando o filho nao existe (`UIFactory.cs:62-68`); o mod usa
   `Transform.Find(...)` e trata o nulo (`RunButton.cs:178`, `SkillTreesTab.cs:324`). Nao e equivalente.
4. **`ActionBarUI` / `SkillTreeUI` / `MenuUI`**: registram o pedido e mandam o hospedeiro nativo
   RECONSTRUIR (`RefreshSkillBar`/`UpdateSkillTreeItems`/`RefreshSelected`); eles **nao criam** o
   elemento visual (`api/README.md:256-262`, secao "NÃO exercitado"). O mod CRIA o elemento a partir de
   um prefab nativo — usar `AddTab`/`AddButton` produziria um registro sem botao. MUDANCA DE
   COMPORTAMENTO.
5. **`TooltipHelper`**: esconde o tooltip nativo; o mod nao desenha tooltip proprio nesta plumbing.

## 7. NAO_EXERCITADO nesta parte 01

* Runtime em jogo: NADA foi chamado dentro do jogo (`NAO_EXERCITADO`; o aceite ja diz que a
  validacao visual e do dono).
* Os 3 vermelhos de `deploy-optin-repo` acima nao foram corrigidos nem removidos.
