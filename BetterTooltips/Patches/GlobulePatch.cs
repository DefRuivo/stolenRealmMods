using System;
using System.Collections.Generic;
using System.Globalization;
using Burst2Flame;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// RV-28 (30/09) — cura DINÂMICA do `Sustenance I/II` no tooltip de TODO globule.
    ///
    /// A FAMÍLIA (censo do próprio jogo + assets, `resources.assets` @1520817xxx-1520829xxx, o cluster
    /// dos GroundEffectInfo — nome E descrição lidos byte a byte, com o comprimento de cada string
    /// conferido): `Cleansing Globule`/"Cleanses all debuffs" (@1520818292),
    /// `Energy Globule`/"Grants an additional Action Point" (@1520823512),
    /// `Health Globule`/"Heals for 50% of Max Health" (@1520824128),
    /// `Mana Globule`/"Restores 50% of Max Mana" (@1520824732),
    /// `Power Globule`/"Increases all damage by 10%" (@1520828936),
    /// `Refreshing Globule`/"Lowers Cooldowns by 1" (@1520829548).
    /// Por que ESTES são "globules": o gatilho do Sustenance é `TriggerType.OnGlobulePickup`, disparado
    /// por `GroundEffect.ExecuteActionOnEnter` quando `GroundEffectInfo.GroundEffectType == Pickup`
    /// (decompilado l.117020-117023) — e a família dos pickups do jogo é essa (a `Magic Hat III`,
    /// "Produce a random Globule on the target hex.", sorteia da mesma lista). Os objetos
    /// `Pickup Health 10`/`Pickup Mana 10` do mesmo cluster NÃO entram: o nome não é `*Globule` e a
    /// descrição deles é a da poção ("Restores 10% health"), texto COMPARTILHADO com o item — uma nota
    /// aqui mentiria para a poção (família do BUG-31/INC-1). Decisão registrada.
    ///
    /// O `Power Globule` é BUFF DE DANO, não cura — e entra do mesmo jeito, porque a cura do Sustenance
    /// acontece ao CONSUMIR o globule, qualquer que seja o efeito dele ("Consuming any Globule..."). A
    /// chave da nota vai nas DUAS descrições possíveis dele: o `GroundEffectInfo.Description`
    /// ("Increases all damage by 10%") e a do status que ele aplica
    /// ("Increases damage and summon damage by 10%", `status.csv:370`), porque o tooltip do ground
    /// effect usa `ActionStatuses[0].Description` QUANDO existe (`Tooltip.ShowGroundEffectTooltip`,
    /// decompilado l.214180) — e isso o asset não deixa ler por byte scan.
    ///
    /// A PORCENTAGEM NÃO É HARDCODED. O ponto aberto do RV-24 é se `SkillsThatReplace` faz a tier II
    /// substituir a I (20%) ou se as duas ficam ativas (8% + 20% = 28%). Aqui isso não é decidido: as
    /// tiers são lidas da LISTA JÁ RESOLVIDA PELO JOGO — `Character.Skills` (decompilado l.32847-32890,
    /// que descarta a skill quando `GetSkill(algum item do SkillsThatReplace DELA) > 0`) — e cada tier
    /// ativa soma, porque cada uma tem o SEU gatilho em `OnGlobulePickup` ("Sustenance I Proc" /
    /// "Sustenance II Proc", os testes do próprio jogo em l.183433/183512). Com uma tier ⇒ 8% ou 20%;
    /// com as duas ⇒ 28%. O texto e o número saem certos nos dois cenários, sem precisar fechar a dúvida.
    ///
    /// Os valores saem das propriedades do personagem em foco: `Character.MaxHealth`/`MaxMana`
    /// (`Mathf.Ceil(this["MaxHealth"])`, l.32362/32364) — o MESMO resolvedor de receptor do RV-22/23.
    /// A base é `% da vida máxima e da mana máxima` (texto do próprio asset do Sustenance). O
    /// ARREDONDAMENTO do motor para a cura real não é legível (o efeito mora no proc, que não está no
    /// dump): o mod mostra o produto com uma casa decimal e não afirma inteiro.
    /// </summary>
    public static class GlobulePatch
    {
        /// <summary>As descrições (chave EXATA do `OptionsManager.Localize`) que o tooltip de um
        /// globule mostra. São elas que o postfix do `LocalizePatch` recebe — o nome do asset vira o
        /// TÍTULO do tooltip (prefixo `<color>` + `[Stacks]`) e por isso NÃO serve de âncora.</summary>
        private static readonly HashSet<string> GlobuleKeys = new HashSet<string>
        {
            "Heals for 50% of Max Health",                 // Health Globule
            "Restores 50% of Max Mana",                    // Mana Globule
            "Cleanses all debuffs",                        // Cleansing Globule
            "Grants an additional Action Point",           // Energy Globule
            "Lowers Cooldowns by 1",                       // Refreshing Globule
            "Increases all damage by 10%",                 // Power Globule (GroundEffectInfo.Description)
            "Increases damage and summon damage by 10%"    // Power Globule (descrição do status; status.csv:370)
        };

        public static bool EhGlobule(string texto)
        {
            return texto != null && GlobuleKeys.Contains(texto);
        }

        /// <summary>Começo exato da descrição do Sustenance no asset da skill (tier I e II).
        /// O texto termina em "of max life and mana." (o RV-14 corrige "life"→"health" só na SAÍDA).</summary>
        private const string PrefixoSustenance = "Consuming any Globule heals you for ";

        /// <summary>
        /// A frase do Sustenance para este globule — "" quando não há nada a mostrar (sem a skill, sem
        /// personagem em foco, ou falha de leitura). Nunca lança.
        /// </summary>
        public static string FraseSustenance(string chaveDaTooltip)
        {
            try
            {
                if (!EhGlobule(chaveDaTooltip))
                {
                    return "";
                }

                Character personagem = ShrineAuraPatch.ReceptorDaTooltip();
                if (personagem == null)
                {
                    Marca("sem numero: nenhum personagem em foco");
                    return "";
                }

                // A LISTA ATIVA do jogo (já resolvida por SkillsThatReplace) — nunca uma tabela nossa.
                // O getter `Character.Skills` remonta a lista a cada chamada (decompilado l.32860+),
                // então o resultado fica em cache curto (1s) por personagem — e o cache caduca sozinho,
                // de modo que aprender uma tier NOVA durante a batalha muda o número em ~1s.
                float pct;
                List<string> tiers;
                PctDasTiersAtivas(personagem, out pct, out tiers);
                if (pct <= 0f || tiers.Count == 0)
                {
                    Marca($"'{chaveDaTooltip}': {personagem.CharacterName} nao tem Sustenance ativa -> sem numero");
                    return "";
                }

                float vida = personagem.MaxHealth;
                float mana = personagem.MaxMana;
                if (vida <= 0f && mana <= 0f)
                {
                    Marca("sem numero: personagem sem MaxHealth/MaxMana");
                    return "";
                }

                string quem = tiers.Count == 1 ? tiers[0] : string.Join(" and ", tiers.ToArray());
                string frase = "Consuming a Globule also heals you for " + pct.ToString("0.#")
                    + "% of your Max Health and Max Mana (" + quem + "): "
                    + (vida * pct / 100f).ToString("0.#") + " health and "
                    + (mana * pct / 100f).ToString("0.#") + " mana with your current pools.";
                Marca($"'{chaveDaTooltip}': {personagem.CharacterName} {quem} = {pct.ToString("0.#")}%"
                    + $" -> {frase}");
                return frase;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Globule RV-28] frase do Sustenance falhou (tooltip intacto): {ex.GetType().Name}: {ex.Message}");
                return "";
            }
        }

        /// <summary>
        /// A % do Sustenance ATIVA e os nomes das tiers que a concedem, lidos de
        /// `Character.Skills` (a lista JÁ RESOLVIDA pelo jogo: uma skill sai dela quando
        /// `GetSkill(algum item do SkillsThatReplace DELA) > 0`, decompilado l.32876-32888).
        /// Cada tier que fica na lista tem o seu próprio gatilho em `OnGlobulePickup`, então as
        /// porcentagens SOMAM — 8% com só a I, 20% com só a II (se a II substitui a I) ou 28% com as
        /// duas (se não substitui). Nada disso é decidido aqui: é o que o jogo tem ativo.
        /// Cache de 1s por personagem (o getter remonta a lista inteira a cada chamada).
        /// </summary>
        private static void PctDasTiersAtivas(Character personagem, out float pct, out List<string> tiers)
        {
            if (_cacheChar == personagem && _cacheTiers != null
                && UnityEngine.Time.realtimeSinceStartup - _cacheQuando < TtlCache)
            {
                pct = _cachePct;
                tiers = _cacheTiers;
                return;
            }

            pct = 0f;
            tiers = new List<string>();
            List<SkillInfo> skills = personagem.Skills;
            if (skills != null)
            {
                foreach (SkillInfo skill in skills)
                {
                    if (skill == null || string.IsNullOrEmpty(skill.Description))
                    {
                        continue;
                    }
                    float daSkill;
                    if (!TentaLerPct(skill.Description, out daSkill) || daSkill <= 0f)
                    {
                        continue;
                    }
                    pct += daSkill;
                    tiers.Add(string.IsNullOrEmpty(skill.SkillName) ? "(sem nome)" : skill.SkillName);
                }
            }

            _cacheChar = personagem;
            _cachePct = pct;
            _cacheTiers = tiers;
            _cacheQuando = UnityEngine.Time.realtimeSinceStartup;
        }

        private static Character _cacheChar;
        private static float _cachePct;
        private static List<string> _cacheTiers;
        private static float _cacheQuando = -999f;
        private const float TtlCache = 1f;

        /// <summary>
        /// Lê a porcentagem da DESCRIÇÃO que o jogo tem daquela skill ativa
        /// ("Consuming any Globule heals you for 8% of max life and mana.") — o número é do asset, não
        /// de uma tabela do mod. Exigir o prefixo inteiro evita casar com texto parecido.
        /// </summary>
        private static bool TentaLerPct(string descricao, out float pct)
        {
            pct = 0f;
            int i = descricao.IndexOf(PrefixoSustenance, StringComparison.Ordinal);
            if (i < 0)
            {
                return false;
            }
            i += PrefixoSustenance.Length;
            int fim = descricao.IndexOf('%', i);
            if (fim < 0)
            {
                return false;
            }
            string numero = descricao.Substring(i, fim - i).Trim();
            return numero.Length > 0
                && float.TryParse(numero, NumberStyles.Float, CultureInfo.InvariantCulture, out pct);
        }

        /// <summary>Loga cada combinação UMA vez (o postfix roda a cada frame de hover).</summary>
        private static readonly HashSet<string> _marcas = new HashSet<string>();

        private static void Marca(string linha)
        {
            try
            {
                if (_marcas.Count >= 200 || !_marcas.Add(linha))
                {
                    return;
                }
                Plugin.Log.LogInfo($"[Globule RV-28] {linha}");
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }
    }
}
