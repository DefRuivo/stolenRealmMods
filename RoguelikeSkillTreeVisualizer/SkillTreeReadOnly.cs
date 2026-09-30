using System;
using System.Collections.Generic;
using System.Linq;
using Burst2Flame;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-2c/2d: abre a Skill Tree NATIVA (`SkillTreeManager`, l.172045 — a mesma do
    /// Campaign -> Change Skills) para o personagem da party, em modo SOMENTE LEITURA.
    ///
    /// A abertura segue o caminho real do jogo (CharacterMenusManager.OpenSkillTreeMenu,
    /// l.48471-48482):
    ///   1. `LoadableUIWindow&lt;SkillTreeManager&gt;.LoadInstanceReference(prefab, placeholder)` +
    ///      espera `Instance != null` (l.48471-48480);
    ///   2. `Instance.Initialize(SkillsFromPoints, unspentPoints, creating)` (l.48481 / l.172380);
    ///   3. `Instance.gameObject.SetActive(true)` (l.48482).
    ///
    /// O contexto do personagem NAO entra por parametro: `SkillTreeManager` e o `Tooltip` leem
    /// `GameLogic.instance.CurrentlySelectedCharacter` (l.172823, l.172388 e o `TooltipCharacter`
    /// do tooltip, l.213124 — e por ele que o tooltip calcula custo de mana, alcance, dano e
    /// "ObtainedByItem/Status"). Por isso o setter e chamado ANTES de abrir; ele e publico
    /// (l.108082) e recusa personagem nao-Owned (l.108117-108120), o que casa com a regra do mod
    /// (so personagens do proprio jogador).
    ///
    /// NUNCA chamar `CharacterMenusManager.CloseSkillTreeMenu()` (l.48490): ele chama
    /// `AcceptSkillChanges(closeMenu: true)` e ESCRITA. O fechamento e feito pelo proprio botao da
    /// janela nativa (que passa por AcceptSkillChanges -> o prefixo de higienizacao em Patches.cs).
    /// </summary>
    internal static class SkillTreeReadOnly
    {
        private static Character _pendingTarget;
        private static float _pendingSince;
        private const float PendingTimeout = 15f;

        internal static void Open(Character target)
        {
            if (target == null)
            {
                return;
            }

            // 1) contexto REAL do personagem (nivel, equipamento, atributos, status atuais)
            GameLogic.instance.CurrentlySelectedCharacter = target;

            SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
            if (instance == null)
            {
                _pendingTarget = target;
                _pendingSince = Time.realtimeSinceStartup;
                ReferenceLoader loader = ReferenceLoader.Instance;
                if (loader == null)
                {
                    Plugin.Log.LogError("RSTV: ReferenceLoader ausente — nao da para carregar a skill tree.");
                    _pendingTarget = null;
                    return;
                }

                Plugin.Log.LogInfo("RSTV-2: SkillTreeManager ainda nao existia — carregando a instancia nativa.");
                LoadableUIWindow<SkillTreeManager>.LoadInstanceReference(
                    loader.SkillTreeManager.gameObject, loader.SkillTreeManagerPlaceholder);
                return;
            }

            Finish(target, instance);
        }

        /// <summary>Chamado todo frame pelo `RstvHost` enquanto a instancia nativa nao chega.</summary>
        internal static void Tick()
        {
            if (_pendingTarget == null)
            {
                return;
            }

            SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
            if (instance != null)
            {
                Character target = _pendingTarget;
                _pendingTarget = null;
                Finish(target, instance);
                return;
            }

            if (Time.realtimeSinceStartup - _pendingSince > PendingTimeout)
            {
                _pendingTarget = null;
                Plugin.Log.LogError("RSTV: timeout esperando o SkillTreeManager carregar (15s).");
            }
        }

        private static void Finish(Character target, SkillTreeManager instance)
        {
            try
            {
                if (target == null || instance == null)
                {
                    return;
                }

                ReadOnlySession.Begin(target);

                // Ativa ANTES de inicializar: `Initialize` busca as abas com
                // `tabHolder.GetComponentsInChildren<SkillTreeTab>()` (l.172394), que ignora filhos
                // inativos — com a janela desligada as abas nao seriam encontradas.
                instance.gameObject.SetActive(true);
                instance.Initialize(target.SkillsFromPoints.ToList(), 0, false);
                ZOrder.EnsureAbove(instance.transform, CharacterChoiceManager.Instance != null
                    ? CharacterChoiceManager.Instance.transform
                    : null);
                ReadOnlySession.InstallCancelInterceptor();

                Plugin.Log.LogInfo("RSTV-2: skill tree read-only aberta para '" + target.CharacterName +
                                   "' (nivel " + target.Level + ", " + target.SkillsFromPoints.Count +
                                   " skills, 0 pontos). ativaNaHierarquia=" + instance.gameObject.activeInHierarchy);
            }
            catch (Exception e)
            {
                ReadOnlySession.End();
                try
                {
                    if (instance != null)
                    {
                        instance.gameObject.SetActive(false);
                    }
                }
                catch (Exception)
                {
                    // a janela ja pode ter sido destruida
                }

                Plugin.Log.LogError("RSTV: falha ao abrir a skill tree: " + e);
            }
        }
    }

    /// <summary>
    /// Sessao de somente leitura. `Active` e o sinal consultado pelos patches (bloqueio do clique
    /// na arvore, higienizacao do commit e esconderijo do RespecButton).
    /// </summary>
    internal static class ReadOnlySession
    {
        internal static bool Active { get; private set; }
        internal static Character Target { get; private set; }

        private static Func<bool> _interceptor;

        internal static void Begin(Character target)
        {
            Active = true;
            Target = target;
            Plugin.Log.LogInfo("RSTV-2: modo somente leitura ATIVO.");
        }

        internal static void End()
        {
            if (!Active)
            {
                return;
            }

            Active = false;
            Target = null;
            RemoveCancelInterceptor();
            ZOrder.Restore();
            Plugin.Log.LogInfo("RSTV-2: modo somente leitura encerrado (nada foi gravado no personagem).");
        }

        /// <summary>
        /// Enquanto a janela nativa esta aberta, Esc/B (UIWindowManager.Update, l.216020) fecharia a
        /// tela de party que esta ATRAS da arvore, deixando a arvore orfa. Este interceptor consome
        /// o cancel e fecha a arvore.
        /// </summary>
        internal static void InstallCancelInterceptor()
        {
            _interceptor = OnCancelPressed;
            UIWindowManager.CancelInterceptor = _interceptor;
        }

        internal static void RemoveCancelInterceptor()
        {
            if (_interceptor != null && UIWindowManager.CancelInterceptor == _interceptor)
            {
                UIWindowManager.CancelInterceptor = null;
            }

            _interceptor = null;
        }

        internal static void Close()
        {
            SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
            End();
            try
            {
                if (instance != null)
                {
                    instance.SkillsToAdd.Clear();
                    instance.SkillsRemoved.Clear();
                    instance.gameObject.SetActive(false);
                }

                if (GUIManager.instance != null && GUIManager.instance.tooltip != null)
                {
                    GUIManager.instance.tooltip.HideTooltip();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao fechar a skill tree read-only: " + e.Message);
            }
        }

        private static bool OnCancelPressed()
        {
            if (!Active)
            {
                return false;
            }

            Plugin.Log.LogInfo("RSTV-2: Esc/B consumido — fechando a skill tree read-only.");
            Close();
            return true;
        }
    }

    /// <summary>
    /// A janela nativa e instanciada sob `ReferenceLoader.SkillTreeManagerPlaceholder` (l.162628),
    /// que e outro ramo da hierarquia do canvas; a tela de party pode ter sido autorada DEPOIS dele.
    /// Sem reordenar, a arvore desenharia ATRAS do Select Party. Aqui so mexemos em indices de irmao
    /// (nunca em parentesco/ancoras, que mudaria o layout) e restauramos no fechamento.
    /// </summary>
    internal static class ZOrder
    {
        private static Transform _movedBranch;
        private static int _movedBranchOldIndex = -1;

        internal static void EnsureAbove(Transform above, Transform reference)
        {
            try
            {
                Restore();
                if (above == null || reference == null)
                {
                    return;
                }

                Transform common = CommonAncestor(above, reference);
                if (common == null)
                {
                    return;
                }

                Transform branchAbove = BranchUnder(common, above);
                Transform branchReference = BranchUnder(common, reference);
                if (branchAbove == null || branchReference == null)
                {
                    return;
                }

                if (branchAbove.GetSiblingIndex() < branchReference.GetSiblingIndex())
                {
                    _movedBranch = branchAbove;
                    _movedBranchOldIndex = branchAbove.GetSiblingIndex();
                    branchAbove.SetAsLastSibling();
                    Plugin.Log.LogInfo("RSTV-2: z-order — ramo '" + branchAbove.name + "' estava em " +
                                       _movedBranchOldIndex + " (atras de '" + branchReference.name +
                                       "', " + branchReference.GetSiblingIndex() + "); movido para o fim.");
                }

                if (above.parent == reference.parent && above.GetSiblingIndex() < reference.GetSiblingIndex())
                {
                    above.SetAsLastSibling();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para garantir o z-order da arvore: " + e.Message);
            }
        }

        internal static void Restore()
        {
            try
            {
                if (_movedBranch != null && _movedBranchOldIndex >= 0)
                {
                    _movedBranch.SetSiblingIndex(_movedBranchOldIndex);
                }
            }
            catch (Exception)
            {
                // a cena pode ter sido descarregada; nada a restaurar
            }
            finally
            {
                _movedBranch = null;
                _movedBranchOldIndex = -1;
            }
        }

        private static Transform CommonAncestor(Transform a, Transform b)
        {
            HashSet<Transform> chain = new HashSet<Transform>();
            for (Transform t = a; t != null; t = t.parent)
            {
                chain.Add(t);
            }

            for (Transform t = b; t != null; t = t.parent)
            {
                if (chain.Contains(t))
                {
                    return t;
                }
            }

            return null;
        }

        private static Transform BranchUnder(Transform ancestor, Transform node)
        {
            Transform current = node;
            while (current != null && current.parent != ancestor)
            {
                current = current.parent;
            }

            return current;
        }
    }
}
