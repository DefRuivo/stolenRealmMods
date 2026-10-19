// AUT-4 — COLETOR RUNTIME (instrumento OPT-IN, SOMENTE LEITURA).
//
// Le do OBJETO VIVO do jogo (nao de print, nao de OCR): texto bruto + renderizado,
// ativo/visivel, fonte/material/shader/keywords, cores, geometria de tela, contexto
// de personagem/tela e OWNERS Harmony. Pede o PNG pela API do Unity quando autorizado.
//
// SEGURANCA:
//   * `Autorizado` default FALSE: sem ela o probe grava {"status":"NAO_EXERCITADO"} e
//     NAO instala motor, NAO le, NAO navega, NAO tira print.
//   * `Sessao` vem do DRIVER (no .cfg) e entra no JSON: e o que liga a evidencia a
//     ESTA rodada (A1 da AUT-4R2). Sem a chave, vale o carimbo local (fallback).
//   * `DemostrarTooltip` (default FALSE) e a porta OPT-IN de IDA-E-VOLTA: chama o
//     handler REAL `Tooltip.ShowTooltip(marcador)` e RELE `Tooltip.Title` — LEITURA
//     reproduzivel, nunca simulacao do produto (A6 da AUT-4R2).
//   * KIT-R0F/F5 — OBSERVAR NAO AUTORIZA ESCREVER: com `DemostrarTooltip=true` e
//     `AutorizaEscritaTooltip=false` (default) a porta fica em modo PASSIVO (le o
//     tooltip vivo, NAO chama handler nenhum). Escrever exige a autorizacao
//     ESPECIFICA `AutorizaEscritaTooltip=true`, e nesse modo o titulo/corpo originais
//     sao lidos ANTES e RESTAURADOS depois, com a restauracao conferida no JSON.
//   * KIT-R0F/F3 — CORRELACAO evento x quadro x PNG: `eventos_frame` traz o
//     Time.frameCount de cada evento (leitura/coleta/PNG solicitado+concluido) e
//     `prints_detalhe` traz pedido/conclusao de CADA PNG. `aplicacao.roteiro_frame` e
//     metadado do ARRANQUE e `quadros_ate_a_ui` conta ticks internos do instrumento:
//     nenhum dos dois e o quadro da coleta.
//   * Driver INDEPENDENTE do Update do plugin (que a Unity DESTROI na 1a cena): o
//     motor e injetado no PlayerLoop do Unity (padrao provado no CAP-1) e, como
//     reforco, num MonoBehaviour criado preguicosamente com cena viva.
//   * Espera de ESTADO (UI com texto renderizado), com teto de tempo — nao sleep cego.
//   * Manifest dos artefatos + ROLLBACK dos arquivos que a rodada cria (inclusive o
//     .cfg que nasce sozinho). A rotina/orquestrador consome isto e restaura EXATO.
//
// Reusa o padrao do CAP-1 (scratch/cap1/CapProbe); nao o reconstroi.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using System.Text;
using BepInEx;
using BepInEx.Bootstrap;
using BepInEx.Configuration;
using HarmonyLib;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Aut4Probe
{
    [BepInPlugin(Guid, "AUT-4 Probe (coletor runtime, instrumento)", Versao)]
    public partial class Aut4ProbePlugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.aut4probe";
        public const string Versao = "0.1.0";

        // --- config ---
        private ConfigEntry<bool> _autorizado;
        private ConfigEntry<string> _outDir;
        private ConfigEntry<float> _orcamento;
        private ConfigEntry<bool> _navegar;
        private ConfigEntry<string> _perfilDir;
        private ConfigEntry<string> _hashFonte;
        private ConfigEntry<int> _maxTextos;
        // A1: identidade da RODADA, gerada pelo driver e injetada no .cfg. Sem esta
        // chave o JSON nao pertence a nenhuma rodada identificavel.
        private ConfigEntry<string> _sessaoCfg;
        // A6: porta OPT-IN de ida-e-volta (LEITURA reproduzivel) — default FALSE.
        private ConfigEntry<bool> _demostrar;
        private ConfigEntry<string> _marcador;

        internal static Aut4ProbePlugin Instancia;
        private Harmony _harmony;

        // --- INT-R1-C2-I1 (entregavel B): GATILHO observacional pela ponte da API ---
        // O patch proprio em OptionsManager.Localize saiu: quem observa aquele alvo agora e o hook
        // `ui.localized` da API, entregue pela ponte `Gumatos.KitApiBridge.AUT4` (assembly companheiro
        // OPCIONAL, carregado por NOME EXATO). Sem a ponte — ou com `PonteApiHook=false`, o default —
        // o gatilho por localizacao nao existe e sobram os dois drivers que ja existiam:
        // GUIManager.Update e o PlayerLoop.
        private ConfigEntry<bool> _ponteApiCfg;
        private IDisposable _ponteApi;

        // --- RSTV (AUT5-F1): GUARDA de leitura somente, por observacao ---
        // `snapshot_*`   = estado do personagem do modal (skills/pontos) no INICIO
        //                  e no FIM da leitura: sem mudanca, nada foi gasto/gravado.
        // `tooltip_*`    = pai/indice do tooltip ANTES (1o estado observado, antes
        //                  de qualquer clique) e DEPOIS (fim da leitura): e a prova
        //                  de reparent/restauracao (RSTV-21).
        // `janelas_*`    = quantas janelas do RSTV ativas ALEM da primeira (>0 e a
        //                  duplicacao).
        // Regra do contrato: membro que nao existir sai `null` -> AUSENTE no
        // avaliador -> NAO_EXERCITADO, NUNCA OK.
        private object _personagemDoModal;
        private Dictionary<string, object> _snapshotAntes;
        private Dictionary<string, object> _snapshotDepois;
        private string _tooltipPaiAntes;
        private object _tooltipIndiceAntes;
        private bool _tooltipAntesLido;
        private string _tooltipPaiDepois;
        private object _tooltipIndiceDepois;
        private object _janelasDuplicadas;

        // --- KIT-R0F/F3: CORRELACAO evento x quadro x PNG ---
        // `_eventosFrame` = {nome do evento -> Time.frameCount no instante}. O antigo
        // `aplicacao.roteiro_frame` e metadado do ARRANQUE (montado no Awake) e
        // `quadros_ate_a_ui` conta TICKS INTERNOS do instrumento: NENHUM dos dois e o
        // quadro em que a leitura ou o PNG aconteceram. Sem estes campos, leitura e PNG
        // ficavam sem quadro, e o PNG sem pedido/conclusao declarados (o unico elo com
        // os pixels era a lista de arquivos).
        private readonly Dictionary<string, object> _eventosFrame = new Dictionary<string, object>();
        // `_printsDetalhe` = {nome do print -> {solicitado_frame, concluido_frame, existe, bytes}}.
        private readonly Dictionary<string, object> _printsDetalhe = new Dictionary<string, object>();

        // --- KIT-R0F/F5: modo PASSIVO x DEMONSTRADOR ATIVO ---
        // `DemostrarTooltip` autoriza OBSERVAR a ida-e-volta; ESCREVER no jogo exige
        // autorizacao SEPARADA e explicita. Sem ela o probe NAO chama ShowTooltip.
        private ConfigEntry<bool> _autorizaEscrita;

        private readonly Dictionary<string, object> _res = new Dictionary<string, object>();
        private readonly Dictionary<string, object> _passos = new Dictionary<string, object>();
        private readonly List<string> _marcos = new List<string>();
        private readonly List<object> _observacoes = new List<object>();
        private readonly List<string> _arquivosDePrint = new List<string>();

        private string _dir;
        private string _sessao;
        private float _t0;
        private float _orcamentoSeg;
        private long _ticks;
        private int _fase;
        private int _quadros;
        private bool _concluido;
        private bool _tentouMotor;
        private string _printAtual;
        private bool _autorizadoOk;

        private static readonly string[] NomesDeAlvo =
        { "Title", "Description", "Subtitle", "BigText", "FooterText", "IfEquippedText", "BossName", "playerName" };

        private void Awake()
        {
            Instancia = this;
            _autorizado = Config.Bind("Geral", "Autorizado", false,
                "Coleta runtime OPT-IN. Default false: sem isto o probe NAO le, NAO navega e NAO tira print.");
            _outDir = Config.Bind("Geral", "OutDir",
                @"C:\dev\stolen-realm\scratch\aut4\out", "Pasta de saida (JSON + PNG).");
            _orcamento = Config.Bind("Geral", "OrcamentoSegundos", 120f,
                "Teto de tempo depois que a UI existe. Passado isso o probe encerra com o que leu.");
            _navegar = Config.Bind("Geral", "Navegar", false,
                "Navegacao por dentro (onClick do botao). Default DESLIGADO.");
            // KIT-14F (rodada 2): o teto da espera por alvo era uma constante sem porta —
            // `_navTentativasMax` existia e NUNCA era ligada (nem no .cfg). Agora tem opcao
            // propria; sem ela vale o default do produto.
            _navTentativasMax = Config.Bind("Geral", "NavegarTentativasMax", NavegacaoTentativasMax,
                "KIT-14F: teto de QUADROS que a navegacao por handler espera o alvo 'Skills' "
                + "aparecer antes de declarar esgotado e seguir para o print.");
            // KIT-14G — ROTEIRO EM ESTAGIOS. O alvo do RSTV vive no HUD da RUN: para o alvo
            // EXISTIR e preciso atravessar menu -> Play -> criacao -> selecao. A busca unica por
            // 'Skills' (KIT-14F) nunca podia chegar la. O roteiro e uma LISTA ORDENADA de trechos
            // de rotulo/nome, no .cfg (sem recompilar para ajustar), e o mapa do que cada tela
            // oferece sai no campo `botoes_vistos` do JSON da rodada.
            _navRota = Config.Bind("Geral", "NavegarRota", "",
                "KIT-14G: ROTEIRO de navegacao em ESTAGIOS separados por ';'. Cada estagio casa um "
                + "trecho (case-insensitive) do rotulo/nome de um botao ATIVO, na ordem. Ex.: "
                + "'Play;Roguelike;Novo Jogo'. Vazio = comportamento historico (procurar o alvo direto).");
            _navAlvoNome = Config.Bind("Geral", "NavegarAlvoNome", "RstvRunSkillTreeButton",
                "KIT-14G: NOME do OBJETO do alvo final. O botao do RSTV nao tem rotulo (e um glifo, "
                + "`RunButton.cs` RSTV-30), entao casar por nome e o unico jeito; rotulo contendo "
                + "'Skills' tambem casa.");
            // KIT14G-SEG2-FIX: seguro mesmo com CliqueFisico=false em configs antigas.
            // O fallback historico exige desativar EXPLICITAMENTE EsperarInteractable.
            _esperarInteractable = Config.Bind("Geral", "EsperarInteractable", true,
                "KIT14G-SEG2-FIX: espera componente habilitado, interactable=true e "
                + "IsInteractable() antes de onClick.Invoke(). Default TRUE, inclusive sem chave. "
                + "FALSE com CliqueFisico=false restaura o fallback historico INSEGURO "
                + "(somente activeInHierarchy), apenas para diagnostico explicitamente autorizado.");
            _cliqueFisico = Config.Bind("Geral", "CliqueFisico", false,
                "KIT-14G-SEG2: gate ADICIONAL de CanvasGroup.blocksRaycasts na hierarquia. "
                + "TRUE tambem exige habilitado/interactable/IsInteractable(), mesmo se "
                + "EsperarInteractable=false. Nao prova raycast, oclusao ou clique humano. "
                + "Default FALSE; nao desativa a espera segura por interactable.");
            _cliqueFisicoEstavel = Config.Bind("Geral", "CliqueFisicoEstavel", 0,
                "KIT-14G-SEG2: quadros CONSECUTIVOS em que o alvo precisa estar clicavel antes do "
                + "clique (0 = clica no 1o quadro em que for clicavel). Serve para esperar a tela "
                + "assentar de verdade.");
            _silencioAposClique = Config.Bind("Geral", "SilencioAposClique", false,
                "KIT-14G-SEG2 (DIAGNOSTICO): quando TRUE, o instrumento PARA de tocar na engine "
                + "(nenhuma varredura, leitura ou print) assim que o ULTIMO estagio do roteiro e "
                + "clicado — so marcos em arquivo. Separa 'a run derrubada pelo proprio inicio' de "
                + "'trabalho do instrumento durante a carga da cena'.");
            _rota.Clear();
            foreach (var trecho in (_navRota.Value ?? string.Empty).Split(';'))
            {
                var limpo = trecho.Trim();
                if (limpo.Length > 0) _rota.Add(limpo);
            }
            _perfilDir = Config.Bind("Geral", "PerfilDir", "",
                "Perfil do r2modman (para o manifesto de rollback).");
            _hashFonte = Config.Bind("Geral", "HashFonte", "",
                "sha256 do fonte/DLL medido; entra em cada observacao (procedencia runtime).");
            _maxTextos = Config.Bind("Geral", "MaxTextos", 400, "Teto de TMP_Text lidos por rodada.");
            _sessaoCfg = Config.Bind("Geral", "Sessao", "",
                "Identidade da RODADA, gerada pelo driver. Vence o carimbo local: e ela que "
                + "liga a evidencia a esta rodada (A1).");
            _demostrar = Config.Bind("Geral", "DemostrarTooltip", false,
                "Porta OPT-IN de ida-e-volta: chama Tooltip.ShowTooltip(marcador) e RELE o titulo. "
                + "E LEITURA (nao simulacao do produto) e o default e FALSE. (A6)");
            _marcador = Config.Bind("Geral", "MarcadorIdaEVolta", "",
                "Marcador unico da ida-e-volta (gerado pelo driver).");
            _autorizaEscrita = Config.Bind("Geral", "AutorizaEscritaTooltip", false,
                "KIT-R0F/F5: autorizacao ESPECIFICA para ESCREVER no tooltip (chamar o handler "
                + "ShowTooltip). Permissao de OBSERVACAO (DemostrarTooltip) NAO autoriza escrita: "
                + "default FALSE. Quando true, o titulo/corpo originais sao lidos ANTES e "
                + "RESTAURADOS depois, com conferencia explicita da restauracao.");

            _ponteApiCfg = Config.Bind("Geral", "PonteApiHook", false,
                "OPT-IN (default FALSE): consumir o hook ui.localized entregue pela ponte "
                + "Gumatos.KitApiBridge.AUT4 (assembly companheiro, carregado por nome EXATO). O patch "
                + "proprio em OptionsManager.Localize foi REMOVIDO; sem esta ponte o gatilho por "
                + "localizacao nao existe e restam GUIManager.Update e o PlayerLoop.");
            ConfigurarRstv();
            _dir = _outDir.Value;
            _orcamentoSeg = _orcamento.Value;
            _t0 = Time.realtimeSinceStartup;
            // A1: a sessao do .cfg (do driver) VENCE o carimbo local; sem ela (rodada
            // manual) o carimbo local fica como fallback declarado.
            _sessao = string.IsNullOrWhiteSpace(_sessaoCfg.Value)
                ? DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture)
                : _sessaoCfg.Value;

            try { Directory.CreateDirectory(_dir); }
            catch (Exception e) { Logger.LogError("AUT4 PROBE: pasta de saida '" + _dir + "': " + e.Message); }

            _res["rotina"] = "AUT-4";
            _res["esquema"] = "AUT-4/1";
            _res["instrumento"] = "AUT4Probe " + Versao + " (BepInEx/plugins/AUT4Probe; removido no fim)";
            _res["aviso"] = "Coleta SOMENTE leitura; nenhum mod do pacote foi alterado.";
            _res["sessao"] = _sessao;
            _res["hash_fonte"] = _hashFonte.Value;
            // L1 (AUD-1): IDENTIDADE do instrumento dentro do proprio JSON — o hash do
            // fonte declarado pelo driver E o sha256 da DLL calculado AGORA, no runtime,
            // sobre o assembly carregado. Sem isto a evidencia nao diz QUAL binario leu.
            _res["identidade"] = IdentidadeDoProbe.Identidade(_hashFonte.Value);
            _res["aplicacao"] = Aplicacao();
            _res["passos"] = _passos;
            _res["observacoes"] = _observacoes;

            if (!_autorizado.Value)
            {
                // GATE DE AUTORIZACAO: sem opt-in nao ha coleta nenhuma.
                _res["status"] = "NAO_EXERCITADO";
                _res["motivo"] = "coleta NAO autorizada (Autorizado=false): nenhuma leitura, PNG ou navegacao.";
                _res["fase"] = "nao-exercitado";
                Marco("AUT4 PROBE: SEM autorizacao (Autorizado=false) — grava NAO_EXERCITADO e nao toca em nada.");
                Escrever();
                return;
            }

            _autorizadoOk = true;
            _res["status"] = "INICIADO";
            _res["fase"] = "carregado";
            Marco("AUT4 PROBE " + Versao + " carregado (coleta AUTORIZADA, somente leitura).");

            try
            {
                _harmony = new Harmony(Guid);
                Gancho("GUIManager", "Update");
                // INT-R1-C2-I1: `GanchoTodos("OptionsManager","Localize")` SAIU daqui. OptionsManager.
                // Localize e exatamente o alvo do hook `ui.localized` (api/Core/Contracts.cs:63): quem
                // instala o patch daquele alvo agora e a API (produtor), e o probe so consome o evento
                // pela ponte opcional. Medido no binario alvo com api/tools/Inspect + ilspycmd, o tipo
                // tem UMA assinatura de Localize — a mesma que a API declara, entao a COBERTURA nao
                // muda; muda o dono do patch.
                LigarPonteOpcional();
            }
            catch (Exception e) { Logger.LogError("AUT4 PROBE: ganchos: " + e.GetType().Name + ": " + e.Message); }

            // DRIVER independente do Update do plugin: injeta no PlayerLoop.
            InstalarNoPlayerLoop();
            Escrever();
        }

        // ------------------------------------------------------------ motor

        private void InstalarNoPlayerLoop()
        {
            try
            {
                var loop = UnityEngine.LowLevel.PlayerLoop.GetCurrentPlayerLoop();
                var meu = new UnityEngine.LowLevel.PlayerLoopSystem
                {
                    type = typeof(Aut4ProbePlugin),
                    updateDelegate = new UnityEngine.LowLevel.PlayerLoopSystem.UpdateFunction(DelegadoDeQuadro)
                };
                for (int i = 0; i < loop.subSystemList.Length; i++)
                {
                    if (loop.subSystemList[i].type != typeof(UnityEngine.PlayerLoop.Update)) continue;
                    var sub = loop.subSystemList[i].subSystemList ?? new UnityEngine.LowLevel.PlayerLoopSystem[0];
                    var novo = new UnityEngine.LowLevel.PlayerLoopSystem[sub.Length + 1];
                    Array.Copy(sub, novo, sub.Length);
                    novo[sub.Length] = meu;
                    loop.subSystemList[i].subSystemList = novo;
                    UnityEngine.LowLevel.PlayerLoop.SetPlayerLoop(loop);
                    Marco("AUT4 PROBE: subsistema injetado no PlayerLoop (Update) — motor por quadro ativo.");
                    return;
                }
                Marco("AUT4 PROBE: NAO achei o subsistema Update no PlayerLoop.");
            }
            catch (Exception e)
            {
                Logger.LogWarning("AUT4 PROBE: injecao no PlayerLoop falhou: " + e.GetType().Name + ": " + e.Message);
            }
        }

        private void DelegadoDeQuadro() { try { Tick("playerloop"); } catch { } }

        private void Gancho(string tipo, string metodo)
        {
            try
            {
                var t = Tipo(tipo);
                if (t == null) { Marco("AUT4 PROBE: tipo '" + tipo + "' NAO encontrado — gancho pulado."); return; }
                var alvo = t.GetMethod(metodo, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static, null, Type.EmptyTypes, null);
                if (alvo == null) { Marco("AUT4 PROBE: '" + tipo + "." + metodo + "()' NAO existe — gancho pulado."); return; }
                Aplicar(alvo, tipo + "." + metodo + "()");
            }
            catch (Exception e) { Logger.LogWarning("AUT4 PROBE: gancho " + tipo + "." + metodo + ": " + e.Message); }
        }

        /// <summary>INT-R1-C2-I1 (entregavel B) — gatilho OPCIONAL pela ponte da API.
        /// Carrega o assembly companheiro por NOME EXATO (`Gumatos.KitApiBridge.AUT4`), dentro de
        /// try/catch, atras da config `PonteApiHook` (default FALSE) — o mesmo padrao de opt-in que o
        /// probe ja usa no gate de autorizacao. Ausente, desligada ou recusada: NENHUMA excecao escapa
        /// e o comportamento e o de hoje (sem gatilho por localizacao).
        /// Por que `Assembly.Load` aqui e nao na ponte do kit: a regra "No assembly loading, script
        /// execution, authorization" (SDK/RegistryV1.cs:47-48) protege o contrato de EXTENSOES do kit;
        /// o probe e instrumento de bancada e uma referencia dura o deixaria sem carregar sempre que a
        /// API nao estivesse instalada.
        /// O callback chega no MESMO thread em que o postfix chegava antes (o Signal publica no thread
        /// do hook — api/Core/Contracts.cs:79), entao o despacho de tick nao muda de natureza.</summary>
        private void LigarPonteOpcional()
        {
            // B3 (revisao independente, rodada 1): com a config em FALSE — o DEFAULT — nada e
            // emitido, nem marco nem chave no JSON: a saida default e literalmente a de hoje
            // (criterio de aceite 3). Com TRUE, todo marco abaixo pertence ao caminho OPT-IN.
            if (!_ponteApiCfg.Value) return;
            try
            {
                var companheiro = Assembly.Load("Gumatos.KitApiBridge.AUT4");
                var tipo = companheiro.GetType("Gumatos.KitApiBridge.AUT4.PonteAut4", false);
                if (tipo == null) { Marco("AUT4 PROBE: companheiro sem PonteAut4 — ponte desligada."); return; }
                var ligar = tipo.GetMethod("Ligar", BindingFlags.Public | BindingFlags.Static, null,
                    new[] { typeof(Action<string>), typeof(Func<string>), typeof(Func<bool>) }, null);
                if (ligar == null) { Marco("AUT4 PROBE: PonteAut4.Ligar com assinatura diferente — ponte desligada."); return; }
                _ponteApi = (IDisposable)ligar.Invoke(null, new object[]
                {
                    (Action<string>)(evento => { try { Tick("hook:" + evento); } catch { } }),
                    (Func<string>)(() => _sessao),
                    (Func<bool>)(() => _autorizadoOk)
                });
                Marco("AUT4 PROBE: ponte da API ligada — gatilho por hook ui.localized (observacional).");
            }
            catch (Exception e)
            {
                _ponteApi = null;
                Logger.LogWarning("AUT4 PROBE: ponte da API indisponivel: " + e.GetType().Name);
                Marco("AUT4 PROBE: ponte da API indisponivel (" + e.GetType().Name + ") — comportamento de hoje.");
            }
        }

        private void Aplicar(MethodBase alvo, string rotulo)
        {
            try
            {
                var post = new HarmonyMethod(typeof(Aut4ProbePlugin).GetMethod("PostfixDoGancho",
                    BindingFlags.Static | BindingFlags.NonPublic));
                _harmony.Patch(alvo, postfix: post);
                Marco("AUT4 PROBE: gancho aplicado em " + rotulo);
            }
            catch (Exception e) { Logger.LogWarning("AUT4 PROBE: patch em " + rotulo + " falhou: " + e.Message); }
        }

        private static void PostfixDoGancho()
        {
            // GUARDA DO CLR (ReferenceEquals), nao o operador == da Unity: o
            // GameObject do plugin e DESTRUIDO na 1a cena e vira "fake null"; com o
            // operador da Unity o gancho DISPARAVA e o guarda engolia a chamada —
            // sintoma identico a "o gancho nao roda" (achado A3 da AUT-4R).
            try { var i = Instancia; if (ReferenceEquals(i, null)) return; i.Tick("gancho"); } catch { }
        }

        private void CriarMotor()
        {
            if (_tentouMotor) return;
            _tentouMotor = true;
            try
            {
                var go = new GameObject("AUT4Probe_Motor");
                DontDestroyOnLoad(go);
                go.AddComponent<MotorDoProbe>();
                Marco("AUT4 PROBE: motor proprio criado (GameObject vivo) — Update por quadro como reforco.");
            }
            catch (Exception e) { Logger.LogWarning("AUT4 PROBE: motor proprio: " + e.Message); }
        }

        private void Update() { if (_autorizadoOk) Tick("BepInEx.Update"); }

        internal void Tick(string origem)
        {
            if (_concluido || !_autorizadoOk) return;
            _ticks++;
            try
            {
                if (_silencio)
                {
                    // KIT-14G-SEG2 (DIAGNOSTICO): SILENCIO — depois do clique que inicia a run o
                    // instrumento NAO toca em mais nada da engine (nem varredura de botoes, nem
                    // leitura, nem print). Se o processo morre mesmo assim, a morte NAO e do
                    // trabalho do instrumento: e do inicio da run. Fica so o marco de vida, no
                    // arquivo proprio, para datar a morte.
                    _quadrosSilencio++;
                    if (_quadrosSilencio == 1 || _quadrosSilencio % 30 == 0)
                    {
                        MarcoClique("silencio_quadro=" + QuadroAtual() + " t=" + TempoSilencio()
                                    + " ticks_em_silencio=" + _quadrosSilencio);
                        Escrever();
                    }
                    return;
                }
                if (_ticks <= 3) Marco("AUT4 PROBE: tick via " + origem + " (quadro " + _ticks + ")");
                if (!_tentouMotor) CriarMotor();
                if (_fase > 0 && Time.realtimeSinceStartup - _t0 > _orcamentoSeg + 90f)
                {
                    _res["status"] = "ORCAMENTO_ESTOURADO";
                    Marco("AUT4 PROBE: orcamento de tempo estourado — encerrando com o que ja foi lido.");
                    Finalizar();
                    return;
                }
                Passo();
            }
            catch (Exception e)
            {
                _passos["tick.fase" + _fase] = Json.Campos("erro", e.GetType().Name + ": " + e.Message);
                _res["status"] = "ERRO";
                _concluido = true;
                Escrever();
            }
        }

        // KIT-14F (rodada 2) — A NAVEGACAO TEM FASE PROPRIA.
        // Na rodada 1 `TentarNavegar()` era chamado UMA vez dentro do `case F_LEITURA`
        // (fase de quadro unico) e o `Ir(F_PRINT1)` logo abaixo era INCONDICIONAL: em
        // producao a rotina tentava uma vez, via `botoes_ativos=0` (tela de LOADING do
        // run704) e seguia para o print — o teto e o ramo `esgotado` eram INALCANCAVEIS.
        // Agora o PROPRIO driver (`Tick -> Passo`, um `Passo` por quadro) reinvoca
        // `TentarNavegar()` quadro a quadro em `F_NAVEGACAO`, ate o alvo aparecer ou o
        // teto esgotar. O laco mora no produto, nao no teste.
        private const int F_ESPERA_UI = 0, F_LEITURA = 1, F_PRINT1 = 2, F_FINAL = 3, F_PRINT2 = 4,
                          F_NAVEGACAO = 5;

        /// <summary>KIT-14F (rodada 2) — `Passo` e o DRIVER: UM passo por QUADRO, chamado pelo
        /// `Tick` (PlayerLoop / `Update` / ganchos). Ele agora e um DESPACHANTE: cada fase vive
        /// num metodo proprio, com o corpo movido INTEIRO (comportamento igual ao de antes).
        /// O motivo nao e estetico: com o `switch` de ~110 linhas, uma chamada de engine
        /// inlinada em QUALQUER fase inutilizava o metodo todo fora do jogo, e nao havia como
        /// um teste dirigir o passo por quadro. Cada fase agora e um passo NOMEADO do driver.</summary>
        private void Passo()
        {
            switch (_fase)
            {
                case F_ESPERA_UI: PassoEsperaUi(); break;
                case F_LEITURA: PassoLeitura(); break;
                case F_NAVEGACAO: PassoNavegacao(); break;
                case F_PRINT1: PassoPrint1(); break;
                case F_FINAL: PassoFinal(); break;
                case F_PRINT2: PassoPrint2(); break;
            }
        }

        private void PassoEsperaUi()
        {
            if (_quadros == 0) { _res["fase"] = "aguardando-ui"; Escrever(); }
            _quadros++;
            bool ui = false, temTexto = false;
            try { ui = UiExiste(); } catch { }
            try { temTexto = ui && TemTextoVisivel(); } catch { }
            if (ui && temTexto)
            {
                Evento("ui_pronta");
                _passos["aguardou_ui"] = Json.Campos("ok", true, "quadros_ate_a_ui", _quadros,
                    "quadros_ate_a_ui_unidade", "ticks do PROPRIO instrumento (contador do probe); NAO e Time.frameCount",
                    "frame_count_da_ui", Time.frameCount,
                    "criterio", "GUIManager.instance.tooltip != null E existe TMP_Text ATIVO na hierarquia com GetParsedText() nao vazio — criterio de COMPONENTE (nao prova pixel desenhado)");
                _passos["mods_carregados"] = ModsCarregados();
                _passos["estado_da_tela"] = EstadoDaTela();
                // RSTV/AUT5-F1: o "antes" do tooltip e o PRIMEIRO estado
                // observado (a UI acabou de existir, antes de qualquer clique).
                LembrarTooltip();
                Ir(F_LEITURA, "lendo-objetos");
            }
            else if (_quadros > 90000)
            {
                _passos["aguardou_ui"] = Json.Campos("ok", false, "quadros", _quadros, "ui_existe", ui, "texto_visivel", temTexto);
                _res["status"] = "SEM_UI";
                Marco("AUT4 PROBE: ABORTOU — a UI com texto na tela nao apareceu.");
                Finalizar();
            }
        }

        private void PassoLeitura()
        {
            Evento("leitura_inicio");
            // RSTV/AUT5-F1: GUARDA — snapshot do personagem no INICIO da
            // leitura; o `_depois` e o MESMO objeto, atualizado no fim
            // (AtualizarGuardasDepois), para o par antes/depois ser real.
            IniciarSnapshotDoModal();
            try { ColetarObservacoes(); } catch (Exception e) { _passos["coleta"] = "erro: " + e.GetType().Name + ": " + e.Message; }
            Evento("coleta_concluida");
            // A6 + F5: ida-e-volta OPT-IN — so quando o cfg manda OBSERVAR.
            // ESCREVER exige `AutorizaEscritaTooltip` (autorizacao separada).
            if (_demostrar.Value) { try { DemostrarIdaEVolta(); } catch (Exception e) { _passos["ida_e_volta"] = "erro: " + e.GetType().Name + ": " + e.Message; } }
            try { _res["owners_harmony"] = OwnersHarmony(); } catch (Exception e) { _passos["owners"] = "erro: " + e.GetType().Name; }
            var ownersFunil = OwnersDosFunils();
            // AGREGADOS (AUD-1: porte do CAP-1, componente isolado
            // `LeituraAgregados`): inventario por shader/fonte, fontes em
            // memoria (com o shader de referencia do TMP) e a lista dos textos
            // DESENHADOS. Contexto da rodada — NAO sao campos de observacao.
            try { _res["inventario"] = LeituraAgregados.Inventario(_maxTextos.Value,
                t => Leitura(t, ownersFunil)); }
            catch (Exception e) { _passos["inventario"] = "erro: " + e.GetType().Name; }
            try { _res["fontes"] = LeituraAgregados.Fontes(); }
            catch (Exception e) { _passos["fontes"] = "erro: " + e.GetType().Name; }
            try { _res["textos_visiveis"] = LeituraAgregados.TextosVisiveis(_maxTextos.Value); }
            catch (Exception e) { _passos["textos_visiveis"] = "erro: " + e.GetType().Name; }
            Evento("textos_visiveis_lidos");
            // KIT-R0F/F3: o nome do campo e HISTORICO. A lista traz TMP_Text ATIVO
            // com texto parseado nao vazio; componente ATIVO com texto NAO prova
            // pixel desenhado (oclusao/CanvasGroup/alfa/recorte temporal nao sao
            // medidos por componente). A interpretacao vai declarada no JSON, ao
            // lado da lista, para nao ser lida como "visivel".
            _res["textos_visiveis_interpretacao"] = LeituraAgregados.InterpretacaoDeVisibilidade();
            try { _res["rollback"] = Rollback(); } catch (Exception e) { _passos["rollback"] = "erro: " + e.GetType().Name; }
            // KIT-14F (rodada 2) — o ROTEIRO depois da leitura, num lugar so. UMA chamada:
            // avaliar a fase duas vezes chamaria `TentarNavegar` duas vezes no mesmo quadro.
            int proximaFase = FaseDepoisDaLeitura();
            Ir(proximaFase, proximaFase == F_NAVEGACAO ? "navegando" : "print-01");
        }

        /// <summary>KIT-14F (rodada 2) — PARA ONDE VAI A RODADA depois de ler.
        /// A navegacao por handler exige ESPERA por quadros (a tela de LOADING do run704 nao
        /// tem botao nenhum no 1o quadro): enquanto o alvo nao apareceu E o teto nao esgotou,
        /// a proxima fase e `F_NAVEGACAO` — e o PROPRIO driver reinvoca `TentarNavegar` quadro
        /// a quadro. Antes, o `Ir(F_PRINT1)` era INCONDICIONAL e a rotina era de quadro unico.</summary>
        private int FaseDepoisDaLeitura()
        {
            if (_navegar.Value)
            {
                TentarNavegar();
                if (!NavegacaoTerminou()) return F_NAVEGACAO;
            }
            return F_PRINT1;
        }

        /// <summary>KIT-14F (rodada 2) — A FASE DE NAVEGACAO: um passo por QUADRO, dado pelo
        /// driver (`Passo`), reinvocando a rotina de navegacao ate o alvo aparecer OU o teto
        /// esgotar. Nao le nada. Quando termina, pede o print e segue o roteiro.</summary>
        private void PassoNavegacao()
        {
            TentarNavegar();
            if (!NavegacaoTerminou()) return;
            if (_rstvCiclo != null && _rstvCiclo.Value)
            {
                if (PassoRstv()) return;
                // No final target was invoked. Empty output remains absence, not a successful cycle.
                _observacoes.Clear();
                _res["observacoes"] = _observacoes;
                _res["rstv_coleta"] = Json.Campos("status", "ALVO_AUSENTE", "sessao", _sessao,
                    "events", _rstvEvents, "owner_provenance", _rstvOwnerEvidence, "physical_input", false);
                PedirPrint("01-ui");
                Ir(F_PRINT1, "print-01");
                return;
            }
            // KIT-14G — RECOLETA **DEPOIS** DA NAVEGACAO (item 3 do escopo do KIT-14G). Antes, a
            // leitura de objetos acontecia em `PassoLeitura` (no quadro do LOADING) e o PNG saia
            // centenas de quadros depois, ja na tela navegada: os dois nao eram o mesmo instante e
            // o texto do loading nao podia ser lido como se fosse o da tela-alvo. Aqui os objetos
            // sao RELIDOS no estado em que a navegacao parou e o print sai em seguida.
            try { Recoletar(); }
            catch (Exception e) { _passos["recoleta"] = "erro: " + e.GetType().Name + ": " + e.Message; }
            // KIT-14F (rodada 2): o print e EFEITO best-effort. Se ele falhar, o ROTEIRO nao
            // pode ficar preso na fase de navegacao (era o risco: excecao em `PedirPrint`
            // deixava `Ir(F_PRINT1)` sem executar e o probe tentava navegar para sempre).
            try { PedirPrint("01-ui"); }
            catch (Exception e) { _passos["print_01-ui"] = "erro: " + e.GetType().Name + ": " + e.Message; }
            Ir(F_PRINT1, "print-01");
        }

        /// <summary>KIT-14G — RELEITURA pos-navegacao. Refaz a coleta de objetos, o inventario e os
        /// textos visiveis no estado ATUAL e reinicia o snapshot do modal, registrando o QUADRO da
        /// releitura (`_recoleta_frame`) para que leitura e PNG sejam correlacionaveis pelo mesmo
        /// instante. Nada aqui e premissa: quem chamou ja saiu da navegacao.</summary>
        private void Recoletar()
        {
            if (_recoletou) return;   // uma releitura so: o roteiro passa por aqui uma vez
            _recoletou = true;
            try { _recoletaFrame = Time.frameCount; } catch { }
            _observacoes.Clear();
            ColetarObservacoes();
            try { IniciarSnapshotDoModal(); } catch { }
            var ownersFunil = OwnersDosFunils();
            try { _res["inventario"] = LeituraAgregados.Inventario(_maxTextos.Value, t => Leitura(t, ownersFunil)); }
            catch (Exception e) { _passos["recoleta_inventario"] = "erro: " + e.GetType().Name; }
            try { _res["textos_visiveis"] = LeituraAgregados.TextosVisiveis(_maxTextos.Value); }
            catch (Exception e) { _passos["recoleta_textos"] = "erro: " + e.GetType().Name; }
            try { _res["estado_da_tela_pos_navegacao"] = EstadoDaTela(); } catch { }
            _res["recoleta"] = Json.Campos(
                "apos_navegacao", true,
                "frame", _recoletaFrame,
                "observacoes", _observacoes.Count,
                "rota_estagios_clicados", _rotaEtapa,
                "alvo_invocado", _navegacaoAlvoInvocado,
                "nota", "objetos lidos DEPOIS da navegacao; o PNG 01-ui e pedido no quadro seguinte "
                        + "e `eventos_frame` traz o quadro de pedido/conclusao dos dois");
        }

        private void PassoPrint1()
        {
            if (PrintPronto() || _quadros++ > 600) { FecharPrint("01-ui"); Ir(F_FINAL, "final"); }
        }

        private void PassoFinal()
        {
            // RSTV/AUT5-F1: o "depois" das guardas e o ULTIMO estado observado.
            AtualizarGuardasDepois();
            PedirPrint("02-final");
            Ir(F_PRINT2, "print-02");
        }

        private void PassoPrint2()
        {
            if (PrintPronto() || _quadros++ > 600) { FecharPrint("02-final"); Finalizar(); }
        }

        private void Ir(int fase, string legivel) { _fase = fase; _quadros = 0; _res["fase"] = legivel; Escrever(); }

        /// <summary>KIT-R0F/F3 — registra o QUADRO (Time.frameCount) de um evento nomeado.
        /// E o elo que faltava entre a leitura, o pedido/conclusao do PNG e os pixels:
        /// `aplicacao.roteiro_frame` e metadado do ARRANQUE e `quadros_ate_a_ui` conta ticks
        /// internos do instrumento — nenhum dos dois e o quadro do evento.</summary>
        private void Evento(string nome)
        {
            try { _eventosFrame[nome] = Time.frameCount; } catch { }
        }

        private void Finalizar()
        {
            // INT-R1-C2-I1: encerrar a ponte da API antes de fechar o JSON — remove a assinatura do
            // Signal do produtor e libera o lease do RegistryV1 (idempotente).
            // B3 (revisao independente, rodada 1): sem ponte LIGADA nada e escrito — nem chave em
            // `_passos` (ela vira campo novo do JSON) nem marco — para a saida default nao mudar.
            if (_ponteApi != null)
            {
                try { _ponteApi.Dispose(); _ponteApi = null; _passos["ponte_api"] = "encerrada"; }
                catch (Exception e) { _passos["ponte_api"] = "erro: " + e.GetType().Name; }
            }
            // RSTV/AUT5-F1: cobre tambem os caminhos de ABORTO (SEM_UI/orcamento):
            // as guardas refletem o ultimo estado lido nesta rodada.
            try { AtualizarGuardasDepois(); } catch { }
            try { _res["owners_harmony"] = _res.ContainsKey("owners_harmony") ? _res["owners_harmony"] : OwnersHarmony(); } catch { }
            try { _res["manifest"] = Manifest(); } catch { }
            try { _res["rollback"] = Rollback(); } catch { }
            _res["prints"] = _arquivosDePrint;
            Evento("fim");
            // KIT-R0F/F3: pedido/conclusao de CADA PNG, em quadro, e os quadros de todos
            // os eventos nomeados. Sem isto nao havia como relacionar leitura, PNG e pixels.
            _res["prints_detalhe"] = _printsDetalhe;
            _res["eventos_frame"] = _eventosFrame;
            // KIT-14G: CONSUMIR o recorder ANTES de encerrar. A trilha passiva vive na memoria do
            // processo do jogo — se ela nao for lida/gravada aqui, o rollback do perfil e do
            // diretorio de dados leva a prova embora (foi o que aconteceu no run710).
            try { LerRecorder(); } catch (Exception e) { _passos["recorder"] = "erro: " + e.GetType().Name + ": " + e.Message; }
            _res["eventos_frame_nota"] = "Time.frameCount no instante de cada evento nomeado. "
                + "`aplicacao.roteiro_frame` e METADADO DO ARRANQUE (montado no Awake) e "
                + "`aguardou_ui.quadros_ate_a_ui` conta TICKS INTERNOS do instrumento: nenhum "
                + "dos dois e o quadro da coleta — use `eventos_frame` para correlacionar.";
            _res["marcos"] = _marcos;
            // KIT-14G-SEG2: o resultado do caminho do clique, no JSON, e o fecho do arquivo proprio.
            _res["clique_eventos"] = _cliques;
            _res["clique_config"] = ConfiguracaoClique();
            FecharMarcos();
            _res["total_observacoes"] = _observacoes.Count;
            _res["gerado_em"] = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);
            _res["duracao_s"] = Math.Round(Time.realtimeSinceStartup - _t0, 3);
            var status = _res.ContainsKey("status") ? Convert.ToString(_res["status"]) : "";
            if (status != "SEM_UI" && status != "ORCAMENTO_ESTOURADO" && status != "ERRO") _res["status"] = "CONCLUIDO";
            _res["fase"] = "concluido";
            Marco("AUT4 PROBE: FIM — " + _observacoes.Count + " observacoes, " + _arquivosDePrint.Count + " prints.");
            _concluido = true;
            Escrever();
        }

        // ------------------------------------------------------------ leitura

        private void ColetarObservacoes()
        {
            var todos = Recursos<TMP_Text>();
            int lidos = 0;
            var ownersFunil = OwnersDosFunils();
            foreach (var t in todos)
            {
                if (t == null) continue;
                if (lidos >= _maxTextos.Value) break;
                bool alvoNomeado = Array.IndexOf(NomesDeAlvo, t.gameObject.name) >= 0;
                bool temTexto = !string.IsNullOrEmpty(t.text);
                if (!alvoNomeado && !(t.gameObject.activeInHierarchy && temTexto)) continue;
                _observacoes.Add(Leitura(t, ownersFunil));
                lidos++;
            }
            _res["observacoes"] = _observacoes;
            _res["total_tmp_text"] = todos.Length;
            _res["lidos"] = lidos;
        }

        // Material em uso, shader, keyword, cores: tudo do OBJETO VIVO.
        // `internal` (nao `private`): o componente isolado `LeituraAgregados` reusa ESTE
        // leitor como amostra do inventario (um unico critério de leitura no probe).
        internal Dictionary<string, object> Leitura(TMP_Text t, List<object> ownersFunil)
        {
            var mat = t.fontSharedMaterial;
            var fonte = t.font;
            var keywords = new Dictionary<string, object>();
            if (mat != null)
            {
                foreach (var kw in new[] { "OUTLINE_ON", "UNDERLAY_ON", "UNDERLAY_INNER", "GLOW_ON", "BEVEL_ON" })
                    keywords[kw] = SeguroBool(() => mat.IsKeywordEnabled(kw));
            }
            var cores = Json.Campos(
                "texto", CorDe(t.color),
                "face", CorDoMaterial(mat, "_FaceColor"),
                "contorno", CorDoMaterial(mat, "_OutlineColor"),
                "sombra", CorDoMaterial(mat, "_UnderlayColor"));
            return Json.Campos(
                "objeto", t.gameObject.name,
                "caminho", Caminho(t.transform),
                "componente", t.GetType().Name,
                "ativo_na_hierarquia", t.gameObject.activeInHierarchy,
                "visivel_na_tela", SeguroBool(() => t.isActiveAndEnabled && t.gameObject.activeInHierarchy),
                "texto_bruto", Trunc(t.text, 600),
                "texto_renderizado", Trunc(Seguro(() => t.GetParsedText()) as string, 600),
                "fonte", fonte != null ? fonte.name : null,
                "material", mat != null ? mat.name : null,
                "shader", mat != null ? Nome(mat.shader) : null,
                "shader_suportado", mat != null && mat.shader != null && mat.shader.isSupported,
                "keywords", keywords,
                "cores", cores,
                "geometria", Geometria(t),
                "tamanho_fonte", Arred(t.fontSize),
                "owners", ownersFunil,
                "personagem", Contexto(),
                // RSTV/AUT5-F1 — guarda de leitura (o `_depois` e atualizado no fim).
                "snapshot_antes", _snapshotAntes,
                "snapshot_depois", _snapshotDepois,
                "tooltip_pai_antes", _tooltipPaiAntes,
                "tooltip_pai_depois", _tooltipPaiDepois,
                "tooltip_indice_antes", _tooltipIndiceAntes,
                "tooltip_indice_depois", _tooltipIndiceDepois,
                "janelas_duplicadas", _janelasDuplicadas,
                "nota_texto_renderizado", t.gameObject.activeInHierarchy ? null
                    : "objeto INATIVO: GetParsedText() sai vazio ate o TMP gerar o mesh; vale o texto_bruto.");
        }

        // ------------------------------------------- RSTV/AUT5-F1: guarda de leitura

        /// <summary>
        /// Estado do personagem do modal: `skills` (lista de str) + `pontos`
        /// (numerico). SOMENTE LEITURA, por reflexao — membro que nao existir sai
        /// `null` (AUSENTE no contrato: NUNCA vira OK). Caminho REAL do jogo
        /// (docs/RSTV-ANALISE.md l.92/l.107): `Character.SkillsFromPoints`
        /// (a mesma lista que o `SkillTreeManager.Initialize` recebe) e
        /// `Character.UnspentSkillPoints`.
        /// </summary>
        private Dictionary<string, object> SnapshotDoPersonagem()
        {
            object ch = _personagemDoModal;
            object skills = null;
            object pontos = null;
            if (ch != null)
            {
                try
                {
                    object lista = Membro(ch, "SkillsFromPoints");
                    if (lista is IEnumerable en && !(lista is string))
                    {
                        var nomes = new List<object>();
                        foreach (var s in en)
                        {
                            if (s == null) continue;
                            object nome = Membro(s, "SkillName");
                            nomes.Add(nome != null
                                ? Convert.ToString(nome, CultureInfo.InvariantCulture)
                                : NomeDoObjeto(s));
                        }
                        skills = nomes;
                    }
                }
                catch { }
                try { pontos = Membro(ch, "UnspentSkillPoints"); } catch { }
            }
            var d = Json.Campos(
                "personagem", ch == null ? null
                    : Convert.ToString(Membro(ch, "CharacterName"), CultureInfo.InvariantCulture),
                "skills", skills, "pontos", pontos);
            if (skills != null) d["fonte_skills"] = "Character.SkillsFromPoints";
            if (pontos != null) d["fonte_pontos"] = "Character.UnspentSkillPoints";
            return d;
        }

        private void IniciarSnapshotDoModal()
        {
            // Captura UMA referencia do alvo efetivo. End() limpa Target, mas o
            // depois continua lendo este personagem, nunca o selecionado global.
            _personagemDoModal = PersonagemDaSessao();
            _snapshotAntes = SnapshotDoPersonagem();
            _snapshotDepois = SnapshotDoPersonagem();
        }

        private object PersonagemDaSessao()
        {
            try
            {
                var t = Tipo("RoguelikeSkillTreeVisualizer.ReadOnlySession");
                if (t == null || !Equals(Estatico(t, "Active"), true)) return null;
                return Estatico(t, "Target");
            }
            catch { return null; }
        }

        private static string NomeDoObjeto(object o)
        {
            var u = o as UnityEngine.Object;
            if (u != null) return u.name;
            return o == null ? null : Convert.ToString(o, CultureInfo.InvariantCulture);
        }

        private object TooltipVivo()
        {
            try
            {
                var t = Tipo("GUIManager");
                object gui = t == null ? null : Estatico(t, "instance");
                return gui == null ? null : Membro(gui, "tooltip");
            }
            catch { return null; }
        }

        /// <summary>`pai` do tooltip = caminho do TRANSFORM PAI (onde o mod
        /// reparenta no hover e tem de devolver ao fechar — RSTV-21).</summary>
        private static string TooltipPai(object tooltip)
        {
            var comp = tooltip as Component;
            if (comp == null || comp.transform == null || comp.transform.parent == null) return null;
            return Caminho(comp.transform.parent);
        }

        /// <summary>`indice` = posicao do tooltip entre os irmaos (restauracao
        /// devolve o MESMO indice; mudar de lugar sem restaurar e defeito).</summary>
        private static object TooltipIndice(object tooltip)
        {
            var comp = tooltip as Component;
            if (comp == null || comp.transform == null) return null;
            return comp.transform.GetSiblingIndex();
        }

        /// <summary>Guarda o PRIMEIRO estado do tooltip (o "antes" do ciclo da janela).</summary>
        private void LembrarTooltip()
        {
            if (_tooltipAntesLido) return;
            object tooltip = TooltipVivo();
            if (tooltip == null) return;   // ainda sem tooltip: tenta de novo no proximo quadro
            _tooltipAntesLido = true;
            _tooltipPaiAntes = TooltipPai(tooltip);
            _tooltipIndiceAntes = TooltipIndice(tooltip);
        }

        // RootName da janela propria do RSTV (`SkillTreesWindow.RootName`, const da
        // fonte do mod). O probe NAO referencia o tipo do mod: conta por nome, no
        // cenario ativo, objeto ATIVO na hierarquia (asset de prefab nao conta).
        private const string JanelaRstvRoot = "RstvSkillTreesWindow";

        /// <summary>Quantas janelas do RSTV ATIVAS existem ALEM da primeira (>0 e
        /// duplicacao). Nunca negativo; `null` so se a consulta falhar.</summary>
        private object JanelasDuplicadas()
        {
            try
            {
                int achadas = 0;
                foreach (var t in Recursos<Transform>())
                {
                    if (t == null || t.gameObject == null) continue;
                    if (t.gameObject.name != JanelaRstvRoot) continue;
                    if (!t.gameObject.activeInHierarchy) continue;
                    if (!t.gameObject.scene.IsValid()) continue;   // asset, nao cena viva
                    achadas++;
                }
                return achadas > 1 ? achadas - 1 : 0;
            }
            catch { return null; }
        }

        /// <summary>
        /// Fecha a guarda: atualiza o "depois" (snapshot do personagem, pai/indice do
        /// tooltip e janelas duplicadas) no MESMO objeto de snapshot ja referenciado
        /// pelas observacoes, e reescreve os escalares em cada observacao.
        /// </summary>
        private void AtualizarGuardasDepois()
        {
            // Dedicated consumer owns its before-open / after-close pair; legacy refresh must not overwrite it.
            if (_rstvCiclo != null && _rstvCiclo.Value) return;
            var depois = SnapshotDoPersonagem();
            if (_snapshotDepois != null)
            {
                _snapshotDepois["personagem"] = depois["personagem"];
                _snapshotDepois["skills"] = depois["skills"];
                _snapshotDepois["pontos"] = depois["pontos"];
            }
            object tooltip = TooltipVivo();
            _tooltipPaiDepois = tooltip == null ? null : TooltipPai(tooltip);
            _tooltipIndiceDepois = tooltip == null ? null : TooltipIndice(tooltip);
            _janelasDuplicadas = JanelasDuplicadas();
            foreach (var o in _observacoes)
            {
                var d = o as Dictionary<string, object>;
                if (d == null) continue;
                d["snapshot_depois"] = _snapshotDepois;
                d["tooltip_pai_depois"] = _tooltipPaiDepois;
                d["tooltip_indice_depois"] = _tooltipIndiceDepois;
                d["janelas_duplicadas"] = _janelasDuplicadas;
            }
        }

        private object Contexto()
        {
            var d = new Dictionary<string, object>();
            try
            {
                var t = Tipo("GUIManager");
                object gui = t == null ? null : Estatico(t, "instance");
                d["gui_state"] = gui == null ? null : Convert.ToString(Membro(gui, "CurrentGuiState"), CultureInfo.InvariantCulture);
            }
            catch { }
            try
            {
                var gt = Tipo("GameLogic");
                object gl = gt == null ? null : Estatico(gt, "instance");
                object ch = gl == null ? null : Membro(gl, "CurrentlySelectedCharacter");
                d["tem_personagem_selecionado"] = ch != null;
                d["personagem"] = ch == null ? null : Convert.ToString(Membro(ch, "CharacterName"), CultureInfo.InvariantCulture);
            }
            catch { }
            return d;
        }

        private bool UiExiste()
        {
            var t = Tipo("GUIManager");
            if (t == null) return false;
            object gui = Estatico(t, "instance");
            if (gui == null) return false;
            object tooltip = Membro(gui, "tooltip");
            return tooltip != null && Membro(tooltip, "Title") is TMP_Text;
        }

        private bool TemTextoVisivel()
        {
            foreach (var t in Recursos<TMP_Text>())
            {
                if (t == null || !t.gameObject.activeInHierarchy || string.IsNullOrEmpty(t.text)) continue;
                var parsed = Seguro(() => t.GetParsedText()) as string;
                if (!string.IsNullOrEmpty(parsed)) return true;
            }
            return false;
        }

        private Dictionary<string, object> EstadoDaTela()
        {
            var d = new Dictionary<string, object>();
            try
            {
                var t = Tipo("GUIManager");
                object gui = t == null ? null : Estatico(t, "instance");
                d["GUIManager.instance"] = gui != null;
                d["CurrentGuiState"] = gui == null ? null : Convert.ToString(Membro(gui, "CurrentGuiState"), CultureInfo.InvariantCulture);
                d["tooltips_em_memoria"] = Tipo("Tooltip") == null ? 0 : Resources.FindObjectsOfTypeAll(Tipo("Tooltip")).Length;
            }
            catch (Exception e) { d["erro"] = e.GetType().Name + ": " + e.Message; }
            return d;
        }

        private Dictionary<string, object> ModsCarregados()
        {
            var lista = new List<object>();
            try
            {
                foreach (var par in Chainloader.PluginInfos)
                {
                    var info = par.Value;
                    if (info == null || info.Metadata == null) continue;
                    lista.Add(Json.Campos("guid", info.Metadata.GUID, "nome", info.Metadata.Name,
                        "versao", info.Metadata.Version == null ? null : info.Metadata.Version.ToString(),
                        "instrumento", info.Metadata.GUID == Guid));
                }
            }
            catch (Exception e) { return Json.Campos("erro", e.GetType().Name + ": " + e.Message); }
            return Json.Campos("total", lista.Count, "plugins", lista);
        }

        // ------------------------------------------------------------ owners Harmony

        private static readonly string[][] FUNIS =
        {
            new[] { "OptionsManager", "Localize" },
            new[] { "GUIManager", "Update" },
            new[] { "Tooltip", "ShowTooltip" },
            new[] { "Tooltip", "ShowSkillTooltip" },
        };

        private List<object> OwnersDosFunils()
        {
            var donos = new List<object>();
            foreach (var par in FUNIS)
            {
                foreach (object o in OwnersDe(par[0], par[1])) if (!donos.Contains(o)) donos.Add(o);
            }
            return donos;
        }

        private Dictionary<string, object> OwnersHarmony()
        {
            var d = new Dictionary<string, object>();
            foreach (var par in FUNIS)
            {
                var chave = par[0] + "." + par[1];
                d[chave] = Json.Campos("metodo_encontrado", Tipo(par[0]) != null, "owners", OwnersDe(par[0], par[1]));
            }
            return Json.Campos("criterio", "owners lidos de Harmony.GetPatchInfo no metodo vivo — nao e presuncao", "por_metodo", d);
        }

        private List<object> OwnersDe(string tipo, string metodo)
        {
            var donos = new List<object>();
            try
            {
                var t = Tipo(tipo);
                if (t == null) return donos;
                foreach (var m in t.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static))
                {
                    if (m.Name != metodo || m.IsAbstract) continue;
                    var pi = HarmonyLib.Harmony.GetPatchInfo(m);
                    if (pi == null || pi.Owners == null) continue;
                    foreach (var dono in pi.Owners) if (!donos.Contains(dono)) donos.Add(dono);
                }
            }
            catch { }
            return donos;
        }

        // ------------------------------------------------------------ navegacao

        // KIT-14F — a navegacao por handler era de QUADRO UNICO: varria os botoes UMA vez e
        // encerrava. No run704 (tela de LOADING) isso lia `botoes_ativos=0` e nao havia
        // tentativa seguinte, nem motivo declarado quando esgotava. Agora:
        //   * ESPERA por quadros, com contagem de tentativas e TETO explicito;
        //   * declara ESTADO e MOTIVO quando esgota sem achar o alvo;
        //   * invoca o handler EXATAMENTE UMA VEZ quando o alvo aparece;
        //   * tem PORTA INJETAVEL (`PortaDeBotoes`) para exercitar a escolha OFFLINE, sem
        //     engine — o caminho de engine segue sendo o default (porta nula).
        private const int NavegacaoTentativasMax = 12;
        private ConfigEntry<int> _navTentativasMax;
        private int _navegacaoTentativas;
        private bool _navegacaoConcluida;
        private string _navegacaoAlvoInvocado;

        // KIT-14G — ROTEIRO em estagios e mapa dos botoes vistos.
        // `_rota` vem do .cfg (`NavegarRota`): estagios ORDENADOS ate a tela do alvo. `_rotaEtapa`
        // e quantos ja foram clicados. `_botoesVistos` = {rotulo/nome -> 1a tentativa em que
        // apareceu ATIVO}: e o MAPA que permite escrever o roteiro a partir de uma rodada real,
        // em vez de adivinhar rotulos.
        private ConfigEntry<string> _navRota;
        private ConfigEntry<string> _navAlvoNome;
        private readonly List<string> _rota = new List<string>();
        private int _rotaEtapa;
        private readonly Dictionary<string, int> _botoesVistos = new Dictionary<string, int>();

        // KIT-14G — recoleta DEPOIS da navegacao (o PNG e a leitura passam a ser do MESMO
        // instante; antes a leitura era do frame do loading e o PNG de centenas de quadros
        // depois).
        private bool _recoletou;
        private int _recoletaFrame = -1;

        // ============================ KIT-14G-SEG2 (t_139f714f) ============================
        // MARCOS DO CAMINHO DO CLIQUE + GATE DE CLIQUE FISICO + SILENCIO POS-CLIQUE.
        //
        // O A/B do run714 isolou o GATILHO (o clique sintetico que inicia a run derruba o jogo
        // com `c0000005` em `ntdll`) mas NAO isolou ONDE no caminho o acesso nasce — e nao
        // podia: o `LogOutput.log` do BepInEx fica em BUFFER e o processo morre antes de
        // esvaziar (o log do boot `A-sem-passivo` termina no 3o tick). Aqui os marcos vao para
        // um ARQUIVO PROPRIO, com `Flush` a cada linha: sobrevivem a morte abrupta e dizem a
        // ULTIMA coisa que o instrumento fez, com QUADRO e INSTANTE.
        //
        // `onClick.Invoke()` ignora o gate de Button.Press: ativo nao implica interactable.
        // EsperarInteractable e seguro por default; CliqueFisico acrescenta CanvasGroup raycast,
        // mas nenhum destes gates prova raycast/oclusao completos ou um clique humano.
        private ConfigEntry<bool> _esperarInteractable;
        private ConfigEntry<bool> _cliqueFisico;
        private ConfigEntry<int> _cliqueFisicoEstavel;
        private ConfigEntry<bool> _silencioAposClique;
        private List<bool> _clicaveis;          // alinhado com a ULTIMA coleta de candidatos
        private List<string> _motivosBloqueio;  // idem: null = clicavel; senao, o porque
        private List<GameObject> _objetos;      // idem: o GameObject de cada candidato
        private bool _silencio;
        private int _quadrosSilencio;
        private string _estavelRotulo;
        private int _estavelQuadros;
        private int? _estavelUltimoFrame;
        private int _estavelIndice = -1;
        private GameObject _estavelObjeto;

        private void ResetarEstabilidade()
        {
            _estavelRotulo = null;
            _estavelQuadros = 0;
            _estavelUltimoFrame = null;
            _estavelIndice = -1;
            _estavelObjeto = null;
        }

        private bool EstavelEnough(int indice, string rotulo, int exigido)
        {
            if (exigido <= 0) { ResetarEstabilidade(); return true; }
            // Sem frame capturado NAO inventar estabilidade a partir de chamadas.
            if (!(_quadroCapturado is int frame)) { ResetarEstabilidade(); return false; }
            var objeto = _objetos != null && indice < _objetos.Count ? _objetos[indice] : null;
            bool mesmoAlvo = rotulo == _estavelRotulo && indice == _estavelIndice
                && ReferenceEquals(objeto, _estavelObjeto);
            if (!mesmoAlvo || !_estavelUltimoFrame.HasValue
                || (frame != _estavelUltimoFrame.Value && frame != _estavelUltimoFrame.Value + 1))
                _estavelQuadros = 1;
            else if (frame != _estavelUltimoFrame.Value)
                _estavelQuadros++;
            _estavelRotulo = rotulo;
            _estavelIndice = indice;
            _estavelObjeto = objeto;
            _estavelUltimoFrame = frame;
            return _estavelQuadros >= exigido;
        }
        // KIT-14G-SEG2: o estado de ENGINE (quadro/instante/cena) e CAPTURADO no caminho de
        // engine e guardado em CAMPO — os marcos leem o campo. O motivo e medido e duro: fora do
        // jogo, QUALQUER metodo que CHAME uma funcao de engine morre no pre-carregamento do CLR
        // com `SecurityException: ECall methods must be packaged into a system module` (e o
        // harness offline dirige `Passo`, que passa por aqui). Chamar `Time.frameCount` direto no
        // roteiro derrubava a parte3 do harness-kit14f com esse erro.
        private object _quadroCapturado;
        private string _tempoCapturado;
        private string _cenaCapturada;
        private List<object> _cliques = new List<object>();
        private string _caminhoMarcos;
        private FileStream _fsMarcos;
        private StreamWriter _swMarcos;
        private bool _marcosTentado;

        /// <summary>KIT-14F (rodada 2) — TETO das tentativas de navegacao, num lugar so.
        /// `_navTentativasMax` e a ConfigEntry do .cfg (`Navegar`/`TentativasMax`); sem ela
        /// (rodada offline) vale o default do produto.</summary>
        private int TetoNavegacao()
        {
            int teto = _navTentativasMax != null ? _navTentativasMax.Value : NavegacaoTentativasMax;
            return teto <= 0 ? NavegacaoTentativasMax : teto;
        }

        /// <summary>KIT-14F (rodada 2) — CONDICAO DE PARADA da fase de navegacao, num lugar so:
        /// o alvo foi invocado OU o teto de tentativas esgotou. Sem isto a fase ficaria viva
        /// para sempre (trava) ou seria de quadro unico (o defeito do run704).</summary>
        private bool NavegacaoTerminou()
            => _navegacaoConcluida || _navegacaoTentativas >= TetoNavegacao();

        /// <summary>KIT-14F — porta INJETAVEL da navegacao (default null = engine real).
        /// Cada item e (rotulo, ativo, invocar): o teste offline serve os mesmos dados que a
        /// varredura de `Button` produziria, sem tocar em ECall da engine.</summary>
        public static Func<List<(string rotulo, bool ativo, Action invocar)>> PortaDeBotoes;

        // Costura OFFLINE alinhada por indice com PortaDeBotoes. Ausente = fixtures antigas
        // representam botoes habilitados/interactables; nunca e fallback do caminho de engine.
        public static Func<int, (bool habilitado, bool interactable, bool interacaoPermitida,
            string bloqueioRaycast)> PortaDeEstadoClique;

        private bool ExigirInteractable()
            => _esperarInteractable == null || _esperarInteractable.Value;

        // Configuracao EFETIVA, engine-free: mesma evidencia no JSON final/evento/marco.
        // CliqueFisico=false nao significa historico: EsperarInteractable default e TRUE.
        private Dictionary<string, object> ConfiguracaoClique()
        {
            bool esperar = ExigirInteractable();
            bool fisico = _cliqueFisico != null && _cliqueFisico.Value;
            bool exigir = esperar || fisico;
            return Json.Campos(
                "esperar_interactable", esperar,
                "gate_clique_fisico", fisico,
                "exigir_interactable", exigir,
                "fallback_historico", !exigir,
                "modo_clique", fisico ? "seguro_interactable_com_gate_fisico"
                    : (esperar ? "seguro_interactable" : "fallback_historico_inseguro"),
                "clique_fisico_estavel_quadros", _cliqueFisicoEstavel != null ? _cliqueFisicoEstavel.Value : 0,
                "silencio_apos_clique", _silencioAposClique != null && _silencioAposClique.Value,
                "silencio_ativado", _silencio,
                "nota", "onClick.Invoke() direto em todos os modos, sem EventSystem; "
                    + "espera segura por interactable por default; CliqueFisico e gate adicional. "
                    + "Fallback historico INSEGURO somente com EsperarInteractable=false E CliqueFisico=false.");
        }

        private List<(string rotulo, bool ativo, Action invocar)> ColetarCandidatos()
        {
            var porta = PortaDeBotoes;
            if (porta != null)
            {
                var servidos = porta() ?? new List<(string, bool, Action)>();
                // As fixtures offline podem servir ativo != interactable sem abrir a engine.
                // A mesma decisao pura abaixo e usada pelo caminho real de Button.
                _clicaveis = new List<bool>();
                _motivosBloqueio = new List<string>();
                _objetos = new List<GameObject>();
                for (int i = 0; i < servidos.Count; i++)
                {
                    var estado = PortaDeEstadoClique != null
                        ? PortaDeEstadoClique(i) : (true, true, true, (string)null);
                    string motivo = MotivoDeEstadoClique(servidos[i].ativo, estado.Item1,
                        estado.Item2, estado.Item3, estado.Item4, ExigirInteractable(),
                        _cliqueFisico != null && _cliqueFisico.Value);
                    _clicaveis.Add(servidos[i].ativo && motivo == null);
                    _motivosBloqueio.Add(motivo);
                    _objetos.Add(null);
                }
                return servidos;
            }

            bool exigir = _cliqueFisico != null && _cliqueFisico.Value;
            // KIT-14G-SEG2: quadro/instante/cena capturados AQUI (caminho de engine) e lidos
            // pelos marcos por CAMPO — ver `CapturarEstadoDeEngine`.
            CapturarEstadoDeEngine();
            var lista = new List<(string rotulo, bool ativo, Action invocar)>();
            var clicaveis = new List<bool>();
            var motivos = new List<string>();
            var objetos = new List<GameObject>();
            foreach (var b in Recursos<Button>())
            {
                if (b == null) continue;
                var botao = b;
                var rotulo = Seguro(() => {
                    var tt = botao.GetComponentInChildren<TMP_Text>();
                    string texto = tt != null ? tt.text : null;
                    // KIT-14G: o botao do RSTV NAO TEM ROTULO (RunButton.cs: o texto e desligado e
                    // o glifo e o rotulo). Sem este fallback ele era INVISIVEL para a escolha do
                    // alvo — a busca por 'Skills' nunca poderia achar o botao da run.
                    return string.IsNullOrEmpty(texto) ? botao.gameObject.name : texto;
                }) as string;
                bool ativo = Seguro(() => (object)botao.gameObject.activeInHierarchy) as bool? ?? false;
                // KIT-14G-SEG2: o mapa do roteiro continua sendo de TODOS os botoes ativos (e o
                // insumo de uma rodada real); o GATE so decide se o instrumento pode CLICAR.
                string motivo = MotivoDeBloqueio(botao, ExigirInteractable(), exigir);
                // `Seguro(<lambda>)`: o `gameObject` do botao e ECall da engine e TEM de ficar no
                // lambda (metodo gerado), nunca no corpo desta varredura — com ele aqui, a varredura
                // inteira deixava de carregar fora do jogo (`SecurityException: ECall ...`, medido
                // com pilha de uma linha em `ColetarCandidatos`).
                var alvo = Seguro(() => (object)botao.gameObject) as GameObject;
                lista.Add((rotulo, ativo, () => botao.onClick.Invoke()));
                clicaveis.Add(ativo && motivo == null);
                motivos.Add(motivo);
                objetos.Add(alvo);
            }
            AdicionarSeletorParty(lista, clicaveis, motivos, objetos);
            _clicaveis = clicaveis;
            _motivosBloqueio = motivos;
            _objetos = objetos;
            return lista;
        }

        /// <summary>KIT14G-SEG2-FIX — gate ANTES do handler direto.
        /// Button.Press usa IsActive()/IsInteractable(); activeInHierarchy sozinho nao basta.
        /// EsperarInteractable e TRUE por default, CliqueFisico soma CanvasGroup.blocksRaycasts.
        /// Fallback historico APENAS com ambas as chaves false; erro de leitura BLOQUEIA.
        /// NoInlining isola as ECalls para o harness offline carregar ColetarCandidatos.</summary>
        [MethodImpl(MethodImplOptions.NoInlining)]
        private static string MotivoDeBloqueio(Button b, bool esperar, bool exigir)
        {
            if (b == null) return "botao_nulo";
            if (!esperar && !exigir) return null; // fallback EXPLICITO, inseguro
            try
            {
                string motivo = MotivoDeEstadoClique(b.gameObject.activeInHierarchy,
                    b.isActiveAndEnabled, b.interactable, b.IsInteractable(), null, esperar, exigir);
                if (motivo != null || !exigir) return motivo;
                for (var t = b.transform; t != null; t = t.parent)
                {
                    var cg = t.GetComponent<CanvasGroup>();
                    if (cg == null) continue;
                    if (!cg.blocksRaycasts) return "CanvasGroup.blocksRaycasts=false em '" + t.name + "'";
                    if (cg.ignoreParentGroups) break;
                }
                return null;
            }
            catch (Exception e) { return "erro_na_checagem:" + e.GetType().Name; }
        }

        // Engine-free: prova offline executa a MESMA decisao do caminho de Button.
        private static string MotivoDeEstadoClique(bool ativo, bool habilitado, bool interactable,
            bool interacaoPermitida, string bloqueioRaycast, bool esperar, bool exigir)
        {
            if (!ativo) return "inativo_na_hierarquia";
            if (!esperar && !exigir) return null;
            if (!habilitado) return "componente_desabilitado";
            if (!interactable) return "interactable=false";
            if (!interacaoPermitida) return "IsInteractable()=false";
            return exigir ? bloqueioRaycast : null;
        }

        private void TentarNavegar()
        {
            var estagios = new List<object>();
            int teto = TetoNavegacao();
            int tentativa = ++_navegacaoTentativas;
            // KIT-14G: LADO SEGURO dos campos novos. Uma instancia montada fora do `Awake` (o
            // harness offline usa `GetUninitializedObject`) nao roda inicializador de campo: sem
            // estas guardas o roteiro derrubaria a escolha do alvo com NullReferenceException —
            // e o lado seguro de uma navegacao e ESPERAR, nunca estourar.
            var rota = _rota ?? new List<string>();
            var vistos = _botoesVistos;
            string nomeDoAlvo = _navAlvoNome == null ? "RstvRunSkillTreeButton" : _navAlvoNome.Value;
            // Explicit '=' target forbids native Skills substring fallback (wrong window).
            bool alvoEstrito = nomeDoAlvo != null && nomeDoAlvo.StartsWith("=", StringComparison.Ordinal);
            if (alvoEstrito) nomeDoAlvo = nomeDoAlvo.Substring(1);
            try
            {
                if (_navegacaoConcluida)
                {
                    estagios.Add(ResumoNavegacao("invocado", tentativa, teto,
                        "alvo '" + (_navegacaoAlvoInvocado ?? "?") + "' ja invocado; nada mais a fazer"));
                    _passos["navegacao"] = estagios;
                    return;
                }

                var candidatos = ColetarCandidatos();
                int ativos = 0;
                foreach (var c in candidatos)
                {
                    if (!c.ativo) continue;
                    ativos++;
                    // KIT-14G: MAPA dos botoes ATIVOS (rotulo/nome -> 1a tentativa em que apareceu).
                    // E daqui que sai o roteiro REAL de uma rodada; sem este mapa o roteiro seria
                    // adivinhado — e roteiro adivinhado nao e prova.
                    if (!string.IsNullOrEmpty(c.rotulo) && vistos != null && !vistos.ContainsKey(c.rotulo))
                        vistos[c.rotulo] = tentativa;
                }
                if (vistos != null) _res["botoes_vistos"] = vistos;

                // KIT-14G: o que se procura NESTE quadro e o estagio ATUAL do roteiro; com o
                // roteiro vazio (default historico) procura-se o alvo final direto.
                string etapaAtual = _rotaEtapa < rota.Count ? rota[_rotaEtapa] : null;
                string procurando = etapaAtual != null ? etapaAtual : "Skills";
                (string rotulo, bool ativo, Action invocar) achado = (null, false, null);
                // KIT-14G run712 — IGUALDADE ANTES DE SUBSTRING. O menu inicial do Stolen Realm
                // tem o botao 'Play' E os banners 'PLAY NOW!'/'WISHLIST NOW!': casar so por
                // substring fazia o estagio 'Play' clicar o ANUNCIO (o primeiro candidato da
                // varredura) e a TELA NAO MUDAVA — a navegacao "nao chegava a Skills" por alvo
                // ambiguo, nao por ausencia de botao (medido no boot `mapa` do run712). Agora o
                // rotulo EXATO do roteiro vence; a substring segue como FALLBACK (rotulos
                // compostos, ex.: 'Skills Tree Btn', e o nome do alvo sem rotulo do RSTV).
                bool alvoFinal = etapaAtual == null;
                bool Exato((string rotulo, bool ativo, Action invocar) c)
                    => !string.IsNullOrEmpty(c.rotulo)
                       && (!(alvoFinal && alvoEstrito)
                           ? (string.Equals(c.rotulo, procurando, StringComparison.OrdinalIgnoreCase)
                           || (alvoFinal && !string.IsNullOrEmpty(nomeDoAlvo)
                               && string.Equals(c.rotulo, nomeDoAlvo, StringComparison.OrdinalIgnoreCase)))
                           : string.Equals(c.rotulo, nomeDoAlvo, StringComparison.OrdinalIgnoreCase));
                bool Contem((string rotulo, bool ativo, Action invocar) c)
                    => !string.IsNullOrEmpty(c.rotulo)
                       && (!(alvoFinal && alvoEstrito)
                           ? (c.rotulo.IndexOf(procurando, StringComparison.OrdinalIgnoreCase) >= 0
                           || (alvoFinal && !string.IsNullOrEmpty(nomeDoAlvo)
                               && string.Equals(c.rotulo, nomeDoAlvo, StringComparison.OrdinalIgnoreCase)))
                           : string.Equals(c.rotulo, nomeDoAlvo, StringComparison.OrdinalIgnoreCase));
                // KIT-14G-SEG2: ALVO CASADO MAS NAO CLICAVEL fica registrado (rotulo + motivo). E a
                // evidencia que separa "o roteiro nao achou o botao" de "achou e clicou fora de
                // tempo" — sem ela o gate seria indistinguivel de uma busca que nao acha nada.
                int achadoIdx = -1, bloqueadoIdx = -1;
                string bloqueadoMotivo = null;
                string Motivo(int i) => (_motivosBloqueio != null && i < _motivosBloqueio.Count) ? _motivosBloqueio[i] : "motivo_desconhecido";
                bool Clicavel(int i) => _clicaveis != null && i >= 0 && i < _clicaveis.Count && _clicaveis[i];
                for (int i = 0; i < candidatos.Count; i++)
                {
                    var c = candidatos[i];
                    if (!c.ativo) continue;
                    if (!Exato(c)) continue;
                    if (Clicavel(i)) { achado = c; achadoIdx = i; break; }
                    if (bloqueadoIdx < 0) { bloqueadoIdx = i; bloqueadoMotivo = Motivo(i); }
                }
                // Exato ATIVO bloqueado continua sendo o alvo: nao clicar banner/substring.
                // Na primeira passagem bloqueadoIdx identifica somente os exatos ativos.
                if (achado.rotulo == null && bloqueadoIdx < 0)
                    for (int i = 0; i < candidatos.Count; i++)
                    {
                        var c = candidatos[i];
                        if (!c.ativo) continue;
                        if (!Contem(c)) continue;
                        if (Clicavel(i)) { achado = c; achadoIdx = i; break; }
                        if (bloqueadoIdx < 0) { bloqueadoIdx = i; bloqueadoMotivo = Motivo(i); }
                    }
                // Conta frames capturados DISTINTOS/consecutivos, nao chamadas do driver.
                // Bloqueio/ausencia do alvo interrompe a sequencia; 0 mantem o clique imediato
                // SOMENTE depois de passar o gate de interacao.
                if (achado.rotulo == null) ResetarEstabilidade();
                if (achado.rotulo != null && achadoIdx >= 0 && !EstavelEnough(achadoIdx, achado.rotulo,
                    _cliqueFisicoEstavel != null ? _cliqueFisicoEstavel.Value : 0))
                {
                    MarcoClique("nav_estabilidade_esperando='" + achado.rotulo + "' quadro=" + QuadroTxt()
                                + " tentativa=" + tentativa + " quadros_estavel=" + _estavelQuadros);
                    achado = (null, false, null);
                    achadoIdx = -1;
                }
                estagios.Add(Json.Campos("estagio", "procurar", "tentativa", tentativa,
                    "tentativas_max", teto, "botoes_ativos", ativos,
                    "rota_etapa", etapaAtual, "rota_total", rota.Count, "procurando", procurando,
                    "achou_skills", etapaAtual == null && achado.rotulo != null,
                    "objeto_achado", achado.rotulo,
                    "clicavel", achado.rotulo != null,
                    "casou_mas_bloqueado", bloqueadoIdx >= 0 ? candidatos[bloqueadoIdx].rotulo : null,
                    "casou_mas_bloqueado_motivo", bloqueadoMotivo,
                    "clicaveis_no_quadro", ContarClicaveis(),
                    "cena_ativa", CenaTxt()));

                // KIT-14G-SEG2: MARCO por tentativa no arquivo proprio (sobrevive a morte abrupta).
                // A rota em andamento (poucos quadros) e registrada SEMPRE; a espera pelo alvo, a
                // cada 30 quadros — assim o arquivo fica legivel e o ultimo marco diz exatamente o
                // que o instrumento fazia quando o processo morreu.
                if (etapaAtual != null || tentativa == 1 || tentativa % 30 == 0)
                    MarcoClique("nav tentativa=" + tentativa + "/" + teto + " quadro=" + QuadroTxt()
                        + " t=" + TempoTxt() + " cena=" + CenaTxt()
                        + " botoes=" + candidatos.Count + " ativos=" + ativos
                        + " clicaveis=" + ContarClicaveis()
                        + " etapa=" + (etapaAtual ?? "-") + "(" + _rotaEtapa + "/" + rota.Count + ")"
                        + " procurando=" + procurando + " achou=" + (achado.rotulo ?? "-")
                        + (bloqueadoIdx >= 0
                            ? " casou_mas_bloqueado='" + candidatos[bloqueadoIdx].rotulo + "' motivo=" + bloqueadoMotivo
                            : ""));

                if (achado.rotulo != null && etapaAtual != null)
                {
                    // ESTAGIO do roteiro: clica, AVANCA e CONTINUA na fase de navegacao — o alvo
                    // final ainda nao foi invocado (quem decide se a navegacao terminou e
                    // `NavegacaoTerminou`, nao este ramo).
                    ResetarEstabilidade();
                    achado.invocar();
                    estagios.Add(Json.Campos("estagio", "rota_clique", "etapa", _rotaEtapa,
                        "objeto", achado.rotulo, "tentativa", tentativa));
                    RegistrarClique("rota_clique", achadoIdx, achado.rotulo, tentativa, rota.Count);
                    _rotaEtapa++;
                    // KIT-14G-SEG2 (DIAGNOSTICO): se o ULTIMO estagio do roteiro acabou de ser
                    // clicado, e' daqui para a frente que a run comeca a carregar. No modo silencio
                    // o instrumento para de tocar na engine AGORA — o que sobrar de vida/dor e' do
                    // jogo, nao do instrumento.
                    if (_silencioAposClique != null && _silencioAposClique.Value && _rotaEtapa >= rota.Count)
                    {
                        _silencio = true;
                        MarcoClique("silencio_ativado apos_ultimo_estagio=" + _rotaEtapa + "/" + rota.Count
                                    + " objeto='" + achado.rotulo + "' quadro=" + QuadroTxt()
                                    + " t=" + TempoTxt() + " cena=" + CenaTxt());
                    }
                    Escrever();
                }
                else if (achado.rotulo != null)
                {
                    ResetarEstabilidade();
                    RstvAntesDeAbrir(achadoIdx >= 0 && _objetos != null && achadoIdx < _objetos.Count ? _objetos[achadoIdx] : null);
                    achado.invocar();
                    _navegacaoConcluida = true;
                    _navegacaoAlvoInvocado = achado.rotulo;
                    estagios.Add(Json.Campos("estagio", "clique_invocado", "objeto", achado.rotulo));
                    RegistrarClique("alvo_final", achadoIdx, achado.rotulo, tentativa, rota.Count);
                    estagios.Add(ResumoNavegacao("invocado", tentativa, teto,
                        "handler do botao '" + achado.rotulo + "' invocado uma vez"
                        + (_rota != null && _rota.Count > 0 ? " depois de " + _rotaEtapa + " estagio(s) do roteiro" : "")));
                }
                else if (tentativa >= teto)
                {
                    estagios.Add(ResumoNavegacao("esgotado", tentativa, teto,
                        "nenhum botao ativo com rotulo contendo '" + procurando + "' em " + teto
                        + " quadros (quadros com 0 botoes ativos na ultima leitura: " + (ativos == 0) + ")"
                        + (_rota != null && _rota.Count > 0 ? "; roteiro '" + string.Join(";", rota.ToArray())
                            + "' parado no estagio " + _rotaEtapa + " de " + rota.Count : "")));
                }
                else
                {
                    estagios.Add(ResumoNavegacao("aguardando", tentativa, teto,
                        bloqueadoIdx >= 0
                            ? "alvo casou mas esta bloqueado: " + bloqueadoMotivo + "; nova tentativa no proximo quadro"
                            : "alvo ainda ausente; nova tentativa no proximo quadro"));
                }
            }
            catch (Exception e)
            {
                // KIT-14G-SEG2: a PILHA entra na evidencia. "falha" sem pilha nao diz ONDE o
                // instrumento estourou — e no modo offline do harness (`Passo` dirigido) a pilha e
                // o unico jeito de ver qual chamada precisou de engine.
                string pilha = e.StackTrace ?? "-";
                if (pilha.Length > 600) pilha = pilha.Substring(0, 600) + "...";
                estagios.Add(ResumoNavegacao("falha", tentativa, teto,
                    e.GetType().Name + ": " + e.Message + " | pilha: " + pilha));
                MarcoClique("nav_falha " + e.GetType().Name + ": " + e.Message + " | pilha: " + pilha);
            }
            _passos["navegacao"] = estagios;
        }

        private static Dictionary<string, object> ResumoNavegacao(string estado, int tentativa,
            int teto, string motivo)
            => Json.Campos("estagio", "resumo", "estado", estado, "tentativas", tentativa,
                           "tentativas_max", teto, "motivo", motivo);

        // ---------------------------------------------------- KIT-14G-SEG2: marcos do clique

        /// <summary>Registra UM clique do instrumento (vai para o JSON e para o arquivo de marcos).
        /// E o "ponto exato do caminho do clique": objeto, rotulo, CAMINHO na hierarquia, quadro,
        /// instante, cena, e o veredito do gate no momento do disparo.</summary>
        private void RegistrarClique(string quando, int idx, string rotulo, int tentativa, int totalEtapas)
        {
            try
            {
                var item = new Dictionary<string, object>();
                item["quando"] = quando;
                item["rotulo"] = rotulo;
                item["etapa_indice"] = _rotaEtapa;
                item["etapa_total"] = totalEtapas;
                item["tentativa"] = tentativa;
                item["quadro"] = QuadroTxt();
                item["t_segundos"] = TempoTxt();
                item["cena_ativa"] = CenaTxt();
                foreach (var campo in ConfiguracaoClique()) item[campo.Key] = campo.Value;
                item["motivo_bloqueio_no_disparo"] = (idx >= 0 && _motivosBloqueio != null && idx < _motivosBloqueio.Count)
                    ? _motivosBloqueio[idx] : null;
                // Costura offline fornece objetos null; nao carregar helper com ECall nesse caso.
                item["objeto_caminho"] = (idx >= 0 && _objetos != null && idx < _objetos.Count
                    && !ReferenceEquals(_objetos[idx], null))
                    ? CaminhoDoObjeto(_objetos[idx]) : null;
                if (_cliques == null) _cliques = new List<object>();
                _cliques.Add(item);
                _res["clique_eventos"] = _cliques;
                MarcoClique("CLIQUE quando=" + quando + " rotulo='" + rotulo + "' etapa=" + item["etapa_indice"]
                            + "/" + totalEtapas + " tentativa=" + tentativa + " quadro=" + item["quadro"]
                            + " t=" + item["t_segundos"] + " cena=" + item["cena_ativa"]
                            + " esperar_interactable=" + item["esperar_interactable"]
                            + " gate_clique_fisico=" + item["gate_clique_fisico"]
                            + " exigir_interactable=" + item["exigir_interactable"]
                            + " fallback_historico=" + item["fallback_historico"]
                            + " modo_clique=" + item["modo_clique"]
                            + " caminho='" + (item["objeto_caminho"] ?? "?") + "'");
            }
            catch { }
        }

        [MethodImpl(MethodImplOptions.NoInlining)]
        private static string CaminhoDoObjeto(GameObject go)
        {
            // ReferenceEquals (e nao o operador == da Unity, que ECall): offline os objetos sao
            // null e o operador da engine nem carrega fora do jogo.
            if (ReferenceEquals(go, null)) return null;
            try { return Caminho(go.transform); } catch { return null; }
        }

        private int ContarClicaveis()
        {
            try
            {
                if (_clicaveis == null) return -1;
                int n = 0;
                foreach (var c in _clicaveis) if (c) n++;
                return n;
            }
            catch { return -1; }
        }

        /// <summary>KIT-14G-SEG2 — CAPTURA o estado de engine (quadro/instante/cena) em CAMPOS.
        /// Chamado SO do caminho de engine (nunca da porta offline): fora do jogo, um metodo que
        /// chame funcao de engine nem carrega (`SecurityException: ECall ...`). `NoInlining` porque
        /// o JIT embutiria este corpo (com ECall) dentro de `ColetarCandidatos`.</summary>
        [MethodImpl(MethodImplOptions.NoInlining)]
        private void CapturarEstadoDeEngine()
        {
            try { _quadroCapturado = Time.frameCount; } catch { }
            try
            {
                _tempoCapturado = Math.Round(Time.realtimeSinceStartup - _t0, 3)
                    .ToString(CultureInfo.InvariantCulture);
            }
            catch { }
            try { _cenaCapturada = UnityEngine.SceneManagement.SceneManager.GetActiveScene().name ?? ""; } catch { }
        }

        // Leituras PURAS do estado capturado (nenhuma toca a engine: os marcos usam estas).
        private string QuadroTxt() { try { return _quadroCapturado == null ? "?" : Convert.ToString(_quadroCapturado, CultureInfo.InvariantCulture); } catch { return "?"; } }
        private string TempoTxt() { return _tempoCapturado ?? "?"; }
        private string CenaTxt() { return _cenaCapturada ?? "?"; }

        [MethodImpl(MethodImplOptions.NoInlining)]
        private object QuadroAtual() { try { return Time.frameCount; } catch { return "?"; } }

        /// <summary>Instante desde o arranque — SO para o marco de vida do modo silencio (roda
        /// apenas DENTRO do jogo: o silencio so e ativado pelo caminho de engine).</summary>
        [MethodImpl(MethodImplOptions.NoInlining)]
        private string TempoSilencio()
        {
            try
            {
                return Math.Round(Time.realtimeSinceStartup - _t0, 3).ToString(CultureInfo.InvariantCulture);
            }
            catch { return "?"; }
        }

        /// <summary>MARCO proprio do caminho do clique, em ARQUIVO SEPARADO com `Flush` a cada
        /// linha. O motivo e curto e duro: o `LogOutput.log` do BepInEx fica em BUFFER e o processo
        /// que morre com `c0000005` nao esvazia o buffer (medido: o log do boot `A-sem-passivo`
        /// termina no 3o tick, apesar de a rodada ter vivido ~30 s). Sem este arquivo nao ha como
        /// dizer QUAL foi a ultima operacao do instrumento antes do acesso invalido.</summary>
        internal void MarcoClique(string linha)
        {
            try
            {
                if (_swMarcos == null && !AbrirMarcos()) return;
                _swMarcos.WriteLine(DateTime.Now.ToString("HH:mm:ss.fff", CultureInfo.InvariantCulture)
                                    + " " + linha);
                _swMarcos.Flush();
            }
            catch { }
        }

        private bool AbrirMarcos()
        {
            if (_marcosTentado) return _swMarcos != null;
            _marcosTentado = true;
            try
            {
                if (string.IsNullOrEmpty(_dir)) return false;
                Directory.CreateDirectory(_dir);
                _caminhoMarcos = Path.Combine(_dir, "marcos-clique.log").Replace('\\', '/');
                _fsMarcos = new FileStream(_caminhoMarcos, FileMode.Append, FileAccess.Write, FileShare.ReadWrite);
                _swMarcos = new StreamWriter(_fsMarcos, new UTF8Encoding(false));
                _swMarcos.AutoFlush = true;
                _res["marcos_clique_arquivo"] = _caminhoMarcos;
                _res["marcos_clique_nota"] = "arquivo proprio com Flush por linha: sobrevive a morte "
                    + "abrupta do processo (o LogOutput.log do BepInEx fica em buffer e se perde no "
                    + "c0000005). O ULTIMO marco e a ultima operacao do instrumento antes do crash.";
                return true;
            }
            catch { _swMarcos = null; return false; }
        }

        private void FecharMarcos()
        {
            try { if (_swMarcos != null) { _swMarcos.Flush(); _swMarcos.Dispose(); } } catch { }
            try { if (_fsMarcos != null) _fsMarcos.Dispose(); } catch { }
            _swMarcos = null; _fsMarcos = null;
        }

        // ------------------------------------------ A6: ida-e-volta (LEITURA opt-in)

        /// <summary>IDA-E-VOLTA — LEITURA, nao simulacao do produto (A6 da AUT-4R2).
        ///
        /// KIT-R0F/F5 — DOIS MODOS, com a ESCRITA em porta OPT-IN SEPARADA:
        ///   * PASSIVO (default): so LE o titulo/corpo que o jogo JA mostra. Permissao de
        ///     OBSERVACAO nao autoriza escrita — `DemostrarTooltip=true` sozinho NAO chama
        ///     o handler do jogo.
        ///   * DEMONSTRADOR ATIVO: exige `AutorizaEscritaTooltip=true` (autorizacao
        ///     ESPECIFICA, default FALSE). Le e guarda o titulo/corpo ORIGINAIS, chama o
        ///     HANDLER REAL (`Tooltip.ShowTooltip`) com o marcador, RELE o que o
        ///     renderizador recebeu e RESTAURA explicitamente o texto original, conferindo
        ///     a restauracao. Sem a restauracao conferida o modo NAO se declara integro.
        /// </summary>
        private void DemostrarIdaEVolta()
        {
            var r = new Dictionary<string, object>();
            string marcador = string.IsNullOrEmpty(_marcador.Value)
                ? ("AUT4-IDA-E-VOLTA-" + _sessao) : _marcador.Value;
            r["marcador"] = marcador;
            r["via"] = "Tooltip.ShowTooltip(marcador) + releitura de Tooltip.Title (LEITURA ida-e-volta)";
            object tooltip = TooltipVivo();
            r["tooltip_encontrado"] = tooltip != null;
            r["escrita_autorizada"] = _autorizaEscrita.Value;
            try
            {
                var tmpTitulo = (tooltip == null ? null : Membro(tooltip, "Title")) as TMP_Text;
                var tmpCorpo = (tooltip == null ? null : Membro(tooltip, "Description")) as TMP_Text;
                string tituloOriginal = tmpTitulo == null ? null : tmpTitulo.text;
                string corpoOriginal = tmpCorpo == null ? null : tmpCorpo.text;
                r["titulo_original_lido"] = tituloOriginal;
                r["corpo_original_lido"] = corpoOriginal;

                if (!_autorizaEscrita.Value)
                {
                    // PASSIVO: permissao de OBSERVACAO NAO autoriza escrita. Nenhuma chamada
                    // ao handler do jogo — so a leitura do que ja estava la.
                    r["modo"] = "PASSIVO";
                    r["chamou"] = false;
                    r["motivo"] = "observacao nao autoriza escrita: `AutorizaEscritaTooltip=false` (default). "
                        + "O handler Tooltip.ShowTooltip NAO foi chamado.";
                    r["titulo_lido"] = tituloOriginal;
                    r["titulo_renderizado_lido"] = tmpTitulo == null ? null : tmpTitulo.GetParsedText();
                    r["conferiu"] = false;
                    r["restauracao_conferida"] = null;   // nada foi escrito: nada a restaurar
                    Marco("AUT4 PROBE: ida-e-volta modo PASSIVO (escrita NAO autorizada) — handler nao chamado");
                    _res["ida_e_volta"] = r;
                    return;
                }

                r["modo"] = "DEMONSTRADOR_ATIVO";
                r["chamou"] = ChamarShowTooltip(tooltip, marcador, marcador + "-CORPO");
                var tmp = (tooltip == null ? null : Membro(tooltip, "Title")) as TMP_Text;
                string lido = tmp == null ? null : tmp.text;
                string lidoRenderizado = tmp == null ? null : tmp.GetParsedText();
                r["titulo_lido"] = lido;
                r["titulo_renderizado_lido"] = lidoRenderizado;
                bool conferiu = string.Equals(lido, marcador) || string.Equals(lidoRenderizado, marcador);
                r["conferiu"] = conferiu;

                // RESTAURACAO EXPLICITA do efeito: titulo/corpo VOLTAM ao valor lido antes,
                // e a volta e CONFERIDA (nao basta escrever e supor que voltou).
                bool restaurado = RestaurarTextos(tmpTitulo, tituloOriginal, tmpCorpo, corpoOriginal);
                r["titulo_restaurado"] = tmpTitulo == null ? null : tmpTitulo.text;
                r["corpo_restaurado"] = tmpCorpo == null ? null : tmpCorpo.text;
                r["restauracao_conferida"] = restaurado;
                Marco("AUT4 PROBE: ida-e-volta " + (conferiu ? "CONFERIU" : "NAO conferiu")
                    + " (marcador " + marcador + ") — restauracao " + (restaurado ? "OK" : "NAO conferida"));
            }
            catch (Exception e)
            {
                r["erro"] = e.GetType().Name + ": " + e.Message;
                r["conferiu"] = false;
            }
            _res["ida_e_volta"] = r;
        }

        /// <summary>KIT-R0F/F5 — RESTAURACAO explicita: devolve titulo/corpo ao valor lido ANTES
        /// da demonstracao e CONFERE a volta. `false` = alguma escrita de restauracao falhou
        /// (a falta fica declarada em vez de suposta).</summary>
        private static bool RestaurarTextos(TMP_Text titulo, string tituloOriginal,
                                            TMP_Text corpo, string corpoOriginal)
        {
            bool ok = true;
            try
            {
                if (titulo != null)
                {
                    titulo.text = tituloOriginal ?? "";
                    ok &= string.Equals(titulo.text, tituloOriginal ?? "");
                }
            }
            catch { ok = false; }
            try
            {
                if (corpo != null)
                {
                    corpo.text = corpoOriginal ?? "";
                    ok &= string.Equals(corpo.text, corpoOriginal ?? "");
                }
            }
            catch { ok = false; }
            return ok;
        }

        /// <summary>Chama `Tooltip.ShowTooltip` pelo HANDLER REAL (assinatura com >=6
        /// parametros), como no CAP-1 — nao inventa caminho paralelo.</summary>
        private bool ChamarShowTooltip(object tooltip, string titulo, string corpo)
        {
            if (tooltip == null) return false;
            var m = tooltip.GetType().GetMethods(BindingFlags.Public | BindingFlags.Instance)
                .FirstOrDefault(x => x.Name == "ShowTooltip" && x.GetParameters().Length >= 6);
            if (m == null) return false;
            var ps = m.GetParameters();
            var args = new object[ps.Length];
            for (int i = 0; i < ps.Length; i++) args[i] = Type.Missing;
            args[0] = titulo;
            args[1] = "";
            args[2] = null;
            args[3] = corpo;
            args[4] = null;
            if (ps[5].ParameterType == typeof(Color)) args[5] = Color.white;
            else if (ps[5].ParameterType == typeof(Color?)) args[5] = (Color?)Color.white;
            m.Invoke(tooltip, args);
            return true;
        }

        // ------------------------------------------------------------ recorder (KIT-04)

        /// <summary>KIT-14G — CONSUMIDOR DO RECORDER (a "trilha passiva" do KIT-04).
        ///
        /// O QUE FALTAVA: `AlimentarPassivo` (Adapter) grava os eventos observados no Core, e o
        /// resultado consolidado vive em `KIT04Core.CorePlugin.ResultadoFinal()`. **Ninguem lia**
        /// esse resultado dentro do processo — foi por isso que a prova do run710 terminou
        /// "INDETERMINADO" e o pedido do KIT-14G e "consumir/ler ResultadoFinal e comprovar
        /// arquivo + contagem".
        ///
        /// COMO: por REFLEXAO. O probe NAO referencia KIT04Core.dll (compila sem o Core); se o
        /// Core nao estiver carregado, o campo `status` sai `AUSENTE` declarado — nunca uma
        /// contagem `0` inventada, que seria pior que a ausencia. O que for lido vai para
        /// `recorder.json` ANTES de o perfil/area isolada serem removidos (a trilha vive na
        /// memoria do processo e desaparece com ele).</summary>
        private void LerRecorder()
        {
            var r = new Dictionary<string, object>();
            r["via"] = "KIT04Core.CorePlugin.Instancia.ResultadoFinal() por reflexao (sem referencia "
                     + "de compilacao; o probe nao depende do Core)";
            try
            {
                var t = Tipo("KIT04Core.CorePlugin");
                r["tipo_core_encontrado"] = t != null;
                object core = t == null ? null : Estatico(t, "Instancia");
                r["instancia_core"] = core != null;
                if (core == null)
                {
                    r["status"] = "AUSENTE";
                    r["motivo"] = "KIT04Core nao carregado nesta sessao: nao ha trilha para ler "
                                + "(sem opt-in `Modo/habilitado=true` do Core nao ha recorder)";
                    _res["recorder"] = r;
                    return;
                }

                var m = core.GetType().GetMethod("ResultadoFinal",
                    BindingFlags.Public | BindingFlags.Instance, null, Type.EmptyTypes, null);
                r["metodo_resultado_final"] = m != null;
                object resultado = m == null ? null : m.Invoke(core, null);
                var dic = resultado as Dictionary<string, object>;
                if (dic == null)
                {
                    r["status"] = "SEM_RESULTADO";
                    _res["recorder"] = r;
                    return;
                }

                int n = 0;
                object eventos;
                if (dic.TryGetValue("eventos", out eventos) && eventos is IEnumerable lista)
                    foreach (var _ in lista) n++;
                r["status"] = "LIDO";
                r["eventos_contados"] = n;
                r["eventos_descartados"] = dic.ContainsKey("eventos_descartados") ? dic["eventos_descartados"] : null;
                r["passivo"] = dic.ContainsKey("passivo") ? dic["passivo"] : null;
                r["sessao_core"] = dic.ContainsKey("sessao") ? dic["sessao"] : null;
                var resumo = dic.ContainsKey("passivo") ? dic["passivo"] as Dictionary<string, object> : null;
                r["passivo_chaves"] = resumo == null ? null : new List<object>(resumo.Keys);

                string caminho = CaminhoRecorder();
                File.WriteAllText(caminho, Json.Serialize(resultado), new UTF8Encoding(false));
                r["arquivo"] = caminho;
                r["arquivo_bytes"] = File.Exists(caminho) ? (object)new FileInfo(caminho).Length : null;
                r["arquivo_sha256"] = File.Exists(caminho) ? Sha256(caminho) : null;
                r["nota"] = "arquivo gravado NO PROCESSO do jogo, antes do rollback: e a prova de "
                          + "trilha que o run710 nao tinha.";
            }
            catch (Exception e)
            {
                r["status"] = "ERRO";
                r["erro"] = e.GetType().Name + ": " + e.Message;
            }
            _res["recorder"] = r;
        }

        private string CaminhoRecorder() { return Path.Combine(_dir, "recorder.json").Replace('\\', '/'); }

        // ------------------------------------------------------------ print (API Unity)

        private void PedirPrint(string nome)
        {
            string caminho = Path.Combine(_dir, nome + ".png").Replace('\\', '/');
            _arquivosDePrint.Add(caminho);
            _printAtual = caminho;
            Evento("png_" + nome + "_solicitado");
            try { ScreenCapture.CaptureScreenshot(caminho); Marco("AUT4 PROBE: print (ScreenCapture) -> " + caminho); }
            catch (Exception e) { _passos["print_" + nome] = "erro: " + e.GetType().Name + ": " + e.Message; }
        }

        private bool PrintPronto() { try { return File.Exists(_printAtual); } catch { return false; } }

        private void FecharPrint(string nome)
        {
            bool existe = false; object bytes = null;
            try { existe = File.Exists(_printAtual); if (existe) bytes = new FileInfo(_printAtual).Length; } catch { }
            _passos["print_" + nome] = Json.Campos("arquivo", _printAtual, "existe", existe, "bytes", bytes);
            // KIT-R0F/F3: o PNG passa a ter quadro de SOLICITACAO e de CONCLUSAO declarados
            // (o nome do arquivo sozinho nao diz QUANDO a captura foi pedida/terminada).
            Evento("png_" + nome + "_concluido");
            _printsDetalhe[nome] = Json.Campos("arquivo", _printAtual, "existe", existe, "bytes", bytes,
                "solicitado_frame", Frame("png_" + nome + "_solicitado"),
                "concluido_frame", Frame("png_" + nome + "_concluido"));
        }

        private object Frame(string evento)
        {
            try { object v; return _eventosFrame.TryGetValue(evento, out v) ? v : null; }
            catch { return null; }
        }

        // ------------------------------------------------------------ manifest / rollback

        private Dictionary<string, object> Manifest()
        {
            var artefatos = new List<object>();
            foreach (var caminho in _arquivosDePrint.Concat(new[] { CaminhoJson(), CaminhoRecorder() }))
            {
                var item = new Dictionary<string, object> { ["arquivo"] = Path.GetFileName(caminho) };
                try { item["bytes"] = new FileInfo(caminho).Length; item["sha256"] = Sha256(caminho); }
                catch (Exception e) { item["erro"] = e.GetType().Name; }
                artefatos.Add(item);
            }
            return Json.Campos("esquema", "AUT-4/1", "total", artefatos.Count, "artefatos", artefatos);
        }

        private Dictionary<string, object> Rollback()
        {
            return Json.Campos(
                "nota", "Rollback EXATO do que a RODADA cria. O orquestrador compara antes/depois e restaura; "
                        + "o .cfg nasce sozinho na 1a execucao e TEM de ser removido se nao existia.",
                "perfil", _perfilDir.Value,
                "probe_dir_perfil", string.IsNullOrEmpty(_perfilDir.Value) ? null
                    : Path.Combine(_perfilDir.Value, "BepInEx", "plugins", "AUT4Probe"),
                "cfg_probe", string.IsNullOrEmpty(_perfilDir.Value) ? null
                    : Path.Combine(_perfilDir.Value, "BepInEx", "config", "com.gumatos.aut4probe.cfg"),
                "arquivos_criados_pela_rodada", new List<object>(_arquivosDePrint) { CaminhoJson(), CaminhoRecorder() },
                "acao", Json.Campos("probe_dir", "REMOVER a pasta se nao existia antes",
                    "cfg", "REMOVER se nao existia; RESTAURAR se existia",
                    "log", "o LogOutput.log e truncado a cada boot: ARQUIVAR antes de lancar"));
        }

        // ------------------------------------------------------------ utilidades

        private string CaminhoJson() { return Path.Combine(_dir, "aut4probe.json").Replace('\\', '/'); }

        private void Escrever()
        {
            try
            {
                // KIT-14G-SEG2: os cliques registrados vao para TODO JSON gravado (nao so no
                // encerramento): se o processo morrer no meio da carga da run, o JSON em disco
                // ainda diz QUAL foi o ultimo clique, com quadro, instante e cena.
                if (_cliques != null && _cliques.Count > 0) _res["clique_eventos"] = _cliques;
                string destino = CaminhoJson();
                string tmp = destino + ".tmp";
                File.WriteAllText(tmp, Json.Serialize(_res), new UTF8Encoding(false));
                if (File.Exists(destino)) File.Delete(destino);
                File.Move(tmp, destino);
            }
            catch (Exception e) { try { Logger.LogError("AUT4 PROBE: gravar json: " + e.GetType().Name + ": " + e.Message); } catch { } }
        }

        private void Marco(string linha)
        {
            _marcos.Add(DateTime.Now.ToString("HH:mm:ss", CultureInfo.InvariantCulture) + " " + linha);
            Logger.LogInfo(linha);
        }

        private static string Sha256(string caminho)
        {
            using (var sha = SHA256.Create())
            using (var fs = File.OpenRead(caminho))
            {
                var hash = sha.ComputeHash(fs);
                var sb = new StringBuilder();
                foreach (var b in hash) sb.Append(b.ToString("x2"));
                return sb.ToString();
            }
        }

        internal static Type Tipo(string nome)
        {
            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                try { var t = asm.GetType(nome, false); if (t != null) return t; } catch { }
            }
            return null;
        }

        private static object Estatico(Type t, string membro)
        {
            try
            {
                var p = t.GetProperty(membro, BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
                if (p != null) return p.GetValue(null);
                var f = t.GetField(membro, BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
                if (f != null) return f.GetValue(null);
            }
            catch { }
            return null;
        }

        private static object Membro(object obj, string membro)
        {
            if (obj == null) return null;
            try
            {
                var t = obj.GetType();
                var p = t.GetProperty(membro, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
                if (p != null && p.CanRead) return p.GetValue(obj);
                var f = t.GetField(membro, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
                if (f != null) return f.GetValue(obj);
            }
            catch { }
            return null;
        }

        private static T[] Recursos<T>() where T : UnityEngine.Object
        {
            try { return Resources.FindObjectsOfTypeAll<T>(); } catch { return new T[0]; }
        }

        internal static string Nome(Shader s) { return s == null ? null : s.name; }

        internal static string Trunc(string s, int max)
        {
            if (s == null) return null;
            s = s.Replace("\r", "\\r").Replace("\n", "\\n");
            return s.Length <= max ? s : s.Substring(0, max) + "...(truncado em " + max + ")";
        }

        [MethodImpl(MethodImplOptions.NoInlining)]
        internal static string Caminho(Transform t)
        {
            try
            {
                var partes = new List<string>();
                for (var atual = t; atual != null && partes.Count < 12; atual = atual.parent) partes.Add(atual.name);
                partes.Reverse();
                return string.Join("/", partes.ToArray());
            }
            catch { return null; }
        }

        internal static Dictionary<string, object> Geometria(TMP_Text t)
        {
            try
            {
                var rt = t.rectTransform;
                if (rt == null) return null;
                var cantos = new Vector3[4];
                rt.GetWorldCorners(cantos);
                float x0 = float.MaxValue, y0 = float.MaxValue, x1 = float.MinValue, y1 = float.MinValue;
                for (int i = 0; i < 4; i++)
                {
                    var p = RectTransformUtility.WorldToScreenPoint(null, cantos[i]);
                    if (p.x < x0) x0 = p.x;
                    if (p.y < y0) y0 = p.y;
                    if (p.x > x1) x1 = p.x;
                    if (p.y > y1) y1 = p.y;
                }
                return Json.Campos(
                    "caixa_na_tela_px", Json.Campos("x", Arred(x0), "y", Arred(y0), "largura", Arred(x1 - x0), "altura", Arred(y1 - y0)),
                    "tamanho_do_rect_px", Json.Campos("largura", Arred(rt.rect.width), "altura", Arred(rt.rect.height)),
                    "escala", Arred(rt.lossyScale.x), "tela", Screen.width + "x" + Screen.height);
            }
            catch { return null; }
        }

        private static string CorDe(Color c)
        {
            return "#" + ColorUtility.ToHtmlStringRGBA(c) + " (r=" + Arred(c.r) + " g=" + Arred(c.g) + " b=" + Arred(c.b) + " a=" + Arred(c.a) + ")";
        }

        private static string CorDoMaterial(Material m, string prop)
        {
            try { return (m == null || !m.HasProperty(prop)) ? null : CorDe(m.GetColor(prop)); }
            catch { return null; }
        }

        private static float Arred(float v) { return (float)Math.Round(v, 3); }

        private static Dictionary<string, object> Aplicacao()
        {
            string cena = "";
            try { cena = UnityEngine.SceneManagement.SceneManager.GetActiveScene().name; } catch { }
            return Json.Campos(
                "produto", Application.productName, "versao_do_jogo", Application.version,
                "unity", Application.unityVersion, "cena_ativa", cena,
                "resolucao", Screen.width + "x" + Screen.height, "plataforma", Application.platform.ToString(),
                "roteiro_frame", Time.frameCount,
                // KIT-R0F/F3: `roteiro_frame` e lido no ARRANQUE (montagem de `aplicacao`),
                // NAO no quadro da coleta — o rotulo abaixo impede a leitura errada.
                "roteiro_frame_origem", "metadado do ARRANQUE: Time.frameCount no instante em que `aplicacao` foi montado (Awake); NAO e o quadro da coleta — ver `eventos_frame`",
                "tempo_de_escala_timeScale", Time.timeScale,
                "hora_local", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture));
        }

        private static object Seguro(Func<object> f) { try { return f(); } catch { return null; } }
        private static bool SeguroBool(Func<bool> f) { try { return f(); } catch { return false; } }
    }

    /// <summary>Motor de reforco: MonoBehaviour criado com cena viva (nunca no Awake).</summary>
    public class MotorDoProbe : MonoBehaviour
    {
        private void Update()
        {
            // `ReferenceEquals` (null do CLR), nao o operador == da Unity: a
            // instancia do plugin e destruida na 1a cena, e o operador da Unity
            // responderia FALSE e deixaria o motor mudo (achado A3 da AUT-4R).
            try { var i = Aut4ProbePlugin.Instancia; if (!ReferenceEquals(i, null)) i.Tick("motor"); } catch { }
        }
    }
}
