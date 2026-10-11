using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using BepInEx;
using UnityEngine;

namespace RoguelikeDebugger
{
    /// <summary>
    /// DBG-R2 (cartao t_3b7c681b) - PROVENIENCIA do dump do RoguelikeDebugger.
    ///
    /// PROBLEMA QUE ISTO RESOLVE
    /// -------------------------
    /// O `LogOutput.log` do BepInEx e' truncado a cada arranque e NAO tem rodape: um dump
    /// incompleto e um dump completo leem IGUAL. Sem saber QUAL build foi observado e SE o dump
    /// fechou, a AUSENCIA de um dado no censo (`tools/census.py` -> `docs/cobertura/*.csv`) nao
    /// pode ser lida como ausencia do fato. Este arquivo carimba essa informacao no PROPRIO fluxo
    /// de log - nao existe sidecar de runtime (o debugger nao escreve arquivo nenhum; prova na
    /// parte01 do cartao).
    ///
    /// O QUE SAI NO LOG (formato `DBG-PROV-V1`, tres linhas)
    /// ----------------------------------------------------
    ///   [Proveniencia] DBG-PROV-V1 inicio | versaoJogo=... | buildSteam=... | sha256Alvo=... |
    ///       dllDebugger=... | sha256Dll=... | identidade=api|local | apiPresente=... |
    ///       apiEnableHooks=... | apiVersao=... | apiSha256=... | alvoConforme=... |
    ///       inicioEm=<ISO-8601 UTC> | estadoDump=INICIADO
    ///   [Proveniencia] DBG-PROV-V1 estado | estadoDump=ABERTO|PARCIAL | ganchosOk=n/n |
    ///       ganchosFalhos=... | metodos=n | matrizFlame=aplicada|ausente | modoLeitura=passivo|ativo
    ///   [Proveniencia] DBG-PROV-V1 fim | estadoDump=FECHADO | motivo=...
    ///
    /// ORDEM: o cabecalho sai ANTES de aplicar os ganchos. Se o arranque morrer no meio, a
    /// identidade ja' esta no log - que e' exatamente o caso em que a falta de dado seria lida como
    /// fato.
    ///
    /// DEPENDENCIA OPCIONAL DA API
    /// ---------------------------
    /// Quando o `RealmApi` (`Gumatos.RealmApi.ApiIdentity`) esta' carregado E com `EnableHooks=true`
    /// no `.cfg` dele, o debugger LE a identidade declarada por ele (jogo/build/versao/hash) em vez
    /// de recalcular, e usa o gate fail-closed `ApiIdentity.Matches`. Sem a API - ausente, desligada
    /// ou com tipo que nao resolve - o debugger segue SOZINHO com o que mede localmente e declara
    /// isso no log. A leitura e' por REFLEXAO: o `.csproj` nao referencia o projeto da API, entao
    /// nada aqui vira dependencia obrigatoria.
    ///
    /// REGRA DO PROJETO: nada estimado. Leitura que falha vira o literal `desconhecido`, nunca um
    /// valor plausivel. Nenhum campo obrigatorio pode sair vazio.
    /// </summary>
    internal static class Proveniencia
    {
        internal const string Marca = "DBG-PROV-V1";
        internal const string Aparelho = "[Proveniencia]";
        internal const string Desconhecido = "desconhecido";

        /// <summary>Nome da assembly do jogo observada - o alvo do dump.</summary>
        private const string Alvo = "Assembly-CSharp";

        /// <summary>Id do aplicativo na Steam (Stolen Realm), para achar o appmanifest do build.</summary>
        private const int AppIdSteam = 1330000;

        // ------------------------------------------------------------- cabecalho ---

        /// <summary>Carimba a identidade do que vai ser observado. Chamado ANTES dos ganchos.</summary>
        internal static void Cabecalho()
        {
            var campos = new List<string>();
            try
            {
                string versao = VersaoDoJogo();
                string sha = Sha256DoAlvo();
                var api = SondaApi(versao, sha);

                campos.Add("versaoJogo=" + Texto(versao));
                campos.Add("buildSteam=" + Texto(api.Identidade == "api" ? api.BuildSteam : BuildSteam()));
                campos.Add("sha256Alvo=" + Texto(sha));
                campos.Add("dllDebugger=" + NomeDll() + "@" + VersaoDll());
                campos.Add("sha256Dll=" + Texto(Sha256DaPropriaDll()));
                campos.Add("identidade=" + api.Identidade);
                campos.Add("apiPresente=" + SimNao(api.Presente));
                campos.Add("apiEnableHooks=" + api.EnableHooks);
                campos.Add("apiVersao=" + api.Versao);
                campos.Add("apiSha256=" + api.Sha256);
                campos.Add("alvoConforme=" + api.Conforme);
                campos.Add("inicioEm=" + DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ", CultureInfo.InvariantCulture));
                campos.Add("estadoDump=INICIADO");
            }
            catch (Exception e)
            {
                // Fail-safe: a identidade que nao deu para medir sai como `!erro:<Tipo>` no proprio
                // campo - nunca vazio (campo vazio seria "sem problema", que e' o oposto).
                campos.Add("erroDeteccao=!erro:" + e.GetType().Name);
                campos.Add("estadoDump=INICIADO");
            }

            Emitir("inicio", campos);
        }

        // --------------------------------------------------------------- estado ---

        /// <summary>
        /// Carimba o que foi REALMENTE aplicado. `PARCIAL` = algum gancho falhou: o dump daquele
        /// recurso nao sai nesta sessao, logo a falta tem de ser lida como falha do instrumento.
        /// </summary>
        internal static void Estado(int ganchosOk, int ganchosTotal, int metodos, IList<string> falhas, bool matrizFlame)
        {
            var campos = new List<string>();
            try
            {
                bool parcial = falhas != null && falhas.Count > 0;
                campos.Add("estadoDump=" + (parcial ? "PARCIAL" : "ABERTO"));
                campos.Add("ganchosOk=" + ganchosOk + "/" + ganchosTotal);
                campos.Add("ganchosFalhos=" + (parcial ? string.Join(",", falhas.ToArray()) : "nenhum"));
                campos.Add("metodos=" + metodos);
                campos.Add("matrizFlame=" + (matrizFlame ? "aplicada" : "ausente"));
                // A matriz Flame chama EvalVoid e escreve em MissingExpressions
                // (Patches/FlameShrineProcPatch.cs:278-284,350): com ela aplicada, esta sessao NAO e'
                // observacao passiva estrita e nao serve para concluir ausencia de dado.
                campos.Add("modoLeitura=" + (matrizFlame ? "ativo" : "passivo"));
            }
            catch (Exception e)
            {
                campos.Add("erroDeteccao=!erro:" + e.GetType().Name);
                campos.Add("estadoDump=PARCIAL");
            }

            Emitir("estado", campos);
        }

        // ------------------------------------------------------------------ fim ---

        /// <summary>Rodape: o unico sinal de que o dump FECHOU (o BepInEx nao escreve rodape).</summary>
        internal static void Fim(string motivo)
        {
            Emitir("fim", new List<string>
            {
                "estadoDump=FECHADO",
                "motivo=" + Texto(motivo)
            });
        }

        // -------------------------------------------------------------- emissao ---

        private static void Emitir(string fase, IList<string> campos)
        {
            try
            {
                var linha = new StringBuilder();
                linha.Append(Aparelho).Append(' ').Append(Marca).Append(' ').Append(fase);
                for (int i = 0; i < campos.Count; i++)
                {
                    linha.Append(" | ").Append(campos[i]);
                }

                var log = Plugin.Log;
                if (log != null)
                {
                    log.LogInfo(linha.ToString());
                }
            }
            catch (Exception)
            {
                // Logar a proveniencia nunca pode derrubar o mod: se o log falhar, o gancho
                // observado continua valendo mais do que a moldura. Sem retry e sem rethrow.
            }
        }

        // ------------------------------------------------------------- medicoes ---

        /// <summary>`Application.version` do jogo que esta' rodando (o valor que o alvo declara).</summary>
        private static string VersaoDoJogo()
        {
            try
            {
                string v = Application.version;
                return string.IsNullOrWhiteSpace(v) ? Desconhecido : v.Trim();
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        /// <summary>SHA-256 do ARQUIVO da assembly do jogo que esta' carregada (observada de fato).</summary>
        private static string Sha256DoAlvo()
        {
            try
            {
                Assembly alvo = null;
                Assembly[] assemblies = AppDomain.CurrentDomain.GetAssemblies();
                for (int i = 0; i < assemblies.Length; i++)
                {
                    string nome = assemblies[i].GetName().Name;
                    if (string.Equals(nome, Alvo, StringComparison.Ordinal))
                    {
                        alvo = assemblies[i];
                        break;
                    }
                }

                if (alvo == null || string.IsNullOrEmpty(alvo.Location))
                {
                    return Desconhecido;
                }

                return Sha256DeArquivo(alvo.Location);
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        /// <summary>SHA-256 do proprio arquivo do debugger (quem observou).</summary>
        private static string Sha256DaPropriaDll()
        {
            try
            {
                string caminho = typeof(Plugin).Assembly.Location;
                return string.IsNullOrEmpty(caminho) ? Desconhecido : Sha256DeArquivo(caminho);
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        private static string Sha256DeArquivo(string caminho)
        {
            using (var sha = SHA256.Create())
            using (var arquivo = File.OpenRead(caminho))
            {
                byte[] hash = sha.ComputeHash(arquivo);
                var sb = new StringBuilder(hash.Length * 2);
                for (int i = 0; i < hash.Length; i++)
                {
                    sb.Append(hash[i].ToString("x2", CultureInfo.InvariantCulture));
                }

                return sb.ToString();
            }
        }

        /// <summary>
        /// Build da Steam lido do `appmanifest_<appid>.acf` (dois niveis acima da raiz do jogo -
        /// layout padrao `<steamapps>/common/<jogo>`). Sem arquivo legivel: `desconhecido`.
        /// </summary>
        private static string BuildSteam()
        {
            try
            {
                string raiz = RaizDoJogo();
                if (string.IsNullOrEmpty(raiz))
                {
                    return Desconhecido;
                }

                string steamapps = Path.GetFullPath(Path.Combine(raiz, "..", ".."));
                string acf = Path.Combine(steamapps, "appmanifest_" + AppIdSteam + ".acf");
                if (!File.Exists(acf))
                {
                    return Desconhecido;
                }

                foreach (string linha in File.ReadAllLines(acf))
                {
                    string limpa = linha.Trim();
                    if (!limpa.StartsWith("\"buildid\"", StringComparison.Ordinal))
                    {
                        continue;
                    }

                    int primeiro = limpa.IndexOf('"', 1);
                    if (primeiro < 0)
                    {
                        continue;
                    }

                    int segundo = limpa.IndexOf('"', primeiro + 1);
                    if (segundo < 0)
                    {
                        continue;
                    }

                    string valor = limpa.Substring(primeiro + 1, segundo - primeiro - 1).Trim();
                    return string.IsNullOrEmpty(valor) ? Desconhecido : valor;
                }

                return Desconhecido;
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        private static string RaizDoJogo()
        {
            try
            {
                string raiz = Paths.GameRootPath;
                if (!string.IsNullOrEmpty(raiz) && Directory.Exists(raiz))
                {
                    return raiz;
                }
            }
            catch (Exception)
            {
                // cai no plano B abaixo
            }

            try
            {
                string dados = Application.dataPath;
                if (!string.IsNullOrEmpty(dados))
                {
                    string pai = Path.GetDirectoryName(dados);
                    if (!string.IsNullOrEmpty(pai) && Directory.Exists(pai))
                    {
                        return pai;
                    }
                }
            }
            catch (Exception)
            {
                // sem raiz: o campo de build sai `desconhecido`
            }

            return null;
        }

        private static string NomeDll()
        {
            try
            {
                return Texto(typeof(Plugin).Assembly.GetName().Name);
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        private static string VersaoDll()
        {
            try
            {
                Assembly eu = typeof(Plugin).Assembly;
                AssemblyInformationalVersionAttribute info =
                    (AssemblyInformationalVersionAttribute)Attribute.GetCustomAttribute(eu, typeof(AssemblyInformationalVersionAttribute));
                if (info != null && !string.IsNullOrWhiteSpace(info.InformationalVersion))
                {
                    return info.InformationalVersion.Trim();
                }

                Version v = eu.GetName().Version;
                return v == null ? Desconhecido : v.ToString();
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        // ------------------------------------------------------------- sonda API ---

        private sealed class Sonda
        {
            internal string Identidade = "local";
            internal bool Presente;
            internal string EnableHooks = Desconhecido;
            internal string Versao = "-";
            internal string Sha256 = "-";
            internal string BuildSteam = Desconhecido;
            internal string Conforme = "indeterminado";
        }

        /// <summary>
        /// Le a identidade da API por REFLEXAO (sem referencia de projeto). Ausente/desligada: o
        /// debugger continua sozinho e declara `identidade=local`. Nada aqui lanca.
        /// </summary>
        private static Sonda SondaApi(string versaoMedida, string shaMedido)
        {
            var sonda = new Sonda();
            try
            {
                Type tipo = null;
                Assembly[] assemblies = AppDomain.CurrentDomain.GetAssemblies();
                for (int i = 0; i < assemblies.Length && tipo == null; i++)
                {
                    try
                    {
                        tipo = assemblies[i].GetType("Gumatos.RealmApi.ApiIdentity", false, false);
                    }
                    catch (Exception)
                    {
                        // assembly que nao deixa listar tipo: nao e' a API
                    }
                }

                if (tipo == null)
                {
                    return sonda;
                }

                sonda.Presente = true;
                sonda.Versao = Texto(Constante(tipo, "Version"));
                sonda.Sha256 = Texto(Constante(tipo, "AssemblySha256"));
                sonda.BuildSteam = Texto(Constante(tipo, "SteamBuildId"));
                sonda.EnableHooks = EnableHooksDaApi();
                sonda.Conforme = MatchesDaApi(tipo, versaoMedida, shaMedido);

                // "presente E ligada" e' a unica condicao em que a identidade da API e' usada no
                // lugar do calculo local (escopo 2 do cartao). Estar presente e desligada NAO muda
                // o que o debugger carimba - so' fica registrado no log.
                if (string.Equals(sonda.EnableHooks, "sim", StringComparison.Ordinal))
                {
                    sonda.Identidade = "api";
                }

                return sonda;
            }
            catch (Exception e)
            {
                sonda.Conforme = "indeterminado";
                sonda.Versao = sonda.Versao == "-" ? "!erro:" + e.GetType().Name : sonda.Versao;
                return sonda;
            }
        }

        /// <summary>Constante estatica do tipo da API (os campos dela sao `const`).</summary>
        private static string Constante(Type tipo, string nome)
        {
            try
            {
                FieldInfo campo = tipo.GetField(nome, BindingFlags.Public | BindingFlags.Static | BindingFlags.FlattenHierarchy);
                if (campo == null)
                {
                    return Desconhecido;
                }

                object valor;
                try
                {
                    valor = campo.GetRawConstantValue();
                }
                catch (Exception)
                {
                    valor = campo.GetValue(null);
                }

                return valor == null ? Desconhecido : Convert.ToString(valor, CultureInfo.InvariantCulture);
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        /// <summary>Gate fail-closed da API: `ApiIdentity.Matches(versao, sha256)`.</summary>
        private static string MatchesDaApi(Type tipo, string versao, string sha)
        {
            try
            {
                MethodInfo metodo = tipo.GetMethod("Matches", BindingFlags.Public | BindingFlags.Static,
                    null, new[] { typeof(string), typeof(string) }, null);
                if (metodo == null)
                {
                    return "indeterminado";
                }

                object resultado = metodo.Invoke(null, new object[] { versao, sha });
                if (resultado is bool)
                {
                    return (bool)resultado ? "sim" : "nao";
                }

                return "indeterminado";
            }
            catch (Exception)
            {
                return "indeterminado";
            }
        }

        /// <summary>`EnableHooks` do `.cfg` da API (BepInEx/config/com.gumatos.realmapi.cfg).</summary>
        private static string EnableHooksDaApi()
        {
            try
            {
                string cfg = Path.Combine(Paths.ConfigPath, "com.gumatos.realmapi.cfg");
                if (!File.Exists(cfg))
                {
                    return Desconhecido;
                }

                foreach (string linha in File.ReadAllLines(cfg))
                {
                    string limpa = linha.Trim();
                    if (limpa.StartsWith("#", StringComparison.Ordinal))
                    {
                        continue;
                    }

                    int igual = limpa.IndexOf('=');
                    if (igual <= 0)
                    {
                        continue;
                    }

                    string chave = limpa.Substring(0, igual).Trim();
                    if (!string.Equals(chave, "EnableHooks", StringComparison.OrdinalIgnoreCase))
                    {
                        continue;
                    }

                    string valor = limpa.Substring(igual + 1).Trim();
                    if (valor.Equals("true", StringComparison.OrdinalIgnoreCase))
                    {
                        return "sim";
                    }

                    if (valor.Equals("false", StringComparison.OrdinalIgnoreCase))
                    {
                        return "nao";
                    }

                    return Desconhecido;
                }

                return Desconhecido;
            }
            catch (Exception)
            {
                return Desconhecido;
            }
        }

        // ---------------------------------------------------------------- textos ---

        private static string Texto(string valor)
        {
            return string.IsNullOrWhiteSpace(valor) ? Desconhecido : valor.Trim();
        }

        private static string SimNao(bool valor)
        {
            return valor ? "sim" : "nao";
        }
    }
}
