using System;
using System.Collections.Generic;

namespace FollowUpMod
{
    /// <summary>
    /// Sobe o NIVEL do personagem ate a ancora do grupo (nunca rebaixa) e enfileira as
    /// recompensas nativas de nivel (Skills/Itens/Atributos) uma unica vez por grupo.
    ///
    /// Unidades (medido em 1.4.9): `ExperienceLevel` e o NIVEL em float
    /// (`CalculatedExperienceLevel => Mathf.Max(ExperienceLevel, 1f)`, `Level => FloorToInt(...)`);
    /// o espaco de XP e `Experience`. Gravar `GetExperienceFloorForLevel(n)` em ExperienceLevel
    /// jogaria o nivel para milhares - por isso a atribuicao e direta.
    /// </summary>
    internal static class PromotionService
    {
        private static readonly object Gate = new object();
        private static readonly Dictionary<Character, int> PromotedForTarget =
            new Dictionary<Character, int>(ReferenceComparer<Character>.Instance);

        internal static void Promote(Character character, int targetLevel, int levelsToGrant, bool ceilingLimited)
        {
            lock (Gate)
            {
                if (PromotedForTarget.TryGetValue(character, out int alreadyFor) && alreadyFor == targetLevel)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: promocao ja aplicada neste grupo");
                    return;
                }
                PromotedForTarget[character] = targetLevel;
            }

            float original = character.ExperienceLevel;
            SessionGuard.MarkPromoted(character, original, targetLevel);
            character.ExperienceLevel = targetLevel;
            FollowUpModPlugin.Log.LogInfo("FU: promovido nivel " + original + "->" + character.ExperienceLevel
                + " (Level=" + character.Level + ") niveis=" + levelsToGrant
                + (ceilingLimited ? " ceiling_limited" : ""));

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
            lock (Gate) PromotedForTarget.Clear();
        }

        private sealed class ReferenceComparer<T> : IEqualityComparer<T> where T : class
        {
            internal static readonly ReferenceComparer<T> Instance = new ReferenceComparer<T>();
            public bool Equals(T x, T y) => ReferenceEquals(x, y);
            public int GetHashCode(T obj) => System.Runtime.CompilerServices.RuntimeHelpers.GetHashCode(obj);
        }
    }
}
