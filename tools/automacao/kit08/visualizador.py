#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-08 - visualizador HTML LOCAL e comparacao de sessoes (Report Viewer).

O QUE E
-------
Gera UM arquivo HTML **estatico** (sem servidor, sem conta, sem CDN, sem rede,
sem dependencia Hermes/IA/credencial) que mostra, por caso/mod, os campos do
ciclo de evidencia do KIT: `esperado`, `observado`, `prova`, `imagem`,
`sessao/build/config` e `lacunas`. Compara baseline x candidata SOMENTE com
contextos compativeis e invalida aprovacao STALE quando a fonte mudou.

AUTOCONTIDO COM RESSALVA (KIT-08F/F8)
-------------------------------------
Imagens locais so entram EMBUTIDAS (data:) quando resolvidas com confinamento a
partir da pasta da entrada. Se nao resolvem, o relatorio NAO se diz autocontido:
a lacuna e explicita e a referencia declarada aparece como texto (nunca um
`src` dependente de arquivo perdido).

SEGURANCA (o que os testes provam)
----------------------------------
* TODO texto recebido (log/evento/motivo/nome) passa por `escapar` (html.escape):
  payload `<script>`/`onerror=`/`javascript:` vira TEXTO INERTE.
* O HTML gerado NAO contem a tag de script - nao ha JS de dado nem de pagina; a
  meta CSP declara `script-src 'none'` (sem `unsafe-inline` de script).
* NENHUMA referencia remota: sem `http(s)://`, sem `//host`, sem `src=`/`href=`
  externos. So referencias LOCAIS validadas por `referencia_local_segura`
  (relativas, dentro do pacote; recusa esquema, absoluto, traversal `..`, UNC,
  percent-encoding e query/fragment - `%2e%2e` decodifica para `..`).
* Contextos incompativeis NAO sao comparados (INDETERMINADO + motivo): minimo
  obrigatorio, SIMETRIA do declarado e `mod` igual. Fonte/DLL proprias da
  candidata nao impedem a comparacao.
* Aprovacao NAO existe por ausencia nem por registro incompleto/sintetico/de
  outro mod; fonte alterada marca STALE. Fixture rotulada nunca vira PASSOU.
* Aceite humano/publicacao e secao SEPARADA e PENDENTE por padrao: a ferramenta
  jamais auto-aprova nem publica.

REUSO: o avaliador e o proprio `cenarios/kit09.py` (importado por caminho); este
modulo NAO reimplementa o avaliador de criterios.

Uso:
    python tools/automacao/kit08/visualizador.py --entrada <json> [--identidade <json>]
        [--baseline <json>] [--aprovacao <json>] --saida <html>

Exit: 0 = relatorio gerado sem falha tecnica; 1 = relatorio gerado com FALHOU,
comparacao nao-OK ou aprovacao STALE/invalida; 2 = erro de uso/infraestrutura
(I/O, argumentos) ou resultado sem conclusao tecnica. Falha de etapa NUNCA vira
verde. So a stdlib e usada.
"""
import argparse
import base64
import hashlib
import html
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))  # raiz do repo
ESQUEMA = "KIT-08/sessao/1"
EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2

# estados do ciclo (reusados do KIT-09/CIC-3)
OK, REPROVADO, NAO_EXERCITADO, INDETERMINADO = (
    "OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")

# ordem dos VEREDITOS (maior = melhor); usada para detectar regressao REAL
_RANK = {"FALHOU": 0, "INDETERMINADO": 1, "NAO_EXERCITADO": 2, "PASSOU": 3,
         "(ausente)": -1}

# chaves de ambiente que PRECISAM existir para comparar duas sessoes
_MINIMO_CONTEXTO = ("versao_jogo", "bepinex")
# chaves comparadas com SIMETRIA (declarado de um lado so = recusa). Fonte/DLL
# ficam fora de proposito: uma candidata pode ter dll/fonte proprias legitimas.
_COMPARA_CONTEXTO = ("versao_jogo", "bepinex", "config_sha", "cena", "personagem",
                     "build_id", "build", "mod")
# hashes que, mudando, tornam uma aprovacao STALE
_HASHES_APROVACAO = ("fonte_sha", "dll_sha", "config_sha")

_MIMES_IMAGEM = ((".png", "image/png"), (".jpg", "image/jpeg"),
                 (".jpeg", "image/jpeg"), (".gif", "image/gif"),
                 (".svg", "image/svg+xml"), (".webp", "image/webp"),
                 (".bmp", "image/bmp"))

_ESQUEMA_URL = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")


def escapar(texto):
    """Escapa QUALQUER texto recebido para texto inerte (aspas incluidas)."""
    if texto is None:
        return ""
    return html.escape(str(texto), quote=True)


def referencia_local_segura(ref):
    """(ok, motivo). Aceita SO caminho relativo e local dentro do pacote.

    O motivo NUNCA ecoa o valor recusado: a referencia pode ser controlada por
    dado recebido e nao deve ser reproduzida no relatorio (nem como texto).

    Confinamento LEXICAL fail-closed: alem de esquema/absoluto/traversal/UNC,
    recusa percent-encoding (`%2e%2e` == `..` depois de decodificar) e
    query/fragment (`?`/`#`), que nao sao caminho de arquivo e cujo efeito
    especifico num browser NAO e afirmado aqui (hardening, nao exfiltracao
    provada).
    """
    if not isinstance(ref, str):
        return False, "referencia nao e texto"
    r = ref.strip()
    if not r:
        return False, "referencia vazia"
    if r != ref or any(c in ref for c in ("\x00", "\n", "\r", "\t")):
        return False, "referencia com espaco de borda ou caractere de controle"
    low = r.lower()
    if _ESQUEMA_URL.match(r):
        return False, "esquema de URL recusado (so caminho local relativo)"
    if low.startswith("//") or r.startswith("/") or r.startswith("\\"):
        return False, "caminho absoluto ou de rede (//, /, \\) recusado"
    if "\\" in r:
        return False, "separador invertido (rede/absoluto) recusado"
    if "%" in r:
        return False, "percent-encoding recusado (decodificaria para path ambiguo)"
    if "?" in r or "#" in r:
        return False, "consulta/fragmento de URL recusado (nao e caminho de arquivo)"
    if ":" in r:
        return False, "dois-pontos recusado (unidade/esquema disfarcado)"
    partes = r.split("/")
    if any(p == ".." for p in partes):
        return False, "traversal '..' recusado"
    if any(p == "" for p in partes):
        return False, "componente de caminho vazio recusado"
    return True, None


def _txt(v):
    return v if isinstance(v, str) else ("" if v is None else str(v))


def _preenchido(v):
    return v is not None and _txt(v).strip() != ""


def _rotulos_fixture(d):
    """Marcas de fixture/sintetico declaradas num dict (doc, identidade, ...).

    O ROTULO do artefato tem precedencia sobre qualquer `prova_runtime`: fixture
    nunca vira prova de runtime (herdado do KIT-09/CIC-3).
    """
    marcas = []
    if not isinstance(d, dict):
        return marcas
    if d.get("sintetico") is True:
        marcas.append("sintetico")
    if d.get("rotulo_fixture"):
        marcas.append("rotulo_fixture")
    if _txt(d.get("procedencia")).strip().lower() == "fixture":
        marcas.append("procedencia=fixture")
    return marcas


def contexto_de(*fontes):
    """Normaliza o contexto (sessao/build/config) a partir de dicts, p/ comparacao."""
    ctx = {}
    for f in fontes:
        if not isinstance(f, dict):
            continue
        for k in ("versao_jogo", "bepinex", "config_sha", "cena", "personagem",
                  "build_id", "build", "sessao", "fonte_sha", "dll_sha"):
            v = f.get(k)
            if k not in ctx and v is not None and v != "":
                ctx[k] = v
    return ctx


def contexto_do_doc(doc):
    """Contexto vivo de um documento: identidade/build/sessao + mod declarado."""
    doc = doc if isinstance(doc, dict) else {}
    ident = doc.get("identidade") if isinstance(doc.get("identidade"), dict) else {}
    build = doc.get("build") if isinstance(doc.get("build"), dict) else {}
    sessao_raw = doc.get("sessao")
    if isinstance(sessao_raw, str):
        sessao = {"id": sessao_raw} if sessao_raw.strip() else {}
    elif isinstance(sessao_raw, dict):
        sessao = sessao_raw
    else:
        sessao = {}
    ctx = contexto_de(ident, build, sessao)
    if _preenchido(doc.get("mod")):
        ctx["mod"] = _txt(doc.get("mod"))
    sid = sessao.get("id") or sessao.get("sessao")
    if _preenchido(sid):
        ctx["sessao"] = _txt(sid)
    return ctx


def contextos_compativeis(a, b):
    """(compativel, [motivos]). Fail-closed: minimo + simetria + divergencia."""
    a = a if isinstance(a, dict) else {}
    b = b if isinstance(b, dict) else {}
    motivos = []
    for k in _MINIMO_CONTEXTO:
        if not _txt(a.get(k)).strip() or not _txt(b.get(k)).strip():
            motivos.append("contexto incompleto: '%s' ausente em baseline/candidata "
                           "- comparacao sem ambiente comum e recusada" % k)
    for k in _COMPARA_CONTEXTO:
        va, vb = a.get(k), b.get(k)
        pa, pb = _preenchido(va), _preenchido(vb)
        if pa != pb:
            lado = "baseline" if pa else "candidata"
            outro = "candidata" if pa else "baseline"
            motivos.append("contexto unilateral em '%s': declarado em %s e ausente "
                           "em %s - simetria exigida" % (k, lado, outro))
        elif pa and pb and str(va) != str(vb):
            motivos.append("contexto divergente em '%s': baseline=%r != candidata=%r"
                           % (k, va, vb))
    return (not motivos), motivos


def aprovacao_stale(aprovacao, contexto_atual):
    """(stale, motivos). Aprovacao concedida contra uma fonte que MUDOU e STALE."""
    if not isinstance(aprovacao, dict) or not aprovacao:
        return False, []
    atual = contexto_atual if isinstance(contexto_atual, dict) else {}
    motivos = []
    for k in _HASHES_APROVACAO:
        antigo = aprovacao.get(k)
        novo = atual.get(k)
        if antigo is None:
            continue
        if novo is None:
            motivos.append("aprovacao declara '%s' mas o contexto ATUAL nao o traz: "
                           "nao da para confirmar atualidade" % k)
        elif str(antigo) != str(novo):
            motivos.append("FONTE ALTERADA: '%s' da aprovacao=%s != atual=%s"
                           % (k, antigo, novo))
    return bool(motivos), motivos


def avaliacao_aprovacao(aprovacao, contexto):
    """(dict) estado = ausente|invalida|stale|vigente + motivos.

    AUSENCIA NAO E APROVACAO. Registro incompleto (sem hashes), sintetico/
    fixture, de outro mod, ou que contradiz o contexto vigente nunca e vigente.
    O unico caminho "vigente" e: dict completo, nao-sintetico, com identidade
    (mod) coerente e hashes confirmados pelo contexto atual.
    """
    if not isinstance(aprovacao, dict) or not aprovacao:
        return {"estado": "ausente", "motivos": ["nenhuma aprovacao registrada"]}
    ctx = contexto if isinstance(contexto, dict) else {}
    motivos = []
    if _rotulos_fixture(aprovacao):
        motivos.append("aprovacao rotulada como sintetica/fixture nunca e vigente")
    # A aprovacao tem de COBRIR a identidade vigente: alem de fonte/dll, todo
    # hash que o contexto atual traz precisa estar declarado e conferido.
    obrigatorios = ["fonte_sha", "dll_sha"] + \
        [k for k in _HASHES_APROVACAO if _preenchido(ctx.get(k))]
    for k in dict.fromkeys(obrigatorios):
        if not isinstance(aprovacao.get(k), str) or not aprovacao.get(k).strip():
            motivos.append("aprovacao incompleta: '%s' ausente ou nao textual "
                           "(nao cobre a identidade atual)" % k)
    if not _preenchido(aprovacao.get("mod")):
        motivos.append("aprovacao sem 'mod': identidade insuficiente")
    elif _preenchido(ctx.get("mod")) and _txt(aprovacao.get("mod")) != _txt(ctx.get("mod")):
        motivos.append("aprovacao de OUTRO mod: %r != contexto %r"
                       % (aprovacao.get("mod"), ctx.get("mod")))
    stale, motivos_stale = aprovacao_stale(aprovacao, ctx)
    if not motivos and stale:
        motivos.extend(motivos_stale)
    if motivos:
        estado = "stale" if any(("FONTE ALTERADA" in m) or ("nao da para confirmar" in m)
                                for m in motivos) else "invalida"
        return {"estado": estado, "motivos": motivos}
    return {"estado": "vigente", "motivos": []}


def inconsistencias_do_criterio(c, contexto):
    """Contradicoes entre o criterio e o contexto vivo do documento (F5).

    So acusa quando os DOIS lados trazem valor: um criterio que se diz da fonte
    X dentro de um documento cuja identidade e Y nao e prova atual.
    """
    if not isinstance(c, dict) or not isinstance(contexto, dict):
        return []
    probs = []
    for k in ("fonte_sha", "dll_sha", "config_sha"):
        vc, vx = c.get(k), contexto.get(k)
        if _preenchido(vc) and _preenchido(vx) and _txt(vc) != _txt(vx):
            probs.append("'%s' do criterio contradiz o contexto atual do documento" % k)
    sc = c.get("sessao")
    if sc is None:
        sc = c.get("sessao_lida")
    sx = contexto.get("sessao")
    if _preenchido(sc) and _preenchido(sx) and isinstance(sc, str) and _txt(sc) != _txt(sx):
        probs.append("'sessao' do criterio contradiz a sessao do documento")
    return probs


def _tem_evidencia(c):
    """Prova declarada NAO vazia (string nao-branca ou lista com item nao-branco)."""
    ev = c.get("evidencia")
    if isinstance(ev, str):
        return bool(ev.strip())
    if isinstance(ev, (list, tuple)):
        return any(_txt(e).strip() for e in ev)
    return False


def origem_sintetica(doc):
    """True quando o DOC (ou identidade/resumo) se declara fixture/sintetico.

    Nesse caso NENHUM criterio vale como PASSOU, mesmo que traga
    `prova_runtime=True`: o rotulo do artefato tem precedencia (herdado do
    KIT-09/CIC-3). Fixture rotulada nunca vira prova de runtime.
    """
    if not isinstance(doc, dict):
        return False
    marcas = list(_rotulos_fixture(doc))
    if _rotulos_fixture(doc.get("identidade")):
        marcas.append("identidade")
    resumo_raw = doc.get("resumo")
    resumo = resumo_raw if isinstance(resumo_raw, dict) else {}
    org_raw = resumo.get("origem")
    org = org_raw if isinstance(org_raw, dict) else {}
    if org.get("sintetica") is True or org.get("marcas"):
        marcas.append("resumo.origem")
    for c in _itens_de(doc):
        if isinstance(c, dict) and c.get("origem_marcas"):
            marcas.append("criterio.origem_marcas")
            break
    return bool(marcas)


def veredito_tecnico(c, fixture=False, contexto=None):
    """PASSOU so com runtime REAL: prova booleana verdadeira, evidencia nao vazia
    e ausencia de contradicao com o contexto vivo do documento.

    `fixture=True` (doc rotulado como sintetico/fixture) REBAIXA PASSOU para
    NAO_EXERCITADO: fixture nunca vira prova de runtime.
    """
    if not isinstance(c, dict):
        return INDETERMINADO
    estado = c.get("estado")
    proc = _txt(c.get("procedencia")).strip()
    provou = c.get("prova_runtime") is True
    if estado == OK and provou and proc == "runtime":
        if not _tem_evidencia(c) or inconsistencias_do_criterio(c, contexto):
            return INDETERMINADO
        return "NAO_EXERCITADO" if fixture else "PASSOU"
    if estado == REPROVADO:
        return "FALHOU"
    if estado == NAO_EXERCITADO:
        return "NAO_EXERCITADO"
    if estado == INDETERMINADO:
        return "INDETERMINADO"
    # OK sem prova runtime/procedencia runtime NAO e PASSOU
    return "INDETERMINADO"


def _itens_de(doc):
    """Lista de criterios do documento (aceita resumo do KIT-09 ou lista direta)."""
    for chave in ("criterios",):
        v = doc.get(chave)
        if isinstance(v, list):
            return v
    resumo = doc.get("resumo")
    if isinstance(resumo, dict) and isinstance(resumo.get("criterios"), list):
        return resumo["criterios"]
    return []


def _resumo_de(doc):
    resumo = doc.get("resumo")
    return resumo if isinstance(resumo, dict) else {}


def _contagem(criterios, fixture=False, contexto=None):
    cont = {}
    for c in criterios:
        v = veredito_tecnico(c, fixture, contexto)
        cont[v] = cont.get(v, 0) + 1
    return cont


def _ids(criterios):
    return [c.get("id") for c in criterios
            if isinstance(c, dict) and _preenchido(c.get("id"))]


def comparar(baseline, candidata):
    """Compara dois docs (com contextos). Incompativel -> INDETERMINADO, sem comparar.

    Fail-closed: fixture nos dois lados nao promove nada; ids duplicados e lado
    sem casos RECUSAM; caso removido e PERDA de veredito contam como regressao
    (o estado cru nao basta para decidir), sem falso verde.
    """
    baseline = baseline if isinstance(baseline, dict) else {}
    candidata = candidata if isinstance(candidata, dict) else {}
    ctx_a = contexto_do_doc(baseline)
    ctx_b = contexto_do_doc(candidata)
    ok, motivos = contextos_compativeis(ctx_a, ctx_b)
    if not ok:
        return {"estado": "INDETERMINADO", "comparavel": False, "motivos": motivos,
                "itens": [], "regressoes": []}
    ids_a, ids_b = _ids(_itens_de(baseline)), _ids(_itens_de(candidata))
    if len(ids_a) != len(set(ids_a)) or len(ids_b) != len(set(ids_b)):
        return {"estado": "INDETERMINADO", "comparavel": False,
                "motivos": ["ids duplicados no documento: comparacao por id seria "
                            "ambiguada (nao sobrescrever em silencio)"],
                "itens": [], "regressoes": []}
    if not ids_a or not ids_b:
        return {"estado": "INDETERMINADO", "comparavel": False,
                "motivos": ["um dos lados esta sem casos: nada a comparar nao e OK"],
                "itens": [], "regressoes": []}
    fa, fb = origem_sintetica(baseline), origem_sintetica(candidata)
    itens_a = {c.get("id"): c for c in _itens_de(baseline)
               if isinstance(c, dict) and c.get("id")}
    itens_b = {c.get("id"): c for c in _itens_de(candidata)
               if isinstance(c, dict) and c.get("id")}
    itens, regressoes = [], []
    for cid in sorted(set(itens_a) | set(itens_b)):
        ca, cb = itens_a.get(cid), itens_b.get(cid)
        va = veredito_tecnico(ca, fa, ctx_a) if ca else "(ausente)"
        vb = veredito_tecnico(cb, fb, ctx_b) if cb else "(ausente)"
        # indice maior = melhor; caso removido ('(ausente)') nunca e melhora
        reg = _RANK.get(vb, -1) < _RANK.get(va, -1)
        item = {"id": cid, "baseline": va, "candidata": vb,
                "mudou": va != vb, "regressao": reg}
        itens.append(item)
        if reg:
            regressoes.append(cid)
    return {"estado": ("FALHOU" if regressoes else "OK"), "comparavel": True,
            "motivos": [], "itens": itens, "regressoes": regressoes}


def _embutir_imagem(ref, base_dir):
    """(data_url|None, motivo). Resolve/embute LOCALMENTE com confinamento real.

    Nada de caminho dependente da pasta de saida: ou embute (data:), ou declara a
    lacuna explicitamente para nao alegar autocontido falso.
    """
    raiz = base_dir if isinstance(base_dir, str) and base_dir.strip() else None
    if raiz is None:
        return None, "origem da entrada nao informada"
    raiz = os.path.abspath(raiz)
    candidato = os.path.abspath(os.path.join(raiz, ref))
    try:
        confinado = os.path.normcase(os.path.commonpath([raiz, candidato])) == \
            os.path.normcase(raiz)
    except ValueError:
        confinado = False
    if not confinado:
        return None, "caminho fora do pacote da entrada"
    if not os.path.isfile(candidato):
        return None, "arquivo local nao encontrado a partir da entrada"
    try:
        with open(candidato, "rb") as fh:
            dados = fh.read()
    except OSError:
        return None, "arquivo local ilegivel"
    ext = os.path.splitext(candidato)[1].lower()
    mime = dict(_MIMES_IMAGEM).get(ext, "application/octet-stream")
    return "data:%s;base64,%s" % (mime, base64.b64encode(dados).decode("ascii")), None


def _bloco_caso(c, imagens, fixture=False, contexto=None, base_dir=None, lacunas_img=None):
    """HTML de um caso/criterio (todos os campos do ciclo, tudo escapado)."""
    cid = _txt(c.get("id"))
    vt = veredito_tecnico(c, fixture, contexto)
    acoes = []
    for chave, rotulo in (("esperado", "esperado"), ("observado", "observado")):
        acoes.append('<div class="campo"><span class="rot">%s</span>'
                     '<span class="val">%s</span></div>' % (rotulo, escapar(c.get(chave))))
    acoes.append('<div class="campo"><span class="rot">motivo/prova</span>'
                 '<span class="val">%s</span></div>' % escapar(c.get("motivo")))
    ev = c.get("evidencia") or []
    if isinstance(ev, (list, tuple)) and ev:
        itens_ev = []
        for e in ev:
            ok, motivo = referencia_local_segura(e)
            if ok:
                itens_ev.append('<code>%s</code>' % escapar(e))
            else:
                itens_ev.append('<code class="recusado">[referencia recusada: %s]</code>'
                                % escapar(motivo))
        acoes.append('<div class="campo"><span class="rot">prova</span>'
                     '<span class="val">%s</span></div>' % " ".join(itens_ev))
    else:
        acoes.append('<div class="campo"><span class="rot">prova</span>'
                     '<span class="val lacuna">nenhuma evidencia declarada</span></div>')
    # imagem (opcional; so local e segura; embutida com confinamento, senao lacuna)
    ref_img = imagens.get(cid, c.get("imagem"))
    if ref_img is not None:
        ok, motivo = referencia_local_segura(ref_img)
        if not ok:
            acoes.append('<div class="campo"><span class="rot">imagem</span>'
                         '<span class="val lacuna">recusada: %s</span></div>'
                         % escapar(motivo))
        else:
            embutida, falha = _embutir_imagem(ref_img, base_dir)
            if embutida:
                acoes.append('<div class="campo"><span class="rot">imagem</span>'
                             '<span class="val"><img src="%s" alt="%s"></span></div>'
                             % (escapar(embutida), escapar(cid)))
            else:
                if isinstance(lacunas_img, list):
                    lacunas_img.append("%s: %s" % (cid, falha))
                acoes.append('<div class="campo"><span class="rot">imagem</span>'
                             '<span class="val lacuna">nao embutida (%s); referencia '
                             'declarada: <code>%s</code></span></div>'
                             % (escapar(falha), escapar(ref_img)))
    # sessao/build/config
    acoes.append('<div class="campo"><span class="rot">sessao</span>'
                 '<span class="val">%s</span></div>'
                 % escapar(c.get("sessao") or c.get("sessoes_lidas")))
    acoes.append('<div class="campo"><span class="rot">fonte/dll/config</span>'
                 '<span class="val">fonte=%s dll=%s config=%s</span></div>'
                 % (escapar(c.get("fonte_sha")), escapar(c.get("dll_sha")),
                    escapar(c.get("config_sha"))))
    acoes.append('<div class="campo"><span class="rot">procedencia</span>'
                 '<span class="val">%s (prova_runtime=%s)</span></div>'
                 % (escapar(c.get("procedencia")), escapar(c.get("prova_runtime"))))
    # lacunas
    lacunas = []
    if c.get("lacuna_probe"):
        lacunas.append(c["lacuna_probe"])
    if not _tem_evidencia(c) and c.get("estado") != REPROVADO:
        lacunas.append("sem evidencia declarada - nunca PASSOU")
    if c.get("prova_runtime") is not True and c.get("estado") != REPROVADO:
        lacunas.append("sem prova de runtime (fixture/ausente) - nunca PASSOU")
    for p in inconsistencias_do_criterio(c, contexto):
        lacunas.append("contradicao com o contexto: %s" % p)
    if c.get("origem_marcas"):
        lacunas.append("origem sintetica/fixture: %s" % ", ".join(map(str, c["origem_marcas"])))
    acoes.append('<div class="campo"><span class="rot">lacunas</span>'
                 '<span class="val lacuna">%s</span></div>'
                 % escapar("; ".join(lacunas) if lacunas else "nenhuma declarada"))
    return ('<div class="caso %s"><h3>%s <span class="mod">%s</span></h3>%s</div>'
            % (escapar(vt.lower()), escapar(cid), escapar(c.get("mod")), "".join(acoes)))


def _secao_comparacao(cmp_):
    linhas = []
    for it in cmp_.get("itens", []):
        cls = "reg" if it["regressao"] else ("mud" if it["mudou"] else "")
        linhas.append('<tr class="%s"><td>%s</td><td>%s</td><td>%s</td></tr>'
                      % (cls, escapar(it["id"]), escapar(it["baseline"]),
                         escapar(it["candidata"])))
    motivos = "".join('<li>%s</li>' % escapar(m) for m in cmp_.get("motivos", []))
    if not cmp_.get("comparavel"):
        corpo = ('<p class="recusado">Comparacao RECUSADA (INDETERMINADO): contextos '
                 'incompativeis/estrutura invalida.</p><ul>%s</ul>' % motivos)
    else:
        corpo = ('<table><tr><th>criterio</th><th>baseline</th><th>candidata</th></tr>%s'
                 '</table>' % ("".join(linhas) or "<tr><td colspan=3>sem casos comuns</td></tr>"))
    return ('<section class="cmp"><h2>Comparacao baseline x candidata</h2>'
            '<p>estado: <b>%s</b> regressoes=%d</p>%s</section>'
            % (escapar(cmp_.get("estado")), len(cmp_.get("regressoes", [])), corpo))


def _secao_aprovacao(aprovacao, aval):
    """Secao de aprovacao: ausencia/invalida/stale/vigente sao estados DISTINTOS."""
    aprov = aprovacao if isinstance(aprovacao, dict) else {}
    estado = aval.get("estado")
    if estado == "ausente":
        return ('<section class="aprov"><h2>Aprovacao tecnica</h2>'
                '<p class="lacuna">nenhuma aprovacao registrada (ausencia NAO e '
                'aprovacao)</p></section>')
    motivos = "".join('<li>%s</li>' % escapar(m) for m in aval.get("motivos", []))
    ident = ('mod=%s fonte=%s dll=%s config=%s'
             % (escapar(aprov.get("mod")), escapar(aprov.get("fonte_sha")),
                escapar(aprov.get("dll_sha")), escapar(aprov.get("config_sha"))))
    if estado == "vigente":
        corpo = ('<p>estado: <b class="passou">VIGENTE</b> (identidade e hashes '
                 'conferidos) %s</p>' % ident)
    else:
        rotulo = "STALE (INVALIDADA)" if estado == "stale" else "INVALIDA (nao e aprovacao)"
        corpo = ('<p>estado: <b class="recusado">%s</b> %s</p>%s'
                 % (rotulo, ident, ("<ul>%s</ul>" % motivos) if motivos else ""))
    return ('<section class="aprov"><h2>Aprovacao tecnica</h2>%s</section>' % corpo)


def renderizar(doc):
    """Devolve o HTML completo (estatico, sem rede, sem script de dado)."""
    doc = doc if isinstance(doc, dict) else {}
    criterios = _itens_de(doc)
    resumo = _resumo_de(doc)
    build = doc.get("build") if isinstance(doc.get("build"), dict) else {}
    sessao_raw = doc.get("sessao")
    if isinstance(sessao_raw, str):
        sessao = {"id": sessao_raw} if sessao_raw.strip() else {}
    elif isinstance(sessao_raw, dict):
        sessao = sessao_raw
    else:
        sessao = {}
    imagens = doc.get("imagens") if isinstance(doc.get("imagens"), dict) else {}
    base_dir = doc.get("_base_dir")

    ctx_atual = contexto_do_doc(doc)
    aval = avaliacao_aprovacao(doc.get("aprovacao"), ctx_atual)

    baseline = doc.get("baseline") if isinstance(doc.get("baseline"), dict) else None
    cmp_ = comparar(baseline, doc) if baseline else None

    fixture = origem_sintetica(doc)
    cont = _contagem(criterios, fixture, ctx_atual)
    lacunas = list(resumo.get("lacunas") or [])
    org_raw = resumo.get("origem")
    origem = org_raw if isinstance(org_raw, dict) else {}
    lacunas_img = []
    casos = "".join(_bloco_caso(c, imagens, fixture, ctx_atual, base_dir, lacunas_img)
                    for c in criterios) or \
        '<p class="lacuna">nenhum caso no documento</p>'
    resumo_linhas = "".join('<li>%s: %d</li>' % (escapar(k), v)
                            for k, v in sorted(cont.items()))

    ctx_linhas = "".join(
        '<li><b>%s</b>: %s</li>' % (escapar(k), escapar(v))
        for k, v in (("sessao", sessao.get("id") or sessao.get("sessao")),
                     ("versao_jogo", ctx_atual.get("versao_jogo")),
                     ("bepinex", ctx_atual.get("bepinex")),
                     ("build_id", ctx_atual.get("build_id") or build.get("id")),
                     ("config_sha", ctx_atual.get("config_sha")),
                     ("fonte_sha", ctx_atual.get("fonte_sha")),
                     ("dll_sha", ctx_atual.get("dll_sha")),
                     ("cena", ctx_atual.get("cena"))))

    css = (
        "body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:0;padding:1.5rem;"
        "background:#0f1115;color:#e6e6e6}section{margin:1rem 0;padding:1rem;"
        "border:1px solid #2a2f3a;border-radius:8px;background:#161a22}"
        "h1,h2,h3{margin:.2rem 0 .6rem}.campo{display:flex;gap:.5rem;padding:.15rem 0;"
        "border-bottom:1px dashed #242a35}.rot{min-width:12rem;color:#8f9bb3}"
        ".val{white-space:pre-wrap;word-break:break-word}.lacuna{color:#e6b450}"
        ".recusado,.reg{color:#ff6b6b}.mud{color:#e6b450}"
        ".caso{background:#12161d;border:1px solid #2a2f3a;border-radius:8px;"
        "padding:.8rem;margin:.6rem 0}.mod{color:#8f9bb3;font-size:.8em}"
        ".faltou{color:#ff6b6b}.passou{color:#5ad17a}code{background:#0b0e13;"
        "padding:.05rem .3rem;border-radius:4px}ul{margin:.3rem 0 .3rem 1.2rem}"
        "img{max-width:100%;border:1px solid #2a2f3a;border-radius:6px}"
        ".pendente{color:#e6b450;font-weight:bold}")

    if lacunas_img:
        aviso_contido = ('<p class="lacuna">Relatorio offline, sem servidor/rede/JS. '
                         'NAO e integralmente autocontido: ha imagem local nao '
                         'embutida (ver lacunas por caso).</p>')
    else:
        aviso_contido = ('<p class="lacuna">Relatorio offline, sem servidor/rede/JS. '
                         'Texto recebido e escapado; nenhuma tag de script e gerada; '
                         'imagens locais entram embutidas (data:).</p>')

    partes = [
        "<!DOCTYPE html>",
        '<html lang="pt-BR"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        # CSP: nada de rede/recurso externo; SCRIPT PROIBIDO (sem unsafe-inline de script).
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"default-src 'none'; style-src 'unsafe-inline'; img-src 'self' "
        "data:; script-src 'none'; base-uri 'none'; form-action 'none'\">",
        '<title>KIT-08 - %s</title>' % escapar(doc.get("mod") or "relatorio"),
        "<style>%s</style></head><body>" % css,
        "<h1>KIT-08 - visualizador local de sessoes</h1>",
        aviso_contido,
        '<section class="ctx"><h2>Mod &amp; contexto</h2>'
        '<p><b>mod</b>: %s</p><ul>%s</ul>%s</section>' % (
            escapar(doc.get("mod")),
            ctx_linhas,
            ('<p class="recusado">ORIGEM SINTETICA/FIXTURE declarada%s - nenhum caso '
             'abaixo vale como prova de runtime (PASSOU rebaixado).</p>'
             % (": " + escapar(", ".join(map(str, origem.get("marcas") or [])))
                if origem.get("marcas") else ""))
            if fixture else ""),
        '<section class="res"><h2>Resumo tecnico</h2><ul>%s</ul>%s</section>' % (
            resumo_linhas or "<li>sem casos</li>",
            ("<p>lacunas: %s</p>" % escapar("; ".join(map(str, lacunas)))) if lacunas else ""),
    ]
    if cmp_ is not None:
        partes.append(_secao_comparacao(cmp_))
    partes.append(_secao_aprovacao(doc.get("aprovacao"), aval))
    partes.append("<section class=\"casos\"><h2>Casos por mod</h2>%s</section>" % casos)
    # veredito tecnico (separado) e aceite humano (separado, PENDENTE)
    vtabela = "".join('<tr><td>%s</td><td class="%s">%s</td></tr>'
                      % (escapar(c.get("id")),
                         escapar(veredito_tecnico(c, fixture, ctx_atual).lower()),
                         escapar(veredito_tecnico(c, fixture, ctx_atual)))
                      for c in criterios)
    partes.append('<section class="tecnico"><h2>Veredito TECNICO (por criterio)</h2>'
                  '<table><tr><th>criterio</th><th>veredito</th></tr>%s</table>'
                  "<p>PASSOU/FALHOU/NAO_EXERCITADO/INDETERMINADO sao distintos. "
                  "Aprovar tecnicamente NAO equivale a aceite humano nem a publicacao.</p>"
                  "</section>" % vtabela)
    partes.append('<section class="humano"><h2>Aceite HUMANO / PUBLICACAO</h2>'
                  '<p class="pendente">PENDENTE (nao concedido por esta ferramenta).</p>'
                  "<p>Requer verificacao humana em jogo, ausencia de alteracao pendente "
                  "e publicacao aprovada pelo dono. Este visualizador nunca auto-aprova, "
                  "nunca publica e nao decide o DoD.</p></section>")
    partes.append('<footer><p>Gerado por KIT-08 (visualizador.py). Esquema %s. '
                  "Sem rede, sem credenciais, sem dependencia Hermes.</p></footer>"
                  % escapar(ESQUEMA))
    partes.append("</body></html>")
    return "\n".join(partes)


# --------------------------------------------------------------------- reuso ----

def _carregar_kit09():
    """Carrega o avaliador KIT-09 por caminho.

    KIT-15F/F9: procura tambem a localizacao do layout DISTRIBUIDO (componentes irmaos:
    `components/viewer/../cenarios/kit09.py`) antes de desistir. A ausencia e declarada
    explicitamente -- nunca vira verde por omissao."""
    candidatos = [
        os.environ.get("KIT08_KIT09") or "",
        os.path.join(_RAIZ, "tools", "automacao", "cenarios", "kit09.py"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cenarios", "kit09.py"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "cenarios", "kit09.py"),
    ]
    caminho = ""
    for c in candidatos:
        if c and os.path.isfile(c):
            caminho = c
            break
    if not caminho:
        raise RuntimeError("KIT-08: avaliador KIT-09 ausente (nao empacotado neste layout)")
    spec = importlib.util.spec_from_file_location("kit09_para_kit08", caminho)
    if spec is None or spec.loader is None:
        raise RuntimeError("KIT-08: nao consegui carregar o KIT-09 em %s" % caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def mesclar_identidade(entrada, identidade):
    """Mescla a identidade FORNECIDA antes de qualquer avaliacao (F6/CLI)."""
    if not isinstance(entrada, dict) or not isinstance(identidade, dict):
        return entrada
    doc = dict(entrada)
    base = doc.get("identidade") if isinstance(doc.get("identidade"), dict) else {}
    base = dict(base)
    base.update(identidade)
    doc["identidade"] = base
    return doc


def montar_doc(entrada):
    """Monta o doc do visualizador; se vier 'observacoes', avalia via KIT-09 (reuso)."""
    if not isinstance(entrada, dict):
        raise ValueError("entrada nao e um objeto JSON")
    doc = dict(entrada)
    if _itens_de(doc):
        return doc
    obs = doc.get("observacoes")
    if obs is None or (isinstance(obs, (list, dict, str)) and not obs):
        # KIT-15F/F9: sem observacoes nao ha o que avaliar -- nao exigir o KIT-09 (que nao e
        # empacotado no layout distribuido). O doc sai como veio; ausencia nao vira verde.
        return doc
    kit09 = _carregar_kit09()
    ident = doc.get("identidade") if isinstance(doc.get("identidade"), dict) else {}
    criterios = kit09.avaliar_cenarios(obs, ident, envelope=doc)
    doc["resumo"] = kit09.resumir(criterios, ident)
    return doc


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-08: visualizador HTML local de sessoes.")
    ap.add_argument("--entrada", required=True, help="JSON da sessao/casos")
    ap.add_argument("--identidade", help="JSON com fonte_sha/dll_sha/config_sha/...")
    ap.add_argument("--baseline", help="JSON da sessao BASELINE para comparacao")
    ap.add_argument("--aprovacao", help="JSON da aprovacao tecnica vigente")
    ap.add_argument("--saida", required=True, help="arquivo HTML de saida")
    args = ap.parse_args(argv)

    def _ler(p):
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)

    # F9: TODA entrada (obrigatoria e opcional) e lida de forma controlada ->
    # exit2 com diagnostico, nunca traceback; falha distinta de skip/sucesso.
    try:
        entrada = _ler(args.entrada)
        identidade = _ler(args.identidade) if args.identidade else None
        baseline = _ler(args.baseline) if args.baseline else None
        aprovacao = _ler(args.aprovacao) if args.aprovacao else None
    except (OSError, ValueError) as erro:
        sys.stderr.write("KIT-08: falha ao ler entrada/opcional: %s\n" % erro)
        return EXIT_NAO_RODOU

    # F6: identidade FORNECIDA entra ANTES de montar/avaliar (CLI == API).
    try:
        doc = montar_doc(mesclar_identidade(entrada, identidade))
    except (ValueError, RuntimeError) as erro:
        sys.stderr.write("KIT-08: entrada invalida: %s\n" % erro)
        return EXIT_NAO_RODOU
    if baseline is not None:
        doc["baseline"] = baseline
    if aprovacao is not None:
        doc["aprovacao"] = aprovacao
    try:
        doc["_base_dir"] = os.path.dirname(os.path.abspath(args.entrada))
    except Exception:  # pragma: no cover - defensivo
        doc["_base_dir"] = None

    html_txt = renderizar(doc)
    try:
        pai = os.path.dirname(os.path.abspath(args.saida))
        if pai and not os.path.isdir(pai):
            os.makedirs(pai, exist_ok=True)
        with open(args.saida, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html_txt)
    except OSError as erro:
        sys.stderr.write("KIT-08: falha ao gravar saida: %s\n" % erro)
        return EXIT_NAO_RODOU

    sha = hashlib.sha256(html_txt.encode("utf-8")).hexdigest()
    ctx = contexto_do_doc(doc)
    cont = _contagem(_itens_de(doc), origem_sintetica(doc), ctx)
    aval = avaliacao_aprovacao(doc.get("aprovacao"), ctx)
    stale = aval.get("estado") == "stale"
    cmp_ = comparar(doc.get("baseline"), doc) if doc.get("baseline") else None
    cmp_ok = (cmp_ is None) or (bool(cmp_.get("comparavel")) and cmp_.get("estado") == "OK")
    print("KIT-08: relatorio=%s bytes=%d sha256=%s contagem=%s aprovacao=%s comparacao=%s"
          % (args.saida, len(html_txt.encode("utf-8")), sha, json.dumps(cont, sort_keys=True),
             aval.get("estado"), (cmp_ or {}).get("estado", "n/a")))
    # F7: o exit agrega TODAS as etapas (criterios, aprovacao e comparacao), sem
    # tratar ausencia/INDETERMINADO/recusa como verde nem misturar 0/1/2.
    if cont.get("FALHOU") or stale or aval.get("estado") == "invalida" or not cmp_ok:
        return EXIT_FALHOU
    if cont.get("PASSOU"):
        return EXIT_OK
    return EXIT_NAO_RODOU


if __name__ == "__main__":
    sys.exit(main())
