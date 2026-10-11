using System;
using RoguelikeLevelProgression.Core;

namespace RoguelikeLevelProgression.Runtime
{
    /// <summary>
    /// Estado efetivo do mod (config + aplicacao dos patches). Fica separado da classe Plugin
    /// para que os patches nao dependam de uma instancia MonoBehaviour.
    /// </summary>
    internal static class PluginState
    {
        public static bool Enabled = true;
        public static int MaxLevelConfig;          // Progression.MaxLevel
        public static int RewardQueryLevel = 20;   // Rewards.RewardQueryLevel
        public static bool Verbose;

        /// <summary>Todo o grupo de gameplay aplicado? Sem isso a politica nao amplia escopo.</summary>
        public static bool GameplayGroupApplied;

        /// <summary>Motivo da ultima recusa de avanco (diagnostico).</summary>
        public static string LastDenial;

        public static void Reset()
        {
            Enabled = true;
            MaxLevelConfig = 0;
            RewardQueryLevel = 20;
            Verbose = false;
            GameplayGroupApplied = false;
            LastDenial = null;
        }
    }

    /// <summary>
    /// Face "jogo" da politica. Toda a decisao pura fica em PolicyCore; aqui apenas se leem
    /// os fatos do personagem/settings e se converte em AdvanceInputs.
    /// </summary>
    public static class Policy
    {
        /// <summary>
        /// Substitui a comparacao vanilla `character.Level &lt; settings.RoguelikeMaxLevel`
        /// no bloco unico de Root.SendGameCompleteFromServer. Assinatura exigida pelo patch
        /// (Character, RoguelikeSettings) - ver BattleResultTranspiler.
        /// </summary>
        public static bool CanAdvance(Character character, RoguelikeSettings settings)
        {
            int vanillaCap = XpCurve.VanillaCapLevel;
            try
            {
                if (settings != null) vanillaCap = settings.RoguelikeMaxLevel;
            }
            catch (Exception)
            {
                // mantem o teto vanilla conhecido
            }

            if (character == null)
            {
                // Sem personagem: nunca ampliar (e o filtro vanilla continua valido em 147739-147775).
                return false;
            }

            AdvanceInputs inputs;
            try
            {
                inputs = BuildInputs(character, vanillaCap);
            }
            catch (Exception ex)
            {
                Log.Error("Policy.CanAdvance: falha ao montar entradas (" + ex.GetType().Name + ": " + ex.Message + "); usando comparacao vanilla");
                return Fallback(character, vanillaCap);
            }

            AdvanceDenial denial;
            try
            {
                return PolicyCore.CanAdvance(in inputs, out denial);
            }
            catch (Exception ex)
            {
                Log.Error("Policy.CanAdvance: falha na decisao (" + ex.GetType().Name + ": " + ex.Message + "); usando comparacao vanilla");
                return Fallback(character, vanillaCap);
            }
        }

        private static bool Fallback(Character character, int vanillaCap)
        {
            try { return character.Level < vanillaCap; }
            catch (Exception) { return false; }
        }

        private static AdvanceInputs BuildInputs(Character character, int vanillaCap)
        {
            var i = new AdvanceInputs();
            i.ModEnabled = PluginState.Enabled;
            i.IsAi = character.IsAI;
            i.IsRoguelikeCharacter = character.IsRoguelikeCharacter;
            i.IsMultiplayer = GameState.IsMultiplayer();
            i.IsRoguelikeMode = GameState.IsRoguelikeMode();
            i.Level = character.Level;
            i.VanillaCap = vanillaCap;
            i.VoluntaryCap = PluginState.MaxLevelConfig;
            i.TargetsPresent = PluginState.GameplayGroupApplied;

            bool ready = XpBackend.EnsureReady();
            i.CurveUsable = ready;
            i.SafetyBound = ready ? XpBackend.SafetyBound : 0;

            if (ready)
            {
                string detail;
                i.NextLevelRepresentable = XpBackend.NextLevelRepresentable(i.Level, out detail);
                int points = XpBackend.PointsPerLevelFor(character);
                i.StatBudgetOk = XpBackend.StatBudgetOk(i.Level + 1, points, out detail);
            }
            return i;
        }

        /// <summary>
        /// Teto efetivo para o getter Character.MaxLevel (postfix, apenas roguelike nao-IA).
        /// Nao escreve em GlobalSettings nem em asset; nao devolve nao-finito.
        /// </summary>
        public static double EffectiveMaxLevel(Character character, double vanillaValue)
        {
            if (character == null) return vanillaValue;
            try
            {
                if (character.IsAI || !character.IsRoguelikeCharacter) return vanillaValue;
                if (!PluginState.Enabled) return vanillaValue;
                if (!PluginState.GameplayGroupApplied) return vanillaValue;
                if (GameState.IsMultiplayer()) return vanillaValue;
                if (!XpBackend.EnsureReady()) return vanillaValue;

                var inputs = new AdvanceInputs
                {
                    ModEnabled = PluginState.Enabled,
                    IsAi = false,
                    IsRoguelikeCharacter = true,
                    IsMultiplayer = false,
                    IsRoguelikeMode = true,
                    Level = character.Level,
                    VanillaCap = XpCurve.VanillaCapLevel,
                    VoluntaryCap = PluginState.MaxLevelConfig,
                    SafetyBound = XpBackend.SafetyBound,
                    CurveUsable = true,
                    NextLevelRepresentable = true,
                    StatBudgetOk = true,
                    TargetsPresent = true,
                };
                double result = PolicyCore.EffectiveMaxLevel(in inputs);
                if (!XpCurve.IsUsableNumber(result)) return vanillaValue;
                return result;
            }
            catch (Exception ex)
            {
                Log.WarnOnce("EffectiveMaxLevel: falha (" + ex.GetType().Name + ": " + ex.Message + "); mantendo valor vanilla");
                return vanillaValue;
            }
        }
    }
}
