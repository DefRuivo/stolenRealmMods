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
    /// RSTV-30 (06/10, pedido do dono EM JOGO): o botao quadrado `Skills` da RUN.
    ///
    /// ONDE ELE MORA AGORA: na BARRA DE BAIXO do HUD, na MESMA linha dos botoes nativos
    /// `Character Btn` (o de INVENTARIO — `CurrentCharacterUI.characterBtn`, que chama
    /// `ButtonPressedCharacter`) e `Skills Tree Btn` (o de SKILLS — `CurrentCharacterUI.skillsBtn`,
    /// que chama `ButtonPressedSkillTree`), no VAO LIVRE medido entre essa linha e o
    /// `Skillbar Index Controls` — o controle nativo que ROTACIONA a barra de skills (`Up`/`Down`
    /// chamam `Skillbar.IncrementSkillbarIndex`). Os nomes e a ordem dos irmaos foram LIDOS do prefab
    /// do HUD (`resources.assets`, `Current Character UI` [556345] -> `Skillbar Layout PC` [526615] ->
    /// `Skillbar Buttons` [526621]); a procedencia de cada numero esta em
    /// `docs/RSTV-30-botao-na-barra-de-baixo.md`.
    ///
    /// POR QUE A MUDANCA: ate a RSTV-29 o clone ficava na linha do `Ping Button` (o canto do
    /// end-turn), longe dos botoes com que o jogador compara, e a VISIBILIDADE dele seguia o portao
    /// de estado — o dono relatou que o botao "some e depois reaparece" quando qualquer personagem
    /// age e que ele "nao aparece enquanto estamos fora de combate". As duas coisas eram as guardas
    /// da run escondendo o botao (ver o cabecalho de `RunTargets`).
    ///
    /// COMO (e o que este arquivo NAO faz):
    ///   - MOLDE: um botao NATIVO da MESMA linha — `ui.skillsBtn` (o `Skills Tree Btn`), com
    ///     fallback em `characterBtn` e depois no `pingBtn`. Clonar o vizinho herda sprite, estados
    ///     e fundo do jogo, como nas outras superficies do mod. O `onClick` SERIALIZADO do molde e
    ///     descartado do jeito da RSTV-12: troca da INSTANCIA do evento
    ///     (`NativeUiHelpers.ClearClickListeners`) ANTES de instalar o nosso listener — no molde novo
    ///     a persistente chama `ButtonPressedSkillTree` (abriria a arvore ESCRITIVEL nativa);
    ///   - NAO ENCOLHE, NAO MOVE E NAO SOBREPOE NENHUM BOTAO NATIVO: a posicao sai de MEDIDAS de
    ///     runtime (bordas do molde, borda direita dos irmaos da linha e borda esquerda do vizinho da
    ///     direita) e o clone entra com `LayoutElement.ignoreLayout = true`, entao o
    ///     `HorizontalLayoutGroup` do container NAO reflui por causa dele. Nao existe pixel chutado:
    ///     o codigo nao tem posicao fixa — ele mede e escreve no log cada numero usado;
    ///   - APARENCIA: fundo do botao + o ICONE nativo (`Icon (2)`), que e o glifo da propria arvore
    ///     de skills. O vao livre medido e mais estreito que um botao nativo, e a esse tamanho um
    ///     glifo le melhor que um rotulo — por isso o clone NAO ganha o texto 'Skills' (o hover
    ///     nativo continua identificando o botao). O "badge" de pontos nao gastos (filho `Text BG`) e
    ///     desligado: o mod nao conta pontos;
    ///   - VISIBILIDADE (RSTV-30): quem manda e o HUD. O clone e filho da barra de baixo, entao ele
    ///     sai de cena junto com o HUD quando o JOGO desliga o HUD (`GUIManager.Update`, l.120485:
    ///     janela de evento, level-up aberto, loja, `ChoosingCharacter`, `CreatingCharacter`,
    ///     `InMainMenu`) e volta junto. Nenhuma guarda de estado esconde o botao — o que sobra de
    ///     guarda decide so o CLIQUE (abaixo);
    ///   - CLIQUE: `interactable` = a regra NATIVA do jogo para o botao 'Skills' do HUD
    ///     (`GUIManager.Update` l.120491: `CurrentGuiState` em InTown/InWorldMap/InCutscene/InBattle e
    ///     `!Root.HideCharacterButtons`) E o portao da run (`RunTargets.GateOk`), que agora so decide
    ///     se o clique pode ABRIR. Quando o portao recusa, o botao CONTINUA VISIVEL, apenas sem
    ///     clique, e o motivo vai para o log — esconder era o defeito que o dono relatou.
    ///
    /// O que este arquivo continua NAO fazendo de proposito: nao mexe no `Update` do HUD
    /// (`CurrentCharacterUI.UIUpdate`, l.330080, roda todo frame e mexe em
    /// `endTurnButton`/`fleeBattleButton`) — quem chama `Mirror()` e o `RstvHost.Update` do mod.
    /// </summary>
    internal static class RunButton
    {
        internal const string ButtonName = "RstvRunSkillTreeButton";
        internal const string Label = "Skills";
        internal const string LabelChildName = "RstvRunLabel";

        /// <summary>Respiro (px) entre o nosso botao e as DUAS bordas do vao livre medido em runtime.
        /// Nao e posicao: e a folga que garante que a medida nunca encoste nos vizinhos.</summary>
        private const float Margem = 2f;

        /// <summary>Largura minima aceitavel (px) do botao quando o vao medido for menor que isso
        /// (resolucao diferente, linha mais apertada). Abaixo disto o clique fica desconfortavel.</summary>
        private const float LarguraMinima = 10f;

        private static CurrentCharacterUI _owner;
        private static GameObject _button;

        /// <summary>O botao NATIVO da barra de baixo que serve de molde/oraculo do clone (RSTV-30).
        /// E dele que saem a aparencia, o rect de referencia e o estado nativo de clique.</summary>
        private static Button _mold;

        private static CurrentCharacterUI _triedFor;

        /// <summary>
        /// NULL-1: instante da proxima reinjecao permitida quando o clone morre com o MESMO HUD vivo
        /// (uma tentativa a cada 2 s). O `Mirror` roda 10x por segundo — sem este teto, um clone que
        /// morre a cada quadro viraria 10 injecoes por segundo.
        /// </summary>
        private static float _proximaTentativa;

        private const float IntervaloDeReinjecao = 2f;

        // Diagnostico: POR QUE o botao esta escondido ou sem clique agora, e onde isso ja foi escrito
        // (um mod que injeta UI nao pode falhar em silencio). `_reasonLogged` guarda o ultimo motivo
        // que foi EFETIVAMENTE logado: o mesmo motivo nao se repete. `_nextReasonLog` so throttla o
        // log de EXCECAO do `Mirror` — o log de motivo e por MUDANCA, nao por tempo.
        private static string _reason;
        private static string _reasonLogged;
        private static float _nextReasonLog;

        /// <summary>RSTV-30: o botao passou a ser SEMPRE visivel com a barra de baixo, entao o estado
        /// que muda (e que se loga por transicao) e o CLIQUE, nao a presenca.</summary>
        private static bool _clicavelLogado;

        /// <summary>Idempotente por instancia de `CurrentCharacterUI` (o HUD e criado de novo a cada
        /// estado que precisa dele: l.136635 e l.136923 criam a instancia e chamam `InitSingleton`).
        /// Idempotente tambem por MOLDE: se o jogo trocar o botao nativo da linha, o clone e refeito.</summary>
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
                // Pedido explicito no config: nao e falha, e o comportamento desejado. RSTV-29F: o
                // motivo nomeia a chave que DE FATO desligou (a mestra AtivarBotao ou a especifica).
                Fail(Plugin.MotivoDoBotaoDaRunDesligado, false);
                return;
            }

            string origemDoMolde;
            Button molde = EscolherMolde(ui, out origemDoMolde);
            if (molde == null)
            {
                Fail("nenhum botao nativo da barra de baixo serve de molde " +
                     "(CurrentCharacterUI.skillsBtn / characterBtn / pingBtn ausentes)", true);
                return;
            }

            if (molde.transform == null || molde.transform.parent == null)
            {
                Fail("o botao nativo molde '" + molde.name + "' esta sem Transform ou sem pai na hierarquia", true);
                return;
            }

            if (_owner == ui && _button != null && _mold == molde)
            {
                return;
            }

            // Um clone VIVO de outro HUD (ou de outro molde) viraria um SEGUNDO botao: some com o
            // antigo antes de criar o novo — o botao continua unico.
            if (_button != null && (_owner != ui || _mold != molde))
            {
                UnityEngine.Object.Destroy(_button);
                _button = null;
            }

            // O CONTAINER real (medido em runtime): o pai do botao nativo da linha. No prefab e o
            // 'Skillbar Buttons' [526621] — o mesmo container dos botoes de inventario e de skills.
            Transform parent = molde.transform.parent;

            RectTransform srcRt = molde.GetComponent<RectTransform>();
            if (srcRt == null)
            {
                Fail("o botao nativo molde '" + molde.name + "' nao tem RectTransform (sem ele nao da " +
                     "para medir o vao livre)", true);
                return;
            }

            Transform existing = parent.Find(ButtonName);
            GameObject clone;
            if (existing != null)
            {
                clone = existing.gameObject;
            }
            else
            {
                clone = UnityEngine.Object.Instantiate(molde.gameObject, parent);
                clone.name = ButtonName;
            }

            // A ORDEM dos irmaos nao desloca nada: a posicao vem do rect (medido abaixo) e o clone
            // entra por ULTIMO so para nao ficar no meio dos indices dos botoes nativos.
            clone.transform.SetAsLastSibling();

            // O `HorizontalLayoutGroup` do container dimensiona/posiciona os filhos DELE: um filho com
            // `ignoreLayout` sai dessa conta por inteiro — e o que garante "nao empurrar os botoes
            // nativos" (nenhum deles muda de tamanho nem de posicao).
            LayoutElement elemento = clone.GetComponent<LayoutElement>();
            if (elemento == null)
            {
                elemento = clone.AddComponent<LayoutElement>();
            }

            elemento.ignoreLayout = true;

            NativeUiHelpers.DisableLocalizers(clone);
            AparenciaDoClone(clone);

            RectTransform newRt = clone.GetComponent<RectTransform>();
            if (newRt == null)
            {
                Fail("o clone do botao ficou sem RectTransform", true);
                return;
            }

            string medidas;
            ColocarNaLinha(parent, srcRt, newRt, out medidas);

            clone.SetActive(molde.gameObject.activeSelf);

            Button button = clone.GetComponent<Button>();
            if (button != null)
            {
                // RSTV-12: o botao molde tem onClick SERIALIZADO (`ButtonPressedSkillTree`, no
                // `skillsBtn`); o `RemoveAllListeners()` sozinho NAO o remove (limpa apenas a lista de
                // runtime) e ele roda ANTES do nosso. Troca a instancia do evento para descartar a
                // lista persistente.
                NativeUiHelpers.ClearClickListeners(button);
                button.onClick.AddListener(new UnityAction(OpenForTarget));
                button.interactable = false;
            }

            _owner = ui;
            _button = clone;
            _mold = molde;
            _triedFor = ui;
            _reason = null;
            _reasonLogged = null;
            _clicavelLogado = false;

            Plugin.Log.LogInfo("RSTV-30: botao '" + Label + "' injetado na BARRA DE BAIXO do HUD (" +
                               medidas + "); pai=" + parent.name + " (o container dos botoes de " +
                               "inventario e de skills); molde=" + origemDoMolde + "; grupo do pai=" +
                               NativeUiHelpers.DescribeGroup(parent) +
                               " — o clone esta com ignoreLayout, entao o grupo NAO reflui por nossa causa.");
        }

        /// <summary>
        /// O molde e um botao NATIVO da MESMA linha em que o clone vai morar. Preferencia pelo
        /// `skillsBtn` (o `Skills Tree Btn`: e o botao do mesmo assunto — a arvore de skills — e e o
        /// irmao imediato a esquerda do vao livre). Fallbacks documentados: `characterBtn` (o de
        /// inventario, tambem da linha) e, em ultimo caso, o `pingBtn` da RSTV-5 (aparece em qualquer
        /// HUD em que os outros dois nao existam).
        /// </summary>
        private static Button EscolherMolde(CurrentCharacterUI ui, out string origem)
        {
            if (ui.skillsBtn != null && ui.skillsBtn.transform != null)
            {
                origem = "CurrentCharacterUI.skillsBtn ('Skills Tree Btn' da barra de baixo)";
                return ui.skillsBtn;
            }

            if (ui.characterBtn != null && ui.characterBtn.transform != null)
            {
                origem = "CurrentCharacterUI.characterBtn (fallback: 'Character Btn', a mesma linha)";
                return ui.characterBtn;
            }

            if (ui.pingBtn != null && ui.pingBtn.transform != null)
            {
                origem = "CurrentCharacterUI.pingBtn (ultimo fallback: o molde da RSTV-5)";
                return ui.pingBtn;
            }

            origem = null;
            return null;
        }

        /// <summary>
        /// Mantem o botao em sincronia com o nativo e com o portao da run. Chamado pelo
        /// `RstvHost.Update` (nunca pelo Update do HUD).
        ///
        /// RSTV-30 — a separacao que conserta o defeito do dono:
        ///   * VISIBILIDADE: nao ha guarda de estado nenhuma. O clone e filho da barra de baixo, entao
        ///     aparece/some junto com o HUD (decisao do JOGO, `GUIManager.Update` l.120485). A unica
        ///     coisa espelhada e o proprio botao nativo (se o jogo esconder so ele);
        ///   * CLIQUE: o portao (`RunTargets.GateOk`) e o estado nativo do botao decidem apenas o
        ///     `interactable`. Recusando, o botao continua VISIVEL e diz o motivo no log — era o
        ///     esconder-e-reaparecer que o dono viu quando qualquer personagem agia.
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
                    Hide(Plugin.MotivoDoBotaoDaRunDesligado, false);
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

                if (_mold == null)
                {
                    Hide("o botao nativo molde da barra de baixo sumiu do HUD", true);
                    return;
                }

                EspelharVisibilidade();
                AplicarClique();
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

        /// <summary>
        /// RSTV-30: a visibilidade do botao e a do HUD (o clone e filho da barra de baixo). O unico
        /// caso que exige espelho e o jogo esconder SO o botao nativo da linha: ai escondemos o
        /// nosso junto, senao ficariamos sozinhos numa linha vazia. Nenhuma outra condicao de jogo
        /// esconde este botao — e o que impede o piscar que o dono relatou.
        /// </summary>
        private static void EspelharVisibilidade()
        {
            bool visivel = _mold.gameObject.activeSelf;
            if (_button.activeSelf != visivel)
            {
                _button.SetActive(visivel);
            }
        }

        /// <summary>
        /// RSTV-30: decide se o clique pode ABRIR agora e aplica isso no `interactable` (NUNCA na
        /// visibilidade). Sao DOIS juizes, nesta ordem:
        ///   1. o JOGO — `CurrentCharacterUI.skillsBtn.interactable` (escrito todo frame por
        ///      `GUIManager.Update` l.120491): false quando o estado de UI nao permite abrir o menu de
        ///      personagem (fora de InTown/InWorldMap/InCutscene/InBattle) ou quando o jogo esta
        ///      escondendo os botoes de personagem (`Root.HideCharacterButtons`);
        ///   2. o PORTAO DA RUN — `RunTargets.GateOk`: recusa quando abrir causaria dano real (mira de
        ///      hex/skill ativa, janela de UI ja aberta, posicionamento inicial) — e o alvo do clique
        ///      (`RunTargets.Resolve`).
        /// Cada transicao e logada UMA vez por motivo (o mesmo motivo nao se repete a cada 0,1 s).
        /// </summary>
        private static void AplicarClique()
        {
            string motivo = null;

            bool oJogoDeixa = _mold != null && _mold.interactable;
            if (!oJogoDeixa)
            {
                motivo = "o botao nativo 'Skills' do HUD esta desabilitado pelo jogo " +
                         "(GUIManager.Update l.120491: CurrentGuiState fora de InTown/InWorldMap/" +
                         "InCutscene/InBattle, ou Root.HideCharacterButtons ligado)";
            }

            bool portaoOk = false;
            if (oJogoDeixa)
            {
                portaoOk = RunTargets.GateOk(out motivo);
            }

            Character alvo = null;
            if (oJogoDeixa && portaoOk)
            {
                alvo = RunTargets.Resolve(out motivo);
            }

            bool clicavel = oJogoDeixa && portaoOk && alvo != null;

            Button button = _button != null ? _button.GetComponent<Button>() : null;
            if (button != null && button.interactable != clicavel)
            {
                button.interactable = clicavel;
            }

            if (clicavel)
            {
                if (_clicavelLogado)
                {
                    return;
                }

                _clicavelLogado = true;
                _reason = null;
                _reasonLogged = null;
                Plugin.Log.LogInfo("RSTV DIAG: botao '" + Label + "' do HUD VISIVEL e clicavel — alvo '" +
                                   alvo.CharacterName + "' (nivel " + alvo.Level + ").");
                return;
            }

            _clicavelLogado = false;

            string texto = motivo != null ? motivo : "sem alvo local na party";
            if (_reasonLogged == texto)
            {
                return;
            }

            _reasonLogged = texto;
            _reason = texto;
            Plugin.Log.LogWarning("RSTV DIAG: botao '" + Label + "' do HUD VISIVEL na barra de baixo e " +
                                  "SEM clique agora — " + texto + " (o botao NAO e escondido: quem manda " +
                                  "na visibilidade e' o HUD).");
        }

        /// <summary>
        /// RSTV-30 — MEDE e COLOCA o clone no vao livre da barra de baixo. Nada aqui e posicao
        /// chutada: os numeros saem do proprio jogo em runtime.
        ///
        ///   1. o rect do MOLDE no espaco LOCAL do container (bordas esquerda/direita, altura e o Y da
        ///      linha) — `GetWorldCorners` + `InverseTransformPoint`, a mesma familia de medidas que o
        ///      mod ja usava em `NativeUiHelpers`;
        ///   2. a borda DIREITA dos botoes nativos da linha (maximo entre os filhos ativos do
        ///      container, ignorando o nosso clone);
        ///   3. o LIMITE da direita: o irmao do container cuja borda esquerda seja a primeira a direita
        ///      do container (e o `Skillbar Index Controls`, o controle de rotacionar a barra de
        ///      skills), medido no MESMO espaco local do passo 2 — nenhum nome fica fixo no codigo e o
        ///      nome medido vai para o log. RSTV-30F: medir o irmao no espaco do PAI e comparar com a
        ///      BORDA ESQUERDA do container misturava os referenciais (o `fimDosNativos` conta do
        ///      PIVOR) e punha o clone depois do rotador. Sem nenhum vizinho medido, o limite e o fim
        ///      dos nativos + uma largura;
        ///   4. a posicao: o clone fica DENTRO do vao livre, com `Margem` de respiro nas duas bordas e
        ///      largura limitada pelo vao (nunca invade os nativos nem o vizinho, e nunca passa da
        ///      largura do molde). O resultado — com cada numero usado — vai para o log.
        /// </summary>
        private static void ColocarNaLinha(Transform container, RectTransform moldeRt, RectTransform novo, out string medidas)
        {
            Vector3[] cantos = new Vector3[4];
            RectTransform containerRt = container as RectTransform;

            // 1) o rect do MOLDE, no espaco LOCAL do container.
            moldeRt.GetWorldCorners(cantos);
            float moldeEsq = container.InverseTransformPoint(cantos[0]).x;
            float moldeDir = container.InverseTransformPoint(cantos[3]).x;
            float larguraMolde = moldeDir - moldeEsq;
            if (larguraMolde <= 1f)
            {
                larguraMolde = moldeRt.sizeDelta.x;
            }

            float alturaMolde = moldeRt.rect.height;
            if (alturaMolde <= 1f)
            {
                alturaMolde = moldeRt.sizeDelta.y;
            }

            float yMolde = moldeRt.anchoredPosition.y;

            // 2) a borda direita dos botoes NATIVOS que ja estao na linha.
            float fimDosNativos = float.MinValue;
            for (int i = 0; i < container.childCount; i++)
            {
                Transform filho = container.GetChild(i);
                if (filho == null || filho == novo.transform || !filho.gameObject.activeSelf)
                {
                    continue;
                }

                RectTransform rt = filho as RectTransform;
                if (rt == null)
                {
                    continue;
                }

                rt.GetWorldCorners(cantos);
                fimDosNativos = Mathf.Max(fimDosNativos, container.InverseTransformPoint(cantos[3]).x);
            }

            if (fimDosNativos == float.MinValue)
            {
                fimDosNativos = moldeDir;
            }

            // 3) o limite da DIREITA: o vizinho mais proximo a direita do container, medido no MESMO
            //    referencial do passo 2 — o espaco LOCAL do container (origem no PIVOR, centro).
            //    RSTV-30F: antes daqui o irmao era medido no espaco do PAI e o limite era a DIFERENCA
            //    contra a borda ESQUERDA do container. Duas origens misturadas: `fimDosNativos` conta
            //    do PIVOR e aquele limite contava da BORDA — com os numeros do prefab o `vao` saia
            //    ~55.7 px maior do que e' (74.6 em vez de 19.0) e o clone ia parar DEPOIS do
            //    `Skillbar Index Controls`, o oposto do pedido do dono. Medindo o irmao com o MESMO
            //    `container.InverseTransformPoint`, `fimDosNativos`, `limite` e `vao` falam a mesma
            //    lingua e a conversao `- cantoEsquerdo` do passo 5 deixa de ser uma travessia solta.
            float limite = float.MinValue;
            string vizinho = "nenhum";
            Transform pai = container.parent;
            if (pai != null && containerRt != null)
            {
                containerRt.GetWorldCorners(cantos);
                float direitaDoContainer = container.InverseTransformPoint(cantos[3]).x;

                float melhor = float.MaxValue;
                for (int i = 0; i < pai.childCount; i++)
                {
                    Transform irmao = pai.GetChild(i);
                    if (irmao == null || irmao == container || irmao == novo.transform || !irmao.gameObject.activeSelf)
                    {
                        continue;
                    }

                    RectTransform rt = irmao as RectTransform;
                    if (rt == null)
                    {
                        continue;
                    }

                    rt.GetWorldCorners(cantos);
                    float esquerdaDoIrmao = container.InverseTransformPoint(cantos[0]).x;

                    // "a direita do container": com tolerancia de meio pixel para o caso de as duas
                    // bordas coincidirem (linha encostada na seguinte).
                    if (esquerdaDoIrmao >= direitaDoContainer - 0.5f && esquerdaDoIrmao < melhor)
                    {
                        melhor = esquerdaDoIrmao;
                        vizinho = irmao.name;
                    }
                }

                if (melhor < float.MaxValue)
                {
                    // `melhor` JA' esta no espaco do CONTAINER — o mesmo de `fimDosNativos`. Nada a
                    // converter (a conversao existia so' porque a medida era feita no PAI).
                    limite = melhor;
                }
            }

            if (limite == float.MinValue)
            {
                limite = fimDosNativos + larguraMolde + Margem;
                vizinho = "nenhum (limite = fim dos nativos + largura do molde)";
            }

            // 4) a posicao derivada: dentro do vao livre, sem tocar ninguem.
            //    A largura e o MENOR entre a do molde e o proprio vao — nunca maior que isso, para
            //    nao invadir nem o ultimo botao nativo nem o vizinho da direita. `LarguraMinima` e o
            //    piso de CONFORTO: abaixo dele o log avisa (a barra mudou de espaco), mas a conta
            //    continua sendo a que nao sobrepoe — sobrepor botao nativo nunca e aceitavel.
            float vao = limite - fimDosNativos - (2f * Margem);
            float largura = Mathf.Min(larguraMolde, vao);
            if (largura < 1f)
            {
                largura = 1f;
            }

            float centro = limite - Margem - (largura * 0.5f);
            float menorCentro = fimDosNativos + Margem + (largura * 0.5f);
            if (centro < menorCentro)
            {
                centro = menorCentro;
            }

            // 5) aplica: as ancoras do molde sao o topo-esquerda do container (medido no prefab:
            //    aMin=aMax=(0,1), pivor (0.5,0.5)). `centro` esta no espaco LOCAL — origem no PIVOR,
            //    igual a `fimDosNativos` e `limite`; o `anchoredPosition`, porem, vai da ANCORA (o
            //    canto superior esquerdo do rect) ate o pivor do clone, e e' so' por isso que o
            //    `rect.xMin` entra na conta.
            novo.anchorMin = new Vector2(0f, 1f);
            novo.anchorMax = new Vector2(0f, 1f);
            novo.pivot = new Vector2(0.5f, 0.5f);
            novo.sizeDelta = new Vector2(largura, alturaMolde);

            float cantoEsquerdo = containerRt != null ? containerRt.rect.xMin : 0f;
            novo.anchoredPosition = new Vector2(centro - cantoEsquerdo, yMolde);

            medidas = "largura=" + largura.ToString("0.#") + " px (nativo " + larguraMolde.ToString("0.#") +
                      " px), altura=" + alturaMolde.ToString("0.#") + " px; borda direita dos nativos=" +
                      fimDosNativos.ToString("0.#") + " px, limite do vizinho '" + vizinho + "'=" +
                      limite.ToString("0.#") + " px, vao livre=" + vao.ToString("0.#") + " px, margem=" +
                      Margem.ToString("0.#") + " px no espaco local de '" + container.name + "'" +
                      (largura < LarguraMinima
                           ? " [AVISO: vao livre abaixo do minimo de conforto (" + LarguraMinima.ToString("0.#") +
                             " px) — o botao ficou com o que cabe SEM sobrepor nenhum nativo]"
                           : string.Empty);
        }

        /// <summary>
        /// Aparencia do clone: o FUNDO do botao (targetGraphic) e os graficos cujo nome comeca com
        /// 'Icon' (o `Icon (2)` do `Skills Tree Btn`, que e o glifo da arvore de skills) ficam; TODO o
        /// resto e desligado — inclusive o 'Text BG', o badge de pontos nao gastos, que nao e do mod.
        /// Tudo o que for mexido vai para o log, porque o prefab nao foi aberto.
        ///
        /// ATENCAO: o `targetGraphic` do MOLDE e um componente DO MOLDE — o clone tem a COPIA dele.
        /// Por isso o alvo e lido do Button DO CLONE (senao o fundo do nosso botao tambem seria
        /// desligado e ele ficaria invisivel).
        /// </summary>
        private static void AparenciaDoClone(GameObject clone)
        {
            try
            {
                Button cloneButton = clone.GetComponent<Button>();
                Graphic fundo = cloneButton != null ? cloneButton.targetGraphic : null;

                Graphic[] graficos = clone.GetComponentsInChildren<Graphic>(true);
                int desligados = 0;
                List<string> mantidos = new List<string>();
                for (int i = 0; i < graficos.Length; i++)
                {
                    Graphic g = graficos[i];
                    if (g == null)
                    {
                        continue;
                    }

                    if (g is TextMeshProUGUI)
                    {
                        // RSTV-30: sem rotulo. O vao livre medido na barra de baixo e mais estreito que
                        // um botao nativo e a esse tamanho o glifo le melhor que o texto; o hover nativo
                        // (ButtonTextOnHover, clonado junto) continua identificando o botao.
                        g.enabled = false;
                        desligados++;
                        continue;
                    }

                    if (g == fundo || g.transform == clone.transform || g.gameObject.name.StartsWith("Icon"))
                    {
                        mantidos.Add(g.GetType().Name + " em '" + g.gameObject.name + "'");
                        continue;
                    }

                    g.enabled = false;
                    desligados++;
                }

                Plugin.Log.LogInfo("RSTV-30: aparencia do clone — graficos desligados: " + desligados +
                                   "; mantidos: " +
                                   (mantidos.Count > 0 ? string.Join(", ", mantidos.ToArray()) : "nenhum") +
                                   " (targetGraphic do clone: " +
                                   (fundo != null ? fundo.GetType().Name + " em '" + fundo.gameObject.name + "'" : "nenhum") +
                                   ").");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para limpar a aparencia do clone (" + e.Message + ").");
            }
        }

        /// <summary>
        /// Esconde o botao e escreve no log POR QUE.
        ///
        /// RSTV-30: depois da mudanca de casa e da separacao entre visibilidade e clique, esconder o
        /// botao SO acontece nestes dois casos, e cada um tem a sua justificativa:
        ///   * `AtivarBotaoNaRun=false` (ou a chave-mestra) — pedido explicito do dono no config;
        ///   * o botao nativo molde sumiu do HUD — sem ele nao ha linha nem visual para seguir.
        /// Estado de jogo (mira, turno, animacao, janela, alvo) NAO esconde mais: vira "sem clique" em
        /// `AplicarClique`. Avisa UMA vez por MOTIVO: guarda o ultimo motivo logado (`_reasonLogged`) e
        /// so volta a escrever quando o motivo MUDA — a mesma estrategia do `AvisoUma` do
        /// BetterCombatText. Sem isso, um estado estavel re-loga o texto identico a cada janela de 5 s:
        /// numa sessao isso rendeu 275 linhas iguais. O botao continua escondido do mesmo jeito — muda
        /// so a frequencia do log.
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
            _clicavelLogado = false;

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
        /// O corpo de abertura da visualizacao read-only pelo HUD da RUN — o portao da run ja validado
        /// (`RunTargets.GateOk`) -> o alvo resolvido na hora (`RunTargets.Resolve`, nunca cacheado) ->
        /// `SkillTreesTab.Abrir(alvo, Run)` (a aba "All Skill Trees" do inventario). Extraido do antigo
        /// `OnClick` para ser REUSADO por tres interlocutores, sem duplicar a logica: o botao do HUD
        /// (`RunButton`), o botao DENTRO da janela do level-up (`LevelUpWindowButton`) e o atalho de
        /// teclado (`SkillTreeShortcut`). NAO e o unico caminho: o RSTV-21 tem um SEGUNDO corpo de
        /// abertura, `RemovalWindowSkillsButton.OnClick` -> `SkillTreesTab.AbrirJanela`, que usa o alvo
        /// do proprio modal (CurrentCharacter) e NAO passa por aqui nem pelo `RunTargets`. Idempotente e
        /// sem estado: se o portao recusar ou nao houver alvo, so loga o motivo e nao abre nada.
        ///
        /// RSTV-30: e AQUI (e so aqui) que o portao recusa — o botao continua na tela.
        /// </summary>
        internal static void OpenForTarget()
        {
            try
            {
                string motivo;
                if (!RunTargets.GateOk(out motivo))
                {
                    // RECUSA: reavalia na hora (o portao tambem deixa o botao sem clique; aqui e a
                    // rede final). O botao NAO e escondido.
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
    }
}
