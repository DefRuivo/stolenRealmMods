// KIT-05F - PipelinePassivo: pipeline de observacao PASSIVA (sem dependencia de
// Unity/BepInEx) reutilizado pelo Core KIT-04 e pelo Adapter SR.
//
// Corrige, no lado C#, os mesmos achados F1-F5 do parecer KIT-05R (op. Python):
//   * F1 - PEDIDO != CAPTURA: `RegistrarCaptura` so cria pedido; a confirmacao
//          exige arquivo PNG real, quadro posterior ao evento e (se declarado)
//          hash SHA256 igual. Nunca afirma simultaneidade.
//   * F2 - PAUSA: em pausa nao se registra, nao se pede/confirma captura e nao
//          se materializa timeout; pendencias do intervalo nao observado sao
//          invalidadas com LACUNA explicita (sem falsa falha ao retomar).
//   * F3 - DEDUP POR FONTE (janela/contexto), nunca global; abrir->fechar->
//          reabrir sobrevive; cliques sao discretos.
//   * F4 - LIMITE explicito para TODO estado auxiliar (degradacoes, rejeitados,
//          pendencias, memoria de dedup, pedidos), com contadores agregados de
//          descarte e limpeza de referencias orfas.
//   * F5 - TIMEOUT: a janela resolve SO dentro do prazo; abertura tardia nao
//          apaga vencimento (o vencimento e materializado antes).
//
// TIPOS: apenas OBSERVADOS. Tipo ativo (clique_emitido/save/equipar/...) e
// REJEITADO. Nada aqui clica, salva, equipa ou modifica o jogo.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace KIT04Core
{
    public class PipelinePassivo
    {
        public const string CliqueRecebido = "clique_recebido";
        public const string JanelaAberta = "janela_aberta";
        public const string JanelaFechada = "janela_fechada";
        public const string Tooltip = "tooltip";
        public const string FalhaCliqueSemJanela = "falha_clique_sem_janela";
        public const string FonteGlobal = "<global>";

        public const string CapturaSolicitada = "solicitada";
        public const string CapturaConfirmada = "confirmada";

        public static readonly string[] TiposObservados = {
            CliqueRecebido, JanelaAberta, JanelaFechada, Tooltip
        };

        public static readonly HashSet<string> TiposAtivos = new HashSet<string> {
            "clique_emitido", "click_emitido", "emitir_clique",
            "save", "salvar", "save_game", "carregar_save",
            "equipar", "equipamento", "desequipar",
            "modificacao", "mutacao", "action_triggered", "acao_executada",
        };

        public static readonly HashSet<string> ChavesAtivas = new HashSet<string> {
            "acao_executada", "clique_emitido", "salvou", "equipou", "modificou",
            "escrita", "mutou", "aplicou",
        };

        private readonly int _filaMax;
        private readonly int _retencaoMax;
        private readonly int _tetoCapturas;
        private readonly int _timeoutJanelaMs;
        private readonly int _limiteAux;
        public readonly string IdSessao;

        private readonly List<Dictionary<string, object>> _eventos = new List<Dictionary<string, object>>();
        private readonly List<Dictionary<string, object>> _degradacoes = new List<Dictionary<string, object>>();
        private readonly List<Dictionary<string, object>> _rejeitados = new List<Dictionary<string, object>>();
        private readonly Dictionary<string, string> _ultimoEstado = new Dictionary<string, string>();
        private readonly List<string> _ordemEstado = new List<string>();
        private readonly Dictionary<string, Dictionary<string, object>> _pendentes = new Dictionary<string, Dictionary<string, object>>();
        private readonly List<string> _ordemPendentes = new List<string>();
        private readonly Dictionary<string, Dictionary<string, object>> _pedidos = new Dictionary<string, Dictionary<string, object>>();
        private readonly List<string> _ordemPedidos = new List<string>();
        private readonly Dictionary<string, Dictionary<string, object>> _capturas = new Dictionary<string, Dictionary<string, object>>();
        private readonly List<string> _ordemCapturas = new List<string>();

        private bool _pausado;
        private int _quadros;
        private int _capturasSolicitadas;
        private int _capturasConfirmadas;
        private int _capturasRecusadas;
        private int _degradacoesTotal;
        private int _degradacoesDescartadas;
        private int _rejeitadosTotal;
        private int _rejeitadosDescartados;
        private int _pendentesDescartados;
        private int _estadosDescartados;
        private int _lacunasTotal;
        private long _pausaInicioMs = -1;
        private long _ultimaLacunaMs = -1;

        public PipelinePassivo(int filaMax = 200, int retencaoMax = 500,
                               int tetoCapturas = 10, int timeoutJanelaMs = 1500,
                               int limiteAux = 0, string idSessao = null)
        {
            if (filaMax < 1) throw new ArgumentOutOfRangeException("filaMax");
            if (retencaoMax < 1) throw new ArgumentOutOfRangeException("retencaoMax");
            if (tetoCapturas < 0) throw new ArgumentOutOfRangeException("tetoCapturas");
            _filaMax = filaMax;
            _retencaoMax = retencaoMax;
            _tetoCapturas = tetoCapturas;
            _timeoutJanelaMs = timeoutJanelaMs;
            _limiteAux = limiteAux > 0 ? limiteAux : retencaoMax;
            IdSessao = string.IsNullOrEmpty(idSessao)
                ? "sessao-" + Guid.NewGuid().ToString("N").Substring(0, 8) : idSessao;
        }

        public bool EstaPausado { get { return _pausado; } }
        public int TetoCapturas { get { return _tetoCapturas; } }
        public int LimiteAux { get { return _limiteAux; } }
        public int PendentesRetidos { get { return _pendentes.Count; } }
        public int PedidosRetidos { get { return _pedidos.Count; } }
        public int CapturasRetidas { get { return _capturas.Count; } }

        // ------------------------------------------------------------- API ----

        public void Pausar(long agoraMs)
        {
            if (_pausado) return;
            _pausado = true;
            _pausaInicioMs = agoraMs;
            Degrada("pausado", null, "pausa segura iniciada");
            if (_pendentes.Count > 0)
            {
                int invalidadas = _pendentes.Count;
                _pendentes.Clear();
                _ordemPendentes.Clear();
                _lacunasTotal++;
                _ultimaLacunaMs = agoraMs;
                Degrada("observacao_interrompida", CliqueRecebido,
                        invalidadas.ToString(CultureInfo.InvariantCulture)
                        + " pendencia(s) invalidada(s) por pausa; intervalo nao observado");
            }
        }

        public void Retomar(long agoraMs)
        {
            if (!_pausado) return;
            _pausado = false;
            if (_lacunasTotal > 0 && _ultimaLacunaMs < 0)
            {
                _ultimaLacunaMs = agoraMs;
            }
        }

        /// <summary>
        /// Registra um evento OBSERVADO. Devolve o evento aceito ou null (com
        /// degradacao/rejeicao explicita — nada e silencioso).
        /// </summary>
        public Dictionary<string, object> Registrar(string tipo,
            Dictionary<string, object> dados = null, string janela = null, long agoraMs = 0)
        {
            dados = dados == null ? new Dictionary<string, object>()
                                  : new Dictionary<string, object>(dados);
            if (_pausado)
            {
                Degrada("pausado", tipo, "entrada descartada em pausa", agoraMs);
                return null;
            }
            if (TiposAtivos.Contains(tipo))
            {
                Rejeita(tipo, "tipo_ativo", agoraMs);
                Degrada("tipo_ativo", tipo, "modo passivo nao emite acao", agoraMs);
                return null;
            }
            bool conhecido = false;
            foreach (string t in TiposObservados) if (t == tipo) conhecido = true;
            if (!conhecido)
            {
                Rejeita(tipo, "tipo_desconhecido", agoraMs);
                Degrada("tipo_desconhecido", tipo, "fora do primeiro conjunto RSTV", agoraMs);
                return null;
            }
            foreach (string k in dados.Keys)
            {
                if (ChavesAtivas.Contains(k))
                {
                    Rejeita(tipo, "dado_ativo", agoraMs);
                    Degrada("dado_ativo", tipo, "chave de acao: " + k, agoraMs);
                    return null;
                }
            }

            // F3 - dedup POR FONTE (janela/contexto); clique e discreto.
            string fonte = janela == null ? FonteGlobal : janela;
            string assinatura = Assinatura(tipo, dados, janela);
            if (tipo != CliqueRecebido)
            {
                string anterior;
                if (_ultimoEstado.TryGetValue(fonte, out anterior) && anterior == assinatura)
                {
                    Degrada("sem_mudanca", tipo,
                            "estado repetido na fonte " + fonte + " (dedup por mudanca)", agoraMs);
                    return null;
                }
                LembraEstado(fonte, assinatura);
            }

            _quadros++;
            var quadro = JsonCampos("indice", _quadros,
                                    "captura_solicitada", false,
                                    "solicitacao_id", null,
                                    "captura_apos_atualizacao_visual", false,
                                    "captura_id", null,
                                    "captura_sha256", null,
                                    "simultaneidade_afirmada", false,
                                    "nota", "PEDIDO nao e captura; exige PNG real posterior");
            var evento = JsonCampos("esquema", "KIT-05F/observacao-passiva/2",
                                    "id", Guid.NewGuid().ToString("N"),
                                    "sessao", IdSessao,
                                    "tipo", tipo,
                                    "ts_ms", agoraMs,
                                    "dados", dados,
                                    "quadro", quadro);
            if (janela != null) evento["janela"] = janela;

            if (tipo == CliqueRecebido && janela != null)
                AdicionaPendente((string)evento["id"], janela, agoraMs + _timeoutJanelaMs);
            else if (tipo == JanelaAberta && janela != null)
                ProcessaAbertura(janela, agoraMs);

            Enfileira(evento);
            return evento;
        }

        /// <summary>F5: materializa vencidos e devolve as falhas NOVAS desta chamada.</summary>
        public List<Dictionary<string, object>> VerificarTimeouts(long agoraMs)
        {
            var criados = new List<Dictionary<string, object>>();
            if (_pausado) return criados;
            MaterializarVencidos(agoraMs, criados);
            return criados;
        }

        /// <summary>F1 (1a fase): PEDIDO de captura. Nunca marca captura.</summary>
        public Dictionary<string, object> RegistrarCaptura(string eventoId,
            string caminho = null, int? indiceQuadro = null, long agoraMs = 0)
        {
            var evento = PorId(eventoId);
            if (evento == null)
            {
                _capturasRecusadas++;
                Degrada("captura_evento_inexistente", null, eventoId, agoraMs);
                return null;
            }
            if (_pausado)
            {
                _capturasRecusadas++;
                Degrada("pausado", (string)evento["tipo"], "pedido barrado em pausa", agoraMs);
                return null;
            }
            if (_capturasSolicitadas >= _tetoCapturas)
            {
                _capturasRecusadas++;
                Degrada("teto_capturas_atingido", (string)evento["tipo"],
                        "teto_capturas=" + _tetoCapturas, agoraMs);
                return null;
            }
            int indiceEvento = (int)Quadro(evento)["indice"];
            if (indiceQuadro.HasValue && indiceQuadro.Value < indiceEvento)
            {
                _capturasRecusadas++;
                Degrada("captura_quadro_anterior", (string)evento["tipo"],
                        "quadro pedido anterior ao evento", agoraMs);
                return null;
            }
            _capturasSolicitadas++;
            string capturaId = "cap-" + Guid.NewGuid().ToString("N").Substring(0, 8);
            var pedido = JsonCampos("captura_id", capturaId, "evento_id", eventoId,
                                    "sessao", IdSessao, "caminho", caminho,
                                    "indice_quadro", indiceQuadro,
                                    "estado", CapturaSolicitada,
                                    "apos_atualizacao_visual", false,
                                    "simultaneidade_afirmada", false);
            _pedidos[capturaId] = pedido;
            _ordemPedidos.Add(capturaId);
            EnquantoExceder(_pedidos, _ordemPedidos, ref _pendentesDescartados);
            Quadro(evento)["captura_solicitada"] = true;
            Quadro(evento)["solicitacao_id"] = capturaId;
            return pedido;
        }

        /// <summary>F1 (2a fase): CONFIRMA com PNG real + quadro posterior + hash.</summary>
        public Dictionary<string, object> ConfirmarCaptura(string capturaId,
            string caminho = null, int? indiceQuadro = null, string hash = null,
            long agoraMs = 0)
        {
            Dictionary<string, object> pedido;
            if (!_pedidos.TryGetValue(capturaId, out pedido))
            {
                _capturasRecusadas++;
                Degrada("confirmacao_sem_pedido", null, capturaId, agoraMs);
                return null;
            }
            if (_pausado)
            {
                _capturasRecusadas++;
                Degrada("pausado", null, "confirmacao barrada em pausa", agoraMs);
                return null;
            }
            var evento = PorId((string)pedido["evento_id"]);
            if (evento == null)
            {
                _capturasRecusadas++;
                Degrada("captura_evento_inexistente", null, (string)pedido["evento_id"], agoraMs);
                return null;
            }
            string alvo = caminho != null ? caminho
                : (pedido["caminho"] == null ? null : (string)pedido["caminho"]);
            if (string.IsNullOrEmpty(alvo) || !File.Exists(alvo))
            {
                _capturasRecusadas++;
                pedido["estado"] = "nao_confirmada";
                Degrada("captura_sem_png_real", (string)evento["tipo"],
                        "sem arquivo PNG em " + alvo, agoraMs);
                return null;
            }
            string sha;
            try { sha = Sha256Arquivo(alvo); }
            catch (IOException ex)
            {
                _capturasRecusadas++;
                pedido["estado"] = "nao_confirmada";
                Degrada("captura_ilegivel", (string)evento["tipo"], ex.Message, agoraMs);
                return null;
            }
            if (hash != null && !string.Equals(hash, sha, StringComparison.OrdinalIgnoreCase))
            {
                _capturasRecusadas++;
                pedido["estado"] = "nao_confirmada";
                Degrada("captura_hash_divergente", (string)evento["tipo"],
                        "declarado=" + hash + " medido=" + sha, agoraMs);
                return null;
            }
            int indiceEvento = (int)Quadro(evento)["indice"];
            object indicePedido = indiceQuadro.HasValue ? (object)indiceQuadro.Value
                                                        : pedido["indice_quadro"];
            int ind = indicePedido == null ? -1 : Convert.ToInt32(indicePedido);
            if (ind <= indiceEvento)
            {
                _capturasRecusadas++;
                pedido["estado"] = "nao_confirmada";
                Degrada("captura_quadro_nao_posterior", (string)evento["tipo"],
                        "quadro=" + ind + " evento=" + indiceEvento, agoraMs);
                return null;
            }
            var captura = JsonCampos("captura_id", capturaId,
                                     "evento_id", (string)pedido["evento_id"],
                                     "sessao", IdSessao,
                                     "caminho", alvo,
                                     "indice_quadro", ind,
                                     "indice_quadro_evento", indiceEvento,
                                     "apos_atualizacao_visual", true,
                                     "sha256", sha,
                                     "tamanho_bytes", new FileInfo(alvo).Length,
                                     "simultaneidade_afirmada", false,
                                     "estado", CapturaConfirmada);
            pedido["estado"] = CapturaConfirmada;
            Quadro(evento)["captura_apos_atualizacao_visual"] = true;
            Quadro(evento)["captura_id"] = capturaId;
            Quadro(evento)["captura_sha256"] = sha;
            _capturas[(string)pedido["evento_id"]] = captura;
            _ordemCapturas.Add((string)pedido["evento_id"]);
            EnquantoExceder(_capturas, _ordemCapturas, ref _estadosDescartados);
            _capturasConfirmadas++;
            _pedidos.Remove(capturaId);
            _ordemPedidos.Remove(capturaId);
            return captura;
        }

        public List<Dictionary<string, object>> Eventos()
        {
            var copia = new List<Dictionary<string, object>>();
            foreach (var e in _eventos) copia.Add(new Dictionary<string, object>(e));
            return copia;
        }

        public List<Dictionary<string, object>> Degradacoes()
        {
            return new List<Dictionary<string, object>>(_degradacoes);
        }

        public Dictionary<string, object> Resumo()
        {
            var porTipo = new Dictionary<string, object>();
            foreach (var e in _eventos)
            {
                string t = (string)e["tipo"];
                porTipo[t] = (porTipo.ContainsKey(t) ? (int)porTipo[t] : 0) + 1;
            }
            return JsonCampos("esquema", "KIT-05F/observacao-passiva/2",
                "sessao", IdSessao,
                "modo", "passivo",
                "pausado", _pausado,
                "runtime", "NAO_EXERCITADO",
                "eventos_total", _eventos.Count,
                "eventos_por_tipo", porTipo,
                "capturas_solicitadas", _capturasSolicitadas,
                "capturas_confirmadas", _capturasConfirmadas,
                "capturas_recusadas", _capturasRecusadas,
                "teto_capturas", _tetoCapturas,
                "fila_max", _filaMax,
                "retencao_max", _retencaoMax,
                "limite_aux", _limiteAux,
                "degradacoes_retidas", _degradacoes.Count,
                "degradacoes_total", _degradacoesTotal,
                "degradacoes_descartadas", _degradacoesDescartadas,
                "rejeitados_retidos", _rejeitados.Count,
                "rejeitados_total", _rejeitadosTotal,
                "rejeitados_descartados", _rejeitadosDescartados,
                "pendentes", _pendentes.Count,
                "pendentes_descartados", _pendentesDescartados,
                "lacunas_total", _lacunasTotal,
                "simultaneidade_afirmada", false);
        }

        // ---------------------------------------------------------- internos ---

        private static Dictionary<string, object> JsonCampos(params object[] pares)
        {
            var d = new Dictionary<string, object>();
            for (int i = 0; i + 1 < pares.Length; i += 2)
                d[(string)pares[i]] = pares[i + 1];
            return d;
        }

        private static Dictionary<string, object> Quadro(Dictionary<string, object> evento)
        {
            return (Dictionary<string, object>)evento["quadro"];
        }

        private static string Assinatura(string tipo, Dictionary<string, object> dados, string janela)
        {
            var chaves = new List<string>(dados.Keys);
            chaves.Sort(StringComparer.Ordinal);
            var sb = new StringBuilder();
            sb.Append(tipo).Append('|').Append(janela == null ? "" : janela).Append('|');
            foreach (string k in chaves)
            {
                if (k == "quadro" || k == "captura" || k == "ts_ms") continue;
                sb.Append(k).Append('=').Append(Convert.ToString(dados[k], CultureInfo.InvariantCulture)).Append(';');
            }
            return sb.ToString();
        }

        private static string Sha256Arquivo(string caminho)
        {
            using (var sha = SHA256.Create())
            using (var fs = File.OpenRead(caminho))
            {
                byte[] h = sha.ComputeHash(fs);
                var sb = new StringBuilder();
                foreach (byte b in h) sb.Append(b.ToString("x2", CultureInfo.InvariantCulture));
                return sb.ToString();
            }
        }

        private void Degrada(string motivo, string tipo, string detalhe, long agoraMs = 0)
        {
            _degradacoesTotal++;
            var item = JsonCampos("motivo", motivo, "tipo", tipo, "ts_ms", agoraMs,
                                  "sessao", IdSessao);
            if (detalhe != null) item["detalhe"] = detalhe;
            _degradacoes.Add(item);
            while (_degradacoes.Count > _limiteAux)
            {
                _degradacoes.RemoveAt(0);
                _degradacoesDescartadas++;
            }
        }

        private void Rejeita(string tipo, string motivo, long agoraMs)
        {
            _rejeitadosTotal++;
            _rejeitados.Add(JsonCampos("tipo", tipo, "motivo", motivo,
                                       "ts_ms", agoraMs, "sessao", IdSessao));
            while (_rejeitados.Count > _limiteAux)
            {
                _rejeitados.RemoveAt(0);
                _rejeitadosDescartados++;
            }
        }

        private void LembraEstado(string fonte, string assinatura)
        {
            if (!_ultimoEstado.ContainsKey(fonte)) _ordemEstado.Add(fonte);
            _ultimoEstado[fonte] = assinatura;
            EnquantoExceder(_ultimoEstado, _ordemEstado, ref _estadosDescartados);
        }

        private void AdicionaPendente(string cliqueId, string janela, long prazoMs)
        {
            _pendentes[cliqueId] = JsonCampos("janela", janela, "prazo_ms", prazoMs);
            _ordemPendentes.Add(cliqueId);
            EnquantoExceder(_pendentes, _ordemPendentes, ref _pendentesDescartados);
        }

        private void EnquantoExceder<T>(Dictionary<string, T> mapa, List<string> ordem, ref int descartes)
        {
            while (mapa.Count > _limiteAux && ordem.Count > 0)
            {
                string velho = ordem[0];
                ordem.RemoveAt(0);
                mapa.Remove(velho);
                descartes++;
            }
        }

        private void LimpaReferencias(string eventoId)
        {
            _capturas.Remove(eventoId);
            _ordemCapturas.Remove(eventoId);
            var orfaos = new List<string>();
            foreach (var par in _pedidos)
                if ((string)par.Value["evento_id"] == eventoId) orfaos.Add(par.Key);
            foreach (string cid in orfaos)
            {
                _pedidos.Remove(cid);
                _ordemPedidos.Remove(cid);
            }
        }

        private void Enfileira(Dictionary<string, object> evento)
        {
            _eventos.Add(evento);
            while (_eventos.Count > _filaMax)
            {
                var sai = _eventos[0];
                _eventos.RemoveAt(0);
                LimpaReferencias((string)sai["id"]);
                Degrada("fila_cheia", (string)sai["tipo"], "fila_max=" + _filaMax);
            }
            if (_eventos.Count > _retencaoMax)
            {
                while (_eventos.Count > _retencaoMax)
                {
                    var sai = _eventos[0];
                    _eventos.RemoveAt(0);
                    LimpaReferencias((string)sai["id"]);
                }
            }
        }

        private void ProcessaAbertura(string janela, long agoraMs)
        {
            int tardias = 0;
            foreach (var par in _pendentes)
                if ((string)par.Value["janela"] == janela && agoraMs > (long)par.Value["prazo_ms"])
                    tardias++;
            if (tardias > 0)
                Degrada("janela_tardia_sem_resolucao", JanelaAberta,
                        "abertura depois do prazo; " + tardias + " pendencia(s) vencida(s)", agoraMs);
            var jogados = new List<Dictionary<string, object>>();
            MaterializarVencidos(agoraMs, jogados);
            ResolveJanela(janela, agoraMs);
        }

        private void ResolveJanela(string janela, long agoraMs)
        {
            var alvos = new List<string>();
            foreach (var par in _pendentes)
            {
                if ((string)par.Value["janela"] != janela) continue;
                if (agoraMs <= (long)par.Value["prazo_ms"]) alvos.Add(par.Key);
            }
            foreach (string cid in alvos)
            {
                _pendentes.Remove(cid);
                _ordemPendentes.Remove(cid);
            }
        }

        private void MaterializarVencidos(long agoraMs, List<Dictionary<string, object>> criados)
        {
            var vencidos = new List<string>();
            foreach (var par in _pendentes)
                if (agoraMs >= (long)par.Value["prazo_ms"]) vencidos.Add(par.Key);
            foreach (string cid in vencidos)
            {
                var pend = _pendentes[cid];
                var evento = JsonCampos("esquema", "KIT-05F/observacao-passiva/2",
                    "id", Guid.NewGuid().ToString("N"),
                    "sessao", IdSessao,
                    "tipo", FalhaCliqueSemJanela,
                    "ts_ms", agoraMs,
                    "dados", JsonCampos("clique_id", cid,
                                        "janela_alvo", pend["janela"],
                                        "motivo", "clique recebido sem janela dentro do timeout",
                                        "timeout_ms", _timeoutJanelaMs,
                                        "prazo_ms", pend["prazo_ms"]),
                    "quadro", JsonCampos("indice", _quadros,
                                        "captura_apos_atualizacao_visual", false,
                                        "simultaneidade_afirmada", false));
                _pendentes.Remove(cid);
                _ordemPendentes.Remove(cid);
                Enfileira(evento);
                criados.Add(evento);
            }
        }

        private Dictionary<string, object> PorId(string eventoId)
        {
            foreach (var e in _eventos)
                if ((string)e["id"] == eventoId) return e;
            return null;
        }
    }
}
