using Burst2Flame;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using TMPro;
using UnityEngine;

namespace BetterStats
{
    /// <summary>
    /// BetterStats — mostra os stats no formato "BASE (COMBINADO)": o valor PURO (pontos
    /// investidos, guardado em character.SavedMap) + o valor FINAL entre parênteses (com
    /// powerups, equipamento e skills já aplicados). Vale para a tela de personagem
    /// (InventoryManager) e a de level up (RoguelikeManager). SEM alteração de gameplay.
    ///
    /// Descoberta que guiou a implementação: no jogo, `Intelligence` é uma CÓPIA de
    /// `IntelligenceBase` (efeito codificado `Intelligence:Base:Source["IntelligenceBase"]`),
    /// então comparar os dois sempre dá igual. A diferença real vem do SavedMap (valor puro)
    /// vs o valor final — é isso que este mod exibe. Ex.: skill "Light's Brilliance" aplica
    /// `IntelligenceBase:Percentage:20`, que só aparece no valor final.
    /// </summary>
    [BepInPlugin("com.gumatos.betterstats", "Better Stats", "1.0.0")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log { get; private set; }

        private void Awake()
        {
            Log = Logger;
            Logger.LogInfo("Better Stats carregado.");

            new Harmony("com.gumatos.betterstats").PatchAll();
            Logger.LogInfo("Better Stats: patches aplicados.");
        }
    }

    /// <summary>
    /// Tela de personagem (inventário): painel "Attributes" com Might/Dexterity/Vitality/
    /// Intelligence/Reflex. Além de "base (combinado)", corrije o layout — a coluna de
    /// valores era alinhada à esquerda num x fixo e o texto vazava pra fora do painel.
    /// </summary>
    [HarmonyPatch(typeof(InventoryManager), nameof(InventoryManager.UpdateStats))]
    public static class InventoryStatPatch
    {
        private static bool _loggedBox;
        private static bool _shiftedValues;

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
                ShiftValuesColumn(__instance);
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
                    component.enableWordWrapping = false;
                    component.text = BuildInventoryValue(component, baseVal, combinedVal);
                    LogBoxOnce(component, baseVal, combinedVal);
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"Better Stats (personagem) erro: {e.Message}");
            }
        }

        /// <summary>
        /// A coluna de valores é um VerticalLayoutGroup posicionado por anchoredPosition.
        /// Como sobra vão entre os labels e os valores, desloca a coluna pra esquerda uma vez
        /// pra o "N (M)" caber dentro do painel sem vazar.
        /// </summary>
        private static void ShiftValuesColumn(InventoryManager mgr)
        {
            if (_shiftedValues)
            {
                return;
            }
            _shiftedValues = true;
            try
            {
                RectTransform holderRt = mgr.AttributesValuesMainHolder as RectTransform;
                if (holderRt == null)
                {
                    return;
                }
                Vector2 p = holderRt.anchoredPosition;
                holderRt.anchoredPosition = new Vector2(p.x - 40f, p.y);
                Plugin.Log.LogInfo($"Better Stats: coluna de valores deslocada x {p.x:0.#} -> {p.x - 40f:0.#} (holderRect={holderRt.rect})");
            }
            catch (System.Exception ex)
            {
                Plugin.Log.LogWarning("Better Stats shift erro: " + ex.Message);
            }
        }

        private static void LogBoxOnce(TextMeshProUGUI comp, float baseVal, float combinedVal)
        {
            if (_loggedBox)
            {
                return;
            }
            _loggedBox = true;
            try
            {
                float bw = comp.GetPreferredValues(baseVal.ToString("F0")).x;
                float pw = comp.GetPreferredValues("(" + combinedVal.ToString("F0") + ")").x;
                Plugin.Log.LogInfo($"Better Stats box: largura={comp.rectTransform.rect.width:0.#} fontSize={comp.fontSize:0.#} baseW={bw:0.#} parenW={pw:0.#}");
            }
            catch
            {
                // diagnóstico nunca deve quebrar a UI
            }
        }

        /// <summary>
        /// "Base" = valor PURO do atributo (criação + pontos de level up), sem powerups/gear/skills.
        /// O SavedMap guarda exatamente isso; `character[nome]` já vem com TODOS os modificadores
        /// (inclusive o +20% da skill "Light's Brilliance"), por isso não serve como base.
        /// </summary>
        internal static float GetBaseValue(Character character, CharacterAttribute baseAttr)
        {
            if (character.SavedMap != null && character.SavedMap.ContainsKey(baseAttr.Guid))
            {
                return Mathf.Ceil(character.SavedMap[baseAttr.Guid]);
            }
            return Mathf.Ceil(character[baseAttr.name]);
        }

        internal static string FormatBaseCombined(float baseVal, float combinedVal, int smallSize)
        {
            if (combinedVal == baseVal)
            {
                return baseVal.ToString("F0");
            }
            string parens = "(" + combinedVal.ToString("F0") + ")";
            if (smallSize > 0)
            {
                return baseVal.ToString("F0") + " <size=" + smallSize + ">" + parens + "</size>";
            }
            return baseVal.ToString("F0") + " " + parens;
        }

        /// <summary>
        /// Versão específica do inventário: o quadrado do valor é estreito, então mede a largura
        /// disponível e encolhe SÓ o parêntese o suficiente pra caber, sem quebrar linha.
        /// </summary>
        internal static string BuildInventoryValue(TextMeshProUGUI comp, float baseVal, float combinedVal)
        {
            string baseText = baseVal.ToString("F0");
            if (combinedVal == baseVal)
            {
                return baseText;
            }
            string parenText = "(" + combinedVal.ToString("F0") + ")";
            float origSize = comp.fontSize;
            if (origSize <= 0f)
            {
                return baseText + " " + parenText;
            }
            float boxW = comp.rectTransform.rect.width;
            float baseW = comp.GetPreferredValues(baseText).x;
            float spaceW = comp.GetPreferredValues(" ").x;
            float parenW = comp.GetPreferredValues(parenText).x;
            if (boxW <= 1f || parenW <= 0.01f)
            {
                return FormatBaseCombined(baseVal, combinedVal, Mathf.Max(6, Mathf.RoundToInt(origSize * 0.7f)));
            }
            float avail = boxW - baseW - spaceW;
            float ratio = Mathf.Clamp(avail / parenW, 0.35f, 1f);
            int parenSize = Mathf.Max(6, Mathf.RoundToInt(origSize * ratio));
            return baseText + " <size=" + parenSize + ">" + parenText + "</size>";
        }
    }

    /// <summary>
    /// Tela de level up (roguelike): StatValues é um único texto multi-linha com os 5 atributos.
    /// Aqui o formato já ficou bom com o parêntese a 70% do tamanho.
    /// </summary>
    [HarmonyPatch(typeof(RoguelikeManager), nameof(RoguelikeManager.UpdateAttributes))]
    public static class RoguelikeStatPatch
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
                int smallSize = (__instance.StatValues.fontSize > 0f) ? Mathf.Max(6, Mathf.RoundToInt(__instance.StatValues.fontSize * 0.7f)) : 0;
                var sb = new System.Text.StringBuilder();
                for (int i = 0; i < count; i++)
                {
                    if (baseAttrs[i] == null || finalAttrs[i] == null)
                    {
                        continue;
                    }
                    float baseVal = InventoryStatPatch.GetBaseValue(character, baseAttrs[i]);
                    float combinedVal = Mathf.Ceil(character[finalAttrs[i].name]);
                    sb.Append(InventoryStatPatch.FormatBaseCombined(baseVal, combinedVal, smallSize)).Append('\n');
                }
                __instance.StatValues.text = sb.ToString();
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"Better Stats (level up) erro: {e.Message}");
            }
        }
    }
}
