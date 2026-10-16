using System;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using HarmonyLib;
using RoguelikeUnlimitedLevelProgression.Core;
using RoguelikeUnlimitedLevelProgression.Runtime;

namespace RoguelikeUnlimitedLevelProgression.Patches
{
    /// <summary>
    /// Patch CRITICO do resultado de batalha (parte06 §1). Unico lugar onde a comparacao
    /// `character.Level &lt; settings.RoguelikeMaxLevel` e substituida por Policy.CanAdvance.
    /// Em qualquer duvida o transpiler devolve as instrucoes ORIGINAIS e o grupo de gameplay
    /// inteiro e revertido pelo PatchRegistry (fail-closed).
    /// </summary>
    public static class BattleResultPatches
    {
        internal static BattleResultTarget ResolveTarget(out string missing)
        {
            missing = null;
            var t = new BattleResultTarget();
            t.GetLevel = Reflect.PropertyGetter(typeof(Character), "Level");
            t.GetRoguelikeSettings = Reflect.Method(typeof(GlobalSettingsManager), "get_instance");
            t.RoguelikeManagerField = Reflect.Field(typeof(GlobalSettingsManager), "roguelikeManager");
            t.RoguelikeMaxLevelField = Reflect.Field(typeof(RoguelikeSettings), "RoguelikeMaxLevel");
            t.GiveExperience = Reflect.Method(typeof(Character), "GiveExperience", new[] { typeof(float), typeof(bool) });
            t.ListAddCharacter = Reflect.Method(typeof(List<Character>), "Add", new[] { typeof(Character) });
            t.CanAdvance = Reflect.Method(typeof(Policy), "CanAdvance", new[] { typeof(Character), typeof(RoguelikeSettings) });

            var absent = new List<string>();
            if (t.GetLevel == null) absent.Add("Character::get_Level");
            if (t.GetRoguelikeSettings == null) absent.Add("GlobalSettingsManager::get_instance");
            if (t.RoguelikeManagerField == null) absent.Add("GlobalSettingsManager::roguelikeManager");
            if (t.RoguelikeMaxLevelField == null) absent.Add("RoguelikeSettings::RoguelikeMaxLevel");
            if (t.GiveExperience == null) absent.Add("Character::GiveExperience");
            if (t.ListAddCharacter == null) absent.Add("List<Character>::Add");
            if (t.CanAdvance == null) absent.Add("Policy::CanAdvance");
            if (absent.Count > 0) missing = string.Join(", ", absent.ToArray());
            return t;
        }

        public static IEnumerable<CodeInstruction> Transpiler(IEnumerable<CodeInstruction> instructions)
        {
            string missing;
            var target = ResolveTarget(out missing);
            var original = new List<CodeInstruction>(instructions);
            if (missing != null)
            {
                BattleResultTranspiler.LastApplied = false;
                BattleResultTranspiler.LastFailure = "membros ausentes na DLL: " + missing;
                Log.Error("Transpiler do resultado: " + BattleResultTranspiler.LastFailure);
                return original;
            }

            List<CodeInstruction> rewritten;
            string failure;
            if (!BattleResultTranspiler.TryTransform(original, target, out rewritten, out failure))
            {
                Log.Error("Transpiler do resultado recusou a janela (" + failure + "); IL original mantido");
                return original;
            }
            return rewritten;
        }
    }

    /// <summary>Getter Character.MaxLevel: postfix apenas em roguelike nao-IA (parte05/B).</summary>
    public static class MaxLevelPatches
    {
        public static void Postfix(Character __instance, ref float __result)
        {
            PatchRegistryEvidence.FirstHook("Character.MaxLevel");
            __result = (float)Policy.EffectiveMaxLevel(__instance, __result);
        }
    }

    /// <summary>
    /// Mirror de XP legado (parte06 §2). Acima de 20, para personagem Roguelike estendido,
    /// os dois efeitos vanilla acontecem com mirror FINITO de nivel 20, e o corpo original
    /// (que chamaria o conversor legado exponencial) e pulado. ExperienceLevel real continua
    /// sendo a fonte do nivel e segue sendo salvo.
    /// </summary>
    public static class LegacyMirrorPatches
    {
        public static bool Prefix(Character __instance, float val)
        {
            if (__instance == null) return Log.Vanilla("CharacterOwner", "character=null");
            if (val <= XpCurve.VanillaCapLevel) return Log.Vanilla("Mirror", "nivel <= 20 (mirror vanilla)");
            if (!ExtensionScope.AppliesTo(__instance)) return true;
            try
            {
                if (__instance.IsLoaded)
                {
                    __instance.OldExperience = OldExperienceConverter.GetOldExperienceFromLevel(XpCurve.VanillaCapLevel);
                }
                __instance.QueueCharacterSave();
                if (PluginState.Verbose)
                {
                    Log.Info("Mirror legado limitado ao nivel 20 para " + __instance.CharacterName + " (ExperienceLevel=" + val.ToString("R") + ")");
                }
                return false;
            }
            catch (Exception ex)
            {
                Log.WarnOnce("Mirror legado falhou para " + __instance.CharacterName + ": " + ex.GetType().Name + ": " + ex.Message + " (executando o corpo vanilla)");
                return true;
            }
        }
    }

    /// <summary>
    /// Os 5 conversores estaticos de XP (parte05/C). Nao ha personagem nestes metodos: a
    /// extensao so vale dentro do escopo sincrono aberto por um leitor explicito de personagem.
    /// Abaixo/ate 20, fora do escopo ou com a extensao suprimida: vanilla integral.
    /// </summary>
    public static class XpStaticPatches
    {
        public static bool PrefixFloor(int level, ref float __result)
        {
            if (XpBackend.Suppressed) return Log.Vanilla("XP", "consulta vanilla suprimida pelo backend");
            if (!ExtensionScope.Active) return Log.Vanilla("XP", "escopo de personagem inativo");
            double value;
            if (!XpBackend.TryFloor(level, out value)) return Log.Vanilla("XP.Floor",
                !XpBackend.Ready ? "backend nao pronto" : level <= XpCurve.VanillaCapLevel ? "nivel <= 20 (curva vanilla)" : "piso calculado nao finito");
            __result = (float)value;
            return false;
        }

        public static bool PrefixNext(int level, ref float __result)
        {
            if (XpBackend.Suppressed) return Log.Vanilla("XP", "consulta vanilla suprimida pelo backend");
            if (!ExtensionScope.Active) return Log.Vanilla("XP", "escopo de personagem inativo");
            double value;
            if (!XpBackend.TryTransition(level, out value)) return Log.Vanilla("XP.Next",
                !XpBackend.Ready ? "backend nao pronto" : level <= XpCurve.VanillaCapLevel ? "nivel <= 20 (curva vanilla)" : "transicao calculada invalida");
            __result = (float)value;
            return false;
        }

        /// <summary>Inversa analitica, sem loop sem bound (parte05/C).</summary>
        public static bool PrefixLevelFromXp(float experience, ref float __result)
        {
            if (XpBackend.Suppressed) return Log.Vanilla("XP", "consulta vanilla suprimida pelo backend");
            if (!ExtensionScope.Active) return Log.Vanilla("XP", "escopo de personagem inativo");
            double level;
            if (!XpBackend.TryLevelFromXp(experience, out level)) return Log.Vanilla("XP.LevelFromXp",
                !XpBackend.Ready ? "backend nao pronto" : !XpCurve.IsUsableNumber(experience) ? "XP nao finito" : experience < XpBackend.Floor20 ? "XP abaixo de F20 (curva vanilla)" : "inversa calculada nao finita");
            __result = (float)level;
            return false;
        }

        public static bool PrefixXpFromLevel(float level, ref float __result)
        {
            if (XpBackend.Suppressed) return Log.Vanilla("XP", "consulta vanilla suprimida pelo backend");
            if (!ExtensionScope.Active) return Log.Vanilla("XP", "escopo de personagem inativo");
            if (!XpCurve.IsUsableNumber(level)) return Log.Vanilla("XP.XpFromLevel", "nivel nao finito");
            if (level <= XpCurve.VanillaCapLevel) return Log.Vanilla("XP.XpFromLevel", "nivel <= 20 (curva vanilla)");
            if (!XpBackend.Ready) return Log.Vanilla("XP", "backend nao pronto");
            double value = XpBackend.XpFromLevel(level);
            if (!XpCurve.IsUsableNumber(value)) return Log.Vanilla("XP.XpFromLevel", "XP calculado nao finito");
            __result = (float)value;
            return false;
        }

        public static bool PrefixLevelIndex(float experience, ref int __result)
        {
            if (XpBackend.Suppressed) return Log.Vanilla("XP", "consulta vanilla suprimida pelo backend");
            if (!ExtensionScope.Active) return Log.Vanilla("XP", "escopo de personagem inativo");
            if (!XpBackend.Ready) return Log.Vanilla("XP", "backend nao pronto");
            double x = experience;
            if (!XpCurve.IsUsableNumber(x)) return Log.Vanilla("XP.LevelIndex", "XP nao finito");
            if (x < XpBackend.Floor20) return Log.Vanilla("XP.LevelIndex", "XP abaixo de F20 (curva vanilla)");
            __result = XpCurve.LevelIndexFromXp(XpBackend.Floor20, XpBackend.Transition20, x);
            return false;
        }
    }

    /// <summary>
    /// Escopos sincronos (parte05/C): prefix empilha, finalizer desempilha (inclusive excecao
    /// e nesting). Abaixo disso a extensao nao existe.
    /// </summary>
    public static class ScopePatches
    {
        public static bool PrefixCharacterOwner(Character __instance, out bool __state)
        {
            __state = false;
            if (__instance == null) return Log.Vanilla("CharacterOwner", "character=null");
            if (!ExtensionScope.AppliesTo(__instance)) return true;
            __state = ExtensionScope.Push(__instance);
            return true;
        }

        public static void FinalizerCharacterOwner(bool __state)
        {
            if (__state) ExtensionScope.Pop();
        }
    }
}
