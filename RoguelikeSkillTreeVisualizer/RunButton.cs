using System;
using System.Collections.Generic;
using Burst2Flame;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-5: o MESMO botao quadrado `Skills` da tela Select Party, agora no HUD da RUN, ancorado no
    /// **Ping Button** (o botao de apontar o hex) — `CurrentCharacterUI.pingBtn`, l.329889, handler
    /// `ButtonPressedPing()` l.330452. Hierarquia: GUI Manager -> In Game GUI -> Ping Button; irmaos na
    /// mesma linha: End Turn Button, End Turn Button Backup, Flee Button, Ping Button, Resume Turn Button.
    ///
    /// Como: clonar o proprio botao nativo (`Instantiate`, mesmo sprite/estados/prefab), inserir como
    /// IRMAO logo depois dele e compensar a largura da linha pelo que foi adicionado — exatamente a
    /// receita ja validada do `SelectPartyButton` (reusa `ApplySquareLayout` nos 3 modos de layout:
    /// com `childForceExpandWidth`, com grupo que controla a largura e sem layout group).
    ///
    /// O que este arquivo NAO faz de proposito:
    ///   - nao mexe no Update do HUD (`CurrentCharacterUI.UIUpdate`, l.330080, roda todo frame e mexe em
    ///     `endTurnButton`/`fleeBattleButton`): quem chama `Mirror()` e o `RstvHost.Update` do mod;
    ///   - nao abre a janela sem o portao 4 fechado (`RunTargets.GateOk`) — quando nao pode abrir, o
    ///     botao fica escondido/desabilitado e o MOTIVO vai para o log ("RSTV DIAG: ...").
    /// </summary>
    internal static class RunButton
    {
        internal const string ButtonName = "RstvRunSkillTreeButton";
        internal const string Label = "Skills";
        internal const string LabelChildName = "RstvRunLabel";

        private static CurrentCharacterUI _owner;
        private static GameObject _button;
        private static CurrentCharacterUI _triedFor;

        /// <summary>
        /// NULL-1: instante da proxima reinjecao permitida quando o clone morre com o MESMO HUD vivo
        /// (uma tentativa a cada 2 s). O `Mirror` roda 10x por segundo — sem este teto, um clone que
        /// morre a cada quadro viraria 10 injecoes por segundo.
        /// </summary>
        private static float _proximaTentativa;

        private const float IntervaloDeReinjecao = 2f;

        // Diagnostico: POR QUE o botao esta escondido agora e onde isso ja foi escrito (um mod que
        // injeta UI nao pode falhar em silencio). `_reasonLogged` guarda o ultimo motivo que foi
        // EFETIVAMENTE logado: o mesmo motivo nao se repete (mais em `Hide`/`Fail`). `_nextReasonLog`
        // so throttla o log de EXCECAO do `Mirror` — o log de motivo e por MUDANCA, nao por tempo.
        private static string _reason;
        private static string _reasonLogged;
        private static float _nextReasonLog;

        // O aviso de "clone sem rotulo" (em `EnsureLabel`) so pode repetir se a injecao se repetir;
        // guarda se ele ja foi dado e se rearma quando um rotulo volta a ser montado.
        private static bool _rotuloSemMoldeLogado;

        // ---------------------------------------------------------------------------------------
        // RSTV-11b: o level-up NAO usa mais este botao
        //
        // A RSTV-9 re-parenteava o clone do HUD para dentro do `SkillSelectWindow` enquanto a janela
        // abria. O prefab (RSTV-10) mostrou que o `SkillSelectWindow` e TELA CHEIA (o "canto" caia no
        // canto da tela, nao do painel) e que ele e o proprio GO ligado/desligado no level-up. O
        // level-up passou a ter um botao PROPRIO, filho direto da janela (`LevelUpWindowButton`,
        // RSTV-11b). A casa deste clone volta a ser SEMPRE a linha do Ping Button: o `Mirror` nao
        // muda mais de casa — so segue o original e o portao 4 (RSTV-5), intocado.
        // ---------------------------------------------------------------------------------------

        /// <summary>Idempotente por instancia de `CurrentCharacterUI` (o HUD e criado de novo a cada
        /// estado que precisa dele: l.136635 e l.136923 criam a instancia e chamam `InitSingleton`).</summary>
        internal static void Ensure(CurrentCharacterUI ui)
        {
            try
            {
                EnsureInternal(ui);
            }
            catch (Exception e)
            {
                Fail("excecao durante a injecao (" + e.GetType().Name + "): " + e.Message, true);
                Plugin.Log.LogError("RSTV: falha ao injetar o botao da run: " + e);
            }
        }

        private static void EnsureInternal(CurrentCharacterUI ui)
        {
            if (ui == null)
            {
                Fail("a instancia do HUD (CurrentCharacterUI) chegou nula", false);
                return;
            }

            if (!Plugin.RunBotaoLigado)
            {
                // Pedido explicito no config: nao e falha, e o comportamento desejado.
                Fail("AtivarBotaoNaRun=false no arquivo de config", false);
                return;
            }

            // Ancora PROVADA: o Ping Button do HUD.
            Button original = ui.pingBtn;
            if (original == null)
            {
                Fail("o botao nativo ancora (CurrentCharacterUI.pingBtn / 'Ping Button', l.329889) nao existe neste HUD", true);
                return;
            }

            if (original.transform == null || original.transform.parent == null)
            {
                Fail("o 'Ping Button' esta sem Transform ou sem pai na hierarquia", true);
                return;
            }

            if (_owner == ui && _button != null)
            {
                return;
            }

            // Um clone VIVO de outro HUD (o HUD foi recriado) viraria um SEGUNDO botao: some com o
            // antigo antes de criar o novo — o botao continua unico.
            if (_button != null && _owner != ui)
            {
                UnityEngine.Object.Destroy(_button);
                _button = null;
            }

            Transform parent = original.transform.parent;
            RectTransform srcRt = original.GetComponent<RectTransform>();
            if (srcRt == null)
            {
                Fail("o 'Ping Button' nao tem RectTransform (sem isso nao da para medir/repor a largura da linha)", true);
                return;
            }

            // MEDIR ANTES de inserir o clone: com layout group, inserir o irmao ja reflui a linha e a
            // medida tirada depois seria a largura JA encolhida (encolheria duas vezes).
            float rowBefore = SelectPartyButton.RowWidth(parent);
            float widthBefore = SelectPartyButton.WorldWidth(srcRt);
            if (widthBefore <= 1f)
            {
                widthBefore = srcRt.sizeDelta.x;
            }

            float side = SelectPartyButton.SquareSide(original, srcRt);

            Transform existing = parent.Find(ButtonName);
            GameObject clone;
            if (existing != null)
            {
                clone = existing.gameObject;
            }
            else
            {
                clone = UnityEngine.Object.Instantiate(original.gameObject, parent);
                clone.name = ButtonName;
            }

            clone.transform.SetSiblingIndex(original.transform.GetSiblingIndex() + 1);
            // escala/ancoras/rotacao vem do Instantiate (mesmo prefab) — nao mexer.

            RectTransform newRt = clone.GetComponent<RectTransform>();
            if (newRt == null)
            {
                Fail("o clone do botao ficou sem RectTransform", true);
                return;
            }

            // O nome novo nao pode ser reescrito pelos componentes de localizacao do jogo, e o icone do
            // Ping (que nao e o fundo do botao) nao deve aparecer no nosso botao.
            SelectPartyButton.DisableLocalizers(clone);
            NeutralizeInheritedVisuals(clone, original);
            EnsureLabel(clone, ui);

            clone.SetActive(original.gameObject.activeSelf);
            SelectPartyButton.ApplySquareLayout(original, srcRt, clone, newRt, side, widthBefore, parent);

            Button button = clone.GetComponent<Button>();
            if (button != null)
            {
                // RSTV-12: o Ping Button tem onClick SERIALIZADO (`ButtonPressedPing`); o
                // `RemoveAllListeners()` sozinho NAO o remove (limpa apenas a lista de runtime) e ele
                // roda ANTES do nosso. Troca a instancia do evento para descartar a lista persistente.
                SelectPartyButton.ClearClickListeners(button);
                button.onClick.AddListener(new UnityAction(OpenForTarget));
                button.interactable = false;
            }

            _owner = ui;
            _button = clone;
            _triedFor = ui;
            _reason = null;
            _reasonLogged = null;

            Plugin.Log.LogInfo(
                "RSTV-5: botao '" + Label + "' injetado no HUD (" + side.ToString("0.#") + "x" + side.ToString("0.#") +
                " px) a direita do Ping Button — largura da linha " + rowBefore.ToString("0.#") +
                " -> " + SelectPartyButton.RowWidth(parent).ToString("0.#") + " px; pai=" + parent.name +
                "; grupo=" + SelectPartyButton.DescribeGroup(parent) + ".");
        }

        /// <summary>
        /// Mantem o botao em sincronia com o original (visibilidade e interactable), com o portao 4
        /// E com o portao 4 (RSTV-5). A CASA do clone e SEMPRE a linha do Ping Button (RSTV-11b: o
        /// level-up nao muda mais o botao de lugar — quem atende o level-up e o `LevelUpWindowButton`,
        /// filho da propria janela). Chamado pelo `RstvHost.Update` do mod (nunca pelo Update do HUD).
        /// </summary>
        internal static void Mirror()
        {
            try
            {
                CurrentCharacterUI ui = CurrentCharacterUI.Instance;
                if (ui == null)
                {
                    return;
                }

                if (!Plugin.RunBotaoLigado)
                {
                    Hide("AtivarBotaoNaRun=false no arquivo de config", false);
                    return;
                }

                if (_button == null)
                {
                    // NULL-1: `_button == null` com o operador da Unity significa "o clone FOI
                    // DESTRUIDO" (fake null) — o campo ESTA preenchido, o objeto e que morreu. Em HUD
                    // NOVO a tentativa e imediata (uma por instancia, `_triedFor`); com o MESMO HUD
                    // (o clone morreu por fora, cena/refresh da hierarquia) o mod REINJETA, no maximo
                    // uma vez a cada 2 s. Antes ele saia daqui CALADO: o gancho disparava, via o clone
                    // morto e nao deixava rastro nenhum no log — o botao sumia para sempre naquele HUD.
                    if (_triedFor == ui && Time.realtimeSinceStartup < _proximaTentativa)
                    {
                        return;
                    }

                    _proximaTentativa = Time.realtimeSinceStartup + IntervaloDeReinjecao;
                    if (_triedFor == ui)
                    {
                        // Fail() escreve UMA vez por motivo (nao a cada 0,1 s) e `Ensure` abaixo ou
                        // devolve o botao ou escreve o motivo proprio da falha.
                        Fail("o clone do botao foi DESTRUIDO com o mesmo HUD ainda vivo (fake null) " +
                             "— reinjetando (uma tentativa a cada 2 s)", true);
                    }

                    Ensure(ui);
                    if (_button == null)
                    {
                        return;
                    }
                }

                if (_owner != ui)
                {
                    return;
                }

                Button original = ui.pingBtn;
                if (original == null)
                {
                    Hide("o 'Ping Button' nativo sumiu do HUD", true);
                    return;
                }

                string motivo;
                bool podeAbrir = RunTargets.GateOk(out motivo);

                Character alvo = null;
                if (podeAbrir)
                {
                    alvo = RunTargets.Resolve(out motivo);
                }

                if (!podeAbrir || alvo == null)
                {
                    Hide(motivo != null ? motivo : "sem alvo local na party", true);
                    return;
                }

                if (_button.activeSelf != original.gameObject.activeSelf)
                {
                    // Segue o original (contrato da RSTV-5).
                    _button.SetActive(original.gameObject.activeSelf);
                }

                Button button = _button.GetComponent<Button>();
                if (button != null && !button.interactable)
                {
                    button.interactable = true;
                }

                if (_reasonLogged != null)
                {
                    _reasonLogged = null;
                    _reason = null;
                    Plugin.Log.LogInfo("RSTV DIAG: botao '" + Label + "' do HUD VISIVEL e clicavel — alvo '" +
                                       alvo.CharacterName + "' (nivel " + alvo.Level + ").");
                }
            }
            catch (Exception e)
            {
                if (Time.realtimeSinceStartup < _nextReasonLog)
                {
                    return;
                }

                _nextReasonLog = Time.realtimeSinceStartup + 5f;
                Plugin.Log.LogError("RSTV: falha no Mirror do botao da run: " + e);
            }
        }

        // ---------------------------------------------------------------------------------------
        // RSTV-11b: a CASA do botao deixou de existir
        //
        // O `CaptureHome`/`HomeInLevelUp`/`HomeInRow` da RSTV-9 (e os campos `_home*` e as constantes
        // `LadoMinimoLevelUp`/`MargemLevelUp`) foram REMOVIDOS: o level-up passou a ser atendido por um
        // botao proprio, filho direto da janela (`LevelUpWindowButton`). Este clone vive SEMPRE na
        // linha do Ping Button — o `Mirror` acima so segue o original e o portao 4.
        // ---------------------------------------------------------------------------------------

        /// <summary>
        /// Esconde/desabilita o botao e escreve no log POR QUE. Avisa UMA vez por MOTIVO: guarda o
        /// ultimo motivo logado (`_reasonLogged`) e so volta a escrever quando o motivo MUDA — a
        /// mesma estrategia do `AvisoUma` do BetterCombatText. Sem isso, um estado estavel fora da
        /// whitelist (ex.: ChoosingCharacter) re-loga o texto identico a cada janela de 5 s: numa
        /// sessao isso rendeu 275 linhas iguais. O botao continua escondido do mesmo jeito — muda so
        /// a frequencia do log.
        /// </summary>
        private static void Hide(string motivo, bool aviso)
        {
            _reason = motivo;

            try
            {
                if (_button != null && _button.activeSelf)
                {
                    _button.SetActive(false);
                }

                if (_button != null)
                {
                    Button button = _button.GetComponent<Button>();
                    if (button != null && button.interactable)
                    {
                        button.interactable = false;
                    }
                }
            }
            catch (Exception)
            {
                // o clone pode ter sido destruido junto com a cena; o log abaixo ainda vale
            }

            if (_reasonLogged == motivo)
            {
                return;
            }

            _reasonLogged = motivo;

            string linha = "RSTV DIAG: botao '" + Label + "' do HUD escondido — " + motivo + ".";
            if (aviso)
            {
                Plugin.Log.LogWarning(linha);
            }
            else
            {
                Plugin.Log.LogInfo(linha);
            }
        }

        private static void Fail(string motivo, bool aviso)
        {
            _reason = motivo;
            if (_reasonLogged == motivo)
            {
                return;
            }

            _reasonLogged = motivo;
            if (aviso)
            {
                Plugin.Log.LogWarning("RSTV DIAG: botao '" + Label + "' da run NAO injetado — " + motivo + ".");
            }
            else
            {
                Plugin.Log.LogInfo("RSTV DIAG: botao '" + Label + "' da run desativado — " + motivo + ".");
            }
        }

        /// <summary>
        /// RSTV-11b/RSTV-16: o corpo de abertura da visualizacao read-only pelo INVENTARIO — o portao 4
        /// ja validado (`RunTargets.GateOk`) -> o alvo resolvido na hora (`RunTargets.Resolve`, nunca
        /// cacheado) -> `SkillTreesTab.Abrir(alvo, Run)` (a aba "All Skill Trees" do inventario, que
        /// aposentou a antiga janela NATIVA separada da RSTV-15). Extraido do antigo `OnClick` para ser
        /// REUSADO por tres interlocutores, sem duplicar a logica: o botao do HUD (`RunButton`), o botao
        /// DENTRO da janela do level-up (`LevelUpWindowButton`) e o atalho de teclado (`SkillTreeShortcut`).
        /// NAO e o unico caminho: o RSTV-21 tem um SEGUNDO corpo de abertura,
        /// `RemovalWindowSkillsButton.OnClick` -> `SkillTreesTab.AbrirJanela`, que usa o alvo do proprio
        /// modal (CurrentCharacter) e NAO passa por aqui nem pelo `RunTargets`. Idempotente e sem estado:
        /// se o portao recusar ou nao houver alvo, so loga o motivo e nao abre nada.
        /// </summary>
        internal static void OpenForTarget()
        {
            try
            {
                string motivo;
                if (!RunTargets.GateOk(out motivo))
                {
                    // RECUSA: reavalia na hora (o portao tambem esconde o botao; aqui e a rede final).
                    Plugin.Log.LogWarning("RSTV-5: abertura RECUSADA — " + motivo + ". Nada foi aberto.");
                    return;
                }

                Character alvo = RunTargets.Resolve(out motivo);
                if (alvo == null)
                {
                    Plugin.Log.LogWarning("RSTV-5: abertura sem alvo — " + motivo + ".");
                    return;
                }

                Plugin.Log.LogInfo("RSTV-16: abrindo a visualizacao read-only -> '" + alvo.CharacterName +
                                   "' (nivel " + alvo.Level + ") na aba 'All Skill Trees' do inventario.");
                SkillTreesTab.Abrir(alvo, ReadOnlyContext.Run);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao abrir a skill tree da run: " + e);
            }
        }

        // ---------------------------------------------------------------------------------------
        // Aparencia do clone
        // ---------------------------------------------------------------------------------------

        /// <summary>
        /// O Ping Button e um botao de ICONE. O fundo do botao (`Button.targetGraphic`) fica; os outros
        /// graficos (o icone do ping) sao desligados no clone para o nosso botao nao mostrar o simbolo
        /// errado. Tudo o que for mexido vai para o log, porque o prefab nao foi aberto.
        /// </summary>
        private static void NeutralizeInheritedVisuals(GameObject clone, Button original)
        {
            try
            {
                // ATENCAO: o `targetGraphic` do ORIGINAL e um componente do ORIGINAL — o clone tem a
                // COPIA dele. Por isso o alvo e lido do Button DO CLONE (senao o fundo do nosso botao
                // tambem seria desligado e ele ficaria invisivel).
                Button cloneButton = clone.GetComponent<Button>();
                Graphic fundo = cloneButton != null ? cloneButton.targetGraphic : null;
                if (fundo == null && original != null)
                {
                    fundo = original.targetGraphic;
                }

                Graphic[] graficos = clone.GetComponentsInChildren<Graphic>(true);
                int desligados = 0;
                List<string> mantidos = new List<string>();
                for (int i = 0; i < graficos.Length; i++)
                {
                    Graphic g = graficos[i];
                    if (g == null || g is TextMeshProUGUI)
                    {
                        continue;
                    }

                    // manter: o fundo do botao E qualquer grafico no PROPRIO objeto do botao (o fundo
                    // costuma viver no root; desligar errado deixaria o botao invisivel, que e pior que
                    // um icone errado). Tudo o que for decidido vai para o log.
                    if (g == fundo || g.transform == clone.transform)
                    {
                        mantidos.Add(g.GetType().Name + " em '" + g.gameObject.name + "'");
                        continue;
                    }

                    g.enabled = false;
                    desligados++;
                }

                Plugin.Log.LogInfo("RSTV-5: aparencia do clone do HUD — graficos herdados desligados: " +
                                   desligados + "; mantidos: " +
                                   (mantidos.Count > 0 ? string.Join(", ", mantidos.ToArray()) : "nenhum") +
                                   " (targetGraphic do clone: " +
                                   (fundo != null ? fundo.GetType().Name + " em '" + fundo.gameObject.name + "'" : "nenhum") +
                                   "). Se o icone do Ping continuar aparecendo, este log diz qual grafico e.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para limpar a aparencia do clone (" + e.Message + ").");
            }
        }

        /// <summary>
        /// Rotulo `Skills` localizado. Se o Ping Button nao tiver texto proprio (botao de icone), um
        /// rotulo e criado a partir de outro texto do MESMO HUD (`chooseSkillsBtn` -> `skillsBtn` ->
        /// `fleeBattleButton` -> qualquer TMP), para herdar fonte/material/estilo do jogo. Sem nenhum
        /// texto doador, o botao fica so com o fundo — e o log diz isso.
        /// </summary>
        private static void EnsureLabel(GameObject clone, CurrentCharacterUI ui)
        {
            try
            {
                TextMeshProUGUI label = clone.GetComponentInChildren<TextMeshProUGUI>(true);
                if (label != null)
                {
                    label.text = OptionsManager.Localize(Label);
                    _rotuloSemMoldeLogado = false;
                    return;
                }

                TextMeshProUGUI doador = FindLabelDonor(ui);
                if (doador == null)
                {
                    if (_rotuloSemMoldeLogado)
                    {
                        return;
                    }

                    _rotuloSemMoldeLogado = true;
                    Plugin.Log.LogWarning("RSTV DIAG: o clone do botao da run ficou SEM rotulo — nao ha " +
                                          "TextMeshProUGUI nem no Ping Button nem em nenhum botao do HUD para servir de molde.");
                    return;
                }

                GameObject rotulo = UnityEngine.Object.Instantiate(doador.gameObject, clone.transform);
                rotulo.name = LabelChildName;
                SelectPartyButton.DisableLocalizers(rotulo);

                RectTransform rt = rotulo.GetComponent<RectTransform>();
                if (rt != null)
                {
                    rt.anchorMin = Vector2.zero;
                    rt.anchorMax = Vector2.one;
                    rt.offsetMin = Vector2.zero;
                    rt.offsetMax = Vector2.zero;
                    rt.localScale = Vector3.one;
                }

                TextMeshProUGUI novo = rotulo.GetComponent<TextMeshProUGUI>();
                if (novo != null)
                {
                    novo.text = OptionsManager.Localize(Label);
                    novo.alignment = TextAlignmentOptions.Center;
                    novo.enableAutoSizing = true;
                    novo.fontSizeMin = 6f;
                    if (novo.fontSizeMax <= 0f || novo.fontSizeMax > 24f)
                    {
                        novo.fontSizeMax = 24f;
                    }
                }

                Plugin.Log.LogInfo("RSTV-5: o Ping Button nao tem texto — o rotulo '" + Label + "' foi criado a " +
                                   "partir do molde '" + doador.gameObject.name + "' (mesma fonte/estilo do jogo).");
                _rotuloSemMoldeLogado = false;
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para montar o rotulo do botao da run (" + e.Message + ").");
            }
        }

        private static TextMeshProUGUI FindLabelDonor(CurrentCharacterUI ui)
        {
            TextMeshProUGUI doador = LabelOf(ui.chooseSkillsBtn);
            if (doador != null)
            {
                return doador;
            }

            doador = LabelOf(ui.skillsBtn);
            if (doador != null)
            {
                return doador;
            }

            doador = LabelOf(ui.fleeBattleButton);
            if (doador != null)
            {
                return doador;
            }

            TextMeshProUGUI[] todos = ui.GetComponentsInChildren<TextMeshProUGUI>(true);
            for (int i = 0; i < todos.Length; i++)
            {
                if (todos[i] != null && todos[i].transform.parent != null && todos[i].gameObject.activeSelf)
                {
                    return todos[i];
                }
            }

            return null;
        }

        private static TextMeshProUGUI LabelOf(Button button)
        {
            return button != null ? button.GetComponentInChildren<TextMeshProUGUI>(true) : null;
        }
    }
}
