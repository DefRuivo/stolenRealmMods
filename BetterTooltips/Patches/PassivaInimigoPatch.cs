using System;
using System.Collections.Generic;
using System.Globalization;
using Burst2Flame;
using HarmonyLib;
using UnityEngine;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// BT-18 (03/10) — PASSIVAS DE INIMIGO (`SpecialEffect` / asset `EnemyMod`): dar ao tooltip do
    /// link do `ExamineWindow` (decompilado l.105319,
    /// `Tooltip.ShowUniversalTooltip(Localize(mod.name), "", Localize(mod.description))`) o que a
    /// descricao exibida NAO traz.
    ///
    /// O QUE O RELATORIO BT-18 PROVOU (fonte desta implementacao —
    /// `docs/cobertura/revisao/BT-18-passivas-inimigo.md`):
    ///   - o enum `SpecialEffect` NAO carrega valor nenhum (§0/§1): e etiqueta de exibicao (90
    ///     valores, so `[Description]`; a unica leitura nominal do enum no assembly e
    ///     `SpecialEffect.ManaShield`, para esconder a mana bar de boss);
    ///   - o valor vive na DATA do asset `EnemyMod` (`effects[].Amount` = expressao avaliada por
    ///     `Game.Eval&lt;float&gt;`, §3.2) e nos `skillTriggers[]` (comportamentos `OnDeath`,
    ///     `OnGettingHitAny`, ... §3.3);
    ///   - o corpo do tooltip e o CAMPO `description` do asset, e o funil por onde ele passa e
    ///     `OptionsManager.Localize` — o MESMO que o `LocalizePatch` intercepta (§6.1/§6.3);
    ///   - a MAIORIA dos 43 mods JA traz o numero na propria descricao (Beastly/Calamitous/Furious/
    ///     Savage I–III 25/50/100, Elusive 25, Destructive 50, Resilient 25, Vampiric 50, Giant,
    ///     Miniature, Monstrous Momentum, Rampaging, Berserking §4.2) -> NADA a fazer nesses:
    ///     acrescentar um numero que ja esta escrito seria ruido;
    ///   - as COMPORTAMENTAIS (on death / on hit / auras / "Casts X") NAO tem numero em texto nenhum
    ///     (§10.5) -> o que da para acrescentar honestamente e CONTEXTO provado: as CONDICOES do
    ///     gatilho extraidas do asset no §10.2;
    ///   - `Redemptive` ("Heals allies on death") NAO tem NENHUM literal numerico: o quanto cura e
    ///     delegado a um `skillTrigger` cujas `Actions` referenciam objetos de acao separados
    ///     (Mass Cure `path_id` 2543785 / Holy Ground 2543782 — CANDIDATOS, §5) -> Onda 2.
    ///
    /// ONDA 1 (a tabela `NotasPorDescricao`): descricao EXIBIDA -> nota curta, com procedencia
    /// escrita em cada entrada. As notas de CONTEXTO saem das CONDICOES do gatilho do §10.2; a
    /// unica com NUMERO (Regenerating) sai da tabela de localizacao do PROPRIO jogo
    /// `enemyMod-description-&lt;GUID&gt;` (§10.4). Onde a descricao ja mostra o valor, NAO ha entrada
    /// (regra do pedido: nao duplicar).
    ///
    /// ONDA 2 (`Redemptive`): resolucao PREGUICOSA em runtime do asset do mod (o gatilho e as
    /// `Actions`/`ActionStatuses` que ele referencia), com `try/catch` e cache — nunca trava a UI nem
    /// avalia expressao de atribuicao (ver `TentaNumero`). Sem numero provado, a nota e QUALITATIVA e
    /// o numero fica na tabela de PLACEHOLDER `ValoresPendentesDeMedicao`, claramente marcada para ser
    /// preenchida apos MEDICAO EM JOGO (§8.1, opcao de risco baixo).
    ///
    /// DOIS GANCHOS, O MESMO TEXTO (idempotente): o postfix do FUNIL (`OptionsManager.Localize`, por
    /// onde o corpo do tooltip nasce — cobre tambem qualquer outro consumidor da descricao) e o
    /// postfix do PROPRIO tooltip (`Tooltip.ShowUniversalTooltip`, l.334459, o metodo que o link de
    /// passive de inimigo chama) como REDE de seguranca para um caminho que entregue a descricao sem
    /// passar pelo funil. `TentaAnexar` devolve null quando a nota JA esta no texto, entao os dois
    /// juntos NUNCA duplicam.
    ///
    /// SEM SEGREDO NEM INVENCAO: nenhum numero e digitado sem procedencia (a de cada entrada esta no
    /// comentario dela) e, sem dado provado, o texto do jogo fica INTACTO — e o log diz o porque.
    /// </summary>
    internal static class PassivaInimigoPatch
    {
        // ------------------------------------------------------------------ ONDA 1 — a tabela

        /// <summary>
        /// Descricao EXIBIDA do `EnemyMod` -> nota (nivel 2). A chave e o texto EXATO que o funil
        /// recebe (`OptionsManager.Localize(enemyMod.description)`); a nota entra num bloco de cor
        /// do nivel 2, no mesmo formato do `LocalizePatch.AnexarNota`. A busca apara as pontas
        /// (espaco sobrando do asset nao pode esconder a chave) — o resto e identidade EXATA.
        ///
        /// NAO entram aqui os mods cuja descricao JA traz o valor (tiers 25/50/100, Elusive 25,
        /// Destructive 50, Resilient 25, Vampiric 50, Giant, Miniature, Monstrous Momentum,
        /// Rampaging, Berserking): anexar de novo seria repetir o que o jogador ja le.
        /// </summary>
        private static readonly Dictionary<string, string> NotasPorDescricao = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            // Regenerating — descricao do ASSET (@1520128628, §4.2): "Regenerates health every
            // turn." — SEM numero no texto exibido.
            // PROCEDENCIA do numero: a tabela de localizacao do PROPRIO jogo
            // `enemyMod-description-<GUID>` (BT-18 §10.4), extraida de `resources.assets`. O asset
            // guarda TAMBEM `effects[].Amount = Source.GetFlatDamageValue * 5` (§4.2), dado
            // DIVERGENTE registrado no §10.5: e ponto de CONFERENCIA EM TELA, nao invencao do mod.
            { "Regenerates health every turn.",
              "Regenerates 20% of Max Health per turn; Max Health is reduced by 30%." },

            // Teleporting — descricao do ASSET (@1520131416, §4.2): "Teleports randomly when
            // struck". CONTEXTO provado pela CONDICAO do gatilho (§10.2): o gatilho so dispara com
            // `!Source.IsRooted && !Source.IsStunned` e o destino e
            // `Cell == Source.RandomEmptyCellByCharacterWithinRange(Source.RandomEnemy, 3)`.
            { "Teleports randomly when struck",
              "It cannot trigger while Rooted or Stunned, and it lands on an empty hex within 3 hexes of an enemy." },

            // Cursed — descricao do ASSET (@1520119244, §4.2): "Applies Curse on striking and when
            // struck". CONTEXTO pela CONDICAO do gatilho (§10.2): so age em acao HOSTIL
            // (`ActionProperties.IsHarmful`) e so se o alvo AINDA NAO tem o status
            // (`Target.HasNoStatus("SHD_Status_Curse")`).
            { "Applies Curse on striking and when struck",
              "Only harmful abilities apply it, and only while the target does not already have Curse." },

            // Vengeful — descricao do ASSET (@1520133988, §4.2): "Gains increased damage for each
            // ally killed". CONTEXTO pela CONDICAO do gatilho (§10.2): `Target.IsAlly(Source)` —
            // conta a morte de um ALIADO DO PROPRIO mod (outro inimigo), nao a dos seus personagens.
            { "Gains increased damage for each ally killed",
              "Counts the death of another enemy allied with it, not the death of your characters." },
        };

        // ------------------------------------------------------------ IDENTIDADE do Redemptive

        /// <summary>O `name` do asset do mod (identificador estavel — §5). O QUE nao existe e um
        /// NUMERO no asset: por isso a Onda 2 resolve em runtime e o numero vive no placeholder.</summary>
        private const string NomeModRedemptive = "Redemptive";

        /// <summary>A descricao EXIBIDA do Redemptive (o campo `description` do asset, §5) — a chave
        /// do tooltip. O `[Description]` do enum (`"Redemptive"`) NAO e a origem desta frase (§6.3).</summary>
        private const string DescricaoRedemptive = "Heals allies on death";

        /// <summary>
        /// ONDA 2 — PLACEHOLDER do valor da cura do `Redemptive` (BT-18 §8.1, opcao de risco baixo
        /// escolhida depois de medir o custo da resolucao em runtime). O valor `null` significa
        /// **AINDA NAO MEDIDO EM JOGO**: enquanto for null, `NotaRedemptive` NAO afirma numero nenhum
        /// (cai na explicacao qualitativa). NADA aqui e estimado: a medicao em jogo e a unica fonte
        /// aceita para preencher (o asset nao tem o literal — §5).
        /// TODO(BT-18): apos a medicao em jogo, trocar o null pelo texto medido (ex.: "Heals allies
        /// for N health on death."). A procedencia (data/sessao) vai no comentario da entrada.
        /// </summary>
        private static readonly Dictionary<string, string> ValoresPendentesDeMedicao = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            { NomeModRedemptive, null },
        };

        // ------------------------------------------------------------------- API dos ganchos

        /// <summary>
        /// Devolve o texto com a NOTA anexada, ou **null** quando nao ha nada a fazer (nao e uma
        /// descricao conhecida, a nota esta vazia, ou a nota JA esta no texto). Idempotente de
        /// proposito: e o que permite os DOIS ganchos rodarem para a MESMA descricao sem duplicar.
        ///
        /// A nota sai no MESMO formato das notas do `LocalizePatch`: `<texto> \n\n
        /// <color=#C8B090>nota</color>`, com o marcador do nivel 2 (que o gancho das notas troca em
        /// runtime pela cor do campo `Tooltip.specialDescColor`).
        /// </summary>
        internal static string TentaAnexar(string textoExibido, string chave)
        {
            if (string.IsNullOrEmpty(textoExibido))
            {
                return null;
            }
            string nota = NotaDe(chave);
            if (string.IsNullOrEmpty(nota))
            {
                return null;
            }
            if (textoExibido.IndexOf(nota, StringComparison.Ordinal) >= 0)
            {
                // Ja anexada (o outro gancho, ou uma chamada anterior com o texto montado): nao
                // acrescenta de novo. E o que impede o Redemptive/Destrutivo de sair duplicado.
                return null;
            }
            MarcaVivo();
            return textoExibido.TrimEnd() + "\n\n"
                + "<color=#" + LocalizePatch.MarcadorCorDeExplicacao + ">" + nota + "</color>";
        }

        /// <summary>A nota de UMA descricao (Onda 1 pela tabela; Onda 2 pelo mod), ou null.</summary>
        private static string NotaDe(string descricao)
        {
            if (string.IsNullOrEmpty(descricao))
            {
                return null;
            }
            string chave = descricao.Trim();
            string nota;
            if (NotasPorDescricao.TryGetValue(chave, out nota))
            {
                return nota;
            }
            if (string.Equals(chave, DescricaoRedemptive, StringComparison.Ordinal))
            {
                return NotaRedemptive();
            }
            return null;
        }

        // ----------------------------------------------------------------- ONDA 2 — Redemptive

        /// <summary>A nota resolvida do Redemptive (cache). null = ainda nao resolvida/indisponivel.</summary>
        private static string _notaRedemptive;

        /// <summary>
        /// ONDA 2 (pre-guicoso): a nota do `Redemptive`. Ordem de preferencia:
        ///   1) o valor MEDIDO (a tabela de placeholder, quando preenchida);
        ///   2) o numero resolvido em runtime por `TentaNumero` (se o asset carregado trouxer uma
        ///      expressao NUMERICA — o caso comum e a cura estar numa acao referenciada, que nao
        ///      expoe numero; ver o comentario de `TentaNumero`);
        ///   3) a explicacao QUALITATIVA com as habilidades que o gatilho referencia (lidas AO VIVO
        ///      do asset: §5 diz que `Actions` aponta para Mass Cure/Holy Ground).
        /// Falha de leitura NUNCA vira numero: devolve null (texto intacto) e o log diz o motivo.
        /// </summary>
        private static string NotaRedemptive()
        {
            if (_notaRedemptive != null)
            {
                return _notaRedemptive;
            }
            if (Burst2Flame.Game.Instance == null)
            {
                // O jogo ainda nao carregou os assets: NAO memoriza a falha — a proxima chamada tenta
                // de novo (a descricao so aparece em tela muito depois do boot).
                return null;
            }
            try
            {
                string medido;
                if (ValoresPendentesDeMedicao.TryGetValue(NomeModRedemptive, out medido)
                    && !string.IsNullOrEmpty(medido))
                {
                    _notaRedemptive = medido;
                    Marca("Redemptive: valor MEDIDO em jogo usado (placeholder preenchido)");
                    return _notaRedemptive;
                }

                EnemyMod mod = AcharMod(NomeModRedemptive);
                if (mod == null)
                {
                    Marca("Redemptive: o asset do mod nao esta em Game.Instance.EnemyMods — nota qualitativa");
                    _notaRedemptive = NotaRedemptiveQualitativa(null);
                    return _notaRedemptive;
                }

                string numero = TentaNumero(mod);
                if (!string.IsNullOrEmpty(numero))
                {
                    _notaRedemptive = "Heals allies for " + numero + " on death.";
                    return _notaRedemptive;
                }

                string habilidades = HabilidadesDoGatilho(mod);
                _notaRedemptive = NotaRedemptiveQualitativa(habilidades);
                Marca("Redemptive: nota resolvida no runtime (habilidades=" +
                    (string.IsNullOrEmpty(habilidades) ? "(nenhuma)" : habilidades) + ")");
                return _notaRedemptive;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[PassivaInimigo BT-18] resolucao do Redemptive falhou "
                    + "(texto do jogo intacto): " + ex.GetType().Name + ": " + ex.Message);
                return null;
            }
        }

        /// <summary>
        /// A explicacao QUALITATIVA do Redemptive (quando nao ha numero provado). Ela NAO inventa
        /// valor: diz de onde a cura vem (§5) — a habilidade que o gatilho conjura — e que o quanto
        /// nao e um numero fixo. Com as habilidades lidas do asset, elas saem nomeadas.
        /// </summary>
        private static string NotaRedemptiveQualitativa(string habilidades)
        {
            if (string.IsNullOrEmpty(habilidades))
            {
                return "On death it heals nearby allies; the amount is not stored with this passive, "
                    + "it comes from the ability this enemy casts when it dies.";
            }
            return "On death it casts " + habilidades + ", so the amount healed follows that ability "
                + "and is not a fixed value.";
        }

        /// <summary>
        /// O asset do mod pelo `name` na lista CARREGADA do jogo (`Game.Instance.EnemyMods` =
        /// `Resources.LoadAll&lt;EnemyMod&gt;("Enemy Mods")`, §3.1). Nao e lista digitada: e o proprio
        /// asset. null quando o mod nao existe neste build.
        /// </summary>
        private static EnemyMod AcharMod(string nome)
        {
            EnemyMod[] mods = Burst2Flame.Game.Instance != null
                ? Burst2Flame.Game.Instance.EnemyMods : null;
            if (mods == null)
            {
                return null;
            }
            foreach (EnemyMod mod in mods)
            {
                if (mod != null && string.Equals(mod.name, nome, StringComparison.Ordinal))
                {
                    return mod;
                }
            }
            return null;
        }

        /// <summary>
        /// As habilidades que os `skillTriggers` do mod referenciam, LIDAS AO VIVO do asset (§5:
        /// `Actions` -> Mass Cure/Holy Ground): nomes das `Actions` e dos `ActionStatuses`. A lista
        /// NAO esta digitada — sai do asset carregado; vazia->null (sem prova, sem nome).
        /// </summary>
        private static string HabilidadesDoGatilho(EnemyMod mod)
        {
            List<string> nomes = new List<string>();
            try
            {
                if (mod.skillTriggers == null)
                {
                    return null;
                }
                foreach (SkillTrigger gatilho in mod.skillTriggers)
                {
                    if (gatilho == null)
                    {
                        continue;
                    }
                    if (gatilho.Actions != null)
                    {
                        foreach (ActionInfo acao in gatilho.Actions)
                        {
                            if (acao != null && !string.IsNullOrEmpty(acao.name))
                            {
                                AdicionarUnico(nomes, acao.name);
                            }
                        }
                    }
                    if (gatilho.ActionStatuses != null)
                    {
                        foreach (ActionStatusInfo status in gatilho.ActionStatuses)
                        {
                            if (status != null && !string.IsNullOrEmpty(status.name))
                            {
                                AdicionarUnico(nomes, status.name);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[PassivaInimigo BT-18] leitura das habilidades do gatilho "
                    + "falhou: " + ex.GetType().Name + ": " + ex.Message);
                return null;
            }
            return nomes.Count == 0 ? null : string.Join(", ", nomes.ToArray());
        }

        /// <summary>
        /// ONDA 2 — tentativa de NUMERO em runtime, por `Game.Eval&lt;float&gt;` sobre as expressoes
        /// numericas dos efeitos do gatilho, com `Source` = o personagem CARREGADOR do mod (o
        /// receptor da tooltip, `ShrineAuraPatch.ReceptorDaTooltip`). Duas guardas para NAO mostrar
        /// numero errado:
        ///   (a) o receptor tem de REALMENTE carregar o mod (`Carrega`) — sem isso o `Source` seria
        ///       outro personagem e a conta sairia errada;
        ///   (b) a expressao tem de ser NUMERICA (sem `=`): o que os efeitos do asset guardam com
        ///       mais frequencia sao ATRIBUICOES (`TargetStored['Healing'] = ...`, §5), e avaliar uma
        ///       atribuicao como float devolveria um numero sem significado — esse caso, de proposito,
        ///       NAO vira valor (o numero vai para a medicao em jogo, na tabela de placeholder).
        /// Devolve null quando nao ha numero provado.
        /// </summary>
        private static string TentaNumero(EnemyMod mod)
        {
            Character receptor = ShrineAuraPatch.ReceptorDaTooltip();
            if (receptor == null || !Carrega(mod, receptor))
            {
                Marca("Redemptive: sem numero — nenhum personagem EM FOCO carrega o mod (Source incerto)");
                return null;
            }
            try
            {
                foreach (string expressao in ExpressoesNumericas(mod))
                {
                    float valor;
                    if (Burst2Flame.Game.TryEval<float>(expressao,
                        new GameFunctionParameters { Source = receptor }, out valor)
                        && valor > 0f && !float.IsNaN(valor) && !float.IsInfinity(valor))
                    {
                        Marca("Redemptive: numero resolvido pela expressao '" + expressao + "' = "
                            + valor.ToString("0.#", CultureInfo.InvariantCulture));
                        return valor.ToString("0.#", CultureInfo.InvariantCulture);
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[PassivaInimigo BT-18] avaliacao numerica do Redemptive falhou "
                    + "(sem numero): " + ex.GetType().Name + ": " + ex.Message);
            }
            return null;
        }

        /// <summary>As expressoes NUMERICAS (sem `=`) dos efeitos das acoes do gatilho — nunca uma
        /// atribuicao (§5). Lista vazia = nenhuma candidata.</summary>
        private static IEnumerable<string> ExpressoesNumericas(EnemyMod mod)
        {
            List<string> expressoes = new List<string>();
            if (mod.skillTriggers == null)
            {
                return expressoes;
            }
            foreach (SkillTrigger gatilho in mod.skillTriggers)
            {
                if (gatilho == null || gatilho.Actions == null)
                {
                    continue;
                }
                foreach (ActionInfo acao in gatilho.Actions)
                {
                    if (acao == null || acao.Effects == null)
                    {
                        continue;
                    }
                    foreach (IEffectInfo efeito in acao.Effects)
                    {
                        GeneralEffect ge = efeito as GeneralEffect;
                        if (ge == null || string.IsNullOrEmpty(ge.Action))
                        {
                            continue;
                        }
                        // `=` presente -> ATRIBUICAO (ex.: `TargetStored['Healing'] = ...`): nao e um
                        // numero e NAO entra (avaliar devolveria lixo). Só a expressao numerica pura
                        // e candidata.
                        if (ge.Action.IndexOf('=') < 0)
                        {
                            expressoes.Add(ge.Action);
                        }
                    }
                }
            }
            return expressoes;
        }

        /// <summary>O receptor carrega ESTE mod? (`Character.EnemyMods`, a lista viva do motor —
        /// §3.1). Falha de leitura = false (conservador: sem prova, nao avalia).</summary>
        private static bool Carrega(EnemyMod mod, Character personagem)
        {
            try
            {
                List<EnemyMod> mods = personagem.EnemyMods;
                if (mods == null)
                {
                    return false;
                }
                foreach (EnemyMod m in mods)
                {
                    if (m == null)
                    {
                        continue;
                    }
                    if (ReferenceEquals(m, mod) || string.Equals(m.name, mod.name, StringComparison.Ordinal))
                    {
                        return true;
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("[PassivaInimigo BT-18] leitura de Character.EnemyMods falhou "
                    + "(sem numero): " + ex.GetType().Name + ": " + ex.Message);
            }
            return false;
        }

        private static void AdicionarUnico(List<string> nomes, string nome)
        {
            if (!nomes.Contains(nome))
            {
                nomes.Add(nome);
            }
        }

        // ------------------------------------------------------------------------- LOG

        /// <summary>Marcador de vida: a PRIMEIRA chamada que passa dos early-returns (ou seja, que
        /// casou uma descricao) sai no log — um boot em que nada casou vira indistinguivel de "mod
        /// morto" sem esta linha (regra do projeto, §8.3).</summary>
        private static bool _vivo;

        private static void MarcaVivo()
        {
            if (_vivo)
            {
                return;
            }
            _vivo = true;
            Plugin.Log.LogInfo("BetterTooltips: [PassivaInimigo BT-18] gancho vivo — 1a descricao de "
                + "passive de inimigo reconhecida (nota pronta para anexar)");
        }

        /// <summary>Loga cada combinacao UMA vez (o funil roda em todo texto do jogo).</summary>
        private static readonly HashSet<string> _marcas = new HashSet<string>();

        private static void Marca(string linha)
        {
            try
            {
                if (_marcas.Count >= 200 || !_marcas.Add(linha))
                {
                    return;
                }
                Plugin.Log.LogInfo("[PassivaInimigo BT-18] " + linha);
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }

        /// <summary>Falha IGNORADA no gancho: registrada UMA vez por motivo, o texto do jogo intacto.</summary>
        private static readonly HashSet<string> _falhasRegistradas = new HashSet<string>();

        internal static void RegistrarFalhaIgnorada(string gancho, Exception e)
        {
            try
            {
                string motivo = gancho + " | " + e.GetType().FullName + ": " + e.Message;
                if (_falhasRegistradas.Count >= 25 || !_falhasRegistradas.Add(motivo))
                {
                    return;
                }
                Plugin.Log.LogError("BetterTooltips: falha IGNORADA em " + gancho
                    + " (texto do jogo mantido intacto) — " + motivo);
            }
            catch
            {
                // nem o proprio log pode derrubar o jogo
            }
        }

        // ------------------------------------------------------------------ OS DOIS GANCHOS

        /// <summary>
        /// Gancho A — o FUNIL (`OptionsManager.Localize`), o MESMO alvo do `LocalizePatch` (mesmo
        /// padrao da l.19-20 de la). So age quando o texto exibido e o INGLES ORIGINAL
        /// (`__result == original`) — em outro idioma a descricao vem traduzida e nos NAO a
        /// tocamos (mesma regra do `LocalizePatch.AplicarNotasDoFunil`). A nota entra no `__result`,
        /// que ja e o que o `ExamineWindow` entrega ao `ShowUniversalTooltip`.
        /// </summary>
        [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
        internal static class LocalizePassivaInimigo
        {
            [HarmonyPostfix]
            private static void Postfix(string original, ref string __result)
            {
                try
                {
                    if (!string.Equals(__result, original, StringComparison.Ordinal))
                    {
                        return;
                    }
                    string novo = TentaAnexar(__result, original);
                    if (novo != null)
                    {
                        __result = novo;
                    }
                }
                catch (Exception e)
                {
                    RegistrarFalhaIgnorada("postfix de Localize (passive de inimigo)", e);
                }
            }
        }

        /// <summary>
        /// Gancho B — o PROPRIO tooltip (`Tooltip.ShowUniversalTooltip`, decompilado l.334459), o
        /// metodo que o link de passive de inimigo chama (l.105319). REDE de seguranca: se a
        /// descricao chegou aqui sem passar pelo funil (ou com o gancho A fora), a nota entra do
        /// mesmo jeito. Idempotente — quando o gancho A ja anexou, `NotaDe` nao reconhece o texto
        /// (ele deixou de ser a chave exata) e nada e feito: NUNCA duplica.
        ///
        /// Alvo por ASSINATURA EXPLICITA (6 tipos, na ordem), nunca por "o primeiro metodo com esse
        /// nome": e a regra do projeto (a mesma do `ShrineAuraPatch`/`CorEOrdemDoTooltip`). O
        /// parametro e lido por NOME (`ref string description`), nunca por `__N`.
        /// </summary>
        [HarmonyPatch(typeof(Tooltip), nameof(Tooltip.ShowUniversalTooltip), new Type[]
        {
            typeof(string),                 // __0 title
            typeof(string),                 // __1 subtitle
            typeof(string),                 // __2 description  <- o corpo que a nota reescreve
            typeof(Vector3?),               // __3 targetPos
            typeof(ControlGlyphInfo?),      // __4 controlGlyphInfo
            typeof(string)                  // __5 footerText
        })]
        internal static class UniversalTooltipPassivaInimigo
        {
            [HarmonyPostfix]
            private static void Postfix(ref string description)
            {
                try
                {
                    string novo = TentaAnexar(description, description);
                    if (novo != null)
                    {
                        description = novo;
                    }
                }
                catch (Exception e)
                {
                    RegistrarFalhaIgnorada("postfix de Tooltip.ShowUniversalTooltip (passive de inimigo)", e);
                }
            }
        }
    }
}
