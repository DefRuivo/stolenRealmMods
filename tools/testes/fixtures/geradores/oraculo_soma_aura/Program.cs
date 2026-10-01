// oraculo_soma_aura: gera as fixtures de escala de aura de shrine.
//
// POR QUE ISTO EXISTE (e por que nao e Python)
// --------------------------------------------
// A formula do motor e `Mathf.Round(BASE * (1 + bonus/100))`, com aritmetica
// FLOAT (single). Unity:
//
//     public static float Round(float f) => (float)Math.Round(f);   // ToEven
//
// O que engana quem reproduz isso "a mao":
//   1. Math.Round e "round half to EVEN" (bancario): 62.5 -> 62, nao 63.
//      E o vocabulario BORDAS do plano ("fracao .5 e -0.4").
//   2. O fator e float, nao double. Neste caso concreto eu conferi que os dois
//      caminhos dao o MESMO resultado para todo par (base, bonus) ALCANCAVEL no
//      jogo (ver AUDITORIA abaixo, impressa e gravada na fixture). Fora do
//      alcancavel eles divergem - por isso a auditoria existe em vez da minha
//      palavra: se um dia alguem ampliar os bonus, a divergencia aparece.
//
// Este oraculo passa pelo caminho do motor e ESCREVE o JSON que vira a fixture
// versionada. O teste em Python (t_exemplo_soma_aura.py) reimplementa a formula
// e confere contra ESTE arquivo - isto e, contra o motor, nao contra a propria
// implementacao (uma fixture gerada pelo proprio testado nao prova nada).
//
// USO:  dotnet run --project tools/testes/fixtures/geradores/oraculo_soma_aura -- tools/testes/fixtures

using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace OraculoSomaAura
{
    internal static class Programa
    {
        private sealed class Cenario
        {
            [JsonPropertyName("id")] public string Id { get; set; }
            [JsonPropertyName("base")] public int Base { get; set; }
            [JsonPropertyName("bonus")] public int Bonus { get; set; }
            [JsonPropertyName("nota")] public string Nota { get; set; }
        }

        private sealed class Resultado
        {
            [JsonPropertyName("id")] public string Id { get; set; }
            [JsonPropertyName("valor")] public int Valor { get; set; }
        }

        // As bases do censo de auras (docs/PLANO-DE-TESTES.md / skill do projeto).
        private static readonly int[] Bases = { -25, 0, 5, 8, 10, 20, 25, 50 };

        // As FONTES do bonus "ShrineEffectBonus": Omnism I (+8), Omnism II (+20),
        // Horn of Devotion (+50 e +100) e Worship (+100). Sao as unicas do jogo.
        private static readonly int[] FontesBonus = { 8, 20, 50, 100 };

        // O CAMINHO DO MOTOR: fator em float, produto em float, Math.Round ToEven.
        private static int Escala(int baseVal, int bonus)
        {
            float fator = 1f + (float)bonus / 100f;
            float produto = (float)baseVal * fator;
            return (int)Math.Round(produto, MidpointRounding.ToEven);
        }

        // A MESMA conta em double, so para auditar. Nao entra na fixture.
        private static int EscalaDouble(int baseVal, int bonus)
        {
            double fator = 1.0 + (double)bonus / 100.0;
            double produto = (double)baseVal * fator;
            return (int)Math.Round(produto, MidpointRounding.ToEven);
        }

        private static readonly Cenario[] Cenarios = new[]
        {
            new Cenario { Id = "sem-bonus",        Base = 20,  Bonus = 0,    Nota = "bonus zero: o valor e a base" },
            new Cenario { Id = "omnism1",          Base = 20,  Bonus = 8,    Nota = "Omnism I (+8)" },
            new Cenario { Id = "omnism2",          Base = 20,  Bonus = 20,   Nota = "Omnism II (+20)" },
            new Cenario { Id = "worship",          Base = 20,  Bonus = 100,  Nota = "Worship (+100) sozinho" },
            new Cenario { Id = "horn-50",          Base = 20,  Bonus = 50,   Nota = "Horn of Devotion, anel +50" },
            new Cenario { Id = "horn-100",         Base = 20,  Bonus = 100,  Nota = "Horn of Devotion, anel +100" },
            new Cenario { Id = "worship-omnism2",  Base = 20,  Bonus = 120,  Nota = "EXCESSO DE SHRINE: Worship (+100) + Omnism II (+20). O defeito plantado soma 20+20=40 a mao; o motor da 44" },
            new Cenario { Id = "tres-bencaos",     Base = 20,  Bonus = 270,  Nota = "EXCESSO DE SHRINE: Worship + os dois Horn + Omnism II" },
            new Cenario { Id = "reaper",           Base = 8,   Bonus = 20,   Nota = "Reaper: base 8 (a menor base) + Omnism II" },
            new Cenario { Id = "seraph",           Base = 10,  Bonus = 150,  Nota = "Seraph: base 10 + os dois Horn" },
            new Cenario { Id = "energia",          Base = 50,  Bonus = 100,  Nota = "Energy: base 50 (a maior) + Worship" },
            new Cenario { Id = "fury-negativo",    Base = -25, Bonus = 120,  Nota = "BORDAS: Fury tem base NEGATIVA (-25) + Worship + Omnism II" },
            new Cenario { Id = "fluxo-zero",       Base = 0,   Bonus = 120,  Nota = "BORDAS: base zero -> total zero, com bonus alto" },
            new Cenario { Id = "arredonda-para-1", Base = 20,  Bonus = -95,  Nota = "BORDAS: bonus negativo -> 20*0.05 = 1 (nao 0)" },
            new Cenario { Id = "fracao-negativa",  Base = 20,  Bonus = -102, Nota = "BORDAS: 20*(-0.02) = -0.4 -> 0 (nao -1)" },
            new Cenario { Id = "borda-meio-7-5",   Base = 5,   Bonus = 50,   Nota = "BORDAS: 5*1.5 = 7.5 -> ToEven -> 8" },
            new Cenario { Id = "borda-meio-12-5",  Base = 5,   Bonus = 150,  Nota = "BORDAS: 5*2.5 = 12.5 -> ToEven -> 12 (o 'normal' seria 13)" },
            new Cenario { Id = "borda-meio-37-5",  Base = 25,  Bonus = 50,   Nota = "BORDAS: 25*1.5 = 37.5 -> ToEven -> 38" },
            new Cenario { Id = "borda-meio-62-5",  Base = 25,  Bonus = 150,  Nota = "BORDAS: 25*2.5 = 62.5 -> ToEven -> 62 (o 'normal' seria 63)" },
            new Cenario { Id = "borda-meio-87-5",  Base = 25,  Bonus = 250,  Nota = "BORDAS: 25*3.5 = 87.5 -> ToEven -> 88" },
            new Cenario { Id = "flame-sem-bonus",  Base = 5,   Bonus = 0,    Nota = "Flame: base 5 sem bonus -> 5" },
            new Cenario { Id = "dwarven-totem",    Base = 20,  Bonus = 200,  Nota = "Dwarven (Totem). ATENCAO: em jogo o Dwarven NAO escala (excecao conhecida, verificada 30/09) - aqui e so a formula que o asset declara" },
        };

        private static List<int> SomasDeSubconjunto(int[] fontes)
        {
            var vistas = new SortedSet<int>();
            int n = fontes.Length;
            for (int mascara = 0; mascara < (1 << n); mascara++)
            {
                int soma = 0;
                for (int i = 0; i < n; i++)
                {
                    if ((mascara & (1 << i)) != 0) soma += fontes[i];
                }
                vistas.Add(soma);
            }
            return new List<int>(vistas);
        }

        private static int Main(string[] args)
        {
            string destino = args.Length > 0 ? args[0] : ".";
            destino = Path.GetFullPath(destino);
            Directory.CreateDirectory(destino);

            var resultados = new List<Resultado>();
            foreach (Cenario c in Cenarios)
            {
                resultados.Add(new Resultado { Id = c.Id, Valor = Escala(c.Base, c.Bonus) });
            }

            // AUDITORIA: a implementacao "natural" em Python usa double. Aqui eu
            // varro TODO par (base do censo x bonus alcancavel) e conto onde float
            // e double discordam. Zero aqui = o teste em Python pode usar a conta
            // normal; maior que zero = o teste precisa emular float32.
            List<int> bonusAlcancaveis = SomasDeSubconjunto(FontesBonus);
            var divergencias = new List<string>();
            foreach (int b in Bases)
            {
                foreach (int bonus in bonusAlcancaveis)
                {
                    if (Escala(b, bonus) != EscalaDouble(b, bonus))
                    {
                        divergencias.Add("base=" + b + " bonus=" + bonus + " float=" + Escala(b, bonus) + " double=" + EscalaDouble(b, bonus));
                    }
                }
            }

            var auditoria = new Dictionary<string, object>
            {
                ["o_que"] = "para todo par (base do censo x bonus alcancavel), float (motor) e double (implementacao natural em Python) dao o mesmo inteiro",
                ["bases"] = Bases,
                ["fontes_de_bonus"] = FontesBonus,
                ["bonus_alcancaveis"] = bonusAlcancaveis,
                ["pares_conferidos"] = Bases.Length * bonusAlcancaveis.Count,
                ["divergencias"] = divergencias,
                ["veredito"] = divergencias.Count == 0
                    ? "0 divergencias: a conta em double basta para este dominio"
                    : divergencias.Count + " divergencias: implementar o teste com emulacao de float32",
            };

            var entrada = new Dictionary<string, object>
            {
                ["caso"] = "soma-aura",
                ["procedencia"] = "oraculo_soma_aura (C#, float + Math.Round ToEven): o mesmo caminho de conta do motor",
                ["formula"] = "Mathf.Round(BASE * (1 + bonus/100)), fator e produto em float",
                ["fonte_vocabulario"] = "docs/PLANO-DE-TESTES.md (EXCESSO DE SHRINE / BORDAS)",
                ["auditoria_float_vs_double"] = auditoria,
                ["cenarios"] = Cenarios,
            };

            var esperado = new Dictionary<string, object>
            {
                ["caso"] = "soma-aura",
                ["procedencia"] = "oraculo_soma_aura (C#, float + Math.Round ToEven) - GERADO, nunca somado a mao",
                ["gerado_por"] = "tools/testes/fixtures/geradores/oraculo_soma_aura",
                ["resultados"] = resultados,
            };

            var opcoes = new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
            };

            string pEntrada = Path.Combine(destino, "soma-aura.entrada.json");
            string pEsperado = Path.Combine(destino, "soma-aura.esperado.json");
            File.WriteAllText(pEntrada, JsonSerializer.Serialize(entrada, opcoes) + "\n", new UTF8Encoding(false));
            File.WriteAllText(pEsperado, JsonSerializer.Serialize(esperado, opcoes) + "\n", new UTF8Encoding(false));

            Console.WriteLine("escrito: " + pEntrada);
            Console.WriteLine("escrito: " + pEsperado);
            Console.WriteLine();
            Console.WriteLine("  cenario                 float  double  divergem");
            Console.WriteLine("  ----------------------- ----- ------- --------");
            foreach (Cenario c in Cenarios)
            {
                int vf = Escala(c.Base, c.Bonus);
                int vd = EscalaDouble(c.Base, c.Bonus);
                Console.WriteLine("  " + c.Id.PadRight(23) + " " + vf.ToString().PadLeft(5) + " " + vd.ToString().PadLeft(7) + " " + (vf != vd ? "  SIM" : "  nao"));
            }
            Console.WriteLine();
            Console.WriteLine("AUDITORIA do dominio alcancavel: " + auditoria["pares_conferidos"] + " pares (base x bonus)");
            Console.WriteLine("  " + auditoria["veredito"]);
            return 0;
        }
    }
}
