#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 (t_a5994af0) — CONTROLE NEGATIVO ISOLADO.

Prova que o controle negativo roda num PERFIL ISOLADO e que o perfil do dono fica
intacto — e que o veredito desse caminho e NEGATIVO (nunca CONFIRMADA, nunca dado
fabricado):

  * a trava `exigir_perfil_isolado` RECUSA o perfil do dono (e qualquer caminho fora
    da raiz isolada), nos dois sentidos: nem o perfil, nem a raiz isolada podem cair
    dentro um do outro;
  * `autorizado=False` (o caminho "sem acesso autorizado ao jogo"): o driver NAO age —
    nenhum probe instalado, nenhum cfg, o stub nao roda — e sai NAO_EXERCITADO/exit 2;
  * `autorizado=True` com um stub que NAO escreve leitura: a rodada RODA (o stub executa
    de verdade, o argv fica em disco) e mesmo assim NAO ha leitura -> NAO_EXERCITADO,
    zero observacao;
  * o perfil do dono e medido ANTES e DEPOIS (impressao por stat): igual byte a byte —
    e `exigir_perfil_do_dono_intacto` ACUSA uma diferenca de verdade (a guarda funciona).

Nada aqui toca jogo, perfil real, save ou publicacao: a area isolada e um diretorio
temporario descartavel.
"""
import json
import os
import sys
import tempfile

import comum as C

sys.path.insert(0, C.RUNTIME)
import controle_negativo as cn  # noqa: E402

META = {
    "nome": "aut4-controle-isolado",
    "categoria": "pura",
    "requer": [],
    "descricao": "controle negativo roda em perfil ISOLADO, recusa o perfil do dono, e o "
                 "caminho sem leitura valida devolve veredito NEGATIVO sem dado fabricado",
}

PROBE_REL = os.path.join("BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")


def _plano():
    plano = dict(C.fixture("plano-exemplo"))
    plano["campos_alvo"] = ["texto_bruto", "texto_renderizado"]
    return plano


def _dll_falsa(raiz):
    caminho = os.path.join(raiz, "Aut4Probe.dll")
    with open(caminho, "wb") as fh:
        fh.write(b"MZ-dll-falsa-do-controle-negativo")
    return caminho


def _recusa(raiz_isolada, perfil, out, dono):
    try:
        cn.exigir_perfil_isolado(raiz_isolada, perfil, out, perfil_dono=dono)
    except cn.PerfilNaoIsolado as erro:
        return str(erro)
    return None


def corpo():
    col = C.coletor()
    plano = _plano()

    with tempfile.TemporaryDirectory(prefix="aut4-cn-") as tmp:
        isolada = os.path.join(tmp, "area-isolada")
        dono = os.path.join(tmp, "perfil-do-dono")
        os.makedirs(os.path.join(dono, "BepInEx", "plugins"))
        with open(os.path.join(dono, "BepInEx", "plugins", "mod-do-dono.dll"), "wb") as fh:
            fh.write(b"dll-do-dono")
        dll = _dll_falsa(tmp)

        # ---- 1) a TRAVA recusa o perfil do dono (fail-closed) --------------------
        C.arc.exigir(_recusa(isolada, dono, None, dono),
                     "o perfil do dono TEM de ser recusado como destino do controle negativo")
        C.arc.exigir(_recusa(isolada, os.path.join(dono, "BepInEx"), None, dono),
                     "um caminho DENTRO do perfil do dono TEM de ser recusado")
        C.arc.exigir(_recusa(isolada, os.path.join(tmp, "fora", "perfil"), None, dono),
                     "perfil FORA da raiz isolada TEM de ser recusado")
        C.arc.exigir(_recusa(isolada, None, os.path.join(tmp, "fora", "out"), dono),
                     "out_dir FORA da raiz isolada TEM de ser recusado")
        C.arc.exigir(_recusa(dono, None, None, dono),
                     "raiz isolada DENTRO do perfil do dono TEM de ser recusada")
        C.arc.exigir(_recusa("", None, None, dono),
                     "sem raiz isolada explicita NAO ha controle negativo (fail-closed)")
        # controle positivo: a area isolada e aceita
        perfil_ok, out_ok = cn.exigir_perfil_isolado(isolada, None, None, perfil_dono=dono)
        C.arc.exigir(cn._dentro(perfil_ok, isolada) and cn._dentro(out_ok, isolada),
                     "a area isolada tem de ser aceita (perfil e out dentro dela)")

        # ---- 2) caminho SEM AUTORIZACAO: o driver NAO age ------------------------
        impressao_dono_antes = cn.impressao_do_diretorio(dono)
        real_antes = cn.impressao_do_diretorio(cn.perfil_do_dono())
        rel = cn.controle_negativo(isolada, plano, dll, autorizado=False, perfil_dono=dono,
                                   coletor_mod=col)
        cn.exigir_veredito_negativo(rel, col)
        C.arc.igual(rel["veredito"], "NAO_EXERCITADO", "sem autorizacao -> NAO_EXERCITADO")
        C.arc.igual(rel["exit_code"], 2, "sem autorizacao -> exit 2")
        C.arc.igual(rel["observacoes"], [], "sem autorizacao -> ZERO observacao")
        C.arc.igual(rel["dados_sinteticos"], False, "sem autorizacao -> nenhum dado fabricado")
        C.arc.igual(rel["stub_rodou"], False, "sem autorizacao -> o stub NAO pode ter rodado")
        C.arc.igual(rel["hot_reload"], False, "o controle negativo nunca promete hot-reload")
        C.arc.exigir(not os.path.exists(os.path.join(rel["perfil_isolado"], PROBE_REL)),
                     "sem autorizacao NENHUM probe pode ser instalado")
        C.arc.exigir(rel["perfil_dono_intacto"], "o perfil do dono tem de ficar intacto")

        # ---- 3) caminho AUTORIZADO com stub: RODA e mesmo assim nao confirma -----
        rel2 = cn.controle_negativo(isolada, plano, dll, autorizado=True, perfil_dono=dono,
                                    coletor_mod=col)
        cn.exigir_veredito_negativo(rel2, col)
        C.arc.igual(rel2["stub_rodou"], True,
                    "com autorizacao o stub TEM de ter rodado (argv em disco)")
        C.arc.exigir(rel2["exit_code"] != 0, "rodada sem leitura NAO pode dar exit 0")
        C.arc.igual(rel2["observacoes"], [], "o stub nao escreve leitura: zero observacao")
        C.arc.igual(rel2["dados_sinteticos"], False, "nenhum dado fabricado no caminho isolado")
        C.arc.exigir(rel2["perfil_dono_intacto"], "o perfil do dono tem de ficar intacto")
        C.arc.exigir(cn._dentro(rel2["perfil_isolado"], isolada),
                     "o controle negativo usa o perfil ISOLADO")
        # a DLL foi instalada NA AREA ISOLADA pelo driver e o rollback a removeu de la
        C.arc.exigir(not os.path.exists(os.path.join(rel2["perfil_isolado"], PROBE_REL)),
                     "nada de probe sobrando no perfil isolado depois do rollback exato")
        # a identificacao do resultado isolado existe e aponta o perfil
        ident = rel2["identificacao"] or {}
        C.arc.exigir("lacunas" in ident and "observado" in ident,
                     "o resultado do controle negativo carrega a identificacao")
        C.arc.igual(ident.get("dll_sha256"), cn.sha256_do_arquivo(dll),
                    "a identificacao aponta o sha256 da DLL usada no controle")

        # ---- 4) o perfil do dono NAO mudou (impressao por stat, antes x depois) --
        C.arc.igual(cn.diferenca_de_impressao(impressao_dono_antes,
                                              cn.impressao_do_diretorio(dono)), [],
                    "o perfil do dono (fake) tem de ficar byte a byte igual")
        real_depois = cn.impressao_do_diretorio(cn.perfil_do_dono())
        if real_antes is not None:
            C.arc.igual(cn.diferenca_de_impressao(real_antes, real_depois), [],
                        "o perfil REAL do dono (r2modman) tem de ficar intacto")

        # ---- 5) a GUARDA acusa de verdade (prova de fogo) ------------------------
        try:
            cn.exigir_perfil_do_dono_intacto(dono, {"a.dll": "1:1"}, {"a.dll": "2:2"})
        except AssertionError:
            pass
        else:
            C.arc.exigir(False, "a guarda do perfil do dono TEM de acusar uma diferenca real")

        # ---- 6) o veredito CONFIRMADA no caminho negativo e DEFEITO --------------
        try:
            cn.exigir_veredito_negativo({"veredito": "CONFIRMADA", "dados_sinteticos": False}, col)
        except AssertionError:
            pass
        else:
            C.arc.exigir(False, "CONFIRMADA num caminho sem leitura tem de ser ACUSADA como defeito")
        try:
            cn.exigir_veredito_negativo({"veredito": "NAO_EXERCITADO", "dados_sinteticos": True}, col)
        except AssertionError:
            pass
        else:
            C.arc.exigir(False, "dados_sinteticos=True tem de ser ACUSADO como defeito")

        # ---- 7) o relatorio e serializavel (declara, nao inventa) ---------------
        texto = json.dumps(rel2, ensure_ascii=False)
        C.arc.exigir("NAO_EXERCITADO" in texto,
                     "o relatorio do controle negativo declara o veredito no JSON")


if __name__ == "__main__":
    C.arc.main(META, corpo)
