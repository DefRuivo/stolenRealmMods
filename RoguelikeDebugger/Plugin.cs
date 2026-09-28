using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace RoguelikeDebugger
{
    /// <summary>
    /// RoguelikeDebugger — mod de INVESTIGAÇÃO: apenas logs, nenhuma alteração de gameplay.
    /// Registra mecânicas internas no LogOutput.log para confirmarmos como o jogo funciona.
    /// </summary>
    [BepInPlugin("com.gumatos.roguelikedebugger", "Roguelike Debugger", "0.1.0")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log { get; private set; }

        private void Awake()
        {
            Log = Logger;
            Logger.LogInfo("Roguelike Debugger carregado.");

            var harmony = new Harmony("com.gumatos.roguelikedebugger");
            harmony.PatchAll();
            Logger.LogInfo("Roguelike Debugger: patches aplicados.");
        }
    }
}
