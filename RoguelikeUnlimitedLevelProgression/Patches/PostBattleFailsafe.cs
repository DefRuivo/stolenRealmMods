using System;
using System.Collections.Generic;
using HarmonyLib;
using RoguelikeUnlimitedLevelProgression.Runtime;

namespace RoguelikeUnlimitedLevelProgression.Patches
{
    /// <summary>
    /// FAILSAFE de pos-batalha (RLP-1).
    ///
    /// Por que existe: o patch critico so age na janela estrutural de
    /// Root.SendGameCompleteFromServer (IL_0092 da DLL do jogo), que fica DEPOIS de duas guardas
    /// de fluxo do proprio jogo:
    ///   IL_0079 FastLinqExtensions::FastContains(GameLogic.AllMyCharacters, character) -> continue
    ///   IL_008d Game::get_RoguelikeModeActive()                                          -> continue
    /// Quando a guarda manda o personagem para o `continue`, a comparacao substituida nao roda.
    /// RLP-2: isso NAO provava a causa das rodadas anteriores. O OnDestroy do plugin removia
    /// TODOS os patches (inclusive este failsafe) ao destruir o host do chainloader.
    ///
    /// Este prefix roda no unico ponto que o jogo comprovadamente executa ao fim da batalha
    /// (PostBattleManager.OpenPostBattleMenu e chamado em IL_0575 do MESMO metodo, com o mesmo
    /// `victory`), e concede o nivel estendido apenas aos personagens que a janela vanilla NAO
    /// promoveu (personagem ausente de `roguelikeCharactersToLevel`). A decisao continua sendo a
    /// MESMA politica (Policy.CanAdvance) — nada e concedido fora do escopo ampliado.
    ///
    /// Fora do escopo ampliado (campanha, IA, multiplayer, mod desligado) este prefix nao faz nada.
    /// </summary>
    public static class PostBattleFailsafePatches
    {
        private static void Deny(string reason) { Log.Refuse("pos-batalha", reason, once: false); }

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
