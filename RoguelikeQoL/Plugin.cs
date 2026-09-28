using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
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

        private void Awake()
        {
            Log = Logger;
            Logger.LogInfo("Roguelike QoL carregado.");

            var harmony = new Harmony("com.gumatos.roguelikeqol");
            harmony.PatchAll();
            Logger.LogInfo("Roguelike QoL: patches aplicados.");

            CreateHud();
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
            Log.LogInfo($"Roguelike QoL: HUD criado (fonte={((font != null) ? font.name : "null")}).");
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
            // Atualiza 2x por segundo — barato o suficiente.
            if (Time.realtimeSinceStartup - _lastUpdate < 0.5f)
            {
                return;
            }
            _lastUpdate = Time.realtimeSinceStartup;
            try
            {
                _hudText.text = BuildHudText();
            }
            catch (System.Exception e)
            {
                Log.LogWarning($"QoL HUD erro: {e.Message}");
                _hudText.text = "";
            }
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
