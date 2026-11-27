using System.Collections.Generic;

namespace FollowUpMod
{
    public readonly struct GroupSnapshot
    {
        /// <summary>Niveis dos membros ja aceitos (sem o candidato).</summary>
        public readonly int[] OtherCharacterLevels;
        /// <summary>Nivel do PRIMEIRO membro aceito: a mesma ancora que o gate nativo compara.</summary>
        public readonly int AnchorLevel;
        public readonly int OwnLevel;
        public readonly string Reason;

        public GroupSnapshot(int[] otherCharacterLevels, int anchorLevel, int ownLevel, string reason)
        {
            OtherCharacterLevels = otherCharacterLevels;
            AnchorLevel = anchorLevel;
            OwnLevel = ownLevel;
            Reason = reason;
        }
    }

    /// <summary>Leitura pura do grupo aceito. Nunca escreve em Character nem em save.</summary>
    internal static class GroupAnchors
    {
        internal static GroupSnapshot Read(Character candidate)
        {
            var root = NetworkingManager.Instance != null && NetworkingManager.Instance.NetworkManager != null
                ? NetworkingManager.Instance.NetworkManager.Root
                : null;
            int own = candidate != null ? (int)candidate.Level : 0;
            if (root == null) return new GroupSnapshot(new int[0], 0, own, "root_missing");
            if (candidate == null) return new GroupSnapshot(new int[0], 0, 0, "candidate_missing");

            var accepted = root.PartyCharactersUnaccepted;
            if (accepted == null || accepted.Count == 0)
                return new GroupSnapshot(new int[0], 0, own, "no_accepted_party");

            var levels = new List<int>(accepted.Count);
            int anchor = 0;
            for (int i = 0; i < accepted.Count; i++)
            {
                var member = accepted[i];
                if (member == null || ReferenceEquals(member, candidate)) continue;
                levels.Add((int)member.Level);
            }
            // O gate nativo usa accepted[0]; se o candidato for justamente o primeiro, a lista
            // util (levels) e a ancora caem no proximo membro aceito.
            anchor = (int)accepted[0].Level;
            if (ReferenceEquals(accepted[0], candidate) && levels.Count > 0) anchor = levels[0];
            return new GroupSnapshot(levels.ToArray(), anchor, own, levels.Count == 0 ? "no_accepted_party" : "ok");
        }
    }
}
