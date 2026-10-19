using System;
using System.IO;
using System.Linq;
using System.Reflection;
using BetterPortuguese.Core;
using HarmonyLib;
using UnityEngine;

namespace BetterPortuguese.Runtime;

internal static class CompositionPatches
{
    [ThreadStatic] private static int itemDepth;
    private sealed class ScopeFrame { public int Previous; }
    private static bool itemReady, damageReady, itemAlive, damageAlive;
    private static Func<Settings> settings;
    private static OnceLog warnings;
    private static Action<string> info;

    public static void Install(Harmony harmony, Func<Settings> current, OnceLog limited, Action<string> log)
    {
        settings = current; warnings = limited; info = log;
        try
        {
            // Deliberately strict: even a compatible game update requires re-inspection.
            // No edits to the assembly; this is a read-only guard for the new group only.
            string actual = Core.Resources.Sha256(File.ReadAllBytes(typeof(Tooltip).Assembly.Location));
            if (actual != Composition.AssemblySha256)
                throw new InvalidOperationException("Assembly-CSharp SHA-256 divergente: " + actual);
        }
        catch (Exception ex) { warnings?.Write("BP-COMP recusado: " + ex.Message); return; }
        try
        {
            MethodInfo display = Bindings.Exact(typeof(Tooltip), "ShowTooltip", typeof(void), false,
                typeof(string), typeof(string), typeof(Sprite), typeof(string), typeof(TooltipOffsetInfo),
                typeof(Color), typeof(Vector3?), typeof(bool), typeof(bool), typeof(float), typeof(ControlGlyphInfo?), typeof(string), typeof(bool));
            RequireArgument(display, "subtitle", typeof(string));
            var sources = new[] {
                Bindings.Exact(typeof(Tooltip), "ShowItemTooltip", typeof(void), false,
                    typeof(Item), typeof(Transform), typeof(TooltipOffsetInfo), typeof(Character), typeof(bool), typeof(bool), typeof(ControlGlyphInfo?), typeof(string), typeof(Item)),
                Bindings.Exact(typeof(Tooltip), "ShowItemTooltip", typeof(void), false, typeof(ItemInfo), typeof(TooltipOffsetInfo)),
                Bindings.Exact(typeof(Tooltip), "ShowTransmogTooltip", typeof(void), false, typeof(ItemInfo), typeof(TooltipOffsetInfo), typeof(ControlGlyphInfo?), typeof(string))
            };
            Patch(harmony, display, nameof(SubtitlePrefix), null, null);
            foreach (var source in sources) Patch(harmony, source, nameof(EnterItem), null, nameof(LeaveItem));
            itemReady = true;
            info?.Invoke("BP-COMP: composicao de raridade registrada (3 origens + ShowTooltip; inclui comparacao; sem transpiler).");
        }
        catch (Exception ex) { itemReady = false; warnings?.Write("BP-COMP raridade recusada: " + ex.Message); }
        try
        {
            var damage = Bindings.Exact(typeof(Tooltip), "GetDamageTypeLabel", typeof(string), true, typeof(DamageType));
            RequireArgument(damage, "damageType", typeof(DamageType));
            Patch(harmony, damage, null, nameof(DamagePostfix), null);
            damageReady = true;
            info?.Invoke("BP-COMP: rotulo Healing registrado em Tooltip.GetDamageTypeLabel.");
        }
        catch (Exception ex) { damageReady = false; warnings?.Write("BP-COMP Healing recusado: " + ex.Message); }
    }

    // Harmony binds these arguments by NAME, not by their slot. Validate before
    // registering any hook in the group; a missing/renamed/retyped target fails closed.
    private static void RequireArgument(MethodInfo method, string name, Type type)
    {
        if (method == null || method.GetParameters().Count(p => p.Name == name && p.ParameterType == type) != 1)
            throw new MissingMethodException("BP-COMP argumento ausente ou alterado: " + name);
    }

    private static void Patch(Harmony harmony, MethodInfo target, string prefix, string postfix, string finalizer)
    {
        HarmonyMethod Hook(string name) => name == null ? null : new HarmonyMethod(typeof(CompositionPatches).GetMethod(name, BindingFlags.Static | BindingFlags.NonPublic)) { priority = Priority.Last };
        harmony.Patch(target, prefix: Hook(prefix), postfix: Hook(postfix), finalizer: Hook(finalizer));
        var patches = Harmony.GetPatchInfo(target);
        if ((prefix != null && patches.Prefixes.Count(p => p.owner == Plugin.Guid) != 1) ||
            (postfix != null && patches.Postfixes.Count(p => p.owner == Plugin.Guid) != 1) ||
            (finalizer != null && patches.Finalizers.Count(p => p.owner == Plugin.Guid) != 1))
            throw new InvalidOperationException("ownership inesperado: " + target.Name);
        foreach (string owner in patches.Owners.Where(o => o != Plugin.Guid))
            warnings?.Write("BP-COMP outro owner em " + target.Name + ": " + owner + "; saida exata sera conferida.");
    }
    private static bool Enabled()
    {
        if (Composition.Enabled(settings?.Invoke(), OptionsManager.CurrentLanguage == LanguageChoice.PortugueseBrazil, out string reason)) return true;
        warnings?.Write("BP-COMP preservou vanilla: " + reason);
        return false;
    }
    private static void EnterItem(out ScopeFrame __state)
    {
        __state = null;
        if (!itemReady) return;
        __state = new ScopeFrame { Previous = itemDepth };
        itemDepth++;
    }
    // Restores nested context on success, exceptions AND skipped originals. Never swallows
    // the game's exception, and never unpatches on destruction of the BepInEx host.
    private static Exception LeaveItem(Exception __exception, ScopeFrame __state)
    {
        if (__state != null) itemDepth = __state.Previous;
        return __exception;
    }
    private static void SubtitlePrefix(ref string subtitle)
    {
        string incoming = subtitle;
        try
        {
            if (!itemReady || itemDepth == 0 || !Enabled()) return;
            if (!itemAlive) { itemAlive = true; info?.Invoke("BP-COMP: gancho de subtitulo vivo em contexto nativo de item."); }
            string corrected = Composition.ItemSubtitle(incoming, out string reason);
            if (reason != null) warnings?.Write("BP-COMP subtitulo preservado: " + reason);
            subtitle = corrected;
            if (incoming != corrected) infoOnce("raridade corrigida");
        }
        catch (Exception ex) { subtitle = incoming; warnings?.Write("BP-COMP subtitulo preservado por excecao: " + ex.GetType().Name); }
    }
    private static void DamagePostfix(DamageType damageType, ref string __result)
    {
        string incoming = __result;
        try
        {
            if (!damageReady || !Enabled()) return;
            if (!damageAlive) { damageAlive = true; info?.Invoke("BP-COMP: gancho de tipo de dano vivo."); }
            string corrected = Composition.DamageLabel(damageType == DamageType.Healing, incoming, out string reason);
            if (reason != null) warnings?.Write("BP-COMP rotulo preservado: " + reason);
            __result = corrected;
            if (incoming != corrected) infoOnce("Healing corrigido: Cura de Dano -> Cura por Dano");
        }
        catch (Exception ex) { __result = incoming; warnings?.Write("BP-COMP rotulo preservado por excecao: " + ex.GetType().Name); }
    }
    private static readonly System.Collections.Generic.HashSet<string> applied = new System.Collections.Generic.HashSet<string>(StringComparer.Ordinal);
    private static void infoOnce(string text) { if (applied.Add(text)) info?.Invoke("BP-COMP: " + text + "."); }
}
