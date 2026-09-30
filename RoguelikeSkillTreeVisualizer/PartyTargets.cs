using System;
using System.Collections.Generic;
using Burst2Flame;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// "O ULTIMO personagem que EU adicionei a party" — regra do README do mod.
    ///
    /// O jogo NAO guarda ordem de adicao: a Current Party e derivada
    /// (`Root.PartyCharactersUnaccepted => CharactersInBattle.FastWhere(!IsAI)`, l.140418, e
    /// `CharactersInBattle => AllCharacters.FastWhere(SelectedForBattle)`, l.140373). Ou seja,
    /// "o ultimo que eu adicionei" nao existe como dado — o mod precisa registrar o evento.
    /// E o que este arquivo faz: o patch em `CharacterChoiceManager.ToggleSelectedCharacter`
    /// (l.208425) alimenta a lista abaixo; a resolucao do alvo acontece NO CLIQUE.
    ///
    /// Por que so `Owned`: `Character.Owned` (l.32261) e `OwnerID == NetworkId local && !IsAI`.
    /// Isso implementa a regra "cada jogador usa os SEUS personagens" — o que o outro jogador
    /// adiciona nao entra nesta lista, entao nao muda o meu contexto.
    /// </summary>
    internal static class PartyTargets
    {
        /// <summary>Ordem local de adicao (mais novo no fim). Nao inclui personagem de outro jogador.</summary>
        private static readonly List<Character> AdditionOrder = new List<Character>();

        internal static bool IsLocal(Character character)
        {
            try
            {
                return character != null && character.Owned;
            }
            catch (Exception)
            {
                return false;
            }
        }

        internal static void NoteAddition(Character character)
        {
            if (!IsLocal(character))
            {
                return;
            }

            AdditionOrder.RemoveAll(c => c == null || c == character || !IsLocal(c));
            AdditionOrder.Add(character);
        }

        internal static void NoteRemoval(Character character)
        {
            if (character == null)
            {
                return;
            }

            AdditionOrder.Remove(character);
        }

        /// <summary>
        /// Alvo do clique: o ultimo que EU adicionei que ainda esta na party. Se a lista local
        /// estiver vazia (ex.: a party ja existia quando a tela abriu), cai para o ultimo da lista
        /// LOCAL da party (`MyPartyCharactersUnaccepted`, l.144841 — nunca o ultimo global).
        /// Devolve null quando a party local esta vazia (=> botao desabilitado).
        /// </summary>
        internal static Character Resolve()
        {
            try
            {
                List<Character> myParty = NetworkingManager.Instance.MyPartyCharactersUnaccepted;
                if (myParty == null || myParty.Count == 0)
                {
                    return null;
                }

                for (int i = AdditionOrder.Count - 1; i >= 0; i--)
                {
                    Character candidate = AdditionOrder[i];
                    if (candidate != null && myParty.Contains(candidate))
                    {
                        return candidate;
                    }
                }

                return myParty[myParty.Count - 1];
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao resolver o personagem da party: " + e.Message);
                return null;
            }
        }
    }
}
