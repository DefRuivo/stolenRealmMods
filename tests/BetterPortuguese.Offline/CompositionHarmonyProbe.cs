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
public class ItemInfo { public string ItemName; }
public class ItemMod { public string name; }
public class Item
{
    public ItemInfo ItemInfo;
    public ItemMod PrefixMod;
    public string NativeName;
    public int Price, Armor;
    public ItemQuality Rarity;
    public int NameReads;
    public string ItemName { [MethodImpl(MethodImplOptions.NoInlining)] get { NameReads++; return NativeName; } }
}
public class TooltipOffsetInfo {} public class Character {} public struct ControlGlyphInfo {}
public enum DamageType { Physical, Healing, Fire, Cold }
public class Weapon : Item { public DamageType DamageType { get; set; } }
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
    public string BigText, FixtureDamageLine;
    public Tooltip Comparison;
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowTooltip(string title, string subtitle, Sprite icon, string description, TooltipOffsetInfo offset, Color color, Vector3? pos=null, bool showIcon=true, bool isItem=false, float alpha=1, ControlGlyphInfo? glyph=null, string footer=null, bool equipped=false) { Drawn=subtitle; Title=title; Description=description; }
    [MethodImpl(MethodImplOptions.NoInlining)] public void ShowItemTooltip(Item item, Transform hovering, TooltipOffsetInfo offset, Character character, bool showComp=true, bool fromLink=false, ControlGlyphInfo? glyph=null, string footer=null, Item comparison=null)
    {
        if (Nested) { Nested=false; ShowItemTooltip(new ItemInfo(),null); }
        ShowTooltip("TITLE",Raw,null,AppendItemMods(item,comparison),null,new Color());
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
    [MethodImpl(MethodImplOptions.NoInlining)] public string AppendItemMods(Item item, Item compItem=null)
    {
        if (FixtureDamageLine != null) return FixtureDamageLine;
        if (!(item is Weapon weapon)) return "DESCRIPTION";
        BigText="<color=#FFFFFF>7-11</color>";
        return "<color=#FFFFFF>"+GetDamageTypeLabel(weapon.DamageType)+"</color>\nBônus [0] — Dano Físico";
    }
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
        Console.OutputEncoding = new System.Text.UTF8Encoding(false);
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
                if(m.Name=="AppendItemMods" && M("PhysicalItemDescriptionPostfix")!=null)post="PhysicalItemDescriptionPostfix";
                if(m.Name=="ShowActionStatusTooltip" && M("EnterFortune")!=null){pre="EnterFortune";fin="LeaveFortune";}
                patch.Invoke(null,new object[]{h,m,pre,post,fin});
            }
            F("itemReady").SetValue(null,true);F("damageReady").SetValue(null,true);
            F("fortuneReady")?.SetValue(null,true);
            F("physicalDescriptionReady")?.SetValue(null,true);
            var itemNameTarget = typeof(Item).GetProperty(nameof(Item.ItemName)).GetGetMethod();
            if (M("ItemNamePostfix") != null)
            {
                patch.Invoke(null,new object[]{h,itemNameTarget,null,"ItemNamePostfix",null});
                F("itemNameReady").SetValue(null,true);
            }
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
            var weapon=new Weapon{DamageType=DamageType.Physical};
            void DrawWeapon() => t.ShowItemTooltip(weapon,null,null,null);
            string line(string label) => "<color=#FFFFFF>"+label+"</color>\nBônus [0] — Dano Físico";
            Tooltip.Label="Dano Físico";
            Mark("physical outside native item tooltip unchanged",Tooltip.GetDamageTypeLabel(DamageType.Physical)==Tooltip.Label);
            DrawWeapon(); Mark("physical item tooltip expected lowercase damage type; got "+t.Description,t.Description==line("Dano físico")&&t.BigText=="<color=#FFFFFF>7-11</color>"&&Depth==0);
            weapon.DamageType=DamageType.Fire; DrawWeapon(); Mark("other damage enum with identical incoming label unchanged",t.Description==line(Tooltip.Label));
            weapon.DamageType=DamageType.Cold; Tooltip.Label="Dano Frio"; DrawWeapon();
            Mark("cold weapon tooltip unchanged",t.Description==line("Dano Frio"));
            weapon.DamageType=DamageType.Healing; Tooltip.Label="Dano Cura"; DrawWeapon();
            Mark("healing weapon tooltip retains existing composition",t.Description==line("Cura por Dano"));
            weapon.DamageType=DamageType.Physical;
            Tooltip.Label="Dano Físico";
            foreach(var s in new[]{new Settings(active:false),new Settings(variant:Conjunto.Original),new Settings(valid:false)})
            {current=s;DrawWeapon();Mark("physical item tooltip blocked by settings "+s.Active+s.Valid+s.Variant,t.Description==line(Tooltip.Label));}
            current=new Settings();OptionsManager.CurrentLanguage=LanguageChoice.English;
            DrawWeapon();Mark("physical eligible-looking label in English untouched",t.Description==line(Tooltip.Label));
            OptionsManager.CurrentLanguage=LanguageChoice.PortugueseBrazil;
            foreach (string unrecognized in new[]{"Dano físico","Dano Físico Crítico","<b>Dano Físico</b>","Físico de Dano","Dano Físico ","Physical Damage",null})
            {Tooltip.Label=unrecognized; DrawWeapon();Mark("physical unexpected or already correct label untouched: "+unrecognized,t.Description==line(unrecognized));}
            foreach (string nonNative in new[]{"<color=#ABCDE>Dano Físico</color>\n", "<color=#FFFFFZ>Dano Físico</color>\n", "<color=#FFFFFFFF>Dano Físico</color>\n", "Header\n"+line("Dano Físico"),"<color=#FFFFFF>Dano Físico</color> extra"})
            {t.FixtureDamageLine=nonNative;DrawWeapon();Mark("physical does not touch a non-native first line",t.Description==nonNative);}
            t.FixtureDamageLine=line("Dano Físico"); Enter(t);
            Mark("nonweapon with identical native-looking prefix untouched",t.Description==t.FixtureDamageLine);
            t.FixtureDamageLine="<color=#aB12Ff>Dano Físico</color>\nrest"; DrawWeapon();
            Mark("physical exact native first line preserves any RGB case",t.Description=="<color=#aB12Ff>Dano físico</color>\nrest");
            t.FixtureDamageLine=null;
            var nativeDescription = methods.Single(m=>m.Name=="AppendItemMods");
            other.Patch(nativeDescription, prefix:new HarmonyMethod(typeof(CompositionHarmonyProbe).GetMethod(nameof(ReplaceNativeDescription), BindingFlags.Static | BindingFlags.NonPublic)));
            try
            {
                t.BigText="native method not called";
                DrawWeapon();
                Mark("physical skips a replacement from another Harmony owner; got "+t.Description,t.Description==ForeignDescription && t.BigText=="native method not called");
            }
            finally { other.UnpatchSelf(); }
            Tooltip.Label="Dano Físico";throwSettings=true;DrawWeapon();
            Mark("physical settings exception preserves native description",t.Description==line(Tooltip.Label)&&Depth==0);throwSettings=false;
            Tooltip.Label="Cura de Dano";
            var tunic = new Item { ItemInfo = new ItemInfo { ItemName = "Blood Mask Tunic" }, PrefixMod = new ItemMod { name = "Reinforced" }, NativeName = "Túnica da Máscara de Sangue Reforçado", Price = 1680, Armor = 4, Rarity = ItemQuality.Rare };
            var info = tunic.ItemInfo; var prefixMod = tunic.PrefixMod;
            string name = tunic.ItemName;
            Mark("QA05 observed feminine item expected Reforçada; got " + name, name == "Túnica da Máscara de Sangue Reforçada");
            Mark("QA05 only the returned name changes",ReferenceEquals(tunic.ItemInfo, info) && ReferenceEquals(tunic.PrefixMod,prefixMod) && tunic.NativeName=="Túnica da Máscara de Sangue Reforçado" && tunic.Price==1680 && tunic.Armor==4 && tunic.Rarity==ItemQuality.Rare);
            tunic.PrefixMod = new ItemMod { name = "Bolstered" };
            Mark("QA05 second native prefix with the same masculine PT value",tunic.ItemName=="Túnica da Máscara de Sangue Reforçada");
            foreach (var c in new[]{
                ("Bladed Buckler", "Wild", "Escudo com Lâmina Selvagem"),
                ("Stone-Cleaver", "Elusive", "Corta-Pedra Elusivo"),
                ("Summoner's Hat", "Trainer's", "Chapéu do Invocador do Treinador"),
                ("Scimitar", (string)null, "Cimitarra"),
                ("Blood Mask Tunic", (string)null, "Túnica da Máscara de Sangue Reforçado"),
                ("Unrelated", "Reinforced", "Túnica da Máscara de Sangue Reforçado"),
                ("Blood Mask Tunic", "ForeignAfix", "Túnica da Máscara de Sangue Reforçado"),
                ("Blood Mask Tunic", "Reinforced", "Túnica da Máscara de Sangue Reforçada"),
                ("Blood Mask Tunic", "Reinforced", "Reforçado Túnica da Máscara de Sangue"),
                ("Blood Mask Tunic", "Reinforced", "Túnica da Máscara de Sangue Reforçado do Treinador"),
                ("Blood Mask Tunic", "Reinforced", "Túnica da Máscara de Sangue Reforçado<color=#FF0099>*</color>"),
                ("Blood Mask Tunic", "Reinforced", (string)null) })
            {
                var control=new Item { ItemInfo=new ItemInfo { ItemName=c.Item1 }, PrefixMod=c.Item2==null ? null : new ItemMod {name=c.Item2}, NativeName=c.Item3 };
                Mark("QA05 out-of-scope item/output preserved: "+c.Item1+"/"+c.Item2+"/"+c.Item3,control.ItemName==c.Item3);
            }
            foreach (var s in new[]{new Settings(active:false),new Settings(variant:Conjunto.Original),new Settings(valid:false)})
            {current=s;Mark("QA05 setting preserves name "+s.Active+s.Valid+s.Variant,tunic.ItemName==tunic.NativeName);}
            current=new Settings();OptionsManager.CurrentLanguage=LanguageChoice.English;
            Mark("QA05 English gate preserves eligible-looking text",tunic.ItemName==tunic.NativeName);
            OptionsManager.CurrentLanguage=LanguageChoice.PortugueseBrazil;throwSettings=true;
            Mark("QA05 settings exception leaves native name untouched",tunic.ItemName==tunic.NativeName);throwSettings=false;
            other.Patch(itemNameTarget,prefix:new HarmonyMethod(typeof(CompositionHarmonyProbe).GetMethod(nameof(ReplaceItemName),BindingFlags.Static|BindingFlags.NonPublic)));
            try
            {
                int reads = tunic.NameReads;
                Mark("QA05 foreign prefix skips original and owns its text",tunic.ItemName==tunic.NativeName && tunic.NameReads==reads);
            }
            finally { other.UnpatchSelf(); }
            h.UnpatchSelf();Enter(t);Mark("unpatched negative control exhibits both defects",t.Drawn=="Lendário Varinha"&&Tooltip.GetDamageTypeLabel(DamageType.Healing)=="Cura de Dano");
            Console.WriteLine("RESULT passed="+passed+" failed=0; SYNTHETIC CLR, game/UI/Mono NOT exercised");return 0;
        }
        catch(Exception ex){Console.WriteLine("FAIL "+ex);return 1;}
        finally{h.UnpatchSelf();other.UnpatchSelf();}
    }
    private const string ForeignDescription = "<color=#FFFFFF>Dano Físico</color>\nDescrição de outro owner";
    private static bool ReplaceItemName(Item __instance, ref string __result) { __result=__instance.NativeName; return false; }
    private static bool ReplaceNativeDescription(ref string __result)
    {
        __result = ForeignDescription;
        return false;
    }
}
