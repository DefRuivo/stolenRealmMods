using System;

namespace RoguelikeUnlimitedLevelProgression.Core
{
    /// <summary>
    /// Curva de XP estendida (parte05/C + parte06). Puro System.Math: NAO usa UnityEngine,
    /// para poder ser exercitada pelo harness isolado sem abrir o jogo.
    ///
    /// Vanilla (corpus 41538-41566):
    ///   GetExperienceForNextLevel(L) = Ceil(base * gain^(L-1))   [com offset subtraido em L==1]
    ///   GetExperienceFloorForLevel(L) = soma de GetExperienceForNextLevel(1..L-1)
    /// Logo F(20) e F(21) sao obtidos do PROPRIO jogo (nao de constante chutada):
    ///   F20 = Floor(20), D20 = Floor(21) - Floor(20).
    /// Extensao para L >= 20: F(L) = F20 + D20*(L-20); XP por transicao = D20 (linear, O(1)).
    /// Em L==20 e L==21 a extensao coincide exatamente com vanilla, por construcao.
    /// </summary>
    public static class XpCurve
    {
        /// <summary>Teto vanilla do modo Roguelike (asset RoguelikeSettings.RoguelikeMaxLevel).</summary>
        public const int VanillaCapLevel = 20;

        /// <summary>
        /// Teto conservador de representacao: acima disso o piso de XP em float ja perde
        /// passos unitarios (float tem 24 bits de mantissa) e nao vale mais a pena avancar.
        /// Nao e um "cap seguro 40/100" inventado: e um limite de representacao derivado
        /// dos parametros reais (ver SafetyBoundLevel).
        /// </summary>
        public const double FloatSafeXpCeiling = 1e30d;

        /// <summary>Maior inteiro que um float representa exatamente (2^24).</summary>
        public const int FloatExactIntegerLimit = 1 << 24;

        public static bool CurveUsable(double floor20, double transition)
        {
            if (!IsUsableNumber(floor20) || !IsUsableNumber(transition)) return false;
            if (floor20 < 0d) return false;
            if (transition <= 0d) return false;
            double floor21 = floor20 + transition;
            if (!IsUsableNumber(floor21)) return false;
            if (!(floor21 > floor20)) return false;
            return true;
        }

        public static bool IsUsableNumber(double v)
        {
            return !double.IsNaN(v) && !double.IsInfinity(v);
        }

        /// <summary>Piso de XP do nivel (vale para level &gt; VanillaCapLevel).</summary>
        public static double Floor(double floor20, double transition, int level)
        {
            return floor20 + transition * (level - VanillaCapLevel);
        }

        /// <summary>XP necessario para sair do nivel (vale para level &gt; VanillaCapLevel).</summary>
        public static double Transition(double transition, int level)
        {
            return transition;
        }

        /// <summary>
        /// Inversa analitica: nivel (fracionario) para um XP >= F20.
        /// Equivale a inversa vanilla aplicada sobre o piso estendido, sem loop sem bound.
        /// </summary>
        public static double LevelFromXp(double floor20, double transition, double xp)
        {
            return VanillaCapLevel + (xp - floor20) / transition;
        }

        /// <summary>
        /// Menor nivel cujo piso e maior que o XP informado (convencao de
        /// Character.GetLevelFromExperience: F(L) &lt;= xp &lt; F(L+1)  =&gt;  L).
        /// </summary>
        public static int LevelIndexFromXp(double floor20, double transition, double xp)
        {
            double raw = LevelFromXp(floor20, transition, xp);
            int level = (int)Math.Floor(raw);
            // protecao de fronteira: o calculo em double pode cair 1 ulp abaixo do inteiro
            if (Floor(floor20, transition, level + 1) <= xp) level++;
            while (level > VanillaCapLevel && Floor(floor20, transition, level) > xp) level--;
            return level;
        }

        /// <summary>
        /// Teto de seguranca do nivel: o menor entre
        ///  (a) limite de representacao do XP em float (F(L) &lt;= 1e30),
        ///  (b) limite de precisao dos pontos de atributo (soma em float exato = 2^24),
        ///  (c) limite de representacao inteira de (Level-1)*pontosPorNivel em int32.
        /// Formula registrada aqui e logada pelo mod na inicializacao.
        /// </summary>
        public static int SafetyBoundLevel(double floor20, double transition, int pointsPerLevel)
        {
            double byXpRaw = VanillaCapLevel + (FloatSafeXpCeiling - floor20) / transition;
            int byXp = ClampToInt(byXpRaw);

            int byStats;
            if (pointsPerLevel <= 0)
            {
                byStats = int.MaxValue - 2;
            }
            else
            {
                byStats = ClampToInt(1d + (double)FloatExactIntegerLimit / pointsPerLevel);
            }

            int byInt;
            if (pointsPerLevel <= 0)
            {
                byInt = int.MaxValue - 2;
            }
            else
            {
                byInt = ClampToInt(1d + (double)(int.MaxValue - 2) / pointsPerLevel);
            }

            int result = Math.Min(byXp, Math.Min(byStats, byInt));
            if (result < VanillaCapLevel + 1) result = VanillaCapLevel + 1;
            return result;
        }

        private static int ClampToInt(double v)
        {
            if (double.IsNaN(v)) return VanillaCapLevel + 1;
            if (v >= int.MaxValue - 2d) return int.MaxValue - 2;
            if (v <= 0d) return 1;
            return (int)Math.Floor(v);
        }
    }
}
