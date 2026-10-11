using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;

[assembly: InternalsVisibleTo("RealmApi.Hooks")]
[assembly: InternalsVisibleTo("RealmApi.Smoke")]

namespace Gumatos.RealmApi
{
    /// <summary>Identidade da API e do único alvo inspecionado. Não é compatibilidade universal.</summary>
    public static class ApiIdentity
    {
        public const string Guid = "com.gumatos.realmapi";
        public const string Name = "RealmApi";
        public const string Version = "0.1.0";
        public const int SteamAppId = 1330000;
        public const string GameVersion = "1.3.1";
        public const string SteamBuildId = "25240684";
        public const string AssemblySha256 = "8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a";

        /// <summary>Gate fail-closed: valores ausentes/divergentes não permitem hooks.</summary>
        public static bool Matches(string version, string sha256) =>
            string.Equals(version, GameVersion, StringComparison.Ordinal) &&
            string.Equals(sha256, AssemblySha256, StringComparison.OrdinalIgnoreCase);
    }

    /// <summary>Assinatura exata de um ponto de observação. Nomes de tipos são FullName.</summary>
    public sealed class HookDescriptor
    {
        public string Id { get; }
        public string TypeName { get; }
        public string MethodName { get; }
        public bool IsStatic { get; }
        public string ReturnType { get; }
        public IReadOnlyList<string> ParameterTypes { get; }
        public HookDescriptor(string id, string typeName, string methodName, bool isStatic, string returnType, params string[] parameters)
        {
            if (string.IsNullOrWhiteSpace(id)) throw new ArgumentException("Hook ID vazio", nameof(id));
            Id=id; TypeName=typeName; MethodName=methodName; IsStatic=isStatic; ReturnType=returnType;
            ParameterTypes=Array.AsReadOnly((string[])parameters.Clone());
        }

        /// <summary>Não usa short name, não escolhe overload arbitrário e não procura em outros assemblies.</summary>
        public MethodInfo Resolve(Assembly assembly)
        {
            var type=assembly.GetType(TypeName, false, false) ?? throw new MissingMemberException(TypeName);
            var matches=type.GetMethods(BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Instance|BindingFlags.Static|BindingFlags.DeclaredOnly)
                .Where(m=>m.Name==MethodName && m.IsStatic==IsStatic && m.ReturnType.FullName==ReturnType &&
                    m.GetParameters().Select(p=>p.ParameterType.FullName).SequenceEqual(ParameterTypes)).ToArray();
            if (matches.Length!=1) throw new MissingMethodException($"{Id}: esperado 1 alvo, encontrados {matches.Length}");
            return matches[0];
        }
    }

    /// <summary>Apenas estes quatro hooks são implementados na base 0.1.0. São postfixes observacionais.</summary>
    public static class HookCatalog
    {
        public static IReadOnlyList<HookDescriptor> All { get; } = Array.AsReadOnly(new[] {
            new HookDescriptor("game.awake", "Burst2Flame.Game", "Awake", false, "System.Void"),
            new HookDescriptor("ui.skill-tree.updated", "SkillTreeManager", "UpdateSkillTreeItems", false, "System.Void"),
            new HookDescriptor("ui.localized", "OptionsManager", "Localize", true, "System.String", "System.String", "LanguageGender", "Gender"),
            new HookDescriptor("combat.turn-started", "GameLogic", "StartNewTurn", false, "System.Void")
        });
    }

    /// <summary>Notificação depois do método. Arguments é cópia da lista, não cópia profunda dos objetos Unity.</summary>
    public sealed class HookNotification
    {
        public string HookId { get; }
        public object? Instance { get; }
        public IReadOnlyList<object?> Arguments { get; }
        public object? Result { get; }
        internal HookNotification(string id, object? instance, object?[] arguments, object? result)
        { HookId=id; Instance=instance; Arguments=Array.AsReadOnly((object?[])arguments.Clone()); Result=result; }
    }

    /// <summary>Subscriptions com remoção individual. Executa no thread do hook, nunca despacha Unity em worker.</summary>
    public sealed class Signal<T>
    {
        private readonly object gate=new object();
        private readonly Dictionary<long, Action<T>> listeners=new Dictionary<long, Action<T>>();
        private long next;
        public IDisposable Subscribe(Action<T> handler)
        {
            if (handler==null) throw new ArgumentNullException(nameof(handler));
            long id; lock(gate) { id=++next; listeners.Add(id,handler); }
            return new Subscription(()=> { lock(gate) listeners.Remove(id); });
        }
        internal void Publish(T value, Action<Exception>? report=null)
        {
            Action<T>[] snapshot; lock(gate) snapshot=listeners.Values.ToArray();
            foreach(var listener in snapshot) try { listener(value); }
                catch(Exception ex) { try { report?.Invoke(ex); } catch { /* logger não pode quebrar o jogo */ } }
        }
        private sealed class Subscription : IDisposable
        {
            private Action? remove;
            public Subscription(Action remove) { this.remove=remove; }
            public void Dispose() { System.Threading.Interlocked.Exchange(ref remove,null)?.Invoke(); }
        }
    }

    /// <summary>Bus observacional; consumidores não publicam eventos nem podem cancelar/mudar argumentos.</summary>
    public static class RealmHooks
    {
        public static Signal<HookNotification> Observed { get; } = new Signal<HookNotification>();
        internal static void Emit(string id, object? instance, object?[] arguments, object? result, Action<Exception>? report) =>
            Observed.Publish(new HookNotification(id,instance,arguments,result),report);
    }

    /// <summary>Acesso explícito somente a propriedades de leitura; sem cache de UnityEngine.Object.</summary>
    public static class RealmAccess
    {
        public static object? ReadProperty(Assembly assembly, string typeName, string propertyName, object? instance=null)
        {
            var type=assembly.GetType(typeName,false,false) ?? throw new MissingMemberException(typeName);
            var property=type.GetProperty(propertyName,BindingFlags.Public|BindingFlags.Static|BindingFlags.Instance|BindingFlags.DeclaredOnly)
                ?? throw new MissingMemberException(typeName,propertyName);
            var getter=property.GetGetMethod() ?? throw new MissingMethodException(typeName,propertyName);
            if (property.GetIndexParameters().Length!=0) throw new ArgumentException("Indexer não suportado");
            if (!getter.IsStatic && (instance==null || !type.IsInstanceOfType(instance))) throw new ArgumentException("Instância incompatível");
            return property.GetValue(getter.IsStatic ? null : instance);
        }
    }
}
