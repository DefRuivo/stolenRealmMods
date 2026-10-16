using System;
using RoguelikeUnlimitedLevelProgression.Patches;

namespace RoguelikeUnlimitedLevelProgression.Runtime
{
    /// <summary>Marcador anterior a qualquer guarda. Nao usa instancia Unity nem cfg Verbose.</summary>
    internal static class PatchRegistryEvidence
    {
        private static bool _seen;
        public static void FirstHook(string origin)
        {
            if (_seen) return;
            _seen = true;
            Log.Info("hook vivo (antes das guardas): " + origin + "; grupo=" + PluginState.GameplayGroupApplied);
            PatchRegistry.LogOwnership("primeiro-hook");
        }
    }
}
