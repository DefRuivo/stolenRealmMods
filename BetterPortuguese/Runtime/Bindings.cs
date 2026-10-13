using System;
using System.Collections.Generic;
using System.Reflection;
using CoreEntry = BetterPortuguese.Core.Entry;

namespace BetterPortuguese.Runtime;
internal static class Bindings
{
    public static MethodInfo Exact(Type type, string name, Type result, bool isStatic, params Type[] parameters)
    {
        var flags = BindingFlags.Public | BindingFlags.NonPublic | (isStatic ? BindingFlags.Static : BindingFlags.Instance) | BindingFlags.DeclaredOnly;
        var method = type.GetMethod(name, flags, null, parameters, null);
        if (method == null || method.IsStatic != isStatic || method.ReturnType != result || method.ContainsGenericParameters) throw new MissingMethodException(type.FullName, name);
        return method;
    }
    public static MethodInfo ListTarget()
    {
        var method = Exact(typeof(OptionsManager), "GetLocalizationEntryList", typeof(List<LocalizationEntry>), true, typeof(string), typeof(LanguageChoice), typeof(bool));
        var parameters = method.GetParameters();
        var names = new[] { "original", "languageChoice", "fallbackToTranslatorKey" };
        for (int i = 0; i < names.Length; i++) if (parameters[i].Name != names[i]) throw new MissingMethodException("Localization parameter names changed");
        return method;
    }
    public static bool Equal(LocalizationEntry game, CoreEntry baseline) => game != null && game.Value == baseline.Value && game.Key == baseline.Key && game.TranslatorKey == baseline.TranslatorKey && game.Feminine == baseline.Feminine && game.Masculine == baseline.Masculine && game.Neutral == baseline.Neutral && (int)game.LanguageGender == baseline.LanguageGender && game.CanBeGendered == baseline.CanBeGendered && game.NeedsGenderInfo == baseline.NeedsGenderInfo;
    public static LocalizationEntry Clone(CoreEntry entry) => new LocalizationEntry { Value = entry.Value, Key = entry.Key, TranslatorKey = entry.TranslatorKey, Feminine = entry.Feminine, Masculine = entry.Masculine, Neutral = entry.Neutral, LanguageGender = (LanguageGender)entry.LanguageGender, CanBeGendered = entry.CanBeGendered, NeedsGenderInfo = entry.NeedsGenderInfo };
}
