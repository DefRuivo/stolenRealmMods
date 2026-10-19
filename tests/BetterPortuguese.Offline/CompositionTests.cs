using System;
using System.IO;
using System.Linq;
using Mono.Cecil;
using BetterPortuguese.Core;

internal static class CompositionTests
{
    private static void Check(bool yes) { if (!yes) throw new Exception("BP-COMP assertion"); }
    private static void Pair(string before, string after)
    {
        string result = Composition.ItemSubtitle(before, out string reason);
        Check(reason == null && result == after);
        Check(Composition.ItemSubtitle(result, out reason) == result && reason == null);
    }
    public static void Run(Action<string, Action> test, string repo, Catalog catalog)
    {
        // Independent examples, not computed by the same map/form selection as production.
        var cases = new[] {
            ("Lendário Varinha", "Lendária Varinha"), ("Raro Espada de 1M", "Rara Espada de 1M"),
            ("Mítico Espada 2M", "Mítica Espada 2M"), ("Lendário Armadura", "Lendária Armadura"),
            ("Raro Maça 1M", "Rara Maça 1M"), ("Mítico Maça 2M", "Mítica Maça 2M"),
            ("Lendário Arma de Haste", "Lendária Arma de Haste"), ("Lendário Arma de 1 Mão", "Lendária Arma de 1 Mão"),
            ("Raro Arma de 2M", "Rara Arma de 2M"), ("Raro Arma de Punho", "Rara Arma de Punho"),
            ("Lendário Cabeça", "Lendária Cabeça"), ("Raro Ferramenta", "Rara Ferramenta"),
            ("Mítico Mercadoria", "Mítica Mercadoria"), ("Lendário Escudo", "Lendário Escudo"),
            ("Mítico Cajado", "Mítico Cajado"), ("Raro Machado de 1M", "Raro Machado de 1M"),
            ("Lendário Machado de 2 Mãos", "Lendário Machado de 2 Mãos"), ("Raro Arco", "Raro Arco"),
            ("Lendário Anel", "Lendário Anel"), ("Mítico Amuleto", "Mítico Amuleto"),
            ("Raro Material", "Raro Material"), ("Raro Consumível", "Raro Consumível"),
            ("Lendário Arma", "Lendária Arma"), ("Comum Varinha", "Comum Varinha"),
            ("Incomum Varinha", "Incomum Varinha"), ("Raro Botas", "Raras Botas"),
            ("Comum Botas", "Comuns Botas"), ("Incomum Luvas", "Incomuns Luvas"),
            ("Lendário Luva", "Lendária Luva"), ("Mítico Capa", "Mítica Capa"),
            ("Lendário Adaga", "Lendária Adaga"), ("Raro Lança", "Rara Lança")
        };
        foreach (var pair in cases) test("BP-COMP agreement " + pair.Item1, () => Pair(pair.Item1, pair.Item2));
        test("BP-COMP main/common no adjective", () => Pair("Varinha", "Varinha"));
        test("BP-COMP exact header and requirements preserved", () => Pair("<color=#123ABC>III</color>\nLendário Varinha\n<color=#FF0000>Requer Nível 9</color>", "<color=#123ABC>III</color>\nLendária Varinha\n<color=#FF0000>Requer Nível 9</color>"));
        foreach (string text in new[] { null, "", "Legendary Wand", "lendário Varinha", "Lendário  Varinha", "Lendário Varinha ", "Lendário Orbe", "Épico Varinha", "<b>Lendário Varinha</b>", "Lendário Varinha\r\n", "Lendário Desarmado", "Lendário Nenhum", "Lendário Varinha\nRaro Escudo", "Varinha\nVarinha" })
        {
            string input = text;
            test("BP-COMP drift preserved " + (text ?? "null"), () => { Check(ReferenceEquals(Composition.ItemSubtitle(input, out string reason), input)); Check(reason != null); });
        }
        test("BP-COMP scope/settings gates", () => {
            Check(Composition.Enabled(new Settings(), true, out _));
            Check(Composition.Enabled(new Settings(integrateMods:false), true, out _));
            Check(!Composition.Enabled(new Settings(), false, out string r) && r != null);
            foreach (var s in new[] { null, new Settings(active:false), new Settings(variant:Conjunto.Original), new Settings(valid:false), new Settings(variant:(Conjunto)99) })
                Check(!Composition.Enabled(s, true, out r) && r != null);
        });
        test("BP-COMP Healing exact output and idempotence", () => {
            Check(Composition.DamageLabel(true, "Cura de Dano", out string r) == "Cura por Dano" && r == null);
            Check(Composition.DamageLabel(true, "Cura por Dano", out r) == "Cura por Dano" && r == null);
        });
        foreach (string text in new[] { null, "Healing Damage", "Cura de Dano Crítico", "Cura de Dano ", "<color=#00FF00>Cura de Dano</color>", "Dano de Cura", "custom" })
            test("BP-COMP Healing drift " + text, () => Check(Composition.DamageLabel(true, text, out string r) == text && r != null));
        test("BP-COMP other damage types untouched", () => {
            foreach (string text in new[] { "Cura de Dano", "Fogo de Dano", "Physical Damage", null })
                Check(Composition.DamageLabel(false, text, out string r) == text && r == null);
        });
        test("BP-COMP actual game contract SHA, enums and labels", () => {
            Check(Resources.Sha256(File.ReadAllBytes(Path.Combine(repo, "lib/Assembly-CSharp.dll"))) == Composition.AssemblySha256);
            using var module = ModuleDefinition.ReadModule(Path.Combine(repo,"lib/Assembly-CSharp.dll"));
            var tooltip = module.Types.Single(t=>t.FullName=="Tooltip");
            Check(tooltip.Methods.Count(m=>m.Name=="ShowItemTooltip")==2);
            foreach (var method in tooltip.Methods.Where(m=>m.Name=="ShowItemTooltip" || m.Name=="ShowTransmogTooltip"))
            {
                Check(method.Body.Instructions.Any(i=>i.Operand is MethodReference r && r.Name=="ShowTooltip"));
                Check(method.Body.Instructions.Any(i=>i.Operand is MethodReference r && r.Name=="LocalizeEnum"));
            }
            var label = tooltip.Methods.Single(m=>m.Name=="GetDamageTypeLabel");
            Check(label.IsStatic && label.ReturnType.FullName=="System.String" && label.Parameters.Single().ParameterType.FullName=="DamageType");
            Check(label.Body.Instructions.Any(i=>i.Operand is string s && s=="[damage type] Damage"));
            Check(label.Body.Instructions.Any(i=>i.Operand is MethodReference r && r.Name=="Replace"));
            Check(module.Types.Single(t=>t.FullName=="ItemQuality").Fields.Where(f=>f.HasConstant).Select(f=>f.Name).SequenceEqual(new[]{"Common","Uncommon","Rare","Legendary","Mythic"}));
            foreach (var type in new[]{"ItemType","EquipmentType"})
                foreach (var field in module.Types.Single(t=>t.FullName==type).Fields.Where(f=>f.HasConstant))
                {
                    if (field.Name=="None" || field.Name=="Unarmed") continue; // no noun: explicitly unsupported
                    string key = field.CustomAttributes.FirstOrDefault(a=>a.AttributeType.Name=="DescriptionAttribute")?.ConstructorArguments[0].Value as string ?? field.Name;
                    var record = catalog.Corrected.Records[key];
                    Check(record.Entries.Count==1 && Composition.Nouns.ContainsKey(record.Entries[0].Value));
                }
            Check(catalog.Corrected.Records["[damage type] Damage"].Entries[0].Value == "[damage type] de Dano");
            Check(catalog.Corrected.Records["Healing"].Entries[0].Value == "Cura");
        });
        test("BP-COMP plugin production hooks wired", () => {
            using var module = ModuleDefinition.ReadModule(Path.Combine(repo,"BetterPortuguese/bin/Release/netstandard2.1/BetterPortuguese.dll"));
            var runtime=module.Types.Single(t=>t.FullName=="BetterPortuguese.Runtime.CompositionPatches");
            var plugin=module.Types.Single(t=>t.FullName=="BetterPortuguese.Plugin");
            Check(plugin.Methods.Single(m=>m.Name=="Awake").Body.Instructions.Any(i=>i.Operand is MethodReference r && r.DeclaringType.Name==runtime.Name && r.Name=="Install"));
            Check(runtime.Fields.Single(f=>f.Name=="itemDepth").CustomAttributes.Any(a=>a.AttributeType.Name=="ThreadStaticAttribute"));
            Check(runtime.Methods.Single(m=>m.Name=="LeaveItem").ReturnType.FullName=="System.Exception");
            Check(!runtime.Methods.Any(m=>m.Body!=null && m.Body.Instructions.Any(i=>i.Operand is MethodReference r && r.Name.StartsWith("Unpatch"))));
        });
    }
}
