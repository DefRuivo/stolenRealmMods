#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_relatorio_aceite.py - AUT-7: teste do relatorio de aceite por mod (DoD).

Roda SOZINHO (ferramenta, nao suite de produto), na convencao de
`tools/automacao/ciclo/test_*.py`: exit 0 = tudo verde, 1 = reprovou, 2 = nao rodou.

O QUE ELE PRENDE (o aceite da tarefa):
  * o relatorio por mod tem de sair com PROVAS, REGRESSAO, LACUNAS e ROTEIRO HUMANO;
  * status TECNICO, ACEITE HUMANO e PUBLICACAO tem de ficar SEPARADOS;
  * "carregado" nao vale como "eficaz": criterio que se declara OK sem evidencia NAO
    pode virar prova vinculante (o rotulo nao aprova);
  * frente sem entrada (AUT-3/5/6 ausente) sai NAO_EXERCITADO — nunca OK;
  * aceite humano declarado sobre mod com falha automatica fica INCONSISTENTE e a
    falha NAO desaparece.

Uso: python tools/automacao/aceite/test_relatorio_aceite.py
"""
import io
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import relatorio_aceite as ra  # noqa: E402

RAIZ = ra.RAIZ
CASOS = []
FALHAS = []


def caso(nome):
    def deco(fn):
        CASOS.append((nome, fn))
        return fn
    return deco


def exigir(cond, msg):
    if not cond:
        raise AssertionError(msg)


def _arquivo_evidencia(nome="aut7-evidencia-rel.json"):
    caminho = os.path.join(tempfile.gettempdir(), nome)
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write("{\"evidencia\": \"arquivo real usado pelo teste do relatorio\"}")
    return caminho


def _decisao(criterios, identidade=None, aceite=None):
    dec = ra._decisao()
    exigir(dec is not None, "decisao.py (CIC-2) indisponivel: sem ela nao ha relatorio honesto")
    return dec.consolidar(criterios, identidade or {"fonte_sha": "f" * 12, "dll_sha": "d" * 12},
                          aceite_humano=aceite)


def _criterios_mistos():
    ev = _arquivo_evidencia()
    return [
        {"id": "X/offline-ok", "mod": "BetterFont", "estado": "OK", "classe": "offline",
         "procedencia": "execucao", "esperado": "suite pura verde", "observado": "PASSOU",
         "motivo": "teste puro do mod", "evidencia": [{"caminho": ev, "sha256": None}],
         "tarefa_origem": "t_674c5976"},
        {"id": "X/regressao", "mod": "BetterFont", "estado": "REPROVADO", "classe": "offline",
         "procedencia": "execucao", "esperado": "sem regressao", "observado": "REPROVOU",
         "motivo": "teste puro reprovou", "evidencia": [ev], "tarefa_origem": "t_674c5976"},
        {"id": "X/visual", "mod": "BetterStats", "estado": "NAO_EXERCITADO", "classe": "runtime",
         "procedencia": "runtime", "esperado": "layout cabe no painel",
         "observado": "julgamento humano nao pronunciado", "motivo": "aceite visual",
         "evidencia": [], "tarefa_origem": "t_674c5976",
         "tipo_pendencia": "julgamento_visual", "autorizacao_necessaria": True,
         "julgamento_humano": "Abrir a ficha e conferir o layout."},
    ]


@caso("relatorio por mod: provas, regressao, lacunas e roteiro humano existem")
def _t_secoes():
    dec = _decisao(_criterios_mistos())
    rel = ra.montar_relatorio(dec, None, {})
    fonte = rel["por_mod"]["BetterFont"]
    exigir([p["id"] for p in fonte["provas"]] == ["X/offline-ok"],
           "a prova vinculante do BetterFont devia ser so a do offline-ok: %r"
           % [p["id"] for p in fonte["provas"]])
    exigir([f["id"] for f in fonte["regressao"]] == ["X/regressao"],
           "a regressao do BetterFont devia estar em regressao: %r"
           % [f["id"] for f in fonte["regressao"]])
    stats = rel["por_mod"]["BetterStats"]
    exigir(any(x["id"] == "X/visual" for x in stats["lacunas"]),
           "a pendencia de runtime devia aparecer nas lacunas do BetterStats")
    exigir(stats["roteiro_humano"] and stats["roteiro_humano"][0]["tipo"] == "julgamento_visual",
           "o roteiro humano do BetterStats devia trazer o julgamento visual")
    exigir(fonte["estado"] == "REPROVADO",
           "mod com falha automatica nao pode ter estado tecnico OK: %r" % fonte["estado"])


@caso("tres estados SEPARADOS: tecnico, aceite humano e publicacao no markdown")
def _t_estados_separados():
    dec = _decisao(_criterios_mistos())
    rel = ra.montar_relatorio(dec, None, {})
    rel["aceite_humano"] = dec.get("aceite_humano")
    rel["publicacao"] = dec.get("publicacao")
    rev = ra._revisoes(None)
    md = ra.markdown_do_relatorio(rel, rev, {})
    exigir("ACEITE HUMANO" in md.upper(), "o relatorio tem de dizer o estado do aceite humano")
    exigir("PUBLICACAO" in md.upper(), "o relatorio tem de dizer o estado da publicacao")
    exigir("NAO_PRONUNCIADO" in md, "aceite humano por padrao e NAO_PRONUNCIADO")
    exigir("NAO_VERIFICADO" in md, "publicacao por padrao e NAO_VERIFICADO")
    for secao in ("### Provas", "### Regressao", "### Lacunas", "### Roteiro humano minimo"):
        exigir(secao in md, "o relatorio tem de ter a secao %r" % secao)
    exigir("PROVISORIA" in md, "com revisao pendente a consolidacao final e PROVISORIA")


@caso("rotulo OK sem evidencia NAO vira prova (o rotulo nao aprova)")
def _t_rotulo_nao_aprova():
    ev = _arquivo_evidencia()
    sem_evidencia = [{"id": "Y/declara-ok", "mod": "BetterFont", "estado": "OK", "classe": "offline",
                      "procedencia": "execucao", "esperado": "x", "observado": "declarado OK",
                      "motivo": "sem prova", "evidencia": [], "tarefa_origem": "t_674c5976"}]
    dec = _decisao(sem_evidencia)
    exigir(not dec["por_mod"]["BetterFont"]["ok_vinculantes"],
           "criterio declarado OK sem evidencia NAO pode virar prova vinculante")
    exigir(dec["falhas_automaticas"],
           "sem prova o criterio tem de virar falha automatica, nao silencio")
    # evidencia com hash DIVERGENTE tambem nao vale
    divergente = [dict(sem_evidencia[0], evidencia=[{"caminho": ev, "sha256": "0" * 64}])]
    dec2 = _decisao(divergente)
    exigir(not dec2["por_mod"]["BetterFont"]["ok_vinculantes"],
           "evidencia com hash divergente nao pode virar prova vinculante")


@caso("frente sem entrada (AUT-3/5/6) sai NAO_EXERCITADO, nunca OK")
def _t_frentes_ausentes():
    c_aut3 = ra.criterios_aut3(RAIZ, os.path.join(RAIZ, "nao-existe.json"), {})
    exigir(len(c_aut3) == 1 and c_aut3[0]["estado"] == "NAO_EXERCITADO",
           "AUT-3 ausente tem de sair NAO_EXERCITADO: %r" % c_aut3)
    c_rstv = ra.criterios_rstv([], {}, None)
    exigir(len(c_rstv) == 1 and c_rstv[0]["estado"] == "NAO_EXERCITADO",
           "AUT-5 sem observacao/resultado tem de sair NAO_EXERCITADO: %r" % c_rstv)
    c_shrines = ra.criterios_shrines([], {}, None)
    exigir(len(c_shrines) == 1 and c_shrines[0]["estado"] == "NAO_EXERCITADO",
           "AUT-6 sem observacao/resultado tem de sair NAO_EXERCITADO: %r" % c_shrines)
    for c in (c_aut3[0], c_rstv[0], c_shrines[0]):
        exigir(c["motivo"] and c["observado"], "%s sem motivo/observado ditos" % c["id"])


@caso("AUT-3 ilegivel tambem nao vira OK (arquivo que nao e resultado da bancada)")
def _t_aut3_ilegivel():
    tmp = os.path.join(tempfile.mkdtemp(prefix="aut7-aut3-"), "falso.json")
    with io.open(tmp, "w", encoding="utf-8") as fh:
        fh.write("{\"qualquer\": 1}")
    criterios = ra.criterios_aut3(RAIZ, tmp, {})
    exigir(len(criterios) == 1 and criterios[0]["estado"] == "NAO_EXERCITADO",
           "arquivo sem veredito do AUT-3 tem de sair NAO_EXERCITADO: %r" % criterios)
    exigir("formato" in criterios[0]["motivo"] or "ilegivel" in criterios[0]["motivo"],
           "o motivo tem de dizer que o formato nao e do AUT-3: %r" % criterios[0]["motivo"])


@caso("aceite humano sobre mod com falha automatica fica INCONSISTENTE (nao esconde)")
def _t_aceite_inconsistente():
    criterios = _criterios_mistos()
    dec = _decisao(criterios, aceite={"BetterFont": {"aceito": True}})
    exigir(dec.get("aceite_inconsistente"),
           "aceite num mod com falha automatica tem de ser sinalizado como inconsistente")
    exigir(dec["por_mod"]["BetterFont"]["falhas_automaticas"],
           "a falha automatica NAO pode desaparecer por causa do aceite")
    md = ra.markdown_do_relatorio(ra.montar_relatorio(dec, None, {}), ra._revisoes(None), {})
    exigir("### Regressao" in md, "o relatorio continua com a secao de regressao")
    exigir("X/regressao" in md, "a regressao do BetterFont tem de estar visivel no relatorio")


@caso("revisoes: pendente deixa PROVISORIO; todas OK libera a consolidacao final")
def _t_revisoes():
    pendente = ra._revisoes(None)
    exigir(pendente["consolidacao_final"] is False, "sem manifesto a consolidacao e PROVISORIA")
    tmp = os.path.join(tempfile.mkdtemp(prefix="aut7-rev-"), "rev.json")
    with io.open(tmp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"revisoes": {"AUT-3R": "OK", "AUT-5R": "OK", "AUT-6R": "OK"}}))
    ok = ra._revisoes(tmp)
    exigir(ok["consolidacao_final"] is True, "com as tres revisoes OK a consolidacao libera: %r" % ok)
    with io.open(tmp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"revisoes": {"AUT-3R": "OK", "AUT-5R": "EM_ANDAMENTO", "AUT-6R": "OK"}}))
    meio = ra._revisoes(tmp)
    exigir(meio["consolidacao_final"] is False and "AUT-5R" in meio["motivo"],
           "revisao em andamento tem de manter PROVISORIO e ser nomeada: %r" % meio)


@caso("relatorio nao afirma eficacia: mod sem criterio nenhum sai NAO_EXERCITADO")
def _t_mod_sem_criterio():
    dec = _decisao([_criterios_mistos()[0]])
    rel = ra.montar_relatorio(dec, None, {})
    debugger = rel["por_mod"]["RoguelikeDebugger"]
    exigir(debugger["estado"] == "NAO_EXERCITADO",
           "mod sem criterio nenhum NAO pode aparecer como OK: %r" % debugger["estado"])
    exigir(debugger["provas"] == [] and debugger["nota"],
           "mod sem criterio tem de dizer que nao tem prova (nota explicita)")


@caso("markdown aguenta as DUAS formas de evidencia (caminho solto e dict)")
def _t_evidencia_duas_formas():
    exigir(ra._nome_ev("/a/b/c.json") == "c.json", "_nome_ev tem de aceitar caminho solto")
    exigir(ra._nome_ev({"caminho": "/a/b/d.json"}) == "d.json", "_nome_ev tem de aceitar dict")
    exigir(ra._nome_ev(None) == "", "_nome_ev tem de aguentar evidencia ausente")


@caso("CLI: --sem-suite consolida e diz o que faltou (nunca sai 0 sem prova)")
def _t_cli():
    out = tempfile.mkdtemp(prefix="aut7-cli-rel-")
    try:
        import subprocess
        argv = [sys.executable, os.path.join(AQUI, "relatorio_aceite.py"),
                "--repo", RAIZ, "--out-dir", out, "--sem-suite",
                "--out", os.path.join(out, "saida.json"),
                "--relatorio", os.path.join(out, "rel.md")]
        proc = subprocess.run(argv, cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=600)
        exigir(proc.returncode in (0, 1, 2), "exit inesperado: %s" % proc.returncode)
        texto = proc.stdout.decode("utf-8", "replace")
        exigir(texto.strip().startswith("{"), "o CLI tem de imprimir o resumo em JSON")
        dados = json.loads(texto)
        exigir(dados.get("criterios", 0) > 0, "o CLI tem de consolidar criterios")
        exigir(os.path.isfile(os.path.join(out, "rel.md")),
               "o --relatorio tem de gravar o markdown")
        exigir(os.path.isfile(os.path.join(out, "saida.json")),
               "o --out tem de gravar o resultado completo")
        md = io.open(os.path.join(out, "rel.md"), encoding="utf-8").read()
        exigir("RELATORIO DE ACEITE" in md.upper() or "relatorio de aceite" in md.lower(),
               "o markdown gravado tem de ser o relatorio de aceite")
    finally:
        import shutil
        shutil.rmtree(out, ignore_errors=True)



def _resultado_frente(pasta, nome, itens, identidade=None):
    dado = {"esquema": "AUT-5/1", "criterios": itens}
    if identidade:
        dado["identidade"] = identidade
    caminho = os.path.join(pasta, nome)
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(dado, ensure_ascii=False))
    return caminho


def _item_frente(id_, estado="OK", mod="RoguelikeSkillTreeVisualizer", evidencia=None):
    return {"id": id_, "mod": mod, "estado": estado, "classe": "runtime", "procedencia": "runtime",
            "esperado": "frente medida", "observado": "medido",
            "evidencia": [evidencia or _arquivo_evidencia("aut7-frente-ev.json")]}


@caso("AUT-5/6: resultado vazio vira LACUNA canonica (nunca frente=0)")
def _t_frente_vazia():
    pasta = tempfile.mkdtemp(prefix="aut7-frente-")
    try:
        vazio = _resultado_frente(pasta, "vazio.json", [])
        for frente, fn, mod in (("AUT-5", ra.criterios_rstv, "RoguelikeSkillTreeVisualizer"),
                                ("AUT-6", ra.criterios_shrines, "BetterTooltips")):
            criterios = fn([], {"fonte_sha": "f" * 64, "dll_sha": "d" * 64},
                           criterios_arquivo=vazio)
            exigir(len(criterios) == 1, "%s vazio tem de gerar UMA lacuna, veio %d" % (frente, len(criterios)))
            exigir(criterios[0]["estado"] == "NAO_EXERCITADO",
                   "%s vazio nao pode virar OK: %r" % (frente, criterios[0]))
            exigir(criterios[0]["id"] == "%s/resultado-vazio" % frente,
                   "o id canonico da lacuna mudou: %r" % criterios[0]["id"])
            exigir(criterios[0]["evidencia"], "%s: a lacuna tem de apontar o arquivo lido" % frente)
        ilegivel = os.path.join(tempfile.mkdtemp(prefix="aut7-frente-"), "ilegivel.json")
        with io.open(ilegivel, "w", encoding="utf-8") as fh:
            fh.write("{nao e json")
        c = ra.criterios_rstv([], {}, criterios_arquivo=ilegivel)
        exigir(len(c) == 1 and c[0]["id"] == "AUT-5/resultado-ilegivel",
               "resultado ilegivel tem de virar lacuna nomeada: %r" % c)
    finally:
        import shutil as _sh
        _sh.rmtree(pasta, ignore_errors=True)


@caso("AUT-5/6: evidencia de item conferida (existencia+sha) e identidade sem emprestimo")
def _t_frente_malformada():
    pasta = tempfile.mkdtemp(prefix="aut7-frente2-")
    try:
        ident = {"fonte_sha": "f" * 64, "dll_sha": "d" * 64}
        bom = _item_frente("AUT-5/bom")
        sem_ev = {"id": "AUT-5/sem-evidencia", "mod": "RoguelikeSkillTreeVisualizer",
                  "estado": "OK", "evidencia": []}
        sem_estado = {"id": "AUT-5/sem-estado", "mod": "RoguelikeSkillTreeVisualizer",
                      "evidencia": ["/x/y.json"]}
        arq = _resultado_frente(pasta, "misto.json", [bom, sem_ev, sem_estado], ident)
        criterios = ra.criterios_rstv([], ident, criterios_arquivo=arq)
        ids = [c["id"] for c in criterios]
        exigir("AUT-5/bom" in ids, "o item valido tem de ser preservado: %r" % ids)
        exigir("AUT-5/resultado-malformado" in ids,
               "item sem evidencia/estado tem de gerar lacuna: %r" % ids)
        # A identidade da rodada entra como RASTRO em TODOS os criterios (achado A7)...
        exigir(all(c.get("identidade_da_rodada", {}).get("fonte_sha") == ident["fonte_sha"]
                   for c in criterios),
               "o adaptador tem de registrar a identidade da rodada em todos os criterios")
        # ...e nunca como prova EMPRESTADA: item OK de runtime sem identidade propria e
        # rebaixado (antes virava OK_VINCULANTE so por causa do emprestimo).
        por_id = {c["id"]: c for c in criterios}
        exigir(por_id["AUT-5/bom"]["estado"] == "NAO_EXERCITADO",
               "item de runtime OK sem identidade PROPRIA nao pode seguir OK: %r"
               % por_id["AUT-5/bom"])
        exigir(not por_id["AUT-5/bom"].get("fonte_sha"),
               "o adaptador NAO pode injetar `fonte_sha` no item como se fosse prova dele")
        exigir("AUT-5/item-nao-vinculado" in ids,
               "o rebaixamento tem de vir com lacuna canonica: %r" % ids)
        # evidencia declarada que nao existe (ou com sha divergente) NAO vira item valido
        ev_ruim = _item_frente("AUT-5/ev-inexistente",
                               evidencia=[{"caminho": os.path.join(pasta, "NAO-EXISTE.json"),
                                           "sha256": "0" * 64}])
        ev_sha = _item_frente("AUT-5/sha-divergente",
                              evidencia=[{"caminho": _arquivo_evidencia(),
                                          "sha256": "f" * 64}])
        arq2 = _resultado_frente(pasta, "ev.json", [ev_ruim, ev_sha], ident)
        ids2 = [c["id"] for c in ra.criterios_rstv([], ident, criterios_arquivo=arq2)]
        exigir("AUT-5/resultado-malformado" in ids2,
               "evidencia inexistente/sha divergente tem de virar malformado: %r" % ids2)
        # identidade divergente: lacuna canonica E o item REBAIXADO (nunca OK)
        ev_bom = _item_frente("AUT-5/div")["evidencia"][0]
        divergente = _resultado_frente(
            pasta, "div.json",
            [_item_frente("AUT-5/div", evidencia=ev_bom)],
            {"fonte_sha": "a" * 64, "dll_sha": "d" * 64})
        c2 = ra.criterios_rstv([], ident, criterios_arquivo=divergente)
        ids3 = [x["id"] for x in c2]
        exigir("AUT-5/identidade-divergente" in ids3,
               "identidade de outra rodada tem de gerar lacuna: %r" % ids3)
        item3 = [x for x in c2 if x["id"] == "AUT-5/div"][0]
        exigir(item3["estado"] == "NAO_EXERCITADO",
               "item de rodada divergente tem de ser REBAIXADO: %r" % item3)
        exigir("AUT-5/item-nao-vinculado" in ids3,
               "o rebaixamento tem de vir com lacuna canonica: %r" % ids3)
    finally:
        import shutil as _sh
        _sh.rmtree(pasta, ignore_errors=True)


@caso("AUT-5/6: rotulo OK com arquivo qualquer e identidade emprestada NAO vira prova (A7)")
def _t_frente_identidade_emprestada():
    """ACHADO A7: os cenarios X5 do parecer COR-AUT7R, reproduzidos no adaptador."""
    pasta = tempfile.mkdtemp(prefix="aut7-a7-")
    try:
        ident = {"fonte_sha": "2" * 64, "dll_sha": "b" * 64, "sessao": "s1"}
        marcador = _arquivo_evidencia("aut7-marcador.txt")   # arquivo REAL e qualquer
        sha = ra._sha(marcador)

        def item(id_, **kw):
            c = {"id": id_, "mod": "BetterTooltips", "estado": "OK", "classe": "runtime",
                 "procedencia": "runtime", "prova_runtime": True, "sessao": "s1",
                 "esperado": "e", "observado": "rotulo OK sem medicao",
                 "evidencia": [{"caminho": marcador, "sha256": sha}]}
            c.update(kw)
            return c

        def roda(itens, ident_result=None):
            caminho = _resultado_frente(pasta, "f.json", itens, ident_result)
            return ra.criterios_shrines([], ident, criterios_arquivo=caminho)

        # X5b: rotulo OK + arquivo qualquer + sessao, SEM identidade propria -> rebaixado
        x5b = roda([item("AUT-6/sint/rotulo")])
        alvo = [c for c in x5b if c["id"] == "AUT-6/sint/rotulo"][0]
        exigir(alvo["estado"] == "NAO_EXERCITADO",
               "X5b: rotulo sem medicao nao pode seguir OK, veio %r" % alvo)
        exigir(any(c["id"] == "AUT-6/item-nao-vinculado" for c in x5b),
               "X5b: tem de sair a lacuna canonica do rebaixamento: %r" % [c["id"] for c in x5b])
        # X5c: item que declara `identidade` divergente -> rebaixado
        x5c = roda([item("AUT-6/sint/ident-div",
                         identidade={"fonte_sha": "0" * 64, "dll_sha": "1" * 64})])
        alvo_c = [c for c in x5c if c["id"] == "AUT-6/sint/ident-div"][0]
        exigir(alvo_c["estado"] == "NAO_EXERCITADO",
               "X5c: item que declara outra rodada nao pode seguir OK, veio %r" % alvo_c)
        # controle POSITIVO: identidade PROPRIA + identidade do resultado conferem -> OK
        proprio = dict(item("AUT-6/sint/proprio"), fonte_sha=ident["fonte_sha"],
                       dll_sha=ident["dll_sha"])
        positivo = roda([proprio], ident_result=ident)
        alvo_p = [c for c in positivo if c["id"] == "AUT-6/sint/proprio"][0]
        exigir(alvo_p["estado"] == "OK",
               "item com identidade propria conferida tem de seguir OK (controle): %r" % alvo_p)
    finally:
        import shutil as _sh
        _sh.rmtree(pasta, ignore_errors=True)


@caso("AUT-6: reusa a frente REAL do aut6/cobertura.py e nunca devolve vazio")
def _t_frente_aut6_adaptador():
    """A frente AUT-6 tem de ser a REAL (aut6/cobertura.py), nunca reimplementada aqui.

    Achado A8: o modulo real nao CARREGAVA na arvore entregue (`aut6/cobertura.py` faz
    `import prova` no TOPO e o diretorio do pacote nao estava no `sys.path`), e a frente
    saia `avaliador-indisponivel` com 0 itens. Agora a frente real responde - sem NUNCA
    cair em `cenarios/tooltips_shrines.py`, que mediria por outras regras.
    """
    ident = {"fonte_sha": "f" * 64, "dll_sha": "d" * 64, "sessao": "s1"}
    preferido = os.path.join(RAIZ, "tools", "automacao", "aut6", "cobertura.py")
    mod, rel, rotulo = ra._frente_avaliador("AUT-6")
    obs = [{"objeto": "Tooltip.Title", "procedencia": "fixture"}]
    criterios = ra.criterios_shrines(obs, ident)
    exigir(isinstance(criterios, list) and criterios,
           "o adaptador do AUT-6 nunca pode devolver lista vazia (frente=0): %r" % criterios)
    exigir(all(isinstance(c, dict) and c.get("id") for c in criterios),
           "todo criterio da frente tem de ter id canonico: %r" % criterios)
    exigir(os.path.isfile(preferido),
           "a frente REAL do AUT-6 tem de existir no repo: %r" % preferido)
    exigir(mod is not None and os.path.abspath(os.path.join(RAIZ, rel)) == os.path.abspath(preferido),
           "a frente real do AUT-6 tem de CARREGAR (achado A8): %r | %s" % (rel, rotulo))
    exigir(hasattr(mod, "avaliar"), "o modulo da frente real tem de expor `avaliar`")
    exigir(all(c.get("adaptador") for c in criterios),
           "cada criterio da frente tem de dizer QUAL adaptador o produziu")
    exigir(not any(str(c.get("id", "")).endswith("avaliador-indisponivel") for c in criterios),
           "com o modulo real carregado nao pode sair `avaliador-indisponivel`: %r"
           % [c.get("id") for c in criterios])
    exigir(not any("tooltips_shrines" in str(c.get("adaptador")) for c in criterios),
           "o antigo cenarios/tooltips_shrines.py nao pode substituir a frente real")
    exigir(ra._ev_rel(preferido) is not None,
           "o modulo da frente real tem de existir e ser hasheavel: %r" % preferido)
    # observacao malformada: lacuna honesta, nunca excecao nem vazio
    criterios2 = ra.criterios_shrines([{"nada": 1}], ident)
    exigir(criterios2 and all(isinstance(c, dict) and c.get("id") for c in criterios2),
           "observacao malformada tem de virar criterio nomeado: %r" % criterios2)


@caso("consolidacao: frente vazia mantem lacuna no resultado (por_frente > 0)")
def _t_consolidacao_frente_vazia():
    pasta = tempfile.mkdtemp(prefix="aut7-cons-")
    try:
        vazio = _resultado_frente(pasta, "vazio.json", [])
        resultado, _codigo = ra.consolidar(RAIZ, pasta, aut3_resultado=None, obs_estilo=None,
                                          crit_rstv=vazio, crit_shrines=vazio, identidade=None,
                                          rodar_suite=False)
        frente = resultado["por_frente"]
        exigir(frente["AUT-5"] > 0 and frente["AUT-6"] > 0,
               "frente vazia nao pode virar frente=0: %r" % frente)
        por_mod = resultado["decisao"].get("por_mod") or {}
        exigir(por_mod.get("RoguelikeSkillTreeVisualizer") and por_mod.get("BetterTooltips"),
               "a decisao do CIC-2 tem de receber os criterios das frentes: %r" % sorted(por_mod))
        chegados = [c for b in por_mod.values() for c in b.get("criterios", [])]
        gatilhos = [c for c in chegados if str(c.get("id", "")).endswith("resultado-vazio")]
        exigir(len(gatilhos) == 2,
               "as DUAS lacunas canonicas tem de chegar a decisao: %r"
               % [c.get("id") for c in chegados])
        exigir(resultado.get("frentes", {}).get("AUT-5"), "o relatorio tem de registrar o adaptador usado")
    finally:
        import shutil as _sh
        _sh.rmtree(pasta, ignore_errors=True)


def rodar():
    print("test_relatorio_aceite.py - %d caso(s)" % len(CASOS))
    for nome, fn in CASOS:
        try:
            fn()
            print("  [OK   ] %s" % nome)
        except AssertionError as erro:
            FALHAS.append((nome, str(erro)))
            print("  [FALHA] %s\n          %s" % (nome, erro))
        except Exception as erro:
            FALHAS.append((nome, "%s: %s" % (type(erro).__name__, erro)))
            print("  [ERRO ] %s\n          %s: %s" % (nome, type(erro).__name__, erro))
    print("total: %d | falhas: %d" % (len(CASOS), len(FALHAS)))
    if FALHAS:
        print("REPROVADAS: %s" % "; ".join(n for n, _ in FALHAS))
        return 1
    print("TUDO OK")
    return 0


if __name__ == "__main__":
    sys.exit(rodar())
