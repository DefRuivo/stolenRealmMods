// KIT-04 Core - Interface genérica para leitura de componentes
using System;
using System.Collections.Generic;
using UnityEngine;

namespace KIT04Core
{
    /// <summary>
    /// Le componentes MonoBehaviour genéricos do Unity.
    /// Retorna null se componente nao existir (AUSENTE, nunca inventa valor).
    /// </summary>
    /// <typeparam name="T">Tipo do componente (deve herdar MonoBehaviour)</typeparam>
    public interface IComponentReader<T> where T : MonoBehaviour
    {
        /// <summary>
        /// Retorna todos os componentes do tipo T ativos na cena.
        /// AUSENTE (nenhum componente do tipo) ⇒ null, nunca array vazio.
        /// </summary>
        T[]? LerTodos();

        /// <summary>
        /// Filtra componentes por nome exato (case-sensitive).
        /// AUSENTE ⇒ null.
        /// </summary>
        T[]? LerPorNome(string nome);

        /// <summary>
        /// Filtra componentes por tag.
        /// AUSENTE ⇒ null.
        /// </summary>
        T[]? LerPorTag(string tag);

        /// <summary>
        /// Inventaria componentes com resumo por propriedade (shader/fonte/material).
        /// </summary>
        /// <param name="maxAmostra">Máximo de amostras para incluir em detalhe</param>
        Dictionary<string, object> Inventariar(int maxAmostra);
    }
}
