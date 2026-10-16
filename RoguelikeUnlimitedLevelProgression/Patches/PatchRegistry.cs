using System;
using System.Collections.Generic;
using System.Reflection;
using HarmonyLib;
using RoguelikeUnlimitedLevelProgression.Runtime;

namespace RoguelikeUnlimitedLevelProgression.Patches
{
    /// <summary>
    /// Aplicacao tudo-ou-nada do grupo de GAMEPLAY (parte05 §5): qualquer alvo ausente, qualquer
    /// excecao de patch ou qualquer recusa do transpiler critico retira TODOS os patches do mod
    /// (fail-closed), em vez de manter metade aplicada.
    /// </summary>
    internal static class PatchRegistry
    {
        internal sealed class Plan
        {
            public string Id;
            public MethodBase Target;
            public MethodInfo Prefix;
            public MethodInfo Postfix;
            public MethodInfo Transpiler;
            public MethodInfo Finalizer;
        }

        /// <summary>
        /// Resolve os alvos Harmony SEM aplicar nada. E o portao fail-closed: qualquer alvo
        /// ausente significa que ApplyAll nao aplica nenhum patch do mod.
        /// Extraido para que o harness isolado exercite a resolucao contra a DLL real.
        /// </summary>
        internal static bool TryBuildPlans(out List<Plan> outPlans, out List<string> outMissing)
        {
            var plans = new List<Plan>();
            var missing = new List<string>();

            void Add(string id, MethodBase target, MethodInfo prefix = null, MethodInfo postfix = null,
                     MethodInfo transpiler = null, MethodInfo finalizer = null)
            {
                if (target == null) { missing.Add(id); return; }
                if (prefix == null && postfix == null && transpiler == null && finalizer == null)
                {
                    missing.Add(id + "#handler");
                    return;
                }
                plans.Add(new Plan { Id = id, Target = target, Prefix = prefix, Postfix = postfix, Transpiler = transpiler, Finalizer = finalizer });
            }

            var tCharacter = typeof(Character);
            var tInventory = typeof(InventoryManager);
            var tSkillbar = typeof(Skillbar);
            var tRogue = typeof(RoguelikeManager);

            // --- grupo de gameplay ---
            Add("Root.SendGameCompleteFromServer",
                Reflect.Method(typeof(Root), "SendGameCompleteFromServer"),
                transpiler: Reflect.Method(typeof(BattleResultPatches), "Transpiler"));

            Add("Character.get_MaxLevel",
                Reflect.PropertyGetter(tCharacter, "MaxLevel"),
                postfix: Reflect.Method(typeof(MaxLevelPatches), "Postfix"));

            Add("Character.ExperienceLevelDidSet",
                Reflect.Method(tCharacter, "ExperienceLevelDidSet", new[] { typeof(float) }),
                prefix: Reflect.Method(typeof(LegacyMirrorPatches), "Prefix"));

            Add("Character.GetExperienceFloorForLevel",
                Reflect.Method(tCharacter, "GetExperienceFloorForLevel", new[] { typeof(int) }),
                prefix: Reflect.Method(typeof(XpStaticPatches), "PrefixFloor"));

            Add("Character.GetExperienceForNextLevel",
                Reflect.Method(tCharacter, "GetExperienceForNextLevel", new[] { typeof(int) }),
                prefix: Reflect.Method(typeof(XpStaticPatches), "PrefixNext"));

            Add("Character.GetExperienceLevelFromExperience",
                Reflect.Method(tCharacter, "GetExperienceLevelFromExperience", new[] { typeof(float) }),
                prefix: Reflect.Method(typeof(XpStaticPatches), "PrefixLevelFromXp"));

            Add("Character.GetExperienceFromExperienceLevel",
                Reflect.Method(tCharacter, "GetExperienceFromExperienceLevel", new[] { typeof(float) }),
                prefix: Reflect.Method(typeof(XpStaticPatches), "PrefixXpFromLevel"));

            Add("Character.GetLevelFromExperience",
                Reflect.Method(tCharacter, "GetLevelFromExperience", new[] { typeof(float) }),
                prefix: Reflect.Method(typeof(XpStaticPatches), "PrefixLevelIndex"));

            var scopePrefix = Reflect.Method(typeof(ScopePatches), "PrefixCharacterOwner");
            var scopeFinalizer = Reflect.Method(typeof(ScopePatches), "FinalizerCharacterOwner");
            Add("Character.get_Experience", Reflect.PropertyGetter(tCharacter, "Experience"), scopePrefix, finalizer: scopeFinalizer);
            Add("Character.get_ExpForNextLevel", Reflect.PropertyGetter(tCharacter, "ExpForNextLevel"), scopePrefix, finalizer: scopeFinalizer);
            Add("Character.get_MaxExperience", Reflect.PropertyGetter(tCharacter, "MaxExperience"), scopePrefix, finalizer: scopeFinalizer);
            Add("Character.GiveExperience",
                Reflect.Method(tCharacter, "GiveExperience", new[] { typeof(float), typeof(bool) }),
                scopePrefix, finalizer: scopeFinalizer);

            Add("InventoryManager.RefreshHealthbars",
                Reflect.Method(tInventory, "RefreshHealthbars"),
                Reflect.Method(typeof(InventoryManagerPatches), "Prefix"),
                Reflect.Method(typeof(InventoryManagerPatches), "Postfix"),
                finalizer: Reflect.Method(typeof(InventoryManagerPatches), "Finalizer"));

            Add("Skillbar.UpdateExpBar",
                Reflect.Method(tSkillbar, "UpdateExpBar"),
                Reflect.Method(typeof(SkillbarPatches), "Prefix"),
                finalizer: Reflect.Method(typeof(SkillbarPatches), "Finalizer"));

            Add("RoguelikeManager.GetSkillChoices",
                Reflect.Method(tRogue, "GetSkillChoices"),
                prefix: Reflect.Method(typeof(RewardQueryPatches), "PrefixSkillChoices"));

            Add("RoguelikeManager.GetItemChoices",
                Reflect.Method(tRogue, "GetItemChoices"),
                Reflect.Method(typeof(RewardQueryPatches), "PrefixItemChoices"),
                Reflect.Method(typeof(RewardQueryPatches), "PostfixItemChoices"));

            Add("RoguelikeManager.GetRoguelikeLevelsNeededCount",
                Reflect.Method(tRogue, "GetRoguelikeLevelsNeededCount"),
                postfix: Reflect.Method(typeof(RewardQueryPatches), "PostfixNeededCount"));

            Add("RoguelikeManager.OpenSkillSelectWindow",
                Reflect.Method(tRogue, "OpenSkillSelectWindow"),
                postfix: Reflect.Method(typeof(LevelUpStagePatches), "PostfixOpenSkillSelectWindow"));

            Add("RoguelikeManager.RerollSkill",
                Reflect.Method(tRogue, "RerollSkill"),
                prefix: Reflect.Method(typeof(RerollPatches), "PrefixRerollSkill"));

            Add("Character.SyncCharacterToPreset",
                Reflect.Method(tCharacter, "SyncCharacterToPreset"),
                postfix: Reflect.Method(typeof(PresetSyncPatches), "Postfix"));

            if (missing.Count > 0)
            {
                outPlans = null;
                outMissing = missing;
                return false;
            }
            outPlans = plans;
            outMissing = missing;
            return true;
        }

        private static string MissingError(List<string> missing)
        {
            return "alvos Harmony ausentes nesta DLL: " + string.Join(", ", missing.ToArray())
                   + " - NENHUM patch do mod foi aplicado (fail-closed)";
        }

        /// <summary>
        /// Aplica o grupo de gameplay: resolve os alvos, aplica tudo e, se qualquer alvo faltar,
        /// qualquer patch falhar ou o transpiler critico recusar, reverte o grupo inteiro.
        /// </summary>
        public static bool ApplyAll(Harmony harmony, out string error)
        {
            error = null;
            List<Plan> plans;
            List<string> missing;
            if (!TryBuildPlans(out plans, out missing))
            {
                error = MissingError(missing);
                return false;
            }

            var applied = new List<Plan>();
            foreach (var p in plans)
            {
                try
                {
                    var processor = harmony.CreateProcessor(p.Target);
                    if (p.Prefix != null) processor.AddPrefix(new HarmonyMethod(p.Prefix));
                    if (p.Postfix != null) processor.AddPostfix(new HarmonyMethod(p.Postfix));
                    if (p.Transpiler != null) processor.AddTranspiler(new HarmonyMethod(p.Transpiler));
                    if (p.Finalizer != null) processor.AddFinalizer(new HarmonyMethod(p.Finalizer));
                    processor.Patch();
                    applied.Add(p);
                }
                catch (Exception ex)
                {
                    error = "falha ao aplicar " + p.Id + ": " + ex.GetType().Name + ": " + ex.Message;
                    Rollback(harmony, applied.Count);
                    return false;
                }
            }

            if (!BattleResultTranspiler.LastApplied)
            {
                error = "transpiler critico do resultado recusou o alvo ("
                        + (BattleResultTranspiler.LastFailure ?? "motivo desconhecido")
                        + "); grupo de gameplay revertido inteiro";
                Rollback(harmony, applied.Count);
                return false;
            }

            // RLP-1 — FAILSAFE de pos-batalha: aplicado SEPARADAMENTE do grupo critico (best-effort).
            // O grupo critico continua tudo-ou-nada; este prefix apenas ADICIONA o nivel estendido
            // que a janela vanilla nao concedeu, entao uma falha aqui e' no-op (nao ha estado
            // parcial: nenhum patch do jogo e' alterado por ele). Motivo: a janela estrutural fica
            // atras das guardas FastContains/RoguelikeModeActive (IL_0079/IL_008d) e pode nunca ser
            // alcancada — ver RLP-1.
            try
            {
                var failsafeTarget = Reflect.Method(typeof(PostBattleManager), "OpenPostBattleMenu");
                var failsafePrefix = Reflect.Method(typeof(PostBattleFailsafePatches), "Prefix");
                if (failsafeTarget == null || failsafePrefix == null)
                {
                    Log.Warn("failsafe de pos-batalha NAO aplicado: "
                             + (failsafeTarget == null ? "PostBattleManager.OpenPostBattleMenu" : "PostBattleFailsafePatches.Prefix")
                             + " nao resolvido (sem efeito; grupo critico intacto)");
                }
                else
                {
                    var failsafeProcessor = harmony.CreateProcessor(failsafeTarget);
                    failsafeProcessor.AddPrefix(new HarmonyMethod(failsafePrefix));
                    failsafeProcessor.Patch();
                    Log.Info("failsafe de pos-batalha aplicado em PostBattleManager.OpenPostBattleMenu");
                }
            }
            catch (Exception ex)
            {
                Log.Warn("failsafe de pos-batalha NAO aplicado (" + ex.GetType().Name + ": " + ex.Message
                         + "); grupo critico intacto");
            }

            Log.Info("Grupo de gameplay aplicado: " + applied.Count + " alvos; janela estrutural encontrada "
                     + BattleResultTranspiler.LastMatchCount + "x");
            return true;
        }

        /// <summary>Leitura independente do carimbo LastApplied: confere owner de cada alvo AGORA.</summary>
        internal static void LogOwnership(string origin)
        {
            try
            {
                List<Plan> plans;
                List<string> missing;
                if (!TryBuildPlans(out plans, out missing))
                {
                    Log.Refuse("ownership/" + origin, MissingError(missing));
                    return;
                }
                int owned = 0;
                foreach (var p in plans)
                {
                    var info = Harmony.GetPatchInfo(p.Target);
                    if (info != null && info.Owners.Contains(Plugin.PluginGuid)) owned++;
                    else Log.Refuse("ownership/" + origin, "owner ausente em " + p.Id);
                }
                var target = Reflect.Method(typeof(PostBattleManager), "OpenPostBattleMenu");
                var failsafe = target == null ? null : Harmony.GetPatchInfo(target);
                bool prefixOwned = failsafe != null && System.Linq.Enumerable.Any(failsafe.Prefixes,
                    p => p.owner == Plugin.PluginGuid && p.PatchMethod.DeclaringType == typeof(PostBattleFailsafePatches));
                var controlTarget = Reflect.Method(typeof(GameLogic), "GetCharacterLootDropModifier");
                var control = controlTarget == null ? null : Harmony.GetPatchInfo(controlTarget);
                bool debuggerOwned = control != null && control.Owners.Contains("com.gumatos.roguelikedebugger");
                Log.Info("ownership [" + origin + "]: gameplay=" + owned + "/" + plans.Count
                         + " failsafePrefix=" + prefixOwned + " debuggerLootModifier=" + debuggerOwned
                         + " assembly=" + typeof(Root).Assembly.Location
                         + " mvid=" + typeof(Root).Module.ModuleVersionId);
                if (!prefixOwned) Log.Refuse("ownership/" + origin, "prefix failsafe ausente AGORA");
            }
            catch (Exception ex)
            {
                Log.Warn("ownership [" + origin + "] NAO CONFERIDO: " + ex.GetType().Name + ": " + ex.Message);
            }
        }

        private static void Rollback(Harmony harmony, int count)
        {
            try
            {
                Harmony.UnpatchID(Plugin.PluginGuid);
            }
            catch (Exception ex)
            {
                Log.Error("rollback falhou: " + ex.GetType().Name + ": " + ex.Message);
            }
            _ = count;
        }
    }
}
