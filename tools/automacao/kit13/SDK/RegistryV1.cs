using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace Gumatos.KitSdk.V1
{
    public sealed class EventV1
    {
        public string Session { get; }
        public long Frame { get; }
        public string Kind { get; }
        public string Data { get; }
        public EventV1(string session, long frame, string kind, string data)
        {
            if (string.IsNullOrWhiteSpace(session) || session.Length > 128 || frame < 0 ||
                string.IsNullOrWhiteSpace(kind) || kind.Length > 128 || data == null || data.Length > 4096)
                throw new ArgumentException("evento v1 invalido");
            Session = session; Frame = frame; Kind = kind; Data = data;
        }
    }

    public sealed class ReadingV1
    {
        public string Status { get; }
        public string Value { get; }
        public ReadingV1(string status, string value = "")
        {
            if (!(status == "OBSERVADO" || status == "AUSENTE" || status == "NAO_EXERCITADO" || status == "FALHOU_FECHADO") ||
                value == null || value.Length > 4096) throw new ArgumentException("leitura v1 invalida");
            Status = status; Value = value;
        }
    }

    public sealed class VerdictV1
    {
        public string Status { get; }
        public string Reason { get; }
        public VerdictV1(string status, string reason = "")
        {
            if (!(status == "PASSOU" || status == "FALHOU" || status == "NAO_EXERCITADO" || status == "FALHOU_FECHADO") ||
                reason == null || reason.Length > 512) throw new ArgumentException("veredito v1 invalido");
            Status = status; Reason = reason;
        }
    }

    // Code extensions are TRUSTED host code, not a security sandbox.
    // No assembly loading, script execution, authorization or Unity dependency here.
    public interface IExtensionV1
    {
        void OnEvent(EventV1 value);
        ReadingV1 Read(string key);
        VerdictV1 Validate(string key, ReadingV1 observed, string expected);
    }

    public sealed class RegistryV1 : IDisposable
    {
        public const string ApiVersion = "1.0.0";
        private readonly object gate = new object();
        private readonly Dictionary<string, Entry> entries = new Dictionary<string, Entry>();
        private readonly Queue<string> diagnostics = new Queue<string>();
        private bool disposed;
        private bool publishing;
        private sealed class Entry
        {
            internal readonly IExtensionV1 Extension;
            internal Entry(IExtensionV1 extension) { Extension = extension; }
        }
        private sealed class Lease : IDisposable
        {
            private readonly RegistryV1 owner;
            private readonly string id;
            private readonly Entry entry;
            internal Lease(RegistryV1 owner, string id, Entry entry)
            { this.owner = owner; this.id = id; this.entry = entry; }
            public void Dispose() { owner.Remove(id, entry); }
        }
        private void Live() { if (disposed) throw new ObjectDisposedException(nameof(RegistryV1)); }
        private void Diagnostic(string id, string operation, Exception error)
        {
            if (diagnostics.Count == 64) diagnostics.Dequeue();
            // Exception messages may contain secrets: retain only bounded type, not message/stack.
            diagnostics.Enqueue(id + ":" + operation + ":" + error.GetType().Name);
        }
        public string[] Diagnostics() { lock (gate) { return diagnostics.ToArray(); } }
        public int Count { get { lock (gate) { return entries.Count; } } }
        public IDisposable Register(string id, string apiVersion, IExtensionV1 extension)
        {
            lock (gate)
            {
                Live();
                if (apiVersion != ApiVersion) throw new NotSupportedException("API_INCOMPATIVEL: esperado " + ApiVersion);
                if (id == null || !Regex.IsMatch(id, @"\A[a-z][a-z0-9.-]{0,63}\z")) throw new ArgumentException("id invalido");
                if (extension == null) throw new ArgumentNullException(nameof(extension));
                if (entries.ContainsKey(id)) throw new InvalidOperationException("EXTENSAO_DUPLICADA");
                if (entries.Count >= 64) throw new InvalidOperationException("LIMITE_EXTENSOES");
                var entry = new Entry(extension); entries.Add(id, entry);
                return new Lease(this, id, entry);
            }
        }
        private void Remove(string id, Entry expected)
        {
            lock (gate)
            {
                if (entries.TryGetValue(id, out var actual) && ReferenceEquals(actual, expected)) entries.Remove(id);
            }
        }
        public void Publish(EventV1 value)
        {
            lock (gate)
            {
                Live();
                if (value == null) throw new ArgumentNullException(nameof(value));
                if (publishing) throw new InvalidOperationException("EVENTO_REENTRANTE");
                publishing = true;
                try
                {
                    foreach (var pair in entries.ToArray())
                    {
                        if (!entries.TryGetValue(pair.Key, out var current) || !ReferenceEquals(current, pair.Value)) continue;
                        try { current.Extension.OnEvent(value); }
                        catch (Exception error) { Diagnostic(pair.Key, "evento", error); }
                    }
                }
                finally { publishing = false; }
            }
        }
        public ReadingV1 Read(string id, string key)
        {
            lock (gate)
            {
                Live();
                if (!entries.TryGetValue(id, out var entry)) return new ReadingV1("AUSENTE");
                try { return entry.Extension.Read(key) ?? throw new InvalidOperationException("leitura null"); }
                catch (Exception error) { Diagnostic(id, "leitura", error); return new ReadingV1("FALHOU_FECHADO"); }
            }
        }
        public VerdictV1 Validate(string id, string key, ReadingV1 observed, string expected)
        {
            lock (gate)
            {
                Live();
                if (observed == null || observed.Status != "OBSERVADO") return new VerdictV1("NAO_EXERCITADO", "leitura nao observada");
                if (!entries.TryGetValue(id, out var entry)) return new VerdictV1("NAO_EXERCITADO", "extensao ausente");
                try { return entry.Extension.Validate(key, observed, expected) ?? throw new InvalidOperationException("veredito null"); }
                catch (Exception error) { Diagnostic(id, "validacao", error); return new VerdictV1("FALHOU_FECHADO"); }
            }
        }
        // Monitor serializes callbacks: once Dispose returns, no old callback is in flight.
        // Callback may unregister itself. Slow/deadlocking trusted code is NOT isolated.
        public void Dispose() { lock (gate) { disposed = true; entries.Clear(); } }
    }
}
