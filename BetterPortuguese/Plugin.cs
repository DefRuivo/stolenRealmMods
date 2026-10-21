using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using UnityEngine.SceneManagement;
using BetterPortuguese.Core;
using BetterPortuguese.Runtime;

namespace BetterPortuguese;

[BepInPlugin("com.gumatos.betterportuguese", "BetterPortuguese", "0.1.1")]
[BepInDependency(ModCatalog.BetterTooltipsGuid, BepInDependency.DependencyFlags.SoftDependency)]
public sealed class Plugin : BaseUnityPlugin
{
    public const string Guid = "com.gumatos.betterportuguese";
    private static readonly StateQueue States = new StateQueue();
    private static Overlay<LocalizationEntry> overlay;
    private static ISet<string> changedKeys = new HashSet<string>(StringComparer.Ordinal);
    private static OnceLog limited;
    private static ManualLogSource log;
    private static Action poll;
    private static bool firstLookup;
    private static bool refreshPending;
    private static float nextPoll;
    private ConfigEntry<bool> active, integrate, diagnostic;
    private ConfigEntry<Conjunto> variant;
    private string lastFile;
    private Harmony harmony;

    private void Awake()
    {
        log = Logger; limited = new OnceLog(s => log.LogWarning(s));
        try
        {
        bool createConfig = !File.Exists(Config.ConfigFilePath);
        // Preserve malformed on-disk choices for diagnosis; Bind must not overwrite them.
        Config.SaveOnConfigSet = false;
        active = Config.Bind("Geral", "Ativo", true, "Ativa somente as camadas do BetterPortuguese.");
        variant = Config.Bind("Geral", "Conjunto", Conjunto.Corrigido, "Corrigido (padrao) ou Original. Original deixa a localizacao vigente do jogo intacta.");
        integrate = Config.Bind("Geral", "IntegracaoMods", true, "Traduz os blocos do BetterTooltips homologado depois da ordem do BT; nao altera a camada base.");
        diagnostic = Config.Bind("Geral", "Diagnostico", false, "Log de estado e patches, sem log por frame/chave.");
        if (createConfig) Config.Save();
        Config.SaveOnConfigSet = true;
        Config.SettingChanged += (_, __) => QueueEntries();
        poll = PollFile; // retained managed callback; no plugin Update/fake-null dependency
        QueueEntries(); PollFile();
        }
        catch (Exception ex)
        {
            poll = null;
            States.Enqueue(new Settings(active: false, valid: false));
            log.LogError("BetterPortuguese: config indisponivel, overrides desativados: " + ex.Message);
        }
        try
        {
            var catalog = Core.Resources.Load(typeof(Plugin).Assembly);
            changedKeys = new HashSet<string>(catalog.Changed.Keys, StringComparer.Ordinal);
            overlay = new Overlay<LocalizationEntry>(catalog, Bindings.Equal, Bindings.Clone, limited);
            log.LogInfo("BetterPortuguese 0.1.1: snapshots completos; " + catalog.Original.Records.Count + " registros; " + catalog.Changed.Count + " chaves corrigidas aprovadas.");
        }
        catch (Exception ex) { overlay = null; log.LogError("BetterPortuguese: camada base desativada: " + ex.Message); }
        ModCatalog mods = null;
        try
        {
            mods = Core.Resources.LoadMods(typeof(Plugin).Assembly);
            log.LogInfo("BetterPortuguese: registry de mods = " + mods.Count + " regras aprovadas (BetterTooltips " + ModCatalog.BetterTooltipsVersion + ").");
        }
        catch (Exception ex) { log.LogWarning("BetterPortuguese: camada de mods desativada, base independente: " + ex.Message); }
        harmony = new Harmony(Guid);
        Install("consulta da lista", () => Bindings.ListTarget(), nameof(ListPostfix));
        // GUIManager.Update is a live main-thread driver even when timeScale == 0.
        // No objects are created in Awake and plugin Update is deliberately unused.
        Install("fila/config/refresh", () => Bindings.Exact(typeof(GUIManager), "Update", typeof(void), false, Type.EmptyTypes), nameof(MainThreadPostfix));
        CompositionPatches.Install(harmony, () => States.Current, limited, message => log.LogInfo(message));
        // BP-EVENTO: linhas de efeito dos eventos ("★ Reroll a skill") nao passam pelo Localize.
        EventEffectText.Install(harmony, () => States.Current != null && States.Current.Diagnostic, log);
        if (mods != null) BetterTooltipsAdapter.Install(mods, () => States.Current, limited, message => log.LogInfo(message));
        log.LogInfo("BetterPortuguese 0.1.1 carregado.");
    }
    private void Install(string label, Func<MethodInfo> target, string patch)
    {
        try
        {
            var method = target();
            harmony.Patch(method, postfix: new HarmonyMethod(typeof(Plugin).GetMethod(patch, BindingFlags.Static | BindingFlags.NonPublic)));
            var info = Harmony.GetPatchInfo(method);
            int own = 0;
            foreach (var p in info.Postfixes) if (p.owner == Guid) own++;
            if (own != 1) throw new InvalidOperationException("Expected one owned postfix, got " + own);
            log.LogInfo("BetterPortuguese: patch " + label + " registrado (owner=" + Guid + ", postfixes proprios=" + own + ").");
            foreach (var p in info.Postfixes)
                if (p.owner != Guid) limited.Write("Outro postfix no alvo " + method.Name + ": " + p.owner + "; nao ha garantia contra mudancas posteriores.");
        }
        catch (Exception ex)
        {
            log.LogError("BetterPortuguese: alvo " + label + " indisponivel: " + ex.Message);
            // Missing driver means settings cannot be safely published/refreshed.
            if (patch == nameof(MainThreadPostfix)) States.Enqueue(new Settings(active: false, valid: false));
        }
    }
    private void QueueEntries() => States.Enqueue(new Settings(active.Value, variant.Value, integrate.Value, diagnostic.Value));
    private void PollFile()
    {
        try
        {
            string text = File.ReadAllText(Config.ConfigFilePath);
            if (text == lastFile) return;
            lastFile = text;
            Settings parsed = ConfigReader.Parse(text, new Settings());
            bool saveOnSet = Config.SaveOnConfigSet;
            try { Config.SaveOnConfigSet = false; Config.Reload(); }
            finally { Config.SaveOnConfigSet = saveOnSet; }
            States.Enqueue(parsed);
        }
        catch (Exception ex)
        {
            States.Enqueue(new Settings(active: false, valid: false));
            limited.Write("Config invalida/ilegivel; overrides desativados: " + ex.GetType().Name + ": " + ex.Message);
            lastFile = null; // allow recovery when the file is fixed, including identical bytes
        }
    }
    private static void ListPostfix(string original, LanguageChoice languageChoice, bool fallbackToTranslatorKey, ref List<LocalizationEntry> __result)
    {
        var incoming = __result;
        try
        {
            if (!firstLookup) { firstLookup = true; log?.LogInfo("BetterPortuguese: gancho da lista vivo; selecao de genero/fallback permanece no jogo."); }
            __result = overlay?.Resolve(original, languageChoice == LanguageChoice.PortugueseBrazil, OptionsManager.CurrentLanguage == LanguageChoice.PortugueseBrazil, States.Current, incoming) ?? incoming;
        }
        catch (Exception ex) { __result = incoming; limited?.Write("Postfix preservou retorno: " + ex.GetType().Name); }
    }
    private static void MainThreadPostfix()
    {
        try
        {
            if (Time.realtimeSinceStartup >= nextPoll)
            { nextPoll = Time.realtimeSinceStartup + 1f; poll?.Invoke(); }
            var before = States.Current;
            if (States.ApplyPending())
            {
                refreshPending |= RefreshPlan.Needed(before, States.Current);
                var s = States.Current;
                log?.LogInfo("BetterPortuguese: estado aplicado na thread principal: " + (s.Valid && s.Active ? s.Variant.ToString() : "desativado") + ", IntegracaoMods=" + s.IntegrateMods + " (" + BetterTooltipsAdapter.Count + " adaptador(es) registrado(s)).");
            }
            if (!refreshPending || !SceneManager.GetActiveScene().IsValid() || OptionsManager.instance == null) return;
            // Invalidate BEFORE calling game UI to avoid refresh reentrancy.
            refreshPending = false;
            int refreshed = UiRefresh.Apply(changedKeys, limited);
            if (States.Current.Diagnostic) log?.LogInfo("BetterPortuguese: refresh dirigido de " + refreshed + " texto(s) aprovado(s); sem LocalizeUI global; tooltips no proximo hover.");
        }
        catch (Exception ex) { limited?.Write("Refresh/config falhou; retorno do jogo preservado: " + ex.GetType().Name); }
    }
}
