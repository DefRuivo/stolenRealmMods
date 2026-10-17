using System;
using System.Collections.Generic;
using System.Reflection;
using BetterPortuguese.Core;

namespace BetterPortuguese.Runtime;

internal static class UiRefresh
{
    private static FieldInfo originals;
    // Called only by the existing main-thread driver on an effective overlay transition.
    public static int Apply(ISet<string> changed, OnceLog log)
    {
        if (OptionsManager.CurrentLanguage != LanguageChoice.PortugueseBrazil || changed.Count == 0) return 0;
        if (originals == null)
        {
            originals = typeof(OptionsManager).GetField("OriginalTextValues", BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.DeclaredOnly);
            if (originals == null || originals.FieldType != typeof(Dictionary<TextOrTMPText, string>))
            {
                originals = null;
                throw new MissingFieldException("OptionsManager.OriginalTextValues dictionary unavailable; reopen UI to refresh.");
            }
        }
        var registered = (Dictionary<TextOrTMPText, string>)originals.GetValue(null);
        if (registered == null) return 0;
        int count = 0;
        foreach (var pair in RefreshPlan.Select(registered, changed))
        {
            try
            {
                if (pair.Key == null || pair.Key.GameObject == null) continue;
                OptionsManager.LocalizeUIText(pair.Key);
                count++;
            }
            catch (Exception ex) { log?.Write("Refresh de texto aprovado preservou demais alvos: " + ex.GetType().Name); }
        }
        return count;
    }
}
