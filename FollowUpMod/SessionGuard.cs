using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

namespace FollowUpMod
{
    /// <summary>
    /// Guarda o nivel original de cada personagem promovido. Na hora de gravar, o valor
    /// original vai para o arquivo e o promovido volta logo depois: o resto do progresso
    /// continua sendo salvo normalmente e apenas o nivel promovido nao persiste.
    ///
    /// Importante (medido em 1.4.9): `SaveDataThrottler.AddToSaveQueue` chama
    /// `Character.Save()` de forma SINCRONA, e o setter de ExperienceLevel chama
    /// `QueueCharacterSave`. Trocar o nivel dentro do save reentra no proprio save; quem
    /// corta a recursao e a profundidade contada em SaveGuardPatch, nao este arquivo.
    /// </summary>
    internal static class SessionGuard
    {
        private sealed class Mark
        {
            internal float OriginalExperienceLevel;
            internal float PromotedExperienceLevel;
        }

        private static readonly ConditionalWeakTable<Character, Mark> Marks =
            new ConditionalWeakTable<Character, Mark>();

        internal static void MarkPromoted(Character character, float originalExperienceLevel, float promotedExperienceLevel)
        {
            if (character == null) return;
            if (Marks.TryGetValue(character, out var existing))
            {
                existing.OriginalExperienceLevel = originalExperienceLevel;
                existing.PromotedExperienceLevel = promotedExperienceLevel;
                return;
            }
            Marks.Add(character, new Mark
            {
                OriginalExperienceLevel = originalExperienceLevel,
                PromotedExperienceLevel = promotedExperienceLevel
            });
        }

        internal static bool IsPromoted(Character character)
        {
            return character != null && Marks.TryGetValue(character, out _);
        }

        /// <summary>Devolve o nivel original ao objeto para o save. true = trocou (e ha que voltar).</summary>
        internal static bool Stash(Character character)
        {
            if (character == null || !Marks.TryGetValue(character, out var mark)) return false;
            try
            {
                character.ExperienceLevel = mark.OriginalExperienceLevel;
                return true;
            }
            catch (Exception ex)
            {
                FollowUpModPlugin.Log.LogWarning("FU: stash falhou: " + ex.GetType().Name + ": " + ex.Message);
                return false;
            }
        }

        internal static void RestorePromoted(Character character)
        {
            if (character == null || !Marks.TryGetValue(character, out var mark)) return;
            try { character.ExperienceLevel = mark.PromotedExperienceLevel; }
            catch (Exception ex) { FollowUpModPlugin.Log.LogWarning("FU: restore falhou: " + ex.GetType().Name); }
        }

        internal static void Forget(Character character)
        {
            if (character == null) return;
            try { Marks.Remove(character); } catch { }
        }

        /// <summary>
        /// Devolve o nivel original a cada personagem marcado e so entao descarta a marca.
        /// Ordem importa: esquecer antes de restaurar deixaria o nivel promovido vivo e
        /// qualquer save posterior o gravaria.
        /// </summary>
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
                catch (System.Exception ex)
                {
                    FollowUpModPlugin.Log.LogWarning("FU: restauracao falhou (" + key.GetType().Name + "): " + ex.GetType().Name);
                }
                Forget(key);
            }
        }
    }
}
