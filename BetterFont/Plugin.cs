using System.Collections.Generic;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using TMPro;
using UnityEngine;

namespace BetterFont
{
    /// <summary>
    /// BetterFont — troca a fonte padrão do jogo por uma serifada (Times New Roman, com
    /// fallback Georgia / Liberation Serif), aplicada a TODOS os textos TMP, inclusive telas
    /// que abrem depois. A fonte original do jogo entra como fallback do asset serifado, então
    /// ícones/símbolos que a Times não tem continuam renderizando (sem quadradinhos).
    /// SEM alteração de gameplay.
    /// </summary>
    [BepInPlugin("com.gumatos.betterfont", "Better Font", "1.0.0")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log { get; private set; }

        private void Awake()
        {
            Log = Logger;
            Logger.LogInfo("Better Font carregado.");

            // NÃO criar o updater aqui! Este Awake roda durante o chainloader do BepInEx, ANTES
            // de existir cena — a Unity DESTRÓI na primeira carga de cena qualquer GameObject
            // criado ali (mesma causa raiz do HUD do RoguelikeQoL, confirmada 29/09), e o updater
            // nunca chegava a receber Update. A criação é PREGUIÇOSA: no primeiro Localize da UI.
            new Harmony("com.gumatos.betterfont").PatchAll();
            Logger.LogInfo("Better Font: patch de gatilho (OptionsManager.Localize) aplicado; updater será criado na primeira UI.");
        }
    }

    /// <summary>
    /// Gatilho da fonte: a cada localização de texto (o funil Localize roda em TODA renderização
    /// de UI), garante que o updater exista e pede uma varredura de fonte com throttle. Assim a
    /// fonte aplica assim que qualquer tela renderiza — sem depender de Update/foco/timeScale.
    /// </summary>
    [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
    public static class LocalizeFontTrigger
    {
        private static void Postfix()
        {
            try
            {
                FontUpdater.Ensure();
            }
            catch
            {
                // nunca quebrar a localização por causa da fonte
            }
        }
    }

    /// <summary>
    /// MonoBehaviour dedicado: roda a varredura de fonte com TEMPO REAL — imune a timeScale=0 e
    /// ao ciclo de vida do plugin. É criado já com a cena viva (ver LocalizeFontTrigger), senão
    /// a Unity o destruiria na primeira carga de cena e o Update nunca rodaria.
    /// </summary>
    public class FontUpdater : MonoBehaviour
    {
        public static FontUpdater Instance { get; private set; }

        private static bool _everDestroyed;

        private float _lastSweep = -99f;
        private TMP_FontAsset _serifFont;
        private readonly HashSet<TMP_Text> _seenTexts = new HashSet<TMP_Text>();
        private bool _loggedFirstSweep;

        /// <summary>Cria o GameObject persistente do updater (idempotente).</summary>
        public static void Create()
        {
            if (Instance != null)
            {
                return;
            }
            var go = new GameObject("BetterFont_Updater");
            DontDestroyOnLoad(go);
            go.AddComponent<FontUpdater>();
        }

        /// <summary>Garante que o updater exista e pede uma varredura (respeitando o throttle).</summary>
        public static void Ensure()
        {
            if (Instance == null)
            {
                if (_everDestroyed)
                {
                    Plugin.Log.LogWarning("Better Font: updater ausente — recriando (a Unity destruiu o anterior).");
                }
                Create();
            }
            Instance?.MaybeSweep();
        }

        private void Awake()
        {
            Instance = this;
            Plugin.Log.LogInfo("Better Font: updater criado.");
            FontSweep(); // primeira passada imediata
        }

        private void Start()
        {
            Plugin.Log.LogInfo("Better Font: Start() do updater chamado (objeto vivo na cena).");
        }

        private void OnDestroy()
        {
            Plugin.Log.LogWarning("Better Font: updater DESTRUÍDO pela Unity.");
            _everDestroyed = true;
            if (Instance == this)
            {
                Instance = null;
            }
        }

        public void MaybeSweep()
        {
            try
            {
                if (Time.realtimeSinceStartup - _lastSweep >= 2f)
                {
                    _lastSweep = Time.realtimeSinceStartup;
                    FontSweep();
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"Better Font erro: {e.Message}\n{e.StackTrace}");
            }
        }

        private void Update()
        {
            if (Time.realtimeSinceStartup - _lastSweep >= 2f)
            {
                _lastSweep = Time.realtimeSinceStartup;
                FontSweep();
            }
        }

        /// <summary>
        /// Aplica a fonte serifada a todos os textos TMP do jogo, incluindo os que surgirem
        /// depois (novas janelas/telas). A fonte original do jogo entra como fallback do asset
        /// serifado, para ícones/símbolos não virarem quadrados.
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
                        Plugin.Log.LogWarning("Better Font: nenhuma fonte serifada disponível no SO.");
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
                        // fallbackFontAssetTable vem null num font asset criado em runtime
                        // (CreateFontAsset) — inicializa antes de usar.
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
                if (!_loggedFirstSweep)
                {
                    _loggedFirstSweep = true;
                    Plugin.Log.LogInfo($"Better Font: varredura aplicada ({_seenTexts.Count} textos vistos).");
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"Better Font erro: {e.Message}\n{e.StackTrace}");
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
                        Plugin.Log.LogInfo($"Better Font: usando '{path}' como fonte serifada.");
                        return asset;
                    }
                    Plugin.Log.LogWarning($"Better Font: '{path}' carregou mas CreateFontAsset retornou null.");
                }
                catch (System.Exception e)
                {
                    Plugin.Log.LogWarning($"Better Font: '{path}' falhou: {e.GetType().Name}: {e.Message}");
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
                        Plugin.Log.LogInfo($"Better Font: usando '{name}' (OS) como fonte serifada.");
                        return asset;
                    }
                }
                catch (System.Exception e)
                {
                    Plugin.Log.LogWarning($"Better Font: '{name}' falhou: {e.GetType().Name}: {e.Message}");
                }
            }
            return null;
        }
    }
}
