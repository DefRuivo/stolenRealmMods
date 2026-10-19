// EXPLICIT SYNTHETIC HOST. Actual production CompositionPatches + HarmonyX on CLR.
// Never loads, patches, opens or writes to the game. Registration hash gate is first
// tested negatively, then private patch helper/ready flags used ONLY by this harness
// to exercise actual hooks against synthetic native-shaped methods.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using BetterPortuguese.Core;
using BetterPortuguese.Runtime;
using HarmonyLib;
using UnityEngine;

namespace UnityEngine { public class Sprite {} public class Transform {} public struct Color {} public struct Vector3 {} }
namespace BetterPortuguese { public static class Plugin { public const string Guid="bp.composition.offline"; } }
public class Item {} public class ItemInfo {} public class TooltipOffsetInfo {} public class Character {} public struct ControlGlyphInfo {}
public enum DamageType { Physical, Healing, Fire }
public class Tooltip
{
    public string Raw = "Lendário Varinha", Drawn;
    public bool Throw, Nested;
    public Tooltip Comparison;
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowTooltip(string title, string subtitle, Sprite icon, string description, TooltipOffsetInfo offset, Color color, Vector3? pos=null, bool showIcon=true, bool isItem=false, float alpha=1, ControlGlyphInfo? glyph=null, string footer=null, bool equipped=false) { Drawn=subtitle; }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowItemTooltip(Item item, Transform hovering, TooltipOffsetInfo offset, Character character, bool showComp=true, bool fromLink=false, ControlGlyphInfo? glyph=null, string footer=null, Item comparison=null)
    {
        if (Nested) { Nested=false; ShowItemTooltip(new ItemInfo(),null); }
        ShowTooltip("TITLE",Raw,null,"DESCRIPTION",null,new Color());
        if (Comparison!=null) Comparison.ShowTooltip("COMPARISON",Comparison.Raw,null,"",null,new Color());
        if (Throw) throw new InvalidOperationException("native failure");
    }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowItemTooltip(ItemInfo item, TooltipOffsetInfo offset) { ShowTooltip("TITLE",Raw,null,"",null,new Color()); }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowTransmogTooltip(ItemInfo item, TooltipOffsetInfo offset, ControlGlyphInfo? glyph=null, string footer=null) { ShowTooltip("TITLE",Raw,null,"",null,new Color()); }
    public static string Label="Cura de Dano";
    [MethodImpl(MethodImplOptions.NoInlining)] public static string GetDamageTypeLabel(DamageType damageType) { return Label; }
}
// Deliberate API drift fixtures: same-typed strings swapped, and a renamed enum.
public class ReorderedTooltip
{
    public string Drawn, Title;
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowTooltip(string subtitle, string title) { Drawn=subtitle; Title=title; }
    public static string RenamedDamage(DamageType type) { return "Cura de Dano"; }
}
public static class CompositionHarmonyProbe
{
    static int passed;
    static Settings current=new Settings();
    static bool throwSettings;
    static readonly List<string> logs=new List<string>();
    static Type T=typeof(CompositionPatches);
    static void Mark(string name, bool ok) { if(!ok)throw new Exception(name);passed++;Console.WriteLine("PASS "+name); }
    static MethodInfo M(string name)=>T.GetMethod(name,BindingFlags.Static|BindingFlags.NonPublic);
    static FieldInfo F(string name)=>T.GetField(name,BindingFlags.Static|BindingFlags.NonPublic);
    static int Depth => (int)F("itemDepth").GetValue(null);
    static void Display(Tooltip t)=>t.ShowTooltip("TITLE","Lendário Varinha",null,"Cura de Dano",null,new Color(),isItem:true);
    static void Enter(Tooltip t)=>t.ShowItemTooltip(new Item(),null,null,null);
    static void Competing(ref string subtitle) { subtitle="Outro formato"; }
    static void Require(MethodInfo method, string name, Type type) => M("RequireArgument").Invoke(null,new object[]{method,name,type});
    static bool Reject(MethodInfo method, string name, Type type)
    {
        try { Require(method,name,type); return false; }
        catch (TargetInvocationException ex) { return ex.InnerException is MissingMethodException; }
    }
    public static int Main()
    {
        var h=new Harmony(BetterPortuguese.Plugin.Guid);
        var other=new Harmony("foreign.composition.offline");
        try
        {
            CompositionPatches.Install(h,()=> {if(throwSettings)throw new Exception("settings");return current;},new OnceLog(s=>logs.Add(s)),s=>logs.Add(s));
            Mark("assembly drift rejected/logged before any hook",!(bool)F("itemReady").GetValue(null)&&!(bool)F("damageReady").GetValue(null)&&logs.Any(s=>s.Contains("SHA-256 divergente")));
            // Bypass only the intentionally mismatching synthetic assembly identity.
            var patch=M("Patch");
            var displayTarget=typeof(Tooltip).GetMethod("ShowTooltip");
            var damageTarget=typeof(Tooltip).GetMethod("GetDamageTypeLabel");
            Require(displayTarget,"subtitle",typeof(string));
            Require(damageTarget,"damageType",typeof(DamageType));
            Mark("named argument contracts accepted",true);
            Mark("missing target fails closed",Reject(null,"subtitle",typeof(string)));
            Mark("renamed subtitle fails closed",Reject(displayTarget,"renamedSubtitle",typeof(string)));
            Mark("retyped subtitle fails closed",Reject(displayTarget,"subtitle",typeof(int)));
            Mark("renamed damageType fails closed",Reject(typeof(ReorderedTooltip).GetMethod("RenamedDamage"),"damageType",typeof(DamageType)));
            var reordered=typeof(ReorderedTooltip).GetMethod("ShowTooltip");
            Require(reordered,"subtitle",typeof(string));
            patch.Invoke(null,new object[]{h,reordered,"SubtitlePrefix",null,null});
            var methods=typeof(Tooltip).GetMethods(BindingFlags.Public|BindingFlags.Instance|BindingFlags.Static|BindingFlags.DeclaredOnly);
            foreach(var m in methods)
            {
                string pre=null,post=null,fin=null;
                if(m.Name=="ShowTooltip")pre="SubtitlePrefix";
                if(m.Name=="ShowItemTooltip"||m.Name=="ShowTransmogTooltip"){pre="EnterItem";fin="LeaveItem";}
                if(m.Name=="GetDamageTypeLabel")post="DamagePostfix";
                patch.Invoke(null,new object[]{h,m,pre,post,fin});
            }
            F("itemReady").SetValue(null,true);F("damageReady").SetValue(null,true);
            var moved=new ReorderedTooltip();
            F("itemDepth").SetValue(null,1);
            try { moved.ShowTooltip("Lendário Varinha","TITLE unchanged"); }
            finally { F("itemDepth").SetValue(null,0); }
            Mark("same-typed argument reorder binds subtitle not title",moved.Drawn=="Lendária Varinha"&&moved.Title=="TITLE unchanged"&&Depth==0);
            var t=new Tooltip();
            Display(t);Mark("no scope => no change even isItem=true",t.Drawn=="Lendário Varinha"&&Depth==0);
            Enter(t);Mark("native-shaped item scope + original executed",t.Drawn=="Lendária Varinha"&&Depth==0);
            t.ShowItemTooltip(new ItemInfo(),null);Mark("ItemInfo overload",t.Drawn=="Lendária Varinha"&&Depth==0);
            t.ShowTransmogTooltip(new ItemInfo(),null);Mark("transmog overload",t.Drawn=="Lendária Varinha"&&Depth==0);
            t.Comparison=new Tooltip{Raw="Raro Armadura"};Enter(t);Mark("comparison tooltip in same native scope",t.Comparison.Drawn=="Rara Armadura"&&Depth==0);
            t.Nested=true;Enter(t);Mark("nested call restores outer scope",t.Drawn=="Lendária Varinha"&&Depth==0);
            t.Throw=true;bool thrown=false;try{Enter(t);}catch(InvalidOperationException e){thrown=e.Message=="native failure";}
            Mark("native exception unchanged, finalizer restores scope",thrown&&Depth==0);t.Throw=false;
            Display(t);Mark("no scope leak after exception",t.Drawn=="Lendário Varinha");
            Mark("Healing postfix",Tooltip.GetDamageTypeLabel(DamageType.Healing)=="Cura por Dano");
            Mark("other damage type not rewritten",Tooltip.GetDamageTypeLabel(DamageType.Fire)=="Cura de Dano");
            foreach(var s in new[]{new Settings(active:false),new Settings(variant:Conjunto.Original),new Settings(valid:false)})
            {current=s;Enter(t);Mark("settings no-op "+s.Active+s.Valid+s.Variant,t.Drawn=="Lendário Varinha"&&Tooltip.GetDamageTypeLabel(DamageType.Healing)=="Cura de Dano");}
            current=new Settings();OptionsManager.CurrentLanguage=LanguageChoice.English;Enter(t);
            Mark("English untouched",t.Drawn=="Lendário Varinha"&&Tooltip.GetDamageTypeLabel(DamageType.Healing)=="Cura de Dano");
            OptionsManager.CurrentLanguage=LanguageChoice.PortugueseBrazil;
            throwSettings=true;Enter(t);Mark("settings exception fail-closed",t.Drawn=="Lendário Varinha"&&Tooltip.GetDamageTypeLabel(DamageType.Healing)=="Cura de Dano"&&Depth==0);throwSettings=false;
            t.Raw="Lendário Orbe";Enter(t);Mark("unknown structure preserved + reason",t.Drawn==t.Raw&&logs.Any(s=>s.Contains("nao reconhecido")));
            Tooltip.Label="custom";Mark("foreign Healing label preserved",Tooltip.GetDamageTypeLabel(DamageType.Healing)=="custom");Tooltip.Label="Cura de Dano";
            var display=methods.Single(m=>m.Name=="ShowTooltip");
            other.Patch(display,prefix:new HarmonyMethod(typeof(CompositionHarmonyProbe).GetMethod("Competing",BindingFlags.Static|BindingFlags.NonPublic)));
            t.Raw="Lendário Varinha";Enter(t);Mark("foreign prefix output preserved",t.Drawn=="Outro formato");other.UnpatchSelf();
            h.UnpatchSelf();Enter(t);Mark("unpatched negative control exhibits both defects",t.Drawn=="Lendário Varinha"&&Tooltip.GetDamageTypeLabel(DamageType.Healing)=="Cura de Dano");
            Console.WriteLine("RESULT passed="+passed+" failed=0; SYNTHETIC CLR, game/UI/Mono NOT exercised");return 0;
        }
        catch(Exception ex){Console.WriteLine("FAIL "+ex);return 1;}
        finally{h.UnpatchSelf();other.UnpatchSelf();}
    }
}
