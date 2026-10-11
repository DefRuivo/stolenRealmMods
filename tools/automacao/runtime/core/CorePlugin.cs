// KIT-04 Core - Plugin principal (genérico, sem dependência de jogo específico)
using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace KIT04Core
{
    /// <summary>
    /// Core genérico do KIT-04: independente de jogo, reutilizável para qualquer Unity.
    /// Configuração desabilitada por padrão (opt-in): enquanto `habilitado` for false,
    /// nenhum método de coleta executa e o resultado sai como NAO_EXERCITADO.
    /// </summary>
    [BepInPlugin("com.gumatos.kit04.core", "KIT-04 Core Genérico", "0.1.0")]
    public class CorePlugin : BaseUnityPlugin
    {
        private static CorePlugin? _instancia;
        public static CorePlugin Instancia => _instancia!;

        // Configurações (desabilitado por padrão — opt-in)
        private ConfigEntry<bool> _habilitado;
        private ConfigEntry<string> _caminhoSaida;
        private ConfigEntry<float> _orcamentoSegundos;
        private ConfigEntry<string> _hashFonteDeclarado;
        private ConfigEntry<string> _idSessao;
        private ConfigEntry<string> _ambiente;
        private ConfigEntry<int> _maxAmostras;
        private ConfigEntry<int> _maxEventos;
        private ConfigEntry<int> _passivoFilaMax;
        private ConfigEntry<int> _passivoRetencaoMax;
        private ConfigEntry<int> _passivoTetoCapturas;
        private ConfigEntry<int> _passivoTimeoutJanelaMs;

        // Estado interno
        private SessionImpl? _sessao;
        private EventosImpl? _eventos;
        private PictureCaptureImpl? _captura;
        private bool _primeiroUpdate = true;
        // KIT-14G-SEG1: garante UMA unica gravacao do evento `inicializacao`, pelo caminho
        // que realmente roda (`Awake`); o `Update` so chama de novo se este ja nao tiver rodado.
        private bool _inicializacaoRegistrada;

        /// <summary>
        /// Registra nova sessão com ID único e ambiente.
        /// </summary>
        public void RegistrarSessao(string idSessao, string ambiente)
        {
            _sessao = new SessionImpl(idSessao, DateTime.Now.ToString("o"), ambiente);
            _idSessao.Value = idSessao;
            _ambiente.Value = ambiente;
        }

        /// <summary>
        /// Retorna true se plugin está habilitado na configuração E sessão ativa existe.
        /// </summary>
        public bool EstaHabilitado()
        {
            return _habilitado.Value && _sessao?.EstaAtiva() == true;
        }

        /// <summary>
        /// Serviço de identidade do Core (contrato ICoreIdentidade, v1.0.0).
        /// </summary>
        public ICoreIdentidade Identidade { get; } = new IdentidadeDoCoreImpl();

        /// <summary>
        /// KIT-05F (F8): trilha passiva do Core — pipeline LIMITADO reutilizado
        /// pela ponte do Adapter SR (dedup por fonte, fila/retenção, teto de
        /// pedidos de captura, pausa e timeout com motivo).
        /// </summary>
        public PipelinePassivo Passivo { get; private set; } = new PipelinePassivo();

        /// <summary>
        /// Calcula identidade do Core (hash SHA256 da DLL).
        /// </summary>
        public Dictionary<string, object> CalcularIdentidade()
        {
            return Identidade.CalcularIdentidade(_hashFonteDeclarado.Value);
        }

        /// <summary>
        /// Registra evento no Core.
        /// </summary>
        public void RegistrarEvento(string tipo, string detalhe, Dictionary<string, object>? dados = null)
        {
            if (_eventos == null)
                _eventos = new EventosImpl(_maxEventos?.Value ?? 500);
            _eventos.RegistrarEvento(tipo, detalhe, dados);
        }

        /// <summary>
        /// KIT-05F (F8): registra um evento OBSERVADO na trilha passiva (limitada).
        /// Nada e emitido se o Core estiver desabilitado (opt-in).
        /// </summary>
        public Dictionary<string, object>? RegistrarEventoPassivo(string tipo,
            Dictionary<string, object>? dados = null, string? janela = null, long agoraMs = 0)
        {
            if (!EstaHabilitado())
                return null;
            return Passivo.Registrar(tipo, dados, janela, agoraMs);
        }

        /// <summary>KIT-05F: resumo da trilha passiva (limites/capturas/lacunas).</summary>
        public Dictionary<string, object> ResumoPassivo() => Passivo.Resumo();

        /// <summary>KIT-05F: eventos OBSERVADOS retidos na trilha passiva.</summary>
        public List<Dictionary<string, object>> EventosPassivos() => Passivo.Eventos();

        /// <summary>KIT-05F: materializa timeouts vencidos da trilha passiva.</summary>
        public List<Dictionary<string, object>> VerificarTimeoutsPassivos(long agoraMs)
            => Passivo.VerificarTimeouts(agoraMs);

        /// <summary>KIT-05F: quantos eventos do livro foram descartados pelo teto.</summary>
        public int EventosDescartados => _eventos?.Descartados ?? 0;

        /// <summary>
        /// Lê componentes genéricos do tipo T.
        /// Retorna null quando o Core está desabilitado OU quando nenhum componente do
        /// tipo existe na cena (AUSENTE ⇒ null, nunca Array.Empty e nunca valor inventado —
        /// spec §"Ler componentes").
        /// </summary>
        public T[]? LerComponentes<T>() where T : MonoBehaviour
        {
            if (!EstaHabilitado())
                return null;
            return new ComponentReaderImpl<T>().LerTodos();
        }

        /// <summary>
        /// Captura screenshot e salva em PNG.
        /// </summary>
        public bool CapturarPNG(string caminhoSaida, int largura, int altura)
        {
            if (!EstaHabilitado())
                return false;
            if (_captura == null)
                _captura = new PictureCaptureImpl();
            return _captura.CapturarPNG(caminhoSaida, largura, altura);
        }

        /// <summary>
        /// Retorna todos os eventos registrados.
        /// </summary>
        public List<Dictionary<string, object>> ObterEventos()
        {
            return _eventos?.ObterEventos() ?? new List<Dictionary<string, object>>();
        }

        /// <summary>
        /// Retorna resultado consolidado em JSON.
        /// Se desabilitado, retorna { "status": "NAO_EXERCITADO" }.
        /// </summary>
        public Dictionary<string, object> ResultadoFinal()
        {
            if (!EstaHabilitado())
                return Json.Campos("status", "NAO_EXERCITADO");

            var resultado = Json.Campos(
                "sessao", _sessao?.ObterIdSessao(),
                "identidade", CalcularIdentidade(),
                "eventos", ObterEventos(),
                "eventos_descartados", EventosDescartados,
                "passivo", Passivo.Resumo());

            var ultimaCaptura = _captura?.ObterUltimaCaptura();
            if (ultimaCaptura != null)
                resultado["ultima_captura_png"] = ultimaCaptura;

            return resultado;
        }

        private void Awake()
        {
            _instancia = this;
            Harmonizer = new Harmony("com.gumatos.kit04.core");

            // Configurações (desabilitado por padrão — opt-in; ver KIT-04F-parte01 §3)
            _habilitado = Config.Bind("Modo", "habilitado", false, "Habilita o Core. Sem ser true, nao executa coleta.");

            _caminhoSaida = Config.Bind("Modo", "caminhoSaida", "scratch/kit/", "Diretório de saída para arquivos gerados.");

            _orcamentoSegundos = Config.Bind("Modo", "orcamentoSegundos", 60f, "Tempo máximo para execução da coleta.");

            _hashFonteDeclarado = Config.Bind("Modo", "hashFonteDeclarado", "", "SHA256 da fonte declarada pelo driver (L1 AUD-1).");

            _idSessao = Config.Bind("Modo", "idSessao", "", "ID da sessão atual.");

            _ambiente = Config.Bind("Modo", "ambiente", "", "Ambiente de execução (dev/teste/prod).");

            _maxAmostras = Config.Bind("Modo", "maxAmostras", 100, "Máximo de amostras em inventários detalhados.");

            // KIT-05F (F8): teto/retenção do livro de eventos (antes: lista sem teto).
            _maxEventos = Config.Bind("Modo", "maxEventos", 500, "Máximo de eventos retidos pelo Core (teto com descarte contado).");

            // KIT-05F (F8): limites EXPLÍCITOS da trilha passiva (pipeline limitado).
            _passivoFilaMax = Config.Bind("Passivo", "filaMax", 200, "Fila de eventos observados (limite).");
            _passivoRetencaoMax = Config.Bind("Passivo", "retencaoMax", 200, "Eventos retidos + teto dos estados auxiliares.");
            _passivoTetoCapturas = Config.Bind("Passivo", "tetoCapturas", 10, "Teto de PEDIDOS de captura (não de confirmações).");
            _passivoTimeoutJanelaMs = Config.Bind("Passivo", "timeoutJanelaMs", 1500, "Timeout para derivar falha_clique_sem_janela.");

            // Iniciar sessão
            var id = string.IsNullOrEmpty(_idSessao.Value) ? $"sessao-{Guid.NewGuid():N}" : _idSessao.Value;
            RegistrarSessao(id, _ambiente.Value ?? "dev");

            // KIT-05F (F8): pipeline passivo do Core (reutilizado pela ponte do Adapter).
            Passivo = new PipelinePassivo(_passivoFilaMax.Value, _passivoRetencaoMax.Value,
                _passivoTetoCapturas.Value, _passivoTimeoutJanelaMs.Value, 0, id);

            // KIT-14G-SEG1: o evento de inicializacao NAO pode depender do `Update()`.
            // MEDIDO nesta bancada (Stolen Realm + BepInEx 5.4.23.5): a Unity DESTROI o
            // GameObject do plugin na 1a carga de cena (padrao provado no CAP-1: `OnDestroy`
            // em t=2,02s) — o `Update()` do plugin nunca ticka, o livro de eventos nunca era
            // criado (`_eventos == null`) e `ResultadoFinal()` devolvia `"eventos": []` mesmo
            // com `Modo/habilitado = true`. O `Awake()` e sincrono ao `AddComponent` do
            // chainloader (antes de qualquer cena) e sempre roda — o proprio recorder ja
            // provava isso pelo bloco `passivo`/`identidade`, que so existem se o `Awake` rodou.
            GarantirInicializacao();
        }

        private void Update()
        {
            if (_primeiroUpdate)
            {
                _primeiroUpdate = false;
                // Diagnostico explicito: so aparece no log se o `Update()` do plugin
                // realmente tickar (nos jogos onde o GameObject sobrevive a 1a cena).
                Logger.LogInfo("KIT-04 Core: primeiro Update() do plugin executado "
                             + "(o GameObject sobreviveu a troca de cena).");
                GarantirInicializacao();
            }
        }

        /// <summary>
        /// KIT-14G-SEG1: registra o evento `inicializacao` UMA vez, por caminho garantido
        /// (`Awake`) e nao pelo `Update()` — que a Unity deixa de chamar quando destroi o
        /// GameObject do plugin na primeira carga de cena.
        /// </summary>
        private void GarantirInicializacao()
        {
            if (_inicializacaoRegistrada)
                return;
            _inicializacaoRegistrada = true;
            RegistrarEvento("inicializacao", "Core plugin carregado");
        }

        private void OnDestroy()
        {
            Harmonizer.PatchAll();
        }

        private Harmony? Harmonizer { get; set; }
    }
}

// Implementações internas

namespace KIT04Core
{
    internal class SessionImpl : ICoreSession
    {
        public SessionImpl(string idSessao, string data, string ambiente)
        {
            IdSessao = idSessao;
            DataHora = data;
            Ambiente = ambiente;
            Ativo = true;
        }

        public void Registrar(string idSessao, string data, string ambiente)
        {
            IdSessao = idSessao;
            DataHora = data;
            Ambiente = ambiente;
            Ativo = true;
        }

        public string ObterIdSessao() => IdSessao;
        public bool EstaAtiva() => Ativo;

        private string IdSessao { get; set; } = "";
        public string DataHora { get; set; } = "";
        public string Ambiente { get; set; } = "";
        private bool Ativo { get; set; }
    }

    internal class EventosImpl : ICoreEvento
    {
        private readonly List<Dictionary<string, object>> _lista = new();
        private readonly int _max;
        private int _descartados;

        /// <summary>KIT-05F (F8): teto EXPLICITO do livro (antes: lista sem teto).</summary>
        public EventosImpl(int maxEventos = 500)
        {
            _max = maxEventos > 0 ? maxEventos : 500;
        }

        public int Teto => _max;
        public int Descartados => _descartados;

        public void RegistrarEvento(string tipo, string detalhe, Dictionary<string, object>? dados = null)
        {
            var evento = Json.Campos(
                "tipo", tipo,
                "detalhe", detalhe,
                "timestamp", DateTime.Now.ToString("o"),
                "dados", dados ?? new Dictionary<string, object>());
            _lista.Add(evento);
            while (_lista.Count > _max)
            {
                _lista.RemoveAt(0);
                _descartados++;
            }
        }

        public List<Dictionary<string, object>> ObterEventos() => _lista;
        public void LimparEventos() { _lista.Clear(); _descartados = 0; }
    }

    internal class PictureCaptureImpl : IPictureCapture
    {
        private Dictionary<string, object>? _ultima;

        public bool CapturarPNG(string caminhoSaida, int largura, int altura)
        {
            try
            {
                // Verificar disponibilidade do módulo
                if (!EstaDisponivel())
                    return false;

                // Capturar tela como Texture2D
                UnityEngine.Texture2D texture = UnityEngine.ScreenCapture.CaptureScreenshotAsTexture();

                // Converter para PNG
                var bytes = ImageConversion.EncodeToPNG(texture);
                if (bytes != null)
                {
                    System.IO.File.WriteAllBytes(caminhoSaida, bytes);
                    _ultima = Json.Campos(
                        "caminho", caminhoSaida,
                        "tamanho_bytes", bytes.Length,
                        "timestamp", DateTime.Now.ToString("o"),
                        "status", "sucesso");
                    UnityEngine.Object.Destroy(texture);
                    return true;
                }

                UnityEngine.Object.Destroy(texture);
                return false;
            }
            catch
            {
                _ultima = Json.Campos(
                    "caminho", caminhoSaida,
                    "timestamp", DateTime.Now.ToString("o"),
                    "status", "erro",
                    "erro", "excecao na captura");
                return false;
            }
        }

        public bool EstaDisponivel()
        {
            // Verificar se módulo de captura existe
            return typeof(UnityEngine.ScreenCapture).GetMethod("CaptureScreenshotAsTexture") != null;
        }

        public Dictionary<string, object>? ObterUltimaCaptura() => _ultima;
    }
}
