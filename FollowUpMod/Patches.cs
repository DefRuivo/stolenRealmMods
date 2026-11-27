using System.Collections.Generic;
using System.Reflection;
using HarmonyLib;

namespace FollowUpMod
{
    /// <summary>
    /// Adequa o nivel ANTES do toggle nativo comparar os niveis. Nao bloqueia nada: a
    /// aceitacao/recusa continua sendo a regra do jogo original (MaxLevelVariance).
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
        private static void Prefix(CharacterChoiceManager __instance) => SelectionGate.Prepare(__instance);

        [HarmonyPostfix]
        private static void Postfix()
        {
            if (NetworkingManager.Instance == null || !NetworkingManager.Instance.IsServer) return;
            HostAnnouncer.Publish();
        }
    }

    /// <summary>
    /// Bloqueia o save do personagem promovido: nivel e recompensas desta sessao nao chegam ao
    /// arquivo. Bloquear (em vez de trocar o nivel durante o save) evita a recursao causada por
    /// SaveDataThrottler -> Character.Save sincrono + setter de ExperienceLevel enfileirando save.
    /// O `force` do jogo passa, porque ele e usado no meio do proprio save internamente.
    /// </summary>
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
        private static bool Prefix(Character __instance)
        {
            return !SessionGuard.ShouldBlockSave(__instance);
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

    /// <summary>
    /// Saida de sessao: devolve o nivel original aos personagens vivos e descarta as marcas.
    /// Restaurar ANTES de esquecer e o que garante que nenhum save do encerramento grave o
    /// nivel promovido.
    /// </summary>
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
            SessionGuard.RestoreAllAndForget();
            PromotionService.Reset();
            FollowUpModPlugin.Log.LogInfo("FU: sessao encerrada; nivel original restaurado");
        }
    }
}
