// oraculo_excesso_shrine: gera as fixtures da familia TST-2 (EXCESSO DE SHRINE).
//
// POR QUE ISTO EXISTE (e por que e C# e nao Python)
// ------------------------------------------------
// A fixture versionada e a PROCEDENCIA dos valores esperados: se o valor esperado
// sair da MESMA implementacao que o teste usa, o teste passa por construcao (regra
// do tools/testes/README.md). Entao o esperado sai daqui: um programa em C# que
// passa pelo caminho de conta do MOTOR -
//
//     Mathf.Round(f)  = (float)Math.Round(f)                  -> half to EVEN
//     Mathf.CeilToInt = (int)Math.Ceiling(f)                  -> a convencao da FICHA
//     aritmetica FLOAT (single), nao double
//
// - e cujas BASES e PERCENTUAIS sao LIDAS dos arquivos versionados
// tools/dados/shrines-esperado.csv e tools/dados/shrines-percentuais.csv, que por sua
// vez sao GERADOS de docs/cobertura/status.csv (censao do dump do jogo) e do
// resources.assets pelo tools/gera_shrines_esperado.py. Nenhuma base, percentual ou
// valor de bonus e digitado neste arquivo.
//
// FALHA EM VEZ DE CHUTAR: se uma aura, atributo ou percentual esperado nao estiver na
// fonte, este programa sai 1 dizendo o que faltou. Tabela errada vira aprovacao de um
// mod errado.
//
// O QUE ELE GERA (tools/testes/fixtures, versionados - NUNCA editar a mao):
//   * excesso-shrine.entrada.json  - as CENAS exigidas pela tarefa TST-2 (bonus 0/8/20/50/100
//     + as combinacoes, duas auras no mesmo atributo, stacks, vida maxima 3/100, alvos do
//     Flame, bordas de formatacao) e a declaracao das fontes.
//   * excesso-shrine.esperado.json - a saida do ORACULO para cada cena: a cadeia do
//     ShrineEffectBonus, a contribuicao de cada aura por bonus, o dano do Flame/Decay por
//     tipo de inimigo, o inteiro de exibicao e a LINHA AGREGADA ("Your active shrine auras")
//     item por item.
//
// AS REGRAS DA LINHA AGREGADA sao a transcricao do mod vivo, cada uma com a citacao
// arquivo:linha em `BetterTooltips/Patches/ShrineAuraPatch.cs` (a fonte e o repositorio):
//   1053 · AcumuladoShrines() (um item por ATRIBUTO, na ordem canonica; sem aura viva, sem linha)
//   1245 · AurasVivas()       (familia = ShrineKeys pela descricao do status)
//   1296 · AurasUnicas()      (RV-46: a MESMA aura repetida na lista viva conta UMA vez - este
//                            e o defeito do print do dono: `Dodge +120%` com a aura valendo 40)
//   1829 · AtributosDasAuras() (um item por atributo, ordem canonica 1032 · OrdemDosAtributos)
//   1915 · ContribuicaoDasAuras() (soma aura por aura do AttributeEffects REAL, x TotalStacks)
//   1592 · ItensSemAtributo() (Dwarven/Decay/Flame: item proprio ou o aviso no LOG, nunca sumir)
//   1668 · ItemDaAuraSemAtributo() (Decay `Mathf.Round`, Flame `Mathf.Max(1, Round(...))`)
//   1774 · RotuloSemAtributo() (Stun chance / Shadow damage per turn / Fire damage to attackers)
//   DWA-2  AurasQueContamPorInstancia (o TIPO do efeito decide a repeticao: aura de ATRIBUTO conta
//                            UMA vez - o motor soma as instancias e o teto corta, RV-46 - e aura de
//                            GATILHO conta UMA vez POR INSTANCIA - o motor avalia o gatilho uma vez
//                            por status vivo: `Character.SkillTriggers` l.33489-33508 +
//                            `ProcessSkillTriggers` l.40953-40959, rolando a chance em l.41211-41216)
//   945 · Format()            (rotulo por atributo; DamageReduction e ManaCostMod teem sinal invertido)
//   972 · ComSinal()          ("+" para >=0, "−" U+2212 para negativo)
//   998 · InteiroDoJogo()     (Mathf.CeilToInt - a grandeza da ficha; NaN/Inf -> 0)
//   1015 · TotalComSinal()     (o total do parenteses, na MESMA grandeza do rotulo)
//
// USO:
//   dotnet run --project tools/testes/fixtures/geradores/oraculo_excesso_shrine -- tools/testes/fixtures

using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace OraculoExcessoShrine
{
    // ------------------------------------------------------------------ modelos

    internal sealed class AuraInfo
    {
        [JsonPropertyName("aura")] public string Aura { get; set; }
        [JsonPropertyName("atributo")] public string Atributo { get; set; }
        [JsonPropertyName("tipo")] public string Tipo { get; set; }
        [JsonPropertyName("base")] public float Base { get; set; }
        [JsonPropertyName("fonte_base")] public string FonteBase { get; set; }
    }

    internal sealed class CenaViva
    {
        [JsonPropertyName("aura")] public string Aura { get; set; }
        [JsonPropertyName("instancias")] public int Instancias { get; set; }
        [JsonPropertyName("stacks")] public int Stacks { get; set; }
        [JsonPropertyName("expressao")] public bool Expressao { get; set; }
    }

    internal sealed class CenaAlvo
    {
        [JsonPropertyName("nome")] public string Nome { get; set; }
        [JsonPropertyName("maxhealth")] public float MaxHealth { get; set; }
        [JsonPropertyName("tipo")] public string Tipo { get; set; }
        [JsonPropertyName("bonus_id")] public string BonusId { get; set; }
    }

    internal sealed class Cena
    {
        [JsonPropertyName("id")] public string Id { get; set; }
        [JsonPropertyName("bonus_id")] public string BonusId { get; set; }
        [JsonPropertyName("maxhealth")] public float MaxHealth { get; set; }
        [JsonPropertyName("tipo_receptor")] public string TipoReceptor { get; set; }
        [JsonPropertyName("vivas")] public List<CenaViva> Vivas { get; set; }
        [JsonPropertyName("alvos")] public List<CenaAlvo> Alvos { get; set; }
        [JsonPropertyName("totais")] public Dictionary<string, float> Totais { get; set; }
        [JsonPropertyName("nota")] public string Nota { get; set; }
    }

    internal sealed class CasoBonus
    {
        [JsonPropertyName("id")] public string Id { get; set; }
        [JsonPropertyName("fontes")] public List<string> Fontes { get; set; }
        [JsonPropertyName("nota")] public string Nota { get; set; }
    }

    internal sealed class CasoFormato
    {
        [JsonPropertyName("id")] public string Id { get; set; }
        [JsonPropertyName("atributo")] public string Atributo { get; set; }
        [JsonPropertyName("valor")] public float Valor { get; set; }
        [JsonPropertyName("nota")] public string Nota { get; set; }
    }

    internal static class Programa
    {
        private static readonly JsonSerializerOptions Opcoes = new JsonSerializerOptions
        {
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
        };

        // ------------------------------------------------- caminho de conta do motor

        /// <summary>Mathf.Round: (float)Math.Round(f), que e half to EVEN (bancario).</summary>
        private static int RoundHalfEven(float v)
        {
            return (int)Math.Round((double)v, MidpointRounding.ToEven);
        }

        /// <summary>Mathf.CeilToInt, a convencao da FICHA (ShrineAuraPatch.cs 998 · InteiroDoJogo()). 0 em NaN/Inf.</summary>
        private static int CeilDisplay(float v)
        {
            return (float.IsNaN(v) || float.IsInfinity(v)) ? 0 : (int)Math.Ceiling((double)v);
        }

        /// <summary>Mathf.Round(BASE * (1 + bonus/100)) - fator e produto em FLOAT (RV-19 §2.2).</summary>
        private static int Escala(float baseVal, int bonus)
        {
            float fator = 1f + (float)bonus / 100f;
            float produto = baseVal * fator;
            return RoundHalfEven(produto);
        }

        // ------------------------------------------------- as fontes do ShrineEffectBonus
        // RV-19 §3: Omnism I (+8, Chaos tier 1), Omnism II (+20, tier 2, que SUBSTITUI a I),
        // Horn of Devotion ({50,100}, Fortune Legendary) e o perk Worship (+100). Os valores
        // 20 e 100 aparecem tambem como `caso_bonus` na tabela do tools/dados, e o oracle
        // CONFERE essa coincidencia mais abaixo (`conferencia_csv`).
        private static readonly Dictionary<string, int> Fontes = new Dictionary<string, int>
        {
            { "Omnism I", 8 },
            { "Omnism II", 20 },
            { "Horn of Devotion (+50)", 50 },
            { "Horn of Devotion (+100)", 100 },
            { "Worship", 100 },
        };

        /// <summary>RV-19 §3: Omnism I e substituida por Omnism II (SkillsThatReplace do motor).</summary>
        private static readonly Dictionary<string, string> Substitui = new Dictionary<string, string>
        {
            { "Omnism I", "Omnism II" },
        };

        private static readonly string[] OrdemDosAtributos =
        {
            "DamageMod", "DamageReduction", "CritChance", "DodgeChance",
            "LifeOnHit", "HealthPerTurnPercent", "ManaPerTurnPercent", "ManaCostMod"
        };

        private static readonly string[] TiposDeInimigo =
        { "boss", "champion", "elite", "soldier", "fodder", "player" };

        // Etiqueta da aura cujo efeito NAO e atributo de personagem (ShrineAuraPatch.cs
        // 1774 · RotuloSemAtributo(): a chave e o texto EXATO da descricao do status; aqui o
        // nome da aura do csv e 1:1 com ela).
        private static readonly Dictionary<string, string> RotuloSemAtributo = new Dictionary<string, string>
        {
            { "Dwarven Aura", "Stun chance" },
            { "Decay Shrine Aura", "Shadow damage per turn" },
            { "Flame Shrine Aura", "Fire damage to attackers" },
        };

        // DWA-2 (ShrineAuraPatch.cs `TipoDoEfeito`/`AurasQueContamPorInstancia`): o TIPO DO EFEITO
        // decide se a instancia repetida conta. Nesta familia, as auras SEM atributo de personagem (as
        // tres com rotulo proprio) tem o efeito no GATILHO do status - o dump do jogo mostra
        // `nAttrEf=0 | nTrig=1` nelas - e o motor monta a lista de gatilhos um POR status vivo
        // (`Character.SkillTriggers`, l.33489-33508), percorre TODAS as entradas (`ProcessSkillTriggers`,
        // l.40953-40959) e rola a chance de novo em cada uma (l.41211-41216): a instancia repetida
        // CONTA, e a linha mostra um item por instancia. As auras de ATRIBUTO seguem contando UMA vez (o
        // motor soma as instancias e o teto do atributo corta - a regra do `Dodge +120%`, RV-46).
        private static bool EfeitoDeGatilho(string aura)
        {
            return RotuloSemAtributo.ContainsKey(aura);
        }

        // ------------------------------------------------- rotulos (transcricao do mod)

        /// <summary>ShrineAuraPatch.cs 972 · ComSinal().</summary>
        private static string ComSinal(float v)
        {
            int n = CeilDisplay(v);
            return (n >= 0 ? "+" : "\u2212") + Math.Abs(n);
        }

        /// <summary>ShrineAuraPatch.cs 1015 · TotalComSinal() (DamageReduction: sinal invertido).</summary>
        private static string TotalComSinal(string nome, float v)
        {
            int n = CeilDisplay(v);
            float exibido = string.Equals(nome, "DamageReduction", StringComparison.Ordinal) ? -n : n;
            return ComSinal(exibido) + "%";
        }

        /// <summary>ShrineAuraPatch.cs 945 · Format(). null = atributo fora da lista conhecida.</summary>
        private static string Format(string attr, float v)
        {
            int n = CeilDisplay(v);
            switch (attr)
            {
                case "DamageReduction":
                    return n > 0 ? "Damage taken \u2212" + n + "%" : "Damage taken +" + Math.Abs(n) + "%";
                case "ManaCostMod":
                    return n <= 0 ? "Mana Costs reduced by " + Math.Abs(n) + "%"
                                  : "Mana Costs increased by " + n + "%";
                case "DamageMod": return "Damage " + ComSinal(v) + "%";
                case "CritChance": return "Crit Chance " + ComSinal(v) + "%";
                case "DodgeChance": return "Dodge " + ComSinal(v) + "%";
                case "LifeOnHit": return "Life Steal " + ComSinal(v) + "%";
                case "HealthPerTurnPercent": return "Health per turn " + ComSinal(v) + "%";
                case "ManaPerTurnPercent": return "Mana per turn " + ComSinal(v) + "%";
                default: return null;
            }
        }

        // ------------------------------------------------- leitura das fontes versionadas

        private static List<string[]> LerCsv(string caminho)
        {
            var linhas = new List<string[]>();
            foreach (string l in File.ReadAllLines(caminho, Encoding.UTF8))
            {
                if (l.Trim().Length == 0)
                {
                    continue;
                }
                linhas.Add(l.Split(','));
            }
            if (linhas.Count < 2)
            {
                throw new InvalidOperationException("fonte sem linhas: " + caminho);
            }
            return linhas;
        }

        /// <summary>Chave do par (aura, atributo) na tabela gerada (o Fury tem duas linhas).</summary>
        private static string ChaveBase(string aura, string atributo)
        {
            return (aura ?? "") + "\u0001" + (atributo ?? "");
        }

        private static string SubirAteRaiz(string inicio)
        {
            string atual = Path.GetFullPath(inicio);
            while (true)
            {
                if (File.Exists(Path.Combine(atual, "tools", "dados", "shrines-esperado.csv"))
                    || Directory.Exists(Path.Combine(atual, ".git")))
                {
                    return atual;
                }
                string pai = Path.GetDirectoryName(atual);
                if (string.IsNullOrEmpty(pai) || pai == atual)
                {
                    throw new InvalidOperationException("nao achei a raiz do repositorio a partir de " + inicio);
                }
                atual = pai;
            }
        }

        // ------------------------------------------------- bonus (a cadeia do §3)

        private static List<string> FontesEfetivas(List<string> fontes)
        {
            return fontes.Where(f => !(Substitui.ContainsKey(f) && fontes.Contains(Substitui[f]))).ToList();
        }

        private static int BonusTotal(List<string> fontes)
        {
            int total = 0;
            foreach (string f in FontesEfetivas(fontes))
            {
                if (!Fontes.ContainsKey(f))
                {
                    throw new InvalidOperationException("fonte de bonus desconhecida: " + f);
                }
                total += Fontes[f];
            }
            return total;
        }

        // ------------------------------------------------- dano do Flame / Decay

        private static int Dano(float maxHealth, float pct, int bonus, bool minimo1)
        {
            float fator = 1f + (float)bonus / 100f;
            float bruto = (maxHealth * pct) * fator;
            int dano = RoundHalfEven(bruto);
            return minimo1 ? Math.Max(1, dano) : dano;
        }

        // ------------------------------------------------- a linha agregada (RV-31/44/46)

        private static Dictionary<string, object> Agregar(Cena cena,
            Dictionary<string, AuraInfo> porAura,
            Dictionary<string, List<string>> atributosPor,
            Dictionary<string, float> basePor,
            Dictionary<string, Dictionary<string, float>> pct,
            Dictionary<string, bool> minimo1,
            Dictionary<string, int> bonusPorId)
        {
            int bonus = bonusPorId[cena.BonusId];

            // (c) RV-46/AurasUnicas (1296 · AurasUnicas()): a MESMA aura repetida na lista viva conta UMA vez.
            // Cada `instancias` da cena e UMA entrada da lista viva (cada (re)entrada na area cria um
            // status novo - o cabecalho do mod, 1296 · AurasUnicas()).
            var contagem = new Dictionary<string, int>();
            var unicas = new List<string>();
            var stacks = new Dictionary<string, int>();
            foreach (CenaViva cv in cena.Vivas)
            {
                for (int i = 0; i < Math.Max(1, cv.Instancias); i++)
                {
                    int n;
                    if (contagem.TryGetValue(cv.Aura, out n))
                    {
                        contagem[cv.Aura] = n + 1;
                        continue;
                    }
                    contagem[cv.Aura] = 1;
                    unicas.Add(cv.Aura);
                    stacks[cv.Aura] = Math.Max(1, cv.Stacks);
                }
            }
            var repeticoes = new List<string>();
            foreach (string a in unicas)
            {
                if (contagem[a] > 1)
                {
                    repeticoes.Add(a + " x" + contagem[a]);
                }
            }

            // (d) AtributosDasAuras (1829 · AtributosDasAuras()): um item por atributo, ordem canonica.
            var achados = new List<string>();
            foreach (string a in unicas)
            {
                foreach (string atributo in atributosPor[a])
                {
                    if (!achados.Contains(atributo))
                    {
                        achados.Add(atributo);
                    }
                }
            }
            var atributos = new List<string>();
            foreach (string canonico in OrdemDosAtributos)
            {
                if (achados.Contains(canonico))
                {
                    atributos.Add(canonico);
                }
            }
            foreach (string a in achados)
            {
                if (!atributos.Contains(a))
                {
                    atributos.Add(a);
                }
            }

            var itens = new List<string>();
            var avisos = new List<string>();
            var somadas = new List<string>();

            // (e) ContribuicaoDasAuras (1915 · ContribuicaoDasAuras()): soma aura por aura do AttributeEffects REAL
            // (x TotalStacks, 1966 · ContribuicaoDasAuras()). NUNCA o total do personagem.
            foreach (string attr in atributos)
            {
                float contrib = 0f;
                bool somou = false;
                foreach (string a in unicas)
                {
                    float baseAura;
                    if (!basePor.TryGetValue(ChaveBase(a, attr), out baseAura))
                    {
                        continue;
                    }
                    contrib += Escala(baseAura, bonus) * stacks[a];
                    somou = true;
                    somadas.Add(a);
                }
                if (somou)
                {
                    float total;
                    if (!cena.Totais.TryGetValue(attr, out total))
                    {
                        throw new InvalidOperationException(
                            "cena '" + cena.Id + "': o atributo '" + attr + "' tem contribuicao mas a cena nao declarou o total");
                    }
                    itens.Add(Format(attr, contrib) + " (total " + TotalComSinal(attr, total) + ")");
                }
            }

            // (f) ItensSemAtributo (1592 · ItensSemAtributo()): nenhuma aura viva sai em silencio. DWA-2: a aura de
            // GATILHO (Dwarven/Decay/Flame) entra UMA vez POR INSTANCIA - o motor avalia o gatilho uma
            // vez por status vivo - e a de ATRIBUTO/desconhecida continua entrando UMA vez (RV-46).
            // O TEXTO de cada item e o do asset (nada somado a mao) e o AVISO, quando existe, sai UMA
            // vez por aura.
            foreach (string a in unicas)
            {
                if (somadas.Contains(a))
                {
                    continue;
                }
                int vezes = EfeitoDeGatilho(a) ? contagem[a] : 1;
                AuraInfo info = porAura[a];
                string rotulo;
                if (!RotuloSemAtributo.TryGetValue(a, out rotulo))
                {
                    avisos.Add("RV-46 AVISO: a aura viva '" + a + "' NAO virou item da linha"
                        + " (efeito sem atributo de personagem e sem etiqueta conhecida)");
                    continue;
                }
                string item = null;
                if (string.Equals(a, "Dwarven Aura", StringComparison.Ordinal))
                {
                    if (!cena.Vivas.Any(v => v.Aura == a && v.Expressao))
                    {
                        avisos.Add("RV-46 AVISO: a aura viva '" + a + "' NAO virou item da linha (sem expressao de chance avaliada)");
                        continue;
                    }
                    item = rotulo + " " + ComSinal(Escala(info.Base, bonus)) + "%";
                }
                else if (string.Equals(a, "Decay Shrine Aura", StringComparison.Ordinal))
                {
                    if (cena.MaxHealth <= 0f)
                    {
                        avisos.Add("RV-46 AVISO: a aura viva '" + a + "' NAO virou item da linha (receptor sem MaxHealth)");
                        continue;
                    }
                    int dano = Dano(cena.MaxHealth, pct[a][cena.TipoReceptor], bonus, minimo1[a]);
                    item = rotulo + " " + dano.ToString("0.#", CultureInfo.InvariantCulture);
                }
                else if (string.Equals(a, "Flame Shrine Aura", StringComparison.Ordinal))
                {
                    var valores = new List<string>();
                    foreach (CenaAlvo alvo in cena.Alvos)
                    {
                        if (alvo.MaxHealth <= 0f)
                        {
                            continue;
                        }
                        int bAlvo = bonusPorId[alvo.BonusId];
                        int dano = Dano(alvo.MaxHealth, pct[a][alvo.Tipo], bAlvo, minimo1[a]);
                        valores.Add(alvo.Nome + " " + dano.ToString("0.#", CultureInfo.InvariantCulture));
                    }
                    if (valores.Count == 0)
                    {
                        avisos.Add("RV-46 AVISO: a aura viva '" + a + "' NAO virou item da linha"
                            + " (nenhum alvo com o status do Flame vivo agora)");
                        continue;
                    }
                    item = rotulo + ": " + string.Join(", ", valores);
                }
                if (item == null)
                {
                    continue;
                }
                for (int i = 0; i < vezes; i++)
                {
                    itens.Add(item);
                }
            }

            string linha = "";
            if (itens.Count == 0)
            {
                avisos.Add("RV-46 sem linha: " + unicas.Count + " aura(s) viva(s) sem nenhum numero provado (nada estimado)");
            }
            else
            {
                linha = "Your active shrine auras: " + string.Join("; ", itens) + ".";
            }

            return new Dictionary<string, object>
            {
                ["id"] = cena.Id,
                ["bonus"] = bonus,
                ["itens"] = itens,
                ["linha"] = linha,
                ["repeticoes"] = repeticoes,
                ["avisos"] = avisos,
            };
        }

        // ------------------------------------------------------------------ main

        private static int Main(string[] args)
        {
            string destino = Path.GetFullPath(args.Length > 0 ? args[0] : ".");
            Directory.CreateDirectory(destino);
            string raiz;
            try
            {
                raiz = SubirAteRaiz(destino);
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine("FALHA(2): " + ex.Message);
                return 2;
            }

            string csvEsperado = Path.Combine(raiz, "tools", "dados", "shrines-esperado.csv");
            string csvPct = Path.Combine(raiz, "tools", "dados", "shrines-percentuais.csv");
            foreach (string caminho in new[] { csvEsperado, csvPct })
            {
                if (!File.Exists(caminho))
                {
                    Console.Error.WriteLine("FALHA(1): fonte ausente: " + caminho
                        + "\n  -> rode `python tools/gera_shrines_esperado.py`; sem a fonte o oracle FALHA em vez de chutar.");
                    return 1;
                }
            }

            // ---------------- bases e atributos (uma linha por aura x atributo, do caso bonus 0)
            // O `Fury` tem DUAS linhas (DamageMod +25 e DamageReduction -25): a aura nao e a chave,
            // o par (aura, atributo) e.
            var aurasLista = new List<AuraInfo>();
            var porAura = new Dictionary<string, AuraInfo>();
            var atributosPor = new Dictionary<string, List<string>>();
            var basePor = new Dictionary<string, float>();
            var contribuicoesCsv = new List<string[]>();
            var casosDoCsv = new HashSet<int>();
            var linhasEsperado = LerCsv(csvEsperado);
            var cabEsperado = linhasEsperado[0];
            int iAura = Array.IndexOf(cabEsperado, "aura");
            int iAtributo = Array.IndexOf(cabEsperado, "atributo");
            int iTipo = Array.IndexOf(cabEsperado, "tipo");
            int iBase = Array.IndexOf(cabEsperado, "base");
            int iFonte = Array.IndexOf(cabEsperado, "fonte_base");
            int iCaso = Array.IndexOf(cabEsperado, "caso_bonus");
            int iContrib = Array.IndexOf(cabEsperado, "contribuicao_esperada");
            foreach (string[] linha in linhasEsperado.Skip(1))
            {
                int caso = int.Parse(linha[iCaso], CultureInfo.InvariantCulture);
                casosDoCsv.Add(caso);
                contribuicoesCsv.Add(linha);
                if (caso != 0)
                {
                    continue;
                }
                var info = new AuraInfo
                {
                    Aura = linha[iAura],
                    Atributo = linha[iAtributo],
                    Tipo = linha[iTipo],
                    Base = float.Parse(linha[iBase], CultureInfo.InvariantCulture),
                    FonteBase = linha[iFonte],
                };
                string chave = ChaveBase(info.Aura, info.Atributo);
                if (basePor.ContainsKey(chave))
                {
                    throw new InvalidOperationException("par (aura, atributo) duplicado no csv: " + chave);
                }
                basePor[chave] = info.Base;
                if (!porAura.ContainsKey(info.Aura))
                {
                    porAura[info.Aura] = info;
                    atributosPor[info.Aura] = new List<string>();
                }
                if (!string.IsNullOrEmpty(info.Atributo))
                {
                    atributosPor[info.Aura].Add(info.Atributo);
                }
                aurasLista.Add(info);
            }

            // ---------------- percentuais do dano (por tipo) + o `minimo1` (so o Flame tem)
            var pct = new Dictionary<string, Dictionary<string, float>>();
            var minimo1 = new Dictionary<string, bool>();
            var linhasPct = LerCsv(csvPct);
            var cabPct = linhasPct[0];
            int jAura = Array.IndexOf(cabPct, "aura");
            int jTipo = Array.IndexOf(cabPct, "tipo");
            int jPct = Array.IndexOf(cabPct, "percentual");
            int jMin = Array.IndexOf(cabPct, "minimo1");
            foreach (string[] linha in linhasPct.Skip(1))
            {
                if (!pct.ContainsKey(linha[jAura]))
                {
                    pct[linha[jAura]] = new Dictionary<string, float>();
                    minimo1[linha[jAura]] = string.Equals(linha[jMin], "sim", StringComparison.Ordinal);
                }
                pct[linha[jAura]][linha[jTipo]] = float.Parse(linha[jPct], CultureInfo.InvariantCulture) / 100f;
            }

            // ---------------- casos de bonus (a unica entrada escrita: as FONTES, nao o total)
            var casosBonus = new List<CasoBonus>
            {
                new CasoBonus { Id = "sem-bonus", Fontes = new List<string>(),
                    Nota = "bonus zero: o valor e a base" },
                new CasoBonus { Id = "omnism1", Fontes = new List<string> { "Omnism I" },
                    Nota = "Omnism I (+8)" },
                new CasoBonus { Id = "omnism2", Fontes = new List<string> { "Omnism II" },
                    Nota = "Omnism II (+20) - ela SUBSTITUI a I (§3)" },
                new CasoBonus { Id = "horn-50", Fontes = new List<string> { "Horn of Devotion (+50)" },
                    Nota = "Horn of Devotion no roll de +50" },
                new CasoBonus { Id = "worship", Fontes = new List<string> { "Worship" },
                    Nota = "perk Worship (+100)" },
                new CasoBonus { Id = "worship-omnism2", Fontes = new List<string> { "Worship", "Omnism II" },
                    Nota = "EXCESSO: Worship (+100) + Omnism II (+20) = 120" },
                new CasoBonus { Id = "worship-omnism1", Fontes = new List<string> { "Worship", "Omnism I" },
                    Nota = "EXCESSO: Worship (+100) + Omnism I (+8) = 108 (a I nao tem quem a substitua aqui)" },
                new CasoBonus { Id = "worship-horn50", Fontes = new List<string> { "Worship", "Horn of Devotion (+50)" },
                    Nota = "EXCESSO: Worship (+100) + Horn (+50) = 150" },
                new CasoBonus { Id = "worship-horn100", Fontes = new List<string> { "Worship", "Horn of Devotion (+100)" },
                    Nota = "EXCESSO: Worship (+100) + Horn (+100) = 200" },
                new CasoBonus { Id = "omnism1-omnism2", Fontes = new List<string> { "Omnism I", "Omnism II" },
                    Nota = "EXCESSO: as DUAS tiers - a I e SUBSTITUIDA pela II: total 20, NAO 28 (RV-19 §3)" },
                new CasoBonus { Id = "tres-omnism", Fontes = new List<string> { "Worship", "Omnism I", "Omnism II" },
                    Nota = "EXCESSO: tres fontes, com as duas tiers dentro = 100 + 20" },
                new CasoBonus { Id = "tres-bencaos", Fontes = new List<string> { "Worship", "Omnism II", "Horn of Devotion (+50)" },
                    Nota = "EXCESSO: tres bencaos acumuladas (Worship + Omnism II + Horn) = 170" },
                new CasoBonus { Id = "tudo", Fontes = new List<string> { "Worship", "Omnism I", "Omnism II", "Horn of Devotion (+50)" },
                    Nota = "EXCESSO: todas as fontes juntas (a I cai pela substituicao) = 170" },
            };
            var bonusPorId = new Dictionary<string, int>();
            var bonusEsperado = new List<Dictionary<string, object>>();
            foreach (CasoBonus c in casosBonus)
            {
                int total = BonusTotal(c.Fontes);
                bonusPorId[c.Id] = total;
                bonusEsperado.Add(new Dictionary<string, object>
                {
                    ["id"] = c.Id,
                    ["fontes"] = c.Fontes,
                    ["substituidas"] = c.Fontes.Where(f => Substitui.ContainsKey(f) && c.Fontes.Contains(Substitui[f])).ToList(),
                    ["total"] = total,
                    ["nota"] = c.Nota,
                });
            }

            // A coincidencia com a tabela gerada (os casos 20 e 100 do csv TEM de existir como
            // tais: o `caso_bonus` da tabela do repositorio e a mesma cadeia do §3).
            var exigidos = new[] { 0, 20, 100 };
            var faltando = exigidos.Where(c => !casosDoCsv.Contains(c)).ToList();
            if (faltando.Count > 0)
            {
                Console.Error.WriteLine("FALHA(1): a tabela gerada nao tem os caso_bonus "
                    + string.Join(", ", faltando) + " - o oracle NAO chuta a cadeia do bonus.");
                return 1;
            }

            // ---------------- conferencia: o oracle x a tabela GERADA (procedencia cruzada)
            var escala = new List<Dictionary<string, object>>();
            var divergencias = new List<string>();
            int conferidas = 0;
            foreach (string[] linha in contribuicoesCsv)
            {
                int caso = int.Parse(linha[iCaso], CultureInfo.InvariantCulture);
                float b = float.Parse(linha[iBase], CultureInfo.InvariantCulture);
                int minha = Escala(b, caso);
                int doCsv = (int)Math.Round(double.Parse(linha[iContrib], CultureInfo.InvariantCulture));
                conferidas++;
                if (minha != doCsv)
                {
                    divergencias.Add(linha[iAura] + "/" + linha[iAtributo] + " base=" + b.ToString("0.##", CultureInfo.InvariantCulture)
                        + " bonus=" + caso + ": oracle=" + minha + " csv=" + doCsv);
                }
            }
            if (divergencias.Count > 0)
            {
                Console.Error.WriteLine("FALHA(1): o oracle DIVERGE da tabela gerada "
                    + "(tools/dados/shrines-esperado.csv) em " + divergencias.Count + " linha(s):");
                foreach (string d in divergencias)
                {
                    Console.Error.WriteLine("  " + d);
                }
                Console.Error.WriteLine("  -> uma das duas contas esta errada; o oracle FALHA em vez de gerar fixture duvidosa.");
                return 1;
            }

            // a matriz da escala: cada aura x atributo x eixo de bonus
            int[] eixoBonus = { 0, 8, 20, 50, 100, 108, 120, 150, 170, 200 };
            foreach (AuraInfo info in aurasLista)
            {
                foreach (int b in eixoBonus)
                {
                    escala.Add(new Dictionary<string, object>
                    {
                        ["aura"] = info.Aura,
                        ["atributo"] = info.Atributo,
                        ["base"] = info.Base,
                        ["bonus"] = b,
                        ["contribuicao"] = Escala(info.Base, b),
                    });
                }
            }

            // ---------------- dano: a matriz (aura de perigo x tipo x vida maxima x bonus)
            var eixoMh = new[] { 3f, 10f, 100f, 233f, 300f };
            var idsDano = new[] { "sem-bonus", "omnism2", "worship", "worship-omnism2" };
            var danos = new List<Dictionary<string, object>>();
            foreach (string aura in new[] { "Flame Shrine Aura", "Decay Shrine Aura" })
            {
                if (!porAura.ContainsKey(aura) || !pct.ContainsKey(aura))
                {
                    Console.Error.WriteLine("FALHA(1): a aura de perigo '" + aura + "' nao esta nas fontes.");
                    return 1;
                }
                foreach (string tipo in TiposDeInimigo)
                {
                    if (!pct[aura].ContainsKey(tipo))
                    {
                        Console.Error.WriteLine("FALHA(1): a aura '" + aura + "' nao tem percentual para o tipo '"
                            + tipo + "' na tabela gerada.");
                        return 1;
                    }
                    foreach (float mh in eixoMh)
                    {
                        foreach (string id in idsDano)
                        {
                            danos.Add(new Dictionary<string, object>
                            {
                                ["aura"] = aura,
                                ["tipo"] = tipo,
                                ["maxhealth"] = mh,
                                ["bonus"] = bonusPorId[id],
                                ["bonus_id"] = id,
                                ["minimo1"] = minimo1[aura],
                                ["dano"] = Dano(mh, pct[aura][tipo], bonusPorId[id], minimo1[aura]),
                            });
                        }
                    }
                }
            }

            // ---------------- bordas de formatacao (a grandeza da FICHA: Ceil)
            var casosFormato = new List<CasoFormato>
            {
                new CasoFormato { Id = "inteiro-nao-ganha-ponto", Atributo = "CritChance", Valor = 40f,
                    Nota = "inteiro: o texto NAO pode ganhar .0" },
                new CasoFormato { Id = "equipamento-fracionario", Atributo = "DodgeChance", Valor = 53.4f,
                    Nota = "valor fracionario do equipamento: a convencao do jogo e Mathf.Ceil (54)" },
                new CasoFormato { Id = "fracao-meio", Atributo = "DamageMod", Valor = 0.5f,
                    Nota = "BORDA .5 exato: Ceil(0.5) = 1" },
                new CasoFormato { Id = "fracao-negativa", Atributo = "DamageMod", Valor = -0.4f,
                    Nota = "BORDA -0.4: Ceil(-0.4) = 0 -> o sinal e lido DEPOIS (\"+0%\")" },
                new CasoFormato { Id = "negativo-inteiro", Atributo = "DamageMod", Valor = -25f,
                    Nota = "negativo inteiro: sinal U+2212" },
                new CasoFormato { Id = "negativo-fracionario", Atributo = "DodgeChance", Valor = -53.4f,
                    Nota = "Ceil(-53.4) = -53 (a ficha mostra -53; inverter antes daria -54)" },
                new CasoFormato { Id = "damage-taken-reduz", Atributo = "DamageReduction", Valor = 20f,
                    Nota = "DamageReduction positivo REDUZ o dano tomado: rotulo invertido" },
                new CasoFormato { Id = "damage-taken-aumenta", Atributo = "DamageReduction", Valor = -30f,
                    Nota = "DamageReduction negativo AUMENTA o dano tomado (o total do print do dono)" },
                new CasoFormato { Id = "energy-reduz", Atributo = "ManaCostMod", Valor = -50f,
                    Nota = "Energy Coil: o EFEITO e -50 (o texto do jogo mostra +50)" },
                new CasoFormato { Id = "energy-aumenta", Atributo = "ManaCostMod", Valor = 20f,
                    Nota = "RV-43: total POSITIVO de ManaCostMod e custo AUMENTADO" },
                new CasoFormato { Id = "energia-total-positivo", Atributo = "ManaCostMod", Valor = -100f,
                    Nota = "a aura empurra -100 mas o resto da ficha e +120 -> total +20 (RV-43)" },
            };
            var formatacao = new List<Dictionary<string, object>>();
            foreach (CasoFormato c in casosFormato)
            {
                string rot = Format(c.Atributo, c.Valor);
                if (rot == null)
                {
                    Console.Error.WriteLine("FALHA(1): o caso de formatacao '" + c.Id + "' usa o atributo '"
                        + c.Atributo + "', que nao esta na lista conhecida do Format.");
                    return 1;
                }
                string tc = TotalComSinal(c.Atributo, c.Valor);
                formatacao.Add(new Dictionary<string, object>
                {
                    ["id"] = c.Id,
                    ["atributo"] = c.Atributo,
                    ["valor"] = c.Valor,
                    ["inteiro"] = CeilDisplay(c.Valor),
                    ["com_sinal"] = ComSinal(c.Valor),
                    ["rotulo"] = rot,
                    ["total_com_sinal"] = tc,
                    ["porcento_no_rotulo"] = rot.Count(ch => ch == '%'),
                    ["porcento_no_total"] = tc.Count(ch => ch == '%'),
                });
            }

            // ---------------- cenas do AGREGADO (a linha "Your active shrine auras")
            var v = new Func<string, int, int, bool, CenaViva>((aura, inst, st, expr) => new CenaViva
            { Aura = aura, Instancias = inst, Stacks = st, Expressao = expr });
            var a = new Func<string, float, string, string, CenaAlvo>((nome, mh, tipo, bonus) => new CenaAlvo
            { Nome = nome, MaxHealth = mh, Tipo = tipo, BonusId = bonus });
            var cenas = new List<Cena>
            {
                new Cena
                {
                    Id = "rogue-x3-stacks-1", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Rogue Aura", 3, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "DodgeChance", 57f } },
                    Nota = "O DEFEITO DO PRINT DO DONO: a MESMA aura 3x na lista viva (cada (re)entrada na area"
                        + " cria um status novo). A contribuicao conta a aura UMA vez (RV-46): Dodge +40%"
                        + " (o numero da linha branca do shrine), NAO +120%.",
                },
                new Cena
                {
                    Id = "fury-so", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Fury", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "DamageMod", 75f }, { "DamageReduction", -30f } },
                    Nota = "ACEITE do dono (RV-19 §9.1, print com Worship): um item por atributo do MESMO status"
                        + " (Fury mexe em DamageMod e DamageReduction); total = resto + contribuicao.",
                },
                new Cena
                {
                    Id = "warrior-mais-fury", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Warrior Aura", 1, 1, true), v("Fury", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "DamageMod", 115f }, { "DamageReduction", -30f } },
                    Nota = "DUAS AURAS NO MESMO ATRIBUTO (Warrior + Fury em DamageMod): as contribuicoes SOMAM"
                        + " (40 + 50 = 90) e o item continua UM (nao se repete). O total 115 e DERIVADO (75 do"
                        + " print com o Fury + 40 do Warrior, com o resto 25 constante de RV-19 §9.1/§9.2) - NAO"
                        + " ha print do dono com as duas auras na mesma area; o que o teste trava aqui e a"
                        + " CONTRIBUICAO e o resto constante.",
                },
                new Cena
                {
                    Id = "tres-fontes-mesmo-atributo", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Warrior Aura", 2, 1, true), v("Fury", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "DamageMod", 115f }, { "DamageReduction", -30f } },
                    Nota = "TRES ENTRADAS VIVAS no mesmo atributo (Warrior x2 + Fury): a deduplicacao (RV-46)"
                        + " deixa Warrior + Fury e o item soma 90 uma vez so; a repeticao vai para o log.",
                },
                new Cena
                {
                    Id = "warrior-stacks-2", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Warrior Aura", 1, 2, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "DamageMod", 155f } },
                    Nota = "STACKS DO MESMO STATUS (TotalStacks = 2): o motor multiplica o valor pelo numero de"
                        + " stacks (Character.cs l.37263; ShrineAuraPatch 1966 · ContribuicaoDasAuras()) - aqui a contribuicao E 40 x 2 = 80,"
                        + " o contrario do caso da aura repetida (que e a mesma aura, nao mais efeito).",
                },
                new Cena
                {
                    Id = "teto-guardian-mais-fury", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Guardian Aura", 1, 1, true), v("Fury", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "DamageMod", 75f }, { "DamageReduction", -50f } },
                    Nota = "O TOTAL NO TETO DO ATRIBUTO (e a contribuicao liquida das DUAS auras): o motor"
                        + " CORTA o total no teto (`HasMax`/`MaxValue`; RV-46/commit bc394e7: DamageReduction"
                        + " MaxValue=50, asset @1519603860). Guardian empurra +40 (dano tomado -40) e Fury"
                        + " empurra -50: a contribuicao LIQUIDA e -10 e o TOTAL fica no teto (-50, que o rotulo"
                        + " le '+50%'). O item tem de trazer a conta das duas auras e o total do motor - nao"
                        + " confundir com o defeito do `Dodge +120%`, que era a MESMA aura contada por ENTRADA"
                        + " da lista viva (e dava um numero impossivel: 120 com o atributo teto 75).",
                },
                new Cena
                {
                    Id = "dwarven-so", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Dwarven Aura", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float>(),
                    Nota = "O DWARVEN SUMIDO: aura viva SEM atributo de personagem e sem NENHUMA outra aura na"
                        + " linha. Antes do RV-46 a linha saia vazia; hoje ela tem de trazer o item proprio"
                        + " (`Stun chance +40%`) - a lista se apresenta como completa.",
                },
                new Cena
                {
                    Id = "dwarven-sem-expressao", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Dwarven Aura", 1, 1, false) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float>(),
                    Nota = "A outra metade da regra: sem expressao avaliada NAO existe numero - a aura sai no LOG"
                        + " com o motivo (`RV-46 AVISO: a aura viva ... NAO virou item`). Nunca sumir calada.",
                },
                new Cena
                {
                    Id = "dwarven-x2", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Dwarven Aura", 2, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float>(),
                    Nota = "DWA-2 (o defeito do dono, 30/09): DOIS Dwarven Shrines no alcance = DUAS "
                        + "`Dwarven Aura` vivas (cada shrine tem o proprio Source). O efeito NAO e "
                        + "atributo de personagem, e GATILHO: o motor monta a lista de gatilhos um por "
                        + "status vivo (`Character.SkillTriggers` l.33489-33508) e percorre todas as "
                        + "entradas (`ProcessSkillTriggers` l.40953-40959), rolando a chance de novo em "
                        + "cada uma (l.41211-41216). Entao a linha tem DOIS itens `Stun chance +40%` - "
                        + "uma rolagem por instancia. NADA de `+80%`: o motor nao soma chance, e numero "
                        + "somado a mao era justamente o defeito do `Dodge +120%` do outro lado.",
                },
                new Cena
                {
                    Id = "decay-x2", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Decay Shrine Aura", 2, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float>(),
                    Nota = "DWA-2 — a MESMA regra numa aura de gatilho que NAO e o Dwarven (prova de que "
                        + "ela e por TIPO, nao por nome): Decay Shrine Aura e `OnTurnStart`, tambem sem "
                        + "atributo de personagem. Com DOIS shrines no alcance o proc de dano roda duas "
                        + "vezes por turno do portador -> dois itens `Shadow damage per turn 20`.",
                },

                new Cena
                {
                    Id = "decay-so", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Decay Shrine Aura", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float>(),
                    Nota = "Decay sozinho (sem atributo): o item proprio vem do asset avaliado pelo motor - com"
                        + " vida maxima 100 e bonus 100 a % do player (10%) DOBRA: 10 -> 20.",
                },
                new Cena
                {
                    Id = "decay-vida-3", BonusId = "sem-bonus", MaxHealth = 3f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Decay Shrine Aura", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float>(),
                    Nota = "BORDA do Decay: vida maxima 3 sem bonus -> 3 x 10% = 0.3 -> Round -> 0. O Decay NAO"
                        + " tem minimo (a nota viva diz \"it can be 0\"): o item tem de sair com 0, nao sumir."
                        + " O MESMO 3 no Flame (matriz dos danos) da 1 pelo Mathf.Max(1, ...) - os dois juntos"
                        + " isolam o minimo de um so.",
                },
                new Cena
                {
                    Id = "flame-varios-alvos", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Flame Shrine Aura", 1, 1, true) },
                    Alvos = new List<CenaAlvo>
                    {
                        a("Kobold", 100f, "player", "worship"),
                        a("Chefe", 300f, "boss", "worship"),
                        a("Tanque", 233f, "elite", "worship"),
                        a("Fodder rasteiro", 3f, "fodder", "sem-bonus"),
                    },
                    Totais = new Dictionary<string, float>(),
                    Nota = "FLAME COM VARIOS ALVOS: um item por alvo, com a vida maxima, a % do tipo e o bonus DELE"
                        + " (o hover nao sabe quem vai atacar - a lista e uma projecao). O alvo com vida 3 e bonus 0"
                        + " isola o MINIMO 1 do Flame (3 x 14% = 0.42 -> Round 0 -> Max(1, ...) = 1).",
                },
                new Cena
                {
                    Id = "flame-sem-alvo", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Flame Shrine Aura", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float>(),
                    Nota = "FLAME SEM ALVO NA AURA: nao existe UM numero (o dano e de quem ataca). A aura nao entra"
                        + " na linha e o LOG diz por que - silencio nunca.",
                },
                new Cena
                {
                    Id = "linha-mista", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva>
                    {
                        v("Warrior Aura", 1, 1, true),
                        v("Rogue Aura", 2, 1, true),
                        v("Dwarven Aura", 1, 1, true),
                        v("Decay Shrine Aura", 1, 1, true),
                        v("Flame Shrine Aura", 1, 1, true),
                    },
                    Alvos = new List<CenaAlvo>
                    {
                        a("Kobold", 100f, "player", "worship"),
                        a("Chefe", 300f, "boss", "worship"),
                    },
                    Totais = new Dictionary<string, float> { { "DamageMod", 115f }, { "DodgeChance", 57f } },
                    Nota = "A LINHA COMPLETA (bonus 100): dois itens de atributo (DamageMod e DodgeChance, na ordem"
                        + " canonica) + os tres itens sem atributo (Dwarven/Decay/Flame), com a Rogue repetida"
                        + " contada UMA vez. Nenhuma aura viva pode ficar de fora.",
                },
                new Cena
                {
                    Id = "energia-total-negativo", BonusId = "sem-bonus", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Energy Aura", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "ManaCostMod", -50f } },
                    Nota = "BORDA: a aura do Energy empurra o custo para BAIXO (-50) - o item tem de ler"
                        + " 'Mana Costs reduced by 50%' com o total NEGATIVO no parenteses.",
                },
                new Cena
                {
                    Id = "energia-total-positivo", BonusId = "worship", MaxHealth = 100f, TipoReceptor = "player",
                    Vivas = new List<CenaViva> { v("Energy Aura", 1, 1, true) },
                    Alvos = new List<CenaAlvo>(),
                    Totais = new Dictionary<string, float> { { "ManaCostMod", 20f } },
                    Nota = "RV-43: a aura empurra -100 e o resto da ficha e +120 -> total +20. A aura reduz o custo,"
                        + " o TOTAL e positivo (custo aumentado) - o item diz os dois sem se contradizer.",
                },
            };

            var agregado = new List<Dictionary<string, object>>();
            foreach (Cena cena in cenas)
            {
                foreach (CenaViva cv in cena.Vivas)
                {
                    if (!porAura.ContainsKey(cv.Aura))
                    {
                        Console.Error.WriteLine("FALHA(1): a cena '" + cena.Id + "' usa a aura '" + cv.Aura
                            + "', que NAO esta na tabela gerada. O oracle nao chuta aura.");
                        return 1;
                    }
                }
                agregado.Add(Agregar(cena, porAura, atributosPor, basePor, pct, minimo1, bonusPorId));
            }

            // ---------------- escrita

            var entrada = new Dictionary<string, object>
            {
                ["caso"] = "excesso-shrine",
                ["procedencia"] = "oraculo_excesso_shrine (C#): aritmetica FLOAT + Math.Round ToEven + "
                    + "Mathf.CeilToInt, o caminho de conta do motor; bases/percentuais LIDOS de "
                    + "tools/dados/shrines-esperado.csv e shrines-percentuais.csv (GERADOS de "
                    + "docs/cobertura/status.csv e do resources.assets por tools/gera_shrines_esperado.py)",
                ["fontes"] = new Dictionary<string, object>
                {
                    ["bases"] = "tools/dados/shrines-esperado.csv (gerado por tools/gera_shrines_esperado.py; "
                        + "cada linha cita docs/cobertura/status.csv:<linha> ou resources.assets@<offset>)",
                    ["percentuais"] = "tools/dados/shrines-percentuais.csv (as acoes Flame/Decay Aura Proc)",
                    ["regra_da_escala"] = "docs/cobertura/revisao/RV-19-shrines.md §2.2: "
                        + "Mathf.Round(BASE * (1 + bonus/100)), half-to-even",
                    ["fontes_do_bonus"] = "RV-19 §3: Omnism I +8, Omnism II +20 (que SUBSTITUI a I), "
                        + "Horn of Devotion {50,100}, Worship +100",
                    ["dano"] = "RV-19 §4.2/§4.3: Flame Max(1, Round(vida * %do tipo * fator)), "
                        + "Decay Round(vida * %do tipo * fator) sem minimo",
                    ["linha_agregada"] = "BetterTooltips/Patches/ShrineAuraPatch.cs (a fonte viva das regras; "
                        + "os itens sao a transcricao citada no cabecalho do oraculo)",
                },
                ["bonus"] = casosBonus,
                ["eixo_bonus"] = eixoBonus,
                ["danos_eixo"] = new Dictionary<string, object>
                {
                    ["tipos"] = TiposDeInimigo,
                    ["maxhealth"] = eixoMh,
                    ["bonus_ids"] = idsDano,
                },
                ["formatacao"] = casosFormato,
                ["agregado"] = cenas,
            };

            var esperado = new Dictionary<string, object>
            {
                ["caso"] = "excesso-shrine",
                ["procedencia"] = "oraculo_excesso_shrine (C#) - GERADO, nunca somado a mao",
                ["gerado_por"] = "tools/testes/fixtures/geradores/oraculo_excesso_shrine",
                ["bonus_total"] = bonusEsperado,
                ["conferencia_csv"] = new Dictionary<string, object>
                {
                    ["o_que"] = "cada linha do tools/dados/shrines-esperado.csv (0/8/20/50/100) recalculada por "
                        + "este oracle",
                    ["linhas_conferidas"] = conferidas,
                    ["divergencias"] = divergencias,
                    ["veredito"] = divergencias.Count == 0
                        ? "0 divergencias: o oracle bate com a tabela gerada do repositorio"
                        : divergencias.Count + " divergencias",
                },
                ["escala"] = escala,
                ["danos"] = danos,
                ["formatacao"] = formatacao,
                ["agregado"] = agregado,
            };

            string pEntrada = Path.Combine(destino, "excesso-shrine.entrada.json");
            string pEsperado = Path.Combine(destino, "excesso-shrine.esperado.json");
            File.WriteAllText(pEntrada, JsonSerializer.Serialize(entrada, Opcoes) + "\n", new UTF8Encoding(false));
            File.WriteAllText(pEsperado, JsonSerializer.Serialize(esperado, Opcoes) + "\n", new UTF8Encoding(false));

            Console.WriteLine("escrito: " + pEntrada);
            Console.WriteLine("escrito: " + pEsperado);
            Console.WriteLine();
            Console.WriteLine("  conferencia com a tabela gerada: " + conferidas + " linhas, "
                + divergencias.Count + " divergencia(s)");
            Console.WriteLine("  escala: " + escala.Count + " valores (" + porAura.Count + " auras x "
                + eixoBonus.Length + " bonus)");
            Console.WriteLine("  danos:  " + danos.Count + " valores");
            Console.WriteLine("  formatacao: " + formatacao.Count + " bordas");
            Console.WriteLine();
            Console.WriteLine("  bonus                    fontes                                    total");
            Console.WriteLine("  ------------------------ ----------------------------------------- -----");
            foreach (Dictionary<string, object> b in bonusEsperado)
            {
                Console.WriteLine("  " + ((string)b["id"]).PadRight(24) + " "
                    + string.Join(" + ", ((List<string>)b["fontes"])).PadRight(41) + " "
                    + ((int)b["total"]).ToString().PadLeft(5));
            }
            Console.WriteLine();
            Console.WriteLine("  cena do agregado             itens  avisos  linha");
            Console.WriteLine("  ---------------------------- ------ -------- -----");
            foreach (Dictionary<string, object> ag in agregado)
            {
                Console.WriteLine("  " + ((string)ag["id"]).PadRight(28) + " "
                    + ((List<string>)ag["itens"]).Count.ToString().PadLeft(6) + " "
                    + ((List<string>)ag["avisos"]).Count.ToString().PadLeft(8) + " "
                    + (((string)ag["linha"]).Length == 0 ? "(vazia: o log diz o motivo)" : ((string)ag["linha"])));
            }
            return 0;
        }
    }
}
