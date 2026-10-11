using System;
using System.Globalization;
using Gumatos.KitSdk.V1;
using Gumatos.KitExampleMod;

namespace Gumatos.KitExampleAdapter
{
    // Instantiate ONLY from an explicitly authorized host; mod never instantiates this.
    public sealed class CounterAdapter : IExtensionV1, IDisposable
    {
        private readonly CounterState state;
        private readonly RegistryV1 registry;
        private readonly IDisposable lease;
        private readonly string session;
        private bool disposed;
        public int Events { get; private set; }
        public CounterAdapter(CounterState state, RegistryV1 registry, string session)
        {
            this.state = state ?? throw new ArgumentNullException(nameof(state));
            this.registry = registry ?? throw new ArgumentNullException(nameof(registry));
            this.session = session;
            // Validate before registration/subscription, so failure leaves no orphan registration.
            _ = new EventV1(session, 0, "counter.changed", "");
            lease = registry.Register("example.counter", RegistryV1.ApiVersion, this);
            state.Changed += Changed;
        }
        private void Changed(int value)
        {
            if (!disposed) registry.Publish(new EventV1(session, value, "counter.changed", value.ToString(CultureInfo.InvariantCulture)));
        }
        public void OnEvent(EventV1 value) { if (value.Session == session && value.Kind == "counter.changed") Events++; }
        public ReadingV1 Read(string key) => key == "count" ? new ReadingV1("OBSERVADO", state.Count.ToString(CultureInfo.InvariantCulture)) : new ReadingV1("AUSENTE");
        public VerdictV1 Validate(string key, ReadingV1 observed, string expected) => key != "count" ? new VerdictV1("NAO_EXERCITADO") :
            new VerdictV1(observed.Value == expected ? "PASSOU" : "FALHOU", "comparacao exata com esperado externo");
        public void Dispose()
        {
            disposed = true;
            state.Changed -= Changed;
            lease.Dispose();
        }
    }
}
