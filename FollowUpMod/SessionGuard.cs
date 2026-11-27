using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

namespace FollowUpMod
{
    /// <summary>
    /// Guarda o nivel original de cada personagem promovido e, na hora de gravar,
    /// devolve o valor original ao arquivo: o save continua guardando o resto do
    /// progresso normalmente, e apenas o nivel promovido nao persiste.
    /// </summary>
    internal static class SessionGuard
    {
        private sealed class Mark
        {
            internal float OriginalExperienceLevel;
        }

        private static readonly ConditionalWeakTable<Character, Mark> Marks = new ConditionalWeakTable<Character, Mark>();
        private static bool _stashing;

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

        internal static bool IsPromoted(Character character) => character != null && Marks.TryGetValue(character, out _);

        /// <summary>Troca o nivel efetivo pelo original enquanto o save roda. Devolve true se trocou.</summary>
        internal static bool Stash(Character character)
        {
            if (_stashing || character == null) return false;
            if (!Marks.TryGetValue(character, out var mark)) return false;
            _stashing = true;
            try { character.ExperienceLevel = mark.OriginalExperienceLevel; }
            catch (Exception ex) { FollowUpModPlugin.Log.LogWarning("FU: stash falhou: " + ex.GetType().Name); return false; }
            finally { _stashing = false; }
            return true;
        }

        internal static void RestorePromoted(Character character, float promotedExperienceLevel)
        {
            if (character == null) return;
            _stashing = true;
            try { character.ExperienceLevel = promotedExperienceLevel; }
            catch (Exception ex) { FollowUpModPlugin.Log.LogWarning("FU: restore falhou: " + ex.GetType().Name); }
            finally { _stashing = false; }
        }

        internal static void Forget(Character character)
        {
            if (character == null) return;
            try { Marks.Remove(character); } catch { }
        }

        internal static void ForgetAll()
        {
            var keys = new List<Character>();
            foreach (var entry in Marks) keys.Add(entry.Key);
            foreach (var key in keys) Forget(key);
        }
    }
}
