// HARNESS ISOLADO do RoguelikeLevelProgression (LEVEL-R2)
//
// Exercita o CODIGO REAL do mod (os mesmos arquivos-fonte sao compilados neste executavel),
// sem abrir o jogo, sem tocar no perfil/save do dono e sem instalar nada. A IL usada nos testes
// do transpiler vem da Assembly-CSharp.dll de referencia (hash conferido), lida por
// System.Reflection em IlLoader.cs.
//
// Saida: linhas "PASS/FAIL/NAO_EXERCITADO <nome> | detalhe" e dois arquivos (txt + json) no
// diretorio informado em argv[0]. Exit code 0 somente quando nao ha FAIL.

using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Reflection;
using System.Reflection.Emit;
using System.Security.Cryptography;
using System.Text;
using HarmonyLib;
using RoguelikeLevelProgression;
using RoguelikeLevelProgression.Core;
using RoguelikeLevelProgression.Patches;
using RoguelikeLevelProgression.Runtime;

namespace RoguelikeLevelProgression.Harness
{
    internal static class Program
    {
        public const string ExpectedAssemblySha256 =
            "8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a";

        private static string _libDir = @"C:\dev\stolen-realm\lib";
        private static readonly List<string> _probeDirs = new List<string>();
        private static string _outDir;
        private static readonly List<string> _lines = new List<string>();
        private static readonly List<string> _json = new List<string>();
        private static int _pass, _fail, _not;
        private static Assembly _acs;

        private static void Pass(string name, string detail)
        {
            _pass++;
            _lines.Add("PASS " + name + " | " + detail);
            _json.Add("{\"status\":\"PASS\",\"name\":" + J(name) + ",\"detail\":" + J(detail) + "}");
        }

        private static void Fail(string name, string detail)
        {
            _fail++;
            _lines.Add("FAIL " + name + " | " + detail);
            _json.Add("{\"status\":\"FAIL\",\"name\":" + J(name) + ",\"detail\":" + J(detail) + "}");
        }

        private static void NotExercised(string name, string reason)
        {
            _not++;
            _lines.Add("NAO_EXERCITADO " + name + " | " + reason);
            _json.Add("{\"status\":\"NAO_EXERCITADO\",\"name\":" + J(name) + ",\"detail\":" + J(reason) + "}");
        }

        private static void Check(bool ok, string name, string okDetail, string failDetail)
        {
            if (ok) Pass(name, okDetail); else Fail(name, failDetail);
        }

        private static string J(string s)
        {
            var sb = new StringBuilder();
            sb.Append('"');
            foreach (char c in s ?? "")
            {
                if (c == '"' || c == '\\') sb.Append('\\').Append(c);
                else if (c < ' ') sb.Append(' ');
                else sb.Append(c);
            }
            sb.Append('"');
            return sb.ToString();
        }

        private static void Section(string title)
        {
            _lines.Add("");
            _lines.Add("== " + title + " ==");
        }

        private static int Main(string[] argv)
        {
            _outDir = argv.Length > 0 ? argv[0] : Path.Combine(Directory.GetCurrentDirectory(), "harness-out");
            if (argv.Length > 1) _libDir = argv[1];
            if (argv.Length > 2) _probeDirs.Add(argv[2]);
            if (argv.Length > 3) _probeDirs.Add(argv[3]);
            Directory.CreateDirectory(_outDir);

            AppDomain.CurrentDomain.AssemblyResolve += Resolve;

            _lines.Add("RLP HARNESS (LEVEL-R2) - " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture));
            _lines.Add("lib: " + _libDir);
            _lines.Add("net: " + Environment.Version + " / " + System.Runtime.InteropServices.RuntimeInformation.FrameworkDescription);

            try
            {
                RunAll();
            }
            catch (Exception ex)
            {
                Fail("harness.fatal", Flatten(ex));
            }

            _lines.Add("");
            _lines.Add("RESUMO: PASS=" + _pass + " FAIL=" + _fail + " NAO_EXERCITADO=" + _not);
            foreach (var l in _lines) Console.WriteLine(l);
            WriteOutputs();
            return _fail == 0 ? 0 : 1;
        }

        private static Assembly Resolve(object sender, ResolveEventArgs e)
        {
            var simple = new AssemblyName(e.Name).Name + ".dll";
            var p = Path.Combine(_libDir, simple);
            if (File.Exists(p)) return Assembly.LoadFrom(p);
            // Dependencias que NAO estao na lib comum (so leitura): MonoMod (exigido pelo
            // AccessTools do HarmonyX) vive no core do BepInEx e Facepunch.Steamworks/outros no
            // Managed do jogo. Nada e copiado nem modificado.
            foreach (var dir in _probeDirs)
            {
                try
                {
                    var q = Path.Combine(dir, simple);
                    if (File.Exists(q)) return Assembly.LoadFrom(q);
                }
                catch (Exception) { }
            }
            return null;
        }

        private static void WriteOutputs()
        {
            File.WriteAllLines(Path.Combine(_outDir, "harness-results.txt"), _lines, new UTF8Encoding(false));
            var sb = new StringBuilder();
            sb.Append("{\n  \"harness\":\"RoguelikeLevelProgression.Harness\",\n");
            sb.Append("  \"task\":\"t_918314e9\",\n");
            sb.Append("  \"pass\":").Append(_pass).Append(", \"fail\":").Append(_fail)
              .Append(", \"not_exercised\":").Append(_not).Append(",\n");
            sb.Append("  \"results\":[\n    ").Append(string.Join(",\n    ", _json.ToArray())).Append("\n  ]\n}\n");
            File.WriteAllText(Path.Combine(_outDir, "harness-results.json"), sb.ToString(), new UTF8Encoding(false));
        }

        // ---------------------------------------------------------------- suites

        private static void RunAll()
        {
            RunSuite("load", LoadAssemblies);
            RunSuite("il", TestIdentityAndIl);
            RunSuite("transpiler", TestTranspiler);
            RunSuite("registry", TestPatchTargets);
            RunSuite("policy", TestPolicyMatrix);
            RunSuite("xpcurve", TestXpCurve);
            RunSuite("xpbackend", TestXpBackend);
            RunSuite("ledger", TestLedger);
            RunSuite("patchguards", TestGuardsStaticEntryPoints);
            RunSuite("notexercised", DeclareNotExercised);
        }

        private static void RunSuite(string name, Action body)
        {
            try
            {
                body();
            }
            catch (Exception ex)
            {
                Fail("suite." + name, Flatten(ex));
            }
        }

        /// <summary>Cadeia completa de excecoes (inclusive TypeInitializationException/InnerException).</summary>
        private static string Flatten(Exception ex)
        {
            var sb = new StringBuilder();
            int depth = 0;
            for (var e = ex; e != null && depth < 5; e = e.InnerException, depth++)
            {
                if (depth > 0) sb.Append(" <- ");
                sb.Append(e.GetType().Name).Append(": ").Append(e.Message);
            }
            return sb.ToString();
        }

        private static void LoadAssemblies()
        {
            Section("CARGA DAS ASSEMBLIES E IDENTIDADE DA REFERENCIA");
            try
            {
                Assembly.LoadFrom(Path.Combine(_libDir, "0Harmony.dll"));
                Assembly.LoadFrom(Path.Combine(_libDir, "BepInEx.dll"));
                _acs = Assembly.LoadFrom(Path.Combine(_libDir, "Assembly-CSharp.dll"));
                Pass("asm.load", "0Harmony/BepInEx/Assembly-CSharp carregadas de " + _libDir);
            }
            catch (Exception ex)
            {
                Fail("asm.load", Flatten(ex));
                return;
            }

            string hash = "";
            try
            {
                using (var sha = SHA256.Create())
                using (var fs = File.OpenRead(Path.Combine(_libDir, "Assembly-CSharp.dll")))
                {
                    hash = BitConverter.ToString(sha.ComputeHash(fs)).Replace("-", "").ToLowerInvariant();
                }
            }
            catch (Exception ex) { Fail("assemblies.hash", ex.Message); return; }

            Check(hash == ExpectedAssemblySha256, "assembly.sha256_matches_spec",
                "sha256 da Assembly-CSharp.dll de referencia = " + hash,
                "hash divergente: obtido " + hash + " esperado " + ExpectedAssemblySha256);
        }

        private static void TestIdentityAndIl()
        {
            Section("IL REAL DO BLOCO CRITICO");
            try
            {
                var mi = FindRootMethod();
                if (mi == null) { Fail("il.root_method", "Root.SendGameCompleteFromServer nao encontrado"); return; }
                Pass("il.root_method", "Root.SendGameCompleteFromServer encontrado: " + Describe(mi));

                var il = IlLoader.Read(mi);
                Check(il.Count > 100, "il.decoded_instruction_count",
                    "IL real decodificada em " + il.Count + " instrucoes (CodeInstruction reais)",
                    "poucas instrucoes decodificadas: " + il.Count);
                Check(IlLoader.DanglingLabelTargets == 0, "il.no_dangling_branch_targets",
                    "todos os branches do metodo-alvo apontam para instrucoes existentes (rotulos fieis a IL real, sem alvo colado no fim)",
                    "branches com alvo fora da lista: " + IlLoader.DanglingLabelTargets);

                int match = FindWindow(il);
                Check(match >= 0, "il.window_present_in_real_il",
                    "janela estrutural vanilla em match=" + match + " (ldloc/callvirt get_Level/call get_instance/ldfld roguelikeManager/ldfld RoguelikeMaxLevel/bge)",
                    "janela estrutural NAO encontrada na IL real");

                if (match >= 0)
                {
                    var branches = CountWindows(il);
                    Check(branches == 1, "il.window_unique_in_real_il",
                        "exatamente 1 janela estrutural na IL real",
                        "esperava 1 janela, encontrei " + branches);
                }
            }
            catch (Exception ex)
            {
                Fail("il.suite", Flatten(ex));
            }
        }

        private static MethodInfo FindRootMethod()
        {
            var root = _acs.GetType("Root");
            if (root == null) return null;
            foreach (var m in root.GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic))
            {
                if (m.Name == "SendGameCompleteFromServer") return m;
            }
            return null;
        }

        private static string Describe(MethodBase m)
        {
            return m.DeclaringType.FullName + "." + m.Name + " (" + m.GetParameters().Length + " parametros)";
        }

        private static bool IsLocalLoad(OpCode op)
        {
            return op == OpCodes.Ldloc_0 || op == OpCodes.Ldloc_1 || op == OpCodes.Ldloc_2 || op == OpCodes.Ldloc_3
                || op == OpCodes.Ldloc || op == OpCodes.Ldloc_S;
        }

        private static bool SameName(object operand, string typeName, string methodName)
        {
            var mi = operand as MethodInfo;
            if (mi == null) return false;
            if (mi.Name != methodName) return false;
            if (typeName == null) return true;
            return mi.DeclaringType != null && mi.DeclaringType.Name == typeName;
        }

        private static bool SameFieldName(object operand, string typeName, string fieldName)
        {
            var fi = operand as FieldInfo;
            if (fi == null) return false;
            if (fi.Name != fieldName) return false;
            return fi.DeclaringType != null && fi.DeclaringType.Name == typeName;
        }

        /// <summary>
        /// Scanner INDEPENDENTE do harness: acha a janela sem usar o codigo do mod. Serve para
        /// contrapor a decisao do transpiler (se os dois divergirem, o teste falha).
        /// </summary>
        private static int FindWindow(IList<CodeInstruction> ins)
        {
            for (int i = 0; i + 5 < ins.Count; i++)
            {
                if (!IsLocalLoad(ins[i].opcode)) continue;
                if (ins[i + 1].opcode != OpCodes.Callvirt || !SameName(ins[i + 1].operand, "Character", "get_Level")) continue;
                if (ins[i + 2].opcode != OpCodes.Call || !SameName(ins[i + 2].operand, "GlobalSettingsManager", "get_instance")) continue;
                if (ins[i + 3].opcode != OpCodes.Ldfld || !SameFieldName(ins[i + 3].operand, "GlobalSettingsManager", "roguelikeManager")) continue;
                if (ins[i + 4].opcode != OpCodes.Ldfld || !SameFieldName(ins[i + 4].operand, "RoguelikeSettings", "RoguelikeMaxLevel")) continue;
                var b = ins[i + 5].opcode;
                if (b != OpCodes.Bge_S && b != OpCodes.Bge) continue;
                if (ins[i + 5].operand == null || ins[i + 5].operand.GetType().FullName != "System.Reflection.Emit.Label") continue;
                return i;
            }
            return -1;
        }

        private static int CountWindows(IList<CodeInstruction> ins)
        {
            int n = 0;
            for (int i = 0; i + 5 < ins.Count; i++)
            {
                if (!IsLocalLoad(ins[i].opcode)) continue;
                if (ins[i + 1].opcode != OpCodes.Callvirt || !SameName(ins[i + 1].operand, "Character", "get_Level")) continue;
                if (ins[i + 2].opcode != OpCodes.Call || !SameName(ins[i + 2].operand, "GlobalSettingsManager", "get_instance")) continue;
                if (ins[i + 3].opcode != OpCodes.Ldfld || !SameFieldName(ins[i + 3].operand, "GlobalSettingsManager", "roguelikeManager")) continue;
                if (ins[i + 4].opcode != OpCodes.Ldfld || !SameFieldName(ins[i + 4].operand, "RoguelikeSettings", "RoguelikeMaxLevel")) continue;
                var b = ins[i + 5].opcode;
                if (b != OpCodes.Bge_S && b != OpCodes.Bge) continue;
                n++;
            }
            return n;
        }

        private static List<CodeInstruction> RealIl()
        {
            return IlLoader.Read(FindRootMethod());
        }

        private static void TestTranspiler()
        {
            Section("TRANSPILER CRITICO (parte06) SOBRE A IL REAL");

            BattleResultTarget target;
            string missing;
            try
            {
                target = BattleResultPatches.ResolveTarget(out missing);   // codigo REAL do mod
            }
            catch (Exception ex) { Fail("transpiler.resolve_target", Flatten(ex)); return; }

            Check(missing == null, "transpiler.resolve_target_real_dll",
                "BattleResultPatches.ResolveTarget achou os 7 membros na DLL real (get_Level, get_instance, roguelikeManager, RoguelikeMaxLevel, GiveExperience, List<Character>::Add, Policy.CanAdvance)",
                "membros ausentes: " + missing);
            if (missing != null) return;

            List<CodeInstruction> il = RealIl();
            int w = FindWindow(il);
            if (w < 0) { Fail("transpiler.window", "janela nao encontrada pelo scanner independente"); return; }

            object originalLabel = il[w + 5].operand;

            List<CodeInstruction> outList;
            string failure;
            bool ok = BattleResultTranspiler.TryTransform(il, target, out outList, out failure);

            Check(ok, "transpiler.real_il_applied",
                "TryTransform aceitou a IL real (LastMatchCount=" + BattleResultTranspiler.LastMatchCount + ")",
                "recusou a IL real: " + failure);
            if (!ok) return;

            Check(BattleResultTranspiler.LastMatchCount == 1, "transpiler.exactly_one_match",
                "LastMatchCount == 1 (janela unica, sem ambiguidade)",
                "LastMatchCount == " + BattleResultTranspiler.LastMatchCount);

            Check(outList.Count == il.Count - 1, "transpiler.get_level_removed",
                "saida tem 1 instrucao a menos (callvirt get_Level retirada): " + il.Count + " -> " + outList.Count,
                "contagem inesperada: " + il.Count + " -> " + outList.Count);

            Check(IsLocalLoad(outList[w].opcode), "transpiler.character_stays_on_stack",
                "a carga do Character (ldloc) permanece no lugar (opcode " + outList[w].opcode + " na posicao " + w + ")",
                "a posicao " + w + " deixou de ser carga de local: " + outList[w].opcode);

            Check(outList[w + 1].opcode == OpCodes.Call && SameName(outList[w + 1].operand, "GlobalSettingsManager", "get_instance"),
                "transpiler.settings_provider_preserved",
                "call GlobalSettingsManager::get_instance preservado",
                "esperava call get_instance na posicao " + (w + 1) + ": " + outList[w + 1].opcode);

            Check(outList[w + 2].opcode == OpCodes.Ldfld && SameFieldName(outList[w + 2].operand, "GlobalSettingsManager", "roguelikeManager"),
                "transpiler.roguelike_settings_on_stack",
                "ldfld GlobalSettingsManager::roguelikeManager (RoguelikeSettings) preservado",
                "esperava ldfld roguelikeManager na posicao " + (w + 2));

            var canAdvance = outList[w + 3].operand as MethodInfo;
            Check(outList[w + 3].opcode == OpCodes.Call && canAdvance != null
                  && canAdvance.Name == "CanAdvance" && canAdvance.DeclaringType == typeof(Policy)
                  && canAdvance.GetParameters().Length == 2
                  && canAdvance.GetParameters()[0].ParameterType == typeof(Character)
                  && canAdvance.GetParameters()[1].ParameterType == typeof(RoguelikeSettings),
                "transpiler.cap_load_becomes_policy_call",
                "ldfld RoguelikeMaxLevel substituido por call Policy.CanAdvance(Character, RoguelikeSettings) -> bool",
                "a substituicao nao e a chamada esperada: " + DescribeMaybe(outList[w + 3]));

            var branch = outList[w + 4];
            Check((branch.opcode == OpCodes.Brfalse_S || branch.opcode == OpCodes.Brfalse) && branch.operand != null && branch.operand.Equals(originalLabel),
                "transpiler.bge_becomes_brfalse_same_target",
                "bge.s -> " + branch.opcode + " com o MESMO destino (Label preservado)",
                "branch invalido: " + branch.opcode + " operando=" + branch.operand);

            bool levelGone = true;
            for (int i = w; i <= w + 4 && i < outList.Count; i++)
            {
                if (outList[i].opcode == OpCodes.Callvirt && SameName(outList[i].operand, "Character", "get_Level")) levelGone = false;
            }
            Check(levelGone, "transpiler.get_level_not_reexecuted",
                "nenhum callvirt get_Level sobrou na janela reescrita (a comparacao de cap sumiu)",
                "ainda existe callvirt get_Level na janela reescrita");

            // contraprova independente da cauda de premio: entre a janela e o destino do branch
            // precisam existir GiveExperience e List<Character>::Add ANTES da instrucao rotulada.
            int labelled = -1;
            for (int i = w + 5; i < outList.Count; i++)
            {
                var labels = IlLoader.LabelsOf(outList[i]);
                for (int k = 0; k < labels.Count; k++)
                {
                    if (labels[k].Equals(originalLabel)) { labelled = i; break; }
                }
                if (labelled >= 0) break;
            }
            bool giveExp = false, listAdd = false;
            for (int i = (labelled >= 0 ? w + 5 : w + 5); i < (labelled >= 0 ? labelled : outList.Count); i++)
            {
                if (SameName(outList[i].operand, "Character", "GiveExperience")) giveExp = true;
                var mi = outList[i].operand as MethodInfo;
                if (mi != null && mi.Name == "Add" && mi.DeclaringType != null && mi.DeclaringType.IsGenericType
                    && mi.DeclaringType.GetGenericTypeDefinition() == typeof(List<>)) listAdd = true;
            }
            Check(labelled > w + 5 && giveExp && listAdd, "transpiler.prize_tail_before_branch_target",
                "entre o branch e o seu destino existem GiveExperience e List<Character>::Add (destino rotulado no indice " + labelled + "): premio E lista pulados juntos quando CanAdvance=false",
                "cauda de premio incompleta: labelled=" + labelled + " GiveExperience=" + giveExp + " List.Add=" + listAdd);

            // (A) labels/blocks da instrucao substituida sao copiados para a nova call
            var injected = RealIl();
            int w2 = FindWindow(injected);
            var mark = IlLoader.MakeLabel(0x7FFF);
            IlLoader.LabelsOf(injected[w2 + 4]).Add(mark);
            List<CodeInstruction> copiedOut;
            string cFailure;
            bool cOk = BattleResultTranspiler.TryTransform(injected, target, out copiedOut, out cFailure);
            bool markMoved = false;
            if (cOk)
            {
                var labels = IlLoader.LabelsOf(copiedOut[w2 + 3]);
                for (int k = 0; k < labels.Count; k++) if (labels[k].Equals(mark)) markMoved = true;
            }
            Check(cOk && markMoved, "transpiler.labels_of_replaced_instruction_preserved",
                "label injetado no ldfld RoguelikeMaxLevel foi copiado para a call Policy.CanAdvance (label/blocks preservados)",
                "cOk=" + cOk + " markMoved=" + markMoved + " falha=" + cFailure);

            // (B) get_Level com label = reescrita insegura -> recusa explicita (fail-closed)
            var dangerous = RealIl();
            int w3 = FindWindow(dangerous);
            IlLoader.LabelsOf(dangerous[w3 + 1]).Add(IlLoader.MakeLabel(0x7000));
            List<CodeInstruction> dOut;
            string dFail;
            bool dOk = BattleResultTranspiler.TryTransform(dangerous, target, out dOut, out dFail);
            Check(!dOk && dFail != null && dFail.Contains("labels"), "transpiler.refuses_when_get_level_has_labels",
                "recusa com motivo explicito quando a instrucao get_Level traz labels: " + dFail,
                "NAO recusou uma reescrita insegura (ok=" + dOk + ", motivo=" + dFail + ")");

            // (C) cauda de premio ausente -> recusa
            var noTail = RealIl();
            int w4 = FindWindow(noTail);
            object lbl4 = noTail[w4 + 5].operand;
            int target4 = -1;
            for (int i = w4 + 6; i < noTail.Count; i++)
            {
                var labels = IlLoader.LabelsOf(noTail[i]);
                for (int k = 0; k < labels.Count; k++) if (labels[k].Equals(lbl4)) target4 = i;
                if (target4 >= 0) break;
            }
            if (target4 > w4 + 6) noTail.RemoveRange(w4 + 6, target4 - (w4 + 6));
            List<CodeInstruction> tOut;
            string tFail;
            bool tOk = BattleResultTranspiler.TryTransform(noTail, target, out tOut, out tFail);
            Check(!tOk && tFail != null && tFail.Contains("premio"), "transpiler.refuses_when_prize_tail_missing",
                "recusa quando a cauda de premio some: " + tFail,
                "NAO recusou (ok=" + tOk + ", motivo=" + tFail + ")");

            // (D) janela alterada -> zero correspondencias
            var mutated = RealIl();
            int w5 = FindWindow(mutated);
            var otherGetter = typeof(Character).GetProperty("Experience").GetGetMethod();
            mutated[w5 + 1].operand = otherGetter;
            List<CodeInstruction> mOut;
            string mFail;
            bool mOk = BattleResultTranspiler.TryTransform(mutated, target, out mOut, out mFail);
            Check(!mOk && BattleResultTranspiler.LastMatchCount == 0, "transpiler.no_match_when_member_swapped",
                "janela com get_Level trocado por get_Experience nao casa (0 correspondencias): " + mFail,
                "casou indevidamente (matches=" + BattleResultTranspiler.LastMatchCount + ")");

            // (E) branch sem Label real -> nao casa
            var noLabel = RealIl();
            int w6 = FindWindow(noLabel);
            noLabel[w6 + 5].operand = 12345;
            List<CodeInstruction> nOut;
            string nFail;
            bool nOk = BattleResultTranspiler.TryTransform(noLabel, target, out nOut, out nFail);
            Check(!nOk && BattleResultTranspiler.LastMatchCount == 0, "transpiler.no_match_when_branch_operand_is_not_label",
                "operando de branch que nao e Label real nao casa (0 correspondencias)",
                "casou com operando invalido (matches=" + BattleResultTranspiler.LastMatchCount + ")");

            // (F) duplicacao da janela -> ambiguidade -> recusa
            var dup = RealIl();
            int w7 = FindWindow(dup);
            var copy = new List<CodeInstruction>();
            for (int i = w7; i <= w7 + 5; i++) copy.Add(new CodeInstruction(dup[i].opcode, dup[i].operand));
            dup.AddRange(copy);
            List<CodeInstruction> dupOut;
            string dupFail;
            bool dupOk = BattleResultTranspiler.TryTransform(dup, target, out dupOut, out dupFail);
            Check(!dupOk && BattleResultTranspiler.LastMatchCount == 2, "transpiler.ambiguous_window_refused",
                "duas janelas casando = recusa explicita (matches=2): " + dupFail,
                "nao recusou ambiguidade (ok=" + dupOk + ", matches=" + BattleResultTranspiler.LastMatchCount + ")");

            // (G) CanAdvance nao resolvido -> recusa
            var t2 = new BattleResultTarget
            {
                GetLevel = target.GetLevel,
                GetRoguelikeSettings = target.GetRoguelikeSettings,
                RoguelikeManagerField = target.RoguelikeManagerField,
                RoguelikeMaxLevelField = target.RoguelikeMaxLevelField,
                GiveExperience = target.GiveExperience,
                ListAddCharacter = target.ListAddCharacter,
                CanAdvance = null
            };
            List<CodeInstruction> cOut2;
            string cFail2;
            bool ok2 = BattleResultTranspiler.TryTransform(RealIl(), t2, out cOut2, out cFail2);
            Check(!ok2 && cFail2 != null && cFail2.Contains("CanAdvance"), "transpiler.refuses_without_canadvance",
                "recusa quando Policy.CanAdvance nao esta resolvido: " + cFail2,
                "nao recusou (ok=" + ok2 + ")");

            // (H) entrada do patch REAL: BattleResultPatches.Transpiler (AccessTools na DLL real)
            var real = RealIl();
            var patched = new List<CodeInstruction>(BattleResultPatches.Transpiler(real));
            Check(patched.Count == real.Count - 1 && BattleResultTranspiler.LastApplied, "transpiler.patch_entrypoint_rewrites",
                "BattleResultPatches.Transpiler(IL real) devolve " + patched.Count + " instrucoes (entrada " + real.Count + ") com LastApplied=true",
                "entrada do patch nao reescreveu: " + patched.Count + " vs " + real.Count + " LastApplied=" + BattleResultTranspiler.LastApplied + " (" + BattleResultTranspiler.LastFailure + ")");

            // (I) em falha, a IL original nao e mutada
            var keep = RealIl();
            int wKeep = FindWindow(keep);
            int before = keep.Count;
            var broken = new List<CodeInstruction>(keep);
            broken.RemoveAt(wKeep + 1);
            List<CodeInstruction> bOut;
            string bFail;
            bool bOk = BattleResultTranspiler.TryTransform(broken, target, out bOut, out bFail);
            Check(!bOk && bOut == null && keep.Count == before, "transpiler.no_partial_mutation_on_failure",
                "em falha TryTransform devolve false/result=null e nao devolve lista parcial",
                "falha com saida parcial: ok=" + bOk + " out=" + (bOut == null ? "null" : bOut.Count.ToString()));
        }

        private static string DescribeMaybe(CodeInstruction ci)
        {
            var mi = ci.operand as MethodInfo;
            return ci.opcode + " " + (mi != null ? mi.DeclaringType.Name + "::" + mi.Name : Convert.ToString(ci.operand));
        }

        private static void TestPatchTargets()
        {
            Section("ALVOS HARMONY REAIS (portao fail-closed do PatchRegistry)");
            try
            {
                List<PatchRegistry.Plan> plans;
                List<string> missing;
                bool ok = PatchRegistry.TryBuildPlans(out plans, out missing);
                Check(ok && missing.Count == 0, "registry.all_targets_resolve_on_real_dll",
                    "todos os " + plans.Count + " alvos do grupo de gameplay resolveram na Assembly-CSharp.dll real (sem alvo ausente -> sem rollback por alvo faltante)",
                    "alvos ausentes: " + string.Join(", ", missing.ToArray()) + " (plans=" + plans.Count + ")");

                var names = new List<string>();
                foreach (var p in plans) names.Add(p.Id);
                Check(names.Contains("Root.SendGameCompleteFromServer") && names.Contains("Character.get_MaxLevel")
                      && names.Contains("RoguelikeManager.GetSkillChoices") && names.Contains("Character.SyncCharacterToPreset"),
                    "registry.critical_targets_present",
                    "alvos criticos presentes: " + names.Count + " ids, incluindo o bloco de resultado, MaxLevel, GetSkillChoices e SyncCharacterToPreset",
                    "faltam alvos criticos: " + string.Join(", ", names.ToArray()));

                NotExercised("registry.apply_and_rollback_effective",
                    "aplicar de fato (Harmony.CreateProcessor/Patch) exige o leitor de IL do MonoMod, que neste host .NET 6 lanca NotSupportedException('Body-less method') mesmo para metodo do proprio harness (SPIKE da rodada 727); rollback efetivo nao pode ser exercitado aqui");
            }
            catch (Exception ex)
            {
                Fail("registry.suite", Flatten(ex));
            }
        }

        private static AdvanceInputs BaseInputs(int level)
        {
            return new AdvanceInputs
            {
                ModEnabled = true,
                IsAi = false,
                IsRoguelikeCharacter = true,
                IsMultiplayer = false,
                IsRoguelikeMode = true,
                Level = level,
                VanillaCap = 20,
                VoluntaryCap = 0,
                SafetyBound = 4000,
                CurveUsable = true,
                NextLevelRepresentable = true,
                StatBudgetOk = true,
                TargetsPresent = true
            };
        }

        private static void TestPolicyMatrix()
        {
            Section("MATRIZ DA POLITICA (PolicyCore - codigo real do mod)");

            int[] levels = new[] { 19, 20, 21, 29, 30, 31 };
            foreach (int lv in levels)
            {
                var i = BaseInputs(lv);
                AdvanceDenial denial;
                bool can = PolicyCore.CanAdvance(in i, out denial);
                string label = (lv - 1) + "->" + lv;
                Check(can && denial == AdvanceDenial.None, "policy.advance_" + label,
                    "nivel " + lv + " avanca (denial=" + denial + ")",
                    "nivel " + lv + " NAO avancou (denial=" + denial + ")");
            }

            // 19->20 dentro do escopo vanilla continua igual, e 20+ deixa de ser bloqueado pelo cap 20
            {
                var at20 = BaseInputs(20);
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in at20, out d);
                var at19 = BaseInputs(19);
                bool can19 = PolicyCore.CanAdvance(in at19, out d);
                Check(can && can19, "policy.cap20_removed_for_rogue",
                    "nivel 19 e 20 avancam sob a extensao (sem teto 20 de gameplay)",
                    "cap 20 ainda bloqueia: 19=" + can19 + " 20=" + can);
            }

            {
                var i = BaseInputs(25); i.IsAi = true;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.VanillaScope, "policy.ai_out_of_scope",
                    "IA fora do escopo ampliado: usa a comparacao vanilla (25 < 20 = false, denial=" + d + ")",
                    "IA entrou no escopo (can=" + can + " denial=" + d + ")");
            }
            {
                var i = BaseInputs(25); i.IsRoguelikeCharacter = false;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.VanillaScope, "policy.campaign_out_of_scope",
                    "campanha fora do escopo ampliado: comparacao vanilla intacta (denial=" + d + ")",
                    "campanha entrou no escopo (can=" + can + ")");
            }
            {
                var i = BaseInputs(25); i.IsMultiplayer = true;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.VanillaScope, "policy.multiplayer_out_of_scope",
                    "multiplayer fora do escopo: branch vanilla mantido (denial=" + d + ")",
                    "multiplayer entrou no escopo (can=" + can + ")");
            }
            {
                var i = BaseInputs(25); i.IsRoguelikeMode = false;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.VanillaScope, "policy.non_roguelike_mode_out_of_scope",
                    "modo nao-roguelike: comparacao vanilla (denial=" + d + ")",
                    "modo nao-roguelike ampliado (can=" + can + ")");
            }
            {
                var i = BaseInputs(25); i.ModEnabled = false;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.VanillaScope, "policy.mod_disabled_vanilla",
                    "General.Enabled=false reproduz o vanilla exato (denial=" + d + ")",
                    "mod desligado ampliou (can=" + can + ")");
            }
            {
                var i = BaseInputs(25); i.TargetsPresent = false;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.TargetMissing, "policy.missing_targets_refuse",
                    "alvo ausente: recusa sem premio (denial=" + d + ")",
                    "ampliou apesar de alvo ausente (can=" + can + " denial=" + d + ")");
            }
            {
                var i = BaseInputs(25); i.CurveUsable = false;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.NumericGuard, "policy.unusable_curve_refuse",
                    "curva F20/D20 inutilizavel: recusa (denial=" + d + ")",
                    "ampliou sem curva valida (can=" + can + ")");
            }
            {
                var i = BaseInputs(25); i.NextLevelRepresentable = false;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.NumericGuard, "policy.unrepresentable_next_level_refuse",
                    "proximo nivel nao representavel: recusa (denial=" + d + ")",
                    "ampliou com representacao invalida (can=" + can + ")");
            }
            {
                var i = BaseInputs(25); i.StatBudgetOk = false;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.NumericGuard, "policy.stat_budget_refuse",
                    "orcamento de pontos fora de int32/float exato: recusa (denial=" + d + ")",
                    "ampliou com pontos fora de faixa (can=" + can + ")");
            }
            {
                var i = BaseInputs(25); i.SafetyBound = 25;
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(!can && d == AdvanceDenial.SafetyBound, "policy.safety_bound_refuse",
                    "limite de representacao atingido: recusa (denial=" + d + ")",
                    "passou do limite de representacao (can=" + can + ")");
            }
            {
                var i = BaseInputs(24); i.VoluntaryCap = 25;
                AdvanceDenial d;
                bool ok1 = PolicyCore.CanAdvance(in i, out d);
                var i2 = BaseInputs(25); i2.VoluntaryCap = 25;
                bool ok2 = PolicyCore.CanAdvance(in i2, out d);
                AdvanceDenial d2;
                PolicyCore.CanAdvance(in i2, out d2);
                Check(ok1 && !ok2 && d2 == AdvanceDenial.VoluntaryCap, "policy.voluntary_cap",
                    "Progression.MaxLevel=25: 24 avanca e 25 para (denial=" + d2 + ")",
                    "teto voluntario nao respeitado: 24=" + ok1 + " 25=" + ok2);
            }
            {
                // config MENOR que o nivel atual nao rebaixa: EffectiveMaxLevel nunca fica abaixo do nivel
                var i = BaseInputs(30); i.VoluntaryCap = 25;
                double eff = PolicyCore.EffectiveMaxLevel(in i);
                AdvanceDenial d;
                bool can = PolicyCore.CanAdvance(in i, out d);
                Check(eff >= 30d && !can, "policy.lower_config_preserves_level",
                    "com nivel 30 e teto voluntario 25: EffectiveMaxLevel=" + eff + " (nao rebaixa) e nao avanca (denial=" + d + ")",
                    "rebaixou ou avancou: eff=" + eff + " can=" + can);
            }
            {
                var i = BaseInputs(20);
                double eff = PolicyCore.EffectiveMaxLevel(in i);
                bool finite = XpCurve.IsUsableNumber(eff);
                Check(finite && eff == 4000d, "policy.effective_max_level_finite",
                    "EffectiveMaxLevel devolve " + eff + " (finito, = limite de representacao) e nunca NaN/Inf",
                    "valor invalido: " + eff);
            }
            {
                var i = BaseInputs(20); i.SafetyBound = 0;
                double eff = PolicyCore.EffectiveMaxLevel(in i);
                Check(eff == 20d, "policy.effective_max_level_fallback_vanilla20",
                    "sem limite de representacao disponivel o teto efetivo volta ao cap vanilla 20 (" + eff + ")",
                    "fallback inesperado: " + eff);
            }
            {
                // duas vitorias: a decisao e determinista e nao muda entre chamadas
                var i1 = BaseInputs(20);
                var i2 = BaseInputs(21);
                AdvanceDenial d1, d2, d3;
                bool v1 = PolicyCore.CanAdvance(in i1, out d1);
                bool v2 = PolicyCore.CanAdvance(in i2, out d2);
                bool v1b = PolicyCore.CanAdvance(in i1, out d3);
                Check(v1 && v2 && v1b, "policy.two_victories_both_advance",
                    "20->21 e 21->22 avancam (duas vitorias, um nivel cada) e a decisao e determinista",
                    "duas vitorias falharam: " + v1 + "/" + v2 + "/" + v1b);
            }
        }

        private static void TestXpCurve()
        {
            Section("CURVA DE XP (XpCurve - codigo real do mod)");
            double f20 = 1234567d;      // valor de bancada: os reais (F20/D20) vem do jogo em runtime
            double d20 = 98765d;

            Check(XpCurve.Floor(f20, d20, 20) == f20 && XpCurve.Floor(f20, d20, 21) == f20 + d20,
                "xp.floor_matches_vanilla_at_20_and_21",
                "F(20)=F20 e F(21)=F20+D20 (extensao coincide com vanilla na fronteira)",
                "F(20)=" + XpCurve.Floor(f20, d20, 20) + " F(21)=" + XpCurve.Floor(f20, d20, 21));

            bool mono = true;
            double prev = XpCurve.Floor(f20, d20, 20);
            for (int l = 21; l <= 200; l++)
            {
                double cur = XpCurve.Floor(f20, d20, l);
                if (!(cur > prev)) mono = false;
                prev = cur;
            }
            Check(mono, "xp.floor_strictly_monotonic_20_200",
                "F(L) estritamente crescente de 20 a 200 (O(1) por nivel)",
                "monotonicidade quebrada");

            bool inv = true;
            bool exact = true;
            for (int l = 21; l <= 500; l++)
            {
                double floor = XpCurve.Floor(f20, d20, l);
                if (XpCurve.LevelIndexFromXp(f20, d20, floor) != l) inv = false;
                if (XpCurve.LevelIndexFromXp(f20, d20, floor - 1d) != l - 1) exact = false;
                double back = XpCurve.LevelFromXp(f20, d20, floor);
                if (Math.Abs(back - l) > 1e-6) exact = false;
            }
            Check(inv, "xp.level_index_inverse_21_500", "LevelIndexFromXp(F(L)) == L para L em 21..500",
                "inversa devolveu nivel errado em algum ponto");
            Check(exact, "xp.inverse_precision_boundary",
                "F(L)-1 cai em L-1 e a inversa analitica recupera L com erro < 1e-6 (fronteira exata)",
                "fronteira/precisao da inversa falhou");

            bool smooth = true;
            for (int l = 21; l <= 500; l++)
            {
                double xp = f20 + d20 * (l - 20) + d20 * 0.5d;
                double lvl = XpCurve.LevelFromXp(f20, d20, xp);
                if (Math.Abs(lvl - (l + 0.5d)) > 1e-6) smooth = false;
            }
            Check(smooth, "xp.fractional_level_roundtrip",
                "XpFromLevel/LevelFromXp coerentes no fracionario (meio nivel -> L+0.5) em 21..500",
                "fracionario divergente");

            Check(XpCurve.Transition(d20, 12345) == d20, "xp.transition_constant_after_20",
                "D(L)=D20 constante depois do 20 (XP por transicao linear)",
                "transicao nao constante");

            Check(!XpCurve.CurveUsable(double.NaN, d20) && !XpCurve.CurveUsable(f20, double.PositiveInfinity)
                  && !XpCurve.CurveUsable(f20, 0d) && !XpCurve.CurveUsable(f20, -1d) && !XpCurve.CurveUsable(-1d, d20)
                  && XpCurve.CurveUsable(f20, d20),
                "xp.curve_usable_guards",
                "CurveUsable rejeita NaN/Inf/zero/negativo e aceita o par valido (guarda numerica real)",
                "guarda numerica de CurveUsable falhou");

            int bound = XpCurve.SafetyBoundLevel(f20, d20, 5);
            int bound2 = XpCurve.SafetyBoundLevel(f20, d20, 20);
            int bound0 = XpCurve.SafetyBoundLevel(f20, d20, 0);
            Check(bound >= 21 && bound2 <= bound && bound0 >= bound && XpCurve.IsUsableNumber(bound),
                "xp.safety_bound_derived",
                "limite de representacao derivado dos parametros: 5 pontos/nivel=" + bound + ", 20 pontos/nivel=" + bound2 + ", sem pontos=" + bound0 + " (>=21, monotono)",
                "limite de representacao invalido: " + bound + "/" + bound2 + "/" + bound0);
        }

        private static void TestXpBackend()
        {
            Section("BACKEND DE XP (XpBackend - codigo real do mod, com seam PrimeForTests)");
            double f20 = 1234567d, d20 = 98765d;
            bool primed = XpBackend.PrimeForTests(f20, d20, 5);
            Check(primed, "xpbackend.prime_ok", "PrimeForTests aceitou o par valido (F20/D20 de bancada; os reais vem do jogo em runtime)",
                "PrimeForTests recusou o par valido");

            double v;
            bool floorAt20 = XpBackend.TryFloor(20, out v);
            bool floorAt21 = XpBackend.TryFloor(21, out v);
            Check(!floorAt20 && floorAt21 && v > f20, "xpbackend.floor_only_after_cap",
                "TryFloor(20) recusa (vanilla decide) e TryFloor(21) devolve " + v,
                "TryFloor fora do esperado: 20=" + floorAt20 + " 21=" + floorAt21);

            double t;
            bool trans = XpBackend.TryTransition(25, out t) && t == d20;
            Check(trans, "xpbackend.transition_after_cap", "TryTransition(25) = D20 (" + d20 + ")",
                "TryTransition invalido");

            bool nextOk = true;
            string detail = null;
            for (int l = 19; l <= 40; l++)
            {
                string d;
                if (!XpBackend.NextLevelRepresentable(l, out d)) { nextOk = false; detail = "L=" + l + ": " + d; break; }
            }
            Check(nextOk, "xpbackend.next_level_representable_19_40",
                "proximo nivel valido (finito, crescente, inversa exata) para L=19..40",
                "falhou: " + detail);

            string d2;
            bool statOk = XpBackend.StatBudgetOk(30, 5, out d2);
            bool statBad = !XpBackend.StatBudgetOk(30000000, 5, out d2);
            bool statBad2 = !XpBackend.StatBudgetOk(int.MaxValue - 3, 5, out d2);
            Check(statOk && statBad && statBad2, "xpbackend.stat_budget_long_checks",
                "orçamento de pontos checado em long: nivel 30 ok, 30M e int.MaxValue-3 recusados",
                "checagem de orçamento errada: ok=" + statOk + " bad=" + statBad + " bad2=" + statBad2);

            double lvl;
            bool lvlOk = XpBackend.TryLevelFromXp((float)(f20 + d20 * 5), out lvl);
            Check(lvlOk && Math.Abs(lvl - 25d) < 1e-4, "xpbackend.level_from_xp",
                "TryLevelFromXp(F(25)) = " + lvl, "inversa por XP invalida: " + lvl);

            bool belowFloor = !XpBackend.TryLevelFromXp((float)(f20 - 1d), out lvl);
            Check(belowFloor, "xpbackend.rejects_xp_below_floor20",
                "XP abaixo de F20 nao entra na extensao (vanilla responde)", "aceitou XP abaixo de F20");

            XpBackend.ResetForTests();
            bool notReadyFloor = !XpBackend.TryFloor(25, out v);
            Check(notReadyFloor, "xpbackend.not_ready_refuses",
                "sem backend pronto (Ready=false) as consultas recusam e a politica usa vanilla",
                "respondeu mesmo sem estar pronto");

            bool ensure = XpBackend.EnsureReady();
            Check(!ensure && XpBackend.LastError != null, "xpbackend.ensure_ready_fails_closed_without_game",
                "EnsureReady() no host sem runtime Unity falha e deixa LastError (fail-closed): " + XpBackend.LastError,
                "EnsureReady() disse estar pronto sem o jogo (ensure=" + ensure + ")");

            NotExercised("xpbackend.real_F20_D20_values",
                "F20/D20 reais vem de Character.GetExperienceFloorForLevel no runtime do jogo (GlobalSettings serializado segue NAO_EXERCITADO desde a R1); a bancada so pode provar a matematica com o par informado");
        }

        private static string TempDir(string tag)
        {
            var d = Path.Combine(Path.GetTempPath(), "rlp-harness-" + tag + "-" + Guid.NewGuid().ToString("N").Substring(0, 8));
            Directory.CreateDirectory(d);
            return d;
        }

        private static void TestLedger()
        {
            Section("LEDGER/Recibos (ReceiptLedgerStore + LedgerService - codigo real do mod)");
            string dir = TempDir("ledger");
            string guid = "char-guid-0001";
            string preset = "preset-aaa";
            var store = new ReceiptLedgerStore(dir);
            LedgerService.ConfigureStoreForTests(store);

            LedgerDocument doc;
            string error;
            var st = store.Load(guid, preset, out doc, out error);
            Check(st == LedgerLoadStatus.Missing && doc == null && LedgerService.ReceiptCountByGuid(guid, preset) == 0,
                "ledger.missing_creates_new_run",
                "arquivo ausente = Missing e S=0 (nada consumido)",
                "esperava Missing/S=0, veio " + st + "/" + LedgerService.ReceiptCountByGuid(guid, preset));

            bool r1 = LedgerService.TryRecordSkippedSkillByGuid(guid, preset, 21, out error);
            bool r2 = LedgerService.TryRecordSkippedSkillByGuid(guid, preset, 22, out error);
            int s = LedgerService.ReceiptCountByGuid(guid, preset);
            Check(r1 && r2 && s == 2, "ledger.two_receipts_recorded",
                "dois recibos de pool vazio gravados (S=2) sem erro",
                "falha ao gravar recibos: r1=" + r1 + " r2=" + r2 + " s=" + s + " err=" + error);

            string jsonPath = store.PathFor(guid);
            Check(File.Exists(jsonPath), "ledger.sidecar_path",
                "sidecar em " + jsonPath + " (padrao Paths.ConfigPath/com.gumatos.roguelikelevelprogression/receipts/<guid>.json)",
                "sidecar nao criado em " + jsonPath);

            string written = File.Exists(jsonPath) ? File.ReadAllText(jsonPath) : "";
            Check(written.Contains("\"schema_version\":1") && written.Contains("empty_skill_pool")
                  && written.Contains("\"character_guid\":\"" + guid + "\"") && written.Contains("\"run_id\":\"")
                  && written.Contains("\"preset_guid\":\"" + preset + "\"") && written.Contains("skipped_skill_receipts"),
                "ledger.sidecar_schema_v1",
                "sidecar contem schema_version/character_guid/run_id/preset_guid/skipped_skill_receipts e motivo empty_skill_pool",
                "schema do sidecar inesperado: " + Short(written));

            // reload: instancia nova do servico le o disco
            LedgerService.ConfigureStoreForTests(new ReceiptLedgerStore(dir));
            int sReload = LedgerService.ReceiptCountByGuid(guid, preset);
            Check(sReload == 2, "ledger.reload_from_disk", "apos reload (cache limpo) S=" + sReload + " (dois recibos persistidos)",
                "reload perdeu recibos: S=" + sReload);

            string bak = store.BackupPathFor(guid);
            Check(File.Exists(bak), "ledger.backup_written", "backup " + Path.GetFileName(bak) + " criado no replace atomico",
                "backup ausente");
            var tmpLeft = Directory.GetFiles(dir, "*.tmp");
            Check(tmpLeft.Length == 0, "ledger.atomic_no_tmp_left", "nenhum .tmp sobrou no diretorio do ledger",
                "arquivos temporarios orfaos: " + tmpLeft.Length);

            // dedupe de ordinal
            var d = new LedgerDocument { CharacterGuid = guid, RunId = "x", PresetGuid = preset };
            bool a1 = d.AddReceipt(1, 21, ReceiptReasons.EmptySkillPool);
            bool a2 = d.AddReceipt(1, 22, ReceiptReasons.EmptySkillPool);
            Check(a1 && !a2 && d.SkippedSkillCount == 1, "ledger.ordinal_dedupe",
                "AddReceipt com ordinal repetido devolve false e nao duplica (S=1)",
                "dedupe falhou: a1=" + a1 + " a2=" + a2 + " S=" + d.SkippedSkillCount);

            // corrupcao: nao consome recompensa
            File.WriteAllText(jsonPath, "{ isto nao e json valido", new UTF8Encoding(false));
            LedgerService.ConfigureStoreForTests(new ReceiptLedgerStore(dir));
            int sCorrupt = LedgerService.ReceiptCountByGuid(guid, preset);
            bool recCorrupt = LedgerService.TryRecordSkippedSkillByGuid(guid, preset, 23, out error);
            Check(sCorrupt == 0 && !recCorrupt && error != null, "ledger.corrupted_not_consumed",
                "sidecar corrompido: S=0 e recibo recusado (" + error + ") - a recompensa NAO e consumida",
                "corrompido consumiu recompensa: S=" + sCorrupt + " rec=" + recCorrupt + " err=" + error);

            // schema nao suportado
            File.WriteAllText(jsonPath, "{\"schema_version\":2,\"character_guid\":\"" + guid + "\",\"run_id\":\"r\",\"preset_guid\":\"" + preset + "\",\"skipped_skill_receipts\":[]}", new UTF8Encoding(false));
            LedgerService.ConfigureStoreForTests(new ReceiptLedgerStore(dir));
            var st2 = store.Load(guid, preset, out doc, out error);
            Check(st2 == LedgerLoadStatus.UnsupportedSchema && LedgerService.ReceiptCountByGuid(guid, preset) == 0,
                "ledger.unsupported_schema_refused",
                "schema_version=2 = UnsupportedSchema e S=0 (nao interpreta formato desconhecido)",
                "schema desconhecido aceito: " + st2);

            // divergencia de identidade (preset)
            File.WriteAllText(jsonPath, "{\"schema_version\":1,\"character_guid\":\"" + guid + "\",\"run_id\":\"r\",\"preset_guid\":\"outro-preset\",\"skipped_skill_receipts\":[{\"ordinal\":1,\"earned_level\":21,\"reason\":\"empty_skill_pool\"}]}", new UTF8Encoding(false));
            LedgerService.ConfigureStoreForTests(new ReceiptLedgerStore(dir));
            var st3 = store.Load(guid, preset, out doc, out error);
            Check(st3 == LedgerLoadStatus.IdentityMismatch && LedgerService.ReceiptCountByGuid(guid, preset) == 0,
                "ledger.identity_mismatch_refused",
                "preset_guid divergente = IdentityMismatch e S=0 (ledger de outra run nao conta)",
                "identidade divergente aceita: " + st3);

            // ordinal duplicado no arquivo = corrompido
            File.WriteAllText(jsonPath, "{\"schema_version\":1,\"character_guid\":\"" + guid + "\",\"run_id\":\"r\",\"preset_guid\":\"" + preset + "\",\"skipped_skill_receipts\":[{\"ordinal\":1,\"earned_level\":21,\"reason\":\"empty_skill_pool\"},{\"ordinal\":1,\"earned_level\":22,\"reason\":\"empty_skill_pool\"}]}", new UTF8Encoding(false));
            LedgerDocument dupDoc; string dupErr;
            var stDup = LedgerDocument.Parse(File.ReadAllText(jsonPath), out dupDoc, out dupErr);
            Check(stDup == LedgerParseStatus.Corrupted, "ledger.duplicate_ordinal_is_corrupt",
                "ordinal duplicado no arquivo = Corrupted (" + dupErr + ")",
                "duplicata aceita: " + stDup);

            // limpa e recomeca
            File.Delete(jsonPath);
            LedgerService.ConfigureStoreForTests(new ReceiptLedgerStore(dir));
            LedgerService.TryRecordSkippedSkillByGuid(guid, preset, 21, out error);

            // run reset SO depois de SyncCharacterToPreset valido
            string runBefore = SnapshotRunId(jsonPath);
            LedgerService.OnPresetSyncSuccessByGuid(guid, null);
            int sAfterNull = LedgerService.ReceiptCountByGuid(guid, preset);
            LedgerService.OnPresetSyncSuccessByGuid(guid, preset);
            int sAfterReset = LedgerService.ReceiptCountByGuid(guid, preset);
            string runAfter = SnapshotRunId(jsonPath);
            Check(sAfterNull == 1 && sAfterReset == 0 && runAfter != runBefore && runAfter != "?" && runAfter != "",
                "ledger.run_reset_only_with_preset",
                "preset nulo NAO reseta (S=1); preset valido reseta (S=0) com run_id novo (" + runBefore + " -> " + runAfter + ")",
                "reset indevido: sNull=" + sAfterNull + " sReset=" + sAfterReset + " run=" + runBefore + "->" + runAfter);

            // reload apos o reset
            LedgerService.ConfigureStoreForTests(new ReceiptLedgerStore(dir));
            Check(LedgerService.ReceiptCountByGuid(guid, preset) == 0, "ledger.reset_persisted",
                "reset persistido no disco (reload = S=0)", "reset nao persistiu");

            // falha de escrita NAO consome recompensa
            string root = TempDir("writefail");
            string blocker = Path.Combine(root, "blocker");
            File.WriteAllText(blocker, "sou um arquivo, nao um diretorio", new UTF8Encoding(false));
            var badStore = new ReceiptLedgerStore(Path.Combine(blocker, "receipts"));
            LedgerService.ConfigureStoreForTests(badStore);
            string badGuid = "char-writefail";
            string wErr;
            bool wOk = LedgerService.TryRecordSkippedSkillByGuid(badGuid, preset, 21, out wErr);
            int wCount = LedgerService.ReceiptCountByGuid(badGuid, preset);
            Check(!wOk && wErr != null && wCount == 0, "ledger.write_failure_does_not_consume",
                "falha de gravacao: recibo recusado (" + Short(wErr) + ") e S continua 0 (rollback em memoria)",
                "falha de escrita consumiu recompensa: ok=" + wOk + " S=" + wCount);

            bool wOk2 = LedgerService.TryRecordSkippedSkillByGuid(badGuid, preset, 21, out wErr);
            Check(!wOk2, "ledger.write_failure_repeatable",
                "nova tentativa com o mesmo problema continua recusando (nada e concedido parcialmente)",
                "segunda tentativa passou: " + wOk2);

            // store volta a funcionar: a recompensa pode ser registrada depois
            var goodStore = new ReceiptLedgerStore(TempDir("recover"));
            LedgerService.ConfigureStoreForTests(goodStore);
            bool recOk = LedgerService.TryRecordSkippedSkillByGuid(badGuid, preset, 21, out wErr);
            Check(recOk && LedgerService.ReceiptCountByGuid(badGuid, preset) == 1, "ledger.retry_after_failure_succeeds",
                "depois do store voltar a funcionar o recibo e gravado (S=1): recompensa nao foi perdida",
                "retentativa falhou: " + recOk + " err=" + wErr);

            // dedupe logico: mesmo nivel, mesmo motivo, sem duplicacao de recompensa
            bool again = LedgerService.TryRecordSkippedSkillByGuid(badGuid, preset, 21, out wErr);
            Check(again && LedgerService.ReceiptCountByGuid(badGuid, preset) == 2, "ledger.sequential_records_get_distinct_ordinals",
                "registros sequenciais recebem ordinais distintos (S=2) - um recibo por nivel perdido",
                "ordinal/contagem inesperada: " + LedgerService.ReceiptCountByGuid(badGuid, preset));

            NotExercised("ledger.queue_subtraction_on_real_character",
                "RewardQueryPatches.PostfixNeededCount (subtracao de S na contagem da fila) e LedgerService.ReceiptCount(Character)/IdentityOf exigem uma instancia real de Character (CharacterSaveFile, CharacterPresetFileGuid, OwnerID) que so existe no runtime Unity; a contagem por guid acima exercita o mesmo caminho de load/cache/rollback");
        }

        private static string SnapshotRunId(string path)
        {
            try
            {
                LedgerDocument d; string e;
                if (LedgerDocument.Parse(File.ReadAllText(path), out d, out e) == LedgerParseStatus.Ok) return d.RunId;
            }
            catch (Exception) { }
            return "?";
        }

        private static string Short(string s)
        {
            if (s == null) return "";
            s = s.Replace('\n', ' ');
            return s.Length > 120 ? s.Substring(0, 120) + "..." : s;
        }

        private static void TestGuardsStaticEntryPoints()
        {
            Section("ENTRADAS ESTATICAS DOS PATCHES SEM RUNTIME UNITY (fora de escopo = vanilla)");
            try
            {
                XpBackend.PrimeForTests(1234567d, 98765d, 5);
                ExtensionScope.ResetForTests();

                float res = 111f;
                bool runVanilla = XpStaticPatches.PrefixFloor(25, ref res);
                Check(runVanilla && res == 111f, "patches.scope_inactive_keeps_vanilla_floor",
                    "com ExtensionScope inativo (campanha/IA/fora de escopo) PrefixFloor devolve true e nao mexe no resultado (vanilla intacto)",
                    "extensao atuou fora do escopo: runVanilla=" + runVanilla + " res=" + res);

                bool runVanilla2 = XpStaticPatches.PrefixNext(25, ref res);
                Check(runVanilla2 && res == 111f, "patches.scope_inactive_keeps_vanilla_transition",
                    "PrefixNext fora do escopo = vanilla (sem tocar no resultado)",
                    "PrefixNext atuou fora do escopo: " + runVanilla2);

                int idxRes = 7;
                bool runVanilla3 = XpStaticPatches.PrefixLevelIndex((float)(1234567d + 98765d * 5), ref idxRes);
                Check(runVanilla3 && idxRes == 7, "patches.scope_inactive_keeps_vanilla_level_index",
                    "PrefixLevelIndex fora do escopo = vanilla (sem tocar no resultado)",
                    "PrefixLevelIndex atuou fora do escopo: " + runVanilla3);

                Check(!ExtensionScope.Active && ExtensionScope.Depth == 0 && ExtensionScope.Owner == null
                      && !ExtensionScope.AppliesTo(null) && !ExtensionScope.Push(null) && ExtensionScope.CurrentExtended() == null,
                    "scope.invariants_and_fail_closed",
                    "escopo inativo por padrao, Push(null) recusado, CurrentExtended() nulo e AppliesTo(null)=false (fail-closed)",
                    "invariantes do escopo violadas");

                // GameState sem rede/jogo: deve tratar como multiplayer (nao ampliar)
                Check(GameState.IsMultiplayer(), "gamestate.no_network_means_multiplayer",
                    "sem NetworkingManager disponivel GameState.IsMultiplayer()=true: o mod NAO amplia escopo (fail-closed)",
                    "GameState.IsMultiplayer() retornou false sem jogo carregado");
            }
            catch (Exception ex)
            {
                Fail("patches.static_entrypoints", Flatten(ex));
            }
        }

        private static void DeclareNotExercised()
        {
            Section("NAO EXERCITADO NESTA BANCADA (motivo declarado, sem PASS fabricado)");
            NotExercised("harmony.runtime_patch_application",
                "PatchProcessor/Patch do Harmony depende do leitor de IL do MonoMod, indisponivel neste host .NET 6 (NotSupportedException 'Body-less method'); a aplicacao real dos patches no processo do jogo fica para o runtime/BepInEx");
            NotExercised("gameplay.battle_result_at_runtime",
                "SendGameCompleteFromServer original exige GUIManager/GameLogic/UnityEngine; so o transpiler e a decisao da politica foram exercitados");
            NotExercised("gameplay.levels_21_to_31_in_game",
                "precisa do jogo aberto com personagem roguelike real (fora do escopo desta fase: sem instalar, sem abrir jogo, sem tocar no perfil do dono)");
            NotExercised("gameplay.legacy_mirror_and_save",
                "Character.ExperienceLevelDidSet/OldExperienceConverter/QueueCharacterSave exigem Character carregado e o save real");
            NotExercised("rewards.skill_and_item_pools",
                "RoguelikeManager.GetSkillChoices/GetItemChoices/OpenSkillSelectWindow/RerollSkill exigem instancia real de RoguelikeManager, botoes e pool de itens/skills");
            NotExercised("rewards.queue_subtraction",
                "PostfixNeededCount precisa de Character real; a contagem equivalente por guid foi exercitada no ledger");
            NotExercised("ui.inventory_and_skillbar",
                "InventoryManager.RefreshHealthbars/Skillbar.UpdateExpBar exigem instancias Unity e textos TMP; apenas as guardas de escopo e o teto efetivo (PolicyCore) foram exercitados");
            NotExercised("multiplayer.branch_vanilla",
                "branch multiplayer e decidido por Root.PlayingMultiplayer em rede real; a politica foi exercitada com IsMultiplayer=true (PolicyCore)");
            NotExercised("save.owner_profile_roundtrip",
                "backup/restauracao de save+sidecar no perfil do dono esta fora do escopo autorizado desta fase");
            NotExercised("xp.real_serialized_parameters",
                "GlobalSettings serializado (ExperienceBasePerLevel/ExperienceExponentialGainPerLevel/ExperienceOffset/NumStatsPerNewLevel) nao pode ser lido (parser EOF desde a R1); F20/D20 reais vem do jogo em runtime");
            NotExercised("plugin.bepinex_lifecycle",
                "Plugin.Awake/config (BaseUnityPlugin) exige o host BepInEx carregado dentro do jogo");
        }
    }
}
