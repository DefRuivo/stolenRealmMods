using System.Reflection;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using Gumatos.RealmApi;
using Gumatos.RealmApi.Skills;
using HarmonyLib;
using Mono.Cecil;

internal static class Program
{
    private static int ran, failed;
    private static void Check(bool condition, string message="assertion") { if(!condition) throw new Exception(message); }
    private static void Throws<T>(Action action) where T:Exception { try { action(); } catch(T) { return; } throw new Exception("Esperado "+typeof(T).Name); }
    private static void Test(string name,Action action) { ran++; try { action(); Console.WriteLine("PASS "+name); } catch(Exception e) { failed++; Console.WriteLine("FAIL "+name+": "+e); } }
    private static void Main(string[] args)
    {
        string gamePath=args.Length>0 ? args[0] : "../../../lib/Assembly-CSharp.dll";
        string pluginPath=args.Length>1 ? args[1] : throw new ArgumentException("Informe o caminho da DLL do plugin para inspeção de metadados");
        var fixture=Assembly.GetExecutingAssembly();
        Test("managed-core-load",()=>Check(typeof(ApiIdentity).Assembly.GetName().Name=="RealmApi.Core"));
        Test("identity-positive",()=>Check(ApiIdentity.Matches("1.3.1",ApiIdentity.AssemblySha256)));
        Test("identity-wrong-version",()=>Check(!ApiIdentity.Matches("1.3.2",ApiIdentity.AssemblySha256)));
        Test("identity-wrong-hash",()=>Check(!ApiIdentity.Matches("1.3.1",new string('0',64))));
        Test("identity-null-fails-closed",()=>Check(!ApiIdentity.Matches(null!,null!)));
        Test("subscription-null-rejected",()=>Throws<ArgumentNullException>(()=>new Signal<int>().Subscribe(null!)));
        Test("subscription-dispose-idempotent",()=> { var s=new Signal<int>(); int n=0; var h=s.Subscribe(x=>n+=x); s.Publish(2); h.Dispose();h.Dispose();s.Publish(9);Check(n==2); });
        Test("subscriber-isolation",()=> { var s=new Signal<int>();int ok=0,errors=0;using var a=s.Subscribe(_=>throw new Exception());using var b=s.Subscribe(_=>ok++);s.Publish(0,_=>errors++);Check(ok==1&&errors==1); });
        Test("reporter-isolation",()=> {var s=new Signal<int>();using var a=s.Subscribe(_=>throw new Exception()); s.Publish(0,_=>throw new Exception());});
        Test("subscription-snapshot",()=> {var s=new Signal<int>();int n=0;IDisposable? second=null;using var first=s.Subscribe(_=>second?.Dispose());second=s.Subscribe(_=>n++);s.Publish(0);s.Publish(0);Check(n==1);});
        Test("notification-list-cloned",()=> {object?[] a={"original"};var n=new HookNotification("x",null,a,null);a[0]="mutated";Check((string)n.Arguments[0]! == "original");});
        Test("exact-qualified-type",()=>Check(HookCatalog.All[0].Resolve(fixture).DeclaringType==typeof(Burst2Flame.Game)));
        Test("absent-target-rejected",()=>Throws<MissingMemberException>(()=>new HookDescriptor("missing","Absent","M",false,"System.Void").Resolve(fixture)));
        Test("wrong-signature-rejected",()=>Throws<MissingMethodException>(()=>new HookDescriptor("bad","OptionsManager","Localize",true,"System.String","System.Int32").Resolve(fixture)));
        Test("static-property-read",()=>Check(RealmAccess.ReadProperty(fixture,"Burst2Flame.Game","Instance") is Burst2Flame.Game));
        Test("absent-property-rejected",()=>Throws<MissingMemberException>(()=>RealmAccess.ReadProperty(fixture,"Burst2Flame.Game","Absent")));
        Test("invalid-instance-rejected",()=>Throws<ArgumentException>(()=>RealmAccess.ReadProperty(fixture,"GameLogic","TurnCount",new object())));
        Test("actual-game-hash",()=> { using var sha=SHA256.Create(); var hash=string.Concat(sha.ComputeHash(File.ReadAllBytes(gamePath)).Select(b=>b.ToString("x2"))); Check(hash==ApiIdentity.AssemblySha256,"Assembly-CSharp hash diferente"); });
        Test("actual-game-hook-metadata",()=> {
            using var game=ModuleDefinition.ReadModule(gamePath);
            foreach(var d in HookCatalog.All) {
                var type=game.Types.Single(t=>t.FullName==d.TypeName);
                var found=type.Methods.Where(m=>m.Name==d.MethodName&&m.IsStatic==d.IsStatic&&m.ReturnType.FullName==d.ReturnType&&m.Parameters.Select(p=>p.ParameterType.FullName).SequenceEqual(d.ParameterTypes)).ToArray();
                Check(found.Length==1,d.Id);
            }
        });
        Test("plugin-attribute-and-version",()=> {
            using var p=ModuleDefinition.ReadModule(pluginPath);
            var plugin=p.Types.Single(t=>t.Name=="RealmApiPlugin");
            var attr=plugin.CustomAttributes.Single(a=>a.AttributeType.FullName=="BepInEx.BepInPlugin");
            Check((string)attr.ConstructorArguments[0].Value==ApiIdentity.Guid);
            Check((string)attr.ConstructorArguments[2].Value==ApiIdentity.Version);
            Check(p.Assembly.Name.Version.ToString()=="0.1.0.0");
        });
        Test("no-game-assembly-dependency",()=> {
            using var p=ModuleDefinition.ReadModule(pluginPath);
            Check(!p.AssemblyReferences.Any(a=>a.Name=="Assembly-CSharp"));
        });
        Test("missing-target-zero-patches",()=> {
            Throws<MissingMemberException>(()=>HookInstallation.Install(fixture,new[]{HookCatalog.All[0],new HookDescriptor("x","Absent","M",false,"System.Void")},"com.gumatos.realmapi.smoke.missing"));
            Check(Harmony.GetPatchInfo(HookCatalog.All[0].Resolve(fixture))?.Owners.Contains("com.gumatos.realmapi.smoke.missing")!=true);
        });
        Test("duplicate-target-rejected",()=>Throws<ArgumentException>(()=>HookInstallation.Install(fixture,new[]{HookCatalog.All[0],HookCatalog.All[0]},"com.gumatos.realmapi.smoke.dup")));
        Test("real-harmony-hooks-dispatch-and-cleanup",()=> {
            var received=new List<HookNotification>();int errors=0;
            using var bad=RealmHooks.Observed.Subscribe(_=>throw new Exception("fixture subscriber"));
            using var good=RealmHooks.Observed.Subscribe(received.Add);
            using var installation=HookInstallation.Install(fixture,HookCatalog.All,ApiIdentity.Guid,_=>errors++);
            Check(installation.InstalledIds.Count==4);
            Throws<InvalidOperationException>(()=>HookInstallation.Install(fixture,HookCatalog.All,"com.gumatos.realmapi.smoke.second"));
            var game=new Burst2Flame.Game();var tree=new SkillTreeManager();var logic=new GameLogic();
            game.InvokeAwake();tree.UpdateSkillTreeItems();var text=OptionsManager.Localize("hello",LanguageGender.None,Gender.None);logic.StartNewTurn();
            Check(received.Count==4&&errors==4,"Os 4 postfixes precisam responder");
            Check(ReferenceEquals(received[0].Instance,game));Check(received[2].Instance==null);
            Check((string)received[2].Arguments[0]! == "hello" && (string)received[2].Result! == text);
            Check(logic.TurnCount==1 && tree.Count==1 && text=="localized:hello","Sem mudança de resultado/argumentos");
            installation.Dispose();installation.Dispose();logic.StartNewTurn();Check(received.Count==4);
            foreach(var d in HookCatalog.All) Check(Harmony.GetPatchInfo(d.Resolve(fixture))?.Owners.Contains(ApiIdentity.Guid)!=true);
        });
        Test("foreign-owner-preserved",()=> {
            var method=HookCatalog.All[3].Resolve(fixture);var other=new Harmony("com.gumatos.realmapi.smoke.foreign");
            try {
                other.Patch(method,postfix:new HarmonyMethod(typeof(Program).GetMethod(nameof(ForeignPostfix),BindingFlags.NonPublic|BindingFlags.Static)));
                var session=HookInstallation.Install(fixture,HookCatalog.All,ApiIdentity.Guid);session.Dispose();
                Check(Harmony.GetPatchInfo(method)?.Owners.Contains(other.Id)==true);
            } finally {other.UnpatchSelf();}
        });
        // ================= API-R1-I2: familia UI (comportamental) =================
        // Alvos dos fixtures: mesmas assinaturas do jogo, sem UnityEngine (o smoke roda em net472,
        // e os assemblies Unity do alvo sao netstandard2.1: nao carregam aqui - medido, CS1705).
        UiHosts Hosts(object? gui=null,object? character=null,object? skillTree=null,object? menu=null) =>
            new UiHosts{GuiManager=gui,CurrentCharacterUi=character,SkillTreeManager=skillTree,MenuTabManager=menu};
        IDisposable BindFixture(bool mutation, UiHosts? hosts=null) { UiFamily.Bind(fixture,hosts ?? Hosts(new GUIManager(),new CurrentCharacterUI(),new SkillTreeManager(),new MenuTabManager()),mutation); return new Unbinder(); }
        var uiFamilies=new[]{UiRequirements.FamilyFactory,UiRequirements.FamilyActionBar,UiRequirements.FamilySkillTree,UiRequirements.FamilyMenu,UiRequirements.FamilyTooltip};
        var uiProbe=new Dictionary<string,Action>{
            [UiRequirements.FamilyFactory]=()=>UiOperations.FactoryHost(),
            [UiRequirements.FamilyActionBar]=()=>UiOperations.ActionBarRemove("x"),
            [UiRequirements.FamilySkillTree]=()=>UiOperations.SkillTreeAdd("t",SkillTree.Fire),
            [UiRequirements.FamilyMenu]=()=>UiOperations.MenuRemove("x"),
            [UiRequirements.FamilyTooltip]=()=>UiOperations.TooltipHide()};
        foreach(var family in uiFamilies)
        {
            var shortName=family.Substring(family.LastIndexOf('.')+1);
            Test("ui-"+shortName+"-target-present",()=> {
                using var scope=BindFixture(true);
                Check(UiFamily.IsBound,"vinculo");
                foreach(var r in UiRequirements.ForFamily(family)) Check(UiFamily.BoundRequirementIds.Contains(r.Id),r.Id);
            });
            Test("ui-"+shortName+"-target-absent",()=> {
                var member=UiRequirements.ForFamily(family).First(r=>r.Kind!=UiMemberKind.Host);
                Throws<MissingMemberException>(()=>member.Resolve(typeof(string).Assembly));
            });
            Test("ui-"+shortName+"-member-absent",()=> {
                var r=UiRequirements.ForFamily(family).First(x=>x.Kind!=UiMemberKind.Host);
                var bogus=new UiRequirement(r.Id+".bogus",r.FamilyType,r.TypeName,r.MemberName+"Bogus",r.Kind,r.IsStatic,r.ReturnType,r.ParameterTypes.ToArray());
                Throws<MissingMemberException>(()=>bogus.Resolve(fixture));
            });
            Test("ui-"+shortName+"-signature-divergent",()=> {
                var r=UiRequirements.ForFamily(family).First(x=>x.Kind!=UiMemberKind.Host);
                var mutated=r.Kind==UiMemberKind.Method
                    ? new UiRequirement(r.Id+".divergente",r.FamilyType,r.TypeName,r.MemberName,r.Kind,r.IsStatic,r.ReturnType,r.ParameterTypes.Concat(new[]{"System.Int32"}).ToArray())
                    : new UiRequirement(r.Id+".divergente",r.FamilyType,r.TypeName,r.MemberName,r.Kind,r.IsStatic,"System.Int32");
                Throws<MissingMethodException>(()=>mutated.Resolve(fixture));
            });
            Test("ui-"+shortName+"-unbound-fails-closed",()=> {
                UiFamily.Unbind();
                Throws<InvalidOperationException>(uiProbe[family]);
                UiFamily.Bind(fixture,Hosts(),true);   // sem hospedeiro o vinculo e possivel; a familia e que falha fechado
                Throws<InvalidOperationException>(uiProbe[family]);
            });
        }
        Test("ui-mutation-requires-optin",()=> {
            using var scope=BindFixture(false);
            foreach(var op in new Action[]{()=>UiOperations.ActionBarRemove("x"),()=>UiOperations.SkillTreeAdd("t",SkillTree.Fire),()=>UiOperations.SkillTreeRemove(SkillTree.Fire),()=>UiOperations.MenuRemove("x"),()=>UiOperations.TooltipHide()})
                Throws<InvalidOperationException>(op);
            Check(!UiOperations.SkillTreeHas(SkillTree.Fire),"consulta pura nao muta");
        });
        Test("ui-host-absent-fails-closed",()=> {
            using var scope=BindFixture(true,Hosts());
            Throws<InvalidOperationException>(()=>UiOperations.TooltipHide());
            Throws<InvalidOperationException>(()=>UiOperations.ActionBarRemove("x"));
        });
        Test("ui-host-wrong-type-rejected",()=> {
            UiFamily.Unbind();
            Throws<ArgumentException>(()=>UiFamily.Bind(fixture,Hosts(new SkillTreeManager()),true));
            Check(!UiFamily.IsBound,"vinculo invalido nao pode deixar estado");
        });
        Test("ui-failed-bind-is-atomic",()=> {
            using var scope=BindFixture(true);
            Throws<MissingMemberException>(()=>UiFamily.Bind(typeof(string).Assembly,Hosts(new GUIManager()),true));
            Check(UiFamily.IsBound,"Bind falho nao altera o vinculo vigente");
            Check(UiFamily.BoundRequirementIds.Count==UiRequirements.All.Count);
        });
        Test("ui-thread-guard",()=> {
            using var scope=BindFixture(true);
            Exception? captured=null;
            var thread=new System.Threading.Thread(()=> { try { UiOperations.TooltipHide(); } catch(Exception ex) { captured=ex; } });
            thread.Start(); thread.Join();
            Check(captured is InvalidOperationException,"uso fora do thread do vinculo deve falhar fechado");
        });
        Test("ui-unbind-clears-family-state",()=> {
            var hosts=Hosts(new GUIManager(),new CurrentCharacterUI(),new SkillTreeManager(),new MenuTabManager());
            var character=(CurrentCharacterUI)hosts.CurrentCharacterUi!;
            character.ActiveSkillbar.Available=true;
            using(var scope=BindFixture(true,hosts)) UiOperations.ActionBarAdd("a",null,null);
            Check(character.ActiveSkillbar.Refreshes==1,"delegou RefreshSkillBar");
            UiFamily.Unbind();
            Check(!UiFamily.IsBound && UiOperations.ActionBarCount==0 && UiOperations.SkillTreeTabCount==0 && UiOperations.MenuTabCount==0,"Unbind zera estado das familias");
        });
        Test("ui-tooltip-delegation-1para1",()=> {
            var gui=new GUIManager();
            using var scope=BindFixture(true,Hosts(gui));
            Check(UiOperations.TooltipRequested==null,"estado inicial sem pedido");
            UiOperations.TooltipShow("titulo","descricao",null);
            Check(UiOperations.TooltipRequested!=null && UiOperations.TooltipRequested!.Title=="titulo","pedido registrado");
            UiOperations.TooltipHide();
            Check(gui.tooltip.Hides==1,"Tooltip::HideTooltip chamado no hospedeiro");
            Check(UiOperations.TooltipRequested==null,"pedido limpo");
        });
        Test("ui-action-bar-delegation",()=> {
            var hosts=Hosts(new GUIManager(),new CurrentCharacterUI(),new SkillTreeManager(),new MenuTabManager());
            var bar=((CurrentCharacterUI)hosts.CurrentCharacterUi!).ActiveSkillbar;
            using var scope=BindFixture(true,hosts);
            Throws<InvalidOperationException>(()=>UiOperations.ActionBarAdd("a",null,null));   // HasAvailableSlot=false -> falha fechado
            Check(UiOperations.ActionBarCount==0,"nao registrou sem slot");
            bar.Available=true;
            UiOperations.ActionBarAdd("a",null,null);
            Check(UiOperations.ActionBarHas("a") && bar.Refreshes==1,"registrou e delegou RefreshSkillBar");
            Throws<ArgumentException>(()=>UiOperations.ActionBarAdd("a",null,null));
            UiOperations.ActionBarUpdateIcon("a",null);
            Check(bar.Refreshes==2);
            UiOperations.ActionBarRemove("a");
            Check(!UiOperations.ActionBarHas("a") && bar.Refreshes==3);
            Throws<InvalidOperationException>(()=>UiOperations.ActionBarRemove("a"));
        });
        Test("ui-skill-tree-delegation",()=> {
            var hosts=Hosts(new GUIManager(),new CurrentCharacterUI(),new SkillTreeManager(),new MenuTabManager());
            var manager=(SkillTreeManager)hosts.SkillTreeManager!;
            using var scope=BindFixture(true,hosts);
            SkillTreeManager.IsNotNullAndIsActive=false;
            Throws<InvalidOperationException>(()=>UiOperations.SkillTreeAdd("t",SkillTree.Fire));
            Check(manager.Count==0,"arvore inativa nao registra");
            SkillTreeManager.IsNotNullAndIsActive=true;
            Check(!UiOperations.SkillTreeHas(SkillTree.Fire));
            UiOperations.SkillTreeAdd("t",SkillTree.Fire);
            Check(UiOperations.SkillTreeHas(SkillTree.Fire) && manager.Count==1,"registrou e delegou UpdateSkillTreeItems");
            Throws<ArgumentException>(()=>UiOperations.SkillTreeAdd("t",SkillTree.Fire));
            Throws<System.ArgumentOutOfRangeException>(()=>UiOperations.SkillTreeAdd("t",(SkillTree)99));
            UiOperations.SkillTreeRemove(SkillTree.Fire);
            Check(!UiOperations.SkillTreeHas(SkillTree.Fire) && manager.Count==2);
            Throws<InvalidOperationException>(()=>UiOperations.SkillTreeRemove(SkillTree.Fire));
        });
        Test("ui-menu-delegation",()=> {
            var hosts=Hosts(new GUIManager(),new CurrentCharacterUI(),new SkillTreeManager(),new MenuTabManager());
            var menu=(MenuTabManager)hosts.MenuTabManager!;
            using var scope=BindFixture(true,hosts);
            UiOperations.MenuAdd("t",null,null);
            Check(UiOperations.MenuHas("t") && menu.Refreshes==1,"registrou e delegou RefreshSelected");
            Throws<ArgumentException>(()=>UiOperations.MenuAdd("t",null,null));
            UiOperations.MenuRemove("t");
            Check(!UiOperations.MenuHas("t") && menu.Refreshes==2);
            Throws<InvalidOperationException>(()=>UiOperations.MenuRemove("t"));
        });
        Test("ui-public-surface-in-plugin-metadata",()=> {
            // Os tipos publicos da familia vivem em RealmApi.dll (netstandard2.1): o CLR do smoke (net472) NAO
            // carrega esse assembly (referencia netstandard 2.1 - medido). A leitura e por METADADOS, como o
            // teste do atributo do plugin. A igualdade de assinatura x inventario e a do conferidor
            // `api/tools/check_ui_contract.py` (evidencia em api/docs/ui-contract-diff.json).
            using var plugin=ModuleDefinition.ReadModule(pluginPath);
            var expected=new Dictionary<string,int>{{"UIFactory",11},{"ActionBarUI",3},{"SkillTreeUI",3},{"MenuUI",2},{"TooltipHelper",2}};
            foreach(var pair in expected)
            {
                var type=plugin.Types.SingleOrDefault(t=>t.FullName=="Gumatos.RealmApi.UI."+pair.Key);
                Check(type!=null,"tipo ausente no plugin: "+pair.Key);
                var methods=type!.Methods.Where(m=>m.IsPublic && m.IsStatic && !m.IsGetter && !m.IsSetter && !m.IsConstructor).ToArray();
                Check(methods.Length==pair.Value,$"{pair.Key}: esperado {pair.Value} metodos publicos estaticos, encontrados {methods.Length}");
                Check(methods.All(m=>!m.HasBody || m.Body.Instructions.Count>1),pair.Key+": metodo vazio (stub silencioso)");
            }
        });
        Test("actual-game-ui-requirements-metadata",()=> {
            using var game=ModuleDefinition.ReadModule(gamePath);
            var all=new List<TypeDefinition>();
            void Flatten(IEnumerable<TypeDefinition> types) { foreach(var t in types) { all.Add(t); Flatten(t.NestedTypes); } }
            Flatten(game.Types);
            foreach(var requirement in UiRequirements.All)
            {
                var type=all.SingleOrDefault(t=>t.FullName==requirement.TypeName);
                Check(type!=null,requirement.Id+": tipo ausente "+requirement.TypeName);
                if(requirement.Kind==UiMemberKind.Host) continue;
                var found=requirement.Kind switch {
                    UiMemberKind.Method=>type!.Methods.Where(m=>m.Name==requirement.MemberName && m.IsStatic==requirement.IsStatic && m.ReturnType.FullName==requirement.ReturnType && m.Parameters.Select(p=>p.ParameterType.FullName).SequenceEqual(requirement.ParameterTypes)).Count(),
                    UiMemberKind.Property=>type!.Properties.Where(p=>p.Name==requirement.MemberName && p.PropertyType.FullName==requirement.ReturnType && ((p.GetMethod?.IsStatic??p.SetMethod?.IsStatic)==requirement.IsStatic)).Count(),
                    _=>type!.Fields.Where(f=>f.Name==requirement.MemberName && f.IsStatic==requirement.IsStatic && f.FieldType.FullName==requirement.ReturnType).Count() };
                Check(found==1,requirement.Id+": esperado 1 alvo, encontrados "+found);
            }
        });
        UiFamily.Unbind();
        Console.WriteLine($"Ran {ran} tests; failures: {failed}");
        Console.WriteLine("NAO_EXERCITADO: BepInEx/Unity runtime, gameplay, saves, multiplayer; somente CLR fixtures + metadados locais.");
        Environment.ExitCode=failed==0 ? 0 : 1;
    }
    private static void ForeignPostfix() { }
}

// Fixtures artificiais: testam Harmony no CLR, não simulam um jogo real nem seus resultados.
public class Game { public void WrongGame() { } }
namespace Burst2Flame {
    public class Game {
        public static Game Instance {get;}=new Game();
        [MethodImpl(MethodImplOptions.NoInlining)] private void Awake() { }
        [MethodImpl(MethodImplOptions.NoInlining)] public void InvokeAwake()=>Awake();
    }
}
public enum LanguageGender { None }
public enum Gender { None }
public class SkillTreeManager {
    public int Count;
    public static bool IsNotNullAndIsActive {get;set;} = true;
    [MethodImpl(MethodImplOptions.NoInlining)] public void UpdateSkillTreeItems()=>Count++;
}
public class GameLogic { public int TurnCount {get;private set;} [MethodImpl(MethodImplOptions.NoInlining)] public void StartNewTurn()=>TurnCount++; }
public class OptionsManager { [MethodImpl(MethodImplOptions.NoInlining)] public static string Localize(string original,LanguageGender languageGender,Gender characterGender)=>"localized:"+original; }

// Fixtures da familia UI (API-R1-I2): nomes e assinaturas iguais aos alvos do jogo medidos em
// lib/Assembly-CSharp.dll; sem UnityEngine, para poderem rodar no CLR do smoke.
public class Tooltip { public int Hides; [MethodImpl(MethodImplOptions.NoInlining)] public void HideTooltip()=>Hides++; }
public class GUIManager {
    private static GUIManager? self;
    public static GUIManager instance { get { self = self ?? new GUIManager(); return self; } set { self = value; } }
    public Tooltip tooltip = new Tooltip();
}
public class Skillbar {
    public bool Available;
    public int Refreshes;
    [MethodImpl(MethodImplOptions.NoInlining)] public bool HasAvailableSlot()=>Available;
    [MethodImpl(MethodImplOptions.NoInlining)] public void RefreshSkillBar()=>Refreshes++;
}
public class CurrentCharacterUI {
    public static CurrentCharacterUI Instance {get;set;} = new CurrentCharacterUI();
    public Skillbar ActiveSkillbar {get;} = new Skillbar();
}
public class MenuTabManager { public int Refreshes; [MethodImpl(MethodImplOptions.NoInlining)] public void RefreshSelected()=>Refreshes++; }
public sealed class Unbinder : IDisposable { public void Dispose()=>UiFamily.Unbind(); }
