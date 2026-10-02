using System;
using System.Collections.Generic;
using System.Globalization;
using Burst2Flame;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// BT-10 (01/10) — o VALOR ABSOLUTO da cura da passiva `Reaper's Toll`, ao lado do percentual
    /// que o jogo ja mostra.
    ///
    /// PEDIDO DO DONO (verbatim): "Reaper's toll: falar quanto que cura por turno com base no valor
    /// da vida maxima do personagem nao so o % da vida".
    ///
    /// O QUE A SKILL FAZ, LIDO DO MOTOR (nao de prosa):
    ///   - o gatilho dela e `OnAnyDeathMinusDead` com a condicao `Target.IsEnemy(Source)` — ou seja,
    ///     a cura dispara QUANDO UM INIMIGO MORRE, nao "por turno" como diz o pedido (a frase do dono
    ///     e a leitura dele, nao a mecanica; escrever "per turn" na linha seria criar uma mentira
    ///     nova, e mentira em tooltip e exatamente o que este mod existe para corrigir);
    ///   - a acao do gatilho (`Reaper's Toll Proc`) tem UM efeito, cuja formula no ASSET e
    ///     `TargetStored['Healing'] = Target['MaxHealth'] * .10f`
    ///     (dump `[Action] 'Reaper's Toll Proc' ... efTipos=0:GeneralEffect{Action=...}`, ex.
    ///     scratch/cap1/fnt1/B-pular-false-diag-on/LogOutput-desta-rotina.log:1019).
    ///     Traduzido: quem tem a passiva se cura em `MaxHealth x 10%` — a vida maxima DELE, a cada
    ///     inimigo que cai.
    ///
    /// DE ONDE SAEM OS DOIS NUMEROS (numero nenhum e digitado):
    ///   1) A VIDA MAXIMA — `Character.MaxHealth`, e a propriedade do MOTOR
    ///      (`Assembly-CSharp.decompiled.cs:33252`: `MaxHealth => Mathf.Ceil(this["MaxHealth"])`).
    ///      O indexador `this["MaxHealth"]` (l.33552) chama `GetAttribute` (l.41412), que e
    ///      `SavedMap[guid] + CalculateAttribute(...)` — isto e, o valor FINAL, com powerups,
    ///      equipamento e skills ja aplicados (NAO o puro de `SavedMap`, que e so os pontos
    ///      investidos). O FINAL e exatamente o que a formula do efeito le (`Target['MaxHealth']`),
    ///      e e por isso que o numero ACOMPANHA o personagem: mudou a vida maxima (item, powerup,
    ///      level, skill de %), muda o valor mostrado. O personagem e o RECEPTOR da tooltip, pelo
    ///      caminho ja estabelecido da familia (`ShrineAuraPatch.ReceptorDaTooltip`, l.566 — o
    ///      MESMO usado por RV-26/RV-28/RV-33).
    ///   2) A PORCENTAGEM — lida da DESCRICAO do proprio asset da skill, em tempo de execucao
    ///      (`SkillInfo.Description`, a lista `Game.Instance.Skills`), como faz o RV-28
    ///      (`GlobulePatch.TentaLerPct`, l.224). Nao vem de tabela do mod nem de constante: se o
    ///      patch do jogo mudar o `10%` do asset, o numero mostrado muda junto, sozinho.
    ///
    /// POR QUE NAO `character["MaxHealth"]` CRU: e o mesmo valor, mas o caminho certo e a
    /// propriedade do motor (que ja faz o `Ceil`). O que o dono alerta para NAO usar e o `SavedMap`
    /// como se fosse o final — `SavedMap` e o PURO (pontos investidos, sem modificador) e serve
    /// para outra coisa (BetterStats usa para o "base"); a cura do jogo NAO usa o puro.
    ///
    /// ONDE O TEXTO ENTRA (docs/TEXTO-TOOLTIPS.md §1/§9):
    ///   - o VALOR vai na LINHA BRANCA (nivel 1), DENTRO da frase do jogo e ANTES do ponto final,
    ///     na cor que o MOTOR ja usa para valor dinamico — o literal `#CBB396` que
    ///     `ApplyDescriptionExpressions` (decompilado l.2327) escreve no `[N]` e `GetDamageString`
    ///     (l.2276) escreve no `*N` (mesmo literal de
    ///     `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR`, 43 usos no Assembly); nenhum hex novo e
    ///     criado — e o do proprio motor. O FORMATO e o da familia da linha do Decay
    ///     (`ShrineAuraPatch.LinhaDecayComValor`, l.850), o MESMO do
    ///     `HungerPatch.InsereValorNaLinha` (l.158): `<frase do jogo> (<valor> health for you).` — o
    ///     ponto FECHA a frase, nunca fica no meio dela (o defeito que a BT-10F consertou:
    ///     `max health. (23.3 health for you)`);
    ///   - a EXPLICACAO do calculo vai no nivel 2 (a nota do mod, marcador `#C8B090` resolvido em
    ///     runtime por `LocalizePatch.ComACorDoJogo`).
    ///
    /// GUARDA: sem personagem em foco, sem vida maxima ou sem a skill/percentual no asset, nao sai
    /// numero NENHUM (a linha do jogo fica inteira) — melhor nao mostrar do que mostrar errado.
    /// Nada aqui e hard-coded de valor: so a IDENTIDADE da skill (o nome do asset, uma string) e a
    /// cor do motor (um hex que ja existe).
    /// </summary>
    internal static class ReaperTollPatch
    {
        /// <summary>Nome do asset da skill (identificador estavel do motor). O dump do jogo traz
        /// exatamente este nome (`[Skill] 'Reaper's Toll' | tipo=Shadow | tier=3 | passivo=sim`,
        /// scratch/cap1/fnt1/*/LogOutput-desta-rotina.log:635).</summary>
        internal const string NomeDaSkill = "Reaper's Toll";

        /// <summary>Cor que o PROPRIO MOTOR escreve nos valores dinamicos: `<color=#CBB396>` em
        /// `ApplyDescriptionExpressions` (l.2327, o `[N]`) e em `GetDamageString` (l.2276, o `*N`).
        /// Nao e hex novo nem escolha estetica — e o literal do motor, o mesmo que
        /// `tools/testes/regras_cor.COR_DO_VALOR_DO_MOTOR` ja usa como `#CBB396`.</summary>
        private const string CorDoValorDoMotor = "CBB396";

        /// <summary>
        /// Monta o texto do NIVEL 1 (com o valor) e a NOTA do nivel 2 para a tooltip do Reaper's
        /// Toll. Devolve false quando nao e essa tooltip ou quando falta qualquer dado provado — e
        /// quem chamou deixa o texto como estava.
        /// </summary>
        public static bool TentaMontar(string original, string linhaDoJogo,
            out string linhaComValor, out string nota)
        {
            linhaComValor = null;
            nota = null;
            try
            {
                SkillInfo skill = SkillDaReaperToll();
                // Identidade da tooltip: so agimos sobre o texto que e a DESCRICAO do asset desta
                // skill (a chave da tabela tem de ser o texto exato do jogo, entao isto nao depende
                // de constante nossa de prosa). O `Equals` confere o tamanho antes, entao toda outra
                // string localizada sai por aqui a custo de uma comparacao.
                if (skill == null || !MesmoTexto(skill.Description, original))
                {
                    return false;
                }

                float pct = PercentualDaSkill(skill);
                if (pct <= 0f)
                {
                    Marca("sem numero: o asset de '" + NomeDaSkill + "' nao trouxe a % na descricao");
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

                // A MESMA conta do efeito do asset (`Target['MaxHealth'] * .10f`), com os dois
                // operandos vindos do motor: a vida final do personagem e a % da descricao do asset.
                // O arredondamento que o jogo aplica ao CURAR nao e legivel (o efeito mora no proc,
                // fora do dump) — por isso a casa decimal do RV-28 (`0.#`), sem afirmar inteiro.
                float cura = vida * pct / 100f;
                string valor = cura.ToString("0.#", CultureInfo.InvariantCulture);

                linhaComValor = InsereValorNaLinha(linhaDoJogo, valor);
                nota = NotaDoCalculo();

                Marca("'" + personagem.CharacterName + "' MaxHealth=" + vida.ToString("0.#")
                    + " x " + pct.ToString("0.#") + "% -> '" + valor + "'");
                return true;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[Reaper's Toll BT-10] valor dinamico falhou (linha intacta): "
                    + ex.GetType().Name + ": " + ex.Message);
                linhaComValor = null;
                nota = null;
                return false;
            }
        }

        /// <summary>Insere o valor ANTES do ponto final da linha do jogo, no formato da linha do
        /// Decay (`ShrineAuraPatch.LinhaDecayComValor`, l.850) — o MESMO do
        /// `HungerPatch.InsereValorNaLinha` (l.158): `<frase do jogo> (<valor> health for you).`. O
        /// ponto FECHA a frase; o valor nunca fica depois dele, na forma
        /// `max health. (23.3 health for you)` que a BT-10 entregou por engano.</summary>
        private static string InsereValorNaLinha(string linhaDoJogo, string valor)
        {
            string corpo = (linhaDoJogo ?? string.Empty).TrimEnd();
            string sufixo = " (<color=#" + CorDoValorDoMotor + ">" + valor + "</color> health for you)";
            if (corpo.EndsWith(".", StringComparison.Ordinal))
            {
                return corpo.Substring(0, corpo.Length - 1) + sufixo + ".";
            }
            return corpo + sufixo + ".";
        }

        /// <summary>A skill do `Reaper's Toll` no asset CARREGADO (`Game.Instance.Skills`,
        /// `List&lt;SkillInfo&gt;`, decompilado l.442635), resolvida UMA vez e guardada: o gancho roda a
        /// cada texto localizado, e varrer a lista inteira a cada chamada seria desperdicio. Falha de
        /// resolucao NAO e memorizada (tenta de novo no proximo texto).</summary>
        private static SkillInfo SkillDaReaperToll()
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

        /// <summary>A porcentagem do asset, lida do PRIMEIRO `%` da descricao
        /// ("Every enemy that dies heals you for 10% of your maximum health." -&gt; 10) e guardada
        /// junto da skill (o texto do asset nao muda durante a sessao).</summary>
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

        /// <summary>Compara a descricao do asset com o texto localizado, aparando as pontas (o asset
        /// tem descricoes com espaco sobrando; o `Limpa` do dump do debugger tambem apara).</summary>
        private static bool MesmoTexto(string a, string b)
        {
            return !string.IsNullOrEmpty(a) && !string.IsNullOrEmpty(b)
                && string.Equals(a.Trim(), b.Trim(), StringComparison.Ordinal);
        }

        /// <summary>A porcentagem do asset, lida do PRIMEIRO `%` da descricao
        /// ("Every enemy that dies heals you for 10% of your maximum health." -&gt; 10). Nada aqui e
        /// constante do mod: e o numero que o jogo carregou.</summary>
        private static bool LePercentual(string descricao, out float pct)
        {
            pct = 0f;
            if (string.IsNullOrEmpty(descricao))
            {
                return false;
            }
            int fim = descricao.IndexOf('%');
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
            return "Based on your own Max Health, so the amount follows your gear, powerups and skills.";
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
                Plugin.Log.LogInfo("[Reaper's Toll BT-10] " + linha);
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }
    }
}
