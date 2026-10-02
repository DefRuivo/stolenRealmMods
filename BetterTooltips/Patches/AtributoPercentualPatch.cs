using System;
using System.Collections.Generic;
using System.Globalization;
using Burst2Flame;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// BT-13 (01/10) — o VALOR ABSOLUTO que as skills de ATRIBUTO EM PORCENTAGEM concedem, ao lado
    /// do percentual que o jogo ja mostra.
    ///
    /// PEDIDO DO DONO (verbatim): "Light's Brilliance e todos as skills de aumento de Attributos em %:
    /// Mostrar quanto essa skill esta dando de valor para os atributos que ela afeta, no caso Lights
    /// brilliance aumenta 20%, se usarmos como exemplo personagem com 100 de intelligence, o bonus que
    /// deveria ser indicado pela skill e de 20 de intelligence".
    ///
    /// A FAMILIA (levantada ANTES de codar; o criterio esta explicito):
    ///   skills cujo PROPRIO `AttributeEffects` aplica o metodo `Percentage` a um dos CINCO ATRIBUTOS
    ///   PRIMARIOS (Might / Dexterity / Intelligence / Vitality / Reflex). Sao SETE, com NOVE efeitos:
    ///     - Light's Brilliance  -> IntelligenceBase +20%
    ///     - Light's Celerity    -> DexterityBase    +20%
    ///     - Light's Endurance   -> VitalityBase     +20%
    ///     - Light's Intuition   -> ReflexBase       +20%
    ///     - Light's Strength    -> MightBase        +20%
    ///     - Strength (Monk T4)  -> MightBase +15%, VitalityBase +15%
    ///     - Speed    (Monk T4)  -> DexterityBase +15%, ReflexBase +15%
    ///   Fonte: `docs/cobertura/skills.csv` (coluna `attr`, linhas 230-234, 375, 391) e o dump do
    ///   debugger `scratch/cap1/fnt1/A-dono-pular-true-diag-on/LogOutput-desta-rotina.log:409`
    ///   (`[Skill] 'Light's Brilliance' | ... | attr=IntelligenceBase:Percentage:20, | nAttrEf=1 |
    ///   attrTipos=0:CharacterEffectInfo{Amount=20;CalculateOnSecondPass=False;
    ///   CharacterAttribute=IntelligenceBase;CharacterEffectMethod=Percentage;EffectTarget=Source;...}`).
    ///   A lista NAO esta digitada aqui: o indice e montado do asset carregado (ver `GaranteIndice`),
    ///   entao ele acompanha o jogo sozinho se a familia mudar.
    ///
    /// O QUE O MOTOR REALMENTE APLICA — o ACHADO desta tarefa (e NAO e a leitura ingenua):
    ///   `Character.CalculateAttribute` (scratch/sac1/Character.cs:11791-11798; no decompilado de
    ///   arquivo unico da familia, l.41383-41390) compoe o atributo em TRES passos, nesta ordem:
    ///     valor = (SavedMap[guid] + SOMA Base)                      // `num += SavedMap` (GetAttribute, l.11863) + Base (l.11794)
    ///     valor = valor * (1 + SOMA Percentage / 100)               // l.11795-11796
    ///     valor = valor * PRODUTO Multiplicative                    // l.11797-11798
    ///   Ou seja: a porcentagem **NAO soma ao valor final** nem incide sobre o numero que o jogador ve —
    ///   ela MULTIPLICA o subtotal (o "base + flat" que existia ANTES das porcentagens). O jogo afirma
    ///   isso no proprio teste de integracao:
    ///   `SkillTreeTestBase.AssertPercentIncrease` (scratch/sac1/SkillTreeTestBase.cs:4396) calcula
    ///   `esperado = antes * (1 + percentual/100)` e
    ///   `LightSkillTest` (scratch/sac1/LightSkillTest.cs:2923-2936) le `caster["IntelligenceBase"]`
    ///   ANTES de aprender a skill, aprende, le DE NOVO e exige `depois ~ antes * 1,20`.
    ///
    ///   E dai a divergencia, que e o ponto: `character["IntelligenceBase"]` (e a ficha, que mostra
    ///   `LevelableCharacterAttributesFinal[i]` — InventoryManager.UpdateStats, scratch/sac1/
    ///   InventoryManager.cs:1060-1062) DEVOLVE O VALOR JA COM A PORCENTAGEM APLICADA (o proprio
    ///   BetterStats registra isso: `character[nome]` "ja vem com TODOS os modificadores (inclusive o
    ///   +20% da skill Light's Brilliance)", scratch/backup_probe/BetterStats_Plugin.cs:241-242).
    ///   Com base 100 o painel mostra 120 — portanto "20% de 120 = 24" seria ERRADO; o que o motor
    ///   acrescenta e 20.
    ///
    /// A CONTA EXATA (e por que ela vale nos DOIS estados da skill — aprendida ou so espiada):
    ///   final = subtotal * (1 + SOMA Percentual/100) * ProdutoMultiplicativo
    ///   => subtotal * ProdutoMultiplicativo = final / (1 + SOMA Percentual/100)
    ///   => o pedaco DESTA skill = subtotal * ProdutoMultiplicativo * pct/100
    ///                           = final * pct / (100 + SOMA Percentual)
    ///   A soma das porcentagens vem do MOTOR (`Character.GetAttributeValueByMethod(attr, Percentage,
    ///   false)`, scratch/sac1/Character.cs:8307 — e o MESMO valor que `CalculateAttribute` usa na
    ///   l.11795) e o fator multiplicativo cancela na algebra, entao ele nao precisa ser lido. Se a
    ///   skill esta APRENDIDA, o `pct` dela ja esta dentro da SOMA e a conta da o valor marginal; se
    ///   ainda NAO esta (arvore de skills), a SOMA a exclui e a conta da exatamente o quanto ela VAI
    ///   dar. Os dois casos dao o MESMO numero — que e o que o dono pediu.
    ///
    /// DE ONDE SAI CADA OPERANDO (numero nenhum e digitado):
    ///   1) O VALOR ATUAL DO ATRIBUTO — `personagem[atributo.name]`, o indexador do MOTOR
    ///      (scratch/sac1/Character.cs:3960) -> `GetAttribute` (l.11820) = SavedMap + CalculateAttribute,
    ///      isto e, o valor FINAL. NAO usamos `character.SavedMap[...]` como se fosse o final (o dono
    ///      alerta no cartao: SavedMap e o PURO, so os pontos investidos — serve de base, nunca de
    ///      modificador) e NAO usamos o "character['X'] puro".
    ///   2) A PORCENTAGEM DA SKILL — `CharacterEffectInfo.TryGetConstantAmount` (scratch/sac1/
    ///      CharacterEffect.cs:228) lida do ASSET carregado (`SkillInfo.AttributeEffects`,
    ///      `Game.Instance.Skills`): a string `Amount` do efeito (hoje "20"/"15"). Se o asset virar
    ///      "25", o numero acompanha sozinho. Efeito cuja `Amount` e EXPRESSAO (ex.: outra skill da
    ///      mesma tabela, `2 * Target.NumEnemiesWithin(5)`) devolve false e aquele atributo NAO e
    ///      adivinhado — sai da conta.
    ///   3) A SOMA DAS PORCENTAGENS — `Character.GetAttributeValueByMethod(attr, Percentage, false)`,
    ///      publico no MOTOR (scratch/sac1/Character.cs:8307).
    ///   O `100f` do denominador NAO e constante de balanceamento: e a escala do proprio motor
    ///   (`1f + .../100f`, sac1 l.11795) — o mesmo literal que converte "20%" em fator.
    ///
    /// ONDE O TEXTO ENTRA (docs/TEXTO-TOOLTIPS.md §1/§9):
    ///   - o VALOR vai na LINHA BRANCA (nivel 1), logo depois da frase do jogo, na cor que o MOTOR ja
    ///     usa para valor dinamico — o literal `#CBB396` de `ApplyDescriptionExpressions` (l.2327, o
    ///     `[N]`) e `GetDamageString` (l.2276, o `*N`); nenhum hex novo e criado;
    ///   - a EXPLICACAO do calculo vai no nivel 2 (a nota do mod, marcador `#C8B090` resolvido em
    ///     runtime por `LocalizePatch.ComACorDoJogo`).
    ///   O rotulo do atributo ("Intelligence") NAO e vocabulario nosso: e o TOKEN `@intelligence@` da
    ///   PROPRIA descricao do asset, passado pelo `Tooltip.ToTitleCase` (l.333651) — exatamente o que
    ///   o tooltip do jogo faz na l.644 ao renderizar esse token.
    ///
    /// GUARDA: sem personagem em foco, sem o asset da skill, sem a % constante no efeito, com o
    /// atributo atual <= 0 ou com a soma das % anulando o denominador, NAO sai numero NENHUM (a linha
    /// do jogo fica INTACTA) — melhor nao mostrar do que mostrar errado.
    /// </summary>
    internal static class AtributoPercentualPatch
    {
        /// <summary>Cor que o PROPRIO MOTOR escreve nos valores dinamicos: `&lt;color=#CBB396&gt;` em
        /// `ApplyDescriptionExpressions` (decompilado l.2327, o `[N]`) e em `GetDamageString` (l.2276,
        /// o `*N`). Nao e hex novo nem escolha estetica — e o literal do motor, o mesmo que
        /// `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR` ja usa como `#CBB396`.</summary>
        private const string CorDoValorDoMotor = "CBB396";

        /// <summary>
        /// Monta o texto do NIVEL 1 (com o valor por atributo) e a NOTA do nivel 2 para uma skill de
        /// atributo em %. Devolve false quando o texto NAO e de uma skill da familia ou quando falta
        /// qualquer dado provado — e quem chamou deixa o texto como estava.
        /// </summary>
        public static bool TentaMontar(string original, string linhaDoJogo,
            out string linhaComValor, out string nota)
        {
            linhaComValor = null;
            nota = null;
            try
            {
                // Pre-filtro BARATO: toda descricao desta familia cita uma porcentagem — o funil roda
                // em todo texto do jogo e as outras strings saem por aqui sem alocar nada.
                if (string.IsNullOrEmpty(original) || original.IndexOf('%') < 0)
                {
                    return false;
                }

                SkillInfo skill = SkillDoTexto(original);
                if (skill == null)
                {
                    return false;
                }

                Character personagem = ShrineAuraPatch.ReceptorDaTooltip();
                if (personagem == null)
                {
                    Marca("sem numero: nenhum personagem em foco");
                    return false;
                }

                List<string> partes = MontaPartes(skill, personagem, original);
                if (partes.Count == 0)
                {
                    Marca("sem numero: '" + skill.SkillName + "' nao rendeu valor em nenhum atributo");
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
                Plugin.Log.LogWarning("[Atributo % BT-13] valor dinamico falhou (linha intacta): "
                    + ex.GetType().Name + ": " + ex.Message);
                linhaComValor = null;
                nota = null;
                return false;
            }
        }

        /// <summary>Um pedaco por efeito de atributo primario em %: `+20 Intelligence`. O sinal e a
        /// casa decimal seguem o padrao da familia BT-10/11/12 (`0.#`), sem afirmar inteiro.</summary>
        private static List<string> MontaPartes(SkillInfo skill, Character personagem, string descricao)
        {
            List<string> partes = new List<string>();
            CharacterAttribute[] primarios = AtributosPrimarios();
            if (primarios == null || skill.AttributeEffects == null)
            {
                return partes;
            }

            foreach (CharacterEffectInfo efeito in skill.AttributeEffects)
            {
                if (efeito == null || efeito.CharacterEffectMethod != CharacterEffectMethod.Percentage
                    || efeito.CalculateOnSecondPass)
                {
                    continue;
                }

                CharacterAttribute atributo = efeito.CharacterAttribute;
                if (!EhAtributoPrimario(atributo, primarios))
                {
                    continue;
                }

                // A % sai do ASSET (o mesmo `Amount` que o motor le para montar a contribuicao). Se
                // for expressao (nao constante), nao arriscamos meia leitura.
                float pct;
                if (!efeito.TryGetConstantAmount(out pct))
                {
                    Marca("atributo '" + atributo.name + "': a % do asset nao e constante ('"
                        + efeito.Amount + "') — fora da conta");
                    continue;
                }

                float atual = personagem[atributo.name];
                if (atual <= 0f)
                {
                    Marca("atributo '" + atributo.name + "': valor atual "
                        + atual.ToString("0.#", CultureInfo.InvariantCulture) + " — sem o que reportar");
                    continue;
                }

                float somaPct = personagem.GetAttributeValueByMethod(
                    atributo, CharacterEffectMethod.Percentage, false);
                float denominador = 100f + somaPct;
                if (denominador < 1f)
                {
                    Marca("atributo '" + atributo.name + "': soma das % ("
                        + somaPct.ToString("0.#", CultureInfo.InvariantCulture) + ") anula o denominador");
                    continue;
                }

                // A MESMA conta do motor: valor_final * pct / (100 + soma das %). Ver o cabecalho.
                float valor = atual * pct / denominador;
                partes.Add((valor >= 0f ? "+" : "")
                    + valor.ToString("0.#", CultureInfo.InvariantCulture)
                    + " " + RotuloDoAtributo(descricao, atributo));

                Marca("atributo '" + atributo.name + "': final="
                    + atual.ToString("0.#", CultureInfo.InvariantCulture)
                    + " soma%=" + somaPct.ToString("0.#", CultureInfo.InvariantCulture)
                    + " pct=" + pct.ToString("0.#", CultureInfo.InvariantCulture)
                    + " -> " + valor.ToString("0.#", CultureInfo.InvariantCulture));
            }
            return partes;
        }

        /// <summary>Os cinco atributos PRIMARIOS, como o MOTOR os declara
        /// (`Game.Instance.LevelableCharacterAttributes` — a MESMA array que a ficha usa;
        /// InventoryManager.UpdateStats, scratch/sac1/InventoryManager.cs:1057-1060). Nenhum nome
        /// esta digitado aqui: se o jogo renomear ou acrescentar um atributo, a familia acompanha.</summary>
        private static CharacterAttribute[] AtributosPrimarios()
        {
            try
            {
                return Game.Instance != null ? Game.Instance.LevelableCharacterAttributes : null;
            }
            catch
            {
                return null;
            }
        }

        private static bool EhAtributoPrimario(CharacterAttribute atributo, CharacterAttribute[] primarios)
        {
            if (atributo == null || primarios == null)
            {
                return false;
            }
            for (int i = 0; i < primarios.Length; i++)
            {
                CharacterAttribute primario = primarios[i];
                if (primario == null)
                {
                    continue;
                }
                if (ReferenceEquals(primario, atributo) || primario.Guid == atributo.Guid)
                {
                    return true;
                }
            }
            return false;
        }

        /// <summary>O rotulo do atributo como o TOOLTIP DO JOGO o renderiza: o token `@intelligence@`
        /// da propria descricao, passado pelo `Tooltip.ToTitleCase` (decompilado l.333651) — que e
        /// exatamente o que a montagem do tooltip faz na l.644. Sem token que case, cai na identidade
        /// do asset (`IntelligenceBase`), que e o nome que o motor carrega.</summary>
        private static string RotuloDoAtributo(string descricao, CharacterAttribute atributo)
        {
            int i = 0;
            while (true)
            {
                int abre = descricao.IndexOf('@', i);
                if (abre < 0)
                {
                    break;
                }
                int fecha = descricao.IndexOf('@', abre + 1);
                if (fecha < 0)
                {
                    break;
                }
                string token = descricao.Substring(abre + 1, fecha - abre - 1);
                if (token.Length > 0 && atributo.name.StartsWith(token, StringComparison.OrdinalIgnoreCase))
                {
                    return Tooltip.ToTitleCase(token);
                }
                i = fecha + 1;
            }
            return atributo.name;
        }

        /// <summary>A nota do NIVEL 2 (a explicacao do calculo). Uma linha, sem numero digitado e sem
        /// `[N]` (o pipeline de expressoes rodaria depois do `Localize` e interpretaria o token —
        /// regra do projeto, ver docs/cobertura/revisao/RV-19-shrines.md).</summary>
        internal static string NotaDoCalculo()
        {
            return "Counted on the attribute value you have before this bonus, so the amount "
                + "grows with your gear, powerups and skills.";
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
            // `Normaliza` devolve a PROPRIA string quando nao ha o que aparar (sem alocacao no caso
            // comum); a descricao que o jogo entrega ao funil e `skill.Description` cru
            // (Tooltip.ShowSkillTooltip: `OptionsManager.Localize(skill.Description)`).
            return indice.TryGetValue(Normaliza(original), out skill) ? skill : null;
        }

        /// <summary>Monta, UMA vez, o indice das skills da familia: as que tem pelo menos um
        /// `CharacterEffectInfo` com metodo `Percentage` sobre um dos cinco atributos primarios.
        /// Descricao repetida entre duas skills da familia vira chave AMBIGUA (valor nulo) e nao
        /// produz numero — fail-safe, em vez de escolher uma das duas no chute. Falha NAO memoriza o
        /// indice: tenta de novo no proximo texto.</summary>
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
                CharacterAttribute[] primarios = Game.Instance.LevelableCharacterAttributes;
                List<SkillInfo> skills = Game.Instance.Skills;
                if (primarios == null || skills == null)
                {
                    return;
                }

                Dictionary<string, SkillInfo> indice = new Dictionary<string, SkillInfo>(StringComparer.Ordinal);
                int ambiguas = 0;
                foreach (SkillInfo skill in skills)
                {
                    if (skill == null || string.IsNullOrEmpty(skill.Description))
                    {
                        continue;
                    }
                    if (!TemPercentualEmPrimario(skill, primarios))
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
                Plugin.Log.LogInfo("BetterTooltips: BT-13 — familia de skills de atributo em %: "
                    + ListaDaFamilia(indice) + " (" + Conta(indice) + " skill(s); "
                    + ambiguas + " descricao(oes) ambigua(s))");
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("BetterTooltips: BT-13 nao montou o indice da familia — "
                    + ex.GetType().Name + ": " + ex.Message);
            }
        }

        private static bool TemPercentualEmPrimario(SkillInfo skill, CharacterAttribute[] primarios)
        {
            if (skill.AttributeEffects == null)
            {
                return false;
            }
            foreach (CharacterEffectInfo efeito in skill.AttributeEffects)
            {
                if (efeito == null || efeito.CharacterEffectMethod != CharacterEffectMethod.Percentage)
                {
                    continue;
                }
                if (EhAtributoPrimario(efeito.CharacterAttribute, primarios))
                {
                    return true;
                }
            }
            return false;
        }

        /// <summary>Lista explicita da familia (o log a imprime no boot — e a prova viva de QUEM
        /// entrou, com o nome do asset e nao com uma lista nossa).</summary>
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

        /// <summary>Apara as pontas e reduz espaco duplo — o funil (`LocalizePatch`) normaliza espacos
        /// no texto exibido, e a identidade nao pode depender de um detalhe invisivel. Devolve a
        /// PROPRIA string quando nao ha nada a mudar (o caso comum, sem alocacao).</summary>
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
                Plugin.Log.LogInfo("[Atributo % BT-13] " + linha);
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }
    }
}
