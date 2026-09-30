using System;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RoguelikeSkillTreeVisualizer (RSTV) — RSTV-2 implementada.
    ///
    /// Na tela "Roguelike -> Select Party" (classe <c>CharacterChoiceManager</c>, l.208094 do
    /// decompilado) um botao QUADRADO aparece a DIREITA do "Choose Powerups"
    /// (<c>CharacterChoiceManager.roguelikePowerupButton</c>, l.208096) e abre a Skill Tree
    /// NATIVA (<c>SkillTreeManager</c>, l.172045 — a mesma do Campaign -> Change Skills) em modo
    /// SOMENTE LEITURA, com o contexto real do personagem (o ultimo que o jogador local adicionou
    /// a party). Nenhum ponto e gasto, nada e gravado.
    ///
    /// Pecas do mod:
    ///   - <c>SelectPartyButton</c>  — clona o botao nativo e compensa a largura da linha;
    ///   - <c>PartyTargets</c>       — ordem de adicao local (o jogo NAO guarda essa ordem);
    ///   - <c>SkillTreeReadOnly</c>  — abertura nativa + sessao de somente leitura;
    ///   - <c>Patches</c>            — os ganchos Harmony (cada um com a linha do decompilado);
    ///   - <c>RstvHost</c>           — MonoBehaviour criado de forma preguicosa.
    ///
    /// Regras do projeto que valem aqui: um mod faz uma coisa so, nada de acoplar com os outros
    /// mods, e o plugin NAO cria GameObject no Awake (este Awake roda durante o chainloader do
    /// BepInEx, antes de existir cena — a Unity destrui o objeto na primeira carga de cena).
    /// A criacao tem de ser PREGUICOSA, ja com cena viva.
    ///
    /// Os pontos de ancoragem e o que NAO deu para determinar estao em
    /// <c>docs/RSTV-ANALISE.md</c> (na raiz do repositorio).
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
            Log.LogInfo("Roguelike Skill Tree Visualizer " + Version +
                        " carregado (RSTV-2: botao ao lado do Choose Powerups + skill tree read-only).");

            try
            {
                new Harmony(Guid).PatchAll(typeof(Plugin).Assembly);
                Log.LogInfo("RSTV: patches Harmony aplicados (7 ganchos).");
            }
            catch (Exception e)
            {
                Log.LogError("RSTV: falha ao aplicar os patches: " + e);
            }
        }
    }
}
