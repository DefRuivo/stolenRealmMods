// AUT-4 — COMPONENTES AGREGADOS DE LEITURA (isolados, SOMENTE LEITURA).
//
// Sao os agregados que o CAP-1 (scratch/cap1/CapProbe) tinha e o AUT-4 ainda nao:
//   * `Inventario`    — todos os TMP_Text vivos, resumidos por shader, por fonte e pelo
//                       combo (shader | fonte), com a amostra dos alvos de tooltip e o
//                       criterio de EFEITO medido no material EM USO.
//   * `Fontes`        — os TMP_FontAsset em memoria (material/shader/atlas/glifos) e o
//                       shader de REFERENCIA do proprio TMP (`ShaderUtilities.ShaderRef_MobileSDF`),
//                       que e a "receita" contra a qual o BetterFont compara.
//   * `TextosVisiveis`— o que JA foi DESENHADO (GetParsedText nao vazio), com geometria.
//
// CONTRATO DE SEGURANCA — o componente e ISOLADO de proposito:
//   * NAO depende da instancia do plugin nem de `Update` (nenhum estado mutavel aqui):
//     sao funcoes ESTATICAS que recebem so o teto de leitura e devolvem JSON.
//   * NAO escreve NADA no jogo: so getters (`GetFloat`/`GetTexture`/
//     `IsKeywordEnabled`/`GetParsedText`/`GetWorldCorners`). Nenhum
//     `EnableKeyword`/`SetColor`/`SetTexture`/`Destroy` — a trava do teste offline
//     (`testes/t_aut4_probe_contrato.py`) recusa se algum deles aparecer.
//   * Campo que nao existe/nao da para medir sai `null` — AUSENTE no contrato do
//     coletor, NUNCA um valor inventado.
//
// Estes agregados sao CONTEXTO da rodada (topo do `aut4probe.json`), nao campos de
// observacao: eles NAO entram em `CAMPOS`/`CAMPOS_EXTRAS` do coletor, entao nao podem
// ser pedidos como `campos_alvo` sem que o esquema do driver seja estendido — o
// criterio continua honesto (A2 da AUT-4R2: alvo fora do schema e plano invalido).
using System;
using System.Collections.Generic;
using System.Reflection;
using TMPro;
using UnityEngine;

namespace Aut4Probe
{
    /// <summary>Leitor de UM texto, injetado pelo chamador: o agregado nao conhece o
    /// estado da rodada (snapshots/guarda do RSTV), so a leitura do objeto vivo. E o que
    /// mantem o componente isolado e substituivel num teste.</summary>
    internal delegate Dictionary<string, object> LeitorDeTexto(TMP_Text t);

    internal static class LeituraAgregados
    {
        /// <summary>Nomes dos componentes de tooltip que entram na amostra mesmo sem
        /// texto (o alvo do mod e lido por NOME, como no CAP-1).</summary>
        private static readonly string[] NomesDeTooltip =
        { "Title", "Description", "Subtitle", "BigText", "FooterText", "IfEquippedText" };

        /// <summary>Resumo de TODOS os TMP_Text vivos: por shader, por fonte, pelo combo e
        /// a contagem de efeito no material EM USO (o mesmo criterio do BetterFont).</summary>
        internal static Dictionary<string, object> Inventario(int maxAmostra, LeitorDeTexto leitura)
        {
            var todos = Recursos<TMP_Text>();
            var porShader = new Dictionary<string, int>();
            var porFonte = new Dictionary<string, int>();
            var porCombo = new Dictionary<string, int>();
            var amostra = new List<object>();
            int comTexto = 0;
            int ativos = 0;
            int comEfeito = 0;
            int semEfeito = 0;

            foreach (var t in todos)
            {
                if (t == null) continue;
                var mat = t.fontSharedMaterial;
                string shader = Nome(mat != null ? mat.shader
                    : (t.font != null && t.font.material != null ? t.font.material.shader : null));
                string fonte = t.font != null ? t.font.name : "(sem fonte)";
                Incrementa(porShader, shader);
                Incrementa(porFonte, fonte);
                Incrementa(porCombo, shader + " | " + fonte);
                bool temTexto = !string.IsNullOrEmpty(t.text);
                if (temTexto) comTexto++;
                if (t.gameObject.activeInHierarchy) ativos++;
                if (EfeitoNoMaterial(mat)) comEfeito++;
                else semEfeito++;

                bool nomeDeTooltip = Array.IndexOf(NomesDeTooltip, t.gameObject.name) >= 0;
                if ((nomeDeTooltip || (temTexto && amostra.Count < maxAmostra)) && leitura != null)
                    amostra.Add(leitura(t));
            }

            return Json.Campos(
                "total_tmp_text", todos.Length,
                "textos_com_efeito_no_material", comEfeito,
                "textos_sem_efeito_no_material", semEfeito,
                "criterio_de_efeito",
                "espelho do criterio do BetterFont (TemEfeitoNoMaterial + SombraDesenhada + TexturaDeEfeito): contorno "
                + "(_OutlineWidth>0 ou _OutlineSoftness>0 ou OUTLINE_ON), sombra DESENHADA (UNDERLAY_ON/UNDERLAY_INNER ou "
                + "|_UnderlayOffsetX|/|_UnderlayOffsetY|/_UnderlayDilate > 0.0001), GLOW_ON/BEVEL_ON e _FaceTex/_BumpMap "
                + "DE VERDADE (nao a textura embutida branca/normal do Unity). A cor da sombra com alfa NAO conta por si: "
                + "e a sombra INERTE do material do jogo (keyword desligada, offset/dilate zero), que o shader nao "
                + "desenha — o BetterFont (BF-5) tambem nao a trata como efeito.",
                "com_texto_nao_vazio", comTexto,
                "ativos_na_hierarquia", ativos,
                "por_shader", porShader,
                "por_fonte", porFonte,
                "por_combo_shader_fonte", porCombo,
                "amostra", amostra,
                "amostra_regra", "todos os TMP_Text com texto nao vazio (ate " + maxAmostra
                + ") + os componentes de tooltip por NOME (Title/Description/Subtitle/BigText/FooterText/IfEquippedText)"
                + " — o resto fica no resumo por shader/fonte.",
                "leitura", "TMP_Text.text / GetParsedText() / fontSharedMaterial.shader / material + geometria de tela (RectTransform.GetWorldCorners).");
        }

        /// <summary>Fontes em memoria + o shader de REFERENCIA do TMP. O shader sai de
        /// `ShaderUtilities.ShaderRef_MobileSDF` lido por REFLEXAO (nao referenciamos o
        /// campo no compile: o instrumento nao quebra com mudanca do TMP).</summary>
        internal static Dictionary<string, object> Fontes()
        {
            var fontes = Recursos<TMP_FontAsset>();
            var lista = new List<object>();
            foreach (var f in fontes)
            {
                if (f == null) continue;
                var mat = f.material;
                lista.Add(Json.Campos(
                    "nome", f.name,
                    "arquivo_de_origem", f.sourceFontFile != null ? f.sourceFontFile.name : null,
                    "material", mat != null ? mat.name : null,
                    "shader", mat != null ? Nome(mat.shader) : null,
                    "shader_suportado", mat != null && mat.shader != null && mat.shader.isSupported,
                    "atlas", f.atlasWidth + "x" + f.atlasHeight,
                    "glifos", f.characterTable != null ? f.characterTable.Count : 0,
                    "multi_atlas", f.isMultiAtlasTexturesEnabled));
            }

            string refMobileSdf = null;
            string erroRef = null;
            try
            {
                var su = Aut4ProbePlugin.Tipo("TMPro.ShaderUtilities");
                var prop = su == null ? null : su.GetProperty("ShaderRef_MobileSDF",
                    BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic);
                var val = prop == null ? null : prop.GetValue(null);
                var shader = val as Shader;
                refMobileSdf = shader != null ? shader.name : null;
                if (shader == null) erroRef = "ShaderRef_MobileSDF nao resolvido (campo/propriedade ausente ou nula)";
            }
            catch (Exception e) { erroRef = e.GetType().Name + ": " + e.Message; }

            var encontrado = Shader.Find("TextMeshPro/Mobile/Distance Field");

            return Json.Campos(
                "total_tmp_fontasset_em_memoria", fontes.Length,
                "fontes", lista,
                "shader_de_referencia_mobile_sdf_do_tmp", refMobileSdf,
                "erro_shader_de_referencia", erroRef,
                "shader_find_mobile_distance_field",
                encontrado != null ? encontrado.name : "(Shader.Find devolveu null)",
                "observacao", "E o shader do material da fonte que o criterio de falha-segura do "
                + "BetterFont compara com o material em uso de cada texto.");
        }

        /// <summary>Textos JA DESENHADOS (GetParsedText nao vazio) com o shader em uso e a
        /// geometria de tela — a lista que prova o que a tela mostra agora.</summary>
        internal static List<object> TextosVisiveis(int max)
        {
            var lista = new List<object>();
            foreach (var t in Recursos<TMP_Text>())
            {
                if (t == null || lista.Count >= max) continue;
                if (!t.gameObject.activeInHierarchy) continue;
                string txt = Seguro(() => t.GetParsedText()) as string;
                if (string.IsNullOrEmpty(txt)) continue;
                var mat = t.fontSharedMaterial;
                lista.Add(Json.Campos(
                    "objeto", t.gameObject.name,
                    "caminho", Aut4ProbePlugin.Caminho(t.transform),
                    "texto_renderizado", Aut4ProbePlugin.Trunc(txt, 160),
                    "shader_em_uso", mat != null ? Nome(mat.shader) : null,
                    "geometria_tela", Aut4ProbePlugin.Geometria(t)));
            }
            return lista;
        }

        // -------------------------------------------- criterio de efeito (porte CAP-1)

        /// <summary>Espelho do criterio do BetterFont (`TemEfeitoNoMaterial`, que delega a
        /// sombra a `SombraDesenhada`, + `TexturaDeEfeito`): o material DESTE texto carrega
        /// contorno/sombra/glow DE VERDADE? E o criterio que classifica a linha do diagnostico e
        /// que exige MEDIR, em vez de assumir. Fonte da verdade: `BetterFont/Plugin.cs`
        /// (TemEfeitoNoMaterial / SombraDesenhada / TexturaDeEfeito).</summary>
        internal static bool EfeitoNoMaterial(Material m)
        {
            try
            {
                if (m == null) return false;
                if (TexturaDeEfeito(m, "_FaceTex") || TexturaDeEfeito(m, "_BumpMap")) return true;
                if (m.IsKeywordEnabled("GLOW_ON") || m.IsKeywordEnabled("BEVEL_ON")) return true;
                if (m.IsKeywordEnabled("OUTLINE_ON") || ValorAtivo(m, "_OutlineWidth") || ValorAtivo(m, "_OutlineSoftness")) return true;
                if (SombraDesenhada(m)) return true;
                return false;
            }
            catch { return true; } // em duvida, tratar como efeito (mesma escolha do mod)
        }

        /// <summary>BF-5 — espelho de `BetterFont/Plugin.cs::SombraDesenhada`: a sombra esta
        /// DESENHADA? A cor da sombra com alfa NAO prova nada por si (o prefab do jogo traz
        /// preto alfa 0.5, keyword desligada e offset/dilate zero: sombra INERTE que o shader
        /// nao renderiza). Decide pelo que faz a sombra APARECER — a keyword ligada ou a
        /// geometria da sombra diferente de zero.</summary>
        private static bool SombraDesenhada(Material m)
        {
            try
            {
                if (m == null) return false;
                if (m.IsKeywordEnabled("UNDERLAY_ON") || m.IsKeywordEnabled("UNDERLAY_INNER")) return true;
                if (ValorDiferenteDeZero(m, "_UnderlayOffsetX")) return true;
                if (ValorDiferenteDeZero(m, "_UnderlayOffsetY")) return true;
                if (ValorDiferenteDeZero(m, "_UnderlayDilate")) return true;
                return false;
            }
            catch { return false; }
        }

        private static bool ValorAtivo(Material m, string prop)
        {
            try { return m.HasProperty(prop) && m.GetFloat(prop) > 0.0001f; } catch { return false; }
        }

        private static bool ValorDiferenteDeZero(Material m, string prop)
        {
            try { return m.HasProperty(prop) && Mathf.Abs(m.GetFloat(prop)) > 0.0001f; } catch { return false; }
        }

        private static bool TexturaDeEfeito(Material m, string prop)
        {
            try
            {
                if (m == null || !m.HasProperty(prop)) return false;
                var tex = m.GetTexture(prop);
                if (tex == null) return false;
                if (tex == Texture2D.whiteTexture || tex == Texture2D.normalTexture ||
                    tex == Texture2D.blackTexture || tex == Texture2D.grayTexture) return false;
                string n = (tex.name ?? string.Empty).Trim().ToLowerInvariant();
                if (n == "white" || n.StartsWith("white ") || n == "bump" || n.StartsWith("bump ") ||
                    n == "gray" || n.StartsWith("gray ") || n == "black" || n.StartsWith("black ") ||
                    n.StartsWith("unity_") || n.StartsWith("unity default")) return false;
                return tex.width > 8 || tex.height > 8;
            }
            catch { return true; }
        }

        // ------------------------------------------------------------- utilitarios

        private static T[] Recursos<T>() where T : UnityEngine.Object
        {
            try { return Resources.FindObjectsOfTypeAll<T>(); } catch { return new T[0]; }
        }

        private static string Nome(Shader s) { return s == null ? null : s.name; }

        private static void Incrementa(Dictionary<string, int> d, string chave)
        {
            if (chave == null) chave = "(nulo)";
            d.TryGetValue(chave, out int atual);
            d[chave] = atual + 1;
        }

        private static object Seguro(Func<object> f) { try { return f(); } catch { return null; } }
    }
}
