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
            Diag.Write("prefix entrou");
            try
            {
                var candidate = manager != null && manager.selectedCharacterChoiceItem != null
                    ? manager.selectedCharacterChoiceItem.Character
                    : null;
                Diag.Write("prefix entrou candidato=" + (candidate == null ? "null" : candidate.CharacterName + "/nivel " + candidate.Level));
                FollowUpModPlugin.Log.LogInfo("FU: prefix entrou candidato=" +
                    (candidate == null ? "null" : candidate.CharacterName + "/nivel " + candidate.Level + "/selecionado " + candidate.SelectedForBattle));
                if (candidate == null) return;
                if (candidate.SelectedForBattle)
                {
                    FollowUpModPlugin.Log.LogInfo("FU: candidato ja selecionado; nada a fazer");
                    return;
                }

                var ctx = Context.Read();
                Diag.Write("contexto mp=" + ctx.IsMultiplayer + " rog=" + ctx.IsRoguelike + " regra=" + ctx.HostAnnouncesRule);
                if (!ctx.IsMultiplayer) { FollowUpModPlugin.Log.LogInfo("FU: inerte (not_multiplayer)"); return; }
                if (!ctx.IsRoguelike) { FollowUpModPlugin.Log.LogInfo("FU: inerte (not_roguelike)"); return; }
                if (!ctx.HostAnnouncesRule)
                {
                    // Modo cliente (validacao): o host nao tem o mod, entao a regra nao foi
                    // anunciada no lobby. Em vez de ficar inerte, adequamos o nivel localmente.
                    // O jogo continua decidindo aceitar/recusar com a regra original, agora
                    // comparando o nivel ja adequado.
                    Diag.Write("host sem regra: modo cliente");
                    FollowUpModPlugin.Log.LogInfo("FU: host sem regra (" + CoopLevelPolicy.LobbyKey + "); modo cliente (adequa localmente)");
                }

                var snapshot = GroupAnchors.Read(candidate);
                Diag.Write("snapshot ancora=" + snapshot.AnchorLevel + " motivo=" + snapshot.Reason);
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
                Diag.Write("EXCECAO no gate: " + ex.GetType().Name + ": " + ex.Message + " | " + ex.StackTrace);
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
