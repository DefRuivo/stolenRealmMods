#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prove_ciclo.py - demonstracao REAL da CLI KIT-12 em SANDBOX (sem jogo, sem fingir runtime).

O QUE ESTA DEMONSTRACAO MOSTRA (com exits e arquivos lidos de volta)
--------------------------------------------------------------------
Uma copia de `tools/` + um mod de FIXTURE (com DLL de fixture DECLARADA) + uma DLL de
INSTRUMENTO de fixture (bytes, nao build) + um `git init` formam a sandbox. Sobre ela, a CLI
`integracao.py` roda a cadeia inteira:

  1. FIXTURE MARCADA (sem defeito), envelope NO FORMATO DO PRODUTOR VIVO e instrumento MEDIDO
     (`--probe-dll`) -> estado INCOMPLETO / exit 2 (residual de runtime: a fixture testa o
     avaliador e NAO comprova runtime - nunca vira PASSOU/OK), com a procedencia da coleta
     CONFERIDA (`hash_fonte_confronto = confere`, campo `dll_probe_sha(medido)`) e SEM nenhuma
     lacuna `cadeia/coleta-*`;
  2. DEFEITO PLANTADO na fixture    -> estado REPROVADO / exit 1, com a fila de correcao
     declarando CRITERIO + CAUSA (caminho real) + PROVA e `execucao_automatica: false`;
  3. CORRECAO CONTROLADA no sandbox -> estado INCOMPLETO / exit 2: o defeito SOME e o
     criterio NAO vira OK (fixture continua fixture);
  3b. COLETA DECLARANDO OUTROS BYTES (`hash_fonte` de outra rodada, sem instrumento declarado)
     -> INCOMPLETO / exit 2 com a lacuna `cadeia/coleta-contraditoria/hash_fonte`;
  3c. COLETA USANDO A CONVENCAO ERRADA (o hash dos ARQUIVOS-FONTE da rodada, como a versao
     defeituosa do KIT-12 aceitava) -> TAMBEM INCOMPLETO / exit 2 com a lacuna
     `cadeia/coleta-contraditoria/hash_fonte`: `fonte_sha` NAO e procedencia de coleta (F5 da
     revisao run670). Esta etapa falha se a confrontacao voltar a apontar para `fonte_sha`;
  3d. ENVELOPE INCOERENTE (o `hash_fonte` nao casa com o instrumento que o PROPRIO envelope
     declara) -> INCOMPLETO / exit 2 com a lacuna `cadeia/coleta-incoerente/hash_fonte`;
  4. `--verificar` depois de mudar a CONFIG -> exit 3 (aprovacao anterior INVALIDADA).

O formato do envelope (topo: `hash_fonte`/`sessao`/`observacoes`; bloco `identidade`:
`hash_dll_do_probe`/`arquivo_dll_do_probe`) e o do PRODUTOR VIVO, conferido contra o artefato
real `docs/automacao/AUT-4-evidencias/r3-confirmada/aut4probe.json` (hash_fonte ==
identidade.hash_dll_do_probe == sha256 da DLL do probe).

Nada aqui abre/fecha o jogo, instala probe, carrega save, compila, commita ou publica.
Nenhum campo executavel da fila e executado: a fila e DECLARATIVA.

USO
---
    python tools/automacao/kit12/prove_ciclo.py --out scratch/kit/KIT-12G-run671
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
AUTOMACAO = os.path.dirname(AQUI)
TOOLS = os.path.dirname(AUTOMACAO)
REPO = os.path.dirname(TOOLS)

CLI = os.path.join(AQUI, "integracao.py")
ENVELOPE_AUT4_REAL = os.path.join(REPO, "docs", "automacao", "AUT-4-evidencias",
                                  "r3-confirmada", "aut4probe.json")


def sha256_file(caminho):
    if not caminho or not os.path.isfile(caminho):
        return None
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def campos_do_envelope_real():
    """Campos declarados do envelope REAL do produtor vivo (prova de FORMATO, nao de runtime)."""
    if not os.path.isfile(ENVELOPE_AUT4_REAL):
        return {"caminho": ENVELOPE_AUT4_REAL, "presente": False}
    with open(ENVELOPE_AUT4_REAL, encoding="utf-8") as fh:
        real = json.load(fh)
    ident = real.get("identidade") or {}
    return {"caminho": ENVELOPE_AUT4_REAL, "presente": True,
            "esquema": real.get("esquema"), "sessao": real.get("sessao"),
            "hash_fonte": real.get("hash_fonte"),
            "identidade_hash_dll_do_probe": ident.get("hash_dll_do_probe"),
            "arquivo_dll_do_probe": ident.get("arquivo_dll_do_probe"),
            "invariante": bool(real.get("hash_fonte") and ident.get("hash_dll_do_probe")
                               and real["hash_fonte"] == ident["hash_dll_do_probe"])}


def area_externa():
    local = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    base = os.path.join(local, "hermes", "cache", "scratch", "kit12-demo-sandbox")
    if os.path.isdir(base):
        shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    return base


def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)


def sandbox():
    """Copia `tools/` (tracked/untracked, sem .git remoto/perfil/credenciais) + mod de fixture."""
    base = area_externa()
    shutil.copytree(os.path.join(REPO, "tools"), os.path.join(base, "tools"),
                    ignore=shutil.ignore_patterns("__pycache__", "bin", "obj", ".git"))
    mod = os.path.join(base, "BetterStats")
    os.makedirs(mod)
    escrever(os.path.join(mod, "Plugin.cs"),
             "// FIXTURE de sandbox criada por prove_ciclo.py: NAO e o Plugin.cs do mod\n"
             "public class Plugin { }\n")
    escrever(os.path.join(mod, "BetterStats.csproj"),
             "<Project Sdk=\"Microsoft.NET.Sdk\">\n  <PropertyGroup>\n"
             "    <Version>1.0.2</Version>\n  </PropertyGroup>\n</Project>\n")
    dll = os.path.join(mod, "bin", "Release", "netstandard2.1", "BetterStats.dll")
    os.makedirs(os.path.dirname(dll))
    with open(dll, "wb") as fh:  # BYTES DE FIXTURE - nao ha build nesta rodada
        fh.write(b"KIT12-DEMO-FIXTURE-DLL-BYTES\n")
    r = subprocess.run(["git", "init", "-q", base], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise SystemExit("git init falhou na sandbox: %s" % r.stderr.decode("utf-8", "replace"))
    return base


def instrumento_de_fixture(base):
    """(caminho, sha256) da DLL de INSTRUMENTO de fixture (bytes em disco, formato do produtor)."""
    caminho = os.path.join(base, "BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "wb") as fh:
        fh.write(b"KIT12-DEMO-PROBE-DLL-BYTES (fixture - nao e a AUT4Probe.dll do jogo)\n")
    return caminho, sha256_file(caminho)


def coleta(caminho, texto, *, hash_fonte, sessao, probe_dll=None, mod="BetterStats",
           identidade=None, declarados=None):
    """Coleta de FIXTURE explicitamente MARCADA, no FORMATO DO PRODUTOR VIVO (AUT-4).

    `hash_fonte` e o sha256 da DLL do INSTRUMENTO (probe) e o bloco `identidade` declara o mesmo
    instrumento e o caminho da DLL. Fixture testa o avaliador - nunca vira prova de runtime.
    """
    ident = dict(identidade or {})
    if probe_dll and "arquivo_dll_do_probe" not in ident:
        ident["arquivo_dll_do_probe"] = probe_dll
    doc = {"esquema": "AUT-4/1", "procedencia": "fixture", "rotulo_fixture": True,
           "sintetico": True, "evidencia_runtime": False, "sessao": sessao,
           "hash_fonte": hash_fonte, "identidade": ident,
           "nota": "FIXTURE: testa o AVALIADOR; nao comprova runtime nem jogo",
           "observacoes": [{"tipo": "atributos_base_final", "mod": mod, "objeto": "Attributes_Text",
                            "atributo": "Strength", "texto_renderizado": texto,
                            "personagem": "Hero", "personagem_display": "Hero",
                            "saved_map": {"Strength": 10},
                            "atributos_final": {"Strength": 15}}]}
    if declarados:
        doc.update(declarados)
    escrever(caminho, json.dumps(doc, ensure_ascii=False, indent=2))
    return caminho


def rodar_cli(rotulo, argv, out_dir):
    r = subprocess.run([sys.executable, CLI] + argv, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, cwd=REPO)
    texto = r.stdout.decode("utf-8", "replace")
    escrever(os.path.join(out_dir, "%s-saida.txt" % rotulo), texto)
    try:
        resumo = json.loads(texto[texto.index("{"):])
    except (ValueError, IndexError):
        resumo = None
    return {"rotulo": rotulo, "comando": " ".join(argv), "exit_code": r.returncode,
            "saida": os.path.abspath(os.path.join(out_dir, "%s-saida.txt" % rotulo)),
            "resumo": resumo}


def ler_resultado(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Demonstracao real da cadeia KIT-12 em sandbox.")
    ap.add_argument("--out", default=os.path.join(REPO, "scratch", "kit", "KIT-12G-run671"),
                    help="diretorio de provas (fora do repo)")
    args = ap.parse_args(argv)
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)
    # Um `ciclo-resultado*.json` de uma rodada ANTERIOR invalida esta por design (os bytes mudam
    # a cada edicao): ele seria lido como "aprovacao anterior" e a etapa 1 sairia exit 3/INVALIDADO.
    # Nada e apagado: o que existir vai para `<out_dir>/anterior/` e a prova fica repetivel.
    anteriores = [n for n in os.listdir(out_dir)
                  if n.startswith("ciclo-resultado") and n.endswith(".json")]
    if anteriores:
        guarda = os.path.join(out_dir, "anterior")
        os.makedirs(guarda, exist_ok=True)
        for nome in anteriores:
            shutil.move(os.path.join(out_dir, nome), os.path.join(guarda, nome))

    base = sandbox()
    probe, sha_probe = instrumento_de_fixture(base)
    cfg = os.path.join(out_dir, "com.gumatos.betterstats.cfg")
    escrever(cfg, "[Geral]\nAtivo = true\n")
    produtor = {"hash_dll_do_probe": sha_probe, "hash_fonte_declarado": sha_probe,
                "arquivo_dll_do_probe": probe}
    obs_ok = coleta(os.path.join(out_dir, "coleta-fixture-ok.json"), "10 (15)",
                    hash_fonte=sha_probe, sessao="fixture-kit12-demo-ok", identidade=produtor)
    obs_def = coleta(os.path.join(out_dir, "coleta-fixture-defeito.json"), "10 (99)",
                     hash_fonte=sha_probe, sessao="fixture-kit12-demo-ok", identidade=produtor)
    obs_est = coleta(os.path.join(out_dir, "coleta-hash-de-outros-bytes.json"), "10 (15)",
                     hash_fonte="0" * 64, sessao="fixture-kit12-demo-estranho")
    obs_inc = coleta(os.path.join(out_dir, "coleta-incoerente.json"), "10 (15)",
                     hash_fonte=sha_probe, sessao="fixture-kit12-demo-incoerente",
                     identidade={"hash_dll_do_probe": "0" * 64, "hash_fonte_declarado": "0" * 64})
    resultado = os.path.join(out_dir, "ciclo-resultado.json")
    res_def = os.path.join(out_dir, "ciclo-resultado-defeito.json")
    res_cor = os.path.join(out_dir, "ciclo-resultado-corrigido.json")
    res_est = os.path.join(out_dir, "ciclo-resultado-hash-estranho.json")
    res_fonte = os.path.join(out_dir, "ciclo-resultado-hash-dos-fontes.json")
    res_inc = os.path.join(out_dir, "ciclo-resultado-incoerente.json")

    comum = ["--repo", base, "--alterados", "BetterStats/Plugin.cs", "--config", cfg]
    passos = [
        # instrumento MEDIDO (`--probe-dll`): o sha256 dos bytes em disco e autoritativo
        ("1-fixture-marcada", ["--observacoes", obs_ok, "--resultado", resultado,
                               "--probe-dll", probe] + comum),
        ("2-defeito-plantado", ["--observacoes", obs_def, "--resultado", res_def,
                                "--probe-dll", probe] + comum),
        ("3-correcao-controlada", ["--observacoes", obs_ok, "--resultado", res_cor,
                                   "--probe-dll", probe] + comum),
        # F1 (run668): coleta que DECLARA bytes de outra rodada nao pode aprovar nada.
        ("3b-coleta-hash-de-outros-bytes", ["--observacoes", obs_est, "--resultado", res_est]
         + comum),
        # F5 (run670): envelope INCOERENTE com o instrumento que ele mesmo declara.
        ("3d-envelope-incoerente", ["--observacoes", obs_inc, "--resultado", res_inc] + comum),
    ]

    registros = []
    for rotulo, extra in passos:
        registros.append(rodar_cli(rotulo, extra, out_dir))

    # F5 (run670): coleta com a convencao ERRADA (hash dos ARQUIVOS-FONTE da rodada, que a versao
    # defeituosa aceitava como `confere`) - montada A PARTIR do fonte_sha MEDIDO da rodada 1.
    fonte_da_rodada = ler_resultado(resultado)["identidade"]["fonte_sha"]
    obs_fonte = coleta(os.path.join(out_dir, "coleta-hash-dos-arquivos-fonte.json"), "10 (15)",
                       hash_fonte=fonte_da_rodada, sessao="fixture-kit12-demo-fonte")
    registros.append(rodar_cli("3c-coleta-hash-dos-arquivos-fonte",
                               ["--observacoes", obs_fonte, "--resultado", res_fonte] + comum,
                               out_dir))

    # (4) invalidacao: o resultado da etapa 1, conferido DEPOIS de mudar a config
    escrever(cfg, "[Geral]\nAtivo = false\n")
    registros.append(rodar_cli("4-verificar-apos-mudanca-de-config",
                               ["--repo", base, "--config", cfg, "--verificar", resultado], out_dir))
    escrever(cfg, "[Geral]\nAtivo = true\n")

    esperado = {"1-fixture-marcada": (2, "INCOMPLETO"),
                "2-defeito-plantado": (1, "REPROVADO"),
                "3-correcao-controlada": (2, "INCOMPLETO"),
                "3b-coleta-hash-de-outros-bytes": (2, "INCOMPLETO"),
                "3d-envelope-incoerente": (2, "INCOMPLETO"),
                "3c-coleta-hash-dos-arquivos-fonte": (2, "INCOMPLETO"),
                "4-verificar-apos-mudanca-de-config": (3, None)}
    problemas = []
    for reg in registros:
        alvo = esperado[reg["rotulo"]]
        if reg["exit_code"] != alvo[0]:
            problemas.append("%s: exit %s != esperado %s" % (reg["rotulo"], reg["exit_code"], alvo[0]))
        if alvo[1] and (reg["resumo"] or {}).get("estado") != alvo[1]:
            problemas.append("%s: estado %s != esperado %s"
                             % (reg["rotulo"], (reg["resumo"] or {}).get("estado"), alvo[1]))

    com_defeito = ler_resultado(res_def)
    corrigido = ler_resultado(res_cor)
    itens = [f for f in com_defeito["fila_correcao"]
             if f["criterio"] == "KIT-10/atributos/base-vs-final/Attributes_Text"]
    if not itens or itens[0]["roteamento"] != "causa" or not itens[0]["caminhos"]:
        problemas.append("fila do defeito sem CAUSA/caminho real")
    if com_defeito["criterios_resumo"]["REPROVADO"] != 1:
        problemas.append("o defeito plantado nao foi marcado REPROVADO")
    if corrigido["criterios_resumo"]["REPROVADO"] != 0 or corrigido["criterios_resumo"]["OK"] != 0:
        problemas.append("apos a correcao o criterio virou REPROVADO ou OK (deveria ser NAO_EXERCITADO)")
    if corrigido["criterios_resumo"]["com_prova_runtime"] != 0:
        problemas.append("fixture marcada produziu prova_runtime")

    # (1) procedencia da coleta CONFERIDA com o instrumento MEDIDO, sem lacuna de procedencia
    ok = ler_resultado(resultado)
    ids_ok = [c["id"] for c in ok["criterios"]]
    lacunas_ok = [i for i in ids_ok if i.startswith("cadeia/coleta-")]
    if lacunas_ok:
        problemas.append("envelope do produtor com instrumento medido criou lacuna de "
                         "procedencia: %s" % lacunas_ok)
    if ok["identidade"]["dll_probe_sha"] != sha_probe or \
            ok["identidade"]["dll_probe_sha_origem"] != "medido-cli":
        problemas.append("o instrumento medido nao entrou na identidade como medicao")
    for c in ok["criterios"]:
        if c.get("coleta"):
            if c["coleta"]["hash_fonte_confronto"] != "confere":
                problemas.append("etapa 1: hash_fonte_confronto=%s" % c["coleta"]["hash_fonte_confronto"])
            if c["coleta"]["hash_fonte_campo_identidade"] != "dll_probe_sha(medido)":
                problemas.append("etapa 1: campo de confronto=%s"
                                 % c["coleta"]["hash_fonte_campo_identidade"])

    # (3b) coleta com hash de OUTROS bytes -> lacuna declarada e nenhum OK
    estranho = ler_resultado(res_est)
    ids_estranho = [c["id"] for c in estranho["criterios"]]
    if "cadeia/coleta-contraditoria/hash_fonte" not in ids_estranho:
        problemas.append("coleta com hash de outros bytes nao declarou a contradicao")
    if estranho["criterios_resumo"]["OK"] != 0 or estranho["criterios_resumo"]["com_prova_runtime"] != 0:
        problemas.append("coleta com hash de outros bytes produziu OK/prova_runtime")
    if estranho["coleta"].get("hash_fonte") != "0" * 64:
        problemas.append("a coleta de hash estranho nao foi lida como tal")

    # (3d) envelope INCOERENTE: hash_fonte != instrumento que o envelope declara
    incoerente = ler_resultado(res_inc)
    ids_inc = [c["id"] for c in incoerente["criterios"]]
    if "cadeia/coleta-incoerente/hash_fonte" not in ids_inc:
        problemas.append("envelope incoerente com o proprio instrumento nao foi declarado")
    if incoerente["criterios_resumo"]["OK"] != 0:
        problemas.append("envelope incoerente produziu OK")

    # (3c) a convencao ERRADA (hash dos arquivos-fonte) NAO confere: `fonte_sha` nao e procedencia
    dos_fontes = ler_resultado(res_fonte)
    ids_fonte = [c["id"] for c in dos_fontes["criterios"]]
    if "cadeia/coleta-contraditoria/hash_fonte" not in ids_fonte:
        problemas.append("coleta com o hash dos ARQUIVOS-FONTE nao foi declarada contraditoria "
                         "(a confrontacao pode ter voltado para fonte_sha)")
    if dos_fontes["criterios_resumo"]["OK"] != 0:
        problemas.append("coleta com hash dos arquivos-fonte produziu OK")
    if dos_fontes["coleta"].get("hash_fonte") != fonte_da_rodada:
        problemas.append("a coleta da etapa 3c nao foi lida como hash dos arquivos-fonte")
    if (dos_fontes.get("identidade") or {}).get("fonte_sha") != fonte_da_rodada:
        problemas.append("a etapa 3c nao usou o fonte_sha real da rodada")

    prova = {
        "esquema": "KIT-12/prova/1", "tarefa": "t_0a434c97",
        "sandbox": base,
        "sandbox_tem_git": os.path.isdir(os.path.join(base, ".git")),
        "prova_de_fixture": {"dll_do_mod": "bytes de fixture (sem build nesta rodada)",
                             "dll_do_instrumento": probe,
                             "sha_dll_do_instrumento": sha_probe,
                             "coleta_rotulada": True},
        "formato_do_envelope": {"fonte": "produtor vivo AUT-4 (hash_fonte == sha256 da DLL do probe)",
                                "referencia_real": campos_do_envelope_real()},
        "passos": registros,
        "defeito": {"criterio": "KIT-10/atributos/base-vs-final/Attributes_Text",
                    "fila_correcao": itens},
        "correcao": {"de": "10 (99)", "para": "10 (15)",
                     "criterios_resumo": corrigido["criterios_resumo"],
                     "estado": corrigido["estado"], "exit_code": corrigido["exit_code"]},
        "procedencia_confrontada": {
            "instrumento_medido": {"criterios_resumo": ok["criterios_resumo"],
                                   "dll_probe_sha": ok["identidade"]["dll_probe_sha"],
                                   "dll_probe_sha_origem": ok["identidade"]["dll_probe_sha_origem"],
                                   "lacunas_de_procedencia": lacunas_ok,
                                   "campo_de_confronto": "dll_probe_sha(medido)"},
            "coleta_hash_de_outros_bytes": {"criterios_resumo": estranho["criterios_resumo"],
                                            "estado": estranho["estado"],
                                            "exit_code": estranho["exit_code"],
                                            "lacuna": "cadeia/coleta-contraditoria/hash_fonte",
                                            "coleta_hash_fonte": estranho["coleta"].get("hash_fonte")},
            "coleta_hash_dos_arquivos_fonte": {
                "criterios_resumo": dos_fontes["criterios_resumo"],
                "estado": dos_fontes["estado"], "exit_code": dos_fontes["exit_code"],
                "lacuna": "cadeia/coleta-contraditoria/hash_fonte",
                "coleta_hash_fonte": dos_fontes["coleta"].get("hash_fonte"),
                "fonte_sha_da_rodada": fonte_da_rodada,
                "nota": "convencao ERRADA (hash dos arquivos-fonte) NAO confere: fonte_sha nao e "
                        "procedencia de coleta (F5 da revisao run670)"},
            "envelope_incoerente": {"criterios_resumo": incoerente["criterios_resumo"],
                                    "estado": incoerente["estado"],
                                    "exit_code": incoerente["exit_code"],
                                    "lacuna": "cadeia/coleta-incoerente/hash_fonte"},
        },
        "programa_nao_executa_fila": True,
        "hashes": {"integracao.py": sha256_file(CLI),
                   "pertinencia.json": sha256_file(os.path.join(AQUI, "pertinencia.json")),
                   "test_kit12_integracao.py": sha256_file(os.path.join(AQUI, "test_kit12_integracao.py")),
                   "prove_ciclo.py": sha256_file(os.path.abspath(__file__)),
                   "coleta-fixture-ok.json": sha256_file(obs_ok),
                   "coleta-fixture-defeito.json": sha256_file(obs_def),
                   "coleta-hash-dos-arquivos-fonte.json": sha256_file(obs_fonte)},
        "problemas": problemas,
        "veredito": "PASSOU" if not problemas else "FALHOU",
        "nao_exercitado": ["jogo/probe/save/perfil real", "build C#", "deploy", "publicacao",
                           "runtime em jogo (AUT-4)", "aceite humano/DoD"],
    }
    destino = os.path.join(out_dir, "prova.json")
    escrever(destino, json.dumps(prova, ensure_ascii=False, indent=2))
    for reg in registros:
        print("%s | exit=%s | estado=%s" % (reg["rotulo"], reg["exit_code"],
                                            (reg["resumo"] or {}).get("estado")))
    print("PROVA|%s|%s" % (prova["veredito"], destino))
    for p in problemas:
        print("PROBLEMA|%s" % p)
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
