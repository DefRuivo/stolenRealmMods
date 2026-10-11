using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;
using Gumatos.KitSdk.V1;

namespace Gumatos.KitApiBridge
{
    /// <summary>
    /// INT-R1-C2-I1 (D4/D5/D6/D8). Adaptador observacional RealmApi -> KitSdk.
    ///
    /// O QUE ELE E: traduz <see cref="HookNotification"/> (contrato do PRODUTOR, api/Core/Contracts.cs:69-77)
    /// em <see cref="EventV1"/> (contrato do CONSUMIDOR, SDK/RegistryV1.cs:8-21), empurrando pelo
    /// <see cref="RegistryV1"/>. Le por vocabulario FECHADO e nunca lanca (D8): o
    /// <c>Signal&lt;T&gt;.Publish</c> roda no thread do hook (Contracts.cs:79) e uma excecao do adaptador
    /// viraria log do produtor com a mensagem inteira, enquanto o kit guarda so o TIPO
    /// (RegistryV1.cs:79-84).
    ///
    /// O QUE ELE NAO E: nao descobre nada (nenhuma reflexao, nenhum arquivo, nenhuma config: D7 recebe
    /// tudo do host por parametro), nao instala hook, nao carrega assembly e nao chama API do Unity.
    /// </summary>
    public sealed class RealmHooksExtension : IExtensionV1, IDisposable
    {
        /// <summary>Par declarado do adaptador (F4): contrato do consumidor.</summary>
        public const string KitApi = "1.0.0";
        /// <summary>Par declarado do adaptador (F4): contrato do produtor.</summary>
        public const string ProducerVersion = "0.1.0";
        /// <summary>Id de registro; satisfaz [a-z][a-z0-9.-]{0,63} de RegistryV1.cs:93.</summary>
        public const string RegistryId = "realmapi.hooks";

        private const int TetoDeData = 4096;                 // EventV1 recusa data > 4096 (RegistryV1.cs:17)
        private const string MarcaDeTruncamento = "[...TRUNCADO]";
        private const int TetoDeDiagnostico = 64;            // espelha o teto do kit (RegistryV1.cs:81)
        private const int TetoDoTextoDeDiagnostico = 512;    // so o TIPO cabe; mensagem nunca vaza
        private const int TetoDoArgumento = 256;
        private const int MaxArgumentos = 8;

        private readonly RegistryV1 registry;
        private readonly Func<bool> producerActive;
        private readonly Action<string> diagnostic;
        private readonly string session;
        private readonly HashSet<string> catalogo;
        private readonly Dictionary<string, long> porHook = new Dictionary<string, long>(StringComparer.Ordinal);
        private readonly Queue<string> diagnostico = new Queue<string>();
        private readonly object diagnosticoGate = new object();
        private readonly object gate = new object();
        private IDisposable? assinatura;
        private IDisposable? lease;
        private long ordinal;
        private long total;
        private long desconhecidos;
        private bool disposed;

        internal RealmHooksExtension(RegistryV1 registry, Func<bool> producerActive, Action<string> diagnostic, string session)
        {
            this.registry = registry;
            this.producerActive = producerActive;
            this.diagnostic = diagnostic;
            this.session = session;
            catalogo = new HashSet<string>(StringComparer.Ordinal);
            // Catalogo do produtor (Contracts.cs:58-66): copiado no inicio; HookId novo do produtor
            // (0.1.x -> 0.2.0) cai em "hooks.unknown" e nunca vira veredito (D5/parte02 §2).
            foreach (var hook in Gumatos.RealmApi.HookCatalog.All) catalogo.Add(hook.Id);
        }

        /// <summary>Registra no kit e assina o sinal do produtor; falha de um lado desfaz o outro.</summary>
        internal void Ligar(Gumatos.RealmApi.Signal<Gumatos.RealmApi.HookNotification> observed, string kitApiDeclarado)
        {
            IDisposable? registro = null;
            IDisposable? assinado = null;
            try
            {
                registro = registry.Register(RegistryId, kitApiDeclarado, this);
                assinado = observed.Subscribe(notificacao => OnEvent(notificacao));
            }
            catch
            {
                try { assinado?.Dispose(); } catch { }
                try { registro?.Dispose(); } catch { }
                throw;
            }
            lock (gate) { lease = registro; assinatura = assinado; }
        }

        // ------------------------------------------------------------------ IExtensionV1

        /// <summary>
        /// Uma observacao do produtor por EventV1. D5: com produtor inativo (API ausente ja nem chega
        /// aqui; EnableHooks=false ou alvo divergente) NAO publica nada e NAO conta. D6: Session vem do
        /// host e Frame e o ordinal da observacao (proibido Frame=0 fixo).
        /// </summary>
        public void OnEvent(Gumatos.RealmApi.HookNotification notificacao)
        {
            try { Observar(notificacao); }
            catch (Exception erro) { Diagnostico("evento:" + erro.GetType().Name); }
        }

        /// <summary>
        /// Membros do IExtensionV1. O adaptador EMPURRA eventos para o kit: um <see cref="EventV1"/> que
        /// chega de volta e eco (o proprio kit chamando a extensao registrada) e nao pode recircular —
        /// se recirculasse, o guardao EVENTO_REENTRANTE do kit (RegistryV1.cs:114) seria a unica barreira.
        /// </summary>
        public void OnEvent(EventV1 value) { }

        private void Observar(Gumatos.RealmApi.HookNotification notificacao)
        {
            if (notificacao == null) throw new ArgumentNullException(nameof(notificacao));
            lock (gate) { if (disposed) return; }
            if (!Ativo()) return;
            EventV1 evento;
            lock (gate)
            {
                if (!catalogo.Contains(notificacao.HookId)) { desconhecidos++; return; }
                var quadro = ordinal++;
                total++;
                long visto;
                porHook.TryGetValue(notificacao.HookId, out visto);
                porHook[notificacao.HookId] = visto + 1;
                evento = new EventV1(session, quadro, notificacao.HookId, MontarResumo(notificacao, quadro));
            }
            Publicar(evento);
        }

        /// <summary>Publica FORA do lock do adaptador: o kit tem lock proprio e inverter a ordem trava.</summary>
        private void Publicar(EventV1 evento)
        {
            try { registry.Publish(evento); }
            catch (Exception erro) { Diagnostico("publicacao:" + erro.GetType().Name); }
        }

        /// <summary>Vocabulario fechado (parte02 §D4): qualquer outra chave e AUSENTE, nunca valor plausivel.</summary>
        public ReadingV1 Read(string key)
        {
            var conhecida = Vocabulario(key);
            if (!Ativo()) return new ReadingV1("NAO_EXERCITADO");
            if (key == "hooks.count") { lock (gate) return new ReadingV1("OBSERVADO", total.ToString(CultureInfo.InvariantCulture)); }
            if (key == "hooks.unknown") { lock (gate) return new ReadingV1("OBSERVADO", desconhecidos.ToString(CultureInfo.InvariantCulture)); }
            if (!conhecida) return new ReadingV1("AUSENTE");
            var hookId = key.Substring("hook.".Length, key.Length - "hook.".Length - ".count".Length);
            long visto;
            lock (gate) porHook.TryGetValue(hookId, out visto);
            return new ReadingV1("OBSERVADO", visto.ToString(CultureInfo.InvariantCulture));
        }

        public VerdictV1 Validate(string key, ReadingV1 observed, string expected)
        {
            if (!Ativo()) return new VerdictV1("NAO_EXERCITADO");
            if (observed == null || observed.Status != "OBSERVADO") return new VerdictV1("NAO_EXERCITADO");
            if (!Vocabulario(key)) return new VerdictV1("NAO_EXERCITADO");
            return new VerdictV1(observed.Value == expected ? "PASSOU" : "FALHOU", "comparacao exata com esperado externo");
        }

        private bool Vocabulario(string? key)
        {
            if (key == "hooks.count" || key == "hooks.unknown") return true;
            if (key == null || !key.StartsWith("hook.", StringComparison.Ordinal) || !key.EndsWith(".count", StringComparison.Ordinal)) return false;
            var hookId = key.Substring("hook.".Length, key.Length - "hook.".Length - ".count".Length);
            return catalogo.Contains(hookId);
        }

        // ------------------------------------------------------------------ D8: nunca lanca

        /// <summary>
        /// Gate do host (D5/D7). O <c>Func</c> e codigo do host e pode falhar (hoje ele le config do
        /// plugin, que toca BepInEx): falha conta como INATIVO e o TIPO vai para o canal de
        /// diagnostico — excecao do adaptador no logger do produtor esta proibida (D8).
        /// </summary>
        private bool Ativo()
        {
            try { return producerActive(); }
            catch (Exception erro) { Diagnostico("produtor:" + erro.GetType().Name); return false; }
        }

        /// <summary>So o TIPO entra; a mensagem pode conter segredo (mesma regra do kit). Limitado.</summary>
        private void Diagnostico(string texto)
        {
            var limitado = Limitar(texto, TetoDoTextoDeDiagnostico);
            lock (diagnosticoGate)
            {
                if (diagnostico.Count >= TetoDeDiagnostico) return;
                diagnostico.Enqueue(limitado);
            }
            try { diagnostic(limitado); } catch { }
        }

        // ------------------------------------------------------------------ resumo do evento (D6)

        private string MontarResumo(Gumatos.RealmApi.HookNotification notificacao, long quadro)
        {
            var texto = new StringBuilder();
            texto.Append("quadro=").Append(quadro.ToString(CultureInfo.InvariantCulture));
            texto.Append("|hook=").Append(notificacao.HookId);
            texto.Append("|alvo=").Append(notificacao.Instance == null ? "nulo" : notificacao.Instance.GetType().Name);
            texto.Append("|args=").Append(ArgumentosLegiveis(notificacao.Arguments));
            var resultado = notificacao.Result as string;
            texto.Append("|resultado=").Append(resultado ?? "nao-texto");
            return Limitar(texto.ToString(), TetoDeData);
        }

        /// <summary>
        /// Resumo LIMITADO: string vem literal (truncada), qualquer outro objeto vira so o nome do TIPO.
        /// Instance nao e serializada e argumentos em geral nao sao tocados: a lista e copia RASA
        /// (Contracts.cs:76), os objetos de dentro seguem vivos do Unity e chama-los aqui lancaria.
        /// </summary>
        private static string ArgumentosLegiveis(IReadOnlyList<object?> argumentos)
        {
            if (argumentos == null || argumentos.Count == 0) return "nenhum";
            var texto = new StringBuilder();
            var limite = argumentos.Count < MaxArgumentos ? argumentos.Count : MaxArgumentos;
            for (var i = 0; i < limite; i++)
            {
                if (i > 0) texto.Append(';');
                var valor = argumentos[i];
                if (valor == null) texto.Append("nulo");
                else if (valor is string literal) texto.Append(Limitar(literal, TetoDoArgumento));
                else texto.Append("tipo:").Append(valor.GetType().Name);
            }
            if (argumentos.Count > limite) texto.Append(";+").Append((argumentos.Count - limite).ToString(CultureInfo.InvariantCulture));
            return texto.ToString();
        }

        /// <summary>Truncamento COM MARCADOR: nada de corte silencioso, nada de estourar o EventV1.</summary>
        private static string Limitar(string texto, int teto)
        {
            if (texto.Length <= teto) return texto;
            if (teto <= MarcaDeTruncamento.Length) return texto.Substring(0, teto);
            return texto.Substring(0, teto - MarcaDeTruncamento.Length) + MarcaDeTruncamento;
        }

        // ------------------------------------------------------------------ ciclo de vida

        /// <summary>Idempotente: remove a assinatura e libera o lease; publicar depois nao faz nada.</summary>
        public void Dispose()
        {
            IDisposable? assinado, registro;
            lock (gate)
            {
                if (disposed) return;
                disposed = true;
                assinado = assinatura;
                registro = lease;
                assinatura = null;
                lease = null;
            }
            try { assinado?.Dispose(); } catch (Exception erro) { Diagnostico("assinatura:" + erro.GetType().Name); }
            try { registro?.Dispose(); } catch (Exception erro) { Diagnostico("lease:" + erro.GetType().Name); }
        }
    }
}
