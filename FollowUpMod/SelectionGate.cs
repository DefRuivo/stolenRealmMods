using System;

namespace FollowUpMod
{
    /// <summary>
    /// Prepara a entrada do personagem no grupo de co-op. Roda no PREFIXO do toggle nativo:
    /// promove ANTES de o jogo comparar os niveis (promover depois seria tarde), e nao decide
    /// aceitacao - quem aceita ou recusa continua sendo o jogo, com a regra original.
    /// </summary>
    internal static class SelectionGate
    {
        internal static void Prepare(CharacterChoiceManager manager)
        {
            try
            {
                var candidate = manager != null && manager.selectedCharacterChoiceItem != null
                    ? manager.selectedCharacterChoiceItem.Character
                    : null;
                if (candidate == null || candidate.SelectedForBattle) return;

                var ctx = Context.Read();
                if (!ctx.IsMultiplayer) { FollowUpModPlugin.Log.LogInfo("FU: inerte (not_multiplayer)"); return; }
                if (!ctx.IsRoguelike) { FollowUpModPlugin.Log.LogInfo("FU: inerte (not_roguelike)"); return; }
                if (!ctx.HostAnnouncesRule) { FollowUpModPlugin.Log.LogInfo("FU: host sem regra (" + CoopLevelPolicy.LobbyKey + "); vanilla"); return; }

                var snapshot = GroupAnchors.Read(candidate);
                if (snapshot.AnchorLevel <= 0)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: sem ancora de grupo (" + snapshot.Reason + "); nada a adequar");
                    return;
                }

                int ceiling = (int)candidate.MaxLevel;
                var decision = CoopLevelPolicy.DecidePromotion((int)candidate.Level, snapshot.AnchorLevel, ceiling);
                FollowUpModPlugin.Log.LogInfo("FU: gate nivel=" + candidate.Level + " ancora=" + snapshot.AnchorLevel
                    + " minimo=" + CoopLevelPolicy.GroupMinimum(snapshot.OtherCharacterLevels)
                    + " promove=" + decision.Promote + " delta=" + decision.LevelsToGrant
                    + (decision.CeilingLimited ? " ceiling_limited" : ""));

                if (decision.Promote)
                    PromotionService.Promote(candidate, decision.TargetLevel, decision.LevelsToGrant, decision.CeilingLimited);
            }
            catch (Exception ex)
            {
                FollowUpModPlugin.Log.LogWarning("FU: gate indisponivel, vanilla: " + ex.GetType().Name + ": " + ex.Message);
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
