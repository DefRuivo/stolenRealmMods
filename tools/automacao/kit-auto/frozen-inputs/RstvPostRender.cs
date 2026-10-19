// KIT-14F4: consumer-only, opt-in native-handler campaign. Never writes character state.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection;
using BepInEx.Configuration;
using HarmonyLib;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace Aut4Probe
{
    public partial class Aut4ProbePlugin
    {
        private ConfigEntry<bool> _rstvCiclo;
        private ConfigEntry<string> _rstvSkill;
        private int _rstvStage = -1, _rstvActionFrame = -1, _rstvTickFrame = -1;
        private float _rstvStarted;
        private Button _rstvOpen;
        private Component _rstvHover;
        private object _rstvExpected, _rstvObserved;
        private Dictionary<string, object> _rstvAfter;
        private readonly List<object> _rstvSamples = new List<object>();
        private readonly List<object> _rstvEvents = new List<object>();
        private readonly List<object> _rstvOwners = new List<object>();
        private readonly List<object> _rstvOwnerEvidence = new List<object>();
        private readonly List<object> _rstvCounts = new List<object>();
        // run1533: diagnostico POR GUARDA (motivo + estado vivo medido no mesmo quadro).
        private readonly List<object> _rstvDiag = new List<object>();
        private string _rstvDiagUltimoMotivo;
        private int _rstvDiagUltimoFrame = -1;
        private Dictionary<string, object> _rstvBefore;
        private string _rstvParentBefore;
        private object _rstvIndexBefore;
        private bool? _rstvClosed, _rstvOpened, _rstvReopened;
        private int _rstvMaxCount;
        private string _rstvPng;
        private const string RstvPanel = "RstvAllSkillTreesPanel";
        private const string RstvHoverTipoNome = "RoguelikeSkillTreeVisualizer.RstvSkillHover";
        // run1533: teto 35s -> 40s. NAO afrouxa criterio: muda so' o tempo de espera por
        // estado observavel; o teto segue ABAIXO da janela de 120s do arnes de boot (um
        // teto maior que a janela deixava o processo ser fechado sem prova nenhuma).
        private const float RstvTetoSegundos = 40f;
        private const int RstvDiagMaximo = 120;
        // run1533: o JSON passa a ser gravado DURANTE a espera (a cada RstvEscritaSegundos),
        // para que um boot cortado ainda deixe o diagnostico em disco.
        private const float RstvEscritaSegundos = 5f;
        private float _rstvEscrita;
        private GameObject _rstvPainelCena;
        private int _rstvPainelCenaFrame = -1;
        private int _rstvCandidatos = -1;
        private int _rstvObservedFrame = -1;
        // KIT-14F5 (R2): QUAL fonte viva devolveu a identidade observada, e o diagnostico da leitura
        // de ReadOnlySession no MESMO quadro. Sem esses dois campos a amostra nao pode declarar a
        // fonte realmente usada — e declarar a fonte errada seria tao grave quanto campo nulo.
        private string _rstvObservedFonte;
        private string _rstvSessaoDiag;
        private const BindingFlags RstvFlags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance;

        private void ConfigurarRstv()
        {
            _rstvCiclo = Config.Bind("Geral", "RstvCiclo", false,
                "OPT-IN consumer only: observe All Trees after render; native hover/close/reopen, not physical input.");
            _rstvSkill = Config.Bind("Geral", "RstvSkillNome", "",
                "Exact authorized non-Bard skill name for native hover. Empty refuses campaign.");
        }

        // Called immediately BEFORE the already-gated final Button handler.
        private void RstvAntesDeAbrir(GameObject go)
        {
            if (_rstvCiclo == null || !_rstvCiclo.Value) return;
            if (go == null || go.name != "RstvRunSkillTreeButton") return;
            if (string.IsNullOrWhiteSpace(_rstvSkill.Value)) throw new InvalidOperationException("Authorized RSTV skill absent");
            _rstvOpen = go.GetComponent<Button>();
            var gl = Estatico(Tipo("GameLogic"), "instance");
            _rstvExpected = gl == null ? null : Membro(gl, "CurrentlySelectedCharacter");
            _personagemDoModal = _rstvExpected;
            _rstvBefore = SnapshotDoPersonagem();
            _rstvBefore["identidade_clr"] = IdClr(_rstvExpected);
            _rstvBefore["frame"] = Time.frameCount;
            _rstvBefore["selecao_fonte"] = "GameLogic.instance.CurrentlySelectedCharacter before final handler (single local party route)";
            _rstvParentBefore = TooltipPai(TooltipVivo());
            _rstvIndexBefore = TooltipIndice(TooltipVivo());
            _rstvActionFrame = Time.frameCount;
            _rstvStarted = Time.realtimeSinceStartup;
            _rstvStage = 0;
            _observacoes.Clear();
            RstvEvento("before_open", go);
            _res["rstv_coleta"] = Json.Campos("status", "AGUARDANDO", "sessao", _sessao,
                "events", _rstvEvents, "counts", _rstvCounts, "physical_input", false);
        }

        private static object IdClr(object o) => ReferenceEquals(o, null) ? null
            : (object)System.Runtime.CompilerServices.RuntimeHelpers.GetHashCode(o);

        // Painel do RSTV a partir de OBJETO VIVO. O campo estatico do produto e' a via
        // preferida; quando ele nao esta disponivel, o GameObject do CONTRATO
        // ('RstvAllSkillTreesPanel', nome publico do painel) e' localizado na cena viva —
        // isso e' o CONTROLE DO PROPRIO INSTRUMENTO, sem depender do interno do RSTV.
        // A fonte usada vai registrada (nunca presumida).
        private GameObject RstvPainel(out string origem)
        {
            origem = null;
            var t = Tipo("RoguelikeSkillTreeVisualizer.SkillTreesTab");
            var estatico = t == null ? null : Estatico(t, "_painel") as GameObject;
            if (estatico != null)
            {
                origem = "RoguelikeSkillTreeVisualizer.SkillTreesTab._painel (campo estatico do produto, objeto vivo)";
                return estatico;
            }
            GameObject naCena = null;
            // run1533: a varredura da cena e' cara — so' quando o estatico nao esta'
            // disponivel e no maximo a cada 10 quadros (o objeto vivo e' cacheado).
            if (Time.frameCount - _rstvPainelCenaFrame >= 10 || _rstvPainelCena == null)
            {
                _rstvPainelCenaFrame = Time.frameCount;
                foreach (var tr in Recursos<Transform>())
                {
                    if (tr == null || tr.name != RstvPanel || !tr.gameObject.scene.IsValid()) continue;
                    if (naCena == null || (tr.gameObject.activeInHierarchy && !naCena.activeInHierarchy)) naCena = tr.gameObject;
                }
                _rstvPainelCena = naCena;
            }
            naCena = _rstvPainelCena;
            if (naCena != null)
                origem = "cena viva: GameObject.name==" + RstvPanel + " (controle do instrumento, sem o estatico do produto)";
            return naCena;
        }

        // Hover pelo TIPO DO COMPONENTE VIVO (nome de tipo do contrato), nunca por indice
        // nem por array interno do mod.
        private static List<Component> RstvHovers(GameObject root)
        {
            var achados = new List<Component>();
            if (root == null) return achados;
            foreach (var c in root.GetComponentsInChildren<Component>(true))
            {
                if (c == null) continue;
                var tn = c.GetType().FullName;
                if (tn == RstvHoverTipoNome || (tn != null && tn.EndsWith(".RstvSkillHover", StringComparison.Ordinal)))
                    achados.Add(c);
            }
            return achados;
        }

        private static string RstvNomeDaSkill(Component hover, out object info)
        {
            info = null;
            if (hover == null) return null;
            var item = Membro(hover, "Item");
            info = item == null ? null : Membro(item, "SkillInfo");
            if (info == null) return null;
            return Convert.ToString(Membro(info, "SkillName"), CultureInfo.InvariantCulture);
        }

        // run1533: texto do componente VIVO em DUAS familias. O host do RSTV renderiza os
        // rotulos de classe com o componente de texto do proprio jogo
        // (SkillTreeTab.treeName e' UnityEngine.UI.Text, NAO TMP) — ler so' TMP devolvia
        // "render vazio" com a arvore na tela. `texto_renderizado` do texto legado e' o
        // proprio `text` (nao existe template/parse como no TMP): nada e' inferido.
        private static bool TextoRenderizado(Component c, out string bruto, out string renderizado)
        {
            bruto = null;
            renderizado = null;
            var tmp = c as TMP_Text;
            if (tmp != null)
            {
                bruto = tmp.text;
                renderizado = tmp.GetParsedText();
                return true;
            }
            var legado = c as UnityEngine.UI.Text;
            if (legado != null)
            {
                bruto = legado.text;
                renderizado = legado.text;
                return true;
            }
            return false;
        }

        private static int RstvTextosVivos(GameObject root)
        {
            if (root == null) return 0;
            int vivos = 0;
            foreach (var c in root.GetComponentsInChildren<Component>(false))
            {
                if (c == null) continue;
                var b = c as Behaviour;
                if (b == null || !b.isActiveAndEnabled) continue;
                string bruto, renderizado;
                if (!TextoRenderizado(c, out bruto, out renderizado)) continue;
                if (!string.IsNullOrWhiteSpace(renderizado)) vivos++;
            }
            return vivos;
        }

        // Geometria do texto LEGADO (mesmas chaves do leitor TMP, a partir do RectTransform vivo).
        private static Dictionary<string, object> GeometriaLegado(Component c)
        {
            try
            {
                var rt = c.transform as RectTransform;
                if (rt == null) return null;
                var cantos = new Vector3[4];
                rt.GetWorldCorners(cantos);
                float x0 = float.MaxValue, y0 = float.MaxValue, x1 = float.MinValue, y1 = float.MinValue;
                for (int i = 0; i < 4; i++)
                {
                    var p = RectTransformUtility.WorldToScreenPoint(null, cantos[i]);
                    if (p.x < x0) x0 = p.x;
                    if (p.y < y0) y0 = p.y;
                    if (p.x > x1) x1 = p.x;
                    if (p.y > y1) y1 = p.y;
                }
                return Json.Campos(
                    "caixa_na_tela_px", Json.Campos("x", Arred(x0), "y", Arred(y0), "largura", Arred(x1 - x0), "altura", Arred(y1 - y0)),
                    "tamanho_do_rect_px", Json.Campos("largura", Arred(rt.rect.width), "altura", Arred(rt.rect.height)),
                    "escala", Arred(rt.lossyScale.x), "tela", Screen.width + "x" + Screen.height);
            }
            catch { return null; }
        }

        // Leitor do texto LEGADO do host vivo — mesmas chaves do leitor TMP do probe.
        private Dictionary<string, object> LeituraLegado(UnityEngine.UI.Text t, List<object> ownersFunil)
        {
            var mat = t.material;
            var fonte = t.font;
            var keywords = new Dictionary<string, object>();
            if (mat != null)
            {
                foreach (var kw in new[] { "OUTLINE_ON", "UNDERLAY_ON", "UNDERLAY_INNER", "GLOW_ON", "BEVEL_ON" })
                    keywords[kw] = SeguroBool(() => mat.IsKeywordEnabled(kw));
            }
            var cores = Json.Campos(
                "texto", CorDe(t.color),
                "face", CorDoMaterial(mat, "_FaceColor"),
                "contorno", CorDoMaterial(mat, "_OutlineColor"),
                "sombra", CorDoMaterial(mat, "_UnderlayColor"));
            return Json.Campos(
                "objeto", t.gameObject.name,
                "caminho", Caminho(t.transform),
                "componente", t.GetType().Name,
                "ativo_na_hierarquia", t.gameObject.activeInHierarchy,
                "visivel_na_tela", SeguroBool(() => t.isActiveAndEnabled && t.gameObject.activeInHierarchy),
                "texto_bruto", Trunc(t.text, 600),
                "texto_renderizado", Trunc(t.text, 600),
                "fonte", fonte != null ? fonte.name : null,
                "material", mat != null ? mat.name : null,
                "shader", mat != null ? Nome(mat.shader) : null,
                "shader_suportado", mat != null && mat.shader != null && mat.shader.isSupported,
                "keywords", keywords,
                "cores", cores,
                "geometria", GeometriaLegado(t),
                "tamanho_fonte", Arred(t.fontSize),
                "owners", ownersFunil,
                "personagem", Contexto(),
                "snapshot_antes", _snapshotAntes,
                "snapshot_depois", _snapshotDepois,
                "tooltip_pai_antes", _tooltipPaiAntes,
                "tooltip_pai_depois", _tooltipPaiDepois,
                "tooltip_indice_antes", _tooltipIndiceAntes,
                "tooltip_indice_depois", _tooltipIndiceDepois,
                "janelas_duplicadas", _janelasDuplicadas,
                "nota_texto_renderizado", "UnityEngine.UI.Text do host vivo: o texto RENDERIZADO e' o proprio `text` (nao ha template/parse como no TMP)");
        }

        // Diagnostico POR GUARDA: registra o motivo que travou o passo com o estado vivo
        // medido no MESMO quadro. Limitado e deduplicado (motivo novo ou a cada 90 quadros).
        private void RstvNota(string motivo, GameObject panel, string origem, int textos, int candidatos, List<string> nomes)
        {
            if (_rstvDiag.Count >= RstvDiagMaximo) return;
            bool mudou = motivo != _rstvDiagUltimoMotivo || Math.Abs(Time.frameCount - _rstvDiagUltimoFrame) >= 90;
            if (!mudou) return;
            _rstvDiagUltimoMotivo = motivo;
            _rstvDiagUltimoFrame = Time.frameCount;
            var tooltip = TooltipVivo() as Component;
            _rstvDiag.Add(Json.Campos(
                "frame", Time.frameCount,
                "decorrido_s", (float)Math.Round(Time.realtimeSinceStartup - _rstvStarted, 2),
                "stage", _rstvStage,
                "motivo", motivo,
                "painel_encontrado", panel != null,
                "painel_origem", origem,
                "painel_ativo", panel != null && panel.activeInHierarchy,
                "painel_path", panel == null ? null : Caminho(panel.transform),
                "textos_no_painel", textos,
                "hover_tipo", RstvHoverTipoNome,
                "hover_candidatos", candidatos,
                "hover_casou", _rstvHover == null ? null : RstvNomeDaSkill(_rstvHover, out _),
                "skills_no_painel", nomes,
                "skill_configurada", _rstvSkill == null ? null : _rstvSkill.Value,
                "tooltip_nome", tooltip == null ? null : tooltip.gameObject.name,
                "tooltip_ativo", tooltip != null && tooltip.gameObject.activeInHierarchy,
                "frame_before_open", _rstvBefore == null ? null : _rstvBefore["frame"]));
            _res["rstv_diagnostico"] = _rstvDiag;
            // Prova sobrevive ao corte: grava o JSON durante a espera (bounded).
            if (Time.realtimeSinceStartup - _rstvEscrita >= RstvEscritaSegundos)
            {
                _rstvEscrita = Time.realtimeSinceStartup;
                try { Escrever(); } catch { }
            }
        }

        private int RstvContar()
        {
            int all = 0, active = 0;
            foreach (var t in Recursos<Transform>())
            {
                if (t == null || t.name != RstvPanel || !t.gameObject.scene.IsValid()) continue;
                all++;
                if (t.gameObject.activeInHierarchy) active++;
            }
            _rstvMaxCount = Math.Max(_rstvMaxCount, all);
            _rstvCounts.Add(Json.Campos("frame", Time.frameCount, "stage", _rstvStage,
                "host", RstvPanel, "all_scene_instances", all, "active_instances", active));
            return all;
        }

        // Ownership is NOT copied from the generic localization funnel. A live hover component
        // identifies its assembly, then actual Harmony patches from THAT assembly identify owners.
        private void RstvProcedencia(Component live)
        {
            var asm = live.GetType().Assembly;
            foreach (var spec in new[] { new[] { "SkillTreeItem", "Toggle" },
                new[] { "CharacterMenusManager", "OpenWindow" }, new[] { "Tooltip", "get_TooltipCharacter" } })
            {
                var t = Tipo(spec[0]);
                if (t == null) continue;
                foreach (var method in t.GetMethods(RstvFlags).Where(m => m.Name == spec[1]))
                {
                    var info = Harmony.GetPatchInfo(method);
                    if (info == null) continue;
                    foreach (var patch in info.Prefixes.Concat(info.Postfixes).Concat(info.Transpilers).Concat(info.Finalizers))
                    {
                        if (patch.PatchMethod == null || patch.PatchMethod.DeclaringType.Assembly != asm) continue;
                        if (!_rstvOwners.Contains(patch.owner)) _rstvOwners.Add(patch.owner);
                        _rstvOwnerEvidence.Add(Json.Campos("owner", patch.owner,
                            "target_method", method.DeclaringType.FullName + "." + method.Name,
                            "patch_method", patch.PatchMethod.DeclaringType.FullName + "." + patch.PatchMethod.Name,
                            "live_component_type", live.GetType().FullName,
                            "live_component_id", live.GetInstanceID(), "live_path", Caminho(live.transform),
                            "assembly", asm.FullName, "assembly_path", asm.Location,
                            "assembly_sha256", IdentidadeDoProbe.Sha256(asm.Location),
                            "same_assembly", patch.PatchMethod.DeclaringType.Assembly == live.GetType().Assembly));
                    }
                }
            }
        }

        private void RstvEvento(string name, GameObject go = null)
        {
            _rstvEvents.Add(Json.Campos("event", name, "frame", Time.frameCount, "sessao", _sessao,
                "id", go == null ? null : (object)go.GetInstanceID(), "path", go == null ? null : Caminho(go.transform),
                "active", go == null ? null : (object)go.activeInHierarchy));
        }

        private static object RstvInvoke(object obj, string method, params object[] args)
        {
            var m = obj.GetType().GetMethods(RstvFlags).Single(x => x.Name == method && x.GetParameters().Length == args.Length);
            return m.Invoke(obj, args);
        }

        private void RstvAmostras(GameObject root, string stage)
        {
            foreach (var comp in root.GetComponentsInChildren<Component>(false))
            {
                if (comp == null) continue;
                var b = comp as Behaviour;
                if (b == null || !b.isActiveAndEnabled) continue;
                string bruto, renderizado;
                if (!TextoRenderizado(comp, out bruto, out renderizado) || string.IsNullOrWhiteSpace(renderizado)) continue;
                var tmp = comp as TMP_Text;
                var sample = tmp != null
                    ? Leitura(tmp, new List<object>(_rstvOwners))
                    : LeituraLegado((UnityEngine.UI.Text)comp, new List<object>(_rstvOwners));
                sample["texto_bruto"] = bruto; // conteudo integral, sem truncar (prova de tooltip)
                sample["texto_renderizado"] = renderizado;
                sample["componente_do_texto"] = comp.GetType().FullName;
                sample["frame"] = Time.frameCount;
                sample["sessao"] = _sessao;
                sample["procedencia"] = "runtime";
                sample["hash_fonte"] = IdentidadeDoProbe.Sha256(typeof(Aut4ProbePlugin).Assembly.Location);
                sample["config_sha"] = IdentidadeDoProbe.Sha256(Config.ConfigFilePath);
                sample["stage"] = stage;
                sample["instance_id"] = comp.GetInstanceID();
                sample["root_id"] = root.GetInstanceID();
                sample["root_path"] = Caminho(root.transform);
                sample["owner_provenance"] = _rstvOwnerEvidence;
                sample["visibilidade_escopo"] = "Componente de texto ATIVO com texto renderizado nao vazio no objeto VIVO do host; nao e' clique fisico, oclusao nem aceite humano de UIUX";
                var geo = sample["geometria"] as Dictionary<string, object>;
                if (geo != null) geo["tela"] = Screen.width + "x" + Screen.height;
                _rstvSamples.Add(sample);
            }
        }

        // Return true while this opt-in campaign owns the post-navigation phase.
        private bool PassoRstv()
        {
            if (_rstvStage < 0) return false;
            if (_rstvTickFrame == Time.frameCount) return true;
            _rstvTickFrame = Time.frameCount;
            if (Time.realtimeSinceStartup - _rstvStarted > RstvTetoSegundos)
            {
                _rstvDiagUltimoMotivo = "TETO_TEMPO " + RstvTetoSegundos + "s atingido no estagio " + _rstvStage;
                RstvNota(_rstvDiagUltimoMotivo, null, null, 0, -1, null);
                RstvFinalizar("TIMEOUT");
                return true;
            }
            // Different hooks may tick repeatedly in one frame. No step can consume its own action.
            if (Time.frameCount <= _rstvActionFrame + 1) return true;
            // KIT-14F5 (R2): o alvo EFETIVO do caminho All Trees e' capturado por OBSERVACAO no
            // primeiro quadro em que uma fonte VIVA o oferece. Nunca substituido pelo alvo esperado
            // (isso seria tautologia) e nunca derivado dele.
            if (_rstvObserved == null)
            {
                var alvoVivo = PersonagemDoModalObservado();
                if (alvoVivo != null)
                {
                    _rstvObserved = alvoVivo;
                    _rstvObservedFrame = Time.frameCount;
                }
            }
            string origemPainel;
            var panel = RstvPainel(out origemPainel);
            switch (_rstvStage)
            {
                case 0:
                case 4:
                    if (panel == null)
                    {
                        RstvNota("painel do RSTV nao localizado (estatico indisponivel e nenhum GameObject vivo com o nome do contrato)", null, null, 0, -1, null);
                        return true;
                    }
                    if (!panel.activeInHierarchy)
                    {
                        RstvNota("painel localizado mas INATIVO na hierarquia", panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    var hovers = RstvHovers(panel);
                    if (hovers.Count == 0)
                    {
                        RstvNota("nenhum componente RstvSkillHover vivo sob o painel", panel, origemPainel, RstvTextosVivos(panel), 0, null);
                        return true;
                    }
                    _rstvCandidatos = hovers.Count;
                    var nomesVivos = new List<string>();
                    foreach (var h in hovers)
                    {
                        var n = RstvNomeDaSkill(h, out _);
                        if (!string.IsNullOrWhiteSpace(n) && !nomesVivos.Contains(n)) nomesVivos.Add(n);
                    }
                    if (_rstvHover == null)
                    {
                        _rstvHover = hovers.FirstOrDefault(c =>
                        {
                            object info;
                            var n = RstvNomeDaSkill(c, out info);
                            if (info == null || string.IsNullOrWhiteSpace(n)) return false;
                            var kind = Convert.ToString(Membro(info, "SkillType"), CultureInfo.InvariantCulture);
                            return kind != "Bard"
                                && string.Equals(n.Trim(), _rstvSkill.Value.Trim(), StringComparison.OrdinalIgnoreCase);
                        });
                    }
                    if (_rstvHover == null)
                    {
                        RstvNota("nenhum hover vivo com SkillName == skill autorizada da config", panel, origemPainel, RstvTextosVivos(panel), hovers.Count, nomesVivos);
                        return true;
                    }
                    if (RstvTextosVivos(panel) == 0)
                    {
                        RstvNota("painel vivo sem TMP_Text ATIVO com texto renderizado (render vazio)", panel, origemPainel, 0, hovers.Count, nomesVivos);
                        return true;
                    }
                    // KIT-14F5 (R2): NAO sobrescreve e NAO inventa — se nenhuma fonte viva devolveu
                    // alvo ate aqui, o campo fica nulo e a amostra declara a ausencia com o motivo.
                    if (_rstvObserved == null)
                    {
                        var alvoVivo = PersonagemDoModalObservado();
                        if (alvoVivo != null)
                        {
                            _rstvObserved = alvoVivo;
                            _rstvObservedFrame = Time.frameCount;
                        }
                    }
                    if (_rstvStage == 0)
                    {
                        _rstvOpened = panel.activeInHierarchy;
                        RstvProcedencia(_rstvHover);
                        RstvAmostras(panel, "tree_after_open");
                        RstvContar();
                        RstvEvento("open_observed", panel);
                        var info = Membro(Membro(_rstvHover, "Item"), "SkillInfo");
                        _res["rstv_skill_viva"] = Json.Campos("nome", Membro(info, "SkillName"),
                            "guid", Membro(info, "Guid"), "tipo", Membro(info, "SkillType")?.ToString(),
                            "raw_asset_description", Membro(info, "Description"),
                            "handler", _rstvHover.GetType().FullName + ".OnPointerEnter", "path", Caminho(_rstvHover.transform));
                        RstvInvoke(_rstvHover, "OnPointerEnter", new object[] { null });
                        RstvEvento("hover_handler", _rstvHover.gameObject);
                        _rstvStage = 1;
                    }
                    else
                    {
                        _rstvReopened = panel.activeInHierarchy;
                        RstvContar();
                        RstvAmostras(panel, "tree_after_reopen");
                        RstvEvento("reopen_observed", panel);
                        RstvFechar();
                        _rstvStage = 5;
                    }
                    _rstvActionFrame = Time.frameCount;
                    break;
                case 1:
                    var tooltip = TooltipVivo() as Component;
                    if (tooltip == null)
                    {
                        RstvNota("tooltip vivo ausente (GUIManager.instance.tooltip null) apos o hover nativo", panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    if (!tooltip.gameObject.activeInHierarchy)
                    {
                        RstvNota("tooltip localizado mas INATIVO na hierarquia apos o hover nativo", panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    var title = Membro(tooltip, "Title") as TMP_Text;
                    var description = Membro(tooltip, "Description") as TMP_Text;
                    if (title == null || description == null || !title.isActiveAndEnabled || !description.isActiveAndEnabled
                        || string.IsNullOrWhiteSpace(title.GetParsedText()) || string.IsNullOrWhiteSpace(description.GetParsedText()))
                    {
                        RstvNota("tooltip ativo sem Title/Description renderizados (title=" + (title == null ? "null" : title.gameObject.name)
                            + " desc=" + (description == null ? "null" : description.gameObject.name) + ")", panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    RstvAmostras(tooltip.gameObject, "tooltip_after_hover");
                    RstvEvento("tooltip_observed", tooltip.gameObject);
                    _rstvPng = System.IO.Path.Combine(_dir, "03-rstv-tooltip.png");
                    ScreenCapture.CaptureScreenshot(_rstvPng);
                    RstvEvento("tooltip_png_requested", tooltip.gameObject);
                    _rstvStage = 2;
                    _rstvActionFrame = Time.frameCount;
                    break;
                case 2:
                    if (!System.IO.File.Exists(_rstvPng) || new System.IO.FileInfo(_rstvPng).Length == 0)
                    {
                        RstvNota("aguardando o PNG do tooltip (efeito best-effort)", panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    RstvEvento("tooltip_png_completed");
                    _arquivosDePrint.Add(_rstvPng);
                    RstvInvoke(_rstvHover, "OnPointerExit", new object[] { null });
                    RstvFechar();
                    _rstvStage = 3;
                    _rstvActionFrame = Time.frameCount;
                    break;
                case 3:
                case 5:
                    if (panel != null && panel.activeInHierarchy)
                    {
                        RstvNota("painel ainda ATIVO depois do fechar nativo", panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    if (PersonagemDaSessao() != null || Equals(Estatico(Tipo("RoguelikeSkillTreeVisualizer.ReadOnlySession"), "Active"), true))
                    {
                        RstvNota("sessao read-only ainda ativa depois do fechar", panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    if (_rstvStage == 3 && (_rstvOpen == null || MotivoDeBloqueio(_rstvOpen, true, true) != null))
                    {
                        RstvNota("botao de reabrir ainda bloqueado: " + (_rstvOpen == null ? "botao ausente" : MotivoDeBloqueio(_rstvOpen, true, true)), panel, origemPainel, RstvTextosVivos(panel), -1, null);
                        return true;
                    }
                    _rstvClosed = panel != null && !panel.activeInHierarchy;
                    RstvContar();
                    _personagemDoModal = _rstvExpected; // pinned original reference, not current global selection
                    _rstvAfter = SnapshotDoPersonagem();
                    _rstvAfter["identidade_clr"] = IdClr(_personagemDoModal);
                    _rstvAfter["frame"] = Time.frameCount;
                    RstvEvento("close_observed", panel);
                    if (_rstvStage == 5) { RstvFinalizar("CONCLUIDO"); break; }
                    _rstvOpen.onClick.Invoke();
                    RstvEvento("reopen_handler", _rstvOpen.gameObject);
                    _rstvStage = 4;
                    _rstvActionFrame = Time.frameCount;
                    break;
            }
            return true;
        }

        /// <summary>KIT-14F5 (R2) — IDENTIDADE DO ALVO POR OBSERVACAO, sem tautologia.
        ///
        /// Duas fontes VIVAS, ambas independentes do campo esperado (<c>_rstvExpected</c>, lido de
        /// <c>GameLogic.instance.CurrentlySelectedCharacter</c> ANTES do handler final):
        ///   1. <c>ReadOnlySession.Active/Target</c> do produto — o caminho que o RSTV declara;
        ///   2. <c>InventoryManager.Instance.CurrentInventoryCharacter</c> — o personagem que a
        ///      JANELA DE INVENTARIO (hosteira da aba All Trees) esta exibindo.
        ///
        /// MEDIDO no boot run1533: (1) devolve <c>Active=False</c> e <c>Target=null</c> no instante da
        /// leitura porque o PROPRIO produto encerra a sessao logo depois de <c>Begin</c>
        /// (<c>RSTV-2: commit higienizado</c> no Player.log) — por isso o diagnostico e registrado e
        /// a fonte (1) nunca e' reaproveitada como identidade. A fonte (2) e' um objeto vivo do jogo,
        /// lido no quadro declarado; se a janela estiver exibindo OUTRO personagem, o valor observado
        /// e' o outro e o confronto por referencia reprova. Nada aqui copia o esperado.</summary>
        private object PersonagemDoModalObservado()
        {
            // (1) sessao read-only do produto — o caminho declarado pelo RSTV.
            try
            {
                var t = Tipo("RoguelikeSkillTreeVisualizer.ReadOnlySession");
                if (t == null)
                {
                    _rstvSessaoDiag = "tipo RoguelikeSkillTreeVisualizer.ReadOnlySession ausente no AppDomain";
                }
                else
                {
                    bool ativa = Equals(Estatico(t, "Active"), true);
                    object alvo = ativa ? Estatico(t, "Target") : null;
                    if (alvo != null)
                    {
                        _rstvObservedFonte = "RoguelikeSkillTreeVisualizer.ReadOnlySession.Target (Active=True) no quadro da leitura";
                        _rstvSessaoDiag = "sessao read-only do produto ATIVA com alvo nao nulo no quadro da leitura";
                        return alvo;
                    }
                    _rstvSessaoDiag = "ReadOnlySession.Active=" + (ativa ? "True" : "False")
                        + ", Target=null no quadro da leitura"
                        + (ativa ? "" : " (sessao encerrada pelo produto apos Begin)");
                }
            }
            catch (Exception e) { _rstvSessaoDiag = "leitura de ReadOnlySession falhou: " + e.GetType().Name; }

            // (2) host do inventario — janela viva que exibe o personagem do modal.
            try
            {
                var ti = Tipo("InventoryManager");
                if (ti != null)
                {
                    object inv = Estatico(ti, "Instance");
                    string via = "InventoryManager.Instance";
                    if (inv == null)
                    {
                        // static herdado de LoadableUIWindow<T>: caminho explicito, se a heranca
                        // de propriedade estatica nao aparecer no tipo derivado nesta runtime.
                        for (var b = ti.BaseType; b != null && inv == null; b = b.BaseType)
                            inv = Estatico(b, "Instance");
                        via = "LoadableUIWindow<InventoryManager>.Instance";
                    }
                    if (inv == null)
                    {
                        inv = UnityEngine.Object.FindObjectOfType(ti);
                        via = "FindObjectOfType(InventoryManager) (Instance estatico nulo)";
                    }
                    if (inv != null)
                    {
                        var alvo = Membro(inv, "CurrentInventoryCharacter");
                        if (alvo != null)
                        {
                            _rstvObservedFonte = via + ".CurrentInventoryCharacter (janela de inventario que hospeda a aba, objeto vivo do jogo)";
                            return alvo;
                        }
                        _rstvSessaoDiag = (_rstvSessaoDiag ?? "") + " | " + via + ".CurrentInventoryCharacter=null";
                        return null;
                    }
                    _rstvSessaoDiag = (_rstvSessaoDiag ?? "") + " | InventoryManager ausente (Instance e FindObjectOfType nulos)";
                }
            }
            catch (Exception e)
            {
                _rstvSessaoDiag = (_rstvSessaoDiag ?? "") + " | leitura de InventoryManager falhou: " + e.GetType().Name;
            }
            return null;
        }

        private void RstvFechar()
        {
            var menu = Estatico(Tipo("CharacterMenusManager"), "Instance");
            if (menu == null) throw new InvalidOperationException("Native menu host absent");
            RstvInvoke(menu, "CloseWindow");
            RstvEvento("close_handler", (menu as Component)?.gameObject);
        }

        private void RstvFinalizar(string status)
        {
            object tooltip = TooltipVivo();
            var observedName = _rstvObserved == null ? null : Membro(_rstvObserved, "CharacterName");
            foreach (Dictionary<string, object> sample in _rstvSamples)
            {
                sample["snapshot_antes"] = _rstvBefore;
                sample["snapshot_depois"] = _rstvAfter; // absent on timeout is NOT converted to equal
                sample["personagem_esperado"] = _rstvExpected == null ? null : Membro(_rstvExpected, "CharacterName");
                sample["personagem"] = Json.Campos(
                    "personagem", observedName,
                    // KIT-14F5 (R2): a fonte DECLARADA e' a que realmente devolveu o objeto.
                    "fonte", _rstvObservedFonte ?? "nenhuma fonte viva devolveu alvo no ciclo",
                    "identidade_clr", IdClr(_rstvObserved),
                    "frame_observado", _rstvObservedFrame < 0 ? null : (object)_rstvObservedFrame,
                    "diagnostico_readonly_session", _rstvSessaoDiag);
                sample["mesma_referencia_alvo"] = !ReferenceEquals(_rstvExpected, null) && ReferenceEquals(_rstvExpected, _rstvObserved);
                sample["identidade_observada_fonte"] = _rstvObservedFonte;
                sample["identidade_observada_clr"] = IdClr(_rstvObserved);
                sample["identidade_esperada_clr"] = IdClr(_rstvExpected);
                sample["tooltip_pai_antes"] = _rstvParentBefore;
                sample["tooltip_indice_antes"] = _rstvIndexBefore;
                sample["tooltip_pai_depois"] = TooltipPai(tooltip);
                sample["tooltip_indice_depois"] = TooltipIndice(tooltip);
                sample["janelas_duplicadas"] = Math.Max(0, _rstvMaxCount - 1);
                sample["janela"] = Json.Campos("aberta", _rstvOpened, "fechada", _rstvClosed, "reaberta", _rstvReopened);
            }
            if (_rstvDiag.Count < RstvDiagMaximo)
                _rstvDiag.Add(Json.Campos("frame", Time.frameCount, "stage", _rstvStage, "motivo", "FINAL " + status,
                    "decorrido_s", (float)Math.Round(Time.realtimeSinceStartup - _rstvStarted, 2),
                    "amostras", _rstvSamples.Count, "eventos", _rstvEvents.Count, "diagnosticos", _rstvDiag.Count));
            _observacoes.Clear();
            _observacoes.AddRange(_rstvSamples);
            _res["observacoes"] = _observacoes;
            _res["rstv_diagnostico"] = _rstvDiag;
            _res["rstv_coleta"] = Json.Campos("status", status, "sessao", _sessao,
                "before", _rstvBefore, "after", _rstvAfter, "events", _rstvEvents, "counts", _rstvCounts,
                "owner_provenance", _rstvOwnerEvidence, "owners", _rstvOwners, "physical_input", false,
                "same_character_reference", !ReferenceEquals(_rstvExpected, null) && ReferenceEquals(_rstvExpected, _rstvObserved),
                "identity_fonte", _rstvObservedFonte,
                "identity_frame_observado", _rstvObservedFrame < 0 ? null : (object)_rstvObservedFrame,
                "identity_observada_clr", IdClr(_rstvObserved),
                "identity_esperada_clr", IdClr(_rstvExpected),
                "identity_readonly_session_diagnostico", _rstvSessaoDiag,
                "samples", _rstvSamples.Count, "tooltip_png", _rstvPng, "diagnostico", _rstvDiag,
                "capabilities_not_collected", new[] { "Dependency", "mechanical_expectations", "physical_click", "human_UIUX" });
            _rstvStage = -2;
            PedirPrint("01-ui");
            Ir(F_PRINT1, "print-01");
        }
    }
}
