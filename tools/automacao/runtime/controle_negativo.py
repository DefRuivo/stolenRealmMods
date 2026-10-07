#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_negativo.py - CONTROLE NEGATIVO ISOLADO (AUT-4 / t_a5994af0).

O QUE ESTE MODULO E
-------------------
A prova, OFFLINE e SEM JOGO, de que o detector SABE DIZER NAO — e de que essa prova
roda num PERFIL ISOLADO, sem tocar no perfil do dono.

  * `exigir_perfil_isolado` e FAIL-CLOSED: o controle negativo so roda com perfil e
    out_dir DENTRO de uma raiz isolada explicita. Apontar para o perfil do dono (ou
    para dentro dele) e RECUSADO com erro nomeado: "sem mover DLL do perfil do dono
    sem autorizacao" vira uma TRAVA, nao um pedido.
  * `montar_perfil_isolado` cria o esqueleto `BepInEx/` do controle dentro da raiz
    isolada. Instalar a DLL do probe e trabalho do DRIVER (`executar_rodada`), que
    instala e faz o rollback EXATO na mesma area isolada.
  * `controle_negativo` usa `coletor.executar_rodada` pelo caminho de STUB (nunca um
    jogo real), mede a IMPRESSAO do perfil do dono ANTES e DEPOIS e exige que ela
    fique igual: o controle negativo NAO pode ter efeito colateral no dono.
  * o veredito exigido e NEGATIVO — `NO` | `AUSENTE` | `NAO_EXERCITADO` | `INCOMPLETO`
    — com zero dado fabricado (`dados_sinteticos` False). Uma `CONFIRMADA` num caminho
    sem leitura valida e DEFEITO, e `exigir_veredito_negativo` a acusa.

NAO INSTALA nada no perfil do dono, nao lanca/encerra jogo, nao carrega save, nao
publica. Sem `--stub` explicito o caminho executavel e RECUSADO: o lancador real do
jogo (steam.exe) nunca e usado aqui.
"""
import argparse
import hashlib
import json
import os
import sys

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2

# Perfil do dono (r2modman). Somente LEITURA — usado como ALVO DA TRAVA, nunca como
# destino de instalacao.
PERFIL_DONO_REL = os.path.join("r2modmanPlus-local", "StolenRealm", "profiles", "Default")


class PerfilNaoIsolado(ValueError):
    """O controle negativo tentou usar um perfil que NAO e isolado."""


def _coletor():
    """Importa o driver (`coletor.py`) do MESMO diretorio deste modulo."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    if aqui not in sys.path:
        sys.path.insert(0, aqui)
    import coletor  # noqa: E402
    return coletor


def sha256_do_arquivo(caminho):
    """sha256 do arquivo (identidade da DLL usada no controle: hash MEDIDO, nunca suposto)."""
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def perfil_do_dono(ambiente=None):
    """Caminho do perfil do dono (r2modman), apenas para a TRAVA. Nao cria nada."""
    amb = ambiente if ambiente is not None else os.environ
    base = str(amb.get("APPDATA") or "").strip()
    if not base:
        return None
    return os.path.join(base, PERFIL_DONO_REL)


def _dentro(caminho, raiz):
    if not caminho or not raiz:
        return False
    c = os.path.normcase(os.path.abspath(caminho))
    r = os.path.normcase(os.path.abspath(raiz))
    return c == r or c.startswith(r + os.sep)


def exigir_perfil_isolado(raiz_isolada, perfil_dir=None, out_dir=None, perfil_dono=None):
    """FAIL-CLOSED: o controle negativo so roda dentro da raiz isolada.

    Devolve `(perfil, out_dir)` absolutos. Levanta `PerfilNaoIsolado` quando:
      * nao ha raiz isolada explicita;
      * a raiz isolada esta DENTRO do perfil do dono;
      * perfil/out_dir ficam fora da raiz isolada, ou DENTRO do perfil do dono.
    """
    if not str(raiz_isolada or "").strip():
        raise PerfilNaoIsolado("controle negativo exige uma raiz ISOLADA explicita (--base); "
                               "sem ela o driver poderia acabar apontando para o perfil do dono")
    raiz = os.path.abspath(raiz_isolada)
    perfil = os.path.abspath(perfil_dir) if perfil_dir else os.path.join(raiz, "perfil-isolado")
    out = os.path.abspath(out_dir) if out_dir else os.path.join(raiz, "out-controle")
    dono = perfil_dono if perfil_dono is not None else perfil_do_dono()
    if dono and _dentro(raiz, dono):
        raise PerfilNaoIsolado("a raiz isolada (%s) esta DENTRO do perfil do dono (%s): recusado"
                               % (raiz, dono))
    for nome, caminho in (("perfil", perfil), ("out_dir", out)):
        if not _dentro(caminho, raiz):
            raise PerfilNaoIsolado("%s fora da raiz isolada (%s nao esta sob %s): recusado — o "
                                   "controle negativo nunca escreve fora da area isolada"
                                   % (nome, caminho, raiz))
        if dono and _dentro(caminho, dono):
            raise PerfilNaoIsolado("%s aponta para DENTRO do perfil do dono (%s): recusado — a DLL "
                                   "do dono nao e movida sem autorizacao" % (nome, dono))
    return perfil, out


def montar_perfil_isolado(base, perfil_dir=None):
    """Cria a arvore `BepInEx/` do controle DENTRO da base isolada (descarpavel).

    Instalar a DLL do probe NAO e trabalho deste modulo: quem instala (e faz o
    rollback EXATO) e `coletor.executar_rodada`. Aqui so nasce o esqueleto do perfil
    isolado — nunca no perfil do dono.
    """
    col = _coletor()
    base = os.path.abspath(base)
    perfil = os.path.abspath(perfil_dir) if perfil_dir else os.path.join(base, "perfil-isolado")
    for sub in (os.path.join("BepInEx", "core"),
                os.path.dirname(col.PROBE_REL_PADRAO),
                os.path.join("BepInEx", "config")):
        os.makedirs(os.path.join(perfil, sub), exist_ok=True)
    return perfil


def impressao_do_diretorio(raiz):
    """Impressao barata e estavel de tudo sob `raiz`: `{rel: "bytes:mtime_ns"}`.

    Usa `stat` (NAO le bytes): a impressao precisa detectar TOQUE no perfil do dono,
    nao re-hashear centenas de MB. `None` quando a raiz nao existe (declarado, nao
    inventado).
    """
    if not raiz or not os.path.isdir(raiz):
        return None
    saida = {}
    for pasta, _dirs, arquivos in os.walk(raiz):
        for nome in sorted(arquivos):
            caminho = os.path.join(pasta, nome)
            rel = os.path.relpath(caminho, raiz)
            try:
                st = os.stat(caminho)
                saida[rel] = "%d:%d" % (st.st_size, st.st_mtime_ns)
            except OSError as erro:
                saida[rel] = "ERRO:%s" % erro
    return saida


def diferenca_de_impressao(antes, depois):
    """O que mudou entre duas impressoes do MESMO diretorio (vazio = intacto)."""
    if antes is None and depois is None:
        return []
    if antes is None or depois is None:
        return ["perfil do dono: existencia mudou (antes=%s, depois=%s)"
                % (antes is not None, depois is not None)]
    return ["%s: %s -> %s" % (k, antes.get(k), depois.get(k))
            for k in sorted(set(antes) | set(depois))
            if antes.get(k) != depois.get(k)]


def exigir_veredito_negativo(resultado, coletor_mod=None):
    """Levanta `AssertionError` se o resultado CONFIRMAR o que nao foi lido.

    O detector so pode dizer NAO/AUSENTE/NAO_EXERCITADO/INCOMPLETO num caminho sem
    leitura valida — e nenhum caminho pode fabricar dado.
    """
    col = coletor_mod or _coletor()
    veredito = resultado.get("veredito") or col.veredito_do_status(resultado.get("status"))
    if veredito not in col.VEREDITOS_NEGATIVOS:
        raise AssertionError("o controle negativo CONFIRMOU (%r): sem leitura valida o veredito "
                             "tem de ser um de %s" % (veredito, ", ".join(col.VEREDITOS_NEGATIVOS)))
    if resultado.get("dados_sinteticos"):
        raise AssertionError("o resultado declara dado sintetico (%r): o detector nunca fabrica"
                             % (resultado.get("dados_sinteticos"),))
    return veredito


def exigir_perfil_do_dono_intacto(perfil_dono, antes, depois):
    """Levanta `AssertionError` se o controle negativo tocou o perfil do dono."""
    diferencas = diferenca_de_impressao(antes, depois)
    if diferencas:
        raise AssertionError("o controle negativo MEXEU no perfil do dono (%s): %s"
                             % (perfil_dono, "; ".join(diferencas)))
    return True


def _stub_negativo(dirbase, perfil, out, flags=()):
    """Stub de lancamento do controle negativo: escreve o argv e SAI.

    Nunca escreve leitura: produz o caminho "a rodada aconteceu e NAO houve leitura",
    que tem de sair NAO_EXERCITADO/AUSENTE — jamais CONCLUIDO. Sem este stub o modulo
    nao lanca nada (o lancador real do jogo e proibido aqui).
    """
    argv_file = os.path.join(dirbase, "stub-argv.json")
    caminho = os.path.join(dirbase, "stub_negativo.py")
    fonte = ("import sys, json\n"
             "with open(%r, 'w', encoding='utf-8') as fh:\n"
             "    fh.write(json.dumps({'argv': sys.argv}))\n" % argv_file)
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(fonte)
    return caminho, argv_file


def controle_negativo(base, plano, dll_probe, *, autorizado=True, comando_lancamento=None,
                      perfil_dono=None, perfil_dir=None, out_dir=None, timeout_s=15, poll_s=0.1,
                      coletor_mod=None):
    """Roda o controle negativo num PERFIL ISOLADO e devolve o relatorio.

    `autorizado=False` exercita o caminho "sem acesso autorizado ao jogo" (o driver
    NAO age; nada e instalado/lancado). `autorizado=True` exercita o caminho em que a
    rodada RODA mas NAO produz leitura (o stub nao escreve JSON do probe) — o veredito
    continua negativo.

    O retorno identifica: veredito, exit_code, negativo, perfil_dono, perfil_dono_intacto,
    impressao_antes/depois (impressao do dono), stub_rodou, perfil_isolado, out_dir e o
    `resultado` cru do driver (que ja traz `identificacao`).
    """
    col = coletor_mod or _coletor()
    perfil, out = exigir_perfil_isolado(base, perfil_dir, out_dir, perfil_dono)
    dono = perfil_dono if perfil_dono is not None else perfil_do_dono()
    antes = impressao_do_diretorio(dono)

    perfil = montar_perfil_isolado(base, perfil_dir=perfil)
    os.makedirs(out, exist_ok=True)
    argv_file = None
    tem_stub = bool(comando_lancamento)
    if tem_stub:
        comando_lancamento = list(comando_lancamento)
    elif autorizado:
        stub, argv_file = _stub_negativo(os.path.abspath(base), perfil, out)
        comando_lancamento = [sys.executable, stub]

    resultado, codigo = col.executar_rodada(
        plano, perfil_dir=perfil, out_dir=out, dll_probe=dll_probe, autorizado=autorizado,
        jogo_disponivel=True, confirmacao="coleta" if autorizado else None,
        comando_lancamento=comando_lancamento, timeout_s=timeout_s, poll_s=poll_s)

    depois = impressao_do_diretorio(dono)
    intacto = not diferenca_de_impressao(antes, depois)
    veredito = resultado.get("veredito") or col.veredito_do_status(resultado.get("status"))
    consolidado = resultado.get("consolidado") or {}
    return {
        "esquema": col.ESQUEMA,
        "rotina": "controle-negativo-isolado",
        "status": resultado.get("status"),
        "veredito": veredito,
        "negativo": veredito in col.VEREDITOS_NEGATIVOS,
        "exit_code": codigo,
        "dados_sinteticos": bool(resultado.get("dados_sinteticos")),
        "hot_reload": False,
        "autorizado": bool(autorizado),
        "perfil_isolado": perfil,
        "out_dir": out,
        "perfil_dono": dono,
        "perfil_dono_intacto": intacto,
        "impressao_antes": antes,
        "impressao_depois": depois,
        "stub_rodou": bool(argv_file and os.path.isfile(argv_file)),
        "observacoes": consolidado.get("observacoes") or [],
        "identificacao": resultado.get("identificacao"),
        "resultado": resultado,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="AUT-4 — controle negativo ISOLADO (sem jogo).")
    ap.add_argument("--plano", required=True, help="plano de coleta (JSON)")
    ap.add_argument("--base", help="raiz ISOLADA (obrigatoria; nunca o perfil do dono)")
    ap.add_argument("--dll-probe", help="DLL do probe a instalar NA AREA ISOLADA")
    ap.add_argument("--stub", nargs="*", default=None,
                    help="comando do stub de lancamento (o lancador real do jogo e proibido aqui)")
    ap.add_argument("--autorizado", action="store_true",
                    help="exercita tambem o caminho autorizado (com o stub)")
    ap.add_argument("--perfil-dono", default=None, help="sobrescreve o alvo da trava do dono")
    ap.add_argument("--out", help="grava o relatorio neste arquivo (JSON)")
    args = ap.parse_args(argv)

    with open(args.plano, encoding="utf-8") as fh:
        plano = json.load(fh)

    if not str(args.base or "").strip():
        relatorio = {"esquema": "AUT-4/1", "rotina": "controle-negativo-isolado",
                     "status": "NAO_EXERCITADO", "veredito": "NAO_EXERCITADO", "negativo": True,
                     "exit_code": EXIT_NAO_RODOU, "dados_sinteticos": False, "hot_reload": False,
                     "motivo": "sem --base (raiz ISOLADA) nao ha controle negativo: recusado antes "
                               "de tocar qualquer arquivo (nunca o perfil do dono por acidente)"}
        codigo = EXIT_NAO_RODOU
    elif args.autorizado and not args.stub:
        relatorio = {"esquema": "AUT-4/1", "rotina": "controle-negativo-isolado",
                     "status": "NAO_EXERCITADO", "veredito": "NAO_EXERCITADO", "negativo": True,
                     "exit_code": EXIT_NAO_RODOU, "dados_sinteticos": False, "hot_reload": False,
                     "motivo": "caminho autorizado exige --stub: o controle negativo NUNCA lanca o "
                               "lancador real do jogo"}
        codigo = EXIT_NAO_RODOU
    else:
        try:
            relatorio = controle_negativo(
                args.base, plano, args.dll_probe, autorizado=bool(args.autorizado),
                comando_lancamento=args.stub, perfil_dono=args.perfil_dono)
            codigo = relatorio["exit_code"] if relatorio["negativo"] else EXIT_FALHOU
        except PerfilNaoIsolado as erro:
            relatorio = {"esquema": "AUT-4/1", "rotina": "controle-negativo-isolado",
                         "status": "NAO_EXERCITADO", "veredito": "NAO_EXERCITADO", "negativo": True,
                         "exit_code": EXIT_NAO_RODOU, "dados_sinteticos": False, "hot_reload": False,
                         "motivo": "PerfilNaoIsolado: %s" % erro}
            codigo = EXIT_NAO_RODOU

    texto = json.dumps(relatorio, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(texto)
    print(texto)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
