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
    /// Agora: (1) as propriedades de estilo do material ANTIGO são transportadas para o material
    /// POR COMPONENTE da fonte nova (t.fontMaterial = instância; o compartilhado nunca é
    /// escrito); (2) por padrão, textos de material ESTILIZADO nem trocam de fonte.
    /// SEM alteração de gameplay.
    /// </summary>
    [BepInPlugin("com.gumatos.betterfont", "Better Font", "1.0.1")]
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
        /// a entrada fica null e o mod continua com o DEFAULT de cada opcao em vez de estourar
        /// NullReference a cada texto da tela. Mesmo padrao do RSTV (<c>Plugin.BotaoLigado</c>).
        /// </summary>
        internal static bool PreservarEstiloLigado
        {
            get { return PreservarEstilo == null || PreservarEstilo.Value; }
        }

        /// <summary>Padrao <c>true</c> (nao troca a fonte de material estilizado).</summary>
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

            // BF-ESTILO: textos com material estilizado (materiais do jogo em combate, titulos etc.)
            // ficam fora da troca por padrão — garante estilo intacto onde a cópia poderia não reproduzir bem.
            PularTextosEstilizados = BindSeguro("Estilo", "PularTextosEstilizados", true,
                "true = NAO troca a fonte dos textos cujo material e estilizado (material proprio, diferente do " +
                "material padrao da fonte daquele componente, ou com shader diferente do material da fonte serifada). " +
                "Nesses textos o visual original fica 100% intacto (so nao ganham a serifa). false = troca a fonte em " +
                "TODOS os textos e transporta o estilo por copia (PreservarEstilo). Padrao: true (seguro). " +
                "Para ver o que foi pulado, ligue LogDiagnosticoEstilo.");

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
        /// nao tem arquivo de config nenhum. Mesmo padrao do RSTV (<c>Plugin.BotaoLigado</c>) e do
        /// BetterCombatText (try/catch no chamador).
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
        // existirem nos DOIS lados (HasProperty) são tocadas — shader que não expõe a
        // propriedade nem recebe o Set, e o que não pôde ser transportado vai para o log.
        private static readonly string[] PropsCor =
        {
            "_FaceColor", "_OutlineColor", "_UnderlayColor"
        };

        private static readonly string[] PropsFloat =
        {
            "_FaceDilate",
            "_OutlineWidth", "_OutlineSoftness",
            "_UnderlayOffsetX", "_UnderlayOffsetY", "_UnderlayDilate", "_UnderlaySoftness"
        };

        private float _lastSweep = -99f;
        private TMP_FontAsset _serifFont;
        private readonly HashSet<TMP_Text> _seenTexts = new HashSet<TMP_Text>();
        private readonly HashSet<string> _diagVistos = new HashSet<string>();
        private readonly HashSet<int> _puladosContados = new HashSet<int>();
        private bool _loggedFirstSweep;
        private int _diagLinhas;
        private bool _diagCortado;

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
        /// BF-ESTILO: antes de cada troca, o material EM USO é lido (fontSharedMaterial), e as
        /// propriedades de ESTILO dele são transportadas para o material POR COMPONENTE da fonte
        /// nova (t.fontMaterial) — nunca escrevemos no material compartilhado nem no material do
        /// font asset. Textos de material estilizado são pulados por padrão (PularTextosEstilizados).
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
                }

                int convertidos = 0;
                int pulados = 0;
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
                        // O material EM USO agora: é ele que carrega a cor/contorno/sombra do jogo.
                        Material antigo = t.fontSharedMaterial;
                        TMP_FontAsset fonteAntiga = t.font;

                        string motivoEstilo;
                        if (Plugin.PularEstilizadosLigado && EhEstilizado(antigo, fonteAntiga, out motivoEstilo))
                        {
                            // Conta/loga o pulo UMA vez por texto (a varredura roda a cada 2s; sem
                            // isto o resumo repetiria para sempre). O texto continua sendo reavaliado
                            // nas passadas seguintes: se o material dele mudar, ele entra na conversão.
                            if (ContarPuloUmaVez(t))
                            {
                                pulados++;
                                Diagnostico("PULADO (material estilizado: " + motivoEstilo + ")", t, fonteAntiga, antigo,
                                    "n/a (texto pulado: fonte e material nao foram tocados)",
                                    "n/a (texto pulado: nada foi transportado)");
                            }
                            continue; // fonte E estilo originais intactos
                        }

                        // A troca de fonte troca o material junto (LoadFontAsset do TMP).
                        t.font = _serifFont;

                        string copiados = null;
                        string naoTransportados = null;
                        if (Plugin.PreservarEstiloLigado && antigo != null && UsaMaterialDaFonteNova(t))
                        {
                            // fontMaterial devolve/cria a CÓPIA do material POR COMPONENTE.
                            Material novo = t.fontMaterial;
                            if (novo != null)
                            {
                                copiados = CopiarEstilo(antigo, novo, out naoTransportados);
                                // contorno/sombra saem para FORA do glifo: sem recalcular o padding
                                // o contorno é cortado na borda do mesh (mesma razão do BetterCombatText).
                                t.UpdateMeshPadding();
                                t.SetVerticesDirty();
                            }
                        }

                        convertidos++;
                        Diagnostico("CONVERTIDO", t, fonteAntiga, antigo, copiados, naoTransportados);
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

                if (convertidos > 0 || pulados > 0)
                {
                    Plugin.Log.LogInfo(
                        $"Better Font: varredura — {convertidos} texto(s) convertidos para a serifa" +
                        (Plugin.PreservarEstiloLigado ? " (estilo transportado por cópia)" : string.Empty) +
                        $", {pulados} pulado(s) por material estilizado, {jaNaSerifa} já na serifa.");
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
        /// ou é de um shader diferente do material da fonte serifada (aí a cópia poderia não
        /// reproduzir a receita do jogo). Nesses casos o padrão é não mexer (ver PularTextosEstilizados).
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
        /// Transporta as propriedades de ESTILO do material antigo para o material novo
        /// (que é a instância POR COMPONENTE), testando HasProperty antes de cada Set e ligando
        /// as keywords que estavam ativas. Devolve, por out, o que existia na origem e NÃO pôde
        /// ser transportado (fica no log de diagnóstico, para nada passar em branco).
        ///
        /// NÃO se copia: _MainTex/_TextureWidth/_TextureHeight/_GradientScale/_ScaleRatio_*
        /// (isso é o ATLAS e a matemática de SDF da fonte NOVA) nem texturas de face (_FaceTex).
        /// </summary>
        private static string CopiarEstilo(Material antigo, Material novo, out string naoTransportados)
        {
            var copiados = new List<string>();
            var perdidos = new List<string>();

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

            // Keywords: elas é que LIGAM o contorno/sombra no shader — copiar só o valor não basta.
            bool contornoAtivo = antigo.IsKeywordEnabled("OUTLINE_ON") || ValorAtivo(antigo, "_OutlineWidth");
            bool sombraAtiva = antigo.IsKeywordEnabled("UNDERLAY_ON") ||
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

            // Recursos de estilo presentes na origem que ficam de fora de propósito/limitação.
            if (antigo.HasProperty("_FaceTex") && antigo.GetTexture("_FaceTex") != null)
            {
                perdidos.Add("_FaceTex (textura de face)");
            }
            if (antigo.HasProperty("_BumpMap") && antigo.GetTexture("_BumpMap") != null)
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
            return copiados.Count > 0 ? string.Join(", ", copiados.ToArray()) : null;
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
        /// BF-ESTILO: linha de diagnóstico por texto (só com LogDiagnosticoEstilo ligado, uma vez
        /// por texto+situação, com teto de linhas para não inundar o log). É o que fecha a dúvida
        /// "por que este texto ficou diferente": mostra material, shader e o que foi/não foi copiado.
        /// </summary>
        private void Diagnostico(string situacao, TMP_Text t, TMP_FontAsset fonteAntiga, Material antigo,
            string copiados, string naoTransportados)
        {
            if (!Plugin.LogDiagnosticoLigado)
            {
                return;
            }
            if (_diagLinhas >= 120)
            {
                if (!_diagCortado)
                {
                    _diagCortado = true;
                    Plugin.Log.LogInfo("Better Font [diag]: limite de 120 linhas atingido — restante omitido.");
                }
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
            _diagLinhas++;

            string shader;
            try
            {
                shader = antigo != null ? Nome(antigo.shader) : "(sem material)";
            }
            catch
            {
                shader = "(shader indisponivel)";
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
                $"material compartilhado='{(antigo != null ? antigo.name : "(nulo)")}' | shader='{shader}' | " +
                $"gradiente de vertice={gradienteVertice} | " +
                $"copiados: {(string.IsNullOrEmpty(copiados) ? "nenhum" : copiados)} | " +
                $"nao transportados: {(string.IsNullOrEmpty(naoTransportados) ? "nenhum" : naoTransportados)}");
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
