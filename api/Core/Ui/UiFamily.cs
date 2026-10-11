using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading;
using Gumatos.RealmApi.Skills;

[assembly: System.Runtime.CompilerServices.InternalsVisibleTo("RealmApi")]

namespace Gumatos.RealmApi
{
    /// <summary>Natureza de um requisito da familia UI: um membro do jogo ou um hospedeiro fornecido pelo consumidor.</summary>
    public enum UiMemberKind { Host, Method, Property, Field }

    /// <summary>
    /// Requisito exato da familia UI sobre o assembly do jogo. Mesma regra de exatidao do `HookDescriptor.Resolve`
    /// (api/Core/Contracts.cs): tipo por FullName, membro por nome + estaticidade + tipo de retorno + lista de parametros
    /// na ordem. Nao escolhe overload arbitrario e nao procura em outros assemblies.
    /// </summary>
    public sealed class UiRequirement
    {
        public string Id { get; }
        /// <summary>Tipo da familia UI (namespace Gumatos.RealmApi.UI) que depende deste requisito.</summary>
        public string FamilyType { get; }
        public UiMemberKind Kind { get; }
        public string TypeName { get; }
        public string MemberName { get; }
        public bool IsStatic { get; }
        public string ReturnType { get; }
        public IReadOnlyList<string> ParameterTypes { get; }
        /// <summary>Propriedade de `UiHosts` que entrega o objeto do hospedeiro (somente Kind==Host).</summary>
        public string HostSelector { get; }

        public UiRequirement(string id, string familyType, string typeName, string memberName, UiMemberKind kind,
            bool isStatic, string returnType, params string[] parameters)
        {
            if (string.IsNullOrWhiteSpace(id)) throw new ArgumentException("Requisito sem ID", nameof(id));
            if (string.IsNullOrWhiteSpace(familyType)) throw new ArgumentException("Requisito sem familia", nameof(familyType));
            if (string.IsNullOrWhiteSpace(typeName)) throw new ArgumentException("Requisito sem tipo", nameof(typeName));
            if (kind != UiMemberKind.Host && string.IsNullOrWhiteSpace(memberName))
                throw new ArgumentException("Requisito de membro sem nome", nameof(memberName));
            Id = id; FamilyType = familyType; Kind = kind; TypeName = typeName; MemberName = memberName;
            IsStatic = isStatic; ReturnType = returnType; ParameterTypes = Array.AsReadOnly((string[])parameters.Clone());
            HostSelector = string.Empty;
        }

        private UiRequirement(string id, string familyType, string typeName, string hostSelector)
        {
            Id = id; FamilyType = familyType; Kind = UiMemberKind.Host; TypeName = typeName; MemberName = string.Empty;
            IsStatic = false; ReturnType = string.Empty; ParameterTypes = Array.AsReadOnly(Array.Empty<string>());
            HostSelector = hostSelector;
        }

        /// <summary>Hospedeiro: o tipo precisa existir no jogo; o objeto vem do consumidor em `UiHosts`.</summary>
        public static UiRequirement Host(string id, string familyType, string typeName, string hostSelector) =>
            new UiRequirement(id, familyType, typeName, hostSelector);

        /// <summary>Resolve o tipo do jogo; ausente e falha fechada (nao devolve null).</summary>
        public Type ResolveType(Assembly assembly)
        {
            if (assembly == null) throw new ArgumentNullException(nameof(assembly));
            return assembly.GetType(TypeName, false, false) ?? throw new MissingMemberException(TypeName);
        }

        /// <summary>Resolve o membro exato; ausente = MissingMemberException, mais de um/nenhum candidato com o membro presente = MissingMethodException.</summary>
        public MemberInfo Resolve(Assembly assembly)
        {
            var type = ResolveType(assembly);
            if (Kind == UiMemberKind.Host) throw new InvalidOperationException("Requisito de hospedeiro nao resolve membro: " + Id);
            MemberInfo[] matches;
            switch (Kind)
            {
                case UiMemberKind.Method:
                    matches = type.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly)
                        .Where(m => m.Name == MemberName && m.IsStatic == IsStatic && m.ReturnType.FullName == ReturnType &&
                            m.GetParameters().Select(p => p.ParameterType.FullName).SequenceEqual(ParameterTypes)).Cast<MemberInfo>().ToArray();
                    break;
                case UiMemberKind.Property:
                    matches = type.GetProperties(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly)
                        .Where(p => p.Name == MemberName && p.GetIndexParameters().Length == 0 && p.PropertyType.FullName == ReturnType &&
                            (p.GetGetMethod(true)?.IsStatic == IsStatic || p.GetSetMethod(true)?.IsStatic == IsStatic)).Cast<MemberInfo>().ToArray();
                    break;
                case UiMemberKind.Field:
                    matches = type.GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly)
                        .Where(f => f.Name == MemberName && f.IsStatic == IsStatic && f.FieldType.FullName == ReturnType).Cast<MemberInfo>().ToArray();
                    break;
                default:
                    throw new InvalidOperationException("Natureza desconhecida: " + Kind);
            }
            if (matches.Length != 1) throw new MissingMethodException($"{Id}: esperado 1 alvo, encontrados {matches.Length}");
            return matches[0];
        }
    }

    /// <summary>Estados de verdade do jogo entregues pelo consumidor. Cada familia exige o seu; nulo = familia indisponivel (falha fechada).</summary>
    public sealed class UiHosts
    {
        public object? GuiManager { get; set; }
        public object? CurrentCharacterUi { get; set; }
        public object? SkillTreeManager { get; set; }
        public object? MenuTabManager { get; set; }
        public static UiHosts Empty { get; } = new UiHosts();
    }

    /// <summary>
    /// Catalogo de requisitos da familia UI. Todo alvo aqui foi medido em `lib/Assembly-CSharp.dll`
    /// (ver api/docs/ui-family-targets.json e o teste `actual-game-ui-requirements-metadata` do smoke).
    /// </summary>
    public static class UiRequirements
    {
        public const string FamilyFactory = "Gumatos.RealmApi.UI.UIFactory";
        public const string FamilyActionBar = "Gumatos.RealmApi.UI.ActionBarUI";
        public const string FamilySkillTree = "Gumatos.RealmApi.UI.SkillTreeUI";
        public const string FamilyMenu = "Gumatos.RealmApi.UI.MenuUI";
        public const string FamilyTooltip = "Gumatos.RealmApi.UI.TooltipHelper";

        public static IReadOnlyList<UiRequirement> All { get; } = Array.AsReadOnly(new[] {
            // UIFactory: a operacao muta a arvore de UI do jogo; exige o hospedeiro da UI.
            UiRequirement.Host("ui.factory.host", FamilyFactory, "GUIManager", nameof(UiHosts.GuiManager)),
            new UiRequirement("ui.factory.instance", FamilyFactory, "GUIManager", "instance", UiMemberKind.Property, true, "GUIManager"),
            // ActionBarUI: barra de acao do personagem atual.
            UiRequirement.Host("ui.action-bar.host", FamilyActionBar, "CurrentCharacterUI", nameof(UiHosts.CurrentCharacterUi)),
            new UiRequirement("ui.action-bar.instance", FamilyActionBar, "CurrentCharacterUI", "Instance", UiMemberKind.Property, true, "CurrentCharacterUI"),
            new UiRequirement("ui.action-bar.skillbar", FamilyActionBar, "CurrentCharacterUI", "ActiveSkillbar", UiMemberKind.Property, false, "Skillbar"),
            new UiRequirement("ui.action-bar.probe", FamilyActionBar, "Skillbar", "HasAvailableSlot", UiMemberKind.Method, false, "System.Boolean"),
            new UiRequirement("ui.action-bar.refresh", FamilyActionBar, "Skillbar", "RefreshSkillBar", UiMemberKind.Method, false, "System.Void"),
            // SkillTreeUI: arvore de habilidades carregada.
            UiRequirement.Host("ui.skill-tree.host", FamilySkillTree, "SkillTreeManager", nameof(UiHosts.SkillTreeManager)),
            new UiRequirement("ui.skill-tree.probe", FamilySkillTree, "SkillTreeManager", "IsNotNullAndIsActive", UiMemberKind.Property, true, "System.Boolean"),
            new UiRequirement("ui.skill-tree.refresh", FamilySkillTree, "SkillTreeManager", "UpdateSkillTreeItems", UiMemberKind.Method, false, "System.Void"),
            // MenuUI: gerenciador de abas de menu.
            UiRequirement.Host("ui.menu.host", FamilyMenu, "MenuTabManager", nameof(UiHosts.MenuTabManager)),
            new UiRequirement("ui.menu.instance", FamilyMenu, "MenuTabManager", "RefreshSelected", UiMemberKind.Method, false, "System.Void"),
            // TooltipHelper: tooltip nativo do jogo, alcancado por GUIManager.instance.tooltip.
            UiRequirement.Host("ui.tooltip.host", FamilyTooltip, "GUIManager", nameof(UiHosts.GuiManager)),
            new UiRequirement("ui.tooltip.instance", FamilyTooltip, "GUIManager", "instance", UiMemberKind.Property, true, "GUIManager"),
            new UiRequirement("ui.tooltip.link", FamilyTooltip, "GUIManager", "tooltip", UiMemberKind.Field, false, "Tooltip"),
            new UiRequirement("ui.tooltip.hide", FamilyTooltip, "Tooltip", "HideTooltip", UiMemberKind.Method, false, "System.Void"),
        });

        public static IReadOnlyList<UiRequirement> ForFamily(string familyType)
        {
            if (string.IsNullOrWhiteSpace(familyType)) throw new ArgumentException("Familia vazia", nameof(familyType));
            return Array.AsReadOnly(All.Where(r => r.FamilyType == familyType).ToArray());
        }
    }

    /// <summary>
    /// Vinculo explicito da familia UI (comportamental) com o jogo. Separada do barramento observacional
    /// (`RealmHooks.Observed`): aqui se MUTA UI, entao ha (1) vinculo explicito, (2) opt-in de mutacao e
    /// (3) guarda de thread. Alvo ausente ou divergente derruba o vinculo inteiro — nunca ha vinculo parcial
    /// e nunca ha no-op silencioso.
    /// </summary>
    public static class UiFamily
    {
        private static readonly object gate = new object();
        private static Dictionary<string, MemberInfo> members = new Dictionary<string, MemberInfo>();
        private static Dictionary<string, object?> hosts = new Dictionary<string, object?>();
        private static int threadId;
        private static bool mutation;

        /// <summary>Verdadeiro somente depois de um `Bind` integral ter dado certo.</summary>
        public static bool IsBound { get; private set; }
        /// <summary>Mutacao de UI habilitada explicitamente (`Bind(..., allowMutation:true)`).</summary>
        public static bool MutationEnabled { get { lock (gate) return mutation; } }
        /// <summary>Thread (o thread principal do Unity) que fez o vinculo.</summary>
        public static int BoundThreadId { get { lock (gate) return threadId; } }
        public static IReadOnlyCollection<string> BoundRequirementIds { get { lock (gate) return members.Keys.Concat(hosts.Keys).OrderBy(x => x, StringComparer.Ordinal).ToArray(); } }

        /// <summary>
        /// Resolve TODOS os requisitos do catalogo contra o assembly do jogo e guarda os hospedeiros fornecidos.
        /// Qualquer requisito ausente/divergente lanca e nada fica vinculado (fail-closed, sem estado parcial).
        /// </summary>
        public static void Bind(Assembly gameAssembly, UiHosts hosts, bool allowMutation = false)
        {
            if (gameAssembly == null) throw new ArgumentNullException(nameof(gameAssembly));
            if (hosts == null) throw new ArgumentNullException(nameof(hosts));

            var resolvedMembers = new Dictionary<string, MemberInfo>();
            var resolvedHosts = new Dictionary<string, object?>();
            foreach (var requirement in UiRequirements.All)
            {
                if (requirement.Kind == UiMemberKind.Host)
                {
                    requirement.ResolveType(gameAssembly);
                    var property = typeof(UiHosts).GetProperty(requirement.HostSelector)
                        ?? throw new InvalidOperationException("Seletor de hospedeiro desconhecido: " + requirement.HostSelector);
                    var value = property.GetValue(hosts);
                    if (value != null && value.GetType().FullName != requirement.TypeName)
                        throw new ArgumentException($"Hospedeiro divergente em {requirement.Id}: {value.GetType().FullName} != {requirement.TypeName}");
                    resolvedHosts.Add(requirement.Id, value);
                }
                else resolvedMembers.Add(requirement.Id, requirement.Resolve(gameAssembly));
            }

            lock (gate)
            {
                members = resolvedMembers;
                UiFamily.hosts = resolvedHosts;
                threadId = Thread.CurrentThread.ManagedThreadId;
                mutation = allowMutation;
                IsBound = true;
            }
            UiOperations.Reset();
        }

        /// <summary>Idempotente. Limpa vinculo, hospedeiros e o estado das cinco familias.</summary>
        public static void Unbind()
        {
            lock (gate)
            {
                members = new Dictionary<string, MemberInfo>();
                hosts = new Dictionary<string, object?>();
                mutation = false;
                IsBound = false;
            }
            UiOperations.Reset();
        }

        /// <summary>Guarda comum: vinculo + opt-in de mutacao + thread. Nunca e no-op.</summary>
        internal static void Require(string familyType, bool mutates)
        {
            if (!IsBound) throw new InvalidOperationException($"Familia {familyType} exige UiFamily.Bind(assembly, hosts) antes de qualquer chamada");
            if (mutates && !MutationEnabled) throw new InvalidOperationException($"Familia {familyType} muta UI: o vinculo precisa de allowMutation:true");
            if (threadId != Thread.CurrentThread.ManagedThreadId)
                throw new InvalidOperationException($"Familia {familyType} so pode ser usada no thread do vinculo (main thread do Unity); vinculada em {threadId}");
        }

        /// <summary>Hospedeiro fornecido pelo consumidor; ausente = familia indisponivel (fail-closed).</summary>
        internal static object Host(string requirementId)
        {
            if (!hosts.TryGetValue(requirementId, out var value) || value == null)
                throw new InvalidOperationException($"Hospedeiro ausente: {requirementId} (nada foi assumido nem ignorado)");
            return value;
        }

        internal static bool HasHost(string requirementId) => hosts.TryGetValue(requirementId, out var v) && v != null;

        private static MemberInfo Member(string requirementId) =>
            members.TryGetValue(requirementId, out var member)
                ? member
                : throw new InvalidOperationException("Requisito nao resolvido: " + requirementId);

        /// <summary>Le/invoca o membro resolvido. Metodo sem parametros, propriedade ou campo. Nada de cache de objetos Unity.</summary>
        internal static object? Read(string requirementId, object? instance = null)
        {
            var member = Member(requirementId);
            switch (member)
            {
                case MethodInfo method:
                    if (!method.IsStatic && instance == null) throw new InvalidOperationException("Alvo de instancia sem hospedeiro: " + requirementId);
                    if (method.GetParameters().Length != 0) throw new InvalidOperationException("Leitura sem argumentos exige metodo sem parametros: " + requirementId);
                    return method.Invoke(method.IsStatic ? null : instance, null);
                case PropertyInfo property:
                    var getter = property.GetGetMethod(true) ?? throw new MissingMethodException(requirementId + ": sem getter");
                    if (!getter.IsStatic && instance == null) throw new InvalidOperationException("Alvo de instancia sem hospedeiro: " + requirementId);
                    return property.GetValue(getter.IsStatic ? null : instance);
                case FieldInfo field:
                    if (!field.IsStatic && instance == null) throw new InvalidOperationException("Alvo de instancia sem hospedeiro: " + requirementId);
                    return field.GetValue(field.IsStatic ? null : instance);
                default: throw new InvalidOperationException("Requisito sem membro: " + requirementId);
            }
        }

        /// <summary>Valor estatico (propriedade/campo/metodo sem parametros e sem instancia).</summary>
        internal static object? Static(string requirementId) => Read(requirementId, null);
    }
}
