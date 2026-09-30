# Changelog — BetterFont

## 1.0.1

**Defeito corrigido (relatado pelo dono): trocar a fonte apagava o estilo e a coloração do jogo — visível principalmente em combate.**

- **Causa (confirmada no IL do TMP):** em TextMeshPro, `texto.font = novaFonte` não troca só o tipo de letra — o `LoadFontAsset()` do TMP descarta o material em uso e passa a usar o material do asset novo (`TextMeshProUGUI.LoadFontAsset` → `m_sharedMaterial = m_fontAsset.material`). Como cor de face, contorno e sombra vivem **no material**, a troca da 1.0.0 (linha `t.font = _serifFont;`) jogava fora o estilo — os materiais estilizados do jogo (`... SDF - Drop Shadow/Outline`, `Title Font ... SDF Material`) não eram reproduzidos.
- **Conserto:** antes de trocar a fonte, o material em uso é capturado (`fontSharedMaterial`) e as **propriedades de estilo** são transportadas para o material **por componente** da fonte nova (`fontMaterial` — instância daquele texto; nada é escrito no material compartilhado nem no material do font asset): `_FaceColor`, `_FaceDilate`, `_OutlineWidth/_OutlineSoftness/_OutlineColor`, `_UnderlayColor/_UnderlayOffsetX/_UnderlayOffsetY/_UnderlayDilate/_UnderlaySoftness`, mais as keywords `OUTLINE_ON`/`UNDERLAY_ON` quando estavam ativas. Todo `Set` é precedido de `HasProperty`.
- **Não transportado de propósito:** atlas/textura e `_GradientScale`/`_TextureWidth`/`_TextureHeight` (pertencem à fonte nova), texturas de face (`_FaceTex`), bevel (`_BumpMap`) e as keywords `GLOW_ON`/`BEVEL_ON` — quando existirem, o log de diagnóstico diz o que ficou de fora.
- **Novo config** `Estilo/PreservarEstilo` (padrão `true`): liga/desliga o transporte do estilo.
- **Novo config** `Estilo/PularTextosEstilizados` (padrão `true`): textos com material estilizado (material próprio do jogo, ex.: títulos e números de combate) **não trocam de fonte** — visual original intacto; só não ganham a serifa. `false` força a serifa em todos, com o estilo transportado por cópia.
- **Novo config** `Diagnostico/LogDiagnosticoEstilo` (padrão `false`): log por texto (objeto, fonte, material compartilhado, shader, o que foi copiado e o que não pôde ser) — para conferir e fechar dúvida.
- `UpdateMeshPadding()` após ligar contorno/sombra (sem isso o contorno é cortado na borda do mesh).
- README: seção do defeito/conserto, tabela de configuração e convivência com o **BetterCombatText** (que clona o material por componente e se re-aplica quando ele muda; o BetterFont só **lê** material de outro mod).

### Correção do aplicador de ganchos (também nesta 1.0.1)

- A troca do `PatchAll()` por **aplicação gancho a gancho** (que entrou nesta versão) veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara o gancho pela **convenção de nome** do Harmony (`LocalizeFontTrigger.Postfix`), que o Harmony aceita exatamente como o atributo — o filtro recusava a única classe de patch: o mod **carregava, logava "carregado." e não aplicava gancho nenhum** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **1 de 1 classe de patch aceita e 1 método de gancho dentro** (antes: 0 de 1). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- **Esta 1.0.1 não tinha sido publicada** (a versão no ar é a 1.0.0, que carrega os dois defeitos): a correção do estilo e a do aplicador entram nesta mesma build, e é ela que vai para a Thunderstore — por isso o número **não** sobe de novo. No caminho feliz nada muda: o conjunto de ganchos aplicados é o mesmo.
- Também nesta versão, do mesmo endurecimento: o `Config.Bind` ganhou guarda (`BindSeguro`, com try/catch e o default documentado valendo em caso de falha) e o `Update()` do plugin ficou protegido no ponto da chamada — um `.cfg` inválido não derruba mais o mod.

### Dependência declarada neste manifest

- `dependencies`: `BepInEx-BepInExPack-5.4.2305` + **`DefRuivo_StolenRealmMods-BetterCombatText-0.1.0`**. O BetterCombatText é quem devolve o estilo (contorno/sombra) nos textos de combate que a troca de fonte, sozinha, não preserva — os dois andam juntos.
- A referência aponta a versão **nova** dos dois lados de propósito: apontar para a 1.0.0 do BetterCombatText faria o gerenciador resolver o MESMO pacote em duas versões (duas DLLs com o mesmo GUID dentro do BepInEx).
- **Ordem de envio importa:** a Thunderstore valida a dependência no upload resolvendo a referência (`No matching package found for reference`), e os dois pacotes se referenciam — a primeira publicação do par precisa de um dos lados apontando para uma versão que já está no ar (nota de ordem registrada em `release/mods.json`).

## 1.0.0

Primeira versão publicada.

- **Troca a fonte renderizada do jogo por uma serifada** — Times New Roman, com fallback para Georgia / Liberation Serif — aplicada a **todos os textos TMP**, inclusive telas que abrem depois (level up, tooltips, menus).
- A **fonte original do jogo entra como fallback** do asset serifado, então ícones e símbolos que a Times não tem continuam renderizando (sem quadradinhos).
- A aplicação é **preguiçosa e com throttle**: o updater é criado na primeira UI viva (gatilho em `OptionsManager.Localize`), porque um GameObject criado no `Awake` do plugin é destruído pelo jogo na primeira carga de cena. A varredura roda com tempo real, então funciona mesmo com `timeScale = 0` (menus).
- **Sem qualquer alteração de gameplay.**
