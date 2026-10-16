using System;
using RoguelikeUnlimitedLevelProgression.Core;

namespace RoguelikeUnlimitedLevelProgression.Runtime
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
            PatchRegistryEvidence.FirstHook("Policy.CanAdvance");
            int vanillaCap = XpCurve.VanillaCapLevel;
            try
            {
                if (settings != null) vanillaCap = settings.RoguelikeMaxLevel;
            }
            catch (Exception ex)
            {
                Log.WarnOnce("Policy.CanAdvance: settings indisponivel (" + ex.GetType().Name + "); teto vanilla conhecido usado");
            }

            if (character == null)
            {
                // Sem personagem: nunca ampliar (e o filtro vanilla continua valido em 147739-147775).
                DiagnoseOnce("character=null");
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
                DiagnoseOnce("falha ao montar entradas: " + ex.GetType().Name);
                return Fallback(character, vanillaCap);
            }

            AdvanceDenial denial;
            bool allow;
            try
            {
                allow = PolicyCore.CanAdvance(in inputs, out denial);
            }
            catch (Exception ex)
            {
                Log.Error("Policy.CanAdvance: falha na decisao (" + ex.GetType().Name + ": " + ex.Message + "); usando comparacao vanilla");
                DiagnoseOnce("falha na decisao: " + ex.GetType().Name);
                return Fallback(character, vanillaCap);
            }

            Diagnose(in inputs, denial, allow);
            return allow;
        }

        private static bool Fallback(Character character, int vanillaCap)
        {
            try { return character.Level < vanillaCap; }
            catch (Exception ex) { return Log.Refuse("politica.Fallback", "leitura do nivel falhou: " + ex.GetType().Name, once: false); }
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
        /// DIAGNOSTICO de decisao (RLP-1/RLP-2). Uma linha por recusa de ampliacao, mesmo
        /// quando Diagnostics.Verbose=false. Verbose controla apenas decisoes positivas.
        /// Inclui cada fato efetivo para distinguir guarda de rede/modo de falha numerica.
        /// </summary>
        private static void Diagnose(in AdvanceInputs i, AdvanceDenial denial, bool allow)
        {
            PluginState.LastDenial = denial.ToString();
            // Recusar AMPLIACAO nao depende de Verbose, mesmo quando vanilla ainda permite
            // avancar abaixo de 20 (VanillaScope).
            if (allow && denial == AdvanceDenial.None && !PluginState.Verbose) return;
            Log.Info("politica: allow=" + allow + " motivo=" + denial + " enabled=" + i.ModEnabled
                         + " nivel=" + i.Level + " capVanilla=" + i.VanillaCap
                         + " personagemRoguelike=" + i.IsRoguelikeCharacter + " modoRoguelike=" + i.IsRoguelikeMode
                         + " ia=" + i.IsAi + " multiplayer=" + i.IsMultiplayer
                         + " alvos=" + i.TargetsPresent + " curva=" + i.CurveUsable
                         + " proximoRepresentavel=" + i.NextLevelRepresentable + " orcamentoPontos=" + i.StatBudgetOk
                         + " tetoVoluntario=" + i.VoluntaryCap + " tetoRepresentacao=" + i.SafetyBound);
        }

        private static void DiagnoseOnce(string motivo)
        {
            PluginState.LastDenial = motivo;
            Log.Refuse("politica", "chamada sem decisao: " + motivo, once: false);
        }

        /// <summary>
        /// Teto efetivo para o getter Character.MaxLevel (postfix, apenas roguelike nao-IA).
        /// Nao escreve em GlobalSettings nem em asset; nao devolve nao-finito.
        ///
        /// Piso de CARGA (R3-01). Character.Load(int) executa
        ///   ExperienceLevel = Mathf.Min(MaxLevel, CharacterSaveFile.ExperienceLevel)
        /// ANTES de ExperienceLevel ser atribuido, entao Character.Level ainda e ~1 e a protecao
        /// do getter nao cobre o nivel salvo. Enquanto o personagem nao esta carregado
        /// (IsLoaded == false) o getter nunca devolve valor abaixo de
        /// CharacterSaveFile.ExperienceLevel — inclusive no caminho de fallback vanilla (grupo nao
        /// aplicado / multiplayer / backend indisponivel), para nao truncar saves acima de 30.
        /// </summary>
        public static double EffectiveMaxLevel(Character character, double vanillaValue)
        {
            if (character == null) { Log.Refuse("MaxLevel", "character=null"); return vanillaValue; }
            try
            {
                // Fora do escopo do mod o comportamento vanilla fica intacto (sem piso de carga).
                if (character.IsAI) { Log.Refuse("MaxLevel", "IsAI=True"); return vanillaValue; }
                if (!character.IsRoguelikeCharacter) { Log.Refuse("MaxLevel", "IsRoguelikeCharacter=False"); return vanillaValue; }
                if (!PluginState.Enabled) { Log.Refuse("MaxLevel", "General.Enabled=False"); return vanillaValue; }

                bool loading = !character.IsLoaded;
                double savedLoadLevel = 0d;
                if (loading)
                {
                    var save = character.CharacterSaveFile;
                    if (save != null) savedLoadLevel = save.ExperienceLevel;
                }

                if (!PluginState.GameplayGroupApplied) Log.Refuse("MaxLevel", "GameplayGroupApplied=False");
                bool extended = PluginState.GameplayGroupApplied
                                && !GameState.IsMultiplayer()
                                && XpBackend.EnsureReady();
                if (!extended) Log.Refuse("MaxLevel", "extensao indisponivel; usando teto vanilla com piso de carga");

                var inputs = new AdvanceInputs
                {
                    ModEnabled = PluginState.Enabled,
                    IsAi = false,
                    IsRoguelikeCharacter = true,
                    IsMultiplayer = false,
                    IsRoguelikeMode = true,
                    Level = character.Level,
                    VanillaCap = XpCurve.VanillaCapLevel,
                    VoluntaryCap = extended ? PluginState.MaxLevelConfig : 0,
                    SafetyBound = extended ? XpBackend.SafetyBound : 0,
                    VanillaMaxLevel = vanillaValue,
                    IsLoading = loading,
                    SavedLoadLevel = savedLoadLevel,
                    CurveUsable = true,
                    NextLevelRepresentable = true,
                    StatBudgetOk = true,
                    TargetsPresent = true,
                };

                double result = PolicyCore.EffectiveMaxLevel(in inputs);
                if (!XpCurve.IsUsableNumber(result))
                {
                    Log.Refuse("MaxLevel", "teto calculado nao finito; mantendo vanilla");
                    return vanillaValue;
                }
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
