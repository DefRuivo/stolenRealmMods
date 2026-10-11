// KIT-05F - harness OFFLINE da trilha passiva (F8).
//
// Prova, SEM abrir/instalar o jogo, que a ponte Core+Adapter tem LIGACAO e
// ESTADO: transicoes reais de tela -> janela_aberta/janela_fechada; clique
// observado -> clique_recebido; pipeline limitado (fila/auxiliares finitos);
// timeout derivado com motivo; captura em duas fases (pedido != confirmacao);
// opt-in false = inerte.
//
// Uso:
//   dotnet run --project tools/automacao/runtime/harness-passivo
//   dotnet run --project tools/automacao/runtime/harness-passivo -- --defeito opt_in
//
// Exit: 0 = todas as verificacoes passaram; 1 = alguma falhou (inclusive no modo
// --defeito, onde a falha e o resultado ESPERADO do controle negativo);
// 2 = uso/infraestrutura.
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using KIT04Adapter.SR;
using KIT04Core;

namespace HarnessPassivo
{
    internal static class Program
    {
        private static int _falhas;
        private static int _oks;
        private static string _defeito;

        private static readonly string[] Telas = {
            "InventoryPanel", "SkillsPanel", "EquipmentPanel", "MapPanel"
        };

        private static int Main(string[] argv)
        {
            for (int i = 0; i < argv.Length; i++)
            {
                if (argv[i] == "--defeito" && i + 1 < argv.Length) { _defeito = argv[++i]; }
                else { Console.WriteLine("uso: HarnessPassivo [--defeito opt_in]"); return 2; }
            }
            Console.WriteLine("============================================================");
            Console.WriteLine(" KIT-05F harness offline da trilha passiva (Core + Adapter)");
            Console.WriteLine(" defeito simulado: " + (_defeito ?? "(nenhum)"));
            Console.WriteLine("============================================================");

            VerificaOptInInerte();
            VerificaTransicoesDeTela();
            VerificaSemRepeticaoPorFrame();
            VerificaTimeoutComMotivo();
            VerificaCliqueSemJanelaNunca();
            VerificaLimitesSobMuitosQuadros();
            VerificaCapturaEmDuasFases();
            VerificaPausaSegura();

            Console.WriteLine("============================================================");
            Console.WriteLine(" verificacoes: " + _oks + " OK, " + _falhas + " FALHA");
            if (_defeito == null && _falhas > 0)
            {
                Console.WriteLine(" VEREDITO HARNESS: VERMELHO (exit 1)");
                return 1;
            }
            if (_defeito != null && _falhas == 0)
            {
                Console.WriteLine(" VEREDITO HARNESS: FALSO VERDE — o defeito simulado NAO foi detectado");
                return 1;
            }
            Console.WriteLine(" VEREDITO HARNESS: " + (_defeito != null
                ? "VERDE do controle negativo (defeito detectado como esperado)"
                : "VERDE (exit 0)"));
            return 0;
        }

        private static void Checa(string nome, bool condicao, string detalhe = null)
        {
            if (condicao) { _oks++; Console.WriteLine("[OK    ] " + nome); }
            else
            {
                _falhas++;
                Console.WriteLine("[FALHA ] " + nome + (detalhe == null ? "" : " -> " + detalhe));
            }
        }

        private static PontePassivaRSTV NovaPonte(bool habilitado, int filaMax = 200,
            int retencaoMax = 200, int tetoCapturas = 10, int timeoutMs = 100)
        {
            return new PontePassivaRSTV(Telas, habilitado, filaMax, retencaoMax,
                                        tetoCapturas, timeoutMs, "harness");
        }

        private static bool[] Estado(int indice)
        {
            var v = new bool[Telas.Length];
            if (indice >= 0) v[indice] = true;
            return v;
        }

        private static void VerificaOptInInerte()
        {
            // No modo --defeito opt_in simulamos uma ponte que IGNORA a flag.
            bool habilitadoDeFato = _defeito == "opt_in";
            var ponte = NovaPonte(habilitadoDeFato);
            var novos = ponte.Observar(Estado(0), true, 0);
            Checa("opt-in false => Observar devolve nada", novos.Count == 0,
                  "eventos=" + novos.Count);
            Checa("opt-in false => pipeline inerte (0 eventos)",
                  ponte.Pipeline.Resumo()["eventos_total"].Equals(0),
                  "eventos_total=" + ponte.Pipeline.Resumo()["eventos_total"]);
        }

        private static void VerificaTransicoesDeTela()
        {
            var ponte = NovaPonte(true);
            long t = 0;
            var novos = ponte.Observar(Estado(0), false, t);   // abre InventoryPanel
            Checa("transicao inativa->ativa vira janela_aberta",
                  novos.Count == 1 && (string)novos[0]["tipo"] == PipelinePassivo.JanelaAberta,
                  "novos=" + novos.Count);
            novos = ponte.Observar(Estado(-1), false, t + 10);  // fecha
            Checa("transicao ativa->inativa vira janela_fechada",
                  novos.Count == 1 && (string)novos[0]["tipo"] == PipelinePassivo.JanelaFechada,
                  "novos=" + novos.Count);
            novos = ponte.Observar(Estado(0), false, t + 20);  // reabre (legitimo)
            Checa("abrir->fechar->reabrir sobrevive",
                  novos.Count == 1 && (string)novos[0]["tipo"] == PipelinePassivo.JanelaAberta,
                  "novos=" + novos.Count);
            Checa("total de eventos coerente (3)", ponte.Pipeline.Resumo()["eventos_total"].Equals(3),
                  "eventos_total=" + ponte.Pipeline.Resumo()["eventos_total"]);
        }

        private static void VerificaSemRepeticaoPorFrame()
        {
            var ponte = NovaPonte(true, filaMax: 1000, retencaoMax: 1000);
            long t = 0;
            ponte.Observar(Estado(1), false, t);
            int recebidos = 0;
            for (int i = 0; i < 500; i++) recebidos += ponte.Observar(Estado(1), false, t + i).Count;
            Checa("500 quadros sem transicao nao geram evento novo", recebidos == 0,
                  "recebidos=" + recebidos);
            Checa("pipeline manteve apenas a janela aberta",
                  ponte.Pipeline.Resumo()["eventos_total"].Equals(1),
                  "eventos_total=" + ponte.Pipeline.Resumo()["eventos_total"]);
        }

        private static void VerificaTimeoutComMotivo()
        {
            var ponte = NovaPonte(true, timeoutMs: 100);
            long t = 0;
            ponte.Observar(Estado(1), false, t);                  // SkillsPanel aberto
            var clique = ponte.Observar(Estado(1), true, t + 5);  // clique COM janela atual
            bool temClique = false;
            foreach (var e in clique)
                if ((string)e["tipo"] == PipelinePassivo.CliqueRecebido) temClique = true;
            Checa("clique observado vira clique_recebido", temClique);
            var depois = new List<Dictionary<string, object>>();
            for (long tt = t + 6; tt <= t + 400; tt += 10)
                depois.AddRange(ponte.Observar(Estado(1), false, tt));
            Dictionary<string, object> falha = null;
            foreach (var e in depois)
                if ((string)e["tipo"] == PipelinePassivo.FalhaCliqueSemJanela) falha = e;
            Checa("clique sem reabertura dentro do prazo vira falha_clique_sem_janela",
                  falha != null);
            if (falha != null)
            {
                var dados = (Dictionary<string, object>)falha["dados"];
                Checa("falha carrega motivo/timeout/clique_id/janela",
                      !string.IsNullOrEmpty((string)dados["motivo"])
                      && dados["timeout_ms"].Equals(100)
                      && !string.IsNullOrEmpty((string)dados["clique_id"])
                      && !string.IsNullOrEmpty((string)dados["janela_alvo"]),
                      "dados=" + string.Join(",", dados.Keys));
            }
        }

        private static void VerificaCliqueSemJanelaNunca()
        {
            var ponte = NovaPonte(true, timeoutMs: 100);
            long t = 0;
            var clique = ponte.Observar(Estado(-1), true, t);   // clique SEM tela aberta
            Checa("clique sem tela nao cria pendencia", ponte.Pipeline.PendentesRetidos == 0,
                  "pendentes=" + ponte.Pipeline.PendentesRetidos);
            var depois = new List<Dictionary<string, object>>();
            for (long tt = t + 200; tt <= t + 300; tt += 100)
                depois.AddRange(ponte.Observar(Estado(-1), false, tt));
            Checa("sem pendencia nao ha falha derivada", depois.Count == 0,
                  "eventos=" + depois.Count);
        }

        private static void VerificaLimitesSobMuitosQuadros()
        {
            var ponte = NovaPonte(true, filaMax: 4, retencaoMax: 4, timeoutMs: 50);
            long t = 0;
            for (int i = 0; i < 300; i++)
            {
                ponte.Observar(Estado(i % Telas.Length), true, t);
                ponte.Observar(Estado(-1), false, t + 1);
                t += 10;
            }
            var resumo = ponte.Pipeline.Resumo();
            Checa("fila/retencao limitadas (<= 4 eventos)",
                  Convert.ToInt32(resumo["eventos_total"]) <= 4,
                  "eventos_total=" + resumo["eventos_total"]);
            Checa("degradacoes retidas <= limite_aux (4)",
                  Convert.ToInt32(resumo["degradacoes_retidas"]) <= 4,
                  "degradacoes_retidas=" + resumo["degradacoes_retidas"]);
            Checa("pendencias retidas <= limite_aux (4)",
                  Convert.ToInt32(resumo["pendentes"]) <= 4,
                  "pendentes=" + resumo["pendentes"]);
            Checa("pedidos retidos <= limite_aux (4)", ponte.Pipeline.PedidosRetidos <= 4,
                  "pedidos=" + ponte.Pipeline.PedidosRetidos);
            Checa("descartes agregados registrados (sem lista ilimitada)",
                  Convert.ToInt32(resumo["degradacoes_descartadas"]) > 0
                  || Convert.ToInt32(resumo["pendentes_descartados"]) > 0,
                  "descartadas=" + resumo["degradacoes_descartadas"]
                  + " pendentes_descartados=" + resumo["pendentes_descartados"]);
        }

        private static void VerificaCapturaEmDuasFases()
        {
            var ponte = NovaPonte(true, tetoCapturas: 5, filaMax: 50, retencaoMax: 50);
            long t = 0;
            var abertura = ponte.Observar(Estado(2), false, t);
            string eventoId = (string)abertura[0]["id"];
            var pedido = ponte.Pipeline.RegistrarCaptura(eventoId, "png-inexistente.png", 2, t);
            Checa("pedido de captura existe com estado 'solicitada'",
                  pedido != null && (string)pedido["estado"] == PipelinePassivo.CapturaSolicitada);
            var quadroDoEvento = (Dictionary<string, object>)ponte.Pipeline.Eventos()[0]["quadro"];
            Checa("PEDIDO nao marca captura no evento",
                  quadroDoEvento["captura_apos_atualizacao_visual"].Equals(false)
                  && quadroDoEvento["captura_solicitada"].Equals(true));
            string capturaId = (string)pedido["captura_id"];
            var recusa = ponte.Pipeline.ConfirmarCaptura(capturaId, null, 99, null, t);
            Checa("confirmacao sem PNG real e recusada", recusa == null);
            string arquivo = Path.Combine(Path.GetTempPath(), "kit05f-harness.passivo.bin");
            File.WriteAllBytes(arquivo, Encoding.ASCII.GetBytes("quadro-posterior"));
            var naoPosterior = ponte.Pipeline.ConfirmarCaptura(capturaId, arquivo, 1, null, t);
            Checa("confirmacao com quadro NAO posterior e recusada", naoPosterior == null);
            var confirmada = ponte.Pipeline.ConfirmarCaptura(capturaId, arquivo, 99, null, t + 1);
            Checa("confirmacao com PNG real + quadro posterior confirma",
                  confirmada != null && (string)confirmada["estado"] == PipelinePassivo.CapturaConfirmada,
                  "confirmada=" + (confirmada == null ? "null" : "ok"));
            if (confirmada != null)
            {
                Checa("captura confirmada carrega sha256/tamanho e nega simultaneidade",
                      !string.IsNullOrEmpty((string)confirmada["sha256"])
                      && Convert.ToInt64(confirmada["tamanho_bytes"]) > 0
                      && confirmada["simultaneidade_afirmada"].Equals(false));
            }
            File.Delete(arquivo);
            Checa("resumo nao promove runtime",
                  "NAO_EXERCITADO".Equals((string)ponte.Pipeline.Resumo()["runtime"]));
        }

        private static void VerificaPausaSegura()
        {
            var ponte = NovaPonte(true, timeoutMs: 100);
            long t = 0;
            ponte.Observar(Estado(3), false, t);
            ponte.Observar(Estado(3), true, t + 1);   // clique observado => pendencia
            ponte.Pipeline.Pausar(t + 2);
            int pendenciasAntes = ponte.Pipeline.PendentesRetidos;
            Checa("pausa invalida pendencias do intervalo nao observado",
                  pendenciasAntes == 0, "pendentes=" + pendenciasAntes);
            var durante = ponte.Observar(Estado(3), true, t + 150);
            Checa("em pausa, nada e observado", durante.Count == 0, "eventos=" + durante.Count);
            var pedido = ponte.Pipeline.RegistrarCaptura(
                (string)ponte.Pipeline.Eventos()[0]["id"], null, null, t + 150);
            Checa("em pausa, pedido de captura e barrado", pedido == null);
            ponte.Pipeline.Retomar(t + 200);
            var depois = ponte.Observar(Estado(3), false, t + 250);
            bool temFalha = false;
            foreach (var e in depois)
                if ((string)e["tipo"] == PipelinePassivo.FalhaCliqueSemJanela) temFalha = true;
            Checa("retomar NAO gera falsa falha da janela nao observada", !temFalha);
        }
    }
}
