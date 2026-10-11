using Mono.Cecil;
using System.Text.Json;
using System.Security.Cryptography;

if(args.Length<2) throw new ArgumentException("Uso: Inspect surface|targets|plugin <dll> | ui <dll> [<dll>...]; somente metadados, sem execução do alvo");
using var module=ModuleDefinition.ReadModule(args[1]);
IEnumerable<TypeDefinition> Flatten(IEnumerable<TypeDefinition> types) {
    foreach(var t in types) { yield return t; foreach(var n in Flatten(t.NestedTypes)) yield return n; }
}
var all=Flatten(module.Types).ToArray();
var replacements=all.Where(t=>t.IsPublic && t.IsAbstract && t.BaseType?.FullName=="BepInEx.BaseUnityPlugin")
    .ToDictionary(t=>t.FullName,t=>"Gumatos.RealmApi.ContractReference.ModLifecycleBase");
foreach(var t in all.Where(t=>t.IsPublic && t.CustomAttributes.Any(a=>a.AttributeType.FullName=="BepInEx.BepInPlugin")))
    replacements[t.FullName]="Gumatos.RealmApi.ContractReference.HostContract";
string Neutral(string value) {
    foreach(var pair in replacements) value=value.Replace(pair.Key,pair.Value);
    return value.Replace(module.Assembly.Name.Name,"Gumatos.RealmApi.ContractReference");
}
var hash=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[1]))).ToLowerInvariant();
object data;
if(args[0]=="surface") {
    var types=all.Where(t=>(t.IsPublic||t.IsNestedPublic)&&!t.FullName.StartsWith("System.")&&!t.FullName.StartsWith("Microsoft.")).Select(t=>new {
        name=Neutral(t.FullName), kind=t.IsEnum?"enum":t.IsInterface?"interface":t.IsValueType?"struct":"class", baseType=Neutral(t.BaseType?.FullName??""),
        methods=t.Methods.Where(m=>m.IsPublic&&!m.IsGetter&&!m.IsSetter&&!m.IsAddOn&&!m.IsRemoveOn).Select(m=>new {
            signature=Neutral(m.FullName), isStatic=m.IsStatic,
            parameters=m.Parameters.Select(p=>new {name=p.Name,type=Neutral(p.ParameterType.FullName),isOptional=p.IsOptional,hasDefault=p.HasConstant,defaultValue=p.HasConstant?p.Constant:null}).ToArray()
        }).OrderBy(x=>x.signature).ToArray(),
        fields=t.Fields.Where(f=>f.IsPublic).Select(f=>new {signature=Neutral(f.FullName),isStatic=f.IsStatic,isReadOnly=f.IsInitOnly,hasConstant=f.HasConstant,constant=f.HasConstant&&t.IsEnum?f.Constant:null}).OrderBy(x=>x.signature).ToArray(),
        properties=t.Properties.Where(p=>p.GetMethod?.IsPublic==true||p.SetMethod?.IsPublic==true).Select(p=>new {signature=Neutral(p.FullName),canRead=p.GetMethod?.IsPublic==true,canWrite=p.SetMethod?.IsPublic==true}).OrderBy(x=>x.signature).ToArray(),
        events=t.Events.Where(e=>e.AddMethod.IsPublic).Select(e=>Neutral(e.FullName)).OrderBy(x=>x).ToArray()
    }).OrderBy(t=>t.name).ToArray();
    data=new {schemaVersion=2,scope="contract-inventory-not-implemented-api",sourceSha256=hash,counts=new {types=types.Length,methods=types.Sum(t=>t.methods.Length),fields=types.Sum(t=>t.fields.Length),properties=types.Sum(t=>t.properties.Length),events=types.Sum(t=>t.events.Length)},types};
} else if(args[0]=="targets") {
    var typeNames=new[]{"Burst2Flame.Game","Character","GameLogic","SkillTreeManager","OptionsManager"};
    var methodNames=new[]{"Awake","ModifyHealth","StartNewTurn","EndTurn","StartGame","ProcessDeath","PerformAction","ProcessSkillTriggers","UpdateSkillTreeItems","Localize"};
    data=new {schemaVersion=2,sha256=hash,assemblyVersion=module.Assembly.Name.Version.ToString(),types=all.Where(t=>typeNames.Contains(t.FullName)).Select(t=>new {name=t.FullName,methods=t.Methods.Where(m=>methodNames.Contains(m.Name)).Select(m=>new {signature=m.FullName,isStatic=m.IsStatic,parameters=m.Parameters.Select(p=>new {name=p.Name,type=p.ParameterType.FullName}).ToArray()}).ToArray()}).OrderBy(t=>t.name).ToArray()};
} else if(args[0]=="plugin") {
    data=new {sha256=hash,assemblyVersion=module.Assembly.Name.Version.ToString(),assemblyReferences=module.AssemblyReferences.Select(a=>a.FullName).ToArray(),types=all.Where(t=>t.IsPublic).Select(t=>new {name=t.FullName,attributes=t.CustomAttributes.Where(a=>a.AttributeType.FullName.StartsWith("BepInEx.")).Select(a=>new {name=a.AttributeType.FullName,arguments=a.ConstructorArguments.Select(c=>c.Value).ToArray()}).ToArray()}).ToArray()};
} else if(args[0]=="ui") {
    // API-R1-I2: superficie implementada da familia UI. Sem anonimizacao: este comando audita a NOSSA API,
    // e a comparacao com o inventario (anonimizado) e feita por api/tools/check_ui_contract.py.
    // Aceita mais de uma DLL (ex.: RealmApi.dll com os tipos publicos + RealmApi.Core.dll com o enum de Skills).
    var sources=new List<TypeDefinition>(all);
    for(int i=2;i<args.Length;i++) sources.AddRange(Flatten(ModuleDefinition.ReadModule(args[i]).Types));
    var ui=sources.Where(t=>t.FullName.StartsWith("Gumatos.RealmApi.UI.")).OrderBy(t=>t.FullName).Select(t=>new {
        name=t.FullName,
        methods=t.Methods.Where(m=>m.IsPublic&&!m.IsConstructor&&!m.IsGetter&&!m.IsSetter&&!m.IsAddOn&&!m.IsRemoveOn).Select(m=>new {
            signature=m.FullName, name=m.Name, isStatic=m.IsStatic, returnType=m.ReturnType.FullName,
            parameters=m.Parameters.Select(p=>new {name=p.Name,type=p.ParameterType.FullName,isOptional=p.IsOptional,hasDefault=p.HasConstant,defaultValue=p.HasConstant?p.Constant:null}).ToArray()
        }).OrderBy(x=>x.signature).ToArray()
    }).ToArray();
    var skillsEnum=sources.Where(t=>t.FullName=="Gumatos.RealmApi.Skills.SkillTree").Select(t=>new {name=t.FullName,fields=t.Fields.Where(f=>f.IsPublic&&f.HasConstant).Select(f=>f.Name).OrderBy(x=>x).ToArray()}).SingleOrDefault();
    data=new {schemaVersion=1,scope="realmapi-ui-family-implemented-surface",sha256=hash,sources=args.Skip(1).ToArray(),types=ui,skillsEnum};
} else throw new ArgumentException("Comando desconhecido");
Console.WriteLine(JsonSerializer.Serialize(data,new JsonSerializerOptions{WriteIndented=true}));
