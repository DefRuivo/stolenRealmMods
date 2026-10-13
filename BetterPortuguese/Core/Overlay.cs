using System;
using System.Collections.Generic;
using System.Threading;

namespace BetterPortuguese.Core;

public enum Conjunto { Original, Corrigido }
internal sealed class Settings
{
    public bool Active { get; }
    public Conjunto Variant { get; }
    public bool IntegrateMods { get; }
    public bool Diagnostic { get; }
    public bool Valid { get; }
    public Settings(bool active = true, Conjunto variant = Conjunto.Corrigido, bool integrateMods = true, bool diagnostic = false, bool valid = true)
    { Active = active; Variant = variant; IntegrateMods = integrateMods; Diagnostic = diagnostic; Valid = valid && Enum.IsDefined(typeof(Conjunto), variant); }
}
internal sealed class StateQueue
{
    private Settings current = new Settings(active: false);
    private Settings pending;
    public Settings Current => Volatile.Read(ref current);
    public void Enqueue(Settings settings) => Interlocked.Exchange(ref pending, settings ?? new Settings(active: false, valid: false));
    // Caller MUST be a game main-thread hook, not the file/event callback.
    public bool ApplyPending()
    {
        var next = Interlocked.Exchange(ref pending, null);
        if (next == null) return false;
        var old = Current;
        if (old.Active == next.Active && old.Variant == next.Variant && old.IntegrateMods == next.IntegrateMods && old.Diagnostic == next.Diagnostic && old.Valid == next.Valid) return false;
        Interlocked.Exchange(ref current, next); return true;
    }
}
internal sealed class OnceLog
{
    private readonly HashSet<string> seen = new HashSet<string>(StringComparer.Ordinal);
    private readonly Action<string> log;
    private readonly int maximum;
    public OnceLog(Action<string> log, int maximum = 128) { this.log = log; this.maximum = maximum; }
    public void Write(string reason)
    {
        bool emit;
        lock (seen) { emit = seen.Count < maximum && seen.Add(reason); }
        if (emit) { try { log?.Invoke(reason); } catch { /* logging must not alter result */ } }
    }
    public int Count { get { lock (seen) return seen.Count; } }
}
internal sealed class Overlay<T>
{
    private readonly Catalog catalog;
    private readonly Func<T, Entry, bool> equal;
    private readonly Func<Entry, T> clone;
    private readonly OnceLog log;
    public Overlay(Catalog catalog, Func<T, Entry, bool> equal, Func<Entry, T> clone, OnceLog log)
    { this.catalog = catalog; this.equal = equal; this.clone = clone; this.log = log; }
    public List<T> Resolve(string key, bool requestedPortuguese, bool effectivePortuguese, Settings settings, List<T> incoming)
    {
        try
        {
            if (catalog == null || settings == null || !settings.Valid || !settings.Active || settings.Variant != Conjunto.Corrigido || !requestedPortuguese || !effectivePortuguese || key == null || !catalog.Changed.TryGetValue(key, out var corrected)) return incoming;
            var baseline = catalog.Original.Records[key].Entries;
            bool same = baseline == null ? incoming == null : incoming != null && baseline.Count == incoming.Count;
            if (same && baseline != null) for (int i = 0; i < baseline.Count; i++) if (!equal(incoming[i], baseline[i])) { same = false; break; }
            if (!same) { log?.Write("Conflito de baseline: " + corrected.Id); return incoming; }
            if (corrected.Entries == null) return incoming;
            var result = new List<T>(corrected.Entries.Count);
            foreach (var entry in corrected.Entries) result.Add(clone(entry));
            return result;
        }
        catch (Exception ex) { log?.Write("Overlay preservou retorno: " + ex.GetType().Name); return incoming; }
    }
}
