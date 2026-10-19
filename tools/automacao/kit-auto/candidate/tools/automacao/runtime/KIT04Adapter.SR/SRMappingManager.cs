// KIT-04F Adapter — SRMappingManager (mapeamentos de sistema)
using KIT04Core;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace KIT04Adapter.SR
{
    /// <summary>
    /// Mapeia entre nomes internos do jogo e identificadores estáveis.
    /// Mantém um dicionário de mapeamento item_id -> nome_jogo, skill_id -> nome_skill, etc.
    /// </summary>
    public class SRMappingManager
    {
        private readonly CorePlugin _core;
        private static SRMappingManager? _instance;

        // Mapeamento base: ID interno -> display name
        private readonly Dictionary<string, Dictionary<string, string>> _mapeamentos =
            new Dictionary<string, Dictionary<string, string>>();

        public SRMappingManager(CorePlugin core)
        {
            _core = core;
            _carregarMapeamentosBase();
        }

        public static void SetInstance(SRMappingManager instance) => _instance = instance;

        private void _carregarMapeamentosBase()
        {
            // Mapeamento de telas (nome GameObject -> display)
            _mapeamentos["telas"] = new Dictionary<string, string>
            {
                { "InventoryPanel", "Inventário" },
                { "SkillsPanel", "Habilidades" },
                { "EquipmentPanel", "Equipamento" },
                { "MapPanel", "Mapa" },
                { "DialogPanel", "Diálogo" },
                { "PausePanel", "Pausa" }
            };

            // Mapeamento de categorias de personagem
            _mapeamentos["personagens"] = new Dictionary<string, string>
            {
                { "PlayerCharacter", "Jogador" },
                { "NPC", "NPC" },
                { "Enemy", "Inimigo" },
                { "Companion", "Companheiro" }
            };

            // Mapeamento de tipos de componente
            _mapeamentos["componentes"] = new Dictionary<string, string>
            {
                { "HealthComponent", "Vida" },
                { "DamageComponent", "Dano" },
                { "InventoryComponent", "Inventário" },
                { "SkillComponent", "Habilidade" },
                { "StatusEffectComponent", "Status" }
            };
        }

        /// <summary>
        /// Obtém o nome de display para um ID interno.
        /// Retorna o próprio ID se não encontrado (fallback seguro).
        /// </summary>
        public string Mapear(string categoria, string idInterno)
        {
            if (_mapeamentos.TryGetValue(categoria, out var dict) && dict.TryGetValue(idInterno, out var nome))
                return nome;

            return idInterno; // Fallback: retorna o ID interno como-is
        }

        /// <summary>
        /// Retorna todos os mapeamentos disponíveis.
        /// </summary>
        public Dictionary<string, Dictionary<string, string>> ObterTodos()
        {
            var resultado = new Dictionary<string, Dictionary<string, string>>();
            foreach (var kvp in _mapeamentos)
            {
                resultado[kvp.Key] = new Dictionary<string, string>(kvp.Value);
            }
            return resultado;
        }

        /// <summary>
        /// Registra um novo mapeamento.
        /// </summary>
        public void AdicionarMapeamento(string categoria, string idInterno, string nomeDisplay)
        {
            if (!_mapeamentos.ContainsKey(categoria))
                _mapeamentos[categoria] = new Dictionary<string, string>();

            _mapeamentos[categoria][idInterno] = nomeDisplay;
        }
    }
}
