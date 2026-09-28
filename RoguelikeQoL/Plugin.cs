using System.Collections;
using System.Collections.Generic;
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
                Plugin.Log.LogWarning($"QoL fonte erro: {e.Message}");
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
                Plugin.Log.LogWarning($"QoL fonte erro: {e.Message}");
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
