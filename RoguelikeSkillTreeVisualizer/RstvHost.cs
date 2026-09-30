using System;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// MonoBehaviour do mod. REGRA DO PROJETO: nada de criar GameObject no `Awake()` do plugin —
    /// ele roda durante o chainloader do BepInEx, antes de existir cena, e a Unity destrui o objeto
    /// na primeira carga de cena (o `Update()` nunca chega). A criacao aqui e PREGUICOSA, a partir
    /// do postfix de `CharacterChoiceManager.OpenCharacterChoiceManager` — cena viva, comprovada.
    ///
    /// Trabalho do Update (timeScale na UI e 0: nada de coroutine com WaitForSeconds):
    ///   1. terminar a abertura da skill tree quando a instancia nativa chega (SkillTreeReadOnly.Tick);
    ///   2. manter o clone do botao em sincronia com o original (visibilidade e interactable).
    /// </summary>
    internal class RstvHost : MonoBehaviour
    {
        private static RstvHost _instance;
        private float _nextMirror;
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
                SkillTreeReadOnly.Tick();

                if (Time.realtimeSinceStartup < _nextMirror)
                {
                    return;
                }

                _nextMirror = Time.realtimeSinceStartup + 0.2f;
                SelectPartyButton.Mirror();
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
