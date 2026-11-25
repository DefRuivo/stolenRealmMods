using System;
using System.Collections.Generic;
using HarmonyLib;
using RoguelikeUnlimitedLevelProgression.Runtime;

namespace RoguelikeUnlimitedLevelProgression.Patches
{
    /// <summary>
    /// CONCESSOR de pos-batalha (RLP-1 / BANTER-1).
    ///
    /// BANTER-1: desde a 0.1.4 este prefix e' o UNICO ponto que concede o nivel estendido, e ele
    /// participa do grupo fail-closed. O patch no metodo de resultado (Root.SendGameCompleteFromServer)
    /// foi REMOVIDO: o HarmonyX reemite o corpo e o emissor retargeta o `leave` do `if` do banter
    /// (#317 -> #322), fazendo o `else` rodar junto e produzindo a segunda fala no heroi com espera
    /// por clique antes das recompensas.
    ///
    /// Por que este ponto: a janela estrutural de Root.SendGameCompleteFromServer (IL_0092 da DLL do
    /// jogo) fica DEPOIS de duas guardas de fluxo do proprio jogo:
    ///   IL_0079 FastLinqExtensions::FastContains(GameLogic.AllMyCharacters, character) -> continue
    ///   IL_008d Game::get_RoguelikeModeActive()                                          -> continue
    /// Quando a guarda manda o personagem para o `continue`, o loop nativo nao promove ninguem.
    /// RLP-2: isso NAO provava a causa das rodadas anteriores. O OnDestroy do plugin removia
    /// TODOS os patches (inclusive este failsafe) ao destruir o host do chainloader.
    ///
    /// Este prefix roda no unico ponto que o jogo comprovadamente executa ao fim da batalha
    /// (PostBattleManager.OpenPostBattleMenu e chamado em IL_0575 do MESMO metodo, com o mesmo
    /// `victory` e a MESMA instancia de lista), e concede o nivel estendido apenas aos personagens
    /// que a janela vanilla NAO
    /// promoveu (personagem ausente de `roguelikeCharactersToLevel`). A decisao continua sendo a
    /// MESMA politica (Policy.CanAdvance) — nada e concedido fora do escopo ampliado.
    ///
    /// Fora do escopo ampliado (campanha, IA, multiplayer, mod desligado) este prefix nao faz nada.
    /// </summary>
    public static class PostBattleFailsafePatches
    {
        private static void Deny(string reason) { Log.Refuse("pos-batalha", reason, once: false); }

        /// <summary>Paridade com <c>FastLinqExtensions::FastContains(GameLogic.AllMyCharacters, c)</c>.
        /// Se o membro nao existir na build, aceita (fail-open SO' nesta guarda de escopo: a lista
        /// nativa e' a fonte; sem ela o comportamento continua o do prefix anterior).</summary>
        private static bool AllMyCharactersFastContains(Character character)
        {
            try
            {
                var logic = GameLogic.instance;
                if (logic == null) return false;
                var all = logic.AllMyCharacters;
                return all != null && all.Contains(character);
            }
            catch (Exception ex)
            {
                Log.WarnOnce("pos-batalha: AllMyCharacters indisponivel (" + ex.GetType().Name + "); guarda pulada");
                return true;
            }
        }

        public static void Prefix(bool victory, List<Character> roguelikeCharactersToLevel)
        {
            try
            {
                Log.Info("pos-batalha: hook entrou; victory=" + victory
                         + " lista=" + (roguelikeCharactersToLevel == null ? "null" : roguelikeCharactersToLevel.Count.ToString())
                         + " enabled=" + PluginState.Enabled + " grupo=" + PluginState.GameplayGroupApplied);
                PatchRegistryEvidence.FirstHook("PostBattleManager.OpenPostBattleMenu");
                PatchRegistry.LogOwnership("pos-batalha");
                if (!victory) { Deny("victory=False"); return; }
                if (roguelikeCharactersToLevel == null) { Deny("roguelikeCharactersToLevel=null"); return; }
                if (!PluginState.Enabled) { Deny("General.Enabled=False"); return; }
                if (!PluginState.GameplayGroupApplied) { Deny("GameplayGroupApplied=False"); return; }

                // Os gates continuam fail-closed; toda recusa agora tem motivo incondicional.
                if (!GameState.IsRoguelikeMode()) { Deny("IsRoguelikeMode=False"); return; }
                if (GameState.IsMultiplayer()) { Deny("IsMultiplayer=True (inclui rede incerta)"); return; }

                var logic = GameLogic.instance;
                if (logic == null) { Deny("GameLogic.instance=null"); return; }
                var controlled = logic.ControlledCharacters;
                if (controlled == null) { Deny("ControlledCharacters=null"); return; }
                var characters = new List<Character>(controlled);
                if (characters.Count == 0) { Deny("ControlledCharacters vazio"); return; }

                var settings = GameState.Settings();

                foreach (Character character in characters)
                {
                    if (character == null) { Deny("character=null na lista controlada"); continue; }
                    Log.Info("pos-batalha: personagem=" + character.CharacterName + " nivel=" + character.Level
                             + " IsAI=" + character.IsAI + " IsRoguelikeCharacter=" + character.IsRoguelikeCharacter);
                    if (character.IsAI) { Deny("IsAI=True: " + character.CharacterName); continue; }
                    if (!character.IsRoguelikeCharacter) { Deny("IsRoguelikeCharacter=False: " + character.CharacterName); continue; }

                    // Paridade com a 1a guarda do loop nativo (IL_0079): personagem fora de
                    // AllMyCharacters e' pulado pelo jogo, entao tambem e' pulado aqui.
                    if (!AllMyCharactersFastContains(character))
                    {
                        Deny("fora de GameLogic.AllMyCharacters (paridade com o loop nativo): " + character.CharacterName);
                        continue;
                    }

                    // A janela vanilla promoveu este personagem: evita nivel dobrado.
                    if (roguelikeCharactersToLevel.Contains(character))
                    {
                        Deny("nivel adicional nao concedido: ja na lista vanilla: " + character.CharacterName);
                        continue;
                    }
                    if (!Policy.CanAdvance(character, settings))
                    {
                        Deny("Policy.CanAdvance=False: " + character.CharacterName + "; " + PluginState.LastDenial);
                        continue;
                    }

                    int before = character.Level;
                    character.GiveExperience(character.ExpForNextLevel);
                    roguelikeCharactersToLevel.Add(character);
                    Log.Info("pos-batalha (failsafe): nivel estendido concedido a " + character.CharacterName
                             + " (" + before + " -> " + character.Level + "); janela vanilla nao havia promovido");
                }
            }
            catch (Exception ex)
            {
                Deny("falha " + ex.GetType().Name + ": " + ex.Message + "; fluxo vanilla mantido");
            }
        }
    }
}
