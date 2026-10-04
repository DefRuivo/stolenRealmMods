using System;
using Burst2Flame;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-21 — a JANELA read-only PROPRIA do mod: um Canvas em overlay (com o MESMO
    /// <see cref="CanvasScaler"/> do jogo) que hospeda o painel "All Skill Trees" FORA do inventario.
    ///
    /// POR QUE ESTA JANELA EXISTE (o defeito do dono, 03/10)
    /// -----------------------------------------------------
    /// O botao 'Skills' injetado no modal "Remove Skill Trees" (<see cref="RemovalWindowSkillsButton"/>)
    /// chamava <c>SkillTreesTab.Abrir</c>, que abre o INVENTARIO (<c>CharacterMenusManager.OpenCharacterMenu</c>)
    /// e so entao seleciona a aba. A tela do modal e a de PARTY SELECT: ali o inventario NAO abre
    /// (o <c>OpenCharacterMenu</c> desiste em silencio quando o personagem nao esta em
    /// <c>AllMyCharacters</c>) — e o clique nao mostrava NADA (log: "o inventario nao abriu em 5 s").
    /// A visao read-only nao devia depender do inventario: ela precisa de um hospedeiro proprio.
    ///
    /// O QUE ELA E (e o que ela NAO e)
    /// ------------------------------
    ///   * E um <b>hospedeiro</b>: cria Canvas + fundo + cabecalho (titulo + botao fechar) + a AREA de
    ///     conteudo onde o <c>SkillTreesTab</c> monta o MESMO painel de arvores que a aba usa
    ///     (<see cref="Conteudo"/>) — a renderizacao continua num lugar so (regra do projeto).
    ///   * NAO e uma janela de UI do jogo: nao entra em <c>UIWindowManager.OpenedWindows</c> e nao
    ///     troca o <c>GUIState</c>. Nao precisa: o conteudo e somente leitura por construcao (os nos
    ///     sao clones do <c>skillTreeItemActivePrefab</c> com o clique barrado por
    ///     <c>SkillTreeItemTogglePatch</c> enquanto a sessao read-only esta ativa), e o fundo do
    ///     Canvas consome o clique, entao nada atras (o proprio modal) e acionado por engano.
    ///   * NAO inventa visual quando ha molde nativo: titulo e botao fechar nascem de CLONES de
    ///     componentes do jogo (o TMP do proprio modal e o <c>closeButton</c> do <c>SkillTreeManager</c>,
    ///     com fallback no modal). So o FUNDO e uma cor solida neutra — e o log diz exatamente de onde
    ///     veio cada peca.
    ///
    /// CICLO DE VIDA
    /// -------------
    /// A janela e DESTRUIDA-e-RECRIADA por sessao de cena? Nao: a raiz e <c>DontDestroyOnLoad</c> e
    /// REUSADA entre aberturas (so <c>SetActive</c>). Quem a FECHA e: (1) o botao fechar; (2) o
    /// <c>Atualizar</c> — se o DONO (a janela do jogo que pediu a visao, o modal) sair de cena, a
    /// janela se fecha sozinha em vez de ficar pendurada por cima da proxima tela.
    /// </summary>
    internal static class SkillTreesWindow
    {
        internal const string RootName = "RstvSkillTreesWindow";
        internal const string FrameName = "RstvWindowFrame";
        internal const string HeaderName = "RstvWindowHeader";
        internal const string ContentName = "RstvWindowContent";
        internal const string TitleName = "RstvWindowTitle";
        internal const string CloseButtonName = "RstvWindowClose";

        internal const string TitleLabel = "All Skill Trees";
        internal const string CloseLabel = "Close";

        private const float MargemLateral = 64f;
        private const float MargemTopo = 48f;
        private const float MargemBase = 48f;       // RSTV-23e: 40 -> 48 (era assimetrica vs topo 48)
        private const float AlturaDoCabecalho = 64f; // RSTV-23e: 52 -> 64 (botao Close colado na borda; 12u de folga)
        private const float LadoDoBotaoFechar = 56f; // RSTV-23e: 40 -> 56 (rotulo "Close" espremido na caixa 40x40)

        private static GameObject _root;
        private static RectTransform _conteudo;
        private static Transform _dono;
        private static TextMeshProUGUI _titulo;   // RSTV-23h: o titulo da janela, para anexar a classe exibida

        /// <summary>
        /// RSTV-21R: aviso de que a janela FECHOU — disparado pelo <see cref="Fechar"/> tanto quando o
        /// botao fechar a desliga quanto quando o <see cref="Atualizar"/> a fecha por o dono sair de
        /// cena. Quem hospeda o painel (<c>SkillTreesTab</c>) se inscreve para LARGAR o modo janela nesse
        /// instante: sem isto o flag <c>_modoJanela</c> ficava pendurado depois do fechamento, ate um
        /// ponto de entrada chamar <c>SairDoModoJanela</c>.
        /// </summary>
        internal static Action Fechou;

        /// <summary>RSTV-22: o tooltip do jogo e MOVIDO para DENTRO da janela enquanto ela esta aberta
        /// (assim ele desenha acima do fundo escuro). O pai/sibling antigos ficam guardados e sao
        /// RESTAURADOS no <see cref="RestaurarTooltip"/>.</summary>
        private static bool _tooltipMovido;
        private static Transform _tooltipPaiAntigo;
        private static int _tooltipSiblingAntigo;
        private static Outline _outlineDoTooltip;   // RSTV-23f: contorno adicionado ao tooltip (removido ao fechar)

        /// <summary>A janela esta visivel AGORA? Exige tambem o dono vivo (o modal ainda em cena).</summary>
        internal static bool Aberta
        {
            get { return _root != null && _root.activeSelf && DonoVivo(); }
        }

        /// <summary>A AREA onde o painel de arvores e montado (filha da janela, abaixo do cabecalho).</summary>
        internal static RectTransform Conteudo
        {
            get { return _conteudo; }
        }

        /// <summary>O dono (a janela do jogo que pediu a visao) ainda esta em cena?</summary>
        internal static bool DonoVivo()
        {
            return _dono != null && _dono.gameObject != null && _dono.gameObject.activeInHierarchy;
        }

        /// <summary>
        /// Garante a janela (cria na 1a vez, reusa depois) e devolve a AREA de conteudo. Idempotente:
        /// chamar de novo so reafirma o dono e religa a raiz — NUNCA cria uma segunda janela.
        /// <paramref name="dono"/> e a janela do jogo de onde se copiam os MOLDES nativos (canvas,
        /// titulo, botao) e cujo ciclo de vida a nossa janela segue.
        /// </summary>
        internal static RectTransform Garantir(Transform dono)
        {
            try
            {
                _dono = dono;

                if (_root != null)
                {
                    if (!_root.activeSelf)
                    {
                        _root.SetActive(true);
                        ElevarTooltip();
                    }

                    return _conteudo;
                }

                return Construir(dono);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-21: falha ao montar a janela read-only: " + e);
                return null;
            }
        }

        /// <summary>
        /// Fecha a janela (so desliga a raiz — ela e REUSADA na proxima abertura).
        ///
        /// RSTV-21R: quando o fechamento acontece (a raiz estava ligada), AVISA quem hospeda o painel via
        /// <see cref="Fechou"/> — o botao fechar e o <see cref="Atualizar"/> passam os DOIS por aqui, entao
        /// nenhum caminho normal deixa o modo janela pendurado.
        /// </summary>
        internal static void Fechar()
        {
            bool fechou = false;
            try
            {
                RestaurarTooltip();

                if (_root != null && _root.activeSelf)
                {
                    _root.SetActive(false);
                    fechou = true;
                    Plugin.Log.LogInfo("RSTV-21: janela read-only fechada.");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: falha ao fechar a janela read-only: " + e.Message);
            }

            if (fechou && Fechou != null)
            {
                try
                {
                    Fechou();
                }
                catch (Exception e)
                {
                    Plugin.Log.LogWarning("RSTV-21: falha ao avisar o fechamento da janela: " + e.Message);
                }
            }
        }

        /// <summary>
        /// Chamado pelo <c>SkillTreesTab.Tick</c>: fecha a janela sozinha quando o DONO sai de cena
        /// (o jogador fechou o modal com ela aberta). Sem isso a janela ficaria pendurada por cima da
        /// proxima tela, porque a raiz e <c>DontDestroyOnLoad</c>.
        /// </summary>
        internal static void Atualizar()
        {
            try
            {
                if (_root != null && _root.activeSelf && !DonoVivo())
                {
                    Fechar();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: falha ao sincronizar a janela read-only com o dono: " + e.Message);
            }
        }

        // ---------------------------------------------------------------------------------------
        // Construcao
        // ---------------------------------------------------------------------------------------

        private static RectTransform Construir(Transform dono)
        {
            // RSTV-22: o MODAL (dono) e a fonte dos MOLDES NATIVOS — Fade/PanelBackground (fundo e
            // moldura), CancelButton (botao fechar) e TitleText (titulo). Nada de cor solida feia nem
            // de fallback de option row.
            RoguelikeSkillTreeRemovalWindow modal = dono != null ? dono.GetComponent<RoguelikeSkillTreeRemovalWindow>() : null;
            Canvas canvasOrigem = CanvasDa(dono);
            Button moldeBotao = BotaoMolde(dono, modal);
            TextMeshProUGUI moldeTexto = TextoMolde(dono, modal);
            Image moldeFundo = modal != null ? modal.Fade : null;
            Image moldePainel = modal != null ? modal.PanelBackground : null;

            // 1) RAIZ — um Canvas em OVERLAY proprio, ACIMA do canvas do jogo (sortingOrder + 100).
            GameObject root = new GameObject(RootName, typeof(RectTransform));
            UnityEngine.Object.DontDestroyOnLoad(root);

            Canvas canvas = root.AddComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = (canvasOrigem != null ? canvasOrigem.sortingOrder : 0) + 100;
            root.AddComponent<GraphicRaycaster>();
            CopiarScaler(canvasOrigem, root.AddComponent<CanvasScaler>());
            // OBS: `_root` so e publicado no FIM da construcao — se algo falhar no meio, a proxima
            // tentativa RECONSTROI em vez de reusar uma janela pela metade.

            // 2) FUNDO — escurece o jogo atras e CONSUME o clique (nada atras e acionado por engano).
            // RSTV-22: herda o sprite/cor do `Fade` do proprio modal; sem ele, cor neutra.
            GameObject fundo = new GameObject("RstvWindowBackdrop", typeof(RectTransform), typeof(Image));
            RectTransform fundoRt = fundo.GetComponent<RectTransform>();
            fundoRt.SetParent(root.transform, false);
            Esticar(fundoRt, 0f, 0f, 0f, 0f);
            Image fundoImg = fundo.GetComponent<Image>();
            fundoImg.raycastTarget = true;
            if (moldeFundo != null && moldeFundo.sprite != null)
            {
                fundoImg.sprite = moldeFundo.sprite;
                fundoImg.type = moldeFundo.type;
                fundoImg.color = moldeFundo.color;
            }
            else
            {
                fundoImg.color = new Color(0f, 0f, 0f, 0.82f);
            }

            // 3) MOLDURA — a janela em si, com o cabecalho no topo e a AREA de conteudo abaixo.
            // RSTV-22: herda o sprite/cor do `PanelBackground` do modal (painel nativo com borda).
            GameObject moldura = new GameObject(FrameName, typeof(RectTransform), typeof(Image));
            RectTransform molduraRt = moldura.GetComponent<RectTransform>();
            molduraRt.SetParent(root.transform, false);
            Esticar(molduraRt, MargemLateral, MargemBase, MargemLateral, MargemTopo);
            Image molduraImg = moldura.GetComponent<Image>();
            molduraImg.raycastTarget = true;
            if (moldePainel != null && moldePainel.sprite != null)
            {
                molduraImg.sprite = moldePainel.sprite;
                molduraImg.type = moldePainel.type;
                molduraImg.color = moldePainel.color;
            }
            else
            {
                molduraImg.color = new Color(0.07f, 0.07f, 0.09f, 0.96f);
            }

            float cabe = MontarCabecalho(molduraRt, moldeTexto, moldeBotao);

            GameObject conteudo = new GameObject(ContentName, typeof(RectTransform));
            RectTransform conteudoRt = conteudo.GetComponent<RectTransform>();
            conteudoRt.SetParent(molduraRt, false);
            conteudoRt.anchorMin = Vector2.zero;
            conteudoRt.anchorMax = Vector2.one;
            conteudoRt.pivot = new Vector2(0.5f, 0.5f);
            conteudoRt.offsetMin = new Vector2(0f, 0f);
            conteudoRt.offsetMax = new Vector2(0f, 0f - cabe);
            conteudoRt.localScale = Vector3.one;
            conteudoRt.localRotation = Quaternion.identity;

            Plugin.Log.LogInfo(
                "RSTV-21: janela read-only montada — Canvas overlay (sortingOrder " + canvas.sortingOrder +
                ", scaler " + (canvasOrigem != null ? "copiado do jogo" : "PADRAO: sem canvas de origem") +
                "), titulo de molde " + (moldeTexto != null ? ("'" + moldeTexto.gameObject.name + "'") : "PADRAO (TMP sem fonte do jogo)") +
                ", botao fechar de molde " + (moldeBotao != null ? ("'" + moldeBotao.gameObject.name + "'") : "PADRAO (botao novo)") +
                "; area de conteudo abaixo do cabecalho (" + cabe.ToString("0.#") + " px).");

            // Publica a janela SO agora, com a construcao inteira concluida (ver a OBS acima).
            _root = root;
            _conteudo = conteudoRt;

            ElevarTooltip();
            return _conteudo;
        }

        /// <summary>
        /// Move o TOOLTIP do jogo para DENTRO da janela enquanto ela estiver aberta.
        ///
        /// POR QUE: o tooltip de skill (hover no noh, <c>gui.tooltip.ShowSkillTooltip</c>) vive no
        /// canvas RAIZ da UI do jogo (ordem 0) — atras da nossa janela (ordem 100). Ergue-lo por
        /// `overrideSorting` no canvas foi o BUG de 03/10 (escondia a janela inteira). A solucao
        /// segura e REPARENTAR o GameObject do tooltip para o nosso Canvas (ultimo irmao): ele passa a
        /// desenhar acima do fundo escuro, reusando TODO o visual nativo (texto/cor/posicao), sem tocar
        /// em ordenacao nenhuma. O pai e o indice antigos ficam guardados e sao RESTAURADOS no
        /// <see cref="Fechar"/> via <see cref="RestaurarTooltip"/>.
        /// </summary>
        private static void ElevarTooltip()
        {
            try
            {
                if (_root == null || _tooltipMovido)
                {
                    return;
                }

                GUIManager gui = GUIManager.instance;
                if (gui == null || gui.tooltip == null)
                {
                    Plugin.Log.LogWarning("RSTV-21: GUIManager.tooltip ausente — o tooltip do noh nao vai aparecer.");
                    return;
                }

                Transform tooltip = gui.tooltip.transform;
                _tooltipPaiAntigo = tooltip.parent;
                _tooltipSiblingAntigo = tooltip.GetSiblingIndex();

                // worldPositionStays=true mantém a posicao de mundo (o tooltip e posicionado por mundo
                // a cada ShowSkillTooltip; aqui so trocamos o canvas onde ele desenha).
                tooltip.SetParent(_root.transform, true);
                tooltip.SetAsLastSibling();
                _tooltipMovido = true;

                // RSTV-23f: o tooltip some no fundo escuro da janela (~15 vs ~9-13 de brilho). Um Outline
                // preto de 2px no Image dele cria uma borda que o separa do painel. Guardado para ser
                // REMOVIDO no `RestaurarTooltip` (nao deixar residuo no tooltip do jogo).
                Image imgDoTooltip = gui.tooltip.GetComponent<Image>();
                if (imgDoTooltip == null)
                {
                    imgDoTooltip = gui.tooltip.GetComponentInChildren<Image>(true);
                }
                if (imgDoTooltip != null && imgDoTooltip.GetComponent<Outline>() == null)
                {
                    _outlineDoTooltip = imgDoTooltip.gameObject.AddComponent<Outline>();
                    _outlineDoTooltip.effectColor = new Color(0f, 0f, 0f, 0.9f);
                    _outlineDoTooltip.effectDistance = new Vector2(2f, -2f);
                }

                Plugin.Log.LogInfo("RSTV-21: tooltip do jogo movido para DENTRO da janela (acima do fundo) — " +
                                   "pai antigo '" + (_tooltipPaiAntigo != null ? _tooltipPaiAntigo.name : "?") +
                                   "'; restaurado ao fechar.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: nao deu para mover o tooltip para a janela: " + e.Message);
            }
        }

        /// <summary>Devolve o tooltip ao pai/indice originais (o ajuste de <see cref="ElevarTooltip"/>).</summary>
        private static void RestaurarTooltip()
        {
            if (!_tooltipMovido)
            {
                return;
            }

            try
            {
                GUIManager gui = GUIManager.instance;
                if (gui != null && gui.tooltip != null && _tooltipPaiAntigo != null)
                {
                    Transform tooltip = gui.tooltip.transform;
                    tooltip.SetParent(_tooltipPaiAntigo, true);
                    int alvo = Mathf.Min(_tooltipSiblingAntigo, _tooltipPaiAntigo.childCount - 1);
                    if (alvo >= 0)
                    {
                        tooltip.SetSiblingIndex(alvo);
                    }
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: falha ao devolver o tooltip ao jogo: " + e.Message);
            }

            _tooltipMovido = false;
            _tooltipPaiAntigo = null;

            // RSTV-23f: remove o contorno que o `ElevarTooltip` adicionou ao tooltip (nao deixar residuo).
            if (_outlineDoTooltip != null)
            {
                try
                {
                    UnityEngine.Object.Destroy(_outlineDoTooltip);
                }
                catch (Exception)
                {
                    // ja destruido
                }
                _outlineDoTooltip = null;
            }
        }

        private static float MontarCabecalho(RectTransform moldura, TextMeshProUGUI moldeTexto, Button moldeBotao)
        {
            GameObject cabecalho = new GameObject(HeaderName, typeof(RectTransform));
            RectTransform cab = cabecalho.GetComponent<RectTransform>();
            cab.SetParent(moldura, false);
            cab.anchorMin = new Vector2(0f, 1f);
            cab.anchorMax = new Vector2(1f, 1f);
            cab.pivot = new Vector2(0.5f, 1f);
            cab.anchoredPosition = Vector2.zero;
            cab.sizeDelta = new Vector2(0f, AlturaDoCabecalho);
            cab.localScale = Vector3.one;

            MontarTitulo(cab, moldeTexto);
            MontarBotaoFechar(cab, moldeBotao, moldeTexto);

            // RSTV-23e: divisor de 2px sob o cabecalho (antes o titulo "flutuava" e a barra de classes
            // comecava colada). Branco em alfa ~0.25, largura total menos 2x16u.
            GameObject divisor = new GameObject("RstvHeaderDivider", typeof(RectTransform), typeof(Image));
            RectTransform divRt = divisor.GetComponent<RectTransform>();
            divRt.SetParent(moldura, false);
            divRt.anchorMin = new Vector2(0f, 1f);
            divRt.anchorMax = new Vector2(1f, 1f);
            divRt.pivot = new Vector2(0.5f, 1f);
            divRt.anchoredPosition = new Vector2(0f, -AlturaDoCabecalho);
            divRt.sizeDelta = new Vector2(-32f, 2f);
            divRt.localScale = Vector3.one;
            Image divImg = divisor.GetComponent<Image>();
            divImg.color = new Color(1f, 1f, 1f, 0.25f);
            divImg.raycastTarget = false;

            return AlturaDoCabecalho;
        }

        private static void MontarTitulo(RectTransform cabecalho, TextMeshProUGUI molde)
        {
            TextMeshProUGUI titulo;
            if (molde != null)
            {
                TextMeshProUGUI clone = UnityEngine.Object.Instantiate(molde, cabecalho);
                clone.gameObject.name = TitleName;
                clone.gameObject.SetActive(true);
                SelectPartyButton.DisableLocalizers(clone.gameObject);
                titulo = clone;
            }
            else
            {
                GameObject go = new GameObject(TitleName, typeof(RectTransform));
                go.transform.SetParent(cabecalho, false);
                titulo = go.AddComponent<TextMeshProUGUI>();
                titulo.font = TMP_Settings.defaultFontAsset;   // sem molde: a fonte padrao do TMP
                titulo.color = Color.white;
                titulo.enableAutoSizing = false;
                titulo.fontSize = 26f;
                titulo.alignment = TextAlignmentOptions.MidlineLeft;
                Plugin.Log.LogWarning("RSTV-21: sem molde de texto no jogo — o titulo da janela usa a " +
                                      "fonte padrao do TMP (pode nao combinar com a UI do jogo).");
            }

            RectTransform rt = titulo.rectTransform;
            rt.anchorMin = new Vector2(0f, 0f);
            rt.anchorMax = new Vector2(1f, 1f);
            rt.pivot = new Vector2(0f, 0.5f);
            rt.offsetMin = new Vector2(16f, 0f);
            rt.offsetMax = new Vector2(-(LadoDoBotaoFechar + 24f), 0f);
            rt.localScale = Vector3.one;

            try
            {
                titulo.text = OptionsManager.Localize(TitleLabel);
                titulo.alignment = TextAlignmentOptions.MidlineLeft;
            }
            catch (Exception e)
            {
                titulo.text = TitleLabel;
                Plugin.Log.LogWarning("RSTV-21: nao deu para localizar o titulo da janela: " + e.Message);
            }

            _titulo = titulo;   // RSTV-23h: guarda a referencia p/ `DefinirSubtitulo` anexar a classe
        }

        /// <summary>
        /// RSTV-23h — anexa o nome da classe exibida ao titulo ("All Skill Trees — Fire"), chamado pelo
        /// <c>SkillTreesTab.TrocarClasse</c>. Sem titulo montado (janela ainda nao aberta), nao faz nada.
        /// </summary>
        internal static void DefinirSubtitulo(string nomeDaClasse)
        {
            try
            {
                if (_titulo == null || string.IsNullOrEmpty(nomeDaClasse))
                {
                    return;
                }

                string baseTitulo;
                try
                {
                    baseTitulo = OptionsManager.Localize(TitleLabel);
                }
                catch (Exception)
                {
                    baseTitulo = TitleLabel;
                }

                _titulo.text = baseTitulo + " — " + nomeDaClasse;
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-23h: nao deu para anexar a classe ao titulo: " + e.Message);
            }
        }

        /// <summary>
        /// Rotulo de reserva (so no caminho SEM molde de botao): um TMP que preenche o botao, com a
        /// fonte do molde de texto quando houver. O TEXTO e escrito logo abaixo (`CloseLabel`).
        /// </summary>
        private static void MontarRotuloNeutro(GameObject botao, TextMeshProUGUI moldeTexto)
        {
            try
            {
                GameObject go = new GameObject(CloseButtonName + "Label", typeof(RectTransform));
                go.transform.SetParent(botao.transform, false);
                RectTransform rt = go.GetComponent<RectTransform>();
                rt.anchorMin = Vector2.zero;
                rt.anchorMax = Vector2.one;
                rt.offsetMin = Vector2.zero;
                rt.offsetMax = Vector2.zero;
                rt.localScale = Vector3.one;

                TextMeshProUGUI tmp = go.AddComponent<TextMeshProUGUI>();
                tmp.font = moldeTexto != null ? moldeTexto.font : TMP_Settings.defaultFontAsset;
                tmp.color = Color.white;
                tmp.alignment = TextAlignmentOptions.Center;
                tmp.enableAutoSizing = true;
                tmp.fontSizeMin = 8f;
                tmp.fontSizeMax = 20f;
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: nao deu para montar o rotulo de reserva do botao fechar: " + e.Message);
            }
        }

        private static void MontarBotaoFechar(RectTransform cabecalho, Button molde, TextMeshProUGUI moldeTexto)
        {
            GameObject botao;
            if (molde != null)
            {
                botao = UnityEngine.Object.Instantiate(molde.gameObject, cabecalho);
            }
            else
            {
                botao = new GameObject(CloseButtonName, typeof(RectTransform), typeof(Image), typeof(Button));
                botao.transform.SetParent(cabecalho, false);
                Image imagem = botao.GetComponent<Image>();
                imagem.color = new Color(0.22f, 0.22f, 0.26f, 1f);
                Button b = botao.GetComponent<Button>();
                b.targetGraphic = imagem;
                MontarRotuloNeutro(botao, moldeTexto);
                Plugin.Log.LogWarning("RSTV-21: sem molde de botao no jogo — o botao fechar usa um visual neutro.");
            }

            botao.name = CloseButtonName;
            botao.SetActive(true);   // o molde pode vir INATIVO (o X do SkillTreeManager pre-carregado)

            RectTransform rt = botao.GetComponent<RectTransform>();
            rt.anchorMin = new Vector2(1f, 0.5f);
            rt.anchorMax = new Vector2(1f, 0.5f);
            rt.pivot = new Vector2(1f, 0.5f);
            rt.anchoredPosition = new Vector2(-22f, 0f);   // RSTV-24d: -10 -> -22 (o Close encostava na borda da moldura)
            rt.sizeDelta = new Vector2(LadoDoBotaoFechar, LadoDoBotaoFechar);
            rt.localScale = Vector3.one;
            rt.localRotation = Quaternion.identity;

            LayoutElement le = botao.GetComponent<LayoutElement>();
            if (le != null)
            {
                le.ignoreLayout = true;
            }

            // O clone herda o onClick SERIALIZADO do molde (o X do SkillTreeManager FECHARIA a arvore
            // de campanha). RSTV-12: trocar a INSTANCIA do evento descarta a lista persistente.
            SelectPartyButton.DisableLocalizers(botao);
            Button componente = botao.GetComponent<Button>();
            if (componente == null)
            {
                componente = botao.AddComponent<Button>();
            }

            SelectPartyButton.ClearClickListeners(componente);
            componente.onClick.AddListener(new UnityAction(Fechar));
            componente.interactable = true;

            TextMeshProUGUI rotulo = botao.GetComponentInChildren<TextMeshProUGUI>(true);
            if (rotulo != null)
            {
                try
                {
                    rotulo.text = OptionsManager.Localize(CloseLabel);
                }
                catch (Exception)
                {
                    rotulo.text = CloseLabel;
                }
            }
        }

        // ---------------------------------------------------------------------------------------
        // Resolucao de moldes / canvas
        // ---------------------------------------------------------------------------------------

        private static Canvas CanvasDa(Transform dono)
        {
            try
            {
                if (dono != null)
                {
                    Canvas[] doDono = dono.GetComponentsInParent<Canvas>(true);
                    if (doDono != null && doDono.Length > 0)
                    {
                        return doDono[0];
                    }
                }

                SkillTreeManager nativo = LoadableUIWindow<SkillTreeManager>.Instance;
                if (nativo != null)
                {
                    Canvas[] doNativo = nativo.GetComponentsInParent<Canvas>(true);
                    if (doNativo != null && doNativo.Length > 0)
                    {
                        return doNativo[0];
                    }
                }

                CharacterMenusManager menu = CharacterMenusManager.Instance;
                if (menu != null)
                {
                    Canvas[] doMenu = menu.GetComponentsInParent<Canvas>(true);
                    if (doMenu != null && doMenu.Length > 0)
                    {
                        return doMenu[0];
                    }
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: nao deu para localizar o Canvas do jogo (o scaler fica o padrao): " + e.Message);
            }

            return null;
        }

        /// <summary>O MOLDE do botao fechar: RSTV-22 — o CANCEL/CLOSE NATIVO do proprio modal (botao de
        /// rodape, combina com a janela); fallback no <c>closeButton</c> do SkillTreeManager e, por fim,
        /// o primeiro Button do dono (a option row — o molde que deixava o botao feio).</summary>
        private static Button BotaoMolde(Transform dono, RoguelikeSkillTreeRemovalWindow modal)
        {
            try
            {
                if (modal != null && modal.CancelButton != null && modal.CancelButton.Root != null)
                {
                    Button doModal = modal.CancelButton.Root.GetComponent<Button>();
                    if (doModal != null)
                    {
                        return doModal;
                    }
                }

                SkillTreeManager nativo = LoadableUIWindow<SkillTreeManager>.Instance;
                if (nativo != null && nativo.closeButton != null)
                {
                    return nativo.closeButton;
                }

                if (dono != null)
                {
                    Button[] botoes = dono.GetComponentsInChildren<Button>(true);
                    if (botoes != null && botoes.Length > 0)
                    {
                        return botoes[0];
                    }
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: falha ao resolver o molde do botao fechar: " + e.Message);
            }

            return null;
        }

        /// <summary>O MOLDE do titulo: RSTV-22 — o <c>TitleText</c> do proprio modal (mesmo estilo do
        /// cabecalho onde a janela nasce); fallback no primeiro TMP do dono e no StatusText do
        /// SkillTreeManager.</summary>
        private static TextMeshProUGUI TextoMolde(Transform dono, RoguelikeSkillTreeRemovalWindow modal)
        {
            try
            {
                if (modal != null && modal.TitleText != null)
                {
                    return modal.TitleText;
                }

                if (dono != null)
                {
                    TextMeshProUGUI[] textos = dono.GetComponentsInChildren<TextMeshProUGUI>(true);
                    if (textos != null && textos.Length > 0)
                    {
                        return textos[0];
                    }
                }

                SkillTreeManager nativo = LoadableUIWindow<SkillTreeManager>.Instance;
                if (nativo != null && nativo.StatusText != null)
                {
                    return nativo.StatusText;
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: falha ao resolver o molde do titulo: " + e.Message);
            }

            return null;
        }

        private static void CopiarScaler(Canvas origem, CanvasScaler destino)
        {
            if (destino == null)
            {
                return;
            }

            if (origem == null)
            {
                return;
            }

            try
            {
                CanvasScaler scaler = origem.GetComponent<CanvasScaler>();
                if (scaler == null)
                {
                    return;
                }

                destino.uiScaleMode = scaler.uiScaleMode;
                destino.referenceResolution = scaler.referenceResolution;
                destino.screenMatchMode = scaler.screenMatchMode;
                destino.matchWidthOrHeight = scaler.matchWidthOrHeight;
                destino.referencePixelsPerUnit = scaler.referencePixelsPerUnit;
                destino.scaleFactor = scaler.scaleFactor;
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-21: nao deu para copiar o CanvasScaler do jogo: " + e.Message);
            }
        }

        private static void Esticar(RectTransform rt, float esquerda, float baixo, float direita, float topo)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = new Vector2(esquerda, baixo);
            rt.offsetMax = new Vector2(0f - direita, 0f - topo);
            rt.localScale = Vector3.one;
            rt.localRotation = Quaternion.identity;
        }
    }
}
