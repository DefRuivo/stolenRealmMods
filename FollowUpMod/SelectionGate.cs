using System;

namespace FollowUpMod
{
    /// <summary>
    /// Decide e prepara a entrada do personagem no grupo de co-op. Roda no PREFIXO do
    /// toggle nativo: a promocao acontece ANTES de o gate original comparar os niveis,
    /// senao o proprio jogo recusaria o personagem por MaxLevelVariance.
    /// </summary>
    internal static class SelectionGate
    {
        internal static bool TryEnter(CharacterChoiceManager manager)
        {
            try
            {
                var candidate = manager != null && manager.selectedCharacterChoiceItem != null
                    ? manager.selectedCharacterChoiceItem.Character
                    : null;
                if (candidate == null || candidate.SelectedForBattle) return true;

                var snapshot = GroupAnchors.Read(candidate);
                if (snapshot.Reason == "root_missing" || snapshot.Reason == "candidate_missing")
                {
                    FollowUpModPlugin.Log.LogInfo("FU: estado do grupo ilegivel (" + snapshot.Reason + "); vanilla");
                    return true;
                }

                var ctx = Context.Read();
                if (!ctx.IsMultiplayer)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: gate inerte (not_multiplayer)");
                    return true;
                }
                if (!ctx.IsRoguelike)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: gate inerte (not_roguelike)");
                    return true;
                }
                if (!ctx.HostAnnouncesRule)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: host sem regra (" + CoopLevelPolicy.LobbyKey + "); vanilla");
                    return true;
                }

                int groupMin = CoopLevelPolicy.GroupMinimum(snapshot.OtherCharacterLevels);
                if (groupMin <= 0) groupMin = (int)candidate.Level; // sem grupo anterior: nada a adequar
                int ceiling = (int)candidate.MaxLevel;
                var decision = CoopLevelPolicy.DecideLevelDelta((int)candidate.Level, groupMin, ceiling);
                FollowUpModPlugin.Log.LogInfo("FU: gate nivel=" + candidate.Level + " grupoMin=" + groupMin
                    + " aceito=" + decision.Accepted + " delta=" + decision.LevelsToGrant
                    + (decision.CeilingLimited ? " ceiling_limited" : ""));

                if (!decision.Accepted)
                {
                    ConfirmWindow.Instance.ShowPopupMessage(
                        OptionsManager.Localize("Cannot Add To Party"),
                        "FollowUpMod: personagem acima do nivel minimo do grupo (" + groupMin + ").");
                    return false;
                }

                if (decision.LevelsToGrant > 0)
                    PromotionService.Promote(candidate, decision.TargetLevel, decision.LevelsToGrant, decision.CeilingLimited);
                return true;
            }
            catch (Exception ex)
            {
                FollowUpModPlugin.Log.LogWarning("FU: gate indisponivel, vanilla: " + ex.GetType().Name + ": " + ex.Message);
                return true;
            }
        }
    }

    internal static class Context
    {
        internal static CoopContext Read()
        {
            bool multiplayer = false, roguelike = false, announced = false;
            try
            {
                var root = NetworkingManager.Instance != null && NetworkingManager.Instance.NetworkManager != null
                    ? NetworkingManager.Instance.NetworkManager.Root
                    : null;
                multiplayer = root != null && root.PlayingMultiplayer;
                roguelike = Burst2Flame.Game.Instance != null && Burst2Flame.Game.Instance.RoguelikeModeActive;
                var lobby = SteamManager.instance != null ? SteamManager.instance.CurrentLobby : null;
                announced = lobby.HasValue && !string.IsNullOrEmpty(lobby.Value.GetData(CoopLevelPolicy.LobbyKey));
            }
            catch (Exception ex)
            {
                FollowUpModPlugin.Log.LogWarning("FU: contexto de rede ilegivel: " + ex.GetType().Name);
            }
            return new CoopContext { IsMultiplayer = multiplayer, IsRoguelike = roguelike, HostAnnouncesRule = announced };
        }
    }
}
