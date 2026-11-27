using System.Collections.Generic;
using System.Reflection;
using HarmonyLib;

namespace FollowUpMod
{
    /// <summary>
    /// Gate de entrada no grupo: promove ANTES do toggle nativo comparar os niveis, e recusa
    /// quem esta acima do minimo do grupo (comportamento do jogo original).
    /// </summary>
    [HarmonyPatch(typeof(CharacterChoiceManager))]
    internal static class SelectionGatePatch
    {
        [HarmonyTargetMethods]
        private static IEnumerable<MethodBase> Targets()
        {
            var method = AccessTools.Method(typeof(CharacterChoiceManager), "ToggleSelectedCharacter", new[] { typeof(int) });
            if (method == null) FollowUpModPlugin.Log.LogError("FU: ToggleSelectedCharacter(int) nao encontrado; gate NAO aplicado");
            else yield return method;
        }

        [HarmonyPrefix]
        [HarmonyPriority(Priority.First)]
        private static bool Prefix(CharacterChoiceManager __instance) => SelectionGate.TryEnter(__instance);

        [HarmonyPostfix]
        private static void Postfix(bool __runOriginal)
        {
            // __runOriginal=false significa que o prefixo recusou: o grupo nao mudou, nao reanuncia.
            if (!__runOriginal) return;
            if (NetworkingManager.Instance == null || !NetworkingManager.Instance.IsServer) return;
            HostAnnouncer.Publish();
        }
    }

    /// <summary>Grava o nivel original no arquivo e devolve o promovido logo depois.</summary>
    [HarmonyPatch(typeof(Character))]
    internal static class SaveGuardPatch
    {
        [HarmonyTargetMethods]
        private static IEnumerable<MethodBase> Targets()
        {
            var method = AccessTools.Method(typeof(Character), "Save", new[] { typeof(bool) });
            if (method == null) FollowUpModPlugin.Log.LogError("FU: Character.Save(bool) nao encontrado; gravacao NAO protegida");
            else yield return method;
        }

        [HarmonyPrefix]
        private static void Prefix(Character __instance, ref float __state)
        {
            __state = __instance != null ? __instance.ExperienceLevel : 0f;
            if (SessionGuard.Stash(__instance))
                FollowUpModPlugin.Log.LogInfo("FU: save com nivel original para nao persistir a promocao");
        }

        [HarmonyPostfix]
        private static void Postfix(Character __instance, float __state)
        {
            if (__state <= 0f) return;
            SessionGuard.RestorePromoted(__instance, __state);
        }
    }

    /// <summary>Sessao de rede iniciada: reanuncia o minimo do grupo vigente.</summary>
    [HarmonyPatch(typeof(Root))]
    internal static class HostAnnouncePatch
    {
        [HarmonyTargetMethods]
        private static IEnumerable<MethodBase> Targets()
        {
            var method = AccessTools.Method(typeof(Root), "set_PlayingMultiplayer", new[] { typeof(bool) });
            if (method == null) FollowUpModPlugin.Log.LogWarning("FU: Root.set_PlayingMultiplayer nao encontrado; host nao anuncia");
            else yield return method;
        }

        [HarmonyPostfix]
        private static void Postfix(bool value)
        {
            if (value) HostAnnouncer.Publish();
        }
    }

    /// <summary>Fim de sessao: descarta promocoes e recompensas desta bancada.</summary>
    [HarmonyPatch(typeof(NetworkingManager))]
    internal static class SessionEndPatch
    {
        [HarmonyTargetMethods]
        private static IEnumerable<MethodBase> Targets()
        {
            var method = AccessTools.Method(typeof(NetworkingManager), "ExecuteExitToMainMenu");
            if (method == null) FollowUpModPlugin.Log.LogWarning("FU: ExecuteExitToMainMenu nao encontrado; limpeza no fechamento");
            else yield return method;
        }

        [HarmonyPostfix]
        private static void Postfix()
        {
            PromotionService.Reset();
            SessionGuard.ForgetAll();
            FollowUpModPlugin.Log.LogInfo("FU: sessao encerrada; promocao descartada");
        }
    }
}
