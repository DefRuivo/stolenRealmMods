using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace BetterTexts
{
    /// <summary>
    /// Plugin BetterTexts — melhora textos, tooltips e descrições do Stolen Realm.
    ///
    /// [BepInPlugin] registra o mod no BepInEx com:
    ///   - GUID:    identificador único do mod (padrão: dominio.dono.nome)
    ///   - Nome:    nome legível exibido nos logs
    ///   - Versão:  versão do mod
    /// </summary>
    [BepInPlugin("com.gumatos.bettertexts", "Better Texts", "0.1.0")]
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
            Logger.LogInfo("Better Texts carregado.");

            // Harmony cria um "patch room" identificado pelo GUID.
            // PatchAll() procura todas as classes com [HarmonyPatch] neste
            // assembly e aplica os patches nos métodos do jogo.
            var harmony = new Harmony("com.gumatos.bettertexts");
            harmony.PatchAll();
            Logger.LogInfo("Better Texts: patches aplicados.");
        }
    }
}
