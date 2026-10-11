using System;
using Gumatos.KitExampleMod;

var state = new CounterState();
state.Observe(); state.Observe();
if (state.Count != 2) { Console.Error.WriteLine("STANDALONE FALHOU"); return 1; }
Console.WriteLine("STANDALONE PASSOU: count=2; kit absent; logic offline, game NAO_EXERCITADO");
return 0;
