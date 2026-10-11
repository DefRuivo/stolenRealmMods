using System;
using System.Collections.Generic;
using KIT04Core;

namespace Gumatos.KitCoreBridge
{
    public static class CorePluginBinding
    {
        // Host must call after Core initialization, on the game's main thread.
        // Permission is supplied by trusted host code, never by a scenario/package.
        public static CoreEventsExtension Create(CorePlugin core, Func<bool> hostObservationAuthorized)
        {
            if (ReferenceEquals(core, null)) throw new ArgumentNullException(nameof(core));
            if (hostObservationAuthorized == null) throw new ArgumentNullException(nameof(hostObservationAuthorized));
            return new CoreEventsExtension(new Facade(core), () => hostObservationAuthorized() && core.EstaHabilitado());
        }
        private sealed class Facade : ICoreEvento
        {
            private readonly CorePlugin core;
            internal Facade(CorePlugin core) { this.core = core; }
            public void RegistrarEvento(string tipo, string detalhe, Dictionary<string, object>? dados = null) => core.RegistrarEvento(tipo, detalhe, dados);
            public List<Dictionary<string, object>> ObterEventos() => core.ObterEventos();
            public void LimparEventos() => throw new NotSupportedException("KIT13 nao limpa auditoria do Core");
        }
    }
}
