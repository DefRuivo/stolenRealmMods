// KIT-04F Adapter — SRCharacterManager (gestão de personagens)
using KIT04Core;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace KIT04Adapter.SR
{
    /// <summary>
    /// Lê informações de personagens ativos no Stolen Realm.
    /// Mapeia atributos, skills, inventário e status por meio de reflexão.
    /// </summary>
    public class SRCharacterManager
    {
        private readonly CorePlugin _core;
        private static SRCharacterManager? _instance;

        // Tipos conhecidos de personagem (via reflexão no runtime)
        private static readonly string[] TiposPersonagem = {
            "PlayerCharacter",
            "NPC",
            "Enemy",
            "Companion"
        };

        public SRCharacterManager(CorePlugin core)
        {
            _core = core;
        }

        public static void SetInstance(SRCharacterManager instance) => _instance = instance;

        /// <summary>
        /// Lista todos os personagens ativos no cenário.
        /// </summary>
        public Dictionary<string, object>[] ListarAtivos()
        {
            if (_core == null || !_core.EstaHabilitado())
                return Array.Empty<Dictionary<string, object>>();

            var personagens = new List<Dictionary<string, object>>();

            // Tenta ler via reflection os tipos conhecidos
            var assemblyCSharp = typeof(GameObject).Assembly;
            foreach (var tipoNome in TiposPersonagem)
            {
                var tipo = assemblyCSharp.GetType($"StolenRealm.{tipoNome}");
                if (tipo == null)
                {
                    // Tenta encontrar por substring
                    foreach (var t in assemblyCSharp.GetTypes())
                    {
                        if (t.Name.Contains(tipoNome))
                        {
                            tipo = t;
                            break;
                        }
                    }
                }

                if (tipo != null)
                {
                    // Busca instâncias via MonoBehaviour
                    var monobehaviours = GameObject.FindObjectsOfType<MonoBehaviour>();
                    foreach (var mb in monobehaviours)
                    {
                        if (mb.GetType() == tipo || mb.GetType().IsSubclassOf(tipo))
                        {
                            var info = new Dictionary<string, object>
                            {
                                { "tipo", tipoNome },
                                { "nome", mb.name },
                                { "ativo", mb.enabled },
                                { "transform", $"pos={mb.transform.position}" },
                                { "timestamp", DateTime.Now.ToString("o") }
                            };
                            personagens.Add(info);
                        }
                    }
                }
            }

            return personagens.ToArray();
        }

        /// <summary>
        /// Obtém atributos de um personagem por reflection.
        /// </summary>
        public Dictionary<string, object> ObterAtributos(string nomePersonagem)
        {
            var resultado = new Dictionary<string, object>
            {
                { "nome", nomePersonagem },
                { "atributos", new Dictionary<string, object>() }
            };

            // Tenta encontrar o componente do personagem
            var assemblyCSharp = typeof(GameObject).Assembly;
            foreach (var tipoNome in TiposPersonagem)
            {
                var tipo = assemblyCSharp.GetType($"StolenRealm.{tipoNome}");
                if (tipo == null)
                    continue;

                var monobehaviours = GameObject.FindObjectsOfType<MonoBehaviour>();
                foreach (var mb in monobehaviours)
                {
                    if ((mb.GetType() == tipo || mb.GetType().IsSubclassOf(tipo)) && mb.name.Contains(nomePersonagem))
                    {
                        // Usa reflection para ler campos/propriedades
                        foreach (var prop in mb.GetType().GetProperties())
                        {
                            try
                            {
                                var valor = prop.GetValue(mb);
                                ((Dictionary<string, object>)resultado["atributos"])[prop.Name] = valor?.ToString() ?? "null";
                            }
                            catch
                            {
                                // Propriedade inacessível — ignora
                            }
                        }
                    }
                }
            }

            return resultado;
        }
    }
}
