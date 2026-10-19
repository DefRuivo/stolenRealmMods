using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using BetterPortuguese.Core;

internal static class ModTests
{
    public static void Run(Action<string,Action> test, string repo)
    {
        ModCatalog map=Resources.LoadMods(typeof(ModTests).Assembly);
        Action<bool> check = b=> {if(!b)throw new Exception("mod assertion");};
        string corpusPath=Environment.GetEnvironmentVariable("BPMODS_CORPUS");
        if (corpusPath != null)
        {
            var rows=JsonShape.Array(StrictJson.Parse(File.ReadAllText(corpusPath)));
            foreach(var raw in rows)
            {
                var row=JsonShape.Object(raw);string note=JsonShape.Text(row["note"]);
                test("BT actual note "+row["table"]+":"+row["line"],()=>check(map.TryNote(note,s=>s,out string _)));
            }
        }
        Func<string,string> names = s=>s=="Intelligence"?"Inteligência":s=="Frostbite I"?"Mordida Gélida I":s=="Armor"?"Armadura":s;
        foreach(var r in map.Rules)
        {
            var rule=r;
            test("BT registry roundtrip "+rule.Id,()=>{
                string source=rule.Source,target=rule.Target;
                for(int i=0;i<rule.Slots.Length;i++)
                {
                    string value=rule.Slots[i]=="number"?"−12,5":rule.Slots[i]=="richNumber"?"<color=#CBB396>23.3</color>":rule.Slots[i]=="opaque"?"Damage +20; Armor 5":"Intelligence";
                    source=source.Replace("{"+i+"}",value);
                    target=target.Replace("{"+i+"}",rule.Slots[i]=="gameText"?names(value):value);
                }
                if(rule.Kind=="note") {check(map.TryNote(source,names,out string value));check(value==target);}
                else {check(map.TryWhole(rule.Kind,source,names,out string value));check(value==target);}
            });
        }
        test("BT settings/idiom no-op matrix",()=>{
            foreach(var s in new[]{new Settings(active:false),new Settings(variant:Conjunto.Original),new Settings(integrateMods:false),new Settings(valid:false)})check(!ModCatalog.Enabled(s,true));
            check(!ModCatalog.Enabled(new Settings(),false));check(ModCatalog.Enabled(new Settings(),true));
        });
        test("BT rebase preserves BP origin and all separators",()=>{
            string note="\n\n<color=#C8B090>Cannot move or perform actions.</color>";
            check(ModText.Rebase(map,"Stunned.","Atordoado.","Stunned."+note,names)=="Atordoado."+note);
            check(ModText.Rebase(map,"A  B ","Texto  do BP ","A B ",names)=="Texto  do BP ");
        });
        test("BT rebase typed dynamic suffix retains exact numeric markup",()=>{
            string n="<color=#CBB396>23.3</color>";
            check(ModText.Rebase(map,"Base.","Base pt.","Base ("+n+" health for you).",names)=="Base pt ("+n+" de vida para você).");
            check(ModText.Rebase(map,"Base","Base pt","Base (<color=#CBB396>+20 Intelligence, +30 Armor</color>)",names)=="Base pt (<color=#CBB396>+20 Inteligência, +30 Armadura</color>)");
        });
        test("BT whole registered note only; no global/player replacement",()=>{
            string note="Cannot move or perform actions.";
            var owned=new HashSet<string>{note};
            string input="Damage\n<color=#CBB396>10</color>\n\n<color=#CBB396>"+note+"</color>";
            string output=ModText.Translate(map,input,owned,names,null);
            check(output==input.Replace(note,"Não pode se mover nem executar ações."));
            check(ModText.Translate(map,"<color=#CBB396>"+note+"</color>",new HashSet<string>(),names,null)=="<color=#CBB396>"+note+"</color>");
        });
        test("BT notes atomic refusal; spaces not normalized",()=>{
            check(!map.TryNote("Cannot move or perform actions. UNKNOWN",names,out string value));
            check(value=="Cannot move or perform actions. UNKNOWN");
            check(map.TryNote("Lasts 3 turns.\nAlso increases the healing you do by the same percentage.",names,out value));check(value.Contains("\nTambém"));
        });
        test("BT headers, synergy, totals, opaque names",()=>{
            string input="\n\n<color=#00D7FF>Your skills on this status: Frostbite I −2% damage per stack.</color>\n\n<color=#00D7FF>Your active shrine auras: Dodge +40% (total +53.4%); Fire damage to attackers: Damage 7, Intelligence 12.</color>";
            string value=ModText.Translate(map,input,new HashSet<string>(),names,null);
            check(value.Contains("Mordida Gélida I −2% de dano por acúmulo"));check(value.Contains("Esquiva +40% (total +53.4%)"));
            check(value.Contains("Dano de Fogo aos atacantes: Damage 7, Intelligence 12."));
            check(value.Count(c=>c=='\n')==input.Count(c=>c=='\n'));
        });
        test("BT map malformed/version/token drift rejected",()=>{
            string json=File.ReadAllText(Path.Combine(repo,"BetterPortuguese/Data/pt-BR.mods.json"));
            foreach(string mutant in new[]{json.Replace("0.1.5","9.9.9"),json.Replace("BT-0001","BAD"),json.Replace("Não pode se mover nem executar ações.","Não pode [9].")})
            {bool refused=false;try{ModCatalog.Parse(mutant);}catch(FormatException){refused=true;}check(refused);}
        });
    }
}
