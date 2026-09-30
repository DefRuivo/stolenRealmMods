using System;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
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
    ///   - <c>SelectPartyButton</c>  — clona o botao nativo da tela Select Party e compensa a largura da linha;
    ///   - <c>RunButton</c>          — RSTV-5: o mesmo botao no HUD DA RUN, ancorado no Ping Button;
    ///   - <c>RunTargets</c>         — RSTV-5: alvo do clique na run + PORTAO DE SEGURANCA (estado do jogo);
    ///   - <c>PartyTargets</c>       — ordem de adicao local (o jogo NAO guarda essa ordem);
    ///   - <c>SkillTreeReadOnly</c>  — abertura nativa + sessao de somente leitura (blindagens 1/2/3/5/6);
    ///   - <c>Patches</c>            — os ganchos Harmony (cada um com a linha do decompilado);
    ///   - <c>RstvHost</c>           — MonoBehaviour criado de forma preguicosa.
    ///
    /// Regras do projeto que valem aqui: um mod faz uma coisa so, nada de acoplar com os outros
    /// mods, e o plugin NAO cria GameObject no Awake (este Awake roda durante o chainloader do
    /// BepInEx, antes de existir cena — a Unity destrui o objeto na primeira carga de cena).
    /// A criacao tem de ser PREGUICOSA, ja com cena viva.
    ///
    /// Um mod que injeta UI e abre janela nativa nao pode falhar em silencio: por isso os ganchos
    /// sao aplicados (e logados) um a um, o resumo do boot traz a CONTAGEM REAL de ganchos
    /// aplicados (nunca um numero fixo escrito no codigo) e cada caminho de falha escreve no log
    /// POR QUE falhou.
    ///
    /// Os pontos de ancoragem e o que NAO deu para determinar estao em
    /// <c>docs/RSTV-ANALISE.md</c> (na raiz do repositorio).
    /// </summary>
    [BepInPlugin(Guid, "Roguelike Skill Tree Visualizer", Version)]
    public class Plugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.roguelikeskilltreevisualizer";
        public const string Version = "0.2.0";

        internal static ManualLogSource Log { get; private set; }

        /// <summary>
        /// Opcao de config para DESLIGAR o botao. O padrao e <c>true</c> = o comportamento de
        /// sempre: quem nao abrir o arquivo de config nao ve diferenca nenhuma.
        /// Arquivo: <c>BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg</c>.
        /// </summary>
        internal static ConfigEntry<bool> AtivarBotao { get; private set; }

        /// <summary>
        /// RSTV-5: opcao de config PROPRIA do botao que aparece DURANTE A RUN, ao lado do botao de
        /// apontar o hex (Ping Button) do HUD. Padrao <c>true</c> (ligado). Desligar aqui NAO desliga
        /// o botao da tela Select Party e vice-versa. O PORTAO DE SEGURANCA
        /// (<c>RunTargets.GateOk</c>) continua valendo mesmo com a opcao ligada: em estado de risco o
        /// botao fica escondido e o log diz por que.
        /// </summary>
        internal static ConfigEntry<bool> AtivarBotaoNaRun { get; private set; }

        /// <summary>
        /// RSTV-5: ajusta o indice de irmao da janela nativa para a arvore ficar POR CIMA do HUD na
        /// run (a janela e outro ramo da hierarquia do canvas). Desligar deixa a arvore no indice em
        /// que o prefab a posicionou — util se o tooltip do jogo aparecer atras da arvore.
        /// </summary>
        internal static ConfigEntry<bool> AjustarZOrderConfig { get; private set; }

        /// <summary>
        /// Forma SEGURA de consultar a opcao: se por algum motivo o config nao pode ser lido/criado,
        /// o mod continua com o comportamento de sempre (botao ligado) em vez de morrer no boot.
        /// </summary>
        internal static bool BotaoLigado
        {
            get { return AtivarBotao == null || AtivarBotao.Value; }
        }

        /// <summary>Mesma regra para o botao da run: config ilegivel = botao LIGADO (com o portao 4).</summary>
        internal static bool RunBotaoLigado
        {
            get { return AtivarBotaoNaRun == null || AtivarBotaoNaRun.Value; }
        }

        internal static bool AjustarZOrder
        {
            get { return AjustarZOrderConfig == null || AjustarZOrderConfig.Value; }
        }

        private void Awake()
        {
            Log = Logger;

            try
            {
                AtivarBotao = Config.Bind(
                    "Geral",
                    "AtivarBotao",
                    true,
                    "Injeta o botao 'Skills' na tela Select Party do modo Roguelike. Padrao: true. " +
                    "Com false o mod carrega e registra os ganchos, mas nao cria botao nenhum na tela.");

                AtivarBotaoNaRun = Config.Bind(
                    "Geral",
                    "AtivarBotaoNaRun",
                    true,
                    "Injeta o botao 'Skills' no HUD DURANTE A RUN (ao lado do Ping Button, o botao de " +
                    "apontar o hex). Padrao: true. Com false o mod nao cria esse botao. ATENCAO: o " +
                    "portao de seguranca (RunTargets.GateOk) vale mesmo com true — em mira de skill, " +
                    "turno do inimigo, personagem agindo/movendo, level-up pendente ou GUIState fora de " +
                    "InBattle/InWorldMap/InTown o botao fica escondido e o log diz por que.");

                AjustarZOrderConfig = Config.Bind(
                    "Geral",
                    "AjustarZOrder",
                    true,
                    "Ajusta o indice de irmao da janela nativa para a arvore ficar POR CIMA do HUD na " +
                    "run. Padrao: true. Desligue se o tooltip do jogo aparecer atras da arvore.");
            }
            catch (Exception e)
            {
                Log.LogError("RSTV: falha ao ler/criar o arquivo de config — seguindo com o padrao " +
                             "(botoes LIGADOS): " + e.Message);
            }

            // Marcador de vida: se esta linha nao aparecer no LogOutput.log, o plugin nem carregou.
            Log.LogInfo("Roguelike Skill Tree Visualizer " + Version +
                        " carregado (RSTV-5: botao na tela Select Party + botao no HUD da run, " +
                        "ancorado no Ping Button, skill tree read-only).");

            AplicarPatches();

            Log.LogInfo("RSTV DIAG: botao 'Skills' da tela Select Party " + (BotaoLigado ? "HABILITADO" : "DESABILITADO") +
                        " nesta sessao (AtivarBotao=" + BotaoLigado + " no config); botao 'Skills' do HUD da run " +
                        (RunBotaoLigado ? "HABILITADO" : "DESABILITADO") +
                        " (AtivarBotaoNaRun=" + RunBotaoLigado + "); portao 4 sempre ativo no botao da run.");
        }

        /// <summary>
        /// Aplica os ganchos UM A UM, em vez de <c>PatchAll()</c>.
        ///
        /// <c>PatchAll()</c> e tudo-ou-nada: se um gancho so falhasse (tipo ou assinatura que mudou
        /// numa versao do jogo), os outros seis nao seriam aplicados e o mod morreria em silencio —
        /// o pior cenario aqui. Com o laco abaixo, o gancho que falha fica escrito no log com o
        /// nome dele e o resto continua funcionando.
        ///
        /// O resumo usa a contagem REAL (quantos ganchos de quantos, e quantos metodos do jogo
        /// casaram), nunca um numero fixo: e por ele que se descobre, lendo o log, que um gancho
        /// nao entrou.
        /// </summary>
        private static void AplicarPatches()
        {
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
                Log.LogError("RSTV: nao deu para listar os tipos do mod — nenhum gancho aplicado: " + e);
                return;
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
                    Log.LogInfo("RSTV: gancho aplicado — " + tipo.Name + " (" + quantos +
                                " metodo(s) do jogo).");
                }
                catch (Exception e)
                {
                    falhas.Add(tipo.Name);
                    Log.LogError("RSTV: FALHA ao aplicar o gancho " + tipo.Name + " — " + e.Message);
                }
            }

            string resumo = "RSTV: patches Harmony aplicados (" + ganchosOk + "/" + ganchosTotal +
                            " ganchos, " + metodosOk + " metodos do jogo).";

            if (falhas.Count == 0)
            {
                Log.LogInfo(resumo);
                return;
            }

            Log.LogError(resumo + " GANCHOS QUE FALHARAM: " + string.Join(", ", falhas.ToArray()) +
                         ". O mod continua de pe, mas o recurso que dependia deles nao existe nesta sessao.");
        }

        /// <summary>
        /// Classe de gancho = tem <c>[HarmonyPatch]</c> no tipo E pelo menos um metodo com
        /// <c>[HarmonyPrefix]</c>/<c>[HarmonyPostfix]</c>. A segunda condicao evita tentar
        /// "patchar" uma classe que carrega o atributo sem ser um gancho de verdade.
        /// </summary>
        private static bool EhClasseDeGancho(Type tipo)
        {
            try
            {
                if (tipo == null || !tipo.IsClass)
                {
                    return false;
                }

                if (tipo.GetCustomAttributes(typeof(HarmonyPatch), false).Length == 0)
                {
                    return false;
                }

                MethodInfo[] metodos = tipo.GetMethods(
                    BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);

                for (int i = 0; i < metodos.Length; i++)
                {
                    MethodInfo metodo = metodos[i];
                    if (metodo.GetCustomAttributes(typeof(HarmonyPrefix), false).Length > 0 ||
                        metodo.GetCustomAttributes(typeof(HarmonyPostfix), false).Length > 0)
                    {
                        return true;
                    }
                }

                return false;
            }
            catch (Exception)
            {
                // atributo com tipo que nao resolve (versao de jogo diferente): nao e gancho nosso
                return false;
            }
        }
    }
}
