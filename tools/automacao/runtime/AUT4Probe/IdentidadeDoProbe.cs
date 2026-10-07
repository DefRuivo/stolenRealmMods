// AUT-4 — IDENTIDADE DO INSTRUMENTO (L1 da AUD-1).
//
// Lacuna L1: o JSON do probe dizia a SESSAO, mas nao dizia QUAL BINARIO leu — o hash
// do fonte/DLL nao estava dentro do JSON do instrumento (so no `consolida.py` do
// CAP-1, que nao e versionado). Sem identidade, uma evidencia de rodada nao pode ser
// amarrada ao artefato que a produziu.
//
// Este componente fecha a lacuna com DOIS valores, dos dois lados da conferencia:
//   * `hash_fonte_declarado` — o valor que o DRIVER injetou no `.cfg` (HashFonte; o
//     driver o deriva do sha256 da DLL instalada). E declaracao, conferida pelo driver
//     contra a DLL em disco (`provar_atualidade`).
//   * `hash_dll_do_probe`    — sha256 CALCULADO AQUI, no runtime, sobre o proprio
//     assembly carregado. Nao vem do `.cfg` e nao pode ser maquiado por config.
//
// Nada e fabricado: se o proprio arquivo nao puder ser lido, o hash sai `null`, o
// motivo sai em `erro` e o JSON declara isso — AUSENTE, nunca um valor plausivel.
using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace Aut4Probe
{
    internal static class IdentidadeDoProbe
    {
        /// <summary>Bloco `identidade` do topo do JSON do probe.</summary>
        internal static Dictionary<string, object> Identidade(string hashFonteDeclarado)
        {
            string arquivo = null;
            object bytes = null;
            string hash = null;
            string erro = null;
            try
            {
                var asm = typeof(Aut4ProbePlugin).Assembly;
                arquivo = string.IsNullOrEmpty(asm.Location) ? null : asm.Location;
                if (arquivo == null)
                {
                    erro = "Assembly.Location vazio (assembly carregado sem arquivo em disco)";
                }
                else if (!File.Exists(arquivo))
                {
                    erro = "arquivo do assembly nao existe em disco: " + arquivo;
                }
                else
                {
                    bytes = new FileInfo(arquivo).Length;
                    hash = Sha256(arquivo);
                }
            }
            catch (Exception e) { erro = e.GetType().Name + ": " + e.Message; }

            return Json.Campos(
                "criterio", "o hash do fonte/DLL medido entra no JSON DO INSTRUMENTO (L1 da AUD-1); "
                + "o hash da DLL e CALCULADO no runtime sobre o assembly carregado, nunca lido do .cfg",
                "hash_fonte_declarado", hashFonteDeclarado,
                "hash_dll_do_probe", hash,
                "arquivo_dll_do_probe", arquivo,
                "bytes_dll_do_probe", bytes,
                "calculo", "sha256 do proprio assembly (typeof(Aut4ProbePlugin).Assembly.Location) "
                + "calculado no carregamento do probe",
                "conferencia_do_driver", "o driver confere este hash contra a DLL em disco e contra "
                + "o HashFonte do .cfg (provar_atualidade); divergencia => NAO_EXERCITADO",
                "erro", erro);
        }

        internal static string Sha256(string caminho)
        {
            using (var sha = SHA256.Create())
            using (var fs = File.OpenRead(caminho))
            {
                var hash = sha.ComputeHash(fs);
                var sb = new StringBuilder();
                foreach (var b in hash) sb.Append(b.ToString("x2"));
                return sb.ToString();
            }
        }
    }
}
