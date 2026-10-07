#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-5/CIC-5/COR-AUT4 — CAMINHO EXECUTAVEL: instalar / lancar / esperar / PROVAR / reverter.

Exercita `coletor.executar_rodada` de verdade, SEM jogo:
  * perfil ISOLADO em diretorio de fixture (scratch), nunca o perfil do dono;
  * "lancamento" por um STUB externo (processo real, `sys.executable`), com o
    caminho do Steam default explicitamente SUBSTITUIDO pelo stub;
  * o stub grava o proprio argv num arquivo -> a prova e o ARTEFATO EM DISCO da
    execucao, nao uma mensagem que o driver inventou;
  * rollback EXATO conferido por bytes (arquivo criado some, modificado volta,
    DIRETORIO pre-existente NAO e removido).

COR-AUT4 (achados da AUT-4R2) e COR-AUT4-F2 (achados A1c/A2/A3/A6 da COR-AUT4R):
  A1 — o driver NAO confirma so porque existe um `aut4probe.json`: exige as TRES
       provas independentes (sessao DESTA rodada injetada no .cfg + JSON mais novo
       que o lancamento; log da rodada com chainloader E linha de vida do probe;
       prints existentes com bytes>0 E POSTERIORES ao lancamento). Um JSON de rodada
       ANTERIOR nao vale; um PNG de rodada anterior no out_dir REUSADO tambem nao.
  A2 — o objeto INATIVO cujo campo-alvo (`texto_renderizado`) nao foi lido NAO
       "fecha" o criterio: o consolidado sai INCOMPLETO e a rodada NAO e CONCLUIDO.
       Vazio (`""`/`[]`/`{}`) e NAO LIDO: o artefato REAL do probe emite `""`.
  A5 — diretorio que ja existia no perfil (pasta do probe vazia) tem de SOBREVIVER
       ao rollback.
  A6 — com `demostrar_tooltip` no plano, o driver exige a prova de ida-e-volta com
       o MARCADOR gerado pelo driver (marcador ausente ou diferente nao confere).

Caso default (nao autorizado) prova que NADA acontece: nem probe, nem cfg, nem o
stub e executado.
"""
import hashlib
import json
import os
import sys
import tempfile
import time

import comum as C

META = {
    "nome": "aut4-execucao",
    "categoria": "pura",
    "requer": [],
    "descricao": "executar_rodada instala/lanca/espera/prova/reverte por artefato em disco; "
                 "sem as 3 provas (sessao/log/prints) NAO confirma; diretorio pre-existente sobrevive",
}

PRELOADER_REL = os.path.join("BepInEx", "core", "BepInEx.Preloader.dll")
PROBE_REL = os.path.join("BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
CFG_REL = os.path.join("BepInEx", "config", "com.gumatos.aut4probe.cfg")
LOG_REL = os.path.join("BepInEx", "LogOutput.log")

# Stub do lancador: le o .cfg DERIVADO pelo driver (a sessao DESTA rodada vive la),
# grava log de boot + linha de vida do probe, um PNG de verdade e o JSON do probe.
# Flags: --nao-escreve --sem-print --sem-log-probe --sessao-errada --status-erro
#        --stale-hash --inativo --ida-volta --print-velho --ida-volta-sem-marcador
STUB_FONTE = r'''
import sys, os, json, hashlib

ARGV_FILE = @ARGV_FILE@
PERFIL = @PERFIL@
OUT = @OUT@
MARKER = @MARKER@
FLAGS = set(sys.argv[1:])
CFG = os.path.join(PERFIL, "BepInEx", "config", "com.gumatos.aut4probe.cfg")


def ler_cfg():
    valores = {}
    try:
        with open(CFG, encoding="utf-8") as fh:
            for linha in fh:
                if "=" in linha:
                    chave, valor = linha.split("=", 1)
                    valores[chave.strip()] = valor.strip()
    except OSError:
        pass
    return valores


cfg = ler_cfg()
with open(ARGV_FILE, "w", encoding="utf-8") as fh:
    fh.write(json.dumps({"argv": sys.argv, "cfg": cfg}))

if "--nao-escreve" in FLAGS:
    sys.exit(0)

log_dir = os.path.join(PERFIL, "BepInEx")
os.makedirs(log_dir, exist_ok=True)
linhas = ["Chainloader startup complete"]
if "--sem-log-probe" not in FLAGS:
    linhas.append("AUT4 PROBE: tick via BepInEx.Update (quadro 1)")
with open(os.path.join(log_dir, "LogOutput.log"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(linhas) + "\n")

dll = os.path.join(PERFIL, "BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
h = hashlib.sha256(open(dll, "rb").read()).hexdigest() if os.path.isfile(dll) else ""
if "--stale-hash" in FLAGS:
    h = "0" * 64

os.makedirs(OUT, exist_ok=True)
prints = []
if "--sem-print" not in FLAGS:
    png = os.path.join(OUT, "01-ui.png")
    if "--print-velho" not in FLAGS:
        with open(png, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
    prints.append(png.replace("\\", "/"))

sessao = cfg.get("Sessao") or "SEM-SESSAO-NA-CFG"
if "--sessao-errada" in FLAGS:
    sessao = "OUTRA-SESSAO-QUALQUER"

obs = [{
    "objeto": "Tooltip.Title", "caminho": "GUI Manager/Tooltip/Title",
    "componente": "TextMeshProUGUI", "ativo_na_hierarquia": True, "visivel_na_tela": True,
    "texto_bruto": MARKER, "texto_renderizado": MARKER,
    "fonte": "LiberationSans SDF", "material": "m", "shader": "TextMeshPro/Distance Field",
    "shader_suportado": True, "tamanho_fonte": 24.0,
    "keywords": {"OUTLINE_ON": True}, "cores": {"face": "#FFFFFFFF"},
    "geometria": {"caixa_na_tela_px": {"x": 1, "y": 2, "largura": 3, "altura": 4}, "escala": 1.0, "tela": "1920x1080"},
    "owners": ["com.gumatos.bettertooltips"],
    "personagem": {"gui_state": "InMainMenu", "tem_personagem_selecionado": False, "personagem": None},
    "nota_texto_renderizado": None,
}]
if "--inativo" in FLAGS:
    obs.append({
        "objeto": "Tooltip.Description", "caminho": "GUI Manager/Tooltip/Description",
        "componente": "TextMeshProUGUI", "ativo_na_hierarquia": False, "visivel_na_tela": False,
        "texto_bruto": MARKER + "-DESC", "texto_renderizado": "",
        "fonte": "LiberationSans SDF", "material": "m", "shader": "TextMeshPro/Distance Field",
        "shader_suportado": True, "tamanho_fonte": 18.0,
        "keywords": {}, "cores": {},
        "geometria": {"caixa_na_tela_px": {"x": 0, "y": 0, "largura": 0, "altura": 0}, "escala": 0.0, "tela": "1920x1080"},
        "owners": [],
        "personagem": {"gui_state": "InMainMenu", "tem_personagem_selecionado": False, "personagem": None},
        "nota_texto_renderizado": "objeto INATIVO: vale o texto_bruto.",
    })

status, fase = "CONCLUIDO", "concluido"
if "--status-erro" in FLAGS:
    status, fase = "ERRO", "erro"

probe = {"esquema": "AUT-4/1", "status": status, "fase": fase,
         "sessao": sessao, "hash_fonte": h, "total_observacoes": len(obs),
         "observacoes": obs, "prints": prints}
if "--ida-volta" in FLAGS:
    marca = cfg.get("MarcadorIdaEVolta") or MARKER
    probe["ida_e_volta"] = {"marcador": marca, "titulo_lido": marca, "conferiu": True,
                            "via": "Tooltip.ShowTooltip(marcador) + releitura de Tooltip.Title"}
if "--ida-volta-sem-marcador" in FLAGS:
    # A6 (COR-AUT4-F2): autodeclaracao `conferiu: true` SEM o marcador do driver.
    probe["ida_e_volta"] = {"titulo_lido": MARKER, "conferiu": True,
                            "via": "autodeclaracao sem o marcador do driver"}
with open(os.path.join(OUT, "aut4probe.json"), "w", encoding="utf-8") as fh:
    json.dump(probe, fh, ensure_ascii=False)
'''

ALVOS_TOTAL = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material",
               "shader", "keywords", "cores", "geometria", "owners"]


def _stub(dirbase, perfil, out, marcador="CIC5-MARCADOR-DISCO"):
    argv_file = os.path.join(dirbase, "stub-argv.json")
    caminho = os.path.join(dirbase, "stub_lancador.py")
    fonte = (STUB_FONTE.replace("@ARGV_FILE@", json.dumps(argv_file))
             .replace("@PERFIL@", json.dumps(perfil))
             .replace("@OUT@", json.dumps(out))
             .replace("@MARKER@", json.dumps(marcador)))
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(fonte)
    return caminho, argv_file


def _plano(alvos=None, demostrar=False):
    plano = dict(C.fixture("plano-exemplo"))
    plano["campos_alvo"] = list(alvos if alvos is not None else ALVOS_TOTAL)
    if demostrar:
        plano["demostrar_tooltip"] = True
    return plano


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _dll_falsa(dirbase):
    p = os.path.join(dirbase, "Aut4Probe.dll")
    with open(p, "wb") as fh:
        fh.write(b"MZ-dll-falsa-para-o-teste-do-caminho-executavel")
    return p


def _rodar(col, plano, raiz, nome, dll, flags=(), timeout=30):
    perfil = os.path.join(raiz, "perfil-" + nome)
    out = os.path.join(raiz, "out-" + nome)
    stub, argv_file = _stub(raiz, perfil, out, marcador="CIC5-" + nome.upper())
    r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                 autorizado=True, jogo_disponivel=True, confirmacao="coleta",
                                 comando_lancamento=[sys.executable, stub] + list(flags),
                                 timeout_s=timeout, poll_s=0.1)
    return r, cod, perfil, out, argv_file


def corpo():
    col = C.coletor()
    plano = _plano()

    with tempfile.TemporaryDirectory(prefix="aut5-exec-") as raiz:
        perfil = os.path.join(raiz, "perfil")          # ISOLADO (fixture), nao o do dono
        out = os.path.join(raiz, "out")
        dll = _dll_falsa(raiz)

        # ---------------- CASO A: default (nao autorizado) NAO age ----------------
        stub, argv_file = _stub(raiz, perfil, out)
        r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                     autorizado=False, jogo_disponivel=True,
                                     confirmacao="coleta",
                                     comando_lancamento=[sys.executable, stub],
                                     timeout_s=10, poll_s=0.1)
        C.arc.igual(cod, 2, "A: default-nao-autorizado -> exit 2")
        C.arc.igual(r["status"], "NAO_EXERCITADO", "A: status NAO_EXERCITADO")
        C.arc.igual(r.get("efeitos_colaterais", []), [], "A: zero efeito colateral")
        C.arc.exigir(not os.path.exists(os.path.join(perfil, PROBE_REL)),
                     "A: NENHUM probe instalado no default")
        C.arc.exigir(not os.path.exists(os.path.join(perfil, CFG_REL)),
                     "A: NENHUM cfg escrito no default")
        C.arc.exigir(not os.path.exists(argv_file),
                     "A: o STUB nao pode ter sido executado no default")

        # ---------------- CASO B: autorizado -> instala/lanca/espera/PROVA/reverte ---
        r, cod, perfil_b, out_b, argv_file = _rodar(col, plano, raiz, "b", dll)
        C.arc.igual(cod, 0, "B: autorizado+confirmado -> exit 0")
        C.arc.igual(r["status"], "CONCLUIDO", "B: status CONCLUIDO")
        C.arc.igual(r["atualidade"]["fonte_ok"], True, "B: fonte/dll/sessao atuais")

        # A1: as tres provas de execucao TEM de estar no resultado
        provas = r.get("provas_execucao") or {}
        C.arc.igual(provas.get("ok"), True, "A1/B: as tres provas de execucao fecham")
        C.arc.igual(provas.get("sessao_confere"), True, "A1/B: o JSON traz a sessao DESTA rodada")
        C.arc.igual(provas.get("json_mais_novo"), True, "A1/B: o JSON e mais novo que o lancamento")
        C.arc.igual(provas.get("log_chainloader"), True, "A1/B: o log da rodada tem o fim do chainloader")
        C.arc.igual(provas.get("log_probe"), True, "A1/B: o log da rodada tem a linha de vida do probe")
        C.arc.igual(provas.get("prints_ok"), True, "A1/B: os prints existem com bytes>0")

        # prova de EXECUCAO REAL: o stub gravou o proprio argv em disco
        C.arc.exigir(os.path.isfile(argv_file), "B: o stub TEM de ter rodado (argv em disco)")
        registro = json.load(open(argv_file, encoding="utf-8"))
        argv = registro["argv"]
        C.arc.exigir("-applaunch" in argv, "B: argv real tem -applaunch")
        C.arc.exigir("1330000" in argv, "B: argv real tem o AppID")
        C.arc.exigir("--doorstop-target-assembly" in argv, "B: argv real tem os argumentos de doorstop")
        C.arc.exigir(any("BepInEx.Preloader.dll" in str(a) for a in argv),
                     "B: argv aponta o preloader do perfil (porta correta)")

        # A1: a sessao da evidencia e a sessao que o DRIVER gerou e injetou no .cfg
        C.arc.exigir(registro["cfg"].get("Sessao"), "A1/B: o cfg derivado tem a chave Sessao")
        C.arc.igual(provas.get("sessao_rodada"), registro["cfg"]["Sessao"],
                    "A1/B: a sessao exigida e a do cfg (nao uma inventada)")
        C.arc.igual(provas.get("sessao_evidencia"), registro["cfg"]["Sessao"],
                    "A1/B: a evidencia consumida carrega a sessao do cfg")

        # cfg derivado (evidencia preservada; o cfg do perfil e removido no rollback)
        ev = os.path.join(out_b, "cfg-instalado.cfg")
        C.arc.exigir(os.path.isfile(ev), "B: o cfg instalado fica como evidencia no out")
        texto = open(ev, encoding="utf-8").read()
        C.arc.exigir("Autorizado = true" in texto, "B: cfg com Autorizado=true")
        C.arc.exigir("Navegar = false" in texto, "B: cfg com Navegar=false (default)")
        C.arc.exigir(_sha(dll) in texto, "B: cfg com HashFonte = sha256 da DLL")
        C.arc.exigir(perfil_b.replace("\\", "\\\\") in texto or perfil_b in texto,
                     "B: cfg com PerfilDir")

        # observacao consumida veio do JSON que o stub escreveu (marcador no disco)
        cons = r["consolidado"]
        marcador_em_disco = json.load(open(os.path.join(out_b, "aut4probe.json"),
                                           encoding="utf-8"))["observacoes"][0]["texto_bruto"]
        textos = [o["campos"]["texto_renderizado"]["valor"] for o in cons["observacoes"]
                  if o["campos"].get("texto_renderizado", {}).get("valor")]
        C.arc.exigir(marcador_em_disco in textos,
                     "B: a observacao consolidada veio do artefato em disco (nao de mensagem inventada)")

        # rollback EXATO: o perfil volta ao que era (nada existia antes)
        C.arc.exigir(not os.path.exists(os.path.join(perfil_b, PROBE_REL)),
                     "B: dll do probe removida no rollback")
        C.arc.exigir(not os.path.isdir(os.path.join(perfil_b, "BepInEx", "plugins", "AUT4Probe")),
                     "B: pasta do probe removida no rollback")
        C.arc.exigir(not os.path.exists(os.path.join(perfil_b, CFG_REL)),
                     "B: cfg criado pelo run foi removido")
        C.arc.exigir(not os.path.exists(os.path.join(perfil_b, LOG_REL)),
                     "B: log (truncado no boot) removido quando nao existia antes")
        C.arc.igual(sorted(r["rollback"]["plano"]["criados"]), sorted(
            [PROBE_REL.replace("/", os.sep), CFG_REL.replace("/", os.sep), LOG_REL.replace("/", os.sep)]),
            "B: rollback classifica os 3 arquivos criados")

        # ---------------- CASO C: arquivos PRE-EXISTENTES voltam byte a byte ------
        perfil2 = os.path.join(raiz, "perfil2")
        out2 = os.path.join(raiz, "out2")
        os.makedirs(os.path.join(perfil2, "BepInEx", "config"))
        cfg2 = os.path.join(perfil2, CFG_REL)
        log2 = os.path.join(perfil2, LOG_REL)
        cfg_bytes = b"[Geral]\nAutorizado = false\n"
        log_bytes = b"LOG-ANTIGO-DO-DONO\n"
        open(cfg2, "wb").write(cfg_bytes)
        open(log2, "wb").write(log_bytes)
        stub2, _ = _stub(raiz, perfil2, out2, marcador="CIC5-MARCADOR-2")
        r2, cod2 = col.executar_rodada(plano, perfil_dir=perfil2, out_dir=out2, dll_probe=dll,
                                       autorizado=True, jogo_disponivel=True,
                                       confirmacao="coleta",
                                       comando_lancamento=[sys.executable, stub2],
                                       timeout_s=30, poll_s=0.1)
        C.arc.igual(cod2, 0, "C: rodada autorizada conclui")
        C.arc.igual(open(cfg2, "rb").read(), cfg_bytes, "C: cfg pre-existente RESTAURADO byte a byte")
        C.arc.igual(open(log2, "rb").read(), log_bytes, "C: log pre-existente RESTAURADO byte a byte")
        C.arc.exigir(not os.path.exists(os.path.join(perfil2, PROBE_REL)),
                     "C: dll nova removida")
        mods = r2["rollback"]["plano"]["modificados"]
        C.arc.exigir(CFG_REL.replace("/", os.sep) in mods and LOG_REL.replace("/", os.sep) in mods,
                     "C: cfg e log contados como MODIFICADOS (restaurados)")

        # ---------------- CASO D: hash de fonte STALE -> nao vira OK --------------
        r3, cod3, _, _, _ = _rodar(col, plano, raiz, "d", dll, flags=("--stale-hash",))
        C.arc.igual(r3["atualidade"]["fonte_ok"], False, "D: hash de fonte desatualizado detectado")
        C.arc.exigir(cod3 != 0, "D: hash stale NAO pode dar exit 0")
        C.arc.igual(r3["status"], "INDETERMINADO", "D: stale -> INDETERMINADO")
        C.arc.exigir(r3["atualidade"]["motivos"], "D: o motivo da nao-atualidade fica registrado")

        # ============ A1 (GRAVE): JSON de rodada ANTERIOR nao confirma ============
        # 1a rodada grava o JSON dessa rodada; 2a NAO escreve nada (o JSON velho fica).
        _, cod_e1, perfil_e, out_e, _ = _rodar(col, plano, raiz, "e", dll)
        C.arc.igual(cod_e1, 0, "A1/E: a 1a rodada (que escreve) conclui")
        time.sleep(1.2)                       # garante mtime estritamente mais antigo
        stub_e, argv_e = _stub(raiz, perfil_e, out_e, marcador="A1-E")
        r_e, cod_e = col.executar_rodada(plano, perfil_dir=perfil_e, out_dir=out_e, dll_probe=dll,
                                         autorizado=True, jogo_disponivel=True,
                                         confirmacao="coleta",
                                         comando_lancamento=[sys.executable, stub_e, "--nao-escreve"],
                                         timeout_s=1, poll_s=0.1)
        C.arc.exigir(cod_e != 0, "A1/E: rodada que NAO escreveu nada NAO pode dar exit 0")
        C.arc.igual(r_e["status"], "NAO_EXERCITADO",
                    "A1/E: JSON de rodada anterior NAO vira CONCLUIDO")
        C.arc.igual(r_e["provas_execucao"]["sessao_confere"], False,
                    "A1/E: a sessao da evidencia velha nao confere")
        C.arc.igual(r_e["provas_execucao"]["json_mais_novo"], False,
                    "A1/E: o JSON e anterior ao lancamento desta rodada")

        # ============ A1b: JSON novo, MAS de outra sessao -> NAO_EXERCITADO =======
        r_f, cod_f, _, _, _ = _rodar(col, plano, raiz, "f", dll, flags=("--sessao-errada",))
        C.arc.igual(r_f["provas_execucao"]["json_mais_novo"], True, "A1/F: o JSON e novo")
        C.arc.igual(r_f["provas_execucao"]["sessao_confere"], False,
                    "A1/F: sessao diferente da rodada -> nao confere")
        C.arc.igual(r_f["status"], "NAO_EXERCITADO", "A1/F: sessao errada -> NAO_EXERCITADO")
        C.arc.exigir(cod_f != 0, "A1/F: exit != 0")

        # ============ A1c: sem PNG/prints -> INDETERMINADO ========================
        r_g, cod_g, _, _, _ = _rodar(col, plano, raiz, "g", dll, flags=("--sem-print",))
        C.arc.igual(r_g["provas_execucao"]["prints_ok"], False, "A1/G: prints vazios nao passam")
        C.arc.igual(r_g["status"], "INDETERMINADO", "A1/G: sem print -> INDETERMINADO")
        C.arc.exigir(cod_g != 0, "A1/G: exit != 0")
        C.arc.exigir(any("print" in f for f in r_g["provas_execucao"]["faltas"]),
                     "A1/G: a falta registrada nomeia os prints")

        # ============ A1d: log sem a linha de vida do probe -> INDETERMINADO ======
        r_h, cod_h, _, _, _ = _rodar(col, plano, raiz, "h", dll, flags=("--sem-log-probe",))
        C.arc.igual(r_h["provas_execucao"]["log_probe"], False, "A1/H: log sem linha do probe nao passa")
        C.arc.igual(r_h["status"], "INDETERMINADO", "A1/H: log sem probe -> INDETERMINADO")
        C.arc.exigir(cod_h != 0, "A1/H: exit != 0")

        # ==== A1c (COR-AUT4-F2): PNG de rodada ANTERIOR no out_dir REUSADO =======
        # o out_dir e reusado por desenho; um PNG VELHO no caminho listado nao
        # prova ESTA rodada (o stub lista o print mas NAO produz imagem nova).
        out_i1c = os.path.join(raiz, "out-i1c")
        os.makedirs(out_i1c, exist_ok=True)
        png_velho = os.path.join(out_i1c, "01-ui.png")
        with open(png_velho, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n" + b"9" * 64)
        os.utime(png_velho, (time.time() - 3600.0, time.time() - 3600.0))
        r_i1c, cod_i1c, _, _, _ = _rodar(col, plano, raiz, "i1c", dll, flags=("--print-velho",))
        C.arc.igual(r_i1c["provas_execucao"]["prints_ok"], False,
                    "A1c: print ANTERIOR a rodada nao vale (mesmo existindo com bytes>0)")
        C.arc.igual(r_i1c["status"], "INDETERMINADO", "A1c: PNG velho -> INDETERMINADO")
        C.arc.exigir(cod_i1c != 0, "A1c: exit != 0")

        # ============ A2 (GRAVE): alvo do objeto INATIVO nao "fecha" ==============
        r_i, cod_i, _, _, _ = _rodar(col, plano, raiz, "i", dll, flags=("--inativo",))
        cons_i = r_i["consolidado"]
        C.arc.exigir(cons_i["status"] != "CONFIRMADA",
                     "A2/I: objeto inativo com alvo nao lido NAO pode consolidar CONFIRMADA")
        C.arc.igual(cons_i["status"], "INCOMPLETO", "A2/I: alvo NAO_APLICAVEL -> INCOMPLETO")
        C.arc.exigir("texto_renderizado" in cons_i["lacunas"],
                     "A2/I: o alvo nao lido aparece nas lacunas")
        C.arc.exigir({"owners", "keywords", "cores"} <= set(cons_i["lacunas"]),
                     "A2/I (COR-AUT4-F2): vazio e NAO LIDO — owners=[] e keywords/cores={} em lacunas")
        C.arc.exigir(cod_i != 0, "A2/I: exit != 0")
        C.arc.igual(r_i["status"], "INCOMPLETO", "A2/I: a rodada NAO e CONCLUIDO")

        # ============ A6: ida-e-volta exigida quando o plano demonstra tooltip ====
        plano_a6 = _plano(demostrar=True)
        r_j, cod_j, _, out_j, _ = _rodar(col, plano_a6, raiz, "j", dll)
        texto_j = open(os.path.join(out_j, "cfg-instalado.cfg"), encoding="utf-8").read()
        C.arc.exigir("DemostrarTooltip = true" in texto_j,
                     "A6/J: o plano com demostrar_tooltip liga DemostrarTooltip no cfg")
        C.arc.exigir("MarcadorIdaEVolta =" in texto_j, "A6/J: o cfg traz o marcador da ida-e-volta")
        C.arc.igual(r_j["status"], "INDETERMINADO",
                    "A6/J: sem a prova de ida-e-volta o driver NAO confirma")
        C.arc.exigir(cod_j != 0, "A6/J: exit != 0")

        r_k, cod_k, _, _, _ = _rodar(col, plano_a6, raiz, "k", dll, flags=("--ida-volta",))
        C.arc.igual(r_k["provas_execucao"]["ida_e_volta_ok"], True,
                    "A6/K: com a prova de ida-e-volta o criterio fecha")
        C.arc.igual(r_k["status"], "CONCLUIDO", "A6/K: com a prova -> CONCLUIDO")
        C.arc.igual(cod_k, 0, "A6/K: exit 0")

        # ==== A6 (COR-AUT4-F2): `conferiu:true` SEM o marcador do driver =========
        r_a6m, cod_a6m, _, _, _ = _rodar(col, plano_a6, raiz, "a6m", dll,
                                          flags=("--ida-volta-sem-marcador",))
        C.arc.igual(r_a6m["provas_execucao"]["ida_e_volta_ok"], False,
                    "A6m: autodeclaracao SEM o marcador do driver NAO pode conferir")
        C.arc.igual(r_a6m["status"], "INDETERMINADO",
                    "A6m: sem o marcador do driver -> INDETERMINADO")
        C.arc.exigir(cod_a6m != 0, "A6m: exit != 0")

        # == A2 secundario (COR-AUT4-F2): plano invalido barra ANTES de tocar o perfil ==
        plano_ruim = _plano(alvos=["field_typo"])
        pv_base = os.path.join(raiz, "pv")            # dirbase PROPRIO (argv isolado)
        os.makedirs(pv_base)
        perfil_pv = os.path.join(raiz, "perfil-pv")
        out_pv = os.path.join(raiz, "out-pv")
        stub_pv, argv_pv = _stub(pv_base, perfil_pv, out_pv)
        r_pv, cod_pv = col.executar_rodada(plano_ruim, perfil_dir=perfil_pv, out_dir=out_pv,
                                           dll_probe=dll, autorizado=True, jogo_disponivel=True,
                                           confirmacao="coleta",
                                           comando_lancamento=[sys.executable, stub_pv])
        C.arc.igual(r_pv["status"], "PLANO_INVALIDO",
                    "A2-sec: campos_alvo invalido -> PLANO_INVALIDO (nao instala/lanca)")
        C.arc.igual(cod_pv, 2, "A2-sec: plano invalido -> exit 2")
        C.arc.exigir(not os.path.exists(argv_pv), "A2-sec: o STUB nao pode ter rodado")
        C.arc.exigir(not os.path.exists(os.path.join(perfil_pv, PROBE_REL)),
                     "A2-sec: NENHUM probe instalado com plano invalido")
        C.arc.exigir(not os.path.exists(os.path.join(perfil_pv, CFG_REL)),
                     "A2-sec: NENHUM cfg escrito com plano invalido")

        # ====== A5: DIRETORIO pre-existente (pasta do probe vazia) sobrevive ======
        perfil_l = os.path.join(raiz, "perfil-l")
        out_l = os.path.join(raiz, "out-l")
        pasta_probe = os.path.join(perfil_l, "BepInEx", "plugins", "AUT4Probe")
        os.makedirs(pasta_probe)
        stub_l, _ = _stub(raiz, perfil_l, out_l, marcador="A5-L")
        r_l, cod_l = col.executar_rodada(plano, perfil_dir=perfil_l, out_dir=out_l, dll_probe=dll,
                                         autorizado=True, jogo_disponivel=True,
                                         confirmacao="coleta",
                                         comando_lancamento=[sys.executable, stub_l],
                                         timeout_s=30, poll_s=0.1)
        C.arc.igual(cod_l, 0, "A5/L: a rodada conclui")
        C.arc.exigir(os.path.isdir(pasta_probe),
                     "A5/L: pasta do probe PRE-EXISTENTE nao pode ser removida no rollback")
        C.arc.exigir(not os.path.exists(os.path.join(perfil_l, PROBE_REL)),
                     "A5/L: a dll (essa sim, nasceu na rodada) foi removida")
        C.arc.exigir(not os.path.exists(os.path.join(perfil_l, CFG_REL)),
                     "A5/L: o cfg criado foi removido")
        C.arc.exigir("BepInEx/plugins/AUT4Probe" not in
                     [str(d).replace(os.sep, "/") for d in
                      r_l["rollback"]["plano"].get("dirs_criados", [])],
                     "A5/L: diretorio pre-existente nao entra em 'dirs_criados'")


if __name__ == "__main__":
    C.arc.main(META, corpo)
