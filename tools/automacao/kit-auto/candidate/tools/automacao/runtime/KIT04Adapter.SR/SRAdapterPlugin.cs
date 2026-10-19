// KIT-04F Adapter — SRAdapterPlugin (ponto de entrada Stolen Realm)
using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using KIT04Core;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace KIT04Adapter.SR
{
    [BepInPlugin("com.gumatos.kit04.adapter.sr", "KIT04-SR-Adapter", "0.1.0")]
    // KIT-14F: o Adapter LE o Core em Awake, entao DECLARA a dependencia. Sem isto o
    // Chainloader do BepInEx 5 nao tem por que ordenar Core antes do Adapter — foi o
    // que o run704 observou (Adapter listado antes do Core) e o que derrubava o Awake
    // com NullReferenceException. O vinculo tambem e retomado quadro a quadro
    // (TentarVincular), para nao depender SO da ordem de carga.
    [BepInDependency("com.gumatos.kit04.core")]
    public class SRAdapterPlugin : BaseUnityPlugin
    {
        private const string HarmonyId = "com.gumatos.kit04.adapter.sr";

        private SRScreenManager _telas = null!;
        private SRCharacterManager _personagens = null!;
        private SROwnerManager _owners = null!;
        private SRMappingManager _mapeamentos = null!;

        public static ConfigEntry<bool> p_Habilitado = null!;
        public static ConfigEntry<string> p_CaminhoSaida = null!;
        // KIT-05F (F8): trilha passiva (opt-in SEPARADO, desabilitado por padrao).
        public static ConfigEntry<bool> p_PassivoHabilitado = null!;

        private PontePassivaRSTV _ponte = null!;
        internal static ConfigEntry<bool> ControleHabilitado = null!;
        internal static ConfigEntry<bool> ControleIniciarObservando = null!;
        internal static readonly Dictionary<string, ConfigEntry<string>> TeclasControle = new();
        private string? _ultimaTela;
        private int _ultimoTotalPersonagens = -1;

        // KIT-14F: estado do vinculo com o Core. "pendente" = o Core ainda nao
        // inicializou; o Adapter fica VIVO e tenta de novo (nunca derreferencia null).
        private bool _vinculado;
        private bool _avisouEsperaDoCore;
        private string _estadoVinculo = "novo";
        public static string Kit14fDiagnostico = "";
        // KIT-14F: resultado do patching Harmony ("nao tentado"/"aplicado"/"falhou: ...").
        // O vinculo NAO depende disto, mas o estado fica DECLARADO em vez de silencioso.
        public static string HarmonyEstado = "nao tentado";
        public static string Kit14fIdentidade()
        {
            var f = typeof(CorePlugin).GetField("_instancia",
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static);
            object campo = f == null ? null : f.GetValue(null);
            object refletida = typeof(CorePlugin).GetProperty("Instancia",
                System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static).GetValue(null);
            object direta = CorePlugin.Instancia;
            return "campo=" + (campo == null ? "null" : "ok")
                + " refletida=" + (refletida == null ? "null" : "ok")
                + " direta=" + (direta == null ? "null" : "ok")
                + " campo==direta:" + ReferenceEquals(campo, direta)
                + " campo==refletida:" + ReferenceEquals(campo, refletida)
                + " asmHash=" + typeof(CorePlugin).Assembly.GetHashCode()
                + " tipoHash=" + typeof(CorePlugin).GetHashCode()
                + " | assembliesKIT04Core=" + string.Join(";", System.Linq.Enumerable.Select(
                    System.Linq.Enumerable.Where(AppDomain.CurrentDomain.GetAssemblies(),
                        a => a.GetName().Name == "KIT04Core"),
                    a => a.GetHashCode() + "@" + a.Location));
        }

        private void Awake()
        {
            // Configurações (opt-in: desabilitado por padrão)
            p_Habilitado = Config.Bind("Modo", "habilitado", false, "Habilita o Adapter SR. Sem ser true, nao executa coleta.");
            p_CaminhoSaida = Config.Bind("Modo", "caminhoSaida", "scratch/kit/", "Diretório de saída para arquivos gerados.");
            p_PassivoHabilitado = Config.Bind("Modo", "passivoHabilitado", false,
                "KIT-05F: habilita a trilha passiva RSTV (observa telas/clique; nada e emitido nem modificado).");

            ControleHabilitado = Config.Bind("Controle", "habilitado", false,
                "OPT-IN separado: atalhos passivos F7/F8/F9/F10 no mesmo motor do recorder; nunca autoriza gameplay.");
            ControleIniciarObservando = Config.Bind("Controle", "iniciarObservando", false,
                "Inicia observacao somente com opt-in explicito; false exige F7.");
            foreach (var par in PonteControleRSTV.AtalhosPadrao())
                TeclasControle[par.Key] = Config.Bind("Atalhos", par.Key, par.Value,
                    "Nome canonico Unity KeyCode; conflito/reservada/tecla invalida desabilita o binding.");

            // Fixture de idioma SOMENTE com opt-in da bancada; KIT16 restaura PlayerPrefs.
            if (Config.Bind("AutoAvaliacao", "habilitado", false, "Comandos internos de bancada.").Value
                && Config.Bind("AutoAvaliacao", "idiomaIngles", false, "Fixture de idioma; exige rollback PlayerPrefs KIT16.").Value)
            {
                PlayerPrefs.SetInt("LanguageChoice", (int)LanguageChoice.English);
                Logger.LogInfo("[KIT-AUTO] fixture idioma English aplicada antes da primeira cena; rollback PlayerPrefs pelo runner");
            }

            // KIT-14F: liga se o Core ja existir; se nao, fica PENDENTE (sem excecao).
            TentarVincular();
            SRPassiveRuntime.Instalar(this);
        }

        /// <summary>
        /// KIT-14F — liga o Adapter ao Core QUANDO o Core existe. Idempotente e segura a
        /// qualquer ordem de carga: com o Core ainda ausente devolve false, declara o
        /// estado "aguardando_core" e o Update tenta de novo. NUNCA acessa membro de Core
        /// nulo (era exatamente esse o NullReferenceException do run704).
        /// </summary>
        /// <summary>
        /// KIT-14F — LEITURA UNICA do Core. Fica num metodo proprio (NoInlining) para o
        /// vinculo ser reavaliado a cada quadro: a propriedade estatica nao pode virar valor
        /// fixo no codigo do chamador entre o primeiro quadro (sem Core) e os seguintes.
        /// </summary>
        [System.Runtime.CompilerServices.MethodImpl(
            System.Runtime.CompilerServices.MethodImplOptions.NoInlining)]
        private static CorePlugin? LerCore() => CorePlugin.Instancia;

        public bool TentarVincular()
        {
            if (_vinculado) return true;
            var core = LerCore();
            Kit14fDiagnostico = "Instancia=" + (core == null ? "null" : "ok")
                + " tipoVisivel=" + typeof(CorePlugin).Assembly.Location
                + " instanciaVisivel=" + (CorePlugin.Instancia == null ? "null" : "ok")
                + " porReflexao=" + (typeof(CorePlugin)
                    .GetProperty("Instancia", System.Reflection.BindingFlags.Public
                                            | System.Reflection.BindingFlags.Static)
                    .GetValue(null) == null ? "null" : "ok")
                + " viaLerCore=" + (core == null ? "null" : "ok");
            if (ReferenceEquals(core, null))
            {
                _estadoVinculo = "aguardando_core";
                if (!_avisouEsperaDoCore)
                {
                    _avisouEsperaDoCore = true;
                    Logger.LogWarning("[KIT04-SR] Core (com.gumatos.kit04.core) ainda nao inicializado: "
                        + "vinculo PENDENTE, o Adapter segue vivo e tenta no proximo quadro.");
                }
                return false;
            }

            // Inicializar managers (recebem CorePlugin agora CONFIRMADO)
            _telas = new SRScreenManager(core);
            _personagens = new SRCharacterManager(core);
            _owners = new SROwnerManager(core);
            _mapeamentos = new SRMappingManager(core);

            SRScreenManager.SetInstance(_telas);
            SRCharacterManager.SetInstance(_personagens);
            SROwnerManager.SetInstance(_owners);
            SRMappingManager.SetInstance(_mapeamentos);

            // KIT-05F (F8): ponte passiva reutilizando o PIPELINE LIMITADO do Core
            // (CorePlugin.Passivo). Opt-in: sem `passivoHabilitado=true`, Observar
            // devolve vazio e nada e registrado.
            _ponte = new PontePassivaRSTV(SRScreenManager.TelasMonitoradas,
                                          p_PassivoHabilitado.Value, core.Passivo);

            // KIT-14F: o estado do VINCULO e do vinculo, nao do patch. Marca o vinculo como
            // concluido ANTES de tentar o Harmony: uma excecao no patching deixava o Adapter
            // ligado mas SEM estado declarado (era o que o harness media em --parte1).
            _vinculado = true;
            _estadoVinculo = "ligado";

            // Aplica Harmony (patching de segurança) — falha NAO derruba o vinculo.
            try
            {
                var harmony = new Harmony(HarmonyId);
                harmony.PatchAll(typeof(SRAdapterPlugin));
                HarmonyEstado = "aplicado";
            }
            catch (Exception e)
            {
                HarmonyEstado = "falhou: " + e.GetType().Name + ": " + e.Message;
                Logger.LogWarning("[KIT04-SR] patch Harmony NAO aplicado: " + HarmonyEstado);
            }

            Logger.LogInfo("[KIT04-SR] Adapter carregado: vinculo com o Core concluido (desabilitado por padrão)");
            return true;
        }

        internal int UpdatesDoPlugin;
        internal int DestruicoesDoPlugin;
        internal void RelatarRuntime(string texto) => Logger.LogInfo("[KIT14F3] " + texto);
        private void OnDestroy()
        {
            DestruicoesDoPlugin++;
            RelatarRuntime("OnDestroy frame=" + Time.frameCount + " updates=" + UpdatesDoPlugin
                + " motores=" + SRPassiveRuntime.ContarMotores());
        }

        private void Update()
        {
            UpdatesDoPlugin++;
            // A trilha passiva pertence exclusivamente ao PlayerLoop: nunca duplica.
            if (p_PassivoHabilitado.Value) return;
            if (!TentarVincular() || !p_Habilitado.Value) return;
            var core = LerCore();
            if (ReferenceEquals(core, null) || !core.EstaHabilitado()) return;

            // Legado (KIT-04F): emite SOMENTE quando o estado muda (sem spam/frame).
            var telaAtual = _telas.CapturarEstadoAtual();
            string? nomeTela = telaAtual == null ? null : (string)telaAtual["tela"];
            if (nomeTela != _ultimaTela)
            {
                _ultimaTela = nomeTela;
                if (telaAtual != null)
                    core.RegistrarEvento("tela_detectada", "Tela identificada", telaAtual);
            }

            // Coleta de personagens: so registra quando o TOTAL muda.
            var chars = _personagens.ListarAtivos();
            int total = chars == null ? 0 : chars.Length;
            if (total != _ultimoTotalPersonagens)
            {
                _ultimoTotalPersonagens = total;
                if (total > 0)
                {
                    var evt = new Dictionary<string, object>
                    {
                        { "count", total },
                        { "timestamp", DateTime.Now.ToString("o") }
                    };
                    core.RegistrarEvento("personagens_lidos", $"Count={total}", evt);
                }
            }
        }

        /// <summary>
        /// KIT-14F — alimenta a trilha passiva (recorder) com o estado observado do quadro e
        /// devolve QUANTOS eventos foram registrados no Core. E o MESMO caminho que o Update
        /// usa; vive em metodo proprio para poder ser exercitado offline (o Update depende da
        /// engine para ler telas/clique).
        /// </summary>
        public int AlimentarPassivo(bool[] ativas, bool cliqueObservado, long agoraMs)
            => AlimentarPassivo(ativas, cliqueObservado, agoraMs, null, null);

        // A API offline continua sem procedencia runtime. Somente o motor que le a
        // engine entrega engine.frame/origem e pede captura dos eventos observados.
        internal int AlimentarPassivo(bool[] ativas, bool cliqueObservado, long agoraMs,
            Dictionary<string, object>? origem, Action<Dictionary<string, object>>? aoEvento)
        {
            if (!PassivoAutorizado() || _ponte == null) return 0;
            var core = LerCore();
            if (ReferenceEquals(core, null)) return 0;
            int registrados = 0;
            foreach (var ev in _ponte.Observar(ativas, cliqueObservado, agoraMs))
            {
                if (origem != null) ev["engine"] = new Dictionary<string, object>(origem);
                core.RegistrarEvento("passivo_" + ev["tipo"],
                                     "evento RSTV observado (passivo)", ev);
                registrados++;
                aoEvento?.Invoke(ev);
            }
            return registrados;
        }

        internal Dictionary<string, object> DiagnosticoPonte() => Json.Campos(
            "vinculado", _vinculado, "ponte_existe", _ponte != null,
            "ponte_habilitada", _ponte?.Habilitado, "transicoes", _ponte?.Transicoes,
            "mesmo_pipeline", ReferenceEquals(_ponte?.Pipeline, LerCore()?.Passivo));

        internal static bool PassivoAutorizado()
        {
            var core = LerCore();
            return p_Habilitado != null && p_Habilitado.Value
                && p_PassivoHabilitado != null && p_PassivoHabilitado.Value
                && !ReferenceEquals(core, null) && core.EstaHabilitado();
        }
    }
}
