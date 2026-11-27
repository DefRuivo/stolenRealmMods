using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

namespace FollowUpMod
{
    /// <summary>
    /// Marca os personagens promovidos nesta sessao. Enquanto a marcacao existir, o save do
    /// personagem NAO roda: nem o nivel promovido, nem as skills/itens/atributos concedidos
    /// pela fila de recompensas chegam ao arquivo. O nivel original e devolvido ao objeto
    /// quando a sessao termina.
    ///
    /// Bloquear (em vez de trocar o nivel durante o save) e o que evita recursao: em 1.4.9
    /// `SaveDataThrottler.ProcessSaveData` chama `Character.Save()` de forma sincrona e o
    /// setter de ExperienceLevel enfileira outro save (Character.cs:5084-5091;
    /// SaveDataThrottler.cs:152-157).
    /// </summary>
    internal static class SessionGuard
    {
        private sealed class Mark
        {
            internal float OriginalExperienceLevel;
        }

        private static readonly ConditionalWeakTable<Character, Mark> Marks =
            new ConditionalWeakTable<Character, Mark>();
        private static readonly HashSet<Character> LoggedBlocks =
            new HashSet<Character>(ReferenceComparer<Character>.Instance);

        internal static void MarkPromoted(Character character, float originalExperienceLevel)
        {
            if (character == null) return;
            if (Marks.TryGetValue(character, out var existing))
            {
                existing.OriginalExperienceLevel = originalExperienceLevel;
                return;
            }
            Marks.Add(character, new Mark { OriginalExperienceLevel = originalExperienceLevel });
        }

        internal static bool IsPromoted(Character character)
        {
            return character != null && Marks.TryGetValue(character, out _);
        }

        internal static bool ShouldBlockSave(Character character)
        {
            if (!IsPromoted(character)) return false;
            lock (LoggedBlocks)
            {
                if (LoggedBlocks.Add(character))
                    FollowUpModPlugin.Log.LogInfo("FU: save do personagem promovido bloqueado (nivel e recompensas ficam so na sessao)");
            }
            return true;
        }

        internal static void Forget(Character character)
        {
            if (character == null) return;
            try { Marks.Remove(character); } catch { }
            lock (LoggedBlocks) LoggedBlocks.Remove(character);
        }

        /// <summary>Devolve o nivel original a cada personagem marcado e so entao descarta a marca.</summary>
        internal static void RestoreAllAndForget()
        {
            var keys = new List<Character>();
            foreach (var entry in Marks) keys.Add(entry.Key);
            foreach (var key in keys)
            {
                try
                {
                    if (Marks.TryGetValue(key, out var mark)) key.ExperienceLevel = mark.OriginalExperienceLevel;
                }
                catch (Exception ex)
                {
                    FollowUpModPlugin.Log.LogWarning("FU: restauracao falhou: " + ex.GetType().Name);
                }
                Forget(key);
            }
        }

        private sealed class ReferenceComparer<T> : IEqualityComparer<T> where T : class
        {
            internal static readonly ReferenceComparer<T> Instance = new ReferenceComparer<T>();
            public bool Equals(T x, T y) => ReferenceEquals(x, y);
            public int GetHashCode(T obj) => RuntimeHelpers.GetHashCode(obj);
        }
    }
}
