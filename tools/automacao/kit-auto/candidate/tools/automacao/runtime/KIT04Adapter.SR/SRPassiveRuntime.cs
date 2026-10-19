// KIT-14F3: observador opt-in de engine, independente do MonoBehaviour do plugin.
using System;
using System.Collections.Generic;
using System.IO;
using KIT04Core;
using UnityEngine;
using UnityEngine.LowLevel;

namespace KIT04Adapter.SR
{
    internal sealed class SRPassiveRuntime
    {
        private static SRPassiveRuntime? _instancia;
        private readonly SRAdapterPlugin _plugin; // referencia CLR: Unity pode destruir o componente
        private readonly string _saida;
        private readonly string _motor = Guid.NewGuid().ToString("N");
        private readonly List<Dictionary<string, object>> _pendentes = new();
        private readonly List<Dictionary<string, object>> _capturas = new();
        private int _ultimoFrame = -1;
        private int _callbacks;
        private int _duplicados;
        private int _eventos;
        private int _observacoes;
        private int _framesComJanela;
        private Dictionary<string, object> _ultimasJanelas = new();
        private float _ultimaPersistencia = -1;
        private string? _erro;
        private SRControlRuntime? _controle;
        private bool _instalado;
        private int _motoresNoFim = -1;
        private int _frameComPluginDestruido = -1;

        private SRPassiveRuntime(SRAdapterPlugin plugin)
        {
            _plugin = plugin;
            // Caminho explicitamente configurado pelo dono da bancada, nunca perfil Default.
            _saida = Path.GetFullPath(SRAdapterPlugin.p_CaminhoSaida.Value);
        }

        internal static void Instalar(SRAdapterPlugin plugin)
        {
            if (!SRAdapterPlugin.PassivoAutorizado())
            {
                plugin.RelatarRuntime("motor OFF; callbacks=0 motores=" + ContarMotores());
                return; // nao instala delegate, evento quitting, diretorio nem arquivo
            }
            if (_instancia != null || ContarMotores() != 0)
            {
                plugin.RelatarRuntime("motor existente; instalacao duplicada recusada");
                return;
            }
            var runtime = new SRPassiveRuntime(plugin);
            var loop = PlayerLoop.GetCurrentPlayerLoop();
            if (!Inserir(ref loop, runtime.Tick))
                throw new InvalidOperationException("PostLateUpdate ausente: observador nao instalado");
            _instancia = runtime;
            PlayerLoop.SetPlayerLoop(loop);
            runtime._instalado = true;
            Application.quitting += runtime.Parar;
            plugin.RelatarRuntime("motor instalado=" + runtime._motor + " motores=" + ContarMotores());
            runtime.Persistir();
        }

        private static bool Inserir(ref PlayerLoopSystem loop, PlayerLoopSystem.UpdateFunction tick)
        {
            if (loop.type == typeof(UnityEngine.PlayerLoop.PostLateUpdate))
            {
                var sub = new List<PlayerLoopSystem>(loop.subSystemList ?? Array.Empty<PlayerLoopSystem>());
                sub.Add(new PlayerLoopSystem { type = typeof(SRPassiveRuntime), updateDelegate = tick });
                loop.subSystemList = sub.ToArray();
                return true;
            }
            if (loop.subSystemList == null) return false;
            for (int i = 0; i < loop.subSystemList.Length; i++)
                if (Inserir(ref loop.subSystemList[i], tick)) return true;
            return false;
        }

        internal static int ContarMotores() => Contar(PlayerLoop.GetCurrentPlayerLoop());
        private static int Contar(PlayerLoopSystem loop)
        {
            int total = loop.type == typeof(SRPassiveRuntime) ? 1 : 0;
            if (loop.subSystemList != null)
                foreach (var sub in loop.subSystemList) total += Contar(sub);
            return total;
        }

        private static void Remover(ref PlayerLoopSystem loop)
        {
            if (loop.subSystemList == null) return;
            var manter = new List<PlayerLoopSystem>();
            foreach (var entrada in loop.subSystemList)
            {
                if (entrada.type == typeof(SRPassiveRuntime)) continue;
                var filho = entrada;
                Remover(ref filho);
                manter.Add(filho);
            }
            loop.subSystemList = manter.ToArray();
        }

        private void Parar()
        {
            if (!_instalado) return;
            var loop = PlayerLoop.GetCurrentPlayerLoop();
            Remover(ref loop);
            PlayerLoop.SetPlayerLoop(loop);
            _instalado = false;
            _controle?.Parar();
            Application.quitting -= Parar;
            _motoresNoFim = ContarMotores();
            Persistir();
            _instancia = null;
            _plugin.RelatarRuntime("motor removido; motores=" + _motoresNoFim + " callbacks=" + _callbacks);
        }

        private void Tick()
        {
            if (!SRAdapterPlugin.PassivoAutorizado()) { Parar(); return; }
            try
            {
                int frame = Time.frameCount;
                if (_ultimoFrame == frame) { _duplicados++; return; }
                _ultimoFrame = frame;
                _callbacks++;
                if (_plugin == null && _frameComPluginDestruido < 0) _frameComPluginDestruido = frame;
                if (!_plugin.TentarVincular()) return;
#if KIT14F3_PRODUTOR_DESLIGADO
                // Mutante real: mesmo lifecycle e diagnostico; NUNCA observa nem registra evento.
#else
                ConfirmarPendentes();
                if (SRAdapterPlugin.ControleHabilitado.Value && _controle == null)
                    _controle = new SRControlRuntime(_plugin, _saida, _motor);
                _controle?.Tick();
                var nomes = SRScreenManager.TelasMonitoradas;
                var ativas = new bool[nomes.Length];
                var janelas = new Dictionary<string, object>();
                for (int i = 0; i < nomes.Length; i++)
                {
                    var go = GameObject.Find(nomes[i]);
                    ativas[i] = go != null && go.activeInHierarchy;
                    if (ativas[i])
                        janelas[nomes[i]] = Json.Campos("instance_id", go.GetInstanceID(),
                            "active_in_hierarchy", go.activeInHierarchy, "path", Caminho(go.transform));
                }
                _observacoes++;
                if (janelas.Count > 0) _framesComJanela++;
                _ultimasJanelas = janelas;
                var origem = Json.Campos("origem", "Unity.PlayerLoop.PostLateUpdate",
                    "frame", frame, "realtime_ms", AgoraMs(), "motor_id", _motor,
                    "sessao", CorePlugin.Instancia.Passivo.IdSessao, "janelas_ativas", janelas,
                    "clique_fisico_inferido", false);
                _eventos += _plugin.AlimentarPassivo(ativas, Input.GetMouseButtonDown(0), AgoraMs(), origem, PedirCaptura);
#endif
                if (Time.realtimeSinceStartup - _ultimaPersistencia >= 1f) Persistir();
            }
            catch (Exception e)
            {
                _erro = e.GetType().Name + ": " + e.Message;
                _plugin.RelatarRuntime("erro observador: " + _erro);
                Parar(); // falha fechada, sem spam por quadro
            }
        }

        private static long AgoraMs() => (long)(Time.realtimeSinceStartup * 1000f);
        private static string Caminho(Transform t)
        {
            string path = t.name;
            while (t.parent != null) { t = t.parent; path = t.name + "/" + path; }
            return path;
        }

        private void PedirCaptura(Dictionary<string, object> ev)
        {
            if ((string)ev["tipo"] != PipelinePassivo.JanelaAberta) return;
            var core = CorePlugin.Instancia;
            // Solicitar pelo pipeline limitado; nao confundir pedido com confirmacao.
            string png = Path.Combine(_saida, "passivo-" + ev["id"] + ".png");
            var pedido = core.Passivo.RegistrarCaptura((string)ev["id"], png,
                Time.frameCount, AgoraMs());
            if (pedido == null) return;
            Directory.CreateDirectory(_saida);
            pedido["engine_frame_evento"] = Time.frameCount;
            pedido["janela"] = ev["janela"];
            _pendentes.Add(pedido);
            ScreenCapture.CaptureScreenshot(png); // arquivo surge no FIM do frame, nunca confirma aqui
        }

        private void ConfirmarPendentes()
        {
            var core = CorePlugin.Instancia;
            for (int i = _pendentes.Count - 1; i >= 0; i--)
            {
                var pedido = _pendentes[i];
                int frameEvento = (int)pedido["engine_frame_evento"];
                string caminho = (string)pedido["caminho"];
                if (Time.frameCount <= frameEvento || !File.Exists(caminho)) continue;
                var captura = core.Passivo.ConfirmarCaptura((string)pedido["captura_id"], caminho,
                    Time.frameCount, null, AgoraMs());
                if (captura == null) continue;
                captura["engine_frame_evento"] = frameEvento;
                captura["engine_frame_confirmacao"] = Time.frameCount;
                captura["janela"] = pedido["janela"];
                captura["motor_id"] = _motor;
                _capturas.Add(captura);
                _pendentes.RemoveAt(i);
                Persistir();
            }
        }

        private void Persistir()
        {
            _ultimaPersistencia = Time.realtimeSinceStartup;
            var core = CorePlugin.Instancia;
            var diagnostico = Json.Campos("esquema", "KIT14F3/engine/1", "sessao", core.Passivo.IdSessao,
                "motor_id", _motor, "instalacoes", 1, "instalado", _instalado,
                "motores_no_loop", ContarMotores(), "motores_apos_remocao", _motoresNoFim,
                "callbacks", _callbacks, "callbacks_duplicados", _duplicados,
                "frame_ultimo", _ultimoFrame, "frame_plugin_destruido", _frameComPluginDestruido,
                "plugin_unity_null", _plugin == null, "plugin_clr_null", ReferenceEquals(_plugin, null),
                "plugin_updates", _plugin.UpdatesDoPlugin, "plugin_destruicoes", _plugin.DestruicoesDoPlugin,
                "core_unity_null", core == null, "core_clr_null", ReferenceEquals(core, null),
                "ponte", _plugin.DiagnosticoPonte(), "observacoes", _observacoes,
                "frames_com_janela", _framesComJanela, "ultimas_janelas", _ultimasJanelas,
                "eventos_produzidos", _eventos, "capturas", _capturas, "capturas_pendentes", _pendentes.Count,
                "erro", _erro, "simultaneidade_afirmada", false);
            Directory.CreateDirectory(_saida);
            EscreverAtomico(Path.Combine(_saida, "adapter-runtime.json"), Json.Serialize(diagnostico));
            EscreverAtomico(Path.Combine(_saida, "recorder-engine.json"), Json.Serialize(core.ResultadoFinal()));
            _controle?.Persistir();
        }

        private static void EscreverAtomico(string path, string json)
        {
            string tmp = path + ".tmp";
            File.WriteAllText(tmp, json);
            if (File.Exists(path)) File.Replace(tmp, path, null);
            else File.Move(tmp, path);
        }
    }
}
