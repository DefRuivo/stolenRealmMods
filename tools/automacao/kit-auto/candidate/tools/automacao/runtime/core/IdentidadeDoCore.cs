// KIT-04 Core - Identidade do instrumento (L1 AUD-1)
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Collections.Generic;

namespace KIT04Core
{
    /// <summary>
    /// Calcula identidade do Core: hash SHA256 da DLL, arquivo, bytes, conferência.
    /// Fecha a lacuna L1: o JSON do instrumento diz a SESSAO, mas nao diz QUAL BINARIO leu.
    /// </summary>
    public static class IdentidadeDoCore
    {
        /// <summary>
        /// Calcula identidade do instrumento com hash_fonte_declarado do driver.
        /// </summary>
        public static Dictionary<string, object> CalcularIdentidade(string hashFonteDeclarado)
        {
            string arquivo = null;
            object bytes = null;
            string hash = null;
            string erro = null;

            try
            {
                var asm = typeof(CorePlugin).Assembly;
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
            catch (Exception e)
            {
                erro = e.GetType().Name + ": " + e.Message;
            }

            return Json.Campos(
                "criterio", "o hash do fonte/DLL mede entra no JSON DO INSTRUMENTO (L1 da AUD-1); " +
                    "o hash da DLL e CALCULADO no runtime sobre o assembly carregado, nunca lido do .cfg",
                "hash_fonte_declarado", hashFonteDeclarado,
                "hash_dll_do_core", hash,
                "arquivo_dll_do_core", arquivo,
                "bytes_dll_do_core", bytes,
                "calculo", "sha256 do proprio assembly (typeof(CorePlugin).Assembly.Location) calculado no carregamento",
                "conferencia_do_driver", "o driver confere este hash contra a DLL em disco e contra o HashFonte do .cfg; " +
                    "divergencia => NAO_EXERCITADO",
                "erro", erro);
        }

        /// <summary>
        /// Calcula SHA256 de um arquivo em disco.
        /// </summary>
        public static string Sha256(string caminho)
        {
            using (var sha = SHA256.Create())
            using (var fs = File.OpenRead(caminho))
            {
                var hash = sha.ComputeHash(fs);
                var sb = new StringBuilder();
                foreach (var b in hash)
                    sb.Append(b.ToString("x2"));
                return sb.ToString();
            }
        }
    }
}
