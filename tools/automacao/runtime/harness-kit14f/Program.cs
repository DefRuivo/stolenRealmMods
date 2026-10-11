// KIT-14F — harness OFFLINE dos 3 defeitos achados pelo run704 do KIT-14.
//
// O QUE ELE FAZ (sem abrir o jogo, sem instalar nada, sem tocar no perfil do dono):
//   parte1  ciclo de vida Adapter/Core: monta os PLUGINS REAIS por reflexao, roda
//           `SRAdapterPlugin.Awake` na ORDEM OBSERVADA (Adapter antes do Core) e exige
//           que nao haja excecao, que o vinculo fique PENDENTE declarado, que o
//           `[BepInDependency]` do Core exista e que o vinculo conclua quando o Core sobe.
//   parte2  trilha passiva (recorder): usa a ponte REAL criada pelo Adapter, alimenta
//           transicoes/clique pelo MESMO metodo que o Update chama e exige CONTAGEM > 0
//           e ARQUIVO de resultado lido de volta do disco.
//   parte3  navegacao por handler: dirige a rotina do probe REAL por varios quadros, com
//           porta injetavel, e exige espera com tentativas, motivo declarado quando esgota
//           e exatamente uma invocacao quando o alvo aparece.
//
// COMO O PLUGIN REAL E MONTADO SEM ENGINE: `BaseUnityPlugin` expoe os backing fields
// `<Config>k__BackingField` / `<Logger>k__BackingField`; `FormatterServices
// .GetUninitializedObject` cria a instancia sem construtor e sem cena. Nada aqui chama
// engine do Unity no caminho exercitado pelos consertos (o caminho pre-conserto da parte3
// PODE chamar: por isso cada parte roda em processo proprio).
//
// EXIT: 0 = todas as verificacoes passaram; 1 = alguma falhou (REPROVOU); 2 = uso/infra.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;

namespace HarnessKit14f
{
    internal static class Program
    {
        private const string Repo = @"C:\dev\stolen-realm";
        private static readonly string Lib = Path.Combine(Repo, "lib");
        private static readonly string Managed =
            @"E:\SteamLibrary\steamapps\common\Stolen Realm\Stolen Realm_Data\Managed";
        private static readonly string CoreBin = Path.Combine(Repo, @"tools\automacao\runtime\core\bin\Release");
        private static readonly string AdapterBin = Path.Combine(Repo, @"tools\automacao\runtime\KIT04Adapter.SR\bin\Release");
        // KIT-14F: pasta ALTERNATIVA do Adapter, para rodar o MESMO harness contra a build
        // PRE-conserto (baseline) e provar o vermelho. Ver --adapter-bin=<dir>.
        private static string _adapterBin = AdapterBin;
        private static readonly string ProbeBin = Path.Combine(Repo, @"tools\automacao\runtime\AUT4Probe\bin\Release");
        // KIT-14F: pasta ALTERNATIVA do probe, para rodar a MESMA parte3 contra a build
        // PRE-conserto (baseline) e provar o vermelho. Ver --probe-bin=<dir>.
        private static string _probeBin = ProbeBin;
        // Somente LEITURA: o BepInEx de verdade traz MonoMod.RuntimeDetour/Utils, que o
        // 0Harmony de lib/ exige para o `new Harmony(id)` do Core subir. Nada e escrito aqui.
        private static readonly string BepInExCore = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            @"r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\core");

        /// <summary>Reexecuta o harness num PROCESSO PROPRIO com a mesma parte/overrides.</summary>
        private static int Reexecutar(string parte)
        {
            var exe = Environment.ProcessPath;
            if (string.IsNullOrEmpty(exe)) exe = Assembly.GetEntryAssembly()?.Location;
            var psi = new System.Diagnostics.ProcessStartInfo(exe) { UseShellExecute = false };
            psi.ArgumentList.Add(parte);
            if (_adapterBin != AdapterBin) psi.ArgumentList.Add("--adapter-bin=" + _adapterBin);
            if (_probeBin != ProbeBin) psi.ArgumentList.Add("--probe-bin=" + _probeBin);
            var proc = System.Diagnostics.Process.Start(psi);
            proc.WaitForExit();
            return proc.ExitCode;
        }

        private static int _oks, _falhas, _naoExercitado, _montagens;
        private static string _dirTrabalho;

        private static int Main(string[] argv)
        {
            AppDomain.CurrentDomain.AssemblyResolve += Resolver;
            var partes = new List<string>();
            foreach (var a in argv)
            {
                if (a.StartsWith("--adapter-bin=", StringComparison.Ordinal))
                    _adapterBin = a.Substring("--adapter-bin=".Length);
                else if (a.StartsWith("--probe-bin=", StringComparison.Ordinal))
                    _probeBin = a.Substring("--probe-bin=".Length);
                else if (a.StartsWith("--parte", StringComparison.Ordinal)) partes.Add(a);
                else { Console.WriteLine("uso: harness-kit14f [--parte1|--parte2|--parte3|--parte4]"
                                         + " [--adapter-bin=<dir>] [--probe-bin=<dir>]"); return 2; }
            }
            foreach (var p in partes)
                if (p != "--parte1" && p != "--parte2" && p != "--parte3" && p != "--parte4")
                { Console.WriteLine("parte desconhecida: " + p); return 2; }

            // KIT-14F: cada parte roda em PROCESSO PROPRIO. As partes compartilham estaticos
            // do Adapter/Core (uma instancia de Type por processo), e rodar tudo no mesmo
            // processo contaminava a contagem da trilha passiva da parte2. Sem argumento de
            // parte, o harness re-executa a si mesmo nas tres.
            if (partes.Count != 1)
            {
                var alvo = partes.Count == 0 ? new List<string> { "--parte1", "--parte2", "--parte3", "--parte4" } : partes;
                int pior = 0;
                foreach (var p in alvo)
                {
                    Console.WriteLine("######## " + p + " (processo proprio) ########");
                    int rc = Reexecutar(p);
                    Console.WriteLine("######## " + p + " exit=" + rc + " ########");
                    if (rc == 2) return 2;
                    if (rc != 0) pior = 1;
                }
                Console.WriteLine("RESULTADO|" + (pior == 0 ? "PASSOU" : "REPROVOU") + "| agregado das partes");
                return pior;
            }

            string parte = partes[0];
            _dirTrabalho = Path.Combine(Path.GetTempPath(), "kit14f-" + Guid.NewGuid().ToString("N").Substring(0, 8));
            Directory.CreateDirectory(_dirTrabalho);

            Console.WriteLine("======================================================================");
            Console.WriteLine(" KIT-14F harness offline — defeitos do run704; parte: " + parte);
            Console.WriteLine(" dir de trabalho: " + _dirTrabalho);
            Console.WriteLine("======================================================================");

            switch (parte)
            {
                case "--parte1": Parte1(); break;
                case "--parte2": Parte2(); break;
                case "--parte3": Parte3(); break;
                case "--parte4": Parte4(); break;
            }

            Console.WriteLine("======================================================================");
            Console.WriteLine(" verificacoes: " + _oks + " OK, " + _falhas + " FALHA, "
                              + _naoExercitado + " NAO_EXERCITADO");
            if (_falhas > 0)
            {
                Console.WriteLine(" RESULTADO|REPROVOU| " + _falhas + " verificacao(oes) falharam.");
                return 1;
            }
            Console.WriteLine(" RESULTADO|PASSOU| todas as verificacoes exercitadas passaram.");
            return 0;
        }

        // ------------------------------------------------------------ utilidades

        private static Assembly Resolver(object _, ResolveEventArgs e)
        {
            var pedido = new AssemblyName(e.Name);
            // 1) PRIMEIRO as ja carregadas: devolver a MESMA instancia evita carregar uma
            //    copia (o build do Adapter copia KIT04Core.dll para o proprio bin, e duas
            //    copias = dois estados estaticos: o Adapter passaria a ver um CorePlugin
            //    diferente do que o harness monta).
            foreach (var a in AppDomain.CurrentDomain.GetAssemblies())
            {
                try
                {
                    if (string.Equals(a.GetName().Name, pedido.Name, StringComparison.OrdinalIgnoreCase)
                        && a.GetName().Version == pedido.Version)
                        return a;
                }
                catch { }
            }
            string nome = pedido.Name + ".dll";
            foreach (var dir in new[] { Lib, Managed, CoreBin, AdapterBin, ProbeBin, BepInExCore })
            {
                try
                {
                    string caminho = Path.Combine(dir, nome);
                    if (File.Exists(caminho)) return Assembly.LoadFrom(caminho);
                }
                catch { }
            }
            return null;
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

        private static void NaoExercitado(string nome, string motivo)
        {
            _naoExercitado++;
            Console.WriteLine("[NAO_EX] " + nome + " -> " + motivo);
        }

        private static Assembly Carregar(string caminho)
        {
            if (!File.Exists(caminho)) throw new FileNotFoundException("assembly ausente: " + caminho);
            return Assembly.LoadFrom(caminho);
        }

        /// <summary>
        /// Traz as dependencias NAO-framework de um assembly carregado por caminho, pelo NOME,
        /// passando pelo resolver do harness. Sem isto o runtime pode acabar carregando uma
        /// COPIA da dependencia na pasta do assembly pedinte (o build do Adapter copia
        /// KIT04Core.dll para o proprio bin) e o Adapter passaria a enxergar um CorePlugin
        /// DIFERENTE do que o harness monta — dois estados estaticos separados.
        /// </summary>
        private static void UnificarReferencias(Assembly asm)
        {
            foreach (var an in asm.GetReferencedAssemblies())
            {
                try { Assembly.Load(an); } catch { /* framework/sem copia local: ja carregado */ }
            }
        }

        private static object NovaInstancia(Type t)
            => FormatterServices.GetUninitializedObject(t);

        private static FieldInfo Campo(Type t, string nome, bool estatico = false)
        {
            var bf = estatico ? (BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static)
                              : (BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            for (var atual = t; atual != null; atual = atual.BaseType)
            {
                var f = atual.GetField(nome, bf);
                if (f != null) return f;
            }
            return null;
        }

        private static object LerCampo(object obj, string nome)
        {
            var f = Campo(obj.GetType(), nome);
            return f == null ? null : f.GetValue(obj);
        }

        private static bool EscreverCampo(object obj, string nome, object valor)
        {
            var f = Campo(obj.GetType(), nome);
            if (f == null) return false;
            try { f.SetValue(obj, valor); return true; } catch { return false; }
        }

        private static MethodInfo Metodo(Type t, string nome, int args = -1)
        {
            foreach (var m in t.GetMethods(BindingFlags.Public | BindingFlags.NonPublic
                                           | BindingFlags.Instance | BindingFlags.Static))
                if (m.Name == nome && (args < 0 || m.GetParameters().Length == args)) return m;
            return null;
        }

        /// <summary>Invoca e devolve a excecao (sem derrubar o harness) ou null.</summary>
        private static Exception Invocar(object obj, MethodInfo m, params object[] args)
        {
            try { m.Invoke(obj, args); return null; }
            catch (TargetInvocationException e) { return e.InnerException ?? e; }
            catch (Exception e) { return e; }
        }

        /// <summary>Igual a `Invocar`, mas devolve tambem o RETORNO do metodo — sem chamar o
        /// alvo duas vezes (era o que fazia "3 quadros" virarem 6 chamadas na rodada 1).</summary>
        private static object InvocarRetorno(object obj, MethodInfo m, out Exception erro, params object[] args)
        {
            try { erro = null; return m.Invoke(obj, args); }
            catch (TargetInvocationException e) { erro = e.InnerException ?? e; return null; }
            catch (Exception e) { erro = e; return null; }
        }

        /// <summary>Liga Config/Logger de um BaseUnityPlugin criado por reflexao.</summary>
        private static void LigarBaseUnityPlugin(object plugin, string nome)
        {
            var t = plugin.GetType();
            while (t != null && t.Name != "BaseUnityPlugin") t = t.BaseType;
            if (t == null) throw new InvalidOperationException("BaseUnityPlugin nao esta na cadeia de " + plugin.GetType().Name);

            var tConfigFile = t.Assembly.GetType("BepInEx.Configuration.ConfigFile");
            var ctor = tConfigFile.GetConstructors()
                .FirstOrDefault(c => c.GetParameters().Length >= 2
                                     && c.GetParameters()[0].ParameterType == typeof(string));
            if (ctor == null) throw new InvalidOperationException("ConfigFile(string, bool) ausente");
            var args = ctor.GetParameters().Select(p => p.ParameterType == typeof(string)
                ? (object)Path.Combine(_dirTrabalho, nome + ".cfg") : false).ToArray();
            object cfg = ctor.Invoke(args);
            Campo(t, "<Config>k__BackingField").SetValue(plugin, cfg);

            var tLoggerStatic = t.Assembly.GetType("BepInEx.Logging.Logger");
            var criar = tLoggerStatic.GetMethods(BindingFlags.Public | BindingFlags.Static)
                .FirstOrDefault(m => m.Name == "CreateLogSource" && m.GetParameters().Length == 1
                                     && m.GetParameters()[0].ParameterType == typeof(string));
            Campo(t, "<Logger>k__BackingField").SetValue(plugin, criar.Invoke(null, new object[] { nome }));

            // KIT-14F — ARTEFATO DO HARNESS, NAO DO PRODUTO:
            // `UnityEngine.Object` sobrecarrega `==` e trata como NULL qualquer objeto sem
            // objeto NATIVO (`IsNativeObjectAlive(o) => o.GetCachedPtr() != IntPtr.Zero`).
            // Um plugin criado por `GetUninitializedObject` tem `m_CachedPtr == 0`, entao
            // `core == null` devolvia TRUE para um Core EXISTENTE e o vinculo nunca concluia.
            // Um plugin REAL sempre tem objeto nativo; aqui marcamos o mesmo estado para a
            // checagem nao mentir.
            MarcarComoObjetoUnityVivo(plugin);
        }

        private static void MarcarComoObjetoUnityVivo(object plugin)
        {
            for (var t = plugin.GetType(); t != null; t = t.BaseType)
            {
                var f = t.GetField("m_CachedPtr", BindingFlags.NonPublic | BindingFlags.Instance);
                if (f != null && f.FieldType == typeof(IntPtr)) { f.SetValue(plugin, new IntPtr(1)); return; }
            }
            throw new InvalidOperationException(
                "campo m_CachedPtr de UnityEngine.Object nao encontrado em " + plugin.GetType().FullName);
        }

        /// <summary>
        /// KIT-14F — ARTEFATO DO HARNESS, NAO DO PRODUTO:
        /// `GetUninitializedObject` NAO roda inicializador de campo, entao propriedades
        /// auto-inicializadas do plugin (ex.: `CorePlugin.Identidade = new IdentidadeDoCoreImpl()`)
        /// ficam null e `ResultadoFinal()` estoura com NRE. A Unity cria o plugin pelo
        /// construtor normal; aqui completamos o que o inicializador faria.
        /// </summary>
        private static void CompletarInicializadoresDePropriedade(object plugin)
        {
            foreach (var p in plugin.GetType().GetProperties(
                         BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance))
            {
                if (p.GetIndexParameters().Length > 0) continue;
                var getter = p.GetGetMethod(true);
                if (getter == null || getter.IsStatic) continue;
                var bf = Campo(plugin.GetType(), "<" + p.Name + ">k__BackingField");
                if (bf == null) continue;
                try
                {
                    if (bf.GetValue(plugin) != null) continue;
                    Type tipo = p.PropertyType;
                    if (!tipo.IsAbstract && !tipo.IsInterface)
                    {
                        EscreverCampo(plugin, bf.Name, Activator.CreateInstance(tipo, true));
                        continue;
                    }
                    var impl = tipo.Assembly.GetTypes().FirstOrDefault(
                        x => x.IsClass && !x.IsAbstract && tipo.IsAssignableFrom(x));
                    if (impl != null) EscreverCampo(plugin, bf.Name, Activator.CreateInstance(impl, true));
                }
                catch { }
            }
        }

        private static bool LigarOptIn(Type tipoPlugin, string nomeCampo, bool valor)
        {
            var f = Campo(tipoPlugin, nomeCampo, estatico: true);
            if (f == null) return false;
            object entry = f.GetValue(null);
            if (entry == null) return false;
            var p = entry.GetType().GetProperty("Value");
            if (p == null) return false;
            p.SetValue(entry, valor);
            return true;
        }

        /// <summary>
        /// KIT-14F: o Core guarda o opt-in em campo de INSTANCIA (`_habilitado`), nao no
        /// campo estatico que `LigarOptIn` procura — chamar aquele aqui devolvia `false`
        /// em silencio e `EstaHabilitado()` seguia falso (era o que travava a parte2).
        /// </summary>
        private static bool LigarOptInInstancia(object plugin, string nomeCampo, bool valor)
        {
            object entry = LerCampo(plugin, nomeCampo);
            if (entry == null) return false;
            var p = entry.GetType().GetProperty("Value");
            if (p == null) return false;
            p.SetValue(entry, valor);
            return true;
        }

        private sealed class Montagem
        {
            public Assembly AsmCore, AsmAdapter;
            public Type TCore, TAdapter;
            public object Core, Adapter;
            public Exception ErroAwakeAdapter, ErroAwakeCore;
            public string CaminhoAwakeAdapter = "(Awake nao executado)";
        }

        /// <summary>Monta Adapter e Core REAIS na ORDEM OBSERVADA no run704: Adapter antes.</summary>
        private static Montagem Montar(bool comCore = true, bool corePrimeiro = false)
        {
            var m = new Montagem();
            m.AsmCore = Carregar(Path.Combine(CoreBin, "KIT04Core.dll"));
            // O bin do Adapter tem uma COPIA de KIT04Core.dll; carregar o Adapter de dentro
            // dele faria o runtime ligar a copia (estado estatico SEPARADO do Core que o
            // harness monta). Copiamos SO o Adapter para uma pasta limpa e carregamos de la.
            string dirLimpo = Path.Combine(_dirTrabalho, "adapter" + (++_montagens));
            Directory.CreateDirectory(dirLimpo);
            File.Copy(Path.Combine(_adapterBin, "KIT04Adapter.SR.dll"),
                      Path.Combine(dirLimpo, "KIT04Adapter.SR.dll"), true);
            m.AsmAdapter = Carregar(Path.Combine(dirLimpo, "KIT04Adapter.SR.dll"));
            UnificarReferencias(m.AsmAdapter);
            UnificarReferencias(m.AsmCore);
            m.TCore = m.AsmCore.GetType("KIT04Core.CorePlugin");
            m.TAdapter = m.AsmAdapter.GetType("KIT04Adapter.SR.SRAdapterPlugin");

            if (comCore && corePrimeiro)
            {
                // 0) Core PRIMEIRO (ordem que o [BepInDependency] passa a garantir).
                m.Core = NovaInstancia(m.TCore);
                LigarBaseUnityPlugin(m.Core, "kit14f-core");
                m.ErroAwakeCore = Invocar(m.Core, Metodo(m.TCore, "Awake", 0));
            }

            // 1) Adapter PRIMEIRO (a ordem que o Chainloader escolheu conforme o run704).
            m.Adapter = NovaInstancia(m.TAdapter);
            LigarBaseUnityPlugin(m.Adapter, "kit14f-adapter");
            CompletarInicializadoresDePropriedade(m.Adapter);
            var awakeAdapter = Metodo(m.TAdapter, "Awake", 0);
            m.ErroAwakeAdapter = Invocar(m.Adapter, awakeAdapter);
            if (m.ErroAwakeAdapter != null)
            {
                var st = m.ErroAwakeAdapter.StackTrace ?? "";
                var linha = st.Split('\n').FirstOrDefault(l => l.Contains("SRAdapterPlugin")) ?? "(sem linha do Adapter)";
                m.CaminhoAwakeAdapter = m.ErroAwakeAdapter.GetType().Name + ": " + m.ErroAwakeAdapter.Message
                                        + " | " + linha.Trim();
            }
            else m.CaminhoAwakeAdapter = "sem excecao";

            if (!comCore) return m;

            // 2) Core DEPOIS (o que a ordem correta faria).
            m.Core = NovaInstancia(m.TCore);
            LigarBaseUnityPlugin(m.Core, "kit14f-core");
            CompletarInicializadoresDePropriedade(m.Core);
            m.ErroAwakeCore = Invocar(m.Core, Metodo(m.TCore, "Awake", 0));
            return m;
        }

        // ------------------------------------------------------------ parte 1

        private static void Parte1()
        {
            Console.WriteLine("-- parte1: ciclo de vida Adapter/Core (NullReferenceException em Awake) --");
            var m = Montar();

            // (a) NENHUMA excecao ao subir o Adapter sem o Core inicializado.
            Checa("Adapter.Awake NAO estoura com o Core ainda nao inicializado",
                  m.ErroAwakeAdapter == null, m.CaminhoAwakeAdapter);

            // (b) o vinculo fica PENDENTE e DECLARADO (nada de estado silencioso).
            string estado = Convert.ToString(LerCampo(m.Adapter, "_estadoVinculo"), CultureInfo.InvariantCulture);
            Checa("Adapter declara vinculo PENDENTE (aguardando_core)", estado == "aguardando_core",
                  "_estadoVinculo=" + (estado ?? "(campo ausente)"));

            // (c) o Adapter DECLARA a dependencia do Core (ordem de carga no Chainloader).
            var deps = new List<string>();
            try
            {
                foreach (var a in m.TAdapter.GetCustomAttributes(false))
                {
                    string n = a.GetType().Name;
                    if (n.IndexOf("BepInDependency", StringComparison.Ordinal) < 0) continue;
                    var p = a.GetType().GetProperty("DependencyGUID");
                    deps.Add(Convert.ToString(p == null ? null : p.GetValue(a), CultureInfo.InvariantCulture));
                }
            }
            catch (Exception e) { Console.WriteLine("   (atributos: " + e.GetType().Name + ")"); }
            Checa("Adapter declara [BepInDependency] do Core (com.gumatos.kit04.core)",
                  deps.Contains("com.gumatos.kit04.core"), "deps=[" + string.Join(",", deps) + "]");

            Checa("Core.Awake subiu no harness (base da prova)", m.ErroAwakeCore == null,
                  m.ErroAwakeCore == null ? null : m.ErroAwakeCore.GetType().Name + ": " + m.ErroAwakeCore.Message);

            // DIAGNOSTICO (evidencia): identidade do Core visto pelo Adapter e pelo harness.
            // KIT-14F — ARMADILHA DO HARNESS (documentada porque ja enganou uma rodada):
            // `UnityEngine.Object` sobrecarrega `==` e trata como NULL todo objeto SEM
            // objeto nativo. O CorePlugin criado aqui por `GetUninitializedObject` tinha
            // `m_CachedPtr == 0` e portanto `core == null` devolvia TRUE para um Core
            // EXISTENTE — o vinculo nunca concluia. `LigarBaseUnityPlugin` agora marca
            // `m_CachedPtr` (um plugin REAL sempre tem objeto nativo), e a checagem para
            // de mentir.
            try
            {
                foreach (var a in AppDomain.CurrentDomain.GetAssemblies())
                    if (a.GetName().Name == "KIT04Core")
                        Console.WriteLine("   KIT04Core[" +
                            System.Runtime.CompilerServices.RuntimeHelpers.GetHashCode(a)
                            + "] @" + a.Location);
                var refCore = m.AsmAdapter.GetReferencedAssemblies()
                    .FirstOrDefault(a => a.Name == "KIT04Core");
                var asmCore2 = Assembly.Load(refCore);
                Console.WriteLine("   Adapter e harness veem o MESMO assembly: "
                                  + ReferenceEquals(asmCore2, m.AsmCore));
                Console.WriteLine("   Adapter e harness veem o MESMO Type: "
                                  + ReferenceEquals(asmCore2.GetType("KIT04Core.CorePlugin"), m.TCore));
                var campoInst = m.TCore.GetField("_instancia",
                    BindingFlags.NonPublic | BindingFlags.Static);
                Console.WriteLine("   CorePlugin._instancia != null: "
                                  + (campoInst != null && campoInst.GetValue(null) != null));
            }
            catch (Exception e) { Console.WriteLine("   (diagnostico falhou: " + e.GetType().Name + ")"); }

            // (d) com o Core vivo, o vinculo conclui e a ponte (trilha passiva) nasce.
            LigarOptIn(m.TAdapter, "p_Habilitado", true);
            LigarOptIn(m.TAdapter, "p_PassivoHabilitado", true);
            var vincular = Metodo(m.TAdapter, "TentarVincular", 0);
            if (vincular == null)
            {
                Checa("Adapter conclui o vinculo quando o Core existe (TentarVincular)", false,
                      "metodo 'TentarVincular' AUSENTE no Adapter (conserto nao aplicado)");
            }
            else
            {
                // KIT-14F: retomada do vinculo e IDEMPOTENTE (o Update chama todo quadro).
                // 3 iteracoes = 3 quadros simulados, com UMA chamada a `TentarVincular` por
                // quadro. (Rodada 1 chamava DUAS vezes por iteracao — `Invocar` + `Invoke`
                // direto — entao "3 quadros" eram 6 chamadas e o rotulo mentia; achado da
                // revisao run707.)
                Exception primeiroErro = null;
                object primeiraPonte = null;
                int concluidas = 0, recriadas = 0, invocacoes = 0;
                for (int i = 1; i <= 3; i++)
                {
                    Exception erro = null;
                    object ret = InvocarRetorno(m.Adapter, vincular, out erro);
                    invocacoes++;
                    if (i == 1) primeiroErro = erro;
                    object ponteAgora = LerCampo(m.Adapter, "_ponte");
                    if (i == 1) primeiraPonte = ponteAgora;
                    else if (!ReferenceEquals(ponteAgora, primeiraPonte)) recriadas++;
                    if (Convert.ToBoolean(ret == null ? false : ret)) concluidas++;
                    Console.WriteLine("   quadro" + i + ": chamadas_a_TentarVincular=" + invocacoes
                                      + " excecao=" + (erro == null ? "nao" : erro.GetType().Name)
                                      + " retorno=" + ret
                                      + " _vinculado=" + LerCampo(m.Adapter, "_vinculado")
                                      + " _estadoVinculo=" + LerCampo(m.Adapter, "_estadoVinculo"));
                }
                Checa("um quadro = UMA chamada a TentarVincular (3 quadros = 3 chamadas)",
                      invocacoes == 3, "invocacoes=" + invocacoes);
                var campoDiag = Campo(m.TAdapter, "Kit14fDiagnostico", estatico: true);
                Console.WriteLine("   DIAGNOSTICO DENTRO DO ADAPTER: "
                                  + (campoDiag == null ? "(campo ausente)" : campoDiag.GetValue(null)));
                var campoHarmony = Campo(m.TAdapter, "HarmonyEstado", estatico: true);
                Console.WriteLine("   estado do patch Harmony (campo HarmonyEstado): "
                                  + (campoHarmony == null ? "(campo ausente)" : campoHarmony.GetValue(null)));

                Checa("Adapter conclui o vinculo quando o Core existe (sem excecao)",
                      primeiroErro == null,
                      primeiroErro == null ? null : primeiroErro.GetType().Name + ": " + primeiroErro.Message);
                Checa("ponte da trilha passiva criada no vinculo", primeiraPonte != null,
                      "_ponte=" + (primeiraPonte == null ? "null" : "instancia"));
                Checa("estado do vinculo = ligado",
                      Convert.ToString(LerCampo(m.Adapter, "_estadoVinculo")) == "ligado",
                      "_estadoVinculo=" + LerCampo(m.Adapter, "_estadoVinculo"));
                Checa("vinculo conclui nos 3 quadros simulados (idempotente)", concluidas == 3,
                      "concluidas=" + concluidas + "/3");
                Checa("a ponte NAO e recriada a cada quadro", recriadas == 0,
                      "recriadas=" + recriadas);
            }

            NaoExercitado("Chainloader real do BepInEx ordenando os plugins dentro do jogo",
                "exige o jogo aberto (proibido clique/boot nao supervisionado nesta rodada); aqui a ordem e SIMULADA pela chamada de Awake Adapter-antes-de-Core");
        }

        // ------------------------------------------------------------ parte 2

        private static void Parte2()
        {
            Console.WriteLine("-- parte2: trilha passiva (recorder) com contagem E arquivo --");
            var m = Montar();
            if (m.ErroAwakeAdapter != null)
            {
                Checa("recorder produz contagem", false,
                      "o Adapter nem subiu: " + m.CaminhoAwakeAdapter + " (a trilha nunca nasce)");
                Checa("recorder produz arquivo de resultado", false,
                      "sem trilha nao ha resultado para gravar");
                return;
            }

            LigarOptIn(m.TAdapter, "p_Habilitado", true);
            LigarOptIn(m.TAdapter, "p_PassivoHabilitado", true);
            Console.WriteLine("   opt-in do Core (instancia _habilitado): "
                              + LigarOptInInstancia(m.Core, "_habilitado", true));

            var vincular = Metodo(m.TAdapter, "TentarVincular", 0);
            if (vincular != null) Invocar(m.Adapter, vincular);
            object ponte = LerCampo(m.Adapter, "_ponte");
            if (ponte == null)
            {
                Checa("recorder tem trilha ligada", false, "_ponte ausente (vinculo nao concluiu)");
                Checa("recorder produz contagem", false, "sem trilha");
                Checa("recorder produz arquivo de resultado", false, "sem trilha");
                return;
            }

            var alimentar = Metodo(m.TAdapter, "AlimentarPassivo", 3);
            if (alimentar == null)
            {
                Checa("recorder e alimentado pelo MESMO metodo que o Update usa (AlimentarPassivo)", false,
                      "metodo 'AlimentarPassivo(bool[],bool,long)' AUSENTE no Adapter (conserto nao aplicado)");
                Checa("recorder produz contagem", false, "sem ponto de alimentacao exercitavel");
                return;
            }

            // Cenario minimo real: abre SkillsPanel -> clique COM janela -> fecha.
            int registrados = 0;
            registrados += Convert.ToInt32(alimentar.Invoke(m.Adapter, new object[] { new[] { false, true, false, false }, false, 0L }));
            registrados += Convert.ToInt32(alimentar.Invoke(m.Adapter, new object[] { new[] { false, true, false, false }, true, 5L }));
            registrados += Convert.ToInt32(alimentar.Invoke(m.Adapter, new object[] { new[] { false, false, false, false }, false, 15L }));
            Console.WriteLine("   eventos injetados na trilha: " + registrados);

            var resultadoFinal = Metodo(m.TCore, "ResultadoFinal", 0);
            object resultado;
            try { resultado = resultadoFinal.Invoke(m.Core, null); }
            catch (Exception e)
            {
                var ie = e is TargetInvocationException t ? (t.InnerException ?? t) : e;
                Checa("Core.ResultadoFinal executou", false,
                      ie.GetType().FullName + ": " + ie.Message
                      + (ie.InnerException == null ? "" : " <- " + ie.InnerException.GetType().Name + ": " + ie.InnerException.Message));
                return;
            }

            var dic = resultado as IDictionary;
            var eventos = dic != null && dic.Contains("eventos") ? dic["eventos"] as IList : null;
            var passivo = dic != null && dic.Contains("passivo") ? dic["passivo"] as IDictionary : null;
            object totalCru = passivo != null && passivo.Contains("eventos_total") ? passivo["eventos_total"] : null;
            int total = totalCru == null ? -1 : Convert.ToInt32(totalCru);
            int nEventos = eventos == null ? -1 : eventos.Count;

            Console.WriteLine("   passivo.eventos_total=" + total + " eventos_do_livro=" + nEventos);
            Checa("recorder capturou CONTAGEM > 0 (passivo.eventos_total)",
                  total > 0, "eventos_total=" + total);
            Checa("recorder registrou os eventos no livro do Core",
                  nEventos > 0, "eventos=" + nEventos);
            if (nEventos > 0)
            {
                var tipos = new List<string>();
                foreach (var ev in eventos)
                {
                    var d = ev as IDictionary;
                    if (d != null && d.Contains("tipo")) tipos.Add(Convert.ToString(d["tipo"]));
                }
                Checa("eventos capturados tem tipo 'passivo_*'", tipos.Any(t => t != null && t.StartsWith("passivo_")),
                      "tipos=[" + string.Join(",", tipos.Take(6)) + "]");
            }

            // ARQUIVO: serializa o resultado com o Json do PROPRIO Core e le de volta do disco.
            string caminhoJson = Path.Combine(_dirTrabalho, "resultado-core.json");
            try
            {
                var tJson = m.AsmCore.GetType("KIT04Core.Json");
                var ser = tJson.GetMethod("Serialize", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static);
                string texto = Convert.ToString(ser.Invoke(null, new[] { resultado }));
                File.WriteAllText(caminhoJson, texto, new System.Text.UTF8Encoding(false));
            }
            catch (Exception e)
            {
                Checa("recorder produz ARQUIVO de resultado", false, "falha ao gravar: " + e.GetType().Name + ": " + e.Message);
                return;
            }
            var fi = new FileInfo(caminhoJson);
            string lido = File.Exists(caminhoJson) ? File.ReadAllText(caminhoJson) : null;
            Checa("recorder produz ARQUIVO de resultado (bytes > 0, lido de volta)",
                  fi.Exists && fi.Length > 0 && !string.IsNullOrEmpty(lido), caminhoJson);
            Checa("arquivo de resultado contem os eventos capturados",
                  !string.IsNullOrEmpty(lido) && lido.Contains("passivo_"), "conteudo: " + (lido == null ? "(vazio)" : lido.Substring(0, Math.Min(120, lido.Length))));

            NaoExercitado("recorder capturando de um jogo REAL em execucao (contagem/arquivo do jogo)",
                "exige o jogo aberto e a build instalada, o que esta rodada nao autoriza; a contagem/arquivo acima vem da trilha REAL alimentada por estado sintetico");
        }

        // ------------------------------------------------------------ parte 3

        // KIT-14F (rodada 2) — A PARTE 3 PASSOU A EXERCITAR O DRIVER REAL.
        // Na rodada 1 ela chamava `TentarNavegar()` num LACO MANUAL (`for` 12x aqui dentro):
        // o laco que o PRODUTO nao tinha era fabricado pelo TESTE — verde falso apontado
        // pela revisao run707. Agora o harness so AVANCA QUADROS chamando `Passo()` (o passo
        // por quadro do produto); quem reinvoca `TentarNavegar` quadro a quadro e o
        // `case F_NAVEGACAO`, alcancado pelo caminho real `F_LEITURA -> F_NAVEGACAO`.
        private static int _chamadasDaPorta;
        private static int _invocacoesDaPorta;
        private static int _alvoAPartirDaChamada = -1;   // <0 = o alvo NUNCA aparece

        private static List<(string rotulo, bool ativo, Action invocar)> PortaDeCenario()
        {
            int chamada = _chamadasDaPorta++;
            var lista = new List<(string, bool, Action)>();
            if (_alvoAPartirDaChamada >= 0 && chamada >= _alvoAPartirDaChamada)
                lista.Add(("Skills", true, () => { _invocacoesDaPorta++; }));
            else
                lista.Add(("Continue", true, () => { }));
            return lista;
        }

        private static List<(string rotulo, bool ativo, Action invocar)> PortaVazia()
        {
            return new List<(string, bool, Action)>();
        }

        /// <summary>Valor de uma const do produto (o teto/teto de fases NAO e inventado pelo
        /// teste: e lido do proprio binario exercitado).</summary>
        private static int LerConst(Type t, string nome, int padrao)
        {
            var f = Campo(t, nome, estatico: true);
            if (f == null) return padrao;
            try { return Convert.ToInt32(f.GetRawConstantValue()); } catch { return padrao; }
        }

        /// <summary>Cria uma ConfigEntry pelo `Bind` do ConfigFile do plugin (mesma porta que
        /// o Awake usa). Sem engine: `ConfigFile` e .NET puro.</summary>
        private static string _erroConfigurar;

        private static object Configurar(object cfg, string secao, string chave, object padrao)
        {
            if (cfg == null) { _erroConfigurar = "ConfigFile ausente no plugin"; return null; }
            var metodos = cfg.GetType().GetMethods(BindingFlags.Public | BindingFlags.Instance)
                .Where(x => x.Name == "Bind" && x.IsGenericMethodDefinition
                    && x.GetParameters().Length == 4
                    && x.GetParameters()[0].ParameterType == typeof(string)
                    && x.GetParameters()[1].ParameterType == typeof(string)
                    && x.GetParameters()[2].ParameterType.IsGenericParameter)
                .ToList();
            // `Bind<T>` tem DUAS sobrecargas de 4 parametros: a 4a pode ser `string` (descricao)
            // ou `ConfigDescription`. A do `string` e a que o Awake usa.
            var m = metodos.FirstOrDefault(x => x.GetParameters()[3].ParameterType == typeof(string))
                    ?? metodos.FirstOrDefault();
            if (m == null)
            {
                _erroConfigurar = "overload Bind(string,string,T,string) nao encontrado em "
                                  + cfg.GetType().FullName + "; candidatos: "
                                  + string.Join(",", cfg.GetType().GetMethods()
                                        .Where(x => x.Name == "Bind")
                                        .Select(x => x.GetParameters().Length).Distinct());
                return null;
            }
            try
            {
                object descricao = m.GetParameters()[3].ParameterType == typeof(string)
                    ? (object)"harness KIT-14F"
                    : Activator.CreateInstance(m.GetParameters()[3].ParameterType, "harness KIT-14F");
                return m.MakeGenericMethod(padrao.GetType())
                        .Invoke(cfg, new[] { secao, chave, padrao, descricao });
            }
            catch (Exception e)
            {
                _erroConfigurar = "invoke Bind<" + padrao.GetType().Name + ">: " + e.GetType().Name + ": " + e.Message;
                return null;
            }
        }

        /// <summary>Monta o plugin REAL do probe com o estado que o Awake inicializa (o
        /// `GetUninitializedObject` nao roda inicializador de campo). ARTEFATO DO HARNESS:
        /// sem isto o `case F_LEITURA` estoura em NullReferenceException ANTES de chegar na
        /// navegacao, e o teste mediria o harness em vez do produto.</summary>
        private static object MontarProbe(Type tProbe, string nome, string dir)
        {
            object probe = NovaInstancia(tProbe);
            LigarBaseUnityPlugin(probe, nome);
            EscreverCampo(probe, "_res", new Dictionary<string, object>());
            EscreverCampo(probe, "_passos", new Dictionary<string, object>());
            EscreverCampo(probe, "_marcos", new List<string>());
            EscreverCampo(probe, "_observacoes", new List<object>());
            EscreverCampo(probe, "_arquivosDePrint", new List<string>());
            EscreverCampo(probe, "_eventosFrame", new Dictionary<string, object>());
            EscreverCampo(probe, "_printsDetalhe", new Dictionary<string, object>());
            EscreverCampo(probe, "_dir", dir);
            var cfg = Campo(tProbe, "<Config>k__BackingField") == null
                ? null : Campo(tProbe, "<Config>k__BackingField").GetValue(probe);
            EscreverCampo(probe, "_navegar", Configurar(cfg, "Geral", "Navegar", true));
            EscreverCampo(probe, "_demostrar", Configurar(cfg, "Geral", "DemostrarTooltip", false));
            EscreverCampo(probe, "_autorizaEscrita", Configurar(cfg, "Geral", "AutorizaEscritaTooltip", false));
            EscreverCampo(probe, "_maxTextos", Configurar(cfg, "Geral", "MaxTextos", 50));
            EscreverCampo(probe, "_perfilDir", Configurar(cfg, "Geral", "PerfilDir", ""));
            EscreverCampo(probe, "_hashFonte", Configurar(cfg, "Geral", "HashFonte", ""));
            EscreverCampo(probe, "_sessaoCfg", Configurar(cfg, "Geral", "Sessao", ""));
            EscreverCampo(probe, "_marcador", Configurar(cfg, "Geral", "MarcadorIdaEVolta", ""));
            EscreverCampo(probe, "_orcamento", Configurar(cfg, "Geral", "OrcamentoSegundos", 1f));
            EscreverCampo(probe, "_outDir", Configurar(cfg, "Geral", "OutDir", dir));
            return probe;
        }

        private static void Parte3()
        {
            Console.WriteLine("-- parte3: navegacao por handler dirigida pelo DRIVER REAL (Passo por QUADRO) --");
            Assembly asmProbe;
            try { asmProbe = Carregar(Path.Combine(_probeBin, "AUT4Probe.dll")); }
            catch (Exception e) { Checa("AUT4Probe.dll carregou", false, e.Message); return; }

            var tProbe = asmProbe.GetType("Aut4Probe.Aut4ProbePlugin");
            if (tProbe == null) { Checa("tipo Aut4ProbePlugin", false, "nao encontrado"); return; }

            Console.WriteLine("   binario exercitado: " + Path.Combine(_probeBin, "AUT4Probe.dll"));
            // O TESTE NAO CHAMA `TentarNavegar` NENHUMA VEZ: quem avanca quadro a quadro e o
            // `Passo()` do PRODUTO. Era exatamente isto que faltava na rodada 1.
            var passo = Metodo(tProbe, "Passo", 0);
            Checa("o PRODUTO expoe o passo por quadro (Passo)", passo != null,
                  "metodo 'Passo()' ausente no binario exercitado");
            if (passo == null) return;

            var campoPorta = Campo(tProbe, "PortaDeBotoes", estatico: true);
            Checa("o PRODUTO tem porta injetavel da fonte de botoes (PortaDeBotoes)", campoPorta != null,
                  "campo 'PortaDeBotoes' ausente: sem costura, a escolha do alvo so existe no jogo");
            if (campoPorta != null)
            {
                Func<List<(string rotulo, bool ativo, Action invocar)>> porta = PortaDeCenario;
                campoPorta.SetValue(null, porta);
            }

            int fLeitura = LerConst(tProbe, "F_LEITURA", 1);
            int fPrint1 = LerConst(tProbe, "F_PRINT1", 2);
            int fNavegacao = LerConst(tProbe, "F_NAVEGACAO", -1);
            int teto = LerConst(tProbe, "NavegacaoTentativasMax", 12);
            Console.WriteLine("   fases do produto: F_LEITURA=" + fLeitura + " F_NAVEGACAO=" + fNavegacao
                              + " F_PRINT1=" + fPrint1 + " | TETO declarado pelo produto=" + teto);
            Checa("o PRODUTO tem FASE propria de navegacao (F_NAVEGACAO)", fNavegacao >= 0,
                  "const 'F_NAVEGACAO' ausente: a navegacao NAO tem fase — e de QUADRO UNICO "
                  + "(o defeito do run704: tenta 1 vez, ve 0 botoes e segue para o print)");
            Checa("o PRODUTO declara TETO de tentativas > 0 (lido do binario, nao do teste)",
                  teto > 0, "NavegacaoTentativasMax=" + teto);

            // ---- ROTEIRO DEPOIS DA LEITURA (o defeito 3 e exatamente aqui).
            // `PassoLeitura()` NAO roda fora do jogo (ver NAO_EXERCITADO ao fim: o corpo dela
            // chama engine). O ROTEIRO que ela usa foi extraido para um passo NOMEADO e
            // engine-free (`FaseDepoisDaLeitura`), que da para exercitar direto — e o IL prova
            // que e ELE que a fase de leitura chama (o `Ir(F_PRINT1)` nao e incondicional).
            var rota = Metodo(tProbe, "FaseDepoisDaLeitura", 0);
            Checa("o PRODUTO tem o roteiro pos-leitura num passo nomeado (FaseDepoisDaLeitura)",
                  rota != null, "metodo 'FaseDepoisDaLeitura()' ausente: o roteiro continua trancado "
                  + "dentro da fase de leitura (quadro unico)");
            if (rota != null)
            {
                _alvoAPartirDaChamada = -1; _chamadasDaPorta = 0; _invocacoesDaPorta = 0;
                object pr = MontarProbe(tProbe, "kit14f-rota", Path.Combine(_dirTrabalho, "rota"));
                Console.WriteLine("   config sintetica do probe (Bind do ConfigFile): "
                                  + (_erroConfigurar == null ? "ok" : "FALHOU -> " + _erroConfigurar));
                Exception erroR = null;
                object retR = InvocarRetorno(pr, rota, out erroR);
                Checa("(A0) sem alvo e teto nao esgotado, o roteiro pos-leitura vai para a FASE DE NAVEGACAO",
                      erroR == null && retR != null && Convert.ToInt32(retR) == fNavegacao,
                      "retorno=" + retR + " (esperado F_NAVEGACAO=" + fNavegacao + ")"
                      + (erroR == null ? "" : " | " + erroR.GetType().Name + ": " + erroR.Message));
            }

            var passoLeitura = Metodo(tProbe, "PassoLeitura", 0);
            var passoNav = Metodo(tProbe, "PassoNavegacao", 0);
            Checa("(IL) `PassoLeitura` chama o roteiro `FaseDepoisDaLeitura` (o print nao e incondicional)",
                  passoLeitura != null && rota != null && ChamaMetodo(passoLeitura, rota),
                  "nao achei a chamada no IL de PassoLeitura");
            Checa("(IL) o despachante `Passo` manda F_NAVEGACAO para o passo nomeado `PassoNavegacao`",
                  passoNav != null && ChamaMetodo(passo, passoNav),
                  "nao achei a chamada no IL de Passo");

            // =============== (A) O DRIVER REAL: um `Passo()` por QUADRO.
            // O alvo aparece DEPOIS de 2 quadros sem alvo (a tela de LOADING do run704).
            _alvoAPartirDaChamada = 2;      // consultas 0,1 -> "Continue"; consulta 2 -> "Skills"
            _chamadasDaPorta = 0; _invocacoesDaPorta = 0;
            string dirA = Path.Combine(_dirTrabalho, "probe-a");
            Directory.CreateDirectory(dirA);
            object probeA = MontarProbe(tProbe, "kit14f-probe-a", dirA);
            EscreverCampo(probeA, "_fase", fNavegacao);

            int quadrosA = 0, faseFinalA = fNavegacao;
            Exception erroA = null;
            while (quadrosA < teto + 5)
            {
                erroA = Invocar(probeA, passo);
                quadrosA++;
                faseFinalA = Convert.ToInt32(LerCampo(probeA, "_fase"));
                if (erroA != null || faseFinalA != fNavegacao) break;
            }
            Console.WriteLine("   (A) quadros avancados pelo driver=" + quadrosA
                              + " fase final=" + faseFinalA
                              + " chamadas da porta=" + _chamadasDaPorta
                              + " invocacoes do alvo=" + _invocacoesDaPorta
                              + " erro=" + (erroA == null ? "nao" : erroA.GetType().Name + ": " + erroA.Message
                                                          + " | onde=" + Onde(erroA)));

            Checa("(A) o DRIVER avancou mais de um quadro (o laco mora no PRODUTO, nao no teste)",
                  quadrosA >= 3, "quadros=" + quadrosA);
            Checa("(A) o PRODUTO releu a fonte de botoes quadro a quadro",
                  _chamadasDaPorta >= 3, "chamadas da porta=" + _chamadasDaPorta);
            Checa("(A) o PRODUTO invocou o handler do alvo EXATAMENTE uma vez",
                  _invocacoesDaPorta == 1, "invocacoes=" + _invocacoesDaPorta);
            Checa("(A) o PRODUTO saiu da fase de navegacao SOZINHO, para o print",
                  faseFinalA == fPrint1, "fase final=" + faseFinalA + " (esperada F_PRINT1=" + fPrint1 + ")"
                  + (erroA == null ? "" : " | erro=" + erroA.GetType().Name + " em " + Onde(erroA)));
            Checa("(A) sem excecao no passo por quadro do driver", erroA == null,
                  erroA == null ? null : erroA.GetType().Name + ": " + erroA.Message + " | onde=" + Onde(erroA));
            if (erroA != null) DumpPassos(probeA);
            var passosA = LerCampo(probeA, "_passos") as IDictionary;
            var listaA = passosA != null && passosA.Contains("navegacao") ? passosA["navegacao"] as IList : null;
            var resumoA = EntradaResumo(listaA);
            Checa("(A) o PRODUTO grava um RESUMO da navegacao (estagio=resumo)", resumoA != null,
                  "nenhuma entrada com estagio=resumo");
            Checa("(A) o resumo declara o alvo INVOCADO com as tentativas gastas",
                  resumoA != null && Texto(resumoA, "estado") == "invocado" && Num(resumoA, "tentativas") == 3,
                  resumoA == null ? "sem resumo" : "estado=" + Texto(resumoA, "estado")
                      + " tentativas=" + Texto(resumoA, "tentativas"));
            Checa("(A) o resumo declara o TETO usado",
                  resumoA != null && Num(resumoA, "tentativas_max") == teto,
                  resumoA == null ? "sem resumo" : "tentativas_max=" + Texto(resumoA, "tentativas_max")
                      + " (produto=" + teto + ")");

            // =============== (B) o alvo NUNCA aparece: o produto tem de ESGOTAR o teto e SAIR
            _alvoAPartirDaChamada = -1;
            _chamadasDaPorta = 0; _invocacoesDaPorta = 0;
            string dirB = Path.Combine(_dirTrabalho, "probe-b");
            Directory.CreateDirectory(dirB);
            object probeB = MontarProbe(tProbe, "kit14f-probe-b", dirB);
            EscreverCampo(probeB, "_fase", fNavegacao);

            int quadrosB = 0, faseFinalB = fNavegacao;
            Exception erroB = null;
            while (quadrosB < teto + 5)
            {
                erroB = Invocar(probeB, passo);
                quadrosB++;
                faseFinalB = Convert.ToInt32(LerCampo(probeB, "_fase"));
                if (erroB != null || faseFinalB != fNavegacao) break;
            }
            Console.WriteLine("   (B) sem alvo: quadros=" + quadrosB + " fase final=" + faseFinalB
                              + " chamadas da porta=" + _chamadasDaPorta
                              + " erro=" + (erroB == null ? "nao" : erroB.GetType().Name));

            Checa("(B) sem alvo, o driver NAO trava: esgota o teto e SAI da fase", faseFinalB == fPrint1,
                  "fase final=" + faseFinalB + " (esperada F_PRINT1=" + fPrint1 + ") apos " + quadrosB + " quadros");
            Checa("(B) o DRIVER gastou exatamente o TETO declarado pelo proprio produto", quadrosB == teto,
                  "quadros=" + quadrosB + " teto do produto=" + teto);
            Checa("(B) sem alvo, o PRODUTO nao invocou handler nenhum", _invocacoesDaPorta == 0,
                  "invocacoes=" + _invocacoesDaPorta);
            var passosB = LerCampo(probeB, "_passos") as IDictionary;
            var listaB = passosB != null && passosB.Contains("navegacao") ? passosB["navegacao"] as IList : null;
            var resumoB = EntradaResumo(listaB);
            Checa("(B) o resumo declara estado=esgotado com MOTIVO",
                  resumoB != null && Texto(resumoB, "estado") == "esgotado"
                  && !string.IsNullOrEmpty(Texto(resumoB, "motivo")),
                  resumoB == null ? "sem resumo" : "estado=" + Texto(resumoB, "estado")
                      + " motivo=" + Texto(resumoB, "motivo"));

            // =============== (C) o TETO vindo da opcao do .cfg que o produto passou a oferecer
            string dirC = Path.Combine(_dirTrabalho, "probe-c");
            Directory.CreateDirectory(dirC);
            object probeC = MontarProbe(tProbe, "kit14f-probe-c", dirC);
            var fCfg = Campo(tProbe, "<Config>k__BackingField");
            var cfgC = fCfg == null ? null : fCfg.GetValue(probeC);
            bool tetoCfg = EscreverCampo(probeC, "_navTentativasMax",
                Configurar(cfgC, "Geral", "NavegarTentativasMax", 4));
            _alvoAPartirDaChamada = -1; _chamadasDaPorta = 0; _invocacoesDaPorta = 0;
            EscreverCampo(probeC, "_fase", fNavegacao);
            int quadrosC = 0, faseFinalC = fNavegacao;
            while (quadrosC < teto + 5)
            {
                var erroC = Invocar(probeC, passo);
                quadrosC++;
                faseFinalC = Convert.ToInt32(LerCampo(probeC, "_fase"));
                if (erroC != null || faseFinalC != fNavegacao) break;
            }
            Console.WriteLine("   (C) teto pelo .cfg (4): campo gravado=" + tetoCfg
                              + " quadros=" + quadrosC + " fase final=" + faseFinalC);
            Checa("(C) com teto=4 no .cfg, o DRIVER esgota em 4 quadros", tetoCfg && quadrosC == 4,
                  "campo gravado=" + tetoCfg + " quadros=" + quadrosC + " (esperado 4)");

            NaoExercitado("navegacao clicando um botao REAL do jogo (onClick do Button da engine)",
                "exige o jogo aberto; aqui o alvo e servido pela porta injetavel — o caminho de engine "
                + "(Recursos<Button>() + botao.onClick.Invoke()) nao roda offline");
            NaoExercitado("o TETO lido de um .cfg REAL em disco",
                "o .cfg do probe nasce no perfil do dono (proibido nesta rodada); a ConfigEntry aqui e "
                + "criada pelo MESMO `Bind` que o Awake usa, em memoria — a leitura do ARQUIVO nao e exercitada");
            NaoExercitado("o corpo de `PassoLeitura()` (a fase de LEITURA) rodando offline",
                "MEDIDO nesta rodada: qualquer metodo do probe que CHAME uma funcao de engine morre no "
                + "pre-carregamento do CLR fora do jogo com `SecurityException: ECall methods must be "
                + "packaged into a system module` (a engine so e 'system module' dentro do proprio jogo). "
                + "Por isso a parte3 dirige o `Passo()` a partir de F_NAVEGACAO (engine-free) e exercita o "
                + "ROTEIRO da leitura pelo passo nomeado `FaseDepoisDaLeitura`, com o IL provando que e ELE "
                + "que `PassoLeitura` chama. O trecho `PassoLeitura -> FaseDepoisDaLeitura -> F_NAVEGACAO` "
                + "executado de ponta a ponta SO no jogo (KIT-14 re-executa depois deste cartao)");
        }

        // ------------------------------------------------------------ parte 4 (KIT-14G)

        private static int _p4Chamada;
        private static int _p4Invocacoes;
        private static string _p4Ultimo;

        /// <summary>KIT-14G — cenario ROTEIRIZADO: cada QUADRO e uma tela diferente, como no jogo
        /// real. 1) menu com 'Play'; 2) tela de criacao com 'Roguelike'; 3) HUD da run, onde o alvo
        /// do RSTV existe SEM ROTULO (so o NOME do objeto — e o caso real: `RunButton.cs` desliga o
        /// texto). O botao 'Continue' esta ATIVO em TODOS os quadros: o roteiro tem de ESCOLHER o
        /// estagio, nao pegar o primeiro ativo.</summary>
        private static List<(string rotulo, bool ativo, Action invocar)> PortaRoteiro()
        {
            int chamada = _p4Chamada++;
            var lista = new List<(string, bool, Action)>();
            if (chamada == 0) lista.Add(("Play", true, () => { _p4Invocacoes++; _p4Ultimo = "Play"; }));
            else if (chamada == 1) lista.Add(("Roguelike", true, () => { _p4Invocacoes++; _p4Ultimo = "Roguelike"; }));
            else lista.Add(("RstvRunSkillTreeButton", true, () => { _p4Invocacoes++; _p4Ultimo = "RstvRunSkillTreeButton"; }));
            lista.Add(("Continue", true, () => { }));
            return lista;
        }

        private static void Parte4()
        {
            Console.WriteLine("-- parte4 (KIT-14G): roteiro em ESTAGIOS, alvo por NOME, recoleta pos-navegacao e consumidor do recorder --");
            Assembly asmProbe;
            try { asmProbe = Carregar(Path.Combine(_probeBin, "AUT4Probe.dll")); }
            catch (Exception e) { Checa("AUT4Probe.dll carregou", false, e.Message); return; }
            var tProbe = asmProbe.GetType("Aut4Probe.Aut4ProbePlugin");
            if (tProbe == null) { Checa("tipo Aut4ProbePlugin", false, "nao encontrado"); return; }

            var passo = Metodo(tProbe, "Passo", 0);
            var campoPorta = Campo(tProbe, "PortaDeBotoes", estatico: true);
            Checa("(4) o PRODUTO expoe o passo por quadro e a porta de botoes",
                  passo != null && campoPorta != null,
                  "passo=" + (passo != null) + " porta=" + (campoPorta != null));
            if (passo == null || campoPorta == null) return;
            campoPorta.SetValue(null, (Func<List<(string, bool, Action)>>)PortaRoteiro);

            int fNavegacao = LerConst(tProbe, "F_NAVEGACAO", -1);
            int fPrint1 = LerConst(tProbe, "F_PRINT1", -2);
            string dir = Path.Combine(_dirTrabalho, "probe-roteiro");
            Directory.CreateDirectory(dir);
            object probe = MontarProbe(tProbe, "kit14g-roteiro", dir);
            var fCfg = Campo(tProbe, "<Config>k__BackingField");
            var cfg = fCfg == null ? null : fCfg.GetValue(probe);

            // O ROTEIRO entra pelo CAMPO que o `Awake` monta a partir da opcao `NavegarRota`
            // (o parse do `.cfg` so roda no Awake, que nao pode ser chamado fora do jogo).
            bool rotaGravada = EscreverCampo(probe, "_rota", new List<string> { "Play", "Roguelike" });
            EscreverCampo(probe, "_botoesVistos", new Dictionary<string, int>());
            EscreverCampo(probe, "_navAlvoNome",
                Configurar(cfg, "Geral", "NavegarAlvoNome", "RstvRunSkillTreeButton"));
            Checa("(4) o roteiro do .cfg e representado na lista de estagios do produto", rotaGravada,
                  "nao consegui gravar o campo `_rota` no binario exercitado");
            if (!rotaGravada) return;

            EscreverCampo(probe, "_fase", fNavegacao);
            int quadros = 0, faseFinal = fNavegacao;
            Exception erro = null;
            while (quadros < 10)
            {
                erro = Invocar(probe, passo);
                quadros++;
                faseFinal = Convert.ToInt32(LerCampo(probe, "_fase"));
                if (erro != null || faseFinal != fNavegacao) break;
            }
            Console.WriteLine("   (4) quadros=" + quadros + " fase final=" + faseFinal
                              + " invocacoes=" + _p4Invocacoes + " ultimo=" + _p4Ultimo);

            Checa("(4) o roteiro clicou UM estagio por tela e o ALVO por ultimo (botao sem rotulo, casado pelo nome)",
                  _p4Invocacoes == 3 && _p4Ultimo == "RstvRunSkillTreeButton",
                  "invocacoes=" + _p4Invocacoes + " ultimo=" + _p4Ultimo);
            Checa("(4) os 2 estagios do roteiro foram consumidos ANTES do alvo",
                  Convert.ToInt32(LerCampo(probe, "_rotaEtapa")) == 2,
                  "_rotaEtapa=" + LerCampo(probe, "_rotaEtapa"));
            Checa("(4) o roteiro NAO pegou o botao 'Continue' (escolha por estagio, nao o primeiro ativo)",
                  _p4Ultimo != "Continue" && _p4Invocacoes == 3, "ultimo=" + _p4Ultimo);
            Checa("(4) a navegacao terminou e o driver SAIU para o print", faseFinal == fPrint1,
                  "fase final=" + faseFinal + " (esperada F_PRINT1=" + fPrint1 + ")");
            Checa("(4) sem excecao no driver por quadro", erro == null,
                  erro == null ? null : erro.GetType().Name + ": " + erro.Message);

            var passos = LerCampo(probe, "_passos") as IDictionary;
            var resumo = EntradaResumo(passos != null && passos.Contains("navegacao") ? passos["navegacao"] as IList : null);
            Checa("(4) o resumo declara o alvo invocado e os estagios do roteiro gastos",
                  resumo != null && Texto(resumo, "estado") == "invocado" && Texto(resumo, "motivo").Contains("estagio"),
                  resumo == null ? "sem resumo" : "estado=" + Texto(resumo, "estado") + " motivo=" + Texto(resumo, "motivo"));

            var res = LerCampo(probe, "_res") as IDictionary;
            var mapa = res != null && res.Contains("botoes_vistos") ? res["botoes_vistos"] as IDictionary : null;
            Checa("(4) o MAPA de botoes vistos e gravado (e o insumo do roteiro de uma rodada real)",
                  mapa != null && mapa.Contains("Play") && mapa.Contains("Roguelike")
                  && mapa.Contains("RstvRunSkillTreeButton"),
                  "mapa=" + (mapa == null ? "(ausente)"
                      : string.Join(",", mapa.Keys.Cast<object>().Select(Convert.ToString).ToArray())));

            // ---- RECOLETA DEPOIS DA NAVEGACAO: o metodo chama engine (ECall) e nao roda offline,
            // entao a prova executavel aqui e o IL de quem O CHAMA + o rastro deixado pela
            // tentativa no ponto certo do roteiro (depois da navegacao, antes do print).
            var passoNav = Metodo(tProbe, "PassoNavegacao", 0);
            var recoletar = Metodo(tProbe, "Recoletar", 0);
            Checa("(4) `PassoNavegacao` RELE os objetos depois de navegar (chama `Recoletar` no IL)",
                  recoletar != null && passoNav != null && ChamaMetodo(passoNav, recoletar),
                  "metodo Recoletar=" + (recoletar != null));
            Checa("(4) o produto TENTOU a recoleta depois da navegacao (offline ela morre no ECall da engine e fica declarada)",
                  passos != null && passos.Contains("recoleta"),
                  "sem rastro de recoleta em `_passos`");

            // ---- CONSUMIDOR DO RECORDER (item 1 do escopo do KIT-14G).
            var lerRecorder = Metodo(tProbe, "LerRecorder", 0);
            Checa("(4) o produto tem consumidor do recorder (`LerRecorder`, por reflexao, sem depender do Core)",
                  lerRecorder != null, "metodo 'LerRecorder' ausente no binario exercitado");
            if (lerRecorder != null)
            {
                Exception e2 = Invocar(probe, lerRecorder);
                var rec = res != null && res.Contains("recorder") ? res["recorder"] as IDictionary : null;
                Checa("(4) sem o Core carregado, o consumidor DECLARA a ausencia (nunca uma contagem 0 inventada)",
                      e2 == null && rec != null && Texto(rec, "status") == "AUSENTE" && !string.IsNullOrEmpty(Texto(rec, "motivo")),
                      "erro=" + (e2 == null ? "nao" : e2.GetType().Name)
                      + " status=" + (rec == null ? "(sem campo recorder)" : Texto(rec, "status")));
            }
            var mCaminho = Metodo(tProbe, "CaminhoRecorder", 0);
            Exception e3 = null;
            object caminho = mCaminho == null ? null : InvocarRetorno(probe, mCaminho, out e3);
            Checa("(4) o artefato do recorder tem caminho declarado (`recorder.json` ao lado do JSON do probe)",
                  e3 == null && caminho != null && Convert.ToString(caminho).EndsWith("recorder.json"),
                  "caminho=" + caminho);

            NaoExercitado("ler `ResultadoFinal()` de um Core REAL com evento contado no jogo",
                "exige o jogo aberto com a trilha passiva ligada (`Modo/habilitado=true` + "
                + "`Modo/passivoHabilitado=true`); aqui o que se prova e o CONSUMIDOR e a declaracao "
                + "de ausencia — a contagem real so sai de uma sessao de jogo");
            NaoExercitado("o roteiro com os ROTULOS REAIS das telas do Stolen Realm",
                "os rotulos saem do campo `botoes_vistos` de uma rodada de jogo (o menu tem 10 botoes); "
                + "aqui as telas sao servidas pela porta injetavel — roteiro adivinhado nao seria prova");
        }

        /// <summary>Descreve (best effort) um IL simples: ldsfld/stsfld/call/ret com o token resolvido.</summary>
        private static List<string> DescreveIL(Module modulo, byte[] il)
        {
            var saida = new List<string>();
            int i = 0;
            while (i < il.Length)
            {
                byte op = il[i];
                switch (op)
                {
                    case 0x7E: // ldsfld
                    case 0x80: // stsfld
                        {
                            int token = BitConverter.ToInt32(il, i + 1);
                            string nome;
                            try { nome = modulo.ResolveField(token).Name; } catch { nome = "token#" + token; }
                            saida.Add((op == 0x7E ? "ldsfld " : "stsfld ") + nome);
                            i += 5;
                            break;
                        }
                    case 0x28: // call
                        {
                            int token = BitConverter.ToInt32(il, i + 1);
                            string nome;
                            try { var mb = modulo.ResolveMethod(token); nome = mb.DeclaringType.Name + "." + mb.Name; }
                            catch { nome = "token#" + token; }
                            saida.Add("call " + nome);
                            i += 5;
                            break;
                        }
                    case 0x2A: saida.Add("ret"); i++; break;
                    case 0x02: saida.Add("ldarg.0"); i++; break;
                    case 0x16: saida.Add("ldc.i4.0"); i++; break;
                    default: saida.Add("op#0x" + op.ToString("x2")); i++; break;
                }
            }
            return saida;
        }

        private static IDictionary EntradaResumo(IList lista)
        {
            if (lista == null) return null;
            foreach (var e in lista)
            {
                var d = e as IDictionary;
                if (d != null && d.Contains("estagio") && Convert.ToString(d["estagio"]) == "resumo") return d;
            }
            return null;
        }

        /// <summary>Primeira linha do stack (quem estourou) — ajuda a separar artefato do
        /// harness de defeito do produto quando um Passo explode offline.</summary>
        private static string Onde(Exception e)
        {
            var st = e == null ? null : e.StackTrace;
            if (string.IsNullOrEmpty(st)) return "(sem stack)";
            var linhas = st.Split('\n');
            return linhas.Length > 0 ? linhas[0].Trim() : "(sem stack)";
        }

        /// <summary>Existe uma chamada (call/callvirt) de `quem` para `alvo` no IL? Leitura
        /// DIRETA do binario exercitado: e o elo que nao pode ser executado offline
        /// (a fase de leitura chama engine), mas que nem por isso fica sem prova.</summary>
        private static bool ChamaMetodo(MethodInfo quem, MethodInfo alvo)
        {
            try
            {
                var corpo = quem == null ? null : quem.GetMethodBody();
                var il = corpo == null ? null : corpo.GetILAsByteArray();
                if (il == null || alvo == null) return false;
                int token = alvo.MetadataToken;
                for (int i = 0; i + 4 < il.Length; i++)
                {
                    if (il[i] != 0x28 && il[i] != 0x6F) continue;     // call / callvirt
                    if (BitConverter.ToInt32(il, i + 1) == token) return true;
                }
            }
            catch { }
            return false;
        }

        /// <summary>Despeja os passos ja gravados pelo produto: quando um `Passo` estoura
        /// offline, e o que diz ATE ONDE o produto chegou antes do artefato.</summary>
        private static void DumpPassos(object probe)
        {
            var p = LerCampo(probe, "_passos") as IDictionary;
            Console.WriteLine("   _passos ate a falha: " + (p == null ? "(null)" : p.Count + " entradas"));
            if (p == null) return;
            foreach (var k in p.Keys) Console.WriteLine("     _passos[" + k + "]=" + Texto(p, Convert.ToString(k)));
            var m = LerCampo(probe, "_marcos") as IEnumerable;
            int n = 0;
            if (m != null) foreach (var l in m) { if (n++ < 5) Console.WriteLine("     marco: " + l); }
        }

        private static string Texto(IDictionary d, string chave)
            => d != null && d.Contains(chave) ? Convert.ToString(d[chave], CultureInfo.InvariantCulture) : "(ausente)";

        /// <summary>Inteiro de um campo do JSON, ou `int.MinValue` quando ausente (nunca
        /// estoura: chave faltando e FALHA da verificacao, nao crash do harness).</summary>
        private static int Num(IDictionary d, string chave)
        {
            if (d == null || !d.Contains(chave) || d[chave] == null) return int.MinValue;
            try { return Convert.ToInt32(d[chave], CultureInfo.InvariantCulture); }
            catch { return int.MinValue; }
        }
    }
}
