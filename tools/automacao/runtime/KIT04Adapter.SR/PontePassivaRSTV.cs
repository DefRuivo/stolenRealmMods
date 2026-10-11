// KIT-05F - PontePassivaRSTV: ponte PASSIVA entre a observacao real do jogo
// (Adapter SR) e o pipeline limitado do Core (KIT04Core.PipelinePassivo).
//
// Reutiliza Core/Adapter/AUT-4/CAP-1: o Adapter ja sabe detectar telas ativas
// (SRScreenManager) e o Core ja sabe capturar PNG (IPictureCapture/CAP-1). Esta
// ponte apenas TRADUZ observacao real em eventos RSTV, com pipeline limitado.
//
// O que ela observa (nada mais):
//   * transicao de estado das telas conhecidas (inativa -> ativa e volta):
//     `janela_aberta` / `janela_fechada`;
//   * o clique RECEBIDO pelo frame (observado no input do engine): apenas
//     `clique_recebido` — a ponte NUNCA emite clique, save, equipamento ou
//     qualquer acao, e nao modifica gameplay.
//
// OPT-IN: `habilitado=false` (padrao) => Observar devolve lista vazia e o
// pipeline nao registra NADA. Sem flag explicita, a trilha passiva e inerte.
//
// ESTE ARQUIVO NAO DEPENDE DE UNITY/BepInEx de proposito: e compilado tambem
// pelo harness offline (tools/automacao/runtime/harness-passivo), que prova a
// ligacao/estado SEM abrir o jogo.
using System.Collections.Generic;

namespace KIT04Adapter.SR
{
    public class PontePassivaRSTV
    {
        private readonly bool _habilitado;
        private readonly string[] _telasConhecidas;
        private readonly bool[] _ativasAnterior;
        private readonly KIT04Core.PipelinePassivo _pipeline;

        public PontePassivaRSTV(string[] telasConhecidas, bool habilitado,
                                int filaMax = 200, int retencaoMax = 200,
                                int tetoCapturas = 10, int timeoutJanelaMs = 1500,
                                string idSessao = null)
            : this(telasConhecidas, habilitado,
                   new KIT04Core.PipelinePassivo(filaMax, retencaoMax, tetoCapturas,
                                                 timeoutJanelaMs, 0, idSessao))
        {
        }

        /// <summary>
        /// KIT-05F (F8): reutiliza um pipeline JA existente do Core
        /// (`CorePlugin.Passivo`) em vez de criar um proprio — a trilha passiva
        /// do instrumento e UMA so.
        /// </summary>
        public PontePassivaRSTV(string[] telasConhecidas, bool habilitado,
                                KIT04Core.PipelinePassivo pipeline)
        {
            _telasConhecidas = telasConhecidas ?? new string[0];
            _habilitado = habilitado;
            _ativasAnterior = new bool[_telasConhecidas.Length];
            _pipeline = pipeline ?? new KIT04Core.PipelinePassivo();
            TelaAtual = null;
            Transicoes = 0;
        }

        public bool Habilitado { get { return _habilitado; } }
        public KIT04Core.PipelinePassivo Pipeline { get { return _pipeline; } }
        public string TelaAtual { get; private set; }
        public int Transicoes { get; private set; }

        /// <summary>Traduz a observacao REAL do frame em eventos RSTV (ou nada).</summary>
        public List<Dictionary<string, object>> Observar(bool[] telasAtivas,
                                                         bool cliqueRecebido,
                                                         long agoraMs)
        {
            var novos = new List<Dictionary<string, object>>();
            if (!_habilitado)
                return novos;   // opt-in false: nenhum evento, nenhum efeito

            bool[] ativas = telasAtivas ?? new bool[_telasConhecidas.Length];
            for (int i = 0; i < _telasConhecidas.Length && i < ativas.Length; i++)
            {
                string nome = _telasConhecidas[i];
                bool agora = ativas[i];
                bool antes = _ativasAnterior[i];
                if (agora == antes) continue;          // sem transicao: nada a observar
                Transicoes++;
                _ativasAnterior[i] = agora;
                Dictionary<string, object> dados =
                    new Dictionary<string, object> { { "nome", nome } };
                var ev = agora
                    ? _pipeline.Registrar(KIT04Core.PipelinePassivo.JanelaAberta, dados, nome, agoraMs)
                    : _pipeline.Registrar(KIT04Core.PipelinePassivo.JanelaFechada, dados, nome, agoraMs);
                if (ev != null) novos.Add(ev);
                TelaAtual = agora ? nome : (TelaAtual == nome ? null : TelaAtual);
            }

            if (cliqueRecebido)
            {
                // Clique OBSERVADO no input: nao e emulado, nao e reemitido.
                var dados = new Dictionary<string, object>
                {
                    { "origem", "input_observado" },
                    { "tela_no_clique", TelaAtual },
                };
                var ev = _pipeline.Registrar(KIT04Core.PipelinePassivo.CliqueRecebido,
                                             dados, TelaAtual, agoraMs);
                if (ev != null) novos.Add(ev);
            }

            novos.AddRange(_pipeline.VerificarTimeouts(agoraMs));
            return novos;
        }
    }
}
