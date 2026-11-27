using System;
using System.Collections.Generic;

namespace FollowUpMod
{
    /// <summary>
    /// Sobe o nivel efetivo do personagem ate o minimo do grupo (nunca rebaixa) e enfileira
    /// as recompensas nativas de nivel (Skills/Itens/Atributos) uma unica vez por grupo.
    /// </summary>
    internal static class PromotionService
    {
        private static readonly object Gate = new object();
        private static readonly Dictionary<Character, int> PromotedForGroupMin =
            new Dictionary<Character, int>(ReferenceComparer<Character>.Instance);

        internal static void Promote(Character character, int targetLevel, int levelsToGrant, bool ceilingLimited)
        {
            lock (Gate)
            {
                if (PromotedForGroupMin.TryGetValue(character, out int alreadyFor) && alreadyFor == targetLevel)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: promocao ja aplicada neste grupo");
                    return;
                }
                PromotedForGroupMin[character] = targetLevel;
            }

            float original = character.ExperienceLevel;
            float target = Character.GetExperienceFloorForLevel(targetLevel);
            SessionGuard.MarkPromoted(character, original, target);
            if (character.ExperienceLevel < target) character.ExperienceLevel = target;
            FollowUpModPlugin.Log.LogInfo("FU: promovido " + original + "->" + character.ExperienceLevel
                + " niveis=" + levelsToGrant + (ceilingLimited ? " ceiling_limited" : ""));

            EnqueueRewards(character);
        }

        internal static void EnqueueRewards(Character character)
        {
            var manager = RoguelikeManager.ForcedInstance;
            if (manager == null)
            {
                FollowUpModPlugin.Log.LogWarning("FU: RoguelikeManager ausente; recompensas nao enfileiradas");
                return;
            }
            manager.AddToSkillSelectionQueue(character, isReroll: false, currencyEarned: 0);
            FollowUpModPlugin.Log.LogInfo("FU: recompensas enfileiradas; pendentes=" + manager.GetRoguelikeLevelsNeededCount(character));
        }

        internal static void Reset()
        {
            lock (Gate) PromotedForGroupMin.Clear();
        }

        private sealed class ReferenceComparer<T> : IEqualityComparer<T> where T : class
        {
            internal static readonly ReferenceComparer<T> Instance = new ReferenceComparer<T>();
            public bool Equals(T x, T y) => ReferenceEquals(x, y);
            public int GetHashCode(T obj) => System.Runtime.CompilerServices.RuntimeHelpers.GetHashCode(obj);
        }
    }
}
