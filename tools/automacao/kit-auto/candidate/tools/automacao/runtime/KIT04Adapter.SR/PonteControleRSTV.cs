// KIT-06 - PonteControleRSTV: plano de CONTROLE de uso do instrumento, sem
// terminal. Espelha o contrato de tools/automacao/runtime/controle_acesso.py
// (mesma logica, do lado C#).
//
// O que ela faz (e SO isso):
//   * observacao PASSIVA on/off;  pausar/retomar;  marcar problema;  exportar;
//   * atalhos configuraveis com validacao (acao desconhecida/ativa, tecla
//     reservada de chat, tecla vazia e CONFLITO sao RECUSADOS);
//   * guards de contexto: chat aberto/digitando, UI de remapeamento e ausencia
//     de foco BLOQUEIAM o atalho (o humano esta escrevendo/reconfigurando);
//   * NUNCA forca foco e NUNCA encerra a sessao do dono;
//   * NUNCA autoriza modo ativo (trava dura): nao ha acao ativa e
//     `HabilitarModoAtivo` sempre falha.
//
// ESTE ARQUIVO NAO DEPENDE DE UNITY/BepInEx de proposito: e compilado tambem
// pelo harness offline (tools/automacao/runtime/harness-controle), que prova
// guards/ligacao/estado SEM abrir o jogo. A leitura real das teclas do engine e
// a UI ficam no Adapter (KIT-G2); aqui esta o nucleo testavel.
//
// `#nullable disable`: o projeto do Adapter habilita nullable; este nucleo usa
// parametros opcionais nulos de proposito (mesma convencao do harness) e nao
// deve poluir o build com CS8625/CS8603.
#nullable disable
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Text;

namespace KIT04Adapter.SR
{
    public class PonteControleRSTV
    {
        public const string EsquemaControle = "KIT-06/controle/1";
        public const string EsquemaExport = "KIT-07/export/1";

        public const string Observar = "observar";
        public const string PararObservacao = "parar_observacao";
        public const string Pausar = "pausar";
        public const string Retomar = "retomar";
        public const string MarcarProblema = "marcar_problema";
        public const string Exportar = "exportar";

        public const string MotivoGuardChat = "guard_chat";
        public const string MotivoGuardRemapeamento = "guard_remapeamento";
        public const string MotivoGuardSemFoco = "guard_sem_foco";
        public const string MotivoSemBinding = "sem_binding";
        public const string MotivoModoAtivo = "modo_ativo_proibido";

        public static readonly string[] AcoesConhecidas = {
            Observar, PararObservacao, Pausar, Retomar, MarcarProblema, Exportar
        };

        /// <summary>Acoes ATIVAS proibidas: nao existem neste plano (trava dura).</summary>
        public static readonly string[] AcoesAtivas = {
            "clique_emitido", "emitir_clique", "save", "salvar", "equipar",
            "modificar", "habilitar_modo_ativo", "modo_ativo", "executar_acao"
        };

        /// <summary>Teclas de CHAT/digitacao reservadas por padrao.</summary>
        public static readonly string[] TeclasReservadasPadrao = {
            "Return", "KeypadEnter", "T", "Y", "Slash", "Backspace", "Space"
        };

        private readonly Dictionary<string, string> _atalhos = new Dictionary<string, string>();
        private readonly List<string[]> _problemasConfig = new List<string[]>();
        private readonly bool _temPipeline;
        private readonly KIT04Core.PipelinePassivo _pipeline;
        private readonly long _inicioRelogio;

        private readonly string _idSessao;
        private readonly int _limiteMarcacoes;
        private readonly int _limiteDegradacoes;
        private readonly int _tetoProblemas;
        private readonly string _pastaExport;

        private readonly Dictionary<string, object> _contexto =
            new Dictionary<string, object>();
        private readonly List<Dictionary<string, object>> _marcacoes =
            new List<Dictionary<string, object>>();
        private readonly List<Dictionary<string, object>> _degradacoes =
            new List<Dictionary<string, object>>();
        private readonly Dictionary<string, int> _contagemDegradacoes =
            new Dictionary<string, int>();
        private readonly List<Dictionary<string, object>> _eventos =
            new List<Dictionary<string, object>>();

        private bool _observando;
        private Dictionary<string, object> _engine;

        // Somente o Adapter que acabou de ler a engine fornece esta procedencia.
        // Harness/offline nao chama isto e continua NAO_EXERCITADO.
        internal void RegistrarLeituraEngine(Dictionary<string, object> engine)
        {
            _engine = (Dictionary<string, object>)CopiaValor(engine);
            Contexto("engine", (Dictionary<string, object>)CopiaValor(engine));
        }

        public PonteControleRSTV(Dictionary<string, string> atalhos = null,
                                 string[] teclasReservadas = null,
                                 KIT04Core.PipelinePassivo pipeline = null,
                                 string idSessao = null,
                                 int limiteMarcacoes = 200,
                                 int limiteDegradacoes = 200,
                                 int tetoProblemas = 50,
                                 string pastaExport = null)
        {
            _pipeline = pipeline;
            _temPipeline = pipeline != null;
            _idSessao = idSessao ?? ("sessao-" + Guid.NewGuid().ToString("N").Substring(0, 8));
            _limiteMarcacoes = limiteMarcacoes < 1 ? 1 : limiteMarcacoes;
            _limiteDegradacoes = limiteDegradacoes < 1 ? 1 : limiteDegradacoes;
            _tetoProblemas = tetoProblemas < 0 ? 0 : tetoProblemas;
            _pastaExport = pastaExport;
            _inicioRelogio = Environment.TickCount;
            Modo = "passivo";
            Contexto("janela", null);
            Contexto("chat_aberto", false);
            Contexto("digitando", false);
            Contexto("remapeando", false);
            Contexto("foco_no_jogo", true);
            ValidaAtalhos(atalhos ?? AtalhosPadrao(), teclasReservadas);
            // F3 (KIT-06R): OWNERSHIP EXPLICITO da coleta. Com pipeline ligado e
            // observacao DESLIGADA, o pipeline comeca PAUSADO — o indicador
            // "parado" nao pode coexistir com coleta escondida.
            if (_temPipeline && !_pipeline.EstaPausado) _pipeline.Pausar(0);
        }

        private bool PipelinePausado()
        {
            return _temPipeline && _pipeline.EstaPausado;
        }

        public string Modo { get; private set; }
        public bool ConsomeInput { get { return false; } }
        public int FocoForcado { get { return 0; } }
        public bool EncerrouSessao { get { return false; } }
        public int ModoAtivoPedidos { get; private set; }
        public bool Observando { get { return _observando; } }
        public Dictionary<string, string> Atalhos { get { return new Dictionary<string, string>(_atalhos); } }
        public List<string[]> ProblemasConfig { get { return new List<string[]>(_problemasConfig); } }

        public static Dictionary<string, string> AtalhosPadrao()
        {
            return new Dictionary<string, string>
            {
                { Observar, "F7" }, { Pausar, "F8" },
                { MarcarProblema, "F9" }, { Exportar, "F10" },
            };
        }

        private static bool Contem(string[] vetor, string valor)
        {
            if (vetor == null) return false;
            for (int i = 0; i < vetor.Length; i++)
                if (vetor[i] == valor) return true;
            return false;
        }

        /// <summary>
        /// Valida o mapa acao->tecla. Atalho com problema e REMOVIDO (nunca
        /// aceito em silencio) e o motivo fica em `ProblemasConfig`.
        /// </summary>
        public void ValidaAtalhos(Dictionary<string, string> atalhos,
                                  string[] teclasReservadas = null)
        {
            _atalhos.Clear();
            _problemasConfig.Clear();
            var reservadas = teclasReservadas ?? TeclasReservadasPadrao;
            var usadas = new Dictionary<string, string>();
            foreach (var par in atalhos)
            {
                string acao = par.Key;
                if (Contem(AcoesAtivas, acao))
                {
                    _problemasConfig.Add(new[] { acao, "acao_ativa_proibida" });
                    continue;
                }
                if (!Contem(AcoesConhecidas, acao))
                {
                    _problemasConfig.Add(new[] { acao, "acao_desconhecida" });
                    continue;
                }
                string tecla = (par.Value ?? "").Trim();
                if (tecla.Length == 0)
                {
                    _problemasConfig.Add(new[] { acao, "tecla_vazia" });
                    continue;
                }
                if (Contem(reservadas, tecla))
                {
                    _problemasConfig.Add(new[] { acao, "tecla_reservada" });
                    continue;
                }
                if (usadas.ContainsKey(tecla))
                {
                    _problemasConfig.Add(new[] { acao, "conflito_tecla" });
                    _problemasConfig.Add(new[] { usadas[tecla], "conflito_tecla" });
                    _atalhos.Remove(usadas[tecla]);
                    continue;
                }
                usadas[tecla] = acao;
                _atalhos[acao] = tecla;
            }
        }

        // -------------------------------------------------------- contexto ----
        private void Contexto(string chave, object valor) { _contexto[chave] = valor; }

        public Dictionary<string, object> AtualizarContexto(string janela = null,
            bool? chatAberto = null, bool? digitando = null, bool? remapeando = null,
            bool? focoNoJogo = null)
        {
            if (janela != null) Contexto("janela", janela);
            if (chatAberto.HasValue) Contexto("chat_aberto", chatAberto.Value);
            if (digitando.HasValue) Contexto("digitando", digitando.Value);
            if (remapeando.HasValue) Contexto("remapeando", remapeando.Value);
            if (focoNoJogo.HasValue) Contexto("foco_no_jogo", focoNoJogo.Value);
            return new Dictionary<string, object>(_contexto);
        }

        public Dictionary<string, object> ContextoAtual()
        {
            return new Dictionary<string, object>(_contexto);
        }

        /// <summary>F6 (KIT-06R): LIMPA a janela corrente (paridade com o
        /// `atualizar_contexto(janela=None)` do lado Python). Em C#, `null` em
        /// AtualizarContexto significa "manter", por isso a limpeza e explicita.</summary>
        public Dictionary<string, object> LimparJanela()
        {
            Contexto("janela", null);
            return new Dictionary<string, object>(_contexto);
        }

        private bool LerBool(string chave)
        {
            object v;
            return _contexto.TryGetValue(chave, out v) && v is bool && (bool)v;
        }

        private string GuardBloqueia()
        {
            if (LerBool("chat_aberto") || LerBool("digitando")) return MotivoGuardChat;
            if (LerBool("remapeando")) return MotivoGuardRemapeamento;
            if (!LerBool("foco_no_jogo")) return MotivoGuardSemFoco;
            return null;
        }

        // ----------------------------------------------------------- teclas ---
        public string AcaoDaTecla(string tecla)
        {
            foreach (var par in _atalhos)
                if (par.Value == tecla) return par.Key;
            return null;
        }

        /// <summary>Processa UMA tecla. Devolve o evento da acao, ou null.</summary>
        public Dictionary<string, object> ProcessarTecla(string tecla, long agoraMs,
                                                         string descricao = null)
        {
            string motivo = GuardBloqueia();
            if (motivo != null)
            {
                Degrada(motivo, "tecla=" + tecla + " ignorada pelo guard", agoraMs);
                return null;
            }
            string acao = AcaoDaTecla(tecla);
            if (acao == null)
            {
                Degrada(MotivoSemBinding, "tecla=" + tecla, agoraMs);
                return null;
            }
            return Executar(acao, agoraMs, descricao, null);
        }

        // KIT-AUTO: despacho de ACAO, nao tecla/input. Mesmos guards do teclado.
        public Dictionary<string, object> ProcessarAcao(string acao, long agoraMs, string descricao = null)
        {
            string motivo = GuardBloqueia();
            if (motivo != null)
            {
                Degrada(motivo, "acao=" + acao + " ignorada pelo guard (driver interno)", agoraMs);
                return null;
            }
            return Executar(acao, agoraMs, descricao, null);
        }

        public Dictionary<string, object> Executar(string acao, long agoraMs,
            string descricao = null, string caminho = null)
        {
            if (Contem(AcoesAtivas, acao))
            {
                Degrada("acao_ativa_proibida", "acao=" + acao, agoraMs);
                return null;
            }
            if (!Contem(AcoesConhecidas, acao))
            {
                Degrada("acao_desconhecida", "acao=" + acao, agoraMs);
                return null;
            }
            if (acao == Observar) return AlternarObservacao(agoraMs);
            if (acao == PararObservacao) return PararObservacaoInterno(agoraMs);
            if (acao == Pausar) return AlternarPausa(agoraMs);
            if (acao == Retomar) return RetomarInterno(agoraMs);
            if (acao == MarcarProblema) return MarcarProblemaInterno(descricao, "media", agoraMs);
            if (acao == Exportar) return ExportarInterno(caminho, agoraMs);
            return null;
        }

        /// <summary>F2 (KIT-06R): OBSERVAR e LIGA/DESLIGA (contrato documentado).</summary>
        private Dictionary<string, object> AlternarObservacao(long agoraMs)
        {
            return _observando ? PararObservacaoInterno(agoraMs) : IniciarObservacao(agoraMs);
        }

        private Dictionary<string, object> IniciarObservacao(long agoraMs)
        {
            if (_observando)
            {
                Degrada("ja_observando", "observacao ja estava ligada", agoraMs);
                return null;
            }
            if (!_temPipeline)
                Degrada("coleta_sem_pipeline",
                        "iniciar observacao sem pipeline ligado; coleta NAO operante",
                        agoraMs);
            _observando = true;
            Modo = "passivo";                       // trava dura
            if (_temPipeline) _pipeline.Retomar(agoraMs);
            return Evento(Observar, agoraMs, null);
        }

        /// <summary>F2 (KIT-06R): RETOMAR despachado. Retoma a coleta pausada e
        /// LIGA a observacao (senao o indicador diria "parado" coletando — F3).</summary>
        private Dictionary<string, object> RetomarInterno(long agoraMs)
        {
            if (!_temPipeline)
            {
                Degrada("sem_pipeline", "retomar sem pipeline ligado", agoraMs);
                return null;
            }
            if (!_pipeline.EstaPausado)
            {
                Degrada("ja_retomado", "nao ha coleta pausada", agoraMs);
                return null;
            }
            _pipeline.Retomar(agoraMs);
            if (!_observando) { _observando = true; Modo = "passivo"; }
            var ev = Evento(Retomar, agoraMs, null);
            ev["pausado"] = false;
            ev["observando"] = true;
            return ev;
        }

        private Dictionary<string, object> PararObservacaoInterno(long agoraMs)
        {
            if (!_observando)
            {
                Degrada("nao_observando", "parar_observacao sem observacao ativa", agoraMs);
                return null;
            }
            _observando = false;
            if (_temPipeline) _pipeline.Pausar(agoraMs);
            return Evento(PararObservacao, agoraMs, null);
        }

        private Dictionary<string, object> AlternarPausa(long agoraMs)
        {
            if (!_observando)
            {
                Degrada("pausar_sem_observacao", "nao ha coleta para pausar", agoraMs);
                return null;
            }
            if (!_temPipeline)
            {
                Degrada("sem_pipeline", "pausa sem pipeline ligado", agoraMs);
                return null;
            }
            if (_pipeline.EstaPausado)
            {
                _pipeline.Retomar(agoraMs);
                return Evento(Retomar, agoraMs, null);
            }
            _pipeline.Pausar(agoraMs);
            return Evento(Pausar, agoraMs, null);
        }

        private Dictionary<string, object> MarcarProblemaInterno(string descricao,
            string severidade, long agoraMs)
        {
            if (!_observando)
            {
                Degrada("marcar_sem_observacao",
                        "marcacao manual exige observacao ativa", agoraMs);
                return null;
            }
            if (_marcacoes.Count >= _tetoProblemas)
            {
                Degrada("teto_problemas_atingido",
                        "teto_problemas=" + _tetoProblemas.ToString(CultureInfo.InvariantCulture),
                        agoraMs);
                return null;
            }
            object janela;
            _contexto.TryGetValue("janela", out janela);
            var marcacao = new Dictionary<string, object>
            {
                { "esquema", EsquemaControle },
                { "id", "mk-" + Guid.NewGuid().ToString("N").Substring(0, 8) },
                { "sessao", _idSessao },
                { "ts_ms", agoraMs },
                { "descricao", descricao ?? "(sem descricao)" },
                { "severidade", severidade },
                { "janela", janela },
                { "pausado_no_momento", _temPipeline && _pipeline.EstaPausado },
                { "foco_forcado", false },
            };
            _marcacoes.Add(marcacao);
            while (_marcacoes.Count > _limiteMarcacoes) _marcacoes.RemoveAt(0);
            var ev = Evento(MarcarProblema, agoraMs, null);
            ev["marcacao_id"] = marcacao["id"];
            return ev;
        }

        // ---------------------------------------------------------- export ----
        public string PastaExportPadrao()
        {
            if (!string.IsNullOrEmpty(_pastaExport)) return _pastaExport;
            string raiz = AppDomain.CurrentDomain.BaseDirectory;
            return Path.Combine(raiz, "scratch", "kit", "KIT-06", "export");
        }

        public Dictionary<string, object> DocumentoExport(long agoraMs)
        {
            var doc = new Dictionary<string, object>
            {
                { "esquema", EsquemaExport },
                { "esquema_controle", EsquemaControle },
                { "sessao", _idSessao },
                { "origem", _engine == null ? "controle-offline (KIT-06); runtime=NAO_EXERCITADO" : "Unity.PlayerLoop.PostLateUpdate (dispatch kind in control telemetry)" },
                { "runtime", _engine == null ? "NAO_EXERCITADO" : "EXERCITADO" },
                { "runtime_exercitado", _engine != null },
                { "modo", Modo },
                { "observando", _observando },
                { "consome_input", ConsomeInput },
                { "foco_forcado", FocoForcado },
                { "encerrou_sessao", EncerrouSessao },
                { "contexto", ContextoAtual() },
                { "marcacoes", Marcacoes() },
                { "problemas_atalhos", CopiaProblemas() },
                { "indicador", Indicador(agoraMs) },
                { "correlacao", new Dictionary<string, object>
                    {
                        { "sessao_controle", _idSessao },
                        { "sessao_coleta", _temPipeline ? _pipeline.IdSessao : null },
                    } },
                { "trilha_controle", Eventos() },
                { "degradacoes_controle", Degradacoes() },
                { "coleta", ColetaDocumento() },
            };
            return doc;
        }

        /// <summary>F4 (KIT-06R): bloco de coleta REAL (reusa o pipeline KIT-05F;
        /// eventos/dados/lacunas retidos com correlacao; nunca fabrica runtime).</summary>
        private Dictionary<string, object> ColetaDocumento()
        {
            var b = new Dictionary<string, object>();
            b["pipeline_ligado"] = _temPipeline;
            var lacunas = new List<string>();
            if (!_temPipeline)
            {
                lacunas.Add("sem pipeline ligado: coleta NAO operante (nenhum evento retido)");
                b["lacunas_honestas"] = lacunas;
                return b;
            }
            b["resumo"] = CopiaValor(_pipeline.Resumo());
            var eventos = _pipeline.Eventos();
            // F6 (KIT-06F): SNAPSHOT DEFENSIVO PROFUNDO. `Resumo()`/`Eventos()`/
            // `Degradacoes()` do pipeline devolvem copia RASA (os dicts de topo
            // sao novos, mas `dados`/`quadro` aninhados seguem por REFERENCIA).
            // Sem `CopiaValor` aqui, mutar `doc["coleta"]["eventos"][i]["quadro"]`
            // corromperia a EVIDENCIA INTERNA do pipeline e os exports seguintes.
            b["eventos"] = CopiaValor(eventos);
            b["degradacoes"] = CopiaValor(_pipeline.Degradacoes());
            b["pedidos_retidos"] = _pipeline.PedidosRetidos;
            b["capturas_retidas"] = _pipeline.CapturasRetidas;
            if (!_observando)
                lacunas.Add("controle parado: os eventos retidos sao HISTORICO, nao coleta ativa");
            if (_observando && !_pipeline.EstaPausado && eventos.Count == 0)
                lacunas.Add("coleta ativa sem eventos retidos ate o momento (lacuna honesta)");
            b["lacunas_honestas"] = lacunas;
            return b;
        }

        private List<string[]> CopiaProblemas()
        {
            var copia = new List<string[]>();
            foreach (var p in _problemasConfig) copia.Add(new[] { p[0], p[1] });
            return copia;
        }

        private Dictionary<string, object> ExportarInterno(string caminho, long agoraMs)
        {
            if (!_observando && _marcacoes.Count == 0)
            {
                Degrada("exportar_sem_dados",
                        "nada para exportar (sem observacao e sem marcacao)", agoraMs);
                return null;
            }
            string pasta = PastaExportPadrao();
            string destino = caminho;
            if (string.IsNullOrEmpty(destino))
                destino = Path.Combine(pasta, "kit06-" + _idSessao + "-" +
                    agoraMs.ToString(CultureInfo.InvariantCulture) + ".json");
            else if (!Path.IsPathRooted(destino))
                destino = Path.Combine(pasta, destino);
            string dir = Path.GetDirectoryName(destino);
            string json = KIT04Core.Json.Serialize(DocumentoExport(agoraMs));
            // F5 (KIT-06R): falha-segura. Erro de IO NAO propaga, NAO emite evento
            // de sucesso e NAO sobrescreve conteudo alheio: degrada e devolve null.
            try
            {
                if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir))
                    Directory.CreateDirectory(dir);
                File.WriteAllText(destino, json, new UTF8Encoding(false));
            }
            catch (System.IO.IOException ex)
            {
                Degrada("export_falha_io", ex.GetType().Name + ": " + ex.Message, agoraMs);
                return null;
            }
            catch (UnauthorizedAccessException ex)
            {
                Degrada("export_falha_io", ex.GetType().Name + ": " + ex.Message, agoraMs);
                return null;
            }
            catch (System.Security.SecurityException ex)
            {
                Degrada("export_falha_io", ex.GetType().Name + ": " + ex.Message, agoraMs);
                return null;
            }
            catch (ArgumentException ex)
            {
                Degrada("export_falha_io", ex.GetType().Name + ": " + ex.Message, agoraMs);
                return null;
            }
            catch (NotSupportedException ex)
            {
                Degrada("export_falha_io", ex.GetType().Name + ": " + ex.Message, agoraMs);
                return null;
            }
            var ev = Evento(Exportar, agoraMs, null);
            ev["caminho"] = Path.GetFullPath(destino);
            return ev;
        }

        // ------------------------------------------------------- indicador ----
        public Dictionary<string, object> Indicador(long agoraMs)
        {
            bool pausado = PipelinePausado();
            string estado = !_observando ? "parado"
                : (!_temPipeline ? "sem_pipeline"
                                 : (pausado ? "pausado" : "observando"));
            bool coletaOperante = _observando && _temPipeline && !pausado;
            object janela; _contexto.TryGetValue("janela", out janela);
            int eventos = 0;
            if (_temPipeline)
            {
                object total;
                if (_pipeline.Resumo().TryGetValue("eventos_total", out total) && total is int)
                    eventos = (int)total;
            }
            return new Dictionary<string, object>
            {
                { "estado", estado },
                { "texto", "COLETA: " + estado + " | janela=" + (janela ?? "-") +
                           " | eventos=" + eventos.ToString(CultureInfo.InvariantCulture) +
                           " | marcacoes=" + _marcacoes.Count.ToString(CultureInfo.InvariantCulture) },
                { "janela", janela },
                { "eventos", eventos },
                { "marcacoes", _marcacoes.Count },
                { "modo", Modo },
                { "pipeline_ligado", _temPipeline },
                { "coleta_operante", coletaOperante },
            };
        }

        // --------------------------------------------------- trava modo ativo -
        /// <summary>TRAVA DURA: sempre falha. O instrumento e PASSIVO.</summary>
        public Dictionary<string, object> HabilitarModoAtivo(long agoraMs)
        {
            ModoAtivoPedidos++;
            Degrada(MotivoModoAtivo, "iniciar/observar nao autoriza modo ativo", agoraMs);
            return null;
        }

        // --------------------------------------------------------- internos ---
        private void Degrada(string motivo, string detalhe, long agoraMs)
        {
            int atual;
            _contagemDegradacoes.TryGetValue(motivo, out atual);
            _contagemDegradacoes[motivo] = atual + 1;
            var item = new Dictionary<string, object>
            {
                { "motivo", motivo }, { "ts_ms", agoraMs }, { "sessao", _idSessao },
            };
            if (detalhe != null) item["detalhe"] = detalhe;
            _degradacoes.Add(item);
            while (_degradacoes.Count > _limiteDegradacoes) _degradacoes.RemoveAt(0);
        }

        private Dictionary<string, object> Evento(string acao, long agoraMs,
                                                  Dictionary<string, object> detalhes)
        {
            var ev = new Dictionary<string, object>
            {
                { "acao", acao }, { "ts_ms", agoraMs }, { "sessao", _idSessao },
                { "contexto", ContextoAtual() },
            };
            if (detalhes != null)
                foreach (var par in detalhes) ev[par.Key] = par.Value;
            _eventos.Add(ev);
            while (_eventos.Count > _limiteDegradacoes) _eventos.RemoveAt(0);
            return ev;
        }

        /// <summary>F6 (KIT-06R): SNAPSHOT DEFENSIVO (deep copy) da marcacao —
        /// alterar o retorno NAO muda a evidencia interna da ponte.</summary>
        public List<Dictionary<string, object>> Marcacoes()
        {
            return CopiaListaDicionarios(_marcacoes);
        }

        public List<Dictionary<string, object>> Degradacoes()
        {
            return CopiaListaDicionarios(_degradacoes);
        }

        public List<Dictionary<string, object>> Eventos()
        {
            return CopiaListaDicionarios(_eventos);
        }

        private static List<Dictionary<string, object>> CopiaListaDicionarios(
            List<Dictionary<string, object>> origem)
        {
            var copia = new List<Dictionary<string, object>>();
            foreach (var item in origem)
                copia.Add((Dictionary<string, object>)CopiaValor(item));
            return copia;
        }

        /// <summary>Copia PROFUNDA de valores aninhados (dicionarios/listas).</summary>
        private static object CopiaValor(object v)
        {
            if (v == null) return null;
            var d = v as Dictionary<string, object>;
            if (d != null)
            {
                var novo = new Dictionary<string, object>();
                foreach (var par in d) novo[par.Key] = CopiaValor(par.Value);
                return novo;
            }
            var ld = v as List<Dictionary<string, object>>;
            if (ld != null) return CopiaListaDicionarios(ld);
            var ls = v as List<string>;
            if (ls != null) return new List<string>(ls);
            var lobj = v as System.Collections.IList;
            if (lobj != null)
            {
                var novo = new List<object>();
                foreach (var item in lobj) novo.Add(CopiaValor(item));
                return novo;
            }
            return v;
        }

        public Dictionary<string, int> ContagemDegradacoes()
        {
            return new Dictionary<string, int>(_contagemDegradacoes);
        }

        public Dictionary<string, object> Resumo(long agoraMs)
        {
            var mapa = new Dictionary<string, object>();
            foreach (var par in _contagemDegradacoes) mapa[par.Key] = par.Value;
            return new Dictionary<string, object>
            {
                { "esquema", EsquemaControle },
                { "sessao", _idSessao },
                { "modo", Modo },
                { "observando", _observando },
                { "pausado", _temPipeline && _pipeline.EstaPausado },
                { "consome_input", ConsomeInput },
                { "foco_forcado", FocoForcado },
                { "encerrou_sessao", EncerrouSessao },
                { "modo_ativo_pedidos", ModoAtivoPedidos },
                { "atalhos_validos", _atalhos.Count },
                { "problemas_atalhos", _problemasConfig.Count },
                { "marcacoes", _marcacoes.Count },
                { "degradacoes", _degradacoes.Count },
                { "degradacoes_por_motivo", mapa },
                { "indicador", Indicador(agoraMs) },
                { "runtime", _engine == null ? "NAO_EXERCITADO" : "EXERCITADO" },
                { "runtime_exercitado", _engine != null },
            };
        }
    }
}
