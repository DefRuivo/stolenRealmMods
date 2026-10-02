using System;
using System.Collections.Generic;
using System.Globalization;
using Burst2Flame;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// BT-11 (01/10) — o VALOR ABSOLUTO da vida maxima que a passiva `Hunger` sacrifica, ao lado do
    /// percentual que o jogo ja mostra.
    ///
    /// PEDIDO DO DONO (verbatim): "a skill Hunger sacrifica vida maxima por turno, e a tooltip hoje so
    /// fala em percentual; ele quer que diga tambem o VALOR ABSOLUTO - quanto de vida maxima vai
    /// sacrificar, com base na vida maxima do personagem".
    ///
    /// O QUE A SKILL FAZ, LIDO DO MOTOR (nao de prosa):
    ///   - o GATILHO REAL e `OnBattleStart` (dump `[Trigger] 'Hunger' | tipo=OnBattleStart ... |
    ///     status=Hunger,`, scratch/cap1/fnt1/A-dono-pular-true-diag-on/LogOutput-desta-rotina.log:638):
    ///     e no COMECO DA BATALHA que ele aplica o status `Hunger` em quem tem a passiva. O status dura
    ///     **3 turnos** (dump `[Status] 'Hunger' | ... | dur=3 | maxStk=1`, mesma log l.2985).
    ///   - o EFEITO do status e `TargetStored['ShadowDamage'] = Target.MaxHealth * .1f`
    ///     (dump `[Status] 'Hunger' ... | efeitosDano=TargetStored['ShadowDamage'] = Target.MaxHealth * .1f`,
    ///     mesma log l.2985; e o literal do motor em scratch/sac1/CompiledDynamicExpresso.cs:36698).
    ///     Traduzido: o portador perde `MaxHealth x 10%` DELE por turno.
    ///   - A FREQUENCIA "POR TURNO" NAO E SUPOSICAO DO PEDIDO — ela e do PROPRIO ASSET (o texto diz
    ///     "Sacrifices 10% maximum health per turn.") e o teste do JOGO a confirma:
    ///     `scratch/sac1/ShadowSkillTest.cs:2029` — depois de aplicar o status e rodar RODADAS inteiras
    ///     (`PassFullRound`), asserta `caster.Health < hp` com a mensagem "Hunger did not sacrifice health
    ///     over two rounds (...)" e loga "PASS: Hunger +10 mana steal, sacrificed X health" (l.2030).
    ///     Diferente do `Reaper's Toll` da BT-10 (que NAO era por turno, e sim a cada morte de inimigo),
    ///     aqui a leitura do dono e a do motor COINCIDEM — por isso a frase "per turn" pode existir na
    ///     linha sem criar mentira nova (ela ja esta na descricao do jogo).
    ///
    /// DE ONDE SAEM OS DOIS NUMEROS (numero nenhum e digitado):
    ///   1) A VIDA MAXIMA — `Character.MaxHealth`, a propriedade do MOTOR
    ///      (`scratch/sac1/Character.cs:3660`: `MaxHealth => Mathf.Ceil(this["MaxHealth"])`; no
    ///      decompilado de arquivo unico da familia, l.33252). O indexador `this["MaxHealth"]`
    ///      (`scratch/sac1/Character.cs:3960`; l.33552) chama `GetAttribute`
    ///      (`scratch/sac1/Character.cs:11820`; l.41412), que e o valor FINAL, com powerups,
    ///      equipamento e skills ja aplicados. E o MESMO valor que a formula do efeito le
    ///      (`Target.MaxHealth`), e e por isso que o numero ACOMPANHA o personagem: mudou a vida
    ///      maxima, muda o valor mostrado. O personagem e o RECEPTOR da tooltip, pelo caminho ja
    ///      estabelecido da familia (`ShrineAuraPatch.ReceptorDaTooltip`, l.566 — o MESMO usado por
    ///      RV-26/RV-28/RV-33).
    ///   2) A PORCENTAGEM — lida da DESCRICAO do proprio asset da skill, em tempo de execucao
    ///      (`SkillInfo.Description`, a lista `Game.Instance.Skills`), como faz o RV-28
    ///      (`GlobulePatch.TentaLerPct`, l.224) e a BT-10 (`ReaperTollPatch.PercentualDaSkill`).
    ///      Nao vem de tabela do mod nem de constante: se o patch do jogo mudar o `10%` do asset, o
    ///      numero mostrado muda junto, sozinho.
    ///
    /// A % CERTA (armadilha que a descricao do `Hunger` arma): o texto tem DUAS porcentagens —
    /// "Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn." A do SACRIFICIO e a que
    /// precede a frase de vida maxima ("10% maximum health"); a primeira ("10% @mana steal@") e a do
    /// MANA. Hoje as duas valem 10, mas isso e coincidencia do asset: ler a "primeira %" (o atalho da
    /// BT-10) mostraria o numero ERRADO se um patch futuro divergir as duas. Por isso o parser ANCORA
    /// na palavra `health` e pega a `%` imediatamente antes dela — nunca a primeira do texto.
    ///
    /// ONDE O TEXTO ENTRA (docs/TEXTO-TOOLTIPS.md §1/§9):
    ///   - o VALOR vai na LINHA BRANCA (nivel 1), dentro da frase do jogo, na cor que o MOTOR ja usa
    ///     para valor dinamico — o literal `#CBB396` que `ApplyDescriptionExpressions` (decompilado
    ///     l.2327) escreve no `[N]` e `GetDamageString` (l.2276) escreve no `*N` (mesmo literal de
    ///     `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR`, 43 usos no Assembly); nenhum hex novo e
    ///     criado — e o do proprio motor. O formato e o da linha do Decay Shrine
    ///     (`ShrineAuraPatch.LinhaDecayComValor`, l.891): o valor entra ANTES do ponto final, como
    ///     " (<valor> health per turn for you).";
    ///   - a EXPLICACAO do calculo vai no nivel 2 (a nota do mod, marcador `#C8B090` resolvido em
    ///     runtime por `LocalizePatch.ComACorDoJogo`).
    ///
    /// GUARDA: sem personagem em foco, sem vida maxima ou sem a skill/percentual no asset, nao sai
    /// numero NENHUM (a linha do jogo fica inteira) — melhor nao mostrar do que mostrar errado.
    /// Nada aqui e hard-coded de valor: so a IDENTIDADE da skill (o nome do asset, uma string) e a
    /// cor do motor (um hex que ja existe).
    /// </summary>
    internal static class HungerPatch
    {
        /// <summary>Nome do asset da skill (identificador estavel do motor). O dump do jogo traz
        /// exatamente este nome (`[Skill] 'Hunger' | tipo=Shadow | tier=3 | passivo=sim`,
        /// scratch/cap1/fnt1/A-dono-pular-true-diag-on/LogOutput-desta-rotina.log:637).</summary>
        internal const string NomeDaSkill = "Hunger";

        /// <summary>Cor que o PROPRIO MOTOR escreve nos valores dinamicos: `<color=#CBB396>` em
        /// `ApplyDescriptionExpressions` (l.2327, o `[N]`) e em `GetDamageString` (l.2276, o `*N`).
        /// Nao e hex novo nem escolha estetica — e o literal do motor, o mesmo que
        /// `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR` ja usa como `#CBB396`.</summary>
        private const string CorDoValorDoMotor = "CBB396";

        /// <summary>
        /// Monta o texto do NIVEL 1 (com o valor) e a NOTA do nivel 2 para a tooltip do `Hunger`.
        /// Devolve false quando nao e essa tooltip ou quando falta qualquer dado provado — e quem
        /// chamou deixa o texto como estava.
        /// </summary>
        public static bool TentaMontar(string original, string linhaDoJogo,
            out string linhaComValor, out string nota)
        {
            linhaComValor = null;
            nota = null;
            try
            {
                SkillInfo skill = SkillDoHunger();
                // Identidade da tooltip: so agimos sobre o texto que e a DESCRICAO do asset desta
                // skill. O texto do `Hunger` e COMPARTILHADO entre a skill e o status de mesmo nome
                // (BUG-32: "o mesmo texto nos dois, mesma mecanica") — os dois mostram o mesmo
                // sacrificio, entao casar os dois e correto, nao efeito colateral.
                if (skill == null || !MesmoTexto(skill.Description, original))
                {
                    return false;
                }

                float pct = PercentualDaSkill(skill);
                if (pct <= 0f)
                {
                    Marca("sem numero: o asset de '" + NomeDaSkill + "' nao trouxe a % do sacrificio");
                    return false;
                }

                Character personagem = ShrineAuraPatch.ReceptorDaTooltip();
                if (personagem == null)
                {
                    Marca("sem numero: nenhum personagem em foco");
                    return false;
                }

                float vida = personagem.MaxHealth;
                if (vida <= 0f)
                {
                    Marca("sem numero: personagem em foco sem MaxHealth");
                    return false;
                }

                // A MESMA conta do efeito do asset (`Target.MaxHealth * .1f`), com os dois operandos
                // vindos do motor: a vida final do personagem e a % da descricao do asset. A casa
                // decimal do RV-28 (`0.#`), sem afirmar inteiro: o jogo pode truncar na aplicacao, e
                // nos mostramos o valor da formula.
                float sacrificio = vida * pct / 100f;
                string valor = sacrificio.ToString("0.#", CultureInfo.InvariantCulture);

                linhaComValor = InsereValorNaLinha(linhaDoJogo, valor);
                nota = NotaDoCalculo();

                Marca("'" + personagem.CharacterName + "' MaxHealth=" + vida.ToString("0.#")
                    + " x " + pct.ToString("0.#") + "% -> '" + valor + "' por turno");
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[Hunger BT-11] valor dinamico falhou (linha intacta): "
                    + ex.GetType().Name + ": " + ex.Message);
                linhaComValor = null;
                nota = null;
                return false;
            }
        }

        /// <summary>Insere o valor ANTES do ponto final da linha do jogo, no formato da linha do Decay
        /// (`ShrineAuraPatch.LinhaDecayComValor`, l.891): `<frase do jogo> (<valor> health per turn
        /// for you).` — o "per turn" ecoa a frequencia que o PROPRIO asset ja declara ("Sacrifices 10%
        /// maximum health per turn."), confirmada pelo teste do jogo.</summary>
        private static string InsereValorNaLinha(string linhaDoJogo, string valor)
        {
            string corpo = (linhaDoJogo ?? string.Empty).TrimEnd();
            string sufixo = " (<color=#" + CorDoValorDoMotor + ">" + valor + "</color> health per turn for you)";
            if (corpo.EndsWith(".", StringComparison.Ordinal))
            {
                return corpo.Substring(0, corpo.Length - 1) + sufixo + ".";
            }
            return corpo + sufixo + ".";
        }

        /// <summary>A skill do `Hunger` no asset CARREGADO (`Game.Instance.Skills`, `List&lt;SkillInfo&gt;`,
        /// decompilado l.442635), resolvida UMA vez e guardada: o gancho roda a cada texto localizado, e
        /// varrer a lista inteira a cada chamada seria desperdicio. Falha de resolucao NAO e memorizada
        /// (tenta de novo no proximo texto).</summary>
        private static SkillInfo SkillDoHunger()
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

        /// <summary>A porcentagem do SACRIFICIO, lida da DESCRICAO do asset e guardada junto da skill (o
        /// texto do asset nao muda durante a sessao). A descricao tem duas `%` — a do mana steal e a do
        /// sacrificio; o parser ancora na frase de vida maxima.</summary>
        private static float PercentualDaSkill(SkillInfo skill)
        {
            if (_pctLido)
            {
                return _pct;
            }
            if (LePercentual(skill.Description, out _pct) && _pct > 0f)
            {
                _pctLido = true;
            }
            return _pct;
        }

        private static bool _pctLido;
        private static float _pct;

        /// <summary>Compara a descricao do asset com o texto localizado. A comparacao NORMALIZA espacos
        /// internos: a descricao do `Hunger` carrega um espaco DUPLO depois do primeiro ponto
        /// ("Grants 10% @mana steal@.  Sacrifices...") enquanto o funil (`LocalizePatch`, normalizacao
        /// de espacos) ja pode ter reduzido o texto exibido a um espaco — sem isto, a identidade
        /// dependeria de um detalhe invisivel de espaco.</summary>
        private static bool MesmoTexto(string a, string b)
        {
            if (string.IsNullOrEmpty(a) || string.IsNullOrEmpty(b))
            {
                return false;
            }
            return string.Equals(NormalizaEspacos(a), NormalizaEspacos(b), StringComparison.Ordinal);
        }

        private static string NormalizaEspacos(string texto)
        {
            string s = texto.Trim();
            while (s.Contains("  "))
            {
                s = s.Replace("  ", " ");
            }
            return s;
        }

        /// <summary>A porcentagem do SACRIFICIO, lida do asset: a `%` que precede a frase de VIDA MAXIMA
        /// ("... Sacrifices 10% maximum health per turn." -&gt; 10). NAO e a primeira `%` do texto (essa e
        /// a do `mana steal`, outro numero possivel) — a ancora e a palavra `health`, e o parser anda
        /// para tras a partir dela. Nada aqui e constante do mod: e o numero que o jogo carregou.</summary>
        private static bool LePercentual(string descricao, out float pct)
        {
            pct = 0f;
            if (string.IsNullOrEmpty(descricao))
            {
                return false;
            }
            int ancora = descricao.IndexOf("health", StringComparison.OrdinalIgnoreCase);
            if (ancora < 0)
            {
                return false;
            }
            int fim = descricao.LastIndexOf('%', ancora);
            if (fim < 0)
            {
                return false;
            }
            int ini = fim;
            while (ini > 0)
            {
                char c = descricao[ini - 1];
                if (char.IsDigit(c) || c == '.' || c == ',')
                {
                    ini--;
                    continue;
                }
                break;
            }
            if (ini >= fim)
            {
                return false;
            }
            string numero = descricao.Substring(ini, fim - ini).Replace(',', '.');
            return float.TryParse(numero, NumberStyles.Float, CultureInfo.InvariantCulture, out pct);
        }

        /// <summary>A nota do NIVEL 2 (a explicacao do calculo). Uma linha, sem numero digitado e
        /// sem `[N]` (o pipeline de expressoes rodaria depois do `Localize` e interpretaria o token
        /// — regra do projeto, ver docs/cobertura/revisao/RV-19-shrines.md).</summary>
        internal static string NotaDoCalculo()
        {
            return "Based on your own Max Health, so the amount sacrificed follows your gear, powerups and skills.";
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
                Plugin.Log.LogInfo("[Hunger BT-11] " + linha);
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }
    }
}
