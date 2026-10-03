using System;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace BetterCombatText
{
    /// <summary>
    /// Coracao do mod: aplica contorno/halo e sombra em UM componente de texto por vez.
    ///
    /// <para><b>REGRA DE OURO (por que o material tem de ser instanciado):</b> no TextMeshPro o
    /// material da fonte e COMPARTILHADO por todos os textos que usam aquela fonte. Mexer nele
    /// muda a interface inteira. O caminho seguro e <c>TMP_Text.fontMaterial</c>, que devolve uma
    /// COPIA por componente (confirmado no IL: <c>TextMeshProUGUI.GetMaterial(mat)</c> chama
    /// <c>CreateMaterialInstance()</c> -> <c>new Material(source)</c> e grava a copia em
    /// <c>m_sharedMaterial</c> daquele componente apenas — mas so quando o componente AINDA nao tem
    /// instancia propria: com o MESMO InstanceID o TMP REUSA a instancia existente (que pode ser de
    /// outro mod) em vez de clonar; o caso e descrito em <c>DetalharAlvo</c>). <c>fontSharedMaterial</c> JAMAIS e
    /// alterado aqui — ele e so lido, para saber em quem estamos.</para>
    ///
    /// <para><b>Falha-segura:</b> todo caminho tem try/catch; componente nulo, material nulo,
    /// shader que nao seja distance field ou GameObject inesperado resultam em log + nada feito,
    /// nunca em excecao para dentro do jogo.</para>
    /// </summary>
    internal static class TextStyler
    {
        // InstanceID do TMP_Text -> material que NOS instanciamos para ele.
        private static readonly Dictionary<int, Material> MateriaisInstanciados = new Dictionary<int, Material>();
        // InstanceID -> shader ja reportado (evita spam de log a cada frame).
        private static readonly Dictionary<string, string> AvisosDados = new Dictionary<string, string>();
        private static readonly HashSet<int> TextosLegadosTratados = new HashSet<int>();
        // InstanceID -> tamanho de fonte ORIGINAL (para o ajuste ser idempotente).
        private static readonly Dictionary<int, float> TamanhoOriginal = new Dictionary<int, float>();
        private static readonly Dictionary<int, float> TamanhoOriginalLegado = new Dictionary<int, float>();
        // BCT-2: InstanceID -> BALDE da sombra aplicado (true = letra escura -> sombra clara).
        // Serve para a REAVALIACAO SEM RE-INSTANCIAR: o jogo pode REUSAR o mesmo componente com
        // outra cor de letra; so quando o BALDE vira e que a cor da sombra e reescrita.
        private static readonly Dictionary<int, bool> BaldeSombraTmp = new Dictionary<int, bool>();
        private static readonly Dictionary<int, bool> BaldeSombraLegado = new Dictionary<int, bool>();

        private static bool _resumoAplicadoSobreNomes;
        private static bool _resumoAplicadoSobreDado;
        private static readonly HashSet<string> DetalhesDados = new HashSet<string>();
        private static bool _inventarioFeito;

        // ------------------------------------------------------------------
        //  Superficies TMP (distance field): nomes em combate, texto do dado,
        //  (opcional) numero de vida.
        // ------------------------------------------------------------------
        internal static void AplicarTmp(TMP_Text tmp, EstiloTmpCfg cfg, string superficie)
        {
            if (tmp == null)
            {
                return;
            }
            if (!cfg.HaloAtivo.Value && !cfg.SombraAtiva.Value && cfg.TamanhoFonteExtra.Value == 0f)
            {
                return; // nada configurado para esta superficie
            }

            try
            {
                var compartilhadoAntes = tmp.fontSharedMaterial;
                if (compartilhadoAntes == null)
                {
                    AvisoUma(superficie + ":sem-material", $"'{Nome(tmp)}' nao tem fontSharedMaterial; ignorado.");
                    return;
                }

                int id = tmp.GetInstanceID();
                if (MateriaisInstanciados.TryGetValue(id, out var nosso) && nosso != null && nosso == compartilhadoAntes)
                {
                    // REAVALIACAO SEM RE-INSTANCIAR (BCT-2): o componente ja tem a NOSSA
                    // instancia de material, mas o jogo pode REUSA-LO mudando a cor da letra
                    // (o mesmo texto vira fogo e depois gelo). A cada chamada relemos a cor e,
                    // se o BALDE da sombra virou, reescrevemos SO `_UnderlayColor` — sem criar
                    // material novo e sem tocar no contorno/offsets.
                    ReavaliarSombraTmp(tmp, cfg, nosso);
                    return; // ja e a nossa instancia deste componente; nada mais a refazer
                }

                // === INSTANCIA POR COMPONENTE (nunca o material compartilhado) ===
                Material mat = tmp.fontMaterial;
                if (mat == null)
                {
                    AvisoUma(superficie + ":instancia-nula", $"'{Nome(tmp)}': fontMaterial devolveu null; ignorado.");
                    return;
                }
                MateriaisInstanciados[id] = mat;

                var shader = mat.shader;
                string nomeShader = shader != null ? shader.name : "(sem shader)";
                bool ehDistanceField = mat.HasProperty("_OutlineWidth");
                bool temUnderlay = mat.HasProperty("_UnderlaySoftness");

                if (cfg.HaloAtivo.Value)
                {
                    if (ehDistanceField)
                    {
                        mat.EnableKeyword("OUTLINE_ON");
                        mat.SetColor("_OutlineColor", cfg.CorContorno);
                        mat.SetFloat("_OutlineWidth", Mathf.Clamp(cfg.LarguraContorno.Value, 0f, 1f));
                        mat.SetFloat("_OutlineSoftness", Mathf.Clamp(cfg.SuavidadeContorno.Value, 0f, 1f));
                    }
                    else
                    {
                        AvisoUma(superficie + ":bitmap",
                            $"'{Nome(tmp)}' usa o shader '{nomeShader}', que NAO tem _OutlineWidth (fonte bitmap, " +
                            "nao distance field). Halo suave IMPOSSIVEL nesta fonte; nada foi alterado nela.");
                    }
                }

                if (cfg.SombraAtiva.Value)
                {
                    if (temUnderlay)
                    {
                        mat.EnableKeyword("UNDERLAY_ON");
                        mat.SetColor("_UnderlayColor", cfg.CorSombraPara(tmp.color));
                        // BCT-3/BCT-4: o BALDE considera o FUNDO declarado (fundo escuro -> sombra
                        // clara) E a LEI do contraste com a LETRA (o balde VIRA se a cor escolhida
                        // nao contrastar com a letra) - a reavaliacao so reescreve se o balde muda.
                        BaldeSombraTmp[id] = Configuracao.UsaSombraClara(tmp.color, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura, cfg.Fundo);
                        mat.SetFloat("_UnderlayOffsetX", Mathf.Clamp(cfg.SombraOffsetX.Value, -2f, 2f));
                        mat.SetFloat("_UnderlayOffsetY", Mathf.Clamp(cfg.SombraOffsetY.Value, -2f, 2f));
                        mat.SetFloat("_UnderlayDilate", Mathf.Clamp(cfg.SombraDilate.Value, -1f, 1f));
                        mat.SetFloat("_UnderlaySoftness", Mathf.Clamp(cfg.SombraSuavidade.Value, 0f, 1f));
                    }
                    else
                    {
                        AvisoUma(superficie + ":sem-underlay",
                            $"'{Nome(tmp)}' / shader '{nomeShader}' nao expoe _UnderlaySoftness; sombra ignorada.");
                    }
                }

                AplicarTamanho(tmp, cfg.TamanhoFonteExtra.Value, id);

                // O halo/underlay saem para FORA do glifo: sem recalcular o padding o contorno e
                // cortado na borda do mesh. UpdateMeshPadding() resolve (usa GetPadding(material)).
                tmp.UpdateMeshPadding();
                tmp.SetVerticesDirty();
                tmp.SetMaterialDirty();

                if (Plugin.Cfg.LogDetalhado.Value)
                {
                    Plugin.Log.LogInfo(
                        $"[{superficie}] '{Nome(tmp)}' tratado: shader='{nomeShader}' " +
                        $"df={ehDistanceField} halo={(cfg.HaloAtivo.Value ? Part(cfg.LarguraContorno) : "off")} " +
                        $"softness={Part(cfg.SuavidadeContorno)} alfa={Part(cfg.AlfaContorno)} " +
                        $"sombra={(cfg.SombraAtiva.Value ? Part(cfg.AlfaSombra) : "off")}");
                }

                // Resumo unico (sem spam) por familia de superficie.
                ReportarResumo(superficie, nomeShader, cfg, ehDistanceField);
                DetalharAlvo(superficie, tmp, compartilhadoAntes, nomeShader, ehDistanceField);
            }
            catch (Exception e)
            {
                AvisoUma(superficie + ":erro", $"falha ao tratar '{Nome(tmp)}': {e.GetType().Name}: {e.Message}");
            }
        }

        /// <summary>
        /// REAVALIACAO SEM RE-INSTANCIAR (BCT-2), caminho TMP. O componente ja tem a NOSSA
        /// instancia de material; o jogo pode reusa-lo com OUTRA cor de letra. Relemos a cor e,
        /// se o BALDE da sombra mudou, escrevemos SO `_UnderlayColor` na instancia que ja e
        /// nossa — nada de `new Material`, nada de contorno/offset/tamanho. Sombra desligada,
        /// sombra nao-adaptativa, shader sem `_UnderlaySoftness` ou balde igual: nada e escrito
        /// (continua idempotente).
        /// </summary>
        private static void ReavaliarSombraTmp(TMP_Text tmp, EstiloTmpCfg cfg, Material nosso)
        {
            try
            {
                if (!cfg.SombraAtiva.Value || !Plugin.Cfg.SombraAdaptativa.Value)
                {
                    return; // sombra desligada, ou comportamento FIXO antigo: nada acompanha a cor
                }
                if (nosso == null || !nosso.HasProperty("_UnderlaySoftness"))
                {
                    return; // shader sem underlay: nao ha cor de sombra para atualizar
                }

                int id = tmp.GetInstanceID();
                bool balde = Configuracao.UsaSombraClara(tmp.color, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura, cfg.Fundo);
                if (BaldeSombraTmp.TryGetValue(id, out var anterior) && anterior == balde)
                {
                    return; // a letra continua no MESMO balde: a sombra ja esta certa
                }
                BaldeSombraTmp[id] = balde;
                nosso.SetColor("_UnderlayColor", cfg.CorSombraPara(tmp.color));
                tmp.SetMaterialDirty();
            }
            catch (Exception e)
            {
                AvisoUma("reavaliacao-tmp:erro",
                    $"falha ao reavaliar a sombra adaptativa no TMP: {e.GetType().Name}: {e.Message}");
            }
        }

        private static void ReportarResumo(string superficie, string nomeShader, EstiloTmpCfg cfg, bool df)
        {
            bool jaReportou = superficie.Contains("dado") ? _resumoAplicadoSobreDado : _resumoAplicadoSobreNomes;
            if (jaReportou)
            {
                return;
            }
            if (superficie.Contains("dado"))
            {
                _resumoAplicadoSobreDado = true;
            }
            else
            {
                _resumoAplicadoSobreNomes = true;
            }

            Plugin.Log.LogInfo(
                $"[{superficie}] APLICADO em '{superficie}' (material instanciado POR COMPONENTE): " +
                $"shader='{nomeShader}', distance field={df}, contorno={Part(cfg.LarguraContorno)} " +
                $"largura / {Part(cfg.SuavidadeContorno)} softness / cor {cfg.CorContornoHex.Value} " +
                $"alfa {Part(cfg.AlfaContorno)}, sombra={(cfg.SombraAtiva.Value ? "on" : "off")} " +
                $"tamanho={(cfg.TamanhoFonteExtra.Value == 0f ? "intocado" : Part(cfg.TamanhoFonteExtra))}.");
        }

        /// <summary>Ajuste de fonte idempotente: sempre parte do tamanho ORIGINAL do componente.</summary>
        private static void AplicarTamanho(TMP_Text tmp, float extra, int id)
        {
            if (extra == 0f)
            {
                return;
            }
            if (!TamanhoOriginal.TryGetValue(id, out var original))
            {
                original = tmp.fontSize;
                TamanhoOriginal[id] = original;
            }
            tmp.fontSize = original + extra;
        }

        // ------------------------------------------------------------------
        //  Superficie legada (UnityEngine.UI.Text): rotulos de stack/turno.
        // ------------------------------------------------------------------
        internal static void AplicarTextoLegado(Text txt, EstiloTextoLegadoCfg cfg, string superficie)
        {
            if (txt == null)
            {
                return;
            }
            if (!cfg.HaloAtivo.Value && !cfg.SombraAtiva.Value && !cfg.Negrito.Value && cfg.TamanhoExtra.Value == 0f)
            {
                return;
            }

            int id = txt.GetInstanceID();
            try
            {
                if (TextosLegadosTratados.Contains(id))
                {
                    // REAVALIACAO SEM RE-CRIAR (BCT-2): o rotulo legado pode ser REUSADO com
                    // outra cor de letra. Se o BALDE virou, trocamos SO o effectColor do
                    // Shadow — sem AddComponent de novo e sem tocar em contorno/tamanho.
                    ReavaliarSombraLegado(txt, cfg);
                    return;
                }
                TextosLegadosTratados.Add(id);

                // O BaseMeshEffect (Outline/Shadow) age sobre o PRIMEIRO Graphic do GameObject.
                // Se houver outro Graphic antes do Text, o contorno iria para o elemento errado —
                // nesse caso NAO adicionamos nada (regra: so mexer no alvo).
                var graphics = txt.gameObject.GetComponents<Graphic>();
                bool alvoEhPrimeiroGraphic = graphics == null || graphics.Length == 0 || graphics[0] == txt;

                if (cfg.HaloAtivo.Value)
                {
                    if (alvoEhPrimeiroGraphic)
                    {
                        var contorno = txt.gameObject.GetComponent<Outline>();
                        if (contorno == null)
                        {
                            contorno = txt.gameObject.AddComponent<Outline>();
                        }
                        contorno.effectColor = cfg.CorContorno;
                        contorno.effectDistance = new Vector2(cfg.RaioContorno.Value, cfg.RaioContorno.Value);
                        contorno.useGraphicAlpha = true;
                    }
                    else
                    {
                        AvisoUma("rotulos:graphic-antes",
                            $"'{txt.gameObject.name}': ha outro Graphic antes do Text no mesmo objeto; " +
                            "contorno NAO adicionado (mexeria no elemento errado).");
                    }
                }

                if (cfg.SombraAtiva.Value && alvoEhPrimeiroGraphic)
                {
                    var sombra = txt.gameObject.GetComponent<Shadow>();
                    if (sombra == null)
                    {
                        sombra = txt.gameObject.AddComponent<Shadow>();
                    }
                    sombra.effectColor = cfg.CorSombraPara(txt.color);
                    sombra.effectDistance = new Vector2(cfg.SombraOffsetX.Value, cfg.SombraOffsetY.Value);
                    sombra.useGraphicAlpha = true;
                    BaldeSombraLegado[id] = Configuracao.UsaSombraClara(txt.color, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura, cfg.Fundo);
                }

                if (cfg.Negrito.Value)
                {
                    txt.fontStyle |= FontStyle.Bold;
                }

                if (cfg.TamanhoExtra.Value != 0f)
                {
                    if (!TamanhoOriginalLegado.TryGetValue(id, out var original))
                    {
                        original = txt.fontSize;
                        TamanhoOriginalLegado[id] = original;
                    }
                    txt.fontSize = Mathf.Max(1, Mathf.RoundToInt(original + cfg.TamanhoExtra.Value));
                }

                if (Plugin.Cfg.LogDetalhado.Value)
                {
                    Plugin.Log.LogInfo(
                        $"[{superficie}] '{txt.gameObject.name}' tratado (UI.Text legado): " +
                        $"contorno={(cfg.HaloAtivo.Value ? Part(cfg.RaioContorno) : "off")}px alfa={Part(cfg.AlfaContorno)}, " +
                        $"sombra={(cfg.SombraAtiva.Value ? Part(cfg.AlfaSombra) : "off")}, negrito={cfg.Negrito.Value}");
                }
            }
            catch (Exception e)
            {
                AvisoUma(superficie + ":erro", $"falha ao tratar '{txt.gameObject.name}': {e.GetType().Name}: {e.Message}");
            }
        }

        /// <summary>
        /// REAVALIACAO SEM RE-CRIAR (BCT-2), caminho LEGADO (UI.Text). Se o rotulo ja tratado for
        /// REUSADO com outra cor de letra e o BALDE da sombra virar, reescrevemos SO o
        /// `effectColor` do Shadow que ja existe — sem `AddComponent` de novo e sem tocar no
        /// contorno, negrito ou tamanho. Sombra desligada, nao-adaptativa, sem Shadow no objeto
        /// ou balde igual: nada e escrito.
        /// </summary>
        private static void ReavaliarSombraLegado(Text txt, EstiloTextoLegadoCfg cfg)
        {
            try
            {
                if (!cfg.SombraAtiva.Value || !Plugin.Cfg.SombraAdaptativa.Value)
                {
                    return; // sombra desligada, ou comportamento FIXO antigo
                }
                var sombra = txt.gameObject.GetComponent<Shadow>();
                if (sombra == null)
                {
                    return; // nao ha sombra nossa registrada neste objeto
                }

                int id = txt.GetInstanceID();
                bool balde = Configuracao.UsaSombraClara(txt.color, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura, cfg.Fundo);
                if (BaldeSombraLegado.TryGetValue(id, out var anterior) && anterior == balde)
                {
                    return; // a letra continua no MESMO balde
                }
                BaldeSombraLegado[id] = balde;
                sombra.effectColor = cfg.CorSombraPara(txt.color);
                txt.SetVerticesDirty();
            }
            catch (Exception e)
            {
                AvisoUma("reavaliacao-legado:erro",
                    $"falha ao reavaliar a sombra adaptativa no texto legado: {e.GetType().Name}: {e.Message}");
            }
        }

        /// <summary>Marca "esta superficie legada ja foi resolvida" sem depender do InstanceID.</summary>
        private static bool _resumoRotulosFeito;

        internal static void ReportarResumoRotulos()
        {
            if (_resumoRotulosFeito)
            {
                return;
            }
            _resumoRotulosFeito = true;
            var cfg = Plugin.Cfg.Rotulos;
            Plugin.Log.LogInfo(
                "[Rotulos de buff/debuff em combate] APLICADO nos rotulos 'xN' e contador de turnos dos icones " +
                $"de status (props 100% locais do objeto, nada compartilhado): contorno duro " +
                $"{(cfg.HaloAtivo.Value ? Part(cfg.RaioContorno) + "px" : "off")} cor {cfg.CorContornoHex.Value} " +
                $"alfa {Part(cfg.AlfaContorno)} (4 copias), sombra={(cfg.SombraAtiva.Value ? "on" : "off")}, " +
                $"negrito={cfg.Negrito.Value}, tamanho={(cfg.TamanhoExtra.Value == 0f ? "intocado" : Part(cfg.TamanhoExtra))}. " +
                "Obs.: este texto e UI.Text legado (sem distance field) — halo SUAVE nao se aplica aqui.");
        }

        // ------------------------------------------------------------------
        //  Diagnostico: prova, em runtime, QUEM e o alvo e QUAL material/fonte ele usa.
        //  Isso fecha a lacuna que NAO da para ler estaticamente (MonoBehaviour sem type tree
        //  nos prefabs: nao se sabe qual material cada componente recebeu).
        // ------------------------------------------------------------------
        private static void DetalharAlvo(string superficie, TMP_Text tmp, Material compartilhadoAntes,
            string nomeShader, bool df)
        {
            if (!DetalhesDados.Add(superficie))
            {
                return;
            }
            try
            {
                string nomeFonte = tmp.font != null ? tmp.font.name : "(nula)";
                string nomeMaterialOriginal = compartilhadoAntes != null ? compartilhadoAntes.name : "(nulo)";
                // Se o material em uso ja e uma instancia (nome com "(Instance)") e nao e a nossa
                // (a nossa ja teria saido no guarda acima), e instancia de outro mod — e o TMP
                // NAO clona por cima. O getter `fontMaterial` (TMP_Text) chama
                // `TextMeshProUGUI.GetMaterial(mat)`, e o IL dele so cria copia quando
                // `m_fontMaterial == null || m_fontMaterial.GetInstanceID() != mat.GetInstanceID()`;
                // com o MESMO InstanceID ele REUSA `m_fontMaterial` (`m_sharedMaterial = m_fontMaterial`,
                // sem `CreateMaterialInstance`) e devolve essa instancia. Escrevemos NELA, sem clonar.
                // Nao espalha, porque a instancia e por componente.
                bool jaEraInstancia = nomeMaterialOriginal.Contains("(Instance)");
                Plugin.Log.LogInfo(
                    $"[{superficie}] alvo: objeto='{Nome(tmp)}', componente={tmp.GetType().Name}, " +
                    $"fonte TMP='{nomeFonte}', material compartilhado lido antes do tratamento='{nomeMaterialOriginal}'" +
                    $"{(jaEraInstancia ? " (ja era instancia por componente de outro mod — o TextMeshProUGUI.GetMaterial so cria copia quando m_fontMaterial e nulo ou tem InstanceID diferente; com o MESMO InstanceID ele REUSA a instancia existente, sem CreateMaterialInstance, e escrevemos NELA, sem clonar)" : " (compartilhado do prefab)")}, " +
                    $"shader='{nomeShader}', tem _OutlineWidth (distance field/SDF)={df}");

                // BCT-3 (DIAGNOSTICO): a cor REAL da letra do alvo e a cor de sombra que FICOU no
                // material. Sem esses dois numeros, "a sombra nao aparece" fica sem nada para
                // conferir — e foi exatamente o estado em que o defeito do campo escuro foi
                // relatado (o log dizia `sombra=on`, que e so a chave do config).
                Color corLetra = tmp.color;
                string sombraNoMaterial = "(este material/superficie nao escreveu _UnderlayColor)";
                try
                {
                    Material inst = tmp.fontMaterial;
                    if (inst != null && inst.HasProperty("_UnderlayColor"))
                    {
                        Color sc = inst.GetColor("_UnderlayColor");
                        sombraNoMaterial = $"#{ColorUtility.ToHtmlStringRGB(sc)} alfa={sc.a:0.###}";
                    }
                }
                catch
                {
                    // leitura best-effort: nao pode derrubar o diagnostico
                }
                Plugin.Log.LogInfo(
                    $"[{superficie}] cor da LETRA no alvo='#{ColorUtility.ToHtmlStringRGB(corLetra)}' " +
                    $"(alfa={corLetra.a:0.###}, luminancia={Configuracao.Luminancia(corLetra):0.###}, " +
                    $"letra {(Configuracao.LetraEscura(corLetra) ? "ESCURA" : "CLARA")}); " +
                    $"BCT-4: a sombra tem de CONTRASTAR com a LETRA (diferenca de luminancia >= " +
                    $"{Configuracao.ContrasteMinimo:0.##}); sombra que FICOU no material=_UnderlayColor '{sombraNoMaterial}'.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: log de detalhe falhou: {e.GetType().Name}: {e.Message}");
            }
            InventarioDeCena();
        }

        private static void InventarioDeCena()
        {
            if (_inventarioFeito)
            {
                return;
            }
            _inventarioFeito = true;
            try
            {
                var tmps = Resources.FindObjectsOfTypeAll<TMP_Text>();
                var legados = Resources.FindObjectsOfTypeAll<TextMesh>();
                Plugin.Log.LogInfo(
                    $"Better Combat Text: inventario de cena — {tmps.Length} TMP_Text (TextMeshPro/UGUI, " +
                    $"elegiveis ao halo suave) e {legados.Length} TextMesh legado (3D, usado por " +
                    "DieSideAwareTextDie — NAO e tocado pelo mod).");

                // Amostra dos materiais de fonte distintos em cena: mostra se todos compartilham
                // UM material (o que tornaria um ajuste no compartilhado catastrofico).
                var contagem = new Dictionary<string, int>();
                for (int i = 0; i < tmps.Length; i++)
                {
                    var t = tmps[i];
                    if (t == null)
                    {
                        continue;
                    }
                    Material m = null;
                    try
                    {
                        m = t.fontSharedMaterial;
                    }
                    catch
                    {
                        // segue o jogo
                    }
                    string chave = m != null ? m.name : "(sem material)";
                    contagem.TryGetValue(chave, out var n);
                    contagem[chave] = n + 1;
                }
                int mostrados = 0;
                foreach (var par in contagem)
                {
                    if (mostrados++ >= 10)
                    {
                        Plugin.Log.LogInfo($"Better Combat Text: ... e mais {contagem.Count - 10} materiais distintos.");
                        break;
                    }
                    Plugin.Log.LogInfo($"Better Combat Text: material de fonte em uso: '{par.Key}' x{par.Value}");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"Better Combat Text: inventario de cena falhou: {e.GetType().Name}: {e.Message}");
            }
        }

        private static string Nome(TMP_Text t)
        {
            try
            {
                return t != null && t.gameObject != null ? t.gameObject.name : "(?)";
            }
            catch
            {
                return "(?)";
            }
        }

        private static string Part(float valor) => valor.ToString("0.###");

        private static string Part(BepInEx.Configuration.ConfigEntry<float> e) => e.Value.ToString("0.###");

        /// <summary>Evita repetir o mesmo aviso a cada frame (os postfixes rodam em loop).</summary>
        private static void AvisoUma(string chave, string mensagem)
        {
            if (AvisosDados.ContainsKey(chave))
            {
                return;
            }
            AvisosDados[chave] = mensagem;
            Plugin.Log.LogWarning("Better Combat Text: " + mensagem);
        }
    }
}
