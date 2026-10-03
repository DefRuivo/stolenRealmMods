using System;
using System.Collections.Generic;
using System.Globalization;
using Burst2Flame;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// BT-20 (02/10) — o VALOR ABSOLUTO que as skills de CONVERSAO DE ATRIBUTO em Armor / Magic Armor
    /// concedem, ao lado da REGRA que o jogo ja mostra.
    ///
    /// PEDIDO DO DONO (verbatim): "Body and Soul = Vitality*5 de Armor e Intelligence*5 de Magic Armor
    /// ... mostrar no tooltip o VALOR ABSOLUTO ... calculado com os stats ATUAIS do personagem (lido em
    /// runtime do motor, nunca digitado a mao)". E o alerta do censo: "nao assumir que e a unica".
    ///
    /// A FAMILIA (levantada do ASSET carregado, nao de lista digitada; o criterio esta explicito em
    /// `EhConvercao`): skills com pelo menos um `CharacterEffectInfo` que
    ///   - aplica o metodo `Base` (conversao PLANA, o `:Base` do `attr` do dump) e NAO e segundo passe;
    ///   - mira um atributo de MITIGACAO — `Armor` ou `MagicArmor`;
    ///   - tem `Amount` NAO-CONSTANTE que le um STAT do proprio personagem (`Source["..."]`).
    /// Censo sobre `docs/cobertura/skills-detalhe.csv` (coluna `attr`, 453 skills): DUAS skills, QUATRO
    /// efeitos —
    ///   - `Body and Soul`        -> `Armor:Base:Source["Vitality"] * 5` + `MagicArmor:Base:Source["Intelligence"] * 5`
    ///   - `Invulnerable Winter`  -> `Armor:Base:Source["Intelligence"] * (1 + (.14f * Source.Level))` + o mesmo em MagicArmor
    /// (o mesmo formato do dump: `Limpa()` troca `"` por `'`, ver `RoguelikeDebugger/EfeitosInfo.cs:283`.)
    /// Nada aqui e digitado: o indice sai de `Game.Instance.Skills` x o `AttributeEffects` de cada uma.
    ///
    /// O MOTOR NAO E REIMPLEMENTADO — o numero sai do PROPRIO interpretador do jogo. As duas `Amount`
    /// acima estao PRECOMPILADAS no cache do build (`CompiledDynamicExpresso`, decompilado
    /// l.61915 `Source[\"Vitality\"] * 5`, l.61956 `Source[\"Intelligence\"] * 5` e l.58922
    /// `Source[\"Intelligence\"] * (1 + (.14f * Source.Level))`) e sao avaliadas por
    /// `Game.TryEval<float>(Amount, GameFunctionParameters { Source = personagem })` — a MESMA conta
    /// que o motor faz ao aplicar o efeito (`Character.GetAttributeWalk`, decompilado l.37874: tenta
    /// `TryGetConstantAmount`, senao `Game.TryEval`). O avaliador reusado e o do RV-20/RV-34, ja
    /// estabelecido para ler formula do asset com o personagem em foco:
    /// `ShrineAuraPatch.ValorDaExpressao` (ShrineAuraPatch.cs:2168). Nao ha aritmetica nova nem
    /// literal de balanceamento no mod.
    ///
    /// A PROVA DO PROPRIO JOGO (fonte de primeira): o teste de integracao `BodyAndSoul`
    /// (`MonkSkillTest`, decompilado l.253550-253571) guarda `caster["Armor"]` e `caster["MagicArmor"]`
    /// ANTES, aprende `MNK_3_P2_Body and Soul` e assere que o ganho e
    /// `caster["Vitality"] * 5f` / `caster["Intelligence"] * 5f` — exatamente o que a `Amount` do
    /// asset avalia. O valor mostrado e o que o motor aplica.
    ///
    /// DE ONDE SAI CADA OPERANDO (numero nenhum e digitado):
    ///   1) O PERSONAGEM — o receptor da tooltip, pelo caminho ja estabelecido da familia
    ///      (`ShrineAuraPatch.ReceptorDaTooltip`, ShrineAuraPatch.cs:595 — o MESMO usado por BT-10/11/12/13).
    ///   2) OS STATS — `Source["Vitality"]` / `Source["Intelligence"]` sao lidos DENTRO da avaliacao, do
    ///      indexador FINAL do motor (`Character.this[string]` -> valor com gear/powerups/skills), como
    ///      manda o pedido ("stats ATUAIS").
    ///   3) O FATOR — esta no PROPRIO `Amount` do asset (`* 5`, `* (1 + .14 * Level)`); nao ha constante
    ///      nossa. Se o asset mudar, o numero muda junto, sozinho.
    ///
    /// ONDE O TEXTO ENTRA (docs/TEXTO-TOOLTIPS.md §1/§9), IGUAL as BT-10..BT-13:
    ///   - o VALOR vai na LINHA BRANCA (nivel 1), ao lado da frase do jogo, na cor que o MOTOR ja usa
    ///     para valor dinamico — o literal `#CBB396` de `ApplyDescriptionExpressions` (`[N]`) e
    ///     `GetDamageString` (`*N`); nenhum hex novo e criado;
    ///   - a EXPLICACAO do calculo vai no nivel 2 (a nota do mod, marcador `#C8B090` resolvido em
    ///     runtime por `LocalizePatch.ComACorDoJogo`).
    ///
    /// GUARDA: sem personagem em foco, sem o asset da skill, sem efeito da familia que avalie, NAO sai
    /// numero NENHUM (a linha do jogo fica INTACTA) — melhor nao mostrar do que mostrar errado.
    ///
    /// GUARDA DA REVISAO BT-20R (03/10): se a skill JA tem `DescriptionExpressions` e a descricao
    /// carrega um token `[N]`, o PROPRIO MOTOR escreve o valor absoluto na frase — a nota do mod vira
    /// repeticao (`... Current Bonus: 123 (+123 Armor, +123 Magic Armor)`) e e PULADA; o caso e a
    /// `Invulnerable Winter`. A `Body and Soul`, sem expressao, continua recebendo a nota — e o caso
    /// do pedido. Mesmo principio do `LocalizePatch` (~l.1086): valor que ja aparece nao se repete.
    /// </summary>
    internal static class ConvercaoAtributoPatch
    {
        /// <summary>Cor que o PROPRIO MOTOR escreve nos valores dinamicos: `&lt;color=#CBB396&gt;` em
        /// `ApplyDescriptionExpressions` (decompilado l.2327, o `[N]`) e em `GetDamageString` (l.2276, o
        /// `*N`). Nao e hex novo nem escolha estetica — e o literal do motor, o mesmo que
        /// `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR` ja usa como `#CBB396`.</summary>
        private const string CorDoValorDoMotor = "CBB396";

        /// <summary>
        /// Monta o texto do NIVEL 1 (com o valor por atributo) e a NOTA do nivel 2 para uma skill de
        /// conversao de atributo em Armor/Magic Armor. Devolve false quando o texto NAO e de uma skill
        /// da familia ou quando falta qualquer dado provado — e quem chamou deixa o texto como estava.
        /// </summary>
        public static bool TentaMontar(string original, string linhaDoJogo,
            out string linhaComValor, out string nota)
        {
            linhaComValor = null;
            nota = null;
            try
            {
                // Pre-filtro BARATO: toda descricao desta familia cita Armor/Magic Armor — o funil roda
                // em todo texto do jogo e as outras strings saem por aqui sem alocar nada.
                if (string.IsNullOrEmpty(original)
                    || original.IndexOf("armor", StringComparison.OrdinalIgnoreCase) < 0)
                {
                    return false;
                }

                SkillInfo skill = SkillDoTexto(original);
                if (skill == null)
                {
                    return false;
                }

                // GUARDA DA REVISAO BT-20R — nao repetir o que o MOTOR ja mostra. Quando a skill
                // tem `DescriptionExpressions` E a descricao carrega um token `[N]`, o proprio
                // `ApplyDescriptionExpressions` (decompilado l.334802) insere o numero na frase do
                // jogo: anexar o valor de novo seria RUIDO, nao informacao — o MESMO principio ja
                // documentado no `LocalizePatch` (l.~1086). A `Invulnerable Winter` cai aqui (a
                // coluna `expr` do censo traz `1 + (.14f *Source.Level); Source['Intelligence'] *
                // (1 + (.14f * Source.Level))` e a descricao fecha em `Current Bonus: [1]`), e a
                // duplicacao `Current Bonus: <...>123</color> (+123 Armor, +123 Magic Armor)`
                // desaparece. A `Body and Soul` da familia NAO entra: o `expr` dela e VAZIO, entao
                // nao ha o que o motor renderize e a NOTA pedida pelo dono continua saindo.
                if (JaRenderizadoPeloMotor(skill))
                {
                    Marca("'" + skill.SkillName + "' ja rende o valor por DescriptionExpressions"
                        + " — linha do jogo intacta (sem repeticao)");
                    return false;
                }

                Character personagem = ShrineAuraPatch.ReceptorDaTooltip();
                if (personagem == null)
                {
                    Marca("sem numero: nenhum personagem em foco");
                    return false;
                }

                List<string> partes = MontaPartes(skill, personagem);
                if (partes.Count == 0)
                {
                    Marca("sem numero: '" + skill.SkillName + "' nao rendeu valor em Armor/Magic Armor");
                    return false;
                }

                string valores = string.Join(", ", partes.ToArray());
                linhaComValor = linhaDoJogo.TrimEnd()
                    + " (<color=#" + CorDoValorDoMotor + ">" + valores + "</color>)";
                nota = NotaDoCalculo();

                Marca("'" + personagem.CharacterName + "' '" + skill.SkillName + "' -> " + valores);
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[Convercao BT-20] valor dinamico falhou (linha intacta): "
                    + ex.GetType().Name + ": " + ex.Message);
                linhaComValor = null;
                nota = null;
                return false;
            }
        }

        /// <summary>Um pedaco por efeito da familia: `+50 Armor`. O sinal e a casa decimal seguem o
        /// padrao da familia BT-10..BT-13 (`0.#`), sem afirmar inteiro. O numero sai do
        /// interpretador do MOTOR (`ShrineAuraPatch.ValorDaExpressao` -> `Game.TryEval`), com a
        /// `Amount` lida do ASSET e `Source` = personagem em foco.</summary>
        private static List<string> MontaPartes(SkillInfo skill, Character personagem)
        {
            List<string> partes = new List<string>();
            if (skill.AttributeEffects == null)
            {
                return partes;
            }

            foreach (CharacterEffectInfo efeito in skill.AttributeEffects)
            {
                if (!EhConvercao(efeito))
                {
                    continue;
                }

                // A MESMA avaliacao do motor ao aplicar o efeito (Character.GetAttributeWalk,
                // decompilado l.37874): a `Amount` do asset com o personagem em foco. Nao ha conta
                // nossa — se a expressao nao estiver no cache compilado do build, TryEval devolve
                // false e NAO mostramos numero nenhum para esse atributo.
                float valor;
                if (!ShrineAuraPatch.ValorDaExpressao(efeito.Amount, personagem, personagem, out valor))
                {
                    Marca("atributo '" + efeito.CharacterAttribute.name + "': a Amount '" + efeito.Amount
                        + "' nao avaliou neste build — fora da conta");
                    continue;
                }

                partes.Add((valor >= 0f ? "+" : "")
                    + valor.ToString("0.#", CultureInfo.InvariantCulture)
                    + " " + RotuloDoAtributo(efeito.CharacterAttribute));

                Marca("atributo '" + efeito.CharacterAttribute.name + "': expressao '" + efeito.Amount
                    + "' -> " + valor.ToString("0.#", CultureInfo.InvariantCulture));
            }
            return partes;
        }

        /// <summary>O criterio da familia, num lugar so (usado tanto pela montagem quanto pelo indice):
        /// metodo `Base` (conversao PLANA), nao-segundo-passe, atributo de MITIGACAO (`Armor` ou
        /// `MagicArmor`) e `Amount` que LE UM STAT do personagem (`Source["..."]`).</summary>
        private static bool EhConvercao(CharacterEffectInfo efeito)
        {
            if (efeito == null || efeito.CharacterEffectMethod != CharacterEffectMethod.Base
                || efeito.CalculateOnSecondPass)
            {
                return false;
            }
            if (!EhArmaduraOuMagicArmor(efeito.CharacterAttribute))
            {
                return false;
            }
            // `Source[` e o marcao do pedido: e a CONVERSAO de um atributo do personagem (Source) em
            // Armor/Magic Armor. Amount constante nao depende do personagem e nao precisa de valor.
            return !string.IsNullOrEmpty(efeito.Amount)
                && efeito.Amount.IndexOf("Source[", StringComparison.Ordinal) >= 0;
        }

        /// <summary>Os atributos de mitigacao que o pedido nomeia. A identidade e o `name` do ASSET
        /// (`Armor` / `MagicArmor`), o mesmo que o debugger publica no `attr` do dump
        /// (`RoguelikeDebugger/Patches/SkillInventoryPatch.cs:464`).</summary>
        private static bool EhArmaduraOuMagicArmor(CharacterAttribute atributo)
        {
            if (atributo == null)
            {
                return false;
            }
            return string.Equals(atributo.name, "Armor", StringComparison.Ordinal)
                || string.Equals(atributo.name, "MagicArmor", StringComparison.Ordinal);
        }

        /// <summary>O rotulo do atributo como o TOOLTIP DO JOGO o renderiza: o `GetTooltipDisplayName()`
        /// do PROPRIO asset (decompilado l.441776), com o fallback do motor
        /// `GUIManager.SpaceOutString(name)` -> "Magic Armor" (l.441762) quando o campo esta vazio. Nao
        /// digitamos "Armor"/"Magic Armor": o texto sai do atributo carregado.</summary>
        private static string RotuloDoAtributo(CharacterAttribute atributo)
        {
            if (atributo == null)
            {
                return string.Empty;
            }
            string rotulo = atributo.GetTooltipDisplayName();
            return string.IsNullOrEmpty(rotulo) ? atributo.name : rotulo;
        }

        /// <summary>A nota do NIVEL 2 (a explicacao do calculo). Uma linha, sem numero digitado e sem
        /// `[N]` (o pipeline de expressoes rodaria depois do `Localize` e interpretaria o token —
        /// regra do projeto, ver docs/cobertura/revisao/RV-19-shrines.md).</summary>
        internal static string NotaDoCalculo()
        {
            return "Counted on your current attributes, so the amount follows your gear, powerups and skills.";
        }

        /// <summary>O MOTOR ja renderiza o valor desta skill? Sim quando ha expressao de descricao
        /// (`SkillInfo.DescriptionExpressions`, `string[]`) E a descricao carrega um token `[N]` que
        /// `ApplyDescriptionExpressions` preenche (decompilado l.334802). Nesse caso o valor absoluto
        /// JA esta na linha do jogo e anexar de novo seria repeticao. Sem expressao (o caso da
        /// `Body and Soul`, coluna `expr` vazia no censo) a linha nao traz numero nenhum — e a nota
        /// do mod continua sendo informacao.</summary>
        private static bool JaRenderizadoPeloMotor(SkillInfo skill)
        {
            string[] expressoes = skill.DescriptionExpressions;
            if (expressoes == null || expressoes.Length == 0)
            {
                return false;
            }
            return TemTokenNumerico(skill.Description);
        }

        /// <summary>Ha um `[N]` (colchete seguido de digito) na descricao — a forma que o pipeline de
        /// `ApplyDescriptionExpressions` interpreta. Le so o PRIMEIRO caractere apos o `[`, como o
        /// motor; por isso `[10]` conta como token (e, no motor, tambem seria lido so o `1`).</summary>
        private static bool TemTokenNumerico(string descricao)
        {
            if (string.IsNullOrEmpty(descricao))
            {
                return false;
            }
            for (int i = 0; i + 1 < descricao.Length; i++)
            {
                if (descricao[i] == '[' && descricao[i + 1] >= '0' && descricao[i + 1] <= '9')
                {
                    return true;
                }
            }
            return false;
        }

        // ---------------------------------------------------------------- o indice da FAMILIA

        private static Dictionary<string, SkillInfo> _porDescricao;
        private static bool _indicePronto;

        /// <summary>Resolve a skill da familia pela descricao localizada. Indice O(1): o gancho roda a
        /// cada texto do jogo e varrer as ~450 skills por chamada seria desperdicio.</summary>
        private static SkillInfo SkillDoTexto(string original)
        {
            GaranteIndice();
            Dictionary<string, SkillInfo> indice = _porDescricao;
            if (indice == null)
            {
                return null;
            }
            SkillInfo skill;
            return indice.TryGetValue(Normaliza(original), out skill) ? skill : null;
        }

        /// <summary>Monta, UMA vez, o indice das skills da familia: as que tem pelo menos um efeito
        /// aceito por `EhConvercao`. Descricao repetida entre duas skills da familia vira chave AMBIGUA
        /// (valor nulo) e nao produz numero — fail-safe, em vez de escolher uma das duas no chute. Falha
        /// NAO memoriza o indice: tenta de novo no proximo texto.</summary>
        private static void GaranteIndice()
        {
            if (_indicePronto)
            {
                return;
            }
            try
            {
                if (Game.Instance == null)
                {
                    return;
                }
                List<SkillInfo> skills = Game.Instance.Skills;
                if (skills == null)
                {
                    return;
                }

                Dictionary<string, SkillInfo> indice = new Dictionary<string, SkillInfo>(StringComparer.Ordinal);
                int ambiguas = 0;
                foreach (SkillInfo skill in skills)
                {
                    if (skill == null || string.IsNullOrEmpty(skill.Description) || !TemConvercao(skill))
                    {
                        continue;
                    }
                    string chave = Normaliza(skill.Description);
                    if (chave.Length == 0)
                    {
                        continue;
                    }
                    SkillInfo ja;
                    if (indice.TryGetValue(chave, out ja))
                    {
                        if (ja != null)
                        {
                            indice[chave] = null;
                            ambiguas++;
                        }
                        continue;
                    }
                    indice[chave] = skill;
                }

                _porDescricao = indice;
                _indicePronto = true;
                Plugin.Log.LogInfo("BetterTooltips: BT-20 — familia de skills de conversao de atributo em"
                    + " Armor/Magic Armor: " + ListaDaFamilia(indice) + " (" + Conta(indice) + " skill(s); "
                    + ambiguas + " descricao(oes) ambigua(s))");
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("BetterTooltips: BT-20 nao montou o indice da familia — "
                    + ex.GetType().Name + ": " + ex.Message);
            }
        }

        private static bool TemConvercao(SkillInfo skill)
        {
            if (skill.AttributeEffects == null)
            {
                return false;
            }
            foreach (CharacterEffectInfo efeito in skill.AttributeEffects)
            {
                if (EhConvercao(efeito))
                {
                    return true;
                }
            }
            return false;
        }

        /// <summary>Lista explicita da familia (o log a imprime no boot — e a prova viva de QUEM entrou,
        /// com o nome do asset e nao com uma lista nossa).</summary>
        private static string ListaDaFamilia(Dictionary<string, SkillInfo> indice)
        {
            List<string> nomes = new List<string>();
            foreach (KeyValuePair<string, SkillInfo> par in indice)
            {
                if (par.Value != null)
                {
                    nomes.Add(par.Value.SkillName);
                }
            }
            nomes.Sort(StringComparer.Ordinal);
            return nomes.Count == 0 ? "(nenhuma)" : string.Join("; ", nomes.ToArray());
        }

        private static int Conta(Dictionary<string, SkillInfo> indice)
        {
            int n = 0;
            foreach (KeyValuePair<string, SkillInfo> par in indice)
            {
                if (par.Value != null)
                {
                    n++;
                }
            }
            return n;
        }

        /// <summary>Apara as pontas e reduz espaco duplo — o funil (`LocalizePatch`) normaliza espacos no
        /// texto exibido, e a identidade nao pode depender de um detalhe invisivel. Devolve a PROPRIA
        /// string quando nao ha nada a mudar (o caso comum, sem alocacao).</summary>
        private static string Normaliza(string texto)
        {
            if (string.IsNullOrEmpty(texto))
            {
                return texto;
            }
            string s = texto.Trim();
            if (s.IndexOf("  ", StringComparison.Ordinal) < 0)
            {
                return s;
            }
            while (s.Contains("  "))
            {
                s = s.Replace("  ", " ");
            }
            return s;
        }

        /// <summary>Loga cada combinacao UMA vez (o postfix roda a cada frame de hover).</summary>
        private static readonly HashSet<string> _marcas = new HashSet<string>();

        private static void Marca(string linha)
        {
            try
            {
                if (_marcas.Count >= 200 || !_marcas.Add(linha))
                {
                    return;
                }
                Plugin.Log.LogInfo("[Convercao BT-20] " + linha);
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }
    }
}
