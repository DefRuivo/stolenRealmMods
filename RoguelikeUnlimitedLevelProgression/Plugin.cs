using System;
using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using RoguelikeUnlimitedLevelProgression.Patches;
using RoguelikeUnlimitedLevelProgression.Runtime;

namespace RoguelikeUnlimitedLevelProgression
{
    /// <summary>
    /// Roguelike Unlimited Level Progression — remove o teto de nivel 20 do modo Roguelike em singleplayer.
    /// Um nivel por vitoria; XP estendido apos o 20 com F20/D20 lidos do proprio jogo; recompensas
    /// Skills -> Itens -> Atributos com recibo duravel quando o pool de skills esgota.
    /// v0.1: em multiplayer a progressao ampliada NAO e habilitada (branch vanilla preservado).
    /// </summary>
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    public class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "com.gumatos.roguelikeunlimitedlevelprogression";
        public const string PluginName = "Roguelike Unlimited Level Progression";
        public const string PluginVersion = "0.1.1";

        internal static Plugin Instance { get; private set; }

        private Harmony _harmony;

        private void Awake()
        {
            Instance = this;
            Log.Attach(Logger);
            Log.Info(PluginName + " " + PluginVersion + " (" + PluginGuid + ") carregado.");

            PluginState.Reset();
            BindConfiguration();

            try
            {
                LedgerService.ConfigureDefault(Paths.ConfigPath);
            }
            catch (Exception ex)
            {
                Log.Error("falha ao configurar o ledger: " + ex.GetType().Name + ": " + ex.Message);
            }

            if (!PluginState.Enabled)
            {
                Log.Warn("General.Enabled=false: nenhum patch aplicado (comportamento vanilla)");
                return;
            }

            _harmony = new Harmony(PluginGuid);
            string error;
            if (!PatchRegistry.ApplyAll(_harmony, out error))
            {
                PluginState.GameplayGroupApplied = false;
                Log.Error("mod INATIVO: " + error);
                try { _harmony.UnpatchSelf(); } catch (Exception) { }
                return;
            }

            PluginState.GameplayGroupApplied = true;
            PatchRegistry.LogOwnership("Awake");
            Log.Info("politica efetiva: MaxLevel(config)=" + (PluginState.MaxLevelConfig == 0 ? "0 (sem teto voluntario)" : PluginState.MaxLevelConfig.ToString())
                     + " RewardQueryLevel=" + PluginState.RewardQueryLevel
                     + " Verbose=" + PluginState.Verbose + " diagnostico=RLP-2 (recusas sempre visiveis)");
            Log.Warn("v0.1 singleplayer: em PlayingMultiplayer a progressao ampliada permanece desligada e "
                     + "saves/ledgers estendidos NAO sao suportados em sessao multiplayer");
        }

        private void BindConfiguration()
        {
            ConfigEntry<bool> enabled = Config.Bind("General", "Enabled", true,
                "Liga a progressao ampliada do modo Roguelike. Desligado = comportamento vanilla integral.");
            ConfigEntry<int> maxLevel = Config.Bind("Progression", "MaxLevel", 0,
                "Teto voluntario de nivel. 0 = sem teto de gameplay configurado. Valores positivos precisam ser >= 21. "
                + "Reduzir NAO rebaixa personagens ja salvos.");
            ConfigEntry<int> queryLevel = Config.Bind("Rewards", "RewardQueryLevel", 20,
                "Nivel de consulta (1..30) das chances de skill e do pool de equipamento nos level-ups acima de 20. "
                + "Mantem o patamar configurado em vez de extrapolar as curvas.");
            ConfigEntry<bool> verbose = Config.Bind("Diagnostics", "Verbose", false,
                "Log detalhado de carga, alvos e primeira chamada da politica. Sem spam por frame.");

            PluginState.Enabled = enabled.Value;

            int configuredMax = maxLevel.Value;
            if (configuredMax != 0 && configuredMax < 21)
            {
                Log.Warn("Progression.MaxLevel=" + configuredMax + " invalido (use 0 ou >= 21); adotando 0 (sem teto voluntario)");
                configuredMax = 0;
            }
            PluginState.MaxLevelConfig = configuredMax;

            int query = queryLevel.Value;
            if (query < 1) query = 1;
            if (query > 30) query = 30;
            if (query != queryLevel.Value)
            {
                Log.Warn("Rewards.RewardQueryLevel=" + queryLevel.Value + " fora de 1..30; adotando " + query);
            }
            PluginState.RewardQueryLevel = query;
            PluginState.Verbose = verbose.Value;
        }

        private void OnDestroy()
        {
            // O host do chainloader e destruido na primeira cena neste jogo. Os hooks e o
            // estado estatico pertencem a SESSAO, nao ao GameObject do BaseUnityPlugin.
            // Nao fazer UnpatchSelf nem desligar GameplayGroupApplied aqui (RLP-2).
            // Rollback de instalacao continua explicito em Awake/PatchRegistry.
            Log.Info("ciclo de vida: OnDestroy do host; patches de sessao PRESERVADOS; grupo="
                     + PluginState.GameplayGroupApplied);
            PatchRegistry.LogOwnership("OnDestroy");
        }
    }
}
