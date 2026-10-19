// KIT-06 - harness OFFLINE do plano de controle (PonteControleRSTV).
//
// Prova, SEM abrir/instalar o jogo:
//   * atalhos configuraveis com validacao (desconhecida/ativa/reservada/vazia/
//     conflito RECUSADAS);
//   * guards de contexto (chat/digitando, remapeamento, sem foco) bloqueiam o
//     atalho com degradacao explicita;
//   * iniciar observacao NUNCA autoriza modo ativo (trava dura);
//   * sem foco forcado e sem encerrar a sessao do dono;
//   * pausa/retomada REAIS ligadas ao pipeline KIT-05F (PipelinePassivo);
//   * marcacao manual com contexto e teto;
//   * export local (JSON) sem Hermes/IA, rotulado runtime=NAO_EXERCITADO,
//     com a EVIDENCIA retida e falha-segura de IO.
//
// Uso:
//   dotnet run --project tools/automacao/runtime/harness-controle
//   dotnet run --project tools/automacao/runtime/harness-controle -- --defeito guard
//   dotnet run --project tools/automacao/runtime/harness-controle -- --defeito ataque
//
// ORACULO DO CONTROLE NEGATIVO (correcao F7 do KIT-06R):
//   Cada verificacao tem um ID ESTAVEL. Um `--defeito <nome>` declara o conjunto
//   EXATO de IDs que DEVEM falhar. O harness so e VERDE (exit 0) quando o
//   conjunto de falhas observado e EXATAMENTE o declarado: falha extra, falha
//   ausente, nome de defeito nao suportado ou infraestrutura recusam (exit != 0).
//   Assim um defeito REAL plantado no fonte (ex.: ConsomeInput false->true) gera
//   uma falha EXTRA e NAO passa por verde.
//
// Exit: 0 = verificacoes OK (inclusive no --defeito, quando as falhas batem o
// conjunto esperado); 1 = falhou / falso verde / conjunto != declarado;
// 2 = uso/infraestrutura (nome de defeito nao suportado).
using System;
using System.Collections.Generic;
using System.IO;
using KIT04Adapter.SR;
using KIT04Core;

namespace HarnessControle
{
    internal static class Program
    {
        private static int _oks;
        private static readonly List<string> _falhasIds = new List<string>();
        private static string _defeito;

        // Conjunto EXATO de IDs que cada defeito simulado DEVE fazer falhar.
        private static readonly Dictionary<string, string[]> Defeitos =
            new Dictionary<string, string[]>
        {
            { "guard", new[] {
                "guard_chat.atalho_nao_dispara",
                "guard_chat.observacao_nao_iniciou",
                "guard_chat.degradacao_registrada" } },
            { "ataque", new[] {
                "config.tecla_reservada_recusada",
                "config.nenhum_atalho_invalido_sobrevive" } },
        };

        private static int Main(string[] argv)
        {
            for (int i = 0; i < argv.Length; i++)
            {
                if (argv[i] == "--defeito" && i + 1 < argv.Length)
                {
                    _defeito = argv[++i];
                    if (!Defeitos.ContainsKey(_defeito))
                    {
                        Console.WriteLine("uso: HarnessControle [--defeito guard|ataque]");
                        Console.WriteLine("defeito NAO suportado: " + _defeito);
                        return 2;
                    }
                }
                else
                {
                    Console.WriteLine("uso: HarnessControle [--defeito guard|ataque]");
                    return 2;
                }
            }
            Console.WriteLine("============================================================");
            Console.WriteLine(" KIT-06 harness offline do plano de controle (atalhos/guards)");
            Console.WriteLine(" defeito simulado: " + (_defeito ?? "(nenhum)"));
            Console.WriteLine("============================================================");

            VerificaAcaoInterna();
            VerificaAtalhosPadrao();
            VerificaValidacaoConfig();
            VerificaGuardChat();
            VerificaGuardRemapeamento();
            VerificaGuardSemFoco();
            VerificaObservarPassivo();
            VerificaTravaModoAtivo();
            VerificaPausaIntegrada();
            VerificaMarcacao();
            VerificaEvidenciaDefensiva();
            VerificaExport();
            VerificaIndicador();
            VerificaNaoEncerraSessao();

            Console.WriteLine("============================================================");
            Console.WriteLine(" verificacoes: " + _oks + " OK, " + _falhasIds.Count + " FALHA");
            if (_defeito == null)
            {
                if (_falhasIds.Count > 0)
                {
                    Console.WriteLine(" VEREDITO HARNESS: VERMELHO (exit 1) -> " +
                                      string.Join(",", _falhasIds));
                    return 1;
                }
                Console.WriteLine(" VEREDITO HARNESS: VERDE (exit 0)");
                return 0;
            }

            // Controle negativo: exige CONJUNTO EXATO de falhas.
            var esperado = new HashSet<string>(Defeitos[_defeito]);
            var obtido = new HashSet<string>(_falhasIds);
            var extras = new List<string>();
            foreach (var id in obtido) if (!esperado.Contains(id)) extras.Add(id);
            var faltando = new List<string>();
            foreach (var id in esperado) if (!obtido.Contains(id)) faltando.Add(id);
            extras.Sort();
            faltando.Sort();
            if (extras.Count == 0 && faltando.Count == 0)
            {
                Console.WriteLine(" VEREDITO HARNESS: VERDE do controle negativo " +
                                  "(conjunto EXATO de " + esperado.Count +
                                  " falha(s) detectado)");
                return 0;
            }
            Console.WriteLine(" VEREDITO HARNESS: FALSO VERDE / conjunto != declarado");
            if (extras.Count > 0)
                Console.WriteLine("   falhas EXTRAS (nao declaradas): " + string.Join(",", extras));
            if (faltando.Count > 0)
                Console.WriteLine("   falhas AUSENTES (declaradas e nao observadas): " +
                                  string.Join(",", faltando));
            return 1;
        }

        private static void Checa(string id, bool condicao, string detalhe = null)
        {
            if (condicao) { _oks++; Console.WriteLine("[OK    ] " + id); }
            else
            {
                _falhasIds.Add(id);
                Console.WriteLine("[FALHA ] " + id + (detalhe == null ? "" : " -> " + detalhe));
            }
        }

        private static PonteControleRSTV Nova(Dictionary<string, string> atalhos = null,
            string[] reservadas = null, PipelinePassivo pipeline = null, string pasta = null)
        {
            return new PonteControleRSTV(atalhos, reservadas, pipeline, "harness",
                                         200, 200, 50, pasta);
        }

        private static string Contagem(Dictionary<string, int> mapa, string chave)
        {
            int v;
            return mapa.TryGetValue(chave, out v) ? v.ToString() : "0";
        }

        // ----------------------------------------------------------------------
        private static void VerificaAcaoInterna()
        {
            string[] acoes = { PonteControleRSTV.Observar, PonteControleRSTV.Pausar,
                PonteControleRSTV.Retomar, PonteControleRSTV.MarcarProblema, PonteControleRSTV.Exportar };
            foreach (string guard in new[] { "chat", "digitando", "remap", "foco" })
            foreach (string acao in acoes)
            {
                var p = Nova();
                p.AtualizarContexto(chatAberto: guard == "chat", digitando: guard == "digitando",
                    remapeando: guard == "remap", focoNoJogo: guard != "foco");
                string motivo = guard == "chat" || guard == "digitando" ? PonteControleRSTV.MotivoGuardChat
                    : guard == "remap" ? PonteControleRSTV.MotivoGuardRemapeamento : PonteControleRSTV.MotivoGuardSemFoco;
                Checa("acao_interna.guard_" + guard + "." + acao,
                    p.ProcessarAcao(acao, 1) == null && p.Eventos().Count == 0
                    && p.Degradacoes().Count == 1 && (string)p.Degradacoes()[0]["motivo"] == motivo);
            }
            var ponte = Nova();
            Checa("acao_interna.observar", ponte.ProcessarAcao(PonteControleRSTV.Observar, 2) != null);
            Checa("acao_interna.marcar", ponte.ProcessarAcao(PonteControleRSTV.MarcarProblema, 3, "checkpoint") != null);
            Checa("acao_interna.gameplay_recusado", ponte.ProcessarAcao("salvar", 4) == null);
            Checa("acao_interna.desconhecida_recusada", ponte.ProcessarAcao("voar", 5) == null);
            Checa("acao_interna.offline_nao_runtime", (bool)ponte.DocumentoExport(6)["runtime_exercitado"] == false);
        }

        private static void VerificaAtalhosPadrao()
        {
            var ponte = Nova();
            Checa("atalhos_padrao.4_validos", ponte.Atalhos.Count == 4,
                  "validos=" + ponte.Atalhos.Count);
            Checa("atalhos_padrao.0_problemas", ponte.ProblemasConfig.Count == 0,
                  "problemas=" + ponte.ProblemasConfig.Count);
            Checa("atalhos_padrao.f7_observar",
                  ponte.AcaoDaTecla("F7") == PonteControleRSTV.Observar);
        }

        private static void VerificaValidacaoConfig()
        {
            // Defeito 'ataque': o chamador ESQUECE de declarar as teclas de chat
            // (lista vazia), como uma UI defeituosa faria — e a validacao deve
            // ACUSAR que "Return" virou atalho valido de coleta.
            string[] reservadas = _defeito == "ataque" ? new string[0] : null;
            const string teclaConflito = "F7";
            var cfg = new Dictionary<string, string>
            {
                { "voar", "F1" },                                   // acao desconhecida
                { "habilitar_modo_ativo", "F2" },                   // acao ativa
                { PonteControleRSTV.Observar, "Return" },           // tecla reservada
                { PonteControleRSTV.Pausar, "   " },                // tecla vazia
                { PonteControleRSTV.MarcarProblema, teclaConflito },
                { PonteControleRSTV.Exportar, teclaConflito },      // conflito
            };
            var ponte = Nova(cfg, reservadas);
            var motivos = new List<string>();
            foreach (var p in ponte.ProblemasConfig) motivos.Add(p[1]);
            Checa("config.acao_desconhecida_recusada", motivos.Contains("acao_desconhecida"));
            Checa("config.acao_ativa_recusada", motivos.Contains("acao_ativa_proibida"));
            Checa("config.tecla_reservada_recusada", motivos.Contains("tecla_reservada"));
            Checa("config.tecla_vazia_recusada", motivos.Contains("tecla_vazia"));
            Checa("config.conflito_recusado", motivos.Contains("conflito_tecla"));
            Checa("config.nenhum_atalho_invalido_sobrevive",
                  ponte.Atalhos.Count == 0, "validos=" + ponte.Atalhos.Count);
        }

        private static void VerificaGuardChat()
        {
            var ponte = Nova();
            bool reportaChat = _defeito != "guard";      // defeito: chamador omite o chat
            ponte.AtualizarContexto(chatAberto: reportaChat);
            var ev = ponte.ProcessarTecla("F7", 0);
            Checa("guard_chat.atalho_nao_dispara", ev == null,
                  ev == null ? "" : "acao=" + ev["acao"]);
            Checa("guard_chat.observacao_nao_iniciou", !ponte.Observando);
            Checa("guard_chat.degradacao_registrada",
                  Contagem(ponte.ContagemDegradacoes(),
                           PonteControleRSTV.MotivoGuardChat) != "0",
                  "guard_chat=" + Contagem(ponte.ContagemDegradacoes(),
                                           PonteControleRSTV.MotivoGuardChat));
        }

        private static void VerificaGuardRemapeamento()
        {
            var ponte = Nova();
            ponte.AtualizarContexto(remapeando: true);
            var ev = ponte.ProcessarTecla("F8", 0);
            Checa("guard_remapeamento.atalho_nao_dispara", ev == null);
            Checa("guard_remapeamento.degradacao_registrada",
                  Contagem(ponte.ContagemDegradacoes(),
                           PonteControleRSTV.MotivoGuardRemapeamento) != "0");
        }

        private static void VerificaGuardSemFoco()
        {
            var ponte = Nova();
            ponte.AtualizarContexto(focoNoJogo: false);
            var ev = ponte.ProcessarTecla("F7", 0);
            Checa("guard_sem_foco.atalho_nao_dispara", ev == null);
            Checa("guard_sem_foco.sem_foco_forcado", ponte.FocoForcado == 0,
                  "foco_forcado=" + ponte.FocoForcado);
            Checa("guard_sem_foco.sem_consumo_input", !ponte.ConsomeInput);
            Checa("guard_sem_foco.degradacao_registrada",
                  Contagem(ponte.ContagemDegradacoes(),
                           PonteControleRSTV.MotivoGuardSemFoco) != "0");
        }

        private static void VerificaObservarPassivo()
        {
            var ponte = Nova();
            var ev = ponte.ProcessarTecla("F7", 0);
            Checa("observar.inicia",
                  ev != null && (string)ev["acao"] == PonteControleRSTV.Observar);
            Checa("observar.modo_passivo", ponte.Modo == "passivo", "modo=" + ponte.Modo);
            // CONTRATO KIT-06F: OBSERVAR e LIGA/DESLIGA — o 2o F7 DESLIGA a
            // coleta (nao e degradacao "ja_observando").
            var ev2 = ponte.ProcessarTecla("F7", 0);
            Checa("observar.segundo_f7_desliga",
                  ev2 != null && (string)ev2["acao"] == PonteControleRSTV.PararObservacao
                  && !ponte.Observando);
        }

        private static void VerificaTravaModoAtivo()
        {
            var ponte = Nova();
            ponte.Executar(PonteControleRSTV.Observar, 0);
            var r = ponte.HabilitarModoAtivo(0);
            Checa("trava_modo_ativo.habilitar_falha", r == null);
            Checa("trava_modo_ativo.modo_passivo", ponte.Modo == "passivo",
                  "modo=" + ponte.Modo);
            Checa("trava_modo_ativo.pedido_contabilizado", ponte.ModoAtivoPedidos == 1,
                  "pedidos=" + ponte.ModoAtivoPedidos);
            Checa("trava_modo_ativo.acao_ativa_recusada",
                  ponte.Executar("emitir_clique", 0) == null
                  && Contagem(ponte.ContagemDegradacoes(), "acao_ativa_proibida") != "0");
        }

        private static void VerificaPausaIntegrada()
        {
            var pipeline = new PipelinePassivo(200, 200, 10, 100, 0, "harness");
            var ponte = Nova(pipeline: pipeline);
            ponte.Executar(PonteControleRSTV.Observar, 0);
            ponte.Executar(PonteControleRSTV.Pausar, 0);
            Checa("pausa.pausar_delega_pipeline", pipeline.EstaPausado);
            Checa("pausa.pipeline_barra_registro",
                  pipeline.Registrar(PipelinePassivo.CliqueRecebido, null, "InventoryPanel", 0) == null);
            ponte.Executar(PonteControleRSTV.Pausar, 0);       // alterna: retoma
            Checa("pausa.retomar_desliga", !pipeline.EstaPausado);
            Checa("pausa.registra_apos_retomar",
                  pipeline.Registrar(PipelinePassivo.CliqueRecebido, null, "InventoryPanel", 1) != null);
        }

        private static void VerificaMarcacao()
        {
            var pipeline = new PipelinePassivo(200, 200, 10, 100, 0, "harness");
            var ponte = Nova(pipeline: pipeline);
            Checa("marcacao.sem_observacao_recusada",
                  ponte.Executar(PonteControleRSTV.MarcarProblema, 0, "cedo demais") == null);
            ponte.Executar(PonteControleRSTV.Observar, 0);
            ponte.AtualizarContexto(janela: "InventoryPanel");
            var ev = ponte.ProcessarTecla("F9", 10, "tooltip cortado");
            Checa("marcacao.f9_registra",
                  ev != null && (string)ev["acao"] == PonteControleRSTV.MarcarProblema);
            var m = ponte.Marcacoes();
            Checa("marcacao.contexto_janela",
                  m.Count == 1 && (string)m[0]["janela"] == "InventoryPanel");
            Checa("marcacao.descricao",
                  m.Count == 1 && (string)m[0]["descricao"] == "tooltip cortado");
        }

        private static void VerificaEvidenciaDefensiva()
        {
            // F6 (KIT-06F): o documento exportado e um SNAPSHOT DEFENSIVO tambem
            // dos objetos ANINHADOS do pipeline (coleta.eventos[*].quadro/dados).
            // Mutar o documento NAO pode contaminar a evidencia interna nem o
            // export seguinte.
            var pipeline = new PipelinePassivo(200, 200, 10, 100, 0, "harness");
            var ponte = Nova(pipeline: pipeline);
            ponte.Executar(PonteControleRSTV.Observar, 0);
            pipeline.Registrar(PipelinePassivo.CliqueRecebido, null, "InventoryPanel", 1);

            var doc = ponte.DocumentoExport(2);
            var eventos = (List<Dictionary<string, object>>)
                ((Dictionary<string, object>)doc["coleta"])["eventos"];
            var quadro = (Dictionary<string, object>)eventos[0]["quadro"];
            var dados = (Dictionary<string, object>)eventos[0]["dados"];
            quadro["nota"] = "ALTERADO PELO CONSUMIDOR";
            dados["injetado"] = "ALTERADO";

            var doc2 = ponte.DocumentoExport(3);
            var ev2 = ((List<Dictionary<string, object>>)
                ((Dictionary<string, object>)doc2["coleta"])["eventos"])[0];
            var interno = pipeline.Eventos()[0];
            var notaDoc = (string)((Dictionary<string, object>)ev2["quadro"])["nota"];
            var notaInt = (string)((Dictionary<string, object>)interno["quadro"])["nota"];
            Checa("evidencia.coleta_aninhado_somente_leitura",
                  notaDoc != "ALTERADO PELO CONSUMIDOR"
                  && notaInt != "ALTERADO PELO CONSUMIDOR",
                  "doc2=" + notaDoc + "; interno=" + notaInt);
            Checa("evidencia.coleta_dados_somente_leitura",
                  !((Dictionary<string, object>)ev2["dados"]).ContainsKey("injetado")
                  && !((Dictionary<string, object>)interno["dados"]).ContainsKey("injetado"));
        }

        private static void VerificaExport()
        {
            string pasta = Path.Combine(Path.GetTempPath(), "harness-controle-kit06");
            var ponte = Nova(pasta: pasta);
            Checa("export.sem_dados_recusado",
                  ponte.Executar(PonteControleRSTV.Exportar, 0) == null);
            ponte.Executar(PonteControleRSTV.Observar, 0);
            ponte.Executar(PonteControleRSTV.MarcarProblema, 0, "contraste baixo");
            var ev = ponte.Executar(PonteControleRSTV.Exportar, 0);
            string caminho = ev == null ? null : (string)ev["caminho"];
            Checa("export.grava_arquivo_local",
                  caminho != null && File.Exists(caminho), "caminho=" + caminho);
            string texto = caminho != null && File.Exists(caminho) ? File.ReadAllText(caminho) : "";
            Checa("export.rotula_nao_exercitado", texto.Contains("NAO_EXERCITADO"));
            Checa("export.declara_contrato_kit07", texto.Contains("KIT-07/export/1"));
            Checa("export.foco_forcado_zero", texto.Contains("\"foco_forcado\":0"));
        }

        private static void VerificaIndicador()
        {
            var pipeline = new PipelinePassivo(200, 200, 10, 100, 0, "harness");
            var ponte = Nova(pipeline: pipeline);
            Checa("indicador.parado", (string)ponte.Indicador(0)["estado"] == "parado");
            ponte.Executar(PonteControleRSTV.Observar, 0);
            Checa("indicador.observando", (string)ponte.Indicador(0)["estado"] == "observando");
            ponte.Executar(PonteControleRSTV.Pausar, 0);
            Checa("indicador.pausado", (string)ponte.Indicador(0)["estado"] == "pausado");
            ponte.AtualizarContexto(janela: "MapPanel");
            Checa("indicador.mostra_contexto",
                  ((string)ponte.Indicador(0)["texto"]).Contains("MapPanel"));
        }

        private static void VerificaNaoEncerraSessao()
        {
            var ponte = Nova();
            ponte.Executar(PonteControleRSTV.Observar, 0);
            ponte.Executar(PonteControleRSTV.PararObservacao, 0);
            Checa("parar.nao_encerra_sessao", !ponte.EncerrouSessao);
            Checa("parar.desliga_coleta", !ponte.Observando);
        }
    }
}
