// KIT-04F Adapter — SRScreenManager (gestão de telas)
using KIT04Core;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace KIT04Adapter.SR
{
    /// <summary>
    /// Identifica e registra telas visíveis no Stolen Realm.
    /// Mapeia as telas principais: Inventory, Skills, Equipment, Map, Dialog, Pause.
    /// </summary>
    public class SRScreenManager
    {
        private readonly CorePlugin _core;
        private static SRScreenManager? _instance;

        // Telas conhecidas por nome de GameObject
        private static readonly string[] TelasConhecidas = {
            "InventoryPanel",
            "SkillsPanel",
            "EquipmentPanel",
            "MapPanel",
            "DialogPanel",
            "PausePanel",
            "RstvSkillTreesWindow", // host alternativo (janela separada)
            "RstvAllSkillTreesPanel" // host atual da aba All Trees (SkillTreesTab.PanelName)
        };

        public SRScreenManager(CorePlugin core)
        {
            _core = core;
        }

        public static void SetInstance(SRScreenManager instance) => _instance = instance;

        /// <summary>KIT-05F: telas monitoradas (leitura; a ponte passiva observa transicoes).</summary>
        public static string[] TelasMonitoradas => TelasConhecidas;

        /// <summary>
        /// Captura o estado da tela atual e retorna um dictionary.
        /// </summary>
        public Dictionary<string, object>? CapturarEstadoAtual()
        {
            if (_instance == null || _instance._core == null)
                return null;

            foreach (var nome in TelasConhecidas)
            {
                var root = GameObject.Find(nome);
                if (root != null && root.activeInHierarchy)
                {
                    var info = new Dictionary<string, object>
                    {
                        { "tela", nome },
                        { "tipo", "ui_panel" },
                        { "ativa", true },
                        { "timestamp", DateTime.Now.ToString("o") }
                    };
                    // Inventario de componentes da tela
                    var componentes = new List<string>();
                    foreach (var comp in root.GetComponents<Component>())
                    {
                        componentes.Add(comp.GetType().Name);
                    }
                    info["componentes"] = componentes.ToArray();
                    return info;
                }
            }

            // Nenhuma tela conhecida ativa — retorna null (ausente, não inventa)
            return null;
        }

        /// <summary>
        /// Retorna todas as telas ativas detectadas.
        /// </summary>
        public Dictionary<string, object>[] ListarTelasAtivas()
        {
            var resultados = new List<Dictionary<string, object>>();

            foreach (var nome in TelasConhecidas)
            {
                var root = GameObject.Find(nome);
                if (root != null && root.activeInHierarchy)
                {
                    var info = new Dictionary<string, object>
                    {
                        { "tela", nome },
                        { "tipo", "ui_panel" },
                        { "ativa", true },
                        { "timestamp", DateTime.Now.ToString("o") }
                    };
                    resultados.Add(info);
                }
            }

            return resultados.ToArray();
        }
    }
}
