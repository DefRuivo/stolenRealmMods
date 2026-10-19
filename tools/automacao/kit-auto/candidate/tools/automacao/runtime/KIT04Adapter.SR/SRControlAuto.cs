// KIT-AUTO: transporte local opt-in de ACOES do kit. Nunca injeta input do SO.
using System;
using System.Collections.Generic;
using System.IO;
using BepInEx.Configuration;
using KIT04Core;
using UnityEngine;

namespace KIT04Adapter.SR
{
    internal sealed partial class SRControlRuntime
    {
        private ConfigEntry<bool> _autoHabilitado = null!;
        private long _autoSequencia;
        private readonly List<Dictionary<string, object>> _autoLeituras = new();
        private void AutoTick()
        {
            if (!_autoHabilitado.Value) return;
            string path = Path.Combine(_saida, "auto-command.txt");
            if (!File.Exists(path)) return;
            if (new FileInfo(path).Length > 8192) return;
            string[] p = File.ReadAllText(path).TrimEnd('\r', '\n').Split('|');
            string sessao = CorePlugin.Instancia.Passivo.IdSessao;
            if (p.Length != 4 || p[0] != sessao || !long.TryParse(p[1], out long seq)
                || seq <= _autoSequencia) return;
            _autoSequencia = seq; // recusas tambem sao consumidas, sem replay por frame
            string acao = p[2];
            bool permitida = acao == PonteControleRSTV.Observar || acao == PonteControleRSTV.Pausar
                || acao == PonteControleRSTV.Retomar || acao == PonteControleRSTV.MarcarProblema
                || acao == PonteControleRSTV.Exportar;
            var ev = permitida ? _ponte.ProcessarAcao(acao, AgoraMs(), p[3]) : null;
            if (ev != null && acao == PonteControleRSTV.Exportar)
                _ultimaExportacao = (string)ev["caminho"];
            _autoLeituras.Add(Json.Campos("origem", "KIT-AUTO/acao-interna/1", "seq", seq,
                "acao", acao, "permitida", permitida, "engine", Engine(),
                "contexto", _ponte.ContextoAtual(), "evento", ev,
                "degradacoes", _ponte.Degradacoes()));
            while (_autoLeituras.Count > 100) _autoLeituras.RemoveAt(0);
            _plugin.RelatarRuntime("[KIT-AUTO] seq=" + seq + " acao=" + acao
                + " resultado=" + (ev == null ? "RECUSADA" : "EXECUTADA"));
            Persistir();
        }
    }
}
