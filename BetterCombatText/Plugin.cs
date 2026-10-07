using System;
using System.Collections.Generic;
using System.Reflection;
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
    ///
    /// <para>Os ganchos sao aplicados UM A UM (ver <c>AplicarPatches</c>), e nao por
    /// <c>PatchAll()</c>: num aplicador unico um gancho ruim deixaria os outros sem aplicar e em
    /// silencio — e este mod tem 9 ganchos espalhados por dois arquivos.</para>
    /// </summary>
    [BepInPlugin(Guid, "Better Combat Text", Versao)]
    public class Plugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.bettercombattext";
        public const string Versao = "0.1.2";

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

            int ganchosOk = AplicarPatches();
            if (ganchosOk == 0)
            {
                // AplicarPatches ja escreveu no log POR QUE nenhum gancho entrou.
                Ativo = false;
                Log.LogError("Better Combat Text: NENHUM gancho foi aplicado — o mod fica inerte nesta sessao " +
                             "(o jogo roda original; o motivo esta nas linhas acima).");
                return;
            }

            try
            {
                Log.LogInfo(
                    "Better Combat Text: alvos dos ganchos (por TIPO, sem parametro posicional): " +
                    "BossHealthbar.set_BossCharacter e PlayerInfoWindow.ShowPlayerInfoWindow (nomes de inimigo), " +
                    "StatusIcon.UpdateStatusIcon (rotulos/stacks de buff e debuff), " +
                    "DiceRollingManager.RollDice e DiceRoller.StartRollVisuals (texto do dado nos eventos)" +
                    (Cfg.AplicarNumeroDeVida.Value ? " + Healthbar.Update (numero de vida, opcional ligado)" : "") +
                    ". Os efeitos aparecem quando cada superficie e escrita pelo jogo — abra um combate/evento para ver.");
                Log.LogInfo(
                    $"Better Combat Text: contorno cor={Cfg.Nomes.CorContornoHex.Value} " +
                    $"alfa={Cfg.Nomes.AlfaContorno.Value:0.###} largura={Cfg.Nomes.LarguraContorno.Value:0.###} " +
                    $"softness={Cfg.Nomes.SuavidadeContorno.Value:0.###} sombra={Cfg.Nomes.SombraAtiva.Value}; " +
                    $"eventos(dado) ativo={Cfg.EventosAtivar.Value}; numero de vida={Cfg.AplicarNumeroDeVida.Value}; " +
                    $"diagnostico no arranque={Cfg.DiagnosticoArranque.Value}.");
                Log.LogInfo($"Better Combat Text: config em BepInEx/config/{Guid}.cfg — " +
                            "para desligar TUDO basta 'Ativar = false' na secao '1. Geral'.");
            }
            catch (Exception e)
            {
                // Os ganchos JA estao aplicados: falha daqui e de LOG, nao de patch — o mod segue de pe.
                Log.LogWarning($"Better Combat Text: falha ao escrever o resumo de config no log: {e.GetType().Name}: {e.Message}");
            }
        }

        /// <summary>
        /// Aplica os ganchos UM A UM, em vez de <c>PatchAll()</c> — e o modelo do repositorio
        /// (BetterTooltips, RoguelikeSkillTreeVisualizer, BetterFont, ...).
        ///
        /// <para><c>PatchAll()</c> e tudo-ou-nada: se UM gancho so falhasse (tipo ou assinatura que
        /// mudou numa versao do jogo), a excecao subia dali e os outros oito nunca eram aplicados —
        /// o mod morria em silencio, sem dizer qual gancho foi o culpado. Com o laco abaixo, o gancho
        /// que falha fica escrito no log com o NOME dele e o resto continua funcionando.</para>
        ///
        /// <para>O resumo usa a contagem REAL (quantos ganchos de quantos, e quantos metodos do jogo
        /// o Harmony registrou), nunca um numero fixo escrito no codigo: e por ele que se descobre,
        /// lendo o log, que um gancho nao entrou.</para>
        /// </summary>
        /// <returns>Quantos ganchos foram aplicados com sucesso (0 = mod inerte).</returns>
        private static int AplicarPatches()
        {
            // Harmony cria um "patch room" identificado pelo GUID do mod.
            Harmony harmony = new Harmony(Guid);
            List<string> falhas = new List<string>();
            int ganchosTotal = 0;
            int ganchosOk = 0;
            int metodosOk = 0;

            Type[] tipos;
            try
            {
                tipos = typeof(Plugin).Assembly.GetTypes();
            }
            catch (Exception e)
            {
                Log.LogError("Better Combat Text: nao deu para listar os tipos do mod — nenhum gancho aplicado: " + e);
                return 0;
            }

            for (int i = 0; i < tipos.Length; i++)
            {
                Type tipo = tipos[i];
                if (!EhClasseDeGancho(tipo))
                {
                    continue;
                }

                ganchosTotal++;
                try
                {
                    PatchClassProcessor processador = harmony.CreateClassProcessor(tipo);
                    List<MethodInfo> aplicados = processador.Patch();
                    int quantos = aplicados != null ? aplicados.Count : 0;
                    metodosOk += quantos;
                    ganchosOk++;
                    Log.LogInfo("Better Combat Text: gancho aplicado — " + tipo.Name + " (" + quantos +
                                " metodo(s) do jogo).");
                }
                catch (Exception e)
                {
                    falhas.Add(tipo.Name);
                    Log.LogError("Better Combat Text: FALHA ao aplicar o gancho " + tipo.Name + " — " + e.Message);
                }
            }

            string resumo = "Better Combat Text: patches Harmony aplicados (" + ganchosOk + "/" + ganchosTotal +
                            " ganchos, " + metodosOk + " metodos do jogo).";

            if (falhas.Count == 0)
            {
                Log.LogInfo(resumo);
                return ganchosOk;
            }

            Log.LogError(resumo + " GANCHOS QUE FALHARAM: " + string.Join(", ", falhas.ToArray()) +
                         ". O mod continua de pe, mas o recurso que dependia deles nao existe nesta sessao.");
            return ganchosOk;
        }

        /// <summary>
        /// Classe de gancho = tem <c>[HarmonyPatch]</c> no TIPO (declarado, nao herdado).
        ///
        /// <para>Aqui NAO se exige <c>[HarmonyPrefix]</c>/<c>[HarmonyPostfix]</c> no metodo: o
        /// Harmony aceita as DUAS formas de declarar um gancho — metodo com o atributo ou metodo
        /// chamado <c>Prefix</c>/<c>Postfix</c> (convencao de nome) — e ha mods do projeto escritos
        /// em uma e em outra. Exigir o atributo pularia, em silencio, os ganchos declarados por nome,
        /// ou seja: mudaria o que o mod faz. Uma classe com <c>[HarmonyPatch]</c> e sem metodo de
        /// patch apenas nao registra nada (<c>Patch()</c> devolve lista vazia), sem efeito colateral
        /// — e o mesmo conjunto que o <c>PatchAll()</c> processaria.</para>
        /// </summary>
        private static bool EhClasseDeGancho(Type tipo)
        {
            try
            {
                if (tipo == null || !tipo.IsClass)
                {
                    return false;
                }

                return tipo.GetCustomAttributes(typeof(HarmonyPatch), false).Length > 0;
            }
            catch (Exception)
            {
                // atributo com tipo que nao resolve (versao de jogo diferente): nao e gancho nosso
                return false;
            }
        }
    }
}
