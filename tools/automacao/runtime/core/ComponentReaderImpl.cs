// KIT-04 Core - Implementação concreta de IComponentReader<T>
using System.Collections.Generic;
using UnityEngine;

namespace KIT04Core
{
    /// <summary>
    /// Leitor genérico de componentes MonoBehaviour.
    ///
    /// Regra central (spec §"Ler componentes"): componente AUSENTE ⇒ retorna <c>null</c>.
    /// Nunca retorna array vazio e nunca inventa valor — array vazio é ambíguo (não distingue
    /// "não existe" de "existe e é vazio"), então é proibido por contrato.
    /// </summary>
    /// <typeparam name="T">Tipo do componente (deve herdar MonoBehaviour)</typeparam>
    public class ComponentReaderImpl<T> : IComponentReader<T> where T : MonoBehaviour
    {
        private static T[]? Presente(T[]? achados)
            => (achados == null || achados.Length == 0) ? null : achados;

        /// <summary>Componentes do tipo T ativos na cena; null se nenhum existir.</summary>
        public T[]? LerTodos()
            => Presente(UnityEngine.Object.FindObjectsOfType<T>());

        /// <summary>Componentes do tipo T com nome exato; null se nenhum casar.</summary>
        public T[]? LerPorNome(string nome)
        {
            var todos = LerTodos();
            if (todos == null)
                return null;

            var filtrados = new List<T>();
            foreach (var c in todos)
            {
                if (c != null && c.name == nome)
                    filtrados.Add(c);
            }
            return Presente(filtrados.ToArray());
        }

        /// <summary>Componentes do tipo T com a tag dada; null se nenhum casar.</summary>
        public T[]? LerPorTag(string tag)
        {
            var todos = LerTodos();
            if (todos == null)
                return null;

            var filtrados = new List<T>();
            foreach (var c in todos)
            {
                if (c != null && c.gameObject.tag == tag)
                    filtrados.Add(c);
            }
            return Presente(filtrados.ToArray());
        }

        /// <summary>
        /// Inventário resumido. Quando o componente está AUSENTE devolve
        /// <c>{"total": 0, "ausente": true}</c> — estado explícito, não silêncio.
        /// </summary>
        public Dictionary<string, object> Inventariar(int maxAmostra)
        {
            var todos = LerTodos();
            if (todos == null)
                return Json.Campos("total", 0, "ausente", true, "amostra", new string[0]);

            var limite = maxAmostra < todos.Length ? maxAmostra : todos.Length;
            var amostra = new List<string>();
            for (var i = 0; i < limite; i++)
                amostra.Add(todos[i] != null ? todos[i].name : "(destruido)");

            return Json.Campos("total", todos.Length, "ausente", false, "amostra", amostra);
        }
    }
}
