using System;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace BetterCombatText
{
    /// <summary>
    /// BetterCombatText — deixa o texto de COMBATE legivel: contorno/halo suave (default: preto a
    /// 10% de alfa, o "sombreamento radial de 10%" pedido) em volta das letras dos NOMES de inimigo
    /// e dos ROTULOS/STACKS de buff e debuff, mais o TEXTO DO DADO nos eventos de rolagem.
    ///
    /// <para>Sem alteracao de gameplay. Nao toca em arquivo nenhum do jogo: so instancia o material
    /// do texto alvo (<c>TMP_Text.fontMaterial</c>) e ajusta propriedades DAQUELE componente.
    /// Nada de Bard/musica.</para>
    ///
    /// <para>Falha-segura: se qualquer coisa nao for encontrada o mod nao faz nada e loga o motivo;
    /// cada patch tem try/catch e o alvo do patch e sempre um TIPO explicito (nunca parametro
    /// posicional <c>ref __N</c>).</para>
    /// </summary>
    [BepInPlugin(Guid, "Better Combat Text", Versao)]
    public class Plugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.bettercombattext";
        public const string Versao = "0.1.0";

        internal static ManualLogSource Log { get; private set; }
        internal static Configuracao Cfg { get; private set; }

        /// <summary>false = config desligou o mod: nenhum patch e aplicado e nada muda no jogo.</summary>
        internal static bool Ativo;

        private void Awake()
        {
            Log = Logger;
            Log.LogInfo($"Better Combat Text {Versao} carregado (GUID {Guid}).");

            try
            {
                Cfg = new Configuracao(Config);
            }
            catch (Exception e)
            {
                Log.LogError($"Better Combat Text: falha ao ler o config — o mod NAO vai alterar nada. {e.GetType().Name}: {e.Message}");
                return;
            }

            if (!Cfg.Ativar.Value)
            {
                Ativo = false;
                Log.LogInfo("Better Combat Text: DESLIGADO no config (secao '1. Geral', chave 'Ativar' = false). " +
                            "Nenhum patch foi aplicado — o jogo roda 100% original.");
                return;
            }

            Ativo = true;

            try
            {
                new Harmony(Guid).PatchAll();
                Log.LogInfo(
                    "Better Combat Text: patches aplicados (por TIPO, sem parametro posicional). Alvos: " +
                    "BossHealthbar.set_BossCharacter e PlayerInfoWindow.ShowPlayerInfoWindow (nomes de inimigo), " +
                    "StatusIcon.UpdateStatusIcon (rotulos/stacks de buff e debuff), " +
                    "DiceRollingManager.RollDice e DiceRoller.StartRollVisuals (texto do dado nos eventos)" +
                    (Cfg.AplicarNumeroDeVida.Value ? " + Healthbar.Update (numero de vida, opcional ligado)" : "") +
                    ". Os efeitos aparecem quando cada superficie e escrita pelo jogo — abra um combate/evento para ver.");
                Log.LogInfo(
                    $"Better Combat Text: contorno cor={Cfg.Nomes.CorContornoHex.Value} " +
                    $"alfa={Cfg.Nomes.AlfaContorno.Value:0.###} largura={Cfg.Nomes.LarguraContorno.Value:0.###} " +
                    $"softness={Cfg.Nomes.SuavidadeContorno.Value:0.###} sombra={Cfg.Nomes.SombraAtiva.Value}; " +
                    $"eventos(dado) ativo={Cfg.EventosAtivar.Value}; numero de vida={Cfg.AplicarNumeroDeVida.Value}.");
                Log.LogInfo($"Better Combat Text: config em BepInEx/config/{Guid}.cfg — " +
                            "para desligar TUDO basta 'Ativar = false' na secao '1. Geral'.");
            }
            catch (Exception e)
            {
                Ativo = false;
                Log.LogError($"Better Combat Text: falha ao aplicar os patches Harmony — mod inerte. {e.GetType().Name}: {e.Message}");
            }
        }
    }
}
