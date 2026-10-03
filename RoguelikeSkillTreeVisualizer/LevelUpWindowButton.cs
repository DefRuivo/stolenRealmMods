using System;
using Burst2Flame;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-11b: o botao `Skills` DENTRO da janela do level-up (proposta C do brainstorm da RSTV-10).
    ///
    /// POR QUE ESTE BOTAO EXISTE (e por que ele aposenta o re-parent da RSTV-9)
    /// ---------------------------------------------------------------------
    /// A RSTV-9 resolvia o level-up RE-PARENTEANDO o clone do HUD para dentro do `SkillSelectWindow`
    /// enquanto a janela estava aberta. O prefab (RSTV-10) mostrou duas coisas que tornam esse caminho
    /// fragil: (1) o `SkillSelectWindow` [680553] e TELA CHEIA (anchor 0,0..1,1), entao o "canto
    /// superior direito" do re-parent caia no canto da TELA, nao no do painel; (2) ele e o proprio GO
    /// que o jogo liga/desliga no level-up. Em vez de mover o botao do HUD de casa, criamos um botao
    /// PROPRIO da janela: um CLONE do `AcceptButton` [503691] que nasce como filho DIRETO do
    /// `SkillSelectWindow` — FORA do `Content` [680573], que tem `VerticalLayoutGroup` +
    /// `ContentSizeFitter`.
    ///
    /// AS DUAS ARMADILHAS DO PREFAB (RSTV-10, secao 4) E COMO SAO TRATADAS AQUI
    /// --------------------------------------------------------------------
    ///  1. Clonar para DENTRO do `Content` reflui o painel e re-dimensiona o `ContentSizeFitter`.
    ///     Aqui o clone e filho DIRETO do `SkillSelectWindow` [680553], que NAO tem LayoutGroup: o
    ///     `LayoutElement` herdado do `AcceptButton` fica INERTE e o painel nao se mexe;
    ///  2. o clone herda o `Button.onClick` SERIALIZADO do original (que chama
    ///     `ConfirmLevelUpSelection` — avanco de level-up = ESCRITA). Por isso `RemoveAllListeners()`
    ///     antes de instalar o nosso listener (`RunButton.OpenForTarget`, o MESMO do botao da run).
    ///     O rotulo "Accept/Next" e escrito pelo `RoguelikeManager.CurLevelUpStage` (l.168718) no
    ///     `AcceptButtonText` do ORIGINAL; o clone tem o proprio `Text`, entao o rotulo dele e
    ///     desligado dos localizadores (`DisableLocalizers`) e reescrito para `Skills`.
    ///
    /// POSICAO: perto do canto SUPERIOR DIREITO do painel VISIVEL (`Content` [680573], ~293x536 px
    /// centralizado), NAO do `SkillSelectWindow` (que e a tela inteira). O alvo e lido do proprio
    /// `Content` em espaco de mundo e convertido para o espaco local da janela.
    ///
    /// IDEMPOTENTE por JANELA: o postfix de `OpenSkillSelectWindow` roda de novo a cada personagem
    /// da fila de level-up (`RoguelikeManager.ConfirmLevelUpSelection`, l.168998), sobre o MESMO
    /// `SkillSelectWindow`. A segunda chamada e NO-OP (`_janela == janela && _button != null`).
    /// </summary>
    internal static class LevelUpWindowButton
    {
        internal const string ButtonName = "RstvLevelUpSkillsButton";
        internal const string Label = "Skills";
        internal const string LabelChildName = "RstvLevelUpLabel";

        /// <summary>Lado do botao dentro da janela (quadrado de toque, nao a barra do Accept).</summary>
        internal const float Lado = 44f;

        /// <summary>Margem do botao ate o canto superior direito do painel `Content`.</summary>
        private const float Margem = 8f;

        private static GameObject _janela;
        private static GameObject _button;
        private static string _reasonLogged;

        /// <summary>
        /// Idempotente por JANELA do level-up. Chamado pelo postfix de
        /// `RoguelikeManager.OpenSkillSelectWindow` (o GO que o jogo liga/desliga no level-up).
        /// </summary>
        internal static void Ensure(RoguelikeManager rok)
        {
            try
            {
                EnsureInternal(rok);
                Refresh();
            }
            catch (Exception e)
            {
                Fail("excecao durante a injecao (" + e.GetType().Name + "): " + e.Message, true);
                Plugin.Log.LogError("RSTV: falha ao injetar o botao da janela do level-up: " + e);
            }
        }

        private static void EnsureInternal(RoguelikeManager rok)
        {
            if (rok == null)
            {
                Fail("a instancia do RoguelikeManager chegou nula", false);
                return;
            }

            if (!Plugin.RunBotaoLigado)
            {
                // Pedido explicito no config: nao e falha, e o comportamento desejado.
                Fail("AtivarBotaoNaRun=false no arquivo de config", false);
                return;
            }

            GameObject janela = rok.SkillSelectWindow;
            if (janela == null)
            {
                Fail("RoguelikeManager.SkillSelectWindow esta nulo (o campo do prefab nao carregou)", true);
                return;
            }

            // RSTV-14: o gancho so roda quando o jogo ABRE a janela (`OpenSkillSelectWindow`), mas a
            // guarda deixa o contrato explicito — fora de uma janela ATIVA o `Ensure` nao injeta
            // nada. Sem ela, um `Ensure` chamado com a janela ja fechada criaria o clone "fora de
            // hora", e ele reapareceria sobre a arvore depois que o ciclo da janela terminou.
            if (!janela.activeSelf)
            {
                Fail("a janela do level-up (" + janela.name + ") NAO esta ativa — nao injetar fora de hora", false);
                return;
            }

            // IDEMPOTENTE por janela: a 2a chamada (proximo personagem da fila, MESMA janela) e no-op.
            if (_janela == janela && _button != null)
            {
                return;
            }

            // Um clone VIVO de OUTRA janela (a janela foi recriada): some com o antigo antes.
            if (_button != null && _janela != janela)
            {
                UnityEngine.Object.Destroy(_button);
                _button = null;
            }

            Button original = rok.AcceptButton;
            if (original == null)
            {
                Fail("RoguelikeManager.AcceptButton esta nulo — sem molde nao ha clone", true);
                return;
            }

            if (original.transform == null)
            {
                Fail("o 'Accept Btn' molde esta sem Transform", true);
                return;
            }

            RectTransform janelaRt = janela.GetComponent<RectTransform>();
            if (janelaRt == null)
            {
                Fail("o SkillSelectWindow esta sem RectTransform (nao da para ancorar o botao)", true);
                return;
            }

            // O pai do AcceptButton e o `Content` [680573]: tem VerticalLayoutGroup + ContentSizeFitter.
            // Ele e o MOLDE do rect do painel (usado so para medir o canto), NUNCA o pai do clone.
            RectTransform contentRt = original.transform.parent as RectTransform;
            if (contentRt == null)
            {
                Fail("o pai do 'Accept Btn' (o painel Content) nao e RectTransform — sem ele nao sei onde fica o canto do painel", true);
                return;
            }

            Transform existing = janela.transform.Find(ButtonName);
            GameObject clone;
            if (existing != null)
            {
                clone = existing.gameObject;
            }
            else
            {
                // Filho DIRETO do SkillSelectWindow (TELA CHEIA), FORA do Content: sem layout group,
                // o LayoutElement herdado fica inerte e o painel NAO reflui.
                clone = UnityEngine.Object.Instantiate(original.gameObject, janela.transform);
                clone.name = ButtonName;
            }

            RectTransform rt = clone.GetComponent<RectTransform>();
            if (rt == null)
            {
                Fail("o clone do 'Accept Btn' ficou sem RectTransform", true);
                return;
            }

            // O nome/rotulo nao podem ser reescritos pelos localizadores do jogo (o clone herda os
            // componentes do AcceptButton). O rotulo "Accept/Next" e escrito no ORIGINAL pelo
            // CurLevelUpStage (l.168718); aqui o clone e limpo e rotulado como `Skills`.
            SelectPartyButton.DisableLocalizers(clone);
            EnsureLabel(clone);

            AnchorToContentCorner(rt, janelaRt, contentRt);

            Button button = clone.GetComponent<Button>();
            if (button == null)
            {
                Fail("o clone do 'Accept Btn' ficou sem componente Button", true);
                return;
            }

            // O onClick SERIALIZADO do AcceptButton chama ConfirmLevelUpSelection (avanco de level-up
            // = ESCRITA): RSTV-12 — o `RemoveAllListeners()` NAO basta (ele limpa so a lista de
            // runtime e o persistente continua), entao a INSTANCIA do evento e trocada para descartar
            // a lista serializada antes de instalar o listener read-only.
            SelectPartyButton.ClearClickListeners(button);
            button.onClick.AddListener(new UnityAction(RunButton.OpenForTarget));
            button.interactable = true;

            _janela = janela;
            _button = clone;
            _reasonLogged = null;

            Plugin.Log.LogInfo(
                "RSTV-11b: botao '" + Label + "' injetado DENTRO da janela do level-up (" + janela.name +
                "), filho direto (fora do Content, sem reflow); " + Lado.ToString("0.#") + "x" + Lado.ToString("0.#") +
                " px no canto superior direito do painel Content; onClick limpo -> RunButton.OpenForTarget().");
        }

        /// <summary>
        /// RSTV-14 — o CICLO DE VIDA do botao: ele existe enquanto a JANELA existe, mas so fica VISIVEL
        /// no estagio de SKILLS do level-up.
        ///
        /// Por que isto existe (o defeito do dono: "o botao fica voando no level-up attributes"): o
        /// `Ensure` so roda no postfix de `OpenSkillSelectWindow`. Depois disso, `RoguelikeManager`
        /// troca o estagio SEM fechar a janela — `CurLevelUpStage` (l.168697) liga/desliga as secoes
        /// (`SkillSection`/`ItemSectionInventory`/`AttributeSection`) e o painel `Content` muda de
        /// tamanho, mas o `SkillSelectWindow` continua ativo. O clone (filho da janela) continuava
        /// visivel no estagio de ATRIBUTOS, com a posicao presa ao canto ANTIGO do painel — o botao
        /// "voando". Aqui, a cada quadro: mostra o clone SO com a janela ativa E no estagio
        /// `LevelUpStage.Skills`; nos outros estagios (Items/Attributes/Currency) ele some. Ao voltar
        /// ao estagio de skills (proximo personagem da fila), o clone e RE-ANcorado no canto atual do
        /// `Content`, porque o painel pode ter mudado de metragem no meio do ciclo.
        ///
        /// Chamado pelo `RstvHost.Update` (10x por segundo) e pelo proprio `Ensure` (idempotente: a
        /// 2a chamada na mesma janela reafirma a visibilidade em vez de recriar o botao).
        /// </summary>
        internal static void Refresh()
        {
            try
            {
                GameObject botao = _button;
                GameObject janela = _janela;
                if (botao == null || janela == null)
                {
                    return;
                }

                RoguelikeManager rok = RoguelikeManager.Instance;
                bool mostrar = rok != null
                    && rok.SkillSelectWindow == janela
                    && janela.activeSelf
                    && rok.CurLevelUpStage == LevelUpStage.Skills;

                if (botao.activeSelf == mostrar)
                {
                    return;
                }

                botao.SetActive(mostrar);

                if (!mostrar)
                {
                    return;
                }

                // Voltou ao estagio de SKILLS: o painel Content pode ter mudado de metragem enquanto
                // o botao estava escondido — re-ancora para o canto ATUAL (sem isso ele "voa").
                RectTransform rt = botao.GetComponent<RectTransform>();
                RectTransform janelaRt = janela.GetComponent<RectTransform>();
                Button molde = rok != null ? rok.AcceptButton : null;
                RectTransform contentRt = molde != null && molde.transform != null
                    ? molde.transform.parent as RectTransform
                    : null;
                if (rt != null && janelaRt != null && contentRt != null)
                {
                    AnchorToContentCorner(rt, janelaRt, contentRt);
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: falha ao sincronizar o botao da janela do level-up (" +
                                      e.GetType().Name + "): " + e.Message);
            }
        }

        /// <summary>
        /// Rotula o clone com `Skills` (localizado). O clone herdou o `Text` do `AcceptButton`, entao
        /// normalmente ja ha um TMP; sem ele o motivo vai para o log (o botao ainda existe, so sem rotulo).
        /// </summary>
        private static void EnsureLabel(GameObject clone)
        {
            TextMeshProUGUI label = clone.GetComponentInChildren<TextMeshProUGUI>(true);
            if (label == null)
            {
                Fail("o clone do 'Accept Btn' ficou SEM TextMeshProUGUI — botao sem rotulo", true);
                return;
            }

            label.text = OptionsManager.Localize(Label);
        }

        /// <summary>
        /// Ancora o clone no canto SUPERIOR DIREITO do painel `Content` (nao da tela). O alvo e lido do
        /// rect de mundo do painel e convertido para o espaco local da janela (que e tela cheia).
        /// </summary>
        internal static void AnchorToContentCorner(RectTransform rt, RectTransform janela, RectTransform content)
        {
            Canvas.ForceUpdateCanvases();

            Vector3[] cantos = new Vector3[4];
            content.GetWorldCorners(cantos);            // 0=BL, 1=TL, 2=TR, 3=BR
            Vector3 superiorDireito = janela.InverseTransformPoint(cantos[2]);

            // A janela tem anchor stretch total e pivot (0.5,0.5): o minimo do rect local e (-w/2,-h/2).
            Vector2 minimo = new Vector2(-janela.rect.width * janela.pivot.x,
                                         -janela.rect.height * janela.pivot.y);

            rt.anchorMin = Vector2.zero;                // (0,0)
            rt.anchorMax = Vector2.zero;
            rt.pivot = new Vector2(1f, 1f);             // pivo no canto superior direito do botao
            rt.localScale = Vector3.one;
            rt.localRotation = Quaternion.identity;
            rt.sizeDelta = new Vector2(Lado, Lado);

            // Com anchor (0,0) e pivot (1,1), o pivo fica em `minimo + anchoredPosition`.
            Vector2 alvo = new Vector2(superiorDireito.x - Margem, superiorDireito.y - Margem);
            rt.anchoredPosition = alvo - minimo;

            rt.SetAsLastSibling();                      // desenha/clica por cima dos irmaos da janela
        }

        /// <summary>
        /// Escreve no log POR QUE o botao nao foi injetado/posicionado, UMA vez por motivo (o postfix
        /// roda a cada personagem da fila; um estado estavel nao pode inundar o LogOutput.log).
        /// </summary>
        private static void Fail(string motivo, bool aviso)
        {
            if (_reasonLogged == motivo)
            {
                return;
            }

            _reasonLogged = motivo;
            string linha = "RSTV DIAG: botao '" + Label + "' da janela do level-up NAO injetado — " + motivo + ".";
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
