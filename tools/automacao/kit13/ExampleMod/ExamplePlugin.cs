using BepInEx;

namespace Gumatos.KitExampleMod
{
    [BepInPlugin("com.gumatos.kit13.example", "KIT13 Standalone Example", "1.0.0")]
    public sealed class ExamplePlugin : BaseUnityPlugin
    {
        public static ExamplePlugin? Instance { get; private set; }
        public CounterState State { get; } = new CounterState();
        private void Awake()
        {
            Instance = this;
            State.Observe();
            Logger.LogInfo("KIT13 standalone observation=" + State.Count);
        }
        private void OnDestroy() { if (ReferenceEquals(Instance, this)) Instance = null; }
    }
}
