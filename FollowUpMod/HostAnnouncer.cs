using System;

namespace FollowUpMod
{
    /// <summary>
    /// Publica no lobby Steam o minimo de nivel do grupo aceito. Serve de marcador
    /// ("host tem o mod") e de numero para diagnostico. Nunca lanca para fora.
    /// </summary>
    internal static class HostAnnouncer
    {
        internal static void Publish()
        {
            try
            {
                if (SteamManager.instance == null || !SteamManager.instance.CurrentLobby.HasValue)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: sem lobby Steam; nada a anunciar");
                    return;
                }
                var root = NetworkingManager.Instance != null && NetworkingManager.Instance.NetworkManager != null
                    ? NetworkingManager.Instance.NetworkManager.Root
                    : null;
                if (root == null || !root.PlayingMultiplayer || !NetworkingManager.Instance.IsServer) return;

                int[] levels = CollectedLevels(root, out int ownLevel);
                int min = levels.Length == 0 ? ownLevel : CoopLevelPolicy.GroupMinimum(levels);
                if (min <= 0) min = ownLevel;
                bool ok = SteamManager.instance.CurrentLobby.Value.SetData(CoopLevelPolicy.LobbyKey, min.ToString());
                FollowUpModPlugin.Log.LogInfo("FU: lobby anunciado min=" + min + " ok=" + ok + " membros=" + levels.Length);
            }
            catch (Exception ex)
            {
                FollowUpModPlugin.Log.LogWarning("FU: anuncio falhou: " + ex.GetType().Name + ": " + ex.Message);
            }
        }

        internal static int[] CollectedLevels(Root root, out int ownLevel)
        {
            var list = root.PartyCharactersUnaccepted;
            ownLevel = 0;
            if (list == null) return new int[0];
            var levels = new int[list.Count];
            for (int i = 0; i < list.Count; i++)
            {
                levels[i] = (int)list[i].Level;
                if (list[i].Owned) ownLevel = levels[i];
            }
            return levels;
        }
    }
}
