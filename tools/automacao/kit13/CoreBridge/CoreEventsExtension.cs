using System;
using System.Globalization;
using KIT04Core;
using Gumatos.KitSdk.V1;

namespace Gumatos.KitCoreBridge
{
    // Optional bridge for the EXISTING ICoreEvento service, provided explicitly by the host.
    // It does not load plugins, authorize observation or assume CorePlugin.Awake has run.
    public sealed class CoreEventsExtension : IExtensionV1
    {
        private readonly ICoreEvento core;
        private readonly Func<bool> enabled;
        public CoreEventsExtension(ICoreEvento core, Func<bool> enabled)
        { this.core = core ?? throw new ArgumentNullException(nameof(core)); this.enabled = enabled ?? throw new ArgumentNullException(nameof(enabled)); }
        public void OnEvent(EventV1 value)
        {
            if (enabled()) core.RegistrarEvento(value.Kind, "KIT13 " + value.Session,
                Json.Campos("quadro", value.Frame, "origem", "kit13-sdk-v1"));
        }
        public ReadingV1 Read(string key)
        {
            if (!enabled()) return new ReadingV1("NAO_EXERCITADO");
            if (key != "events.count") return new ReadingV1("AUSENTE");
            return new ReadingV1("OBSERVADO", core.ObterEventos().Count.ToString(CultureInfo.InvariantCulture));
        }
        public VerdictV1 Validate(string key, ReadingV1 observed, string expected)
        {
            if (!enabled() || key != "events.count") return new VerdictV1("NAO_EXERCITADO");
            return new VerdictV1(observed.Value == expected ? "PASSOU" : "FALHOU");
        }
    }
}
