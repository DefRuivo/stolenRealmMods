using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// RV-49 (06/10) - MEDICAO EM JOGO DO `Source["ShrineEffectBonus"]` DO DANO DO FLAME SHRINE.
    /// Cartao: t_126adeca. Pergunta da auditoria RV-19 §9(ii) / RV-22: no dano de RETORNO do
    /// Flame, o fator `(1 + Source["ShrineEffectBonus"]/100)` le o bonus de QUEM?
    ///
    /// O QUE JA ESTA PROVADO DO CODIGO (nao repetido aqui): a formula vive no efeito da ACAO
    /// `Flame Aura Proc` e e `Mathf.Max(1, Mathf.Round(Target["MaxHealth"] * pct * (1 +
    /// Source["ShrineEffectBonus"]/100)))`, com `pct` vindo de `GetValueByEnemyType`
    /// (2,5/8/10/12/14/5 % para boss/champion/elite/soldier/fodder/jogador). O que NAO esta
    /// provado e qual personagem ocupa o slot `Source` no proc REAL - e e isso que este probe
    /// mede, sem inferir nada: tudo o que sai no log foi lido do objeto do jogo.
    ///
    /// O QUE O LOG PASSA A TER (prefixo estavel `[FlameRV49]`, um `grep` pega tudo):
    ///  (1) `BOOT` - dump do ASSET pelo runtime: a expressao REAL da acao `* Aura Proc` e TODOS os
    ///      campos do gatilho do status (`TriggerType`, `Condition`, `Targets`, `UseTriggerSource`).
    ///      `UseTriggerSource` + a cadeia do build (`TriggerSource = actionStatus.Source` na criacao
    ///      do status; `character = trigger.UseTriggerSource && trigger.TriggerSource != null ?
    ///      trigger.TriggerSource : this` em `Character.ProcessSkillTriggers`) e o que DECIDE quem
    ///      entra no `Source` do proc.
    ///  (2) `PROC` - todo `Game.EvalVoid` cuja expressao cita `ShrineEffectBonus` (e o funil por onde
    ///      `Character.GetActionDamage` avalia a formula do dano) sai com a expressao e com o
    ///      `Source`/`Target` DO MOTOR: nome, `IsAI`, tipo, time, `MaxHealth` e o
    ///      `ShrineEffectBonus` REAL de cada lado.
    ///  (3) `CRU` - o `[0]` que a expressao acabou de GRAVAR nos dicionarios do motor
    ///      (`FireDamage`/`ShadowDamage`/...), ANTES dos multiplicadores.
    ///  (4) `PCT` - todo `Character.GetValueByEnemyType` (so as duas formulas de shrine o chamam):
    ///      os 6 percentuais, quem chamou e o que voltou.
    ///  (5) `DANO` - o `__result` de `Character.GetActionDamage` (lista de `DamageInstance`:
    ///      `DamageType` + `DamageMin/Max` + `DamageActual`), o dano FINAL do motor.
    ///  (6) `MATRIZ` - contra-prova executada pelo MOTOR, com a MESMA string capturada no boot: a
    ///      expressao reavaliada com o `Source` = o ALVO do proc e o termo `Source["ShrineEffectBonus"]`
    ///      trocado por 0 / 8 (Omnism I) / 20 (Omnism II) / 100 (Horn of Devotion). E a tabela
    ///      "sem Omnism x com Omnism" sem depender de o dono trocar de equipamento; a linha do proc
    ///      REAL (2) diz qual das duas pontas o jogo usa de verdade. NENHUM personagem e alterado:
    ///      a matriz usa dicionarios `SourceStored`/`TargetStored` NOVOS, so le o resultado, e
    ///      devolve `Game.CurrentGameFunctionParameters` ao valor de antes.
    ///
    /// REGRA DO PROJETO: nada aqui estima valor. Leitura que falha vira marcador `!erro:<Tipo>` no
    /// proprio campo; o probe nunca altera gameplay (o unico estado que ele cria e local).
    /// </summary>
    internal static class FlameProbe
    {
        internal const string Tag = "[FlameRV49]";
        internal const string Atributo = "ShrineEffectBonus";
        internal const string StatusFlame = "Flame Shrine Aura";
        internal const string StatusDecay = "Decay Shrine Aura";

        private static bool _bootFeito;
        private static int _bootEstavel;
        private static int _bootUltimo = -1;
        private static int _bootTentativas;

        private static bool _emMatriz;
        private static readonly HashSet<string> _textosRegistrados = new HashSet<string>();

        /// <summary>Estamos dentro da matriz? (guarda de reentrancia: a matriz chama `Game.EvalVoid`,
        /// que e o proprio metodo ganchado.)</summary>
        internal static bool EmMatriz => _emMatriz;

        /// <summary>A expressao e do fator do shrine? (so ela dispara o probe; o resto do jogo nao.)</summary>
        internal static bool Interessa(string expressao)
        {
            return !string.IsNullOrEmpty(expressao) && expressao.IndexOf(Atributo, StringComparison.Ordinal) >= 0;
        }

        internal static void Marca(string linha)
        {
            try
            {
                Plugin.Log.LogInfo(Tag + " " + linha);
            }
            catch (Exception)
            {
                // log de diagnostico: falhar aqui nao pode derrubar o jogo
            }
        }

        internal static void Aviso(string linha)
        {
            try
            {
                Plugin.Log.LogWarning(Tag + " " + linha);
            }
            catch (Exception)
            {
            }
        }

        // ------------------------------------------------------------------ leitura segura

        internal static string Limpa(string s) => EfeitosInfo.Limpa(s);

        private static string Seguro(string rotulo, Func<string> leitura)
        {
            try
            {
                return leitura() ?? "(vazio)";
            }
            catch (Exception ex)
            {
                return "!erro:" + ex.GetType().Name;
            }
        }

        internal static string NomeDe(Character c)
        {
            return Seguro("nome", () =>
            {
                string n = c.CharacterName;
                return string.IsNullOrEmpty(n) ? "(sem nome)" : n;
            });
        }

        internal static string TipoDe(Character c)
        {
            return Seguro("tipo", () => c.IsAI ? c.EnemyType.ToString() : "player");
        }

        /// <summary>O `ShrineEffectBonus` REAL do personagem. O indexador LANCA para nome desconhecido
        /// (atributo ausente no build), entao a leitura e guardada com o mesmo criterio do BetterTooltips:
        /// so le depois de `Game.Instance.GetAttribute(Atributo) != null`.</summary>
        internal static string BonusDe(Character c)
        {
            return Seguro("bonus", () =>
            {
                if (c == null)
                {
                    return "(sem personagem)";
                }
                if (Game.Instance == null || Game.Instance.GetAttribute(Atributo) == null)
                {
                    return "(atributo ausente neste build)";
                }
                return c[Atributo].ToString("0.###");
            });
        }

        internal static string Descreve(Character c)
        {
            if (c == null)
            {
                return "(null)";
            }
            var sb = new StringBuilder();
            sb.Append("'").Append(NomeDe(c)).Append("'");
            sb.Append(" IsAI=").Append(Seguro("isai", () => c.IsAI ? "sim" : "nao"));
            sb.Append(" tipo=").Append(TipoDe(c));
            sb.Append(" time=").Append(Seguro("time", () => c.TeamIndex.ToString()));
            sb.Append(" id=").Append(Seguro("id", () => c.ID.ToString()));
            sb.Append(" MaxHealth=").Append(Seguro("maxhealth", () => c.MaxHealth.ToString("0.#")));
            sb.Append(" ShrineEffectBonus=").Append(BonusDe(c));
            sb.Append(" info=").Append(Seguro("info", () => c.CharacterInfo == null ? "(sem CharacterInfo)" : c.CharacterInfo.name));
            return sb.ToString();
        }

        // ------------------------------------------------------------------ dicionarios do motor

        private static readonly string[] ChavesDeDano =
        {
            "FireDamage", "ShadowDamage", "ColdDamage", "LightningDamage",
            "PhysicalDamage", "HolyDamage", "Healing", "HealingForced", "ManaDamage"
        };

        /// <summary>Le (sem inserir chave nova) os valores que a expressao gravou nos dicionarios do
        /// motor. `SimpleDefaultDictionary` INSERE a chave na LEITURA, por isso a leitura passa por
        /// `ContainsKey` primeiro: nada e criado no dicionario do jogo por causa do log.</summary>
        private static void AnexaCrus(StringBuilder sb, string rotulo, SimpleDefaultDictionary<string, float> dic)
        {
            if (dic == null)
            {
                return;
            }
            foreach (string chave in ChavesDeDano)
            {
                try
                {
                    if (dic.ContainsKey(chave))
                    {
                        sb.Append(" ").Append(rotulo).Append("[").Append(chave).Append("]=")
                          .Append(dic[chave].ToString("0.####"));
                    }
                }
                catch (Exception ex)
                {
                    sb.Append(" ").Append(rotulo).Append("[").Append(chave).Append("]=!erro:")
                      .Append(ex.GetType().Name);
                }
            }
        }

        internal static string Crus(GameFunctionParameters p)
        {
            var sb = new StringBuilder();
            AnexaCrus(sb, "TargetStored", p.TargetStored);
            AnexaCrus(sb, "SourceStored", p.SourceStored);
            return sb.Length == 0 ? "(nenhuma chave de dano gravada)" : sb.ToString().Trim();
        }

        // ------------------------------------------------------------------ matriz (contra-prova)

        /// <summary>So aceita a forma em que a UNICA atribuicao e a propria chave do dicionario
        /// (`TargetStored["X"] = ...` / `SourceStored["X"] = ...`). Assim a matriz pode reavaliar a
        /// string sem risco de escrever em personagem: as atribuicoes do motor vao para o dicionario
        /// NOVO que a matriz monta.</summary>
        private static bool FormaSegura(string expressao, out bool gravaNoTarget, out string chave)
        {
            gravaNoTarget = true;
            chave = null;
            if (string.IsNullOrEmpty(expressao))
            {
                return false;
            }
            const string alvo = "TargetStored[\"";
            const string fonte = "SourceStored[\"";
            int corte;
            if (expressao.StartsWith(alvo, StringComparison.Ordinal))
            {
                corte = alvo.Length;
            }
            else if (expressao.StartsWith(fonte, StringComparison.Ordinal))
            {
                gravaNoTarget = false;
                corte = fonte.Length;
            }
            else
            {
                return false;
            }
            int fim = expressao.IndexOf("\"] = ", corte, StringComparison.Ordinal);
            if (fim < 0)
            {
                return false;
            }
            // Exatamente UMA atribuicao, e ela e a do inicio (a do dicionario).
            if (Conta(expressao, "\"] = ") != 1)
            {
                return false;
            }
            chave = expressao.Substring(corte, fim - corte);
            return !string.IsNullOrEmpty(chave);
        }

        private static int Conta(string texto, string trecho)
        {
            int n = 0;
            int i = texto.IndexOf(trecho, StringComparison.Ordinal);
            while (i >= 0)
            {
                n++;
                i = texto.IndexOf(trecho, i + trecho.Length, StringComparison.Ordinal);
            }
            return n;
        }

        /// <summary>Pre-registra a string no guard de aviso do cache do jogo
        /// (`CompiledDynamicExpresso.MissingExpressions`, campo privado estatico), para a string nova
        /// da matriz nao imprimir uma linha `No Compiled Expression` por sessao. O valor nao muda: quem
        /// resolve a expressao e o OUTRO cache (`CompiledExpressions`) e, faltando la, o interpretador.
        /// Falha de reflexao = nada suprimido (o aviso volta como era), nenhuma excecao sai daqui.</summary>
        private static void RegistrarTexto(string expressao)
        {
            if (!_textosRegistrados.Add(expressao))
            {
                return;
            }
            try
            {
                Type tipo = typeof(Game).Assembly.GetType("CompiledDynamicExpresso")
                    ?? typeof(Game).Assembly.GetType("Burst2Flame.CompiledDynamicExpresso");
                FieldInfo campo = tipo?.GetField("MissingExpressions", BindingFlags.Static | BindingFlags.NonPublic);
                var avisos = campo?.GetValue(null) as HashSet<string>;
                if (avisos != null)
                {
                    avisos.Add(expressao);
                }
            }
            catch (Exception)
            {
            }
        }

        internal static void Matriz(string expressao, GameFunctionParameters parameters)
        {
            if (_emMatriz)
            {
                return;
            }
            try
            {
                bool gravaNoTarget;
                string chave;
                if (!FormaSegura(expressao, out gravaNoTarget, out chave))
                {
                    Marca("MATRIZ pulada: a expressao nao tem a forma segura 'Stored[\"X\"] = <RHS>' "
                        + "(uma atribuicao, no inicio) - nada foi reavaliado.");
                    return;
                }
                Character alvo = parameters.Target;
                if (alvo == null)
                {
                    Marca("MATRIZ pulada: o proc nao trouxe `Target` (sem personagem para a contra-prova).");
                    return;
                }
                Marca("MATRIZ inicio: Source = o ALVO do proc (" + NomeDe(alvo) + ", ShrineEffectBonus real="
                    + BonusDe(alvo) + "), chave='" + chave + "', gravada em "
                    + (gravaNoTarget ? "TargetStored" : "SourceStored"));

                string semFator = "Source[\"" + Atributo + "\"]";
                if (expressao.IndexOf(semFator, StringComparison.Ordinal) < 0)
                {
                    Marca("MATRIZ: a expressao nao cita " + semFator + " - contra-prova nao se aplica.");
                    return;
                }

                var variantes = new List<KeyValuePair<string, float?>>();
                variantes.Add(new KeyValuePair<string, float?>("bonus do proprio alvo (substituicao NENHUMA)",
                    null));
                variantes.Add(new KeyValuePair<string, float?>("bonus=0 (sem Omnism)", 0f));
                variantes.Add(new KeyValuePair<string, float?>("bonus=8 (Omnism I)", 8f));
                variantes.Add(new KeyValuePair<string, float?>("bonus=20 (Omnism II)", 20f));
                variantes.Add(new KeyValuePair<string, float?>("bonus=100 (Horn of Devotion)", 100f));

                var guardados = new List<string>();
                _emMatriz = true;
                GameFunctionParameters guardado = Game.CurrentGameFunctionParameters;
                try
                {
                    foreach (var variante in variantes)
                    {
                        string texto = expressao;
                        if (variante.Value.HasValue)
                        {
                            texto = expressao.Replace(semFator, "(" + variante.Value.Value.ToString("0.###") + ")");
                            RegistrarTexto(texto);
                        }
                        var p = parameters;
                        p.Source = alvo;
                        p.SourceStored = new SimpleDefaultDictionary<string, float>(new Dictionary<string, float>());
                        p.TargetStored = new SimpleDefaultDictionary<string, float>(new Dictionary<string, float>());
                        Game.EvalVoid(texto, p);
                        var dic = gravaNoTarget ? p.TargetStored : p.SourceStored;
                        string valor;
                        try
                        {
                            valor = (dic != null && dic.ContainsKey(chave)) ? dic[chave].ToString("0.####") : "!ausente";
                        }
                        catch (Exception ex)
                        {
                            valor = "!erro:" + ex.GetType().Name;
                        }
                        guardados.Add("MATRIZ '" + variante.Key + "' -> " + chave + "=" + valor);
                    }
                }
                finally
                {
                    Game.CurrentGameFunctionParameters = guardado;
                    _emMatriz = false;
                }

                foreach (string linha in guardados)
                {
                    Marca(linha);
                }
                Marca("MATRIZ fim (Source = " + NomeDe(alvo) + "; MaxHealth do alvo depois de tudo="
                    + Seguro("maxhealth", () => alvo.MaxHealth.ToString("0.#")) + ")");
            }
            catch (Exception ex)
            {
                _emMatriz = false;
                Aviso("MATRIZ falhou (" + ex.GetType().Name + "): " + ex.Message);
            }
        }

        // ------------------------------------------------------------------ dump de boot

        /// <summary>Despeja, UMA vez por sessao, o asset VIVO das duas auras de perigo: a expressao
        /// REAL da acao `* Aura Proc` (pelo `Effects[]` do proprio asset, por reflexao como o
        /// EfeitosInfo) e os campos do gatilho do status. E este dump que diz se o `Source` do proc
        /// e o `this` (o personagem que tomou o golpe) ou o `actionStatus.Source` (o personagem do
        /// SHRINE) - `UseTriggerSource` e o campo que decide.</summary>
        private static void Dump(ActionStatusInfo s)
        {
            if (s == null)
            {
                return;
            }
            Marca("BOOT status '" + Limpa(s.Name) + "' guid=" + Seguro("guid", () => s.Guid.ToString()));
            Marca("BOOT desc='" + Limpa(s.Description ?? "") + "'");
            if (s.DescriptionExpressions != null)
            {
                for (int i = 0; i < s.DescriptionExpressions.Length; i++)
                {
                    Marca("BOOT descExpr[" + i + "]='" + Limpa(s.DescriptionExpressions[i] ?? "") + "'");
                }
            }
            Marca("BOOT efeitos_do_status=" + EfeitosInfo.Descreve(s.Effects));

            var gatilhos = s.SkillTriggers;
            if (gatilhos == null || gatilhos.Length == 0)
            {
                Marca("BOOT gatilhos=NENHUM no status (a acao do proc nao sai por aqui)");
            }
            else
            {
                for (int i = 0; i < gatilhos.Length; i++)
                {
                    SkillTrigger tg = gatilhos[i];
                    if (tg == null)
                    {
                        continue;
                    }
                    Marca("BOOT gatilho[" + i + "] triggerType=" + (int)tg.TriggerType + " (" + tg.TriggerType
                        + ") condition='" + Limpa(tg.Condition ?? "") + "' alvos='" + Limpa(tg.Targets ?? "")
                        + "' useTriggerSource=" + Seguro("uts", () => tg.UseTriggerSource ? "SIM" : "nao")
                        + " triggerSource=" + (tg.TriggerSource == null ? "(null)" : Descreve(tg.TriggerSource))
                        + " cd=" + Seguro("cd", () => tg.Cooldown.ToString("0.#"))
                        + " maxUses='" + Limpa(tg.MaxNumUses ?? "") + "'");
                    Marca("BOOT gatilho[" + i + "] generalEffects=" + EfeitosInfo.Descreve(tg.GeneralEffects));
                    if (tg.Actions != null)
                    {
                        for (int a = 0; a < tg.Actions.Length; a++)
                        {
                            ActionInfo ac = tg.Actions[a];
                            if (ac == null)
                            {
                                continue;
                            }
                            Marca("BOOT acao[" + a + "] '" + Limpa(ac.name) + "' useCondition='"
                                + Limpa(ac.UseCondition ?? "") + "'");
                            Marca("BOOT acao[" + a + "] efeitos=" + EfeitosInfo.Descreve(ac.Effects));
                            if (ac.DescriptionExpressions != null)
                            {
                                for (int d = 0; d < ac.DescriptionExpressions.Length; d++)
                                {
                                    Marca("BOOT acao[" + a + "] descExpr[" + d + "]='"
                                        + Limpa(ac.DescriptionExpressions[d] ?? "") + "'");
                                }
                            }
                        }
                    }
                }
            }
        }

        /// <summary>O ASSET do ground effect da familia `Flame Shrine` (o gerador da aura): e ele que diz
        /// PARA QUEM a aura vai (players x inimigos) e qual personagem o ground effect usa como `Source`.
        /// Sem isso a receita de jogo ficaria no chute: quem precisa TOMAR o golpe para o gatilho
        /// `OnGettingHitDamaging` disparar e exatamente quem carrega o status da aura.</summary>
        private static void DumpGroundEffectsDeShrine()
        {
            try
            {
                if (Game.Instance == null || Game.Instance.GroundEffects == null)
                {
                    Marca("BOOT ground effects: lista indisponivel");
                    return;
                }
                var lista = Game.Instance.GroundEffects;
                Marca("BOOT ground effects carregados=" + lista.Count);
                var naoShrines = new StringBuilder();
                foreach (GroundEffectInfo ge in new List<GroundEffectInfo>(lista))
                {
                    if (ge == null)
                    {
                        continue;
                    }
                    string nomeAsset = Seguro("nome_asset", () => ge.name);
                    string tipo = Seguro("tipo_ge", () => ge.GroundEffectType.ToString());
                    if (tipo != "Shrine")
                    {
                        naoShrines.Append(nomeAsset).Append("(").Append(tipo).Append(") ");
                        continue;
                    }
                    string nomeCampo = Seguro("nome_campo", () => ge.Name ?? "(sem Name)");
                    Marca("BOOT GE '" + nomeAsset + "' campo='" + nomeCampo + "' tipo=" + tipo);
                    Marca("BOOT GE '" + nomeAsset + "' raio=" + Seguro("raio", () => ge.Radius.ToString())
                        + " alvos_enemy=" + Seguro("ae", () => ge.GroundTargets.EffectsEnemies ? "SIM" : "nao")
                        + " alvos_player=" + Seguro("ap", () => ge.GroundTargets.EffectsPlayers ? "SIM" : "nao")
                        + " ignora_summons=" + Seguro("is", () => ge.GroundTargets.IgnorePlayerSummons ? "SIM" : "nao")
                        + " targetingComplexo=" + Seguro("tc", () => ge.UseComplexTargeting ? "SIM" : "nao")
                        + " targetConditions='" + Seguro("tcond", () => ge.GroundTargetConditions ?? "") + "'");
                    Marca("BOOT GE '" + nomeAsset + "' expira=" + Seguro("exp", () => ge.CanExpire ? "SIM" : "nao")
                        + " turnos=" + Seguro("turnos", () => ge.TurnsToExpire.ToString())
                        + " charInfo=" + Seguro("ci", () => ge.CharacterInfo == null ? "(sem CharacterInfo)" : ge.CharacterInfo.name)
                        + " nStatuses=" + Seguro("ns", () => ge.ActionStatuses == null ? "0" : ge.ActionStatuses.Length.ToString())
                        + " nTriggers=" + Seguro("nt", () => ge.SkillTriggers == null ? "0" : ge.SkillTriggers.Length.ToString()));
                    if (ge.ActionStatuses != null)
                    {
                        var nomes = new StringBuilder();
                        foreach (ActionStatusInfo s in ge.ActionStatuses)
                        {
                            if (s == null)
                            {
                                continue;
                            }
                            nomes.Append(Limpa(s.Name)).Append("; ");
                        }
                        Marca("BOOT GE '" + nomeAsset + "' statuses=" + nomes.ToString().TrimEnd(' ', ';'));
                    }
                    // O personagem do SHRINE nasce sem bonus? Le o CharacterEffects do proprio asset.
                    try
                    {
                        if (ge.CharacterInfo != null && ge.CharacterInfo.CharacterEffects != null)
                        {
                            var sb = new StringBuilder();
                            foreach (CharacterEffectInfo ef in ge.CharacterInfo.CharacterEffects)
                            {
                                if (ef == null)
                                {
                                    continue;
                                }
                                sb.Append(Limpa(ef.CharacterAttribute == null ? "(sem atributo)"
                                        : ef.CharacterAttribute.name))
                                  .Append("=").Append(Limpa(ef.Amount ?? "")).Append("; ");
                            }
                            Marca("BOOT GE '" + nomeAsset + "' charInfo.CharacterEffects="
                                + (sb.Length == 0 ? "(vazio)" : sb.ToString().TrimEnd(' ', ';')));
                        }
                    }
                    catch (Exception ex)
                    {
                        Marca("BOOT GE '" + nomeAsset + "' CharacterEffects=!erro:" + ex.GetType().Name);
                    }
                }
                if (naoShrines.Length > 0)
                {
                    Marca("BOOT ground effects NAO-shrine: " + naoShrines.ToString().TrimEnd());
                }
            }
            catch (Exception ex)
            {
                Aviso("BOOT ground effects falhou (" + ex.GetType().Name + "): " + ex.Message);
            }
        }

        internal static void TentarBoot(List<ActionStatusInfo> lista)
        {
            if (_bootFeito || lista == null)
            {
                return;
            }
            try
            {
                // O jogo popula os status incrementalmente no loading: despeja com o tamanho estavel.
                if (lista.Count == _bootUltimo)
                {
                    _bootEstavel++;
                }
                else
                {
                    _bootEstavel = 1;
                    _bootUltimo = lista.Count;
                }
                _bootTentativas++;
                if (_bootEstavel < 5)
                {
                    return;
                }
                if (lista.Count < 2)
                {
                    return;
                }
                _bootFeito = true;
                Marca("BOOT status carregados=" + lista.Count + " atributo '" + Atributo + "' no build="
                    + Seguro("attr", () => (Game.Instance != null && Game.Instance.GetAttribute(Atributo) != null)
                        ? "SIM" : "NAO"));
                var copia = new List<ActionStatusInfo>(lista);
                ActionStatusInfo flame = null;
                ActionStatusInfo decay = null;
                foreach (ActionStatusInfo s in copia)
                {
                    if (s == null)
                    {
                        continue;
                    }
                    if (flame == null && s.Name == StatusFlame)
                    {
                        flame = s;
                    }
                    if (decay == null && s.Name == StatusDecay)
                    {
                        decay = s;
                    }
                }
                if (flame == null)
                {
                    Aviso("BOOT status '" + StatusFlame + "' NAO esta na lista de " + lista.Count
                        + " status deste build - sem dump do gatilho (a medicao do proc continua valendo)");
                }
                Dump(flame);
                Dump(decay);
                DumpGroundEffectsDeShrine();
                Marca("BOOT os alvos da acao citam 'Target.GetValueByEnemyType' e o fator lê 'Source["
                    + Atributo + "]' - quem ocupa o Source do PROC REAL sai nas linhas PROC abaixo");
            }
            catch (Exception ex)
            {
                _bootFeito = true;
                Aviso("BOOT dump falhou (" + ex.GetType().Name + "): " + ex.Message);
            }
        }
    }

    /// <summary>O dump de boot sai pelo MESMO getter que o inventario de status usa (o jogo popula a
    /// lista por ele). Nao substitui o inventario: e um recorte de 2 status, com os campos que a
    /// pergunta do RV-49 precisa.</summary>
    [HarmonyPatch(typeof(Game), "get_ActionStatuses")]
    public static class FlameBootPatch
    {
        private static void Postfix(List<ActionStatusInfo> __result)
        {
            FlameProbe.TentarBoot(__result);
        }
    }

    /// <summary>O PROC REAL. `Game.EvalVoid` e o funil por onde `Character.GetActionDamage` avalia a
    /// string da formula (decompilado: `Game.EvalVoid(text2, new GameFunctionParameters { Source =
    /// source, Target = target, SourceStored, TargetStored, ... })`). So a expressao que cita
    /// `ShrineEffectBonus` interessa - o resto do jogo nao gera linha nenhuma.</summary>
    [HarmonyPatch(typeof(Game), "EvalVoid")]
    public static class FlameEvalVoidPatch
    {
        private static void Prefix(string expression, GameFunctionParameters parameters, out bool __state)
        {
            __state = !FlameProbe.EmMatriz && FlameProbe.Interessa(expression);
            if (!__state)
            {
                return;
            }
            FlameProbe.Marca("PROC expr='" + FlameProbe.Limpa(expression) + "'");
            FlameProbe.Marca("PROC Source=" + FlameProbe.Descreve(parameters.Source));
            FlameProbe.Marca("PROC Target=" + FlameProbe.Descreve(parameters.Target));
        }

        private static void Postfix(string expression, GameFunctionParameters parameters, bool __state)
        {
            if (!__state)
            {
                return;
            }
            FlameProbe.Marca("CRU " + FlameProbe.Crus(parameters));
            FlameProbe.Matriz(expression, parameters);
        }
    }

    /// <summary>O dano FINAL do motor (antes da mitigacao de armadura/resistencia, que e aplicada
    /// depois): a lista de `DamageInstance` que o jogo vai aplicar.</summary>
    [HarmonyPatch(typeof(Character), "GetActionDamage")]
    public static class FlameGetActionDamagePatch
    {
        private static void Prefix(string actionString, out bool __state)
        {
            __state = !FlameProbe.EmMatriz && FlameProbe.Interessa(actionString);
        }

        private static void Postfix(bool __state, List<DamageInstance> __result, Character source, Character target)
        {
            if (!__state)
            {
                return;
            }
            if (__result == null || __result.Count == 0)
            {
                FlameProbe.Marca("DANO final: NENHUMA instance (expressao sem dano) - fonte="
                    + FlameProbe.NomeDe(source) + " alvo=" + FlameProbe.NomeDe(target));
                return;
            }
            for (int i = 0; i < __result.Count; i++)
            {
                DamageInstance d = __result[i];
                FlameProbe.Marca("DANO final[" + i + "] tipo=" + d.DamageType
                    + " min=" + d.DamageMin.ToString("0.####")
                    + " max=" + d.DamageMax.ToString("0.####")
                    + " ACTUAL=" + d.DamageActual.ToString("0.####")
                    + " crit=" + d.DidCrit
                    + " quem_leva=" + FlameProbe.Descreve(d.DamageTarget));
            }
        }
    }

    /// <summary>O `pct` resolvido. `GetValueByEnemyType` so e chamado pelas DUAS formulas de aura de
    /// perigo (Flame/Decay), entao nao ha spam: cada linha e um pct de proc.</summary>
    [HarmonyPatch(typeof(Character), "GetValueByEnemyType")]
    public static class FlamePctPatch
    {
        private static void Postfix(Character __instance, float boss, float champion, float elite, float soldier,
            float fodder, float player, float __result)
        {
            if (FlameProbe.EmMatriz)
            {
                return;
            }
            FlameProbe.Marca("PCT de " + FlameProbe.Descreve(__instance) + " -> "
                + __result.ToString("0.####") + " (boss=" + boss.ToString("0.####")
                + " champion=" + champion.ToString("0.####") + " elite=" + elite.ToString("0.####")
                + " soldier=" + soldier.ToString("0.####") + " fodder=" + fodder.ToString("0.####")
                + " player=" + player.ToString("0.####") + ")");
        }
    }
}
