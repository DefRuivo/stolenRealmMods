// KIT-04F Adapter — SROwnerManager (gestão de owners/proprietários)
using KIT04Core;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace KIT04Adapter.SR
{
    /// <summary>
    /// Gerencia o rastreamento de proprietários de assets (objetos, componentes, prefabs).
    /// Mapeia a cadeia de ownership: cena > objeto > componente > sub-componente.
    /// </summary>
    public class SROwnerManager
    {
        private readonly CorePlugin _core;
        private static SROwnerManager? _instance;

        public SROwnerManager(CorePlugin core)
        {
            _core = core;
        }

        public static void SetInstance(SROwnerManager instance) => _instance = instance;

        /// <summary>
        /// Retorna todos os owners de um tipo de componente dado.
        /// </summary>
        public Dictionary<string, object>[] ListarOwners<T>() where T : Component
        {
            if (_core == null || !_core.EstaHabilitado())
                return Array.Empty<Dictionary<string, object>>();

            var componentes = GameObject.FindObjectsOfType<T>();
            var resultados = new List<Dictionary<string, object>>();

            foreach (var comp in componentes)
            {
                if (comp == null)
                    continue;

                var owner = new Dictionary<string, object>
                {
                    { "tipo_componente", comp.GetType().FullName },
                    { "nome_objeto", comp.gameObject.name },
                    { "tag", comp.gameObject.tag },
                    { "layer", comp.gameObject.layer },
                    { "ativo", comp.gameObject.activeInHierarchy },
                    { "cena", comp.gameObject.scene.name },
                    { "timestamp", DateTime.Now.ToString("o") }
                };

                resultados.Add(owner);
            }

            return resultados.ToArray();
        }

        /// <summary>
        /// Obtém o hierarchy path completo de um GameObject.
        /// </summary>
        public string GetHierarchyPath(GameObject obj)
        {
            if (obj == null)
                return "";

            var parts = new List<string>();
            var current = obj;
            while (current != null)
            {
                parts.Add(current.name);
                current = current.transform.parent?.gameObject;
            }
            parts.Reverse();
            return "/" + string.Join("/", parts);
        }
    }
}
