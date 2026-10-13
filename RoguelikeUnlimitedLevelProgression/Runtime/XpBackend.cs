using System;
using RoguelikeUnlimitedLevelProgression.Core;

namespace RoguelikeUnlimitedLevelProgression.Runtime
{
    /// <summary>
    /// Backend de XP estendido (parte05/C). F20 e D20 sao lidos do PROPRIO jogo, chamando os
    /// metodos vanilla com a extensao temporariamente suprimida — nenhuma constante chutada,
    /// nenhum valor serializado presumido (GlobalSettings serializado ficou NAO_EXERCITADO na R1).
    /// </summary>
    internal static class XpBackend
    {
        [ThreadStatic] private static bool _suppressed;

        public static bool Ready { get; private set; }
        public static double Floor20 { get; private set; }
        public static double Transition20 { get; private set; }
        public static int SafetyBound { get; private set; }
        public static int PointsPerLevel { get; private set; }
        public static string LastError { get; private set; }
        public static string BoundFormula { get; private set; }

        /// <summary>Verdadeiro enquanto o mod consulta os metodos vanilla (sem extensao).</summary>
        public static bool Suppressed { get { return _suppressed; } }

        public static int CapLevelForQueries()
        {
            return PluginState.RewardQueryLevel;
        }

        public static bool EnsureReady()
        {
            if (Ready) return true;
            try
            {
                _suppressed = true;
                float f20, f21;
                try
                {
                    f20 = Character.GetExperienceFloorForLevel(XpCurve.VanillaCapLevel);
                    f21 = Character.GetExperienceFloorForLevel(XpCurve.VanillaCapLevel + 1);
                }
                finally
                {
                    _suppressed = false;
                }

                double floor20 = f20;
                double d20 = (double)f21 - (double)f20;
                if (!XpCurve.CurveUsable(floor20, d20))
                {
                    LastError = "parametros vanilla invalidos: F20=" + f20.ToString("R") + " F21=" + f21.ToString("R")
                                + " D20=" + d20.ToString("R") + " (exigidos: finitos, D20>0, F21>F20)";
                    Log.WarnOnce("XP estendido indisponivel: " + LastError);
                    return false;
                }

                Floor20 = floor20;
                Transition20 = d20;
                PointsPerLevel = DefaultPointsPerLevel();
                SafetyBound = XpCurve.SafetyBoundLevel(floor20, d20, PointsPerLevel);
                BoundFormula = "min(20+floor((1e30-F20)/D20), 1+2^24/pontosPorNivel, 1+(int.MaxValue-2)/pontosPorNivel)"
                               + " com F20=" + floor20.ToString("R") + " D20=" + d20.ToString("R")
                               + " pontosPorNivel=" + PointsPerLevel + " => " + SafetyBound;
                Ready = true;
                Log.InfoOnce("XP estendido pronto: F20=" + floor20.ToString("R") + " D20=" + d20.ToString("R")
                             + " teto de representacao=" + SafetyBound);
                Log.Info("Formula do teto de representacao: " + BoundFormula);
                return true;
            }
            catch (Exception ex)
            {
                _suppressed = false;
                LastError = ex.GetType().Name + ": " + ex.Message;
                Log.WarnOnce("XP estendido indisponivel: " + LastError);
                return false;
            }
        }

        /// <summary>Pontos de atributo concedidos por nivel de acordo com o jogo carregado.</summary>
        private static int DefaultPointsPerLevel()
        {
            int points = 0;
            try
            {
                var s = GameState.Settings();
                var mgr = GlobalSettingsManager.instance;
                if (mgr != null && mgr.globalSettings != null)
                {
                    points = mgr.globalSettings.NumStatsPerNewLevel;
                }
                _ = s;
            }
            catch (Exception)
            {
                points = 0;
            }
            if (points <= 0) points = 1; // guarda: evita divisao por zero na formula do teto
            return points;
        }

        /// <summary>Pontos por nivel considerando o bonus por personagem (AdditionalRoguelikeAttributesPointsPerLevel).</summary>
        public static int PointsPerLevelFor(Character c)
        {
            int points = PointsPerLevel > 0 ? PointsPerLevel : 1;
            try
            {
                if (c != null) points += (int)c["AdditionalRoguelikeAttributesPointsPerLevel"];
            }
            catch (Exception)
            {
                // sem o atributo, mantem o valor global
            }
            return points > 0 ? points : 1;
        }

        // ---- consultas de curva usadas pelos prefixes ----

        public static bool TryFloor(int level, out double value)
        {
            value = 0d;
            if (!Ready || level <= XpCurve.VanillaCapLevel) return false;
            value = XpCurve.Floor(Floor20, Transition20, level);
            return XpCurve.IsUsableNumber(value);
        }

        public static bool TryTransition(int level, out double value)
        {
            value = 0d;
            if (!Ready || level <= XpCurve.VanillaCapLevel) return false;
            value = XpCurve.Transition(Transition20, level);
            return XpCurve.IsUsableNumber(value) && value > 0d;
        }

        public static bool TryLevelFromXp(float xp, out double level)
        {
            level = 0d;
            if (!Ready) return false;
            double x = xp;
            if (!XpCurve.IsUsableNumber(x) || x < Floor20) return false;
            level = XpCurve.LevelFromXp(Floor20, Transition20, x);
            return XpCurve.IsUsableNumber(level);
        }

        public static bool TryXpFromLevel(float level)
        {
            if (!Ready) return false;
            if (!XpCurve.IsUsableNumber(level) || level <= XpCurve.VanillaCapLevel) return false;
            int whole = (int)Math.Floor(level);
            double frac = level - whole;
            double floorOf = XpCurve.Floor(Floor20, Transition20, whole);
            return XpCurve.IsUsableNumber(floorOf + frac * Transition20);
        }

        public static double XpFromLevel(float level)
        {
            int whole = (int)Math.Floor(level);
            double frac = level - whole;
            return XpCurve.Floor(Floor20, Transition20, whole) + frac * Transition20;
        }

        /// <summary>Proximo nivel e representavel, finito e estritamente crescente.</summary>
        public static bool NextLevelRepresentable(int currentLevel, out string detail)
        {
            detail = null;
            if (!Ready)
            {
                detail = "backend nao pronto";
                return false;
            }
            if (currentLevel < 0 || currentLevel >= int.MaxValue - 2)
            {
                detail = "nivel atual fora de faixa: " + currentLevel;
                return false;
            }
            int next = currentLevel + 1;
            double fN, fN1;
            if (!TryFloor(next, out fN) && next > XpCurve.VanillaCapLevel)
            {
                detail = "F(" + next + ") nao finito";
                return false;
            }
            if (!TryFloor(next + 1, out fN1) && (next + 1) > XpCurve.VanillaCapLevel)
            {
                detail = "F(" + (next + 1) + ") nao finito";
                return false;
            }
            if (next > XpCurve.VanillaCapLevel && !(fN1 > fN))
            {
                detail = "F(" + next + ")=" + fN.ToString("R") + " nao e estritamente menor que F(" + (next + 1) + ")=" + fN1.ToString("R");
                return false;
            }
            if (next > XpCurve.VanillaCapLevel)
            {
                // a inversa de F(L+1) deve resultar em L+1
                double back = XpCurve.LevelFromXp(Floor20, Transition20, fN1);
                int idx = XpCurve.LevelIndexFromXp(Floor20, Transition20, fN1);
                if (idx != next + 1)
                {
                    detail = "inversa de F(" + (next + 1) + ") devolveu " + idx;
                    return false;
                }
                if (Math.Abs(back - (next + 1)) > 1e-6)
                {
                    detail = "inversa analitica imprecisa em L=" + (next + 1) + ": " + back.ToString("R");
                    return false;
                }
            }
            return true;
        }

        /// <summary>Orcamento de pontos de atributo em long, sem perder incremento unitario em float.</summary>
        public static bool StatBudgetOk(int nextLevel, int pointsPerLevel, out string detail)
        {
            detail = null;
            if (nextLevel < 1)
            {
                detail = "nivel invalido";
                return false;
            }
            long total = (long)(nextLevel - 1) * pointsPerLevel;
            if (total > int.MaxValue - 2L)
            {
                detail = "soma de pontos excede int32: " + total;
                return false;
            }
            if (total > XpCurve.FloatExactIntegerLimit)
            {
                detail = "soma de pontos excede o inteiro exato de float (2^24): " + total;
                return false;
            }
            return true;
        }

        public static void ResetForTests()
        {
            Ready = false;
            Floor20 = 0d;
            Transition20 = 0d;
            SafetyBound = 0;
            PointsPerLevel = 0;
            LastError = null;
            BoundFormula = null;
            _suppressed = false;
        }

        /// <summary>
        /// Seam do harness isolado: fixa F20/D20/pontos SEM consultar o jogo (que exige o runtime
        /// Unity). O mod nunca chama isto — em producao os valores vem de EnsureReady(). Serve para
        /// exercitar o MESMO codigo de consulta/validacao (TryFloor/TryTransition/LevelFromXp/
        /// NextLevelRepresentable/StatBudgetOk) sem abrir o jogo.
        /// </summary>
        public static bool PrimeForTests(double floor20, double transition, int pointsPerLevel)
        {
            ResetForTests();
            if (!XpCurve.CurveUsable(floor20, transition)) return false;
            Floor20 = floor20;
            Transition20 = transition;
            PointsPerLevel = pointsPerLevel > 0 ? pointsPerLevel : 1;
            SafetyBound = XpCurve.SafetyBoundLevel(floor20, transition, PointsPerLevel);
            Ready = true;
            return true;
        }
    }
}
