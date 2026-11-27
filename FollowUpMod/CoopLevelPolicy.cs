using System;

namespace FollowUpMod
{
    public readonly struct PromotionDecision
    {
        public readonly bool Promote;
        public readonly int TargetLevel;
        public readonly int LevelsToGrant;
        public readonly bool CeilingLimited;

        public PromotionDecision(bool promote, int targetLevel, int levelsToGrant, bool ceilingLimited)
        {
            Promote = promote;
            TargetLevel = targetLevel;
            LevelsToGrant = levelsToGrant;
            CeilingLimited = ceilingLimited;
        }
    }

    // struct comum (nao 'readonly struct'): netstandard2.1 nao tem IsExternalInit para 'init',
    // e propriedade autoimplementada com setter nao e permitida em struct readonly.
    public struct CoopContext
    {
        public bool IsMultiplayer { get; set; }
        public bool IsRoguelike { get; set; }
        public bool HostAnnouncesRule { get; set; }
    }

    public static class CoopLevelPolicy
    {
        /// <summary>Chave publicada pelo host no lobby Steam. Presenca = host tem o mod.</summary>
        public const string LobbyKey = "followup.level";

        public static int GroupMinimum(int[] currentLevels)
        {
            if (currentLevels == null || currentLevels.Length == 0) return 0;
            int min = int.MaxValue;
            foreach (int level in currentLevels) if (level < min) min = level;
            return min;
        }

        public static int GroupMaximum(int[] currentLevels)
        {
            if (currentLevels == null || currentLevels.Length == 0) return 0;
            int max = int.MinValue;
            foreach (int level in currentLevels) if (level > max) max = level;
            return max;
        }

        /// <summary>
        /// Decide apenas a PROMOCAO. Quem esta abaixo da ancora do grupo sobe ate ela (ou ate o
        /// teto do jogo); quem esta na ancora ou acima dela nao e tocado, e a aceitacao/recusa
        /// continua sendo a regra do jogo original (MaxLevelVariance). Nunca rebaixa.
        /// </summary>
        public static PromotionDecision DecidePromotion(int characterLevel, int anchorLevel, int gameCeiling)
        {
            if (anchorLevel <= 0) return new PromotionDecision(false, characterLevel, 0, false);
            if (characterLevel >= anchorLevel) return new PromotionDecision(false, characterLevel, 0, false);
            int ceiling = gameCeiling > 0 ? gameCeiling : anchorLevel;
            int target = Math.Min(anchorLevel, ceiling);
            int levels = target > characterLevel ? target - characterLevel : 0;
            return new PromotionDecision(levels > 0, target, levels, anchorLevel > ceiling);
        }
    }
}
