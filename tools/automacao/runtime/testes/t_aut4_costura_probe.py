#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-5/CIC-5/COR-AUT4 — COSTURA probe -> coletor (B1/B2/B3 da AUT-4R + A2/A3/A4 da AUT-4R2).

Prova, contra o JSON REAL que o probe grava (`aut4probe.json`, fixture rotulada no
formato exato do C#):

  B1 — `sessao`/`hash_fonte` ficam no TOPO do JSON; a costura os injeta em cada
       observacao (sem isso, `normalizar_observacao(...,"runtime")` RECUSA);
  B2 — os 5 campos uteis que o schema descartava (componente, visivel_na_tela,
       shader_suportado, tamanho_fonte, nota_texto_renderizado) ATRAVESSAM;
  B3 — objeto nomeado INATIVO nao vira lacuna por `texto_renderizado` (o TMP so
       preenche o mesh quando ativo): o fallback e DECLARADO, nao falso OK visual.

COR-AUT4 (AUT-4R2):
  A2 — `campos_alvo` GOVERNA o veredito: alvo AUSENTE/NAO_APLICAVEL => lacuna e
       INCOMPLETO (o fallback e informacao, nunca satisfacao do criterio); alvo
       fora do schema => PlanoInvalido (nao "fecha" por engano).
  A3 — rotulo de fixture LIDO DO ARTEFATO tem precedencia sobre a intencao do
       chamador: nunca e consolidado como runtime.
  A4 — `status`/`fase` terminal de falha do probe rebaixa o resultado: sem
       `status=CONCLUIDO` o desfecho NAO e CONFIRMADA e o exit != 0.

Controle negativo no mesmo teste: um objeto ATIVO sem `texto_renderizado` CONTINUA
sendo lacuna (nao se maquia com o fallback dos inativos).
"""
import json
import os
import tempfile

import comum as C

META = {
    "nome": "aut4-costura-probe",
    "categoria": "pura",
    "requer": [],
    "descricao": "topo->observacao (B1), extras preservados (B2), alvo por cenario governa o "
                 "veredito (A2), procedencia do artefato vence (A3), status de falha rebaixa (A4)",
}

EXTRAS = ("componente", "visivel_na_tela", "shader_suportado", "tamanho_fonte",
          "nota_texto_renderizado")

ALVOS_SEM_RENDER = ["objeto", "texto_bruto", "fonte", "material", "shader", "keywords",
                    "cores", "geometria", "owners"]
ALVOS_COM_RENDER = ALVOS_SEM_RENDER + ["texto_renderizado"]


def _escrever(dados):
    fd, caminho = tempfile.mkstemp(prefix="aut5-probe-", suffix=".json")
    os.close(fd)
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False)
    return caminho


def _saida_runtime(fx, status="CONCLUIDO", fase="concluido"):
    """Saida do probe com procedencia runtime (a observacao ATIVA, com todos os campos).

    A inativa (com o fallback NAO_APLICAVEL) entra so quando o caso pede — o caminho
    feliz nao pode carregar um alvo que nao foi lido.
    """
    obs = []
    for o in fx["observacoes"][:1]:
        copia = {k: v for k, v in o.items() if k not in ("sessao", "hash_fonte")}
        obs.append(copia)
    dados = {"esquema": "AUT-4/1", "procedencia": "runtime", "status": status, "fase": fase,
             "sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"],
             "observacoes": obs, "prints": []}
    if status is None:
        dados.pop("status")
    if fase is None:
        dados.pop("fase")
    return dados


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")

    # ---- B1: sem a costura o JSON do probe NAO entra (a observacao nao tem hash) ----
    cru = fx["observacoes"][0]
    try:
        col.normalizar_observacao(cru, procedencia="runtime")
    except col.ObservacaoInvalida as erro:
        C.arc.exigir("hash" in str(erro).lower() or "sessao" in str(erro).lower(),
                     "B1: a recusa tem de nomear a falta de sessao/hash (veio: %s)" % erro)
    else:
        C.arc.exigir(False, "B1: observacao do probe sem sessao/hash foi ACEITA crua")

    # ---- carregar_saida_probe + anexar_contexto: o topo chega em cada item ----
    saida = col.carregar_saida_probe(_escrever(fx))
    C.arc.igual(saida["sessao"], fx["sessao"], "topo: sessao lida")
    C.arc.igual(saida["hash_fonte"], fx["hash_fonte"], "topo: hash_fonte lido")
    C.arc.igual(len(saida["observacoes"]), 2, "duas observacoes")

    anexadas = col.anexar_contexto(saida["observacoes"],
                                   {"sessao": saida["sessao"], "hash_fonte": saida["hash_fonte"]})
    for o in anexadas:
        C.arc.exigir(str(o.get("hash_fonte") or "").strip(), "B1: cada observacao ganhou hash_fonte")
        C.arc.exigir(str(o.get("sessao") or "").strip(), "B1: cada observacao ganhou sessao")

    n = col.normalizar_observacao(anexadas[0], procedencia="runtime")
    C.arc.exigir(n["ok"], "B1: com a costura a observacao ativa fecha ok")
    C.arc.igual(n["hash_fonte"], fx["hash_fonte"], "procedencia carrega o hash do topo")

    # ---- B2: os 5 extras atravessam (antes eram descartados) ----
    for campo in EXTRAS:
        C.arc.exigir(campo in n["campos"], "B2: campo %r foi descartado pela costura" % campo)
    C.arc.igual(n["campos"]["componente"]["valor"], "TextMeshProUGUI", "B2: componente preservado")

    # ---- B3: objeto INATIVO -> texto_renderizado NAO_APLICAVEL (fallback declarado) ----
    inativa = col.normalizar_observacao(anexadas[1], procedencia="runtime", alvos=ALVOS_SEM_RENDER)
    rend = inativa["campos"]["texto_renderizado"]
    C.arc.igual(rend["estado"], "NAO_APLICAVEL", "B3: inativo declara rendered como N/A")
    C.arc.igual(rend.get("fallback"), "texto_bruto", "B3: o fallback e o texto_bruto, declarado")
    C.arc.exigir(inativa["nao_aplicaveis"], "B3: o N/A fica visivel (nao some)")
    C.arc.igual(inativa["lacunas"], [],
                "B3/A2: fora do alvo, o fallback do inativo NAO penaliza")

    # ================= A2 (GRAVE): campos_alvo GOVERNA o veredito =================
    # a MESMA observacao inativa: pedindo o rendered, o alvo nao lido vira LACUNA.
    cobrada = col.normalizar_observacao(anexadas[1], procedencia="runtime", alvos=ALVOS_COM_RENDER)
    C.arc.exigir("texto_renderizado" in cobrada["lacunas"],
                 "A2: alvo NAO_APLICAVEL (nao lido) TEM de contar como lacuna")
    C.arc.igual(cobrada["ok"], False, "A2: com lacuna de alvo, nao fecha ok")

    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    obs_rt = col.anexar_contexto(fx["observacoes"], ctx)
    fecha, codigo = col.consolidar(plano, obs_rt, "runtime", contexto=ctx, alvos=ALVOS_COM_RENDER)
    C.arc.igual(fecha["status"], "INCOMPLETO",
                "A2: alvo nao lido -> INCOMPLETO (o fallback nao satisfaz o criterio)")
    C.arc.exigir(codigo != 0, "A2: INCOMPLETO -> exit != 0")
    C.arc.exigir("texto_renderizado" in fecha["lacunas"], "A2: a lacuna nomeia o alvo")
    C.arc.exigir(fecha["nao_aplicaveis"], "A2: o N/A continua declarado no resultado")

    # o MESMO dado fecha quando o alvo nao pede o rendered: e o alvo que governa.
    restrito, cod_restrito = col.consolidar(plano, obs_rt, "runtime", contexto=ctx,
                                            alvos=ALVOS_SEM_RENDER)
    C.arc.igual(restrito["status"], "CONFIRMADA",
                "A2: sem o alvo rendered o mesmo cenario fecha (o alvo governa)")
    C.arc.igual(cod_restrito, 0, "A2: exit 0 quando o alvo pedido foi lido")

    # alvo fora do schema => PLANO INVALIDO (nao pode "fechar" por engano)
    for alvo_ruim in (["field_typo"], ["texto_bruto", "nao_existe"]):
        try:
            col.consolidar(plano, obs_rt, "runtime", contexto=ctx, alvos=alvo_ruim)
        except col.PlanoInvalido as erro:
            C.arc.exigir(alvo_ruim[-1] in str(erro), "A2: a recusa nomeia o alvo invalido")
        else:
            C.arc.exigir(False, "A2: alvo fora do schema (%r) foi ACEITO" % alvo_ruim)

    # ---- HONESTIDADE: a FIXTURE rotulada NAO vira runtime (auto-detect) ----
    fstatus, fcodigo = col.consolidar_probe(_escrever(fx), plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(fstatus["status"], "FIXTURE", "fixture rotulada tem de sair FIXTURE, nunca runtime")
    C.arc.igual(fcodigo, 2, "fixture rotulada -> exit 2")

    # ========= A3: rotulo do ARTEFATO tem precedencia sobre o chamador ============
    forcado, cod_forcado = col.consolidar_probe(_escrever(fx), plano, alvos=ALVOS_SEM_RENDER,
                                                procedencia="runtime")
    C.arc.igual(forcado["status"], "FIXTURE",
                "A3: chamador dizer 'runtime' NAO pode maquiar artefato rotulado fixture")
    C.arc.igual(cod_forcado, 2, "A3: exit 2 mesmo com procedencia=runtime do chamador")
    C.arc.igual(forcado.get("evidencia_runtime"), False, "A3: fixture nunca vira evidencia_runtime")

    # A3 (COR-AUT4-F2): `evidencia_runtime: false` SOZINHO — sem `procedencia` e sem
    # `rotulo_fixture` — ja e declaracao de fixture; nao pode virar runtime nem ser
    # invertido para true.
    so_falso = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
    so_falso["evidencia_runtime"] = False
    res_falso, cod_falso = col.consolidar_probe(_escrever(so_falso), plano,
                                                alvos=ALVOS_SEM_RENDER)
    C.arc.igual(res_falso["status"], "FIXTURE",
                "A3 (F2): evidencia_runtime=false sozinho tem de sair FIXTURE")
    C.arc.igual(cod_falso, 2, "A3 (F2): evidencia_runtime=false -> exit 2")
    C.arc.igual(res_falso.get("evidencia_runtime"), False,
                "A3 (F2): o campo declarado NAO pode ser invertido para true")

    # ========= A4: status/fase terminal de falha do probe rebaixa o veredito ======
    ok_res, ok_cod = col.consolidar_probe(_saida_runtime(fx), plano, alvos=ALVOS_COM_RENDER)
    C.arc.igual(ok_res["status"], "CONFIRMADA",
                "A4: com status=CONCLUIDO e alvos lidos, o desfecho confirma")
    C.arc.igual(ok_cod, 0, "A4: exit 0 no caminho feliz")

    for status, fase in (("ERRO", "erro"), ("SEM_UI", "erro"),
                         ("ORCAMENTO_ESTOURADO", "orcamento-estourado"),
                         ("NAO_EXERCITADO", "nao-exercitado")):
        res, cod = col.consolidar_probe(_saida_runtime(fx, status=status, fase=fase),
                                        plano, alvos=ALVOS_COM_RENDER)
        C.arc.exigir(res["status"] != "CONFIRMADA",
                     "A4: probe %s/%s nao pode consolidar CONFIRMADA" % (status, fase))
        C.arc.exigir(cod != 0, "A4: probe %s/%s -> exit != 0" % (status, fase))

    # instrumento que nao declara status nenhum tambem NAO confirma (senao o
    # silencio viraria aprovacao).
    res_mudo, cod_mudo = col.consolidar_probe(_saida_runtime(fx, status=None, fase=None),
                                              plano, alvos=ALVOS_COM_RENDER)
    C.arc.exigir(res_mudo["status"] != "CONFIRMADA",
                 "A4: instrumento sem status nao pode ser aprovado pelo silencio")
    C.arc.exigir(cod_mudo != 0, "A4: sem status -> exit != 0")

    # ---- CONTROLE NEGATIVO: objeto ATIVO sem rendered CONTINUA lacuna ----
    ativa_sem_render = dict(anexadas[0])
    ativa_sem_render["texto_renderizado"] = None
    ativa_sem_render["nota_texto_renderizado"] = None
    ruim = col.normalizar_observacao(ativa_sem_render, procedencia="runtime",
                                     alvos=["texto_renderizado"])
    C.arc.exigir("texto_renderizado" in ruim["lacunas"],
                 "objeto ATIVO sem rendered e lacuna de verdade (nao pode virar N/A)")
    C.arc.igual(ruim["ok"], False, "ativa com lacuna nao fecha ok")

    # ===== A2 (COR-AUT4-F2): a forma REAL do artefato (`""`) e NAO LIDO ==========
    # `GetParsedText()` devolve `string.Empty` (nunca null); o probe tambem pode
    # emitir `{}` (material nulo) e `[]` (funil sem owner). Vazio NAO e leitura.
    ativa_vazia = dict(anexadas[0])
    ativa_vazia["texto_renderizado"] = ""            # forma REAL do artefato
    nv = col.normalizar_observacao(ativa_vazia, procedencia="runtime",
                                   alvos=["texto_renderizado"])
    C.arc.exigir("texto_renderizado" in nv["lacunas"],
                 "A2 (F2): texto_renderizado='' (forma REAL do probe) TEM de virar lacuna")
    C.arc.igual(nv["ok"], False, "A2 (F2): vazio nao pode fechar ok")
    for campo, vazio in (("owners", []), ("keywords", {}), ("cores", {})):
        obs_v = dict(anexadas[0])
        obs_v[campo] = vazio
        nv2 = col.normalizar_observacao(obs_v, procedencia="runtime", alvos=[campo])
        C.arc.exigir(campo in nv2["lacunas"],
                     "A2 (F2): %s=%r (vazio) TEM de virar lacuna" % (campo, vazio))

    # ===== A3 (COR-AUT4-F3): a FORMA de `evidencia_runtime` e RECUSADA ==========
    # Um artefato que traz a STRING "false" (ou 0, "0", null) NAO satisfazia
    # `is False`: escapava e CONFIRMAVA como runtime. A FORMA errada TEM de recusar
    # — nunca CONFIRMADA. (Aqui nao ha `procedencia` nem `rotulo_fixture`: o UNICO
    # sinal e a propria forma do campo, igual ao artefato que o defeito aceitava.)
    for forma in ("false", 0, "0", None, "False", 1, "true"):
        art = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
        art["evidencia_runtime"] = forma
        r_f, cod_f = col.consolidar_probe(_escrever(art), plano, alvos=ALVOS_SEM_RENDER)
        C.arc.exigir(r_f["status"] != "CONFIRMADA",
                     "A3 (F3): evidencia_runtime=%r (forma nao-canonica) NAO pode confirmar" % (forma,))
        C.arc.igual(r_f["status"], "FIXTURE",
                    "A3 (F3): evidencia_runtime=%r tem de sair FIXTURE" % (forma,))
        C.arc.igual(cod_f, 2, "A3 (F3): evidencia_runtime=%r -> exit 2" % (forma,))
        C.arc.igual(r_f.get("evidencia_runtime"), False,
                    "A3 (F3): o campo declarado nunca pode ser invertido para true")

    # CONTROLE positivo do caminho feliz: o bool `True` legitimo continua runtime.
    feliz = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
    feliz["evidencia_runtime"] = True
    r_ok, cod_ok = col.consolidar_probe(_escrever(feliz), plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(r_ok["status"], "CONFIRMADA",
                "A3 (F3): o bool True legitimo TEM de continuar runtime")
    C.arc.igual(cod_ok, 0, "A3 (F3): bool True -> exit 0")

    # CONTROLE: a chave AUSENTE e o caminho do probe REAL (o C# nao emite a chave).
    sem_chave = {k: v for k, v in fx.items()
                 if k not in ("procedencia", "rotulo_fixture", "evidencia_runtime")}
    r_aus, cod_aus = col.consolidar_probe(_escrever(sem_chave), plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(r_aus["status"], "CONFIRMADA",
                "A3 (F3): sem a chave (probe real) o artefato continua runtime")
    C.arc.igual(cod_aus, 0, "A3 (F3): sem a chave -> exit 0")

    # ===== COR-AUT4-F4: a PRESENCA de `evidencia_runtime` e derivada INTERNAMENTE ==
    # O artefato NAO pode governar o proprio veredito pela chave interna
    # `evidencia_runtime_presente`: a presenca tem de sair do que o coletor VIU no
    # JSON de entrada. Um artefato com a FORMA ERRADA `evidencia_runtime: "false"` E
    # `evidencia_runtime_presente: false` (ou 0) CONFIRMAVA como runtime.
    for mentira in (False, 0):
        art_f4 = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
        art_f4["evidencia_runtime"] = "false"           # forma errada de verdade
        art_f4["evidencia_runtime_presente"] = mentira  # a chave interna do artefato mente
        r4, c4 = col.consolidar_probe(_escrever(art_f4), plano, alvos=ALVOS_SEM_RENDER)
        C.arc.igual(r4["status"], "FIXTURE",
                    "F4: campo presente em forma errada + presente=%r tem de sair FIXTURE"
                    % (mentira,))
        C.arc.igual(c4, 2, "F4: forma autocontraditoria (presente=%r) -> exit 2" % (mentira,))
        C.arc.igual(r4.get("evidencia_runtime"), False,
                    "F4: o campo declarado nao pode ser invertido para true")

    # a mentira da chave interna NAO muda o veredito do caso canonico: bool False
    # presente + presente=false continua declaracao NAO-runtime -> FIXTURE.
    art_bool = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
    art_bool["evidencia_runtime"] = False
    art_bool["evidencia_runtime_presente"] = False
    rb, cb = col.consolidar_probe(_escrever(art_bool), plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(rb["status"], "FIXTURE", "F4: bool False + presente=false continua FIXTURE")
    C.arc.igual(cb, 2, "F4: bool False + presente=false -> exit 2")

    # ... e nem quando o artefato diz `presente=true` para um campo AUSENTE: a chave
    # interna nao pode CRIAR presenca. Ausencia REAL da chave = caminho do probe = runtime.
    art_mente_presente = {k: v for k, v in fx.items()
                          if k not in ("procedencia", "rotulo_fixture", "evidencia_runtime")}
    art_mente_presente["evidencia_runtime_presente"] = True
    rp, cp = col.consolidar_probe(_escrever(art_mente_presente), plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(rp["status"], "CONFIRMADA",
                "F4: a chave interna nao pode CRIAR presenca; chave ausente = runtime")
    C.arc.igual(cp, 0, "F4: chave ausente (com presente=true mentiroso) -> exit 0")

    # --- IDEMPOTENCIA (pitfall): dict cru do probe, dict JA MAPEADO e JSON de arquivo
    # passam pelo MESMO mapeador. O dict mapeado SEMPRE tem `evidencia_runtime` (None
    # quando o probe real NAO a emite): derivar a presenca de novo de `in dados`
    # transformaria o caminho legitimo 'chave ausente = runtime' em FIXTURE na 2a
    # passagem. Aqui se prova que os TRES casos seguem runtime.
    saida_crua = _saida_runtime(fx)                      # dict cru, sem a chave
    cru_res, cru_cod = col.consolidar_probe(saida_crua, plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(cru_res["status"], "CONFIRMADA",
                "F4 idem: dict CRU do probe sem a chave = runtime")
    C.arc.igual(cru_cod, 0, "F4 idem: dict cru -> exit 0")

    caminho_cru = _escrever(saida_crua)                  # JSON lido do arquivo
    arq_res, arq_cod = col.consolidar_probe(caminho_cru, plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(arq_res["status"], "CONFIRMADA",
                "F4 idem: JSON de arquivo sem a chave = runtime")
    C.arc.igual(arq_cod, 0, "F4 idem: JSON de arquivo -> exit 0")

    mapeado = col.carregar_saida_probe(caminho_cru)      # dict JA MAPEADO (2a passagem)
    map_res, map_cod = col.consolidar_probe(mapeado, plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(map_res["status"], "CONFIRMADA",
                "F4 idem: dict JA MAPEADO sem a chave NAO pode virar FIXTURE (pitfall)")
    C.arc.igual(map_cod, 0, "F4 idem: dict ja mapeado -> exit 0")

    # o dict mapeado do artefato autocontraditorio tambem NAO escapa: 2a passagem
    # mantem a presenca derivada da entrada crua -> FIXTURE.
    mapeado_defeito = col.carregar_saida_probe(
        _escrever(dict(art_f4, evidencia_runtime="false", evidencia_runtime_presente=False)))
    md_res, md_cod = col.consolidar_probe(mapeado_defeito, plano, alvos=ALVOS_SEM_RENDER)
    C.arc.igual(md_res["status"], "FIXTURE",
                "F4 idem: artefato autocontraditorio mapeado continua FIXTURE")
    C.arc.igual(md_cod, 2, "F4 idem: artefato autocontraditorio mapeado -> exit 2")


if __name__ == "__main__":
    C.arc.main(META, corpo)
