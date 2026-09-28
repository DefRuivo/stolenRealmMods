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

            CreateHud();
        }

        private void Start()
        {
            StartCoroutine(FontApplier());
        }

        /// <summary>
        /// QoL-2: aplica a fonte serifada a todos os textos TMP do jogo, incluindo os que
        /// surgirem depois (novas janelas/telas). A fonte original do jogo entra como
        /// fallback do font asset serifado, para ícones/símbolos não virarem quadrados.
        /// </summary>
        private IEnumerator FontApplier()
        {
            while (true)
            {
                yield return new WaitForSeconds(2f);
                try
                {
                    if (_serifFont == null)
                    {
                        _serifFont = CreateSerifFont();
                        if (_serifFont == null)
                        {
                            Log.LogWarning("QoL fonte: nenhuma fonte serifada disponível no SO.");
                            yield return new WaitForSeconds(30f);
                            continue;
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
                    Log.LogWarning($"QoL fonte erro: {e.Message}");
                }
            }
        }

        private static TMP_FontAsset CreateSerifFont()
        {
            string[] candidates = { "Times New Roman", "Georgia", "Liberation Serif", "Cambria", "Book Antiqua" };
            foreach (var name in candidates)
            {
                try
                {
                    Font osFont = Font.CreateDynamicFontFromOSFont(name, 36);
                    if (osFont != null)
                    {
                        Log.LogInfo($"QoL fonte: usando '{name}' como fonte serifada.");
                        return TMP_FontAsset.CreateFontAsset(osFont);
                    }
                }
                catch
                {
                    // tenta a próxima candidata
                }
            }
            return null;
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
