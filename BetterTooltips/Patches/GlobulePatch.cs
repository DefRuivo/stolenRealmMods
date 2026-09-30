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
    /// (ilspycmd: `player.ProcessSkillTriggers(..., TriggerType.OnGlobulePickup)` + `Root.Increment
    /// GlobulePickupCountAchievementStat`; enum `GroundEffectType { Pickup, Shrine, Destructable }`) — e a
    /// família dos pickups do jogo é essa (a `Magic Hat III`, "Produce a random Globule on the target hex.",
    /// sorteia da mesma lista; o `BattleManager.SpawnPickup` sorteia de `BattleDrops`, do mesmo tipo).
    ///
    /// RV-32 (30/09) — OS PICKUPS DE POÇÃO TAMBÉM ENTRAM. A RV-28 os deixou de fora por acreditar que a
    /// descrição deles fosse a MESMA da poção. Não é — e isso foi medido, não suposto: varredura byte a
    /// byte de `resources.assets` (1,7 GB) com `grep -abo` + leitura pontual, sem UnityPy.
    /// No cluster dos GroundEffectInfo (@1520825016 `Pickup Health 10` → campo `Name` "Minor Healing
    /// Potion" @1520825328, `Description` "Restores 10% health" @1520825352) a descrição é EXCLUSIVA do
    /// pickup. O ITEM de mesmo nome tem OUTRO texto, em outro cluster: @1521192488 "Minor Healing Potion"
    /// → @1521192860 "Restores 75 health." (bate com `docs/cobertura/itens.csv:510`). Cada uma das SEIS
    /// descrições de pickup ("Restores 10% / 15% / 20% health", "Restores 10% / 15% / 20% mana") aparece
    /// UMA única vez em todo o asset — nenhuma outra entidade a usa. O que É compartilhado é só o TÍTULO
    /// do tooltip (o campo `Name` do GroundEffectInfo, localizado por `Tooltip.ShowGroundEffectTooltip`,
    /// decompilado l.1243, e que é o nome do item: "Minor Healing Potion"); a nota entra pela DESCRIÇÃO,
    /// então a poção não é tocada. Sem mentira para outro dono — a lacuna fecha.
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
        /// TÍTULO do tooltip (prefixo `<color>` + `[Stacks]`) e por isso NÃO serve de âncora.
        /// RV-32: a família instrumentada é a do gatilho `OnGlobulePickup` — estes sete (os seis
        /// `*Globule`) MAIS as seis descrições exclusivas dos pickups de poção, em `PickupKeys`.</summary>
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
            return texto != null && (GlobuleKeys.Contains(texto) || PickupKeys.Contains(texto));
        }

        /// <summary>RV-32 — as descrições dos SEIS pickups de poção do cluster (@1520825016-@1520828016,
        /// assets `Pickup Health 10/15/20x 1` e `Pickup Mana 10/15/20x 1`). São GroundEffectInfo de
        /// `GroundEffectType == Pickup` — o MESMO gatilho do Sustenance — e por isso a nota vale aqui.
        /// Cada texto é EXCLUSIVO: a varredura do asset acha UMA ocorrência de cada, no próprio pickup
        /// (o item correspondente diz outra coisa: "Restores 75/300/… health."). O título do tooltip
        /// ("Minor Healing Potion", "Healing Potion", …) é que coincide com o nome do item — por isso ele
        /// NÃO serve de âncora: a nota entra pelo postfix do `Localize` da DESCRIÇÃO.</summary>
        private static readonly HashSet<string> PickupKeys = new HashSet<string>
        {
            "Restores 10% health",   // Pickup Health 10   -> Name "Minor Healing Potion"
            "Restores 15% health",   // Pickup Health 15   -> Name "Healing Potion"
            "Restores 20% health",   // Pickup Health 20x 1-> Name "Major Healing Potion"
            "Restores 10% mana",     // Pickup Mana 10     -> Name "Minor Mana Potion"
            "Restores 15% mana",     // Pickup Mana 15     -> Name "Mana Potion"
            "Restores 20% mana"      // Pickup Mana 20x 1  -> Name "Major Mana Potion"
        };

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
                // RV-32: no pickup de poção o que o jogador faz é PEGAR o item. Chamar a poção de
                // "Globule" seria errado — a mesma cura, com o sujeito certo em cada família.
                string abertura = PickupKeys.Contains(chaveDaTooltip)
                    ? "Picking this up also heals you for "
                    : "Consuming a Globule also heals you for ";
                string frase = abertura + pct.ToString("0.#")
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
