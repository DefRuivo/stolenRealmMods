using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using HarmonyLib;

namespace RoguelikeLevelProgression.Patches
{
    /// <summary>Membros reais do alvo, resolvidos por AccessTools em tempo de carga.</summary>
    public sealed class BattleResultTarget
    {
        public MethodInfo GetLevel;
        public MethodInfo GetRoguelikeSettings;   // GlobalSettingsManager::get_instance
        public FieldInfo RoguelikeManagerField;   // GlobalSettingsManager::roguelikeManager
        public FieldInfo RoguelikeMaxLevelField;  // RoguelikeSettings::RoguelikeMaxLevel
        public MethodInfo GiveExperience;
        public MethodInfo ListAddCharacter;
        public MethodInfo CanAdvance;             // Policy.CanAdvance(Character, RoguelikeSettings)
    }

    /// <summary>
    /// NUCLEO do patch critico (parte06 §1). Nao hardcode local index nem offset IL:
    /// a janela e reconhecida pela ASSINATURA ESTRUTURAL das instrucoes e dos membros.
    ///
    /// Janela vanilla unica (corpus 647428-647433 / evidence/root-result.il.txt):
    ///   ldloc.X                       ; Character
    ///   callvirt  Character::get_Level
    ///   call      GlobalSettingsManager::get_instance
    ///   ldfld     GlobalSettingsManager::roguelikeManager   (RoguelikeSettings)
    ///   ldfld     RoguelikeSettings::RoguelikeMaxLevel      (int32)
    ///   bge(.s)   destino
    /// Reescrita:
    ///   ldloc.X
    ///   call      GlobalSettingsManager::get_instance
    ///   ldfld     GlobalSettingsManager::roguelikeManager
    ///   call      Policy.CanAdvance(Character, RoguelikeSettings)  -> bool
    ///   brfalse(.s) MESMO destino
    /// O stack muda de [int,int] (bge) para [bool] (brfalse), o que e exatamente a comparacao
    /// "pode avancar" — false pula premio E inclusao na lista, pois o alvo do branch e o fim
    /// do bloco (IL_00c6), apos GiveExperience e List::Add.
    ///
    /// Exigencia: EXATAMENTE UMA correspondencia completa, com cauda de premio
    /// (GiveExperience + List&lt;Character&gt;::Add) presente entre o branch e seu destino.
    /// Qualquer ambiguidade ou ausencia = falha explicita (o grupo de gameplay faz rollback).
    /// </summary>
    public static class BattleResultTranspiler
    {
        public static int LastMatchCount = -1;
        public static string LastFailure = "transpiler ainda nao executado";
        public static bool LastApplied;

        public static bool TryTransform(IList<CodeInstruction> input, BattleResultTarget t,
                                        out List<CodeInstruction> result, out string failure)
        {
            result = null;
            failure = null;

            var ins = new List<CodeInstruction>(input);
            int match = -1;
            int matches = 0;
            for (int i = 0; i + 5 < ins.Count; i++)
            {
                string reason;
                if (WindowMatches(ins, i, t, out reason))
                {
                    matches++;
                    if (match < 0) match = i;
                }
            }
            LastMatchCount = matches;

            if (matches == 0)
            {
                failure = "nenhuma correspondencia estrutural completa no bloco de resultado";
                LastFailure = failure;
                LastApplied = false;
                return false;
            }
            if (matches > 1)
            {
                failure = "correspondencia ambigua: " + matches + " janelas casaram";
                LastFailure = failure;
                LastApplied = false;
                return false;
            }
            if (!HasPrizeTail(ins, match, t, out failure))
            {
                LastFailure = failure;
                LastApplied = false;
                return false;
            }
            if (!CanRewrite(ins, match, t, out failure))
            {
                LastFailure = failure;
                LastApplied = false;
                return false;
            }

            int levelLoad = match, getLevel = match + 1, getSettings = match + 2;
            int settingsField = match + 3, maxLevelField = match + 4, branch = match + 5;

            // preserva labels/exception blocks da instrucao que esta sendo substituida
            var canAdvance = new CodeInstruction(OpCodes.Call, t.CanAdvance);
            CopyList(ins[maxLevelField], canAdvance, "labels");
            CopyList(ins[maxLevelField], canAdvance, "blocks");
            ins[maxLevelField] = canAdvance;

            // bge -> brfalse para o MESMO destino, mantendo labels/blocks e o operando original
            CodeInstruction br = ins[branch];
            br.opcode = br.opcode == OpCodes.Bge_S ? OpCodes.Brfalse_S : OpCodes.Brfalse;

            ins.RemoveAt(getLevel);

            // getSettings/settingsField/levelLoad permanecem intactos (labels preservadas)
            _ = getSettings;
            _ = settingsField;
            _ = levelLoad;

            result = ins;
            LastFailure = null;
            LastApplied = true;
            return true;
        }

        private static bool IsAnyLocalLoad(OpCode op)
        {
            // ldloc.0..3, ldloc.s, ldloc — sem fixar o indice (parte06: nao hardcode local 4)
            if (op == OpCodes.Ldloc_0 || op == OpCodes.Ldloc_1 || op == OpCodes.Ldloc_2 || op == OpCodes.Ldloc_3) return true;
            return op == OpCodes.Ldloc || op == OpCodes.Ldloc_S;
        }

        private static bool SameMethod(object operand, MethodInfo expected)
        {
            if (expected == null || operand == null) return false;
            var mi = operand as MethodInfo;
            if (mi == null) return false;
            if (mi == expected) return true;
            return mi.MetadataToken == expected.MetadataToken
                && mi.DeclaringType == expected.DeclaringType
                && string.Equals(mi.Name, expected.Name, System.StringComparison.Ordinal);
        }

        private static bool SameField(object operand, FieldInfo expected)
        {
            if (expected == null || operand == null) return false;
            var fi = operand as FieldInfo;
            if (fi == null) return false;
            if (fi == expected) return true;
            return fi.MetadataToken == expected.MetadataToken
                && fi.DeclaringType == expected.DeclaringType
                && string.Equals(fi.Name, expected.Name, System.StringComparison.Ordinal);
        }

        private static bool WindowMatches(IList<CodeInstruction> ins, int i, BattleResultTarget t, out string reason)
        {
            reason = null;
            if (!IsAnyLocalLoad(ins[i].opcode)) return false;
            if (ins[i + 1].opcode != OpCodes.Callvirt || !SameMethod(ins[i + 1].operand, t.GetLevel)) return false;
            if (ins[i + 2].opcode != OpCodes.Call || !SameMethod(ins[i + 2].operand, t.GetRoguelikeSettings)) return false;
            if (ins[i + 3].opcode != OpCodes.Ldfld || !SameField(ins[i + 3].operand, t.RoguelikeManagerField)) return false;
            if (ins[i + 4].opcode != OpCodes.Ldfld || !SameField(ins[i + 4].operand, t.RoguelikeMaxLevelField)) return false;
            OpCode b = ins[i + 5].opcode;
            if (b != OpCodes.Bge_S && b != OpCodes.Bge) return false;
            if (!IsBranchTarget(ins[i + 5].operand)) return false;
            reason = "ok";
            return true;
        }

        /// <summary>
        /// Verifica, SEM nomear o tipo Label (que vive em mscorlib e nao resolve no alvo
        /// netstandard2.1), que o operando e um alvo de branch real.
        /// </summary>
        private static bool IsBranchTarget(object operand)
        {
            if (operand == null) return false;
            return operand.GetType().FullName == "System.Reflection.Emit.Label";
        }

        private static System.Collections.IList ListOf(CodeInstruction ci, string name)
        {
            var f = Reflect.Field(typeof(CodeInstruction), name);
            if (f != null) return f.GetValue(ci) as System.Collections.IList;
            var p = Reflect.Property(typeof(CodeInstruction), name);
            if (p != null) return p.GetValue(ci, null) as System.Collections.IList;
            return null;
        }

        private static void CopyList(CodeInstruction from, CodeInstruction to, string name)
        {
            var src = ListOf(from, name);
            var dst = ListOf(to, name);
            if (src == null || dst == null) return;
            for (int i = 0; i < src.Count; i++) dst.Add(src[i]);
        }

        private static int CountOf(CodeInstruction ci, string name)
        {
            var l = ListOf(ci, name);
            return l == null ? 0 : l.Count;
        }

        private static bool LabelsContain(CodeInstruction ci, object target)
        {
            var l = ListOf(ci, "labels");
            if (l == null) return false;
            for (int i = 0; i < l.Count; i++)
            {
                if (Equals(l[i], target)) return true;
            }
            return false;
        }

        /// <summary>
        /// Cauda de premio: entre a janela e o destino do branch precisa existir a chamada
        /// GiveExperience(float,bool) E o Add na lista roguelikeCharactersThatShouldLevel.
        /// </summary>
        private static bool HasPrizeTail(IList<CodeInstruction> ins, int match, BattleResultTarget t, out string failure)
        {
            failure = null;
            int branch = match + 5;
            object target = ins[branch].operand;
            bool giveExperience = false, listAdd = false;
            int limit = System.Math.Min(ins.Count, branch + 24);
            for (int j = branch + 1; j < limit; j++)
            {
                if (LabelsContain(ins[j], target)) break;
                if ((ins[j].opcode == OpCodes.Callvirt || ins[j].opcode == OpCodes.Call) && SameMethod(ins[j].operand, t.GiveExperience))
                {
                    giveExperience = true;
                    continue;
                }
                if (ins[j].opcode == OpCodes.Callvirt && SameMethod(ins[j].operand, t.ListAddCharacter))
                {
                    listAdd = true;
                }
            }
            if (!giveExperience)
            {
                failure = "cauda de premio ausente: GiveExperience nao encontrado entre o branch e seu destino";
                return false;
            }
            if (!listAdd)
            {
                failure = "cauda de premio ausente: List<Character>::Add nao encontrado entre o branch e seu destino";
                return false;
            }
            return true;
        }

        private static bool CanRewrite(IList<CodeInstruction> ins, int match, BattleResultTarget t, out string failure)
        {
            failure = null;
            var removed = ins[match + 1];
            if (CountOf(removed, "labels") > 0 || CountOf(removed, "blocks") > 0)
            {
                failure = "a instrucao get_Level removida possui labels/exception blocks: reescrita insegura";
                return false;
            }
            if (t.CanAdvance == null)
            {
                failure = "Policy.CanAdvance nao resolvido";
                return false;
            }
            return true;
        }
    }
}
