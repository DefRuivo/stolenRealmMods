// INT-R1-C5 — PROBE do hook `ui.localized` (instrumento de bancada, opt-in, SOMENTE LEITURA).
//
// PARA QUE EXISTE
// ---------------
// O instrumento `tools/cobertura_ui_localized.py` mede a COBERTURA das tabelas do
// BetterTooltips contra o texto que o JOGO SERVIU. Quem produz essa evidencia e este
// probe: ele assina o hook `ui.localized` da API propria
// (`api/Core/Contracts.cs:63` -> `OptionsManager.Localize`, estatico, retorno string) e
// grava, uma linha JSON por chamada, o par `(chave = arguments[0], resultado = __result)`.
//
// O QUE ELE NAO FAZ (e por que)
// -----------------------------
//   * NAO reescreve o texto: a API 0.1.0 e OBSERVACIONAL (`api/README.md:42,145-146`).
//     Quem reescreve e o BetterTooltips, que por isso NAO migra para a API.
//   * NAO referencia o Assembly-CSharp: o assembly do jogo e resolvido por NOME em runtime.
//   * NAO instala hook sem autorizacao explicita: `Autorizado=false` (padrao) grava
//     `{"status":"NAO_EXERCITADO"}` e nao toca em nada.
//   * NAO passa pelo gate sem conferir IDENTIDADE: o sha256 do Assembly-CSharp.dll do
//     jogo tem de casar com `ApiIdentity.AssemblySha256` (fail-closed, igual ao plugin
//     da API). Divergiu -> nao instala e diz o motivo no arquivo de saida.
//
// COMO SE USA (rodada AUTORIZADA pelo dono, nunca por build)
// ---------------------------------------------------------
//   1. copie para a MESMA pasta do plugin: LocalizedProbe.dll + RealmApi.dll +
//      RealmApi.Core.dll + RealmApi.Hooks.dll (sem as duas ultimas o BepInEx nao resolve);
//   2. `BepInEx/config/com.gumatos.localizedprobe.cfg`: `Autorizado = true` e
//      `Saida = <caminho do jsonl>` (o driver escreve o cfg; ver o runbook);
//   3. abra o jogo (a leitura acontece em toda localizacao em ingles);
//   4. consuma o JSONL com `python tools/cobertura_ui_localized.py --observacoes <arquivo>`.
// A PROCEDENCIA sai carimbada em cada linha (`"procedencia":"runtime"`): o instrumento
// recusa medicao de fixture como se fosse jogo.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using BepInEx;
using BepInEx.Configuration;
using Gumatos.RealmApi;
using UnityEngine;

namespace Gumatos.LocalizedProbe
{
    [BepInPlugin(Guid, "LocalizedProbe (INT-R1-C5: cobertura ui.localized, instrumento)", Versao)]
    public class LocalizedProbePlugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.localizedprobe";
        public const string Versao = "0.1.0";
        public const string Alvo = "ui.localized";
        public const string MarcadorDeBoot = "LocalizedProbe carregado.";

        private ConfigEntry<bool> _autorizado;
        private ConfigEntry<string> _saida;
        private ConfigEntry<string> _sessao;

        private HookInstallation _instalacao;
        private IDisposable _assinatura;
        private StreamWriter _escritor;
        private string _hashFonte;
        private readonly object _porta = new object();
        private long _sequencia;

        private void Awake()
        {
            _autorizado = Config.Bind("Geral", "Autorizado", false,
                "FALSE (padrao): nao instala hook, nao le e grava NAO_EXERCITADO. TRUE exige rodada autorizada pelo dono.");
            _saida = Config.Bind("Geral", "Saida", DefaultSaida(),
                "Arquivo JSONL de saida (uma linha por texto localizado: chave/resultado).");
            _sessao = Config.Bind("Geral", "Sessao", "",
                "Identidade da RODADA, injetada pelo driver. Sem ela a evidencia nao pertence a nenhuma rodada.");

            Logger.LogInfo(MarcadorDeBoot);

            if (!_autorizado.Value)
            {
                EscreverStatus("NAO_EXERCITADO", "Autorizado=false", null);
                return;
            }

            var assembly = AcharAssemblyDoJogo();
            if (assembly == null)
            {
                EscreverStatus("NAO_EXERCITADO", "Assembly-CSharp nao esta carregado", null);
                return;
            }

            string hash = Sha256De(assembly.Location);
            string versao = Application.version;
            if (!ApiIdentity.Matches(versao, hash))
            {
                EscreverStatus("NAO_EXERCITADO",
                    "identidade divergente: versao=" + (versao ?? "(nula)") + " sha256=" + (hash ?? "(nulo)"), hash);
                return;
            }

            try
            {
                _hashFonte = hash;
                var descritor = HookCatalog.All.First(d => d.Id == Alvo);
                _instalacao = HookInstallation.Install(assembly, new[] { descritor }, Guid,
                    ex => Logger.LogError("LocalizedProbe: falha de assinante (isolada): " + ex.Message));
                AbrirEscritor();
                _assinatura = RealmHooks.Observed.Subscribe(Receber);
                Logger.LogInfo("LocalizedProbe: hook " + Alvo + " instalado; saida em " + _saida.Value);
            }
            catch (Exception e)
            {
                EscreverStatus("NAO_EXERCITADO", "nao consegui instalar o hook " + Alvo + ": " + e.GetType().Name + ": " + e.Message, hash);
                DisposeTudo();
            }
        }

        /// <summary>Consumidor do barramento: so o hook alvo, so leitura. Nunca lanca para fora.</summary>
        private void Receber(HookNotification n)
        {
            if (n == null || n.HookId != Alvo) return;
            try
            {
                string chave = n.Arguments != null && n.Arguments.Count > 0 ? n.Arguments[0] as string : null;
                string resultado = n.Result as string;
                if (chave == null || resultado == null) return;
                lock (_porta)
                {
                    if (_escritor == null) return;
                    _escritor.WriteLine(Linha(_sequencia++, chave, resultado));
                    _escritor.Flush();
                }
            }
            catch (Exception e)
            {
                // o probe nao pode quebrar o jogo por causa do proprio log
                try { Logger.LogError("LocalizedProbe: falha ao gravar (ignorada): " + e.Message); } catch { }
            }
        }

        private string Linha(long sequencia, string chave, string resultado)
        {
            var sb = new StringBuilder(256);
            sb.Append('{');
            sb.Append("\"esquema\":\"ui-localized/1\",");
            sb.Append("\"hook\":\"").Append(Alvo).Append("\",");
            sb.Append("\"sequencia\":").Append(sequencia.ToString(CultureInfo.InvariantCulture)).Append(',');
            sb.Append("\"procedencia\":\"runtime\",");
            sb.Append("\"sessao\":").Append(Texto(_sessao.Value)).Append(',');
            sb.Append("\"hash_fonte\":").Append(Texto(_hashFonte)).Append(',');
            sb.Append("\"chave\":").Append(Texto(chave)).Append(',');
            sb.Append("\"resultado\":").Append(Texto(resultado));
            sb.Append('}');
            return sb.ToString();
        }

        private void AbrirEscritor()
        {
            var pasta = Path.GetDirectoryName(_saida.Value);
            if (!string.IsNullOrEmpty(pasta)) Directory.CreateDirectory(pasta);
            _escritor = new StreamWriter(new FileStream(_saida.Value, FileMode.Create, FileAccess.Write, FileShare.Read),
                new UTF8Encoding(false));
        }

        private void EscreverStatus(string status, string motivo, string hash)
        {
            try
            {
                var pasta = Path.GetDirectoryName(_saida.Value);
                if (!string.IsNullOrEmpty(pasta)) Directory.CreateDirectory(pasta);
                using (var w = new StreamWriter(new FileStream(_saida.Value, FileMode.Create, FileAccess.Write, FileShare.Read),
                           new UTF8Encoding(false)))
                {
                    w.WriteLine("{\"hook\":\"" + Alvo + "\",\"status\":" + Texto(status) +
                                ",\"motivo\":" + Texto(motivo) +
                                ",\"sessao\":" + Texto(_sessao.Value) +
                                ",\"hash_fonte\":" + Texto(hash) + "}");
                }
                Logger.LogWarning("LocalizedProbe: " + status + " - " + motivo);
            }
            catch (Exception e)
            {
                try { Logger.LogError("LocalizedProbe: nao consegui gravar o status: " + e.Message); } catch { }
            }
        }

        private static Assembly AcharAssemblyDoJogo()
        {
            return AppDomain.CurrentDomain.GetAssemblies()
                .FirstOrDefault(a => a != null && a.GetName().Name == "Assembly-CSharp");
        }

        private static string Sha256De(string caminho)
        {
            if (string.IsNullOrEmpty(caminho) || !File.Exists(caminho)) return null;
            using (var sha = SHA256.Create())
            using (var fs = File.OpenRead(caminho))
            {
                var hash = sha.ComputeHash(fs);
                var sb = new StringBuilder(hash.Length * 2);
                foreach (var b in hash) sb.Append(b.ToString("x2", CultureInfo.InvariantCulture));
                return sb.ToString();
            }
        }

        private static string Texto(string s)
        {
            if (s == null) return "null";
            var sb = new StringBuilder(s.Length + 2);
            sb.Append('"');
            foreach (var c in s)
            {
                switch (c)
                {
                    case '"': sb.Append("\\\""); break;
                    case '\\': sb.Append("\\\\"); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default:
                        if (c < ' ') sb.Append("\\u").Append(((int)c).ToString("x4", CultureInfo.InvariantCulture));
                        else sb.Append(c);
                        break;
                }
            }
            sb.Append('"');
            return sb.ToString();
        }

        private static string DefaultSaida()
        {
            try
            {
                string jogo = Paths.GameRootPath;
                if (!string.IsNullOrEmpty(jogo))
                    return Path.Combine(jogo, "int-r1-c5-observacao-ui-localized.jsonl");
            }
            catch { /* sem contexto do jogo: cai no diretorio atual */ }
            return Path.Combine(Directory.GetCurrentDirectory(), "int-r1-c5-observacao-ui-localized.jsonl");
        }

        private void DisposeTudo()
        {
            lock (_porta)
            {
                if (_escritor != null)
                {
                    try { _escritor.Flush(); _escritor.Dispose(); } catch { }
                    _escritor = null;
                }
            }
            if (_assinatura != null) { try { _assinatura.Dispose(); } catch { } _assinatura = null; }
            if (_instalacao != null) { try { _instalacao.Dispose(); } catch { } _instalacao = null; }
        }

        private void OnDestroy() => DisposeTudo();
    }
}
