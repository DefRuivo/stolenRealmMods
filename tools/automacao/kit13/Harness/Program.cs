using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Gumatos.KitSdk.V1;
using Gumatos.KitExampleMod;
using Gumatos.KitExampleAdapter;

static class Program
{
    static void Check(bool value) { if (!value) throw new Exception("ASSERTION"); }
    static void Throws<T>(Action action) where T : Exception
    { try { action(); } catch (T) { return; } throw new Exception("EXPECTED_" + typeof(T).Name); }
    static EventV1 Event() => new EventV1("offline-run661", 1, "test", "");
    sealed class Extension : IExtensionV1
    {
        public Action<EventV1> EventHandler = _ => { };
        public Func<string, ReadingV1> Reader = _ => new ReadingV1("OBSERVADO", "7");
        public Func<string, ReadingV1, string, VerdictV1> Validator = (_, value, expected) => new VerdictV1(value.Value == expected ? "PASSOU" : "FALHOU");
        public void OnEvent(EventV1 e) => EventHandler(e);
        public ReadingV1 Read(string key) => Reader(key);
        public VerdictV1 Validate(string key, ReadingV1 value, string expected) => Validator(key, value, expected);
    }
    static int Main(string[] args)
    {
        var tests = new Dictionary<string, Action>
        {
            ["version"] = () => { using var r = new RegistryV1(); Throws<NotSupportedException>(() => r.Register("one", "2.0.0", new Extension())); Check(r.Count == 0); },
            ["duplicate"] = () => { using var r = new RegistryV1(); using var a = r.Register("one", RegistryV1.ApiVersion, new Extension()); Throws<InvalidOperationException>(() => r.Register("one", RegistryV1.ApiVersion, new Extension())); },
            ["unregister"] = () => { using var r = new RegistryV1(); int n = 0; var a = r.Register("one", RegistryV1.ApiVersion, new Extension { EventHandler = _ => n++ }); r.Publish(Event()); a.Dispose(); a.Dispose(); r.Publish(Event()); Check(n == 1 && r.Read("one", "k").Status == "AUSENTE"); },
            ["replacement"] = () => { using var r = new RegistryV1(); var old = r.Register("one", RegistryV1.ApiVersion, new Extension()); old.Dispose(); using var fresh = r.Register("one", RegistryV1.ApiVersion, new Extension()); old.Dispose(); Check(r.Count == 1); },
            ["mid-publish"] = () => { using var r = new RegistryV1(); IDisposable? b = null; int calls = 0; using var a = r.Register("one", RegistryV1.ApiVersion, new Extension { EventHandler = _ => b!.Dispose() }); b = r.Register("two", RegistryV1.ApiVersion, new Extension { EventHandler = _ => calls++ }); r.Publish(Event()); b.Dispose(); Check(calls == 0); },
            ["event-isolation"] = () => { using var r = new RegistryV1(); int n = 0; using var a = r.Register("one", RegistryV1.ApiVersion, new Extension { EventHandler = _ => throw new Exception("DO_NOT_LOG_SECRET") }); using var b = r.Register("two", RegistryV1.ApiVersion, new Extension { EventHandler = _ => n++ }); r.Publish(Event()); Check(n == 1 && r.Diagnostics().Length == 1 && !r.Diagnostics()[0].Contains("DO_NOT_LOG_SECRET")); },
            ["reader-isolation"] = () => { using var r = new RegistryV1(); using var a = r.Register("one", RegistryV1.ApiVersion, new Extension { Reader = _ => throw new Exception() }); Check(r.Read("one", "k").Status == "FALHOU_FECHADO" && r.Diagnostics().Length == 1); },
            ["validator-isolation"] = () => { using var r = new RegistryV1(); using var a = r.Register("one", RegistryV1.ApiVersion, new Extension { Validator = (_, _, _) => throw new Exception() }); Check(r.Validate("one", "k", new ReadingV1("OBSERVADO", "7"), "7").Status == "FALHOU_FECHADO"); },
            ["absent"] = () => { using var r = new RegistryV1(); using var a = r.Register("one", RegistryV1.ApiVersion, new Extension()); Check(r.Validate("one", "k", new ReadingV1("AUSENTE"), "").Status == "NAO_EXERCITADO"); },
            ["reentrant"] = () => { using var r = new RegistryV1(); int n = 0; using var a = r.Register("one", RegistryV1.ApiVersion, new Extension { EventHandler = _ => { if (++n < 3) r.Publish(Event()); } }); r.Publish(Event()); Check(n == 1 && r.Diagnostics().Length == 1); },
            ["limit"] = () => { using var r = new RegistryV1(); for (int i = 0; i < 64; i++) r.Register("ext" + i, RegistryV1.ApiVersion, new Extension()); Throws<InvalidOperationException>(() => r.Register("last", RegistryV1.ApiVersion, new Extension())); },
            ["disposed"] = () => { var r = new RegistryV1(); r.Register("one", RegistryV1.ApiVersion, new Extension()); r.Dispose(); Throws<ObjectDisposedException>(() => r.Read("one", "k")); Check(r.Count == 0); },
            ["dto"] = () => { Throws<ArgumentException>(() => new ReadingV1("PASSOU")); Throws<ArgumentException>(() => new EventV1("s", -1, "k", "")); Throws<ArgumentException>(() => new VerdictV1("UNKNOWN")); },
            ["adapter"] = () => { var s = new CounterState(); using var r = new RegistryV1(); using (var a = new CounterAdapter(s, r, "offline-run661")) { s.Observe(); Check(a.Events == 1 && r.Read("example.counter", "count").Value == "1"); Check(r.Validate("example.counter", "count", r.Read("example.counter", "count"), "1").Status == "PASSOU"); Check(r.Validate("example.counter", "count", r.Read("example.counter", "count"), "2").Status == "FALHOU"); } s.Observe(); Check(s.Count == 2 && r.Count == 0); },
            ["mod-isolation"] = () => { var s = new CounterState(); int observed = 0; s.Changed += _ => throw new Exception(); s.Changed += n => observed = n; s.Observe(); Check(s.Count == 1 && observed == 1); },
            ["diagnostic-limit"] = () => { using var r = new RegistryV1(); using var a = r.Register("one", RegistryV1.ApiVersion, new Extension { EventHandler = _ => throw new Exception() }); for (int i = 0; i < 100; i++) r.Publish(Event()); Check(r.Diagnostics().Length == 64); },
            ["dispose-waits"] = () => {
                using var r = new RegistryV1(); using var entered = new ManualResetEventSlim(); using var release = new ManualResetEventSlim(); using var started = new ManualResetEventSlim();
                var lease = r.Register("one", RegistryV1.ApiVersion, new Extension { EventHandler = _ => { entered.Set(); if (!release.Wait(2000)) throw new Exception("test bound"); } });
                var pub = Task.Run(() => r.Publish(Event())); Check(entered.Wait(2000));
                var removal = Task.Run(() => { started.Set(); lease.Dispose(); });
                try { Check(started.Wait(2000)); Check(!removal.Wait(100)); } finally { release.Set(); }
                Check(Task.WaitAll(new[] { pub, removal }, 2000)); Check(r.Count == 0);
            }
        };
        int failures = 0, count = 0;
        foreach (var test in tests.Where(p => args.Length == 0 || p.Key == args[0]))
        {
            count++;
            try { test.Value(); Console.WriteLine("PASS|" + test.Key); }
            catch (Exception e) { failures++; Console.WriteLine("FAIL|" + test.Key + "|" + e.GetType().Name); }
        }
        if (count == 0) { Console.WriteLine("NAO_EXERCITADO: caso ausente"); return 2; }
        Console.WriteLine($"Ran {count} tests; failures={failures}; OFFLINE_ONLY");
        return failures == 0 ? 0 : 1;
    }
}
