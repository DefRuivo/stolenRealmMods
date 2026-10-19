// Synthetic CLR host, production BP hooks + verbatim BT regrouping body.
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Reflection;
using System.Runtime.CompilerServices;
using BetterPortuguese.Core;
using BetterPortuguese.Runtime;
using HarmonyLib;

namespace UnityEngine {public class Sprite{} public class Transform{} public struct Color{} public struct Vector3{}}
public class TooltipOffsetInfo{} public struct ControlGlyphInfo{}
public class FakeText {public string text;}
public class Tooltip
{
    public FakeText Description=new FakeText();
    [MethodImpl(MethodImplOptions.NoInlining)]public void Render(string description){Description.text=description;}
}
namespace BepInEx.Bootstrap {
    public static class Chainloader {public static Dictionary<string,PluginInfo> PluginInfos=new Dictionary<string,PluginInfo>();}
    public class PluginInfo {public Meta Metadata;public object Instance;}
    public class Meta {public Version Version;}
}
public class FakeLog {public void LogInfo(string s){} }
public static class Plugin {public static FakeLog Log=new FakeLog();}
public static class StatusSkillSynergyPatch {public const string Marcador="Your skills on this status:";}
public static class ShrineAuraPatch {public const string MarcadorLinhaDeAuras="Your active shrine auras:";}
public static partial class BTOrder
{
    static bool _diagnosticadoCor;
    static string _corEspecialDoJogo="CBB396";
    const string MarcadorCorDeExplicacao="C8B090";
    public static HashSet<string> _conteudosDeNota=new HashSet<string>();
    public static string AuraColor="00D7FF";
    static string CorDaLinhaDeAuras()=>AuraColor;
    static void RegistrarFalhaIgnorada(string s,Exception ex){throw new Exception(s,ex);}
}
public static class NativeShaped
{
    public static string Drawn;
    public static bool Throw;
    [MethodImpl(MethodImplOptions.NoInlining)]public static void Build(string original,ref string __result)
    {
        if(original!=__result)return;
        __result=original+"\n\n<color=#C8B090>Cannot move or perform actions.</color>";
        if(Throw)throw new InvalidOperationException("native");
    }
    [MethodImpl(MethodImplOptions.NoInlining)]public static void ShowTooltip(ref string description){Drawn=description;}
}
public static class ModsHarmonyProbe
{
    static int passed;
    static Settings current=new Settings();
    static Type T=typeof(BetterTooltipsAdapter);
    static List<string> logs=new List<string>();
    static MethodInfo M(string n)=>T.GetMethod(n,BindingFlags.NonPublic|BindingFlags.Static);
    static void Field(string n,object v)=>T.GetField(n,BindingFlags.NonPublic|BindingFlags.Static).SetValue(null,v);
    static void Check(bool b,string name){if(!b)throw new Exception(name);passed++;Console.WriteLine("PASS "+name);}
    public static int Main(string[] args)
    {
        var bp=new Harmony(BetterTooltipsAdapter.Owner);var bt=new Harmony(ModCatalog.BetterTooltipsGuid);
        try
        {
            var map=ModCatalog.Parse(File.ReadAllText(args[0]));
            BetterTooltipsAdapter.Install(map,()=>current,new OnceLog(s=>logs.Add(s)),s=>logs.Add(s));
            Check(BetterTooltipsAdapter.Count==0&&logs.Any(s=>s.Contains("ausente")),"BT absent fail-closed, base independent");
            BepInEx.Bootstrap.Chainloader.PluginInfos[ModCatalog.BetterTooltipsGuid]=new BepInEx.Bootstrap.PluginInfo{Metadata=new BepInEx.Bootstrap.Meta{Version=new Version("9.9.9")},Instance=new object()};
            BetterTooltipsAdapter.Install(map,()=>current,new OnceLog(s=>logs.Add(s)),s=>logs.Add(s));
            Check(BetterTooltipsAdapter.Count==0&&logs.Any(s=>s.Contains("versao BT nao homologada")),"BT version drift rejected before patching");
            BepInEx.Bootstrap.Chainloader.PluginInfos[ModCatalog.BetterTooltipsGuid].Metadata.Version=new Version("0.1.5");
            BetterTooltipsAdapter.Install(map,()=>current,new OnceLog(s=>logs.Add(s)),s=>logs.Add(s));
            Check(BetterTooltipsAdapter.Count==0&&logs.Any(s=>s.Contains("Assembly-CSharp divergente")),"game identity drift rejected before patching");
            Field("map",map);Field("settings",(Func<Settings>)(()=>current));Field("warnings",new OnceLog(s=>logs.Add(s)));Field("info",(Action<string>)(s=>logs.Add(s)));Field("ready",true);Field("notes",BTOrder._conteudosDeNota);
            MethodInfo build=typeof(NativeShaped).GetMethod("Build"),display=typeof(NativeShaped).GetMethod("ShowTooltip");
            M("Hook").Invoke(null,new object[]{bp,build,"SourcePrefix","SourcePostfix","SourceFinalizer"});
            M("Hook").Invoke(null,new object[]{bp,display,"DisplayPrefix",null,null});
            bt.Patch(display,prefix:new HarmonyMethod(typeof(BTOrder).GetMethod("Prefix",BindingFlags.NonPublic|BindingFlags.Static)));
            string source="Stunned.",text="Atordoado.";
            NativeShaped.Build(source,ref text);Check(text=="Atordoado.\n\n<color=#C8B090>Cannot move or perform actions.</color>","production bridge runs BT once and preserves BP origin");
            BTOrder._conteudosDeNota.Add("Cannot move or perform actions.");
            NativeShaped.ShowTooltip(ref text);Check(NativeShaped.Drawn.Contains("Não pode se mover nem executar ações."),"production final hook after actual BT regrouping");
            foreach(var s in new[]{new Settings(active:false),new Settings(integrateMods:false),new Settings(variant:Conjunto.Original),new Settings(valid:false)})
            {current=s;text="Atordoado.";NativeShaped.Build(source,ref text);Check(text=="Atordoado.","bridge no-op "+s.Active+s.Valid+s.Variant+s.IntegrateMods);}
            current=new Settings();OptionsManager.CurrentLanguage=LanguageChoice.English;text=source;NativeShaped.Build(source,ref text);Check(text.Contains("Cannot move"),"English retains BT result");
            OptionsManager.CurrentLanguage=LanguageChoice.PortugueseBrazil;
            NativeShaped.Throw=true;text="Atordoado.";bool thrown=false;try{NativeShaped.Build(source,ref text);}catch(InvalidOperationException){thrown=true;}
            Check(thrown&&text=="Atordoado.","production finalizer restores origin, preserves native exception");NativeShaped.Throw=false;
            string a="Lasts 3 turns.",b="Also increases the healing you do by the same percentage.";
            BTOrder._conteudosDeNota.Add(a);BTOrder._conteudosDeNota.Add(b);
            Func<string,string> note=s=>"<color=#CBB396>"+s+"</color>";
            foreach(string auraColor in new[]{"00D7FF","CBB396"})
            for(int mask=0;mask<16;mask++)
            {
                BTOrder.AuraColor=auraColor;
                string raw="DAMAGE <color=#CBB396>123</color>";
                if((mask&1)!=0)raw+="\n\n"+note(a);
                if((mask&2)!=0)raw+="\n\n"+note(b);
                if((mask&4)!=0)raw+="\n<color=#00D7FF>Your skills on this status: Frostbite I −2% damage per stack.</color>";
                if((mask&8)!=0)raw+="\n\n<color=#00D7FF>Your active shrine auras: Dodge +40% (total +53.4%).</color>";
                raw=raw.Replace("#00D7FF","#"+auraColor);
                raw+="\n\nCOST 5";
                current=new Settings(active:false);text=raw;NativeShaped.ShowTooltip(ref text);string control=NativeShaped.Drawn;
                string expectedControl="DAMAGE <color=#CBB396>123</color>\n\nCOST 5";
                if((mask&1)!=0)expectedControl+="\n\n"+note(a);
                if((mask&2)!=0)expectedControl+="\n\n"+note(b);
                if((mask&4)!=0)expectedControl+="\n\n<color=#"+auraColor+">Your skills on this status: Frostbite I −2% damage per stack.</color>";
                if((mask&8)!=0)expectedControl+="\n\n<color=#"+auraColor+">Your active shrine auras: Dodge +40% (total +53.4%).</color>";
                Check(control==expectedControl,"BT control exact independent separators/order mask="+mask+" palette="+auraColor);
                current=new Settings();text=raw;NativeShaped.ShowTooltip(ref text);string translated=NativeShaped.Drawn;
                string expected=control.Replace(a,"Dura 3 turnos.").Replace(b,"Também aumenta a cura que você realiza na mesma porcentagem.")
                    .Replace("Your skills on this status:","Suas habilidades neste status:").Replace("% damage per stack","% de dano por acúmulo")
                    .Replace("Your active shrine auras:","Suas auras de santuário ativas:").Replace("Dodge +40%","Esquiva +40%");
                Check(translated==expected,"BP on/off same BT order, blank lines, colors, numbers mask="+mask);
                Check(!translated.Contains("\n\n\n")&&translated.StartsWith("DAMAGE <color=#CBB396>123</color>"),"no numeric block displacement or orphan separators mask="+mask);
                if((mask&8)!=0)Check(translated.EndsWith("<color=#"+auraColor+">Suas auras de santuário ativas: Esquiva +40% (total +53.4%).</color>"),"aura last mask="+mask);
            }
            MethodInfo render=typeof(Tooltip).GetMethod("Render");
            M("Hook").Invoke(null,new object[]{bp,render,null,"DisplayPostfix",null});
            var tooltip=new Tooltip();string linked="<color=#CBB396>Atordoado.\n\n<color=#CBB396>Cannot move or perform actions.</color></color>";
            tooltip.Render(linked);Check(tooltip.Description.text==linked.Replace("Cannot move or perform actions.","Não pode se mover nem executar ações."),"post-render handles nested BT notes created by native linked statuses");
            current=new Settings(active:false);tooltip.Render(linked);Check(tooltip.Description.text==linked,"post-render disabled preserves every byte");current=new Settings();
            bp.UnpatchSelf();text="Atordoado.";NativeShaped.Build(source,ref text);Check(text=="Atordoado.","unpatched negative control loses translated BT block");
            Console.WriteLine("RESULT passed="+passed+" failed=0; SYNTHETIC CLR + verbatim BT prefix, no game patched");return 0;
        }
        catch(Exception ex){Console.WriteLine("FAIL "+ex);return 1;}
        finally{bp.UnpatchSelf();bt.UnpatchSelf();}
    }
}
