using System;
using System.Collections.Generic;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;

namespace FollowUpMod
{
    [BepInPlugin(Guid, "FollowUpMod", Version)]
    public sealed class FollowUpModPlugin : BaseUnityPlugin
    {
        public const string Guid = "com.gumatos.followupmod";
        public const string Version = "0.1.0";

        internal static ManualLogSource Log = null!;
        internal static Harmony HarmonyInstance = null!;

        private void Awake()
        {
            Log = Logger;
            Diag.Write("Awake " + Version + " obj=" + (gameObject != null ? gameObject.name : "null"));
            UnityEngine.Object.DontDestroyOnLoad(gameObject);
            Diag.ReportAssemblies();
            HarmonyInstance = new Harmony(Guid);

            int ok = 0;
            var failed = new List<string>();

            // Patch manual (HarmonyInstance.Patch + HarmonyMethod). O PatchClassProcessor
            // registrava os patches ("metodos patcheados=5") sem que nenhum hook rodasse em
            // jogo - inclusive com o mod SOZINHO no plugins/. Patch manual devolve o metodo
            // gerado, entao da para provar a anexacao e nao apenas acreditar nela.
            void Manual(string label, Type target, string methodName, Type[] args, Type patchClass)
            {
                try
                {
                    var alvo = AccessTools.Method(target, methodName, args);
                    if (alvo == null)
                    {
                        failed.Add(label + ":alvo-ausente");
                        Diag.Write("ALVO AUSENTE " + label + " (" + target.Name + "." + methodName + ")");
                        return;
                    }
                    var pre = AccessTools.Method(patchClass, "Prefix");
                    var post = AccessTools.Method(patchClass, "Postfix");
                    var gerado = HarmonyInstance.Patch(alvo,
                        pre == null ? null : new HarmonyMethod(pre),
                        post == null ? null : new HarmonyMethod(post));
                    ok++;
                    Diag.Write("patch " + label + " pre=" + (pre != null) + " post=" + (post != null)
                        + " ret=" + (gerado == null ? "NULL" : gerado.Name));
                    Log.LogInfo("FU: patch aplicado " + label);
                }
                catch (Exception ex)
                {
                    failed.Add(label + ":" + ex.GetType().Name);
                    Diag.Write("FALHOU " + label + " " + ex.GetType().Name + ": " + ex.Message);
                    Log.LogError("FU: patch falhou " + label + ": " + ex);
                }
            }

            Manual("SelectionGate", typeof(CharacterChoiceManager), "ToggleSelectedCharacter", new[] { typeof(int) }, typeof(SelectionGatePatch));
            Manual("SaveGuard", typeof(Character), "Save", new[] { typeof(bool) }, typeof(SaveGuardPatch));
            Manual("HostAnnounce", typeof(Root), "set_PlayingMultiplayer", new[] { typeof(bool) }, typeof(HostAnnouncePatch));
            Manual("SessionEnd", typeof(NetworkingManager), "ExecuteExitToMainMenu", Type.EmptyTypes, typeof(SessionEndPatch));
            Manual("Sonda", typeof(Character), "get_Level", Type.EmptyTypes, typeof(DiagProbePatch));
            Manual("CliqueTile", typeof(CharacterChoiceItem), "MouseDown", new[] { typeof(int) }, typeof(TileClickPatch));
            Manual("OrdemNivel", typeof(RoguelikeManager), "Start", Type.EmptyTypes, typeof(LevelUpOrderPatch));
            Manual("FluxoNivel", typeof(RoguelikeManager), "ConfirmLevelUpSelection", Type.EmptyTypes, typeof(LevelUpFlowPatch));

            // Registro efetivamente visivel para o Harmony deste processo.
            int hookTypes = 0;
            var alvos = new List<string>();
            try
            {
                foreach (var method in HarmonyInstance.GetPatchedMethods())
                {
                    var info = Harmony.GetPatchInfo(method);
                    if (info == null) continue;
                    bool ours = false;
                    foreach (var p in info.Prefixes) if (p.owner == Guid) ours = true;
                    foreach (var p in info.Postfixes) if (p.owner == Guid) ours = true;
                    if (!ours) continue;
                    hookTypes++;
                    alvos.Add(method.DeclaringType != null ? method.DeclaringType.Name + "." + method.Name : method.Name);
                }
            }
            catch (Exception ex) { Log.LogWarning("FU: contagem de patches falhou: " + ex.GetType().Name); }

            Log.LogInfo("FollowUpMod " + Version + " ativo: " + ok + "/8 patches; metodos patcheados=" + hookTypes
                + " [" + string.Join(", ", alvos) + "]"
                + (failed.Count == 0 ? "" : " falhas=" + string.Join(",", failed)));
        }

        private void Start()
        {
            Diag.Write("Start vivo; activeInHierarchy=" + gameObject.activeInHierarchy + " obj=" + gameObject.name);
        }

        private float _relogio;

        // Diagnostico: o Harmony diz "patcheado" no Awake; aqui provamos o estado DEPOIS do
        // jogo carregar, porque outro mod pode recompor o metodo e derrubar o nosso prefixo.
        private void Update()
        {
            _relogio += UnityEngine.Time.unscaledDeltaTime;
            if (_relogio < 20f) return;
            _relogio = -1000f;
            try
            {
                foreach (var nome in new[] { "ToggleSelectedCharacter", "get_Level" })
                {
                    var tipo = typeof(CharacterChoiceManager);
                    if (nome == "get_Level") tipo = null;
                    var mi = nome == "get_Level"
                        ? AccessTools.Method(typeof(Character), "get_Level")
                        : AccessTools.Method(typeof(CharacterChoiceManager), "ToggleSelectedCharacter", new[] { typeof(int) });
                    if (mi == null) { Diag.Write("estado " + nome + ": metodo nulo"); continue; }
                    var info = Harmony.GetPatchInfo(mi);
                    var donos = new List<string>();
                    if (info != null)
                        foreach (var p in info.Prefixes) donos.Add("pre:" + p.owner + "@" + p.priority);
                    Diag.Write("estado " + nome + ": hooks=" + (info == null ? 0 : info.Prefixes.Count + info.Postfixes.Count)
                        + " donos=[" + string.Join(" | ", donos) + "]");
                }
            }
            catch (Exception ex) { Diag.Write("estado falhou: " + ex.GetType().Name); }
        }

        private void OnDestroy()
        {
            // NAO despatchear aqui: se o objeto for destruido/reconstruido no carregamento, o
            // UnpatchSelf derrubava todos os ganchos silenciosamente (sintoma: Awake logado e
            // nenhum hook rodando depois).
            Diag.Write("OnDestroy chamado; patches mantidos");
        }
    }
}
