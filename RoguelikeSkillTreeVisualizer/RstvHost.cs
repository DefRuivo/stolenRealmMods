using System;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// MonoBehaviour do mod. REGRA DO PROJETO: nada de criar GameObject no `Awake()` do plugin —
    /// ele roda durante o chainloader do BepInEx, antes de existir cena, e a Unity destrui o objeto
    /// na primeira carga de cena (o `Update()` nunca chega). A criacao aqui e PREGUICOSA, ja' com
    /// cena viva, a partir de um dos ganchos das superficies que RESTAM (a aba do inventario, o HUD
    /// da run, o modal 'Remove Skill Trees') ou do atalho de teclado — todos chamam `Ensure()`, que
    /// e' idempotente. Ate a RSTV-29 havia tambem o gancho da tela Select Party; com aquela
    /// superficie removida ele deixou de existir (ver `Patches.cs`).
    ///
    /// Trabalho do Update (timeScale na UI e 0: nada de coroutine com WaitForSeconds):
    ///   1. o CICLO DE VIDA da aba "All Skill Trees" (RSTV-16) — a sessao read-only nasce e morre com
    ///      a aba selecionada (SkillTreesTab.Tick), lendo o proprio sistema de abas do inventario;
    ///   2. o botao da RUN segue o original e reavalia o PORTAO 4 (`RunTargets.GateOk`) — 0,1 s,
    ///      porque o estado que o portao olha (mira, turno, animacao) muda rapido. O Update do proprio
    ///      HUD (`CurrentCharacterUI.UIUpdate`, l.330080) roda todo frame e mexe no `endTurnButton` —
    ///      nao e lugar para o mod.
    /// </summary>
    internal class RstvHost : MonoBehaviour
    {
        private static RstvHost _instance;
        private float _nextRunMirror;
        private float _lastErrorLog;

        internal static RstvHost Ensure()
        {
            if (_instance != null)
            {
                return _instance;
            }

            GameObject go = new GameObject("RstvHost");
            UnityEngine.Object.DontDestroyOnLoad(go);
            _instance = go.AddComponent<RstvHost>();
            Plugin.Log.LogInfo("RSTV: host criado (cena viva) — Update() ativo.");
            return _instance;
        }

        private void Update()
        {
            try
            {
                SkillTreesTab.Tick();

                // RSTV-14: o botao DENTRO da janela do level-up segue o CICLO DE VIDA da janela —
                // some nos estagios que nao sao de skills (antes ele "voava" sobre o estagio de
                // atributos) e volta (re-ancorado) quando o estagio de skills retorna.
                LevelUpWindowButton.Refresh();

                if (Time.realtimeSinceStartup >= _nextRunMirror)
                {
                    // Portao 4 reavaliado 10x por segundo: o botao da run some/volta conforme a mira,
                    // o turno e as animacoes mudam.
                    _nextRunMirror = Time.realtimeSinceStartup + 0.1f;
                    RunButton.Mirror();
                }
            }
            catch (Exception e)
            {
                if (Time.realtimeSinceStartup - _lastErrorLog < 5f)
                {
                    return;
                }

                _lastErrorLog = Time.realtimeSinceStartup;
                Plugin.Log.LogError("RSTV: falha no Update do host: " + e);
            }
        }
    }
}
