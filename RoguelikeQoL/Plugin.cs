using System;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using UnityEngine.UI;

namespace RoguelikeQoL
{
    /// <summary>
    /// RoguelikeQoL — mod de qualidade de vida, SEM alterações de gameplay.
    /// QoL-1: HUD de modificadores da run — painel sobreposto no canto superior esquerdo com
    /// os agregados da party (Treasure Find, Gold Find) e o modificador de experiência da
    /// batalha atual. Valores lidos das MESMAS fontes que o jogo usa:
    ///   Treasure = Σ character["DropQuantityMod"]   (GetCharacterLootDropModifier)
    ///   Gold     = Σ character["GoldMod"]           (ApplyGoldModifiers)
    ///   Exp      = CurrentBattle.expModifier
    ///
    /// Este mod agora é SÓ o HUD: a troca de fonte (QoL-2) virou o mod **BetterFont** e o
    /// display de stats "base (combinado)" (QoL-3) virou o mod **BetterStats**.
    /// </summary>
    [BepInPlugin("com.gumatos.roguelikeqol", "Roguelike QoL", "0.1.0")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log { get; private set; }

        /// <summary>
        /// HUD desabilitado por padrão (decisão de projeto, 29/09). Para ligar sem recompilar
        /// nada, edite <c>BepInEx/config/com.gumatos.roguelikeqol.cfg</c> e mude
        /// <c>AtivarHUD = false</c> para <c>true</c>.
        /// </summary>
        internal static ConfigEntry<bool> AtivarHud { get; private set; }

        /// <summary>
        /// Forma SEGURA de consultar a opcao: se o config nao pode ser lido/criado (arquivo
        /// ausente/corrompido ou chave com tipo invalido), o mod segue com o DEFAULT da opcao
        /// (HUD DESLIGADO) em vez de morrer no boot com NullReference. Mesmo padrao do RSTV
        /// (<c>Plugin.BotaoLigado</c>) e do BetterCombatText (try/catch no chamador).
        /// </summary>
        internal static bool HudLigado
        {
            get { return AtivarHud != null && AtivarHud.Value; }
        }

        private void Awake()
        {
            Log = Logger;

            try
            {
                AtivarHud = Config.Bind(
                    "Geral",
                    "AtivarHUD",
                    false,
                    "Mostra o HUD de modificadores da run no canto superior esquerdo (Treasure Find / Gold Find / Exp Mod). Padrão: false (desligado).");
            }
            catch (Exception e)
            {
                Log.LogError("Roguelike QoL: falha ao ler/criar o arquivo de config — seguindo com o padrao " +
                             "(HUD DESLIGADO): " + e.Message);
            }

            if (!HudLigado)
            {
                Logger.LogInfo("Roguelike QoL carregado — HUD DESABILITADO (AtivarHUD=false no config).");
                return;
            }

            Logger.LogInfo("Roguelike QoL carregado — HUD habilitado.");

            // NÃO criar o updater aqui! Este Awake roda durante o chainloader do BepInEx, ANTES de
            // existir cena — e a Unity DESTRÓI o GameObject na primeira carga de cena (confirmado
            // 29/09 no log: "QoL: updater DESTRUÍDO pela Unity"), então ele nunca chegava a
            // receber Update() e o HUD não aparecia. A criação é PREGUIÇOSA: acontece no primeiro
            // Localize da UI (ver LocalizeHudTrigger), quando já existe cena viva.
            // So chega aqui com o HUD LIGADO (o marcador de boot "... carregado." ja foi escrito
            // acima). Os ganchos sao aplicados um a um: um gancho ruim nao derruba os outros.
            AplicarPatches();

            Logger.LogInfo("QoL: o updater sera criado de forma PREGUICOSA no primeiro " +
                           "OptionsManager.Localize da UI (nunca no Awake: a Unity destroi GameObject " +
                           "criado durante o chainloader do BepInEx).");
        }

        /// <summary>
        /// Aplica os ganchos UM A UM, em vez de <c>PatchAll()</c>.
        ///
        /// <c>PatchAll()</c> e tudo-ou-nada: um gancho so que falhasse (tipo ou assinatura que mudou
        /// numa versao do jogo) deixaria os outros sem aplicar — e em silencio. Com o laco abaixo, o
        /// gancho que falha fica escrito no log com o nome dele e o resto continua funcionando. O
        /// resumo usa a contagem REAL, nunca um numero fixo. Mesmo modelo do
        /// RoguelikeSkillTreeVisualizer; quando tudo da certo os patches aplicados sao EXATAMENTE os
        /// mesmos de antes.
        /// </summary>
        private static void AplicarPatches()
        {
            var harmony = new Harmony("com.gumatos.roguelikeqol");
            var falhas = new List<string>();
            int ganchosTotal = 0;
            int ganchosOk = 0;
            int metodosOk = 0;

            Type[] tipos;
            try
            {
                tipos = typeof(Plugin).Assembly.GetTypes();
            }
            catch (Exception e)
            {
                Log.LogError("QoL: nao deu para listar os tipos do mod — nenhum gancho aplicado: " + e);
                return;
            }

            for (int i = 0; i < tipos.Length; i++)
            {
                Type tipo = tipos[i];
                if (!EhClasseDeGancho(tipo))
                {
                    continue;
                }

                ganchosTotal++;
                try
                {
                    PatchClassProcessor processador = harmony.CreateClassProcessor(tipo);
                    List<MethodInfo> aplicados = processador.Patch();
                    int quantos = aplicados != null ? aplicados.Count : 0;
                    metodosOk += quantos;
                    ganchosOk++;
                    Log.LogInfo("QoL: gancho aplicado — " + tipo.Name + " (" + quantos + " metodo(s) do jogo).");
                }
                catch (Exception e)
                {
                    falhas.Add(tipo.Name);
                    Log.LogError("QoL: FALHA ao aplicar o gancho " + tipo.Name + " — " + e.Message);
                }
            }

            string resumo = "QoL: patches Harmony aplicados (" + ganchosOk + "/" + ganchosTotal +
                            " ganchos, " + metodosOk + " metodos do jogo).";

            if (falhas.Count == 0)
            {
                Log.LogInfo(resumo);
                return;
            }

            Log.LogError(resumo + " GANCHOS QUE FALHARAM: " + string.Join(", ", falhas.ToArray()) +
                         ". O mod continua de pe, mas o recurso que dependia deles nao existe nesta sessao.");
        }

        /// <summary>
        /// Classe de gancho = tem <c>[HarmonyPatch]</c> no TIPO (declarado, nao herdado) — a MESMA
        /// condicao que o <c>PatchAll()</c> exigia para processar a classe.
        ///
        /// AQUI NAO SE EXIGE <c>[HarmonyPrefix]</c>/<c>[HarmonyPostfix]</c> NO METODO: os ganchos
        /// deste mod sao declarados pela CONVENCAO DE NOME do Harmony (metodo chamado <c>Postfix</c>,
        /// ver <c>LocalizeHudTrigger</c>), que o Harmony aceita exatamente como aceita o atributo —
        /// os nomes sao <c>Prefix</c>/<c>Postfix</c>/<c>Transpiler</c>/<c>Finalizer</c>. Exigir o
        /// atributo PULA os ganchos deste mod: o mod carrega, loga "carregado." e nao aplica nada —
        /// o silencio parecendo sucesso. Uma classe com <c>[HarmonyPatch]</c> e sem metodo de patch
        /// apenas nao registra nada (<c>Patch()</c> devolve lista vazia), sem efeito colateral — e o
        /// mesmo conjunto que o <c>PatchAll()</c> processaria. Mesmo filtro do BetterTooltips.
        /// </summary>
        private static bool EhClasseDeGancho(Type tipo)
        {
            try
            {
                if (tipo == null || !tipo.IsClass)
                {
                    return false;
                }

                return tipo.GetCustomAttributes(typeof(HarmonyPatch), false).Length > 0;
            }
            catch (Exception)
            {
                // atributo com tipo que nao resolve (versao de jogo diferente): nao e gancho nosso
                return false;
            }
        }
    }

    /// <summary>
    /// Gatilho do HUD. A cada localização de texto da UI: garante que o updater exista (recria
    /// se a Unity tiver destruído) e pede um refresh do HUD (com throttle interno).
    /// </summary>
    [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
    public static class LocalizeHudTrigger
    {
        private static void Postfix()
        {
            try
            {
                QoLUpdater.Ensure();
            }
            catch
            {
                // nunca quebrar a localização do jogo por causa do HUD
            }
        }
    }

    /// <summary>
    /// MonoBehaviour do HUD. Normalmente atualiza em Update() a cada 0,5s, mas como o Update
    /// deste objeto nem sempre é entregue neste jogo, o mesmo refresh também é disparado pelo
    /// gatilho de Localize — os dois caminhos usam o MESMO RefreshIfDue (idempotente).
    /// </summary>
    public class QoLUpdater : MonoBehaviour
    {
        private const float RefreshInterval = 0.5f;

        private Text _hudText;
        private float _lastUpdate = -99f;
        private bool _loggedFirstTick;
        private bool _loggedFirstLocalize;
        private bool _loggedFirstText;

        public static QoLUpdater Instance { get; private set; }

        private static bool _everDestroyed;

        /// <summary>Cria o GameObject persistente do HUD (idempotente).</summary>
        public static void Create()
        {
            if (Instance != null)
            {
                return;
            }
            var go = new GameObject("RoguelikeQoL_Updater");
            DontDestroyOnLoad(go);
            go.AddComponent<QoLUpdater>();
        }

        /// <summary>Garante que o updater exista e força um refresh (respeitando o throttle).</summary>
        public static void Ensure()
        {
            if (Instance == null)
            {
                if (_everDestroyed)
                {
                    Plugin.Log.LogWarning("QoL: updater ausente — recriando (a Unity destruiu o anterior).");
                }
                Create();
            }
            if (Instance == null)
            {
                return;
            }
            Instance.MarkLocalizeSeen();
            Instance.RefreshIfDue();
        }

        private void Awake()
        {
            Instance = this;
            Plugin.Log.LogInfo("QoL: updater criado.");
            CreateHud();
        }

        private void Start()
        {
            Plugin.Log.LogInfo("QoL: Start() do updater chamado (objeto vivo na cena).");
        }

        private void OnDestroy()
        {
            Plugin.Log.LogWarning("QoL: updater DESTRUÍDO pela Unity.");
            _everDestroyed = true;
            if (Instance == this)
            {
                Instance = null;
            }
        }

        internal void MarkLocalizeSeen()
        {
            if (_loggedFirstLocalize)
            {
                return;
            }
            _loggedFirstLocalize = true;
            Plugin.Log.LogInfo("QoL: primeiro Localize recebido (a UI do jogo está rodando).");
        }

        internal void RefreshIfDue()
        {
            if (Time.realtimeSinceStartup - _lastUpdate < RefreshInterval)
            {
                return;
            }
            _lastUpdate = Time.realtimeSinceStartup;
            Refresh();
        }

        private void Update()
        {
            if (!_loggedFirstTick)
            {
                _loggedFirstTick = true;
                Plugin.Log.LogInfo("QoL: primeiro Update do updater OK (ciclo de vida funcionando).");
            }
            RefreshIfDue();
        }

        private void Refresh()
        {
            if (_hudText == null)
            {
                return;
            }
            try
            {
                string text = BuildHudText();
                if (!_loggedFirstText && !string.IsNullOrEmpty(text))
                {
                    // Prova, pelo log, que o HUD tem conteúdo (só acontece dentro de uma run,
                    // quando a party existe) — dá pra validar sem depender de screenshot.
                    _loggedFirstText = true;
                    Plugin.Log.LogInfo($"QoL HUD texto: {text.Replace("\n", " | ")}");
                }
                _hudText.text = text;
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"QoL HUD erro: {e.Message}");
                _hudText.text = "";
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
