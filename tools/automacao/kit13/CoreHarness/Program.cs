using System;
using System.Collections.Generic;
using KIT04Core;
using Gumatos.KitSdk.V1;
using Gumatos.KitCoreBridge;

bool enabled = false;
var service = new Events();
using var registry = new RegistryV1();
using var lease = registry.Register("core.events", RegistryV1.ApiVersion, new CoreEventsExtension(service, () => enabled));
var sample = new EventV1("offline-run661", 10, "observed", "ignored");
registry.Publish(sample);
if (service.Items.Count != 0 || registry.Read("core.events", "events.count").Status != "NAO_EXERCITADO") return 1;
enabled = true;
registry.Publish(sample);
if (service.Items.Count != 1 || registry.Read("core.events", "events.count").Value != "1") return 1;
if (registry.Validate("core.events", "events.count", registry.Read("core.events", "events.count"), "1").Status != "PASSOU") return 1;
Console.WriteLine("CoreBridge PASSOU: disabled=0 enabled=1; ICoreEvento fake; game NAO_EXERCITADO");
return 0;

sealed class Events : ICoreEvento
{
    public List<Dictionary<string, object>> Items { get; } = new();
    public void RegistrarEvento(string tipo, string detalhe, Dictionary<string, object>? dados = null) => Items.Add(Json.Campos("tipo", tipo, "detalhe", detalhe, "dados", dados!));
    public List<Dictionary<string, object>> ObterEventos() => new(Items);
    public void LimparEventos() => Items.Clear();
}
