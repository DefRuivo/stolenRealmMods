using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using BetterPortuguese.Core;
using BepInEx.Bootstrap;
using HarmonyLib;
using UnityEngine;

namespace BetterPortuguese.Runtime;

internal static class BetterTooltipsAdapter
{
    public const string Owner = "com.gumatos.betterportuguese.mods.bettertooltips";
    private static ModCatalog map;
    private static Func<Settings> settings;
    private static OnceLog warnings;
    private static Action<string> info;
    private static ISet<string> notes;
    private static OnceLog diagLog;
    private static bool ready, sourceAlive, displayAlive;
    [ThreadStatic] private static int localizing;
    private sealed class Frame { public string Original, Localized; }
    public static int Count => ready ? 1 : 0;

    public static void Install(ModCatalog catalog, Func<Settings> current, OnceLog limited, Action<string> log)
    {
        warnings = limited; info = log; settings = current; map = catalog;
        var h = new Harmony(Owner);
        try
        {
            if (!Chainloader.PluginInfos.TryGetValue(ModCatalog.BetterTooltipsGuid, out var plugin))
                throw new InvalidOperationException("BetterTooltips ausente; sem adaptador");
            if (plugin.Metadata.Version.ToString() != ModCatalog.BetterTooltipsVersion)
                throw new InvalidOperationException("versao BT nao homologada: " + plugin.Metadata.Version);
            if (Core.Resources.Sha256(File.ReadAllBytes(typeof(Tooltip).Assembly.Location)) != Composition.AssemblySha256)
                throw new InvalidOperationException("Assembly-CSharp divergente; adaptador recusado");
            Assembly assembly = plugin.Instance.GetType().Assembly;
            Type funnel = assembly.GetType("BetterTooltips.Patches.LocalizePatch", true);
            MethodInfo source = Bindings.Exact(funnel, "AplicarNotasDoFunil", typeof(void), true, typeof(string), typeof(string).MakeByRefType());
            if (source.GetParameters()[0].Name != "original" || source.GetParameters()[1].Name != "__result") throw new MissingMethodException("BT source arguments changed");
            var registry = funnel.GetField("_conteudosDeNota", BindingFlags.Static | BindingFlags.NonPublic);
            notes = registry?.GetValue(null) as ISet<string> ?? throw new MissingFieldException("BT note registry changed");
            MethodInfo display = Bindings.Exact(typeof(Tooltip), "ShowTooltip", typeof(void), false,
                typeof(string), typeof(string), typeof(Sprite), typeof(string), typeof(TooltipOffsetInfo), typeof(Color), typeof(Vector3?),
                typeof(bool), typeof(bool), typeof(float), typeof(ControlGlyphInfo?), typeof(string), typeof(bool));
            if (display.GetParameters()[3].Name != "description") throw new MissingMethodException("Tooltip description argument changed");
            Hook(h, source, nameof(SourcePrefix), nameof(SourcePostfix), nameof(SourceFinalizer));
            Hook(h, display, nameof(DisplayPrefix), nameof(DisplayPostfix), null);
            diagLog = new OnceLog(log, 200);
            ready = true;
            info?.Invoke("BP-MODS: 1 adaptador registrado, BetterTooltips " + ModCatalog.BetterTooltipsVersion + "; " + map.Count + " regras; origem BP -> montagem/ordem BT -> traducao final; nenhum patch novo em Update.");
        }
        catch (Exception ex)
        {
            ready = false;
            h.UnpatchSelf(); // install rollback ONLY, never lifecycle teardown
            warnings?.Write("BP-MODS desativado, base independente: " + ex.GetType().Name + ": " + ex.Message);
        }
    }
    private static void Hook(Harmony harmony, MethodInfo target, string pre, string post, string fin)
    {
        HarmonyMethod M(string name) => name == null ? null : new HarmonyMethod(typeof(BetterTooltipsAdapter).GetMethod(name, BindingFlags.Static|BindingFlags.NonPublic)) { priority=Priority.Last, after=new[]{ModCatalog.BetterTooltipsGuid} };
        harmony.Patch(target, prefix:M(pre), postfix:M(post), finalizer:M(fin));
        var p = Harmony.GetPatchInfo(target);
        if ((pre != null && p.Prefixes.Count(x=>x.owner==Owner)!=1) || (post != null && p.Postfixes.Count(x=>x.owner==Owner)!=1) || (fin != null && p.Finalizers.Count(x=>x.owner==Owner)!=1))
            throw new InvalidOperationException("Adapter ownership mismatch: " + target.Name);
    }
    // TEMPORARY DIAGNOSTIC (Diagnostico=true): logs the shrine/aura blocks that reach the
    // translation layer, once per distinct text, so a live hover says exactly what happened.
    private static void Diag(string tag, string input, string output)
    {
        if (input == null || input.IndexOf("shrine", StringComparison.OrdinalIgnoreCase) < 0 &&
            input.IndexOf("aura", StringComparison.OrdinalIgnoreCase) < 0) return;
        if (settings?.Invoke()?.Diagnostic != true) return;
        diagLog?.Write("BP-DIAG " + tag + " changed=" + (input != output)
            + " in<" + Cut(input) + "> out<" + Cut(output) + ">");
    }
    private static string Cut(string text)
    {
        string flat = text.Replace("\n", "\\n");
        return flat.Length <= 400 ? flat : flat.Substring(0, 400) + "…";
    }
    private static bool Enabled()
    {
        if (ready && localizing == 0 && ModCatalog.Enabled(settings?.Invoke(), OptionsManager.CurrentLanguage == LanguageChoice.PortugueseBrazil)) return true;
        if (localizing == 0) warnings?.Write("BP-MODS preservou BT/vanilla: adaptador/config/idioma fora do escopo ativo Corrigido+IntegracaoMods+pt-BR.");
        return false;
    }
    private static string LocalizeName(string text)
    {
        try
        {
            localizing++;
            string result = OptionsManager.Localize(text);
            // Never let a glossary note become part of an attribute/skill name.
            return result != null && result.IndexOf('\n') < 0 && result.IndexOf('<') < 0 ? result : text;
        }
        finally { localizing--; }
    }
    // __1 is deliberate: BT's argument is literally named __result although it
    // RETURNS VOID. Binding checks its exact name/type before installing this hook.
    private static void SourcePrefix(string original, ref string __1, out Frame __state)
    {
        __state = null;
        try
        {
            if (!Enabled() || original == null || __1 == null) return;
            __state = new Frame { Original=original, Localized=__1 };
            __1 = original; // BT alone evaluates its existing tables/rules, once
        }
        catch (Exception ex) { warnings?.Write("BP-MODS origem preservada: " + ex.GetType().Name); }
    }
    private static void SourcePostfix(ref string __1, Frame __state)
    {
        if (__state == null) return;
        try
        {
            __1 = ModText.Rebase(map, __state.Original, __state.Localized, __1, LocalizeName);
            if (!sourceAlive) { sourceAlive=true; info?.Invoke("BP-MODS: origem localizada preservada; montagem BT viva."); }
        }
        catch (Exception ex) { __1=__state.Localized; warnings?.Write("BP-MODS composicao recusada, origem preservada: " + ex.GetType().Name); }
    }
    private static Exception SourceFinalizer(Exception __exception, ref string __1, Frame __state)
    {
        if (__exception != null && __state != null) __1=__state.Localized;
        return __exception;
    }
    // Native ShowTooltip can append linked {STA=...} descriptions AFTER its
    // prefixes (Tooltip.cs:660). Translate those newly created BT blocks too,
    // without regrouping them or changing the native linked-status layout.
    private static void DisplayPostfix(Tooltip __instance)
    {
        string incoming = null;
        try
        {
            if (!Enabled() || __instance == null || __instance.Description == null) return;
            incoming = __instance.Description.text;
            string translated = ModText.Translate(map, incoming, notes, LocalizeName, s=>warnings?.Write("BP-MODS: " + s));
            Diag("postfix", incoming, translated);
            if (translated != incoming) __instance.Description.text = translated;
        }
        catch (Exception ex) { warnings?.Write("BP-MODS texto renderizado preservado: " + ex.GetType().Name); }
    }
    private static void DisplayPrefix(ref string description)
    {
        string incoming = description;
        try
        {
            if (!Enabled()) return;
            // The BT prefix has already regrouped ENGLISH identities. Translation
            // changes neither separators, colors nor order, only owned text content.
            description = ModText.Translate(map, incoming, notes, LocalizeName, s=>warnings?.Write("BP-MODS: " + s));
            Diag("prefix", incoming, description);
            if (!displayAlive && description != incoming) { displayAlive=true; info?.Invoke("BP-MODS: traducao final viva depois da ordem BT."); }
        }
        catch (Exception ex) { description=incoming; warnings?.Write("BP-MODS saida preservada: " + ex.GetType().Name); }
    }
}
