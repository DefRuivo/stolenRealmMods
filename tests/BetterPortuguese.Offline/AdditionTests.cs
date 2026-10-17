using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Nodes;
using BetterPortuguese.Core;
using E = BetterPortuguese.Core.Entry;

internal static class AdditionTests
{
    private sealed class Case
    {
        public JsonObject Original, Corrected, Change;
        public JsonArray Diff;
        public string Key;
        public Catalog Parse() => Catalog.Parse(Original.ToJsonString(), Corrected.ToJsonString(), Diff.ToJsonString());
        public JsonObject Target => (JsonObject)((JsonArray)Corrected["records"])[0];
    }
    private static JsonNode Copy(JsonNode n) => n == null ? null : JsonNode.Parse(n.ToJsonString());
    private static JsonObject Entry(string key, string value) => new JsonObject {
        ["Value"]=value,["Key"]=key,["TranslatorKey"]=null,["Feminine"]=null,["Masculine"]=null,["Neutral"]=null,
        ["LanguageGender"]=0,["CanBeGendered"]=false,["NeedsGenderInfo"]=false };
    private static Case Make(bool absent = false, string key = " exact [0] <b>key</b>\n", string value = " exato [0] <b>valor</b>\n")
    {
        var source = new JsonObject { ["taskId"]="t_12345678",["artifactSha256"]=new string('a',64),["resourcePath"]="SYNTHETIC_ADDITION_TEST",["resourcePathId"]=1,["resourceAssetSha256"]=new string('b',64),["assemblySha256"]=new string('c',64),["canonicalMemberSha256"]=new string('d',64) };
        var original = new JsonObject { ["schemaVersion"]=1,["locale"]="pt-BR",["variant"]="Original",["source"]=source,
            ["records"]=new JsonArray(new JsonObject{["id"]="LANG-00001",["key"]=key,["presentInSource"]=!absent,["entries"]=absent?null:new JsonArray()}),["manualRecords"]=new JsonArray() };
        var corrected=(JsonObject)Copy(original); corrected["variant"]="Corrigido";
        var entry=Entry(key,value); ((JsonObject)((JsonArray)corrected["records"])[0])["entries"]=new JsonArray(Copy(entry));
        var change=new JsonObject{["operation"]="addEntry",["id"]="LANG-00001",["key"]=key,["entryIndex"]=0,["before"]=absent?null:new JsonArray(),["after"]=entry,["approvalTaskId"]="t_12345678"};
        return new Case{Original=original,Corrected=corrected,Change=change,Diff=new JsonArray(change),Key=key};
    }
    private static void Check(bool yes) { if(!yes)throw new Exception("addition assertion"); }
    private static void Reject(Action action, string reason = null)
    {
        try { action(); } catch(FormatException e) { Check(reason == null || e.Message.Contains(reason)); return; }
        throw new Exception("addition negative control accepted");
    }
    private static E Clone(E e)=>new E(E.Fields.ToDictionary(f=>f,f=>e[f]));
    public static void Run(Action<string,Action> test)
    {
        test("addEntry empty list exact metadata/token success",()=>{var f=Make();var c=f.Parse();Check(c.Changed.Count==1&&c.Original.Records[f.Key].Entries.Count==0&&c.Corrected.Records[f.Key].Entries[0].Key==f.Key);});
        test("addEntry null baseline success preserves Original identity",()=>{var f=Make(true);var c=f.Parse();Check(c.Original.Records[f.Key].Entries==null&&!c.Corrected.Records[f.Key].PresentInSource&&c.Changed.Count==1);});
        test("addEntry null and empty are distinct",()=>{foreach(bool absent in new[]{false,true}){var f=Make(absent);f.Change["before"]=absent?new JsonArray():null;Reject(()=>f.Parse(),"Baseline null/empty mismatch");}});
        test("addEntry rejects populated key",()=>{var f=Make();((JsonObject)((JsonArray)f.Original["records"])[0])["entries"]=new JsonArray(Entry(f.Key,"old"));Reject(()=>f.Parse(),"Entry already exists");});
        test("addEntry rejects unknown key and identity mismatch",()=>{foreach(string field in new[]{"id","key"}){var f=Make();f.Change[field]="missing";Reject(()=>f.Parse(),"Unknown ID/key");}});
        test("addEntry invalid position negative and beyond end",()=>{foreach(int index in new[]{-1,1,int.MaxValue}){var f=Make();f.Change["entryIndex"]=index;Reject(()=>f.Parse(),"Only entryIndex 0");}});
        test("addEntry invalid operation and schema fields",()=>{var f=Make();f.Change["operation"]="append";Reject(()=>f.Parse(),"Unsupported diff operation");f=Make();f.Change["field"]="Value";Reject(()=>f.Parse(),"Unexpected/missing fields");f=Make();f.Change.Remove("operation");Reject(()=>f.Parse());});
        test("addEntry missing approval and malformed approval",()=>{foreach(string approval in new[]{null,"","t_zzzzzzzz","t_123456789"}){var f=Make();f.Change["approvalTaskId"]=approval;Reject(()=>f.Parse());}});
        test("addEntry rejects duplicate target",()=>{var f=Make();f.Diff.Add(Copy(f.Change));Reject(()=>f.Parse(),"Duplicate addEntry target");});
        test("addEntry rejects omitted metadata and invalid types",()=>{foreach(string field in E.Fields){var f=Make();((JsonObject)f.Change["after"]).Remove(field);Reject(()=>f.Parse());}foreach(string field in new[]{"entryIndex","before","after"}){var f=Make();f.Change[field]="bad";Reject(()=>f.Parse());}});
        test("addEntry rejects invented gender/fallback/key metadata",()=>{foreach(string field in E.Fields.Where(x=>x!="Value")){var f=Make();((JsonObject)f.Change["after"])[field]=field=="LanguageGender"?JsonValue.Create(1):field=="CanBeGendered"||field=="NeedsGenderInfo"?JsonValue.Create(true):JsonValue.Create("invented");Reject(()=>f.Parse(),"Unsupported metadata");}});
        test("addEntry rejects null empty whitespace Value",()=>{foreach(string value in new[]{null,""," \r\n"}){var f=Make();((JsonObject)f.Change["after"])["Value"]=value;Reject(()=>f.Parse(),"Value must be nonblank");}});
        test("addEntry rejects unapproved list or null cardinality changes",()=>{foreach(bool absent in new[]{true,false}){var f=Make(absent);f.Diff.Clear();Reject(()=>f.Parse(),"List/absence operations");}});
        test("addEntry must be reflected in corrected",()=>{var f=Make();f.Target["entries"]=new JsonArray();Reject(()=>f.Parse(),"not exactly reflected");f=Make(true);f.Target["entries"]=null;Reject(()=>f.Parse(),"not exactly reflected");});
        test("addEntry exact full entry after comparison",()=>{foreach(string field in E.Fields){var f=Make();var after=(JsonObject)((JsonArray)f.Target["entries"])[0];after[field]=field=="LanguageGender"?JsonValue.Create(1):field=="CanBeGendered"||field=="NeedsGenderInfo"?JsonValue.Create(true):JsonValue.Create("different");Reject(()=>f.Parse(),"not exactly reflected");}});
        test("addEntry refuses second entry and identity/presence mutation",()=>{var f=Make();((JsonArray)f.Target["entries"]).Add(Entry(f.Key,"extra"));Reject(()=>f.Parse(),"not exactly reflected");f=Make(true);f.Target["presentInSource"]=true;Reject(()=>f.Parse(),"Immutable ID/key/presence changed");});
        test("addEntry token loss duplicate substitution fail closed",()=>{foreach(string value in new[]{"[0] key","[0] [0] <b>key</b>","[1] <b>key</b>","[0] <i>key</i>"}){var f=Make(value:value);Reject(()=>f.Parse(),"Functional tokens/tags changed");}});
        test("addEntry tokens reorder permitted inventory unchanged",()=>{var f=Make(key:"[0] [1]",value:"[1] [0]");Check(f.Parse().Changed.Count==1);});
        test("addEntry does not inherit TokenGuard edit exceptions",()=>{TokenGuard.RegisterException("t_abcdef12","0.1.0",new[]{"<addition-only>"},Array.Empty<string>());var f=Make(key:"<addition-only>source",value:"translation");Reject(()=>f.Parse(),"Functional tokens/tags changed");});
        test("addEntry failed parse does not register token exception",()=>{var f=Make(key:"[unique-addition-token]",value:"translation");Reject(()=>f.Parse());Reject(()=>TokenGuard.Check("[unique-addition-token]","translation"));});
        test("addEntry mixed legacy edit regression",()=>{var f=Make();var old=new JsonObject{["id"]="LANG-00002",["key"]="old",["presentInSource"]=true,["entries"]=new JsonArray(Entry("old","before"))};((JsonArray)f.Original["records"]).Add(old);var next=(JsonObject)Copy(old);((JsonObject)((JsonArray)next["entries"])[0])["Value"]="after";((JsonArray)f.Corrected["records"]).Add(next);f.Diff.Add(new JsonObject{["id"]="LANG-00002",["key"]="old",["entryIndex"]=0,["field"]="Value",["before"]="before",["after"]="after",["approvalTaskId"]="t_12345678"});Check(f.Parse().Changed.Count==2);});
        test("addEntry overlay empty/null cloned no mutation",()=>{foreach(bool absent in new[]{true,false}){var f=Make(absent);var c=f.Parse();var engine=new Overlay<E>(c,(a,b)=>a.Same(b),Clone,new OnceLog(_=>{}));var incoming=absent?null:new List<E>();var a=engine.Resolve(f.Key,true,true,new Settings(),incoming);var b=engine.Resolve(f.Key,true,true,new Settings(),incoming);Check(a.Count==1&&a[0].Same(c.Corrected.Records[f.Key].Entries[0])&&!ReferenceEquals(a,b)&&!ReferenceEquals(a[0],b[0])&&(incoming==null||incoming.Count==0));}});
        test("addEntry overlay Original disabled invalid wrong languages no-op",()=>{foreach(bool absent in new[]{true,false}){var f=Make(absent);var c=f.Parse();var engine=new Overlay<E>(c,(a,b)=>a.Same(b),Clone,new OnceLog(_=>{}));var incoming=absent?null:new List<E>();foreach(var s in new[]{new Settings(active:false),new Settings(variant:Conjunto.Original),new Settings(valid:false),new Settings(variant:(Conjunto)99)})Check(ReferenceEquals(engine.Resolve(f.Key,true,true,s,incoming),incoming));Check(ReferenceEquals(engine.Resolve(f.Key,false,true,new Settings(),incoming),incoming));Check(ReferenceEquals(engine.Resolve(f.Key,true,false,new Settings(),incoming),incoming));}});
        test("addEntry preserves unknown writer and null/empty conflicts",()=>{foreach(bool absent in new[]{true,false}){var f=Make(absent);var c=f.Parse();var engine=new Overlay<E>(c,(a,b)=>a.Same(b),Clone,new OnceLog(_=>{}));var writer=new List<E>{Clone(c.Corrected.Records[f.Key].Entries[0])};Check(ReferenceEquals(engine.Resolve(f.Key,true,true,new Settings(),writer),writer));var mismatch=absent?new List<E>():null;Check(ReferenceEquals(engine.Resolve(f.Key,true,true,new Settings(),mismatch),mismatch));}});
        test("addEntry clone failure preserves incoming",()=>{var f=Make();var c=f.Parse();var engine=new Overlay<E>(c,(a,b)=>a.Same(b),_=>throw new Exception("clone"),new OnceLog(_=>{}));var incoming=new List<E>();Check(ReferenceEquals(engine.Resolve(f.Key,true,true,new Settings(),incoming),incoming));});
    }
}
