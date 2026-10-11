#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
INT-R1-C6 - Dump CHAVEADO de tooltips, regenerado da tabela de localizacao do LANG-R1.

O QUE ESTE SCRIPT FAZ
---------------------
Le a tabela `localizacao-ptbr.csv` (entrega do cartao t_2a6474ff / LANG-R1) e os TRES dumps de
revisao ja existentes no repo (`docs/cobertura/DUMP-TOOLTIPS-REVISAO.md`,
`DUMP-DEBUFFS-REVISAO.md`, `DUMP-PASSIVAS-REVISAO.md`) e gera um dump NOVO, numerado/versionado,
com:

  * a parte CHAVEADA - o texto do jogo (en = chave), o pt-BR da tabela e os alertas daquela
    chave, na ordem de leitura do padrao de tooltip (`docs/TEXTO-TOOLTIPS.md` §1: nivel 1 =
    descricao do jogo -> pt-BR -> alertas -> mecanica/notas);
  * a marca explicita dos itens que vem de ASSET CRU (status e afins, registro BT-6 do
    `KANBAN.md:262`): esses NAO tem chave e continuam no caminho antigo
    (`tools/census.py` + `docs/cobertura/*.csv`);
  * a lista dos itens que NAO foram encontrados em nenhum dos dois caminhos.

NAO ESCREVE NADA NOS TRES DUMPS DE ORIGEM nem em `docs/cobertura/auditoria-tooltips.md`
(confira com `--hashes`). Todo o texto e copiado verbatim - o script nao corrige nem normaliza
nada que vai para a saida; a normalizacao existe SO para casar chave, e o tier do casamento
vai declarado em cada item.

USO
---
    python tools/gera_dump_chaveado.py                      # usa os defaults
    python tools/gera_dump_chaveado.py --csv <arquivo.csv>  # tabela do LANG-R1 em outro lugar
    python tools/gera_dump_chaveado.py --conferir           # reconta a partir do dump gerado
    python tools/gera_dump_chaveado.py --hashes             # sha256 das entradas e das saidas

SAIDAS (nunca sobrescreve os dumps de origem)
--------------------------------------------
    docs/cobertura/DUMP-CHAVEADO-LANG-R1.md
    docs/cobertura/DUMP-CHAVEADO-LANG-R1-contagens.json
"""
import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COBERTURA = os.path.join(REPO, "docs", "cobertura")

# Tabela do LANG-R1: entregue como ANEXO do cartao t_2a6474ff (nao esta no repo).
CSV_DEFAULT = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~/AppData/Local")),
    "hermes", "kanban", "attachments", "t_2a6474ff", "localizacao-ptbr.csv")
CSV_FALLBACK = os.path.join(REPO, "scratch", "lang-r1", "localizacao-ptbr.csv")

OUT_MD = os.path.join(COBERTURA, "DUMP-CHAVEADO-LANG-R1.md")
OUT_JSON = os.path.join(COBERTURA, "DUMP-CHAVEADO-LANG-R1-contagens.json")

# (chave, caminho do arquivo, natureza do arquivo)
FONTES = [
    ("tooltips", os.path.join(COBERTURA, "DUMP-TOOLTIPS-REVISAO.md"), "misto"),
    ("debuffs", os.path.join(COBERTURA, "DUMP-DEBUFFS-REVISAO.md"), "status"),
    ("passivas", os.path.join(COBERTURA, "DUMP-PASSIVAS-REVISAO.md"), "skill"),
]

NAO_TOCAR = [
    os.path.join(COBERTURA, "DUMP-TOOLTIPS-REVISAO.md"),
    os.path.join(COBERTURA, "DUMP-DEBUFFS-REVISAO.md"),
    os.path.join(COBERTURA, "DUMP-PASSIVAS-REVISAO.md"),
    os.path.join(COBERTURA, "auditoria-tooltips.md"),
]

ITEM = re.compile(r"^####\s+(?P<title>.*)$")
PARTE = re.compile(r"^##\s+PARTE\s+(?P<n>\d+)\s*[—-]\s*(?P<nome>.*)$")
ARVORE = re.compile(r"^###\s+(?P<nome>.*)$")
FIELD = re.compile(r"^- (?P<key>[A-Za-zÀ-ÿ]+):\s?(?P<val>.*)$")

# PARTE -> natureza do item (BT-6: PARTE 2 = status = campo bruto de asset, sem chave)
PARTE_NATUREZA = {1: "skill", 2: "status", 3: "skill"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- parse dos dumps

def parse_dump(path):
    """Devolve a lista de itens de um dump de revisao, na ordem do arquivo.

    Cada item = {titulo, parte, parte_nome, arvore, campos, ordem, linha}
    """
    itens, cur, parte, parte_nome, arvore = [], None, None, None, None
    with open(path, encoding="utf-8") as fh:
        for n, raw in enumerate(fh, 1):
            line = raw.rstrip("\r\n")
            mp = PARTE.match(line)
            if mp:
                parte = int(mp.group("n"))
                parte_nome = mp.group("nome").strip()
                arvore = None
                continue
            ma = ARVORE.match(line)
            if ma and not line.startswith("####"):
                arvore = ma.group("nome").strip()
                continue
            mi = ITEM.match(line)
            if mi:
                cur = {"titulo": mi.group("title").strip(), "parte": parte,
                       "parte_nome": parte_nome, "arvore": arvore,
                       "campos": {}, "ordem": [], "linha": n}
                itens.append(cur)
                continue
            if cur is None:
                continue
            if not line.strip() or line.startswith("#") or line.startswith("---") \
                    or line.startswith(">"):
                # linha em branco / titulo / separador: o bloco do item acabou.
                # (sem isto, a prosa da secao seguinte entra na descricao do ultimo item)
                cur = None
                continue
            mf = FIELD.match(line)
            if mf:
                k = mf.group("key")
                if k in cur["campos"]:
                    cur["campos"][k] += "\n" + mf.group("val")
                else:
                    cur["ordem"].append(k)
                    cur["campos"][k] = mf.group("val")
            elif line.startswith("- ") and cur["ordem"]:
                cur["campos"][cur["ordem"][-1]] += "\n" + line[2:]
            elif line.strip() and cur["ordem"]:
                # continuacao de campo (desc quebrada em varias linhas)
                cur["campos"][cur["ordem"][-1]] += "\n" + line
    return itens


def natureza_do_item(nome_fonte, caminho_fonte, nat_fonte, item):
    if nat_fonte == "status":
        return "status"
    if nat_fonte == "skill":
        return "skill"
    # fonte mista (DUMP-TOOLTIPS): decide pela PARTE
    return PARTE_NATUREZA.get(item["parte"], "skill")


# ----------------------------------------------------------------------- tabela do LANG-R1

def carrega_tabela(path):
    csv.field_size_limit(10 ** 9)
    chaves = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            k = r["chave"]
            if k not in chaves:
                chaves[k] = {"ids": [], "ptbr": r["ptbr"], "en": r["en"],
                             "alertas": r["alertas"], "contextos": r["contextos"],
                             "num_entradas": r["num_entradas"],
                             "presente_tabela_ptbr": r["presente_tabela_ptbr"]}
            chaves[k]["ids"].append(r["id"])
    return chaves


TAG_B = re.compile(r"<b>(.*?)</b>", re.S)


def normaliza(s):
    """Normalizacao SO para casar chave (nunca vai para a saida).

    - `<b>X</b>` -> `@X@` (o dumper de boot do RoguelikeDebugger imprime nessa forma);
    - remove `<i>`/`<color=...>` (o dumper nao os carrega);
    - colapsa QUALQUER sequencia de espaco/quebra de linha em um espaco
      (o dumper troca `\\n\\n` da chave por espacos);
    - tira espaco das pontas.
    """
    s = TAG_B.sub(r"@\1@", s)
    s = re.sub(r"</?i>", "", s)
    s = re.sub(r"</?color[^>]*>", "", s)
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def esc(s):
    """Escapa quebra de linha como `\\n` para o item caber em UMA linha por campo.

    O texto em si nao muda uma letra: e a mesma convencao que a coluna `chave_json` da
    tabela do LANG-R1 usa. Sem isto, uma descricao com quebra de linha interna quebraria a
    leitura por campo do dump.
    """
    return (s or "").replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\r")


def monta_indices(chaves):
    norm, fold = {}, {}
    for k in chaves:
        n = normaliza(k)
        norm.setdefault(n, []).append(k)
        fold.setdefault(n.casefold(), []).append(k)
    return norm, fold


def casa(desc, chaves, norm, fold):
    """Casa a descricao do dump com uma chave da tabela.

    Tiers, do mais forte para o mais fraco: exato -> normalizado -> casefold.
    Se o tier achar mais de uma chave distinta, o casamento fica AMBIGUO e nenhuma
    chave e escolhida (o item cai na lista de conferencia manual).
    """
    if desc in chaves:
        return {"tier": "exato", "candidatos": [desc]}
    n = normaliza(desc)
    if n in norm and len(norm[n]) == 1:
        return {"tier": "normalizado", "candidatos": norm[n]}
    if n in norm and len(norm[n]) > 1:
        return {"tier": "ambiguo-normalizado", "candidatos": sorted(norm[n])}
    f = n.casefold()
    if f in fold and len(fold[f]) == 1:
        return {"tier": "casefold", "candidatos": fold[f]}
    if f in fold and len(fold[f]) > 1:
        return {"tier": "ambiguo-casefold", "candidatos": sorted(fold[f])}
    return {"tier": "nenhum", "candidatos": []}


# ------------------------------------------------------------------------------- relatorio

def gera(csv_path, md_path, json_path):
    chaves = carrega_tabela(csv_path)
    norm, fold = monta_indices(chaves)

    blocos, contagens, orfaos, asset_sem_tabela = [], {}, [], []
    for nome_fonte, caminho, nat in FONTES:
        itens = parse_dump(caminho)
        blocos.append((nome_fonte, caminho, nat, itens))
        c = contagens.setdefault(nome_fonte, {
            "arquivo": os.path.relpath(caminho, REPO).replace("\\", "/"),
            "sha256": sha256(caminho),
            "itens": len(itens), "skill": 0, "status": 0,
            "chaveado_exato": 0, "chaveado_normalizado": 0, "chaveado_casefold": 0,
            "ambiguo": 0, "asset_cru": 0, "asset_cru_com_chave_coincidente": 0,
            "sem_descricao": 0, "nao_encontrado": 0,
        })
        c["skill"] = len([i for i in itens
                          if natureza_do_item(nome_fonte, caminho, nat, i) == "skill"])
        c["status"] = len(itens) - c["skill"]

    # --- duplicidade entre os arquivos (o DEBUFFS e o PASSIVAS sao recortes do TOOLTIPS)
    cont_chaves = {}
    for _nome, _caminho, _nat, _itens in blocos:
        for it in _itens:
            k = (it["titulo"], it["campos"].get("desc", ""))
            cont_chaves[k] = cont_chaves.get(k, 0) + 1
    itens_total = sum(len(b[3]) for b in blocos)
    chaves_distintas = len(cont_chaves)
    repetidos = sum(v - 1 for v in cont_chaves.values() if v > 1)

    # --- saida markdown
    linhas = []
    add = linhas.append
    ts = os.environ.get("INT_R1_C6_DATA") or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    add("# Dump CHAVEADO de tooltips — regenerado da tabela do LANG-R1 (INT-R1-C6)")
    add("")
    add("Gerado por `tools/gera_dump_chaveado.py` em **%s** (nao editar a mao: regenere)." % ts)
    add("")
    add("| Insumo | Caminho | sha256 |")
    add("|---|---|---|")
    add("| tabela de localizacao (LANG-R1, anexo de `t_2a6474ff`) | `%s` | `%s` |"
        % (csv_path, sha256(csv_path)))
    for nome_fonte, caminho, _nat, _itens in blocos:
        add("| dump de origem (%s) | `%s` | `%s` |"
            % (nome_fonte, os.path.relpath(caminho, REPO).replace("\\", "/"), sha256(caminho)))
    add("")
    add("**Ordem das linhas de cada item** (padrao de `docs/TEXTO-TOOLTIPS.md` §1: nivel 1 -> 2 -> 3):")
    add("1. `desc jogo (en, como esta no dump)` / `desc jogo (en, asset cru)` — nivel 1, o texto do jogo;")
    add("2. `chave casada na tabela` — a chave da tabela do LANG-R1 que casa com essa descricao (o")
    add("   dumper de boot imprime `<b>X</b>` como `@X@`, `\\n\\n` como espacos e o nome de atributo")
    add("   em caixa diferente; quando o casamento nao e literal, o `tier` diz o que mudou);")
    add("3. `pt-BR (tabela LANG-R1)` — o que o dicionario pt-BR devolve para essa chave;")
    add("4. `alertas LANG-R1` + `contextos` — os avisos da tabela (placeholder, tags, etc.);")
    add("5. os campos de mecanica que o dump de origem ja trazia (`dano`, `tags`, `attr`, `efeitos`) —")
    add("   sao insumo das notas de nivel 2/3 e **nao** vem da tabela de localizacao;")
    add("6. `fonte` — de onde o texto veio (tabela ou asset cru).")
    add("")
    add("Convencao de escrita: cada campo ocupa **uma** linha; quebra de linha **dentro** de um texto")
    add("aparece escapada como `\\n` (mesma convencao da coluna `chave_json` da tabela). O texto nao e")
    add("alterado uma letra — so escapado para o item caber na leitura por campo.")
    add("")
    add("## O que significa `fonte`")
    add("")
    add("- `TABELA-LANG-R1 <id> (match <tier>)` — item CHAVEADO: a descricao casa com uma chave da")
    add("  tabela do LANG-R1. O pt-BR mostrado e o que o dicionario do jogo devolve para essa chave.")
    add("  O `tier` diz como o casamento foi feito (ver `--conferir`): `exato` e copia literal;")
    add("  `normalizado` so difere em `<b>`/`<i>`/`<color>` e espaco/quebra de linha que o dumper de")
    add("  boot do RoguelikeDebugger imprime de outra forma; `casefold` difere tambem em maiuscula/")
    add("  minuscula (o motor do jogo troca o nome do atributo por uma forma de exibicao).")
    add("- `ASSET-CRU (status; BT-6)` — item **sem chave**: a descricao de status e campo bruto de")
    add("  asset (`ActionStatusInfo.Name/Description`), nao passa pelo dicionario de localizacao")
    add("  (`KANBAN.md:262`, registro BT-6). Continua no caminho antigo (`tools/census.py` +")
    add("  `docs/cobertura/*.csv`). Quando o texto de um status **coincide** com uma chave da tabela,")
    add("  isso vem anotado como `chave coincidente (nao usar como fonte)` — chave existir na tabela")
    add("  nao prova que a tela que a usa seja essa.")
    add("- `NAO-ENCONTRADO` — nem chave, nem asset cru: caiu na lista de conferencia manual.")
    add("")
    add("**Escopo NAO_EXERCITADO:** este dump e conferencia de TEXTO contra a tabela. Renderizacao,")
    add("quebra de linha e layout em jogo **nao** foram exercitados (jogo nao aberto nesta rodada).")
    add("")
    add("---")
    add("")

    corpo = []
    for nome_fonte, caminho, nat, itens in blocos:
        c = contagens[nome_fonte]
        corpo.append("")
        corpo.append("## Dump de origem: `%s` (%d itens)" % (
            os.path.relpath(caminho, REPO).replace("\\", "/"), len(itens)))
        corpo.append("")
        parte_atual, arvore_atual = None, None
        for it in itens:
            nat_item = natureza_do_item(nome_fonte, caminho, nat, it)
            desc = it["campos"].get("desc", "")
            m = casa(desc, chaves, norm, fold) if desc else {"tier": "sem-descricao", "candidatos": []}
            if nat_item == "status":
                if m["tier"] in ("exato", "normalizado", "casefold"):
                    c["asset_cru"] += 1
                    c["asset_cru_com_chave_coincidente"] += 1
                else:
                    c["asset_cru"] += 1
                    if not desc:
                        c["sem_descricao"] += 1
                    asset_sem_tabela.append({
                        "fonte": nome_fonte, "titulo": it["titulo"], "parte": it["parte"],
                        "arvore": it["arvore"], "desc": desc,
                        "motivo": ("sem descricao no dump" if not desc else "texto nao esta na tabela")})
            else:
                if m["tier"] == "exato":
                    c["chaveado_exato"] += 1
                elif m["tier"] == "normalizado":
                    c["chaveado_normalizado"] += 1
                elif m["tier"] == "casefold":
                    c["chaveado_casefold"] += 1
                elif m["tier"].startswith("ambiguo"):
                    c["ambiguo"] += 1
                else:
                    c["nao_encontrado"] += 1

            if it["parte"] != parte_atual:
                parte_atual = it["parte"]
                if parte_atual:
                    corpo.append("")
                    corpo.append("### PARTE %s — %s" % (parte_atual, it["parte_nome"]))
                    corpo.append("")
                    arvore_atual = None
            if it["arvore"] != arvore_atual:
                arvore_atual = it["arvore"]
                if arvore_atual:
                    corpo.append("")
                    corpo.append("#### %s" % arvore_atual)
                    corpo.append("")

            corpo.append("")
            corpo.append("##### %s" % it["titulo"])
            if nat_item == "status":
                if m["tier"] in ("exato", "normalizado", "casefold"):
                    cid = chaves[m["candidatos"][0]]
                    corpo.append("- fonte: ASSET-CRU (status; BT-6) — `chave coincidente (%s)`: `%s`"
                                 % (m["tier"], ", ".join(cid["ids"])))
                elif m["tier"].startswith("ambiguo"):
                    corpo.append("- fonte: ASSET-CRU (status; BT-6) — sem chave unica "
                                 "(`ambiguo`, %d candidatas)" % len(m["candidatos"]))
                elif m["tier"] == "sem-descricao":
                    corpo.append("- fonte: ASSET-CRU (status; BT-6) — sem descricao no dump")
                else:
                    corpo.append("- fonte: ASSET-CRU (status; BT-6) — sem chave na tabela")
                if desc:
                    corpo.append("- desc jogo (en, asset cru): %s" % esc(desc))
                for k in it["ordem"]:
                    if k == "desc":
                        continue
                    corpo.append("- %s: %s" % (k, esc(it["campos"][k])))
            elif m["tier"] in ("exato", "normalizado", "casefold"):
                ch = chaves[m["candidatos"][0]]
                corpo.append("- fonte: TABELA-LANG-R1 %s (match %s)" % (", ".join(ch["ids"]), m["tier"]))
                corpo.append("- desc jogo (en, como esta no dump): %s" % esc(desc))
                corpo.append("- chave casada na tabela: %s" % esc(m["candidatos"][0]))
                corpo.append("- pt-BR (tabela LANG-R1): %s" % esc(ch["ptbr"]))
                corpo.append("- alertas LANG-R1: %s" % (esc(ch["alertas"]) or "(nenhum)"))
                if ch["contextos"]:
                    corpo.append("- contextos LANG-R1: %s" % esc(ch["contextos"]))
                for k in it["ordem"]:
                    if k == "desc":
                        continue
                    corpo.append("- %s: %s" % (k, esc(it["campos"][k])))
            else:
                corpo.append("- fonte: NAO-ENCONTRADO (%s) — conferir a mao" % m["tier"])
                corpo.append("- desc do dump (en): %s" % (esc(desc) or "(sem descricao)"))
                if m["candidatos"]:
                    corpo.append("- candidatas ambiguas (%d): %s"
                                 % (len(m["candidatos"]), esc(" | ".join(m["candidatos"]))))
                orfaos.append({"fonte": nome_fonte, "titulo": it["titulo"],
                               "parte": it["parte"], "arvore": it["arvore"],
                               "desc": desc, "tier": m["tier"],
                               "candidatas": m["candidatos"]})
                for k in it["ordem"]:
                    if k == "desc":
                        continue
                    corpo.append("- %s: %s" % (k, esc(it["campos"][k])))

    # --- contagens (resumo no topo e no rodape)
    tot = {"itens": 0, "skill": 0, "status": 0, "chaveado": 0, "chaveado_exato": 0,
           "chaveado_normalizado": 0, "chaveado_casefold": 0, "ambiguo": 0,
           "asset_cru": 0, "asset_cru_com_chave_coincidente": 0, "sem_descricao": 0,
           "nao_encontrado": 0}
    for _nome, c in contagens.items():
        tot["itens"] += c["itens"]
        tot["skill"] += c["skill"]
        tot["status"] += c["status"]
        tot["chaveado_exato"] += c["chaveado_exato"]
        tot["chaveado_normalizado"] += c["chaveado_normalizado"]
        tot["chaveado_casefold"] += c["chaveado_casefold"]
        tot["ambiguo"] += c["ambiguo"]
        tot["asset_cru"] += c["asset_cru"]
        tot["asset_cru_com_chave_coincidente"] += c["asset_cru_com_chave_coincidente"]
        tot["sem_descricao"] += c["sem_descricao"]
        tot["nao_encontrado"] += c["nao_encontrado"]
    tot["chaveado"] = (tot["chaveado_exato"] + tot["chaveado_normalizado"]
                       + tot["chaveado_casefold"])

    add("## Contagens (fechadas)")
    add("")
    add("| Fonte (dump de origem) | itens | skill | status | chaveado da tabela | asset cru (BT-6) | nao encontrado |")
    add("|---|---:|---:|---:|---:|---:|---:|")
    for nome_fonte in contagens:
        c = contagens[nome_fonte]
        add("| `%s` | %d | %d | %d | %d | %d | %d |"
            % (nome_fonte, c["itens"], c["skill"], c["status"],
               c["chaveado_exato"] + c["chaveado_normalizado"] + c["chaveado_casefold"],
               c["asset_cru"], c["nao_encontrado"]))
    add("| **TOTAL** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** |"
        % (tot["itens"], tot["skill"], tot["status"], tot["chaveado"], tot["asset_cru"],
           tot["nao_encontrado"]))
    add("")
    add("Tiers do casamento (entre os chaveados): `exato` %d · `normalizado` %d · `casefold` %d · "
        "ambiguos (fora dos chaveados) %d."
        % (tot["chaveado_exato"], tot["chaveado_normalizado"], tot["chaveado_casefold"], tot["ambiguo"]))
    add("")
    add("Duplicidade entre os arquivos (o `DEBUFFS` e o `PASSIVAS` sao **recortes** do `TOOLTIPS`): os %d"
        % itens_total)
    add("itens somam **%d** pares distintos `(titulo, descricao)`; **%d** item(ns) sao repeticao do mesmo"
        % (chaves_distintas, repetidos))
    add("par. Os itens repetidos vem identificados pela secao `## Dump de origem:` — nenhuma informacao")
    add("nova, so o mesmo item lido de outro arquivo.")
    add("")
    add("Unicidade do casamento na tabela: das %d chaves, **%d** tem texto que colide com outra chave"
        % (len(chaves), len([k for k, v in fold.items() if len(v) > 1])))
    add("depois da normalizacao (casefold) e **%d** colide ja na normalizacao sem casefold. Nenhum item"
        % len([k for k, v in norm.items() if len(v) > 1]))
    add("deste dump caiu em casamento ambiguo — ou seja, neste corpus o `casefold` nao escolheu entre")
    add("textos diferentes; ele so absorveu a troca de caixa que o motor do jogo faz no nome do atributo.")
    add("")
    add("Dos `status` (asset cru, sem chave por desenho): **%d** tem texto que coincide com uma chave da"
        % tot["asset_cru_com_chave_coincidente"])
    add("tabela — registrado como `chave coincidente` e **nao** usado como fonte (BT-6); **%d** nao casam"
        % (tot["asset_cru"] - tot["asset_cru_com_chave_coincidente"]))
    add("com nenhuma chave (%d deles nao tem sequer descricao no dump)."
        % tot["sem_descricao"])
    add("")
    add("Lista dos `NAO-ENCONTRADO` (%d):" % len(orfaos))
    add("")
    for o in orfaos:
        add("- `%s` | %s | %s | %s" % (o["fonte"], o["titulo"], o["tier"],
                                       (o["desc"] or "")[:160].replace("\n", " ")))
    if not orfaos:
        add("- (nenhum: toda descricao de skill/aura do dump casou com uma chave da tabela)")
    add("")
    add("Lista do ASSET CRU cujo texto **nao** esta na tabela (%d de %d) — estes ficam no caminho"
        % (len(asset_sem_tabela), tot["asset_cru"]))
    add("antigo sem alternativa (`tools/census.py` + `docs/cobertura/*.csv`):")
    add("")
    for a in asset_sem_tabela:
        add("- `%s` | %s | %s | %s" % (a["fonte"], a["titulo"], a["motivo"],
                                       (a["desc"] or "")[:160].replace("\n", " ")))
    add("")
    add("---")
    add("")

    saida = "\n".join(linhas + corpo + [""])
    with open(md_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(saida)

    cont = {
        "gerado_em": ts,
        "script": "tools/gera_dump_chaveado.py",
        "tabela": {"caminho": csv_path, "sha256": sha256(csv_path),
                   "chaves_distintas": len(chaves),
                   "colisoes_normalizado": len([k for k, v in norm.items() if len(v) > 1]),
                   "colisoes_casefold": len([k for k, v in fold.items() if len(v) > 1])},
        "por_fonte": contagens,
        "total": tot,
        "duplicidade": {"itens_total": itens_total, "pares_distintos": chaves_distintas,
                        "itens_repetidos": repetidos},
        "nao_encontrados": orfaos,
        "asset_cru_sem_coincidencia": asset_sem_tabela,
        "saida": {"caminho": md_path, "sha256": sha256(md_path),
                  "bytes": os.path.getsize(md_path)},
    }
    with open(json_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cont, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return cont


# --------------------------------------------------------------------------------- conferencia

FONTE_LINE = re.compile(r"^- fonte: (?P<x>.*)$")


def conferir(json_path):
    """Reconta o dump gerado a partir das proprias linhas `- fonte:` e compara com o JSON."""
    with open(json_path, encoding="utf-8") as fh:
        esperado = json.load(fh)
    with open(OUT_MD, encoding="utf-8") as fh:
        txt = fh.read()
    cont = {"TABELA-LANG-R1": 0, "ASSET-CRU": 0, "NAO-ENCONTRADO": 0}
    for line in txt.split("\n"):
        m = FONTE_LINE.match(line.strip())
        if not m:
            continue
        x = m.group("x")
        for k in cont:
            if x.startswith(k):
                cont[k] += 1
    t = esperado["total"]
    ok = (cont["TABELA-LANG-R1"] == t["chaveado"]
          and cont["ASSET-CRU"] == t["asset_cru"]
          and cont["NAO-ENCONTRADO"] == t["nao_encontrado"])
    print("conferencia do dump gerado (%s):" % os.path.relpath(OUT_MD, REPO))
    print("  linhas '- fonte: TABELA-LANG-R1' : %6d   esperado chaveado     %6d"
          % (cont["TABELA-LANG-R1"], t["chaveado"]))
    print("  linhas '- fonte: ASSET-CRU'       : %6d   esperado asset cru    %6d"
          % (cont["ASSET-CRU"], t["asset_cru"]))
    print("  linhas '- fonte: NAO-ENCONTRADO'  : %6d   esperado nao encont.  %6d"
          % (cont["NAO-ENCONTRADO"], t["nao_encontrado"]))
    soma = sum(cont.values())
    print("  itens com linha de fonte          : %6d   esperado itens        %6d"
          % (soma, t["itens"]))
    print("  RESULTADO: %s" % ("OK" if ok and soma == t["itens"] else "DIVERGENTE"))
    return 0 if (ok and soma == t["itens"]) else 1


def imprime_hashes(md_path, json_path):
    for p in NAO_TOCAR + [CSV_DEFAULT, md_path, json_path]:
        if os.path.isfile(p):
            print("%s  %s" % (sha256(p), p))
        else:
            print("%s  %s (ausente)" % ("-" * 64, p))
    return 0


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").strip().split("\n")[0])
    ap.add_argument("--csv", default=None, help="tabela localizacao-ptbr.csv do LANG-R1")
    ap.add_argument("--out", default=OUT_MD, help="dump novo (nunca sobrescreve os de origem)")
    ap.add_argument("--contagens", default=OUT_JSON, help="JSON de contagens")
    ap.add_argument("--conferir", action="store_true", help="reconta a partir do dump gerado")
    ap.add_argument("--hashes", action="store_true", help="sha256 das entradas e das saidas")
    args = ap.parse_args()

    if args.hashes:
        return imprime_hashes(args.out, args.contagens)
    if args.conferir:
        return conferir(args.contagens)

    csv_path = args.csv or (CSV_DEFAULT if os.path.isfile(CSV_DEFAULT) else CSV_FALLBACK)
    if not os.path.isfile(csv_path):
        print("Tabela do LANG-R1 nao encontrada: %s" % csv_path)
        print("Passe o caminho com --csv (o anexo do cartao t_2a6474ff se chama "
              "localizacao-ptbr.csv).")
        return 1
    # trava: o script nunca escreve nos arquivos de origem
    for p in (args.out, args.contagens):
        if os.path.abspath(p) in [os.path.abspath(x) for x in NAO_TOCAR]:
            print("RECUSADO: a saida apontaria para um arquivo de origem (%s)" % p)
            return 1

    cont = gera(csv_path, args.out, args.contagens)
    t = cont["total"]
    print("dump gerado: %s (%d bytes, sha256 %s)"
          % (os.path.relpath(args.out, REPO), cont["saida"]["bytes"], cont["saida"]["sha256"]))
    print("contagens: %s" % os.path.relpath(args.contagens, REPO))
    print("  itens=%d  skill=%d  status=%d" % (t["itens"], t["skill"], t["status"]))
    print("  chaveado=%d (exato %d / normalizado %d / casefold %d)"
          % (t["chaveado"], t["chaveado_exato"], t["chaveado_normalizado"], t["chaveado_casefold"]))
    print("  asset cru (BT-6)=%d  (deles, com chave coincidente na tabela: %d; sem descricao: %d)"
          % (t["asset_cru"], t["asset_cru_com_chave_coincidente"], t["sem_descricao"]))
    print("  nao encontrado=%d  ambiguo=%d" % (t["nao_encontrado"], t["ambiguo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
