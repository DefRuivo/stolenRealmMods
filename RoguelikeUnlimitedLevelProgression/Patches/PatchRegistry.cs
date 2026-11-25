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

            // BANTER-1 (1.4.9 / 26878331): Root.SendGameCompleteFromServer NAO recebe patch nenhum.
            // Qualquer patch Harmony nesse metodo (prefix, postfix, transpiler — ate' um transpiler
            // que devolve as instrucoes intactas) faz o HarmonyX RECONSTRUIR o corpo inteiro com o
            // ILManipulator, e o emissor descarta o `leave` que sai do `if` do banter (#317) e emite
            // um `leave` sintetico para o fim do handler: o alvo vira #322, o inicio do `else`, e o
            // ramo do `else` passa a rodar EM ADICAO ao `if`. Sintoma medido: segunda fala atribuida
            // ao heroi e espera por clique antes da janela de recompensa.
            // A concessao do nivel estendido vive no prefix de PostBattleManager.OpenPostBattleMenu
            // (mesma lista, mesma Policy). Aqui so' se verifica o CONTRATO: se o metodo sumir, o
            // grupo inteiro recusa aplicar (fail-closed) em vez de seguir sem a garantia.
            if (Reflect.Method(typeof(Root), "SendGameCompleteFromServer") == null)
            {
                missing.Add("Root.SendGameCompleteFromServer#contrato-nao-patcheado");
            }

            Add("PostBattleManager.OpenPostBattleMenu",
                Reflect.Method(typeof(PostBattleManager), "OpenPostBattleMenu"),
                prefix: Reflect.Method(typeof(PostBattleFailsafePatches), "Prefix"));

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

            // R-ULLP-1 — clamp de BuildCode.CreateCharacter (tipo NOVO da beta 1.4.8).
            // Best-effort, mesma regra do failsafe acima: o postfix apenas RESTAURA o nivel que o
            // clamp vanilla rebaixou (e so quando a configuracao do dono pede nivel acima do vanilla).
            // Sem ele o comportamento e' exatamente o de hoje, portanto uma falha aqui nao deixa
            // estado parcial e nao pode derrubar o grupo critico.
            try
            {
                MethodInfo bcTarget;
                MethodInfo bcPostfix;
                string bcDetail;
                if (!BuildCodePatches.TryResolve(out bcTarget, out bcPostfix, out bcDetail))
                {
                    Log.Info("build code: postfix NAO aplicado (" + bcDetail + "); grupo critico intacto");
                }
                else
                {
                    var bcProcessor = harmony.CreateProcessor(bcTarget);
                    bcProcessor.AddPostfix(new HarmonyMethod(bcPostfix));
                    bcProcessor.Patch();
                    Log.Info("build code: postfix aplicado em " + bcDetail + " (R-ULLP-1)");
                }
            }
            catch (Exception ex)
            {
                Log.Warn("build code: postfix NAO aplicado (" + ex.GetType().Name + ": " + ex.Message
                         + "); grupo critico intacto");
            }

            Log.Info("Grupo de gameplay aplicado: " + applied.Count + " alvos; "
                     + "Root.SendGameCompleteFromServer sem patch (BANTER-1)");
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
                // BANTER-1: o metodo de resultado nao pode ter NENHUM patch deste mod. Se aparecer
                // um, o corpo foi reemitido e a duplicacao do banter volta.
                var resultTarget = Reflect.Method(typeof(Root), "SendGameCompleteFromServer");
                var resultInfo = resultTarget == null ? null : Harmony.GetPatchInfo(resultTarget);
                bool resultPatched = resultInfo != null && resultInfo.Owners.Contains(Plugin.PluginGuid);
                var controlTarget = Reflect.Method(typeof(GameLogic), "GetCharacterLootDropModifier");
                var control = controlTarget == null ? null : Harmony.GetPatchInfo(controlTarget);
                bool debuggerOwned = control != null && control.Owners.Contains("com.gumatos.roguelikedebugger");
                Log.Info("ownership [" + origin + "]: gameplay=" + owned + "/" + plans.Count
                         + " resultPatched=" + resultPatched + " debuggerLootModifier=" + debuggerOwned
                         + " assembly=" + typeof(Root).Assembly.Location
                         + " mvid=" + typeof(Root).Module.ModuleVersionId);
                if (resultPatched) Log.Refuse("ownership/" + origin, "Root.SendGameCompleteFromServer PATCHED (BANTER-1)");
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
