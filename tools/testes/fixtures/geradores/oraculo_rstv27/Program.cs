// oraculo_rstv27: gera a fixture rstv27-rodape-valor (RSTV-27).
//
// POR QUE ISTO EXISTE (e por que e' C# e nao Python)
// --------------------------------------------------
// O defeito do RSTV-27 e' um NUMERO ERRADO no rodape da tooltip de skill ativa (mana /
// cooldown / alcance) quando a janela read-only monta a tooltip na tela Party Select. O
// valor esperado NAO pode sair da mesma implementacao que o teste Python usa - senao o
// teste passa por construcao (regra do tools/testes/README.md). Entao o esperado sai
// daqui: um programa em C# que passa pelo MESMO caminho de conta do MOTOR, transcrito do
// decompilado do `ActionInfo` (lib/Assembly-CSharp.dll):
//
//   * mana      GetManaCost(Character)  = Max(0, Ceil(base * ratio * (1+ManaCostMod/100)
//                                            * (1+ManaCostMod<SkillType>/100)
//                                            * (1 + (Level-1) * manaScalePerLevelPercentage/100)))
//               GetManaCost()           = Floor(base * ratio)
//   * cooldown  GetActionCooldown(Character) = Floor(Eval(Cooldown, Source=character))
//                                            + CooldownMod + CooldownMod<SkillType>  (Max(1,..) se > 1)
//               GetActionCooldown()     = Floor(Eval(Cooldown, parametros default))
//   * alcance   GetSimpleRange(Character, TargetInfo)
//               = Max(SimpleRange != 0 ? 1 : 0, SimpleRange + RangeAdderMelee/Ranged)  (teto de cego)
//               GetSimpleRange(TargetInfo) = SimpleRange cru
//
// O caminho do RODAPE (decompilado do `Tooltip.ShowSkillTooltip`) e' o ternario
// `tooltipCharacter == null ? <sem personagem> : <com personagem>`: este oraculo calcula os
// DOIS lados, e o teste Python prende QUAL deles a montagem do mod escolhe.
//
// FALHA EM VEZ DE CHUTAR: se o cenario nao declarar uma grandeza usada, este programa sai 1
// dizendo o que faltou; e se os dois caminhos NAO divergirem em nenhum campo, sai 1 tambem
// (o caso nao provaria nada).
//
// USO:
//   dotnet run --project tools/testes/fixtures/geradores/oraculo_rstv27 -- tools/testes/fixtures

using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace OraculoRstv27
{
    // ------------------------------------------------------------------ modelos (cenario)

    internal sealed class Globais
    {
        [JsonPropertyName("manaCostBase")] public float ManaCostBase { get; set; }
        [JsonPropertyName("manaScalePerLevelPercentage")] public float ManaScalePerLevel { get; set; }
    }

    internal sealed class Alvo
    {
        [JsonPropertyName("SimpleRange")] public int SimpleRange { get; set; }
    }

    internal sealed class Skill
    {
        [JsonPropertyName("nome")] public string Nome { get; set; }
        [JsonPropertyName("SkillType")] public string SkillType { get; set; }
        [JsonPropertyName("ManaCostRatio")] public float ManaCostRatio { get; set; }
        [JsonPropertyName("Cooldown")] public string Cooldown { get; set; }
        [JsonPropertyName("tags")] public List<string> Tags { get; set; }
        [JsonPropertyName("target")] public Alvo Target { get; set; }
    }

    internal sealed class Personagem
    {
        [JsonPropertyName("IsAI")] public bool IsAI { get; set; }
        [JsonPropertyName("Level")] public float Level { get; set; }
        [JsonPropertyName("ManaUnlimited")] public float ManaUnlimited { get; set; }
        [JsonPropertyName("ManaCostMod")] public float ManaCostMod { get; set; }
        [JsonPropertyName("ManaCostModDoTipo")] public float ManaCostModDoTipo { get; set; }
        [JsonPropertyName("CooldownMod")] public float CooldownMod { get; set; }
        [JsonPropertyName("CooldownModDoTipo")] public float CooldownModDoTipo { get; set; }
        [JsonPropertyName("RangeAdderMelee")] public int RangeAdderMelee { get; set; }
        [JsonPropertyName("RangeAdderRanged")] public int RangeAdderRanged { get; set; }
        [JsonPropertyName("IsBlind")] public bool IsBlind { get; set; }
    }

    internal sealed class Entrada
    {
        [JsonPropertyName("caso")] public string Caso { get; set; }
        [JsonPropertyName("globais")] public Globais Globais { get; set; }
        [JsonPropertyName("skill")] public Skill Skill { get; set; }
        [JsonPropertyName("personagens")] public Dictionary<string, Personagem> Personagens { get; set; }
        [JsonPropertyName("cenario")] public Dictionary<string, JsonElement> Cenario { get; set; }
    }

    internal static class Programa
    {
        private static readonly JsonSerializerOptions Opcoes = new JsonSerializerOptions
        {
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
        };

        // ------------------------------------------------- caminho de conta do motor

        /// <summary>Mathf.CeilToInt (a convencao da ficha).</summary>
        private static int CeilToInt(float v)
        {
            return (int)Math.Ceiling((double)v);
        }

        /// <summary>Mathf.FloorToInt.</summary>
        private static int FloorToInt(float v)
        {
            return (int)Math.Floor((double)v);
        }

        /// <summary>
        /// O `Game.Eval&lt;float&gt;(Cooldown, ...)` do motor. Neste caso o Cooldown do cenario e' um
        /// LITERAL numerico (declarado no entrada): o oraculo aceita so' isso e FALHA em vez de
        /// inventar um avaliador de expressao. A divergencia dos dois caminhos vem do CooldownMod,
        /// que so' o caminho COM personagem soma.
        /// </summary>
        private static float EvalLiteral(string expressao)
        {
            float v;
            if (!float.TryParse((expressao ?? "").Trim(), NumberStyles.Float,
                                CultureInfo.InvariantCulture, out v))
            {
                throw new InvalidOperationException(
                    "o oraculo so' avalia Cooldown LITERAL; veio: " + (expressao ?? "(vazio)"));
            }
            return v;
        }

        /// <summary>ActionInfo.GetManaCost() - o caminho SEM personagem.</summary>
        private static int ManaSemPersonagem(Entrada e)
        {
            return FloorToInt(e.Globais.ManaCostBase * e.Skill.ManaCostRatio);
        }

        /// <summary>ActionInfo.GetManaCost(Character) - o caminho COM personagem.</summary>
        private static int ManaComPersonagem(Entrada e, Personagem c)
        {
            if (c.ManaUnlimited > 0f)
            {
                return 0;
            }
            float num = e.Globais.ManaCostBase * e.Skill.ManaCostRatio;
            num *= 1f + c.ManaCostMod / 100f;
            // Game.Instance.GetAttribute("ManaCostMod" + SkillType): o atributo existe no motor e o
            // valor dele e' o do personagem (0 no caso declarado).
            num *= 1f + c.ManaCostModDoTipo / 100f;
            if (!c.IsAI)
            {
                float n5 = c.Level - 1f;
                num *= 1f + n5 * e.Globais.ManaScalePerLevel / 100f;
            }
            return Math.Max(0, CeilToInt(num));
        }

        /// <summary>ActionInfo.GetActionCooldown() - o caminho SEM personagem.</summary>
        private static int CooldownSemPersonagem(Entrada e)
        {
            if (string.IsNullOrWhiteSpace(e.Skill.Cooldown))
            {
                return 0;
            }
            return FloorToInt(EvalLiteral(e.Skill.Cooldown));
        }

        /// <summary>ActionInfo.GetActionCooldown(Character) - o caminho COM personagem.</summary>
        private static int CooldownComPersonagem(Entrada e, Personagem c)
        {
            if (string.IsNullOrWhiteSpace(e.Skill.Cooldown))
            {
                return 0;
            }
            int num = FloorToInt(EvalLiteral(e.Skill.Cooldown));
            if (num > 1)
            {
                int mod = (int)c.CooldownMod;          // (int)character["CooldownMod"]
                mod += (int)c.CooldownModDoTipo;        // (int)character["CooldownMod" + SkillType]
                num = Math.Max(1, num + mod);
            }
            return num;
        }

        /// <summary>ActionInfo.GetSimpleRange(TargetInfo) - o caminho SEM personagem.</summary>
        private static int AlcanceSemPersonagem(Entrada e)
        {
            return e.Skill.Target.SimpleRange;
        }

        /// <summary>ActionInfo.GetSimpleRange(Character, TargetInfo) - o caminho COM personagem.</summary>
        private static int AlcanceComPersonagem(Entrada e, Personagem c)
        {
            int num = e.Skill.Target.SimpleRange != 0 ? 1 : 0;
            int num2 = e.Skill.Target.SimpleRange;
            if (e.Skill.Tags != null && e.Skill.Tags.Contains("Melee"))
            {
                num2 += c.RangeAdderMelee;
            }
            if (e.Skill.Tags != null && e.Skill.Tags.Contains("Ranged"))
            {
                num2 += c.RangeAdderRanged;
            }
            if (c.IsBlind && num2 > num)
            {
                num2 = num;
            }
            return Math.Max(num, num2);
        }

        // ------------------------------------------------------------------ main

        private static int Main(string[] args)
        {
            string destino = Path.GetFullPath(args.Length > 0 ? args[0] : ".");
            string caminhoEntrada = Path.Combine(destino, "rstv27-rodape-valor.entrada.json");
            if (!File.Exists(caminhoEntrada))
            {
                Console.Error.WriteLine("FALHA(1): cenario ausente: " + caminhoEntrada
                    + "\n  -> o oraculo calcula o ESPERADO a partir do cenario versionado; sem ele nao ha prova.");
                return 1;
            }

            Entrada entrada;
            try
            {
                entrada = JsonSerializer.Deserialize<Entrada>(File.ReadAllText(caminhoEntrada, Encoding.UTF8));
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine("FALHA(1): nao consegui ler o cenario: " + ex.Message);
                return 1;
            }
            if (entrada == null || entrada.Globais == null || entrada.Skill == null
                || entrada.Skill.Target == null || entrada.Personagens == null || entrada.Personagens.Count == 0)
            {
                Console.Error.WriteLine("FALHA(1): o cenario esta incompleto (globais/skill/target/personagens).");
                return 1;
            }

            var semPersonagem = new Dictionary<string, object>
            {
                ["mana"] = ManaSemPersonagem(entrada),
                ["cooldown"] = CooldownSemPersonagem(entrada),
                ["alcance"] = AlcanceSemPersonagem(entrada),
            };

            var porPersonagem = new Dictionary<string, Dictionary<string, object>>();
            var divergencias = new List<string>();
            foreach (KeyValuePair<string, Personagem> par in entrada.Personagens.OrderBy(p => p.Key, StringComparer.Ordinal))
            {
                var valores = new Dictionary<string, object>
                {
                    ["mana"] = ManaComPersonagem(entrada, par.Value),
                    ["cooldown"] = CooldownComPersonagem(entrada, par.Value),
                    ["alcance"] = AlcanceComPersonagem(entrada, par.Value),
                };
                porPersonagem[par.Key] = valores;

                bool divergiu = false;
                foreach (string campo in new[] { "mana", "cooldown", "alcance" })
                {
                    if (!Equals(valores[campo], semPersonagem[campo]))
                    {
                        divergiu = true;
                    }
                }
                if (!divergiu)
                {
                    Console.Error.WriteLine("FALHA(1): o personagem '" + par.Key
                        + "' da' EXATAMENTE os mesmos numeros da base nos 3 campos -"
                        + " um caso assim nao prova nada (o teste nao morderia o defeito).");
                    return 1;
                }
                divergencias.Add(par.Key);
            }

            var esperado = new Dictionary<string, object>
            {
                ["caso"] = "rstv27-rodape-valor",
                ["procedencia"] = "oraculo_rstv27 (C#) - GERADO, nunca somado a mao: o caminho de conta do "
                    + "motor transcrito do decompilado do ActionInfo (lib/Assembly-CSharp.dll), com "
                    + "aritmetica FLOAT e as conversoes Mathf.CeilToInt / Mathf.FloorToInt / Mathf.Max",
                ["gerado_por"] = "tools/testes/fixtures/geradores/oraculo_rstv27",
                ["caminhos"] = new Dictionary<string, object>
                {
                    ["sem_personagem"] = "Tooltip.ShowSkillTooltip com `tooltipCharacter = TooltipCharacter` null: "
                        + "ActionInfo.GetManaCost() / GetActionCooldown() / GetSimpleRange(TargetInfo)",
                    ["com_personagem"] = "Tooltip.ShowSkillTooltip com `tooltipCharacter` != null: "
                        + "ActionInfo.GetManaCost(Character) / GetActionCooldown(Character) / GetSimpleRange(Character, TargetInfo)",
                },
                ["sem_personagem"] = semPersonagem,
                ["por_personagem"] = porPersonagem,
                ["personagens_com_divergencia"] = divergencias,
            };

            string caminhoEsperado = Path.Combine(destino, "rstv27-rodape-valor.esperado.json");
            File.WriteAllText(caminhoEsperado, JsonSerializer.Serialize(esperado, Opcoes) + "\n",
                              new UTF8Encoding(false));

            Console.WriteLine("escrito: " + caminhoEsperado);
            Console.WriteLine();
            Console.WriteLine("  caminho SEM personagem (o defeito): mana=" + semPersonagem["mana"]
                + " cooldown=" + semPersonagem["cooldown"] + " alcance=" + semPersonagem["alcance"]);
            foreach (KeyValuePair<string, Dictionary<string, object>> par in porPersonagem)
            {
                Console.WriteLine("  caminho COM personagem '" + par.Key.PadRight(8) + "': mana="
                    + par.Value["mana"] + " cooldown=" + par.Value["cooldown"]
                    + " alcance=" + par.Value["alcance"]);
            }
            return 0;
        }
    }
}
