using System;

namespace Gumatos.KitExampleMod
{
    // Standalone mod domain: no SDK/Core/Adapter reference.
    public sealed class CounterState
    {
        public int Count { get; private set; }
        public event Action<int>? Changed;
        public void Observe()
        {
            Count++;
            // A faulty optional observer must not break the mod or other observers.
            var listeners = Changed;
            if (listeners == null) return;
            foreach (Action<int> listener in listeners.GetInvocationList())
                try { listener(Count); } catch (Exception) { /* optional observer isolated */ }
        }
    }
}
