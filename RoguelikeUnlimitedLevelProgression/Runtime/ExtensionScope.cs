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
        private static bool _multiplayerLogged;

        /// <summary>Root.PlayingMultiplayer. Sem certeza devolve true (= nao ampliar).</summary>
        public static bool IsMultiplayer()
        {
            try
            {
                var nm = NetworkingManager.Instance;
                if (nm == null) return true;
                var networkManager = nm.NetworkManager;
                if (networkManager == null) return true;
                var root = networkManager.Root;
                if (root == null) return true;
                return root.PlayingMultiplayer;
            }
            catch (Exception)
            {
                // Antes da rede existir nao ha como distinguir: nao amplia.
                if (!_multiplayerLogged)
                {
                    _multiplayerLogged = true;
                    Log.WarnOnce("estado de rede indisponivel; ampliacao tratada como multiplayer (vanilla)");
                }
                return true;
            }
        }

        /// <summary>Burst2Flame.Game.Instance.RoguelikeModeActive.</summary>
        public static bool IsRoguelikeMode()
        {
            try
            {
                var game = Burst2Flame.Game.Instance;
                if (game == null) return false;
                return game.RoguelikeModeActive;
            }
            catch (Exception)
            {
                return false;
            }
        }

        public static RoguelikeSettings Settings()
        {
            try
            {
                var mgr = GlobalSettingsManager.instance;
                if (mgr == null) return null;
                return mgr.roguelikeManager;
            }
            catch (Exception)
            {
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
            if (c == null) return false;
            try
            {
                if (!PluginState.Enabled) return false;
                if (c.IsAI) return false;
                if (!c.IsRoguelikeCharacter) return false;
            }
            catch (Exception)
            {
                return false;
            }
            if (!GameState.IsRoguelikeMode()) return false;
            if (GameState.IsMultiplayer()) return false;
            return true;
        }

        /// <summary>Empilha o escopo. Devolve true se esta chamada realmente empilhou.</summary>
        public static bool Push(Character c)
        {
            if (c == null) return false;
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
            if (_depth <= 0) return null;
            var c = _owner;
            if (c == null) return null;
            return AppliesTo(c) ? c : null;
        }

        public static void ResetForTests()
        {
            _depth = 0;
            _owner = null;
        }
    }
}
