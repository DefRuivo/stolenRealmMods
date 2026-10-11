using System;
using System.Collections.Generic;
using System.IO;
using RoguelikeLevelProgression.Core;

namespace RoguelikeLevelProgression.Runtime
{
    /// <summary>
    /// Servico do sidecar: identidade do personagem, cache por guid, gravacao atomica e
    /// reset de run. Falha de gravacao NAO consome a recompensa: quem pergunta decide.
    /// </summary>
    internal static class LedgerService
    {
        internal const string ModFolderName = "com.gumatos.roguelikelevelprogression";

        private static readonly object _gate = new object();
        private static readonly Dictionary<string, LedgerDocument> _cache = new Dictionary<string, LedgerDocument>(StringComparer.OrdinalIgnoreCase);
        private static readonly Dictionary<string, LedgerLoadStatus> _status = new Dictionary<string, LedgerLoadStatus>(StringComparer.OrdinalIgnoreCase);
        private static ReceiptLedgerStore _store;

        public static ReceiptLedgerStore Store { get { return _store; } }

        public static void ConfigureDefault(string configPath)
        {
            _store = new ReceiptLedgerStore(Path.Combine(configPath, ModFolderName, "receipts"));
            Log.Info("Ledger em " + _store.Directory);
        }

        public static void ConfigureStoreForTests(ReceiptLedgerStore store)
        {
            _store = store;
            ResetAll();
        }

        public static void ResetAll()
        {
            lock (_gate)
            {
                _cache.Clear();
                _status.Clear();
            }
        }

        /// <summary>Identidade estavel do personagem (CharacterSaveFile.Guid), com fallbacks explicitos.</summary>
        public static string IdentityOf(Character c)
        {
            if (c == null) return null;
            try
            {
                var save = c.CharacterSaveFile;
                if (save != null && !string.IsNullOrEmpty(save.Guid)) return save.Guid;
            }
            catch (Exception) { }
            try
            {
                if (!string.IsNullOrEmpty(c.CharacterPresetFileGuid)) return "preset-" + c.CharacterPresetFileGuid;
            }
            catch (Exception) { }
            try
            {
                return "owner" + c.OwnerID + "-" + (c.CharacterName ?? "unknown");
            }
            catch (Exception) { }
            return null;
        }

        public static string PresetGuidOf(Character c)
        {
            if (c == null) return "";
            try { return c.CharacterPresetFileGuid ?? ""; }
            catch (Exception) { return ""; }
        }

        private static LedgerDocument EnsureLoaded(string guid, string presetGuid)
        {
            LedgerDocument doc;
            if (_cache.TryGetValue(guid, out doc)) return doc;
            if (_store == null)
            {
                _status[guid] = LedgerLoadStatus.Corrupted;
                return null;
            }

            string error;
            var st = _store.Load(guid, presetGuid, out doc, out error);
            switch (st)
            {
                case LedgerLoadStatus.Missing:
                    doc = ReceiptLedgerStore.NewRun(guid, presetGuid);
                    _cache[guid] = doc;
                    _status[guid] = LedgerLoadStatus.Missing;
                    if (PluginState.Verbose) Log.Info("Ledger novo para " + guid + " (run " + doc.RunId + ")");
                    return doc;
                case LedgerLoadStatus.Ok:
                    _cache[guid] = doc;
                    _status[guid] = LedgerLoadStatus.Ok;
                    return doc;
                default:
                    _status[guid] = st;
                    Log.Error("Ledger de " + guid + " nao utilizavel (" + st + "): " + error
                              + " - a recompensa NAO sera consumida nem convertida em recibo");
                    return null;
            }
        }

        public static LedgerLoadStatus StatusOf(string guid)
        {
            LedgerLoadStatus st;
            if (guid != null && _status.TryGetValue(guid, out st)) return st;
            return LedgerLoadStatus.Missing;
        }

        /// <summary>Numero de skills substituidas (S) para o personagem. 0 quando o ledger nao e utilizavel.</summary>
        public static int ReceiptCount(Character c)
        {
            return ReceiptCountByGuid(IdentityOf(c), PresetGuidOf(c));
        }

        /// <summary>
        /// Mesma contagem com a identidade explicita. Existe para o harness isolado exercitar o
        /// caminho real de load/cache/contagem sem instanciar Character (que exige o runtime Unity).
        /// O mod sempre entra por ReceiptCount(Character).
        /// </summary>
        public static int ReceiptCountByGuid(string guid, string presetGuid)
        {
            if (guid == null) return 0;
            lock (_gate)
            {
                var doc = EnsureLoaded(guid, presetGuid);
                if (doc == null) return 0;
                return doc.SkippedSkillCount;
            }
        }

        /// <summary>
        /// Registra um recibo permanente de skill nao concedida. A gravacao precisa concluir
        /// ANTES de o estagio ser pulado; do contrario devolve false e o chamador nao consome.
        /// </summary>
        public static bool TryRecordSkippedSkill(Character c, int earnedLevel, out string error)
        {
            return TryRecordSkippedSkillByGuid(IdentityOf(c), PresetGuidOf(c), earnedLevel, out error);
        }

        /// <summary>Mesma rotina com a identidade explicita (seam do harness isolado).</summary>
        public static bool TryRecordSkippedSkillByGuid(string guid, string presetGuid, int earnedLevel, out string error)
        {
            error = null;
            if (guid == null)
            {
                error = "identidade do personagem indisponivel";
                return false;
            }
            lock (_gate)
            {
                var doc = EnsureLoaded(guid, presetGuid);
                if (doc == null)
                {
                    error = "ledger nao utilizavel (" + StatusOf(guid) + ")";
                    return false;
                }
                int ordinal = doc.NextOrdinal();
                if (!doc.AddReceipt(ordinal, earnedLevel, ReceiptReasons.EmptySkillPool))
                {
                    // dedupe: ja existia um recibo com esse ordinal
                    return true;
                }
                try
                {
                    _store.Save(doc);
                    _status[guid] = LedgerLoadStatus.Ok;
                }
                catch (LedgerWriteException ex)
                {
                    // rollback do recibo em memoria: nao consumir a recompensa
                    doc.SkippedSkillReceipts.RemoveAll(r => r.Ordinal == ordinal);
                    error = "falha ao gravar o recibo: " + ex.Message;
                    Log.Error("Recibo de skill nao gravado para " + guid + ": " + error);
                    return false;
                }
                Log.Info("Recibo de skill registrado: guid=" + guid + " ordinal=" + ordinal
                         + " nivel=" + earnedLevel + " motivo=" + ReceiptReasons.EmptySkillPool
                         + " (S=" + doc.SkippedSkillCount + ")");
                return true;
            }
        }

        /// <summary>
        /// Reset de run. Chamado SOMENTE depois de SyncCharacterToPreset valido (parte05 §4);
        /// preset nulo nao reseta.
        /// </summary>
        public static void OnPresetSyncSuccess(Character c, string presetGuid)
        {
            if (c == null) return;
            OnPresetSyncSuccessByGuid(IdentityOf(c), presetGuid);
        }

        /// <summary>Mesmo reset com a identidade explicita (seam do harness isolado).</summary>
        public static void OnPresetSyncSuccessByGuid(string guid, string presetGuid)
        {
            if (string.IsNullOrEmpty(presetGuid))
            {
                Log.Warn("SyncCharacterToPreset sem preset valido: ledger NAO foi resetado");
                return;
            }
            if (guid == null) return;
            lock (_gate)
            {
                var doc = EnsureLoaded(guid, presetGuid);
                if (doc == null)
                {
                    // ledger corrompido: um reset sobrescreveria prova; cria documento novo e loga
                    doc = ReceiptLedgerStore.NewRun(guid, presetGuid);
                    _cache[guid] = doc;
                    Log.Warn("Ledger de " + guid + " estava " + StatusOf(guid) + "; criando documento novo para a run");
                }
                else
                {
                    ReceiptLedgerStore.StartNewRun(doc, presetGuid);
                }
                try
                {
                    _store.Save(doc);
                    _status[guid] = LedgerLoadStatus.Ok;
                    Log.Info("Run resetada para " + guid + " (run " + doc.RunId + ")");
                }
                catch (LedgerWriteException ex)
                {
                    Log.Error("Falha ao gravar a run resetada de " + guid + ": " + ex.Message);
                }
            }
        }
    }
}
