using System.Collections.Generic;

namespace FollowUpMod
{
    public readonly struct GroupSnapshot
    {
        public readonly int[] OtherCharacterLevels;
        public readonly int OwnLevel;
        public readonly string Reason;

        public GroupSnapshot(int[] otherCharacterLevels, int ownLevel, string reason)
        {
            OtherCharacterLevels = otherCharacterLevels;
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
            if (root == null) return new GroupSnapshot(new int[0], candidate != null ? (int)candidate.Level : 0, "root_missing");
            if (candidate == null) return new GroupSnapshot(new int[0], 0, "candidate_missing");

            var accepted = root.PartyCharactersUnaccepted;
            var levels = new List<int>();
            if (accepted != null)
            {
                for (int i = 0; i < accepted.Count; i++)
                {
                    var member = accepted[i];
                    if (member != null && !ReferenceEquals(member, candidate)) levels.Add((int)member.Level);
                }
            }
            return new GroupSnapshot(levels.ToArray(), (int)candidate.Level,
                levels.Count == 0 ? "no_accepted_party" : "ok");
        }
    }
}
