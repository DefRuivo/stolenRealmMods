using System;
using System.Collections.Generic;
using System.Linq;

namespace BetterPortuguese.Core;

// Only the effective base overlay changes visible text in 0.1.0 (mod/manual registry empty).
internal static class RefreshPlan
{
    private static bool Effective(Settings s) => s != null && s.Valid && s.Active && s.Variant == Conjunto.Corrigido;
    public static bool Needed(Settings before, Settings after) => Effective(before) != Effective(after);

    // Snapshot before touching Unity: native calls/other postfixes may mutate the registry.
    // Match the original key, not current translated text, so rollback selects the same objects.
    public static KeyValuePair<T, string>[] Select<T>(IEnumerable<KeyValuePair<T, string>> registered, ISet<string> changed)
        => registered.Where(p => p.Value != null && changed.Contains(p.Value)).ToArray();
}
