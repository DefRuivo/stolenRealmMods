// EXPLICITLY SYNTHETIC API objects: never used to compile the real plugin.
// Actual game/plugin signatures and embedded bytes are checked separately via Cecil.
using System.Collections.Generic;
public enum LanguageChoice { Default, English, PortugueseBrazil }
public enum LanguageGender { None, Male, Female, Neutral, PluralMale, PluralFemale, PluralNeutral }
public class LocalizationEntry
{
    public string Value, Key, TranslatorKey, Feminine, Masculine, Neutral;
    public LanguageGender LanguageGender;
    public bool CanBeGendered, NeedsGenderInfo;
}
public static class OptionsManager
{
    public static LanguageChoice CurrentLanguage = LanguageChoice.PortugueseBrazil;
    public static List<LocalizationEntry> GetLocalizationEntryList(string original, LanguageChoice languageChoice, bool fallbackToTranslatorKey = false) => null;
}
