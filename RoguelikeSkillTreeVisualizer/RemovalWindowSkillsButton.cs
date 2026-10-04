using System;
using Burst2Flame;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-20 — o botao `Skills` no CABECALHO do modal "Remove Skill Trees"
    /// (<see cref="RoguelikeSkillTreeRemovalWindow"/>, l.170602).
    ///
    /// O QUE ELE FAZ: fica no topo a DIREITA do titulo (o espaco escuro livre, acima da
    /// <c>TitleDivider</c>) e abre o viewer read-only do RSTV para o personagem DO PROPRIO MODAL
    /// (<c>RoguelikeSkillTreeRemovalWindow.CurrentCharacter</c>, l.170661/170727).
    ///
    /// RSTV-21: o caminho de abertura e a JANELA PROPRIA do mod (<see cref="SkillTreesWindow"/>, via
    /// <see cref="SkillTreesTab.AbrirJanela"/>), NAO mais a aba do inventario: o modal vive na tela de
    /// PARTY SELECT, onde <c>CharacterMenusManager.OpenCharacterMenu</c> nao abre (o personagem nao
    /// esta em <c>AllMyCharacters</c>) e o clique nao mostrava nada. O CONTEUDO e o mesmo da aba
    /// "All Trees" (as funcoes de montagem sao as mesmas) — muda so o hospedeiro do painel.
    ///
    /// COMO O BOTAO NASCE (contrato da RSTV-2/RSTV-5): e um CLONE de um botao NATIVO do proprio modal
    /// (o `Root` do `CancelButton`; fallback no `AcceptButton`) — assim herda sprite, estados
    /// (normal/hover/pressed) e o texto do jogo, sem inventar visual. Duas armadilhas tratadas aqui:
    ///
    ///  1. ANTI-DUPLICACAO (por NOME + por JANELA): a janela do modal e UM objeto so, ligado/desligado
    ///     pelo jogo a cada abertura (`Open` l.170723). O `Ensure` e idempotente — a 2a abertura
    ///     ENCONTRA o clone ja existente e apenas reafirma o alvo/rotulo; nunca cria um segundo
    ///     botao. Se a janela em si for recriada (instancia nova), o clone antigo e destruido antes.
    ///  2. LISTENER SERIALIZADO (RSTV-12): o botao molde carrega um `onClick` PERSISTENTE no prefab
    ///     (o do Cancel — fecharia o modal). O `RemoveAllListeners()` NAO limpa a lista serializada;
    ///     por isso a INSTANCIA do evento e trocada (`SelectPartyButton.ClearClickListeners`) antes de
    ///     instalar o nosso listener.
    ///
    /// READ-ONLY (o que NAO precisa ser blindado aqui): o viewer continua sendo SOMENTE LEITURA pelas
    /// camadas que ja existem. O unico caminho do jogo que GRAVA skill ao sair do viewer e
    /// <c>SkillTreeManager.AcceptSkillChanges(closeMenu:true)</c> (l.177650), chamado pelo
    /// <c>CharacterMenusManager.CloseSkillTreeMenu</c> — e ele comeca com <c>if (!needsAccept)
    /// return;</c>, ou seja, so escreve se o jogador tiver mexido na arvore. O clique que poe
    /// <c>needsAccept</c> em true e barrado pelos prefixos do <c>Patches.cs</c>
    /// (<c>SkillTreeItemTogglePatch</c> / <c>ResetSkillPoints</c>) enquanto a sessao read-only esta
    /// ativa; a rede final e a higienizacao do proprio <c>AcceptSkillChanges</c>. Este arquivo NAO
    /// adiciona nenhum caminho de escrita — o clique chama o <c>SkillTreesTab.AbrirJanela</c> (a janela
    /// propria do RSTV-21), que tambem so LE o personagem.
    ///
    /// O modal nao tem metodo `Update` publico nem gancho de abrir proprio alem do `Open`, entao o
    /// gancho e o postfix de `RoguelikeSkillTreeRemovalWindow.Open(Character)` (Patches.cs).
    /// </summary>
    internal static class RemovalWindowSkillsButton
    {
        internal const string ButtonName = "RstvRemovalSkillsButton";
        internal const string Label = "Skills";

        /// <summary>Texto do HEADING do modal (o titulo cujo lado direito o botao ocupa). E o rotulo
        /// pelo qual o probe de runtime acha o container do cabecalho (ver <see cref="ProbeFaixaDoTitulo"/>).</summary>
        internal const string TituloEsperado = "Remove Skill Trees";

        /// <summary>Lado do botao (quadrado de toque no canto do cabecalho).</summary>
        internal const float Lado = 44f;

        /// <summary>Margem do botao ate o canto superior direito da area do cabecalho.</summary>
        private const float Margem = 8f;

        /// <summary>Largura minima para aceitar como "faixa do cabecalho" o pai achado pelo probe.
        /// Abaixo disso o pai e so a caixa do texto do titulo (o botao cairia em cima do heading) e o
        /// probe e descartado em favor do `Panel`.</summary>
        private const float LarguraMinimaDaFaixa = 120f;

        /// <summary>Dono atual (a instancia viva do modal). Trocar de instancia = recriar o clone.</summary>
        private static RoguelikeSkillTreeRemovalWindow _window;
        private static GameObject _button;

        private static string _reasonLogged;

        /// <summary>
        /// Idempotente por INSTANCIA de <see cref="RoguelikeSkillTreeRemovalWindow"/>. Chamado pelo
        /// postfix de <c>Open(Character)</c> — roda em TODA abertura do modal, inclusive re-abertura
        /// sobre a MESMA janela.
        /// </summary>
        internal static void Ensure(RoguelikeSkillTreeRemovalWindow window)
        {
            try
            {
                EnsureInternal(window);
            }
            catch (Exception e)
            {
                Fail("excecao durante a injecao (" + e.GetType().Name + "): " + e.Message, true);
                Plugin.Log.LogError("RSTV-20: falha ao injetar o botao do modal 'Remove Skill Trees': " + e);
            }
        }

        private static void EnsureInternal(RoguelikeSkillTreeRemovalWindow window)
        {
            if (window == null)
            {
                Fail("a instancia do modal 'Remove Skill Trees' chegou nula", false);
                return;
            }

            if (!Plugin.RemocaoBotaoLigado)
            {
                // Pedido explicito no config: nao e falha, e o comportamento desejado.
                Fail("AtivarBotaoNaRemocao=false no arquivo de config", false);
                return;
            }

            // Ja existe clone DESTA janela? Reafirma alvo/rotulo e sai (anti-duplicacao por janela).
            if (_window == window && _button != null)
            {
                Reafirmar();
                return;
            }

            // Janela NOVA (instancia trocada) com clone antigo vivo: o clone morre junto com a janela
            // antiga; se ainda existir por algum motivo, some com ele antes de criar o proximo.
            if (_button != null && _window != window)
            {
                UnityEngine.Object.Destroy(_button);
                _button = null;
            }

            // ---- resolucao 1: o MOLDE nativo (clona um botao do proprio modal) ---------------------
            // Preferencia: o `CancelButton` (existe sempre; o `AcceptButton` fica escondido no estado
            // locked, l.170839). Fallback: `AcceptButton`. Sem nenhum dos dois, NAO ha clone nativo.
            Button molde = null;
            string origemMolde = null;

            if (window.CancelButton != null && window.CancelButton.Root != null)
            {
                molde = window.CancelButton.Root.GetComponent<Button>();
                origemMolde = "CancelButton";
            }

            if (molde == null && window.AcceptButton != null && window.AcceptButton.Root != null)
            {
                molde = window.AcceptButton.Root.GetComponent<Button>();
                origemMolde = "AcceptButton";
            }

            if (molde == null)
            {
                // Ultimo recurso: o primeiro Button filho do modal (contrato "clone nativo" preservado).
                Button[] botoes = window.GetComponentsInChildren<Button>(true);
                if (botoes != null && botoes.Length > 0)
                {
                    molde = botoes[0];
                    origemMolde = "primeiro Button filho do modal";
                }
            }

            if (molde == null)
            {
                Fail("o modal nao tem nenhum Button nativo para servir de molde (CancelButton/AcceptButton ausentes)", true);
                return;
            }

            if (molde.transform == null || molde.transform.parent == null)
            {
                Fail("o botao molde ('" + origemMolde + "') esta sem Transform ou sem pai na hierarquia", true);
                return;
            }

            // ---- resolucao 2: o PAI (a faixa do cabecalho) ------------------------------------------
            // A HIERARQUIA DO CABECALHO NAO EXISTE NO ASSEMBLY: o modal monta o heading em runtime a
            // partir do prefab (o `TitleText` e so um TextMeshProUGUI publico; o container/ancoras
            // vivem no asset). Por isso o container NAO e presumido por nome: ele e DESCOBERTO em
            // runtime por um PROBE sobre o TITULO RENDERIZADO (o MESMO padrao de navegacao por rotulo
            // renderizado usado no resto do mod) — acha o TMP cujo texto e o heading localizado e usa
            // o PAI dele como faixa do cabecalho. O botao assim amarra ao TITULO que o pedido nomeia
            // ("a direita do titulo"), sem depender do nome do GameObject no prefab.
            //
            // A cadeia abaixo e FALLBACK (prefab sem o titulo esperado, ou titulo ainda nao desenhado):
            //   `Panel` (campo publico provado, l.170631) -> pai do `TitleText` -> pai da
            //   `TitleDivider` -> o proprio modal. Todos os caminhos poem o botao no canto superior
            //   direito da faixa, que e o espaco escuro livre a direita do heading.
            RectTransform pai = null;
            string origemPai = null;
            string tituloRenderizado;

            RectTransform faixaDoTitulo = ProbeFaixaDoTitulo(window, out tituloRenderizado);
            if (faixaDoTitulo != null)
            {
                pai = faixaDoTitulo;
                origemPai = "probe do titulo renderizado (\"" + tituloRenderizado + "\")";
            }
            else if (window.Panel != null)
            {
                pai = window.Panel;
                origemPai = "Panel (fallback: o probe do titulo nao achou uma faixa larga)";
            }
            else if (window.TitleText != null && window.TitleText.rectTransform != null)
            {
                pai = window.TitleText.rectTransform.parent as RectTransform;
                origemPai = "pai do TitleText (fallback)";
            }
            else if (window.TitleDivider != null)
            {
                pai = window.TitleDivider.rectTransform.parent as RectTransform;
                origemPai = "pai da TitleDivider (fallback)";
            }
            else
            {
                pai = window.transform as RectTransform;
                origemPai = "transform do proprio modal (fallback)";
            }

            if (pai == null)
            {
                Fail("nao foi possivel resolver a area do cabecalho (probe do titulo/Panel/TitleText/TitleDivider nulos)", true);
                return;
            }

            // ---- clona (ou reaproveita) o botao ----------------------------------------------------
            Transform existente = Procurar(window.transform);
            GameObject clone;
            if (existente != null)
            {
                clone = existente.gameObject;
                if (clone.transform.parent != pai)
                {
                    clone.transform.SetParent(pai, false);
                }
            }
            else
            {
                clone = UnityEngine.Object.Instantiate(molde.gameObject, pai);
                clone.name = ButtonName;
            }

            clone.transform.SetAsLastSibling();

            RectTransform rt = clone.GetComponent<RectTransform>();
            if (rt == null)
            {
                Fail("o clone do botao ficou sem RectTransform", true);
                return;
            }

            // Canto SUPERIOR DIREITO do pai, recuado pela margem. Com anchor/pivot (1,1) a posicao e
            // EXATA sem depender de layout pendente (nao precisa medir cantos de mundo).
            rt.anchorMin = new Vector2(1f, 1f);
            rt.anchorMax = new Vector2(1f, 1f);
            rt.pivot = new Vector2(1f, 1f);
            rt.localScale = Vector3.one;
            rt.localRotation = Quaternion.identity;
            rt.sizeDelta = new Vector2(Lado, Lado);
            rt.anchoredPosition = new Vector2(0f - Margem, 0f - Margem);

            // O LayoutElement herdado do botao de rodape e inerte sem LayoutGroup no pai; com
            // `ignoreLayout` fica inerte em QUALQUER pai (o clone nao deve entrar em contas de layout).
            LayoutElement le = clone.GetComponent<LayoutElement>();
            if (le != null)
            {
                le.ignoreLayout = true;
            }

            // O rotulo/estado nao podem ser reescritos pelos localizadores do jogo (o clone herda os
            // componentes do molde).
            SelectPartyButton.DisableLocalizers(clone);
            EnsureLabel(clone);

            Button botao = clone.GetComponent<Button>();
            if (botao == null)
            {
                Fail("o clone do botao ficou sem componente Button", true);
                return;
            }

            // RSTV-12: trocar a INSTANCIA do evento descarta o onClick SERIALIZADO do molde (o
            // "Cancel" fecharia o modal) antes de instalar o listener read-only.
            SelectPartyButton.ClearClickListeners(botao);
            botao.onClick.AddListener(new UnityAction(OnClick));
            botao.interactable = true;

            clone.SetActive(window.gameObject.activeSelf);

            _window = window;
            _button = clone;
            _reasonLogged = null;

            Plugin.Log.LogInfo(
                "RSTV-20: botao '" + Label + "' injetado no cabecalho do modal 'Remove Skill Trees' " +
                "(" + Lado.ToString("0.#") + "x" + Lado.ToString("0.#") + " px, canto superior direito de '" +
                pai.name + "' via " + origemPai + "), clone de '" + molde.gameObject.name + "' (" + origemMolde +
                "; onClick limpo -> SkillTreesTab.AbrirJanela(CurrentCharacter, RemocaoDeArvores) [RSTV-21: janela propria, sem inventario]; " +
                "janela=" + window.name + ".");
        }

        /// <summary>
        /// Reabertura sobre a MESMA janela: o clone ja existe — so reafirma rotulo/estado (o alvo e
        /// lido do `CurrentCharacter` na hora do clique, nunca cacheado).
        /// </summary>
        private static void Reafirmar()
        {
            if (_button == null || _window == null)
            {
                return;
            }

            try
            {
                if (_button.activeSelf != _window.gameObject.activeSelf)
                {
                    _button.SetActive(_window.gameObject.activeSelf);
                }

                EnsureLabel(_button);
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-20: nao deu para reafirmar o botao do modal (" +
                                      e.GetType().Name + "): " + e.Message);
            }
        }

        /// <summary>
        /// O clique: abre o viewer read-only do RSTV para o personagem DO MODAL, lido do
        /// <c>CurrentCharacter</c> no exato momento do clique (nunca cacheado — o jogo troca o
        /// personagem a cada abertura do modal, l.170727).
        ///
        /// RSTV-21: o caminho aqui NAO e mais o <c>SkillTreesTab.Abrir</c> (que abre o INVENTARIO e
        /// seleciona a aba). O modal vive na tela de PARTY SELECT, onde <c>OpenCharacterMenu</c> NAO
        /// abre (o personagem nao esta em <c>AllMyCharacters</c>) — o clique nao mostrava nada. A visao
        /// passa a abrir numa JANELA PROPRIA (<see cref="SkillTreesWindow"/>), ancorada na janela do
        /// modal (de onde saem os moldes nativos e o ciclo de vida: fechou o modal, a janela fecha).
        /// O CONTEUDO e o mesmo "All Skill Trees" da run — muda so o hospedeiro.
        /// </summary>
        private static void OnClick()
        {
            try
            {
                RoguelikeSkillTreeRemovalWindow janela = _window;
                Character alvo = janela != null ? janela.CurrentCharacter : null;
                if (alvo == null)
                {
                    Plugin.Log.LogWarning("RSTV-20: clique no botao '" + Label +
                                          "' sem personagem no modal (CurrentCharacter nulo) — nada foi aberto.");
                    return;
                }

                Plugin.Log.LogInfo("RSTV-20: clique no botao '" + Label + "' do modal -> '" + alvo.CharacterName +
                                   "' (nivel " + alvo.Level + ") na JANELA read-only de todas as arvores (RSTV-21).");
                SkillTreesTab.AbrirJanela(alvo, ReadOnlyContext.RemocaoDeArvores, janela.transform);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-20: falha no clique do botao do modal: " + e);
            }
        }

        /// <summary>Rotula o clone com `Skills` (localizado), reusando o `Text` herdado do molde.</summary>
        private static void EnsureLabel(GameObject clone)
        {
            TextMeshProUGUI label = clone.GetComponentInChildren<TextMeshProUGUI>(true);
            if (label == null)
            {
                Fail("o clone do botao ficou SEM TextMeshProUGUI — botao sem rotulo", true);
                return;
            }

            label.text = OptionsManager.Localize(Label);
        }

        /// <summary>
        /// PROBE de runtime do container do cabecalho: acha, entre os textos do modal, o TMP cujo
        /// conteudo e o HEADING localizado (<see cref="TituloEsperado"/>) e devolve o PAI dele.
        ///
        /// POR QUE PROBE e nao um campo: a hierarquia/ancoras do cabecalho vivem no PREFAB (asset) e
        /// nao no assembly — o unico campo publico provado e o <c>TitleText</c> (um TMP), nao o
        /// container. Navegar pelo ROTULO RENDERIZADO e o padrao do mod para achar algo cuja posicao
        /// so existe em runtime, e ainda deixa o botao amarrado ao TITULO (nao a um nome de GameObject).
        ///
        /// Guarda: so aceita o pai se ele for uma faixa LARGA (<see cref="LarguraMinimaDaFaixa"/>) —
        /// uma caixa estreita seria o retangulo do proprio texto e o botao cairia sobre o heading.
        /// Devolve null (o chamador cai para o `Panel`) quando nao acha o titulo ou a faixa e estreita.
        /// </summary>
        private static RectTransform ProbeFaixaDoTitulo(RoguelikeSkillTreeRemovalWindow window, out string textoAchado)
        {
            textoAchado = null;
            try
            {
                string esperado = OptionsManager.Localize(TituloEsperado);
                if (string.IsNullOrEmpty(esperado))
                {
                    return null;
                }

                TextMeshProUGUI[] textos = window.GetComponentsInChildren<TextMeshProUGUI>(true);
                for (int i = 0; i < textos.Length; i++)
                {
                    TextMeshProUGUI texto = textos[i];
                    if (texto == null || texto.text == null || texto.rectTransform == null)
                    {
                        continue;
                    }

                    if (texto.text.Trim() != esperado.Trim())
                    {
                        continue;
                    }

                    RectTransform pai = texto.rectTransform.parent as RectTransform;
                    if (pai == null)
                    {
                        return null;
                    }

                    float largura = pai.rect.width;
                    if (largura <= 1f)
                    {
                        largura = pai.sizeDelta.x;
                    }

                    if (largura < LarguraMinimaDaFaixa)
                    {
                        Plugin.Log.LogInfo("RSTV-20: o probe achou o titulo renderizado, mas o container " +
                                           "dele e estreito (" + largura.ToString("0.#") + " px < " +
                                           LarguraMinimaDaFaixa.ToString("0.#") + ") — usando o `Panel`.");
                        return null;
                    }

                    textoAchado = texto.text;
                    return pai;
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-20: falha no probe do titulo renderizado (" +
                                      e.GetType().Name + "): " + e.Message);
            }

            return null;
        }

        /// <summary>Acha um clone NOSSO em qualquer profundidade (a janela pode reusar subarvores).</summary>
        private static Transform Procurar(Transform raiz)
        {
            if (raiz == null)
            {
                return null;
            }

            Transform[] todos = raiz.GetComponentsInChildren<Transform>(true);
            for (int i = 0; i < todos.Length; i++)
            {
                Transform t = todos[i];
                if (t != null && t.name == ButtonName)
                {
                    return t;
                }
            }

            return null;
        }

        /// <summary>
        /// Escreve no log POR QUE o botao nao foi injetado, UMA vez por motivo (o postfix roda a cada
        /// abertura do modal; um estado estavel nao pode inundar o LogOutput.log).
        /// </summary>
        private static void Fail(string motivo, bool aviso)
        {
            if (_reasonLogged == motivo)
            {
                return;
            }

            _reasonLogged = motivo;
            string linha = "RSTV DIAG: botao '" + Label + "' do modal 'Remove Skill Trees' NAO injetado — " +
                           motivo + ".";
            if (aviso)
            {
                Plugin.Log.LogWarning(linha);
            }
            else
            {
                Plugin.Log.LogInfo(linha);
            }
        }
    }
}
