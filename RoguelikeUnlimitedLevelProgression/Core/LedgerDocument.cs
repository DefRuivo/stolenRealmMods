using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace RoguelikeUnlimitedLevelProgression.Core
{
    public sealed class SkillReceipt
    {
        public int Ordinal;
        public int EarnedLevel;
        public string Reason = ReceiptReasons.EmptySkillPool;

        public const string ReasonEmptySkillPool = "empty_skill_pool";
    }

    public static class ReceiptReasons
    {
        public const string EmptySkillPool = "empty_skill_pool";
    }

    public enum LedgerParseStatus
    {
        Ok = 0,
        Corrupted = 1,
        UnsupportedSchema = 2,
        IdentityMismatch = 3,
    }

    /// <summary>
    /// Sidecar v1 (parte05 §4), schema FIXO:
    /// {"schema_version":1,"character_guid":"&lt;guid&gt;","run_id":"&lt;uuid&gt;","preset_guid":"&lt;guid&gt;",
    ///  "skipped_skill_receipts":[{"ordinal":1,"earned_level":21,"reason":"empty_skill_pool"}]}
    /// Sem PII/tokens. Nivel/skills/pontos continuam no save vanilla.
    /// </summary>
    public sealed class LedgerDocument
    {
        public const int CurrentSchemaVersion = 1;

        public int SchemaVersion = CurrentSchemaVersion;
        public string CharacterGuid = "";
        public string RunId = "";
        public string PresetGuid = "";
        public readonly List<SkillReceipt> SkippedSkillReceipts = new List<SkillReceipt>();

        /// <summary>
        /// Numero de skills substituidas por recibo (S). E o valor subtraido de
        /// GetRoguelikeLevelsNeededCount. Recibos nao concedem dinheiro/atributos.
        /// </summary>
        public int SkippedSkillCount { get { return SkippedSkillReceipts.Count; } }

        public int NextOrdinal()
        {
            int max = 0;
            for (int i = 0; i < SkippedSkillReceipts.Count; i++)
            {
                if (SkippedSkillReceipts[i].Ordinal > max) max = SkippedSkillReceipts[i].Ordinal;
            }
            return max + 1;
        }

        /// <summary>Adiciona um recibo idempotente. Devolve false se o ordinal ja existia (dedupe).</summary>
        public bool AddReceipt(int ordinal, int earnedLevel, string reason)
        {
            for (int i = 0; i < SkippedSkillReceipts.Count; i++)
            {
                if (SkippedSkillReceipts[i].Ordinal == ordinal) return false;
            }
            SkippedSkillReceipts.Add(new SkillReceipt { Ordinal = ordinal, EarnedLevel = earnedLevel, Reason = reason });
            SkippedSkillReceipts.Sort((a, b) => a.Ordinal.CompareTo(b.Ordinal));
            return true;
        }

        public string Serialize()
        {
            var sb = new StringBuilder(256);
            sb.Append("{\"schema_version\":").Append(MiniJson.Number(SchemaVersion));
            sb.Append(",\"character_guid\":").Append(MiniJson.Escape(CharacterGuid));
            sb.Append(",\"run_id\":").Append(MiniJson.Escape(RunId));
            sb.Append(",\"preset_guid\":").Append(MiniJson.Escape(PresetGuid));
            sb.Append(",\"skipped_skill_receipts\":[");
            for (int i = 0; i < SkippedSkillReceipts.Count; i++)
            {
                if (i > 0) sb.Append(',');
                var r = SkippedSkillReceipts[i];
                sb.Append("{\"ordinal\":").Append(MiniJson.Number(r.Ordinal));
                sb.Append(",\"earned_level\":").Append(MiniJson.Number(r.EarnedLevel));
                sb.Append(",\"reason\":").Append(MiniJson.Escape(r.Reason));
                sb.Append('}');
            }
            sb.Append("]}");
            return sb.ToString();
        }

        public static LedgerParseStatus Parse(string text, out LedgerDocument doc, out string error)
        {
            doc = null;
            error = null;
            var root = MiniJson.TryParseObject(text, out error);
            if (root == null) return LedgerParseStatus.Corrupted;

            object v;
            if (!root.TryGetValue("schema_version", out v)) { error = "schema_version ausente"; return LedgerParseStatus.Corrupted; }
            int version = AsInt(v, out error);
            if (error != null) return LedgerParseStatus.Corrupted;
            if (version != CurrentSchemaVersion) { error = "schema_version " + version + " nao suportado"; return LedgerParseStatus.UnsupportedSchema; }

            var d = new LedgerDocument { SchemaVersion = version };
            if (!TryString(root, "character_guid", out d.CharacterGuid, out error)) return Fail(error, LedgerParseStatus.Corrupted);
            if (!TryString(root, "run_id", out d.RunId, out error)) return Fail(error, LedgerParseStatus.Corrupted);
            if (!TryString(root, "preset_guid", out d.PresetGuid, out error)) return Fail(error, LedgerParseStatus.Corrupted);

            object arrObj;
            if (!root.TryGetValue("skipped_skill_receipts", out arrObj)) { error = "skipped_skill_receipts ausente"; return LedgerParseStatus.Corrupted; }
            var arr = arrObj as List<object>;
            if (arr == null) { error = "skipped_skill_receipts nao e array"; return LedgerParseStatus.Corrupted; }
            var seen = new HashSet<int>();
            foreach (var item in arr)
            {
                var o = item as Dictionary<string, object>;
                if (o == null) { error = "recibo nao e objeto"; return LedgerParseStatus.Corrupted; }
                int ordinal = AsInt(Require(o, "ordinal", ref error), out error);
                if (error != null) return LedgerParseStatus.Corrupted;
                int earned = AsInt(Require(o, "earned_level", ref error), out error);
                if (error != null) return LedgerParseStatus.Corrupted;
                string reason;
                if (!TryString(o, "reason", out reason, out error)) return LedgerParseStatus.Corrupted;
                if (!seen.Add(ordinal)) { error = "ordinal duplicado: " + ordinal; return LedgerParseStatus.Corrupted; }
                d.SkippedSkillReceipts.Add(new SkillReceipt { Ordinal = ordinal, EarnedLevel = earned, Reason = reason });
            }
            d.SkippedSkillReceipts.Sort((a, b) => a.Ordinal.CompareTo(b.Ordinal));
            doc = d;
            return LedgerParseStatus.Ok;
        }

        private static LedgerParseStatus Fail(string error, LedgerParseStatus status)
        {
            return status;
        }

        private static object Require(Dictionary<string, object> o, string key, ref string error)
        {
            object v;
            if (!o.TryGetValue(key, out v)) { error = key + " ausente"; return null; }
            return v;
        }

        private static bool TryString(Dictionary<string, object> o, string key, out string value, out string error)
        {
            value = null;
            error = null;
            object v;
            if (!o.TryGetValue(key, out v)) { error = key + " ausente"; return false; }
            if (v == null) { value = ""; return true; }
            var s = v as string;
            if (s == null) { error = key + " nao e string"; return false; }
            value = s;
            return true;
        }

        private static int AsInt(object v, out string error)
        {
            error = null;
            if (v is long) return (int)(long)v;
            if (v is double)
            {
                double d = (double)v;
                if (Math.Floor(d) != d) { error = "inteiro esperado"; return 0; }
                return (int)d;
            }
            error = "inteiro esperado";
            return 0;
        }
    }
}
