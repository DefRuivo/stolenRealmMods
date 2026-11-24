using System;
using System.Reflection;
using RoguelikeUnlimitedLevelProgression.Runtime;

namespace RoguelikeUnlimitedLevelProgression.Patches
{
    /// <summary>
    /// R-ULLP-1 — build code nascendo com nivel rebaixado.
    ///
    /// Na beta 1.4.8 (buildid 26767595) o tipo NOVO `BuildCode` faz, em `CreateCharacter()`:
    ///   character.ExperienceLevel = Mathf.Min(character.MaxLevel, ExperienceLevel);
    /// e `CharacterMenusManager.ShowBuildCode(BuildCode)` e' quem chama `CreateCharacter()`.
    /// O personagem em construcao NAO e' IsRoguelikeCharacter, entao o postfix do mod em
    /// Character.get_MaxLevel o trata como fora de escopo e devolve o teto vanilla (20): qualquer
    /// build code acima de 20 nasce rebaixado, sem aviso.
    ///
    /// Correcao minima: postfix NESTE metodo (e so nele), que restaura o nivel declarado pelo build
    /// code quando a decisao de Policy.BuildCodeLevelOverride autoriza. Por que postfix aqui e nao
    /// transpiler no clamp nem mexida no getter:
    ///  - o getter Character.MaxLevel e' lido por muitos pontos do jogo; alterar o retorno "para
    ///    build code" atingiria todos eles (e o clamp de Character.Load(int) junto);
    ///  - um transpiler teria de reescrever instrucoes de IL desta janela, o que e mais fragil e
    ///    desnecessario: o valor que o build code quer ja esta no proprio objeto (`ExperienceLevel`);
    ///  - o postfix so ESCREVE quando o clamp efetivamente rebaixou e a configuracao do dono pede
    ///    nivel acima do vanilla; em qualquer outro caso e' no-op (fail-closed), e se o tipo nao
    ///    existir (build sem build code) nada e' aplicado.
    ///
    /// BuildCode e' tipo NOVO: este arquivo nao o referencia em tempo de compilacao (o projeto
    /// compila contra a lib antiga). Tudo por reflexao, sem HarmonyLib.AccessTools (ver Reflect.cs).
    /// </summary>
    internal static class BuildCodePatches
    {
        internal const string TargetTypeName = "BuildCode";
        internal const string TargetMethodName = "CreateCharacter";

        private static Type _type;
        private static bool _typeResolved;
        private static FieldInfo _experienceField;
        private static PropertyInfo _experienceProperty;
        private static bool _memberResolved;

        /// <summary>Tipo BuildCode do assembly do jogo, ou null em build que nao o tem.</summary>
        internal static Type ResolveType()
        {
            if (_typeResolved) return _type;
            _typeResolved = true;
            try
            {
                _type = typeof(Character).Assembly.GetType(TargetTypeName, throwOnError: false);
            }
            catch (Exception ex)
            {
                Log.WarnOnce("buildcode: GetType(" + TargetTypeName + ") falhou (" + ex.GetType().Name + "): "
                             + ex.Message + "); patch nao aplicado");
                _type = null;
            }
            return _type;
        }

        /// <summary>Alvo Harmony (`BuildCode.CreateCharacter`) resolvido por reflexao, ou null.</summary>
        internal static MethodInfo ResolveTarget()
        {
            return Reflect.Method(ResolveType(), TargetMethodName);
        }

        /// <summary>Resolucao completa do patch opcional (alvo + handler), exercitavel pelo harness.</summary>
        internal static bool TryResolve(out MethodInfo target, out MethodInfo postfix, out string detail)
        {
            target = ResolveTarget();
            postfix = Reflect.Method(typeof(BuildCodePatches), "Postfix");
            if (target == null)
            {
                detail = TargetTypeName + "." + TargetMethodName + " ausente nesta DLL";
                return false;
            }
            if (postfix == null)
            {
                detail = "handler BuildCodePatches.Postfix nao resolvido";
                return false;
            }
            detail = TargetTypeName + "." + TargetMethodName + "(" + target.GetParameters().Length
                     + " parametros) -> " + target.ReturnType.Name;
            return true;
        }

        /// <summary>
        /// Postfix de BuildCode.CreateCharacter. Parametros em `object` de proposito: o tipo
        /// BuildCode nao existe na build antiga, entao nao pode aparecer em assinatura compilada.
        /// </summary>
        public static void Postfix(object __instance, Character __result)
        {
            try
            {
                if (__instance == null || __result == null) return;

                double declared;
                if (!TryReadDeclaredLevel(__instance, out declared))
                {
                    Log.WarnOnce("buildcode: campo ExperienceLevel do BuildCode nao encontrado; clamp vanilla mantido");
                    return;
                }

                double assigned = __result.ExperienceLevel;
                double? target = Policy.BuildCodeLevelOverride(declared, assigned);
                if (!target.HasValue) return;

                __result.ExperienceLevel = (float)target.Value;

                if (__result.ExperienceLevel != (float)target.Value)
                {
                    // Nao deveria acontecer (nenhum setter do jogo re-clampa), mas se acontecer o
                    // valor observado fica registrado em vez de passar como sucesso.
                    Log.Warn("buildcode: escrita do nivel nao pegou (pedido=" + target.Value
                             + " observado=" + __result.ExperienceLevel + ")");
                }
                else
                {
                    Log.Info("buildcode: ExperienceLevel do build code restaurado de " + assigned
                             + " para " + __result.ExperienceLevel + " (R-ULLP-1)");
                }
            }
            catch (Exception ex)
            {
                Log.WarnOnce("buildcode: postfix falhou (" + ex.GetType().Name + ": " + ex.Message
                             + "); nivel do clamp vanilla mantido");
            }
        }

        private static bool TryReadDeclaredLevel(object instance, out double level)
        {
            level = 0d;
            if (!_memberResolved)
            {
                _memberResolved = true;
                var t = instance.GetType();
                _experienceField = Reflect.Field(t, "ExperienceLevel");
                if (_experienceField == null) _experienceProperty = Reflect.Property(t, "ExperienceLevel");
            }

            if (_experienceField != null && _experienceField.FieldType == typeof(float))
            {
                level = (float)_experienceField.GetValue(instance);
                return true;
            }
            if (_experienceProperty != null && _experienceProperty.PropertyType == typeof(float)
                && _experienceProperty.CanRead)
            {
                level = (float)_experienceProperty.GetValue(instance, null);
                return true;
            }
            return false;
        }
    }
}
