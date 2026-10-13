using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Diagnostics;
using System.Threading.Tasks;
using BetterPortuguese.Core;
using BetterPortuguese.Runtime;
using HarmonyLib;
using Mono.Cecil;
using CoreEntry = BetterPortuguese.Core.Entry;
using Res = BetterPortuguese.Core.Resources;

internal static class Program
{
    private static int passed, failed;
    private static Catalog real, fixture;
    private static string original, corrected, diff;
    private static List<CoreEntry> game;
    private static Overlay<CoreEntry> engine;
    private static void Check(bool yes, string message = "assert") { if (!yes) throw new Exception(message); }
    private static void Reject(Action action)
    { try { action(); } catch (FormatException) { return; } throw new Exception("Negative control was ACCEPTED"); }
    private static void Test(string name, Action action)
    {
        try { action(); passed++; Console.WriteLine("PASS " + name); }
        catch (Exception e) { failed++; Console.WriteLine("FAIL " + name + " " + e); }
    }
    private static Dictionary<string, object> E(string value, string feminine = null, string masculine = "", string neutral = null) => new Dictionary<string, object> {
        ["Value"] = value, ["Key"] = "exact", ["TranslatorKey"] = null, ["Feminine"] = feminine, ["Masculine"] = masculine, ["Neutral"] = neutral, ["LanguageGender"] = 0, ["CanBeGendered"] = false, ["NeedsGenderInfo"] = false };
    private static CoreEntry Entry(string value) => new CoreEntry(JsonShape.Object(StrictJson.Parse(JsonSerializer.Serialize(E(value)))));
    private static CoreEntry Clone(CoreEntry e) => new CoreEntry(CoreEntry.Fields.ToDictionary(f => f, f => e[f]));
    private static void MakeFixture()
    {
        var source = new Dictionary<string, object> { ["taskId"]="t_12345678", ["artifactSha256"]=new string('a',64), ["resourcePath"]="synthetic", ["resourcePathId"]=1, ["resourceAssetSha256"]=new string('b',64), ["assemblySha256"]=new string('c',64), ["canonicalMemberSha256"]=new string('d',64) };
        var entry = E("Base [0] {STA=X} *0 <b>value</b>\n", "", "", "");
        var records = new[] {
            new Dictionary<string,object> { ["id"]="LANG-00001", ["key"]=" exact \n", ["presentInSource"]=true, ["entries"]=new[]{entry} },
            new Dictionary<string,object> { ["id"]="LANG-00002", ["key"]="absent", ["presentInSource"]=false, ["entries"]=null },
            new Dictionary<string,object> { ["id"]="LANG-00003", ["key"]="empty", ["presentInSource"]=true, ["entries"]=Array.Empty<object>() } };
        var root = new Dictionary<string,object> { ["schemaVersion"]=1, ["locale"]="pt-BR", ["variant"]="Original", ["source"]=source, ["records"]=records, ["manualRecords"]=Array.Empty<object>() };
        original = JsonSerializer.Serialize(root);
        string before = (string)entry["Value"], after = "Corrigido [0] {STA=X} *0 <b>value</b>\n";
        entry["Value"] = after; root["variant"] = "Corrigido"; corrected = JsonSerializer.Serialize(root);
        diff = JsonSerializer.Serialize(new[]{new Dictionary<string,object> { ["id"]="LANG-00001", ["key"]=" exact \n", ["entryIndex"]=0, ["field"]="Value", ["before"]=before, ["after"]=after, ["approvalTaskId"]="t_12345678" }});
        fixture = Catalog.Parse(original, corrected, diff);
        game = fixture.Original.Records[" exact \n"].Entries.Select(Clone).ToList();
        engine = new Overlay<CoreEntry>(fixture, (a,b)=>a.Same(b), Clone, new OnceLog(_=>{}));
    }
    private static List<CoreEntry> Resolve(List<CoreEntry> list = null, Settings settings = null, string key = " exact \n", bool req = true, bool eff = true)
        => engine.Resolve(key, req, eff, settings ?? new Settings(), list ?? game);
    private static void Metadata(string repo, string config)
    {
        using var gameDll = ModuleDefinition.ReadModule(Path.Combine(repo,"lib/Assembly-CSharp.dll"));
        var options = gameDll.Types.Single(t=>t.FullName=="OptionsManager");
        var method = options.Methods.Single(m=>m.Name=="GetLocalizationEntryList");
        Check(method.IsStatic && method.ReturnType.FullName=="System.Collections.Generic.List`1<LocalizationEntry>");
        Check(method.Parameters.Select(p=>p.ParameterType.FullName).SequenceEqual(new[]{"System.String","LanguageChoice","System.Boolean"}));
        Check(method.Parameters.Select(p=>p.Name).SequenceEqual(new[]{"original","languageChoice","fallbackToTranslatorKey"}));
        var localize=options.Methods.Single(m=>m.Name=="Localize" && m.Parameters.Count==3);
        var calls=localize.Body.Instructions.Where(i=>i.Operand is MethodReference).Select(i=>((MethodReference)i.Operand).Name).ToList();
        int highlighted=calls.IndexOf("GetStringWithProcessedHighlightedText"), attributes=calls.IndexOf("ApplyAttributeTextTags"), gendered=calls.IndexOf("GetGenderizedText"), feminine=calls.IndexOf("GetFeminine");
        Check(highlighted>=0 && attributes>highlighted && gendered>attributes && feminine>gendered,"Real IL preprocessing order");
        foreach(string getter in new[]{"GetLocalization","GetFeminine","GetMasculine","GetNeutral"})
            Check(options.Methods.Single(m=>m.Name==getter).Body.Instructions.Any(i=>i.Operand is MethodReference r && r.Name=="GetLocalizationEntryList"),"Real getter pipeline "+getter);
        Check(options.Properties.Single(p=>p.Name=="CurrentLanguage").GetMethod.IsStatic);
        Check(options.Methods.Any(m=>m.Name=="LocalizeUI" && m.IsStatic && m.Parameters.Count==1 && m.Parameters[0].ParameterType.FullName=="System.Boolean" && m.ReturnType.FullName=="System.Void"));
        Check(gameDll.Types.Single(t=>t.FullName=="GUIManager").Methods.Any(m=>m.Name=="Update" && !m.IsStatic && m.Parameters.Count==0 && m.ReturnType.FullName=="System.Void"));
        var enumType = gameDll.Types.Single(t=>t.FullName=="LanguageGender");
        Check(enumType.Fields.Where(f=>f.HasConstant).Select(f=>(int)f.Constant).SequenceEqual(Enumerable.Range(0,7)));
        var entryType = gameDll.Types.Single(t=>t.FullName=="LocalizationEntry");
        Check(CoreEntry.Fields.All(f=>entryType.Fields.Any(x=>x.Name==f && x.IsPublic)));
        using var plugin = ModuleDefinition.ReadModule(Path.Combine(repo,"BetterPortuguese/bin",config,"netstandard2.1/BetterPortuguese.dll"));
        Check(plugin.Assembly.Name.Version.ToString()=="0.1.0.0");
        var attribute = plugin.Types.Single(t=>t.FullName=="BetterPortuguese.Plugin").CustomAttributes.Single(a=>a.AttributeType.Name=="BepInPlugin");
        Check((string)attribute.ConstructorArguments[0].Value=="com.gumatos.betterportuguese" && (string)attribute.ConstructorArguments[2].Value=="0.1.0");
        Check(plugin.Resources.Count==ResourceHashes.Expected.Count);
        foreach (var pair in ResourceHashes.Expected)
        {
            var resource = (EmbeddedResource)plugin.Resources.Single(r=>r.Name=="BetterPortuguese.Data."+pair.Key);
            byte[] data = resource.GetResourceData();
            Check(Res.Sha256(data)==pair.Value && data.SequenceEqual(File.ReadAllBytes(Path.Combine(repo,"BetterPortuguese/Data",pair.Key))), pair.Key);
        }
        Console.WriteLine("EVIDENCE real API and DLL resources checked: " + config);
    }
    public static int Main(string[] args)
    {
        string repo=Path.GetFullPath(args.Length>0?args[0]:".");
        Test("load embedded immutable snapshots",()=>{real=Res.Load(typeof(Program).Assembly); Check(real.Original.Records.Count==9095 && real.Original.ManualCount==2 && real.Changed.Count==0);});
        Test("9090/8097/1286/5 lossless corpus",()=>{Check(real.Original.Records.Values.Count(r=>r.PresentInSource)==9090); Check(real.Original.Records.Values.Sum(r=>r.Entries?.Count??0)==8097); Check(real.Original.Records.Values.Count(r=>r.Entries?.Count==0)==1286); Check(real.Original.Records.Values.Count(r=>r.Entries==null)==5);});
        Test("empty mod registry",()=>Check(Res.LoadMods(typeof(Program).Assembly)==0));
        Test("embedded corruption fails SHA and preserves base",()=>{
            using var module=ModuleDefinition.ReadModule(Path.Combine(repo,"BetterPortuguese/bin/Release/netstandard2.1/BetterPortuguese.dll"));
            var old=(EmbeddedResource)module.Resources.Single(r=>r.Name=="BetterPortuguese.Data.pt-BR.original.json");
            var bytes=old.GetResourceData();bytes[0]=(byte)'!';
            module.Resources.Remove(old);module.Resources.Add(new EmbeddedResource(old.Name,old.Attributes,bytes));
            using var buffer=new MemoryStream();module.Write(buffer);
            var corrupt=Assembly.Load(buffer.ToArray());
            try{Res.Read(corrupt,"pt-BR.original.json");}catch(InvalidDataException){Check(real.Changed.Count==0);return;}
            throw new Exception("corrupted resource accepted");
        });
        Test("missing resource fails closed",()=>{try{Res.Read(typeof(string).Assembly,"pt-BR.original.json");}catch(InvalidDataException){return;}throw new Exception("missing resource accepted");});
        Test("approved synthetic fixture only",MakeFixture);
        Test("strict duplicate root",()=>Reject(()=>StrictJson.Parse("{\"a\":1,\"a\":2}")));
        Test("strict duplicate nested",()=>Reject(()=>StrictJson.Parse("{\"outer\":{\"a\":1,\"a\":2}}")));
        Test("duplicate decoded unicode key",()=>Reject(()=>StrictJson.Parse("{\"a\":1,\"\\u0061\":2}")));
        Test("invalid JSON syntax controls",()=>{foreach(var text in new[]{"[1,]","{\"a\":1,}","01","+1","NaN","1.","1e","null x","\"\\q\"","\"a\nb\"","\"\\uD800\""}) Reject(()=>StrictJson.Parse(text));});
        Test("UTF8 escapes null/empty/newline",()=>{var value=JsonShape.Array(StrictJson.Parse("[null,\"\",\"á\\n\\\"\\\\\",\"\\uD83D\\uDE00\"]")); Check(value[0]==null && (string)value[1]=="" && (string)value[2]=="á\n\"\\" && (string)value[3]=="😀");});
        Test("bad UTF8",()=>{try{Res.Decode(new byte[]{0xc3,0x28});}catch(System.Text.DecoderFallbackException){return;}throw new Exception("bad UTF8 accepted");});
        Test("duplicate record ID",()=>Reject(()=>Catalog.Parse(original.Replace("LANG-00002","LANG-00001"),corrected,diff)));
        Test("duplicate record key",()=>Reject(()=>Catalog.Parse(original.Replace("\"empty\"","\"absent\""),corrected,diff)));
        Test("identity source key changed",()=>Reject(()=>Catalog.Parse(original,corrected.Replace("\"empty\"","\"new\""),diff)));
        Test("unapproved correction",()=>Reject(()=>Catalog.Parse(original,corrected,"[]")));
        Test("missing approval",()=>Reject(()=>Catalog.Parse(original,corrected,diff.Replace("t_12345678",""))));
        Test("diff before mismatch",()=>Reject(()=>Catalog.Parse(original,corrected,diff.Replace("Base","Wrong"))));
        Test("tokens all preserved",()=>TokenGuard.Check("[0] [name] [[attr]] *0 {STA=X} {a,b} [he] <sprite=0> <color=#ABC><b><i><size=10>X</size></i></b></color>","[name] [0] [[attr]] *0 {STA=X} {a,b} [he] <sprite=0> <color=#ABC><b><i><size=10>Y</size></i></b></color>"));
        Test("token loss/double/tag rejection",()=>{Reject(()=>TokenGuard.Check("[0]","[1]")); Reject(()=>TokenGuard.Check("[0] [0]","[0]")); Reject(()=>TokenGuard.Check("<b>X</b>","<i>X</i>"));});
        Test("override does not mutate game list/entries",()=>{var output=Resolve();Check(!ReferenceEquals(output,game)&&!ReferenceEquals(output[0],game[0]));Check(game[0].Value.StartsWith("Base") && output[0].Value.StartsWith("Corrigido"));});
        Test("all nine fields equality",()=>{var e=fixture.Original.Records[" exact \n"].Entries[0];foreach(var field in CoreEntry.Fields){var d=CoreEntry.Fields.ToDictionary(f=>f,f=>e[f]);d[field]=field=="LanguageGender"?(object)1m:field=="CanBeGendered"||field=="NeedsGenderInfo"?(object)true:"sentinel"; Check(!e.Same(new CoreEntry(d)),field);}});
        Test("Original/disabled/invalid no-op",()=>{foreach(var s in new[]{new Settings(variant:Conjunto.Original),new Settings(active:false),new Settings(variant:(Conjunto)99),new Settings(valid:false)}) Check(ReferenceEquals(Resolve(settings:s),game));});
        Test("requested/effective wrong language no-op",()=>{Check(ReferenceEquals(Resolve(req:false),game));Check(ReferenceEquals(Resolve(eff:false),game));});
        Test("exact lookup whitespace/case/null",()=>{foreach(var k in new[]{null,"exact"," exact "," EXACT \n","missing","absent","empty"}) Check(ReferenceEquals(Resolve(key:k),game));});
        Test("conflicting/new list preserved",()=>{var sentinel=new List<CoreEntry>{Entry("sentinel")};Check(ReferenceEquals(Resolve(sentinel),sentinel));var extra=new List<CoreEntry>(game){Entry("extra")};Check(ReferenceEquals(Resolve(extra),extra));});
        Test("clones independent per lookup",()=>{var a=Resolve();var b=Resolve();Check(!ReferenceEquals(a,b)&&!ReferenceEquals(a[0],b[0]));});
        Test("clone exception fail closed",()=>{var bad=new Overlay<CoreEntry>(fixture,(a,b)=>a.Same(b),e=>throw new Exception("isca"),new OnceLog(_=>{}));Check(ReferenceEquals(bad.Resolve(" exact \n",true,true,new Settings(),game),game));});
        Test("logger exception fail closed",()=>{var bad=new Overlay<CoreEntry>(fixture,(a,b)=>throw new Exception("isca"),Clone,new OnceLog(_=>throw new Exception("log")));Check(ReferenceEquals(bad.Resolve(" exact \n",true,true,new Settings(),game),game));});
        Test("bounded diagnostic once",()=>{int n=0;var l=new OnceLog(_=>n++,2);for(int i=0;i<10;i++)l.Write("same");l.Write("other");l.Write("third");Check(n==2&&l.Count==2);});
        Test("config defaults",()=>{var s=ConfigReader.Parse("[Geral]\n",new Settings());Check(s.Active&&s.Variant==Conjunto.Corrigido&&s.IntegrateMods&&!s.Diagnostic);});
        Test("config Original in runtime",()=>Check(ConfigReader.Parse("[Geral]\r\nConjunto = Original\r\nAtivo = true",new Settings()).Variant==Conjunto.Original));
        Test("config invalid fail closed",()=>{foreach(var t in new[]{"Conjunto=bad","Conjunto=1","Ativo=wat","Conjunto=Original\nConjunto=Corrigido","wrong=x","badline"})Reject(()=>ConfigReader.Parse("[Geral]\n"+t,new Settings()));});
        Test("config integration disabled base independent",()=>Check(Resolve(settings:ConfigReader.Parse("[Geral]\nIntegracaoMods=false",new Settings()))[0].Value.StartsWith("Corrigido")));
        Test("queue main-thread atomic and repeated toggle",()=>{var q=new StateQueue();Task.Run(()=>q.Enqueue(new Settings())).Wait();Check(!q.Current.Active);Check(q.ApplyPending()&&q.Current.Active);for(int i=0;i<20;i++){q.Enqueue(new Settings(variant:Conjunto.Original));q.ApplyPending();Check(ReferenceEquals(Resolve(settings:q.Current),game));q.Enqueue(new Settings());q.ApplyPending();Check(Resolve(settings:q.Current)[0].Value.StartsWith("Corrigido"));}q.Enqueue(new Settings());Check(!q.ApplyPending());});
        Test("API stub binding exact/missing signature",()=>{Check(Bindings.ListTarget()!=null);try{Bindings.Exact(typeof(OptionsManager),"GetLocalizationEntryList",typeof(string),true,typeof(string));}catch(MissingMethodException){return;}throw new Exception("bad binding accepted");});
        Test("game entry clone nine fields",()=>{var e=fixture.Corrected.Records[" exact \n"].Entries[0];var g=Bindings.Clone(e);Check(Bindings.Equal(g,e));g.TranslatorKey="unknown";Check(!Bindings.Equal(g,e));});
        Test("first nonblank/gender lists fixture",()=>{var a=E(" ",null,""," ");var b=E("Value","Female","Male","Neutral");var list=new[]{a,b}.Select(x=>new CoreEntry(JsonShape.Object(StrictJson.Parse(JsonSerializer.Serialize(x))))).ToList();foreach(var f in new[]{"Value","Feminine","Masculine","Neutral"})Check((string)list.First(e=>!string.IsNullOrWhiteSpace((string)e[f]))[f]==(string)b[f]);});
        Test("real Debug API/resources",()=>Metadata(repo,"Debug"));
        Test("real Release API/resources",()=>Metadata(repo,"Release"));
        Console.WriteLine("HARMONY execution is a separate desktop-CLR probe (HarmonyCoreProbe.cs); local HarmonyX is not CoreCLR/net6-compatible.");
        Test("no-op corpus performance allocation",()=>{var noOp=new Overlay<CoreEntry>(real,(a,b)=>a.Same(b),Clone,new OnceLog(_=>{}));var s=new Settings();for(int i=0;i<100;i++)noOp.Resolve(" exact \n",true,true,s,game);long before=GC.GetAllocatedBytesForCurrentThread();var sw=Stopwatch.StartNew();for(int i=0;i<100000;i++)Check(ReferenceEquals(noOp.Resolve(" exact \n",true,true,s,game),game));sw.Stop();long bytes=GC.GetAllocatedBytesForCurrentThread()-before;Console.WriteLine("PERF 100000 no-op lookups ms="+sw.Elapsed.TotalMilliseconds+" allocated="+bytes);Check(bytes<1024);});
        Console.WriteLine("RESULT passed="+passed+" failed="+failed+"; synthetic fixture tests != runtime game verification");
        return failed==0?0:1;
    }
}
