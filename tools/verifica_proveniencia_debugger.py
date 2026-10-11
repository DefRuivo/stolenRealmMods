#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifica_proveniencia_debugger.py - o verificador do bloco `DBG-PROV-V1` (cartao t_3b7c681b).

PARA QUE EXISTE
---------------
Os censos `docs/cobertura/*.csv` sao regenerados por `tools/census.py` a partir do dump de boot do
RoguelikeDebugger (`LogOutput.log`). O dump nao dizia QUAL build foi observado nem SE ele terminou -
logo "o dado nao esta no CSV" podia significar tanto "o jogo nao tem" quanto "o dump veio de outro
build e/ou foi cortado no meio". Este verificador exige o carimbo de proveniencia e REPROVA quem nao
o tem; so' o veredito 0 (dump completo e identificado) libera a leitura "nao existe no jogo".

    python tools/verifica_proveniencia_debugger.py LogOutput.log
    python tools/verifica_proveniencia_debugger.py LogOutput.log --alvo api/docs/target-game.json
    python tools/verifica_proveniencia_debugger.py LogOutput.log --json

VEREDITOS (e o exit code)
-------------------------
    0  COMPLETO   cabecalho com TODOS os campos exigidos, identidade conhecida, estado ABERTO com a
                  contagem de ganchos coerente e rodape FECHADO; com `--alvo`, tudo bate com o alvo.
    2  TRUNCADO   a proveniencia esta' certa, mas o dump NAO esta' fechado (falta o rodape), ou algum
                  gancho falhou (estado PARCIAL), ou a identidade ficou incompleta
                  (`buildSteam=desconhecido`). Proveniencia serve para auditar; NAO serve para
                  concluir ausencia de dado.
    1  REPROVADO  sem cabecalho `DBG-PROV-V1`, campo obrigatorio ausente/vazio, sha256 fora de 64
                  hex, bloco internamente incoerente, ou divergencia com `--alvo`.

O QUE ESTE VERIFICADOR NAO PROVA
--------------------------------
Nao executa o jogo, nao le o LogOutput.log do dono por conta propria (o caminho e' argumento) e nao
valida se o hash declarado corresponde ao arquivo real do jogo - isso o plugin mede em runtime. Ele
verifica o CARIMBO: presenca, coerencia interna e aderencia ao alvo declarado.
"""
import argparse
import json
import os
import re
import sys

# Só o bloco do debugger interessa; o resto do LogOutput.log (BepInEx, outros mods) é ignorado.
# A marca do formato e' FONTE UNICA: o teste puro (t_dbg_r2_proveniencia.py) confere que ela e' a
# mesma que o C# emite (RoguelikeDebugger/Proveniencia.cs -> Proveniencia.Marca).
MARCA = "DBG-PROV-V1"
LINHA = re.compile(
    r"\[Proveniencia\]\s+" + MARCA + r"\s+(?P<fase>[A-Za-z]+)\s*\|(?P<corpo>.*)$"
)
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
CONTAGEM = re.compile(r"^(\d+)/(\d+)$")

OBRIGATORIOS_INICIO = (
    "versaoJogo", "buildSteam", "sha256Alvo", "dllDebugger", "sha256Dll",
    "identidade", "apiPresente", "apiEnableHooks", "apiVersao", "apiSha256",
    "alvoConforme", "inicioEm", "estadoDump",
)
OBRIGATORIOS_ESTADO = ("estadoDump", "ganchosOk", "ganchosFalhos", "metodos", "matrizFlame", "modoLeitura")
OBRIGATORIOS_FIM = ("estadoDump", "motivo")

COMPLETO, TRUNCADO, REPROVADO = 0, 2, 1


def _campo(corpo):
    """`chave=valor | chave=valor` -> dict. Chave sem `=` é anomalia (valor None)."""
    pares = {}
    for pedaco in corpo.split("|"):
        pedaco = pedaco.strip()
        if not pedaco:
            continue
        if "=" not in pedaco:
            pares[pedaco] = None
            continue
        chave, valor = pedaco.split("=", 1)
        pares[chave.strip()] = valor.strip()
    return pares


def ler_log(caminho):
    """Todas as linhas do bloco, por fase, na ordem em que aparecem."""
    fases = {"inicio": [], "estado": [], "fim": []}
    with open(caminho, "r", encoding="utf-8", errors="replace") as arquivo:
        for linha in arquivo:
            achado = LINHA.search(linha.rstrip("\r\n"))
            if not achado:
                continue
            fase = achado.group("fase").lower()
            fases.setdefault(fase, []).append(_campo(achado.group("corpo")))
    return fases


def _faltando(campos, exigidos, onde):
    """Campos ausentes OU vazios. Nao existe campo obrigatorio vazio que passe."""
    return ["%s: %s" % (onde, chave) for chave in exigidos
            if chave not in campos or campos[chave] is None or campos[chave] == ""]


def verificar(caminho, alvo_caminho=None):
    """Devolve (veredito, motivos, avisos, notas, campos).

    `motivos`  -> REPROVADO. `avisos` -> TRUNCADO (proveniencia ok, dado incompleto).
    `notas`    -> informacao que NAO muda o veredito (ex.: a sessao usar a matriz Flame, que nao e'
                  leitura passiva estrita) - ela precisa aparecer, mas nao e' um defeito do carimbo.
    """
    motivos, avisos, notas = [], [], []
    fases = ler_log(caminho)

    inicio = fases["inicio"][-1] if fases["inicio"] else None
    estado = fases["estado"][-1] if fases["estado"] else None
    fim = fases["fim"][-1] if fases["fim"] else None

    if inicio is None:
        return REPROVADO, ["sem cabecalho de proveniencia ({0}): o dump nao diz qual build foi "
                           "observado nem se terminou".format("DBG-PROV-V1 inicio")], [], [], {}

    campos = {"inicio": inicio}
    motivos += _faltando(inicio, OBRIGATORIOS_INICIO, "inicio")

    if inicio.get("estadoDump") not in (None, "INICIADO"):
        motivos.append("inicio: estadoDump=%r (esperado INICIADO)" % inicio.get("estadoDump"))

    for chave in ("sha256Alvo", "sha256Dll"):
        valor = inicio.get(chave)
        if valor and not HEX64.match(valor):
            motivos.append("%s nao e' sha256 de 64 hex: %r" % (chave, valor))

    if inicio.get("inicioEm") and not ISO.match(inicio["inicioEm"]):
        motivos.append("inicioEm nao esta' em ISO-8601 UTC: %r" % inicio["inicioEm"])

    if inicio.get("identidade") not in (None, "api", "local"):
        motivos.append("identidade desconhecida: %r" % inicio.get("identidade"))

    if inicio.get("apiPresente") not in (None, "sim", "nao"):
        motivos.append("apiPresente desconhecido: %r" % inicio.get("apiPresente"))

    if inicio.get("apiEnableHooks") not in (None, "sim", "nao", "desconhecido"):
        motivos.append("apiEnableHooks desconhecido: %r" % inicio.get("apiEnableHooks"))

    if inicio.get("alvoConforme") not in (None, "sim", "nao", "indeterminado"):
        motivos.append("alvoConforme desconhecido: %r" % inicio.get("alvoConforme"))

    if inicio.get("alvoConforme") == "nao":
        motivos.append("alvoConforme=nao: o alvo observado diverge do alvo declarado pela API "
                       "(o dump nao serve de base para o censo do alvo)")

    # Coerencia: identidade=api so' com a API presente, ligada e com versao/hash declarados.
    if inicio.get("identidade") == "api":
        if inicio.get("apiPresente") != "sim" or inicio.get("apiEnableHooks") != "sim":
            motivos.append("identidade=api sem apiPresente=sim e apiEnableHooks=sim")
        if not inicio.get("apiVersao") or inicio["apiVersao"] in ("-", "desconhecido"):
            motivos.append("identidade=api sem apiVersao")
        if not inicio.get("apiSha256") or not HEX64.match(inicio["apiSha256"]):
            motivos.append("identidade=api sem apiSha256 de 64 hex")

    if estado is None:
        motivos.append("sem linha `estado` (DBG-PROV-V1 estado): nao da' para saber se os ganchos "
                       "entraram nesta sessao")
    else:
        campos["estado"] = estado
        motivos += _faltando(estado, OBRIGATORIOS_ESTADO, "estado")
        if estado.get("estadoDump") not in (None, "ABERTO", "PARCIAL"):
            motivos.append("estado: estadoDump=%r (esperado ABERTO ou PARCIAL)" % estado.get("estadoDump"))
        if estado.get("estadoDump") == "PARCIAL":
            avisos.append("estadoDump=PARCIAL: algum gancho nao entrou nesta sessao (falhas: %s) - o "
                          "dump do recurso que dependia dele NAO saiu"
                          % (estado.get("ganchosFalhos") or "?"))
        contagem = CONTAGEM.match(estado.get("ganchosOk") or "")
        if not contagem:
            motivos.append("estado: ganchosOk fora do formato n/n: %r" % estado.get("ganchosOk"))
        else:
            ok, total = int(contagem.group(1)), int(contagem.group(2))
            if ok > total or total == 0:
                motivos.append("estado: ganchosOk incoerente: %d/%d" % (ok, total))
            elif estado.get("estadoDump") == "ABERTO" and ok != total:
                motivos.append("estado: estadoDump=ABERTO com falha de gancho (%d/%d)" % (ok, total))
        if estado.get("modoLeitura") not in (None, "passivo", "ativo"):
            motivos.append("estado: modoLeitura desconhecido: %r" % estado.get("modoLeitura"))
        if estado.get("matrizFlame") not in (None, "aplicada", "ausente"):
            motivos.append("estado: matrizFlame desconhecido: %r" % estado.get("matrizFlame"))

    if fim is None:
        avisos.append("sem rodape `fim`: o dump NAO esta' fechado (pode ter sido cortado no meio)")
    else:
        campos["fim"] = fim
        motivos += _faltando(fim, OBRIGATORIOS_FIM, "fim")
        if fim.get("estadoDump") not in (None, "FECHADO"):
            motivos.append("fim: estadoDump=%r (esperado FECHADO)" % fim.get("estadoDump"))

    if inicio.get("buildSteam") in ("desconhecido", None, ""):
        avisos.append("buildSteam=desconhecido: sem o build, a identidade do alvo esta' incompleta")

    if estado and estado.get("modoLeitura") == "ativo":
        notas.append("modoLeitura=ativo: a matriz Flame esta' aplicada e ela chama EvalVoid/escreve "
                     "MissingExpressions (FlameShrineProcPatch.cs:278-284,350) - a sessao NAO e' "
                     "observacao passiva estrita (isso NAO invalida a identidade do dump, mas quem "
                     "for concluir ausencia de dado precisa saber)")

    if alvo_caminho:
        try:
            with open(alvo_caminho, "r", encoding="utf-8") as arquivo:
                alvo = json.load(arquivo)
        except Exception as erro:  # alvo pedido e ilegivel: nao da' para aprovar nada
            motivos.append("alvo ilegivel (%s): %s" % (alvo_caminho, erro))
        else:
            campos["alvo"] = alvo
            esperado = alvo.get("assemblyCSharpSha256")
            if esperado and (inicio.get("sha256Alvo") or "").lower() != esperado.lower():
                motivos.append("sha256Alvo do dump (%s) diverge do alvo (%s)"
                               % (inicio.get("sha256Alvo"), esperado))
            if alvo.get("gameVersion") and inicio.get("versaoJogo") != alvo["gameVersion"]:
                motivos.append("versaoJogo do dump (%s) diverge do alvo (%s)"
                               % (inicio.get("versaoJogo"), alvo["gameVersion"]))
            if alvo.get("steamBuildId") and inicio.get("buildSteam") not in (None, "desconhecido") \
                    and inicio["buildSteam"] != alvo["steamBuildId"]:
                motivos.append("buildSteam do dump (%s) diverge do alvo (%s)"
                               % (inicio.get("buildSteam"), alvo["steamBuildId"]))

    if motivos:
        return REPROVADO, motivos, avisos, notas, campos
    if avisos:
        return TRUNCADO, motivos, avisos, notas, campos
    return COMPLETO, motivos, avisos, notas, campos


NOMES = {COMPLETO: "COMPLETO", TRUNCADO: "TRUNCADO", REPROVADO: "REPROVADO"}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verifica o carimbo de proveniencia DBG-PROV-V1 de um dump do RoguelikeDebugger.")
    parser.add_argument("log", help="caminho do dump (LogOutput.log)")
    parser.add_argument("--alvo", default=None,
                        help="JSON do alvo declarado (ex.: api/docs/target-game.json)")
    parser.add_argument("--json", action="store_true", help="saida JSON em vez do relatorio humano")
    args = parser.parse_args(argv)

    if not os.path.isfile(args.log):
        print("verifica_proveniencia_debugger: dump nao encontrado: %s" % args.log, file=sys.stderr)
        return REPROVADO

    veredito, motivos, avisos, notas, campos = verificar(args.log, args.alvo)

    if args.json:
        print(json.dumps({"log": args.log, "veredito": NOMES[veredito], "exit": veredito,
                          "motivos": motivos, "avisos": avisos, "notas": notas,
                          "campos": campos}, ensure_ascii=False, indent=2, sort_keys=True))
        return veredito

    print("dump:      %s" % args.log)
    print("veredito:  %s (exit %d)" % (NOMES[veredito], veredito))
    inicio = campos.get("inicio") or {}
    if inicio:
        print("alvo:      jogo=%s buildSteam=%s sha256=%s" % (
            inicio.get("versaoJogo"), inicio.get("buildSteam"), inicio.get("sha256Alvo")))
        print("observou:  dll=%s sha256=%s" % (inicio.get("dllDebugger"), inicio.get("sha256Dll")))
        print("identidade:%s (apiPresente=%s apiEnableHooks=%s apiVersao=%s alvoConforme=%s)"
              % (inicio.get("identidade"), inicio.get("apiPresente"), inicio.get("apiEnableHooks"),
                 inicio.get("apiVersao"), inicio.get("alvoConforme")))
    estado = campos.get("estado") or {}
    if estado:
        print("ganchos:   %s (falhas=%s) matrizFlame=%s modoLeitura=%s"
              % (estado.get("ganchosOk"), estado.get("ganchosFalhos"), estado.get("matrizFlame"),
                 estado.get("modoLeitura")))
    print("dump fechou: %s" % ("sim" if campos.get("fim") else "NAO"))
    for nota in notas:
        print("NOTA:      %s" % nota)
    for aviso in avisos:
        print("AVISO:     %s" % aviso)
    for motivo in motivos:
        print("MOTIVO:    %s" % motivo)
    return veredito


if __name__ == "__main__":
    sys.exit(main())
