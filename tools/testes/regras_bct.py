#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_bct.py - TST-8: as regras do BetterCombatText, lidas do FONTE vivo e do IL da DLL.

POR QUE ESTA BIBLIOTECA EXISTE
------------------------------
O BetterCombatText (BCT) e o mod que da contorno/sombra ao TEXTO DE COMBATE: nomes de
inimigo, rotulos/stacks de buff e debuff, texto do dado nos eventos e (opcional) o numero
de vida. Ele NAO tem fixture propria e NAO tem oraculo: o que da para verificar a maquina e
(a) a ESTRUTURA do fonte versionado e (b) os METADADOS da DLL construida - a regra de ouro
("nunca escrever no material compartilhado") e uma afirmacao sobre o CODIGO COMPILADO, e a
checagem mais forte dela e a AUSENCIA do setter entre as referencias do IL, que nao depende
de achar todas as linhas do fonte.

Este modulo e o par de `regras_bf`/`regras_bf_estilo` (BetterFont) do lado do BCT, e segue o
mesmo contrato: o META dos testes declara a categoria "pura" (nao precisa da lib/ do jogo),
o defeito plantado vive em funcoes `defeito_*`/`Modelo*Antes*` para os testes MOSTRAREM
REPROVANDO, e todo numero que o teste compara e LIDO do fonte (nunca digitado) - a unica
excecao e a ESPEC (a exigencia do dono, transcrita como constante e citada).

O QUE ESTA AQUI
---------------
  1. METADADOS DA DLL (IL)   - um leitor minimo de PE/metadata .NET em PYTHON PURO (sem
     dotnet, sem dnfile): le o stream `#~` (tabelas) e o `#Strings` e decodifica TypeRef,
     MemberRef e AssemblyRef. E com isso que se prova que `set_fontSharedMaterial` NAO
     aparece entre as REFERENCIAS do mod, e que o mod nao referencia o outro mod.
  2. O FONTE VIVO            - helpers de leitura (corpo de metodo, sem comentarios, linha).
  3. REGRA DE OURO           - o material e sempre a COPIA por componente (getter
     `fontMaterial`), nunca o compartilhado (nenhum setter).
  4. IDEMPOTENCIA            - aplicar duas vezes no mesmo componente nao acumula
     (o registro por InstanceID) + o MODELO transcrito do guarda.
  5. DEFAULTS                - Tooltip de status DESLIGADO (Title/Description sao
     compartilhados com skill/item/powerup), eventos/dado LIGADO, chave mestra LIGADA.
  6. DESLIGAR E INERTE       - com Ativar=false nenhum gancho age.
  7. CAMINHO LEGADO          - UnityEngine.UI.Text recebe contorno DURO (Outline/Shadow),
     nunca material de distance field.
  8. DIAGNOSTICO DE ARRANQUE - o intervalo (5s), a PARADA no primeiro sucesso e a chave que
     desliga a varredura - modelados como funcao pura do tempo e do estado.
  9. PRECONDICAO DO SHADER   - o efeito e confirmado por `HasProperty("_OutlineWidth")`
     ANTES de aplicar, nunca presumido pelo nome do shader.
 10. O APLICADOR             - gancho a gancho com contagem real (sem `PatchAll`), e a
     CONTRA-PROVA da trava `tools/check_patches.py`: um filtro que exigisse atributo e nao
     citasse os nomes de convencao TEM de ser reprovado por ela.
 11. CONVIVENCIA             - do lado do BCT: o codigo (e a DLL) nao citam o BetterFont.
 12. SOMBRA ADAPTATIVA (BCT-2)- cor da letra -> luminancia (Color.grayscale) -> balde -> hex:
     letra escura (< 0.5) ganha sombra CLARA e letra clara ganha sombra ESCURA #000000, inclusive
     no REUSO do componente (reavaliacao sem re-instancia). A paleta vem da fixture
     `fixtures/cores-do-jogo.entrada.json`, nunca digitada.
 13. SOMBRA VISIVEL - O FUNDO MANDA (BCT-3): a sombra e escolhida pelo CONTRASTE COM O FUNDO
     (chave `Fundo` por superficie: `escuro` -> sombra clara; `claro` -> escura #000000;
     `auto` -> a regra do BCT-2 pela letra). Conserta o defeito relatado (nome de inimigo, letra
     clara, com sombra preta invisivel no campo de batalha ESCURO).
 14. CONTRASTE COM A LETRA (BCT-4) - A LEI: a sombra tem de CONTRASTAR COM A LETRA, nao so com o
     fundo. O BCT-3 presumia letra escura ao declarar fundo escuro, mas a letra do nome do inimigo
     e CLARA e e o #CBB396 (highlightedColor/specialDescColor) - a MESMA cor da sombra clara: a
     sombra saia igual a letra (contraste zero, invisivel/blob). Agora a sombra CLARA e o BRANCO
     (#FFFFFF) e, se a cor do balde escolhido nao contrastar com a LETRA (diferenca de luminancia
     < `ContrasteMinimo`), o balde VIRA. Defeito plantado: `defeito_sombra_sem_contraste_com_a_letra`.
15. POLARIDADE PELA FONTE (BCT-5) - o LIMIAR nao bastava (#CBB396 x #FFFFFF = 0.283, "passava") e
     o `.cfg` do perfil herdou `CorSombraClara = CBB396` (a propria cor da fonte). A regra passa a
     decidir pelo LADO: letra CLARA -> sombra ESCURA; letra ESCURA -> sombra CLARA; o FUNDO so
     PROPOE (veto da letra). Alfa minimo para a sombra ser visivel. Defeitos plantados:
     `defeito_letra_clara_sombra_clara` e `defeito_alfa_sombra_baixo`.

REGRA DO PROJETO (docs/PLANO-DE-TESTES.md): todo teste tem de ser MOSTRADO REPROVANDO. Cada
funcao `defeito_*` desta biblioteca existe para o teste plantar o defeito EM MEMORIA, ver as
checagens reprovarem, e so entao considera-las prontas. A rodada FISICA (o fonte editado de
verdade, o teste reprovando, o fonte restaurado byte a byte) esta registrada em
`tools/testes/bct-prova-reprovando.log`.

USO (a leitura de IL tambem roda sozinha, para conferir a prova na mao):
    python tools/testes/regras_bct.py                       # a DLL do pacote (ou do bin/)
    python tools/testes/regras_bct.py <caminho-da.dll>
"""
import glob
import hashlib
import io
import json
import os
import re
import struct
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc  # noqa: E402
import recorte as rec  # noqa: E402  (FORMATO-8: os casadores de chave delegam a ele)

# ===========================================================================
#  localizacao e leitura do FONTE
# ===========================================================================

DIR_MOD = "BetterCombatText"
PLUGIN = "Plugin.cs"
PATCHES = "Patches.cs"
DIAG = "DiagnosticoArranque.cs"
CFG = "Configuracao.cs"
STYLER = "TextStyler.cs"
FONTES = (PLUGIN, PATCHES, DIAG, CFG, STYLER)


def raiz_mod():
    return os.path.join(arc.raiz_do_repo(), DIR_MOD)


def caminho_fonte(nome):
    return os.path.join(raiz_mod(), nome)


def fonte(nome):
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with io.open(caminho_fonte(nome), encoding="utf-8") as fh:
        return fh.read()


def fontes():
    """Todos os .cs do mod, por nome."""
    return dict((n, fonte(n)) for n in FONTES)


def corpo(src, declaracao):
    """Corpo `{...}` de um metodo, a partir da DECLARACAO exata — DELEGA ao recorte ESTRUTURAL.

    FORMATO-8 — O QUE ESTAVA ERRADO AQUI: o recorte era um casador de chaves LOCAL, cego a
    LITERAL de string e que devolvia `None` em SILENCIO (o oposto do contrato do `recorte.py`).
    Um `}` dentro de um literal (`string s = "}";`) fechava o bloco CEDO (corpo TRUNCADO) e um
    metodo sem fechamento virava `None`, indistinguivel de "a declaracao nao existe". Agora a
    conta e a do `recorte.py` (`rec.bloco_apos`): literal-aware e FALHA ALTO quando as chaves nao
    fecham.

    `rec.bloco_apos` — e nao `rec.corpo_do_metodo` — porque o CONTRATO dos consumidores deste
    modulo e o corpo COMECANDO em `{` (eles procuram trechos a partir da primeira chave); a
    declaracao AUSENTE continua devolvendo `None`, que o chamador relata como "nao achei".
    """
    i = src.find(declaracao)
    if i < 0:
        return None
    return rec.bloco_apos(src, i)


def _bloco_de(src, j):
    """O bloco `{...}` que abre em `src[j]` — DELEGA ao `rec.bloco_balanceado` (literal-aware).

    FORMATO-8: mesma troca do `corpo`. O contrato de `j` ja era apontar para um `{`; chaves que
    NAO fecham agora FALHAM ALTO (`arc.Falhou`) em vez de virar `None` em silencio — um `}` de
    literal nao fecha o bloco, e chaves abertas sem fechamento nao viram um pedaco que "passa".
    """
    return rec.bloco_balanceado(src, j)


def sem_comentarios(src):
    """O CODIGO EFETIVO: o fonte sem comentario de LINHA (`//`) e de BLOCO (`/* */`).

    Copia deliberada de `regras_bf.sem_comentarios`: comentario nao e codigo, e um defeito
    escondido num comentario (a chamada que virou `// cena = ...`) satisfaz busca de
    substring. Literais de string/char sao preservados (o `//` dentro de um literal nao e
    comentario). Duplicado de proposito: `regras_bf` esta em uso por outra tarefa (FIX-7) e
    a leitura do BCT nao pode depender de um modulo que muda embaixo dela.
    """
    saida = []
    i, n = 0, len(src)
    literal = None
    while i < n:
        c = src[i]
        if literal is None:
            if src.startswith("//", i):
                while i < n and src[i] != "\n":
                    i += 1
                continue
            if src.startswith("/*", i):
                i += 2
                while i < n and not src.startswith("*/", i):
                    i += 1
                i += 2
                continue
            if c == '"' or c == "'":
                literal = c
            saida.append(c)
            i += 1
            continue
        saida.append(c)
        if c == "\\" and i + 1 < n:
            saida.append(src[i + 1])
            i += 2
            continue
        if c == literal:
            literal = None
        i += 1
    return "".join(saida)


def linha_de(src, trecho, a_partir_de=0):
    """A linha (1-based) da PRIMEIRA ocorrencia de `trecho` a partir de `a_partir_de`."""
    i = src.find(trecho, a_partir_de)
    if i < 0:
        return None
    return src.count("\n", 0, i) + 1


def comentarios_acima(src, linha, quantas=40):
    """O texto dos comentarios contiguos ate `quantas` linhas acima de `linha` (1-based)."""
    linhas = src.splitlines()
    trecho = linhas[max(0, linha - 1 - quantas):max(0, linha - 1)]
    return "\n".join(l for l in trecho if l.strip().startswith(("//", "/*", "*")))


# ===========================================================================
#  1) METADADOS DA DLL (IL) - leitor .NET minimo em Python puro
# ===========================================================================
# A REGRA DE OURO e uma afirmacao sobre o CODIGO COMPILADO: "o mod NUNCA escreve no material
# compartilhado". A checagem mais forte dela nao e procurar linhas no fonte (que depende de
# achar TODAS as linhas), e provar a AUSENCIA do setter entre as REFERENCIAS do IL: em .NET,
# `x.fontSharedMaterial = v` vira uma referencia (MemberRef) ao metodo `set_fontSharedMaterial`
# de TMP_Text; se essa referencia NAO existe na tabela MemberRef da DLL, o compilador nao viu
# nenhuma atribuicao, em nenhuma linha, de nenhum arquivo do mod.
#
# O leitor abaixo le o PE, acha o CLI header (data directory 14), a raiz de metadados (BSJB),
# o stream de tabelas (`#~`) e o `#Strings`, e decodifica TypeRef (0x01), MemberRef (0x0A) e
# AssemblyRef (0x23) com os tamanhos de linha da ECMA-335. Toda a matematica de tamanho vem do
# proprio arquivo (HeapSizes, contagem de linhas de cada tabela) - nada digitado.

TABELAS = {
    0x00: "Module", 0x01: "TypeRef", 0x02: "TypeDef", 0x03: "FieldPtr", 0x04: "Field",
    0x05: "MethodPtr", 0x06: "MethodDef", 0x07: "ParamPtr", 0x08: "Param", 0x09: "InterfaceImpl",
    0x0A: "MemberRef", 0x0B: "Constant", 0x0C: "CustomAttribute", 0x0D: "FieldMarshal",
    0x0E: "DeclSecurity", 0x0F: "ClassLayout", 0x10: "FieldLayout", 0x11: "StandAloneSig",
    0x12: "EventMap", 0x14: "Event", 0x15: "PropertyMap", 0x17: "Property",
    0x18: "MethodSemantics", 0x19: "MethodImpl", 0x1A: "ModuleRef", 0x1B: "TypeSpec",
    0x1C: "ImplMap", 0x1D: "FieldRVA", 0x20: "Assembly", 0x21: "AssemblyProcessor",
    0x22: "AssemblyOS", 0x23: "AssemblyRef", 0x24: "AssemblyRefProcessor", 0x25: "AssemblyRefOS",
    0x26: "File", 0x27: "ExportedType", 0x28: "ManifestResource", 0x29: "NestedClass",
    0x2A: "GenericParam", 0x2B: "MethodSpec", 0x2C: "GenericParamConstraint",
}

# Indices codificados usados pelos tamanhos de linha (ECMA-335 II.24.2.6).
CODED = {
    "TypeDefOrRef": (2, [0x02, 0x01, 0x1B]),
    "HasConstant": (2, [0x04, 0x08, 0x17]),
    "HasCustomAttribute": (5, [0x06, 0x04, 0x01, 0x02, 0x08, 0x09, 0x0A, 0x00, 0x0E, 0x17,
                               0x14, 0x11, 0x1A, 0x1B, 0x20, 0x23, 0x26, 0x27, 0x28, 0x2A, 0x2B]),
    "HasFieldMarshal": (1, [0x04, 0x08]),
    "HasDeclSecurity": (2, [0x02, 0x06, 0x20]),
    "MemberRefParent": (3, [0x02, 0x01, 0x1A, 0x06, 0x1B]),
    "HasSemantics": (1, [0x14, 0x17]),
    "MethodDefOrRef": (1, [0x06, 0x0A]),
    "MemberForwarded": (1, [0x04, 0x06]),
    "Implementation": (2, [0x26, 0x23, 0x27]),
    "CustomAttributeType": (3, [None, None, 0x06, 0x0A, None]),
    "ResolutionScope": (2, [0x00, 0x1A, 0x23, 0x01]),
    "TypeOrMethodDef": (1, [0x02, 0x06]),
}

# O que a REGRA DE OURO proibe: qualquer SETTER de material. No TextMeshPro, o material
# COMPARTILHADO e escrito (a) pelo setter da propriedade `fontSharedMaterial`, (b) pelo setter
# de `fontSharedMaterials`, (c) pelos setters de `material`/`materials`/`sharedMaterial`, que
# no TMP_Text/Graphic apontam para o mesmo `m_sharedMaterial`. O efeito por componente NAO usa
# setter nenhum: o mod le `fontMaterial` (getter) e escreve no objeto que ele devolve.
REGEX_SETTER_DE_MATERIAL = re.compile(r"(?i)^set_.*material")

# CONTROLE POSITIVO do leitor: se estas referencias NAO aparecerem, o leitor nao esta lendo as
# referencias (e a ausencia do setter nao provaria nada - "varre e nao acha nada").
MEMBROS_ESPERADOS = ("get_fontSharedMaterial", "get_fontMaterial", "SetMaterialDirty",
                     "set_fontSize", "set_fontStyle", "set_effectColor", "set_effectDistance",
                     "HasProperty", "GetInstanceID", "SetColor", "SetFloat", "EnableKeyword")

PACOTE_GLOB = os.path.join("dist", "gumatos-BetterCombatText-*.zip")
ENTRADA_DLL_NO_PACOTE = "plugins/BetterCombatText/BetterCombatText.dll"


def _u16(d, o):
    return struct.unpack_from("<H", d, o)[0]


def _u32(d, o):
    return struct.unpack_from("<I", d, o)[0]


def _u64(d, o):
    return struct.unpack_from("<Q", d, o)[0]


def _rva_para_offset(d, secoes, rva):
    for va, vsize, praw, rawsize in secoes:
        if va <= rva < va + max(vsize, rawsize):
            return praw + (rva - va)
    raise ValueError("RVA %#x fora das secoes do PE" % rva)


def _secoes(d):
    pe = _u32(d, 0x3C)
    if d[pe:pe + 4] != b"PE\x00\x00":
        raise ValueError("nao e um PE (assinatura ausente em %#x)" % pe)
    nsec = _u16(d, pe + 6)
    size_opt = _u16(d, pe + 20)
    opt = pe + 24
    magic = _u16(d, opt)
    base = opt + (96 if magic == 0x10B else (112 if magic == 0x20B else -1))
    if base < 0:
        raise ValueError("optional header desconhecido: %#x" % magic)
    cli_rva = _u32(d, base + 14 * 8)
    secs = []
    p = opt + size_opt
    for _ in range(nsec):
        vsize = _u32(d, p + 8)
        va = _u32(d, p + 12)
        rawsize = _u32(d, p + 16)
        praw = _u32(d, p + 20)
        secs.append((va, vsize, praw, rawsize))
        p += 40
    return secs, cli_rva


def _streams_de_metadados(d):
    secs, cli_rva = _secoes(d)
    cli = _rva_para_offset(d, secs, cli_rva)
    raiz = _rva_para_offset(d, secs, _u32(d, cli + 8))
    if _u32(d, raiz) != 0x424A5342:
        raise ValueError("raiz de metadados sem a assinatura BSJB")
    verlen = _u32(d, raiz + 12)
    p = raiz + 16 + verlen
    nstreams = _u16(d, p + 2)
    p += 4
    streams = {}
    for _ in range(nstreams):
        off = _u32(d, p)
        tam = _u32(d, p + 4)
        p += 8
        j = p
        while d[j] != 0:
            j += 1
        streams[d[p:j].decode("ascii")] = (raiz + off, tam)
        p = (j + 1 + 3) & ~3
    return streams


def _tabelas(d, tab_ini):
    hs = d[tab_ini + 6]
    valid = _u64(d, tab_ini + 8)
    p = tab_ini + 24
    rows = {}
    for t in range(64):
        if valid & (1 << t):
            rows[t] = _u32(d, p)
            p += 4
    return rows, hs, p


def _tam_simples(rows, t):
    return 4 if rows.get(t, 0) > 0xFFFF else 2


def _tam_codificado(rows, nome):
    bits, tabs = CODED[nome]
    maior = max(rows.get(t, 0) for t in tabs if t is not None)
    return 4 if maior >= (1 << (16 - bits)) else 2


def _tam_linha(rows, t, hs):
    s = 4 if hs & 1 else 2      # indice de #Strings
    g = 4 if hs & 2 else 2      # indice de #GUID
    b = 4 if hs & 4 else 2      # indice de #Blob
    S = lambda x: _tam_simples(rows, x)          # noqa: E731
    C = lambda n: _tam_codificado(rows, n)       # noqa: E731
    T = {
        0x00: 2 + s + g + g + g,
        0x01: C("ResolutionScope") + s + s,
        0x02: 4 + s + s + C("TypeDefOrRef") + S(0x04) + S(0x06),
        0x03: S(0x04),
        0x04: 2 + s + b,
        0x05: S(0x06),
        0x06: 4 + 2 + 2 + s + b + S(0x08),
        0x07: S(0x08),
        0x08: 2 + 2 + s,
        0x09: S(0x02) + C("TypeDefOrRef"),
        0x0A: C("MemberRefParent") + s + b,
        0x0B: 1 + 1 + C("HasConstant") + b,
        0x0C: C("HasCustomAttribute") + C("CustomAttributeType") + b,
        0x0D: C("HasFieldMarshal") + b,
        0x0E: 2 + C("HasDeclSecurity") + b,
        0x0F: 2 + 4 + S(0x02),
        0x10: 4 + S(0x04),
        0x11: b,
        0x12: S(0x02) + S(0x14),
        0x14: 2 + s + C("TypeDefOrRef"),
        0x15: S(0x02) + S(0x17),
        0x17: 2 + s + b,
        0x18: 2 + S(0x06) + C("HasSemantics"),
        0x19: S(0x02) + C("MethodDefOrRef") + C("MethodDefOrRef"),
        0x1A: s,
        0x1B: b,
        0x1C: 2 + C("MemberForwarded") + s + S(0x1A),
        0x1D: 4 + S(0x04),
        0x20: 4 + 2 + 2 + 2 + 2 + 4 + b + s + s,
        0x21: 4,
        0x22: 4 + 4 + 4,
        0x23: 2 + 2 + 2 + 2 + 4 + b + s + s + b,
        0x24: 4 + S(0x23),
        0x25: 4 + 4 + 4 + S(0x23),
        0x26: 4 + s + b,
        0x27: 4 + 4 + s + s + C("Implementation"),
        0x28: 4 + 4 + s + C("Implementation"),
        0x29: S(0x02) + S(0x02),
        0x2A: 2 + 2 + C("TypeOrMethodDef") + s,
        0x2B: C("MethodDefOrRef") + b,
        0x2C: S(0x2A) + C("TypeDefOrRef"),
    }
    if t not in T:
        raise ValueError("a tabela %#x (%s) nao tem tamanho de linha conhecido"
                         % (t, TABELAS.get(t, "?")))
    return T[t]


def ler_metadados(dados):
    """Le TypeRef/MemberRef/AssemblyRef da DLL. Devolve um dict (ver o docstring do modulo)."""
    streams = _streams_de_metadados(dados)
    if "#~" not in streams or "#Strings" not in streams:
        raise ValueError("a DLL nao tem os streams #~ / #Strings (nao e .NET?)")
    strings_ini, strings_tam = streams["#Strings"]
    strings = dados[strings_ini:strings_ini + strings_tam]
    tab_ini = streams["#~"][0]
    rows, hs, p0 = _tabelas(dados, tab_ini)
    off = {}
    p = p0
    for t in range(64):
        if t in rows:
            off[t] = p
            p += rows[t] * _tam_linha(rows, t, hs)

    def strz(i):
        j = strings.find(b"\x00", i)
        return strings[i:j].decode("utf-8", "replace")

    s = 4 if hs & 1 else 2
    bsz = 4 if hs & 4 else 2

    # --- TypeRef (0x01): Namespace + Name
    c = _tam_codificado(rows, "ResolutionScope")
    typerefs = {}
    for i in range(rows.get(0x01, 0)):
        base = off[0x01] + i * _tam_linha(rows, 0x01, hs)
        typerefs[i + 1] = (strz(_u16(dados, base + c)), strz(_u16(dados, base + c + s)))

    # --- MemberRef (0x0A): Class (codificado) + Name + Signature
    cm = _tam_codificado(rows, "MemberRefParent")
    tabs = CODED["MemberRefParent"][1]
    bits = CODED["MemberRefParent"][0]
    membros = []
    for i in range(rows.get(0x0A, 0)):
        base = off[0x0A] + i * _tam_linha(rows, 0x0A, hs)
        parent = _u16(dados, base)
        tag = parent & ((1 << bits) - 1)
        linha = parent >> bits
        nome = strz(_u16(dados, base + cm))
        parent_tab = tabs[tag] if tag < len(tabs) else None
        if parent_tab == 0x01 and linha in typerefs:
            pai_ns, pai_nome = typerefs[linha]
            pai = ("%s.%s" % (pai_ns, pai_nome)) if pai_ns else pai_nome
        else:
            pai = "%s:%d" % (TABELAS.get(parent_tab, "?") if parent_tab is not None else "?", linha)
        membros.append((nome, pai))

    # --- AssemblyRef (0x23): Name
    asm = []
    if rows.get(0x23, 0):
        ca = _tam_linha(rows, 0x23, hs)
        for i in range(rows[0x23]):
            base = off[0x23] + i * ca
            asm.append(strz(_u16(dados, base + 4 + 8 + bsz)))

    return {
        "sha256": hashlib.sha256(dados).hexdigest(),
        "tamanho": len(dados),
        "typerefs": sorted(set(("%s.%s" % v) if v[0] else v[1] for v in typerefs.values())),
        "memberrefs": membros,
        "nomes_de_membros": sorted(set(n for n, _ in membros)),
        "assemblyrefs": asm,
        "linhas": dict((TABELAS.get(t, hex(t)), rows[t]) for t in sorted(rows)),
    }


def candidatos_de_dll():
    """A DLL do BCT, na ordem: pacote em dist/ (a do PACOTE), bin/Release, bin/Debug.

    A do PACOTE vem primeiro porque e ela que o jogador instala - a prova tem de ser sobre o
    mesmo artefato que sai daqui. `dist/` e `bin/` sao gitignored (artefato de build), entao
    quem nao tem o build ve `NAO RODOU` - nunca um verde que esconde a checagem.
    """
    achados = []
    pacotes = sorted(glob.glob(os.path.join(arc.raiz_do_repo(), PACOTE_GLOB)))
    if pacotes:
        caminho = pacotes[-1]           # o mais novo pelo nome (= versao)
        try:
            with zipfile.ZipFile(caminho) as z:
                if ENTRADA_DLL_NO_PACOTE in z.namelist():
                    achados.append(("pacote %s!%s" % (os.path.relpath(caminho, arc.raiz_do_repo()),
                                                      ENTRADA_DLL_NO_PACOTE),
                                    z.read(ENTRADA_DLL_NO_PACOTE)))
        except (zipfile.BadZipFile, IOError):
            pass
    for sub in ("Release", "Debug"):
        p = os.path.join(raiz_mod(), "bin", sub, "netstandard2.1", "BetterCombatText.dll")
        if os.path.isfile(p):
            with io.open(p, "rb") as fh:
                achados.append((os.path.relpath(p, arc.raiz_do_repo()).replace("\\", "/"), fh.read()))
    return achados


def dll_do_pacote():
    """(origem, dados) da melhor DLL disponivel, ou (None, None)."""
    achados = candidatos_de_dll()
    return achados[0] if achados else (None, None)


def setters_de_material_em(meta):
    """As REFERENCIAS a setters de material na DLL (regra de ouro). Lista vazia = ok."""
    return sorted(set(n for n, _ in meta["memberrefs"] if REGEX_SETTER_DE_MATERIAL.match(n)))


def il_com_o_setter_do_compartilhado(dados):
    """PLANTA o defeito no IL: renomeia a REFERENCIA de leitura para a de ESCRITA.

    `get_fontSharedMaterial` e `set_fontSharedMaterial` tem o MESMO comprimento (o prefixo
    `get_`/`set_`), entao a troca dos bytes no `#Strings` mantem a DLL valida e a tabela
    MemberRef apontando para o nome novo: e exatamente o que a DLL seria se o mod tivesse
    escrito `x.fontSharedMaterial = v` em alguma linha. Se a troca nao achar o alvo (a
    referencia sumiu), devolve os bytes originais - e o teste REPROVA dizendo que o plantio
    nao achou onde agir (defeito do plantio, nao prova de nada).
    """
    alvo = b"get_fontSharedMaterial"
    if dados.count(alvo) != 1:
        return dados
    return dados.replace(alvo, b"set_fontSharedMaterial", 1)


def falhas_dos_metadados(meta):
    """As checagens do IL: leitor vivo, controle positivo, ausencia de setter, zero acoplamento."""
    falhas = []
    if len(meta["memberrefs"]) < 20:
        falhas.append("a DLL so tem %d referencia(s) de membro: o leitor de IL nao esta lendo a "
                      "tabela MemberRef (uma ausencia de setter assim nao prova nada)"
                      % len(meta["memberrefs"]))
    faltando = [m for m in MEMBROS_ESPERADOS if m not in meta["nomes_de_membros"]]
    if faltando:
        falhas.append("o leitor de IL nao achou %d referencia(s) que a DLL TEM (%s): o controle "
                      "positivo falhou - sem ele, 'nao achei o setter' seria vacuidade"
                      % (len(faltando), ", ".join(faltando)))
    proibidos = setters_de_material_em(meta)
    if proibidos:
        falhas.append("a REGRA DE OURO caiu: a DLL referencia SETTER(ES) de material (%s). No TMP "
                      "o setter escreve no MATERIAL COMPARTILHADO - a UI inteira mudaria. O mod "
                      "tem de escrever so na COPIA por componente devolvida pelo getter "
                      "`fontMaterial`" % ", ".join(proibidos))
    acoplamento = [a for a in meta["assemblyrefs"] if a.lower().startswith(("betterfont", "bettercombattext"))]
    if acoplamento:
        falhas.append("a DLL referencia outro mod do pacote em AssemblyRef: %s" % acoplamento)
    return falhas


# ===========================================================================
#  3) A REGRA DE OURO no FONTE (o par da checagem de IL)
# ===========================================================================

APLICAR_TMP = "internal static void AplicarTmp("


def falhas_regra_de_ouro_no_fonte(src):
    """O fonte so LE o compartilhado e escreve na copia? Lista vazia = ok."""
    falhas = []
    applicar = corpo(src, APLICAR_TMP)
    if applicar is None:
        return ["nao achei `AplicarTmp` no TextStyler.cs"]

    # (a) o compartilhado e LIDO, nunca escrito.
    if "fontSharedMaterial =" in applicar.replace("==", ""):
        falhas.append("`AplicarTmp` ATRIBUI a `fontSharedMaterial`: e o material COMPARTILHADO, "
                      "o mesmo objeto de todo texto daquela fonte - escrever nele muda a UI toda")
    if "compartilhadoAntes = tmp.fontSharedMaterial" not in applicar:
        falhas.append("`AplicarTmp` nao le o material compartilhado antes de clonar "
                      "(`compartilhadoAntes`): sem essa leitura nao da para saber em quem estamos")
    if "tmp.fontMaterial" not in applicar:
        falhas.append("`AplicarTmp` nao usa o getter `tmp.fontMaterial` (a COPIA por componente): "
                      "sem ele nao ha instancia por componente nenhuma")

    # (b) nenhuma atribuicao a material/m_sharedMaterial em NENHUMA linha do arquivo.
    efetivo = sem_comentarios(src)
    for alvo, rotulo in ((".fontSharedMaterial =", "fontSharedMaterial"),
                         (".sharedMaterial =", "sharedMaterial"),
                         ("m_sharedMaterial =", "m_sharedMaterial")):
        if alvo in efetivo:
            falhas.append("o TextStyler ATRIBUI a `%s` em algum ponto (fora de comentario): a "
                          "copia por componente deixou de ser a unica via" % rotulo)

    # (c) a clonagem e delegada ao TMP (`fontMaterial` -> GetMaterial -> CreateMaterialInstance),
    #     e o mod NAO escreve no material de outro mod: se o material em uso ja e uma instancia
    #     de OUTRO mod, o getter do TMP devolve ESSA instancia (nao clona por cima) - ver o
    #     achado registrado no log. O que o mod pode garantir e: nunca usa o SETTER.
    return falhas


def defeito_escreve_no_compartilhado(src=None):
    """PLANTA: o mod passa a ESCREVER no material compartilhado (o defeito da regra de ouro)."""
    texto = fonte(STYLER) if src is None else src
    alvo = "                Material mat = tmp.fontMaterial;"
    novo = ("                Material mat = tmp.fontSharedMaterial;\n"
            "                tmp.fontSharedMaterial = mat;")
    if alvo not in texto:
        return texto
    return texto.replace(alvo, novo, 1)


# ===========================================================================
#  4) IDEMPOTENCIA - o registro por InstanceID
# ===========================================================================

class ModeloEstilizadorTmp(object):
    """MODELO do guarda de idempotencia de `AplicarTmp` (C# -> Python).

    O C# guarda, por InstanceID do componente, o material que ELE instanciou. Na segunda
    chamada para o mesmo componente - o postfix roda a cada escrita do texto, a cada frame -
    o guarda casa (`nosso == compartilhadoAntes`) e a rotina sai sem tocar em nada: nao
    re-instancia material e nao re-aplica propriedade.

    `aplicar(id, material_em_uso)` devolve `"aplicou"` na primeira vez e `"no-op"` depois.
    """

    def __init__(self):
        self.registro = {}
        self.aplicacoes = 0          # quantas vezes o mod instanciou material + escreveu props
        self.materiais = 0           # quantas instancias de material o mod criou

    def aplicar(self, id_componente, material_em_uso):
        if id_componente in self.registro and self.registro[id_componente] == material_em_uso:
            return "no-op"
        self.registro[id_componente] = "instancia-%d" % id_componente
        self.aplicacoes += 1
        self.materiais += 1
        return "aplicou"


class ModeloEstilizadorTmpSemGuarda(ModeloEstilizadorTmp):
    """O DEFEITO transcrito: sem o guarda, cada chamada re-instancia e re-aplica (acumula)."""

    def aplicar(self, id_componente, material_em_uso):
        self.registro[id_componente] = "instancia-%d-%d" % (id_componente, self.aplicacoes)
        self.aplicacoes += 1
        self.materiais += 1
        return "aplicou"


def falhas_da_idempotencia(src, src_patches=None):
    """O guarda por InstanceID esta de pe nos DOIS caminhos (TMP e legado)? Vazio = ok."""
    falhas = []
    applicar = corpo(src, APLICAR_TMP)
    if applicar is None:
        return ["nao achei `AplicarTmp` no TextStyler.cs"]

    if "MateriaisInstanciados.TryGetValue(id, out var nosso)" not in applicar:
        falhas.append("`AplicarTmp` nao consulta `MateriaisInstanciados`: sem o registro por "
                      "InstanceID a rotina re-instancia o material e re-aplica o efeito a cada "
                      "postfix (a cada escrita do texto) - o efeito NAO e idempotente")
    if "nosso == compartilhadoAntes" not in applicar:
        falhas.append("o guarda de `AplicarTmp` nao compara o material registrado com o material "
                      "em uso: ele nao reconhece 'o texto ja esta tratado'")
    i_guarda = applicar.find("nosso == compartilhadoAntes")
    i_instancia = applicar.find("Material mat = tmp.fontMaterial;")
    i_registra = applicar.find("MateriaisInstanciados[id] = mat;")
    if i_guarda < 0 or i_instancia < 0 or i_registra < 0:
        falhas.append("o caminho de idempotencia de `AplicarTmp` esta incompleto "
                      "(consulta, instancia ou registro sumiu)")
    elif not (i_guarda < i_instancia < i_registra):
        falhas.append("a ORDEM do guarda mudou em `AplicarTmp`: a consulta ao registro tem de vir "
                      "ANTES de instanciar o material e o registro tem de vir depois - invertida, "
                      "o texto ja tratado e reinstanciado antes de ser reconhecido")

    tamanho = corpo(src, "private static void AplicarTamanho(")
    if tamanho is None:
        falhas.append("nao achei `AplicarTamanho` no TextStyler.cs")
    else:
        if "TamanhoOriginal.TryGetValue(id, out var original)" not in tamanho:
            falhas.append("`AplicarTamanho` nao guarda o tamanho ORIGINAL do componente: o ajuste "
                          "de fonte soma em cima do valor JA somado e acumula a cada chamada")
        if "tmp.fontSize = original + extra;" not in tamanho:
            falhas.append("`AplicarTamanho` nao parte do original (`= original + extra`): "
                          "acumula")

    legado = corpo(src, "internal static void AplicarTextoLegado(")
    if legado is None:
        falhas.append("nao achei `AplicarTextoLegado` no TextStyler.cs")
    else:
        if "TextosLegadosTratados.Contains(id)" not in legado:
            falhas.append("o caminho LEGADO nao tem guarda de 'ja tratado' "
                          "(`TextosLegadosTratados`): re-aplicaria a cada escrita do rotulo")
        if "TamanhoOriginalLegado.TryGetValue(id, out var original)" not in legado:
            falhas.append("o caminho LEGADO nao guarda o tamanho original: o ajuste de fonte "
                          "acumularia")
    return falhas


def defeito_sem_guarda_idempotencia(src=None):
    """PLANTA: o guarda de idempotencia do caminho TMP some (re-instancia a cada chamada).

    Remove o BLOCO TODO do `if (MateriaisInstanciados.TryGetValue(...))` - inclusive a
    reavaliacao da sombra que vive dentro dele (BCT-2) -, de forma literal-aware: o corpo do
    `if` pode ganhar linha nova sem quebrar o plantio (o `_bloco_de` acha o fechamento certo).
    """
    texto = fonte(STYLER) if src is None else src
    marca = "if (MateriaisInstanciados.TryGetValue(id, out var nosso)"
    i = texto.find(marca)
    if i < 0:
        return texto
    j = texto.find("{", i)
    if j < 0:
        return texto
    bloco = _bloco_de(texto, j)
    if not bloco:
        return texto
    return texto[:i] + texto[j + len(bloco):]


def defeito_tamanho_acumula(src=None):
    """PLANTA: o ajuste de fonte soma no valor ATUAL (acumula a cada chamada)."""
    texto = fonte(STYLER) if src is None else src
    alvo = "tmp.fontSize = original + extra;"
    if alvo not in texto:
        return texto
    return texto.replace(alvo, "tmp.fontSize = tmp.fontSize + extra;", 1)


# ===========================================================================
#  5) DEFAULTS (Configuracao.cs, com arquivo:linha)
# ===========================================================================

RE_BIND = re.compile(r"Bind\(\s*([A-Za-z_]\w*|\"[^\"]*\")\s*,\s*\"([^\"]+)\"\s*,\s*"
                     r"(true|false|-?\d+(?:\.\d+)?f?|\"[^\"]*\")")


def binds_com_linha(src):
    """Os `cfg.Bind(...)` do fonte, com secao/chave/default e a LINHA. Nada digitado."""
    secoes = dict((m.group(1), m.group(2))
                  for m in re.finditer(r"var\s+(\w+)\s*=\s*\"([^\"]*)\"", src))
    achados = []
    for m in RE_BIND.finditer(src):
        sec_ref, chave, valor = m.group(1), m.group(2), m.group(3)
        secao = sec_ref[1:-1] if sec_ref.startswith('"') else secoes.get(sec_ref, sec_ref)
        if valor == "true":
            v = True
        elif valor == "false":
            v = False
        else:
            v = valor
        achados.append({"secao": secao, "chave": chave, "valor": v,
                        "linha": src.count("\n", 0, m.start()) + 1})
    return achados


# A ESPEC do dono (pedido de 30/09): o grupo do tooltip DESLIGADO (Title/Description sao
# compartilhados), o grupo de eventos/dado LIGADO, a chave mestra LIGADA, o numero de vida
# DESLIGADO (fora do pedido), o diagnostico LIGADO.
ESPEC_DEFAULTS = (
    ("1. Geral", "Ativar", True),
    ("1. Geral", "DiagnosticoNoArranque", True),
    ("4. Eventos", "Ativar", True),
    ("5. Extra", "AplicarNoNumeroDeVida", False),
    ("6. Tooltip", "Ativar", False),
)


def falhas_dos_defaults(src):
    """Os defaults do .cfg batem com a ESPEC? Vazio = ok. Toda falha aponta arquivo:linha."""
    falhas = []
    achados = binds_com_linha(src)
    for secao, chave, valor in ESPEC_DEFAULTS:
        casa = [a for a in achados if secao in (a["secao"] or "") and a["chave"] == chave]
        if not casa:
            falhas.append("nao achei o `Bind` de %s > %s em %s" % (secao, chave, CFG))
            continue
        a = casa[0]
        if a["valor"] != valor:
            falhas.append("%s:%d - o default de '%s' > %s mudou: esperado %r, obtido %r"
                          % (CFG, a["linha"], a["secao"], chave, valor, a["valor"]))

    # O grupo do tooltip vem desligado POR UM MOTIVO que tem de estar escrito: Title/Description
    # sao os MESMOS componentes dos tooltips de skill/item/powerup (ligar espalharia o efeito).
    tooltip = [a for a in achados if "Tooltip" in (a["secao"] or "") and a["chave"] == "Ativar"]
    if tooltip:
        acima = comentarios_acima(src, tooltip[0]["linha"], 40)
        if "Title" not in acima or "Description" not in acima:
            falhas.append("o motivo do tooltip vir DESLIGADO nao esta escrito acima do default "
                          "(%s:%d): Title/Description sao os MESMOS componentes dos tooltips de "
                          "skill/item/powerup, e quem ligar tem de saber disso"
                          % (CFG, tooltip[0]["linha"]))
    return falhas


def defeito_default_tooltip_ligado(src=None):
    """PLANTA: o tooltip de status passa a vir LIGADO (espalharia o efeito para todo tooltip)."""
    texto = fonte(CFG) if src is None else src
    alvo = 'TooltipAtivar = cfg.Bind(secTooltip, "Ativar", false,'
    if alvo not in texto:
        return texto
    return texto.replace(alvo, 'TooltipAtivar = cfg.Bind(secTooltip, "Ativar", true,', 1)


def defeito_default_eventos_desligado(src=None):
    """PLANTA: o grupo de eventos/dado passa a vir DESLIGADO (o pedido do dono e ligado)."""
    texto = fonte(CFG) if src is None else src
    alvo = 'EventosAtivar = cfg.Bind(secDado, "Ativar", true,'
    if alvo not in texto:
        return texto
    return texto.replace(alvo, 'EventosAtivar = cfg.Bind(secDado, "Ativar", false,', 1)


# ===========================================================================
#  6) DESLIGAR E INERTE (Ativar = false)
# ===========================================================================

RE_PATCH = re.compile(r"\[HarmonyPatch\s*\(")


def _atributos_harmony(src):
    """[(texto_do_atributo, pos, fim)] dos `[HarmonyPatch(...)]`, com parenteses balanceados.

    O casamento por `[^\\]]*` quebra no atributo que tem `new[] { typeof(X) }` (o `]` de
    `new[]` fecha a classe de caracteres): o `PatchTooltipDeStatus` e um deles, e ele ficaria
    FORA da varredura em silencio. Aqui o fim do atributo sai do balanceamento de parenteses.
    """
    achados = []
    for m in RE_PATCH.finditer(src):
        prof, k = 0, src.index("(", m.start())
        while k < len(src):
            if src[k] == "(":
                prof += 1
            elif src[k] == ")":
                prof -= 1
                if prof == 0:
                    break
            k += 1
        achados.append((src[m.start():k + 1], m.start(), k + 1))
    return achados


def classes_de_gancho(src, arquivo=""):
    """[(classe, atributo, linha, [(metodo, corpo, declaracao)])] das classes com [HarmonyPatch]."""
    achados = []
    for atributo, pos, fim in _atributos_harmony(src):
        mc = re.search(r"class\s+(\w+)", src[fim:])
        if not mc:
            continue
        pos_classe = fim + mc.start()
        bloco = _bloco_de(src, src.find("{", pos_classe))
        if bloco is None:
            continue
        metodos = []
        for mm in re.finditer(r"(?:private|internal|public)\s+static\s+(?:void|\w+)\s+"
                              r"(Prefix|Postfix|Transpiler|Finalizer)\s*\(", bloco):
            corpo_m = _bloco_de(bloco, bloco.find("{", mm.end()))
            metodos.append((mm.group(1), corpo_m, mm.group(0)))
        achados.append((mc.group(1), atributo, src.count("\n", 0, pos) + 1, metodos))
    return achados


def _corpo_de_metodo(arquivo_src, nome):
    m = re.search(r"(?:private|internal|public)\s+static\s+[\w<>\[\],.\s]*?\s+%s\s*\(" % nome,
                  arquivo_src)
    if not m:
        return None
    return corpo(arquivo_src, m.group(0))


def _guardado(corpo_metodo, arquivo_src):
    """O gancho e inerte com Ativar=false - direto ou por delegacao a um metodo do arquivo?"""
    if corpo_metodo is None:
        return False
    if "!Plugin.Ativo" in corpo_metodo:
        return True
    for nome in set(re.findall(r"\b([A-Z]\w*)\s*\(", corpo_metodo)):
        sub = _corpo_de_metodo(arquivo_src, nome)
        if sub and "!Plugin.Ativo" in sub:
            return True
    return False


def falhas_desligar_inertes(src_plugin, src_outros):
    """Com Ativar=false nenhum gancho age (nem Patch, nem diagnostico)? Vazio = ok."""
    falhas = []
    awake = corpo(src_plugin, "private void Awake()")
    if awake is None:
        return ["nao achei `Awake` no Plugin.cs"]
    i_ativo = awake.find("if (!Cfg.Ativar.Value)")
    i_aplicar = awake.find("AplicarPatches()")
    if i_ativo < 0:
        falhas.append("`Awake` nao checa a chave mestra (`if (!Cfg.Ativar.Value)`): com "
                      "Ativar=false o mod ainda aplicaria gancho")
    elif i_aplicar >= 0 and i_ativo > i_aplicar:
        falhas.append("`Awake` aplica os ganchos ANTES de checar a chave mestra: com Ativar=false "
                      "os ganchos ja estariam no ar")
    if "Ativo = false;" not in awake:
        falhas.append("`Awake` nao marca `Ativo = false` no caminho desligado")

    achados = classes_de_gancho(src_plugin)
    for nome_arq, texto in src_outros.items():
        achados.extend(classes_de_gancho(texto, nome_arq))
    if not achados:
        return falhas + ["nao achei nenhuma classe com [HarmonyPatch] no mod"]
    for classe, atributo, linha, metodos in achados:
        if not metodos:
            continue
        fonte_do_arquivo = src_plugin
        for texto in src_outros.values():
            if "class " + classe in texto:
                fonte_do_arquivo = texto
                break
        for metodo, corpo_m, _ in metodos:
            if not _guardado(corpo_m, fonte_do_arquivo):
                falhas.append("o gancho %s.%s nao e inerte com `Ativar=false`: o postfix roda "
                              "(e muda a tela) mesmo com o mod desligado" % (classe, metodo))
    return falhas


def defeito_gancho_sem_guarda(src=None):
    """PLANTA: um gancho perde o `if (!Plugin.Ativo)` (age com o mod desligado)."""
    texto = fonte(PATCHES) if src is None else src
    alvo = ("        private static void Postfix(BossHealthbar __instance)\n"
            "        {\n"
            "            if (!Plugin.Ativo)\n"
            "            {\n"
            "                return;\n"
            "            }\n")
    if alvo not in texto:
        return texto
    return texto.replace(alvo,
                         "        private static void Postfix(BossHealthbar __instance)\n        {\n", 1)


class ModeloDeModo(object):
    """MODELO do modo do mod: `Ativo` decide se algum gancho pode agir.

    `gancho(superficie)` responde o que o C# responde com a chave mestra: com `Ativo=false`
    o postfix sai no primeiro `if (!Plugin.Ativo)` - nada e tocado, e nada lanca excecao.
    """

    def __init__(self, ativo):
        self.ativo = ativo
        self.mudou = 0
        self.agiu = 0

    def gancho(self, superficie):
        if not self.ativo:
            return "nada"
        self.agiu += 1
        self.mudou += 1
        return "mudou"


class ModeloDeModoAntesDaChave(ModeloDeModo):
    """O DEFEITO transcrito: os ganchos agem mesmo com o mod desligado."""

    def gancho(self, superficie):
        self.agiu += 1
        self.mudou += 1
        return "mudou"


# ===========================================================================
#  7) CAMINHO LEGADO (UnityEngine.UI.Text)
# ===========================================================================

APLICAR_LEGADO = "internal static void AplicarTextoLegado("
NAO_PODE_TER_NO_LEGADO = ("fontMaterial", "fontSharedMaterial", "_OutlineWidth",
                          "_UnderlaySoftness", "EnableKeyword", "new Material", "SetFloat",
                          "mat.Set")


def falhas_do_caminho_legado(src):
    """O rotulo de status (UI.Text) recebe contorno DURO e nenhum material SDF? Vazio = ok."""
    falhas = []
    legado = corpo(src, APLICAR_LEGADO)
    if legado is None:
        return ["nao achei `AplicarTextoLegado` no TextStyler.cs"]

    for trecho, rotulo in (("AddComponent<Outline>", "o contorno DURO (componente Outline)"),
                           ("effectDistance", "a distancia do contorno duro"),
                           ("effectColor", "a cor do contorno/sombra"),
                           ("AddComponent<Shadow>", "a sombra dura (componente Shadow)"),
                           ("GetComponents<Graphic>()", "a guarda do primeiro Graphic")):
        if trecho not in legado:
            falhas.append("o caminho legado nao tem %s: o rotulo de status ficaria sem o efeito "
                          "que EXISTE nesse tipo de texto" % rotulo)

    for proibido in NAO_PODE_TER_NO_LEGADO:
        if proibido in legado:
            falhas.append("o caminho legado usa `%s`: UI.Text e fonte BITMAP (sem distance field), "
                          "nao existe contorno suave nem material SDF ali - esse caminho tem de "
                          "ser o contorno DURO" % proibido)
    return falhas


def falhas_da_ligacao_legada(src_patches):
    """A superficie legada e mesmo os rotulos de stack/turno (o TIPO real, lido do jogo)?"""
    falhas = []
    if "TextStyler.AplicarTextoLegado(icone.stackCount" not in src_patches:
        falhas.append("o patch dos rotulos nao chama `AplicarTextoLegado` no `icone.stackCount`: o "
                      "caminho legado deixou de ser ligado aos rotulos de stack do StatusIcon")
    if "TextStyler.AplicarTextoLegado(icone.turnCount" not in src_patches:
        falhas.append("o patch dos rotulos nao chama `AplicarTextoLegado` no `icone.turnCount`")
    if "TextStyler.AplicarTmp(icone.stackCount" in src_patches:
        falhas.append("o patch dos rotulos trata o `stackCount` como TMP: o tipo real e "
                      "UnityEngine.UI.Text (medido em jogo) e o caminho seria o errado")
    return falhas


def defeito_legado_usa_material(src=None):
    """PLANTA: o caminho legado passa a pedir material de distance field (impossivel ali)."""
    texto = fonte(STYLER) if src is None else src
    alvo = "                if (cfg.Negrito.Value)\n                {\n                    txt.fontStyle |= FontStyle.Bold;\n                }"
    novo = ("                bool df = txt.fontMaterial.HasProperty(\"_OutlineWidth\");\n"
            "                if (cfg.Negrito.Value)\n"
            "                {\n"
            "                    txt.fontStyle |= FontStyle.Bold;\n"
            "                }")
    if alvo not in texto:
        return texto
    return texto.replace(alvo, novo, 1)


# ===========================================================================
#  8) DIAGNOSTICO DE ARRANQUE - o intervalo, a PARADA e a chave
# ===========================================================================

# A ESPEC do dono (pedido de 30/09, e o que o proprio diagnostico documenta):
#   espera minima 20s, intervalo 5s (era 2s), desistir em 240s.
ESPEC_DIAG = (20.0, 5.0, 240.0)
CONST_DIAG = ("EsperaMinima", "IntervaloChecagem", "DesistirEm")


def constantes_do_diagnostico(src=None):
    """Os tres `private const float` do diagnostico, LIDOS do fonte (nunca digitados)."""
    texto = fonte(DIAG) if src is None else src
    valores = []
    for nome in CONST_DIAG:
        m = re.search(r"private\s+const\s+float\s+%s\s*=\s*([\d.]+)f" % nome, texto)
        if m is None:
            return None
        valores.append(float(m.group(1)))
    return tuple(valores)


class ModeloDiagnostico(object):
    """MODELO PURO do `DiagnosticoRotina.Tentar` (C# -> Python): varre ou nao varre?

    `tentar(agora, tem_alvo, ativo, config_ligada)` responde o que o C# responde:
      * `None`      -> nao fez nada (cedo demais, dentro do intervalo, desligado, ja feito);
      * `"varreu"`  -> a varredura de cena RODOU (custo);
      * `"rodou"`   -> varreu E rodou o diagnostico e ENCERROU (nada mais e varrido).
    """

    def __init__(self, espera_minima, intervalo, desistir_em):
        self.espera_minima = espera_minima
        self.intervalo = intervalo
        self.desistir_em = desistir_em
        self.feito = False
        self.falhou = False
        self.proxima = 0.0
        self.varreduras = 0
        self.execucoes = 0

    def tentar(self, agora, tem_alvo, ativo=True, config_ligada=True):
        if self.feito or self.falhou or not ativo:
            return None
        if not config_ligada:
            self.feito = True      # desligado no config: encerra e nao varre NUNCA
            return None
        if agora < self.espera_minima or agora < self.proxima:
            return None
        self.proxima = agora + self.intervalo
        self.varreduras += 1
        if not tem_alvo and agora < self.desistir_em:
            return "varreu"
        self.feito = True
        self.execucoes += 1
        return "rodou"


class ModeloDiagnosticoIntervalo2(ModeloDiagnostico):
    """O DEFEITO de desempenho transcrito: varredura a cada 2s (o intervalo antigo)."""

    def __init__(self, espera_minima, desistir_em):
        ModeloDiagnostico.__init__(self, espera_minima, 2.0, desistir_em)


class ModeloDiagnosticoSemParada(ModeloDiagnostico):
    """O DEFEITO antigo transcrito: o diagnostico NUNCA encerra (varre para sempre)."""

    def tentar(self, agora, tem_alvo, ativo=True, config_ligada=True):
        if self.falhou or not ativo:
            return None
        if not config_ligada:
            return None                       # ignora a chave: varre mesma
        if agora < self.espera_minima or agora < self.proxima:
            return None
        self.proxima = agora + self.intervalo
        self.varreduras += 1
        self.execucoes += 1
        return "varreu"


def simular_arranque(modelo, ate_segundos, passo=0.1, tem_alvo_em=None, config_ligada=True):
    """Roda o gatilho por frame (o `GUIManager.Update` chama `Tentar`) e devolve o modelo."""
    t = 0.0
    alvo = tem_alvo_em is not None and t >= tem_alvo_em
    while t <= ate_segundos + 1e-9:
        alvo = tem_alvo_em is not None and t >= tem_alvo_em
        modelo.tentar(t, alvo, config_ligada=config_ligada)
        t += passo
    return modelo


def falhas_do_diagnostico(src):
    """O intervalo (5s), a PARADA no primeiro sucesso e a chave que desliga. Vazio = ok."""
    falhas = []
    valores = constantes_do_diagnostico(src)
    if valores is None:
        return ["nao achei as tres constantes do diagnostico (%s) em %s: o teste le o intervalo do "
                "fonte, nunca digita o numero" % ("/".join(CONST_DIAG), DIAG)]
    if valores != ESPEC_DIAG:
        divergentes = ", ".join("%s=%s (esperado %s)" % (nome, obtido, esperado)
                                for nome, obtido, esperado in zip(CONST_DIAG, valores, ESPEC_DIAG)
                                if obtido != esperado)
        falhas.append("%s - as constantes do diagnostico divergem da ESPEC: %s. O intervalo era "
                      "2s e virou 5s, e a varredura tem de PARAR no primeiro sucesso"
                      % (DIAG, divergentes))

    tentar = corpo(src, "internal static void Tentar(")
    if tentar is None:
        return falhas + ["nao achei `Tentar` no DiagnosticoArranque.cs"]
    if "_feito || _falhou || !Plugin.Ativo" not in tentar:
        falhas.append("`Tentar` perdeu a guarda de estado (`_feito || _falhou || !Plugin.Ativo`): "
                      "a rotina voltaria a varrer depois de encerrada")
    if "Cfg.DiagnosticoArranque.Value" not in tentar:
        falhas.append("`Tentar` nao le a chave de config que desliga a varredura "
                      "(`DiagnosticoNoArranque`): o custo da varredura nao teria como ser zerado")
    if "TemAlvoEmCena()" not in tentar:
        falhas.append("`Tentar` nao checa se algum alvo ja esta em cena (`TemAlvoEmCena`)")
    elif "agora < DesistirEm" not in tentar:
        falhas.append("`Tentar` nao tem o corte de desistencia (`agora < DesistirEm`)")

    # A PARADA no primeiro sucesso e ESTRUTURAL: o `_feito = true;` que encerra a varredura tem
    # de estar DEPOIS da checagem de alvo em cena e ANTES do `Rodar()`. (Conferir so a presenca
    # do token nao vale: ha outro `_feito = true;` no ramo do config, e ele sozinho satisfazia a
    # busca de substring - a mesma armadilha que a REV-56 achou na trava do orcamento.)
    i_alvo = tentar.find("TemAlvoEmCena()")
    i_rodar = tentar.find("Rodar();")
    i_feito = tentar.find("_feito = true;", i_alvo if i_alvo >= 0 else 0)
    if i_alvo < 0 or i_rodar < 0:
        falhas.append("`Tentar` nao tem o par 'checa alvo em cena -> roda' (a varredura nao PARA "
                      "no primeiro sucesso)")
    elif i_feito < 0 or i_feito > i_rodar:
        falhas.append("`Tentar` nao encerra a varredura (`_feito = true;`) entre a checagem de "
                      "alvo em cena e o `Rodar()`: a varredura continua a cada intervalo, para "
                      "sempre, que e o defeito de desempenho medido (~110 varreduras por arranque)")
    return falhas


def defeito_diagnostico_2s(src=None):
    """PLANTA: o intervalo volta a 2s (o defeito de desempenho medido)."""
    texto = fonte(DIAG) if src is None else src
    alvo = "private const float IntervaloChecagem = 5f;"
    if alvo not in texto:
        return texto
    return texto.replace(alvo, "private const float IntervaloChecagem = 2f;", 1)


def defeito_diagnostico_sem_parada(src=None):
    """PLANTA: a varredura deixa de encerrar no primeiro sucesso (varre para sempre)."""
    texto = fonte(DIAG) if src is None else src
    alvo = "                _feito = true;\n                Plugin.Log.LogInfo(temAlvo"
    if alvo not in texto:
        return texto
    return texto.replace(alvo, "                Plugin.Log.LogInfo(temAlvo", 1)


def defeito_diagnostico_ignora_config(src=None):
    """PLANTA: a chave `DiagnosticoNoArranque=false` deixa de desligar a varredura."""
    texto = fonte(DIAG) if src is None else src
    alvo = "                if (!Plugin.Cfg.DiagnosticoArranque.Value)\n"
    if alvo not in texto:
        return texto
    return texto.replace(alvo, "                if (false)\n", 1)


# ===========================================================================
#  9) A PRECONDICAO DO SHADER
# ===========================================================================

SHADER_LOG = os.path.join("tools", "fixtures", "bf-shaders-em-jogo.log")


def shaders_medidos():
    """As variantes de shader dos textos de combate, da MEDICAO versionada em jogo.

    E o mesmo arquivo que o BetterFont cita: o diagnostico de arranque (CAP-1) leu, em jogo,
    o shader de cada superficie alvo. Os nomes começam com `TextMeshPro/Distance Field` - e
    por isso a precondicao do efeito e a CAPACIDADE (`_OutlineWidth`), nao o nome.
    """
    caminho = os.path.join(arc.raiz_do_repo(), SHADER_LOG)
    if not os.path.isfile(caminho):
        return None
    achados = []
    with io.open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            if "shader=TextMeshPro/" in linha:
                achados.append(linha.split("shader=", 1)[1].strip())
    return achados


def falhas_da_precondicao(src):
    """O mod CONFIRMA a precondicao (HasProperty) antes de aplicar? Vazio = ok."""
    falhas = []
    applicar = corpo(src, APLICAR_TMP)
    if applicar is None:
        return ["nao achei `AplicarTmp` no TextStyler.cs"]

    if 'HasProperty("_OutlineWidth")' not in applicar:
        falhas.append("`AplicarTmp` nao confirma `HasProperty(\"_OutlineWidth\")` antes do halo: "
                      "ele voltaria a PRESUMIR que o material tem o efeito (o texto ficaria mudo, "
                      "ou o halo nao aparece, sem o mod dizer por que)")
    if 'HasProperty("_UnderlaySoftness")' not in applicar:
        falhas.append("`AplicarTmp` nao confirma `HasProperty(\"_UnderlaySoftness\")` antes da "
                      "sombra")
    i_conf = applicar.find('HasProperty("_OutlineWidth")')
    i_usa = applicar.find('SetColor("_OutlineColor"')
    if i_conf >= 0 and i_usa >= 0 and i_conf > i_usa:
        falhas.append("a confirmacao do `_OutlineWidth` vem DEPOIS de escrever a cor do contorno: "
                      "a escrita aconteceria sem a precondicao confirmada")
    # A recusa por NOME de shader e o defeito que o BCT nao pode ter (o nome varia por
    # superficie - ver `shaders_medidos`); o criterio e a CAPACIDADE.
    if re.search(r"shader\.name\s*==|shader\.name\.Contains", applicar):
        falhas.append("`AplicarTmp` decide pelo NOME do shader: as superficies alvo usam "
                      "variantes diferentes (Distance Field, Distance Field Overlay, Distance "
                      "Field (Surface) - medido em jogo) e o nome nao diz se o EFEITO existe")
    if "ehDistanceField" not in applicar or "temUnderlay" not in applicar:
        falhas.append("`AplicarTmp` nao guarda a confirmacao em variavel propria "
                      "(`ehDistanceField`/`temUnderlay`) - a precondicao nao chega ao ramo de "
                      "aplicacao")
    # A confirmacao tem de GOVERNAR o ramo: o halo e a sombra so entram no `if (<precondicao>)`,
    # com o caminho de recusa no `else`. Conferir so a existencia da variavel nao vale - ela
    # pode continuar declarada e o ramo aplicar assim mesmo.
    for precondicao, rotulo in (("ehDistanceField", "o halo (_OutlineWidth)"),
                                ("temUnderlay", "a sombra (_UnderlaySoftness)")):
        if "if (%s)" % precondicao not in applicar:
            falhas.append("`AplicarTmp` nao poe %s dentro de `if (%s)`: o efeito seria aplicado "
                          "sem a precondicao confirmada (o material nao tem a propriedade e a "
                          "escrita nao faz nada, em silencio)" % (rotulo, precondicao))
    if "AvisoUma(superficie" not in applicar:
        falhas.append("`AplicarTmp` nao avisa (uma vez por superficie) quando a precondicao FALHA: "
                      "o texto ficaria sem efeito, em silencio")
    return falhas


def defeito_precondicao_nao_confere(src=None):
    """PLANTA: o mod deixa de confirmar a precondicao e aplica direto."""
    texto = fonte(STYLER) if src is None else src
    alvo = ("                    if (ehDistanceField)\n                    {")
    if alvo not in texto:
        return texto
    return texto.replace(alvo, "                    if (true)\n                    {", 1)


def defeito_precondicao_por_nome(src=None):
    """PLANTA: a decisao passa a ser pelo NOME do shader (em vez da capacidade)."""
    texto = fonte(STYLER) if src is None else src
    alvo = 'bool ehDistanceField = mat.HasProperty("_OutlineWidth");'
    if alvo not in texto:
        return texto
    return texto.replace(alvo,
                         'bool ehDistanceField = shader != null && shader.name.Contains("Distance Field");', 1)


# ===========================================================================
# 10) O APLICADOR (gancho a gancho) e a CONTRA-PROVA de tools/check_patches.py
# ===========================================================================

APLICAR_PATCHES = "private static int AplicarPatches()"
EH_CLASSE = "private static bool EhClasseDeGancho("


def falhas_do_aplicador(src_plugin):
    """Gancho a gancho, com contagem REAL, sem PatchAll. Vazio = ok."""
    falhas = []
    corpo_ap = corpo(src_plugin, APLICAR_PATCHES)
    if corpo_ap is None:
        return ["nao achei `AplicarPatches` no Plugin.cs"]
    if "PatchAll(" in sem_comentarios(src_plugin):
        falhas.append("o Plugin.cs usa `PatchAll()`: e tudo-ou-nada - um gancho ruim deixa os "
                      "outros sem aplicar, em silencio (foi o defeito que deixou 4 mods inertes)")
    if "CreateClassProcessor(tipo)" not in corpo_ap:
        falhas.append("o aplicador nao cria o processador por classe "
                      "(`harmony.CreateClassProcessor(tipo)`)")
    if "processador.Patch()" not in corpo_ap:
        falhas.append("o aplicador nao aplica classe a classe (`processador.Patch()`)")
    if "EhClasseDeGancho(tipo)" not in corpo_ap:
        falhas.append("o aplicador nao filtra pelo `EhClasseDeGancho(tipo)`")
    if "ganchosOk++" not in corpo_ap or "metodosOk += quantos" not in corpo_ap:
        falhas.append("o aplicador nao conta os ganchos REAIS (ganchosOk/metodosOk): o resumo "
                      "passaria a ser um numero fixo, e um gancho que nao entrou nao apareceria")
    if 'ganchosOk + "/" + ganchosTotal' not in corpo_ap:
        falhas.append('o resumo do aplicador nao usa a contagem REAL (ganchosOk + "/" + '
                      'ganchosTotal): um gancho que nao entrou nao apareceria no log')

    filtro = corpo(src_plugin, EH_CLASSE)
    if filtro is None:
        falhas.append("nao achei `EhClasseDeGancho`: sem filtro proprio, o aplicador nao sabe o "
                      "que e gancho")
    else:
        if "typeof(HarmonyPatch)" not in filtro:
            falhas.append("o filtro nao aceita a classe por `[HarmonyPatch]` no TIPO")
        for atributo_de_metodo in ("HarmonyPrefix", "HarmonyPostfix", "HarmonyTranspiler",
                                   "HarmonyFinalizer"):
            if atributo_de_metodo in filtro:
                falhas.append("o filtro passou a EXIGIR `%s` no METODO: os ganchos declarados pela "
                              "CONVENCAO DE NOME do Harmony (metodo `Postfix`) ficariam de fora, em "
                              "silencio - foi o defeito dos 4 mods inertes" % atributo_de_metodo)

    return falhas


def _check_patches():
    """Importa `tools/check_patches.py` (o modulo compartilhado) sem executar o `main`."""
    if "tools" not in sys.path:
        sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
    import check_patches  # noqa: E402
    return check_patches


def decisao_do_check_patches(src_plugin, fontes_do_projeto):
    """A decisao da REGRA 5 de `check_patches` sobre um projeto dado. Devolve (reprova, detalhe).

    Transcreve o ramo que REPROVA: o filtro do mod exige atributo no metodo
    (`HarmonyPrefix`/`HarmonyPostfix`) e NAO cita os nomes de convencao E existem ganchos
    declarados por convencao de nome -> `check_patches` reprova. A conta sai do codigo: as
    classes de patch vem de TODOS os .cs do projeto (o filtro vive no Plugin.cs, as classes
    nos outros arquivos) e os metodos de gancho de `classes_de_patch` - igual ao `main`.
    """
    cp = _check_patches()
    codigo, sem_comentario, _ = cp.separar(src_plugin)
    classes = []
    for texto in (fontes_do_projeto or []):
        codigo_cs, _, _ = cp.separar(texto)
        classes.extend(cp.classes_de_patch(codigo_cs))
    por_nome = [g for c in classes for g in c[2] if g[2]]
    filtros = cp.filtros_de_gancho(codigo, sem_comentario)
    exigem = [f for f in filtros
              if cp.ATRIBUTOS_DO_HARMONY.search(f[2]) and not cp.NOMES_DE_CONVENCAO.search(f[2])]
    cobertura = "%d classe(s) de patch, %d metodo(s) de gancho (%d por nome)" % (
        len(classes), sum(len(c[2]) for c in classes), len(por_nome))
    if exigem and por_nome:
        return True, ("%s (Plugin.cs:%d) exige atributo no metodo e nao cita os nomes de "
                      "convencao: %s - o mod carregaria aplicando 0 gancho por nome"
                      % (exigem[0][0], exigem[0][1], cobertura))
    return False, cobertura + "; nenhum filtro exigindo atributo sobre gancho por nome"


def defeito_filtro_exige_atributo(src=None):
    """PLANTA: o filtro passa a exigir `[HarmonyPostfix]` no metodo (o defeito A-1)."""
    texto = fonte(PLUGIN) if src is None else src
    alvo = "                return tipo.GetCustomAttributes(typeof(HarmonyPatch), false).Length > 0;"
    defeito = ("                return tipo.GetCustomAttributes(typeof(HarmonyPatch), false).Length > 0\n"
               "                    && System.Array.Exists(\n"
               "                        tipo.GetMethods(System.Reflection.BindingFlags.Public |\n"
               "                            System.Reflection.BindingFlags.NonPublic |\n"
               "                            System.Reflection.BindingFlags.Instance |\n"
               "                            System.Reflection.BindingFlags.Static),\n"
               "                        m => m.GetCustomAttributes(typeof(HarmonyPostfix), false).Length > 0);")
    if alvo not in texto:
        return texto
    return texto.replace(alvo, defeito, 1)


# ===========================================================================
# 11) CONVIVENCIA COM O BetterFont (do lado do BCT)
# ===========================================================================

# Nomes/GUIDs do OUTRO mod. O CODIGO (e a DLL) do BCT nao pode conhecer nenhum deles - a
# dependencia do pacote (manifest.json) e uma escolha de empacotamento documentada no README
# ("Needs: BepInEx 5 and BetterFont"), nao codigo.
PROIBIDOS = ("BetterFont", "betterfont", "com.gumatos.betterfont",
             "DefRuivo_StolenRealmMods-BetterFont")


def ocorrencias_de_acoplamento(texto, proibidos=PROIBIDOS):
    return [p for p in proibidos if p in texto]


def mencionados_no_texto(texto, proibidos=PROIBIDOS):
    """Ocorrencias no texto CRU (com comentario) - usado para REPORTAR menciona em comentario."""
    return [p for p in proibidos if p in texto]


def defeito_acopla_betterfont(texto=None):
    """PLANTA: o CODIGO do BCT passa a citar o nome E o GUID do BetterFont.

    O plantio e em CODIGO (dois literais compilados no assembly), nao em comentario: um
    comentario nao cria dependencia nenhuma e nao aparece no IL - a checagem tem de pegar o
    caso que importa, que e o codigo conhecer o outro mod.
    """
    src = fonte(STYLER) if texto is None else texto
    alvo = "        private static bool _inventarioFeito;"
    novo = ('        // ModParceiro: nome e GUID do outro mod (plantio da contra-prova)\n'
            '        private const string ModParceiroNome = "BetterFont";\n'
            '        private const string ModParceiroGuid = "com.gumatos.betterfont";\n'
            '        private static bool _inventarioFeito;')
    if alvo not in src:
        return src
    return src.replace(alvo, novo, 1)


def referencia_ao_outro_mod_nos_metadados(meta):
    """TypeRef/AssemblyRef/MemberRef que citam o outro mod (vazio = zero acoplamento)."""
    achados = []
    for nome in meta["typerefs"] + meta["assemblyrefs"]:
        achados.extend(p for p in PROIBIDOS if p in nome)
    for nome, pai in meta["memberrefs"]:
        achados.extend(p for p in PROIBIDOS if p in nome or p in pai)
    return sorted(set(achados))


# ===========================================================================
# 12) SOMBRA ADAPTATIVA (BCT-2) - cor da letra -> luminancia -> balde -> hex
# ===========================================================================
#
# A ESPEC do dono (fechada em clarify, 02/10): a sombra deixa de ser FIXA e igual ao contorno
# e passa a ACOMPANHAR a cor da letra -
#
#     luminancia <  0.5  -> letra ESCURA -> sombra CLARA   (#CBB396)
#     luminancia >= 0.5  -> letra CLARA  -> sombra ESCURA  (#000000)
#
# A luminancia e a `Color.grayscale` do Unity: 0.299R + 0.587G + 0.114B. O #CBB396 e o
# specialDescColor/highlightedColor do jogo; o #000000 e o preto neutro de antes. As cores NAO
# sao digitadas aqui como fonte da verdade: o teste le a PALETA da fixture versionada
# `cores-do-jogo.entrada.json` (leitura datada do prefab 01/10) e so confere que os HEX da
# SPEC sao os que a propria paleta carrega.

FIXTURE_CORES = os.path.join("tools", "testes", "fixtures", "cores-do-jogo.entrada.json")

# BCT-4: a sombra CLARA e o BRANCO PURO. O #CBB396 (o padrao do BCT-2/BCT-3) e a PROPRIA cor de
# texto do jogo (highlightedColor/specialDescColor) e a cor comum do nome do inimigo — a sombra
# saia IGUAL a letra (contraste zero, o defeito de 02/10). Ele fica registrado como
# SOMBRA_CLARA_ANTIGA para a ISCA do teste.
SOMBRA_CLARA = "FFFFFF"          # sombra CLARA (contrasta com a letra clara; aparece no campo escuro)
SOMBRA_CLARA_ANTIGA = "CBB396"   # o DEFEITO: a propria cor da letra do inimigo
SOMBRA_ESCURA = "000000"         # preto neutro
LIMIAR_LUMINANCIA = 0.5          # Color.grayscale: < 0.5 = letra escura; >= 0.5 = letra clara
# BCT-4: diferenca MINIMA de luminancia entre a LETRA e a sombra para a sombra CONTRASTAR com ela.
# Abaixo disto as duas cores sao "a mesma cor" para o olho (a sombra vira blob/invisivel).
CONTRASTE_MINIMO = 0.2

# ---------------------------------------------------------------------------
#  BCT-3 - O FUNDO MANDA (o dono relatou 02/10: "nao ve sombra NENHUMA nos nomes
#  de inimigo"). O defeito NAO era a sombra nao ser escrita: o log de 02/10
#  (linha 3270, `sombra=on`) e a AUSENCIA do aviso `sem-underlay` provam que o
#  ramo `temUnderlay` rodou. O defeito e a COR: no BCT-2 a sombra era escolhida
#  pela luminancia da LETRA, e o nome do inimigo e uma cor CLARA (branco ou cor
#  de qualidade) -> sombra #000000. O campo de batalha do Stolen Realm e ESCURO:
#  preto sobre escuro nao aparece (contraste zero).
#
#  A regra certa para uma sombra e o CONTRASTE COM O FUNDO, nao com a letra:
#      fundo ESCURO -> sombra CLARA  (#CBB396 fica visivel sobre o campo escuro)
#      fundo CLARO  -> sombra ESCURA (#000000 fica visivel sobre fundo claro)
#      fundo NAO declarado (auto) -> a regra do BCT-2 (luminancia da LETRA)
#  A superficie dos NOMES declara `fundo: "escuro"` (o dono confirmou o campo
#  escuro); as outras superficies ficam em `auto` - nenhum efeito colateral.
# ---------------------------------------------------------------------------

FUNDO_AUTO = "auto"       # nao declarado: a sombra segue a luminancia da LETRA (BCT-2)
FUNDO_ESCURO = "escuro"   # campo de batalha escuro: a sombra visivel e a CLARA
FUNDO_CLARO = "claro"     # fundo claro: a sombra visivel e a ESCURA

FUNDOS = (FUNDO_AUTO, FUNDO_ESCURO, FUNDO_CLARO)

# A ESPEC do dono (02/10): a superficie dos NOMES de inimigo e a UNICA que declara
# fundo escuro; e ela que o dono olhou em jogo.
FUNDO_DAS_SUPERFICIES = (
    ("Nomes", "Nomes = new EstiloTmpCfg(cfg, secNomes,", FUNDO_ESCURO),
    ("EventosDado", "EventosDado = new EstiloTmpCfg(cfg, secDado,", FUNDO_AUTO),
    ("NumeroDeVida", "NumeroDeVida = new EstiloTmpCfg(cfg, secExtra", FUNDO_AUTO),
    ("TooltipStatus", "TooltipStatus = new EstiloTmpCfg(cfg, secTooltip,", FUNDO_AUTO),
)


def paleta_do_jogo():
    """A paleta do GUIManager, da fixture versionada (nunca digitada)."""
    caminho = os.path.join(arc.raiz_do_repo(), FIXTURE_CORES)
    if not os.path.isfile(caminho):
        return None
    with io.open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def luminancia(hex6):
    """A luminancia na conta EXATA da Color.grayscale do Unity: 0.299R + 0.587G + 0.114B."""
    h = (hex6 or "").lstrip("#")
    if len(h) != 6:
        raise ValueError("cor tem de ser RRGGBB, veio %r" % (hex6,))
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return 0.299 * r + 0.587 * g + 0.114 * b


def contraste_com_a_letra(hex_letra, hex_sombra):
    """BCT-4: o quanto a sombra contrasta com a LETRA (diferenca de luminancia; 0 = mesma cor)."""
    return abs(luminancia(hex_letra) - luminancia(hex_sombra))


def sombra_para(hex_letra, fundo=FUNDO_AUTO, limiar=LIMIAR_LUMINANCIA):
    """A REGRA PURA (BCT-2/BCT-3/BCT-4/BCT-5): cor -> (fundo) -> balde -> hex da sombra.

    O FUNDO PROPOE a polaridade (BCT-3): fundo ESCURO -> sombra CLARA (a escura sumiria no
    campo); fundo CLARO -> sombra ESCURA; sem fundo declarado (`auto`) vale a luminancia da
    LETRA (BCT-2: letra escura -> clara; letra clara -> escura).

    O VETO DA LETRA (BCT-5) vem em seguida: a sombra tem de ficar do LADO OPOSTO da luminancia
    da letra — fonte CLARA -> sombra ESCURA; fonte ESCURA -> sombra CLARA. Se a proposta do fundo
    puser a sombra do MESMO lado da letra, ela VIRA. Era o defeito relatado (o dono, 02/10, a
    SEGUNDA rodada): a letra CLARA #CBB396 recebia a sombra CLARA (#CBB396 do `.cfg` antigo ou o
    #FFFFFF do default do codigo) — clara sobre clara, "a sombra fica da mesma cor da fonte". O
    LIMIAR do BCT-4 (0.2) sozinho nao pegava: #CBB396 contra #FFFFFF difere so 0.283. Agora e o
    LADO que decide; a lei numerica do BCT-4 fica como rede (se a cor escolhida nao contrastar e
    a oposta contrastar mais, a oposta vence).
    """
    L = luminancia(hex_letra)
    if fundo == FUNDO_ESCURO:
        clara = True
    elif fundo == FUNDO_CLARO:
        clara = False
    else:
        clara = L < limiar
    # BCT-5 — O VETO DA LETRA: a sombra do MESMO lado da luminancia da letra VIRA.
    # (clara == True e uma sombra CLARA; a letra e CLARA quando `L >= limiar`.)
    if clara != (L < limiar):
        clara = not clara
    escolhida = SOMBRA_CLARA if clara else SOMBRA_ESCURA
    oposta = SOMBRA_ESCURA if clara else SOMBRA_CLARA
    # BCT-4 — a lei numerica (rede contra um balde mal configurado).
    if contraste_com_a_letra(hex_letra, escolhida) < CONTRASTE_MINIMO:
        if contraste_com_a_letra(hex_letra, oposta) > contraste_com_a_letra(hex_letra, escolhida):
            clara = not clara
            escolhida = SOMBRA_CLARA if clara else SOMBRA_ESCURA
    return escolhida


def balde_da_sombra(hex_letra, limiar=LIMIAR_LUMINANCIA, fundo=FUNDO_AUTO):
    """A regra pura (BCT-2/BCT-3/BCT-4) devolvendo o HEX da sombra. Ver `sombra_para`."""
    return sombra_para(hex_letra, fundo=fundo, limiar=limiar)


def sombra_regra_antiga(hex_letra, fundo=FUNDO_AUTO, limiar=LIMIAR_LUMINANCIA):
    """O DEFEITO transcrito (o BCT-3 ANTES do BCT-4): sombra clara FIXA no #CBB396, sem a lei do
    contraste. Com fundo escuro e letra #CBB396 devolve #CBB396 - a sombra IGUAL a letra (o
    defeito relatado pelo dono)."""
    if fundo == FUNDO_ESCURO:
        return SOMBRA_CLARA_ANTIGA
    if fundo == FUNDO_CLARO:
        return SOMBRA_ESCURA
    return SOMBRA_CLARA_ANTIGA if luminancia(hex_letra) < limiar else SOMBRA_ESCURA


class ModeloFundoDaSombra(object):
    """MODELO da escolha (BCT-3/BCT-4, C# -> Python).

    A POLARIDADE sai do FUNDO (BCT-3) e a cor passa pela LEI do contraste com a LETRA (BCT-4).
    Espelha o `Configuracao.UsaSombraClara`/`CorSombraAdaptativa` do C#.
    """

    def sombra(self, hex_letra, fundo=FUNDO_AUTO):
        return sombra_para(hex_letra, fundo=fundo)


class ModeloFundoDaSombraAntes(object):
    """O DEFEITO do BCT-3 ANTES do BCT-4: o #CBB396 fixo no balde claro, sem a lei do contraste.

    E o comportamento relatado pelo dono: a letra clara #CBB396 do nome do inimigo ganha sombra
    #CBB396 - a MESMA cor da letra (contraste zero, invisivel/blob).
    """

    def sombra(self, hex_letra, fundo=FUNDO_AUTO):
        return sombra_regra_antiga(hex_letra, fundo=fundo)


class ModeloFundoDaSombraIgnoraFundo(ModeloFundoDaSombra):
    """O DEFEITO do BCT-2 transcrito: a sombra ignora o fundo e olha so a LETRA.

    E o comportamento que motivou o BCT-3 - a letra clara do nome do inimigo ganha sombra
    #000000 e a sombra SOME no campo escuro.
    """

    def sombra(self, hex_letra, fundo=FUNDO_AUTO):
        return sombra_para(hex_letra, fundo=FUNDO_AUTO)


def hex_da_sombra_fixa(hex_letra, cor_fixa=SOMBRA_ESCURA):
    """A REGRA ANTIGA (o DEFEITO): a sombra ignora a luminancia e e sempre a cor fixa."""
    return cor_fixa


def tabela_de_baldes(paleta=None):
    """(nome, hex, luminancia, balde) para cada cor da paleta do GUIManager."""
    p = paleta if paleta is not None else paleta_do_jogo()
    if p is None:
        raise arc.Falhou("fixture de cores ausente: %s" % FIXTURE_CORES)
    cores = p["guimanager"]["cores"]
    linhas = []
    for nome in sorted(cores):
        hexv = cores[nome]
        linhas.append((nome, hexv, luminancia(hexv), balde_da_sombra(hexv)))
    return linhas


class ModeloEstilizadorAdaptativo(ModeloEstilizadorTmp):
    """MODELO da sombra ADAPTATIVA com REAVALIACAO SEM RE-INSTANCIAR (BCT-2, C# -> Python).

    `aplicar_com_cor(id, material, cor_letra)` e a PRIMEIRA passada: instancia o material
    (guarda por InstanceID, como o `ModeloEstilizadorTmp`), grava o balde e escreve a cor da
    sombra. `reavaliar(id, cor_letra)` e a chamada SEGUINTE (o postfix roda a cada escrita):
    rele a cor e, se o BALDE virou, escreve SO a cor da sombra - nao re-instancia (`materiais`
    continua 1) e nao toca no contorno.

    `trocas_de_sombra` conta as vezes que a cor da sombra mudou; `escritas_de_contorno` conta
    as instancias de material (tem de ser 1 no componente reusado).
    """

    def __init__(self):
        ModeloEstilizadorTmp.__init__(self)
        self.baldes = {}
        self.sombra = {}
        self.trocas_de_sombra = 0
        self.escritas_de_contorno = 0

    def aplicar_com_cor(self, id_componente, material_em_uso, cor_letra):
        resultado = self.aplicar(id_componente, material_em_uso)
        balde = balde_da_sombra(cor_letra)
        self.baldes[id_componente] = balde
        self.sombra[id_componente] = balde
        self.escritas_de_contorno += 1
        return resultado

    def reavaliar(self, id_componente, cor_letra):
        novo = balde_da_sombra(cor_letra)
        if self.baldes.get(id_componente) == novo:
            return "no-op"
        self.baldes[id_componente] = novo
        self.sombra[id_componente] = novo       # SO a cor da sombra muda
        self.trocas_de_sombra += 1
        return "trocou-sombra"


class ModeloEstilizadorAdaptativoFixo(ModeloEstilizadorAdaptativo):
    """O DEFEITO transcrito: a sombra e FIXA (sempre a escura) e ignora a luminancia.

    Toda letra ganha a sombra da PRIMEIRA cor; o reuso do componente com outra cor NAO troca
    nada - exatamente o comportamento antigo que a tarefa substitui.
    """

    def aplicar_com_cor(self, id_componente, material_em_uso, cor_letra):
        resultado = self.aplicar(id_componente, material_em_uso)
        self.baldes[id_componente] = hex_da_sombra_fixa(cor_letra)
        self.sombra[id_componente] = hex_da_sombra_fixa(cor_letra)
        self.escritas_de_contorno += 1
        return resultado

    def reavaliar(self, id_componente, cor_letra):
        return "no-op"      # a sombra fixa nunca acompanha a cor reusada


def falhas_da_sombra_adaptativa(src_cfg, src_styler):
    """A sombra ADAPTATIVA esta de pe (chaves, regra pura, leitura da cor e reavaliacao)? Vazio = ok."""
    falhas = []

    # --- 1) as TRES chaves novas, sob '1. Geral', com os defaults da ESPEC -------------------
    binds = binds_com_linha(src_cfg)
    for chave, valor in (("SombraAdaptativa", True),
                         ("CorSombraClara", SOMBRA_CLARA),
                         ("CorSombraEscura", SOMBRA_ESCURA)):
        casa = [b for b in binds if b["chave"] == chave and "1. Geral" in (b["secao"] or "")]
        if not casa:
            falhas.append("Configuracao.cs nao tem o `Bind` de '1. Geral' > %s" % chave)
        else:
            obtido = casa[0]["valor"]
            if isinstance(obtido, str) and len(obtido) >= 2 and obtido[0] == '"' and obtido[-1] == '"':
                obtido = obtido[1:-1]   # default de string vem entre aspas do fonte
            if obtido != valor:
                falhas.append("Configuracao.cs:%d - default de '%s' tem de ser %r, veio %r"
                              % (casa[0]["linha"], chave, valor, obtido))

    # --- 2) a regra PURA no C#: luminancia do Unity + limiar ---------------------------------
    if "0.299f * c.r + 0.587f * c.g + 0.114f * c.b" not in src_cfg:
        falhas.append("Configuracao.cs nao calcula a luminancia como a Color.grayscale do Unity "
                      "(0.299R + 0.587G + 0.114B): o balde sairia de outra formula")
    if "LimiarLuminancia = 0.5f" not in src_cfg:
        falhas.append("Configuracao.cs nao fixa o limiar 0.5 (o corte da paleta decidido pelo dono)")
    if "CorSombraAdaptativa(" not in src_cfg or "LetraEscura(" not in src_cfg:
        falhas.append("Configuracao.cs nao tem a escolha adaptativa (`CorSombraAdaptativa`/"
                      "`LetraEscura`): a sombra nao teria como virar de balde")

    # --- 3) a superficie TMP: LE a cor real da letra e escolhe a sombra por ela ---------------
    applicar = corpo(src_styler, APLICAR_TMP)
    if applicar is None:
        return falhas + ["nao achei `AplicarTmp` no TextStyler.cs"]
    if "tmp.color" not in applicar:
        falhas.append("`AplicarTmp` nao LE a cor real da letra (`tmp.color`): a sombra nao "
                      "teria como acompanhar a cor")
    if "CorSombraPara(tmp.color)" not in applicar:
        falhas.append("`AplicarTmp` nao escolhe a sombra PELA cor da letra "
                      "(`cfg.CorSombraPara(tmp.color)`): voltaria a sombra FIXA")
    if "_UnderlayColor" not in applicar:
        falhas.append("`AplicarTmp` nao escreve `_UnderlayColor`: nao ha cor de sombra no TMP")

    # --- 4) REAVALIACAO SEM RE-INSTANCIAR: no ramo do guarda, atualiza SO a sombra ------------
    if "ReavaliarSombraTmp(tmp, cfg, nosso)" not in applicar:
        falhas.append("`AplicarTmp` nao reavalia a sombra no ramo 'ja e o nosso material' "
                      "(`ReavaliarSombraTmp(tmp, cfg, nosso)`): um texto REUSADO ficaria com a "
                      "sombra da primeira cor")
    i_guarda = applicar.find("nosso == compartilhadoAntes")
    i_reaval = applicar.find("ReavaliarSombraTmp(tmp, cfg, nosso)")
    if i_guarda < 0 or i_reaval < 0 or i_reaval < i_guarda:
        falhas.append("a reavaliacao de `AplicarTmp` nao esta no ramo do guarda por InstanceID: "
                      "ou ela nao existe, ou roda fora do 'ja e o nosso' (re-avaliaria sempre)")

    reaval_tmp = corpo(src_styler, "private static void ReavaliarSombraTmp(")
    if reaval_tmp is None:
        falhas.append("nao achei `ReavaliarSombraTmp` no TextStyler.cs")
    else:
        if "tmp.color" not in reaval_tmp:
            falhas.append("`ReavaliarSombraTmp` nao rele a cor da letra (`tmp.color`)")
        if 'SetColor("_UnderlayColor"' not in reaval_tmp:
            falhas.append("`ReavaliarSombraTmp` nao atualiza SO `_UnderlayColor`")
        if "new Material" in reaval_tmp:
            falhas.append("`ReavaliarSombraTmp` cria material novo: a reavaliacao NAO pode "
                          "re-instanciar, so trocar a cor da sombra")
        if "BaldeSombraTmp" not in reaval_tmp:
            falhas.append("`ReavaliarSombraTmp` nao guarda/consulta o BALDE por componente: "
                          "reescreveria a sombra a cada chamada")

    # --- 5) a superficie LEGADA (UI.Text): le a cor e atualiza o Shadow.effectColor -----------
    legado = corpo(src_styler, APLICAR_LEGADO)
    if legado is None:
        return falhas + ["nao achei `AplicarTextoLegado` no TextStyler.cs"]
    if "txt.color" not in legado:
        falhas.append("`AplicarTextoLegado` nao LE a cor real do rotulo (`txt.color`)")
    if "CorSombraPara(txt.color)" not in legado:
        falhas.append("`AplicarTextoLegado` nao escolhe a sombra PELA cor do rotulo "
                      "(`cfg.CorSombraPara(txt.color)`): voltaria a sombra FIXA")
    if "ReavaliarSombraLegado(txt, cfg)" not in legado:
        falhas.append("`AplicarTextoLegado` nao reavalia a sombra no ramo 'ja tratado' "
                      "(`ReavaliarSombraLegado(txt, cfg)`): um rotulo REUSADO ficaria com a "
                      "sombra da primeira cor")

    reaval_leg = corpo(src_styler, "private static void ReavaliarSombraLegado(")
    if reaval_leg is None:
        falhas.append("nao achei `ReavaliarSombraLegado` no TextStyler.cs")
    else:
        if "txt.color" not in reaval_leg:
            falhas.append("`ReavaliarSombraLegado` nao rele a cor do rotulo (`txt.color`)")
        if "sombra.effectColor" not in reaval_leg:
            falhas.append("`ReavaliarSombraLegado` nao atualiza SO o `Shadow.effectColor`")
        if "AddComponent<Shadow>" in reaval_leg:
            falhas.append("`ReavaliarSombraLegado` re-cria o Shadow (`AddComponent<Shadow>`): a "
                          "reavaliacao NAO pode re-criar componente, so trocar a cor")
        if "BaldeSombraLegado" not in reaval_leg:
            falhas.append("`ReavaliarSombraLegado` nao guarda/consulta o BALDE por componente")

    return falhas


def defeito_sombra_fixa_ignora_luminancia(src=None):
    """PLANTA: a sombra volta a ser FIXA (a cor do contorno) e ignora a luminancia da letra.

    E a regra ANTIGA (`CorSombra => HexComAlfa(CorContornoHex.Value, AlfaSombra.Value)`): no
    TMP a escolha adaptativa vira `cfg.CorSombra`; as checagens TEM de reprovar.
    """
    texto = fonte(STYLER) if src is None else src
    alvo = "cfg.CorSombraPara(tmp.color)"
    if alvo not in texto:
        return texto
    return texto.replace(alvo, "cfg.CorSombra", 1)


def defeito_reavaliacao_ausente(src=None):
    """PLANTA: a reavaliacao sem re-instancia some (um texto reusado fica com a sombra da 1a cor)."""
    texto = fonte(STYLER) if src is None else src
    alvo = "                    ReavaliarSombraTmp(tmp, cfg, nosso);\n"
    if alvo not in texto:
        return texto
    return texto.replace(alvo, "", 1)


# ===========================================================================
# 13) SOMBRA VISIVEL - O FUNDO MANDA (BCT-3)
# ===========================================================================
# O dono relatou 02/10: "nao ve NENHUMA sombra nos nomes de inimigo". O log
# (l.3270 `sombra=on`, sem o aviso `sem-underlay`) prova que a sombra E escrita -
# o defeito e a COR: a letra do nome e CLARA e o BCT-2 escolhia a sombra pela
# LETRA -> #000000 sobre o campo ESCURO = contraste zero. A regra passa a ser o
# CONTRASTE COM O FUNDO, e a superficie dos NOMES declara `fundo: "escuro"`.

FUNDO_BIND = 'FundoTexto = cfg.Bind(sec, "Fundo", fundo,'
NOMES_BLOCO = "Nomes = new EstiloTmpCfg(cfg, secNomes,"


def argumentos_da_chamada(src, marca):
    """A FAIXA de uma CHAMADA `marca(...)` — do `(` que casa ate o `)` que o fecha.

    Os construtores de `EstiloTmpCfg`/`EstiloTextoLegadoCfg` sao chamadas com PARENTESES, nao
    blocos `{}`: o `corpo`/`bloco_de` deste modulo casa chaves e devolveria `None` (falha alta)
    numa chamada. Varredura literal-aware (a descricao de secao `" (numero de vida)"` tem
    parenteses DENTRO de um literal — sem o salto do literal, a conta fecharia no lugar errado).
    """
    i = src.find(marca)
    if i < 0:
        return None
    j = src.find("(", i)
    if j < 0:
        return None
    nivel, p = 0, j
    while p < len(src):
        c = src[p]
        if c == '"':
            p = rec.fim_do_literal(src, p)
            continue
        if c == "(":
            nivel += 1
        elif c == ")":
            nivel -= 1
            if nivel == 0:
                return src[j:p + 1]
        p += 1
    return None


def falhas_da_sombra_visivel(src_cfg, src_styler):
    """A sombra sai VISIVEL com o fundo declarado? Lista vazia = ok (BCT-3)."""
    falhas = []

    # --- 1) o FUNDO existe no C#: enum, parser e o ramo da decisao ------------------------
    for trecho, rotulo in (
            ("enum FundoSombra", "o enum `FundoSombra`"),
            ("FundoSombraDe(", "o parser do config (`FundoSombraDe`)"),
            ("UsaSombraClara(", "a decisao pela VISIBILIDADE (`UsaSombraClara`)")):
        if trecho not in src_cfg:
            falhas.append("Configuracao.cs nao tem %s: o fundo nao teria como decidir a sombra "
                          "(e a sombra continuaria invisivel no campo escuro)" % rotulo)

    decisao = corpo(src_cfg, "internal static bool UsaSombraClara(")
    if decisao is None:
        falhas.append("nao achei `UsaSombraClara` no Configuracao.cs")
    else:
        # O espaco em branco varia (indentacao/linha) - normalizo para conferir o PAR
        # rotulo->decisao, e nao so a presenca das duas metades soltas.
        plano = re.sub(r"\s+", " ", decisao)
        if "case FundoSombra.Escuro: usarClara = true;" not in plano:
            falhas.append("`UsaSombraClara` nao liga FUNDO ESCURO -> sombra CLARA (`case "
                          "FundoSombra.Escuro: usarClara = true;`): e o ramo que conserta o "
                          "defeito relatado (preto sobre escuro nao aparece)")
        if "case FundoSombra.Claro: usarClara = false;" not in plano:
            falhas.append("`UsaSombraClara` nao liga FUNDO CLARO -> sombra ESCURA (`case "
                          "FundoSombra.Claro: usarClara = false;`)")
        if "LetraEscura(" not in decisao:
            falhas.append("`UsaSombraClara` perdeu o fallback da luminancia da LETRA (o caso "
                          "`auto`, a regra do BCT-2 que vale quando o fundo nao e declarado)")

    regra = corpo(src_cfg, "internal static Color CorSombraAdaptativa(")
    if regra is None:
        falhas.append("nao achei `CorSombraAdaptativa` no Configuracao.cs")
    elif "FundoSombra fundo" not in src_cfg:
        falhas.append("`CorSombraAdaptativa` nao recebe o FUNDO: a regra nao teria como depender "
                      "dele")
    elif "UsaSombraClara(corLetra, clara, escura, fundo)" not in regra:
        falhas.append("`CorSombraAdaptativa` nao decide por "
                      "`UsaSombraClara(corLetra, clara, escura, fundo)`")

    # --- 2) as superficies DECLARAM o fundo (a chave existe e o default e o da ESPEC) -----
    construtor = corpo(src_cfg, "public EstiloTmpCfg(ConfigFile cfg, string sec,")
    if construtor is None:
        falhas.append("nao achei o construtor de `EstiloTmpCfg`")
    else:
        if FUNDO_BIND not in construtor:
            falhas.append("`EstiloTmpCfg` nao declara a chave `Fundo` (`%s`)" % FUNDO_BIND)
        if "public FundoSombra Fundo =>" not in src_cfg:
            falhas.append("`EstiloTmpCfg` nao expoe a propriedade `Fundo` (o styler nao teria "
                          "como ler o fundo declarado)")

    for nome, marca, esperado in FUNDO_DAS_SUPERFICIES:
        bloco = argumentos_da_chamada(src_cfg, marca)
        if bloco is None:
            falhas.append("nao achei a chamada de `%s` (%s) no Configuracao.cs" % (nome, marca))
            continue
        esperado_arg = 'fundo: "%s"' % esperado
        if esperado_arg not in bloco:
            falhas.append("`%s` nao declara `%s`: com o fundo errado a sombra sai invisivel (ou "
                          "muda o que o dono ja aprovou nas outras superficies)" % (nome, esperado_arg))

    # --- 3) o STYLER le o fundo (nos DOIS caminhos e na reavaliacao) -----------------------
    applicar = corpo(src_styler, APLICAR_TMP)
    if applicar is None:
        falhas.append("nao achei `AplicarTmp` no TextStyler.cs")
    else:
        if "UsaSombraClara(tmp.color, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura, cfg.Fundo)" not in applicar:
            falhas.append("`AplicarTmp` nao escolhe o balde da sombra pelo FUNDO e pelas DUAS "
                          "cores (`UsaSombraClara(tmp.color, Plugin.Cfg.CorSombraClara, "
                          "Plugin.Cfg.CorSombraEscura, cfg.Fundo)`): a sombra voltaria a ser "
                          "escolhida so pela letra e sem a lei do contraste")

    reaval_tmp = corpo(src_styler, "private static void ReavaliarSombraTmp(")
    if reaval_tmp is None:
        falhas.append("nao achei `ReavaliarSombraTmp` no TextStyler.cs")
    elif "UsaSombraClara(tmp.color, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura, cfg.Fundo)" not in reaval_tmp:
        falhas.append("`ReavaliarSombraTmp` nao usa o FUNDO+cores no balde: um texto reusado "
                      "poderia trocar de sombra por causa da letra mesmo com o fundo declarado")

    legado = corpo(src_styler, APLICAR_LEGADO)
    if legado is None:
        falhas.append("nao achei `AplicarTextoLegado` no TextStyler.cs")
    elif "UsaSombraClara(txt.color, Plugin.Cfg.CorSombraClara, Plugin.Cfg.CorSombraEscura, cfg.Fundo)" not in legado:
        falhas.append("`AplicarTextoLegado` nao escolhe o balde da sombra pelo FUNDO+cores")
    return falhas


def defeito_nomes_fundo_auto(src=None):
    """PLANTA: a superficie dos NOMES volta a nao declarar o fundo (o defeito do BCT-2)."""
    texto = fonte(CFG) if src is None else src
    alvo = 'fundo: "escuro");'
    if alvo not in texto:
        return texto
    return texto.replace(alvo, 'fundo: "auto");', 1)


def defeito_sombra_ignora_fundo(src=None):
    """PLANTA: `UsaSombraClara` deixa de ligar FUNDO ESCURO a sombra clara (a regra do BCT-2 volta)."""
    texto = fonte(CFG) if src is None else src
    alvo = "                    usarClara = true;      // BCT-3: fundo escuro -> sombra CLARA"
    if alvo not in texto:
        return texto
    return texto.replace(
        alvo, "                    usarClara = false;     // DEFEITO: fundo escuro -> sombra ESCURA", 1)


# ===========================================================================
# 14) CONTRASTE COM A LETRA - A LEI (BCT-4) e a POLARIDADE PELA FONTE (BCT-5)
# ===========================================================================
# O defeito relatado em 02/10 (a SEGUNDA rodada): o nome do inimigo tem a letra CLARA e ela e o
# #CBB396 (highlightedColor). O BCT-3 dava a essa letra a sombra CLARA #CBB396 - a MESMA cor da
# letra. A sombra existe e nao contrasta (invisivel, ou um blob). A lei: a sombra tem de
# CONTRASTAR COM A LETRA (diferenca de luminancia >= `ContrasteMinimo`); se a cor do balde
# escolhido nao contrastar, o balde VIRA. A sombra clara passa a ser o BRANCO (#FFFFFF).
#
# BCT-5 (a TERCEIRA rodada, o dono: "a sombra fica na mesma cor da fonte"): o LIMIAR do BCT-4
# nao bastava — bege #CBB396 contra branco #FFFFFF difere so 0.283 (>= 0.2, "passava") e a letra
# CLARA ganhava a sombra CLARA. Fora isso, o `.cfg` do perfil herdou `CorSombraClara = CBB396`
# (a PROPRIA cor da fonte): o BepInEx nao reescreve chave existente, entao o default novo do
# BCT-4 nunca chegou a instalacao. A REGRA passa a decidir pelo LADO: fonte CLARA -> sombra
# ESCURA; fonte ESCURA -> sombra CLARA; o FUNDO so PROPOE e leva o VETO DA LETRA. E o alfa dos
# NOMES sobe (>= `ALFA_SOMBRA_MINIMA`) para a sombra escura ser VISIVEL.


def falhas_do_contraste_da_letra(src_cfg, src_styler):
    """A LEI do BCT-4 esta de pe (constante, guarda no C# e o styler medindo)? Vazio = ok."""
    falhas = []

    # --- 1) a constante e o medidor do contraste -------------------------------------------
    if "ContrasteMinimo" not in src_cfg:
        falhas.append("Configuracao.cs nao tem a constante `ContrasteMinimo`: a lei 'a sombra "
                      "contrasta com a LETRA' ficaria sem limiar")
    if "ContrasteComALetra(" not in src_cfg:
        falhas.append("Configuracao.cs nao tem `ContrasteComALetra` (o medidor de contraste entre "
                      "a sombra e a LETRA)")

    # --- 2) a guarda VIRA o balde quando a cor escolhida nao contrasta com a letra -----------
    decisao = corpo(src_cfg, "internal static bool UsaSombraClara(")
    if decisao is None:
        falhas.append("nao achei `UsaSombraClara` no Configuracao.cs")
    else:
        if "ContrasteComALetra(corLetra, escolhida)" not in decisao:
            falhas.append("`UsaSombraClara` nao mede o contraste entre a LETRA e a cor "
                          "ESCOLHIDA (`ContrasteComALetra(corLetra, escolhida)`): a lei do "
                          "contraste nao teria como reprovar a sombra da propria cor da letra")
        if "usarClara = !usarClara;" not in decisao:
            falhas.append("`UsaSombraClara` nao VIRA o balde quando a cor escolhida nao contrasta "
                          "com a LETRA: a letra #CBB396 em fundo escuro continuaria ganhando sombra "
                          "#CBB396 (a MESMA cor - o defeito relatado)")
        # BCT-5: o VETO DA LETRA (o LADO da luminancia decide) - sem ele a letra CLARA ganha
        # sombra CLARA (#FFFFFF), que sobre o bege do glifo e "a mesma cor (clara) da fonte".
        if "usarClara != LetraEscura(corLetra)" not in decisao:
            falhas.append("`UsaSombraClara` perdeu o VETO DA LETRA (BCT-5): a sombra pode ficar do "
                          "MESMO lado da luminancia da FONTE (clara-sobre-clara) - e o defeito 'a "
                          "sombra fica da mesma cor da fonte'")
        if "< ContrasteMinimo" not in decisao:
            falhas.append("`UsaSombraClara` nao compara o contraste com `ContrasteMinimo`: o "
                          "limiar ficaria solto")
        # a decisao precisa das DUAS cores para medir o contraste (a assinatura e fora do corpo).
        if "UsaSombraClara(Color corLetra, Color clara, Color escura, FundoSombra fundo)" not in src_cfg:
            falhas.append("`UsaSombraClara` nao recebe as DUAS cores (`Color clara`/`Color "
                          "escura`): nao teria como medir o contraste com a letra")

    # --- 3) a sombra CLARA corrigida (o branco), nao o #CBB396 (a cor da propria letra) -------
    if '"CorSombraClara", "%s"' % SOMBRA_CLARA not in src_cfg:
        falhas.append("o default de `CorSombraClara` nao e o branco #%s: com o #%s (a PROPRIA cor "
                      "da letra do inimigo) a sombra clara volta a ficar igual a letra"
                      % (SOMBRA_CLARA, SOMBRA_CLARA_ANTIGA))

    # --- 4) o styler mede o contraste nos DOIS caminhos e na reavaliacao ---------------------
    for trecho, rotulo in (("UsaSombraClara(tmp.color, Plugin.Cfg.CorSombraClara, "
                            "Plugin.Cfg.CorSombraEscura, cfg.Fundo)", "AplicarTmp"),
                           ("CorSombraPara(tmp.color)", "AplicarTmp (a cor escrita)")):
        applicar = corpo(src_styler, APLICAR_TMP)
        if applicar is None:
            falhas.append("nao achei `AplicarTmp` no TextStyler.cs")
            break
        if trecho not in applicar:
            falhas.append("`%s` nao usa `%s`: a sombra nao sairia pela lei do contraste"
                          % (rotulo, trecho))
    return falhas


def defeito_letra_clara_sombra_clara(src=None):
    """PLANTA: some o VETO DA LETRA (BCT-5) - a proposta do FUNDO vale sempre.

    E o defeito relatado pelo dono: a letra CLARA do nome do inimigo (#CBB396, luminancia 0.717)
    em fundo escuro ganha a sombra CLARA #FFFFFF (o default do codigo) - clara sobre clara, "a
    sombra fica da mesma cor da fonte". Sem o veto, `usarClara` fica `true` (fundo escuro) e o
    limiar de 0.2 do BCT-4 nao pega #CBB396 x #FFFFFF (difere 0.283).
    """
    texto = fonte(CFG) if src is None else src
    alvo = ("            if (usarClara != LetraEscura(corLetra))\n"
            "            {\n"
            "                usarClara = !usarClara;\n"
            "            }\n")
    if alvo not in texto:
        return texto
    return texto.replace(
        alvo, "            // DEFEITO plantado: SEM o veto da letra (a sombra pode ficar do mesmo lado da fonte)\n", 1)


# O nome antigo do MESMO plantio (a guarda que faltava virou o VETO DA LETRA no BCT-5).
defeito_sombra_sem_contraste_com_a_letra = defeito_letra_clara_sombra_clara


# BCT-5 — a sombra dos NOMES tem de ter ALFA suficiente para ser VISIVEL. A 0.35 ela ficava
# translucida demais sobre o glifo e se confundia com a propria fonte ("mesma cor da fonte").
ALFA_SOMBRA_MINIMA = 0.5


def falhas_da_visibilidade(src_cfg):
    """A sombra dos NOMES e VISIVEL (alfa suficiente)? Lista vazia = ok (BCT-5)."""
    falhas = []
    bloco = argumentos_da_chamada(src_cfg, NOMES_BLOCO)
    if bloco is None:
        return ["nao achei a chamada de `Nomes` (%s) no Configuracao.cs" % NOMES_BLOCO]
    m = re.search(r"alfaSombra:\s*([\d.]+)f", bloco)
    if m is None:
        return ["`Nomes` nao declara `alfaSombra`: sem alfa a sombra fica invisivel"]
    alfa = float(m.group(1))
    if alfa < ALFA_SOMBRA_MINIMA:
        falhas.append("Configuracao.cs - o `alfaSombra` dos NOMES e %.2f: abaixo de %.2f a sombra "
                      "escura fica translucida demais e se confunde com o proprio glifo (o "
                      "'sombra da mesma cor da fonte')" % (alfa, ALFA_SOMBRA_MINIMA))
    return falhas


def defeito_alfa_sombra_baixo(src=None):
    """PLANTA: o alfa da sombra dos NOMES volta a 0.35 (fraca demais para se ver)."""
    texto = fonte(CFG) if src is None else src
    bloco = argumentos_da_chamada(texto, NOMES_BLOCO)
    if bloco is None:
        return texto
    m = re.search(r"alfaSombra:\s*[\d.]+f", bloco)
    if m is None:
        return texto
    novo = "alfaSombra: 0.35f"
    return texto.replace(m.group(0), novo, 1)


def defeito_cor_sombra_clara_volta_cbb396(src=None):
    """PLANTA: a sombra clara volta ao #CBB396 (a PROPRIA cor da letra do inimigo)."""
    texto = fonte(CFG) if src is None else src
    alvo = '"CorSombraClara", "%s",' % SOMBRA_CLARA
    if alvo not in texto:
        return texto
    return texto.replace(alvo, '"CorSombraClara", "%s",' % SOMBRA_CLARA_ANTIGA, 1)


# ===========================================================================
# 15) O BCT NAO VAZA PARA A JANELA DO LEVEL-UP (R2)
# ===========================================================================
# O dono relatou 02/10: o rotulo de secao da janela de level-up ("Select Attributes",
# `RoguelikeManager.SectionLabelText`, decompilado l.168605) ficou com "sombra muito grossa".
# A investigacao (prefab + log + codigo) fechou:
#   * O BCT NAO patcheia `RoguelikeManager` nem toca no `SectionLabelText`: as superficies dele
#     sao 7 metodos de 7 tipos (nome de inimigo, rotulos de status, texto do dado, tooltip,
#     numero de vida) - nada ali. Ele escreve SEMPRE no material POR COMPONENTE (getter
#     `fontMaterial`), entao nao ha caminho para alcancar outro texto.
#   * A sombra do 'Select Attributes' vem do BETTERFONT (outro mod), nao do BCT: o material do
#     prefab ('Regular Font (Minion Pro Regular) SDF Material') traz `_UnderlayColor` preto alfa
#     0.5 com o keyword UNDERLAY_ON DESLIGADO (sombra INERTE - offset/dilate/softness 0). O
#     BetterFont decide "sombra em uso" por `_UnderlayColor.a > 0.001` (sem olhar o keyword) e
#     LIGA o UNDERLAY_ON ao transportar o estilo: a sombra que o jogo nunca desenhava passa a
#     aparecer. (O `AcceptButtonText` do mesmo prefab expoe o mesmo padrao com o "Title Font".)
# Esta secao e a TRAVA do lado do BCT: o mod nao pode ganhar gancho (nem citar) a janela do
# level-up.

# As 7 superficies REAIS do BCT, lidas dos `[HarmonyPatch]` de Patches.cs (controle positivo).
SUPERFICIES_DO_BCT = ("BossHealthbar", "PlayerInfoWindow", "StatusIcon", "DiceRollingManager",
                      "DiceRoller", "Tooltip", "Healthbar")

# Os tipos da JANELA DO LEVEL-UP. Se algum aparecer nos ganchos ou no fonte do BCT, o mod esta
# vazando para uma tela que NAO e alvo (o `RoguelikeManager` e quem escreve o SectionLabelText).
TIPOS_DO_LEVELUP = ("RoguelikeManager", "SectionLabelText", "LevelUpStage", "SkillSelectWindow")

RE_PATCH_TIPO = re.compile(r"\[HarmonyPatch\s*\(\s*typeof\s*\(\s*([A-Za-z_]\w*)")


def tipos_dos_ganchos(src_patches):
    """Os TIPOS do jogo que o BCT patcheia, lidos dos `[HarmonyPatch(typeof(X), ...)]`."""
    return sorted(set(RE_PATCH_TIPO.findall(src_patches)))


class ModeloDeAlcanceDoBct(object):
    """MODELO do ALCANCE do mod: ele so estiliza os tipos que patcheia.

    `toca(tipo)` responde o que o C# responde - so os tipos com gancho recebem `AplicarTmp`.
    `RoguelikeManager` (o dono da janela do level-up) NAO esta entre eles.
    """

    def __init__(self, tipos):
        self.tipos = set(tipos)

    def toca(self, tipo):
        return tipo in self.tipos


def falhas_do_vazamento_no_levelup(src_patches, fontes):
    """O BCT fica nas 7 superficies e NAO cita a janela do level-up? Vazio = ok."""
    falhas = []
    tipos = tipos_dos_ganchos(src_patches)
    if not tipos:
        falhas.append("nao achei nenhum `[HarmonyPatch(typeof(...))]` em Patches.cs: o leitor de "
                      "tipos nao esta lendo (uma ausencia de vazamento assim nao provaria nada)")
    faltando = [t for t in SUPERFICIES_DO_BCT if t not in tipos]
    if faltando:
        falhas.append("o leitor de ganchos nao achou superficie(s) que o mod TEM (%s): o controle "
                      "positivo falhou" % ", ".join(faltando))
    vazou = [t for t in tipos if t in TIPOS_DO_LEVELUP]
    if vazou:
        falhas.append("o BCT ganhou gancho na JANELA DO LEVEL-UP (%s): ela NAO e alvo do mod - o "
                      "'Select Attributes' (SectionLabelText) sairia estilizado pelo BCT"
                      % ", ".join(vazou))
    for nome in sorted(fontes):
        texto = fontes[nome]
        citados = [t for t in TIPOS_DO_LEVELUP if t in texto]
        if citados:
            falhas.append("o fonte %s cita a janela do level-up (%s): o BCT nao pode conhecer essa "
                          "tela" % (nome, ", ".join(citados)))
    return falhas


def defeito_gancho_no_levelup(src=None):
    """PLANTA: o BCT ganha um gancho na janela do level-up (o vazamento que esta secao proibe)."""
    texto = fonte(PATCHES) if src is None else src
    alvo = '    [HarmonyPatch(typeof(BossHealthbar), "set_BossCharacter")]'
    novo = ('    [HarmonyPatch(typeof(RoguelikeManager), "OpenSkillSelectWindow")]\n'
            '    internal static class PatchVazamentoLevelUp\n'
            '    {\n'
            '        private static void Postfix(RoguelikeManager __instance)\n'
            '        {\n'
            '        }\n'
            '    }\n\n' + alvo)
    if alvo not in texto:
        return texto
    return texto.replace(alvo, novo, 1)


# ===========================================================================
#  CLI: a leitura de IL sozinha (a prova exigida, na mao)
# ===========================================================================

def _relatar(dados, rotulo):
    meta = ler_metadados(dados)
    print("DLL      : %s" % rotulo)
    print("sha256   : %s (%d bytes)" % (meta["sha256"], meta["tamanho"]))
    print("tabelas  : %s" % ", ".join("%s=%d" % (k, v) for k, v in sorted(meta["linhas"].items())))
    print("MemberRef: %d linhas" % len(meta["memberrefs"]))
    print("AssemblyRef: %s" % ", ".join(meta["assemblyrefs"]))
    setters = setters_de_material_em(meta)
    print("REFERENCIAS a SETTER de material: %s" % (", ".join(setters) if setters else "NENHUMA"))
    for alvo in ("get_fontSharedMaterial", "get_fontMaterial", "set_fontSharedMaterial"):
        print("  %-24s entre as referencias? %s" % (alvo, alvo in meta["nomes_de_membros"]))
    print("-- checagens --")
    falhas = falhas_dos_metadados(meta)
    print("  falhas: %s" % (falhas or "nenhuma"))
    mutado = il_com_o_setter_do_compartilhado(dados)
    print("-- contra-prova (o defeito plantado no IL) --")
    if mutado == dados:
        print("  NAO deu para plantar (a referencia de leitura nao esta la)")
    else:
        m2 = ler_metadados(mutado)
        print("  com o setter plantado: %s" % (setters_de_material_em(m2) or "??"))
    return 1 if falhas else 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with io.open(sys.argv[1], "rb") as fh:
            sys.exit(_relatar(fh.read(), sys.argv[1]))
    origem, dados = dll_do_pacote()
    if dados is None:
        print("nenhuma DLL do BCT encontrada (dist/gumatos-BetterCombatText-*.zip ou bin/)")
        sys.exit(2)
    sys.exit(_relatar(dados, origem))
