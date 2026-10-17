// SYNTHETIC data, actual production core, real HarmonyX/MonoMod on desktop CLR.
// No game assemblies are loaded and no game methods are patched here.
using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
using BetterPortuguese.Core;
using HarmonyLib;
public static class HarmonyCoreProbe
{
    static readonly List<string> order = new List<string>();
    static bool corrected = true;
    static int passed;
    static List<Entry> baseline;
    static Overlay<Entry> engine;
    const string BP="bp.offline", BT="bt.offline", BF="bf.offline";
    static Entry Clone(Entry e) => new Entry(Entry.Fields.ToDictionary(f=>f,f=>e[f]));
    [MethodImpl(MethodImplOptions.NoInlining)] static List<Entry> Query(string original) => baseline;
    static void Bp(string original, ref List<Entry> __result)
    { order.Add("BP"); __result=engine.Resolve(original,true,true,new Settings(variant:corrected?Conjunto.Corrigido:Conjunto.Original),__result); }
    static void Bt(ref List<Entry> __result) { order.Add("BT"); }
    static void Bf(ref List<Entry> __result) { order.Add("BF"); }
    static void Unknown(ref List<Entry> __result) { __result=new List<Entry>{Clone(baseline[0]),Clone(baseline[0])}; }
    static void Mark(string name, bool ok) { if(!ok) throw new Exception(name); passed++;Console.WriteLine("PASS "+name); }
    static MethodInfo M(string name) => typeof(HarmonyCoreProbe).GetMethod(name,BindingFlags.Static|BindingFlags.NonPublic);
    static HarmonyMethod Patch(string name, string[] after) => new HarmonyMethod(M(name)){after=after};
    static void Run(bool reverse)
    {
        var bp=new Harmony(BP);var bt=new Harmony(BT);var bf=new Harmony(BF);var target=M("Query");
        try {
            if(reverse){bp.Patch(target,postfix:Patch("Bp",new[]{BT,BF}));bt.Patch(target,postfix:Patch("Bt",Array.Empty<string>()));bf.Patch(target,postfix:Patch("Bf",Array.Empty<string>()));}
            else{bf.Patch(target,postfix:Patch("Bf",Array.Empty<string>()));bt.Patch(target,postfix:Patch("Bt",Array.Empty<string>()));bp.Patch(target,postfix:Patch("Bp",new[]{BT,BF}));}
            order.Clear();corrected=true;var result=Query("key");Mark("execute production overlay corrected order "+reverse,result[0].Value=="corrected"&&order.Count==3&&order.Last()=="BP");
            var info=Harmony.GetPatchInfo(target);Mark("owners once "+reverse,info.Postfixes.Count(x=>x.owner==BP)==1&&info.Postfixes.Single(x=>x.owner==BP).after.SequenceEqual(new[]{BT,BF}));
            corrected=false;Mark("Original output reference "+reverse,ReferenceEquals(Query("key"),baseline));corrected=true;
            Mark("asset entry/list unchanged "+reverse,baseline.Count==1 && baseline[0].Value=="baseline");
        } finally { bp.UnpatchSelf();bt.UnpatchSelf();bf.UnpatchSelf(); }
    }
    public static int Main(string[] args)
    {
        try {
            string root=AppDomain.CurrentDomain.BaseDirectory;
            var catalog=Catalog.Parse(File.ReadAllText(Path.Combine(root,"fixture.original.json")),File.ReadAllText(Path.Combine(root,"fixture.corrigido.json")),File.ReadAllText(Path.Combine(root,"fixture.diff.json")));
            baseline=catalog.Original.Records["key"].Entries.Select(Clone).ToList();
            engine=new Overlay<Entry>(catalog,(a,b)=>a.Same(b),Clone,new OnceLog(s=>Console.WriteLine("CONFLICT "+s)));
            Console.WriteLine("HOST "+Environment.Version+" Harmony "+typeof(Harmony).Assembly.FullName);
            Run(false);Run(true);
            var bp=new Harmony(BP);var unknown=new Harmony("unknown.offline");var target=M("Query");
            try { unknown.Patch(target,postfix:Patch("Unknown",Array.Empty<string>()));bp.Patch(target,postfix:Patch("Bp",new[]{"unknown.offline"}));var result=Query("key");Mark("unknown writer preserved",result.Count==2 && result.All(e=>e.Value=="baseline")); }
            finally { bp.UnpatchSelf();unknown.UnpatchSelf(); }
            try { bp.Patch(target,postfix:Patch("Bp",new[]{"owner.absent"}));Mark("missing owner allowed",Query("key")[0].Value=="corrected"); }
            finally { bp.UnpatchSelf(); }
            var bt=new Harmony(BT);
            try { bp.Patch(target,postfix:Patch("Bp",new[]{BT}));bt.Patch(target,postfix:Patch("Bt",new[]{BP}));order.Clear();Query("key");Mark("dependency cycle detected by pair (not guaranteed order)",order.Count==2 && Harmony.GetPatchInfo(target).Postfixes.All(x=>x.after.Length==1)); }
            finally { bp.UnpatchSelf();bt.UnpatchSelf(); }
            foreach (string key in new[]{"empty","absent"})
            {
                baseline=key=="absent"?null:new List<Entry>();
                var originalBaseline=baseline;
                try {
                    bp.Patch(target,postfix:Patch("Bp",Array.Empty<string>()));
                    corrected=true;var result=Query(key);
                    Mark("addEntry real Harmony " + key,result!=null&&result.Count==1&&result[0].Value=="added "+key&&!ReferenceEquals(result,baseline));
                    Mark("addEntry original list untouched " + key,ReferenceEquals(baseline,originalBaseline)&&(baseline==null||baseline.Count==0));
                    corrected=false;Mark("addEntry Original reference " + key,ReferenceEquals(Query(key),baseline));corrected=true;
                    baseline=new List<Entry>{Clone(result[0])};
                    Mark("addEntry populated unknown writer preserved " + key,ReferenceEquals(Query(key),baseline));
                } finally {bp.UnpatchSelf();}
            }
            Mark("all probe owners cleaned",Harmony.GetPatchInfo(target)==null||Harmony.GetPatchInfo(target).Postfixes.Count==0);
            Console.WriteLine("RESULT passed="+passed+" failed=0; no game target patched");return 0;
        }catch(Exception e){Console.WriteLine("FAIL "+e);return 1;}
    }
}
