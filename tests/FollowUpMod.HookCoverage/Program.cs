using System.Reflection;
using System.Runtime.Loader;

if (args.Length < 1) { Console.Error.WriteLine("uso: FollowUpMod.HookCoverage <FollowUpMod.dll> [dir de dependencias...]"); return 2; }

// A DLL do mod referencia BepInEx/Harmony/Assembly-CSharp. Para inspecionar ATRIBUTOS
// (e nao executar o plugin), resolvemos as dependencias a partir de lib/ e da pasta
// Managed do jogo -- sem copiar assembly do jogo para o repositorio.
var searchDirs = args.Skip(1).Where(Directory.Exists).ToArray();
AssemblyLoadContext.Default.Resolving += (context, name) =>
{
    var file = name.Name + ".dll";
    foreach (var dir in searchDirs)
    {
        var candidate = Path.Combine(dir, file);
        if (File.Exists(candidate)) return context.LoadFromAssemblyPath(Path.GetFullPath(candidate));
    }
    return null;
};

var asm = AssemblyLoadContext.Default.LoadFromAssemblyPath(Path.GetFullPath(args[0]));

static Type[] AllTypes(Assembly assembly)
{
    try { return assembly.GetTypes(); }
    catch (ReflectionTypeLoadException ex) { return ex.Types.Where(t => t != null).ToArray()!; }
}

const BindingFlags All = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance;
var types = AllTypes(asm);

var patchClasses = types
    .Where(t => t.GetCustomAttributes().Any(a => a.GetType().Name == "HarmonyPatch"))
    .Select(t => t.FullName).OrderBy(n => n).ToArray();

var hooks = types
    .SelectMany(t => t.GetMethods(All))
    .Where(m => m.GetCustomAttributes().Any(a => a.GetType().Name is "HarmonyPrefix" or "HarmonyPostfix" or "HarmonyTranspiler"))
    .Select(m => m.DeclaringType!.Name + "." + m.Name).OrderBy(n => n).ToArray();

var targets = types.SelectMany(t => t.GetMethods(All))
    .Count(m => m.GetCustomAttributes().Any(a => a.GetType().Name == "HarmonyTargetMethods"));

Console.WriteLine("PATCH_CLASSES=" + patchClasses.Length + " HOOK_METHODS=" + hooks.Length + " TARGET_METHODS=" + targets);
foreach (var c in patchClasses) Console.WriteLine("  class " + c);
foreach (var h in hooks) Console.WriteLine("  hook  " + h);

// Contrato EXATO (nao so contagem): 4 classes, 6 hooks e 4 alvos resolvidos por nome.
string[] expectedHooks =
{
    "HostAnnouncePatch.Postfix",
    "SaveGuardPatch.Postfix",
    "SaveGuardPatch.Prefix",
    "SelectionGatePatch.Postfix",
    "SelectionGatePatch.Prefix",
    "SessionEndPatch.Postfix",
};
string[] expectedClasses =
{
    "FollowUpMod.HostAnnouncePatch",
    "FollowUpMod.SaveGuardPatch",
    "FollowUpMod.SelectionGatePatch",
    "FollowUpMod.SessionEndPatch",
};
if (!hooks.SequenceEqual(expectedHooks) || !patchClasses.SequenceEqual(expectedClasses) || targets != 4)
{
    Console.WriteLine("FAIL cobertura de patches diferente do contrato");
    return 1;
}
Console.WriteLine("HOOKS_OK");
return 0;
