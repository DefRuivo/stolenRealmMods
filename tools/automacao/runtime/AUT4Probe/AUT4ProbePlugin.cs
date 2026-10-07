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
    public class Aut4ProbePlugin : BaseUnityPlugin
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
                GanchoTodos("OptionsManager", "Localize");
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

        private void GanchoTodos(string tipo, string metodo)
        {
            try
            {
                var t = Tipo(tipo);
                if (t == null) return;
                foreach (var m in t.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static))
                {
                    if (m.Name != metodo || m.IsAbstract) continue;
                    Aplicar(m, tipo + "." + metodo + "(" + m.GetParameters().Length + " arg)");
                }
            }
            catch (Exception e) { Logger.LogWarning("AUT4 PROBE: ganchos " + tipo + "." + metodo + ": " + e.Message); }
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

        private const int F_ESPERA_UI = 0, F_LEITURA = 1, F_PRINT1 = 2, F_FINAL = 3, F_PRINT2 = 4;

        private void Passo()
        {
            switch (_fase)
            {
                case F_ESPERA_UI:
                    {
                        if (_quadros == 0) { _res["fase"] = "aguardando-ui"; Escrever(); }
                        _quadros++;
                        bool ui = false, temTexto = false;
                        try { ui = UiExiste(); } catch { }
                        try { temTexto = ui && TemTextoVisivel(); } catch { }
                        if (ui && temTexto)
                        {
                            _passos["aguardou_ui"] = Json.Campos("ok", true, "quadros_ate_a_ui", _quadros,
                                "criterio", "GUIManager.instance.tooltip != null E existe TMP_Text ativo com GetParsedText() nao vazio (a tela desenhou)");
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
                        break;
                    }

                case F_LEITURA:
                    {
                        // RSTV/AUT5-F1: GUARDA — snapshot do personagem no INICIO da
                        // leitura; o `_depois` e o MESMO objeto, atualizado no fim
                        // (AtualizarGuardasDepois), para o par antes/depois ser real.
                        IniciarSnapshotDoModal();
                        try { ColetarObservacoes(); } catch (Exception e) { _passos["coleta"] = "erro: " + e.GetType().Name + ": " + e.Message; }
                        // A6: ida-e-volta OPT-IN (LEITURA): so quando o cfg manda.
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
                        try { _res["rollback"] = Rollback(); } catch (Exception e) { _passos["rollback"] = "erro: " + e.GetType().Name; }
                        if (_navegar.Value) TentarNavegar();
                        PedirPrint("01-ui");
                        Ir(F_PRINT1, "print-01");
                        break;
                    }

                case F_PRINT1:
                    if (PrintPronto() || _quadros++ > 600) { FecharPrint("01-ui"); Ir(F_FINAL, "final"); }
                    break;

                case F_FINAL:
                    // RSTV/AUT5-F1: o "depois" das guardas e o ULTIMO estado observado.
                    AtualizarGuardasDepois();
                    PedirPrint("02-final");
                    Ir(F_PRINT2, "print-02");
                    break;

                case F_PRINT2:
                    if (PrintPronto() || _quadros++ > 600) { FecharPrint("02-final"); Finalizar(); }
                    break;
            }
        }

        private void Ir(int fase, string legivel) { _fase = fase; _quadros = 0; _res["fase"] = legivel; Escrever(); }

        private void Finalizar()
        {
            // RSTV/AUT5-F1: cobre tambem os caminhos de ABORTO (SEM_UI/orcamento):
            // as guardas refletem o ultimo estado lido nesta rodada.
            try { AtualizarGuardasDepois(); } catch { }
            try { _res["owners_harmony"] = _res.ContainsKey("owners_harmony") ? _res["owners_harmony"] : OwnersHarmony(); } catch { }
            try { _res["manifest"] = Manifest(); } catch { }
            try { _res["rollback"] = Rollback(); } catch { }
            _res["prints"] = _arquivosDePrint;
            _res["marcos"] = _marcos;
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

        private void TentarNavegar()
        {
            var estagios = new List<object>();
            try
            {
                Button alvo = null;
                int ativos = 0;
                foreach (var b in Recursos<Button>())
                {
                    if (b == null) continue;
                    if (b.gameObject.activeInHierarchy) ativos++;
                    if (alvo != null) continue;
                    var rotulo = Seguro(() => { var tt = b.GetComponentInChildren<TMP_Text>(); return tt != null ? tt.text : null; }) as string;
                    if (!string.IsNullOrEmpty(rotulo) && rotulo.IndexOf("Skills", StringComparison.OrdinalIgnoreCase) >= 0
                        && b.gameObject.activeInHierarchy) alvo = b;
                }
                estagios.Add(Json.Campos("estagio", "procurar", "botoes_ativos", ativos, "achou_skills", alvo != null));
                if (alvo != null)
                {
                    alvo.onClick.Invoke();
                    estagios.Add(Json.Campos("estagio", "clique_invocado", "objeto", alvo.gameObject.name));
                }
            }
            catch (Exception e) { estagios.Add(Json.Campos("estagio", "falha", "erro", e.GetType().Name)); }
            _passos["navegacao"] = estagios;
        }

        // ------------------------------------------ A6: ida-e-volta (LEITURA opt-in)

        /// <summary>IDA-E-VOLTA — LEITURA, nao simulacao do produto (A6 da AUT-4R2).
        ///
        /// Chama o HANDLER REAL do jogo (`Tooltip.ShowTooltip`) com um marcador unico
        /// (gerado pelo driver) e RELE o titulo do tooltip VIVO. Se o texto lido for o
        /// marcador, esta provado que a leitura le o que o renderizador recebeu — e o
        /// criterio "prova reproduzivel de leitura ida-e-volta" passa a ter instrumento.
        /// Porta OPT-IN: so roda com `DemostrarTooltip=true` (default FALSE); nenhum dado
        /// do jogo e gravado (o tooltip e repintado pelo jogo no quadro seguinte).
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
            try
            {
                r["chamou"] = ChamarShowTooltip(tooltip, marcador, marcador + "-CORPO");
                var tmp = (tooltip == null ? null : Membro(tooltip, "Title")) as TMP_Text;
                string lido = tmp == null ? null : tmp.text;
                string lidoRenderizado = tmp == null ? null : tmp.GetParsedText();
                r["titulo_lido"] = lido;
                r["titulo_renderizado_lido"] = lidoRenderizado;
                bool conferiu = string.Equals(lido, marcador) || string.Equals(lidoRenderizado, marcador);
                r["conferiu"] = conferiu;
                Marco("AUT4 PROBE: ida-e-volta " + (conferiu ? "CONFERIU" : "NAO conferiu")
                    + " (marcador " + marcador + ")");
            }
            catch (Exception e)
            {
                r["erro"] = e.GetType().Name + ": " + e.Message;
                r["conferiu"] = false;
            }
            _res["ida_e_volta"] = r;
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

        // ------------------------------------------------------------ print (API Unity)

        private void PedirPrint(string nome)
        {
            string caminho = Path.Combine(_dir, nome + ".png").Replace('\\', '/');
            _arquivosDePrint.Add(caminho);
            _printAtual = caminho;
            try { ScreenCapture.CaptureScreenshot(caminho); Marco("AUT4 PROBE: print (ScreenCapture) -> " + caminho); }
            catch (Exception e) { _passos["print_" + nome] = "erro: " + e.GetType().Name + ": " + e.Message; }
        }

        private bool PrintPronto() { try { return File.Exists(_printAtual); } catch { return false; } }

        private void FecharPrint(string nome)
        {
            bool existe = false; object bytes = null;
            try { existe = File.Exists(_printAtual); if (existe) bytes = new FileInfo(_printAtual).Length; } catch { }
            _passos["print_" + nome] = Json.Campos("arquivo", _printAtual, "existe", existe, "bytes", bytes);
        }

        // ------------------------------------------------------------ manifest / rollback

        private Dictionary<string, object> Manifest()
        {
            var artefatos = new List<object>();
            foreach (var caminho in _arquivosDePrint.Concat(new[] { CaminhoJson() }))
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
                "arquivos_criados_pela_rodada", new List<object>(_arquivosDePrint) { CaminhoJson() },
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
                "roteiro_frame", Time.frameCount, "tempo_de_escala_timeScale", Time.timeScale,
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
