using System.Collections;
using System.Collections.Generic;
using Burst2Flame;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace RoguelikeQoL
{
    /// <summary>
    /// RoguelikeQoL — mod de qualidade de vida, SEM alterações de gameplay.
    /// QoL-1: HUD de modificadores da run — mostra em tempo real os agregados
    /// da party (Treasure Find, Gold Find) e o modificador de experiência da
    /// batalha atual. Valores lidos das MESMAS fontes que o jogo usa:
    ///   Treasure = Σ character["DropQuantityMod"]   (GetCharacterLootDropModifier)
    ///   Gold     = Σ character["GoldMod"]           (ApplyGoldModifiers)
    ///   Exp      = CurrentBattle.expModifier
    /// </summary>
    [BepInPlugin("com.gumatos.roguelikeqol", "Roguelike QoL", "0.1.0")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log { get; private set; }

        private Text _hudText;
        private float _lastUpdate = -99f;
        private float _lastFontSweep = -99f;

        // QoL-2: fonte serifada (Times New Roman ou similar) aplicada globalmente.
        private TMP_FontAsset _serifFont;
        private readonly HashSet<TMP_Text> _seenTexts = new HashSet<TMP_Text>();

        private void Awake()
        {
            Log = Logger;
            Logger.LogInfo("Roguelike QoL carregado.");

            var harmony = new Harmony("com.gumatos.roguelikeqol");
            harmony.PatchAll();
            Logger.LogInfo("Roguelike QoL: patches aplicados.");

            // O GameObject do próprio plugin BepInEx NÃO recebe Update neste jogo —
            // criamos nosso próprio objeto persistente com um MonoBehaviour dedicado.
            var updaterGo = new GameObject("RoguelikeQoL_Updater");
            DontDestroyOnLoad(updaterGo);
            updaterGo.AddComponent<QoLUpdater>();
            Logger.LogInfo("QoL: updater próprio criado (recebe Update de forma garantida).");
        }
    }

    /// <summary>
    /// Gatilho da fonte (QoL-2): a cada localização de texto (o funil Localize roda em
    /// TODA renderização de UI), pede uma varredura de fonte com throttle. Assim a fonte
    /// aplica assim que qualquer tela renderiza — sem depender de Update/foco/timeScale.
    /// </summary>
    [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
    public static class LocalizeFontTrigger
    {
        private static void Postfix()
        {
            try
            {
                QoLUpdater.Instance?.MaybeSweep();
            }
            catch
            {
                // nunca quebrar a localização por causa da fonte
            }
        }
    }

    /// <summary>
    /// QoL-3: stats no formato "BASE (COMBINADO)". O jogo guarda os pontos investidos em
    /// atributos "XBase" (Game.Instance.LevelableCharacterAttributes) e o valor final/combinado
    /// em "X" (Game.Instance.LevelableCharacterAttributesFinal). A tela de personagem
    /// (InventoryManager) mostrava só o combinado; a de level up (RoguelikeManager) só a base.
    /// Agora ambas mostram "base (combinado)" quando diferem.
    /// </summary>
    [HarmonyPatch(typeof(InventoryManager), nameof(InventoryManager.UpdateStats))]
    public static class InventoryStatBaseCombined
    {
        private static bool _loggedDiag;

        internal static void LogDiagnostic(Character character)
        {
            if (_loggedDiag)
            {
                return;
            }
            _loggedDiag = true;
            try
            {
                var sb = new System.Text.StringBuilder();
                sb.Append("QoL-3 diag: char=").Append(character.CharacterName);
                CharacterAttribute[] baseAttrs = Game.Instance.LevelableCharacterAttributes;
                CharacterAttribute[] finalAttrs = Game.Instance.LevelableCharacterAttributesFinal;
                int n = System.Math.Min(baseAttrs.Length, finalAttrs.Length);
                for (int i = 0; i < n; i++)
                {
                    float savedVal = (character.SavedMap != null && character.SavedMap.ContainsKey(baseAttrs[i].Guid))
                        ? Mathf.Ceil(character.SavedMap[baseAttrs[i].Guid]) : -1f;
                    sb.Append("; ").Append(baseAttrs[i].name).Append(":saved=").Append(savedVal)
                      .Append(",val=").Append(Mathf.Ceil(character[baseAttrs[i].name]))
                      .Append('/').Append(finalAttrs[i].name).Append('=').Append(Mathf.Ceil(character[finalAttrs[i].name]));
                }
                sb.Append(" | AbilityPower=").Append(Mathf.Ceil(character["AbilityPower"]));
                if (character.Effects != null)
                {
                    sb.Append(" | effects: ");
                    foreach (CharacterEffect e in character.Effects)
                    {
                        if (e != null && e.CharacterAttribute != null)
                        {
                            sb.Append(e.CharacterAttribute.name).Append(':').Append(e.CharacterEffectMethod).Append(':').Append(e.Amount).Append(", ");
                        }
                    }
                }
                // Roguelike powerups (ex.: "Light's Brilliance") — nome + efeitos por nível.
                try
                {
                    var nm = NetworkingManager.Instance;
                    if (nm != null && nm.NetworkManager != null && nm.NetworkManager.Root != null)
                    {
                        var root = nm.NetworkManager.Root;
                        if (root.RoguelikePowerupsByConnection != null &&
                            root.RoguelikePowerupsByConnection.ContainsKey(character.OwnerID))
                        {
                            var set = root.RoguelikePowerupsByConnection[character.OwnerID];
                            if (set != null && set.PowerupAndLevels != null)
                            {
                                sb.Append(" | powerups: ");
                                foreach (var pal in set.PowerupAndLevels)
                                {
                                    if (pal == null || pal.Level <= 0)
                                    {
                                        continue;
                                    }
                                    RoguelikePowerup p = Game.Instance.GetFromRoguelikePowerupDict(Game.Instance.GetGuidFromString(pal.Guid));
                                    if (p == null || p.PowerupLevels == null || pal.Level - 1 >= p.PowerupLevels.Length)
                                    {
                                        continue;
                                    }
                                    sb.Append(p.Name).Append(" L").Append(pal.Level).Append(": ");
                                    var effs = p.PowerupLevels[pal.Level - 1].CharacterEffects;
                                    if (effs != null)
                                    {
                                        foreach (var ei in effs)
                                        {
                                            if (ei != null && ei.CharacterAttribute != null)
                                            {
                                                sb.Append(ei.CharacterAttribute.name).Append(':').Append(ei.CharacterEffectMethod).Append(':').Append(ei.Amount).Append(", ");
                                            }
                                        }
                                    }
                                    sb.Append("; ");
                                }
                            }
                        }
                    }
                }
                catch (System.Exception ex)
                {
                    sb.Append(" | powerups ERRO: ").Append(ex.Message);
                }
                // Skills com efeitos de atributo (ex.: "Light's Brilliance").
                try
                {
                    sb.Append(" | skillsFromPoints: ");
                    DumpSkills(sb, character.SkillsFromPoints);
                    sb.Append(" | skillsAll: ");
                    DumpSkills(sb, character.Skills);
                }
                catch (System.Exception ex)
                {
                    sb.Append(" | skills ERRO: ").Append(ex.Message);
                }
                // Status effects com efeitos de atributo.
                try
                {
                    sb.Append(" | statuses: ");
                    if (character.ActionStatuses != null)
                    {
                        foreach (var st in character.ActionStatuses)
                        {
                            if (st == null || st.ActionStatusInfo == null)
                            {
                                continue;
                            }
                            var effs2 = st.ActionStatusInfo.AttributeEffects;
                            if (effs2 == null || effs2.Length == 0)
                            {
                                continue;
                            }
                            sb.Append(st.ActionStatusInfo.name).Append(": ");
                            foreach (var ei in effs2)
                            {
                                if (ei != null && ei.CharacterAttribute != null)
                                {
                                    sb.Append(ei.CharacterAttribute.name).Append(':').Append(ei.CharacterEffectMethod).Append(':').Append(ei.Amount).Append(", ");
                                }
                            }
                            sb.Append("; ");
                        }
                    }
                }
                catch (System.Exception ex)
                {
                    sb.Append(" | statuses ERRO: ").Append(ex.Message);
                }
                // Contexto + equipamento (ItemCharacterEffects) + debug de contribuições de Inteligência.
                try
                {
                    var nm2 = NetworkingManager.Instance;
                    if (nm2 != null && nm2.NetworkManager != null && nm2.NetworkManager.Root != null)
                    {
                        sb.Append(" | PlayingRoguelike=").Append(nm2.NetworkManager.Root.PlayingRoguelike);
                    }
                }
                catch { }
                try
                {
                    sb.Append(" | equipped: ");
                    if (character.EquippedItems != null)
                    {
                        foreach (var it in character.EquippedItems)
                        {
                            if (it == null || it.ItemCharacterEffects == null)
                            {
                                continue;
                            }
                            sb.Append(it.ItemName).Append(": ");
                            foreach (var ic in it.ItemCharacterEffects)
                            {
                                if (ic != null && ic.CharacterAttribute != null)
                                {
                                    sb.Append(ic.CharacterAttribute.name).Append(':').Append(ic.Method).Append(':').Append(ic.Amount).Append(", ");
                                }
                            }
                            sb.Append("; ");
                        }
                    }
                }
                catch (System.Exception ex)
                {
                    sb.Append(" | equipped ERRO: ").Append(ex.Message);
                }
                Plugin.Log.LogInfo(sb.ToString());
                // Debug nativo do jogo: lista TODAS as contribuições (com origem) para Intelligence.
                try
                {
                    var intelAttr = Game.Instance.GetAttribute("Intelligence");
                    if (intelAttr != null)
                    {
                        character.DebugCharacterAttribute(intelAttr);
                    }
                    var intelBaseAttr = Game.Instance.GetAttribute("IntelligenceBase");
                    if (intelBaseAttr != null)
                    {
                        character.DebugCharacterAttribute(intelBaseAttr);
                    }
                }
                catch { }
            }
            catch (System.Exception ex)
            {
                Plugin.Log.LogWarning("QoL-3 diag erro: " + ex.Message);
            }
        }

        private static void DumpSkills(System.Text.StringBuilder sb, System.Collections.Generic.List<SkillInfo> skills)
        {
            if (skills == null)
            {
                sb.Append("(null)");
                return;
            }
            foreach (var sk in skills)
            {
                if (sk == null || sk.AttributeEffects == null || sk.AttributeEffects.Length == 0)
                {
                    continue;
                }
                sb.Append(sk.SkillName).Append(": ");
                foreach (var ei in sk.AttributeEffects)
                {
                    if (ei != null && ei.CharacterAttribute != null)
                    {
                        sb.Append(ei.CharacterAttribute.name).Append(':').Append(ei.CharacterEffectMethod).Append(':').Append(ei.Amount).Append(", ");
                    }
                }
                sb.Append("; ");
            }
        }

        internal static float GetBaseValue(Character character, CharacterAttribute baseAttr)
        {
            // "Base" = valor PURO do atributo (criação + pontos de level up), sem powerups/gear/skills.
            // O SavedMap guarda exatamente isso; o character[nome] já vem com TODOS os modificadores
            // (inclusive o +20% da Light's Brilliance), por isso não serve como "base".
            if (character.SavedMap != null && character.SavedMap.ContainsKey(baseAttr.Guid))
            {
                return Mathf.Ceil(character.SavedMap[baseAttr.Guid]);
            }
            return Mathf.Ceil(character[baseAttr.name]);
        }

        private static void Postfix(InventoryManager __instance, Character character)
        {
            try
            {
                if (character == null || __instance == null || __instance.AttributesValuesMainHolder == null)
                {
                    return;
                }
                CharacterAttribute[] baseAttrs = Game.Instance.LevelableCharacterAttributes;
                CharacterAttribute[] finalAttrs = Game.Instance.LevelableCharacterAttributesFinal;
                if (baseAttrs == null || finalAttrs == null)
                {
                    return;
                }
                int count = System.Math.Min(baseAttrs.Length, finalAttrs.Length);
                for (int i = 0; i < count; i++)
                {
                    if (i >= __instance.AttributesValuesMainHolder.childCount || baseAttrs[i] == null || finalAttrs[i] == null)
                    {
                        continue;
                    }
                    Transform child = __instance.AttributesValuesMainHolder.GetChild(i);
                    TextMeshProUGUI component = ((child != null) ? child.GetComponent<TextMeshProUGUI>() : null);
                    if (component == null)
                    {
                        continue;
                    }
                    float baseVal = GetBaseValue(character, baseAttrs[i]);
                    float combinedVal = Mathf.Ceil(character[finalAttrs[i].name]);
                    component.text = FormatBaseCombined(baseVal, combinedVal);
                }

                InventoryStatBaseCombined.LogDiagnostic(character);
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"QoL-3 stats (personagem) erro: {e.Message}");
            }
        }

        internal static string FormatBaseCombined(float baseVal, float combinedVal)
        {
            if (combinedVal != baseVal)
            {
                return baseVal.ToString("F0") + " (" + combinedVal.ToString("F0") + ")";
            }
            return baseVal.ToString("F0");
        }
    }

    [HarmonyPatch(typeof(RoguelikeManager), nameof(RoguelikeManager.UpdateAttributes))]
    public static class RoguelikeStatBaseCombined
    {
        private static void Postfix(RoguelikeManager __instance)
        {
            try
            {
                if (__instance == null || __instance.StatValues == null)
                {
                    return;
                }
                Character character = __instance.CurrentRoguelikeSkillSelectingCharacter;
                if (character == null)
                {
                    return;
                }
                CharacterAttribute[] baseAttrs = Game.Instance.LevelableCharacterAttributes;
                CharacterAttribute[] finalAttrs = Game.Instance.LevelableCharacterAttributesFinal;
                if (baseAttrs == null || finalAttrs == null)
                {
                    return;
                }
                int count = System.Math.Min(baseAttrs.Length, finalAttrs.Length);
                var sb = new System.Text.StringBuilder();
                for (int i = 0; i < count; i++)
                {
                    if (baseAttrs[i] == null || finalAttrs[i] == null)
                    {
                        continue;
                    }
                    float baseVal = InventoryStatBaseCombined.GetBaseValue(character, baseAttrs[i]);
                    float combinedVal = Mathf.Ceil(character[finalAttrs[i].name]);
                    sb.Append(InventoryStatBaseCombined.FormatBaseCombined(baseVal, combinedVal)).Append('\n');
                }
                __instance.StatValues.text = sb.ToString();
                InventoryStatBaseCombined.LogDiagnostic(character);
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"QoL-3 stats (level up) erro: {e.Message}");
            }
        }
    }

    /// <summary>
    /// MonoBehaviour dedicado que roda o HUD (QoL-1) e a varredura de fonte (QoL-2)
    /// em Update com TEMPO REAL — imune a timeScale=0 e ao ciclo de vida do plugin.
    /// </summary>
    public class QoLUpdater : MonoBehaviour
    {
        private Text _hudText;
        private float _lastUpdate = -99f;
        private float _lastFontSweep = -99f;
        private bool _loggedFirstTick;

        private TMP_FontAsset _serifFont;
        private readonly HashSet<TMP_Text> _seenTexts = new HashSet<TMP_Text>();

        private void Awake()
        {
            Instance = this;
            CreateHud();
            FontSweep(); // primeira passada imediata (textos já existentes no boot)
        }

        public static QoLUpdater Instance { get; private set; }

        /// <summary>
        /// Disparada por QUALQUER localização de texto (postfix do Localize) — aplica a
        /// fonte imediatamente quando a UI renderiza, sem depender de Update/foco/timeScale.
        /// Throttle de 2s de tempo real para não varrer a cada caractere.
        /// </summary>
        public void MaybeSweep()
        {
            try
            {
                if (Time.realtimeSinceStartup - _lastFontSweep >= 2f)
                {
                    _lastFontSweep = Time.realtimeSinceStartup;
                    FontSweep();
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"QoL fonte erro: {e.Message}\n{e.StackTrace}");
            }
        }

        private void CreateHud()
        {
            // Canvas próprio, sobreposto à UI do jogo — não toca na UI original.
            GameObject go = new GameObject("RoguelikeQoL_HUD");
            DontDestroyOnLoad(go);
            Canvas canvas = go.AddComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = 999;

            var panelGo = new GameObject("Panel");
            panelGo.transform.SetParent(go.transform, false);
            var text = panelGo.AddComponent<Text>();
            // Unity 2022 removeu os recursos builtin antigos: "Arial.ttf" retorna null.
            // Usamos "LegacyRuntime.ttf" e, se faltar, criamos uma fonte dinâmica do SO.
            Font font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            if (font == null)
            {
                font = Font.CreateDynamicFontFromOSFont("Arial", 18);
            }
            text.font = font;
            Plugin.Log.LogInfo($"Roguelike QoL: HUD criado (fonte={((font != null) ? font.name : "null")}).");
            text.fontSize = 18;
            text.color = new Color(1f, 0.95f, 0.6f, 0.95f);
            text.horizontalOverflow = HorizontalWrapMode.Overflow;
            text.verticalOverflow = VerticalWrapMode.Overflow;
            var outline = panelGo.AddComponent<Outline>();
            outline.effectColor = new Color(0f, 0f, 0f, 0.9f);
            outline.effectDistance = new Vector2(1.2f, -1.2f);
            var rt = panelGo.GetComponent<RectTransform>();
            rt.anchorMin = new Vector2(0f, 1f);
            rt.anchorMax = new Vector2(0f, 1f);
            rt.pivot = new Vector2(0f, 1f);
            rt.anchoredPosition = new Vector2(12f, -12f);
            _hudText = text;
            _hudText.text = "";
        }

        private void Update()
        {
            if (!_loggedFirstTick)
            {
                _loggedFirstTick = true;
                Plugin.Log.LogInfo("QoL: primeiro Update do updater OK (ciclo de vida funcionando).");
            }

            // HUD: 2x por segundo.
            if (Time.realtimeSinceStartup - _lastUpdate >= 0.5f)
            {
                _lastUpdate = Time.realtimeSinceStartup;
                try
                {
                    _hudText.text = BuildHudText();
                }
                catch (System.Exception e)
                {
                    Plugin.Log.LogWarning($"QoL HUD erro: {e.Message}");
                    _hudText.text = "";
                }
            }

            // Fonte: a cada 2s de tempo real.
            if (Time.realtimeSinceStartup - _lastFontSweep >= 2f)
            {
                _lastFontSweep = Time.realtimeSinceStartup;
                FontSweep();
            }
        }

        /// <summary>
        /// QoL-2: aplica a fonte serifada a todos os textos TMP do jogo, incluindo os que
        /// surgirem depois (novas janelas/telas). A fonte original do jogo entra como
        /// fallback do font asset serifado, para ícones/símbolos não virarem quadrados.
        /// </summary>
        private void FontSweep()
        {
            try
            {
                if (_serifFont == null)
                {
                    _serifFont = CreateSerifFont();
                    if (_serifFont == null)
                    {
                        Plugin.Log.LogWarning("QoL fonte: nenhuma fonte serifada disponível no SO.");
                        return;
                    }
                }
                foreach (var t in Resources.FindObjectsOfTypeAll<TMP_Text>())
                {
                    if (t == null)
                    {
                        continue;
                    }
                    if (!_seenTexts.Contains(t))
                    {
                        // Primeira vez que vemos este texto: registra a fonte original
                        // como fallback do serifado (uma única vez).
                        // QoL-2c: fallbackFontAssetTable vem null em font asset criado
                        // em runtime (CreateFontAsset) — inicializa antes de usar.
                        if (_serifFont.fallbackFontAssetTable == null)
                        {
                            _serifFont.fallbackFontAssetTable = new List<TMP_FontAsset>();
                        }
                        if (t.font != null && t.font != _serifFont &&
                            !_serifFont.fallbackFontAssetTable.Contains(t.font))
                        {
                            _serifFont.fallbackFontAssetTable.Add(t.font);
                        }
                        _seenTexts.Add(t);
                    }
                    if (t.font != _serifFont)
                    {
                        t.font = _serifFont;
                    }
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"QoL fonte erro: {e.Message}\n{e.StackTrace}");
            }
        }

        private static TMP_FontAsset CreateSerifFont()
        {
            // Caminhos de ARQUIVO primeiro (mais confiável que resolução por nome no Unity):
            string[] fileCandidates =
            {
                "C:/Windows/Fonts/times.ttf",                    // Times New Roman
                "C:/Windows/Fonts/georgia.ttf",                  // Georgia (serifa parecida)
                "C:/Windows/Fonts/LiberationSerif-Regular.ttf",  // Liberation Serif
            };
            foreach (var path in fileCandidates)
            {
                try
                {
                    if (!System.IO.File.Exists(path))
                    {
                        continue;
                    }
                    Font fileFont = new Font(path);
                    if (fileFont == null)
                    {
                        continue;
                    }
                    TMP_FontAsset asset = TMP_FontAsset.CreateFontAsset(fileFont);
                    if (asset != null)
                    {
                        Plugin.Log.LogInfo($"QoL fonte: usando '{path}' como fonte serifada.");
                        return asset;
                    }
                    Plugin.Log.LogWarning($"QoL fonte: '{path}' carregou mas CreateFontAsset retornou null.");
                }
                catch (System.Exception e)
                {
                    Plugin.Log.LogWarning($"QoL fonte: '{path}' falhou: {e.GetType().Name}: {e.Message}");
                }
            }

            // Último recurso: resolução por nome do SO.
            string[] nameCandidates = { "Times New Roman", "Georgia", "Liberation Serif", "Cambria" };
            foreach (var name in nameCandidates)
            {
                try
                {
                    Font osFont = Font.CreateDynamicFontFromOSFont(name, 36);
                    if (osFont == null)
                    {
                        continue;
                    }
                    TMP_FontAsset asset = TMP_FontAsset.CreateFontAsset(osFont);
                    if (asset != null)
                    {
                        Plugin.Log.LogInfo($"QoL fonte: usando '{name}' (OS) como fonte serifada.");
                        return asset;
                    }
                }
                catch (System.Exception e)
                {
                    Plugin.Log.LogWarning($"QoL fonte: '{name}' falhou: {e.GetType().Name}: {e.Message}");
                }
            }
            return null;
        }

        private static string BuildHudText()
        {
            var nm = NetworkingManager.Instance;
            if (nm == null || nm.MyPartyCharacters == null || nm.MyPartyCharacters.Count == 0)
            {
                return "";
            }

            float treasure = 0f;
            float gold = 0f;
            foreach (var c in nm.MyPartyCharacters)
            {
                if (c == null)
                {
                    continue;
                }
                treasure += c["DropQuantityMod"];
                gold += c["GoldMod"];
            }

            var lines = new System.Collections.Generic.List<string>();
            if (treasure > 0f)
            {
                lines.Add($"Treasure Find: +{treasure:0.#}%");
            }
            if (gold > 0f)
            {
                lines.Add($"Gold Find: +{gold:0.#}%");
            }

            var battle = GameLogic.instance?.CurrentBattle;
            if (battle != null && !string.IsNullOrEmpty(battle.expModifier) &&
                float.TryParse(battle.expModifier, out float expMod) && expMod > 0f)
            {
                lines.Add($"Exp Mod: +{expMod:0.#}%");
            }

            return string.Join("\n", lines);
        }
    }
}
