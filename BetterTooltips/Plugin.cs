using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace BetterTooltips
{
    /// <summary>
    /// Plugin BetterTooltips — melhora textos, tooltips e descrições do Stolen Realm.
    ///
    /// [BepInPlugin] registra o mod no BepInEx com:
    ///   - GUID:    identificador único do mod (padrão: dominio.dono.nome)
    ///   - Nome:    nome legível exibido nos logs
    ///   - Versão:  versão do mod
    /// </summary>
    [BepInPlugin("com.gumatos.bettertooltips", "Better Tooltips", "0.1.1")]
    public class Plugin : BaseUnityPlugin
    {
        /// <summary>
        /// Logger estático para as classes de patch poderem logar.
        /// </summary>
        internal static ManualLogSource Log { get; private set; }

        /// <summary>
        /// Awake() é chamado pelo BepInEx quando o plugin é carregado,
        /// logo no início do jogo (antes da primeira cena carregar).
        /// </summary>
        private void Awake()
        {
            Log = Logger;
            Logger.LogInfo("Better Tooltips carregado.");

            // Harmony cria um "patch room" identificado pelo GUID.
            // PatchAll() procura todas as classes com [HarmonyPatch] neste
            // assembly e aplica os patches nos métodos do jogo.
            var harmony = new Harmony("com.gumatos.bettertooltips");
            harmony.PatchAll();
            Logger.LogInfo("Better Tooltips: patches aplicados.");
        }
    }
}
