using System;
using HarmonyLib;

namespace RoguelikeUnlimitedLevelProgression.Runtime
{
    /// <summary>
    /// Estado de sessao lido do jogo. Falha de leitura NAO amplia escopo (fail-closed):
    /// sem certeza de modo/rede, o mod se comporta como vanilla.
    /// </summary>
    internal static class GameState
    {
        private static bool UnknownNetwork(string reason)
        {
            Log.Refuse("rede", reason + "; multiplayer efetivo=True (fail-closed)");
            return true;
        }

        /// <summary>Root.PlayingMultiplayer. Sem certeza devolve true (= nao ampliar).</summary>
        public static bool IsMultiplayer()
        {
            try
            {
                var nm = NetworkingManager.Instance;
                if (nm == null) return UnknownNetwork("NetworkingManager.Instance=null");
                var networkManager = nm.NetworkManager;
                if (networkManager == null) return UnknownNetwork("NetworkManager=null");
                var root = networkManager.Root;
                if (root == null) return UnknownNetwork("Root=null");
                bool multiplayer = root.PlayingMultiplayer;
                Log.InfoOnce("estado de rede: Root.PlayingMultiplayer=" + multiplayer);
                if (multiplayer) Log.Refuse("rede", "Root.PlayingMultiplayer=True");
                return multiplayer;
            }
            catch (Exception ex)
            {
                return UnknownNetwork("leitura indisponivel: " + ex.GetType().Name + ": " + ex.Message);
            }
        }

        /// <summary>Burst2Flame.Game.Instance.RoguelikeModeActive.</summary>
        public static bool IsRoguelikeMode()
        {
            try
            {
                var game = Burst2Flame.Game.Instance;
                if (game == null) return Log.Refuse("modo", "Game.Instance=null");
                bool active = game.RoguelikeModeActive;
                Log.InfoOnce("estado de modo: Game.RoguelikeModeActive=" + active);
                if (!active) Log.Refuse("modo", "Game.RoguelikeModeActive=False");
                return active;
            }
            catch (Exception ex)
            {
                return Log.Refuse("modo", "leitura indisponivel: " + ex.GetType().Name + ": " + ex.Message);
            }
        }

        public static RoguelikeSettings Settings()
        {
            try
            {
                var mgr = GlobalSettingsManager.instance;
                if (mgr == null)
                {
                    Log.Refuse("settings", "GlobalSettingsManager.instance=null; usando fallback vanilla");
                    return null;
                }
                var settings = mgr.roguelikeManager;
                if (settings == null) Log.Refuse("settings", "roguelikeManager=null; usando fallback vanilla");
                return settings;
            }
            catch (Exception ex)
            {
                Log.Refuse("settings", "leitura indisponivel: " + ex.GetType().Name + ": " + ex.Message);
                return null;
            }
        }
    }

    /// <summary>Log curto com deduplicacao, sem depender de instancia MonoBehaviour.</summary>
    internal static class Log
    {
        private static readonly System.Collections.Generic.HashSet<string> _seen = new System.Collections.Generic.HashSet<string>();
        private static BepInEx.Logging.ManualLogSource _source;

        public static void Attach(BepInEx.Logging.ManualLogSource source) { _source = source; }

        public static void Info(string msg)
        {
            if (_source != null) _source.LogInfo(msg);
        }

        public static void Warn(string msg)
        {
            if (_source != null) _source.LogWarning(msg);
        }

        public static void Error(string msg)
        {
            if (_source != null) _source.LogError(msg);
        }

        public static void WarnOnce(string msg)
        {
            if (_seen.Add("W:" + msg)) Warn(msg);
        }

        // Recusas sao sempre visiveis, mesmo com Diagnostics.Verbose=false. Getters quentes
        // deduplicam por origem+motivo; decisoes de batalha podem pedir uma linha por chamada.
        public static bool Refuse(string origin, string reason, bool once = true)
        {
            PluginState.LastDenial = origin + ": " + reason;
            string message = "ampliacao recusada [" + origin + "]: " + reason;
            if (once) WarnOnce(message); else Warn(message);
            return false;
        }

        public static bool Vanilla(string origin, string reason)
        {
            Refuse(origin, reason);
            return true; // Prefix Harmony: executar o corpo vanilla.
        }

        internal static void ResetSeenForTests() { _seen.Clear(); }

        public static void InfoOnce(string msg)
        {
            if (_seen.Add("I:" + msg)) Info(msg);
        }
    }

    /// <summary>
    /// Escopo sincrono por personagem (parte05/C). Os 5 conversores estaticos de XP nao sabem
    /// o dono; a extensao so vale enquanto um leitor explicito de personagem Roguelike estiver
    /// no escopo. Prefix empilha, Finalizer desempilha inclusive em excecao/nesting.
    /// </summary>
    internal static class ExtensionScope
    {
        [ThreadStatic] private static int _depth;
        [ThreadStatic] private static Character _owner;

        public static bool Active { get { return _depth > 0; } }
        public static Character Owner { get { return _owner; } }
        public static int Depth { get { return _depth; } }

        /// <summary>Amplia para este personagem? (singleplayer, roguelike, nao-IA, mod ligado)</summary>
        public static bool AppliesTo(Character c)
        {
            if (c == null) return Log.Refuse("escopo", "character=null");
            try
            {
                if (!PluginState.Enabled) return Log.Refuse("escopo", "General.Enabled=False");
                if (c.IsAI) return Log.Refuse("escopo", "IsAI=True");
                if (!c.IsRoguelikeCharacter) return Log.Refuse("escopo", "IsRoguelikeCharacter=False");
            }
            catch (Exception ex)
            {
                return Log.Refuse("escopo", "leitura do personagem falhou: " + ex.GetType().Name + ": " + ex.Message);
            }
            if (!GameState.IsRoguelikeMode()) return Log.Refuse("escopo", "modo roguelike=False");
            if (GameState.IsMultiplayer()) return Log.Refuse("escopo", "multiplayer efetivo=True");
            return true;
        }

        /// <summary>Empilha o escopo. Devolve true se esta chamada realmente empilhou.</summary>
        public static bool Push(Character c)
        {
            if (c == null) return Log.Refuse("escopo.Push", "character=null");
            if (_depth == 0) _owner = c;
            _depth++;
            return true;
        }

        public static void Pop()
        {
            if (_depth > 0)
            {
                _depth--;
                if (_depth == 0) _owner = null;
            }
        }

        /// <summary>Personagem do escopo atual, se ele ainda for elegivel.</summary>
        public static Character CurrentExtended()
        {
            if (_depth <= 0) { Log.Refuse("escopo.CurrentExtended", "escopo inativo"); return null; }
            var c = _owner;
            if (c == null) { Log.Refuse("escopo.CurrentExtended", "owner=null"); return null; }
            return AppliesTo(c) ? c : null;
        }

        public static void ResetForTests()
        {
            _depth = 0;
            _owner = null;
        }
    }
}
