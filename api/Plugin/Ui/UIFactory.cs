using System;
using Gumatos.RealmApi;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace Gumatos.RealmApi.UI
{
    /// <summary>
    /// Familia COMPORTAMENTAL: as operacoes aqui MUTAM a UI do jogo (clonar, copiar layout, ligar clique,
    /// trocar texto/icone, destruir). Nao publica evento observacional e nao e um postfix Harmony.
    /// Toda chamada exige `UiFamily.Bind(assembly, hosts, allowMutation:true)` e roda no thread do vinculo.
    /// Assinaturas identicas ao contrato do inventario (`api/docs/contract-inventory.json`, familia UI).
    /// </summary>
    public static class UIFactory
    {
        private const string Family = UiRequirements.FamilyFactory;

        /// <summary>Clona `template`. Sem pai explicito, o clone vai para o pai do template; sem pai, para a raiz da UI do jogo.</summary>
        public static GameObject Clone(GameObject template, string? name = null)
        {
            if (template == null) throw new ArgumentNullException(nameof(template));
            var parent = template.transform.parent;
            return Clone(template, parent != null ? parent : UiRoot(), name);
        }

        /// <summary>Clona `template` sob `parent`, preservando o transform local (convencao de UI).</summary>
        public static GameObject Clone(GameObject template, Transform parent, string? name = null)
        {
            UiFamily.Require(Family, true);
            if (template == null) throw new ArgumentNullException(nameof(template));
            if (parent == null) throw new ArgumentNullException(nameof(parent));
            var clone = UnityEngine.Object.Instantiate(template, parent, false);
            if (!string.IsNullOrEmpty(name)) clone.name = name;
            return clone;
        }

        /// <summary>Clona um componente nativo (um `Component`, nao o GameObject inteiro).</summary>
        public static Component CloneComponent(Component template, string? name = null)
        {
            UiFamily.Require(Family, true);
            if (template == null) throw new ArgumentNullException(nameof(template));
            var clone = UnityEngine.Object.Instantiate(template);
            if (!string.IsNullOrEmpty(name)) clone.gameObject.name = name;
            return clone;
        }

        /// <summary>Copia a geometria de layout de `source` para `target` e aplica o deslocamento.</summary>
        public static void CopyRectLayout(RectTransform source, RectTransform target, Vector2 positionOffset = default)
        {
            UiFamily.Require(Family, true);
            if (source == null) throw new ArgumentNullException(nameof(source));
            if (target == null) throw new ArgumentNullException(nameof(target));
            target.anchorMin = source.anchorMin;
            target.anchorMax = source.anchorMax;
            target.pivot = source.pivot;
            target.sizeDelta = source.sizeDelta;
            target.anchoredPosition = source.anchoredPosition + positionOffset;
        }

        /// <summary>Filho DIRETO por nome. Ausente falha fechado (nao devolve null).</summary>
        public static Transform FindChild(Transform parent, string name)
        {
            UiFamily.Require(Family, false);
            if (parent == null) throw new ArgumentNullException(nameof(parent));
            if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Nome vazio", nameof(name));
            return parent.Find(name) ?? throw new InvalidOperationException("Filho ausente: " + name);
        }

        /// <summary>Liga `onClick` ao botao nativo do GameObject. Sem `Button` no alvo, falha fechado.</summary>
        public static void BindClick(GameObject go, UnityAction onClick)
        {
            UiFamily.Require(Family, true);
            if (go == null) throw new ArgumentNullException(nameof(go));
            if (onClick == null) throw new ArgumentNullException(nameof(onClick));
            var button = go.GetComponent<Button>() ?? throw new MissingComponentException("Button ausente em " + go.name);
            button.onClick.AddListener(onClick);
        }

        /// <summary>Define o texto do componente UGUI nativo. (TextMeshPro fica fora desta entrega; ver README.)</summary>
        public static void SetText(GameObject go, string text)
        {
            UiFamily.Require(Family, true);
            if (go == null) throw new ArgumentNullException(nameof(go));
            var label = go.GetComponent<Text>() ?? throw new MissingComponentException("Text (UGUI) ausente em " + go.name);
            label.text = text;
        }

        /// <summary>Define o icone no `Image` do alvo (ou do filho indicado por `childNameHint`). Icone nulo desabilita a imagem.</summary>
        public static void SetIcon(GameObject go, Sprite icon, string? childNameHint = null)
        {
            UiFamily.Require(Family, true);
            if (go == null) throw new ArgumentNullException(nameof(go));
            var target = string.IsNullOrWhiteSpace(childNameHint) ? go : FindChild(go.transform, childNameHint!).gameObject;
            var image = target.GetComponent<Image>() ?? throw new MissingComponentException("Image ausente em " + target.name);
            image.sprite = icon;
            image.enabled = icon != null;
        }

        /// <summary>Desabilita todo texto UGUI do alvo e dos filhos.</summary>
        public static void DisableAllText(GameObject go)
        {
            UiFamily.Require(Family, true);
            if (go == null) throw new ArgumentNullException(nameof(go));
            foreach (var label in go.GetComponentsInChildren<Text>(true)) label.enabled = false;
        }

        /// <summary>Desabilita todo layout automatico (LayoutGroup) dos filhos, para posicionar a mao.</summary>
        public static void DisableChildLayouts(GameObject go)
        {
            UiFamily.Require(Family, true);
            if (go == null) throw new ArgumentNullException(nameof(go));
            foreach (var group in go.GetComponentsInChildren<LayoutGroup>(true)) group.enabled = false;
        }

        /// <summary>Destroi o GameObject nativo. Alvo nulo falha fechado (nao e no-op silencioso).</summary>
        public static void Destroy(GameObject go)
        {
            UiFamily.Require(Family, true);
            if (go == null) throw new ArgumentNullException(nameof(go));
            UnityEngine.Object.Destroy(go);
        }

        private static Transform UiRoot()
        {
            var gui = UiOperations.FactoryHost();
            return gui is Component component ? component.transform : throw new InvalidOperationException("Hospedeiro da UI nao e um Component do Unity");
        }
    }
}
