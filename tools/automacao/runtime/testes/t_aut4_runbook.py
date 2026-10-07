#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 (t_ef6e8a29) — o RUNBOOK da rodada autorizada tem de casar com o DISCO.

Consolidar evidencia offline nao pode ser escrever um texto bonito: o runbook
`docs/automacao/AUT-4-runbook-rodada-autorizada.md` e o documento que o dono le
antes de autorizar a rodada em jogo. Se ele declarar um hash que nao e o do
binario, uma chave de config que o probe nao tem, ou uma contagem de testes que
nao existe, o operador planeja em cima de numero falso.

Este teste e a trava contra essa deriva:

  * TODO sha256 declarado no runbook (fonte, componentes, DLL do probe, driver,
    controle negativo, runner e a DLL do JOGO) casa byte a byte com o arquivo;
  * TODA chave do `.cfg` (a lista viva `coletor.CFG_CHAVES`) esta documentada —
    quem le o runbook ve a configuracao que o driver realmente escreve;
  * as contagens citadas sao as REAIS do disco (testes e iscas);
  * as frases de gate/limite existem: preparado NAO exercitado, aceite humano e
    publicacao do DoD explicitamente fora do automatismo, build sem deploy, e os
    caminhos vigiados do rollback.

Puro: nao abre jogo, nao instala nada, nao escreve nada — so le bytes.
"""
import hashlib
import os
import re

import comum as C

META = {
    "nome": "aut4-runbook",
    "categoria": "pura",
    "requer": [],
    "descricao": "o runbook da rodada autorizada casa com o disco (hashes, chaves do cfg, "
                 "contagens) e declara os limites de aceite humano/DoD",
}

RUNBOOK = "AUT-4-runbook-rodada-autorizada.md"

# Identidade da build que o runbook TEM de declarar (relativo a raiz do repo).
# Inclui a DLL do JOGO: a prova de que a frente nao a tocou.
ARTEFATOS = (
    ("fonte do probe", "tools/automacao/runtime/AUT4Probe/AUT4ProbePlugin.cs"),
    ("agregados do probe", "tools/automacao/runtime/AUT4Probe/LeituraAgregados.cs"),
    ("identidade do probe", "tools/automacao/runtime/AUT4Probe/IdentidadeDoProbe.cs"),
    ("serializador JSON", "tools/automacao/runtime/AUT4Probe/Json.cs"),
    ("projeto do probe", "tools/automacao/runtime/AUT4Probe/AUT4Probe.csproj"),
    ("DLL do probe", "tools/automacao/runtime/AUT4Probe/bin/Release/AUT4Probe.dll"),
    ("driver/coletor", "tools/automacao/runtime/coletor.py"),
    ("controle negativo", "tools/automacao/runtime/controle_negativo.py"),
    ("runner offline", "tools/automacao/runtime/roda_testes_runtime.py"),
    ("DLL do JOGO (intocada)", "lib/Assembly-CSharp.dll"),
)

# Frases que o runbook NAO pode perder (todas em ASCII, sem acento, de proposito).
FRASES_EXIGIDAS = (
    ("PREPARADO_NAO_EXERCITADO", "o status declarado tem de ser PREPARADO_NAO_EXERCITADO"),
    ("NAO_EXERCITADO", "a rodada runtime tem de estar declarada NAO_EXERCITADA"),
    ("ACEITE HUMANO", "o runbook tem de declarar que automacao nao substitui aceite humano"),
    ("DoD", "o runbook tem de nomear o DoD (publicacao nao e automatica)"),
    ("-p:DeployToBepInEx=false", "builds sao sempre sem deploy"),
    ("dados_sinteticos", "a regra de nao fabricar dado tem de estar escrita"),
    ("hot_reload", "o runbook tem de declarar que nao ha hot-reload"),
    ("CONFIRMADA", "o vocabulario do detector (CONFIRMADA e o negativo) tem de estar exposto"),
    ("BepInEx/plugins", "a arvore vigiada de plugins tem de estar documentada"),
    ("BepInEx/config", "a arvore vigiada de config tem de estar documentada"),
    ("LogOutput.log", "o log vigiado tem de estar documentado"),
)

# Contagens ANTIGAS que nao podem sobreviver (o runbook e consolidacao: numero velho
# e numero falso). Fronteira de digito pelo mesmo motivo de t_aut4_estado_docs.py.
CONTAGENS_ANTIGAS = (r"(?<!\d)14/14(?!\d)", r"(?<!\d)10/10(?!\d)",
                     r"(?<!\d)8/8(?!\d)", r"(?<!\d)30 iscas", r"(?<!\d)22 iscas")


def sha_do_arquivo(caminho):
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def hashes_do_disco():
    """{rotulo: sha256} medido AGORA, relativo a raiz do repo."""
    return {rotulo: sha_do_arquivo(os.path.join(C.REPO, rel.replace("/", os.sep)))
            for rotulo, rel in ARTEFATOS}


def cfg_chaves():
    """A lista VIVA de chaves do `.cfg` (quem define e o modulo sob teste)."""
    return list(C.coletor().CFG_CHAVES)


def contagens():
    """(n_testes, n_iscas) do disco — o mesmo criterio do runner."""
    testes = [n for n in os.listdir(os.path.join(C.RUNTIME, "testes"))
              if n.startswith("t_") and n.endswith(".py")]
    iscas = [n for n in os.listdir(os.path.join(C.RUNTIME, "testes", "contra-prova"))
             if n.startswith("cp_") and n.endswith(".py")]
    return len(testes), len(iscas)


def checar(texto, hashes, chaves, n_testes, n_iscas):
    """Devolve a lista de PROBLEMAS do runbook (vazia = conforme o contrato).

    Devolve em vez de levantar para a contra-prova poder afirmar o falso: a isca
    planta um defeito no texto e exige que `checar` o ACUSE.
    """
    problemas = []
    if not (texto or "").strip():
        return ["runbook vazio/ilegivel"]
    for rotulo, digest in sorted(hashes.items()):
        if digest not in texto:
            problemas.append("hash de %s nao declarado no runbook (esperado %s)" % (rotulo, digest))
    for chave in chaves:
        if chave not in texto:
            problemas.append("chave do cfg nao documentada: %s" % chave)
    if "%d/%d" % (n_testes, n_testes) not in texto:
        problemas.append("contagem real de testes (%d/%d) nao citada" % (n_testes, n_testes))
    if "%d iscas" % n_iscas not in texto:
        problemas.append("contagem real de iscas (%d iscas) nao citada" % n_iscas)
    for marca, motivo in FRASES_EXIGIDAS:
        if marca not in texto:
            problemas.append("%s (faltou: %r)" % (motivo, marca))
    for antiga in CONTAGENS_ANTIGAS:
        if re.search(antiga, texto):
            problemas.append("contagem ANTIGA sobrevivente: %s" % antiga)
    return problemas


def corpo():
    caminho = os.path.join(C.dir_docs(), RUNBOOK)
    C.arc.exigir(os.path.isfile(caminho),
                 "o runbook da rodada autorizada tem de existir: %s" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        texto = fh.read()

    n_testes, n_iscas = contagens()
    problemas = checar(texto, hashes_do_disco(), cfg_chaves(), n_testes, n_iscas)
    C.arc.igual(problemas, [],
                "o runbook tem de casar com o disco (hashes/chaves/contagens) e declarar os limites")


if __name__ == "__main__":
    C.arc.main(META, corpo)
