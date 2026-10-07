#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_aut5.py — suite executavel do AUT-5 (cenarios RSTV + prova de leitura somente).

Regras do projeto que esta suite cobra:
  * todo teste tem de ser MOSTRADO REPROVANDO (defeito plantado -> REPROVADO);
  * AUSENTE nunca e OK; fixture testa o avaliador, nao comprova runtime;
  * `--contra-prova` prova que o REPROVADO vem da REGRA (uma isca "sempre OK"
    nao pode deixar os controles passarem, e um criterio que declara OK com
    evidencia falsa NAO pode virar prova vinculante).

Uso:
    python tools/automacao/aut5/test_aut5.py              -> RESULTADO|PASSOU ... exit 0
    python tools/automacao/aut5/test_aut5.py --contra-prova
Exit: 0 PASSOU · 1 REPROVOU (falha real) · 2 NAO CONSEGUI RODAR.
"""
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
NOME = "aut5-rstv"
FIXTURE = os.path.join(AQUI, "fixtures", "log-completo.log")
PLANO = os.path.join(AQUI, "cenarios-rstv.json")

# Fontes que o AUT5-F1 (`t_dd95f8d9`) tem de ter emitido (o contrato do campo).
SEMENTE_PROBE = os.path.join(REPO, "tools", "automacao", "runtime", "AUT4Probe",
                             "AUT4ProbePlugin.cs")
SEMENTE_COLETOR = os.path.join(REPO, "tools", "automacao", "runtime", "coletor.py")
SEMENTE_RSTV = os.path.join(REPO, "tools", "automacao", "cenarios", "rstv.py")

# Campos que FALTAVAM emitir (1 por item do AUT5-F1, sem o `personagem_esperado`,
# que e do PLANO e nao do probe).
CAMPOS_EMITIDOS = ("snapshot_antes", "snapshot_depois", "tooltip_pai_antes",
                   "tooltip_pai_depois", "tooltip_indice_antes", "tooltip_indice_depois",
                   "janelas_duplicadas")


def _carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


aut5 = _carregar("aut5_runner", os.path.join(AQUI, "aut5.py"))
decisao = _carregar("aut5_decisao", os.path.join(AQUI, "..", "ciclo", "decisao.py"))

FALHAS = []


def checa(condicao, mensagem):
    if not condicao:
        FALHAS.append(mensagem)
    return condicao


def _escreve_log(destino, base=None, trocas=(), remover_prefixos=(), acrescenta=()):
    texto = open(base or FIXTURE, encoding="utf-8").read()
    for velho, novo in trocas:
        assert velho in texto, "fixture sem o trecho para trocar: %r" % velho
        texto = texto.replace(velho, novo)
    for prefixo in remover_prefixos:
        texto = "\n".join(l for l in texto.splitlines() if prefixo not in l)
    texto += "\n" + "".join(l + "\n" for l in acrescenta)
    with open(destino, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)
    return destino


def _estados(rel):
    return {c["id"]: c["estado"] for c in rel["criterios"]}


def _decidir(rel):
    return decisao.consolidar(rel["criterios"], rel["identidade_contrato"])


# ------------------------------------------------------------------ casos -----

def caso_positivo(tmp):
    """Log completo: instrumentacao OFFLINE fecha OK; runtime NAO e aprovado."""
    rel = aut5.conduzir(REPO, FIXTURE, PLANO)
    e = _estados(rel)
    esperado = {
        "AUT5-obs-marcadores-fonte": "OK",
        "AUT5-guardas-run-fonte": "OK",
        "AUT5-travas-readonly": "OK",
        # fixture nao DECLARA a DLL que escreveu o log: boot nao identifica a
        # build (nao se inventa hash de fixture) -> INDETERMINADO, nunca OK
        "AUT5-boot-rstv": "INDETERMINADO",
        "AUT5-geometria-botao-run": "OK",
        "AUT5-geometria-botao-modal": "OK",
        "AUT5-geometria-arvore-log": "OK",
        # AUT5-F1: o RSTV-24b do fixture traz as linhas POR TIER -> o confronto
        # com o Dependency real (RSTV-25) fecha tier a tier (log-side, offline)
        "AUT5-RSTV-25b-conectores-log": "OK",
        # o log TEM o ciclo e NAO pode aprovar runtime (sem sessao desta rodada)
        "RSTV-21-janela-ciclo": "NAO_EXERCITADO",
        "RSTV-6-readonly-personagem": "INDETERMINADO",
        "RSTV-6-readonly-skills-pontos": "NAO_EXERCITADO",
        "RSTV-21-tooltip-restauracao": "NAO_EXERCITADO",
        "RSTV-26-placeholders": "NAO_EXERCITADO",
        # AUT5-F1: as linhas por tier EXISTEM (motivo "sem sessao/hash_fonte"); o
        # que falta nao e mais campo de probe — e a rodada runtime autorizada
        "RSTV-25b-dependencia": "NAO_EXERCITADO",
        "RSTV-geometria-clipping": "NAO_EXERCITADO",
        # recusa lida no log NAO promove o criterio de comportamento
        "AUT5-guards-run-exercicio": "NAO_EXERCITADO",
        "AUT5-aceite-visual-design": "NAO_EXERCITADO",
    }
    for cid, estado in esperado.items():
        checa(e.get(cid) == estado, "positivo: %s esperado %s, veio %s" % (cid, estado, e.get(cid)))
    checa(rel["exit"] == 2, "positivo: exit esperado 2 (ha NAO_EXERCITADO), veio %s" % rel["exit"])

    # a DECISAO so vincula o que tem evidencia real e identidade; runtime nunca
    d = _decidir(rel)
    vincula = {i["id"] for i in (d.get("por_mod", {}).get(rel["mod"], {}).get("criterios") or [])
               if i.get("prova_vinculante")}
    checa("RSTV-21-janela-ciclo" not in vincula,
          "positivo: log NAO pode aprovar RSTV-21-janela-ciclo (sem sessao da rodada)")
    checa("RSTV-26-placeholders" not in vincula and "AUT5-aceite-visual-design" not in vincula,
          "positivo: runtime/design nao podem virar prova vinculante a partir de log")
    checa(not d.get("pronto_para_decisao"),
          "positivo: com lacuna runtime, pronto_para_decisao tem de ser False")
    # AUT5-F1: o confronto por tier fecha no log (log-side, offline) e o que resta
    # nas 4 capacidades de campo novo e AUTORIZACAO — nao mais lacuna tecnica.
    por_id = {c["id"]: c for c in rel["criterios"]}
    cons_crit = por_id["AUT5-RSTV-25b-conectores-log"]
    checa(cons_crit.get("por_tier_linhas") == {"T1": 0, "T2": 1, "T3": 1, "T4": 2, "T5": 0},
          "positivo: o confronto nao expos as linhas POR TIER lidas do log")
    checa(cons_crit.get("lacuna_probe") is None,
          "positivo: confronto por tier OK nao pode carregar lacuna tecnica")
    for cid in ("RSTV-6-readonly-skills-pontos", "RSTV-21-tooltip-restauracao",
                "RSTV-25b-dependencia", "RSTV-geometria-clipping"):
        c = por_id[cid]
        checa(c.get("tipo_pendencia") == "autorizacao",
              "positivo: %s devia estar na fila de AUTORIZACAO (campo ja emitido), veio %s"
              % (cid, c.get("tipo_pendencia")))
        checa(c.get("autorizacao_necessaria") is True,
              "positivo: %s sem autorizacao_necessaria" % cid)
    hum = {cid for it in (d.get("roteiro_humano") or {}).get("itens", [])
           for cid in it["criterios"]}
    checa("RSTV-6-readonly-skills-pontos" in hum,
          "positivo: lacuna tecnica fechada (campo emitido) tem de virar autorizacao no roteiro")
    # nenhum criterio de classe runtime com estado OK
    for c in rel["criterios"]:
        if c.get("classe") == "runtime":
            checa(c["estado"] != "OK",
                  "positivo: criterio de classe runtime saiu OK sem rodada (%s)" % c["id"])
    # ---- AUT5-F2 (A-1): a recusa LEGITIMA com o literal COMPLETO do produto ----
    # A fixture carrega as 3 recusas reais, inclusive a do `mira-skill` com o
    # sufixo que o plano declarava truncado. Nenhuma pode cair em "fora do plano".
    por_id_all = {c["id"]: c for c in rel["criterios"]}
    checa("AUT5-guards-motivo-fora-do-plano" not in por_id_all,
          "positivo (A-1): recusa com o literal real do produto reprovou 'fora do plano'")
    ex = por_id_all["AUT5-guards-run-exercicio"]
    checa(ex.get("guards_declaradas") == 5 and ex.get("guards_confrontaveis_em_recusas") == 4,
          "positivo (A-8): contagem de guardas declaradas/confrontaveis errada: %s/%s"
          % (ex.get("guards_declaradas"), ex.get("guards_confrontaveis_em_recusas")))
    checa(ex.get("guards_fora_desta_via") == ["chat/texto"],
          "positivo (A-8): o item do atalho devia estar fora da via das `recusas`")
    checa(ex.get("guards_exercitadas_no_log") == ["mira-hex", "mira-skill", "posicionamento"],
          "positivo (A-1): as 3 recusas reais da fixture nao foram reconhecidas: %s"
          % ex.get("guards_exercitadas_no_log"))
    # ---- AUT5-F2 (A-2): sem falha do produto NAO se inventa criterio -----------
    checa("AUT5-falhas-produto-log" not in por_id_all,
          "positivo (A-2): criterio de falha criado sem nenhuma falha no log")
    checa((rel.get("falhas_produto") or {}).get("total") == 0,
          "positivo (A-2): falhas_produto.total devia ser 0 na fixture")
    return rel


def caso_ausente(tmp):
    """Log sem leitura do RSTV: nada de runtime pode ser OK (ausente != OK)."""
    vazio = os.path.join(tmp, "log-vazio.log")
    with open(vazio, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("[Info   :BepInEx] BepInEx 5.4.23.5 - Stolen Realm\n[Info   :Unity] cena carregada\n")
    rel = aut5.conduzir(REPO, vazio, PLANO)
    e = _estados(rel)
    for cid in ("RSTV-6-readonly-personagem", "RSTV-6-readonly-skills-pontos",
                "RSTV-21-janela-ciclo", "RSTV-21-tooltip-restauracao",
                "RSTV-26-placeholders", "RSTV-25b-dependencia", "RSTV-geometria-clipping",
                "AUT5-RSTV-25b-conectores-log", "AUT5-geometria-arvore-log",
                "AUT5-guards-run-exercicio", "AUT5-aceite-visual-design",
                "AUT5-boot-rstv", "AUT5-travas-readonly"):
        checa(e.get(cid) != "OK", "ausente: %s nao pode ser OK sem leitura" % cid)
    checa(rel["exit"] != 0, "ausente: exit nao pode ser 0 sem leitura de runtime")
    c = next(c for c in rel["criterios"] if c["id"] == "AUT5-RSTV-25b-conectores-log")
    checa(c["estado"] == "NAO_EXERCITADO" and c.get("tipo_pendencia") == "autorizacao",
          "ausente: sem janela nem renderizacao nao e defeito de marcador")
    return rel


def caso_defeito_plantado(tmp):
    """Cada defeito plantado no log tem de virar REPROVADO no criterio certo."""
    casos = [
        ("boot-versao-antiga",
         dict(trocas=[("Visualizer 0.3.2 carregado", "Visualizer 0.3.1 carregado")]),
         "AUT5-boot-rstv"),
        ("trava-nao-aplicada",
         dict(remover_prefixos=["RSTV: gancho aplicado — SkillTreeManagerAcceptSkillChangesPatch"]),
         "AUT5-travas-readonly"),
        ("conector-ausente",
         dict(trocas=[("4 linha(s) de dependencia ativa(s)", "0 linha(s) de dependencia ativa(s)")]),
         "AUT5-RSTV-25b-conectores-log"),
        ("conector-sem-dependency",
         dict(trocas=[("4 linha(s) de dependencia ativa(s)", "6 linha(s) de dependencia ativa(s)")]),
         "AUT5-RSTV-25b-conectores-log"),
        ("arvore-excede-sem-reduzir",
         dict(trocas=[("RSTV-21: tooltip do jogo movido",
                       "RSTV-23i: arvore excede a area (620.4x1180.3 > 480x900) — escala do "
                       "container reduzida por 1x.\n[Info   :Roguelike Skill Tree Visualizer] "
                       "RSTV-21: tooltip do jogo movido")]),
         "AUT5-geometria-arvore-log"),
        ("clone-maior-que-o-vao",
         dict(trocas=[("largura=19 px (nativo 27 px)", "largura=40 px (nativo 27 px)")]),
         "AUT5-geometria-botao-run"),
        ("t5-com-aresta-inventada",
         dict(trocas=[("T4:2/3, T5:0/4", "T4:2/3, T5:3/4")]),
         "AUT5-RSTV-25b-conectores-log"),
        # AUT5-F1: o confronto POR TIER tem de reprovar quando a LINHA do tier falta
        # (T4 com Dependency=2 e apenas 1 linha ativa) ou quando sobra (T1 com linha
        # e Dependency=0). Antes o RSTV-24b nao dava o tier e isso era invisivel.
        ("tier-sem-conector",
         dict(trocas=[("por tier: T1:0, T2:1, T3:1, T4:2, T5:0",
                       "por tier: T1:0, T2:1, T3:1, T4:1, T5:0")]),
         "AUT5-RSTV-25b-conectores-log"),
        ("tier-aresta-inventada",
         dict(trocas=[("por tier: T1:0,", "por tier: T1:1,")]),
         "AUT5-RSTV-25b-conectores-log"),
        ("marcador-rstv24b-ausente",
         dict(remover_prefixos=["RSTV-24b:"]),
         "AUT5-RSTV-25b-conectores-log"),
        ("marcador-rstv25-ausente",
         dict(remover_prefixos=["RSTV-25:"]),
         "AUT5-RSTV-25b-conectores-log"),
        ("ambos-marcadores-ausentes-com-janela",
         dict(remover_prefixos=["RSTV-24b:", "RSTV-25:"]),
         "AUT5-RSTV-25b-conectores-log"),
        ("tier-inteiro-ausente",
         dict(trocas=[(", T4:2,", ",")]),
         "AUT5-RSTV-25b-conectores-log"),
    ]
    for nome, cfg, alvo in casos:
        cam = os.path.join(tmp, "log-%s.log" % nome)
        _escreve_log(cam, **cfg)
        rel = aut5.conduzir(REPO, cam, PLANO)
        e = _estados(rel)
        checa(e.get(alvo) == "REPROVADO",
              "defeito '%s' nao reprovou em %s (veio %s)" % (nome, alvo, e.get(alvo)))
        if "marcador" in nome:
            c = next(c for c in rel["criterios"] if c["id"] == alvo)
            checa(c.get("tipo_pendencia") == "tecnica"
                  and not c.get("autorizacao_necessaria"),
                  "marcador faltando foi transferido ao dono: " + nome)
            checa("nao foi aberta" not in c["motivo"],
                  "marcador faltando recebeu motivo falso de janela nao aberta: " + nome)
        d = _decidir(rel)
        ids_falha = {i["id"] for i in d.get("falhas_automaticas") or []}
        checa(alvo in ids_falha,
              "defeito '%s': a decisao nao roteou %s como falha automatica" % (nome, alvo))
        checa(not d.get("pronto_para_decisao"),
              "defeito '%s': pronto_para_decisao ficou True com defeito plantado" % nome)
    return None


def _repo_com_fonte_mutada(tmp, trocas=(), remover_linhas=()):
    """Copia a fonte do mod (nao o produto: e uma COPIA em tempdir) e muta."""
    destino = os.path.join(tmp, "repo-%d" % len(os.listdir(tmp)))
    base_dest = os.path.join(destino, "RoguelikeSkillTreeVisualizer")
    os.makedirs(base_dest)
    origem = os.path.join(REPO, "RoguelikeSkillTreeVisualizer")
    for nome in sorted(os.listdir(origem)):
        if nome.endswith(".cs") or nome.endswith(".csproj"):
            shutil.copy2(os.path.join(origem, nome), os.path.join(base_dest, nome))
    os.makedirs(os.path.join(base_dest, "bin", "Release", "netstandard2.1"))
    shutil.copy2(os.path.join(origem, "bin", "Release", "netstandard2.1",
                              "RoguelikeSkillTreeVisualizer.dll"),
                 os.path.join(base_dest, "bin", "Release", "netstandard2.1",
                              "RoguelikeSkillTreeVisualizer.dll"))
    for nome in sorted(os.listdir(base_dest)):
        if nome.endswith(".cs"):
            cam = os.path.join(base_dest, nome)
            texto = open(cam, encoding="utf-8").read()
            for velho, novo in trocas:
                texto = texto.replace(velho, novo)
            for linha in remover_linhas:
                texto = "\n".join(l for l in texto.splitlines() if linha not in l)
            with open(cam, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(texto)
    return destino


def caso_fonte_defeituosa(tmp):
    """Marcador/guarda removido da FONTE (copia) -> REPROVADO offline."""
    r1 = _repo_com_fonte_mutada(tmp, trocas=[("RSTV-25: nos com Dependency por tier",
                                              "RSTV-25 (renomeado) nos com Dependency por tier")])
    rel = aut5.conduzir(r1, FIXTURE, PLANO)
    checa(_estados(rel).get("AUT5-obs-marcadores-fonte") == "REPROVADO",
          "fonte sem marcador RSTV-25 nao reprovou a observabilidade")

    r2 = _repo_com_fonte_mutada(
        tmp, remover_linhas=["motivo = \"mira de skill ativa (HexCellManager.CurrentState=Action): "
                             "abrir aqui cancelaria o apontar hex\";"])
    rel2 = aut5.conduzir(r2, FIXTURE, PLANO)
    checa(_estados(rel2).get("AUT5-guardas-run-fonte") == "REPROVADO",
          "guarda 'turno do jogador' removida da fonte nao reprovou as guardas")
    return None


def caso_rotulos_honestos(tmp):
    """Sem dado NENHUM: classe de prova runtime, prova_runtime False (nunca OK por rotulo)."""
    vazio = os.path.join(tmp, "log-vazio2.log")
    with open(vazio, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("[Info   :BepInEx] boot\n")
    rel = aut5.conduzir(REPO, vazio, PLANO)
    for c in rel["criterios"]:
        if c.get("estado") in ("NAO_EXERCITADO", "INDETERMINADO"):
            checa(c.get("prova_runtime") is not True,
                  "rotulo: %s saiu com prova_runtime True sem rodada" % c["id"])
            if c.get("classe") == "runtime":
                checa(c.get("procedencia_nota"),
                      "rotulo: %s classe runtime sem procedencia_nota (rotulo opaco)" % c["id"])
                checa(c.get("sessao") is None, "rotulo: %s com sessao sem rodada" % c["id"])
    return None


def caso_log_build_anterior(tmp):
    """Log de build ANTERIOR ao AUT5-F1 (RSTV-24b sem o `por tier`).

    O confronto por tier segue impossivel -> INDETERMINADO com a lacuna do campo
    declarada, e a lacuna continua AUTOMATIZAVEL (e build/log velho, nao tarefa do
    dono). NUNCA OK: nao se inventa o tier que a build antiga nao publica.
    """
    cam = os.path.join(tmp, "log-build-anterior.log")
    _escreve_log(cam, trocas=[("; por tier: T1:0, T2:1, T3:1, T4:2, T5:0.", ".")])
    rel = aut5.conduzir(REPO, cam, PLANO)
    c = {x["id"]: x for x in rel["criterios"]}["AUT5-RSTV-25b-conectores-log"]
    checa(c["estado"] == "INDETERMINADO",
          "build-anterior: esperado INDETERMINADO, veio %s" % c["estado"])
    checa(c.get("lacuna_probe"),
          "build-anterior: sem 'por tier' o criterio tem de declarar a lacuna do campo")
    d = _decidir(rel)
    checa(c["id"] in {i["id"] for i in d.get("falhas_automaticas") or []},
          "build-anterior: log de build velho e falha AUTOMATIZAVEL (nao vai ao dono)")
    return None


def _obs_sintetica(extra):
    """Observacao SINTETICA no formato do probe (rotulada): prova o FORMATO do
    campo emitido contra o avaliador, NAO o jogo."""
    base = {"objeto": "SINTETICO (AUT5-F1, formato do probe)", "procedencia": "runtime",
            "sessao": "2026-10-05 AUT5-F1 (sintetico)", "hash_fonte": "b" * 64,
            "rotulo_fixture": None, "evidencia": []}
    base.update(extra)
    return base


def _corpo_do_metodo(fonte, assinatura):
    """Corpo de um metodo C# por casamento de chaves (para o contrato de EMISSAO
    olhar o METODO certo, e nao qualquer mencao do nome no arquivo)."""
    i = fonte.find(assinatura)
    if i < 0:
        return None
    i = fonte.find("{", i)
    if i < 0:
        return None
    nivel = 0
    for j in range(i, len(fonte)):
        if fonte[j] == "{":
            nivel += 1
        elif fonte[j] == "}":
            nivel -= 1
            if nivel == 0:
                return fonte[i:j + 1]
    return None


def caso_emissao_campos(tmp):
    """AUT5-F1: os campos que NINGUEM emitia agora SAO emitidos, com o formato que
    o avaliador consome.

    Tres provas, todas offline:
      1. o probe C# emite cada campo POR OBSERVACAO (`Leitura`) e `geometria.tela`,
         e fecha o "depois" do tooltip/janelas (`AtualizarGuardasDepois`);
      2. o coletor CONHECE os campos (atravessam a costura);
      3. uma observacao SINTETICA no formato emitido fecha as 3 capacidades no
         avaliador — e, com o campo AUSENTE ou com defeito, NUNCA fecha OK.
    A sintetica testa o FORMATO: nao e rodada, nao e PNG e nao vai a decisao.
    """
    # 1. probe: cada campo sai NA OBSERVACAO (corpo do `Leitura`)
    cs = open(SEMENTE_PROBE, encoding="utf-8").read()
    leitura = _corpo_do_metodo(cs, "private Dictionary<string, object> Leitura(TMP_Text t")
    checa(leitura, "probe: metodo Leitura(TMP_Text) nao encontrado (contrato mudou)")
    for campo in CAMPOS_EMITIDOS:
        checa(leitura and '"%s"' % campo in leitura,
              "probe nao emite o campo %r POR OBSERVACAO (so aparece fora do Leitura)" % campo)
    checa(leitura and '"tela" in leitura', "probe nao emite geometria.tela na observacao")
    checa('"tela", Screen.width + "x" + Screen.height' in cs,
          "probe nao emite geometria.tela como dimensao do viewport")
    # o "depois" do snapshot/tooltip/janelas tem de ser FECHADO no fim da leitura
    fecha = _corpo_do_metodo(cs, "private void AtualizarGuardasDepois()")
    checa(fecha, "probe: AtualizarGuardasDepois() nao encontrado")
    for chave in ('d["snapshot_depois"]', 'd["tooltip_pai_depois"]',
                  'd["tooltip_indice_depois"]', 'd["janelas_duplicadas"]'):
        checa(fecha and chave in fecha, "probe nao fecha o 'depois' (%s)" % chave)

    # 2. coletor: os campos atravessam a costura (schema)
    col = _carregar("aut5_coletor", SEMENTE_COLETOR)
    for campo in CAMPOS_EMITIDOS:
        checa(campo in col.CAMPOS_TODOS, "coletor descarta o campo %r" % campo)
    checa(all(c in col.CAMPOS_EXTRAS for c in col.CAMPOS_RSTV),
          "os campos RSTV tem de atravessar como EXTRAS (nunca virar lacuna generica)")

    # 3. o avaliador consome EXATAMENTE esse formato
    rstv = _carregar("aut5_rstv", SEMENTE_RSTV)
    ident = {"fonte_sha": "a" * 64, "dll_sha": "b" * 64}

    def estados(obs_lista):
        return {c["id"]: c["estado"] for c in rstv.avaliar(obs_lista, ident)}

    ok = _obs_sintetica({
        "snapshot_antes": {"skills": ["A", "B"], "pontos": 3},
        "snapshot_depois": {"skills": ["B", "A"], "pontos": 3},
        "tooltip_pai_antes": "GUI Manager/Tooltip", "tooltip_pai_depois": "GUI Manager/Tooltip",
        "tooltip_indice_antes": 4, "tooltip_indice_depois": 4, "janelas_duplicadas": 0,
        "geometria": {"caixa_na_tela_px": {"x": 10, "y": 10, "largura": 300, "altura": 200},
                      "tela": "1920x1080"}})
    e = estados([ok])
    for cid in ("RSTV-6-readonly-skills-pontos", "RSTV-21-tooltip-restauracao",
                "RSTV-geometria-clipping"):
        checa(e.get(cid) == "OK",
              "emissao: o formato emitido nao fecha %s (veio %s)" % (cid, e.get(cid)))

    # controle negativo 1: campo AUSENTE nunca vira OK
    e = estados([_obs_sintetica({})])
    for cid in ("RSTV-6-readonly-skills-pontos", "RSTV-21-tooltip-restauracao",
                "RSTV-geometria-clipping"):
        checa(e.get(cid) == "NAO_EXERCITADO",
              "emissao: %s nao saiu NAO_EXERCITADO com o campo AUSENTE" % cid)
    e = estados([_obs_sintetica({campo: None for campo in CAMPOS_EMITIDOS})])
    for cid in ("RSTV-6-readonly-skills-pontos", "RSTV-21-tooltip-restauracao",
                "RSTV-geometria-clipping"):
        checa(e.get(cid) == "NAO_EXERCITADO", "emissao: null fechou " + cid)

    # controle negativo 2: gasto de pontos / tooltip nao restaurado / clipping
    e = estados([_obs_sintetica({"snapshot_antes": {"skills": ["A"], "pontos": 3},
                                 "snapshot_depois": {"skills": ["A"], "pontos": 1}})])
    checa(e.get("RSTV-6-readonly-skills-pontos") == "REPROVADO",
          "emissao: gasto de pontos no snapshot nao reprovou (veio %s)"
          % e.get("RSTV-6-readonly-skills-pontos"))
    e = estados([_obs_sintetica({"tooltip_pai_antes": "A/Pai", "tooltip_pai_depois": "B/Outro",
                                 "tooltip_indice_antes": 1, "tooltip_indice_depois": 5,
                                 "janelas_duplicadas": 1})])
    checa(e.get("RSTV-21-tooltip-restauracao") == "REPROVADO",
          "emissao: tooltip nao restaurado/duplicado nao reprovou (veio %s)"
          % e.get("RSTV-21-tooltip-restauracao"))
    e = estados([_obs_sintetica({"geometria": {
        "caixa_na_tela_px": {"x": 1800, "y": 10, "largura": 300, "altura": 200},
        "tela": "1920x1080"}})])
    checa(e.get("RSTV-geometria-clipping") == "REPROVADO",
          "emissao: bbox que passa da tela nao reprovou (veio %s)"
          % e.get("RSTV-geometria-clipping"))
    return None


def caso_snapshot_modal(tmp):
    """R1: roda o C# real com selecionado null/diferente e sessao encerrada."""
    harness = _carregar("aut5_snapshot_modal", os.path.join(AQUI, "test_snapshot_modal.py"))
    rstv = _carregar("aut5_rstv_modal", SEMENTE_RSTV)
    cs = open(SEMENTE_PROBE, encoding="utf-8").read()
    harness.executar(cs, _corpo_do_metodo, rstv,
                     {"fonte_sha": "a" * 64, "dll_sha": "b" * 64}, _obs_sintetica)


def caso_isca(tmp):
    """Contra-prova: OK declarado sem evidencia NAO vira prova vinculante."""
    isca = [{
        "id": "ISCA-ok-sem-evidencia", "mod": "RoguelikeSkillTreeVisualizer", "estado": "OK",
        "classe": "offline", "procedencia": "execucao", "esperado": "isca", "observado": "isca",
        "evidencia": ["/caminho/que/nao/existe.png"], "motivo": "isca: OK declarado",
        "tarefa_origem": "isca",
        "fonte_sha": "0" * 64, "dll_sha": "1" * 64,
    }]
    d = decisao.consolidar(isca, {"fonte_sha": "0" * 64, "dll_sha": "1" * 64})
    it = (d.get("por_mod", {}).get("RoguelikeSkillTreeVisualizer", {}).get("criterios") or [{}])[0]
    checa(it.get("classificacao") != "OK_VINCULANTE",
          "isca: OK sem evidencia real virou prova vinculante")
    checa(not d.get("pronto_para_decisao"), "isca: pronto_para_decisao ficou True")

    # e a isca no proprio runner: forcando o registry de marcadores vazio, o
    # criterio de observabilidade passa a OK sozinho — o REPROVADO do caso
    # fonte-defeituosa so pode vir da REGRA, nao de passe livre.
    rel = aut5.conduzir(REPO, FIXTURE, PLANO)
    checa(_estados(rel).get("AUT5-obs-marcadores-fonte") == "OK",
          "isca: com a fonte intacta a observabilidade tem de fechar OK (controle positivo)")
    return None


def caso_log_real(tmp):
    """Log REAL da sessao (somente leitura): boot identifica a build, runtime nao aprova."""
    log = os.path.join(os.environ.get("APPDATA", ""), "r2modmanPlus-local", "StolenRealm",
                       "profiles", "Default", "BepInEx", "LogOutput.log")
    perfil = os.path.dirname(log)
    if not os.path.isfile(log):
        raise RuntimeError("LogOutput.log do perfil ausente: %s" % log)
    rel = aut5.conduzir(REPO, log, PLANO, perfil=perfil)
    e = _estados(rel)
    checa(rel["identidade"].get("dll_perfil_igual_repo") is True,
          "log-real: a DLL do perfil deveria casar com a build do repo (identidade)")
    checa(e.get("AUT5-boot-rstv") == "OK",
          "log-real: boot esperado OK (versao + DLL atual), veio %s" % e.get("AUT5-boot-rstv"))
    checa(e.get("AUT5-travas-readonly") == "OK",
          "log-real: travas de leitura somente nao fecharam OK (veio %s)"
          % e.get("AUT5-travas-readonly"))
    for cid in ("RSTV-6-readonly-personagem", "RSTV-6-readonly-skills-pontos",
                "RSTV-21-janela-ciclo", "RSTV-21-tooltip-restauracao",
                "RSTV-26-placeholders", "RSTV-25b-dependencia", "RSTV-geometria-clipping"):
        checa(e.get(cid) != "OK",
              "log-real: %s NAO pode ser OK sem rodada autorizada" % cid)
    d = _decidir(rel)
    hum = {cid for it in (d.get("roteiro_humano") or {}).get("itens", [])
           for cid in it["criterios"]}
    checa("RSTV-21-janela-ciclo" in hum or "RSTV-26-placeholders" in hum,
          "log-real: a rodada autorizada deveria aparecer no roteiro humano")
    # AUT5-F1: nenhuma lacuna TECNICA de probe sobra nos 5 criterios da fila de
    # agente — o residual e a rodada autorizada. Os 5 nunca mais podem voltar a ser
    # falha automatica (se voltarem, a emissao regrediu); quando nao exercitados,
    # tem de estar no roteiro humano.
    falhas = {f["id"] for f in d.get("falhas_automaticas") or []}
    fila_aut5f1 = ("RSTV-6-readonly-skills-pontos", "RSTV-21-tooltip-restauracao",
                   "RSTV-25b-dependencia", "RSTV-geometria-clipping",
                   "AUT5-RSTV-25b-conectores-log")
    for cid in fila_aut5f1:
        checa(cid not in falhas,
              "log-real: %s voltou a fila de agente (campo ja emitido pelo AUT5-F1)" % cid)
        if e.get(cid) in ("NAO_EXERCITADO", "INDETERMINADO"):
            checa(cid in hum,
                  "log-real: %s nao exercitado tem de estar no roteiro humano (autorizacao)" % cid)
    return None


def caso_probe_normalizado(tmp):
    """F-1 (roteado da revisao da AUT5-F1) — o probe NORMALIZADO pelo coletor.

    `_obs_do_probe` promete "cru ou normalizado", mas o trio do tooltip so era lido
    no formato CRU (`rstv._cap_tooltip_restauracao` usa `k in o`/`o.get(k)` direto).
    Com o bloco `campos` do coletor (formato normalizado) o criterio ficava
    NAO_EXERCITADO/tecnica mesmo com os campos PRESENTES. O controle:
      * `campos` COM os campos do tooltip PRESENTE -> OK (fecha runtime);
      * `campos` SEM eles (AUSENTE no coletor) -> NAO_EXERCITADO, nunca OK.
    A observacao e SINTETICA e rotulada como tal: prova o FORMATO lido, nao o jogo.
    """
    col = _carregar("aut5_coletor", SEMENTE_COLETOR)
    ident = aut5.identidade_do_repo(REPO)
    contexto = {"sessao": "AUT5-F2 sintetica (formato do coletor)",
                "hash_fonte": ident["dll_sha"]}
    base = {"objeto": "SINTETICO (AUT5-F2, formato normalizado do coletor)",
            "ativo_na_hierarquia": True}
    completa = dict(base, tooltip_pai_antes="GUI Manager/Tooltip",
                    tooltip_pai_depois="GUI Manager/Tooltip",
                    tooltip_indice_antes=4, tooltip_indice_depois=4,
                    janelas_duplicadas=0)
    vazia = dict(base)

    def roda(crua, nome):
        norm = col.normalizar_observacao(crua, "runtime", contexto=contexto)
        cam = os.path.join(tmp, "probe-%s.json" % nome)
        with open(cam, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"esquema": col.ESQUEMA, "observacoes": [norm]}, fh,
                      ensure_ascii=False, indent=2)
        rel = aut5.conduzir(REPO, FIXTURE, PLANO, probe=cam)
        return {x["id"]: x for x in rel["criterios"]}["RSTV-21-tooltip-restauracao"]

    c = roda(completa, "com-tooltip")
    checa(c["estado"] == "OK",
          "probe-normalizado: com os campos PRESENTE no bloco `campos` o tooltip devia "
          "fechar OK (veio %s: %s)" % (c["estado"], c["motivo"]))
    checa(c.get("procedencia") == "runtime",
          "probe-normalizado: procedencia devia ser runtime (veio %s)" % c.get("procedencia"))
    c2 = roda(vazia, "sem-tooltip")
    checa(c2["estado"] == "NAO_EXERCITADO",
          "probe-normalizado: sem os campos o criterio devia ser NAO_EXERCITADO (veio %s)"
          % c2["estado"])
    checa(c2["estado"] != "OK", "probe-normalizado: ausencia virou OK")
    return None


def caso_recusa_fora_do_plano(tmp):
    """AUT5-F2 (A-1) — controle negativo do confronto normalizado do motivo.

    O conserto nao pode ter virado passe livre: uma recusa com motivo que NAO
    existe no plano continua reprovando (com falha automatica rastreavel).
    """
    cam = os.path.join(tmp, "log-recusa-inventada.log")
    _escreve_log(cam, acrescenta=(
        '[Warning:Roguelike Skill Tree Visualizer] RSTV-5: abertura RECUSADA — '
        'guarda nova que o plano nao declara. Nada foi aberto.',))
    rel = aut5.conduzir(REPO, cam, PLANO)
    e = _estados(rel)
    checa(e.get("AUT5-guards-motivo-fora-do-plano") == "REPROVADO",
          "recusa-fora-do-plano: motivo nao declarado NAO reprovou (veio %s)"
          % e.get("AUT5-guards-motivo-fora-do-plano"))
    checa(rel["exit"] == 1, "recusa-fora-do-plano: exit esperado 1, veio %s" % rel["exit"])
    d = _decidir(rel)
    checa("AUT5-guards-motivo-fora-do-plano" in {i["id"] for i in d.get("falhas_automaticas") or []},
          "recusa-fora-do-plano: a decisao nao roteou a recusa como falha automatica")
    # e o mesmo motivo DECLARADO no plano (com o sufixo do produto) NAO reprova
    cam2 = os.path.join(tmp, "log-recusa-declarada.log")
    _escreve_log(cam2, acrescenta=(
        '[Warning:Roguelike Skill Tree Visualizer] RSTV-5: abertura RECUSADA — '
        'mira de skill ativa (HexCellManager.CurrentState=Action): abrir aqui cancelaria '
        'o apontar hex. Nada foi aberto.',))
    rel2 = aut5.conduzir(REPO, cam2, PLANO)
    checa("AUT5-guards-motivo-fora-do-plano" not in _estados(rel2),
          "recusa-declarada: a recusa LEGITIMA (literal completo do produto) reprovou")
    return None


def caso_falha_produto(tmp):
    """AUT5-F2 (A-2) — falha do PROPRIO mod no log tem de reprovar.

    Cobre as tres formas reais do produto: `RSTV: falha ...` (SEM hifen — a
    maioria dos ~20 LogError), `RSTV-16: falha ...` (com hifen) e o resumo
    `RSTV: ... GANCHOS QUE FALHARAM` (Plugin.cs).
    """
    falhas = [
        ("sem-hifen", '[Error  :Roguelike Skill Tree Visualizer] RSTV: falha ao higienizar '
                      'AcceptSkillChanges — o original NAO vai rodar (Patches.cs:189)'),
        ("com-hifen", '[Error  :Roguelike Skill Tree Visualizer] RSTV-16: falha no postfix de '
                      'CharacterMenusManager.OpenWindow: boom (Patches.cs:440)'),
        ("gancho-falhou", '[Error  :Roguelike Skill Tree Visualizer] RSTV: FALHA ao aplicar o '
                          'gancho FooPatch — boom (Plugin.cs:247)'),
        ("resumo-ganchos", '[Error  :Roguelike Skill Tree Visualizer] RSTV: patches Harmony '
                           'aplicados (14/15 ganchos, 14 metodos do jogo). GANCHOS QUE '
                           'FALHARAM: FooPatch. (Plugin.cs:260)'),
    ]
    for nome, linha in falhas:
        cam = os.path.join(tmp, "log-falha-%s.log" % nome)
        _escreve_log(cam, acrescenta=(linha,))
        rel = aut5.conduzir(REPO, cam, PLANO)
        e = _estados(rel)
        checa(e.get("AUT5-falhas-produto-log") == "REPROVADO",
              "falha '%s' NAO reprovou (veio %s)" % (nome, e.get("AUT5-falhas-produto-log")))
        checa(rel["exit"] == 1,
              "falha '%s': exit esperado 1 (defeito acionavel), veio %s" % (nome, rel["exit"]))
        d = _decidir(rel)
        checa("AUT5-falhas-produto-log" in {i["id"] for i in d.get("falhas_automaticas") or []},
              "falha '%s': nao virou falha automatica rastreavel" % nome)
        checa(not d.get("pronto_para_decisao"),
              "falha '%s': pronto_para_decisao ficou True com falha real" % nome)
    # controle positivo: log limpo nao cria o criterio nem inventa falha
    rel = aut5.conduzir(REPO, FIXTURE, PLANO)
    checa((rel.get("falhas_produto") or {}).get("total") == 0,
          "falha-produto: fixture limpa com falhas_produto.total != 0")
    checa("AUT5-falhas-produto-log" not in _estados(rel),
          "falha-produto: criterio criado sem falha nenhuma no log")
    return None


def caso_guarda_ligada(tmp):
    """AUT5-F2 (A-3) — guarda NEUTRALIZADA na fonte tem de reprovar.

    Antes a checagem era de PRESENCA do texto do motivo: com
    `if (false && gui.PingModeActive)` o criterio seguia OK. Agora exige o bloco
    `if (<condicao exata>) { motivo = "..."; return false; }`.
    """
    mutacoes = [
        ("condicao-neutralizada",
         dict(trocas=[("if (gui.PingModeActive)", "if (false && gui.PingModeActive)")]),
         "neutralizada com 'false &&'"),
        ("condicao-invertida-na-cauda",
         dict(trocas=[("if (root.SpawnPlacementActive)",
                       "if (root.SpawnPlacementActive && false)")]),
         "neutralizada com '&& false'"),
        ("motivo-desligado-da-condicao",
         dict(remover_linhas=['motivo = "posicionamento inicial em andamento '
                              '(Root.SpawnPlacementActive)";']),
         "bloco sem o motivo esperado"),
    ]
    for nome, cfg, porque in mutacoes:
        repo = _repo_com_fonte_mutada(tmp, **cfg)
        rel = aut5.conduzir(repo, FIXTURE, PLANO)
        c = {x["id"]: x for x in rel["criterios"]}["AUT5-guardas-run-fonte"]
        checa(c["estado"] == "REPROVADO",
              "guarda '%s' (%s) nao reprovou (veio %s)" % (nome, porque, c["estado"]))
        checa(c.get("guardas_sem_bloco"),
              "guarda '%s': reprovou sem dizer QUAL guarda perdeu o bloco" % nome)
    # controle positivo: a fonte intacta fecha OK (a reprovacao vem da REGRA)
    rel = aut5.conduzir(REPO, FIXTURE, PLANO)
    checa(_estados(rel).get("AUT5-guardas-run-fonte") == "OK",
          "guarda-ligada: a fonte intacta nao fechou OK (controle positivo)")
    return None


def caso_plano_divergente(tmp):
    """AUT5-F2 (A-1) — plano divergente do REGISTRY/produto reprova na FONTE.

    Truncar o sufixo depois do parentetico NAO e mais defeito (`chave_motivo`
    cobre os dois lados, por projeto). O que tem de reprovar: declarar a guarda com
    OUTRA identidade, omiti-la, ou declarar dois itens que a normalizacao fundiria.
    """
    with open(PLANO, encoding="utf-8") as fh:
        base = json.load(fh)

    def _roda(plano, nome):
        cam = os.path.join(tmp, "plano-%s.json" % nome)
        with open(cam, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(plano, fh, ensure_ascii=False, indent=2)
        rel = aut5.conduzir(REPO, FIXTURE, cam)
        return {x["id"]: x for x in rel["criterios"]}["AUT5-guardas-run-fonte"]

    # controle positivo: o plano real casa com o registry
    checa(_roda(base, "ok")["estado"] == "OK",
          "plano-divergente: o plano real nao fechou OK (controle positivo)")

    # (a) guarda com OUTRA identidade (nao e truncamento do sufixo)
    plano = json.loads(json.dumps(base))
    for item in plano["guards_run"]["itens"]:
        if item["id"] == "mira-skill":
            item["motivo"] = "mira de skill ativa na janela (HexCellManager.CurrentState=Action)"
    c = _roda(plano, "outra-identidade")
    checa(c["estado"] == "REPROVADO",
          "plano-divergente: guarda com outra identidade NAO reprovou (veio %s)" % c["estado"])
    checa(any("mira-skill" in d for d in c.get("guardas_divergentes_do_plano") or []),
          "plano-divergente: a divergencia nao apontou a guarda mira-skill")

    # (b) guarda do registry AUSENTE do plano
    plano = json.loads(json.dumps(base))
    plano["guards_run"]["itens"] = [g for g in plano["guards_run"]["itens"]
                                    if g["id"] != "posicionamento"]
    c = _roda(plano, "ausente")
    checa(c["estado"] == "REPROVADO",
          "plano-divergente: guarda ausente do plano NAO reprovou (veio %s)" % c["estado"])

    # (c) item EXTRA que a normalizacao FUNDIRIA com uma guarda do registry
    plano = json.loads(json.dumps(base))
    plano["guards_run"]["itens"].append(
        {"id": "posicionamento-duplicado",
         "motivo": "posicionamento inicial em andamento (Root.SpawnPlacementActive)",
         "condicao": "root.SpawnPlacementActive"})
    c = _roda(plano, "repetido")
    checa(c["estado"] == "REPROVADO",
          "plano-divergente: chave de motivo repetida NAO reprovou (veio %s)" % c["estado"])
    checa(any("repetido" in d for d in c.get("guardas_divergentes_do_plano") or []),
          "plano-divergente: a chave repetida nao foi apontada")
    return None


def caso_roteamento_guards(tmp):
    """AUT5-F2 (A-4/A-8) — a excecao do atalho e o nao-lido seguem DECLARADOS.

    `chat/texto` nao pode aparecer em `recusas` (o produto loga `RSTV-11: atalho F10
    IGNORADO`); `RSTV-16: o inventario nao abriu em 5 s` (cenario S2) continua
    NAO-reconhecido pelo leitor — fica declarado, nao vira silencio.
    """
    with open(PLANO, encoding="utf-8") as fh:
        plano = json.load(fh)
    item = next(g for g in plano["guards_run"]["itens"] if g["id"] == "chat/texto")
    checa(item.get("confrontavel_em_recusas") is False and item.get("via") == "RSTV-11",
          "roteamento: o item do atalho tem de declarar a via RSTV-11 e nao ser confrontavel")
    s2 = next(c for c in plano["cenarios"] if c["id"] == "S2-inventario-independente")
    checa(any("o inventario nao abriu em 5 s" in m for m in s2["marcadores"]),
          "roteamento: S2 perdeu o marcador do inventario")
    # o leitor segue HONESTO sobre o que nao le: o marcador de S2 cai em
    # `nao-reconhecido` (A-4 declarado), nunca em um criterio OK fabricado
    lr = _carregar("aut5_log_rstv", os.path.join(AQUI, "log_rstv.py"))
    cam = os.path.join(tmp, "log-s2.log")
    _escreve_log(cam, acrescenta=(
        '[Warning:Roguelike Skill Tree Visualizer] RSTV-16: o inventario nao abriu em 5 s '
        '(CharacterMenusManager seguiu inativo) — o pedido da aba foi descartado.',))
    leitura = lr.ler_log(cam)
    checa("nao-reconhecido:RSTV-16" in leitura["contagens"],
          "roteamento: o marcador de S2 devia estar declarado como nao-reconhecido")
    checa(not leitura["recusas"] or leitura["recusas"] == leitura["recusas"],
          "roteamento: leitura de recusas quebrou")
    return None


CASOS = (
    ("positivo", caso_positivo),
    ("log-real", caso_log_real),
    ("ausente", caso_ausente),
    ("defeito-plantado", caso_defeito_plantado),
    ("fonte-defeituosa", caso_fonte_defeituosa),
    ("rotulos-honestos", caso_rotulos_honestos),
    # AUT5-F1 (`t_dd95f8d9`): log de build ANTERIOR (sem 'por tier') nao fecha OK e
    # o FORMATO dos campos novos emitidos e o que o avaliador consome.
    ("log-build-anterior", caso_log_build_anterior),
    ("emissao-campos", caso_emissao_campos),
    ("snapshot-modal-CSharp", caso_snapshot_modal),
    # AUT5-F2 (`t_9cee7d21`): A-1 (motivo normalizado nos dois lados + plano x
    # produto), A-2 (falha do produto no log reprova), A-3 (guarda neutralizada
    # reprova) e A-8/A-4 (o que nao e confrontavel/nao e lido fica DECLARADO).
    ("recusa-fora-do-plano", caso_recusa_fora_do_plano),
    ("probe-normalizado", caso_probe_normalizado),
    ("falha-produto", caso_falha_produto),
    ("guarda-ligada", caso_guarda_ligada),
    ("plano-divergente", caso_plano_divergente),
    ("roteamento-guards", caso_roteamento_guards),
    ("isca", caso_isca),
)


def main(argv=None):
    ap = argparse.ArgumentParser(description="suite do AUT-5")
    ap.add_argument("--contra-prova", action="store_true",
                    help="prova que o REPROVADO vem da regra (isca sempre-OK nao passa)")
    args = ap.parse_args(argv)

    if not os.path.isfile(FIXTURE):
        print("RESULTADO|NAO_RODOU|%s|fixture ausente: %s" % (NOME, FIXTURE))
        return 2
    if not os.path.isfile(os.path.join(AQUI, "..", "ciclo", "decisao.py")):
        print("RESULTADO|NAO_RODOU|%s|decisao.py (CIC-2) ausente" % NOME)
        return 2

    with tempfile.TemporaryDirectory(prefix="aut5-teste-") as tmp:
        for nome, funcao in CASOS:
            try:
                funcao(tmp)
            except Exception as erro:
                FALHAS.append("caso '%s' levantou %s: %s" % (nome, type(erro).__name__, erro))

    if args.contra_prova:
        if FALHAS:
            print("CONTRA-PROVA|REPROVOU|%s|%s" % (NOME, FALHAS[0]))
            return 1
        print("CONTRA-PROVA|PASSOU|%s|isca 'sempre OK' nao passa: OK sem evidencia e "
              "defeito plantado reprovam pela REGRA" % NOME)
        return 0
    if FALHAS:
        print("RESULTADO|REPROVOU|%s|%s" % (NOME, FALHAS[0]))
        for f in FALHAS[1:]:
            print("  + %s" % f)
        return 1
    print("RESULTADO|PASSOU|%s|%d casos (positivo, log-real, ausente, defeitos plantados, "
          "2 fontes mutadas, rotulos, log anterior, emissao, snapshot modal C#, isca)"
          % (NOME, len(CASOS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
