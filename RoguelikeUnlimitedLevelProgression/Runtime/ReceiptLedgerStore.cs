using System;
using System.IO;
using System.Text;
using RoguelikeUnlimitedLevelProgression.Core;

namespace RoguelikeUnlimitedLevelProgression.Runtime
{
    public enum LedgerLoadStatus
    {
        Missing = 0,
        Ok = 1,
        Corrupted = 2,
        UnsupportedSchema = 3,
        IdentityMismatch = 4,
        WriteFailure = 5,
    }

    public sealed class LedgerWriteException : Exception
    {
        public LedgerWriteException(string message, Exception inner) : base(message, inner) { }
    }

    /// <summary>
    /// Guarda do sidecar v1: leitura/escrita atomica (temporario + replace + backup) em
    /// &lt;base&gt;/&lt;character-guid&gt;.json. Nao usa o indice do save como identidade.
    /// Falha de escrita NAO pode consumir recompensa: quem chama trata LedgerWriteException.
    /// Sem dependencia de UnityEngine (Paths.ConfigPath e passado pelo Plugin), para que o
    /// harness isolado exercite o codigo real em um diretorio temporario.
    /// </summary>
    public sealed class ReceiptLedgerStore
    {
        private readonly string _dir;

        public ReceiptLedgerStore(string directory)
        {
            if (string.IsNullOrEmpty(directory)) throw new ArgumentNullException(nameof(directory));
            _dir = directory;
        }

        public string Directory { get { return _dir; } }

        public string PathFor(string characterGuid)
        {
            return Path.Combine(_dir, SafeName(characterGuid) + ".json");
        }

        public string BackupPathFor(string characterGuid)
        {
            return Path.Combine(_dir, SafeName(characterGuid) + ".json.bak");
        }

        public static string SafeName(string guid)
        {
            if (string.IsNullOrEmpty(guid)) return "unknown";
            var sb = new StringBuilder(guid.Length);
            foreach (char c in guid)
            {
                bool ok = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '-' || c == '_';
                sb.Append(ok ? c : '_');
            }
            return sb.ToString();
        }

        public LedgerLoadStatus Load(string characterGuid, string expectedPresetGuid, out LedgerDocument doc, out string error)
        {
            doc = null;
            error = null;
            string path = PathFor(characterGuid);
            if (!File.Exists(path))
            {
                return LedgerLoadStatus.Missing;
            }

            string text;
            try
            {
                text = File.ReadAllText(path, Encoding.UTF8);
            }
            catch (Exception ex)
            {
                error = "leitura falhou: " + ex.Message;
                return LedgerLoadStatus.Corrupted;
            }

            LedgerParseStatus status = LedgerDocument.Parse(text, out doc, out error);
            if (status == LedgerParseStatus.UnsupportedSchema) return LedgerLoadStatus.UnsupportedSchema;
            if (status != LedgerParseStatus.Ok)
            {
                if (string.IsNullOrEmpty(error)) error = "ledger corrompido";
                doc = null;
                return LedgerLoadStatus.Corrupted;
            }

            if (!string.IsNullOrEmpty(expectedPresetGuid)
                && !string.IsNullOrEmpty(doc.PresetGuid)
                && !string.Equals(doc.PresetGuid, expectedPresetGuid, StringComparison.OrdinalIgnoreCase))
            {
                error = "preset_guid divergente: ledger=" + doc.PresetGuid + " esperado=" + expectedPresetGuid;
                doc = null;
                return LedgerLoadStatus.IdentityMismatch;
            }
            if (!string.IsNullOrEmpty(characterGuid)
                && !string.IsNullOrEmpty(doc.CharacterGuid)
                && !string.Equals(doc.CharacterGuid, characterGuid, StringComparison.OrdinalIgnoreCase))
            {
                error = "character_guid divergente";
                doc = null;
                return LedgerLoadStatus.IdentityMismatch;
            }
            return LedgerLoadStatus.Ok;
        }

        public void Save(LedgerDocument doc)
        {
            if (doc == null) throw new ArgumentNullException(nameof(doc));
            string path = PathFor(doc.CharacterGuid);
            string tmp = path + ".tmp";
            string json = doc.Serialize();
            try
            {
                // A criacao do diretorio DEVE estar dentro do try: uma falha de disco/permissao
                // aqui tambem e falha de gravacao (LedgerWriteException) e nao pode escapar como
                // excecao crua para o fluxo de recompensa do jogo.
                System.IO.Directory.CreateDirectory(_dir);
                File.WriteAllText(tmp, json, new UTF8Encoding(encoderShouldEmitUTF8Identifier: false));
                if (File.Exists(path))
                {
                    File.Replace(tmp, path, BackupPathFor(doc.CharacterGuid), ignoreMetadataErrors: true);
                }
                else
                {
                    File.Move(tmp, path);
                }
            }
            catch (Exception ex)
            {
                try { if (File.Exists(tmp)) File.Delete(tmp); } catch { /* limpeza best-effort */ }
                throw new LedgerWriteException("falha ao gravar o sidecar em " + path, ex);
            }
        }

        /// <summary>Cria um documento novo (run nova) preservando guid/preset.</summary>
        public static LedgerDocument NewRun(string characterGuid, string presetGuid)
        {
            return new LedgerDocument
            {
                SchemaVersion = LedgerDocument.CurrentSchemaVersion,
                CharacterGuid = characterGuid ?? "",
                RunId = Guid.NewGuid().ToString(),
                PresetGuid = presetGuid ?? "",
            };
        }

        /// <summary>
        /// Reset de run: SO deve ser chamado apos SyncCharacterToPreset valido (parte05 §4).
        /// Guid/preset nulos NAO resetam (o chamador nao deve nem chamar).
        /// </summary>
        public static void StartNewRun(LedgerDocument doc, string presetGuid)
        {
            if (doc == null) throw new ArgumentNullException(nameof(doc));
            doc.RunId = Guid.NewGuid().ToString();
            if (!string.IsNullOrEmpty(presetGuid)) doc.PresetGuid = presetGuid;
            doc.SkippedSkillReceipts.Clear();
        }
    }
}
