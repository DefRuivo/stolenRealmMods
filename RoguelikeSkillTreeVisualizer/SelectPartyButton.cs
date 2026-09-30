using System;
using Burst2Flame;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-2a: o botao quadrado a DIREITA do "Choose Powerups" (`CharacterChoiceManager.roguelikePowerupButton`,
    /// l.208096), na MESMA linha.
    ///
    /// Como: clonar o proprio botao nativo (mesmo sprite/estados/prefab — `Instantiate`, l.53 da analise),
    /// inserir como IRMAO logo apos ele e compensar a largura da linha pelo que foi adicionado. Assim
    /// nem a linha cresce, nem o `Accept Party` (l.208130) muda de tamanho.
    ///
    /// O sprite/tamanho/ancora vivem no prefab (`resources.assets`), que nao foi aberto: por isso tudo
    /// aqui e medido em runtime e logado (linha antes -> depois), para conferir em jogo.
    /// </summary>
    internal static class SelectPartyButton
    {
        internal const string ButtonName = "RstvSkillTreeButton";
        internal const string Label = "Skills";

        private static CharacterChoiceManager _owner;
        private static GameObject _button;

        // Diagnostico: POR QUE o botao nao esta injetado agora (um mod que injeta UI nao pode
        // falhar em silencio) e em qual instancia da tela isso ja foi reportado.
        private static string _reason;
        private static string _reasonLogged;
        private static CharacterChoiceManager _diagnosedFor;

        /// <summary>Idempotente por instancia de `CharacterChoiceManager`.</summary>
        internal static void Ensure(CharacterChoiceManager manager)
        {
            try
            {
                if (manager == null)
                {
                    Fail("a instancia da tela Select Party chegou nula", false);
                    return;
                }

                if (!Plugin.BotaoLigado)
                {
                    // Pedido explicito no config: nao e falha, e o comportamento desejado.
                    Fail("AtivarBotao=false no arquivo de config", false);
                    return;
                }

                Button original = manager.roguelikePowerupButton;
                if (original == null)
                {
                    Fail("o botao nativo do qual o clone nasce (roguelikePowerupButton / 'Choose Powerups') nao existe nesta tela", true);
                    return;
                }

                if (original.transform == null || original.transform.parent == null)
                {
                    Fail("o botao nativo 'Choose Powerups' esta sem Transform ou sem pai na hierarquia", true);
                    return;
                }

                if (_owner == manager && _button != null)
                {
                    return;
                }

                Transform parent = original.transform.parent;
                RectTransform srcRt = original.GetComponent<RectTransform>();
                if (srcRt == null)
                {
                    Fail("o botao nativo 'Choose Powerups' nao tem RectTransform (sem isso nao da para medir/repor a largura da linha)", true);
                    return;
                }

                // MEDIR ANTES de inserir o clone: com layout group, inserir o irmao ja reflui a linha
                // e a medida tirada depois seria a largura JA encolhida (encolheria duas vezes).
                float rowBefore = RowWidth(parent);
                float widthBefore = WorldWidth(srcRt);
                if (widthBefore <= 1f)
                {
                    widthBefore = srcRt.sizeDelta.x;
                }

                float side = SquareSide(original, srcRt);

                Transform existing = parent.Find(ButtonName);
                GameObject clone;
                if (existing != null)
                {
                    clone = existing.gameObject;
                }
                else
                {
                    clone = UnityEngine.Object.Instantiate(original.gameObject, parent);
                    clone.name = ButtonName;
                }

                clone.transform.SetSiblingIndex(original.transform.GetSiblingIndex() + 1);
                // escala/ancoras/rotacao vem do Instantiate (mesmo prefab) — nao mexer.

                RectTransform newRt = clone.GetComponent<RectTransform>();
                if (newRt == null)
                {
                    Fail("o clone do botao ficou sem RectTransform", true);
                    return;
                }

                TextMeshProUGUI cloneLabel = clone.GetComponentInChildren<TextMeshProUGUI>(true);
                if (cloneLabel != null)
                {
                    cloneLabel.text = OptionsManager.Localize(Label);
                }

                // O nome novo nao pode ser reescrito pelos componentes de localizacao do jogo
                // (senao a troca de idioma devolveria "Choose Powerups" nos dois botoes).
                DisableLocalizers(clone);

                clone.SetActive(original.gameObject.activeSelf);
                ApplySquareLayout(original, srcRt, clone, newRt, side, widthBefore, parent);

                Button button = clone.GetComponent<Button>();
                if (button != null)
                {
                    button.onClick.RemoveAllListeners();
                    button.onClick.AddListener(new UnityAction(OnClick));
                    button.interactable = PartyTargets.Resolve() != null;
                }

                _owner = manager;
                _button = clone;
                _reason = null;
                _reasonLogged = null;
                _diagnosedFor = manager;

                Plugin.Log.LogInfo(
                    "RSTV-2: botao '" + Label + "' injetado (" + side.ToString("0.#") + "x" + side.ToString("0.#") +
                    " px) a direita do Choose Powerups — largura da linha " + rowBefore.ToString("0.#") +
                    " -> " + RowWidth(parent).ToString("0.#") + " px; pai=" + parent.name +
                    "; grupo=" + DescribeGroup(parent));
            }
            catch (Exception e)
            {
                Fail("excecao durante a injecao (" + e.GetType().Name + "): " + e.Message, true);
                Plugin.Log.LogError("RSTV: falha ao injetar o botao: " + e);
            }
        }

        /// <summary>
        /// O `Update()` do jogo (l.208236) liga/desliga o `roguelikePowerupButton` conforme
        /// `Root.PlayingRoguelike`. O nosso clone precisa seguir o original (nada de botao orfao no
        /// Select Party da campanha) e ficar desabilitado quando a party LOCAL esta vazia.
        /// </summary>
        internal static void Mirror()
        {
            CharacterChoiceManager manager = CharacterChoiceManager.Instance;
            if (manager == null || !Plugin.BotaoLigado)
            {
                return;
            }

            if (_button == null)
            {
                // O botao nao existe: em vez de sumir em silencio, reporta UMA vez — com o motivo
                // e o estado da tela — qual foi o problema.
                if (_diagnosedFor != manager && manager.gameObject.activeInHierarchy)
                {
                    _diagnosedFor = manager;
                    DumpDiagnosis(manager);
                }

                return;
            }

            if (manager != _owner)
            {
                return;
            }

            Button original = manager.roguelikePowerupButton;
            if (original == null)
            {
                return;
            }

            bool shouldBeActive = original.gameObject.activeSelf;
            if (_button.activeSelf != shouldBeActive)
            {
                _button.SetActive(shouldBeActive);
            }

            Button button = _button.GetComponent<Button>();
            if (button != null)
            {
                bool canOpen = PartyTargets.Resolve() != null;
                if (button.interactable != canOpen)
                {
                    button.interactable = canOpen;
                }
            }
        }

        /// <summary>
        /// Registra o motivo pelo qual o botao nao esta injetado e o escreve no log (UMA vez por
        /// motivo, para nao inundar o LogOutput.log a cada 0,2 s). <paramref name="aviso"/> separa
        /// "deu errado" (aviso, em amarelo) de "foi desligado de proposito" (info).
        /// </summary>
        private static void Fail(string motivo, bool aviso)
        {
            _reason = motivo;
            if (_reasonLogged == motivo)
            {
                return;
            }

            _reasonLogged = motivo;
            if (aviso)
            {
                Plugin.Log.LogWarning("RSTV DIAG: botao '" + Label + "' NAO injetado — " + motivo + ".");
            }
            else
            {
                Plugin.Log.LogInfo("RSTV DIAG: botao '" + Label + "' desativado — " + motivo + ".");
            }
        }

        /// <summary>
        /// Resumo de diagnostico: quando a tela esta aberta e o botao nao apareceu, TODO o estado
        /// relevante vai para o log de uma vez (motivo + o que foi encontrado na hierarquia), para
        /// nao precisar de uma segunda rodada para descobrir o que faltou.
        /// </summary>
        private static void DumpDiagnosis(CharacterChoiceManager manager)
        {
            string tela = manager != null && manager.gameObject != null ? manager.gameObject.name : "AUSENTE";
            bool ativa = manager != null && manager.gameObject != null && manager.gameObject.activeInHierarchy;

            Button original = manager != null ? manager.roguelikePowerupButton : null;
            Transform parent = original != null && original.transform != null ? original.transform.parent : null;

            Plugin.Log.LogWarning(
                "RSTV DIAG: a tela Select Party esta aberta e o botao '" + Label + "' NAO foi injetado. " +
                "motivo=" + (_reason != null ? _reason : "desconhecido") +
                "; tela=" + tela +
                "; ativaNaHierarquia=" + ativa +
                "; botao nativo do clone=" + (original != null ? "presente" : "AUSENTE") +
                "; paiDoBotao=" + (parent != null ? parent.name : "AUSENTE") +
                "; grupo=" + DescribeGroup(parent) +
                "; party local=" + PartyTargets.LocalPartyCount() + " personagem(ns).");
        }

        private static void OnClick()
        {
            try
            {
                Character target = PartyTargets.Resolve();
                if (target == null)
                {
                    Plugin.Log.LogWarning("RSTV: clique sem personagem local na party — nada a abrir.");
                    return;
                }

                Plugin.Log.LogInfo("RSTV-2: clique no botao '" + Label + "' -> '" + target.CharacterName +
                                   "' (nivel " + target.Level + ").");
                SkillTreeReadOnly.Open(target);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no clique do botao: " + e);
            }
        }

        // ---------------------------------------------------------------------------------------
        // Layout
        // ---------------------------------------------------------------------------------------

        private static float SquareSide(Button original, RectTransform rect)
        {
            float height = rect.rect.height;
            if (height <= 1f)
            {
                height = rect.sizeDelta.y;
            }

            if (height <= 1f)
            {
                LayoutElement le = original.GetComponent<LayoutElement>();
                if (le != null && le.preferredHeight > 0f)
                {
                    height = le.preferredHeight;
                }
            }

            if (height <= 1f)
            {
                height = 44f;
            }

            return height;
        }

        private static void ApplySquareLayout(Button original, RectTransform srcRt, GameObject clone,
            RectTransform newRt, float side, float widthBefore, Transform parent)
        {
            float height = srcRt.rect.height > 1f ? srcRt.rect.height : side;

            LayoutElement srcLe = EnsureLayoutElement(original.gameObject);
            LayoutElement newLe = EnsureLayoutElement(clone);
            newLe.preferredWidth = side;
            newLe.minWidth = side;
            newLe.flexibleWidth = 0f;
            newLe.preferredHeight = height;
            newLe.minHeight = height;

            HorizontalOrVerticalLayoutGroup group = FindRowGroup(parent, original.transform);
            bool groupControlsWidth = group != null && group.childControlWidth && !group.childForceExpandWidth;
            float spacing = group != null ? group.spacing : 0f;

            if (group != null && group.childForceExpandWidth)
            {
                Plugin.Log.LogInfo("RSTV: linha usa LayoutGroup com childForceExpandWidth — o proprio grupo " +
                                   "acomoda o filho novo (sem compensacao manual de largura).");
            }
            else if (groupControlsWidth)
            {
                // Caso A: o grupo dimensiona os filhos pelo LayoutElement.
                float srcPreferred = srcLe.preferredWidth > 0f ? srcLe.preferredWidth : widthBefore;
                float shrinkBy = side + spacing; // o grupo tambem insere um espacamento a mais
                float newPreferred = Mathf.Max(1f, srcPreferred - shrinkBy);
                srcLe.minWidth = Mathf.Min(srcLe.minWidth > 0f ? srcLe.minWidth : newPreferred, newPreferred);
                srcLe.preferredWidth = newPreferred;
                srcRt.sizeDelta = new Vector2(Mathf.Max(0f, srcRt.sizeDelta.x - shrinkBy), srcRt.sizeDelta.y);
                newRt.sizeDelta = new Vector2(Mathf.Max(0f, newRt.sizeDelta.x - (widthBefore - side)), newRt.sizeDelta.y);
                LayoutRebuilder.ForceRebuildLayoutImmediate(parent as RectTransform);
            }
            else
            {
                // Caso B: sem layout group (ou sem controle de largura) — encolhe o original mantendo a
                // borda ESQUERDA fixa e reposiciona o clone logo a direita dele.
                float gap = spacing > 0f ? spacing : 4f;
                float shrinkBy = side + gap;
                ShrinkKeepingLeftEdge(srcRt, Mathf.Max(1f, widthBefore - shrinkBy));
                newRt.sizeDelta = new Vector2(Mathf.Max(0f, newRt.sizeDelta.x - (widthBefore - side)), newRt.sizeDelta.y);
                Canvas.ForceUpdateCanvases();
                PlaceToTheRight(srcRt, newRt, gap);
            }

            Plugin.Log.LogInfo("[RSTV-2] geometria: original=" + WorldWidth(srcRt).ToString("0.#") +
                               " clone=" + WorldWidth(newRt).ToString("0.#") + " linha=" +
                               (parent as RectTransform != null ? RowWidth(parent).ToString("0.#") : "?"));
        }

        private static float WorldWidth(RectTransform rect)
        {
            if (rect == null)
            {
                return 0f;
            }

            Vector3[] corners = new Vector3[4];
            rect.GetWorldCorners(corners);
            return corners[3].x - corners[0].x;
        }

        private static float RowWidth(Transform parent)
        {
            RectTransform row = parent as RectTransform;
            if (row == null || row.childCount == 0)
            {
                return 0f;
            }

            Vector3[] corners = new Vector3[4];
            float min = float.MaxValue;
            float max = float.MinValue;
            for (int i = 0; i < row.childCount; i++)
            {
                RectTransform child = row.GetChild(i) as RectTransform;
                if (child == null || !child.gameObject.activeSelf)
                {
                    continue;
                }

                child.GetWorldCorners(corners);
                min = Mathf.Min(min, corners[0].x);
                max = Mathf.Max(max, corners[3].x);
            }

            return max > min ? max - min : 0f;
        }

        private static void ShrinkKeepingLeftEdge(RectTransform rect, float newWidth)
        {
            Vector3[] before = new Vector3[4];
            rect.GetWorldCorners(before);
            float leftBefore = before[0].x;
            float width = before[3].x - before[0].x;
            if (width <= 1f)
            {
                return;
            }

            rect.sizeDelta = new Vector2(rect.sizeDelta.x - (width - newWidth), rect.sizeDelta.y);
            Canvas.ForceUpdateCanvases();
            Vector3[] after = new Vector3[4];
            rect.GetWorldCorners(after);
            float delta = leftBefore - after[0].x;
            if (Mathf.Abs(delta) > 0.01f)
            {
                rect.position += new Vector3(delta, 0f, 0f);
            }
        }

        private static void PlaceToTheRight(RectTransform left, RectTransform right, float gap)
        {
            Vector3[] leftCorners = new Vector3[4];
            Vector3[] rightCorners = new Vector3[4];
            left.GetWorldCorners(leftCorners);
            right.GetWorldCorners(rightCorners);
            float delta = (leftCorners[3].x + gap) - rightCorners[0].x;
            right.position += new Vector3(delta, 0f, 0f);
        }

        private static HorizontalOrVerticalLayoutGroup FindRowGroup(Transform parent, Transform source)
        {
            if (parent == null)
            {
                return null;
            }

            HorizontalOrVerticalLayoutGroup group = parent.GetComponent<HorizontalOrVerticalLayoutGroup>();
            if (group != null && source.parent == group.transform)
            {
                return group;
            }

            Transform grandParent = parent.parent;
            if (grandParent != null)
            {
                HorizontalOrVerticalLayoutGroup up = grandParent.GetComponent<HorizontalOrVerticalLayoutGroup>();
                if (up != null && source.parent == up.transform)
                {
                    return up;
                }
            }

            return null;
        }

        private static string DescribeGroup(Transform parent)
        {
            if (parent == null)
            {
                return "nenhum";
            }

            LayoutGroup group = parent.GetComponent<LayoutGroup>();
            return group == null ? "nenhum" : group.GetType().Name;
        }

        private static LayoutElement EnsureLayoutElement(GameObject go)
        {
            LayoutElement le = go.GetComponent<LayoutElement>();
            return le != null ? le : go.AddComponent<LayoutElement>();
        }

        private static void DisableLocalizers(GameObject root)
        {
            Component[] components = root.GetComponentsInChildren<Component>(true);
            for (int i = 0; i < components.Length; i++)
            {
                Component component = components[i];
                if (component == null)
                {
                    continue;
                }

                string typeName = component.GetType().Name;
                if (typeName.IndexOf("Localiz", StringComparison.OrdinalIgnoreCase) >= 0 ||
                    typeName.IndexOf("Localize", StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    Behaviour behaviour = component as Behaviour;
                    if (behaviour != null)
                    {
                        behaviour.enabled = false;
                        Plugin.Log.LogInfo("RSTV: localizador '" + typeName + "' desativado no botao clonado.");
                    }
                }
            }
        }
    }
}
