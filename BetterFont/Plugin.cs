using System;
using System.Collections.Generic;
using System.Reflection;
using BepInEx;
using BepInEx.Configuration;
using BepInEx.Logging;
using HarmonyLib;
using TMPro;
using UnityEngine;

namespace BetterFont
{
    /// <summary>
    /// BetterFont — troca a fonte padrão do jogo por uma serifada (Times New Roman, com
    /// fallback Georgia / Liberation Serif), aplicada a TODOS os textos TMP, inclusive telas
    /// que abrem depois. A fonte original do jogo entra como fallback do asset serifado, então
    /// ícones/símbolos que a Times não tem continuam renderizando (sem quadradinhos).
    ///
    /// BF-ESTILO (1.0.1) — o defeito da 1.0.0 e o conserto: em TextMeshPro, atribuir
    /// TMP_Text.font NÃO troca só o tipo de letra. O setter chama LoadFontAsset(), e o
    /// LoadFontAsset do TMP DESCARTA o material em uso e passa a usar o material do asset novo
    /// (IL confirmado: TextMeshProUGUI.LoadFontAsset -> m_sharedMaterial = m_fontAsset.material).
    /// Como cor de face, contorno e sombra do jogo vivem NO MATERIAL, a troca de fonte apagava
    /// o estilo — o defeito relatado ("quebra o estilo e a coloração durante o combate").
    /// Conserto: as propriedades de estilo do material ANTIGO são transportadas para o material
    /// POR COMPONENTE da fonte nova (t.fontMaterial = instância; o compartilhado nunca é escrito).
    ///
    /// BF-1 (conserto NA CAUSA, genérico e sem acoplar mod nenhum) — o que faltava: quem tem
    /// material PRÓPRIO (o jogo em combate/títulos, e QUALQUER mod que tenha aplicado efeito
    /// naquele texto antes) era PULADO, e ficava na fonte original enquanto o resto da interface
    /// mudava — a interface inconsistente relatada pelo dono. A decisão de pular partia de um
    /// medo conservador (trocar a fonte apagaria o efeito do outro mod), e o medo era justo
    /// ANTES da cópia existir. Agora o mod faz o que interessa: TROCA a fonte e REAPLICA no
    /// material novo os efeitos que já estavam no material anterior daquele texto (contorno,
    /// sombra/underlay, cor de face e as keywords que os ligam). Nada aqui cita ou conhece outro
    /// mod: a regra é só "o que estava no material anterior daquele texto, continua lá".
    /// Reversível por config: PularTextosEstilizados = true restaura o comportamento antigo
    /// (texto com material próprio fica 100% intocado) e, quando o efeito em uso NÃO pode ser
    /// reproduzido com fidelidade (textura de face, bevel, glow), o texto NÃO é tocado —
    /// falha-segura: em dúvida, nada pior que hoje. SEM alteração de gameplay.
    ///
    /// BF-2 (1.0.2) — o BF-1 RECUSAVA exatamente o caso que ele existe para consertar. O que
    /// faltava, em ordem:
    ///   1. TRANSPORTE ENTRE VARIANTES DE SHADER. As propriedades de estilo vivem nas DUAS
    ///      variantes de SDF do TMP (a fonte serifada sai com 'TextMeshPro/Mobile/Distance
    ///      Field', via ShaderUtilities.ShaderRef_MobileSDF, e os alvos de combate do jogo usam
    ///      'TextMeshPro/Distance Field Overlay' e '(Surface)'); o que muda é a VARIANTE, não o
    ///      conjunto de propriedades. O BF-1 tratava shader diferente como recusa — e os textos
    ///      de combate ficavam na fonte original. Agora a variante diferente é cópia
    ///      BEST-EFFORT, propriedade por propriedade com HasProperty (o padrão do arquivo), e o
    ///      que a variante nova não expuser entra no log como "não transportado".
    ///   2. ORDEM DA FALHA-SEGURA: a fonte e o estilo daquele texto são mexidos JUNTOS e
    ///      revertidos juntos — nenhuma exceção deixa "fonte trocada com estilo parcial".
    ///   3. BURACOS DE PROPRIEDADE fechados: UNDERLAY_INNER, MASK_SOFT/HARD/TEX + _ClipRect,
    ///      _MaskSoftnessX/Y, _VertexOffsetX/Y são transportados; _WeightNormal/_WeightBold são
    ///      REGISTRADOS no log (são parâmetro da fonte/atlas, não do efeito — quem manda é a
    ///      fonte nova); nada fica em branco.
    ///   4. O PORTÃO olha o EFEITO PRESENTE no material, não a classificação do texto: texto
    ///      NÃO classificado como estilizado cuja fonte traz _FaceTex/bevel/glow também fica
    ///      intocado (com o motivo nomeado), e o portão não é pulado pelo PreservarEstilo.
    ///   5. A doc dizia que ".cfg ausente volta ao conservador" — falso: chave ausente apenas
    ///      cria a entrada com o default do Bind (false) e usa o caminho novo. Corrigido aqui,
    ///      no README e no CHANGELOG.
    /// </summary>
    [BepInPlugin("com.gumatos.betterfont", "Better Font", "1.0.2")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource Log { get; private set; }

        /// <summary>BF-ESTILO: transporta cor/contorno/sombra do material antigo para o novo.</summary>
        internal static ConfigEntry<bool> PreservarEstilo { get; private set; }

        /// <summary>BF-ESTILO: não troca a fonte de quem tem material próprio (estilo intocado).</summary>
        internal static ConfigEntry<bool> PularTextosEstilizados { get; private set; }

        /// <summary>BF-ESTILO: log por texto (objeto, fonte, material, shader, o que foi copiado).</summary>
        internal static ConfigEntry<bool> LogDiagnosticoEstilo { get; private set; }

        /// <summary>
        /// Getters SEGUROS das opcoes: se o config nao pudo ser lido/criado (ver <c>BindSeguro</c>),
        /// a entrada fica null e o mod continua com um valor FIXO em vez de estourar NullReference
        /// a cada texto da tela. Mesmo padrao do RSTV (<c>Plugin.BotaoLigado</c>).
        ///
        /// ATENCAO (BF-2, doc que estava FALSA): o valor fixo NAO e "o default do Bind" em todos
        /// os casos. Em <c>PularTextosEstilizados</c> o default do Bind e <c>false</c> (caminho
        /// novo, a fonte e trocada) e aqui, sem entrada, o valor e <c>true</c> (ESCAPE — o texto
        /// estilizado fica intocado). Ou seja: falha de config cai no CONSERVADOR, que e escolha
        /// deste getter, nao o default da chave. E chave/arquivo AUSENTE nao e falha de config:
        /// o BepInEx cria a entrada com o default do Bind (<c>false</c>) e o caminho novo vale —
        /// conferido no <c>ConfigFile.Bind</c> do BepInEx 5.4.23 (chave inexistente = ConfigEntry
        /// novo com o defaultValue; so o tipo nao suportado levanta excecao e cai no <c>BindSeguro</c>).
        /// </summary>
        internal static bool PreservarEstiloLigado
        {
            get { return PreservarEstilo == null || PreservarEstilo.Value; }
        }

        /// <summary>BF-ESTILO/BF-1: ESCAPE do comportamento antigo. Default do Bind:
        /// <c>false</c> (a fonte e trocada e os efeitos do material anterior sao preservados).
        /// Sem entrada (falha ao ler/criar o config) vale <c>true</c> — o CONSERVADOR.</summary>
        internal static bool PularEstilizadosLigado
        {
            get { return PularTextosEstilizados == null || PularTextosEstilizados.Value; }
        }

        /// <summary>Padrao <c>false</c> (sem log de diagnostico por texto).</summary>
        internal static bool LogDiagnosticoLigado
        {
            get { return LogDiagnosticoEstilo != null && LogDiagnosticoEstilo.Value; }
        }

        private void Awake()
        {
            Log = Logger;

            // Config: cada Bind passa por BindSeguro. Arquivo ausente/corrompido, ou chave com tipo
            // invalido, NAO pode derrubar o mod nem impedir o jogo de carregar — em falha vale o
            // DEFAULT de cada opcao (pelos getters seguros abaixo) e o erro fica no log.
            //
            // BF-ESTILO: PreservarEstilo transporta o estilo do material ANTIGO para o material
            // POR COMPONENTE da fonte nova (é o conserto do defeito: atribuir .font troca o material).
            PreservarEstilo = BindSeguro("Estilo", "PreservarEstilo", true,
                "true = antes de trocar a fonte, copia as propriedades de ESTILO do material que o texto ja usava " +
                "(cor de face _FaceColor, contorno _OutlineWidth/_OutlineSoftness/_OutlineColor, sombra _UnderlayColor/" +
                "_UnderlayOffsetX/_UnderlayOffsetY/_UnderlayDilate/_UnderlaySoftness, _FaceDilate) para o material " +
                "POR COMPONENTE da fonte nova (t.fontMaterial -- nunca o material compartilhado), e liga as keywords " +
                "OUTLINE_ON/UNDERLAY_ON que estavam ativas. Em TextMeshPro trocar 'font' troca o MATERIAL junto, e o " +
                "estilo do jogo vive no material. false = troca a fonte deixando o material novo como veio " +
                "(comportamento da 1.0.0, que apagava cor/contorno/sombra).");

            // BF-1: ESCAPE do comportamento antigo (1.0.1). Default FALSE: a fonte é trocada e os
            // efeitos que já estavam no material daquele texto são reaplicados no material novo —
            // é o que faz o texto estilizado por OUTRO mod (ou pelo próprio jogo) receber a
            // serifa SEM perder contorno/sombra. Quem preferir o comportamento antigo (texto com
            // material próprio fica 100% intocado, sem serifa) liga esta chave.
            PularTextosEstilizados = BindSeguro("Estilo", "PularTextosEstilizados", false,
                "false (padrao) = troca a fonte TAMBEM dos textos cujo material e estilizado (material proprio, " +
                "diferente do material padrao da fonte daquele componente, ou de uma VARIANTE de shader diferente " +
                "do material da fonte serifada) e REAPLICA neles os efeitos de material que ja estavam ali (cor de " +
                "face, contorno _OutlineWidth/_OutlineSoftness/_OutlineColor, sombra _UnderlayColor/_UnderlayOffsetX/Y/" +
                "_UnderlayDilate/_UnderlaySoftness/UNDERLAY_INNER, recorte _ClipRect, offsets _VertexOffsetX/Y e as " +
                "keywords OUTLINE_ON/UNDERLAY_ON, propriedade por propriedade com HasProperty), copiando para o " +
                "material POR COMPONENTE da fonte nova. Variante de shader diferente NAO e recusa: e o caso dos " +
                "textos de combate do jogo (fonte serifada = 'Mobile/Distance Field'; os alvos de combate usam " +
                "'Distance Field Overlay'/'Distance Field (Surface)') e as propriedades de estilo existem nas duas. " +
                "E o que faz QUALQUER mod que tenha aplicado efeito antes continuar funcionando. O texto so NAO e " +
                "tocado quando o material em uso traz um efeito que a copia nao reproduz (textura de face _FaceTex, " +
                "bevel _BumpMap, GLOW_ON/BEVEL_ON) - e ai o motivo sai NOMEADO no log. " +
                "true = ESCAPE, comportamento antigo da 1.0.1: NAO troca a fonte de quem tem material estilizado " +
                "(o visual original fica 100% intacto, so nao ganha a serifa). Sem entrada no config (falha ao " +
                "ler/criar), o getter seguro vale true - o CONSERVADOR; chave ausente no .cfg NAO cai aqui (o " +
                "BepInEx cria a entrada com este default false). Para ver o que foi pulado, ligue LogDiagnosticoEstilo.");

            LogDiagnosticoEstilo = BindSeguro("Diagnostico", "LogDiagnosticoEstilo", false,
                "true = loga um bloco por texto tratado: objeto, fonte, material compartilhado, shader, quais " +
                "propriedades de estilo foram copiadas e quais existiam na origem mas NAO podem ser transportadas " +
                "(ex.: _FaceTex, GLOW_ON, _GradientScale do atlas). Serve para conferir um texto especifico e para " +
                "saber se algo ainda ficou diferente do original. Padrao: false (sem spam no log).");

            Logger.LogInfo(
                $"Better Font carregado (v{Info.Metadata.Version}): preservar estilo={PreservarEstiloLigado}, " +
                $"pular textos estilizados={PularEstilizadosLigado}, diagnostico={LogDiagnosticoLigado}.");

            // NÃO criar o updater aqui! Este Awake roda durante o chainloader do BepInEx, ANTES
            // de existir cena — a Unity DESTRÓI na primeira carga de cena qualquer GameObject
            // criado ali (mesma causa raiz do HUD do RoguelikeQoL, confirmada 29/09), e o updater
            // nunca chegava a receber Update. A criação é PREGUIÇOSA: no primeiro Localize da UI.
            AplicarPatches();

            Logger.LogInfo("Better Font: o updater sera criado de forma PREGUICOSA no primeiro " +
                           "OptionsManager.Localize da UI (nunca no Awake: a Unity destroi GameObject " +
                           "criado durante o chainloader do BepInEx).");
        }

        /// <summary>
        /// <c>Config.Bind</c> com guarda: arquivo de config ausente/corrompido (ou chave com tipo
        /// invalido) nao pode derrubar o mod nem impedir o jogo de carregar. Em falha devolve null e
        /// o getter seguro correspondente passa a valer o DEFAULT — o mesmo comportamento de quem
        /// nao tem arquivo de config nenhum. Mesmo padrao dos outros mods do projeto (getter seguro
        /// no lugar da leitura direta).
        /// </summary>
        private ConfigEntry<T> BindSeguro<T>(string secao, string chave, T padrao, string descricao)
        {
            try
            {
                return Config.Bind(secao, chave, padrao, descricao);
            }
            catch (Exception e)
            {
                Log.LogError("Better Font: falha ao ler/criar a chave '" + chave + "' do config — usando o " +
                             "padrao (" + padrao + "): " + e.Message);
                return null;
            }
        }

        /// <summary>
        /// Aplica os ganchos UM A UM, em vez de <c>PatchAll()</c>.
        ///
        /// <c>PatchAll()</c> e tudo-ou-nada: um gancho so que falhasse (tipo ou assinatura que mudou
        /// numa versao do jogo) deixaria TODOS os outros sem aplicar — e em silencio. Com o laco
        /// abaixo, o gancho que falha fica escrito no log com o nome dele e o resto continua
        /// funcionando. O resumo usa a contagem REAL (quantos ganchos de quantos, e quantos metodos
        /// do jogo casaram), nunca um numero fixo: e por ele que se descobre, lendo o log, que um
        /// gancho nao entrou. Mesmo modelo do RoguelikeSkillTreeVisualizer.
        /// </summary>
        private static void AplicarPatches()
        {
            var harmony = new Harmony("com.gumatos.betterfont");
            var falhas = new List<string>();
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
                Log.LogError("Better Font: nao deu para listar os tipos do mod — nenhum gancho aplicado: " + e);
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
                    Log.LogInfo("Better Font: gancho aplicado — " + tipo.Name + " (" + quantos +
                                " metodo(s) do jogo).");
                }
                catch (Exception e)
                {
                    falhas.Add(tipo.Name);
                    Log.LogError("Better Font: FALHA ao aplicar o gancho " + tipo.Name + " — " + e.Message);
                }
            }

            string resumo = "Better Font: patches Harmony aplicados (" + ganchosOk + "/" + ganchosTotal +
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
        /// Classe de gancho = tem <c>[HarmonyPatch]</c> no TIPO (declarado, não herdado) — a MESMA
        /// condição que o <c>PatchAll()</c> exigia para processar a classe.
        ///
        /// AQUI NÃO SE EXIGE <c>[HarmonyPrefix]</c>/<c>[HarmonyPostfix]</c> NO MÉTODO: os ganchos
        /// deste mod são declarados pela CONVENÇÃO DE NOME do Harmony (método chamado <c>Postfix</c>,
        /// ver <c>LocalizeFontTrigger</c>), que o Harmony aceita exatamente como aceita o atributo —
        /// os nomes são <c>Prefix</c>/<c>Postfix</c>/<c>Transpiler</c>/<c>Finalizer</c>. Exigir o
        /// atributo PULA os ganchos deste mod: o mod carrega, loga "carregado." e não aplica nada —
        /// o silêncio parecendo sucesso. Uma classe com <c>[HarmonyPatch]</c> e sem método de patch
        /// apenas não registra nada (<c>Patch()</c> devolve lista vazia), sem efeito colateral — é o
        /// mesmo conjunto que o <c>PatchAll()</c> processaria. Mesmo filtro do BetterTooltips.
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

    /// <summary>
    /// Gatilho da fonte: a cada localização de texto (o funil Localize roda em TODA renderização
    /// de UI), garante que o updater exista e pede uma varredura de fonte com throttle. Assim a
    /// fonte aplica assim que qualquer tela renderiza — sem depender de Update/foco/timeScale.
    /// </summary>
    [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
    public static class LocalizeFontTrigger
    {
        private static void Postfix()
        {
            try
            {
                FontUpdater.Ensure();
            }
            catch
            {
                // nunca quebrar a localização por causa da fonte
            }
        }
    }

    /// <summary>
    /// MonoBehaviour dedicado: roda a varredura de fonte com TEMPO REAL — imune a timeScale=0 e
    /// ao ciclo de vida do plugin. É criado já com a cena viva (ver LocalizeFontTrigger), senão
    /// a Unity o destruiria na primeira carga de cena e o Update nunca rodaria.
    /// </summary>
    public class FontUpdater : MonoBehaviour
    {
        public static FontUpdater Instance { get; private set; }

        private static bool _everDestroyed;

        // Propriedades de ESTILO copiadas do material antigo para o material novo. Só as que
        // existirem nos DOIS lados (HasProperty) são tocadas — variante de shader que não expõe a
        // propriedade nem recebe o Set, e o que não pôde ser transportado vai para o log.
        private static readonly string[] PropsCor =
        {
            "_FaceColor", "_OutlineColor", "_UnderlayColor"
        };

        private static readonly string[] PropsFloat =
        {
            "_FaceDilate",
            "_OutlineWidth", "_OutlineSoftness",
            "_UnderlayOffsetX", "_UnderlayOffsetY", "_UnderlayDilate", "_UnderlaySoftness",
            // BF-2: buracos que a revisão mediu e que passavam em branco.
            "_VertexOffsetX", "_VertexOffsetY",   // deslocamento de vértice do estilo
            "_MaskSoftnessX", "_MaskSoftnessY"    // suavidade do recorte (par de _ClipRect)
        };

        /// <summary>BF-2: propriedades de VETOR transportadas — o recorte do texto mascarado/rolável.</summary>
        private static readonly string[] PropsVetor =
        {
            "_ClipRect"
        };

        /// <summary>
        /// BF-2: keywords de recorte (masking). O TMP liga MASK_SOFT ao mascarar um texto
        /// (TextMeshProUGUI.EnableMasking) e o valor de _ClipRect sai do UpdateMask; sem transportar,
        /// texto dentro de máscara/rolagem perde o recorte ao ganhar material novo. Best-effort: a
        /// keyword só tem efeito se o shader novo a declarar (conferido no próprio jogo: as variantes
        /// 'Distance Field'/'Mobile/Distance Field' deste TMP 3.x declaram UNDERLAY_INNER/GLOW_ON/
        /// BEVEL_ON/OUTLINE_ON/UNDERLAY_ON; MASK_* é de TMP mais novo).
        /// </summary>
        private static readonly string[] KeywordsMascara =
        {
            "MASK_SOFT", "MASK_HARD", "MASK_TEX"
        };

        /// <summary>
        /// BF-2: propriedades de PESO da fonte. NÃO se copiam — são parâmetro do atlas/fonte (como
        /// _GradientScale), quem manda é a fonte NOVA; mas, quando a origem difere do novo, elas são
        /// REGISTRADAS no log. É o que fecha o buraco "não é copiado NEM logado". A prova de que são
        /// da FONTE (e não do efeito): é o próprio `TMP_FontAsset.CreateFontAssetInstance` que as
        /// escreve no material da fonte nova, de `tMP_FontAsset.normalStyle` / `.boldStyle`, junto com
        /// `_MainTex`/`_TextureWidth`/`_TextureHeight`/`_GradientScale` do atlas.
        /// </summary>
        private static readonly string[] PropsDeFonteRegistradas =
        {
            "_WeightNormal", "_WeightBold"
        };

        private float _lastSweep = -99f;
        private TMP_FontAsset _serifFont;
        private readonly HashSet<TMP_Text> _seenTexts = new HashSet<TMP_Text>();
        private readonly HashSet<string> _diagVistos = new HashSet<string>();
        private readonly HashSet<int> _puladosContados = new HashSet<int>();
        private bool _loggedFirstSweep;
        /// <summary>
        /// BF-2: TETO do diagnóstico para a linha de ROTINA — texto cujo material NÃO carrega
        /// efeito nenhum (a UI comum). BF-2R: este teto é POR CENA (ver
        /// <c>OrcamentoDoDiagnosticoPorCena</c>), e é alcançável — na BF-2 ele era inalcançável.
        /// </summary>
        internal const int TetoDiagRotina = 120;

        /// <summary>
        /// TETO das linhas de EFEITO — a que o dono liga o diagnóstico para ler: o texto cujo
        /// MATERIAL carrega contorno/sombra/glow (o caso de combate), o que ficou intocado por o
        /// efeito não ser transportável e o revertido por falha. BF-2R: POR CENA, e a classificação é
        /// explícita (quem chama diz se há efeito no material) — nunca tirada do CONTEÚDO da linha.
        /// </summary>
        internal const int TetoDiagEfeito = 300;

        /// <summary>
        /// BF-3 — TETO PRÓPRIO da linha PULADA PELO ESCAPE (<c>PularTextosEstilizados</c> ligado):
        /// o escape não transportou efeito nenhum, então o pulo não disputa o orçamento de EFEITO.
        /// Com a chave do dono ligada a varredura pula ~484 numa passada (log do dono: 484 e 624 —
        /// <c>tools/fixtures/bf-varredura-em-jogo.log</c>); sem teto próprio o de 300 se esgotava
        /// antes da linha de combate, que nessa config E um pulado.
        /// </summary>
        internal const int TetoDiagEscape = 700;

        /// <summary>
        /// BF-3 — as TRÊS categorias de linha do diagnóstico, ditas por quem chama (nunca tiradas do
        /// CONTEÚDO da linha, que foi o defeito da BF-2):
        ///   <c>Rotina</c>  — o material daquele texto NÃO carrega efeito (a UI comum);
        ///   <c>Efeito</c>  — o material CARREGA efeito (contorno/sombra/glow: o caso de combate);
        ///   <c>Escape</c>  — o texto foi PULADO pelo escape (<c>PularTextosEstilizados</c>): nada foi
        ///                    transportado daquele texto, então a linha dele não é "de efeito" e não
        ///                    disputa o orçamento de efeito.
        /// </summary>
        internal enum TipoLinhaDiag
        {
            Rotina,
            Efeito,
            Escape
        }

        private int _diagLinhas;
        private int _diagLinhasDeEfeito;
        private int _diagLinhasDeEscape;
        // BF-2R: a cena do orçamento de diagnóstico em vigor. Antes os contadores eram da
        // SESSÃO: a varredura de boot vê 400+ textos (medido no log do dono — 406 e 484 numa
        // passada, versionado em tools/fixtures/) e o teto de efeito se esgotava ANTES da cena de
        // combate, que é exatamente o defeito que este conserto fecha.
        private string _diagCena;
        private readonly HashSet<string> _diagCortesAvisados = new HashSet<string>();
        private bool _catalogoDoMaterialNovo;

        /// <summary>Cria o GameObject persistente do updater (idempotente).</summary>
        public static void Create()
        {
            if (Instance != null)
            {
                return;
            }
            var go = new GameObject("BetterFont_Updater");
            DontDestroyOnLoad(go);
            go.AddComponent<FontUpdater>();
        }

        /// <summary>Garante que o updater exista e pede uma varredura (respeitando o throttle).</summary>
        public static void Ensure()
        {
            if (Instance == null)
            {
                if (_everDestroyed)
                {
                    Plugin.Log.LogWarning("Better Font: updater ausente — recriando (a Unity destruiu o anterior).");
                }
                Create();
            }
            Instance?.MaybeSweep();
        }

        private void Awake()
        {
            Instance = this;
            Plugin.Log.LogInfo("Better Font: updater criado.");
            FontSweep(); // primeira passada imediata
        }

        private void Start()
        {
            Plugin.Log.LogInfo("Better Font: Start() do updater chamado (objeto vivo na cena).");
        }

        private void OnDestroy()
        {
            Plugin.Log.LogWarning("Better Font: updater DESTRUÍDO pela Unity.");
            _everDestroyed = true;
            if (Instance == this)
            {
                Instance = null;
            }
        }

        public void MaybeSweep()
        {
            try
            {
                if (Time.realtimeSinceStartup - _lastSweep >= 2f)
                {
                    _lastSweep = Time.realtimeSinceStartup;
                    FontSweep();
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"Better Font erro: {e.Message}\n{e.StackTrace}");
            }
        }

        private void Update()
        {
            // Guarda no PONTO DE CHAMADA (o FontSweep ja tem a guarda interna, mas um Update que
            // lanca excecao a cada frame e classe de bug conhecida neste projeto — o log encheria
            // e o objeto poderia ser desativado pela Unity). Mesmo formato do MaybeSweep.
            try
            {
                if (Time.realtimeSinceStartup - _lastSweep >= 2f)
                {
                    _lastSweep = Time.realtimeSinceStartup;
                    FontSweep();
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"Better Font erro no Update: {e.Message}\n{e.StackTrace}");
            }
        }

        /// <summary>
        /// Aplica a fonte serifada a todos os textos TMP do jogo, incluindo os que surgirem
        /// depois (novas janelas/telas). A fonte original do jogo entra como fallback do asset
        /// serifado, para ícones/símbolos não virarem quadrados.
        ///
        /// BF-ESTILO/BF-1: antes de cada troca, o material EM USO é lido (fontSharedMaterial), e as
        /// propriedades de ESTILO dele são transportadas para o material POR COMPONENTE da fonte
        /// nova (t.fontMaterial) — nunca escrevemos no material compartilhado nem no material do
        /// font asset. Um texto com material PRÓPRIO (o jogo em combate/títulos, ou texto que
        /// QUALQUER mod já estilizou) também troca de fonte: os efeitos que já estavam no material
        /// dele viajam junto. O comportamento antigo (texto estilizado 100% intocado) continua
        /// disponível ligando PularTextosEstilizados.
        ///
        /// BF-2: (a) VARIANTE de shader diferente não é mais recusa — é cópia best-effort
        /// (HasProperty por propriedade), que é o caso dos textos de combate do jogo; (b) o portão
        /// do "não dá para reproduzir" olha o EFEITO PRESENTE no material, não a classificação do
        /// texto; (c) fonte e estilo mudam juntos e são revertidos juntos se algo falhar.
        /// </summary>
        private void FontSweep()
        {
            try
            {
                if (_serifFont == null)
                {
                    _serifFont = CreateSerifFont();
                    if (_serifFont == null)
                    {
                        Plugin.Log.LogWarning("Better Font: nenhuma fonte serifada disponível no SO.");
                        return;
                    }
                    // fallbackFontAssetTable vem null num font asset criado em runtime
                    // (CreateFontAsset) — inicializa antes de usar.
                    if (_serifFont.fallbackFontAssetTable == null)
                    {
                        _serifFont.fallbackFontAssetTable = new List<TMP_FontAsset>();
                    }
                    // BF-2: uma linha, uma vez, com o MATERIAL DA FONTE NOVA e quais propriedades
                    // transportadas ele expõe. É o que prova, no log, que a variante da fonte nova
                    // aceita cada peça do transporte (sem isso a resposta ficaria só no olho de quem
                    // lê o jogo) e fecha a dúvida "por que esta propriedade ficou de fora".
                    CatalogoDoMaterialNovo();
                }

                int convertidos = 0;
                int pulados = 0;
                int naoPreservaveis = 0;
                int revertidos = 0;
                int jaNaSerifa = 0;

                foreach (var t in Resources.FindObjectsOfTypeAll<TMP_Text>())
                {
                    if (t == null)
                    {
                        continue;
                    }

                    RegistrarFallback(t);

                    if (t.font == _serifFont)
                    {
                        jaNaSerifa++;
                        continue;
                    }

                    try
                    {
                        // O material EM USO agora: é ele que carrega a cor/contorno/sombra do jogo
                        // — e também o efeito que outro mod possa ter aplicado NESTE texto.
                        Material antigo = t.fontSharedMaterial;
                        TMP_FontAsset fonteAntiga = t.font;

                        // BF-1: "estilizado" = material próprio (o em uso não é o material padrão da
                        // própria fonte do texto) ou shader diferente do da fonte serifada. É o caso
                        // do material que outro mod clona POR COMPONENTE para aplicar contorno/halo.
                        string motivoEstilo;
                        bool estilizado = EhEstilizado(antigo, fonteAntiga, out motivoEstilo);

                        // BF-3 — O EFEITO DO MATERIAL É LIDO ANTES DO ESCAPE, de proposito: o pulado
                        // pelo escape NAO e linha de efeito (nada foi transportado daquele texto) e
                        // vai para o teto PROPRIO do escape (TetoDiagEscape), nunca para o de EFEITO.
                        // Antes o call site do escape passava `true` fixo: com PularTextosEstilizados
                        // ligado os ~484 pulados de uma varredura consumiam o teto de 300 e a linha
                        // de combate (que nessa config E um pulado) ficava de fora.
                        bool efeitoPresente = TemEfeitoNoMaterial(antigo);

                        if (estilizado && Plugin.PularEstilizadosLigado)
                        {
                            // ESCAPE: comportamento antigo da 1.0.1 — fonte E estilo originais intactos.
                            // Conta/loga o pulo UMA vez por texto (a varredura roda a cada 2s; sem
                            // isto o resumo repetiria para sempre). O texto continua sendo reavaliado
                            // nas passadas seguintes: se o material dele mudar, ele entra na conversão.
                            if (ContarPuloUmaVez(t))
                            {
                                pulados++;
                                Diagnostico("PULADO (escape: material estilizado: " + motivoEstilo + ")", t, fonteAntiga, antigo,
                                    "n/a (texto pulado: fonte e material nao foram tocados)",
                                    "n/a (texto pulado: nada foi transportado)", null, TipoLinhaDiag.Escape);
                            }
                            continue; // o dono pediu o comportamento antigo: nada aqui e tocado
                        }

                        // BF-2 — O PORTÃO OLHA O EFEITO PRESENTE NO MATERIAL, nunca a classificação
                        // do texto nem o PreservarEstilo: qualquer material que carregue um efeito
                        // que a cópia não reproduz (textura de face, bevel, glow) mantém aquele texto
                        // INTACTO, com o motivo NOMEADO no log. Antes o portão só valia para
                        // "estilizado && PreservarEstiloLigado" — o texto NÃO classificado cuja
                        // própria fonte traz _FaceTex/GLOW_ON/BEVEL_ON era trocado e perdia o efeito,
                        // e o PreservarEstilo=false pulava o portão inteiro.
                        // BF-3: `efeitoPresente` já foi lido ACIMA do escape (o pulado pelo escape não
                        // é linha de efeito), então aqui só se usa.
                        string motivoNaoPreservavel = null;
                        if (efeitoPresente &&
                            !EstiloTransportavel(antigo, Plugin.PreservarEstiloLigado, out motivoNaoPreservavel))
                        {
                            if (ContarPuloUmaVez(t))
                            {
                                naoPreservaveis++;
                                Diagnostico("PULADO (efeito do material nao transportavel: " + motivoNaoPreservavel + ")",
                                    t, fonteAntiga, antigo,
                                    "n/a (texto pulado: fonte e material nao foram tocados)",
                                    "n/a (texto pulado: nada foi transportado)", null, TipoLinhaDiag.Efeito);
                            }
                            continue; // efeito intacto: melhor que uma copia incompleta
                        }

                        // BF-2 — ORDEM DA FALHA-SEGURA: a troca de fonte e o transporte de estilo são
                        // UMA operação, revertida INTEIRA se qualquer passo falhar. Antes a fonte era
                        // trocada primeiro e uma exceção na cópia/UpdateMeshPadding deixava o texto com
                        // "fonte trocada e estilo pela metade" — a meia cópia que este conserto diz
                        // evitar. A troca de fonte troca o material junto (LoadFontAsset do TMP); o
                        // efeito do material ANTIGO é reaplicado logo abaixo, no material POR
                        // COMPONENTE daquele texto.
                        string copiados = null;
                        string naoTransportados = null;
                        string registros = null;
                        try
                        {
                            t.font = _serifFont;

                            if (Plugin.PreservarEstiloLigado && antigo != null && UsaMaterialDaFonteNova(t))
                            {
                                // fontMaterial devolve/cria a CÓPIA do material POR COMPONENTE.
                                Material novo = t.fontMaterial;
                                if (novo != null)
                                {
                                    copiados = CopiarEstilo(antigo, novo, out naoTransportados, out registros);
                                    // contorno/sombra saem para FORA do glifo: sem recalcular o
                                    // padding o contorno é cortado na borda do mesh.
                                    t.UpdateMeshPadding();
                                    t.SetVerticesDirty();
                                }
                            }
                        }
                        catch (System.Exception e)
                        {
                            // REVERSÃO: a fonte e o material daquele texto voltam ao que eram. Nenhum
                            // texto fica com a fonte trocada e o estilo pela metade.
                            ReverterTexto(t, fonteAntiga, antigo);
                            if (ContarPuloUmaVez(t))
                            {
                                revertidos++;
                                Diagnostico("REVERTIDO (falha ao trocar a fonte/transportar o estilo — texto devolvido ao " +
                                    "original: " + e.GetType().Name + ": " + e.Message + ")",
                                    t, fonteAntiga, antigo,
                                    "n/a (texto revertido: nada ficou aplicado)",
                                    "n/a (texto revertido: nada foi transportado)", null,
                                    efeitoPresente ? TipoLinhaDiag.Efeito : TipoLinhaDiag.Rotina);
                            }
                            continue;
                        }

                        convertidos++;
                        // BF-2R: "linha de efeito" = o material DESTE texto carregava efeito (o caso de
                        // combate que o diagnóstico existe para conferir) — não "a linha tem conteúdo",
                        // que era o critério quebrado da BF-2 (copiados nunca vem vazio). Sem isto, toda
                        // linha consumia o teto de efeito e o teto de rotina era inalcançável.
                        Diagnostico(efeitoPresente ? "CONVERTIDO (efeito do material anterior transportado)" : "CONVERTIDO",
                            t, fonteAntiga, antigo, copiados, naoTransportados, registros,
                            efeitoPresente ? TipoLinhaDiag.Efeito : TipoLinhaDiag.Rotina);
                    }
                    catch (System.Exception e)
                    {
                        Plugin.Log.LogWarning($"Better Font: falha ao tratar um texto: {e.GetType().Name}: {e.Message}");
                    }
                }

                if (!_loggedFirstSweep)
                {
                    _loggedFirstSweep = true;
                    Plugin.Log.LogInfo($"Better Font: varredura aplicada ({_seenTexts.Count} textos vistos).");
                }

                if (convertidos > 0 || pulados > 0 || naoPreservaveis > 0 || revertidos > 0)
                {
                    Plugin.Log.LogInfo(
                        $"Better Font: varredura — {convertidos} texto(s) convertidos para a serifa" +
                        (Plugin.PreservarEstiloLigado ? " (efeitos do material anterior transportados)" : string.Empty) +
                        $", {pulados} pulado(s) pelo escape (PularTextosEstilizados ligado), " +
                        $"{naoPreservaveis} intocado(s) por efeito nao transportavel, " +
                        $"{revertidos} revertido(s) por falha ao aplicar (nada ficou pela metade), {jaNaSerifa} ja na serifa.");
                }
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning($"Better Font erro: {e.Message}\n{e.StackTrace}");
            }
        }

        /// <summary>
        /// Registra a fonte ORIGINAL do texto como fallback da serifada (uma vez por texto),
        /// para glifos que a Times/Georgia não tem continuarem renderizando.
        /// </summary>
        private void RegistrarFallback(TMP_Text t)
        {
            if (_seenTexts.Contains(t))
            {
                return;
            }
            _seenTexts.Add(t);
            try
            {
                if (_serifFont.fallbackFontAssetTable == null)
                {
                    _serifFont.fallbackFontAssetTable = new List<TMP_FontAsset>();
                }
                if (t.font != null && t.font != _serifFont && !_serifFont.fallbackFontAssetTable.Contains(t.font))
                {
                    _serifFont.fallbackFontAssetTable.Add(t.font);
                }
            }
            catch
            {
                // fallback é melhor-esforço: nunca derruba a varredura
            }
        }

        /// <summary>
        /// "Estilizado" = o material do componente NÃO é o material padrão da própria fonte dele,
        /// ou é de um shader diferente do material da fonte serifada. É o retrato de "alguém mexeu
        /// no material deste texto" — o jogo (títulos/números de combate) ou QUALQUER mod que tenha
        /// clonado o material por componente para aplicar efeito.
        ///
        /// BF-2: esta classificação serve APENAS ao escape (PularTextosEstilizados). O portão que
        /// decide se o texto pode ser mexido NÃO é mais ela — é o EFEITO PRESENTE no material
        /// (TemEfeitoNoMaterial + EstiloTransportavel), e por isso um texto NÃO classificado cuja
        /// fonte traz _FaceTex/bevel/glow também é protegido.
        /// </summary>
        private bool EhEstilizado(Material antigo, TMP_FontAsset fonteAntiga, out string motivo)
        {
            motivo = null;
            if (antigo == null)
            {
                return false;
            }

            if (fonteAntiga != null && fonteAntiga.material != null && antigo != fonteAntiga.material)
            {
                motivo = $"material proprio '{antigo.name}' (padrao da fonte '{fonteAntiga.name}' = " +
                         $"'{fonteAntiga.material.name}')";
                return true;
            }

            Material padraoNovo = _serifFont != null ? _serifFont.material : null;
            if (padraoNovo != null && antigo.shader != padraoNovo.shader)
            {
                motivo = $"shader '{Nome(antigo.shader)}' != '{Nome(padraoNovo.shader)}' da fonte serifada";
                return true;
            }

            return false;
        }

        /// <summary>
        /// BF-1/BF-2 — FALHA-SEGURA do caminho que preserva efeito: só se troca a fonte de um texto
        /// cujo material carrega EFEITO se o que está EM USO nele puder ser reproduzido no material
        /// da fonte nova. Uma cópia parcial (ex.: contorno copiado e textura de face perdida) sairia
        /// PIOR que não mexer — então, em dúvida, a resposta é NÃO e o texto fica exatamente como
        /// está (o comportamento de hoje, nunca pior). Quem chama já conferiu que há efeito
        /// (TemEfeitoNoMaterial) — sem efeito não há o que proteger.
        ///
        /// BF-2 — o que MUDOU nesta conferência:
        ///  * VARIANTE de shader diferente NÃO reprova mais. As propriedades de estilo vivem nas
        ///    DUAS variantes de SDF do TMP (a fonte serifada sai com 'Mobile/Distance Field', via
        ///    ShaderUtilities.ShaderRef_MobileSDF, e os alvos de combate do jogo usam 'Distance
        ///    Field Overlay' e 'Distance Field (Surface)'); o que muda é a VARIANTE, não o conjunto
        ///    de propriedades. Reprovar aqui era recusar exatamente o caso que o conserto existe
        ///    para atender. O transporte virou best-effort propriedade por propriedade com
        ///    HasProperty, e o que a variante nova não expuser sai no log como não transportado.
        ///  * TEXTURA DE FACE e bevel contam como "em uso" só quando a textura é de VERDADE: o
        ///    default do shader para _FaceTex é a textura embutida BRANCA do Unity e o de _BumpMap é
        ///    o normal map embutido — `GetTexture` devolve esses objetos (não null) mesmo sem efeito
        ///    nenhum, e contá-los reprovava todo material de SDF. Ver TexturaDeEfeito.
        ///  * As duas últimas conferências (o material novo expõe contorno/underlay) só valem com a
        ///    cópia LIGADA — sem cópia pedida (PreservarEstilo=false) elas não têm objeto. O que
        ///    barra acima (efeito que a cópia não reproduz) vale sempre, para a promessa "em dúvida,
        ///    nada pior que hoje" não depender da config.
        /// </summary>
        private bool EstiloTransportavel(Material antigo, bool transporteLigado, out string motivo)
        {
            motivo = null;
            try
            {
                if (antigo == null)
                {
                    return true;
                }

                if (antigo.HasProperty("_FaceTex") && TexturaDeEfeito(antigo.GetTexture("_FaceTex")))
                {
                    motivo = "_FaceTex (textura de face) em uso — a copia nao transporta textura";
                    return false;
                }

                if (antigo.HasProperty("_BumpMap") && TexturaDeEfeito(antigo.GetTexture("_BumpMap")))
                {
                    motivo = "_BumpMap (bevel) em uso — a copia nao transporta bevel";
                    return false;
                }

                if (antigo.IsKeywordEnabled("GLOW_ON"))
                {
                    motivo = "GLOW_ON ligado — glow nao e transportado";
                    return false;
                }

                if (antigo.IsKeywordEnabled("BEVEL_ON"))
                {
                    motivo = "BEVEL_ON ligado — bevel nao e transportado";
                    return false;
                }

                if (!transporteLigado)
                {
                    // Sem cópia pedida: as conferências abaixo são sobre a CÓPIA caber no material
                    // novo, e não há cópia. O que barra acima continua valendo.
                    return true;
                }

                Material padraoNovo = _serifFont != null ? _serifFont.material : null;
                if (padraoNovo == null)
                {
                    motivo = "a fonte serifada ainda nao tem material";
                    return false;
                }

                bool contornoEmUso = antigo.IsKeywordEnabled("OUTLINE_ON") || ValorAtivo(antigo, "_OutlineWidth");
                if (contornoEmUso && !padraoNovo.HasProperty("_OutlineWidth"))
                {
                    motivo = "contorno em uso e o material novo nao expoe _OutlineWidth (fonte bitmap)";
                    return false;
                }

                bool sombraEmUso = antigo.IsKeywordEnabled("UNDERLAY_ON") ||
                                   antigo.IsKeywordEnabled("UNDERLAY_INNER") ||
                                   (antigo.HasProperty("_UnderlayColor") && antigo.GetColor("_UnderlayColor").a > 0.001f);
                if (sombraEmUso && !padraoNovo.HasProperty("_UnderlaySoftness"))
                {
                    motivo = "sombra em uso e o material novo nao expoe underlay";
                    return false;
                }

                return true;
            }
            catch (Exception e)
            {
                // Em duvida NAO estilizar: qualquer falha na conferencia reprova o transporte.
                motivo = "nao deu para conferir o efeito (" + e.GetType().Name + ")";
                return false;
            }
        }

        /// <summary>
        /// BF-2 — O CRITÉRIO DO PORTÃO: este MATERIAL carrega efeito? A pergunta certa é esta, e não
        /// "este texto foi classificado como estilizado?": o material da PRÓPRIA fonte pode trazer
        /// _FaceTex/bevel/glow (texto não classificado, que o BF-1 trocava e deixava perder o
        /// efeito), e o texto classificado é o caso mais comum, não o único. Vale com PreservarEstilo
        /// ligado ou desligado — é uma proteção, não uma preferência de estilo.
        /// </summary>
        private static bool TemEfeitoNoMaterial(Material m)
        {
            try
            {
                if (m == null)
                {
                    return false;
                }

                if (m.HasProperty("_FaceTex") && TexturaDeEfeito(m.GetTexture("_FaceTex")))
                {
                    return true;
                }
                if (m.HasProperty("_BumpMap") && TexturaDeEfeito(m.GetTexture("_BumpMap")))
                {
                    return true;
                }
                if (m.IsKeywordEnabled("GLOW_ON") || m.IsKeywordEnabled("BEVEL_ON"))
                {
                    return true;
                }
                if (m.IsKeywordEnabled("OUTLINE_ON") || ValorAtivo(m, "_OutlineWidth") || ValorAtivo(m, "_OutlineSoftness"))
                {
                    return true;
                }
                if (m.IsKeywordEnabled("UNDERLAY_ON") || m.IsKeywordEnabled("UNDERLAY_INNER"))
                {
                    return true;
                }
                if (m.HasProperty("_UnderlayColor") && m.GetColor("_UnderlayColor").a > 0.001f)
                {
                    return true;
                }
                return false;
            }
            catch
            {
                // Em dúvida, tratar como efeito: aí a conferência roda e decide (conservador).
                return true;
            }
        }

        /// <summary>
        /// BF-2 — a textura é um EFEITO de verdade ou só o default do shader? Um default de textura
        /// ("white"/"bump" no shader) é servido pelo Unity como textura EMBUTIDA, minúscula e
        /// compartilhada; `Material.GetTexture` devolve esse objeto (não null) mesmo quando o texto
        /// não usa textura nenhuma. Uma textura de face/bevel real tem o tamanho do atlas. Sem esta
        /// distinção, a falha-segura reprovava todo material de SDF — o mesmo defeito que o BF-2
        /// veio consertar, por outro motivo.
        /// </summary>
        private static bool TexturaDeEfeito(Texture tex)
        {
            try
            {
                if (tex == null)
                {
                    return false;
                }
                if (tex == Texture2D.whiteTexture || tex == Texture2D.normalTexture ||
                    tex == Texture2D.blackTexture || tex == Texture2D.grayTexture)
                {
                    return false;
                }

                string n = (tex.name ?? string.Empty).Trim().ToLowerInvariant();
                if (n == "white" || n.StartsWith("white ") || n == "bump" || n.StartsWith("bump ") ||
                    n == "gray" || n.StartsWith("gray ") || n == "black" || n.StartsWith("black ") ||
                    n.StartsWith("unity_") || n.StartsWith("unity default"))
                {
                    return false;
                }

                // As embutidas do Unity têm poucos pixels; face/bevel de verdade é do tamanho do atlas.
                return tex.width > 8 || tex.height > 8;
            }
            catch
            {
                return true; // em dúvida, tratar como efeito (conservador: não mexe)
            }
        }

        /// <summary>
        /// Transporta as propriedades de ESTILO do material antigo para o material novo
        /// (que é a instância POR COMPONENTE), testando HasProperty antes de cada Set e ligando
        /// as keywords que estavam ativas. Devolve, por out, o que existia na origem e NÃO pôde
        /// ser transportado (fica no log de diagnóstico, para nada passar em branco) e, em
        /// <paramref name="registros"/>, o que fica fora de propósito COM o motivo dito — os pesos
        /// da fonte, a troca de variante de shader e as keywords que dependem da variante.
        ///
        /// NÃO se copia: _MainTex/_TextureWidth/_TextureHeight/_GradientScale/_ScaleRatio_*
        /// (isso é o ATLAS e a matemática de SDF da fonte NOVA), texturas de face (_FaceTex), bevel
        /// (_BumpMap) nem os pesos _WeightNormal/_WeightBold (parâmetro da fonte).
        ///
        /// BF-2: a variante de shader da origem pode ser DIFERENTE da do material novo — todo Set é
        /// feito atrás de HasProperty e o que a variante nova não expuser vai para "não transportados".
        /// </summary>
        private static string CopiarEstilo(Material antigo, Material novo, out string naoTransportados, out string registros)
        {
            var copiados = new List<string>();
            var perdidos = new List<string>();
            var registrado = new List<string>();

            // BF-2: a troca de VARIANTE fica dita ANTES de qualquer cópia — é o "antes/depois" que
            // explica, no log, por que uma propriedade pode não existir no destino.
            try
            {
                if (antigo.shader != novo.shader)
                {
                    registrado.Add("variante de shader '" + Nome(antigo.shader) + "' -> '" + Nome(novo.shader) +
                                   "' (transporte best-effort: cada propriedade so entra se a variante nova a expuser)");
                }
            }
            catch
            {
            }

            for (int i = 0; i < PropsCor.Length; i++)
            {
                string p = PropsCor[i];
                if (antigo.HasProperty(p) && novo.HasProperty(p))
                {
                    novo.SetColor(p, antigo.GetColor(p));
                    copiados.Add(p);
                }
                else if (antigo.HasProperty(p))
                {
                    perdidos.Add(p + " (shader novo nao expoe)");
                }
            }

            for (int i = 0; i < PropsFloat.Length; i++)
            {
                string p = PropsFloat[i];
                if (antigo.HasProperty(p) && novo.HasProperty(p))
                {
                    novo.SetFloat(p, antigo.GetFloat(p));
                    copiados.Add(p);
                }
                else if (antigo.HasProperty(p))
                {
                    perdidos.Add(p + " (shader novo nao expoe)");
                }
            }

            // BF-2: propriedades de VETOR (o recorte _ClipRect do texto mascarado/rolável).
            for (int i = 0; i < PropsVetor.Length; i++)
            {
                string p = PropsVetor[i];
                if (antigo.HasProperty(p) && novo.HasProperty(p))
                {
                    novo.SetVector(p, antigo.GetVector(p));
                    copiados.Add(p);
                }
                else if (antigo.HasProperty(p))
                {
                    perdidos.Add(p + " (shader novo nao expoe)");
                }
            }

            // Keywords: elas é que LIGAM o contorno/sombra no shader — copiar só o valor não basta.
            bool contornoAtivo = antigo.IsKeywordEnabled("OUTLINE_ON") || ValorAtivo(antigo, "_OutlineWidth");
            bool sombraAtiva = antigo.IsKeywordEnabled("UNDERLAY_ON") ||
                               antigo.IsKeywordEnabled("UNDERLAY_INNER") ||
                               (antigo.HasProperty("_UnderlayColor") && antigo.GetColor("_UnderlayColor").a > 0.001f);

            if (contornoAtivo && novo.HasProperty("_OutlineWidth"))
            {
                novo.EnableKeyword("OUTLINE_ON");
                copiados.Add("OUTLINE_ON");
            }
            else if (contornoAtivo)
            {
                perdidos.Add("OUTLINE_ON (shader novo sem _OutlineWidth: fonte bitmap)");
            }

            if (sombraAtiva && novo.HasProperty("_UnderlaySoftness"))
            {
                novo.EnableKeyword("UNDERLAY_ON");
                copiados.Add("UNDERLAY_ON");
            }
            else if (sombraAtiva)
            {
                perdidos.Add("UNDERLAY_ON (shader novo sem underlay)");
            }

            // BF-2: a sombra INTERNA (UNDERLAY_INNER) era o buraco que virava "outer" calado. A
            // keyword é transportada; como keyword de shader NÃO se confere por HasProperty, o aviso
            // de que ela depende de a variante nova a declarar vai para os registros.
            if (antigo.IsKeywordEnabled("UNDERLAY_INNER"))
            {
                novo.EnableKeyword("UNDERLAY_INNER");
                copiados.Add("UNDERLAY_INNER");
                if (antigo.shader != novo.shader)
                {
                    registrado.Add("UNDERLAY_INNER: keyword transportada, mas so tem efeito se a variante '" +
                                   Nome(novo.shader) + "' a declarar (senao a sombra sai 'outer')");
                }
            }

            // BF-2: recorte de texto mascarado/rolável — as keywords de masking do TMP.
            for (int i = 0; i < KeywordsMascara.Length; i++)
            {
                string k = KeywordsMascara[i];
                if (!antigo.IsKeywordEnabled(k))
                {
                    continue;
                }
                novo.EnableKeyword(k);
                copiados.Add(k);
                registrado.Add(k + ": keyword de masking transportada; so tem efeito se a variante '" +
                               Nome(novo.shader) + "' a declarar");
            }

            // BF-2: pesos da fonte — não se copiam (são da fonte NOVA, como _GradientScale), mas não
            // passam em branco: quando diferem da origem, saem registrados com o motivo.
            for (int i = 0; i < PropsDeFonteRegistradas.Length; i++)
            {
                RegistrarDiferenca(antigo, novo, registrado, PropsDeFonteRegistradas[i],
                    "parametro da fonte/atlas: fica o do novo (nao e efeito do texto)");
            }

            // Recursos de estilo presentes na origem que ficam de fora de propósito/limitação.
            // BF-2: textura de face/bevel só conta quando é de VERDADE (o default "white"/"bump" do
            // shader é a textura embutida do Unity e não é efeito nenhum) — senão o log acusava
            // perda de uma textura que nunca esteve em uso.
            if (antigo.HasProperty("_FaceTex") && TexturaDeEfeito(antigo.GetTexture("_FaceTex")))
            {
                perdidos.Add("_FaceTex (textura de face)");
            }
            if (antigo.HasProperty("_BumpMap") && TexturaDeEfeito(antigo.GetTexture("_BumpMap")))
            {
                perdidos.Add("_BumpMap (bevel)");
            }
            if (antigo.IsKeywordEnabled("GLOW_ON"))
            {
                perdidos.Add("GLOW_ON");
            }
            if (antigo.IsKeywordEnabled("BEVEL_ON"))
            {
                perdidos.Add("BEVEL_ON");
            }
            if (antigo.HasProperty("_GradientScale") && novo.HasProperty("_GradientScale") &&
                !Mathf.Approximately(antigo.GetFloat("_GradientScale"), novo.GetFloat("_GradientScale")))
            {
                perdidos.Add("_GradientScale origem=" + antigo.GetFloat("_GradientScale").ToString("0.##") +
                             " novo=" + novo.GetFloat("_GradientScale").ToString("0.##") +
                             " (fica o do atlas novo)");
            }

            naoTransportados = perdidos.Count > 0 ? string.Join("; ", perdidos.ToArray()) : null;
            registros = registrado.Count > 0 ? string.Join("; ", registrado.ToArray()) : null;
            return copiados.Count > 0 ? string.Join(", ", copiados.ToArray()) : null;
        }

        /// <summary>
        /// BF-2: registra no log uma propriedade que existe na ORIGEM e difere do destino, com o
        /// motivo de ela ficar fora. É o que fecha o buraco "não é copiado NEM logado" — vale para os
        /// parâmetros da fonte (peso), que não são efeito do texto mas calavam sem deixar rastro.
        /// </summary>
        private static void RegistrarDiferenca(Material antigo, Material novo, List<string> registros, string prop, string motivo)
        {
            if (antigo == null || novo == null || registros == null || !antigo.HasProperty(prop))
            {
                return;
            }

            float origem = antigo.GetFloat(prop);
            bool existeNoNovo = novo.HasProperty(prop);
            float destino = existeNoNovo ? novo.GetFloat(prop) : 0f;
            if (existeNoNovo && Mathf.Approximately(origem, destino))
            {
                return;
            }

            registros.Add(prop + " origem=" + origem.ToString("0.###") + " novo=" +
                          (existeNoNovo ? destino.ToString("0.###") : "(propriedade ausente)") +
                          " (" + motivo + ")" + (existeNoNovo ? string.Empty : " — o shader novo nao expoe a propriedade"));
        }

        private static bool ValorAtivo(Material m, string prop)
        {
            return m.HasProperty(prop) && m.GetFloat(prop) > 0.0001f;
        }

        /// <summary>
        /// Marca "este texto estilizado já foi contado no resumo" (uma vez por componente), para
        /// o resumo da varredura não repetir a cada 2 segundos. Não é cache de decisão: o texto
        /// continua sendo reavaliado.
        /// </summary>
        private bool ContarPuloUmaVez(TMP_Text t)
        {
            try
            {
                return _puladosContados.Add(t.GetInstanceID());
            }
            catch
            {
                return true;
            }
        }

        /// <summary>
        /// Confere que o componente REALMENTE passou a usar o atlas da fonte serifada (ou seja,
        /// o LoadFontAsset fez efeito). É a guarda que impede o pior caso: instanciar/copiar
        /// estilo para um material que ainda aponta para o atlas da fonte ANTIGA.
        /// </summary>
        private bool UsaMaterialDaFonteNova(TMP_Text t)
        {
            try
            {
                Material m = t.fontSharedMaterial;
                Texture atlas = _serifFont != null ? (Texture)_serifFont.atlasTexture : null;
                if (m == null || atlas == null || !m.HasProperty("_MainTex"))
                {
                    return false;
                }
                Texture tex = m.GetTexture("_MainTex");
                return tex != null && tex.GetInstanceID() == atlas.GetInstanceID();
            }
            catch
            {
                return false;
            }
        }

        private static string Nome(Shader s)
        {
            return s != null ? s.name : "(sem shader)";
        }

        private static string NomeObjeto(TMP_Text t)
        {
            try
            {
                return t != null && t.gameObject != null ? t.gameObject.name : "(?)";
            }
            catch
            {
                return "(?)";
            }
        }

        /// <summary>
        /// BF-2R — ZERA o orçamento do diagnóstico quando a CENA muda, e devolve a cena em vigor.
        ///
        /// É o que faz o teto se esgotar DEPOIS da linha que interessa. A varredura de boot vê 400+
        /// textos (medido no log do dono: 406 e 484 numa passada; o próprio CAP-1 contou 488 TMP
        /// texts na tela) e, com o orçamento sendo da SESSÃO (como era na BF-2), o teto de efeito se
        /// esgotava antes da cena de combate — a linha que o dono liga o diagnóstico para ler não
        /// saía nunca. Com o orçamento POR CENA, cada cena nova (o combate inclusive) começa com os
        /// dois tetos inteiros.
        ///
        /// POR QUE A CENA ATIVA É UM BOM MARCO (não é escolha arbitrária): o PRÓPRIO JOGO usa
        /// `SceneManager.GetActiveScene()` como marcador de estado — o `LoadingScreen` espera
        /// `while (GetActiveScene().buildIndex != 1)` e decide pular o carregamento por
        /// `GetActiveScene().buildIndex == 1`, e a cena de carregamento entra por
        /// `LoadScene("Loading")` (Assembly-CSharp decompilado). O log de diagnóstico continua
        /// LIMITADO mesmo com o reset: `_diagVistos` só deixa sair UMA linha por texto+situação na
        /// sessão inteira, então uma cena que se recarrega não repete o que já foi dito.
        ///
        /// Sem cena legível (exceção, ou nenhuma cena ativa) o orçamento é MANTIDO — conservador:
        /// nunca loga a mais por causa de uma leitura que falhou.
        /// </summary>
        private void OrcamentoDoDiagnosticoPorCena()
        {
            string cena;
            try
            {
                cena = UnityEngine.SceneManagement.SceneManager.GetActiveScene().name;
            }
            catch
            {
                return;
            }

            if (cena == _diagCena)
            {
                return;
            }

            _diagCena = cena;
            _diagLinhas = 0;
            _diagLinhasDeEfeito = 0;
            _diagLinhasDeEscape = 0;
            _diagCortesAvisados.Clear();
            Plugin.Log.LogInfo("Better Font [diag]: cena '" + (string.IsNullOrEmpty(cena) ? "(sem nome)" : cena) +
                               "' — orcamento de diagnostico zerado (os tetos sao por cena).");
        }

        /// <summary>
        /// BF-ESTILO: linha de diagnóstico por texto (só com LogDiagnosticoEstilo ligado, uma vez
        /// por texto+situação, com teto de linhas para não inundar o log). É o que fecha a dúvida
        /// "por que este texto ficou diferente": mostra material, shader (de ONDE veio e PARA ONDE
        /// foi), o que foi copiado, o que não pôde ir e o que fica fora de propósito.
        ///
        /// BF-2/BF-2R: dois tetos, POR CENA. A linha de ROTINA (texto cujo material não carrega
        /// efeito nenhum) para em <c>TetoDiagRotina</c>; a linha de EFEITO — o texto cujo material
        /// carrega efeito (o caso de combate), mais o intocado por efeito não transportável e o
        /// revertido — para em <c>TetoDiagEfeito</c>.
        ///
        /// O QUE ESTAVA ERRADO (BF-2 → BF-2R, achado da revisão independente): (a) a classificação
        /// era tirada do CONTEÚDO da linha — <c>copiados</c> nunca vem vazio num texto convertido
        /// (as cores de face existem nos dois shaders), então toda linha era "de efeito" e o teto de
        /// ROTINA era INALCANÇÁVEL; (b) os contadores eram da SESSÃO e a varredura de boot vê 400+
        /// textos, então o teto de 300 se esgotava ANTES da cena de combate. Agora a classificação é
        /// EXPLÍCITA (parâmetro <paramref name="tipo"/>: quem chama sabe se há efeito no material) e o
        /// orçamento é POR CENA. A prova está na suite: `t_bf_diag_orcamento.py`.
        ///
        /// O QUE AINDA ESTAVA ERRADO (BF-2R → BF-3, achado da revisão independente): a classificação
        /// era explícita, mas o call site do PULADO PELO ESCAPE passava "de efeito" — e com
        /// <c>PularTextosEstilizados=true</c> (a config do dono) a varredura pula ~484 textos numa
        /// passada, que esgotavam o teto de EFEITO antes da linha de combate. Um texto pulado pelo
        /// escape não transportou efeito nenhum: ele é a categoria <c>Escape</c>, com teto PRÓPRIO
        /// (<c>TetoDiagEscape</c>), e não disputa o orçamento de efeito.
        /// </summary>
        private void Diagnostico(string situacao, TMP_Text t, TMP_FontAsset fonteAntiga, Material antigo,
            string copiados, string naoTransportados, string registros, TipoLinhaDiag tipo)
        {
            if (!Plugin.LogDiagnosticoLigado)
            {
                return;
            }

            OrcamentoDoDiagnosticoPorCena();

            if (tipo == TipoLinhaDiag.Efeito)
            {
                if (_diagLinhasDeEfeito >= TetoDiagEfeito)
                {
                    AvisoDeCorte("de efeito", TetoDiagEfeito);
                    return;
                }
            }
            else if (tipo == TipoLinhaDiag.Escape)
            {
                if (_diagLinhasDeEscape >= TetoDiagEscape)
                {
                    AvisoDeCorte("pulado pelo escape", TetoDiagEscape);
                    return;
                }
            }
            else if (_diagLinhas >= TetoDiagRotina)
            {
                AvisoDeCorte("de rotina", TetoDiagRotina);
                return;
            }

            string chave;
            try
            {
                chave = situacao + "#" + t.GetInstanceID();
            }
            catch
            {
                chave = situacao + "#" + NomeObjeto(t);
            }
            if (!_diagVistos.Add(chave))
            {
                return;
            }

            if (tipo == TipoLinhaDiag.Efeito)
            {
                _diagLinhasDeEfeito++;
            }
            else if (tipo == TipoLinhaDiag.Escape)
            {
                _diagLinhasDeEscape++;
            }
            else
            {
                _diagLinhas++;
            }

            string shader;
            try
            {
                shader = antigo != null ? Nome(antigo.shader) : "(sem material)";
            }
            catch
            {
                shader = "(shader indisponivel)";
            }

            // BF-2: o "antes/depois" da variante. Texto pulado/revertido não foi tocado — dizer que
            // ele "foi para a serifa" seria mentira no log.
            string shaderDestino;
            try
            {
                bool foiConvertido = !situacao.StartsWith("PULADO", StringComparison.Ordinal) &&
                                     !situacao.StartsWith("REVERTIDO", StringComparison.Ordinal);
                Material materialNovo = _serifFont != null ? _serifFont.material : null;
                shaderDestino = !foiConvertido ? "(variante nao trocada: material intocado)"
                              : (materialNovo != null ? Nome(materialNovo.shader) : "(fonte serifada sem material)");
            }
            catch
            {
                shaderDestino = "(shader indisponivel)";
            }

            bool gradienteVertice = false;
            try
            {
                gradienteVertice = t.enableVertexGradient;
            }
            catch
            {
            }

            Plugin.Log.LogInfo(
                $"[diag] {situacao} | objeto='{NomeObjeto(t)}' ({t.GetType().Name}) | " +
                $"fonte='{(fonteAntiga != null ? fonteAntiga.name : "(nula)")}' -> " +
                $"'{(_serifFont != null ? _serifFont.name : "(nula)")}' | " +
                $"material compartilhado='{(antigo != null ? antigo.name : "(nulo)")}' | " +
                $"shader='{shader}' -> '{shaderDestino}' | " +
                $"gradiente de vertice={gradienteVertice} | " +
                $"copiados: {(string.IsNullOrEmpty(copiados) ? "nenhum" : copiados)} | " +
                $"nao transportados: {(string.IsNullOrEmpty(naoTransportados) ? "nenhum" : naoTransportados)} | " +
                $"registros: {(string.IsNullOrEmpty(registros) ? "nenhum" : registros)}");
        }

        /// <summary>BF-2: avisa UMA vez por teto que o restante daquele tipo de linha foi omitido.</summary>
        private void AvisoDeCorte(string qual, int teto)
        {
            if (!_diagCortesAvisados.Add(qual))
            {
                return;
            }
            Plugin.Log.LogInfo("Better Font [diag]: limite de " + teto + " linhas " + qual +
                               " atingido — restante omitido (o resumo da varredura continua valendo).");
        }

        /// <summary>
        /// BF-2 — REVERSÃO da falha-segura: devolve o texto ao estado anterior (fonte e material
        /// originais) quando a troca de fonte ou o transporte de estilo falha no meio. Cada passo
        /// protegido por conta própria: se a volta da fonte falhar, o material original ainda é
        /// restaurado, e nada aqui pode derrubar a varredura. O padding é recalculado porque o
        /// contorno/sombra saem dele.
        /// </summary>
        private static void ReverterTexto(TMP_Text t, TMP_FontAsset fonteAntiga, Material antigo)
        {
            try
            {
                if (fonteAntiga != null)
                {
                    t.font = fonteAntiga;
                }
            }
            catch
            {
            }

            try
            {
                if (antigo != null)
                {
                    t.fontSharedMaterial = antigo;
                }
            }
            catch
            {
            }

            try
            {
                t.UpdateMeshPadding();
                t.SetVerticesDirty();
            }
            catch
            {
            }
        }

        /// <summary>
        /// BF-2 — uma linha (só com LogDiagnosticoEstilo ligado), UMA vez por sessão, com o material
        /// da fonte NOVA e quais propriedades do transporte ele expõe. É a resposta, no log, para
        /// "por que esta propriedade ficou de fora" — e a prova de que a variante da fonte serifada
        /// aceita o transporte, que é o caso dos textos de combate.
        /// </summary>
        private void CatalogoDoMaterialNovo()
        {
            if (!Plugin.LogDiagnosticoLigado || _catalogoDoMaterialNovo)
            {
                return;
            }
            _catalogoDoMaterialNovo = true;

            try
            {
                Material m = _serifFont != null ? _serifFont.material : null;
                if (m == null)
                {
                    Plugin.Log.LogInfo("Better Font [diag]: a fonte serifada nao tem material — nao ha o que catalogar.");
                    return;
                }

                var linhas = new List<string>();
                for (int i = 0; i < PropsCor.Length; i++)
                {
                    linhas.Add(PropsCor[i] + "=" + SimNao(m.HasProperty(PropsCor[i])));
                }
                for (int i = 0; i < PropsFloat.Length; i++)
                {
                    linhas.Add(PropsFloat[i] + "=" + SimNao(m.HasProperty(PropsFloat[i])));
                }
                for (int i = 0; i < PropsVetor.Length; i++)
                {
                    linhas.Add(PropsVetor[i] + "=" + SimNao(m.HasProperty(PropsVetor[i])));
                }
                for (int i = 0; i < PropsDeFonteRegistradas.Length; i++)
                {
                    linhas.Add(PropsDeFonteRegistradas[i] + "=" + SimNao(m.HasProperty(PropsDeFonteRegistradas[i])));
                }

                Plugin.Log.LogInfo(
                    "[diag] catalogo do material da fonte nova: fonte='" +
                    (_serifFont != null ? _serifFont.name : "(nula)") + "' shader='" + Nome(m.shader) +
                    "' | expoe: " + string.Join(", ", linhas.ToArray()) +
                    " | keywords do TMP nesta versao sao declaradas no shader, nao em propriedade (ver 'registros' nas linhas de texto)");
            }
            catch (System.Exception e)
            {
                Plugin.Log.LogWarning("Better Font [diag]: catalogo do material novo falhou: " + e.Message);
            }
        }

        private static string SimNao(bool v)
        {
            return v ? "sim" : "nao";
        }

        /// <summary>
        /// BF-2: o asset criado em runtime vem **sem nome** — `TMP_FontAsset.CreateFontAssetInstance`
        /// monta o material (com o atlas, `_GradientScale` e os pesos `_WeightNormal`/`_WeightBold`
        /// da fonte NOVA) mas nunca seta `name`. Como o diagnóstico imprime o nome da fonte nova, sem
        /// isto a linha do dono sairia "fonte='' -> ''" e não diria qual fonte entrou. É só o rótulo
        /// do log; nada em jogo depende dele.
        /// </summary>
        private static void NomearFonteSerifada(TMP_FontAsset asset, string origem)
        {
            try
            {
                asset.name = "BetterFont Serif (" + origem + ")";
            }
            catch
            {
            }
        }

        private static TMP_FontAsset CreateSerifFont()
        {
            // Caminhos de ARQUIVO primeiro (mais confiável que resolução por nome no Unity):
            string[] fileCandidates =
            {
                "C:/Windows/Fonts/times.ttf",                    // Times New Roman
                "C:/Windows/Fonts/georgia.ttf",                  // Georgia (serifa parecida)
                "C:/Windows/Fonts/LiberationSerif-Regular.ttf",  // Liberation Serif
            };
            foreach (var path in fileCandidates)
            {
                try
                {
                    if (!System.IO.File.Exists(path))
                    {
                        continue;
                    }
                    Font fileFont = new Font(path);
                    if (fileFont == null)
                    {
                        continue;
                    }
                    TMP_FontAsset asset = TMP_FontAsset.CreateFontAsset(fileFont);
                    if (asset != null)
                    {
                        NomearFonteSerifada(asset, System.IO.Path.GetFileName(path));
                        Plugin.Log.LogInfo($"Better Font: usando '{path}' como fonte serifada.");
                        return asset;
                    }
                    Plugin.Log.LogWarning($"Better Font: '{path}' carregou mas CreateFontAsset retornou null.");
                }
                catch (System.Exception e)
                {
                    Plugin.Log.LogWarning($"Better Font: '{path}' falhou: {e.GetType().Name}: {e.Message}");
                }
            }

            // Último recurso: resolução por nome do SO.
            string[] nameCandidates = { "Times New Roman", "Georgia", "Liberation Serif", "Cambria" };
            foreach (var name in nameCandidates)
            {
                try
                {
                    Font osFont = Font.CreateDynamicFontFromOSFont(name, 36);
                    if (osFont == null)
                    {
                        continue;
                    }
                    TMP_FontAsset asset = TMP_FontAsset.CreateFontAsset(osFont);
                    if (asset != null)
                    {
                        NomearFonteSerifada(asset, name);
                        Plugin.Log.LogInfo($"Better Font: usando '{name}' (OS) como fonte serifada.");
                        return asset;
                    }
                }
                catch (System.Exception e)
                {
                    Plugin.Log.LogWarning($"Better Font: '{name}' falhou: {e.GetType().Name}: {e.Message}");
                }
            }
            return null;
        }
    }
}
