using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace BetterPortuguese.Core;

// addEntry v1 creates a single neutral Value entry only for a known empty/absent
// Original record. It never appends to populated lists or creates snapshot identities.
internal sealed class EntryAddition
{
    public Entry After { get; }
    private EntryAddition(Entry after) { After = after; }

    public static EntryAddition Parse(Dictionary<string, object> d, Snapshot original)
    {
        JsonShape.Fields(d, "operation", "id", "key", "entryIndex", "before", "after", "approvalTaskId");
        if (JsonShape.Text(d["operation"]) != "addEntry") throw new FormatException("Unsupported diff operation");
        string id = JsonShape.Text(d["id"]), key = JsonShape.Text(d["key"]);
        string prefix = "addEntry " + id + ": ";
        if (!Regex.IsMatch(JsonShape.Text(d["approvalTaskId"]), "^t_[a-f0-9]{8}$")) throw new FormatException(prefix + "Approval task missing/invalid");
        if (!original.Records.TryGetValue(key, out var baseline) || baseline.Id != id) throw new FormatException(prefix + "Unknown ID/key");
        if (JsonShape.Int(d["entryIndex"]) != 0) throw new FormatException(prefix + "Only entryIndex 0 supported");
        if (baseline.Entries != null && baseline.Entries.Count != 0) throw new FormatException(prefix + "Entry already exists; populated baseline");
        // Null is ABSENCE, [] is PRESENT BUT EMPTY. They are not interchangeable.
        if (baseline.Entries == null ? d["before"] != null : d["before"] == null || JsonShape.Array(d["before"]).Count != 0)
            throw new FormatException(prefix + "Baseline null/empty mismatch");
        var after = new Entry(JsonShape.Object(d["after"]));
        if (string.IsNullOrWhiteSpace(after.Value)) throw new FormatException(prefix + "Value must be nonblank");
        // Canonical metadata comes from the game's zero-initialized Entry and the
        // corpus invariant Entry.Key == lookup key. No invented gender variants.
        if (after.Key != key || after.TranslatorKey != null || after.Feminine != null || after.Masculine != null || after.Neutral != null ||
            after.LanguageGender != 0 || after.CanBeGendered || after.NeedsGenderInfo)
            throw new FormatException(prefix + "Unsupported metadata; expected neutral Value-only entry");
        // New text has no Portuguese baseline: compare against the exact English
        // lookup key, not null/empty. Do NOT register or inherit edit exceptions.
        if (!TokenGuard.Inventory(key).SequenceEqual(TokenGuard.Inventory(after.Value), StringComparer.Ordinal))
            throw new FormatException(prefix + "Functional tokens/tags changed against source key");
        return new EntryAddition(after);
    }
}
