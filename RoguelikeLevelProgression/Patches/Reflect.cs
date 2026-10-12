using System;
using System.Reflection;
using RoguelikeLevelProgression.Runtime;

namespace RoguelikeLevelProgression.Patches
{
    /// <summary>
    /// Resolucao de membros por reflexao DIRETA, com a mesma semantica usada pelo mod antes
    /// (busca em tipo e tipos-base, publico/nao-publico, instancia/estatico).
    ///
    /// Por que nao usamos HarmonyLib.AccessTools aqui: o inicializador estatico do AccessTools
    /// (HarmonyX) chama MethodInvoker.GetHandler(null) quando Exception::PrepForRemoting /
    /// FixRemotingException nao existem — o que acontece em qualquer runtime moderno fora do
    /// Mono antigo do jogo. Isso torna o AccessTools inutilizavel em bancada e acrescenta uma
    /// dependencia de inicializacao que nao precisamos: todos os alvos deste mod sao buscas
    /// simples por nome/assinatura. A resolucao continua sendo feita contra os TIPOS REAIS do
    /// assembly carregado (nenhum nome de membro e adivinhado: alvo ausente devolve null e o
    /// grupo de gameplay inteiro e revertido pelo PatchRegistry).
    /// </summary>
    internal static class Reflect
    {
        internal const BindingFlags Any =
            BindingFlags.Instance | BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;

        internal static MethodInfo Method(Type type, string name, params Type[] parameters)
        {
            if (type == null || string.IsNullOrEmpty(name)) return null;
            for (var t = type; t != null; t = t.BaseType)
            {
                MethodInfo mi = null;
                try
                {
                    if (parameters == null || parameters.Length == 0)
                    {
                        var candidates = t.GetMethods(Any);
                        foreach (var c in candidates)
                        {
                            if (c.Name != name) continue;
                            if (mi == null) mi = c;
                        }
                    }
                    else
                    {
                        mi = t.GetMethod(name, Any, null, parameters, null);
                    }
                }
                catch (AmbiguousMatchException)
                {
                    // mesma tolerancia do AccessTools: fica com o primeiro candidato declarado
                }
                if (mi != null) return mi;
            }
            return null;
        }

        internal static PropertyInfo Property(Type type, string name)
        {
            if (type == null || string.IsNullOrEmpty(name)) return null;
            for (var t = type; t != null; t = t.BaseType)
            {
                var p = t.GetProperty(name, Any);
                if (p != null) return p;
            }
            return null;
        }

        /// <summary>Getter da propriedade (equivale a AccessTools.PropertyGetter).</summary>
        internal static MethodInfo PropertyGetter(Type type, string name)
        {
            var p = Property(type, name);
            if (p == null) return null;
            return p.GetGetMethod(nonPublic: true);
        }

        internal static FieldInfo Field(Type type, string name)
        {
            if (type == null || string.IsNullOrEmpty(name)) return null;
            for (var t = type; t != null; t = t.BaseType)
            {
                var f = t.GetField(name, Any);
                if (f != null) return f;
            }
            return null;
        }
    }
}
