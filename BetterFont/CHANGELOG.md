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

## 1.0.0

Primeira versão publicada.

- **Troca a fonte renderizada do jogo por uma serifada** — Times New Roman, com fallback para Georgia / Liberation Serif — aplicada a **todos os textos TMP**, inclusive telas que abrem depois (level up, tooltips, menus).
- A **fonte original do jogo entra como fallback** do asset serifado, então ícones e símbolos que a Times não tem continuam renderizando (sem quadradinhos).
- A aplicação é **preguiçosa e com throttle**: o updater é criado na primeira UI viva (gatilho em `OptionsManager.Localize`), porque um GameObject criado no `Awake` do plugin é destruído pelo jogo na primeira carga de cena. A varredura roda com tempo real, então funciona mesmo com `timeScale = 0` (menus).
- **Sem qualquer alteração de gameplay.**
