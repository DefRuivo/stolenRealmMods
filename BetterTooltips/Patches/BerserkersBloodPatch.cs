using System;
using System.Collections.Generic;
using System.Globalization;
using Burst2Flame;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// BT-12 (01/10) — o BONUS DE DANO CALCULADO da passiva `Beserker's Blood`, ao lado da REGRA
    /// ("por cada 1% de vida faltando") que o jogo ja mostra.
    ///
    /// PEDIDO DO DONO (verbatim): "a skill Berserker's Blood da bonus de dano com base na vida
    /// PERDIDA; a tooltip hoje nao mostra esse bonus calculado; ele quer ver QUANTO de bonus de
    /// dano ela esta dando, com base na vida que o personagem perdeu."
    ///
    /// FORMULA REAL, LIDA DO MOTOR (nao de prosa) — o asset da skill, no dump:
    ///   `[Skill] 'Beserker's Blood' | tipo=Warrior | tier=3 | passivo=sim |
    ///    attr=DamageMod:Base:Source.HealthRatioInverse * 100, |
    ///    attrTipos=0:CharacterEffectInfo{Amount=Source.HealthRatioInverse * 100;
    ///    CharacterAttribute=DamageMod;CharacterEffectMethod=Base;EffectTarget=Source;...} |
    ///    desc=" For every 1% of health missing, gain 1% increased damage."`
    ///   (scratch/cap1/fnt1/B-pular-false-diag-on/LogOutput-desta-rotina.log:607).
    /// Traduzido: o atributo `DamageMod` (Base) recebe `HealthRatioInverse x 100` — ou seja,
    /// "+X% de dano", onde X e a fracao de vida que FALTA, em porcento. A frase do asset diz
    /// exatamente isso ("for every 1% of health missing, gain 1% increased damage").
    ///
    /// 'VIDA PERDIDA' — DEFINIDA NO CODIGO DO JOGO, NAO SUPOSTA (a pergunta central da tarefa):
    ///   - `scratch/sac1/Character.cs:4644`: `public float HealthRatio => this["Health"] / MaxHealth;`
    ///     e `scratch/sac1/Character.cs:4646`: `public float HealthRatioInverse => 1f - HealthRatio;`
    ///     (a bancada do decompilado; no arquivo unico da familia: `Character.MaxHealth` na
    ///     l.33252, o indexador `this[string]` na l.33552 e `GetAttribute` na l.41412).
    ///   - NAO existe campo guardado de "vida perdida" no motor: NAO ha `LastHealthLost`,
    ///     `DamageTakenThisTurn` nem acumulador do genero. O jogo CALCULA a fracao em cima da
    ///     HORA — `1 - (vida atual / vida maxima)`. O campo `lastMaxHealthRatio` (l.500/7078/7090)
    ///     NAO e isso: e o snapshot usado para RESSCALAR a vida atual quando a vida maxima muda,
    ///     e nao a fracao de vida faltando que a formula le. Quem a formula do asset le e
    ///     `Source.HealthRatioInverse`, e e ELE que usamos.
    ///   - Logo "vida perdida" = `MaxHealth - vida atual` (em pontos) = `MaxHealth x
    ///     HealthRatioInverse` (fracao); e o bonus = essa fracao x o fator da formula.
    ///
    /// DE ONDE SAEM OS DOIS OPERANDOS (numero nenhum e digitado):
    ///   1) A FRACAO PERDIDA — `Character.HealthRatioInverse`, a propriedade do MOTOR
    ///      (`scratch/sac1/Character.cs:4646`). Ela le `this["Health"]` e `MaxHealth`, os DOIS
    ///      pelo indexador (l.3960) -> `GetAttribute` (l.11820): o valor FINAL, com powerups,
    ///      equipamento e skills aplicados (NAO o `SavedMap` puro, que e so os pontos investidos).
    ///      Por isso o numero ACOMPANHA o personagem: tomou dano -> subiu; curou -> desceu. E a
    ///      MESMA propriedade que a formula do asset le (`Source.HealthRatioInverse`). O personagem
    ///      e o RECEPTOR da tooltip (`ShrineAuraPatch.ReceptorDaTooltip`, l.566 — o mesmo caminho
    ///      de RV-26/RV-28/RV-33, e o mesmo padrao de BT-10/BT-11).
    ///   2) O FATOR — lido da PROPRIA FORMULA do asset, em tempo de execucao
    ///      (`SkillInfo.AttributeEffects[i].Amount`, a lista `Game.Instance.Skills`). O `Amount`
    ///      carregado e a string `Source.HealthRatioInverse * 100`; o parser ANCORA na propriedade
    ///      `HealthRatioInverse` e le a CONSTANTE que a multiplica (o `100`). NAO ha `100` digitado
    ///      no mod: se o asset mudar o fator, o numero mostrado muda junto, sozinho.
    ///      BT-12A: o parser le a EQUIVALENCIA, nao a grafia. Passam as formas que sao a MESMA conta
    ///      (uma constante x uma referencia a `HealthRatioInverse`): ordem dos fatores trocada
    ///      (`100 * Source.HealthRatioInverse`), sufixo `f`/`F` (`* 100f`), parenteses em volta da
    ///      expressao inteira ou de um lado (`(Source.HealthRatioInverse * 100)`), espaco livre. A
    ///      tabela de casos e a prova dos DOIS sentidos moram em `scratch/bt12/casos_ancora.json`,
    ///      rodada pelo espelho (`scratch/bt12/verifica.py`) e pelo .cs COMPILADO
    ///      (`scratch/bt12/parser_csharp.py`). Recusadas: sem a ancora (campo trocado, `SavedMap`,
    ///      termo como texto/indice), soma/divisao/segunda multiplicacao (`... * 100 + 5`), o lado
    ///      oposto sem ser UM numero constante (`* Source.DamageMod`), embrulho que muda o valor
    ///      (`Mathf.Max(1, ...)`) e a negacao do termo — a linha do jogo fica INTACTA.
    ///      RESSALVA MEDIDA (BT-12R): o embrulho `Mathf.Round(<ref>, <casas>)` e ACEITO e o
    ///      arredondamento e IGNORADO — `Mathf.Round(HealthRatioInverse,1) * 100` le o fator `100`
    ///      como se fosse `HealthRatioInverse * 100`. E o unico embrulho aceito, porque ele nao muda
    ///      o FATOR; aplicar as casas mudaria a CONTA do bonus (arredondar a fracao antes de
    ///      multiplicar) sem prova de que o motor do jogo avalia o `Mathf.Round` — fica registrado
    ///      como ressalva, nao como adivinhacao.
    ///
    /// ONDE O TEXTO ENTRA (docs/TEXTO-TOOLTIPS.md §1/§9):
    ///   - o VALOR vai na LINHA BRANCA (nivel 1), logo depois da frase do jogo, na cor que o MOTOR
    ///     ja usa para valor dinamico — o literal `#CBB396` que `ApplyDescriptionExpressions`
    ///     (decompilado l.2327) escreve no `[N]` e `GetDamageString` (l.2276) escreve no `*N`
    ///     (mesmo literal de `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR`, 43 usos no Assembly);
    ///     nenhum hex novo e criado — e o do proprio motor. O formato e o da FAMILIA (o MESMO do
    ///     `ReaperTollPatch.InsereValorNaLinha` pos-BT-10F e do `HungerPatch.InsereValorNaLinha`):
    ///     a frase do jogo TERMINA no ponto, o mod CORTA esse ponto e SOLDA o parenteses no fim,
    ///     fechando a frase de novo — `... gain 1% increased damage (23.3% increased damage right
    ///     now).` O `. (` no MEIO da frase e o defeito que a BT-10F consertou (e que a BT-12F
    ///     tirou daqui);
    ///   - a EXPLICACAO do calculo vai no nivel 2 (a nota do mod, marcador `#C8B090` resolvido em
    ///     runtime por `LocalizePatch.ComACorDoJogo`).
    ///
    /// GUARDA: sem personagem em foco, sem vida maxima, sem a skill no asset ou sem o fator legivel
    /// da formula, nao sai numero NENHUM (a linha do jogo fica INTACTA) — melhor nao mostrar do que
    /// mostrar errado.
    /// Nada aqui e hard-coded de valor: so a IDENTIDADE da skill (o nome do asset, uma string) e a
    /// cor do motor (um hex que ja existe).
    /// </summary>
    internal static class BerserkersBloodPatch
    {
        /// <summary>Nome do asset da skill (identificador estavel do motor). O dump do jogo traz
        /// exatamente este nome — com o "e" de `Beserker` como o asset o escreve
        /// (`[Skill] 'Beserker's Blood' | tipo=Warrior | tier=3 | passivo=sim`,
        /// scratch/cap1/fnt1/B-pular-false-diag-on/LogOutput-desta-rotina.log:607).</summary>
        internal const string NomeDaSkill = "Beserker's Blood";

        /// <summary>A substring que ANCORA a leitura do fator na formula do asset — o nome da
        /// propriedade do motor que a formula le. Nao e numero nem constante de balanceamento: e a
        /// identidade do termo (o dump traz `Amount=Source.HealthRatioInverse * 100`).</summary>
        private const string TermoDaFormula = "HealthRatioInverse";

        /// <summary>Cor que o PROPRIO MOTOR escreve nos valores dinamicos: `<color=#CBB396>` em
        /// `ApplyDescriptionExpressions` (l.2327, o `[N]`) e em `GetDamageString` (l.2276, o `*N`).
        /// Nao e hex novo nem escolha estetica — e o literal do motor, o mesmo que
        /// `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR` ja usa como `#CBB396`.</summary>
        private const string CorDoValorDoMotor = "CBB396";

        /// <summary>
        /// Monta o texto do NIVEL 1 (com o valor) e a NOTA do nivel 2 para a tooltip do `Beserker's
        /// Blood`. Devolve false quando nao e essa tooltip ou quando falta qualquer dado provado — e
        /// quem chamou deixa o texto como estava.
        /// </summary>
        public static bool TentaMontar(string original, string linhaDoJogo,
            out string linhaComValor, out string nota)
        {
            linhaComValor = null;
            nota = null;
            try
            {
                SkillInfo skill = SkillDoBerserkersBlood();
                // Identidade da tooltip: so agimos sobre o texto que e a DESCRICAO do asset desta
                // skill (o `Equals` confere o tamanho antes, entao toda outra string localizada sai
                // por aqui a custo de uma comparacao).
                if (skill == null || !MesmoTexto(skill.Description, original))
                {
                    return false;
                }

                float fator = FatorDaFormula(skill);
                if (fator <= 0f)
                {
                    Marca("sem numero: a formula de '" + NomeDaSkill + "' nao trouxe um fator legivel");
                    return false;
                }

                Character personagem = ShrineAuraPatch.ReceptorDaTooltip();
                if (personagem == null)
                {
                    Marca("sem numero: nenhum personagem em foco");
                    return false;
                }

                float vidaMaxima = personagem.MaxHealth;
                if (vidaMaxima <= 0f)
                {
                    Marca("sem numero: personagem em foco sem MaxHealth");
                    return false;
                }

                // A FRACAO de vida que falta, do MOTOR (`1 - vida atual / vida maxima`,
                // Character.cs:4646). Sem clamp de proposito: o motor NAO limita, e o numero
                // exibido tem de ser o que o motor calcularia (regra: nada somado a mao).
                float razaoPerdida = personagem.HealthRatioInverse;

                // A MESMA conta da formula do asset (`Source.HealthRatioInverse * 100`), com os
                // dois operandos vindos do motor: a fracao perdida do personagem e o fator lido da
                // propria formula. Ex.: 23,3% de vida faltando x 100 -> "+23,3% de dano".
                float bonus = razaoPerdida * fator;
                string valor = bonus.ToString("0.#", CultureInfo.InvariantCulture);

                linhaComValor = InsereValorNaLinha(linhaDoJogo, valor);
                nota = NotaDoCalculo();

                float perdida = vidaMaxima * razaoPerdida;
                Marca("'" + personagem.CharacterName + "' MaxHealth=" + vidaMaxima.ToString("0.#")
                    + " perdida=" + perdida.ToString("0.#")
                    + " (x " + fator.ToString("0.#") + ") -> '" + valor + "% de dano'");
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[Beserker's Blood BT-12] valor dinamico falhou (linha intacta): "
                    + ex.GetType().Name + ": " + ex.Message);
                linhaComValor = null;
                nota = null;
                return false;
            }
        }

        /// <summary>Insere o valor ANTES do ponto final da linha do jogo, no formato da FAMILIA
        /// (o MESMO do `ReaperTollPatch.InsereValorNaLinha` pos-BT-10F e do
        /// `HungerPatch.InsereValorNaLinha`): `<frase do jogo> (<valor>% increased damage right
        /// now).` O ponto FECHA a frase; o valor nunca fica depois dele — a forma
        /// `gain 1% increased damage. (<valor>% increased damage right now)` punha o ponto no MEIO
        /// e deixava a frase sem fechar (o mesmo defeito que a BT-10F consertou no Reaper's Toll,
        /// `max health. (23.3 health for you)`). O `%` fica fora da cor porque o motor colore o
        /// NUMERO, e a unidade e a mesma que a frase ja usa ("gain 1% increased damage").</summary>
        private static string InsereValorNaLinha(string linhaDoJogo, string valor)
        {
            string corpo = (linhaDoJogo ?? string.Empty).TrimEnd();
            string sufixo = " (<color=#" + CorDoValorDoMotor + ">" + valor
                + "</color>% increased damage right now)";
            if (corpo.EndsWith(".", StringComparison.Ordinal))
            {
                return corpo.Substring(0, corpo.Length - 1) + sufixo + ".";
            }
            return corpo + sufixo + ".";
        }

        /// <summary>A skill do `Beserker's Blood` no asset CARREGADO (`Game.Instance.Skills`,
        /// `List&lt;SkillInfo&gt;`), resolvida UMA vez e guardada: o gancho roda a cada texto
        /// localizado, e varrer a lista inteira a cada chamada seria desperdicio. Falha de
        /// resolucao NAO e memorizada (tenta de novo no proximo texto).</summary>
        private static SkillInfo SkillDoBerserkersBlood()
        {
            if (_skill != null)
            {
                return _skill;
            }
            if (Game.Instance == null)
            {
                return null;
            }
            List<SkillInfo> skills = Game.Instance.Skills;
            if (skills == null)
            {
                return null;
            }
            foreach (SkillInfo skill in skills)
            {
                if (skill != null && string.Equals(skill.SkillName, NomeDaSkill, StringComparison.Ordinal))
                {
                    _skill = skill;
                    return _skill;
                }
            }
            return null;
        }

        private static SkillInfo _skill;

        /// <summary>O FATOR da formula do asset, lido do `Amount` do efeito de atributo que cita
        /// `HealthRatioInverse` (o dump traz `Amount=Source.HealthRatioInverse * 100`) e guardado
        /// junto da skill (o asset nao muda durante a sessao). Nao ha numero digitado: o `100` sai
        /// do proprio asset. Formula fora da forma `HealthRatioInverse * &lt;numero&gt;` devolve 0
        /// (a linha do jogo fica intacta) em vez de adivinhar.</summary>
        private static float FatorDaFormula(SkillInfo skill)
        {
            if (_fatorLido)
            {
                return _fator;
            }
            if (skill.AttributeEffects == null)
            {
                return 0f;
            }
            foreach (CharacterEffectInfo efeito in skill.AttributeEffects)
            {
                if (efeito == null || string.IsNullOrEmpty(efeito.Amount))
                {
                    continue;
                }
                if (LeFatorDaFormula(efeito.Amount, out _fator) && _fator > 0f)
                {
                    _fatorLido = true;
                    return _fator;
                }
            }
            return 0f;
        }

        private static bool _fatorLido;
        private static float _fator;

        /// <summary>Le a CONSTANTE que multiplica `HealthRatioInverse` na expressao do asset —
        /// "Source.HealthRatioInverse * 100" -> 100. Le a EQUIVALENCIA, nao a grafia: aceita ordem
        /// dos fatores trocada, sufixo `f`/`F`, parenteses em volta de qualquer lado e espaco onde o
        /// jogo nao poe. O que NAO aceita: (a) expressao sem a ancora `HealthRatioInverse` (campo
        /// trocado, `SavedMap`, o termo so como texto/indice); (b) mais de uma multiplicacao de topo
        /// (`... * 100 + 5`, `... * 100 * 2`); (c) o lado que nao e a ancora sem ser UM numero
        /// constante (`* Source.DamageMod`); (d) embrulho em volta da ancora que nao seja o
        /// `Mathf.Round` equivalente (`Mathf.Max(1, ...)` muda o valor) nem a negacao do termo.
        /// Nada aqui e constante do mod: e o numero que o jogo carregou.</summary>
        private static bool LeFatorDaFormula(string formula, out float fator)
        {
            fator = 0f;
            if (string.IsNullOrEmpty(formula))
            {
                return false;
            }
            // Sem a propriedade ANCORA, nao ha o que ler (nao pegamos "o primeiro numero da string").
            if (formula.IndexOf(TermoDaFormula, StringComparison.Ordinal) < 0)
            {
                return false;
            }

            // Parenteses em volta da EXPRESSAO INTEIRA sao ignorados (`( A * B )` = `A * B`); os que
            // agrupam so um lado ficam, e sao tratados lado a lado depois.
            string expressao = TiraParentesesDeFora(formula.Trim());

            int estrela = -1;
            int multiplicacoes = 0;
            int profundidade = 0;
            for (int i = 0; i < expressao.Length; i++)
            {
                char c = expressao[i];
                if (c == '(')
                {
                    profundidade++;
                }
                else if (c == ')')
                {
                    profundidade--;
                    if (profundidade < 0)
                    {
                        return false; // parenteses desbalanceados: nao arriscamos
                    }
                }
                else if (c == '*' && profundidade == 0)
                {
                    multiplicacoes++;
                    estrela = i;
                }
            }
            // Exatamente UMA multiplicacao de nivel de topo: `... * 100 * 2` (duas estrelas) nao
            // passa, e `... + 5` cai no teste do numero (o lado do numero nao e so um numero).
            if (profundidade != 0 || multiplicacoes != 1)
            {
                return false;
            }

            string esquerda = expressao.Substring(0, estrela).Trim();
            string direita = expressao.Substring(estrela + 1).Trim();
            bool termoNaEsquerda = esquerda.IndexOf(TermoDaFormula, StringComparison.Ordinal) >= 0;
            bool termoNaDireita = direita.IndexOf(TermoDaFormula, StringComparison.Ordinal) >= 0;
            // A ancora tem de estar de UM lado so: nem ausente, nem nos dois.
            if (termoNaEsquerda == termoNaDireita)
            {
                return false;
            }

            string ladoDaAncora = termoNaEsquerda ? esquerda : direita;
            string ladoDoNumero = termoNaEsquerda ? direita : esquerda;
            return EhReferenciaDaRazao(ladoDaAncora) && TentaNumero(ladoDoNumero, out fator);
        }

        /// <summary>Tira os parenteses que envolvem a EXPRESSAO INTEIRA, um nivel por vez, e para
        /// quando o primeiro `(` nao fecha no ultimo caractere (parenteses que agrupam so um pedaco
        /// ficam para o tratamento por lado) ou quando estao desbalanceados.</summary>
        private static string TiraParentesesDeFora(string texto)
        {
            texto = texto.Trim();
            while (texto.Length >= 2 && texto[0] == '(' && texto[texto.Length - 1] == ')')
            {
                int profundidade = 0;
                bool fechaNoFim = true;
                for (int i = 0; i < texto.Length; i++)
                {
                    if (texto[i] == '(')
                    {
                        profundidade++;
                    }
                    else if (texto[i] == ')')
                    {
                        profundidade--;
                        if (profundidade == 0 && i != texto.Length - 1)
                        {
                            fechaNoFim = false;
                            break;
                        }
                    }
                }
                if (!fechaNoFim || profundidade != 0)
                {
                    break;
                }
                texto = texto.Substring(1, texto.Length - 2).Trim();
            }
            return texto;
        }

        /// <summary>O texto sem nenhum espaco (o espacamento e livre na expressao do asset).</summary>
        private static string SemEspacos(string texto)
        {
            return string.Concat(texto.Split(
                new char[] { ' ', '\t', '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries));
        }

        /// <summary>O lado da ancora tem de ser uma REFERENCIA ao termo — `Source.HealthRatioInverse`,
        /// `HealthRatioInverse` — e nao um uso qualquer da palavra (texto de indice, sufixo colado).
        /// O unico embrulho aceito e `Mathf.Round(<referencia>, <casas>)`: a ancora le o FATOR do lado
        /// de fora normalmente e IGNORA o arredondamento (RESSALVA da BT-12R, registrada no resumo da
        /// classe). Embrulhos que MUDAM o valor (`Mathf.Max(1, ...)`) nao sao a mesma conta e caem fora.</summary>
        private static bool EhReferenciaDaRazao(string lado)
        {
            string termo = SemEspacos(TiraParentesesDeFora(lado.Trim()));
            const string embrulho = "Mathf.Round(";
            if (termo.StartsWith(embrulho, StringComparison.Ordinal)
                && termo.EndsWith(")", StringComparison.Ordinal))
            {
                int fecha = termo.Length - 1;
                int virgula = UltimaVirgulaDeTopo(termo, embrulho.Length, fecha);
                if (virgula < 0)
                {
                    return false;
                }
                string referencia = termo.Substring(embrulho.Length, virgula - embrulho.Length);
                string casas = termo.Substring(virgula + 1, fecha - virgula - 1);
                return EhReferenciaSimples(referencia) && EhInteiroDeDigitos(casas);
            }
            return EhReferenciaSimples(termo);
        }

        /// <summary>A referencia PURA a propriedade: o termo no FIM, antecedido por um ACESSO
        /// (`algo.`) ou sozinho — nunca por aspas, `[`, outro simbolo ou um sufixo colado
        /// (`HealthRatioInverseValue` nao passa). Sem operador aritmetico em volta (o `*` ja foi
        /// separado e o `-`/`+` nao sobrevivem ao teste dos caracteres de acesso).</summary>
        private static bool EhReferenciaSimples(string texto)
        {
            if (!texto.EndsWith(TermoDaFormula, StringComparison.Ordinal))
            {
                return false;
            }
            int corte = texto.Length - TermoDaFormula.Length;
            if (corte == 0)
            {
                return true;
            }
            if (texto[corte - 1] != '.')
            {
                return false;
            }
            for (int i = 0; i < corte - 1; i++)
            {
                char c = texto[i];
                if (!(char.IsLetterOrDigit(c) || c == '_' || c == '.'))
                {
                    return false;
                }
            }
            return true;
        }

        /// <summary>Posicao da ULTIMA virgula de nivel de topo dentro de [inicio, fim); -1 se nao ha.
        /// Serve ao `Mathf.Round(<referencia>, <casas>)` — a virgula que separa os dois argumentos.</summary>
        private static int UltimaVirgulaDeTopo(string texto, int inicio, int fim)
        {
            int profundidade = 0;
            int ultima = -1;
            for (int i = inicio; i < fim; i++)
            {
                char c = texto[i];
                if (c == '(')
                {
                    profundidade++;
                }
                else if (c == ')')
                {
                    profundidade--;
                }
                else if (c == ',' && profundidade == 0)
                {
                    ultima = i;
                }
            }
            return ultima;
        }

        /// <summary>O lado oposto a ancora tem de ser UM numero constante — e so isso: digitos, `.`
        /// ou `,`, com o sufixo `f`/`F` opcional (o literal de `float` da linguagem). Qualquer outra
        /// coisa (`Source.DamageMod`, `SavedMap[...]`, `100 + 5`) devolve false e a linha do jogo
        /// fica intacta.</summary>
        private static bool TentaNumero(string lado, out float numero)
        {
            numero = 0f;
            string texto = SemEspacos(TiraParentesesDeFora(lado.Trim()));
            if (texto.Length > 0 && (texto[texto.Length - 1] == 'f' || texto[texto.Length - 1] == 'F'))
            {
                texto = texto.Substring(0, texto.Length - 1);
            }
            bool temDigito = false;
            foreach (char c in texto)
            {
                if (char.IsDigit(c))
                {
                    temDigito = true;
                }
                else if (c != '.' && c != ',')
                {
                    return false;
                }
            }
            if (!temDigito)
            {
                return false;
            }
            return float.TryParse(texto.Replace(',', '.'),
                NumberStyles.Float, CultureInfo.InvariantCulture, out numero);
        }

        /// <summary>Um inteiro escrito SO com digitos (as casas do `Mathf.Round`).</summary>
        private static bool EhInteiroDeDigitos(string texto)
        {
            bool tem = false;
            foreach (char c in texto)
            {
                if (!char.IsDigit(c))
                {
                    return false;
                }
                tem = true;
            }
            return tem;
        }

        /// <summary>Compara a descricao do asset com o texto localizado, aparando as pontas (o asset
        /// tem descricoes com espaco sobrando — esta tem um espaco ANTES de "For every..."; o
        /// `Limpa` do dump do debugger tambem apara).</summary>
        private static bool MesmoTexto(string a, string b)
        {
            return !string.IsNullOrEmpty(a) && !string.IsNullOrEmpty(b)
                && string.Equals(a.Trim(), b.Trim(), StringComparison.Ordinal);
        }

        /// <summary>A nota do NIVEL 2 (a explicacao do calculo). Uma linha, sem numero digitado e
        /// sem `[N]` (o pipeline de expressoes rodaria depois do `Localize` e interpretaria o token
        /// — regra do projeto, ver docs/cobertura/revisao/RV-19-shrines.md).</summary>
        internal static string NotaDoCalculo()
        {
            return "Counts the health you are missing right now as a share of your maximum health, "
                + "so the bonus rises as you take damage and falls as you heal.";
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
                Plugin.Log.LogInfo("[Beserker's Blood BT-12] " + linha);
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }
    }
}
