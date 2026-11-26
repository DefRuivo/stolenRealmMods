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
public enum ItemQuality { Common, Uncommon, Rare, Legendary, Mythic }
public enum StatusType { Buff, Fortune }
public enum PersistentDurationType { Normal }
public class ActionStatus {}
namespace Burst2Flame { public class ActionStatusInfo { public StatusType StatusType; public ItemQuality Rarity; } }
public class Tooltip
{
    public string Raw = "Lendário Varinha", Drawn;
    public string Title, Description, InnerDrawn;
    public bool Throw, Nested;
    public Tooltip Comparison;
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowTooltip(string title, string subtitle, Sprite icon, string description, TooltipOffsetInfo offset, Color color, Vector3? pos=null, bool showIcon=true, bool isItem=false, float alpha=1, ControlGlyphInfo? glyph=null, string footer=null, bool equipped=false) { Drawn=subtitle; Title=title; Description=description; }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowItemTooltip(Item item, Transform hovering, TooltipOffsetInfo offset, Character character, bool showComp=true, bool fromLink=false, ControlGlyphInfo? glyph=null, string footer=null, Item comparison=null)
    {
        if (Nested) { Nested=false; ShowItemTooltip(new ItemInfo(),null); }
        ShowTooltip("TITLE",Raw,null,"DESCRIPTION",null,new Color());
        if (Comparison!=null) Comparison.ShowTooltip("COMPARISON",Comparison.Raw,null,"",null,new Color());
        if (Throw) throw new InvalidOperationException("native failure");
    }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowItemTooltip(ItemInfo item, TooltipOffsetInfo offset) { ShowTooltip("TITLE",Raw,null,"",null,new Color()); }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowTransmogTooltip(ItemInfo item, TooltipOffsetInfo offset, ControlGlyphInfo? glyph=null, string footer=null) { ShowTooltip("TITLE",Raw,null,"",null,new Color()); }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowActionStatusTooltip(Burst2Flame.ActionStatusInfo actionStatusInfo, Character source, Character target, Item sourceItem, PersistentDurationType persistentDurationType, string footer="", float level=1f, bool fromLink=false, string header="", ActionStatus sourceStatus=null, string descriptionOverride=null)
    {
        if (Nested)
        {
            Nested=false;
            ShowActionStatusTooltip(new Burst2Flame.ActionStatusInfo { StatusType=StatusType.Buff }, source, target, sourceItem, persistentDurationType);
            InnerDrawn = Drawn;
        }
        if (Comparison != null) Comparison.ShowTooltip("OTHER",Raw,null,"OTHER DESCRIPTION",null,new Color());
        ShowTooltip("<color=#7EE9FFFF>Amuleto do Javali</color>",Raw,null,descriptionOverride ?? "Efeito [0] inalterado",null,new Color(),isItem:fromLink);
        if (Throw) throw new InvalidOperationException("native status failure");
    }
    public static string Label="Cura de Dano";
    [MethodImpl(MethodImplOptions.NoInlining)] public static string GetDamageTypeLabel(DamageType damageType) { return Label; }
}
// Deliberate API drift fixtures: same-typed strings swapped, and a renamed enum.
public class ReorderedTooltip
{
    public string Drawn, Title;
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowTooltip(string subtitle, string title, bool isItem=true) { Drawn=subtitle; Title=title; }
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
    static void Status(Tooltip t, ItemQuality quality, StatusType kind=StatusType.Fortune, bool asItem=false) =>
        t.ShowActionStatusTooltip(new Burst2Flame.ActionStatusInfo { StatusType=kind, Rarity=quality }, null,null,null,PersistentDurationType.Normal,fromLink:asItem);
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
            Mark("assembly drift rejected/logged before any hook",!(bool)F("itemReady").GetValue(null)&&!(bool)F("damageReady").GetValue(null)&&!(bool)F("fortuneReady").GetValue(null)&&logs.Any(s=>s.Contains("SHA-256 divergente")));
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
                if(m.Name=="ShowActionStatusTooltip" && M("EnterFortune")!=null){pre="EnterFortune";fin="LeaveFortune";}
                patch.Invoke(null,new object[]{h,m,pre,post,fin});
            }
            F("itemReady").SetValue(null,true);F("damageReady").SetValue(null,true);
            F("fortuneReady")?.SetValue(null,true);
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
            var fortune=new Tooltip();
            var tiers=new[]{("Comum Sorte","Fortuna comum"),("Incomum Sorte","Fortuna incomum"),("Raro Sorte","Fortuna rara"),("Lendário Sorte","Fortuna lendária"),("Mítico Sorte","Fortuna mítica")};
            fortune.Raw=tiers[2].Item1; Status(fortune,ItemQuality.Rare);
            Mark("native rare fortune: expected Fortuna rara; got "+fortune.Drawn,fortune.Drawn==tiers[2].Item2);
            Mark("fortune preserves title markup and description",fortune.Title=="<color=#7EE9FFFF>Amuleto do Javali</color>"&&fortune.Description=="Efeito [0] inalterado");
            for(int i=0;i<tiers.Length;i++)
            {
                fortune.Raw=tiers[i].Item1;Status(fortune,(ItemQuality)i);Mark("fortune tier "+i,fortune.Drawn==tiers[i].Item2);
                fortune.Raw=tiers[i].Item2;Status(fortune,(ItemQuality)i);Mark("fortune idempotence "+i,fortune.Drawn==tiers[i].Item2);
            }
            fortune.Raw="Raro Sorte";Status(fortune,ItemQuality.Rare,StatusType.Buff);Mark("other status untouched",fortune.Drawn==fortune.Raw);
            Status(fortune,ItemQuality.Rare,asItem:true);Mark("item draw under fortune caller untouched",fortune.Drawn==fortune.Raw);
            Status(fortune,ItemQuality.Mythic);Mark("wrong tier label untouched",fortune.Drawn==fortune.Raw);
            Status(fortune,(ItemQuality)99);Mark("unknown tier untouched",fortune.Drawn==fortune.Raw);
            fortune.Comparison=new Tooltip();Status(fortune,ItemQuality.Rare);Mark("other tooltip instance untouched",fortune.Drawn=="Fortuna rara"&&fortune.Comparison.Drawn==fortune.Raw);fortune.Comparison=null;
            fortune.Nested=true;Status(fortune,ItemQuality.Rare);Mark("nested non-Fortune untouched, outer scope restored",fortune.InnerDrawn=="Raro Sorte"&&fortune.Drawn=="Fortuna rara");
            fortune.Throw=true;try { Status(fortune,ItemQuality.Rare);Mark("exception lost",false); } catch(InvalidOperationException ex) { Mark("native status exception preserved",ex.Message=="native status failure"); } fortune.Throw=false;
            fortune.ShowTooltip("OTHER",fortune.Raw,null,"",null,new Color());Mark("no fortune scope leaks after exception",fortune.Drawn==fortune.Raw);
            foreach(string malformed in new[]{null,"Rare Fortune","Raro  Sorte","Raro Sorte ","Raro Sorte\nOutro","<b>Raro Sorte</b>"})
            { fortune.Raw=malformed;Status(fortune,ItemQuality.Rare);Mark("unrecognized fortune label untouched: "+malformed,fortune.Drawn==malformed); }
            fortune.Raw="Rare Fortune";OptionsManager.CurrentLanguage=LanguageChoice.English;Status(fortune,ItemQuality.Rare);Mark("English fortune untouched",fortune.Drawn==fortune.Raw);
            OptionsManager.CurrentLanguage=LanguageChoice.PortugueseBrazil;current=new Settings(variant:Conjunto.Original);fortune.Raw="Raro Sorte";Status(fortune,ItemQuality.Rare);Mark("original PT-BR fortune untouched",fortune.Drawn==fortune.Raw);current=new Settings();
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
