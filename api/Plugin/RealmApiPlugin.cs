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
            { log.LogInfo("RealmApi "+ApiIdentity.Version+": nenhum hook instalado — Safety.EnableHooks=false (default do dono; não é falha de alvo). Alvo que seria exigido: jogo "+ApiIdentity.GameVersion+", build "+ApiIdentity.SteamBuildId+", sha256 "+Short(ApiIdentity.AssemblySha256)+"."); return; }
            try
            {
                var game=AppDomain.CurrentDomain.GetAssemblies().Single(a=>a.GetName().Name=="Assembly-CSharp");
                string hash;
                using(var sha=SHA256.Create()) using(var file=File.OpenRead(game.Location))
                    hash=string.Concat(sha.ComputeHash(file).Select(b=>b.ToString("x2")));
                if(!ApiIdentity.Matches(Application.version,hash))
                { log.LogError("RealmApi: alvo incompatível; nenhum hook instalado. Application.version="+Application.version
                    +" (exigido "+ApiIdentity.GameVersion+"), assembly.sha256="+hash
                    +" (exigido "+ApiIdentity.AssemblySha256+", para build "+ApiIdentity.SteamBuildId+")."
                    +" Build nova = nova medição, não afrouxar o portão."); return; }
                installation=HookInstallation.Install(game,HookCatalog.All,ApiIdentity.Guid,ex=>log?.LogError(ex));
                Application.quitting += Shutdown;
                log.LogInfo("RealmApi "+ApiIdentity.Version+": target "+ApiIdentity.GameVersion+" / build "+ApiIdentity.SteamBuildId+" / sha256 "+Short(hash)+"; hooks="+string.Join(",",installation.InstalledIds));
            }
            catch(Exception ex) { log.LogError("RealmApi: instalação recusada: "+ex); }
        }
        private static string Short(string sha) => sha.Length<=12 ? sha : sha.Substring(0,12)+"…";
        private static void Shutdown()
        {
            try { installation?.Dispose(); }
            catch(Exception ex) { log?.LogError(ex); }
            finally { installation=null; Application.quitting-=Shutdown; }
        }
        // Sem OnDestroy/Update do plugin: o ciclo Unity do objeto não determina a vida dos hooks.
    }
}
