using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using HarmonyLib;

namespace Gumatos.RealmApi
{
    /// <summary>Instalação explícita, resolução total antes de patch e remoção somente do owner da API.</summary>
    public sealed class HookInstallation : IDisposable
    {
        private static HookInstallation? active;
        private readonly Harmony harmony;
        private readonly Dictionary<MethodBase,string> installed=new Dictionary<MethodBase,string>();
        private readonly Action<Exception>? report;
        private bool disposed;
        public IReadOnlyCollection<string> InstalledIds => installed.Values.ToArray();
        private HookInstallation(string owner, Action<Exception>? report) { harmony=new Harmony(owner); this.report=report; }

        /// <summary>Assembly e catálogo explícitos; consumidores normalmente não precisam chamar isso.</summary>
        public static HookInstallation Install(Assembly assembly, IEnumerable<HookDescriptor> descriptors, string owner, Action<Exception>? report=null)
        {
            if (active!=null) throw new InvalidOperationException("Há uma instalação ativa; remova-a antes de reinstalar");
            if (string.IsNullOrWhiteSpace(owner)) throw new ArgumentException("Owner vazio",nameof(owner));
            var resolved=descriptors.Select(d => (Descriptor:d, Method:d.Resolve(assembly))).ToArray();
            if(resolved.Select(x=>x.Descriptor.Id).Distinct().Count()!=resolved.Length ||
               resolved.Select(x=>x.Method).Distinct().Count()!=resolved.Length) throw new ArgumentException("IDs/alvos duplicados");
            foreach(var target in resolved)
                if (!((!target.Descriptor.IsStatic && target.Descriptor.ReturnType=="System.Void") ||
                      (target.Descriptor.IsStatic && target.Descriptor.ReturnType=="System.String")))
                    throw new NotSupportedException("Formato de postfix não suportado: "+target.Descriptor.Id);
            var session=new HookInstallation(owner,report);
            active=session;
            try
            {
                foreach(var target in resolved)
                {
                    session.installed.Add(target.Method,target.Descriptor.Id);
                    var postfix=typeof(HookInstallation).GetMethod(target.Descriptor.IsStatic ? nameof(StringPostfix) : nameof(VoidPostfix),BindingFlags.NonPublic|BindingFlags.Static);
                    session.harmony.Patch(target.Method,postfix:new HarmonyMethod(postfix));
                    var info=Harmony.GetPatchInfo(target.Method);
                    if(info==null || !info.Postfixes.Any(p=>p.owner==owner && p.PatchMethod==postfix))
                        throw new InvalidOperationException("Owner/postfix ausente: "+target.Descriptor.Id);
                }
                return session;
            }
            catch { session.Dispose(); throw; }
        }
        private static void VoidPostfix(MethodBase __originalMethod, object __instance, object[] __args) =>
            Notify(__originalMethod,__instance,__args,null);
        private static void StringPostfix(MethodBase __originalMethod, object[] __args, string __result) =>
            Notify(__originalMethod,null,__args,__result);
        private static void Notify(MethodBase method, object? instance, object?[] args, object? result)
        {
            var session=active;
            if(session==null || !session.installed.TryGetValue(method,out var id)) return;
            RealmHooks.Emit(id,instance,args,result,session.report);
        }
        /// <summary>Idempotente; não remove patches de outros mods nem subscriptions dos consumidores.</summary>
        public void Dispose()
        {
            if(disposed) return;
            harmony.UnpatchSelf();
            disposed=true;
            installed.Clear();
            if(ReferenceEquals(active,this)) active=null;
        }
    }
}
