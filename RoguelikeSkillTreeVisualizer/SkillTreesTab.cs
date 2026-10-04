using System;
using System.Collections.Generic;
using Burst2Flame;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-16 — a aba "All Skill Trees" DENTRO do inventario (decisao do dono, 02/10): uma aba nova na
    /// barra do <c>CharacterMenusManager</c> que mostra TODAS as arvores de skill em modo somente
    /// leitura. A janela read-only separada das RSTV-2/5/15 foi APOSENTADA.
    ///
    /// AS PREMISSAS CORRIGIDAS PELOS REVISORES (02/10)
    /// ----------------------------------------------
    ///  1. O READ-ONLY NAO E AUTOMATICO. A `SkillTreeManager` e PRE-CARREGADA pelo jogo
    ///     (`LoadingScreen.LoadStateBasedResources`, l.136586-136596) e fica `SetActive(false)` — logo
    ///     `LoadableUIWindow&lt;SkillTreeManager&gt;.Instance` NAO e nulo e as guardas
    ///     `if (Instance == null) return;` de `SkillTreeItem` NAO disparam: um clique cairia no corpo
    ///     real e mutaria `SkillsToAdd`. O read-only vem da SESSAO: `ReadOnlySession.Active = true`
    ///     enquanto a aba esta visivel, e o prefixo `SkillTreeItemTogglePatch` (Patches.cs) ja barra o
    ///     clique quando a sessao esta ativa. NAO confiar em guarda de null.
    ///  2. A FONTE certa NAO e `SkillsByTreeDict` (l.443327, filtra so Tier/Disabled/FullReleaseMode e
    ///     OMITE `DontIncludeInTree` e o DLC). A regra canonica e a de `RefreshAvailableSkillTrees`
    ///     (l.170100-170118): percorrer `miscSettings.SkillTabTypes` e exigir
    ///     `MeetsDLCRequirements(type)` + existir skill com
    ///     `!Disabled && !DontIncludeInTree && Game.Instance.FullReleaseModeEnabled(skill)`. No
    ///     conteudo, o predicado e aplicado direto sobre `Game.Instance.Skills` (o `EditorSkills`).
    ///  3. NAO reusar `PopulateAllTrees`/`PopulateTree`/`ProcessDependencyLines`: sao metodos DE
    ///     INSTANCIA e dependem de `skillTreeShowers[]` e do estado vivo. Aqui o layout e
    ///     REIMPLEMENTADO desacoplado (mesma formula de `PopulateTree`, l.177739-177772, e de
    ///     `ProcessDependencyLines`, l.177056), sem tocar no manager.
    ///  4. SAO ~10 classes visiveis (Bard fora por decisao do dono; `Basic`/`Innate` NAO sao arvores —
    ///     excluidos em l.170113; Chaos condicional pelo `FullReleaseModeEnabled`/DLC). A lista espelha
    ///     `RefreshAvailableSkillTrees`.
    ///  5. `MenuTabManager.Underline` tem largura FIXA no prefab (~74.5): ao selecionar a aba, a largura
    ///     e ajustada para a do rotulo (`preferredWidth`) e RESTAURADA ao sair.
    ///  6. O rotulo "All Skill Trees" e largo (~130u) e pode encostar no ouro/X em 4:3/16:10; a
    ///     constante `TabLabel` esta num lugar so — se apertar em jogo, trocar por "Skill Trees" ou
    ///     "All Trees" (~78u).
    ///  7. A fileira de classes reusa a fileira NATIVA `SkillTreeTab` (icone+nome, l.178841), mostrando
    ///     UMA arvore por vez — nada de grade de 11 mini-arvores. Fallback: clone da aba do header.
    ///  8. A aba ENTRA no array publico `MenuTabs` (`GetNextActiveTab` usa `Array.IndexOf`; fora dele o
    ///     jogo loga "Tabbing broke"). O handler da aba chama `SelectButton` (so marca) — quem troca o
    ///     conteudo e o onClick; `SelectButtonAndInvoke` fica so no caminho programatico (que re-invocaria
    ///     se usado dentro do proprio handler). `Initialize()` NUNCA e chamado as cegas (dispara
    ///     `SelectFirstActiveButton`). O inventario abre PRIMEIRO; a aba e selecionada depois.
    ///
    /// AS PECAS (decompilado — os numeros de linha sao de Assembly-CSharp)
    /// -------------------------------------------------------------------
    ///  * A barra e o `MenuTabManager` (l.140632, array PUBLICO `MenuTabs[]` l.140636);
    ///    `SelectButtonAndInvoke` (l.140765) marca E invoca; `SelectButton` (l.140744) so realca. O
    ///    acesso e `GetComponentInChildren&lt;MenuTabManager&gt;(true)` (l.49100 — a propriedade e privada).
    ///  * O no e o `GUIManager.skillTreeItemActivePrefab` (l.119765); a posicao replica `PopulateTree`
    ///    (l.177739): por tier, `((xVal-1)*±hp ± hp/2, (tier-1)*-vp)`, com o sinal pela existencia de
    ///    `ActionsGranted`; `hp`/`vp` sao `nodeHorizontalPadding`(47)/`tierVerticalPadding`(35).
    ///  * As linhas de dependencia replicam `SkillTreeItem.ProcessDependencyLines` (l.177056): por no,
    ///    os filhos cujo `SkillInfo.Dependency` aponta para ele — 1 filho liga a `DependencyLine`
    ///    (reparenteada para a NOSSA area), 2 ligam o `DoubleDep`, nenhum desliga os dois.
    ///
    /// IDEMPOTENTE por NOME; o gancho de reinjecao e o postfix de `CharacterMenusManager.OpenWindow`
    /// (Patches.cs). A vida da visualizacao (e da sessao read-only) passa a ser a do SISTEMA DE ABAS.
    /// </summary>
    internal static class SkillTreesTab
    {
        internal const string TabName = "RstvAllSkillTreesTab";

        // ---------------------------------------------------------------------------------------
        // RSTV-17 (o ponto 6 antigo, agora MEDIDO no prefab) — O ROTULO E A LARGURA DA ABA
        // ---------------------------------------------------------------------------------------
        // O HLG do header ('Menu Tab Manager', na cena level1) e MiddleCenter com
        // childControlWidth LIGADO e spacing 29.03: cada aba tem a largura do PROPRIO rotulo.
        // As 3 abas nativas medem, em unidades do prefab: Character=97.82 | Skill Tree=87.12 |
        // Fortunes=83.67. "All Skill Trees" dava ~163u (~1.7x a maior) e, como o grupo e
        // CENTRADO, a aba larga empurrava as 3 nativas para a esquerda — o "re-centralizar" do
        // grupo que o dono viu (image_660d3b/image_894109). "All Trees" (~78u) fica dentro do
        // padrao nativo; e `FixarLarguraDaAba` ainda trava a largura na da maior aba nativa.
        internal const string TabLabel = "All Trees";
        internal const string PanelName = "RstvAllSkillTreesPanel";
        internal const string ClassBarName = "RstvClassBar";
        internal const string TreeAreaName = "RstvTreeArea";
        internal const string NodeContainerName = "RstvNodeContainer";

        private const float MargemSuperior = 6f;
        private const float MargemInferior = 8f;
        private const float MargemLateral = 8f;
        private const float AlturaDaBarraDeClasses = 84f;

        // ---------------------------------------------------------------------------------------
        // RSTV-17 — OS NUMEROS DO `SkillTreeTab` NATIVO (medidos no PREFAB, nao estimados)
        // ---------------------------------------------------------------------------------------
        // Fonte: `resources.assets`, 'Skill Tree Window' > 'Tabs' > 'Skill Tree Tab' (+ 11 clones) —
        // lido com UnityPy (tipetree gerado da `Assembly-CSharp`) e conferido byte a byte. A
        // referencia visual `image_e488a3.png` (a fileira nativa) e EXATAMENTE o que o prefab diz:
        //   aba      RectTransform 64x64, anchorMin/Max (0,0), pivot (0.5,0.5), localScale 1
        //   icone    ('Icon')  56x56, escala 1, ap (0,0)
        //   rotulo   ('Text')  37.86x40, escala 0.7, ap (0,-27.1)
        //   holder   'Tabs' = HorizontalLayoutGroup spacing 9.6, childAlignment MiddleCenter,
        //            childControlWidth/Height DESLIGADOS (= o filho conserva o proprio 64x64; o
        //            grupo so posiciona). '+11 abas' => passo 64 + 9.6 = 73.6u.
        private const float LadoDoBotaoDeClasse = 64f;       // ABA nativa (era 74.5 — esticava a aba)
        private const float LadoDoIconeDaClasse = 56f;       // 'Icon' nativo
        private const float EspacamentoDaBarraDeClasses = 9.6f; // spacing do HLG nativo
        private const float LarguraDoRotuloDaClasse = 37.86f;   // 'Text' nativo
        private const float AlturaDoRotuloDaClasse = 40f;
        private const float EscalaDoRotuloDaClasse = 0.7f;
        private const float YDoRotuloDaClasse = -27.1f;
        private const float DeslocamentoDoIconeDaClasse = 4f;  // RSTV-23d: +7 -> +4 (icone -24..+32, dentro do tile; antes estourava 3u no topo)
        private const float TamanhoDaFonteDoRotulo = 15f;      // RSTV-23d: 13 -> 15 (fonte fixa; 13 era o texto mais fragil da tela)
        private const float LarguraDoRotuloManual = 64f;       // RSTV-22: caixa do rotulo no fallback (cabe 'Lightning' em 1 linha)
        private const float AlturaDoRotuloManual = 16f;        // RSTV-23d: 14 -> 16 (acompanha a fonte 15)
        private const float YDoRotuloManual = -29f;            // RSTV-23d: -26.5 -> -29 (respiro ~3u do icone e ~8.6u da base)

        // Padroes do prefab (SkillTreeManager.nodeHorizontalPadding/tierVerticalPadding, l.177207-177209).
        private const float PaddingHorizontalPadrao = 47f;
        private const float PaddingVerticalPadrao = 35f;

        // ---------------------------------------------------------------------------------------
        // RSTV-18 — A ESCALA x1.7 DO CONTAINER NATIVO ('Skill Item Container')
        // ---------------------------------------------------------------------------------------
        // MEDIDO no prefab (level1, 'Skill Tree Window Roguelike' > 'Skill Item Container',
        // path_id 490738): RectTransform 1000x800 ancorado no CENTRO, anchoredPosition (0, 26.7) e
        // localScale (1.7, 1.7, 1.7). Os NOS nascem DENTRO dele: 'Skill Tree Item Active' com
        // RectTransform 30x30 e localScale 0.9 -> 30 x 0.9 x 1.7 = 45.9u efetivo (os ~78px da
        // referencia em tela). Sem o container o mod desenhava 30 x 0.9 x 1.0 = 27u (46px) — a razao
        // x1.70 que o dono viu lado a lado. O PITCH tambem escala junto: horizontal 47 x 1.7 = 79.9u
        // e vertical 33 x 1.7 = 56.1u (47/33 sao lidos do `SkillTreeManager` em runtime, l.177207).
        // O container e SO um frame de escala: os nos ficam como filhos com o mesmo anchoredPosition
        // de `PopulateTree`, e as linhas de dependencia continuam no IRMAO sem escala (`_areaDaArvore`).
        private const float EscalaDoContainerDeNos = 1.7f;
        private const float LarguraDoContainerDeNos = 1000f;    // RectTransform do 'Skill Item Container'
        private const float AlturaDoContainerDeNos = 800f;
        private const float YDoContainerDeNos = 26.7f;          // anchoredPosition do container nativo
        private const float LadoDoNoDoPrefab = 30f;             // 'Skill Tree Item Active' (30x30)
        private const float EscalaDoNoDoPrefab = 0.9f;          // localScale do no no prefab

        private static CharacterMenusManager _menu;
        private static MenuTabManager _mgr;
        private static MenuTab _aba;
        private static TextMeshProUGUI _rotuloAba;
        private static GameObject _painel;
        private static RectTransform _areaDaArvore;
        private static RectTransform _containerDeNos;
        private static GameObject _barraDeClasses;

        private static SkillType _tipoAtual = SkillType.Fire;
        private static SkillType _construidoPara = (SkillType)(-1);
        private static readonly List<SkillTreeItem> _itens = new List<SkillTreeItem>();
        private static readonly List<SkillTreeTab> _botoesDeClasse = new List<SkillTreeTab>();

        /// <summary>RSTV-22: um botao de classe montado a MAO (fallback sem SkillTreeTab nativo), com o
        /// highlight de selecao — o <see cref="MarcarClasse"/> alterna os DOIS caminhos.</summary>
        private sealed class BotaoManualDeClasse
        {
            internal SkillType Tipo;
            internal Image Highlight;
        }

        private static readonly List<BotaoManualDeClasse> _botoesManuais = new List<BotaoManualDeClasse>();

        private static bool _barraConstruida;

        /// <summary>RSTV-21: o painel esta hospedado na JANELA propria (<see cref="SkillTreesWindow"/>)
        /// em vez da aba do inventario. O painel e unico; trocar de modo DESMONTA e remonta sob o outro
        /// host (ver <see cref="AbrirJanela"/>/<see cref="SairDoModoJanela"/>).</summary>
        private static bool _modoJanela;

        private static bool _pedido;
        private static float _pedidoEm;
        private static ReadOnlyContext _contextoPendente = ReadOnlyContext.Inventario;
        private static string _ultimoAviso;

        /// <summary>
        /// RSTV-20: o personagem pedido EXPLICITAMENTE pelo interlocutor que abriu a visualizacao
        /// (hoje: o modal "Remove Skill Trees"). Consumido UMA vez por `IniciarSessaoReadOnly`; o
        /// clique manual na aba continua resolvendo pelo `RunTargets`.
        /// </summary>
        private static Character _alvoDoPedido;

        private static Vector2? _underlineOriginal;
        private static bool _underlineAjustado;

        /// <summary>A aba esta mostrando o conteudo AGORA? O <c>SkillTreeItemTogglePatch</c> le isto.</summary>
        internal static bool Aberto
        {
            get { return _painel != null && _painel.activeSelf; }
        }

        // ---------------------------------------------------------------------------------------
        // 1) A INJECAO DA ABA (idempotente por nome)
        // ---------------------------------------------------------------------------------------

        internal static void Ensure(CharacterMenusManager menu)
        {
            try
            {
                if (menu == null)
                {
                    Aviso("CharacterMenusManager nulo — impossivel injetar a aba");
                    return;
                }

                _menu = menu;

                MenuTabManager mgr = menu.GetComponentInChildren<MenuTabManager>(true);
                if (mgr == null)
                {
                    Aviso("MenuTabManager nao encontrado dentro do CharacterMenusManager (a barra de abas mudou?)");
                    return;
                }

                _mgr = mgr;

                MenuTab existente = Procurar(mgr);
                if (existente != null)
                {
                    _aba = existente;
                    _rotuloAba = existente.GetComponentInChildren<TextMeshProUGUI>(true);
                    // RSTV-17: a injecao e idempotente, mas a LARGURA das abas nativas so existe
                    // depois do 1o layout — repetir aqui (barato, so reescreve o LayoutElement) faz a
                    // trava valer quando a medida finalmente esta disponivel, sem criar 2a aba.
                    FixarLarguraDaAba(existente.gameObject, mgr);
                    return;
                }

                if (menu.TabSkillTree == null)
                {
                    Aviso("menu.TabSkillTree nulo — sem o molde nativo nao ha como clonar a aba");
                    return;
                }

                Transform pai = menu.TabSkillTree.transform.parent;
                GameObject clone = UnityEngine.Object.Instantiate(menu.TabSkillTree.gameObject, pai);
                clone.name = TabName;
                clone.SetActive(true);
                clone.transform.SetAsLastSibling();

                SelectPartyButton.DisableLocalizers(clone);

                TextMeshProUGUI rotulo = clone.GetComponentInChildren<TextMeshProUGUI>(true);
                if (rotulo != null)
                {
                    rotulo.text = OptionsManager.Localize(TabLabel);
                    _rotuloAba = rotulo;
                }
                else
                {
                    Aviso("o clone da aba ficou SEM TextMeshProUGUI — a aba aparece sem rotulo");
                }

                // RSTV-17: o grupo de abas do header e CENTRADO e cada aba tem a largura do proprio
                // rotulo — a aba nova, se ficar mais larga que as nativas, re-centraliza o grupo.
                // Aqui ela trava na largura da MAIOR aba nativa (lida das 3 abas do jogo).
                FixarLarguraDaAba(clone, mgr);

                MenuTab nova = clone.GetComponent<MenuTab>();
                if (nova == null)
                {
                    Aviso("o clone da aba ficou SEM o componente MenuTab (o proprio jogo o reinicializa no Update da barra?)");
                }

                Button botao = clone.GetComponent<Button>();
                if (botao != null)
                {
                    // RSTV-12: trocar a INSTANCIA do evento descarta os listeners PERSISTENTES
                    // (serializados no prefab) que o `RemoveAllListeners()` nao remove.
                    SelectPartyButton.ClearClickListeners(botao);
                    botao.onClick.AddListener(new UnityAction(SelecionarEMostrar));
                }
                else
                {
                    Aviso("o clone da aba ficou SEM Button — a aba nao seria clicavel");
                }

                // PONTO 8: a aba TEM de entrar no array publico. `GetNextActiveTab` (l.140700) usa
                // `Array.IndexOf(MenuTabs, ...)`; fora dele o jogo loga "Tabbing broke". Aqui NAO se
                // chama `Initialize()` (dispararia `SelectFirstActiveButton`).
                MenuTab[] antigo = mgr.MenuTabs;
                if (antigo == null)
                {
                    antigo = new MenuTab[0];
                }

                MenuTab[] novo = new MenuTab[antigo.Length + 1];
                Array.Copy(antigo, novo, antigo.Length);
                novo[antigo.Length] = nova;
                mgr.MenuTabs = novo;
                _aba = nova;

                Plugin.Log.LogInfo("RSTV-16: aba '" + TabLabel + "' injetada na barra '" + (pai != null ? pai.name : "?") +
                                   "' (clone de '" + menu.TabSkillTree.gameObject.name + "'); abas agora: " + novo.Length +
                                   "; rotulo=" + (rotulo != null ? rotulo.text : "(sem TMP)") +
                                   "; onClick limpo -> SkillTreesTab.SelecionarEMostrar; MenuTabs inclui a aba.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-16: falha ao injetar a aba '" + TabLabel + "': " + e);
            }
        }

        private static MenuTab Procurar(MenuTabManager mgr)
        {
            if (mgr == null)
            {
                return null;
            }

            MenuTab[] abas = mgr.MenuTabs;
            if (abas != null)
            {
                for (int i = 0; i < abas.Length; i++)
                {
                    MenuTab t = abas[i];
                    if (t != null && t.gameObject != null && t.gameObject.name == TabName)
                    {
                        return t;
                    }
                }
            }

            Transform filho = mgr.transform.Find(TabName);
            if (filho != null)
            {
                return filho.GetComponent<MenuTab>();
            }

            return null;
        }

        /// <summary>
        /// RSTV-17 — trava a largura da aba nova na largura da MAIOR aba NATIVA.
        /// <para>
        /// O HLG do header ('Menu Tab Manager') tem <c>childAlignment = MiddleCenter</c> e
        /// <c>childControlWidth = true</c>: cada aba mede o proprio rotulo e o grupo e centrado.
        /// Como as abas nativas medem 97.82 / 87.12 / 83.67 (unidades do prefab), um rotulo mais
        /// largo empurra as 3 para a esquerda. Um <c>LayoutElement</c> (prioridade 1, acima do
        /// TMP) fixa a largura da aba nova na maior nativa — assim o grupo fica tao equilibrado
        /// quanto as 3 abas do jogo. Se as nativas ainda nao tiverem sido medidas (largura 0),
        /// NADA e fixado (o comportamento nativo fica intacto).
        /// </para>
        /// </summary>
        private static void FixarLarguraDaAba(GameObject clone, MenuTabManager mgr)
        {
            try
            {
                float largura = LarguraDaAbaNativa(mgr, clone);
                if (largura <= 1f)
                {
                    return;
                }

                LayoutElement le = clone.GetComponent<LayoutElement>();
                if (le == null)
                {
                    le = clone.AddComponent<LayoutElement>();
                }

                le.preferredWidth = largura;
                le.minWidth = 0f;
                le.flexibleWidth = 0f;

                Plugin.Log.LogInfo("RSTV-17: largura da aba '" + TabLabel + "' travada em " +
                                   largura.ToString("0.##") + "u (a maior aba nativa) para o grupo centrado nao desequilibrar.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-17: nao deu para fixar a largura da aba: " + e.Message);
            }
        }

        /// <summary>
        /// A largura da aba nativa mais larga das <c>MenuTabs</c> do header (o <c>preferredWidth</c>
        /// do TMP de cada aba — que e exatamente o que o HLG com <c>childControlWidth</c> usa).
        /// Fallback: a largura ja resolvida do RectTransform. A aba nova e excluida da conta.
        /// </summary>
        private static float LarguraDaAbaNativa(MenuTabManager mgr, GameObject nova)
        {
            float maior = 0f;
            MenuTab[] abas = mgr != null ? mgr.MenuTabs : null;
            if (abas != null)
            {
                for (int i = 0; i < abas.Length; i++)
                {
                    MenuTab aba = abas[i];
                    if (aba == null || aba.gameObject == null || aba.gameObject == nova)
                    {
                        continue;
                    }

                    float largura = 0f;
                    TextMeshProUGUI tmp = aba.GetComponentInChildren<TextMeshProUGUI>(true);
                    if (tmp != null)
                    {
                        largura = tmp.preferredWidth;
                    }

                    if (largura <= 1f)
                    {
                        RectTransform rt = aba.transform as RectTransform;
                        if (rt != null)
                        {
                            largura = rt.rect.width;
                        }
                    }

                    if (largura > maior)
                    {
                        maior = largura;
                    }
                }
            }

            return maior;
        }

        // ---------------------------------------------------------------------------------------
        // 2) ABRIR A ABA (o clique, e o caminho do botao/atalho)
        // ---------------------------------------------------------------------------------------

        /// <summary>
        /// Caminho do botao do HUD / atalho F10 / botao do level-up — o corpo de abertura pelo
        /// INVENTARIO: o DESTINO e este <c>Abrir</c>, chamado por <c>RunButton.OpenForTarget</c> (que
        /// ja passou pelo <c>RunTargets.GateOk</c> e resolveu o alvo). A abertura da visao read-only
        /// tem DOIS corpos: alem deste (inventario), o modal "Remove Skill Trees" —
        /// <c>RemovalWindowSkillsButton.OnClick</c> -&gt; <see cref="AbrirJanela"/> — NAO passa por
        /// <c>RunButton</c> nem por <c>RunTargets</c> (usa o alvo do proprio modal).
        /// PONTO 8: abre o inventario PRIMEIRO (<c>OpenCharacterMenu</c>) e seleciona a aba depois
        /// (<c>SelectButtonAndInvoke</c> troca o CONTEUDO, l.140765). Se o menu ja esta aberto, a
        /// selecao e imediata.
        /// </summary>
        internal static void Abrir(Character alvo, ReadOnlyContext contexto)
        {
            try
            {
                CharacterMenusManager menu = CharacterMenusManager.Instance;
                if (menu == null)
                {
                    Plugin.Log.LogError("RSTV-16: CharacterMenusManager.Instance ausente — sem o menu nao ha aba; nada foi aberto.");
                    return;
                }

                RstvHost.Ensure();

                // RSTV-21: se a JANELA read-only propria estava aberta, este caminho assume a visao —
                // desmonta o painel dela (o host muda) antes de seguir para a aba do inventario.
                SairDoModoJanela();

                // PONTO 1: a sessao read-only (que barra o clique — a `SkillTreeManager` e
                // pre-carregada, `Instance` NAO e nulo) nasce JUNTO com a aba: e o `SelecionarEMostrar`
                // (o onClick, disparado pelo `SelectButtonAndInvoke`) quem chama
                // `IniciarSessaoReadOnly`. Guardar o contexto aqui deixa o log fiel.
                _contextoPendente = contexto;
                // RSTV-20: guarda o ALVO do pedido. O clique nao conhece o personagem (l.1443 do
                // doc: "quem da a vida a sessao e a aba") e o `IniciarSessaoReadOnly` resolveria pelo
                // `RunTargets` — para o modal "Remove Skill Trees" isso poderia ser OUTRO personagem.
                // O alvo do pedido e consumido UMA vez na abertura da sessao.
                _alvoDoPedido = alvo;
                Ensure(menu);

                if (_mgr == null || _aba == null)
                {
                    Plugin.Log.LogWarning("RSTV-16: a aba nao esta na barra — o inventario sera aberto, mas a aba '" +
                                          TabLabel + "' nao existe nesta sessao.");
                }

                if (menu.gameObject.activeSelf)
                {
                    Plugar();
                    return;
                }

                _pedido = true;
                _pedidoEm = Time.realtimeSinceStartup;
                Plugin.Log.LogInfo("RSTV-16: abrindo o inventario (CharacterMenusManager.OpenCharacterMenu) para " +
                                   "selecionar a aba '" + TabLabel + "' (alvo=" + (alvo != null ? alvo.CharacterName : "nenhum") + ").");
                menu.OpenCharacterMenu();
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-16: falha ao abrir a aba '" + TabLabel + "': " + e);
            }
        }

        private static void Plugar()
        {
            if (_mgr == null || _aba == null)
            {
                _pedido = false;
                return;
            }

            _pedido = false;
            _mgr.SelectButtonAndInvoke(_aba);
        }

        // ---------------------------------------------------------------------------------------
        // RSTV-21 — A JANELA PROPRIA (read-only sem o inventario)
        // ---------------------------------------------------------------------------------------

        /// <summary>
        /// Abre a visao read-only numa JANELA PROPRIA (<see cref="SkillTreesWindow"/>) — para os pontos
        /// de entrada que NAO tem o inventario disponivel, como o botao 'Skills' do modal "Remove Skill
        /// Trees" na tela de Party Select (ali o <c>OpenCharacterMenu</c> NAO abre: o personagem nao
        /// esta em <c>AllMyCharacters</c>).
        ///
        /// O CONTEUDO e o MESMO da aba (as funcoes de montagem sao as mesmas) — muda so o HOSPEDEIRO
        /// do painel. O alvo e o contexto do pedido seguem o mesmo contrato dos outros pontos de
        /// entrada: o personagem do modal entra como <c>_alvoDoPedido</c> e e consumido UMA vez por
        /// <c>IniciarSessaoReadOnly</c>.
        /// </summary>
        /// <param name="dono">A janela do jogo que PEDE a visao (dela saem os moldes nativos e o ciclo
        /// de vida: quando o dono sai de cena, a janela se fecha sozinha).</param>
        internal static void AbrirJanela(Character alvo, ReadOnlyContext contexto, Transform dono)
        {
            try
            {
                RstvHost.Ensure();

                // RSTV-21R: a janela avisa quando FECHA (o botao fechar ou o dono fora de cena, via
                // `Atualizar`); aqui largamos o modo janela nesse aviso, para `_modoJanela` nunca ficar
                // pendurado depois do fechamento. A ATRIBUICAO (e nao `+=`) mantem um unico handler.
                SkillTreesWindow.Fechou = AoFecharJanela;

                _contextoPendente = contexto;
                _alvoDoPedido = alvo;

                RectTransform area = SkillTreesWindow.Garantir(dono);
                if (area == null)
                {
                    Plugin.Log.LogError("RSTV-21: nao foi possivel criar a janela read-only — nada foi aberto.");
                    return;
                }

                // Troca de host: um painel que estava sob o inventario nao serve na janela (ancoras e
                // pai diferentes) — desmonta antes; ConstruirPainel o recria sob a area da janela.
                if (!_modoJanela)
                {
                    DestruirPainel();
                }

                _modoJanela = true;

                IniciarSessaoReadOnly();
                Mostrar();

                Plugin.Log.LogInfo("RSTV-21: janela read-only ABERTA com TODAS as arvores (alvo=" +
                                   (alvo != null ? alvo.CharacterName : "nenhum") + ", contexto=" + contexto +
                                   ") — sem depender do inventario.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-21: falha ao abrir a janela read-only: " + e);
            }
        }

        /// <summary>
        /// Sai do modo JANELA (se ativo): fecha a janela e desmonta o painel. Chamado quando outro
        /// ponto de entrada assume a visao (a aba do inventario) — o painel e unico e o host muda.
        /// </summary>
        private static void SairDoModoJanela()
        {
            if (!_modoJanela)
            {
                return;
            }

            _modoJanela = false;
            SkillTreesWindow.Fechar();
            DestruirPainel();
        }

        /// <summary>
        /// RSTV-21R — larga o MODO JANELA quando a janela FECHA por qualquer caminho: o botao fechar
        /// (que chama <see cref="SkillTreesWindow.Fechar"/> direto) ou o <see cref="SkillTreesWindow.Atualizar"/>
        /// (quando o DONO sai de cena). Inscrito em <see cref="SkillTreesWindow.Fechou"/> pela
        /// <see cref="AbrirJanela"/>: sem isto o flag <c>_modoJanela</c> ficava pendurado <c>true</c> depois
        /// do fechamento, ate um ponto de entrada chamar <see cref="SairDoModoJanela"/>. A guarda por
        /// <c>_modoJanela</c> evita reentrada quando o fechamento veio do proprio
        /// <see cref="SairDoModoJanela"/> (que ja largou o modo e o painel).
        /// </summary>
        private static void AoFecharJanela()
        {
            if (!_modoJanela)
            {
                return;
            }

            _modoJanela = false;
            DestruirPainel();

            if (ReadOnlySession.Active)
            {
                ReadOnlySession.End();
                Plugin.Log.LogInfo("RSTV-21: a janela read-only fechou — modo janela largado e a sessao read-only encerrada.");
            }
        }

        /// <summary>
        /// Desmonta o painel e todo o estado de renderizacao que aponta para ele (ele sera recriado
        /// sob o outro host). Sem isto, a troca de host deixaria o painel preso na hierarquia errada.
        /// </summary>
        private static void DestruirPainel()
        {
            try
            {
                LimparItens();
                AjustarUnderline(false);

                if (_painel != null)
                {
                    UnityEngine.Object.Destroy(_painel);
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: falha ao desmontar o painel das arvores: " + e.Message);
            }

            _painel = null;
            _areaDaArvore = null;
            _containerDeNos = null;
            _barraDeClasses = null;
            _barraConstruida = false;
            _botoesDeClasse.Clear();
            _botoesManuais.Clear();
        }

        /// <summary>
        /// O onClick da NOSSA aba (clique do jogador). PONTO 8: marca a aba com <c>SelectButton</c> (so
        /// realca — nao re-invoca o onClick), encerra os conteudos nativos abertos e mostra o painel.
        /// </summary>
        internal static void SelecionarEMostrar()
        {
            try
            {
                RstvHost.Ensure();

                // RSTV-21: se a JANELA read-only propria estava aberta, este clique assume a visao.
                SairDoModoJanela();

                IniciarSessaoReadOnly();

                if (_mgr != null && _aba != null)
                {
                    _mgr.SelectButton(_aba);
                }

                FecharConteudosNativos();
                Mostrar();
                AjustarUnderline(true);

                Plugin.Log.LogInfo("RSTV-16: aba '" + TabLabel + "' selecionada — arvores read-only visiveis " +
                                   "(classe=" + _tipoAtual + ").");
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-16: falha ao tratar o clique da aba '" + TabLabel + "': " + e);
            }
        }

        /// <summary>PONTO 1: o read-only nao depende de guarda de null — depende da sessao ativa.</summary>
        private static void IniciarSessaoReadOnly()
        {
            if (ReadOnlySession.Active)
            {
                return;
            }

            Character alvo = null;
            string motivo = null;

            // RSTV-20: quem ABRIU a visualizacao pode ter um alvo EXPLICITO (o personagem do modal
            // "Remove Skill Trees", que nao e necessariamente o `CurrentlySelectedCharacter`). O
            // pedido e consumido UMA vez, aqui — o clique manual na aba (SelecionarEMostrar) segue
            // caindo no `RunTargets.Resolve` de sempre.
            Character pedido = _alvoDoPedido;
            _alvoDoPedido = null;

            if (pedido != null)
            {
                alvo = pedido;
                motivo = "alvo explicito do pedido (" + pedido.CharacterName + ")";
            }
            else
            {
                try
                {
                    alvo = RunTargets.Resolve(out motivo);
                }
                catch (Exception e)
                {
                    motivo = e.GetType().Name + ": " + e.Message;
                }
            }

            if (alvo == null)
            {
                Plugin.Log.LogInfo("RSTV-16: nenhum personagem local resolvido para o contexto (" + motivo +
                                   ") — a aba mostra TODAS as arvores; o bloqueio de clique segue ativo pela sessao.");
            }

            ReadOnlySession.Begin(alvo, _contextoPendente);
        }

        private static void FecharConteudosNativos()
        {
            CharacterMenusManager menu = _menu != null ? _menu : CharacterMenusManager.Instance;
            if (menu == null)
            {
                return;
            }

            menu.CloseCharacterMenu();
            menu.CloseSkillTreeMenu();
            menu.CloseFortuneMenu();
        }

        // ---------------------------------------------------------------------------------------
        // 3) O CICLO DE VIDA — a vida agora e a do SISTEMA DE ABAS
        // ---------------------------------------------------------------------------------------

        internal static void Tick()
        {
            try
            {
                // RSTV-21: a janela propria se fecha quando o DONO sai de cena (o jogador fechou o
                // modal) — a raiz dela e DontDestroyOnLoad e nao pode ficar pendurada na proxima tela.
                SkillTreesWindow.Atualizar();

                if (_pedido)
                {
                    CharacterMenusManager menu = _menu != null ? _menu : CharacterMenusManager.Instance;
                    if (menu != null && menu.gameObject.activeInHierarchy)
                    {
                        Plugar();
                    }
                    else if (Time.realtimeSinceStartup - _pedidoEm > 5f)
                    {
                        // A abertura e do jogo e pode ser recusada EM SILENCIO (o `OpenCharacterMenu`
                        // desiste quando o personagem nao esta em `AllMyCharacters`). Sem este teto, o
                        // pedido ficaria pendente para sempre.
                        _pedido = false;
                        Plugin.Log.LogWarning("RSTV-16: o inventario nao abriu em 5 s (CharacterMenusManager " +
                                              "seguiu inativo) — o pedido da aba '" + TabLabel + "' foi descartado.");
                    }
                }

                if (_painel == null)
                {
                    return;
                }

                bool devia = DeviaEstarVisivel();
                if (_painel.activeSelf == devia)
                {
                    if (devia && _construidoPara != _tipoAtual)
                    {
                        Popular(_tipoAtual);
                    }

                    return;
                }

                _painel.SetActive(devia);

                if (devia)
                {
                    AjustarUnderline(true);
                    if (_construidoPara != _tipoAtual)
                    {
                        Popular(_tipoAtual);
                    }

                    return;
                }

                AjustarUnderline(false);

                if (ReadOnlySession.Active)
                {
                    ReadOnlySession.End();
                    Plugin.Log.LogInfo(_modoJanela
                        ? "RSTV-21: a janela read-only deixou de estar aberta — sessao read-only encerrada."
                        : "RSTV-16: a aba '" + TabLabel + "' deixou de ser a selecionada — " +
                          "sessao read-only encerrada.");
                }
            }
            catch (Exception e)
            {
                if (_ultimoAviso == "tick")
                {
                    return;
                }

                _ultimoAviso = "tick";
                Plugin.Log.LogError("RSTV-16: falha no Tick da aba: " + e);
            }
        }

        private static bool DeviaEstarVisivel()
        {
            // RSTV-21: no modo JANELA quem decide e a propria janela (e o dono dela) — nao ha aba.
            if (_modoJanela)
            {
                return SkillTreesWindow.Aberta;
            }

            if (_aba == null || _mgr == null)
            {
                return false;
            }

            CharacterMenusManager menu = _menu != null ? _menu : CharacterMenusManager.Instance;
            if (menu == null || !menu.gameObject.activeInHierarchy)
            {
                return false;
            }

            return _mgr.SelectedMenuTab == _aba;
        }

        /// <summary>
        /// PONTO 5: a `Underline` das abas tem largura fixa (~74.5) e o nosso rotulo e mais largo. Ao
        /// entrar, a largura vira a do rotulo (`preferredWidth`) e ao sair e RESTAURADA ao valor
        /// original (guardado na primeira vez).
        /// </summary>
        private static void AjustarUnderline(bool ligado)
        {
            try
            {
                // RSTV-21: na janela propria nao existe a barra de abas do inventario — a Underline
                // nao e mexida (nem no abrir, nem no fechar).
                if (_modoJanela)
                {
                    return;
                }

                if (_mgr == null || _mgr.Underline == null)
                {
                    return;
                }

                if (ligado)
                {
                    if (!_underlineOriginal.HasValue)
                    {
                        _underlineOriginal = _mgr.Underline.sizeDelta;
                    }

                    float largura = LarguraDoRotulo();
                    _mgr.Underline.sizeDelta = new Vector2(largura, _underlineOriginal.Value.y);
                    _underlineAjustado = true;
                    return;
                }

                if (_underlineAjustado && _underlineOriginal.HasValue)
                {
                    _mgr.Underline.sizeDelta = _underlineOriginal.Value;
                    _underlineAjustado = false;
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-16: nao deu para ajustar a Underline das abas: " + e.Message);
            }
        }

        private static float LarguraDoRotulo()
        {
            try
            {
                if (_rotuloAba != null)
                {
                    float w = _rotuloAba.preferredWidth;
                    if (w > 1f)
                    {
                        return w;
                    }

                    Vector2 pref = _rotuloAba.GetPreferredValues(_rotuloAba.text);
                    if (pref.x > 1f)
                    {
                        return pref.x;
                    }
                }
            }
            catch (Exception)
            {
                // cai no fallback
            }

            return 130f;
        }

        // ---------------------------------------------------------------------------------------
        // 4) O CONTEUDO — as arvores montadas na mao
        // ---------------------------------------------------------------------------------------

        private static void Mostrar()
        {
            if (_painel == null)
            {
                ConstruirPainel();
            }

            if (_painel == null)
            {
                return;
            }

            _painel.SetActive(true);

            if (!_barraConstruida)
            {
                ConstruirBarraDeClasses();
            }

            if (_construidoPara != _tipoAtual)
            {
                Popular(_tipoAtual);
            }
        }

        /// <summary>
        /// A LISTA DE CLASSES — espelho de <c>RefreshAvailableSkillTrees</c> (l.170100-170118): percorre
        /// <c>MiscSettings.SkillTabTypes</c> (l.141356) e exige, por tipo, (a) nao ser
        /// <c>Basic</c>/<c>Innate</c> (nao sao arvores, l.170113), (b) <c>MeetsDLCRequirements(type)</c>,
        /// (c) existir skill com <c>!Disabled &amp;&amp; !DontIncludeInTree &amp;&amp;
        /// FullReleaseModeEnabled(skill)</c>. O BARD e pulado por decisao do dono (nao esta no jogo) —
        /// e, mesmo que estivesse, o predicado (c) o excluiria.
        /// </summary>
        internal static List<SkillType> TiposDaAba()
        {
            List<SkillType> tipos = new List<SkillType>();
            try
            {
                GlobalSettingsManager gsm = GlobalSettingsManager.instance;
                SteamManager steam = SteamManager.instance;
                Burst2Flame.Game jogo = Burst2Flame.Game.Instance;

                if (gsm == null || gsm.miscSettings == null || gsm.miscSettings.SkillTabTypes == null ||
                    steam == null || jogo == null || jogo.Skills == null)
                {
                    Aviso("GlobalSettingsManager/SteamManager/Game.Skills indisponivel — sem isso nao ha classes para montar");
                    return tipos;
                }

                List<SkillType> todos = gsm.miscSettings.SkillTabTypes;
                for (int i = 0; i < todos.Count; i++)
                {
                    SkillType tipo = todos[i];
                    if (tipo == SkillType.Bard)
                    {
                        continue;
                    }

                    if (tipo == SkillType.Basic || tipo == SkillType.Innate)
                    {
                        continue;
                    }

                    if (!steam.MeetsDLCRequirements(tipo))
                    {
                        continue;
                    }

                    if (!TemSkillsVisiveis(tipo))
                    {
                        continue;
                    }

                    if (!tipos.Contains(tipo))
                    {
                        tipos.Add(tipo);
                    }
                }
            }
            catch (Exception e)
            {
                Aviso("nao deu para montar a lista de classes: " + e.Message);
            }

            return tipos;
        }

        /// <summary>O predicado (c) de `RefreshAvailableSkillTrees` (l.170113), por tipo.</summary>
        private static bool TemSkillsVisiveis(SkillType tipo)
        {
            try
            {
                Burst2Flame.Game jogo = Burst2Flame.Game.Instance;
                if (jogo == null || jogo.Skills == null)
                {
                    return false;
                }

                List<SkillInfo> todos = jogo.Skills;
                for (int i = 0; i < todos.Count; i++)
                {
                    SkillInfo s = todos[i];
                    if (s != null && s.SkillType == tipo && !s.Disabled && !s.DontIncludeInTree &&
                        jogo.FullReleaseModeEnabled(s))
                    {
                        return true;
                    }
                }
            }
            catch (Exception)
            {
                // na duvida, nao lista a classe
            }

            return false;
        }

        private static void ConstruirPainel()
        {
            // RSTV-21: no modo JANELA o painel nasce sob a area da janela propria (ancoras esticadas),
            // nao sob o menu do inventario.
            if (_modoJanela)
            {
                ConstruirPainelNaJanela();
                return;
            }

            CharacterMenusManager menu = _menu != null ? _menu : CharacterMenusManager.Instance;
            if (menu == null)
            {
                return;
            }

            RectTransform menuRt = menu.transform as RectTransform;
            MenuTabManager mgr = _mgr != null ? _mgr : menu.GetComponentInChildren<MenuTabManager>(true);
            if (menuRt == null || mgr == null)
            {
                Aviso("sem RectTransform do menu ou sem MenuTabManager — nao da para posicionar o painel");
                return;
            }

            Transform existente = menu.transform.Find(PanelName);
            if (existente != null)
            {
                _painel = existente.gameObject;
                AtarPecasDoPainel(existente);
                _painel.transform.SetAsLastSibling();
                return;
            }

            GameObject painel = new GameObject(PanelName, typeof(RectTransform));
            RectTransform rt = painel.GetComponent<RectTransform>();
            rt.SetParent(menu.transform, false);
            rt.SetAsLastSibling();
            _painel = painel;

            PainelAbaixoDaBarra(rt, menuRt, mgr.transform as RectTransform);

            ConstruirFilhosDoPainel(rt);
            painel.SetActive(false);

            Plugin.Log.LogInfo("RSTV-16: painel da aba criado sob '" + menu.transform.name + "' — topo abaixo da barra de " +
                               "abas, area da arvore " + _areaDaArvore.rect.width.ToString("0.#") + "x" + _areaDaArvore.rect.height.ToString("0.#") + " px.");
        }

        /// <summary>
        /// RSTV-21: monta o painel DENTRO da janela propria (<see cref="SkillTreesWindow"/>), esticado
        /// na area de conteudo que ela reserva (abaixo do cabecalho). O CONTEUDO e o MESMO da aba —
        /// quem muda e so o hospedeiro (ver <see cref="ConstruirFilhosDoPainel"/>).
        /// </summary>
        private static void ConstruirPainelNaJanela()
        {
            RectTransform area = SkillTreesWindow.Conteudo;
            if (area == null)
            {
                Aviso("a janela read-only nao tem area de conteudo — o painel nao pode ser montado");
                return;
            }

            Transform existente = area.Find(PanelName);
            if (existente != null)
            {
                _painel = existente.gameObject;
                AtarPecasDoPainel(existente);
                _painel.transform.SetAsLastSibling();
                return;
            }

            GameObject painel = new GameObject(PanelName, typeof(RectTransform));
            RectTransform rt = painel.GetComponent<RectTransform>();
            rt.SetParent(area, false);
            rt.SetAsLastSibling();
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            // RSTV-23b: margem no painel do modo JANELA (a aba ja tem via `PainelAbaixoDaBarra`). Sem
            // ela o painel preenchia a area inteira e a ultima fileira da arvore encostava na borda
            // inferior da moldura (margem 0). 8u nas laterais/baixo = respiro de ~10px.
            rt.offsetMin = new Vector2(8f, 8f);
            rt.offsetMax = new Vector2(-8f, 0f);
            rt.localScale = Vector3.one;
            rt.localRotation = Quaternion.identity;
            _painel = painel;

            ConstruirFilhosDoPainel(rt);
            painel.SetActive(false);

            Plugin.Log.LogInfo("RSTV-21: painel da janela read-only criado sob '" + area.name + "' — area da arvore " +
                               _areaDaArvore.rect.width.ToString("0.#") + "x" + _areaDaArvore.rect.height.ToString("0.#") +
                               " px (host proprio, SEM o inventario).");
        }

        /// <summary>Reata as referencias de um painel que JA existe (idempotencia por NOME).</summary>
        private static void AtarPecasDoPainel(Transform painel)
        {
            _areaDaArvore = painel.Find(TreeAreaName) as RectTransform;
            _containerDeNos = GarantirContainerDeNos(_areaDaArvore);
            Transform barra = painel.Find(ClassBarName);
            _barraDeClasses = barra != null ? barra.gameObject : null;
            _barraConstruida = barra != null && barra.childCount > 0;
        }

        /// <summary>
        /// RSTV-21: os FILHOS do painel — a barra de classes no topo, a area da arvore abaixo e o
        /// frame x1.7 dos nos. Extraido de <c>ConstruirPainel</c> para os DOIS hospedeiros (a aba do
        /// inventario e a janela propria) montarem o MESMO conteudo; o posicionamento do painel em si
        /// e responsabilidade de cada host.
        /// </summary>
        private static void ConstruirFilhosDoPainel(RectTransform rt)
        {
            GameObject barra2 = new GameObject(ClassBarName, typeof(RectTransform));
            RectTransform barra2Rt = barra2.GetComponent<RectTransform>();
            barra2Rt.SetParent(rt, false);
            barra2Rt.anchorMin = new Vector2(0f, 1f);
            barra2Rt.anchorMax = new Vector2(1f, 1f);
            barra2Rt.pivot = new Vector2(0.5f, 1f);
            barra2Rt.anchoredPosition = new Vector2(0f, -8f);  // RSTV-23e: -2 -> -8 (afasta a barra do divisor do cabecalho)
            barra2Rt.sizeDelta = new Vector2(0f, AlturaDaBarraDeClasses);

            HorizontalLayoutGroup grupo = barra2.AddComponent<HorizontalLayoutGroup>();
            // RSTV-17: os MESMOS parametros do HLG nativo do 'Tabs' (SkillTreeManager):
            // MiddleCenter, spacing 9.6, childControlWidth/Height DESLIGADOS. Sem os controles
            // ligados, cada botao conserva o proprio RectTransform 64x64 e o grupo so o POSICIONA
            // (era o `childControlWidth=true` + `LayoutElement` 74.5 que esticava a aba).
            grupo.childAlignment = TextAnchor.MiddleCenter;
            grupo.spacing = EspacamentoDaBarraDeClasses;
            grupo.childControlWidth = false;
            grupo.childControlHeight = false;
            grupo.childForceExpandWidth = false;
            grupo.childForceExpandHeight = false;
            grupo.childScaleWidth = false;
            grupo.childScaleHeight = false;
            _barraDeClasses = barra2;

            GameObject area = new GameObject(TreeAreaName, typeof(RectTransform));
            RectTransform areaRt = area.GetComponent<RectTransform>();
            areaRt.SetParent(rt, false);
            areaRt.anchorMin = new Vector2(0f, 0f);
            areaRt.anchorMax = new Vector2(1f, 1f);
            areaRt.pivot = new Vector2(0.5f, 0.5f);
            areaRt.offsetMin = new Vector2(0f, 0f);
            areaRt.offsetMax = new Vector2(0f, -(AlturaDaBarraDeClasses + 4f));
            _areaDaArvore = areaRt;

            // RSTV-18: o frame x1.7 por dentro da area — e ele que da aos nos e ao pitch a escala
            // do 'Skill Item Container' nativo (a area em si fica em escala 1, para as linhas).
            _containerDeNos = GarantirContainerDeNos(areaRt);

            _barraConstruida = false;
        }

        /// <summary>
        /// RSTV-18 — o 'Skill Item Container' NATIVO (level1, 'Skill Tree Window Roguelike' > GO 490738):
        /// um frame CENTRADO com <c>localScale 1.7</c> que envolve os nos da arvore. E ele que faz o no
        /// sair em 30 x 0.9 x 1.7 = 45.9u (em vez de 27u) e o pitch em 47 x 1.7 = 79.9u — o tamanho da
        /// referencia. Reconstruido com os MESMOS numeros do prefab (1000x800, escala 1.7).
        ///
        /// RSTV-19 — a POSICAO (os nos caiam no rodape, cortados pela borda). No NATIVO o container e
        /// filho DIRETO da JANELA do SkillTreeManager, ancorado no CENTRO dela, com
        /// <c>anchoredPosition (0, 26.7)</c>: o centro do container cai 26.7u ACIMA do centro da janela.
        /// Aqui o pai e a <c>RstvTreeArea</c>, cujo centro NAO e o centro da janela — a area comeca
        /// <c>AlturaDaBarraDeClasses + 4</c> abaixo do topo do painel, e o painel comeca abaixo da barra
        /// de abas. Na janela viva (barra 'Menu Tab Manager' [762] = ap 11.2, altura 53.7) o centro da
        /// area fica ~64.25u ABAIXO do centro da janela; copiar o (0, 26.7) CRU para dentro da AREA
        /// jogava os nos 64.25u baixo demais — o tier 5 encostava no rodape e era cortado (bottom do no
        /// a ~4u da borda). Aqui o container sobe esse deslocamento MEDIDO do vivo e volta para a
        /// posicao relativa do nativo (centro da JANELA + YDoContainerDeNos).
        /// IDEMPOTENTE por NOME (a aba reusa o painel entre aberturas).
        /// </summary>
        private static RectTransform GarantirContainerDeNos(RectTransform area)
        {
            if (area == null)
            {
                return null;
            }

            RectTransform container = area.Find(NodeContainerName) as RectTransform;
            if (container == null)
            {
                GameObject go = new GameObject(NodeContainerName, typeof(RectTransform));
                container = go.GetComponent<RectTransform>();
                container.SetParent(area, false);
            }

            container.anchorMin = new Vector2(0.5f, 0.5f);   // igual ao 'Skill Item Container' nativo
            container.anchorMax = new Vector2(0.5f, 0.5f);
            container.pivot = new Vector2(0.5f, 0.5f);
            container.sizeDelta = new Vector2(LarguraDoContainerDeNos, AlturaDoContainerDeNos);
            // RSTV-19: centro do container = centro da JANELA + YDoContainerDeNos (como o nativo) —
            // nao o centro da AREA, que fica ~64.25u mais abaixo (senao os nos caem no rodape).
            container.anchoredPosition = new Vector2(0f, DeslocamentoDoCentroDaArea(area) + YDoContainerDeNos);
            container.localRotation = Quaternion.identity;
            container.localScale = new Vector3(EscalaDoContainerDeNos, EscalaDoContainerDeNos, EscalaDoContainerDeNos);

            // Fica no FUNDO da area: as linhas de dependencia entram como IRMAS (em escala 1) e o
            // `SetSiblingIndex(0)` delas deixa o container por cima, com os nos desenhados na frente.
            container.SetSiblingIndex(0);
            return container;
        }

        /// <summary>
        /// RSTV-19 — o quanto o centro da <c>RstvTreeArea</c> esta ABAIXO do centro da janela do
        /// SkillTreeManager, em unidades locais da propria area (positivo = a janela esta acima). E o
        /// ajuste que devolve ao container a posicao relativa do 'Skill Item Container' nativo
        /// (centro da janela + 26.7). MEDIDO do VIVO (transform inverso), nunca estimado: acompanha a
        /// barra de abas de verdade — a mesma que o <c>PainelAbaixoDaBarra</c> mede para o painel.
        /// Sem a janela (ou sem pai), devolve 0 e o container fica no comportamento anterior.
        /// </summary>
        private static float DeslocamentoDoCentroDaArea(RectTransform area)
        {
            if (area == null)
            {
                return 0f;
            }

            // RSTV-21: no modo JANELA a referencia e o proprio painel (ele preenche a area da janela,
            // entao o container fica no centro do painel, como no nativo); na aba, e a janela do menu.
            RectTransform janela = _modoJanela
                ? (_painel != null ? _painel.transform as RectTransform : null)
                : (_menu != null ? _menu.transform as RectTransform : null);
            if (janela == null && area.parent != null)
            {
                janela = area.parent.parent as RectTransform;   // area -> painel -> janela do menu
            }

            if (janela == null)
            {
                return 0f;
            }

            return area.InverseTransformPoint(janela.position).y;
        }

        private static void PainelAbaixoDaBarra(RectTransform painel, RectTransform janela, RectTransform barra)
        {
            Canvas.ForceUpdateCanvases();

            float topoLocal;
            if (barra != null)
            {
                Vector3[] cantos = new Vector3[4];
                barra.GetWorldCorners(cantos);              // 0=BL, 1=TL, 2=TR, 3=BR
                Vector3 bl = janela.InverseTransformPoint(cantos[0]);
                Vector3 br = janela.InverseTransformPoint(cantos[3]);
                topoLocal = Mathf.Min(bl.y, br.y) - MargemSuperior;
            }
            else
            {
                // Fallback documentado: a barra fica ~197 px abaixo do topo (SkillTreeStyle.StatusTopOffset).
                topoLocal = janela.rect.height * (1f - janela.pivot.y) - 200f - MargemSuperior;
            }

            Vector2 minimo = new Vector2(-janela.rect.width * janela.pivot.x,
                                         -janela.rect.height * janela.pivot.y);

            painel.anchorMin = Vector2.zero;
            painel.anchorMax = Vector2.zero;
            painel.pivot = new Vector2(0f, 1f);
            painel.localScale = Vector3.one;
            painel.localRotation = Quaternion.identity;

            float largura = Mathf.Max(1f, janela.rect.width - 2f * MargemLateral);
            float altura = Mathf.Max(60f, topoLocal - MargemInferior - minimo.y);
            painel.sizeDelta = new Vector2(largura, altura);
            painel.anchoredPosition = new Vector2(MargemLateral, topoLocal - minimo.y);
        }

        /// <summary>
        /// PONTO 7: a fileira de classes reusa os `SkillTreeTab` NATIVOS (icone+nome, l.178841) que o
        /// prefab da `SkillTreeManager` ja tem em <c>tabHolder</c> (l.177223, um filho por entrada de
        /// `SkillTabTypes`). Sem a instancia viva, cai no clone da aba do header.
        /// </summary>
        private static void ConstruirBarraDeClasses()
        {
            CharacterMenusManager menu = _menu != null ? _menu : CharacterMenusManager.Instance;
            if (_barraDeClasses == null)
            {
                Aviso("sem a barra de classes do painel — nao da para montar os botoes de classe");
                return;
            }

            List<SkillType> tipos = TiposDaAba();
            SkillTreeManager nativo = LoadableUIWindow<SkillTreeManager>.Instance;
            Transform tabHolder = nativo != null ? nativo.tabHolder : null;
            List<SkillType> ordemDoAsset = OrdemDoAsset();

            bool viaNativo = tabHolder != null && tabHolder.childCount > 0 && ordemDoAsset != null;
            _botoesDeClasse.Clear();
            _botoesManuais.Clear();

            for (int i = 0; i < tipos.Count; i++)
            {
                SkillType tipo = tipos[i];
                GameObject origem = null;
                int indice = ordemDoAsset != null ? ordemDoAsset.IndexOf(tipo) : -1;

                if (viaNativo && indice >= 0 && indice < tabHolder.childCount)
                {
                    origem = tabHolder.GetChild(indice).gameObject;
                }

                GameObject molde = origem != null
                    ? origem
                    : (menu != null && menu.TabSkillTree != null ? menu.TabSkillTree.gameObject : null);
                if (molde == null)
                {
                    Aviso("sem molde para o botao de classe " + tipo);
                    continue;
                }

                GameObject botao = UnityEngine.Object.Instantiate(molde, _barraDeClasses.transform);
                botao.name = "RstvClassButton_" + tipo;
                botao.SetActive(true);

                SelectPartyButton.DisableLocalizers(botao);

                SkillTreeTab tab = botao.GetComponent<SkillTreeTab>();
                if (tab != null)
                {
                    tab.skillType = tipo;
                    if (tab.treeIcon != null)
                    {
                        tab.treeIcon.sprite = IconeDe(tipo);
                    }

                    if (tab.treeName != null)
                    {
                        tab.treeName.text = OptionsManager.LocalizeEnum(tipo);
                    }

                    // O SkillTreeTab do jogo chama `PopulateTab` -> `SkillTreeManager.ChooseTree`
                    // (l.178958): wiring que NAO queremos (mexeria na arvore nativa). O componente fica
                    // no clone (nao foi `Init`ado, entao o Update dele e inerte), e o dlcLinker (hover
                    // de DLC) some.
                    DisableDlcLinker(tab);
                    _botoesDeClasse.Add(tab);
                }
                else
                {
                    // RSTV-22 (fallback bonito): o molde caiu na aba do header (MenuTab), que NAO tem
                    // icone de classe — ficava uma fileira de abas de menu. O clone e DESCARTADO e o
                    // botao e montado DO ZERO com o icone do asset (TreeIcons) + nome da classe, no
                    // mesmo 64x64 do SkillTreeTab nativo. O clique (TrocarClasse) e instalado logo
                    // abaixo, como no caminho nativo.
                    UnityEngine.Object.Destroy(botao);
                    botao = MontarBotaoDeClasseManual(tipo);
                    if (botao == null)
                    {
                        continue;
                    }
                }

                AplicarDimensionamentoNativo(botao, tab);

                EnsureLayoutElement(botao);

                Button bt = botao.GetComponent<Button>();
                if (bt != null)
                {
                    SelectPartyButton.ClearClickListeners(bt);
                    SkillType capturado = tipo;
                    bt.onClick.AddListener(new UnityAction(delegate { TrocarClasse(capturado); }));
                }
            }

            _barraConstruida = true;
            MarcarClasse(_tipoAtual);

            string nomes = "";
            for (int i = 0; i < tipos.Count; i++)
            {
                nomes += (i > 0 ? ", " : "") + tipos[i];
            }

            Plugin.Log.LogInfo("RSTV-16: barra de classes com " + tipos.Count + " botao(oes) via " +
                               (viaNativo ? "SkillTreeTab NATIVO (icone+nome)" : "botao montado a MAO (icone+nome)") + " — " +
                               nomes + " (Bard FORA; Basic/Innate fora; DLC/FullRelease respeitados).");
        }

        /// <summary>
        /// RSTV-22 — botao de classe montado a MAO (so no fallback, quando nao ha SkillTreeTab nativo
        /// para clonar — a janela propria abre numa cena sem o SkillTreeManager carregado). Um quadrado
        /// 64x64 com o ICONE da classe (asset `TreeIcons`) e o NOME abaixo — o mesmo layout do
        /// SkillTreeTab nativo medido no prefab (icone 56x56, rotulo 37.86x40 em escala 0.7, em
        /// (0,-27.1)). O highlight de selecao fica numa Image filha, alternada pelo
        /// <see cref="MarcarClasse"/>.
        /// </summary>
        private static GameObject MontarBotaoDeClasseManual(SkillType tipo)
        {
            GameObject botao = new GameObject("RstvClassButton_" + tipo, typeof(RectTransform));
            botao.transform.SetParent(_barraDeClasses.transform, false);

            RectTransform rt = botao.GetComponent<RectTransform>();
            rt.anchorMin = new Vector2(0f, 0f);
            rt.anchorMax = new Vector2(0f, 0f);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(LadoDoBotaoDeClasse, LadoDoBotaoDeClasse);
            rt.localScale = Vector3.one;

            // Fundo clicavel (Image + Button) transparente.
            Image fundo = botao.AddComponent<Image>();
            fundo.color = Color.clear;
            Button bt = botao.AddComponent<Button>();
            bt.targetGraphic = fundo;

            // HIGHLIGHT de selecao (claridade leve), desligado por padrao.
            // RSTV-23c: alfa 0.22 -> 0.12 — o platao inteiro de 50% branco derrubava o contraste do
            // rotulo selecionado para ~2.5:1 (WCAG pede 4.5:1). Um brilho sutil mantem a marcacao
            // sem esconder o nome.
            GameObject hl = new GameObject("Highlight", typeof(RectTransform));
            hl.transform.SetParent(botao.transform, false);
            Image hlImg = hl.AddComponent<Image>();
            hlImg.color = new Color(1f, 1f, 1f, 0.12f);
            RectTransform hlRt = hl.GetComponent<RectTransform>();
            hlRt.anchorMin = Vector2.zero;
            hlRt.anchorMax = Vector2.one;
            hlRt.offsetMin = Vector2.zero;
            hlRt.offsetMax = Vector2.zero;
            hl.SetActive(false);

            // ICONE 56x56, centralizado no eixo X e um pouco ACIMA do centro (deixa a faixa de baixo
            // livre para a legenda). preserveAspect=true mantem a proporcao do sprite do TreeIcons.
            GameObject iconeGo = new GameObject("Icon", typeof(RectTransform));
            iconeGo.transform.SetParent(botao.transform, false);
            Image icone = iconeGo.AddComponent<Image>();
            icone.sprite = IconeDe(tipo);
            icone.preserveAspect = true;
            RectTransform iconeRt = iconeGo.GetComponent<RectTransform>();
            iconeRt.anchorMin = new Vector2(0.5f, 0.5f);
            iconeRt.anchorMax = new Vector2(0.5f, 0.5f);
            iconeRt.pivot = new Vector2(0.5f, 0.5f);
            iconeRt.anchoredPosition = new Vector2(0f, DeslocamentoDoIconeDaClasse);
            iconeRt.sizeDelta = new Vector2(LadoDoIconeDaClasse, LadoDoIconeDaClasse);
            iconeRt.localScale = Vector3.one;

            // NOME da classe: LEGENDA abaixo do icone. Sem autoSizing (o texto grande cobria o icone);
            // fonte FIXA pequena + escala 0.7 (mesma do nativo), ancorada na faixa de baixo do botao.
            GameObject nomeGo = new GameObject("Text", typeof(RectTransform));
            nomeGo.transform.SetParent(botao.transform, false);
            TextMeshProUGUI nome = nomeGo.AddComponent<TextMeshProUGUI>();
            nome.font = TMP_Settings.defaultFontAsset;
            nome.text = OptionsManager.LocalizeEnum(tipo);
            nome.fontSize = TamanhoDaFonteDoRotulo;
            nome.alignment = TextAlignmentOptions.Center;
            nome.textWrappingMode = TextWrappingModes.NoWrap;   // RSTV-22: 1 linha sempre ('Lightning' cabe em 64u)
            nome.overflowMode = TextOverflowModes.Overflow;  // se estourar, transborda em vez de quebrar
            nome.color = Color.white;
            RectTransform nomeRt = nomeGo.GetComponent<RectTransform>();
            nomeRt.anchorMin = new Vector2(0.5f, 0.5f);
            nomeRt.anchorMax = new Vector2(0.5f, 0.5f);
            nomeRt.pivot = new Vector2(0.5f, 0.5f);
            nomeRt.anchoredPosition = new Vector2(0f, YDoRotuloManual);
            nomeRt.sizeDelta = new Vector2(LarguraDoRotuloManual, AlturaDoRotuloManual);
            nomeRt.localScale = new Vector3(EscalaDoRotuloDaClasse, EscalaDoRotuloDaClasse, EscalaDoRotuloDaClasse);

            _botoesManuais.Add(new BotaoManualDeClasse { Tipo = tipo, Highlight = hlImg });
            return botao;
        }

        private static void DisableDlcLinker(SkillTreeTab tab)
        {
            try
            {
                Behaviour linker = tab.dlcLinker;
                if (linker != null)
                {
                    linker.enabled = false;
                }
            }
            catch (Exception)
            {
                // sem dlcLinker: nada a desligar
            }
        }

        /// <summary>
        /// RSTV-17 — o dimensionamento do <c>SkillTreeTab</c> NATIVO, aplicado ao clone.
        /// <para>
        /// O QUE ESTAVA ERRADO: o clone e copiado pelo <c>Instantiate</c> (logo herdaria 64x64),
        /// mas o <c>HorizontalLayoutGroup</c> antigo tinha <c>childControlWidth/Height = true</c> +
        /// <c>LayoutElement</c> 74.5x76 — o grupo SOBRESCREVIA o RectTransform do clone para
        /// 74.5x76 (aba esticada, passo 78.5u em vez de 73.6u, fileira fora de escala e alinhada
        /// a esquerda). Aqui os valores nativos sao REIMPOSTOS explicitamente (aba, icone e rotulo),
        /// de modo que o clone fica IDENTICO a uma aba nativa mesmo se o molde vier do fallback
        /// (a aba do header, que nao tem `SkillTreeTab`).
        /// </para>
        /// </summary>
        private static void AplicarDimensionamentoNativo(GameObject botao, SkillTreeTab tab)
        {
            try
            {
                RectTransform rt = botao.GetComponent<RectTransform>();
                if (rt != null)
                {
                    rt.anchorMin = new Vector2(0f, 0f);          // igual ao SkillTreeTab nativo
                    rt.anchorMax = new Vector2(0f, 0f);
                    rt.pivot = new Vector2(0.5f, 0.5f);
                    rt.sizeDelta = new Vector2(LadoDoBotaoDeClasse, LadoDoBotaoDeClasse);
                    rt.localScale = Vector3.one;
                }

                if (tab == null)
                {
                    return;
                }

                // O ICONE (o que a referencia image_e488a3 mede): 56x56, escala 1, centrado.
                if (tab.treeIcon != null)
                {
                    RectTransform icone = tab.treeIcon.rectTransform;
                    if (icone != null)
                    {
                        icone.anchorMin = new Vector2(0.5f, 0.5f);
                        icone.anchorMax = new Vector2(0.5f, 0.5f);
                        icone.pivot = new Vector2(0.5f, 0.5f);
                        icone.anchoredPosition = Vector2.zero;
                        icone.sizeDelta = new Vector2(LadoDoIconeDaClasse, LadoDoIconeDaClasse);
                        icone.localScale = Vector3.one;
                    }
                }

                // O ROTULO (nome da classe): 37.86x40 em escala 0.7, em (0,-27.1).
                if (tab.treeName != null)
                {
                    RectTransform rotulo = tab.treeName.rectTransform;
                    if (rotulo != null)
                    {
                        rotulo.anchorMin = new Vector2(0.5f, 0.5f);
                        rotulo.anchorMax = new Vector2(0.5f, 0.5f);
                        rotulo.pivot = new Vector2(0.5f, 0.5f);
                        rotulo.anchoredPosition = new Vector2(0f, YDoRotuloDaClasse);
                        rotulo.sizeDelta = new Vector2(LarguraDoRotuloDaClasse, AlturaDoRotuloDaClasse);
                        rotulo.localScale = new Vector3(EscalaDoRotuloDaClasse, EscalaDoRotuloDaClasse, EscalaDoRotuloDaClasse);
                    }
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-17: nao deu para aplicar o dimensionamento nativo do SkillTreeTab: " + e.Message);
            }
        }

        /// <summary>
        /// RSTV-17: com <c>childControlWidth/Height = false</c> (como no HLG nativo) o grupo NAO
        /// redimensiona o filho — o <c>LayoutElement</c> so fica como documentacao do tamanho nativo
        /// (64x64). Antes ele valia 74.5x76 e, com o controle LIGADO, esticava a aba.
        /// </summary>
        private static void EnsureLayoutElement(GameObject botao)
        {
            LayoutElement le = botao.GetComponent<LayoutElement>();
            if (le == null)
            {
                le = botao.AddComponent<LayoutElement>();
            }

            le.preferredWidth = LadoDoBotaoDeClasse;
            le.minWidth = LadoDoBotaoDeClasse;
            le.preferredHeight = LadoDoBotaoDeClasse;
            le.minHeight = LadoDoBotaoDeClasse;
        }

        private static List<SkillType> OrdemDoAsset()
        {
            try
            {
                GlobalSettingsManager gsm = GlobalSettingsManager.instance;
                if (gsm != null && gsm.miscSettings != null)
                {
                    return gsm.miscSettings.SkillTabTypes;
                }
            }
            catch (Exception)
            {
                // sem lista do asset
            }

            return null;
        }

        private static Sprite IconeDe(SkillType tipo)
        {
            try
            {
                GlobalSettingsManager gsm = GlobalSettingsManager.instance;
                if (gsm == null || gsm.miscSettings == null)
                {
                    return null;
                }

                int idx = gsm.miscSettings.SkillTabTypes.IndexOf(tipo);
                Sprite[] icones = gsm.miscSettings.TreeIcons;
                if (idx >= 0 && icones != null && idx < icones.Length)
                {
                    return icones[idx];
                }
            }
            catch (Exception)
            {
                // sem icone
            }

            return null;
        }

        private static void MarcarClasse(SkillType tipo)
        {
            for (int i = 0; i < _botoesDeClasse.Count; i++)
            {
                SkillTreeTab tab = _botoesDeClasse[i];
                if (tab == null)
                {
                    continue;
                }

                bool selecionado = tab.skillType == tipo;
                try
                {
                    if (tab.highlight != null)
                    {
                        tab.highlight.gameObject.SetActive(selecionado);
                    }
                }
                catch (Exception)
                {
                    // sem highlight no clone
                }
            }

            // RSTV-22: os botoes montados a MAO (fallback) tambem alternam o highlight de selecao.
            for (int i = 0; i < _botoesManuais.Count; i++)
            {
                BotaoManualDeClasse bm = _botoesManuais[i];
                if (bm == null || bm.Highlight == null)
                {
                    continue;
                }

                bm.Highlight.gameObject.SetActive(bm.Tipo == tipo);
            }
        }

        private static void TrocarClasse(SkillType tipo)
        {
            try
            {
                _tipoAtual = tipo;
                MarcarClasse(tipo);
                Popular(tipo);

                // RSTV-23h: indica no titulo da janela qual classe esta sendo exibida.
                string nomeDaClasse;
                try
                {
                    nomeDaClasse = OptionsManager.LocalizeEnum(tipo);
                }
                catch (Exception)
                {
                    nomeDaClasse = tipo.ToString();
                }
                SkillTreesWindow.DefinirSubtitulo(nomeDaClasse);

                Plugin.Log.LogInfo("RSTV-16: classe visualizada -> " + tipo + ".");
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-16: falha ao trocar para a classe " + tipo + ": " + e);
            }
        }

        /// <summary>
        /// Monta a arvore de UMA classe. PONTO 2: o predicado de `RefreshAvailableSkillTrees`
        /// (l.170113) aplicado sobre `Game.Instance.Skills` — NAO `SkillsByTreeDict` (que omite
        /// `DontIncludeInTree` e DLC). PONTO 3: o layout e NOSSO (formula de `PopulateTree`, l.177739).
        /// </summary>
        internal static void Popular(SkillType tipo)
        {
            if (_areaDaArvore == null)
            {
                return;
            }

            // RSTV-18: os nos vivem no frame x1.7 ('RstvNodeContainer'); a area (escala 1) fica para as
            // linhas de dependencia. Sem o frame (cena estranha), cai na propria area — nunca some.
            RectTransform paiDeNos = _containerDeNos != null ? _containerDeNos : _areaDaArvore;

            LimparItens();

            Burst2Flame.Game jogo = Burst2Flame.Game.Instance;
            if (jogo == null || jogo.Skills == null)
            {
                Aviso("Game.Instance/Skills ausente — sem a lista de skills nao ha arvore");
                return;
            }

            GUIManager gui = GUIManager.instance;
            if (gui == null || gui.skillTreeItemActivePrefab == null)
            {
                Aviso("GUIManager.skillTreeItemActivePrefab ausente — sem o no da arvore");
                return;
            }

            float hp = PaddingHorizontalPadrao;
            float vp = PaddingVerticalPadrao;
            SkillTreeManager nativo = LoadableUIWindow<SkillTreeManager>.Instance;   // SO LEITURA
            if (nativo != null)
            {
                hp = nativo.nodeHorizontalPadding;
                vp = nativo.tierVerticalPadding;
            }

            List<SkillInfo> todos = jogo.Skills;
            List<SkillInfo>[] porTier = new List<SkillInfo>[5];
            for (int t = 0; t < 5; t++)
            {
                porTier[t] = new List<SkillInfo>();
            }

            for (int i = 0; i < todos.Count; i++)
            {
                SkillInfo s = todos[i];
                if (s == null || s.SkillType != tipo || s.Disabled || s.DontIncludeInTree)
                {
                    continue;
                }

                if (!jogo.FullReleaseModeEnabled(s))
                {
                    continue;
                }

                int t = s.Tier - 1;
                if (t < 0 || t >= 5)
                {
                    continue;
                }

                porTier[t].Add(s);
            }

            for (int tier = 0; tier < 5; tier++)
            {
                List<SkillInfo> lista = porTier[tier];
                for (int i = 0; i < lista.Count; i++)
                {
                    SkillInfo info = lista[i];
                    SkillTreeItem item = UnityEngine.Object.Instantiate(gui.skillTreeItemActivePrefab, paiDeNos);
                    item.name = "RstvItem_" + tipo + "_T" + (tier + 1) + "_" + i;
                    item.SkillInfo = info;

                    if (item.SkillIcon != null)
                    {
                        item.SkillIcon.sprite = info.Icon;
                    }

                    if (item.UpgradeInfo != null)
                    {
                        item.UpgradeInfo.text = info.UpgradeText;
                    }

                    bool temAcao = info.ActionsGranted != null && info.ActionsGranted.Length != 0;
                    RectTransform rt = item.GetComponent<RectTransform>();
                    if (rt != null)
                    {
                        rt.anchoredPosition = new Vector2(
                            (info.xVal - 1f) * (temAcao ? -hp : hp) + (temAcao ? -hp / 2f : hp / 2f),
                            tier * -vp);
                    }

                    RstvSkillHover hover = item.gameObject.GetComponent<RstvSkillHover>();
                    if (hover == null)
                    {
                        hover = item.gameObject.AddComponent<RstvSkillHover>();
                    }

                    hover.Item = item;
                    _itens.Add(item);
                }
            }

            DesenharLinhasDeDependencia();
            CentralizarArvoreVerticalmente();
            _construidoPara = tipo;

            float escalaContainer = paiDeNos == _containerDeNos ? EscalaDoContainerDeNos : 1f;
            Plugin.Log.LogInfo("RSTV-16: arvore de " + tipo + " montada com " + _itens.Count +
                               " no(s) (Game.Instance.Skills: !Disabled && !DontIncludeInTree && " +
                               "FullReleaseModeEnabled; padding " + hp.ToString("0.#") + "/" + vp.ToString("0.#") +
                               "; clique bloqueado por ReadOnlySession.Active=" + ReadOnlySession.Active + ").");
            Plugin.Log.LogInfo("RSTV-18: container dos nos (" + NodeContainerName + ") em escala " +
                               escalaContainer.ToString("0.##") + "x -> no " +
                               (LadoDoNoDoPrefab * EscalaDoNoDoPrefab * escalaContainer).ToString("0.#") +
                               "u efetivo, pitch horizontal " + (hp * escalaContainer).ToString("0.#") +
                               "u / vertical " + (vp * escalaContainer).ToString("0.#") + "u.");

            // RSTV-24c: define o subtitulo ("All Skill Trees — <Classe>") a CADA carga — antes so era
            // chamado no `TrocarClasse` (nao rodava na 1a abertura, e o titulo ficava sem a classe).
            DefinirSubtituloDaClasse(tipo);
        }

        /// <summary>RSTV-23h/24c: anexa o nome da classe exibida ao titulo da janela.</summary>
        private static void DefinirSubtituloDaClasse(SkillType tipo)
        {
            string nomeDaClasse;
            try
            {
                nomeDaClasse = OptionsManager.LocalizeEnum(tipo);
            }
            catch (Exception)
            {
                nomeDaClasse = tipo.ToString();
            }
            SkillTreesWindow.DefinirSubtitulo(nomeDaClasse);
        }

        /// <summary>
        /// PONTO 3: reimplementa `SkillTreeItem.ProcessDependencyLines` (l.177056) SEM o manager — o
        /// container das linhas e a NOSSA area, nunca `manager.skillTreeShowers`.
        /// </summary>
        private static void DesenharLinhasDeDependencia()
        {
            if (_areaDaArvore == null)
            {
                return;
            }

            for (int i = 0; i < _itens.Count; i++)
            {
                SkillTreeItem responsavel = _itens[i];
                if (responsavel == null || responsavel.SkillInfo == null)
                {
                    continue;
                }

                List<SkillTreeItem> filhos = new List<SkillTreeItem>();
                for (int j = 0; j < _itens.Count; j++)
                {
                    SkillTreeItem candidato = _itens[j];
                    if (candidato != null && candidato.SkillInfo != null &&
                        candidato.SkillInfo.Dependency == responsavel.SkillInfo)
                    {
                        filhos.Add(candidato);
                    }
                }

                if (responsavel.DependencyLine != null)
                {
                    if (filhos.Count == 1)
                    {
                        responsavel.DependencyLine.gameObject.SetActive(true);
                        // RSTV-23a: as linhas entram no CONTAINER dos nos (escala 1.7), como o nativo
                        // (`ProcessDependencyLines` parenta no `skillTreeShowers[...]`, tambem 1.7). Antes
                        // entravam na AREA (escala 1) — o sizeDelta `Distance/1.5` virava 33% curto e o
                        // traco 1.7x fino em relacao aos nos.
                        RectTransform paiDasLinhas = _containerDeNos != null ? _containerDeNos : _areaDaArvore;
                        responsavel.DependencyLine.transform.SetParent(paiDasLinhas, false);
                        responsavel.DependencyLine.transform.SetSiblingIndex(0);

                        RectTransform linha = responsavel.DependencyLine.GetComponent<RectTransform>();
                        RectTransform da = responsavel.GetComponent<RectTransform>();
                        RectTransform para = filhos[0] != null ? filhos[0].GetComponent<RectTransform>() : null;
                        if (linha != null && da != null && para != null)
                        {
                            linha.position = Vector3.Lerp(da.position, para.position, 0.5f);

                            // RSTV-25: o `Distance/1.5f` do nativo assume o sprite com padding e a linha
                            // no MESMO shower; aqui a linha pode estar em escala (container 1.7). Para o
                            // traco cobrir EXATAMENTE a distancia mundo, dividimos pela escala MUNDO
                            // (lossyScale) — sem o fator 1.5 que deixava um vao de ~4u entre a ponta e o no.
                            float distanciaMundo = Vector3.Distance(da.position, para.position);
                            float escalaMundo = Mathf.Abs(linha.lossyScale.y);
                            escalaMundo = escalaMundo > 0.001f ? escalaMundo : 1f;
                            linha.sizeDelta = new Vector2(linha.sizeDelta.x, distanciaMundo / escalaMundo);

                            // RSTV-24b: a linha e um sprite VERTICAL (sizeDelta 3x40) e so era POSICIONADA
                            // no ponto medio — herda rotacao 0 e ficava VERTICAL ao lado dos nos, nao
                            // DIAGONAL conectando-os. O sprite aponta para CIMA com rotacao 0, entao
                            // `Atan2(dy,dx) - 90` aponta de `da` p/ `para`.
                            Vector3 delta = para.position - da.position;
                            float angulo = Mathf.Atan2(delta.y, delta.x) * Mathf.Rad2Deg - 90f;
                            linha.rotation = Quaternion.Euler(0f, 0f, angulo);
                        }
                    }
                    else
                    {
                        responsavel.DependencyLine.gameObject.SetActive(false);
                    }
                }

                if (responsavel.DoubleDep != null)
                {
                    responsavel.DoubleDep.SetActive(filhos.Count == 2);
                }
            }

            // RSTV-24b: diagnostico — quantas linhas ficaram ativas e se tem sprite (para achar por que
            // as linhas de dependencia nao desenham na tela).
            int ativas = 0;
            int comSprite = 0;
            string corPrimeira = "?";
            for (int i = 0; i < _itens.Count; i++)
            {
                SkillTreeItem item = _itens[i];
                if (item == null || item.DependencyLine == null || !item.DependencyLine.gameObject.activeSelf)
                {
                    continue;
                }
                ativas++;
                if (item.DependencyLine.sprite != null)
                {
                    comSprite++;
                }
                if (corPrimeira == "?")
                {
                    corPrimeira = item.DependencyLine.color.ToString();
                }
            }
            Plugin.Log.LogInfo("RSTV-24b: " + ativas + " linha(s) de dependencia ativa(s), " + comSprite +
                               " com sprite (de " + _itens.Count + " no(s)); cor da 1a = " + corPrimeira + ".");

            // RSTV-25: diagnostico do T4->T5 — quantos nos por tier TEM Dependency (para entender por que
            // o tier 5 fica sem linha de entrada na tela).
            string porTier = "";
            for (int t = 1; t <= 5; t++)
            {
                int comDep = 0;
                int total = 0;
                for (int i = 0; i < _itens.Count; i++)
                {
                    SkillTreeItem item = _itens[i];
                    if (item == null || item.SkillInfo == null || item.SkillInfo.Tier != t)
                    {
                        continue;
                    }
                    total++;
                    if (item.SkillInfo.Dependency != null)
                    {
                        comDep++;
                    }
                }
                porTier += (porTier.Length == 0 ? "" : ", ") + "T" + t + ":" + comDep + "/" + total;
            }
            Plugin.Log.LogInfo("RSTV-25: nos com Dependency por tier — " + porTier + ".");
        }

        /// <summary>
        /// RSTV-23b/23g — centraliza a arvore na AREA, nos DOIS eixos. Antes sobrava ~111px de vao
        /// morto no topo, a ultima fileira encostava na base e a arvore ficava ~48px a esquerda do
        /// centro (as colunas de `ActionsGranted` puxam para a esquerda). Calcula o bbox dos nos (em
        /// unidades LOCAIS do container, escala 1.7) e desloca o container para o centro do bbox cair
        /// no centro da area.
        /// </summary>
        private static void CentralizarArvoreVerticalmente()
        {
            // RSTV-24a: o centering pelo bbox e SO para o modo JANELA (na aba, o offset nativo do
            // container — `DeslocamentoDoCentroDaArea + YDoContainerDeNos` — ja posiciona certo).
            if (!_modoJanela || _containerDeNos == null || _itens == null || _itens.Count == 0)
            {
                return;
            }

            float minX = float.MaxValue;
            float maxX = float.MinValue;
            float minY = float.MaxValue;
            float maxY = float.MinValue;
            int contados = 0;
            for (int i = 0; i < _itens.Count; i++)
            {
                RectTransform rt = _itens[i] != null ? _itens[i].GetComponent<RectTransform>() : null;
                if (rt == null)
                {
                    continue;
                }

                float x = rt.anchoredPosition.x;
                float y = rt.anchoredPosition.y;
                float meiaL = rt.sizeDelta.x * 0.5f * Mathf.Abs(rt.localScale.x);
                float meiaA = rt.sizeDelta.y * 0.5f * Mathf.Abs(rt.localScale.y);
                minX = Mathf.Min(minX, x - meiaL);
                maxX = Mathf.Max(maxX, x + meiaL);
                minY = Mathf.Min(minY, y - meiaA);
                maxY = Mathf.Max(maxY, y + meiaA);
                contados++;
            }

            if (contados == 0 || minX >= maxX || minY >= maxY)
            {
                return;
            }

            float centroX = (minX + maxX) * 0.5f;
            float centroY = (minY + maxY) * 0.5f;
            float ajusteX = -centroX * EscalaDoContainerDeNos;
            float ajusteY = -centroY * EscalaDoContainerDeNos;

            // CLAMP do topo (RSTV-24a): o topo do bbox (em unidades da area) nao pode passar do topo da
            // area — senao a 1a fileira invade a barra de classes. Se passar, desce o container o suficiente.
            if (_areaDaArvore != null)
            {
                float topoDaArea = _areaDaArvore.rect.height * 0.5f;
                float topoDoBbox = ajusteY + maxY * EscalaDoContainerDeNos;
                if (topoDoBbox > topoDaArea)
                {
                    ajusteY -= (topoDoBbox - topoDaArea);
                }
            }

            // SUBSTITUI (nao soma): o container fica posicionado SO pelo centro do bbox, centrado na
            // AREA. Antes somava ao offset nativo (+70.7u) e a arvore ia parar centrada na JANELA.
            _containerDeNos.anchoredPosition = new Vector2(ajusteX, ajusteY);

            Plugin.Log.LogInfo("RSTV-24a: arvore centralizada na AREA (bbox local " +
                               minX.ToString("0.#") + ".." + maxX.ToString("0.#") + " x " +
                               minY.ToString("0.#") + ".." + maxY.ToString("0.#") + ", pos " +
                               ajusteX.ToString("0.#") + "," + ajusteY.ToString("0.#") + "u).");

            // RSTV-23i: clamp — se o bbox (em unidades da area, x1.7) exceder a area da arvore, reduz a
            // escala do container para caber (protecao contra classes mais largas invadirem a moldura).
            if (_areaDaArvore != null)
            {
                float larguraArea = _areaDaArvore.rect.width;
                float alturaArea = _areaDaArvore.rect.height;
                float larguraBbox = (maxX - minX) * EscalaDoContainerDeNos;
                float alturaBbox = (maxY - minY) * EscalaDoContainerDeNos;
                if (larguraArea > 1f && alturaArea > 1f &&
                    (larguraBbox > larguraArea || alturaBbox > alturaArea))
                {
                    float fator = Mathf.Min(larguraArea / larguraBbox, alturaArea / alturaBbox);
                    fator = Mathf.Clamp(fator, 0.5f, 1f);
                    Vector3 escala = _containerDeNos.localScale;
                    _containerDeNos.localScale = new Vector3(escala.x * fator, escala.y * fator, escala.z * fator);
                    Plugin.Log.LogInfo("RSTV-23i: arvore excede a area (" + larguraBbox.ToString("0.#") + "x" +
                                       alturaBbox.ToString("0.#") + " > " + larguraArea.ToString("0.#") + "x" +
                                       alturaArea.ToString("0.#") + ") — escala do container reduzida por " +
                                       fator.ToString("0.##") + "x.");
                }
            }
        }

        private static void LimparItens()
        {
            for (int i = 0; i < _itens.Count; i++)
            {
                SkillTreeItem item = _itens[i];
                if (item == null)
                {
                    continue;
                }

                try
                {
                    if (item.DependencyLine != null && item.DependencyLine.gameObject != null)
                    {
                        UnityEngine.Object.Destroy(item.DependencyLine.gameObject);
                    }

                    if (item.gameObject != null)
                    {
                        UnityEngine.Object.Destroy(item.gameObject);
                    }
                }
                catch (Exception)
                {
                    // cena descarregada: nada a destruir
                }
            }

            _itens.Clear();
            _construidoPara = (SkillType)(-1);
        }

        private static void Aviso(string motivo)
        {
            if (_ultimoAviso == motivo)
            {
                return;
            }

            _ultimoAviso = motivo;
            Plugin.Log.LogWarning("RSTV-16: " + motivo + ".");
        }
    }

    /// <summary>
    /// Tooltip read-only do no: o tooltip NATIVO da skill aparece no hover, o que da utilidade a arvore
    /// sem nenhuma escrita (o <c>Tooltip.ShowSkillTooltip(SkillTreeItem)</c> so LE). Defensivo: sem
    /// GUIManager/tooltip, nao faz nada.
    /// </summary>
    internal class RstvSkillHover : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
    {
        internal SkillTreeItem Item;
        private Outline _outline;   // RSTV-24e: contorno dourado adicionado no hover (removido no exit)

        public void OnPointerEnter(PointerEventData eventData)
        {
            try
            {
                if (Item == null || Item.SkillInfo == null)
                {
                    return;
                }

                GUIManager gui = GUIManager.instance;
                if (gui == null || gui.tooltip == null)
                {
                    return;
                }

                gui.tooltip.ShowSkillTooltip(Item);

                // RSTV-23f/24e: marca o no sob o mouse. O `Hover` nativo e sutil demais (anel 48 vs 38-43),
                // entao alem dele adicionamos um OUTLINE dourado no icone — bem mais visivel.
                if (Item.Hover != null)
                {
                    Item.Hover.gameObject.SetActive(true);
                }

                if (Item.SkillIcon != null && Item.SkillIcon.GetComponent<Outline>() == null)
                {
                    _outline = Item.SkillIcon.gameObject.AddComponent<Outline>();
                    _outline.effectColor = new Color(1f, 0.85f, 0.4f, 1f);   // dourado
                    _outline.effectDistance = new Vector2(2f, -2f);
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-16: falha ao mostrar o tooltip da skill: " + e.Message);
            }
        }

        public void OnPointerExit(PointerEventData eventData)
        {
            try
            {
                GUIManager gui = GUIManager.instance;
                if (gui != null && gui.tooltip != null)
                {
                    gui.tooltip.HideTooltip();
                }

                if (Item != null && Item.Hover != null)
                {
                    Item.Hover.gameObject.SetActive(false);
                }

                if (_outline != null)
                {
                    try
                    {
                        UnityEngine.Object.Destroy(_outline);
                    }
                    catch (Exception)
                    {
                        // ja destruido
                    }
                    _outline = null;
                }
            }
            catch (Exception)
            {
                // sem tooltip: nada a esconder
            }
        }
    }
}
