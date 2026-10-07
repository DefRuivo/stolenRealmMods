using System;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RoguelikeSkillTreeVisualizer (RSTV) — abre a Skill Tree NATIVA do jogo
    /// (<c>SkillTreeManager</c>, l.177201 — a mesma do Campaign -> Change Skills) em modo SOMENTE
    /// LEITURA, com o contexto real do personagem. Nenhum ponto e gasto, nada e gravado.
    ///
    /// Superficies (botoes 'Skills') que existem:
    ///   - o HUD DA RUN (RSTV-5), ancorado no Ping Button — <c>RunButton</c>;
    ///   - o CABECALHO do modal "Remove Skill Trees" (RSTV-20) — <c>RemovalWindowSkillsButton</c>;
    ///   - o ATALHO de teclado (RSTV-11a) — <c>SkillTreeShortcut</c>.
    ///
    /// HISTORICO: ate a RSTV-29 havia tambem um botao na tela Select Party, injetado ao lado do
    /// "Choose Powerups" (`CharacterChoiceManager.roguelikePowerupButton`, l.328521). Em 06/10 o
    /// dono decidiu REMOVER aquela superficie (nao era confiavel e o botao do modal ja a atende);
    /// o <c>SelectPartyButton</c> foi apagado e os ganchos daquela tela sumiram (ver `Patches.cs`).
    ///
    /// Pecas do mod:
    ///   - <c>RunButton</c>          — RSTV-5: o botao no HUD DA RUN, ancorado no Ping Button;
    ///   - <c>RemovalWindowSkillsButton</c> — RSTV-20: o botao do cabecalho do modal;
    ///   - <c>RunTargets</c>         — RSTV-5: alvo do clique na run + PORTAO DE SEGURANCA (estado do jogo);
    ///   - <c>PartyTargets</c>       — ordem de adicao local, usada pelo atalho na tela Select Party;
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
        public const string Version = "0.3.3";

        internal static ManualLogSource Log { get; private set; }

        /// <summary>
        /// RSTV-29: CHAVE-MESTRA dos botoes 'Skills' que RESTAM — o do HUD da run, o da janela de
        /// LEVEL-UP e o do modal "Remove Skill Trees" (a tela Select Party nao tem mais botao). Com
        /// <c>false</c> NENHUM deles e' injetado; as chaves especificas
        /// (<c>AtivarBotaoNaRun</c>/<c>AtivarBotaoNaRemocao</c>) continuam valendo por superficie.
        /// Padrao <c>true</c> = o comportamento de sempre: quem nao abrir o arquivo de config nao ve
        /// diferenca nenhuma.
        ///
        /// RSTV-29F (achado A da RSTV-29R): a decisao e' MANTER a chave-mestra (nao separar) e deixar
        /// o ALCANCE explicito. Antes da RSTV-29 esta chave controlava SO' o botao da tela Select
        /// Party; hoje o MESMO nome desliga tambem o HUD da run, o botao da janela de level-up e o
        /// modal — logo quem ja tinha <c>false</c> no arquivo (para tirar so' o botao da tela de
        /// party) perde os outros. O perfil do dono usa <c>true</c>, entao isso nao o afeta hoje. O
        /// alcance fica escrito na descricao do config (abaixo) e nos docs.
        /// Arquivo: <c>BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg</c>.
        /// </summary>
        internal static ConfigEntry<bool> AtivarBotao { get; private set; }

        /// <summary>
        /// RSTV-5: opcao de config PROPRIA do botao que aparece DURANTE A RUN, ao lado do botao de
        /// apontar o hex (Ping Button) do HUD. Padrao <c>true</c> (ligado). Desligar aqui desliga SO'
        /// o botao da run; a chave-mestra <c>AtivarBotao</c> e a do modal sao independentes (o botao
        /// so' aparece com ESTA chave E a mestra ligadas). O PORTAO DE SEGURANCA
        /// (<c>RunTargets.GateOk</c>) continua valendo mesmo com a opcao ligada: em estado de risco o
        /// botao fica escondido e o log diz por que.
        /// </summary>
        internal static ConfigEntry<bool> AtivarBotaoNaRun { get; private set; }

        /// <summary>
        /// RSTV-11a: liga/desliga o ATALHO de teclado (proposta D) que abre a MESMA skill tree
        /// read-only, sem depender do botao do HUD. Padrao <c>true</c> (ligado). Desligar aqui nao
        /// mexe nos botoes (o HUD da run e o modal seguem com o comportamento de sempre).
        /// </summary>
        internal static ConfigEntry<bool> AtalhoSkillTree { get; private set; }

        /// <summary>
        /// RSTV-11a: a TECLA do atalho. Padrao <c>KeyCode.F10</c>. A tecla e lida CRUA
        /// (<c>Input.GetKeyDown</c>), entao NAO passa pela acao 10 nativa do jogo (que abriria junto
        /// a janela vanilla <c>ToggleSkillTreeMenu</c>). Aceita qualquer <c>KeyCode</c> do Unity
        /// (ex.: F9, K, Mouse4).
        /// </summary>
        internal static ConfigEntry<KeyCode> TeclaAtalhoSkillTree { get; private set; }

        /// <summary>
        /// RSTV-20: opcao de config PROPRIA do botao no CABECALHO do modal "Remove Skill Trees".
        /// Padrao <c>true</c> (ligado). Desligar aqui nao mexe nos outros botoes.
        /// </summary>
        internal static ConfigEntry<bool> AtivarBotaoNaRemocao { get; private set; }

        /// <summary>
        /// Forma SEGURA de consultar a chave-mestra: se por algum motivo o config nao pode ser
        /// lido/criado, o mod continua com o comportamento de sempre (botoes ligados) em vez de
        /// morrer no boot.
        /// </summary>
        internal static bool BotaoLigado
        {
            get { return AtivarBotao == null || AtivarBotao.Value; }
        }

        /// <summary>Botao da run: a chave-mestra E a da run; config ilegivel = LIGADO (com o portao 4).</summary>
        internal static bool RunBotaoLigado
        {
            get { return BotaoLigado && (AtivarBotaoNaRun == null || AtivarBotaoNaRun.Value); }
        }

        /// <summary>Mesma regra para o atalho: config ilegivel = atalho LIGADO (com os guards do jogo).</summary>
        internal static bool AtalhoLigado
        {
            get { return AtalhoSkillTree == null || AtalhoSkillTree.Value; }
        }

        /// <summary>Botao do modal "Remove Skill Trees": chave-mestra E a do modal; ilegivel = LIGADO.</summary>
        internal static bool RemocaoBotaoLigado
        {
            get { return BotaoLigado && (AtivarBotaoNaRemocao == null || AtivarBotaoNaRemocao.Value); }
        }

        /// <summary>
        /// RSTV-29F (achado B da RSTV-29R): POR QUE o botao da run esta desligado, nomeando a chave que
        /// de fato o desligou. Com a chave-mestra <c>false</c> a especifica pode estar <c>true</c>, e o
        /// log NAO pode mentir dizendo "AtivarBotaoNaRun=false". Cobre o HUD da run E o botao da janela
        /// de level-up (os dois consomem <c>RunBotaoLigado</c>).
        /// </summary>
        internal static string MotivoDoBotaoDaRunDesligado
        {
            get
            {
                if (!BotaoLigado)
                {
                    return "AtivarBotao=false no arquivo de config (chave-mestra: desliga o botao da " +
                           "run, o da janela de level-up e o do modal)";
                }

                return "AtivarBotaoNaRun=false no arquivo de config";
            }
        }

        /// <summary>
        /// RSTV-29F (achado B): idem para o botao do modal — com a mestra <c>false</c> o motivo passa a
        /// nomear <c>AtivarBotao</c>, nunca a especifica que continua <c>true</c>.
        /// </summary>
        internal static string MotivoDoBotaoDoModalDesligado
        {
            get
            {
                if (!BotaoLigado)
                {
                    return "AtivarBotao=false no arquivo de config (chave-mestra: desliga o botao da " +
                           "run, o da janela de level-up e o do modal)";
                }

                return "AtivarBotaoNaRemocao=false no arquivo de config";
            }
        }

        /// <summary>A tecla do atalho; sem config, o padrao do mod e <c>KeyCode.F10</c>.</summary>
        internal static KeyCode TeclaAtalho
        {
            get { return TeclaAtalhoSkillTree != null ? TeclaAtalhoSkillTree.Value : KeyCode.F10; }
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
                    "CHAVE-MESTRA dos botoes 'Skills' que restam (RSTV-29): o do HUD da run, o da " +
                    "janela de LEVEL-UP e o do modal 'Remove Skill Trees'. Padrao: true. Com false o " +
                    "mod carrega e registra os ganchos, mas NAO cria botao nenhum em lugar nenhum — " +
                    "desliga o HUD da run, o botao da janela de level-up E o modal de uma vez (para " +
                    "desligar so' uma superficie use a chave especifica dela). A tela Select Party " +
                    "nao tem mais botao (a superficie foi removida).");

                AtivarBotaoNaRun = Config.Bind(
                    "Geral",
                    "AtivarBotaoNaRun",
                    true,
                    "Injeta o botao 'Skills' no HUD DURANTE A RUN, na BARRA DE BAIXO — na mesma " +
                    "linha dos botoes nativos de inventario e de skills, no vao livre medido antes do " +
                    "controle que rotaciona a barra de skills (RSTV-30). Padrao: true. Com false (ou " +
                    "com a chave-mestra AtivarBotao=false) o mod nao cria esse botao. ATENCAO: o " +
                    "portao da run (RunTargets.GateOk) vale mesmo com true — em mira de hex ou de " +
                    "skill, com uma janela de UI aberta ou no posicionamento inicial da batalha o " +
                    "botao fica SEM CLIQUE (continua visivel, na barra) e o log diz por que.");

                AtalhoSkillTree = Config.Bind(
                    "Geral",
                    "AtalhoSkillTree",
                    true,
                    "Liga o atalho de TECLADO que abre a mesma skill tree read-only (sem depender do " +
                    "botao do HUD). Padrao: true. A tecla nao dispara durante chat, remap de tecla, " +
                    "janela de evento ou menu sem alvo: os guards do KeybindManager.Update sao " +
                    "replicados no mod.");

                TeclaAtalhoSkillTree = Config.Bind(
                    "Geral",
                    "TeclaAtalhoSkillTree",
                    KeyCode.F10,
                    "A tecla do atalho da skill tree. Padrao: F10. Aceita qualquer KeyCode do Unity " +
                    "(F9, K, Mouse4, ...). Nao usa a acao 10 nativa, entao NAO abre a janela vanilla " +
                    "de skill tree junto.");

                AtivarBotaoNaRemocao = Config.Bind(
                    "Geral",
                    "AtivarBotaoNaRemocao",
                    true,
                    "Injeta o botao 'Skills' no CABECALHO do modal 'Remove Skill Trees' (canto superior " +
                    "direito do titulo), que abre a arvore read-only do personagem do proprio modal. " +
                    "Padrao: true. Com false (ou com a chave-mestra AtivarBotao=false) o mod nao cria " +
                    "esse botao.");
            }
            catch (Exception e)
            {
                Log.LogError("RSTV: falha ao ler/criar o arquivo de config — seguindo com o padrao " +
                             "(botoes LIGADOS): " + e.Message);
            }

            // Marcador de vida: se esta linha nao aparecer no LogOutput.log, o plugin nem carregou.
            Log.LogInfo("Roguelike Skill Tree Visualizer " + Version +
                        " carregado (RSTV-29: botoes 'Skills' no HUD da run e no modal 'Remove Skill " +
                        "Trees', mais o atalho de teclado; a arvore nativa abre em skill tree read-only).");

            AplicarPatches();

            Log.LogInfo("RSTV DIAG: chave-mestra AtivarBotao=" + BotaoLigado + " — botao 'Skills' do HUD " +
                        "da run " + (RunBotaoLigado ? "HABILITADO" : "DESABILITADO") +
                        " (AtivarBotaoNaRun=" + (AtivarBotaoNaRun == null || AtivarBotaoNaRun.Value) + "; RSTV-30: " +
                        "na BARRA DE BAIXO, visivel com o HUD — o portao da run decide so' o CLIQUE); " +
                        "botao 'Skills' do modal 'Remove Skill Trees' " +
                        (RemocaoBotaoLigado ? "HABILITADO" : "DESABILITADO") +
                        " (AtivarBotaoNaRemocao=" + (AtivarBotaoNaRemocao == null || AtivarBotaoNaRemocao.Value) + "); " +
                        "atalho " + (AtalhoLigado ? ("LIGADO na tecla " + TeclaAtalho) : "DESABILITADO") +
                        " (RSTV-11a: guards do KeybindManager replicados; sem acao nativa).");
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
