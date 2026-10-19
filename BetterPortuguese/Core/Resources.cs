using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;

namespace BetterPortuguese.Core;
internal static class Resources
{
    public static string Sha256(byte[] bytes)
    { using var sha = SHA256.Create(); return BitConverter.ToString(sha.ComputeHash(bytes)).Replace("-", "").ToLowerInvariant(); }
    public static string Decode(byte[] bytes) => new UTF8Encoding(false, true).GetString(bytes);
    public static string Read(Assembly assembly, string name)
    {
        using var stream = assembly.GetManifestResourceStream("BetterPortuguese.Data." + name) ?? throw new InvalidDataException("Missing embedded resource " + name);
        using var buffer = new MemoryStream(); stream.CopyTo(buffer);
        var bytes = buffer.ToArray();
        if (!ResourceHashes.Expected.TryGetValue(name, out var expected) || Sha256(bytes) != expected) throw new InvalidDataException("Resource SHA-256 mismatch " + name);
        return Decode(bytes);
    }
    public static Catalog Load(Assembly assembly)
    {
        // Manifest and audit files checked too, but editorial proposals are NEVER read into the overlay.
        foreach (var kv in ResourceHashes.Expected)
            if (kv.Key != "pt-BR.mods.json") Read(assembly, kv.Key);
        return Catalog.Parse(Read(assembly, "pt-BR.original.json"), Read(assembly, "pt-BR.corrigido.json"), Read(assembly, "correcoes.diff.json"));
    }
    public static ModCatalog LoadMods(Assembly assembly) => ModCatalog.Parse(Read(assembly, "pt-BR.mods.json"));
}
