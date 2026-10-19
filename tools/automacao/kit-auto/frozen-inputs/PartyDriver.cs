// KIT-14F2: explicit route tokens, native handlers only, no owner save seed.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using UnityEngine;
using UnityEngine.UI;

namespace Aut4Probe
{
    public partial class Aut4ProbePlugin
    {
        private string _partyUltimoEstado;
        private bool _partyHudPngRequested;
        private readonly HashSet<object> _partyInvocados = new HashSet<object>();

        // Pure shared decision for offline regressions and live candidate filtering.
        internal static string PartyBlock(bool managerActive, bool blocked, bool tileActive,
            bool tileReady, bool owned, bool deleted, bool dead, bool selected, int eligible, int party)
        {
            if (!managerActive) return "manager_inativo";
            if (blocked) return "modal_ou_inputBlocker";
            if (party != 0) return "party_ja_selecionada";
            if (eligible != 1) return "personagem_ausente_ou_ambiguo";
            if (!tileActive) return "tile_inativo";
            if (!tileReady) return "tile_Start_pendente";
            if (!owned) return "personagem_nao_local";
            if (deleted || dead) return "personagem_invalido";
            if (selected) return "ja_selecionado_nao_togglar";
            return null;
        }

        private static int PartyCount(object value)
            => value is IEnumerable en ? en.Cast<object>().Count() : -1;

        private void PartyLog(Dictionary<string, object> data)
        {
            _res["party_driver"] = data;
            string state = Json.Serialize(data);
            if (state == _partyUltimoEstado) return;
            _partyUltimoEstado = state;
            MarcoClique("PARTY " + state + " quadro=" + QuadroTxt() + " t=" + TempoTxt());
        }

        private void AdicionarSeletorParty(List<(string rotulo, bool ativo, Action invocar)> list,
            List<bool> clickable, List<string> reasons, List<GameObject> objects)
        {
            // Only explicitly requested stages activate this additional write-capable driver.
            string stage = _rota != null && _rotaEtapa < _rota.Count ? _rota[_rotaEtapa] : null;
            if (stage == null && _rota != null && _rota.Contains("@PartyCharacter"))
            {
                var gm = Estatico(Tipo("GUIManager"), "instance");
                var gl = Estatico(Tipo("GameLogic"), "instance");
                var net = Estatico(Tipo("NetworkingManager"), "Instance");
                var root = Membro(Membro(net, "NetworkManager"), "Root");
                var hud = Estatico(Tipo("CurrentCharacterUI"), "Instance") as Component;
                var debug = Tipo("DebugWindow");
                var loading = Estatico(Tipo("LoadingScreen"), "Instance");
                if (!_partyHudPngRequested && hud != null && hud.gameObject.activeInHierarchy
                    && _outDir != null)
                {
                    string path = System.IO.Path.Combine(_outDir.Value, "00-hud.png");
                    ScreenCapture.CaptureScreenshot(path);
                    _res["party_hud_capture"] = Json.Campos("path", path, "requested_frame", QuadroTxt(),
                        "note", "native Unity screenshot; file existence verified by external driver");
                    _partyHudPngRequested = true;
                }
                PartyLog(Json.Campos("stage", "hud_wait", "gui", Membro(gm, "CurrentGuiState")?.ToString(),
                    "current_character", Membro(Membro(gl, "CurrentlySelectedCharacter"), "CharacterName"),
                    "my_party", PartyCount(Membro(net, "MyPartyCharacters")),
                    "my_party_unaccepted", PartyCount(Membro(net, "MyPartyCharactersUnaccepted")),
                    "hud_exists", hud != null, "hud_active", hud != null && hud.gameObject.activeInHierarchy,
                    "hide_basic_ui", Estatico(debug, "HideBasicUI"),
                    "hide_character_buttons", Membro(root, "HideCharacterButtons"),
                    "main_fade", Membro(loading, "MainFadeActive"),
                    "game_started", Membro(gl, "GameStarted")));
            }
            if (stage == "@HudInitialize")
            {
                var gm = Estatico(Tipo("GUIManager"), "instance");
                var gl = Estatico(Tipo("GameLogic"), "instance");
                var net = Estatico(Tipo("NetworkingManager"), "Instance");
                var loading = Estatico(Tipo("LoadingScreen"), "Instance");
                string gui = Membro(gm, "CurrentGuiState")?.ToString();
                bool hudReady = gui == "InWorldMap" && PartyCount(Membro(net, "MyPartyCharacters")) == 1
                    && Membro(gl, "CurrentlySelectedCharacter") != null
                    && Equals(Membro(loading, "MainFadeActive"), false);
                PartyLog(Json.Campos("stage", stage, "gui", gui, "ready", hudReady,
                    "mechanism", "CurrentCharacterUI.ForcedInstance native lazy accessor"));
                list.Add((stage, hudReady, () => {
                    // PlayerMovement.Update normally loads this on first left input before
                    // ProcessLeftMouseClick. Use the same native loader and initialization, no SetActive.
                    var before = Estatico(Tipo("CurrentCharacterUI"), "Instance") as Component;
                    var native = Estatico(Tipo("CurrentCharacterUI"), "ForcedInstance") as Component;
                    if (native == null) throw new InvalidOperationException("Native HUD loader returned null");
                    // LoadingScreen.LoadReferences normally performs this exactly once after
                    // InstantiateReferenceObject; lazy getter alone omits the native initialization.
                    if (before == null) native.GetType().GetMethod("InitSingleton", Type.EmptyTypes).Invoke(native, null);
                    MarcoClique("HUD_INITIALIZED accessor=CurrentCharacterUI.ForcedInstance InitSingleton="
                        + (before == null) + " path=" + CaminhoDoObjeto(native.gameObject) + " quadro=" + QuadroTxt());
                }));
                clickable.Add(hudReady); reasons.Add(hudReady ? null : "aguardando_run_carregada"); objects.Add(null);
                return;
            }
            if (stage != "@PartyCharacter" && stage != "@PartyAccept") return;
            var manager = Estatico(Tipo("CharacterChoiceManager"), "Instance") as Component;
            bool active = manager != null && manager.gameObject.activeInHierarchy;
            var network = Estatico(Tipo("NetworkingManager"), "Instance");
            int party = PartyCount(Membro(network, "MyPartyCharactersUnaccepted"));
            var data = Json.Campos("stage", stage, "manager_active", active,
                "party_count", party, "mechanism", "native_handler", "physical_click", false);
            if (!active) { PartyLog(data); return; }
            var blocker = Membro(manager, "inputBlocker") as GameObject;
            var rename = Membro(manager, "renameCharacterWindow") as GameObject;
            bool blocked = blocker == null || blocker.activeInHierarchy
                || rename == null || rename.activeInHierarchy
                || !Equals(Membro(manager, "HasPendingSkillTreeRemovalPrompt"), false);
            var accept = Membro(manager, "acceptBtn") as Button;
            data["input_blocked"] = blocked;
            data["accept_interactable"] = accept != null && accept.IsInteractable();
            if (stage == "@PartyAccept")
            {
                string reason = party < 1 ? "party_vazia_ou_ausente" : blocked ? "modal_ou_inputBlocker"
                    : MotivoDeBloqueio(accept, true, true);
                if (accept == null) reason = "accept_ausente";
                data["block_reason"] = reason;
                PartyLog(data);
                if (accept == null) return;
                list.Add((stage, accept.gameObject.activeInHierarchy, () => {
                    // Recheck at dispatch, not just at enumeration.
                    if (PartyCount(Membro(network, "MyPartyCharactersUnaccepted")) < 1
                        || MotivoDeBloqueio(accept, true, true) != null)
                        throw new InvalidOperationException("Party Accept changed before dispatch");
                    MarcoClique("PARTY_ACCEPT handler=Button.onClick party=" + party);
                    accept.onClick.Invoke();
                }));
                clickable.Add(reason == null); reasons.Add(reason); objects.Add(accept.gameObject);
                return;
            }
            var holder = Membro(manager, "notInPartyHolder") as Transform;
            var type = Tipo("CharacterChoiceItem");
            if (holder == null || type == null) { data["block_reason"] = "holder_ou_tipo_ausente"; PartyLog(data); return; }
            var tiles = holder.GetComponentsInChildren(type, false).Cast<Component>()
                .Where(c => Membro(c, "Character") != null).ToList();
            data["eligible_tiles"] = tiles.Count;
            if (tiles.Count != 1) { data["block_reason"] = "personagem_ausente_ou_ambiguo"; PartyLog(data); return; }
            var tile = tiles[0];
            var character = Membro(tile, "Character");
            bool tileReady = ReferenceEquals(Membro(tile, "manager"), manager);
            bool owned = Equals(Membro(character, "Owned"), true);
            bool deleted = !Equals(Membro(character, "IsDeleted"), false);
            bool dead = !Equals(Membro(character, "HardcoreDeath"), false);
            bool selected = !Equals(Membro(character, "SelectedForBattle"), false);
            string why = PartyBlock(active, blocked, tile.gameObject.activeInHierarchy && ((Behaviour)tile).isActiveAndEnabled,
                tileReady, owned, deleted, dead, selected, tiles.Count, party);
            for (var tr = tile.transform; tr != null && why == null; tr = tr.parent)
                foreach (var cg in tr.GetComponents<CanvasGroup>())
                    if (!cg.interactable || !cg.blocksRaycasts) { why = "CanvasGroup_bloqueado"; break; }
            if (_partyInvocados.Contains(character)) why = "handler_ja_invocado_aguardando_efeito";
            data["character_name"] = Membro(character, "CharacterName");
            data["selected_for_battle"] = selected;
            data["tile_manager_ready"] = tileReady;
            data["tile_path"] = CaminhoDoObjeto(tile.gameObject);
            data["block_reason"] = why;
            PartyLog(data);
            var mouseDown = type.GetMethod("MouseDown", new[] { typeof(int) });
            if (mouseDown == null) return;
            list.Add((stage, tile.gameObject.activeInHierarchy, () => {
                if (!Equals(Membro(character, "SelectedForBattle"), false)
                    || PartyCount(Membro(network, "MyPartyCharactersUnaccepted")) != 0)
                    throw new InvalidOperationException("Party changed before selection; refuse toggle");
                _partyInvocados.Add(character);
                mouseDown.Invoke(tile, new object[] { 0 });
                MarcoClique("PARTY_SELECTED handler=CharacterChoiceItem.MouseDown(0) name="
                    + Membro(character, "CharacterName") + " selected=" + Membro(character, "SelectedForBattle")
                    + " party_after=" + PartyCount(Membro(network, "MyPartyCharactersUnaccepted")));
            }));
            clickable.Add(why == null); reasons.Add(why); objects.Add(tile.gameObject);
        }
    }
}
