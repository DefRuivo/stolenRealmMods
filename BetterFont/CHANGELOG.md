# Changelog — BetterFont

## 1.0.1

**Defeito corrigido (relatado pelo dono): trocar a fonte apagava o estilo e a coloração do jogo — visível principalmente em combate.**

- **Causa (confirmada no IL do TMP):** em TextMeshPro, `texto.font = novaFonte` não troca só o tipo de letra — o `LoadFontAsset()` do TMP descarta o material em uso e passa a usar o material do asset novo (`TextMeshProUGUI.LoadFontAsset` → `m_sharedMaterial = m_fontAsset.material`). Como cor de face, contorno e sombra vivem **no material**, a troca da 1.0.0 (linha `t.font = _serifFont;`) jogava fora o estilo — os materiais estilizados do jogo (`... SDF - Drop Shadow/Outline`, `Title Font ... SDF Material`) não eram reproduzidos.
- **Conserto:** antes de trocar a fonte, o material em uso é capturado (`fontSharedMaterial`) e as **propriedades de estilo** são transportadas para o material **por componente** da fonte nova (`fontMaterial` — instância daquele texto; nada é escrito no material compartilhado nem no material do font asset): `_FaceColor`, `_FaceDilate`, `_OutlineWidth/_OutlineSoftness/_OutlineColor`, `_UnderlayColor/_UnderlayOffsetX/_UnderlayOffsetY/_UnderlayDilate/_UnderlaySoftness`, mais as keywords `OUTLINE_ON`/`UNDERLAY_ON` quando estavam ativas. Todo `Set` é precedido de `HasProperty`.
- **Não transportado de propósito:** atlas/textura e `_GradientScale`/`_TextureWidth`/`_TextureHeight` (pertencem à fonte nova), texturas de face (`_FaceTex`), bevel (`_BumpMap`) e as keywords `GLOW_ON`/`BEVEL_ON` — quando existirem, o log de diagnóstico diz o que ficou de fora.
- **Novo config** `Estilo/PreservarEstilo` (padrão `true`): liga/desliga o transporte do estilo.
- **Novo config** `Estilo/PularTextosEstilizados` (na primeira versão desta 1.0.1, padrão `true`): textos com material próprio (títulos, números de combate) **não trocam de fonte** — visual intacto; só não ganham a serifa. **Em BF-1 esta chave virou o ESCAPE do comportamento antigo e o padrão passou a `false`** — ver a seção do BF-1 abaixo.
- **Novo config** `Diagnostico/LogDiagnosticoEstilo` (padrão `false`): log por texto (objeto, fonte, material compartilhado, shader, o que foi copiado e o que não pôde ser) — para conferir e fechar dúvida.
- `UpdateMeshPadding()` após ligar contorno/sombra (sem isso o contorno é cortado na borda do mesh).
- README: seção do defeito/conserto, tabela de configuração e a convivência com **outros mods que estilizam texto** (o mecanismo do material clonado por componente e por que ele deixa de ser um caso à parte).

### Conserto NA CAUSA: a fonte é trocada E o efeito de material é preservado (BF-1, nesta mesma 1.0.1)

- **Defeito (relatado pelo dono, 30/09): com os dois mods de estilização ligados, os textos de combate ficavam na fonte ORIGINAL enquanto o resto da interface ficava serifada — interface inconsistente.** A causa era a própria proteção da 1.0.1: `EhEstilizado` chamava de "estilizado" todo texto cujo material **em uso** não é o material da sua fonte e mandava **pular** o texto. Quem aplica contorno/halo clonando o material **por componente** (é o mecanismo correto, exigido para não escrever no material compartilhado) deixava o texto exatamente nessa condição — e o BetterFont passava a ignorá-lo.
- **Conserto na causa, genérico e sem acoplar mod nenhum:** o texto estilizado **passa a trocar de fonte**, e os efeitos que já estavam no material anterior daquele texto (cor de face `_FaceColor`/`_FaceDilate`, contorno `_OutlineWidth`/`_OutlineSoftness`/`_OutlineColor` + `OUTLINE_ON`, sombra `_UnderlayColor`/`_UnderlayOffsetX`/`_UnderlayOffsetY`/`_UnderlayDilate`/`_UnderlaySoftness` + `UNDERLAY_ON`) são reaplicados no material **por componente** da fonte nova (`fontMaterial`), com `UpdateMeshPadding()` para o contorno/sombra não serem cortados na borda do mesh. A regra é uma só — "o que estava no material anterior daquele texto continua lá" —, então vale para **qualquer** mod que tenha aplicado efeito antes, não para um caso específico. Nenhuma linha deste mod cita, referencia ou conhece outro mod.
- **Ordem indiferente entre os mods:** efeito aplicado **antes** é transportado pelo BetterFont; efeito aplicado **depois** clona o material já serifado e o mantém. Não há corrida nem ordem obrigatória.
- **Falha-segura (`EstiloTransportavel`):** só se troca a fonte de um texto estilizado se o efeito **em uso** puder ser reproduzido com fidelidade no material novo. Reprova (e aí o texto **não é tocado**, exatamente o comportamento de hoje) quando o efeito depende de textura de face (`_FaceTex`), de bevel (`_BumpMap`), das keywords `GLOW_ON`/`BEVEL_ON`, de um shader diferente do material da fonte serifada, ou de contorno/sombra que o material novo não expõe. Uma cópia parcial sairia **pior** que não mexer; em dúvida (incluindo exceção na conferência), **não estiliza**.
- **Reversível por config:** `Estilo/PularTextosEstilizados` continua existindo e **agora é o escape** — com `true`, o texto com material próprio fica 100% intocado (o comportamento antigo). O padrão virou **`false`** porque era ele que produzia a interface inconsistente; os padrões dos outros dois (`PreservarEstilo = true`, `LogDiagnosticoEstilo = false`) **não mudaram**. Com o `.cfg` ausente/ilegível (getter seguro), o escape vale como ligado — ou seja, cai no comportamento conservador.
- **Log de resumo da varredura** passou a separar os três desfechos: convertidos (efeitos transportados), pulados pelo escape e intocados por efeito não transportável — é por ele que se vê, sem abrir o jogo, se algum texto saiu do caminho novo.

### Correção do aplicador de ganchos (também nesta 1.0.1)

- A troca do `PatchAll()` por **aplicação gancho a gancho** (que entrou nesta versão) veio acompanhada de um filtro de classe de gancho que exigia `[HarmonyPrefix]`/`[HarmonyPostfix]` **no método**. Este mod declara o gancho pela **convenção de nome** do Harmony (`LocalizeFontTrigger.Postfix`), que o Harmony aceita exatamente como o atributo — o filtro recusava a única classe de patch: o mod **carregava, logava "carregado." e não aplicava gancho nenhum** (o silêncio parecendo sucesso; era o defeito A-1 da REV-2, em 4 mods).
- O filtro agora exige só `[HarmonyPatch]` **no TIPO** — o mesmo conjunto de classes que o `PatchAll()` processava. Medido invocando o filtro real da DLL construída: **1 de 1 classe de patch aceita e 1 método de gancho dentro** (antes: 0 de 1). Em todo o projeto, os 4 mods afetados passaram de 0/14 para **14/14** classes de patch aceitas.
- **Esta 1.0.1 não tinha sido publicada** (a versão no ar é a 1.0.0, que carrega os dois defeitos): a correção do estilo e a do aplicador entram nesta mesma build, e é ela que vai para a Thunderstore — por isso o número **não** sobe de novo. No caminho feliz nada muda: o conjunto de ganchos aplicados é o mesmo.
- Também nesta versão, do mesmo endurecimento: o `Config.Bind` ganhou guarda (`BindSeguro`, com try/catch e o default documentado valendo em caso de falha) e o `Update()` do plugin ficou protegido no ponto da chamada — um `.cfg` inválido não derruba mais o mod.

### Dependência declarada neste manifest

- `dependencies`: `BepInEx-BepInExPack-5.4.2305` — **só**. Este manifest **não** declara o `DefRuivo_StolenRealmMods-BetterCombatText` (era o que ele declarava no pacote antigo deste 1.0.1).
- **A dependência entre os dois é UMA DIREÇÃO: `BetterCombatText 0.1.0` → `BetterFont 1.0.1`** — o `BetterCombatText` é quem devolve o estilo (contorno/sombra) nos textos de combate que a troca de fonte, sozinha, não preserva, e é ele que declara a referência. O caminho de volta foi removido no commit `ac0210f`.
- **Por que a mão dupla não sobe (provado no código da Thunderstore):** no upload a plataforma **resolve** cada referência (`DependencyField` usa `PackageReferenceValidator(resolve=True)`) e **recusa** a que não existe, com `No matching package found for reference`. Com os dois lados se referenciando, cada lado apontava para uma versão **inédita** (este `1.0.1` e o `BetterCombatText 0.1.0`, nenhuma das duas no ar) — não havia ordem de envio válida: quem subisse primeiro falhava. Foi por isso que a direção única substituiu a mão dupla, e não por preferência.
- **Ordem de envio que funciona:** o `BetterFont 1.0.1` (este pacote, sem a dependência de volta) sobe primeiro; depois sobe o `BetterCombatText 0.1.0` declarando o `BetterFont 1.0.1` — a mesma ordem registrada em [`release/mods.json`](../release/mods.json).
- **Opção do dono (não é plano, não existe hoje):** se quiser o **ciclo** de verdade, com os dois se referenciando, o caminho é um **`BetterFont 1.0.2` depois**, declarando o `BetterCombatText 0.1.0` já publicado.
- O zip desta 1.0.1 na Release (`pack-2026-09-30`) é o pacote com a **direção única**: o asset antigo (com a mão dupla no manifest) foi substituído em 30/09/2026.

## 1.0.0

Primeira versão publicada.

- **Troca a fonte renderizada do jogo por uma serifada** — Times New Roman, com fallback para Georgia / Liberation Serif — aplicada a **todos os textos TMP**, inclusive telas que abrem depois (level up, tooltips, menus).
- A **fonte original do jogo entra como fallback** do asset serifado, então ícones e símbolos que a Times não tem continuam renderizando (sem quadradinhos).
- A aplicação é **preguiçosa e com throttle**: o updater é criado na primeira UI viva (gatilho em `OptionsManager.Localize`), porque um GameObject criado no `Awake` do plugin é destruído pelo jogo na primeira carga de cena. A varredura roda com tempo real, então funciona mesmo com `timeScale = 0` (menus).
- **Sem qualquer alteração de gameplay.**
