#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 (t_a5994af0) — JOGO ABERTO, FRENTE UNICA e a IDENTIDADE de cada resultado.

Duas travas do contrato, provadas offline:

  * COM O JOGO ABERTO so se LE instrumentacao JA CARREGADA. Se o probe nao esta
    carregado nesta sessao, nao ha hot-reload: a rodada declara REINICIO NECESSARIO e
    sai NAO_EXERCITADO — nada e instalado, nada e lido, nada e prometido.
  * UMA UNICA FRENTE controla o jogo: com outra frente ativa a rodada NAO age
    (NAO_EXERCITADO), mesmo autorizada — e o caminho executavel nao chega a lancar.

E prova que o caminho executavel do driver carrega a IDENTIDADE do resultado (hash de
fonte/DLL, configuracao, cenario, observado/esperado, evidencia e lacunas) e o veredito
do detector — nunca CONFIRMADA sem status de conclusao.

Sem jogo: a rodada executavel usa um STUB (processo real de Python), nunca o lancador
do jogo; o perfil e um diretorio temporario.
"""
import json
import os
import sys
import tempfile

import comum as C

META = {
    "nome": "aut4-jogo-aberto-frente",
    "categoria": "pura",
    "requer": [],
    "descricao": "jogo aberto sem instrumentacao exige REINICIO (nunca hot-reload); frente "
                 "duplicada nao age; todo resultado carrega identificacao e veredito do detector",
}

CHAVES_IDENTIFICACAO = ("dll_sha256", "hash_fonte", "configuracao", "cenario",
                        "observado", "esperado", "evidencia", "lacunas")


def _plano():
    plano = dict(C.fixture("plano-exemplo"))
    plano["campos_alvo"] = ["texto_bruto", "texto_renderizado"]
    return plano


def _stub(dirbase, argv_file):
    caminho = os.path.join(dirbase, "stub_lancador.py")
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write("import sys, json\n"
                 "with open(%r, 'w', encoding='utf-8') as fh:\n"
                 "    fh.write(json.dumps({'argv': sys.argv}))\n" % argv_file)
    return caminho


def _dll_falsa(dirbase):
    caminho = os.path.join(dirbase, "Aut4Probe.dll")
    with open(caminho, "wb") as fh:
        fh.write(b"MZ-dll-falsa-do-jogo-aberto")
    return caminho


def corpo():
    col = C.coletor()
    plano = _plano()

    # ---- 1) jogo aberto x instrumentacao carregada ------------------------------
    sem_jogo = col.decidir_com_jogo_aberto(jogo_aberto=False, probe_carregado=False)
    C.arc.igual(sem_jogo["status"], "NAO_EXERCITADO", "sem jogo aberto: NAO_EXERCITADO")
    C.arc.igual(sem_jogo["pode_ler"], False, "sem jogo aberto: nada a ler")
    C.arc.igual(sem_jogo["hot_reload"], False, "sem jogo: nenhum hot-reload prometido")

    sem_probe = col.decidir_com_jogo_aberto(jogo_aberto=True, probe_carregado=False)
    C.arc.igual(sem_probe["status"], "NAO_EXERCITADO",
                "jogo aberto SEM o probe: NAO_EXERCITADO (nao confirma)")
    C.arc.igual(sem_probe["reinicio_necessario"], True,
                "jogo aberto sem probe: declarar REINICIO NECESSARIO")
    C.arc.igual(sem_probe["hot_reload"], False,
                "trocar a DLL NAO tem hot-reload: o driver nao pode prometer isso")
    C.arc.igual(sem_probe["pode_ler"], False, "sem instrumentacao nao ha o que ler")
    C.arc.exigir("REINICIAR" in sem_probe["motivo"].upper(),
                 "o motivo do reinicio tem de nomear o reinicio explicitamente")

    com_probe = col.decidir_com_jogo_aberto(jogo_aberto=True, probe_carregado=True)
    C.arc.igual(com_probe["status"], "PRONTO_PARA_LER",
                "jogo aberto COM o probe carregado: a rodada so LE")
    C.arc.igual(com_probe["pode_ler"], True, "com instrumentacao carregada: pode ler")
    C.arc.igual(com_probe["reinicio_necessario"], False, "com o probe carregado nao ha reinicio")
    C.arc.igual(com_probe["hot_reload"], False, "mesmo lendo, nenhum hot-reload")
    C.arc.igual(com_probe["dados_sinteticos"], False, "nenhum dado fabricado")

    # ---- 2) FRENTE UNICA ---------------------------------------------------------
    decisao = col.decidir_autorizacao(True, True, "coleta", frente_ativa=True)
    C.arc.igual(decisao["pode_coletar"], False, "frente ativa: a rodada NAO coleta")
    C.arc.igual(decisao["status"], "NAO_EXERCITADO", "frente duplicada -> NAO_EXERCITADO")
    C.arc.exigir(decisao["motivo"], "a recusa pela frente duplicada tem de estar motivada")

    rodada, codigo = col.planejar_rodada(plano, True, True, "coleta", frente_ativa=True)
    C.arc.igual(codigo, 2, "frente duplicada: planejar_rodada nao age (exit 2)")
    C.arc.igual(rodada["resultado"]["status"], "NAO_EXERCITADO",
                "frente duplicada: o plano nao vira rodada")

    # ---- 3) o caminho EXECUTAVEL com frente ativa nao lanca NADA -----------------
    with tempfile.TemporaryDirectory(prefix="aut4-jogo-") as raiz:
        perfil = os.path.join(raiz, "perfil")
        out = os.path.join(raiz, "out")
        dll = _dll_falsa(raiz)
        argv_file = os.path.join(raiz, "stub-argv.json")
        stub = _stub(raiz, argv_file)
        r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                     autorizado=True, jogo_disponivel=True, confirmacao="coleta",
                                     comando_lancamento=[sys.executable, stub],
                                     timeout_s=5, poll_s=0.1, frente_ativa=True)
        C.arc.igual(cod, 2, "frente duplicada: executar_rodada NAO age (exit 2)")
        C.arc.igual(r["status"], "NAO_EXERCITADO", "frente duplicada -> NAO_EXERCITADO")
        C.arc.exigir(not os.path.exists(argv_file),
                     "frente duplicada: o STUB nao pode ter rodado")
        C.arc.exigir(not os.path.exists(os.path.join(perfil, "BepInEx")),
                     "frente duplicada: nada pode ter sido instalado no perfil")

        # ---- 4) IDENTIDADE + veredito do detector no caminho executavel ---------
        perfil2 = os.path.join(raiz, "perfil2")
        out2 = os.path.join(raiz, "out2")
        argv2 = os.path.join(raiz, "stub-argv2.json")
        stub2 = _stub(raiz, argv2)
        r2, cod2 = col.executar_rodada(plano, perfil_dir=perfil2, out_dir=out2, dll_probe=dll,
                                       autorizado=True, jogo_disponivel=True, confirmacao="coleta",
                                       comando_lancamento=[sys.executable, stub2],
                                       timeout_s=5, poll_s=0.1)
        C.arc.exigir(os.path.isfile(argv2), "a rodada autorizada TEM de lancar (stub em disco)")
        C.arc.exigir(cod2 != 0, "rodada sem leitura do probe NAO pode dar exit 0")
        C.arc.igual(r2["status"], "NAO_EXERCITADO", "o stub nao escreve o JSON: NAO_EXERCITADO")
        C.arc.igual(r2["hot_reload"], False, "o driver nunca promete hot-reload")

        C.arc.igual(r2["detector"]["veredito"], col.veredito_do_status(r2["status"]),
                    "o veredito do detector e a traducao do status do driver")
        C.arc.exigir(r2["detector"]["veredito"] in col.VEREDITOS_NEGATIVOS,
                     "status NAO_EXERCITADO -> veredito negativo")
        C.arc.igual(r2["detector"]["dados_sinteticos"], False, "nenhum dado fabricado")
        C.arc.igual(r2["detector"]["hot_reload"], False, "detector: nenhum hot-reload")

        ident = r2.get("identificacao") or {}
        for chave in CHAVES_IDENTIFICACAO:
            C.arc.exigir(chave in ident, "o resultado executavel tem de identificar %r" % chave)
        C.arc.exigir(ident["hash_fonte"], "a identificacao tem de trazer o hash de fonte/DLL")
        C.arc.igual(ident["hash_fonte"], col._sha256(dll),
                    "o hash de fonte e o sha256 MEDIDO da DLL em disco")
        C.arc.exigir(str(ident["evidencia"] or "").strip(),
                     "a identificacao nomeia a evidencia (out_dir)")

        # O caminho sem autorizacao tambem carrega identidade e veredito negativo.
        r3, cod3 = col.executar_rodada(plano, perfil_dir=perfil2, out_dir=out2, dll_probe=dll,
                                       autorizado=False, jogo_disponivel=True, confirmacao="coleta",
                                       timeout_s=5, poll_s=0.1)
        C.arc.igual(cod3, 2, "sem autorizacao -> exit 2")
        C.arc.igual(r3["status"], "NAO_EXERCITADO", "sem autorizacao -> NAO_EXERCITADO")
        C.arc.exigir(r3["detector"]["veredito"] in col.VEREDITOS_NEGATIVOS,
                     "sem autorizacao: veredito negativo")
        C.arc.exigir("identificacao" in r3, "sem autorizacao: o resultado tambem se identifica")

        # Nenhum status fora de CONCLUIDO/OK pode virar CONFIRMADA no detector.
        for status in ("NAO_EXERCITADO", "INDETERMINADO", "INCOMPLETO", "ERRO", "RESIDUO",
                       "PLANO_INVALIDO", "FIXTURE"):
            C.arc.exigir(col.veredito_do_status(status) in col.VEREDITOS_NEGATIVOS,
                         "status %r nao pode confirmar" % status)

        # ---- 5) CLI: --jogo-aberto e o caminho sem autorizacao ------------------
        # (o CLI imprime o JSON do resultado: aqui interessa o EXIT CODE)
        import contextlib
        import io
        plano_path = os.path.join(C.DIR_FIXTURES, "plano-exemplo.entrada.json")
        with contextlib.redirect_stdout(io.StringIO()):
            cod_sem_probe = col.main(["--plano", plano_path, "--jogo-aberto"])
            cod_com_probe = col.main(["--plano", plano_path, "--jogo-aberto", "--probe-carregado"])
            cod_detectar = col.main(["--plano", plano_path, "--detectar"])
        C.arc.igual(cod_sem_probe, 2,
                    "CLI --jogo-aberto sem --probe-carregado -> exit 2 (NAO_EXERCITADO)")
        C.arc.igual(cod_com_probe, 0,
                    "CLI --jogo-aberto --probe-carregado -> PRONTO_PARA_LER (exit 0)")
        C.arc.igual(cod_detectar, 2,
                    "CLI --detectar sem --saida-probe -> NAO_EXERCITADO (exit 2)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
