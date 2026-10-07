#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUD-1 — ESPERA/TIMEOUT, BACKUP, MANIFESTO e RESTAURACAO EXATA (sem residuo).

Esta frente (t_7e8f495b) fecha as lacunas L1/L2 da auditoria AUD-1
(`docs/automacao/AUD-1-auditoria-reuso-CAP1-fixtures-checa_shrines.md`) e prova, por
execucao offline, o contrato de restauracao/rollback:

  * VARREDURA (L1) — a rodada vigia `BepInEx/plugins/**` e `BepInEx/config/**`
    inteiros, nao so os 3 nomes do contrato: arquivo que a rodada cria num caminho
    NAO previsto entra em `criados` e volta no rollback (o BepInEx varre `plugins/`
    recursivamente: arquivo que nasce ali vira mod carregado);
  * BACKUP DE LOG — `backup_do_log` arquiva o `LogOutput.log` antes do lancamento
    (um boot TRUNCA o log) e registra bytes/sha256; ausencia e DECLARADA;
  * MANIFESTO — `montar_manifest_da_rodada` descreve artefato por nome/bytes/sha256,
    o estado antes/depois de cada arquivo vigiado (criado/modificado/removido/
    intocado) e o backup que permite restaurar;
  * RESTAURACAO — `verificar_sem_residuo` prova (pos-rollback) que o perfil voltou
    EXATO; residuo/divergencia/falta/diretorio sobrando => `limpo=False` e a rodada
    sai `RESIDUO`/exit 1, nunca "limpa";
  * ENCERRAMENTO (L2) — o jogo e fechado em DUAS ETAPAS: GRACIOSO
    (`CloseMainWindow`, que funciona onde `taskkill` e bloqueado) e so depois o
    FORCADO por PID; sem medicao, RECUSA (nada e executado).

Nada aqui abre/encerra o jogo: o "lancamento" e um STUB (processo real, sem jogo) e
os executores de fechamento sao INJETADOS (gravam o argv, nao fecham processo
nenhum). Perfil sempre ISOLADO em diretorio de fixture/scratch.
"""
import hashlib
import json
import os
import sys
import tempfile

import comum as C

META = {
    "nome": "aut4-restauracao",
    "categoria": "pura",
    "requer": [],
    "descricao": "espera/timeout, backup de log, manifesto e RESTAURACAO EXATA (sem residuo) "
                 "com varredura de arvore + encerramento em duas etapas (gracioso->forcado)",
}

PRELOADER_REL = os.path.join("BepInEx", "core", "BepInEx.Preloader.dll")
PROBE_REL = os.path.join("BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
CFG_REL = os.path.join("BepInEx", "config", "com.gumatos.aut4probe.cfg")
LOG_REL = os.path.join("BepInEx", "LogOutput.log")
EXTRA_REL = os.path.join("BepInEx", "plugins", "extra-mod", "extra.dll")

# Stub do lancador: escreve log de boot + linha de vida do probe, PNG, JSON do probe
# (com a sessao DESTA rodada e o hash da DLL instalada) e, com --extra, um arquivo
# num caminho que o CONTRATO NAO PREVE (é o "criado durante a coleta" da prova).
# --extra-travado cria esse arquivo somente-leitura (o rollback entao FALHA de verdade).
STUB_FONTE = r'''
import sys, os, json, hashlib

PERFIL = @PERFIL@
OUT = @OUT@
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
log_dir = os.path.join(PERFIL, "BepInEx")
os.makedirs(log_dir, exist_ok=True)
with open(os.path.join(log_dir, "LogOutput.log"), "w", encoding="utf-8") as fh:
    fh.write("Chainloader startup complete\n")
    fh.write("AUT4 PROBE: tick via BepInEx.Update (quadro 1)\n")

dll = os.path.join(PERFIL, "BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
h = hashlib.sha256(open(dll, "rb").read()).hexdigest() if os.path.isfile(dll) else ""

os.makedirs(OUT, exist_ok=True)
png = os.path.join(OUT, "01-ui.png")
with open(png, "wb") as fh:
    fh.write(b"\x89PNG\r\n\x1a\n" + b"0" * 64)

if "--extra" in FLAGS:
    extra_dir = os.path.join(PERFIL, "BepInEx", "plugins", "extra-mod")
    os.makedirs(extra_dir, exist_ok=True)
    extra = os.path.join(extra_dir, "extra.dll")
    with open(extra, "wb") as fh:
        fh.write(b"MZ-extra-criado-pela-rodada")
    if "--extra-travado" in FLAGS:
        os.chmod(extra, 0o444)

obs = [{
    "objeto": "Tooltip.Title", "caminho": "GUI Manager/Tooltip/Title",
    "componente": "TextMeshProUGUI", "ativo_na_hierarquia": True, "visivel_na_tela": True,
    "texto_bruto": "REST-MARCADOR", "texto_renderizado": "REST-MARCADOR",
    "fonte": "LiberationSans SDF", "material": "m", "shader": "TextMeshPro/Distance Field",
    "shader_suportado": True, "tamanho_fonte": 24.0,
    "keywords": {"OUTLINE_ON": True}, "cores": {"face": "#FFFFFFFF"},
    "geometria": {"caixa_na_tela_px": {"x": 1, "y": 2, "largura": 3, "altura": 4},
                  "escala": 1.0, "tela": "1920x1080"},
    "owners": ["com.gumatos.bettertooltips"],
    "personagem": {"gui_state": "InMainMenu", "tem_personagem_selecionado": False,
                   "personagem": None},
    "nota_texto_renderizado": None,
}]
probe = {"esquema": "AUT-4/1", "status": "CONCLUIDO", "fase": "concluido",
         "sessao": cfg.get("Sessao") or "SEM-SESSAO", "hash_fonte": h,
         "total_observacoes": len(obs), "observacoes": obs,
         "prints": [png.replace("\\", "/")]}
with open(os.path.join(OUT, "aut4probe.json"), "w", encoding="utf-8") as fh:
    json.dump(probe, fh, ensure_ascii=False)
'''

ALVOS = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material", "shader",
         "keywords", "cores", "geometria", "owners"]


def _sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _stub(dirbase, perfil, out):
    caminho = os.path.join(dirbase, "stub_rest.py")
    fonte = (STUB_FONTE.replace("@PERFIL@", json.dumps(perfil))
             .replace("@OUT@", json.dumps(out)))
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(fonte)
    return caminho


def _dll_falsa(dirbase):
    p = os.path.join(dirbase, "Aut4Probe.dll")
    with open(p, "wb") as fh:
        fh.write(b"MZ-dll-falsa-para-o-teste-de-restauracao")
    return p


def _plano(alvos=None):
    plano = dict(C.fixture("plano-exemplo"))
    plano["campos_alvo"] = list(alvos if alvos is not None else ALVOS)
    return plano


# ---------------------------------------------------------------- varredura (L1)

def _varredura(col):
    with tempfile.TemporaryDirectory(prefix="aut4-rest-varr-") as raiz:
        perfil = os.path.join(raiz, "perfil")
        fundo = os.path.join(perfil, "BepInEx", "plugins", "mod", "sub")
        os.makedirs(fundo)
        alvo = os.path.join(fundo, "coisa.txt")
        open(alvo, "w", encoding="utf-8").write("criado longe do contrato")
        vigiados = col.caminhos_vigiados(perfil, [PROBE_REL, CFG_REL, LOG_REL])
        C.arc.exigir(os.path.join("BepInEx", "plugins", "mod", "sub", "coisa.txt") in vigiados,
                     "L1: a varredura TEM de enxergar arquivo em subpasta de plugins (nao so "
                     "os 3 nomes do contrato)")
        C.arc.exigir(LOG_REL in vigiados, "L1: o LogOutput.log do contrato continua vigiado")
        snap = col.snapshot_arquivos(perfil, vigiados)
        C.arc.igual(snap[os.path.join("BepInEx", "plugins", "mod", "sub", "coisa.txt")],
                    _sha(alvo), "L1: o arquivo varrido entra no snapshot com o sha256 real")


# ------------------------------------------------------------- backup de log

def _backup_log(col):
    with tempfile.TemporaryDirectory(prefix="aut4-rest-bkp-") as raiz:
        log = os.path.join(raiz, "BepInEx", "LogOutput.log")
        os.makedirs(os.path.dirname(log))
        C.arc.igual(col.backup_do_log(log, raiz)["existia"], False,
                    "BKP: sem log anterior a AUSENCIA e declarada (nada inventado)")
        log_bytes = b"LOG-ANTIGO-DO-DONO\n"
        with open(log, "wb") as fh:
            fh.write(log_bytes)
        sha_antes = _sha(log)
        registro = col.backup_do_log(log, raiz)
        C.arc.igual(registro["existia"], True, "BKP: log anterior declarado")
        C.arc.igual(registro["bytes"], len(log_bytes), "BKP: bytes do backup")
        C.arc.igual(registro["sha256"], sha_antes, "BKP: sha256 do backup = sha do original")
        C.arc.exigir(not os.path.exists(log),
                     "BKP: o log do perfil e REMOVIDO (o boot desta rodada passa a ser o unico)")
        C.arc.igual(_sha(registro["backup"]), sha_antes,
                    "BKP: o arquivo de backup tem os MESMOS bytes do original")
        C.arc.exigir(os.path.basename(registro["backup"]) == "log-anterior.log",
                     "BKP: o backup fica como log-anterior.log no out_dir")


# ----------------------------------------------- restauracao / residuo (prova)

def _residuo(col):
    with tempfile.TemporaryDirectory(prefix="aut4-rest-res-") as raiz:
        perfil = os.path.join(raiz, "perfil")
        os.makedirs(os.path.join(perfil, "BepInEx", "config"))
        antigo = os.path.join(perfil, "BepInEx", "config", "outro.cfg")
        open(antigo, "w", encoding="utf-8").write("original\n")
        relativos = col.caminhos_vigiados(perfil, [PROBE_REL, CFG_REL, LOG_REL])
        antes = col.snapshot_arquivos(perfil, relativos)
        dirs_antes = col.snapshot_dirs(perfil, relativos)

        C.arc.igual(col.verificar_sem_residuo(perfil, relativos, antes, dirs_antes)["limpo"],
                    True, "RES: nada tocado => restauracao limpa")

        # (a) arquivo CRIADO que sobrou
        criado = os.path.join(perfil, "BepInEx", "plugins", "mod", "novo.dll")
        os.makedirs(os.path.dirname(criado))
        open(criado, "wb").write(b"residuo")
        r = col.verificar_sem_residuo(perfil, relativos, antes, dirs_antes)
        C.arc.igual(r["limpo"], False, "RES: arquivo criado sobrando NAO pode ser 'limpo'")
        C.arc.exigir(os.path.join("BepInEx", "plugins", "mod", "novo.dll") in r["residuos"],
                     "RES: o residuo e NOMEADO")
        C.arc.exigir("BepInEx/plugins/mod" in [d.replace(os.sep, "/") for d in r["dirs_residuo"]],
                     "RES: o diretorio criado pela rodada que sobrou tambem e residuo")
        os.remove(criado)
        os.rmdir(os.path.dirname(criado))                              # .../plugins/mod
        os.rmdir(os.path.dirname(os.path.dirname(criado)))             # .../plugins

        # (b) arquivo MODIFICADO (divergente)
        open(antigo, "w", encoding="utf-8").write("ALTERADO\n")
        r = col.verificar_sem_residuo(perfil, relativos, antes, dirs_antes)
        C.arc.igual(r["limpo"], False, "RES: hash diferente NAO e restauracao")
        C.arc.exigir(os.path.join("BepInEx", "config", "outro.cfg") in r["divergentes"],
                     "RES: o divergente e nomeado")
        open(antigo, "w", encoding="utf-8").write("original\n")

        # (c) arquivo REMOVIDO que nao voltou
        os.remove(antigo)
        r = col.verificar_sem_residuo(perfil, relativos, antes, dirs_antes)
        C.arc.exigir(os.path.join("BepInEx", "config", "outro.cfg") in r["faltando"],
                     "RES: arquivo que a rodada removeu e nao voltou tem de ser declarado")
        open(antigo, "w", encoding="utf-8").write("original\n")
        C.arc.igual(col.verificar_sem_residuo(perfil, relativos, antes, dirs_antes)["limpo"],
                    True, "RES: devolvido ao estado de antes => limpo de novo")


# ------------------------------------------------------------------ manifesto

def _manifesto(col):
    with tempfile.TemporaryDirectory(prefix="aut4-rest-man-") as raiz:
        out = os.path.join(raiz, "out")
        perfil = os.path.join(raiz, "perfil")
        os.makedirs(out)
        json_ = os.path.join(out, "aut4probe.json")
        open(json_, "w", encoding="utf-8").write("{}")
        antes = {CFG_REL: "a" * 64}
        depois = {CFG_REL: "b" * 64, EXTRA_REL: "c" * 64}
        m = col.montar_manifest_da_rodada(out, perfil, sorted(set(antes) | set(depois)),
                                          antes, depois, backups={CFG_REL: "bkp"})
        C.arc.igual(m["total_artefatos"], 1, "MAN: o artefato de evidencia entra no manifest")
        C.arc.igual(m["artefatos"][0]["arquivo"], "aut4probe.json", "MAN: nomeado pelo relativo")
        C.arc.igual(m["artefatos"][0]["sha256"], _sha(json_), "MAN: sha256 medido do disco")
        por_arq = {i["arquivo"]: i for i in m["arquivos_vigiados"]}
        C.arc.igual(por_arq[EXTRA_REL]["estado"], "criado",
                    "MAN: arquivo que a rodada criou e classificado 'criado' (mesmo fora do contrato)")
        C.arc.igual(por_arq[CFG_REL]["estado"], "modificado", "MAN: cfg tocado e 'modificado'")
        C.arc.igual(por_arq[CFG_REL]["backup"], "bkp", "MAN: o manifest nomeia o backup")
        C.arc.exigir(EXTRA_REL in m["criados"], "MAN: a lista de 'criados' nomeia o extra")
        # estado 'intocado' e 'removido' tambem sao distinguidos
        m2 = col.montar_manifest_da_rodada(out, perfil, [],
                                           {"x": "1", "y": "2"}, {"x": "1"}, backups={})
        estados = {i["arquivo"]: i["estado"] for i in m2["arquivos_vigiados"]}
        C.arc.igual(estados["x"], "intocado", "MAN: hash igual => intocado")
        C.arc.igual(estados["y"], "removido", "MAN: sumiu => removido")


# ------------------------------------------------- encerramento em duas etapas

def _encerramento(col):
    comandos = col.comandos_de_fechamento(4242)
    C.arc.igual([c["modo"] for c in comandos], ["gracioso", "forcado"],
                "L2: a ORDEM e gracioso -> forcado")
    gracioso, forcado = comandos
    C.arc.exigir(any("CloseMainWindow" in str(a) for a in gracioso["argv"]),
                 "L2: o primeiro caminho e o fechamento gracioso (CloseMainWindow)")
    C.arc.exigir("4242" in " ".join(gracioso["argv"]), "L2: o gracioso e por PID")
    C.arc.igual(forcado["argv"][:3], ["taskkill", "/F", "/PID"], "L2: o forcado e por PID")

    # RECUSA (sem medicao) nao executa NADA.
    recusa = col.planejar_encerramento("Stolen Realm.exe", None, None)
    executados = []
    C.arc.igual(col.encerrar_processos(recusa, executar=executados.append,
                                       pid_vivo=lambda p: True), [],
                "L2: plano RECUSADO nao gera acao nenhuma")
    C.arc.igual(executados, [], "L2: recusado nao executa comando nenhum (fail-closed)")
    plano_vazio = col.planejar_encerramento("x.exe", {7}, {7})
    C.arc.igual(col.encerrar_processos(plano_vazio, executar=executados.append), [],
                "L2: nada-a-encerrar nao gera acao")

    # O gracioso resolveu: NAO escala para o forcado.
    plano = col.planejar_encerramento("Stolen Realm.exe", {100}, {100, 4242})
    chamadas = []
    acoes = col.encerrar_processos(plano, executar=chamadas.append,
                                   pid_vivo=lambda p: False, dormir=lambda s: None)
    C.arc.igual(plano["pids"], [4242], "L2: encerra SO o PID novo (o do dono nao)")
    C.arc.igual(len(chamadas), 1, "L2: com o gracioso funcionando, NAO ha comando forcado")
    C.arc.igual(acoes[0]["tentativas"][0]["modo"], "gracioso", "L2: tentou o gracioso")
    C.arc.igual(acoes[0]["fechado"], True, "L2: fechado confirmado pela medicao do PID")

    # O processo CONTINUA vivo: cai no forcado, na ordem.
    vivo = {"ok": True}
    chamadas2 = []
    acoes2 = col.encerrar_processos(plano, executar=chamadas2.append,
                                    pid_vivo=lambda p: vivo["ok"], dormir=lambda s: None)
    C.arc.igual([t["modo"] for t in acoes2[0]["tentativas"]], ["gracioso", "forcado"],
                "L2: gracioso primeiro e, se continuar vivo, forcado depois")
    C.arc.exigir(any("taskkill" in " ".join(c) for c in chamadas2),
                 "L2: o forcado por PID e o FALLBACK executado")
    # a medicao indisponivel tambem escala (nao da para confirmar que saiu)
    chamadas3 = []
    col.encerrar_processos(plano, executar=chamadas3.append, pid_vivo=lambda p: None,
                           dormir=lambda s: None)
    C.arc.igual(len(chamadas3), 2, "L2: sem confirmacao, o forcado tambem e tentado")

    fonte = open(os.path.join(C.RUNTIME, "coletor.py"), encoding="utf-8").read()
    C.arc.exigir('"/F", "/IM"' not in fonte,
                 "L2: matar por IMAGEM (todas as instancias) nao pode existir no driver")
    C.arc.exigir("CloseMainWindow" in fonte, "L2: o fechamento gracioso tem de estar no driver")


# ------------------------------------------------------- rodada completa (stub)

def _rodada(col, raiz, nome, dll, plano, flags=(), log_anterior=None, encerrar=None):
    perfil = os.path.join(raiz, "perfil-" + nome)
    out = os.path.join(raiz, "out-" + nome)
    if log_anterior is not None:
        os.makedirs(os.path.join(perfil, "BepInEx"), exist_ok=True)
        with open(os.path.join(perfil, LOG_REL), "wb") as fh:
            fh.write(log_anterior)
    stub = _stub(raiz, perfil, out)
    return col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                               autorizado=True, jogo_disponivel=True, confirmacao="coleta",
                               comando_lancamento=[sys.executable, stub] + list(flags),
                               timeout_s=30, poll_s=0.1, **(encerrar or {}))


def _rodada_completa(col):
    with tempfile.TemporaryDirectory(prefix="aut4-rest-rod-") as raiz:
        dll = _dll_falsa(raiz)
        plano = _plano()

        # ---- caso A: rodada limpa, com um arquivo criado FORA do contrato -------
        r, cod = _rodada(col, raiz, "extra", dll, plano, flags=("--extra",))
        C.arc.igual(cod, 0, "ROD/A: rodada limpa conclui (exit 0)")
        C.arc.igual(r["status"], "CONCLUIDO", "ROD/A: status CONCLUIDO")
        C.arc.igual(r["restauracao"]["limpo"], True,
                    "ROD/A: prova de restauracao EXATA (sem residuo)")
        C.arc.igual(r["backup_log"]["existia"], False,
                    "ROD/A: sem log anterior => ausencia declarada no registro do backup")
        criados = r["rollback"]["plano"]["criados"]
        C.arc.exigir(EXTRA_REL.replace("/", os.sep) in criados,
                     "ROD/A: o arquivo criado FORA do contrato entra em 'criados' e volta")
        C.arc.exigir(PROBE_REL.replace("/", os.sep) in criados, "ROD/A: a DLL do probe volta")
        C.arc.exigir(CFG_REL.replace("/", os.sep) in criados, "ROD/A: o cfg criado volta")
        perfil_a = os.path.join(raiz, "perfil-extra")
        C.arc.exigir(not os.path.exists(os.path.join(perfil_a, EXTRA_REL)),
                     "ROD/A: o extra sumiu do perfil (restauracao de arquivo criado na coleta)")
        C.arc.exigir(not os.path.isdir(os.path.join(perfil_a, "BepInEx", "plugins", "extra-mod")),
                     "ROD/A: o diretorio criado pela rodada tambem saiu (sem efeito residual)")
        C.arc.exigir(not os.path.isdir(os.path.join(perfil_a, "BepInEx")),
                     "ROD/A: o perfil voltou ao que era (nem BepInEx restou)")
        man = r["manifest"]
        C.arc.exigir(man["total_artefatos"] > 0, "ROD/A: o manifest lista os artefatos da rodada")
        nomes = [a["arquivo"] for a in man["artefatos"]]
        C.arc.exigir("aut4probe.json" in nomes, "ROD/A: o JSON do probe entra no manifest")
        C.arc.exigir(EXTRA_REL.replace("/", os.sep) in man["criados"],
                     "ROD/A: o manifest classifica o arquivo criado na coleta")

        # ---- caso B: log ANTERIOR e arquivado (bytes/sha) e RESTAURADO ----------
        log_bytes = b"LOG-ANTIGO-DO-DONO\n"
        r_b, cod_b = _rodada(col, raiz, "log", dll, plano, log_anterior=log_bytes)
        C.arc.igual(cod_b, 0, "ROD/B: a rodada conclui")
        bkp = r_b["backup_log"]
        C.arc.igual(bkp["existia"], True, "ROD/B: o log anterior foi detectado")
        C.arc.igual(bkp["sha256"],
                    hashlib.sha256(log_bytes).hexdigest(),
                    "ROD/B: o registro do backup traz o sha256 do log anterior")
        perfil_b = os.path.join(raiz, "perfil-log")
        C.arc.igual(open(os.path.join(perfil_b, LOG_REL), "rb").read(), log_bytes,
                    "ROD/B: o log do dono volta byte a byte no rollback")
        C.arc.igual(r_b["restauracao"]["limpo"], True, "ROD/B: restauracao exata")

        # ---- caso C: encerramento GRACIOSO primeiro (executor INJETADO) ---------
        chamadas = []
        plano_pids = [{100}, {100, 4242}]

        def medir(imagem):
            return plano_pids.pop(0)

        r_c, cod_c = _rodada(col, raiz, "fecha", dll, plano,
                             encerrar={"encerrar_imagem": "Stolen Realm.exe",
                                       "pids_medir": medir,
                                       "fechar_executar": chamadas.append,
                                       "pid_vivo": lambda p: False})
        C.arc.igual(cod_c, 0, "ROD/C: a rodada conclui com o encerramento decidido")
        C.arc.igual(r_c["encerramento"]["pids"], [4242],
                    "ROD/C: encerra o PID que nasceu na rodada (nao o 100, do dono)")
        C.arc.igual(len(chamadas), 1, "ROD/C: gracioso resolveu => zero comando forcado")
        C.arc.exigir("CloseMainWindow" in " ".join(chamadas[0]),
                     "ROD/C: o comando executado foi o fechamento gracioso")
        C.arc.igual(r_c["encerramento"]["acoes"][0]["tentativas"][0]["modo"], "gracioso",
                    "ROD/C: a acao registrada nomeia o modo gracioso")

        # ---- caso D: ROLLBACK que FALHA de verdade => status RESIDUO / exit 1 ---
        r_d, cod_d = _rodada(col, raiz, "travado", dll, plano,
                             flags=("--extra", "--extra-travado"))
        travado = os.path.join(raiz, "perfil-travado", EXTRA_REL)
        C.arc.exigir(cod_d != 0, "ROD/D: rodada com efeito residual NAO pode dar exit 0")
        C.arc.igual(r_d["status"], "RESIDUO",
                    "ROD/D: restauracao nao exata => status RESIDUO (nunca 'limpo')")
        C.arc.igual(r_d["restauracao"]["limpo"], False,
                    "ROD/D: a prova de restauracao acusa o residuo")
        C.arc.exigir(EXTRA_REL.replace("/", os.sep) in r_d["restauracao"]["residuos"],
                     "ROD/D: o arquivo residual e NOMEADO")
        C.arc.exigir("rollback_erro" in r_d,
                     "ROD/D: a falha do rollback e registrada (o driver nao cai)")
        C.arc.exigir(os.path.exists(travado), "ROD/D: o arquivo travado de fato sobrou")
        os.chmod(travado, 0o666)          # libera o TemporaryDirectory para limpar


def corpo():
    col = C.coletor()
    _varredura(col)
    _backup_log(col)
    _residuo(col)
    _manifesto(col)
    _encerramento(col)
    _rodada_completa(col)


if __name__ == "__main__":
    C.arc.main(META, corpo)
