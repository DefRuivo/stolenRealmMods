using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using BepInEx;
using BepInEx.Logging;
using UnityEngine;

namespace Gumatos.RealmApi
{
    /// <summary>Plugin-base observacional, desabilitado por padrão até smoke autorizado em jogo.</summary>
    [BepInPlugin(ApiIdentity.Guid, ApiIdentity.Name, ApiIdentity.Version)]
    [BepInProcess("Stolen Realm.exe")]
    public sealed class RealmApiPlugin : BaseUnityPlugin
    {
        private static HookInstallation? installation;
        private static ManualLogSource? log;
        private void Awake()
        {
            log=Logger;
            if (!Config.Bind("Safety", "EnableHooks", false, "Habilitar somente após autorização de teste em jogo; a versão e hash precisam coincidir.").Value)
            { log.LogInfo("RealmApi 0.1.0: hooks desabilitados por Safety.EnableHooks=false"); return; }
            try
            {
                var game=AppDomain.CurrentDomain.GetAssemblies().Single(a=>a.GetName().Name=="Assembly-CSharp");
                string hash;
                using(var sha=SHA256.Create()) using(var file=File.OpenRead(game.Location))
                    hash=string.Concat(sha.ComputeHash(file).Select(b=>b.ToString("x2")));
                if(!ApiIdentity.Matches(Application.version,hash))
                { log.LogError("RealmApi: alvo incompatível; nenhum hook instalado. Application.version="+Application.version+" assembly.sha256="+hash); return; }
                installation=HookInstallation.Install(game,HookCatalog.All,ApiIdentity.Guid,ex=>log?.LogError(ex));
                Application.quitting += Shutdown;
                log.LogInfo("RealmApi 0.1.0: target 1.3.1 / build-inspecionado 25240684; hooks="+string.Join(",",installation.InstalledIds));
            }
            catch(Exception ex) { log.LogError("RealmApi: instalação recusada: "+ex); }
        }
        private static void Shutdown()
        {
            try { installation?.Dispose(); }
            catch(Exception ex) { log?.LogError(ex); }
            finally { installation=null; Application.quitting-=Shutdown; }
        }
        // Sem OnDestroy/Update do plugin: o ciclo Unity do objeto não determina a vida dos hooks.
    }
}
