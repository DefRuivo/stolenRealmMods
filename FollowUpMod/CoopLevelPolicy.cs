using System;

namespace FollowUpMod
{
    public readonly struct LevelDecision
    {
        public readonly bool Accepted;
        public readonly int TargetLevel;
        public readonly int LevelsToGrant;
        public readonly bool CeilingLimited;

        public LevelDecision(bool accepted, int targetLevel, int levelsToGrant, bool ceilingLimited)
        {
            Accepted = accepted;
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
        /// Abaixo do minimo do grupo: aceito e promovido ate o minimo (ou ate o teto do jogo).
        /// Acima do minimo: recusado, como no jogo original. Nunca rebaixa.
        /// </summary>
        public static LevelDecision DecideLevelDelta(int characterLevel, int groupMinimum, int gameCeiling)
        {
            // Sem grupo anterior (minimo desconhecido/0): aceita sem conceder nada.
            if (groupMinimum <= 0) return new LevelDecision(true, characterLevel, 0, false);
            if (characterLevel > groupMinimum)
                return new LevelDecision(false, characterLevel, 0, false);
            int ceiling = gameCeiling > 0 ? gameCeiling : characterLevel;
            int target = Math.Min(groupMinimum, ceiling);
            int levels = target > characterLevel ? target - characterLevel : 0;
            return new LevelDecision(true, target, levels, groupMinimum > ceiling);
        }
    }
}
