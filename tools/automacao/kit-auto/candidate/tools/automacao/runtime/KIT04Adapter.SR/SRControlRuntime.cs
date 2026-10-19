// KIT-RSTV-INT: controle passivo no MESMO PlayerLoop/pipeline do recorder F3.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using Burst2Flame;
using KIT04Core;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using TMPro;

namespace KIT04Adapter.SR
{
    internal sealed partial class SRControlRuntime
    {
        private readonly SRAdapterPlugin _plugin;
        private readonly PonteControleRSTV _ponte;
        private readonly string _saida, _motor, _sha;
        private readonly int _pid = Process.GetCurrentProcess().Id;
        private readonly Dictionary<string, KeyCode> _teclas = new();
        private readonly List<Dictionary<string, object>> _leituras = new();
        private readonly List<string> _invalidas = new();
        private readonly List<string> _reservadas = new(PonteControleRSTV.TeclasReservadasPadrao);
        private int _ultimoFrame = -1;
        private bool _ativo = true;
        private string? _erroContexto;
        private string? _ultimaExportacao;

        internal SRControlRuntime(SRAdapterPlugin plugin, string saida, string motor)
        {
            _plugin = plugin; _saida = saida; _motor = motor;
            _autoHabilitado = plugin.Config.Bind("AutoAvaliacao", "habilitado", false,
                "KIT-AUTO: comandos locais de acao na bancada; nao e input de teclado.");
            using (var sha = SHA256.Create())
                _sha = BitConverter.ToString(sha.ComputeHash(File.ReadAllBytes(typeof(SRControlRuntime).Assembly.Location)))
                    .Replace("-", "").ToLowerInvariant();
            var atalhos = new Dictionary<string, string>();
            foreach (var par in SRAdapterPlugin.TeclasControle)
            {
                string nome = par.Value.Value.Trim();
                if (!Enum.TryParse<KeyCode>(nome, false, out var tecla) ||
                    !Enum.IsDefined(typeof(KeyCode), tecla) || tecla == KeyCode.None ||
                    nome != tecla.ToString() || nome.StartsWith("Mouse", StringComparison.Ordinal))
                {
                    _invalidas.Add(par.Key + ":KeyCode_invalido:" + nome);
                    continue;
                }
                atalhos[par.Key] = nome;
            }
            // A tecla de chat configurada no jogo tambem e reservada.
            var kb = KeybindManager.instance;
            if (kb != null) _reservadas.Add(kb.chatKey.ToString());
            _ponte = new PonteControleRSTV(atalhos, _reservadas.ToArray(), CorePlugin.Instancia.Passivo,
                CorePlugin.Instancia.Passivo.IdSessao, pastaExport: Path.Combine(saida, "exports"));
            foreach (var par in _ponte.Atalhos) _teclas[par.Value] = (KeyCode)Enum.Parse(typeof(KeyCode), par.Value);
            if (SRAdapterPlugin.ControleIniciarObservando.Value)
                _ponte.Executar(PonteControleRSTV.Observar, AgoraMs());
            foreach (var erro in _invalidas) _plugin.RelatarRuntime("controle binding recusado: " + erro);
            foreach (var erro in _ponte.ProblemasConfig) _plugin.RelatarRuntime("controle binding recusado: " + string.Join(":", erro));
            _plugin.RelatarRuntime("controle instanciado; mesmo pipeline=True atalhos=" + _teclas.Count);
        }

        private static long AgoraMs() => (long)(Time.realtimeSinceStartup * 1000f);

        private bool FocoDeTexto()
        {
            var chat = MessageWindowManager.instance;
            if (chat != null && chat.TextInputIsFocused) return true;
            if (ItemStashManager.IsNotNullAndIsActive &&
                (LoadableUIWindow<ItemStashManager>.Instance.StashInventory.TextInputIsFocused ||
                 LoadableUIWindow<ItemStashManager>.Instance.PlayerInventory.TextInputIsFocused)) return true;
            var debug = DebugWindow.Instance;
            if (debug != null && debug.AllItemsInventory.TextInputIsFocused) return true;
            if (InventoryManager.IsNotNullAndIsActive && LoadableUIWindow<InventoryManager>.Instance.Inventory.TextInputIsFocused) return true;
            if (FortuneWindow.IsNotNullAndIsActive && LoadableUIWindow<FortuneWindow>.Instance.TextInputIsFocused) return true;
            var selected = EventSystem.current == null ? null : EventSystem.current.currentSelectedGameObject;
            if (selected != null)
            {
                var input = selected.GetComponentInParent<InputField>();
                if (input != null && input.isFocused) return true;
                var tmp = selected.GetComponentInParent<TMP_InputField>();
                if (tmp != null && tmp.isFocused) return true;
            }
            return false;
        }

        internal void Tick()
        {
            if (_ultimoFrame == Time.frameCount) return;
            _ultimoFrame = Time.frameCount;
            if (!SRAdapterPlugin.ControleHabilitado.Value)
            {
                // Opt-out em runtime interrompe coleta do controle e encerra o binding.
                Parar(); return;
            }
            if (!_ativo) return;
            bool chatAberto = true, digitando = true, remapeando = true;
            _erroContexto = null;
            try
            {
                var kb = KeybindManager.instance;
                var opcoes = OptionsManager.instance;
                remapeando = kb == null || opcoes == null || kb.DisableKeybinds || opcoes.CurrentlyBindingControls;
                var chat = MessageWindowManager.instance;
                chatAberto = chat != null && chat.gameObject.activeInHierarchy &&
                    chat.CurrentActiveMessageType == MessageWindowMessageType.Chat;
                digitando = FocoDeTexto();
            }
            catch (Exception e)
            {
                _erroContexto = e.GetType().Name + ": " + e.Message;
                // Sem certeza de contexto, nenhum atalho passa.
                chatAberto = digitando = remapeando = true;
            }
            string? janela = null;
            foreach (var nome in SRScreenManager.TelasMonitoradas)
                if (GameObject.Find(nome) != null) { janela = nome; break; }
            if (janela == null) _ponte.LimparJanela();
            _ponte.AtualizarContexto(janela, chatAberto, digitando, remapeando, Application.isFocused);
            _ponte.RegistrarLeituraEngine(Engine());
            AutoTick();
            foreach (var par in _teclas)
            {
                if (!Input.GetKeyDown(par.Value)) continue;
                // Recheca reserva de chat atual (remapeamento pode ter mudado desde o boot).
                var kb = KeybindManager.instance;
                if (kb == null || kb.chatKey == par.Value)
                {
                    _plugin.RelatarRuntime("controle tecla recusada: reserva de chat/contexto ausente " + par.Key);
                    continue;
                }
                var ev = _ponte.ProcessarTecla(par.Key, AgoraMs(), "Problema marcado em jogo (atalho " + par.Key + ")");
                if (ev != null && (string)ev["acao"] == PonteControleRSTV.Exportar)
                    _ultimaExportacao = (string)ev["caminho"];
                _leituras.Add(Json.Campos("tecla", par.Key, "frame", Time.frameCount,
                    "origem", "Unity.Input.GetKeyDown", "contexto", _ponte.ContextoAtual(),
                    "evento", ev, "degradacoes", _ponte.Degradacoes()));
                while (_leituras.Count > 100) _leituras.RemoveAt(0);
                _plugin.RelatarRuntime("controle tecla=" + par.Key + " acao=" + (ev == null ? "RECUSADA" : ev["acao"]));
                Persistir();
            }
        }

        private Dictionary<string, object> Engine() => Json.Campos(
            "origem", "Unity.PlayerLoop.PostLateUpdate", "frame", Time.frameCount,
            "pid", _pid, "motor_id", _motor, "sessao", CorePlugin.Instancia.Passivo.IdSessao,
            "adapter_sha256", _sha, "utc_unix_ms", DateTimeOffset.UtcNow.ToUnixTimeMilliseconds());

        internal void Parar()
        {
            if (!_ativo) return;
            _ativo = false;
            if (_ponte.Observando) _ponte.Executar(PonteControleRSTV.PararObservacao, AgoraMs());
            Persistir();
        }

        internal void Persistir()
        {
            var janelas = new List<string>();
            foreach (var nome in SRScreenManager.TelasMonitoradas)
                if (GameObject.Find(nome) != null) janelas.Add(nome);
            var doc = Json.Campos("esquema", "KIT-RSTV-INT/runtime/1", "engine", Engine(),
                "ativo", _ativo, "mesmo_pipeline", true, "controle", _ponte.Resumo(AgoraMs()),
                "contexto", _ponte.ContextoAtual(), "atalhos", _ponte.Atalhos,
                "teclas_invalidas", _invalidas, "problemas_atalhos", _ponte.ProblemasConfig,
                "leituras_teclado", _leituras, "marcacoes", _ponte.Marcacoes(),
                "eventos", _ponte.Eventos(), "degradacoes", _ponte.Degradacoes(),
                "janelas_ativas", janelas, "ultima_exportacao", _ultimaExportacao,
                "erro_contexto", _erroContexto, "auto_habilitado", _autoHabilitado.Value,
                "comandos_auto", _autoLeituras);
            string path = Path.Combine(_saida, "controle-runtime.json"), tmp = path + ".tmp";
            Directory.CreateDirectory(_saida);
            File.WriteAllText(tmp, Json.Serialize(doc));
            if (File.Exists(path)) File.Replace(tmp, path, null); else File.Move(tmp, path);
        }
    }
}
