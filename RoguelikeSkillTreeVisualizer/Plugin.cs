using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RoguelikeSkillTreeVisualizer (RSTV) — ESQUELETO (0.1.0).
    ///
    /// Alvo: na tela "Roguelike -> Select Party" (classe <c>CharacterChoiceManager</c>, l.208094 do
    /// decompilado) adicionar um botao QUADRADO a direita do "Choose Powerups"
    /// (<c>CharacterChoiceManager.roguelikePowerupButton</c>, l.208096) que abre a Skill Tree
    /// NATIVA (classe <c>SkillTreeManager</c>, l.172045 — a mesma do Campaign -> Change Skills)
    /// em modo SOMENTE LEITURA, com o contexto real do personagem.
    ///
    /// Nada disso esta implementado ainda: este arquivo e o ponto de partida. Os pontos de
    /// ancoragem, o que a tela nativa exige e o que NAO deu para determinar estao em
    /// <c>docs/RSTV-ANALISE.md</c> (na raiz do repositorio).
    ///
    /// Regras do projeto que valem aqui: um mod faz uma coisa so, nada de acoplar com os outros
    /// mods, e o plugin NAO cria GameObject no Awake (este Awake roda durante o chainloader do
    /// BepInEx, antes de existir cena — a Unity destroi o objeto na primeira carga de cena).
    /// A criacao tem de ser PREGUICOSA, ja com cena viva.
    /// </summary>
    [BepInPlugin(Guid, "Roguelike Skill Tree Visualizer", Version)]
    public class Plugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.roguelikeskilltreevisualizer";
        public const string Version = "0.1.0";

        internal static ManualLogSource Log { get; private set; }

        private void Awake()
        {
            Log = Logger;

            // Marcador de vida: se esta linha nao aparecer no LogOutput.log, o plugin nem carregou.
            Log.LogInfo("Roguelike Skill Tree Visualizer " + Version + " carregado (esqueleto, sem patch ativo).");

            // Os patches entram na proxima fase (RSTV-2). Sem PatchAll() por enquanto: o mod
            // carrega, loga e nao toca em nada do jogo.
            //
            // new Harmony(Guid).PatchAll();

            Log.LogInfo("RSTV: nenhum patch aplicado nesta versao — veja docs/RSTV-ANALISE.md.");
        }
    }

    // ---------------------------------------------------------------------------------------------
    // ESQUELETO DOS PATCHES (comentado DE PROPOSITO — descomentar na RSTV-2, um de cada vez,
    // validando no jogo entre cada um). Cada anotacao traz a linha do decompilado.
    // ---------------------------------------------------------------------------------------------
    //
    // /// <summary>
    // /// 1) Injetar o botao quando a tela Select Party e aberta/reaberta.
    // /// Ancora: CharacterChoiceManager.OpenCharacterChoiceManager() — l.208278 (chamado a cada
    // /// abertura; a tela e resetada antes por ResetCharacterChoice(), l.208219).
    // /// NAO usar o Update() da tela (l.208231) como gancho: ele roda todo frame e ja mexe em
    // /// acceptBtn (l.208235) e roguelikePowerupButton (l.208236).
    // /// </summary>
    // [HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.OpenCharacterChoiceManager))]
    // public static class CharacterChoiceManager_Open_Patch
    // {
    //     private static void Postfix(CharacterChoiceManager __instance)
    //     {
    //         try
    //         {
    //             // TODO RSTV-2a: clonar __instance.roguelikePowerupButton -> botao quadrado a DIREITA,
    //             // na MESMA linha, sem crescer a linha nem mudar o tamanho do acceptBtn (l.208130).
    //             // Duplicar por instancia tem de ser idempotente (guardar a referencia criada).
    //         }
    //         catch (System.Exception e)
    //         {
    //             Plugin.Log.LogError("RSTV: falha ao injetar o botao: " + e);
    //         }
    //     }
    // }
    //
    // /// <summary>
    // /// 2) Rastrear "o ultimo personagem que EU adicionei" a party.
    // /// Ancora: CharacterChoiceManager.ToggleSelectedCharacter(int) — l.208425; a entrada na party
    // /// grava character.SelectedForBattle = true (l.208470) e character.ControllerPlayerId (l.208471).
    // /// O jogo NAO guarda ordem de adicao (a party e derivada de AllCharacters filtrando
    // /// SelectedForBattle — l.140373 / l.140418), entao a ordem tem de ser registrada aqui.
    // /// </summary>
    // [HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.ToggleSelectedCharacter))]
    // public static class CharacterChoiceManager_Toggle_Patch
    // {
    //     private static void Postfix(CharacterChoiceManager __instance, int controllerPlayerId)
    //     {
    //         // TODO RSTV-2b: registrar o alvo quando ele for Owned (Character.Owned, l.32261) e o
    //         // jogador for o local; ao remover, cair para o ultimo local ainda em
    //         // NetworkingManager.Instance.MyPartyCharactersUnaccepted (l.144841).
    //     }
    // }
    //
    // /// <summary>
    // /// 3) Abrir a Skill Tree nativa em somente leitura (chamado no clique do botao novo).
    // /// Ancora: CharacterMenusManager.OpenSkillTreeMenu — l.48443; a carga preguiçosa e
    // /// LoadableUIWindow<SkillTreeManager>.LoadInstanceReference(...) (l.48471-48480) e a
    // /// inicializacao e Instance.Initialize(learnedSkills, unspentPoints, creating) — l.48481 / l.172380.
    // /// O contexto do personagem NAO entra por parametro: SkillTreeManager le
    // /// GameLogic.instance.CurrentlySelectedCharacter (l.108082; setter recusa personagem nao-Owned,
    // /// l.108124).
    // /// </summary>
    // public static void OpenSkillTreeReadOnly(Character target)
    // {
    //     // TODO RSTV-2c:
    //     // GameLogic.instance.CurrentlySelectedCharacter = target;
    //     // LoadableUIWindow<SkillTreeManager>.Instance.Initialize(target.SkillsFromPoints.ToList(), 0, creating: false);
    //     // LoadableUIWindow<SkillTreeManager>.Instance.gameObject.SetActive(true);
    //     // NUNCA chamar CharacterMenusManager.CloseSkillTreeMenu() (l.48490): ele chama
    //     // AcceptSkillChanges(closeMenu: true) e ESCRITA.
    // }
    //
    // /// <summary>
    // /// 4) SOMENTE LEITURA. O jogo NAO tem flag de read-only (varredura por readOnly/viewOnly: zero).
    // /// O que se usa: unspentPoints = 0 (CanLevel exige freeSkillPoints >= custo — l.322961),
    // /// RespecButton escondido (l.172867) e estes dois no-op:
    // ///   - SkillTreeManager.AcceptSkillChanges(bool)      — l.172494 (unico caminho que persiste)
    // ///   - SkillTreeItem.ToggleAddToSkillToAddList()      — l.171967 (clique no no da arvore)
    // /// </summary>
    // [HarmonyPatch(typeof(SkillTreeManager), nameof(SkillTreeManager.AcceptSkillChanges))]
    // public static class SkillTreeManager_Accept_Patch
    // {
    //     private static bool Prefix() => !ReadOnlyMode.Active; // false = nao executa o original
    // }
}
