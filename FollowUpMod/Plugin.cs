using System;
using System.Collections.Generic;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace FollowUpMod
{
    [BepInPlugin(Guid, "FollowUpMod", Version)]
    public sealed class FollowUpModPlugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.followupmod";
        public const string Version = "0.1.0";

        internal static ManualLogSource Log = null!;
        internal static Harmony HarmonyInstance = null!;

        private void Awake()
        {
            Log = Logger;
            HarmonyInstance = new Harmony(Guid);
            int ok = 0;
            var failed = new List<string>();
            void Apply(string name, Action action)
            {
                try { action(); ok++; Log.LogInfo("FU: patch aplicado " + name); }
                catch (Exception ex) { failed.Add(name + ":" + ex.GetType().Name); Log.LogError("FU: patch falhou " + name + " " + ex.GetType().Name + ": " + ex.Message); }
            }
            Apply("SelectionGatePatch", () => HarmonyInstance.CreateClassProcessor(typeof(SelectionGatePatch)).Patch());
            Apply("SaveGuardPatch", () => HarmonyInstance.CreateClassProcessor(typeof(SaveGuardPatch)).Patch());
            Apply("HostAnnouncePatch", () => HarmonyInstance.CreateClassProcessor(typeof(HostAnnouncePatch)).Patch());
            Apply("SessionEndPatch", () => HarmonyInstance.CreateClassProcessor(typeof(SessionEndPatch)).Patch());
            Log.LogInfo("FollowUpMod " + Version + " ativo: " + ok + "/4 patches" + (failed.Count == 0 ? "" : " falhas=" + string.Join(",", failed)));
        }

        private void OnDestroy()
        {
            try { HarmonyInstance?.UnpatchSelf(); } catch { }
        }
    }
}
