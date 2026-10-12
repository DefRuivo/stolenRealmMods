// LEITOR DE IL DO HARNESS (RoguelikeLevelProgression, LEVEL-R2)
//
// Por que este arquivo existe: no host .NET 6 da bancada, o leitor de IL do MonoMod usado pelo
// Harmony (`PatchProcessor.GetOriginalInstructions`) lanca NotSupportedException
// ("Body-less method"). Para NAO cair em replicas, este loader le a IL REAL da
// Assembly-CSharp.dll de referencia com System.Reflection (metadados + MethodBody nativos do
// CLR) e monta objetos HarmonyLib.CodeInstruction REAIS, que sao entregues ao transpiler REAL
// do mod. Os operandos sao resolvidos pelos tokens de metadado (Module.ResolveMethod/Field),
// os labels de branch sao Label reais, e as listas `labels`/`blocks` sao as do proprio
// CodeInstruction.
//
// Nao ha aqui nenhuma copia da logica de decisao: somente (a) leitura de IL e (b) acesso aos
// membros do CodeInstruction. Toda a decisao testada mora no codigo do mod.

using System;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using HarmonyLib;

namespace RoguelikeLevelProgression.Harness
{
    public sealed class IlLoadFailure : Exception
    {
        public IlLoadFailure(string message) : base(message) { }
    }

    public static class IlLoader
    {
        public static int DecodedInstructions;
        /// <summary>Branches cujo alvo esta no fim do metodo (materializados na ultima instrucao).</summary>
        public static int DanglingLabelTargets;

        private static readonly FieldInfo LabelsField =
            typeof(CodeInstruction).GetField("labels", BindingFlags.Public | BindingFlags.Instance);
        private static readonly FieldInfo BlocksField =
            typeof(CodeInstruction).GetField("blocks", BindingFlags.Public | BindingFlags.Instance);
        private static readonly FieldInfo LabelValueField =
            FindLabelValueField();

        private static readonly Dictionary<ushort, OpCode> OpCodesByValue = BuildOpCodeTable();

        private static FieldInfo FindLabelValueField()
        {
            foreach (var f in typeof(Label).GetFields(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic))
            {
                if (f.FieldType == typeof(int)) return f;
            }
            return null;
        }

        private static Dictionary<ushort, OpCode> BuildOpCodeTable()
        {
            var map = new Dictionary<ushort, OpCode>();
            foreach (var f in typeof(OpCodes).GetFields(BindingFlags.Public | BindingFlags.Static))
            {
                if (f.FieldType != typeof(OpCode)) continue;
                var op = (OpCode)f.GetValue(null);
                map[unchecked((ushort)op.Value)] = op;
            }
            return map;
        }

        /// <summary>Cria um Label REAL (System.Reflection.Emit.Label) com o valor informado.</summary>
        public static Label MakeLabel(int value)
        {
            if (LabelValueField == null) throw new IlLoadFailure("campo de valor de Label nao encontrado");
            object boxed = new Label();
            LabelValueField.SetValue(boxed, value);
            return (Label)boxed;
        }

        public static List<Label> LabelsOf(CodeInstruction ci)
        {
            if (LabelsField == null) throw new IlLoadFailure("campo 'labels' de CodeInstruction nao encontrado");
            return (List<Label>)LabelsField.GetValue(ci);
        }

        public static List<ExceptionBlock> BlocksOf(CodeInstruction ci)
        {
            if (BlocksField == null) throw new IlLoadFailure("campo 'blocks' de CodeInstruction nao encontrado");
            return (List<ExceptionBlock>)BlocksField.GetValue(ci);
        }

        /// <summary>Le a IL real do metodo e devolve a lista de CodeInstruction equivalente.</summary>
        public static List<CodeInstruction> Read(MethodInfo method)
        {
            var body = method.GetMethodBody();
            if (body == null) throw new IlLoadFailure("metodo sem corpo: " + method);
            byte[] il = body.GetILAsByteArray();
            if (il == null) throw new IlLoadFailure("IL indisponivel para " + method);

            var module = method.Module;
            Type[] typeArgs = method.DeclaringType != null ? method.DeclaringType.GetGenericArguments() : null;
            Type[] methodArgs = method.IsGenericMethodDefinition ? method.GetGenericArguments() : null;

            // primeira passada: offsets -> indice
            var offsets = new List<int>();
            var sizes = new List<int>();
            int pos = 0;
            while (pos < il.Length)
            {
                int start = pos;
                ushort code = il[pos];
                int head = 1;
                if (code == 0xFE) { code = (ushort)(0xFE00 | il[pos + 1]); head = 2; }
                OpCode op;
                if (!OpCodesByValue.TryGetValue(code, out op))
                    throw new IlLoadFailure("opcode desconhecido 0x" + code.ToString("X4") + " em " + method.Name + " offset 0x" + start.ToString("x4"));
                int operandSize = OperandSize(op, il, pos + head);
                offsets.Add(start);
                sizes.Add(head + operandSize);
                pos = start + head + operandSize;
            }

            var indexByOffset = new Dictionary<int, int>();
            for (int i = 0; i < offsets.Count; i++) indexByOffset[offsets[i]] = i;

            // segunda passada: monta as instrucoes (labels sao anexados DEPOIS, pois um branch
            // pode apontar para uma instrucao que ainda nao foi construida)
            var result = new List<CodeInstruction>(offsets.Count);
            var pending = new List<KeyValuePair<int, Label>>();
            DanglingLabelTargets = 0;
            for (int i = 0; i < offsets.Count; i++)
            {
                int start = offsets[i];
                int head = il[start] == 0xFE ? 2 : 1;
                ushort code = head == 2 ? (ushort)(0xFE00 | il[start + 1]) : (ushort)il[start];
                var op = OpCodesByValue[code];
                try
                {
                    object operand = DecodeOperand(op, il, start + head, module, typeArgs, methodArgs, indexByOffset, offsets);
                    var ci = new CodeInstruction(op, operand);
                    if (op.OperandType == OperandType.InlineBrTarget || op.OperandType == OperandType.ShortInlineBrTarget)
                    {
                        int targetOffset = TargetOffset(op, il, start + head, start + head + OperandSize(op, il, start + head));
                        pending.Add(new KeyValuePair<int, Label>(targetOffset, (Label)operand));
                    }
                    result.Add(ci);
                }
                catch (IlLoadFailure) { throw; }
                catch (Exception ex)
                {
                    throw new IlLoadFailure("falha decodificando offset 0x" + start.ToString("x4") + " opcode " + op
                                            + " no metodo " + method.Name + ": " + ex.GetType().Name + " " + ex.Message);
                }
            }

            foreach (var p in pending)
            {
                int targetIndex;
                if (indexByOffset.TryGetValue(p.Key, out targetIndex))
                {
                    LabelsOf(result[targetIndex]).Add(p.Value);
                    continue;
                }
                // Branch para o FIM do metodo (depois da ultima instrucao): o leitor do Harmony
                // tambem materializa esse alvo. Contamos como "pendente" para o teste poder
                // afirmar que o metodo-alvo nao depende desse caso.
                DanglingLabelTargets++;
                LabelsOf(result[result.Count - 1]).Add(p.Value);
            }
            DecodedInstructions = result.Count;
            return result;
        }

        private static int TargetOffset(OpCode op, byte[] il, int operandPos, int nextOffset)
        {
            if (op.OperandType == OperandType.ShortInlineBrTarget)
                return nextOffset + (sbyte)il[operandPos];
            return nextOffset + BitConverter.ToInt32(il, operandPos);
        }

        private static int OperandSize(OpCode op, byte[] il, int p)
        {
            switch (op.OperandType)
            {
                case OperandType.InlineNone: return 0;
                case OperandType.ShortInlineI:
                case OperandType.ShortInlineVar:
                case OperandType.ShortInlineBrTarget: return 1;
                case OperandType.InlineVar: return 2;
                case OperandType.InlineI:
                case OperandType.InlineBrTarget:
                case OperandType.ShortInlineR:
                case OperandType.InlineString:
                case OperandType.InlineField:
                case OperandType.InlineMethod:
                case OperandType.InlineType:
                case OperandType.InlineTok:
                case OperandType.InlineSig: return 4;
                case OperandType.InlineI8:
                case OperandType.InlineR: return 8;
                case OperandType.InlineSwitch:
                    int n = BitConverter.ToInt32(il, p);
                    return 4 + 4 * n;
                default:
                    throw new IlLoadFailure("tipo de operando nao suportado: " + op.OperandType);
            }
        }

        private static object DecodeOperand(OpCode op, byte[] il, int p, Module module,
                                            Type[] typeArgs, Type[] methodArgs,
                                            Dictionary<int, int> indexByOffset, List<int> offsets)
        {
            switch (op.OperandType)
            {
                case OperandType.InlineNone: return null;
                case OperandType.ShortInlineI: return (sbyte)il[p];
                case OperandType.ShortInlineVar: return (int)il[p];
                case OperandType.InlineVar: return (int)BitConverter.ToUInt16(il, p);
                case OperandType.InlineI: return BitConverter.ToInt32(il, p);
                case OperandType.InlineI8: return BitConverter.ToInt64(il, p);
                case OperandType.ShortInlineR: return BitConverter.ToSingle(il, p);
                case OperandType.InlineR: return BitConverter.ToDouble(il, p);
                case OperandType.InlineString: return module.ResolveString(BitConverter.ToInt32(il, p));
                case OperandType.ShortInlineBrTarget: return MakeLabel(TargetOffset(op, il, p, p + 1));
                case OperandType.InlineBrTarget: return MakeLabel(TargetOffset(op, il, p, p + 4));
                case OperandType.InlineSwitch:
                    {
                        int n = BitConverter.ToInt32(il, p);
                        var targets = new Label[n];
                        int baseOffset = p + 4 + 4 * n;
                        for (int k = 0; k < n; k++)
                        {
                            targets[k] = MakeLabel(baseOffset + BitConverter.ToInt32(il, p + 4 + 4 * k));
                        }
                        return targets;
                    }
                case OperandType.InlineMethod:
                    return module.ResolveMethod(BitConverter.ToInt32(il, p), typeArgs, methodArgs);
                case OperandType.InlineField:
                    return module.ResolveField(BitConverter.ToInt32(il, p), typeArgs, methodArgs);
                case OperandType.InlineType:
                    return module.ResolveType(BitConverter.ToInt32(il, p), typeArgs, methodArgs);
                case OperandType.InlineTok:
                    return module.ResolveMember(BitConverter.ToInt32(il, p), typeArgs, methodArgs);
                default:
                    throw new IlLoadFailure("operando nao decodificado: " + op.OperandType);
            }
        }
    }
}
