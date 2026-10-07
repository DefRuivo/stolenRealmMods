#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aut5.py — AUT-5: conduz os cenarios do RSTV e PROVA a leitura somente.

O QUE ESTE ARQUIVO E
--------------------
O condutor (runner) da frente AUT-5. Ele NAO julga por conta propria: ele monta
as observacoes a partir de fontes REAIS e SOMENTE LEITURA (o `LogOutput.log` do
mod, o JSON do probe AUT-4 quando existir, a propria fonte do mod), chama o
avaliador de cenarios RSTV (`tools/automacao/cenarios/rstv.py`, CIC-3) e a
camada de decisao (`tools/automacao/ciclo/decisao.py`, CIC-2), e emite um
relatorio com **hash de fonte/DLL, configuracao, cenario, observado/esperado,
evidencia e lacunas**.

O QUE ELE NUNCA FAZ (por regra da tarefa)
-----------------------------------------
* nao instala probe, nao inicia/encerra o jogo, nao carrega save, nao publica;
* nao escreve no perfil do dono (le a DLL e o `.cfg` do perfil apenas para
  registrar a identidade dos bytes);
* nao transforma marcador ausente em OK — AUSENTE e lacuna declarada;
* nao usa o proprio log como "esperado": o ALVO esperado vem do plano/cenario.

CLASSES DE CRITERIO
-------------------
* `AUT5`           — instrumentacao: os marcadores/guardas que a automacao EXIGE
                     existirem na fonte e o boot real no log (classe offline).
* `RoguelikeSkillTreeVisualizer` — comportamento do mod nos cenarios (classe
                     runtime; hoje NAO_EXERCITADO sem a rodada autorizada).

USO
---
    python tools/automacao/aut5/aut5.py --repo C:/dev/stolen-realm \
        [--log <LogOutput.log>] [--plano tools/automacao/aut5/cenarios-rstv.json] \
        [--probe <aut4probe.json>] [--perfil <BepInEx do perfil>] \
        [--out <relatorio.json>] [--texto] [--sem-decisao]

Exit: 0 = tudo exercitado e sem defeito · 1 = ha REPROVADO (defeito acionavel)
      2 = NAO CONSEGUI RODAR ou ha NAO_EXERCITADO/INDETERMINADO (incompleto).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from log_rstv import (GATES_READONLY, GUARDAS, MARCADORES_FONTE, MOD,
                      chave_motivo, consistencia_dependencia, guarda_ligada,
                      ler_log, observacoes, sha256_file)

RAIZ_CENARIOS = os.path.join(os.path.dirname(AQUI), "cenarios")
RAIZ_CICLO = os.path.join(os.path.dirname(AQUI), "ciclo")
MOD_INSTRUMENTACAO = "AUT5"

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2
TAREFA = "t_76a41ea7"

OK, REPROVADO, NAO_EXERCITADO, INDETERMINADO = (
    "OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")


# ----------------------------------------------------------------- identidade ---

def _fonte_do_mod(repo):
    """Lista (relpath, sha256) das fontes do RSTV — a base do `fonte_sha`."""
    base = os.path.join(repo, MOD)
    arquivos = []
    for raiz, _dirs, nomes in os.walk(base):
        if os.sep + "obj" in raiz or os.sep + "bin" in raiz or os.sep + "." in raiz:
            continue
        for nome in sorted(nomes):
            if nome.endswith(".cs") or nome.endswith(".csproj"):
                cam = os.path.join(raiz, nome)
                arquivos.append((os.path.relpath(cam, repo).replace("\\", "/"),
                                 sha256_file(cam)))
    return sorted(arquivos)


def identidade_do_repo(repo, perfil=None):
    """Identidade dos bytes: `fonte_sha` (arvore de fonte do RSTV) + `dll_sha`.

    `fonte_sha` = sha256 de "<relpath>\\t<sha256>" das fontes, ordenado — a
    IDENTIDADE da arvore de fonte do mod (nao de um arquivo solto). Declarada
    aqui e usada como identidade do cenario em todos os criterios.
    """
    fontes = _fonte_do_mod(repo)
    h = hashlib.sha256()
    for rel, sha in fontes:
        h.update(("%s\t%s\n" % (rel, sha)).encode("utf-8"))
    ident = {"esquema": "AUT5/identidade/1",
             "fonte_sha": h.hexdigest(),
             "fontes": {rel: sha for rel, sha in fontes}}
    csproj = os.path.join(repo, MOD, "%s.csproj" % MOD)
    m = re.search(r"<Version>([^<]+)</Version>",
                  open(csproj, encoding="utf-8").read()) if os.path.isfile(csproj) else None
    ident["versao"] = m.group(1).strip() if m else None
    dll = os.path.join(repo, MOD, "bin", "Release", "netstandard2.1",
                       "%s.dll" % MOD)
    if not os.path.isfile(dll):
        dll = os.path.join(repo, MOD, "bin", "Debug", "netstandard2.1", "%s.dll" % MOD)
    ident["dll_sha"] = sha256_file(dll)
    ident["dll"] = os.path.abspath(dll) if os.path.isfile(dll) else None
    if perfil:
        p_dll = os.path.join(perfil, "plugins", MOD, "%s.dll" % MOD)
        ident["dll_perfil"] = os.path.abspath(p_dll)
        ident["dll_perfil_sha"] = sha256_file(p_dll)
        cfg = os.path.join(perfil, "config", "com.gumatos.roguelikeskilltreevisualizer.cfg")
        ident["config_perfil"] = os.path.abspath(cfg) if os.path.isfile(cfg) else None
        ident["config_sha"] = sha256_file(cfg)
    ident["dll_perfil_igual_repo"] = bool(ident.get("dll_perfil_sha")
                                          and ident.get("dll_sha")
                                          and ident["dll_perfil_sha"] == ident["dll_sha"])
    return ident


def identidade_do_cenario(ident):
    """Identidade no formato do contrato do ciclo (fonte_sha/dll_sha/config_sha)."""
    d = {"fonte_sha": ident.get("fonte_sha"), "dll_sha": ident.get("dll_sha")}
    if ident.get("config_sha"):
        d["config_sha"] = ident["config_sha"]
        d["config_perfil"] = ident.get("config_perfil")
    if ident.get("dll_perfil_sha"):
        d["dll_perfil_sha"] = ident["dll_perfil_sha"]
    d["versao"] = ident.get("versao")
    return d


# ------------------------------------------------------------------ criterios ---

def _ev(caminhos):
    """Evidencia como [{caminho, sha256}] — o que a decisao CONFERE em disco."""
    saida = []
    for cam in caminhos:
        if not cam:
            continue
        saida.append({"caminho": os.path.abspath(cam), "sha256": sha256_file(cam)})
    return saida


def _crit(cid, mod, estado, classe, proc, esperado, observado, motivo,
          evidencia, tarefa, extra=None):
    c = {"id": cid, "mod": mod, "estado": estado, "classe": classe,
         "procedencia": proc, "esperado": esperado, "observado": observado,
         "evidencia": evidencia, "motivo": motivo, "tarefa_origem": tarefa}
    for k, v in (extra or {}).items():
        c.setdefault(k, v)
    return c


def _ler_texto(caminho):
    if not caminho or not os.path.isfile(caminho):
        return ""
    with open(caminho, encoding="utf-8", errors="replace") as fh:
        return fh.read()


# ------------------------------------------------- instrumentacao (offline) ---

def criterios_instrumentacao(repo, ident, leitura, plano):
    """Criterios de CLASSE OFFLINE: os instrumentos que a automacao exige.

    Sem esses marcadores/guardas na fonte, ou sem o boot real no log, a
    automacao NAO consegue julgar os cenarios — e isso e uma regressao
    detectavel offline (REPROVADO), nao uma lacuna de rodada.
    """
    out = []
    fontes = [os.path.join(repo, MOD, nome) for nome in sorted(os.listdir(os.path.join(repo, MOD)))
              if nome.endswith(".cs")]
    texto = "\n".join(_ler_texto(c) for c in fontes)
    ev_fonte = _ev([os.path.join(repo, MOD, "Plugin.cs"),
                    os.path.join(repo, MOD, "SkillTreesTab.cs")])

    faltando = sorted(m for m in MARCADORES_FONTE if m not in texto)
    if faltando:
        out.append(_crit(
            "AUT5-obs-marcadores-fonte", MOD_INSTRUMENTACAO, REPROVADO, "offline", "execucao",
            "todos os marcadores de diagnostico exigidos pela automacao existem na fonte",
            "ausentes na fonte: %s" % faltando,
            "REGRESSAO DE OBSERVABILIDADE: sem esses marcadores a automacao perde a "
            "capacidade de julgar a tarefa %s"
            % sorted({MARCADORES_FONTE[m] for m in faltando}),
            ev_fonte, "AUT-5"))
    else:
        out.append(_crit(
            "AUT5-obs-marcadores-fonte", MOD_INSTRUMENTACAO, OK, "offline", "execucao",
            "todos os marcadores de diagnostico exigidos pela automacao existem na fonte",
            "%d marcadores presentes em %d arquivos .cs" % (len(MARCADORES_FONTE), len(fontes)),
            "marcadores de RSTV-21/25b/6 presentes na fonte (lidos do disco)",
            ev_fonte + _ev([os.path.join(repo, MOD, "SkillTreesWindow.cs"),
                            os.path.join(repo, MOD, "SkillTreeReadOnly.cs")]), "AUT-5"))

    run_targets = os.path.join(repo, MOD, "RunTargets.cs")
    txt_rt = _ler_texto(run_targets)
    ev_rt = _ev([run_targets])
    trycatch = "catch (Exception" in txt_rt
    # A-3 (AUT5-F2): a checagem era de PRESENCA do texto do motivo — com a guarda
    # neutralizada (`if (false && gui.PingModeActive)`) o criterio continuava OK.
    # Agora cada guarda tem de estar LIGADA ao `if (<condicao>)` que a produz e ao
    # `return false;` que fecha o caminho (`log_rstv.guarda_ligada`).
    desconectadas = []
    for gid, motivo, condicao in GUARDAS:
        ligada, porque = guarda_ligada(txt_rt, condicao, motivo)
        if not ligada:
            desconectadas.append("%s (%s)" % (gid, porque))
    # A-1 (AUT5-F2): o PLANO e o REGISTRY tem de declarar a MESMA guarda — mesmo
    # `id` e mesma CHAVE de motivo. Foi esse desalinhamento (plano com o motivo
    # TRUNCADO vs produto com o literal COMPLETO) que fazia a recusa legitima sair
    # como "fora do plano" na rodada. Truncar o sufixo depois do parentetico NAO e
    # mais defeito (a normalizacao cobre, por projeto — ver `chave_motivo`); o que
    # reprova aqui e declarar guarda com OUTRA identidade, faltando, ou dois itens
    # que a normalizacao fundiria em um so.
    itens_plano_lista = list((plano.get("guards_run") or {}).get("itens") or [])
    chaves_plano = [chave_motivo(g.get("motivo")) for g in itens_plano_lista]
    repetidas = sorted({c for c in chaves_plano if chaves_plano.count(c) > 1})
    itens_plano = {g.get("id"): g for g in itens_plano_lista}
    divergentes = []
    for gid, motivo, _cond in GUARDAS:
        item = itens_plano.get(gid)
        if item is None:
            divergentes.append("%s: ausente do plano" % gid)
        elif chave_motivo(item.get("motivo")) != chave_motivo(motivo):
            divergentes.append("%s: plano=%r registry=%r"
                               % (gid, chave_motivo(item.get("motivo")), chave_motivo(motivo)))
    for chave in repetidas:
        divergentes.append("motivo normalizado repetido no plano: %r (fundiria duas guardas)"
                           % chave)
    if desconectadas or divergentes or not trycatch:
        out.append(_crit(
            "AUT5-guardas-run-fonte", MOD_INSTRUMENTACAO, REPROVADO, "offline", "execucao",
            "as %d guardas da run existem na fonte, cada uma LIGADA ao seu `if` e ao "
            "`return false`, com o plano declarando a mesma guarda" % len(GUARDAS),
            "sem bloco condicao->motivo->return: %s; plano divergente: %s; try/catch=%s"
            % (desconectadas or "nenhuma", divergentes or "nenhuma", trycatch),
            "guarda da run removida/neutralizada (ou plano declarando motivo diferente do "
            "produto): o roteiro de risco do RSTV-6 perde a trava",
            ev_rt, "RSTV-6", {"guardas_sem_bloco": desconectadas,
                              "guardas_divergentes_do_plano": divergentes}))
    else:
        out.append(_crit(
            "AUT5-guardas-run-fonte", MOD_INSTRUMENTACAO, OK, "offline", "execucao",
            "as %d guardas da run existem na fonte, cada uma LIGADA ao seu `if` e ao "
            "`return false`, com o plano declarando a mesma guarda" % len(GUARDAS),
            "%d/%d guardas com `if (<condicao>) -> motivo -> return false` conferido na "
            "fonte e no plano; catch com lado seguro (nao abrir)"
            % (len(GUARDAS), len(GUARDAS)),
            "guards de turno/mira/janela/posicionamento/acao/movimento presentes E ligados "
            "(RunTargets.GateOk); plano sem motivo truncado",
            ev_rt, "RSTV-6"))

    pat = os.path.join(repo, MOD, "Patches.cs")
    txt_p = _ler_texto(pat)
    falta_fonte = [g for g in GATES_READONLY if g not in txt_p]
    aplicados = [g for g in GATES_READONLY if g in (leitura.get("ganchos") or [])]
    if falta_fonte:
        out.append(_crit(
            "AUT5-travas-readonly", MOD_INSTRUMENTACAO, REPROVADO, "offline", "execucao",
            "as travas de leitura somente existem na fonte e foram aplicadas no boot",
            "ausentes na fonte: %s" % falta_fonte,
            "trava de leitura somente removida da fonte (nenhuma escrita no personagem)",
            _ev([pat]), "RSTV-6"))
    elif not leitura.get("existe") or not leitura.get("versao"):
        out.append(_crit(
            "AUT5-travas-readonly", MOD_INSTRUMENTACAO, NAO_EXERCITADO, "offline", "execucao",
            "as travas de leitura somente existem na fonte e foram aplicadas no boot",
            "fonte OK (%s); log %s" % (",".join(GATES_READONLY),
                                       "ausente" if not leitura.get("existe")
                                       else "sem linha de boot do RSTV"),
            "sem boot do RSTV no log nao ha prova de que as travas foram APLICADAS",
            _ev([pat]), "RSTV-6",
            {"lacuna_probe": "log de boot do RSTV ausente", "tipo_pendencia": "tecnica"}))
    elif len(aplicados) != len(GATES_READONLY):
        out.append(_crit(
            "AUT5-travas-readonly", MOD_INSTRUMENTACAO, REPROVADO, "offline", "execucao",
            "as travas de leitura somente existem na fonte e foram aplicadas no boot",
            "aplicados no log: %s (faltam %s)"
            % (aplicados, [g for g in GATES_READONLY if g not in aplicados]),
            "RISCO DE ESCRITA: trava de leitura somente existe na fonte mas NAO foi aplicada "
            "no boot desta build",
            _ev([pat]) + _ev([leitura["caminho"]]), "RSTV-6"))
    else:
        out.append(_crit(
            "AUT5-travas-readonly", MOD_INSTRUMENTACAO, OK, "offline", "execucao",
            "as travas de leitura somente existem na fonte e foram aplicadas no boot",
            "fonte OK; ganchos aplicados no log: %s" % ",".join(aplicados),
            "leitura somente com gancho de commit higienizado e de reset de pontos",
            _ev([pat]) + _ev([leitura["caminho"]]), "RSTV-6"))

    # boot real: versao do log == versao da fonte E a DLL do log == a DLL atual
    ev_log = _ev([leitura["caminho"]]) if leitura.get("existe") else []
    if not leitura.get("existe"):
        out.append(_crit(
            "AUT5-boot-rstv", MOD_INSTRUMENTACAO, NAO_EXERCITADO, "offline", "execucao",
            "o mod carrega com a versao da fonte e aplica todos os ganchos",
            "log ausente", "sem LogOutput.log nao ha prova de boot",
            [], "AUT-5", {"lacuna_probe": "LogOutput.log ausente", "tipo_pendencia": "tecnica"}))
    elif not leitura.get("versao"):
        out.append(_crit(
            "AUT5-boot-rstv", MOD_INSTRUMENTACAO, NAO_EXERCITADO, "offline", "execucao",
            "o log de boot e da versao da fonte (%s)" % ident.get("versao"),
            "log sem a linha '<mod> <versao> carregado'",
            "o log nao tem linha de boot do RSTV: nao ha prova de carregamento desta sessao",
            ev_log, "AUT-5",
            {"lacuna_probe": "log sem linha de boot do RSTV", "tipo_pendencia": "tecnica"}))
    elif leitura.get("versao") != ident.get("versao"):
        out.append(_crit(
            "AUT5-boot-rstv", MOD_INSTRUMENTACAO, REPROVADO, "offline", "execucao",
            "o log de boot e da versao da fonte (%s)" % ident.get("versao"),
            "log=versao %s" % leitura.get("versao"),
            "log de OUTRA build: nao vale como prova da build atual",
            ev_log, "AUT-5"))
    elif not leitura.get("identifica_build"):
        out.append(_crit(
            "AUT5-boot-rstv", MOD_INSTRUMENTACAO, INDETERMINADO, "offline", "execucao",
            "a DLL do log e a DLL atual",
            "dll do log=%s dll atual=%s" % (leitura.get("dll_sha_declarado"),
                                            leitura.get("dll_sha_conhecido")),
            "bytes da DLL divergentes: log nao identifica a build medida",
            ev_log, "AUT-5"))
    else:
        out.append(_crit(
            "AUT5-boot-rstv", MOD_INSTRUMENTACAO, OK, "offline", "execucao",
            "o mod carrega com a versao da fonte e aplica os ganchos",
            "versao %s; %d ganchos aplicados; dll == build atual"
            % (leitura.get("versao"), len(leitura.get("ganchos") or [])),
            "boot real da DLL atual no log (leitura de bytes em disco)",
            ev_log + _ev([os.path.join(repo, MOD, "Plugin.cs")]), "AUT-6"))

    # geometria do botao da run no log (RSTV-6/30: injetar SEM empurrar nem sobrepor botao nativo)
    hud = (leitura.get("hud") or {}).get("botao")
    if hud:
        # RSTV-30: o criterio deixou de ser "a largura da linha nao cresceu" (o botao nao mora mais na
        # linha do Ping) e passou a ser "a largura do clone CABE no vao livre medido entre os botoes
        # nativos e o vizinho da direita" — mais forte: com `ignoreLayout`, o LayoutGroup do container
        # nao reflui, entao nenhum botao nativo se move nem encolhe.
        invade = (hud["largura_px"] > hud["vao_px"] + 0.5 or
                  hud["largura_px"] > hud["nativo_px"] + 0.5)
        out.append(_crit(
            "AUT5-geometria-botao-run", MOD_MOD_GEO, REPROVADO if invade else OK,
            "offline", "execucao",
            "botao injetado na BARRA DE BAIXO com largura DENTRO do vao livre medido (sem empurrar "
            "nem sobrepor botao nativo)",
            "botao %.1fx%.1f px (nativo %.1f px); vao livre %.1f px; limite do vizinho '%s'=%.1f px; "
            "borda dos nativos=%.1f px; pai=%s"
            % (hud["largura_px"], hud["altura_px"], hud["nativo_px"], hud["vao_px"],
               hud["vizinho"], hud["limite_px"], hud["nativos_px"], hud["pai"]),
            ("o botao ficou MAIOR que o vao livre medido (invadiria o vizinho ou os nativos)" if invade
             else "botao injetado na barra de baixo dentro do vao livre medido (RSTV-30)"),
            ev_log, "RSTV-6"))
    else:
        out.append(_crit(
            "AUT5-geometria-botao-run", MOD_MOD_GEO, NAO_EXERCITADO, "offline", "execucao",
            "botao injetado na BARRA DE BAIXO com largura dentro do vao livre medido",
            "marcador 'RSTV-30: botao Skills injetado na BARRA DE BAIXO' ausente no log",
            "sem o marcador nao ha geometria do botao da run para conferir",
            ev_log, "RSTV-6",
            {"lacuna_probe": "marcador RSTV-30 de injecao do botao do HUD ausente",
             "tipo_pendencia": "tecnica"}))

    botoes_modal = (leitura.get("modais") or {}).get("botoes") or []
    if botoes_modal:
        b = botoes_modal[0]
        certo = b["lado_px"] > 0 and ("canto superior direito" in (b.get("pai") or ""))
        out.append(_crit(
            "AUT5-geometria-botao-modal", MOD_MOD_GEO, OK if certo else REPROVADO,
            "offline", "execucao",
            "botao 'Skills' injetado no cabecalho do modal, canto superior direito",
            "rotulo=%s; %.1fx%.1f px; origem=%s" % (b["rotulo"], b["lado_px"], b["lado_px"],
                                                    (b.get("pai") or "")[:80]),
            "botao do modal com geometria declarada no log",
            ev_log, "RSTV-21"))
    else:
        out.append(_crit(
            "AUT5-geometria-botao-modal", MOD_MOD_GEO, NAO_EXERCITADO, "offline", "execucao",
            "botao 'Skills' injetado no cabecalho do modal",
            "marcador 'RSTV-20: botao ... injetado no cabecalho do modal' ausente",
            "sem o marcador nao ha geometria do botao do modal",
            ev_log, "RSTV-21",
            {"lacuna_probe": "marcador RSTV-20 de injecao do botao do modal ausente",
             "tipo_pendencia": "tecnica"}))

    # confronto Dependency x conectores pelo log (RSTV-25b, parte automatizavel)
    cons = consistencia_dependencia(leitura)
    arvore_exercitada = (bool(leitura.get("linhas_dependencia"))
                        or bool(leitura.get("dependency_por_tier"))
                        or bool(leitura.get("geometria_arvore"))
                        or any(j.get("aberta") for j in leitura.get("janelas") or []))
    if cons is None and arvore_exercitada:
        ausentes = [nome for nome, campo in (("RSTV-24b", "linhas_dependencia"),
                                             ("RSTV-25", "dependency_por_tier"))
                    if not leitura.get(campo)]
        out.append(_crit(
            "AUT5-RSTV-25b-conectores-log", MOD_MOD_GEO, REPROVADO, "offline", "execucao",
            "arvore exercitada emite RSTV-24b e RSTV-25 para confronto POR TIER",
            "marcadores ausentes: " + ", ".join(ausentes),
            "arvore exercitada, mas falta emissao/leitura de " + ", ".join(ausentes),
            ev_log, "RSTV-25b", {"tipo_pendencia": "tecnica",
                                  "marcadores_ausentes": ausentes}))
    elif cons is None:
        # AUT5-F1: o RSTV-24b/RSTV-25 so existem quando o mod RENDERIZA a arvore —
        # sem a janela aberta nao ha leitura NENHUMA. Com o campo por tier ja
        # emitido pelo mod, o que falta nao e instrumento: e a rodada autorizada
        # Nao ha sinal de abertura/renderizacao nem qualquer lado do confronto.
        c = _crit(
            "AUT5-RSTV-25b-conectores-log", MOD_MOD_GEO, NAO_EXERCITADO, "offline", "execucao",
            "Dependency real (RSTV-25) x linhas ativas (RSTV-24b) consistentes, POR TIER",
            "linhas_dependencia=%s linhas_por_tier=%s dependency_por_tier=%s"
            % (bool(leitura.get("linhas_dependencia")), bool(leitura.get("linhas_por_tier")),
               bool(leitura.get("dependency_por_tier"))),
            "a janela read-only nao foi aberta nesta sessao: nao ha Dependency lido nem linhas "
            "ativas — o confronto por tier ja e possivel (AUT5-F1), falta a rodada que o exercita",
            ev_log, "RSTV-25b",
            {"lacuna_probe": "RSTV-24b/RSTV-25 exigem a arvore renderizada (janela read-only "
                             "aberta na rodada autorizada)"})
        out.append(_marcar_pendencia_runtime(
            c, "autorizacao",
            "Autorizar UMA rodada com a janela read-only aberta numa classe COM dependencias: o "
            "log traz o RSTV-24b (por tier, AUT5-F1) e o RSTV-25, e o confronto fecha por tier."))
    else:
        detalhe = json.dumps({k: cons[k] for k in ("soma_com_dependency", "linhas_ativas", "nos",
                                                   "com_sprite", "por_tier", "por_tier_linhas")},
                             ensure_ascii=False)
        if cons["conector_ausente"]:
            estado, motivo = REPROVADO, (
                "conector AUSENTE: %d no(s) com Dependency real e apenas %d linha(s) ativa(s)"
                % (cons["soma_com_dependency"], cons["linhas_ativas"]))
            extra = {"tipo_pendencia": "tecnica",
                     "t5_sem_dependency": cons["t5_sem_dependency"]}
        elif cons["conector_sem_dependency"]:
            estado, motivo = REPROVADO, (
                "conector SEM Dependency: %d linha(s) ativa(s) para %d no(s) com Dependency"
                % (cons["linhas_ativas"], cons["soma_com_dependency"]))
            extra = {"tipo_pendencia": "tecnica",
                     "t5_sem_dependency": cons["t5_sem_dependency"]}
        elif cons["inconsistencias_por_tier"]:
            estado, motivo = REPROVADO, (
                "confronto POR TIER inconsistente: "
                + "; ".join(i["defeito"] for i in cons["inconsistencias_por_tier"]))
            extra = {"tipo_pendencia": "tecnica",
                     "inconsistencias_por_tier": cons["inconsistencias_por_tier"],
                     "t5_sem_dependency": cons["t5_sem_dependency"]}
        elif cons["por_tier_ok"]:
            # AUT5-F1: com a contagem POR TIER o confronto fecha — total E por tier.
            estado, motivo = OK, (
                "confronto POR TIER consistente: Dependency real == linhas ativas em "
                "todos os %d tier(s); total %d == %d (T5 sem Dependency e ausencia LEGITIMA)"
                % (len(cons["por_tier"]), cons["soma_com_dependency"], cons["linhas_ativas"]))
            extra = {"por_tier_linhas": cons["por_tier_linhas"],
                     "t5_sem_dependency": cons["t5_sem_dependency"]}
        else:
            estado, motivo = INDETERMINADO, (
                "consistente no TOTAL (Dependency=%d == linhas=%d); o confronto POR TIER segue "
                "impossivel: este log e de build ANTERIOR ao AUT5-F1 (RSTV-24b sem o 'por tier')"
                % (cons["soma_com_dependency"], cons["linhas_ativas"]))
            extra = {"tipo_pendencia": "tecnica",
                     "lacuna_probe": "log de build anterior ao AUT5-F1: RSTV-24b so da o TOTAL "
                                     "de linhas; falta a contagem por tier",
                     "t5_sem_dependency": cons["t5_sem_dependency"]}
        out.append(_crit(
            "AUT5-RSTV-25b-conectores-log", MOD_MOD_GEO, estado, "offline", "execucao",
            "Dependency real (RSTV-25) x linhas ativas (RSTV-24b) consistentes, POR TIER; "
            "T5 sem Dependency e ausencia LEGITIMA",
            detalhe, motivo, ev_log, "RSTV-25b", extra))

    # geometria da arvore na janela (RSTV-24a/23i) — clamp registrado quando excede
    g = leitura.get("geometria_arvore")
    if not g:
        c = _crit(
            "AUT5-geometria-arvore-log", MOD_MOD_GEO, NAO_EXERCITADO, "offline", "execucao",
            "arvore centralizada na AREA e, se exceder, reducao registrada",
            "RSTV-24a/RSTV-23i ausentes no log",
            "a janela read-only nao foi aberta: nao ha bbox da arvore para conferir",
            ev_log, "RSTV-25b",
            {"lacuna_probe": "RSTV-24a/23i exigem a arvore renderizada na janela"})
        out.append(_marcar_pendencia_runtime(
            c, "autorizacao",
            "Autorizar UMA rodada e abrir a janela read-only; anexar PNG da arvore inteira "
            "para o aceite de design."))
    else:
        excede = bool(g.get("excede_area"))
        fator = g.get("fator_escala")
        if excede and (not fator or float(fator) >= 1.0):
            estado, motivo = REPROVADO, (
                "a arvore excede a area e a reducao NAO foi aplicada (fator=%s) — risco de "
                "clipping" % fator)
        elif excede:
            estado, motivo = OK, ("a arvore excedeu a area e a reducao foi aplicada "
                                  "(fator %sx), sem clipping" % fator)
        else:
            estado, motivo = OK, "bbox da arvore dentro da AREA (RSTV-24a), sem reducao necessaria"
        out.append(_crit(
            "AUT5-geometria-arvore-log", MOD_MOD_GEO, estado, "offline", "execucao",
            "arvore centralizada na AREA e, se exceder, reducao registrada",
            json.dumps(g, ensure_ascii=False), motivo, ev_log, "RSTV-25b"))
    return out


MOD_MOD_GEO = MOD  # os criterios de geometria sao do proprio mod (nao da instrumentacao)


# ------------------------------------------------------------------- runtime ---

def _marcar_pendencia_runtime(c, tipo, instrucoes=None, nota=None):
    """Marca um criterio NAO EXERCITADO cuja prova SO existe numa rodada.

    A leitura honesta: nao ha dado nenhum, e a UNICA classe de prova capaz de
    fechar o criterio e `runtime`. O rotulo fica explicitamente documentado
    (`procedencia_nota`) e `prova_runtime=False`/`sessao=None` — a camada de
    decisao NAO consegue aprovar por rotulo (o contrato positivo de runtime exige
    prova_runtime+sessao+hashes), e o `tipo_pendencia` roteia:
    `autorizacao` -> dono (autorizar a rodada) · `tecnica` -> fila de agente.
    """
    c["classe"] = "runtime"
    c["procedencia"] = "runtime"
    c["prova_runtime"] = False
    c["sessao"] = None
    c["procedencia_nota"] = nota or (
        "sem leitura ainda: 'runtime' e a CLASSE DE PROVA exigida pelo cenario (so uma "
        "rodada autorizada fecha o criterio), NAO uma rodada executada; prova_runtime=false")
    c["tipo_pendencia"] = tipo
    c["autorizacao_necessaria"] = (tipo == "autorizacao")
    if instrucoes:
        c["instrucoes_humanas"] = instrucoes
    return c


def _plano_map(plano):
    por_id = {}
    for cid, cap in (plano.get("capacidades") or {}).items():
        por_id[cid] = cap
    return por_id


def criterios_rstv(ident, leitura, plano, probe=None):
    """Roda o avaliador RSTV (CIC-3) sobre as observacoes reais e mapeia o plano.

    * criterio EXERCITADO (tem leitura): a `classe` sai do que a leitura
      realmente e (log/execucao nunca vira `runtime`);
    * criterio SEM LEITURA nenhuma cuja prova so existe em jogo: classe de prova
      `runtime` (documentada em `procedencia_nota`) e roteamento por
      `pendencia_primaria` do plano — falta de rodada autorizada (`autorizacao`)
      vs falta de campo de probe/coletor (`tecnica`, fila de agente).
    """
    try:
        spec = importlib.util.spec_from_file_location(
            "rstv_cenarios", os.path.join(RAIZ_CENARIOS, "rstv.py"))
        rstv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rstv)
    except Exception as erro:
        return [], "avaliador RSTV indisponivel: %s: %s" % (type(erro).__name__, erro)

    ev = [leitura["caminho"]] if leitura.get("existe") else []
    obs = observacoes(leitura, evidencia=ev, dll_sha=ident.get("dll_perfil_sha"))
    if probe:
        obs.extend(_obs_do_probe(probe))
    ident_cenario = identidade_do_cenario(ident)
    criterios = rstv.avaliar(obs, ident_cenario)

    mapa = _plano_map(plano)
    for c in criterios:
        cap = mapa.get(c["id"]) or {}
        # "sem leitura NENHUMA" (a capacidade nao recebeu dado nenhum): a unica
        # classe de prova capaz de fechar e runtime. Dado presente mas
        # incompleto NAO entra aqui — continua `execucao`/offline, classe do
        # que foi realmente lido (nunca promovido a runtime por rotulo).
        sem_leitura = (c.get("estado") in (NAO_EXERCITADO, INDETERMINADO)
                       and c.get("procedencia") == "execucao"
                       and str(c.get("motivo") or "").startswith("sem observacao/leitura"))
        # AUT5-F1: o dado do log EXISTE, mas o avaliador nao fecha sem a rodada
        # ("runtime sem sessao/hash_fonte"). Depois de o probe/coletor passarem a
        # emitir o campo (itens 1-4 do AUT5-F1), a lacuna NAO e mais tecnica — o
        # que resta e a AUTORIZACAO da rodada runtime (roteamento pelo plano).
        so_falta_rodada = (c.get("estado") in (NAO_EXERCITADO, INDETERMINADO)
                           and c.get("procedencia") == "execucao"
                           and "sessao" in str(c.get("motivo") or ""))
        if sem_leitura or so_falta_rodada:
            prim = cap.get("pendencia_primaria") or "tecnica"
            c["cenarios"] = cap.get("cenarios")
            c["campos_necessarios"] = cap.get("campos_necessarios")
            c["motivo_plano"] = cap.get("motivo")
            _marcar_pendencia_runtime(c, prim, cap.get("instrucoes_humanas"))
        else:
            # classe coerente com a procedencia REAL da leitura
            c["classe"] = "runtime" if c.get("procedencia") == "runtime" else "offline"
    return criterios, None


def _achata_campos(o):
    """Achata o bloco `campos` (formato NORMALIZADO do coletor CIC-5) em chaves planas.

    F-1 da revisao da AUT5-F1 (`t_dd95f8d9`, roteado a este card): o docstring de
    `_obs_do_probe` promete "cru ou normalizado", mas o trio do tooltip so valia no
    formato CRU — `rstv._cap_tooltip_restauracao` (`rstv.py:543-575`) le
    `k in o`/`o.get(k)` direto, enquanto as outras capacidades usam `_campo()`, que
    aceita as duas formas. Sem achatar, a observacao normalizada do coletor deixava
    `RSTV-21-tooltip-restauracao` em NAO_EXERCITADO/tecnica mesmo com os campos
    PRESENTES.

    Regra identica a de `rstv._campo`: campo PRESENTE vira chave plana com o seu
    `valor`; NAO_APLICAVEL (objeto INATIVO) usa o `fallback` declarado; AUSENTE nao
    vira chave nenhuma — ausencia NUNCA vira valor.
    """
    campos = o.get("campos")
    if not isinstance(campos, dict):
        return o
    for nome, item in campos.items():
        if not isinstance(item, dict) or "valor" not in item:
            continue
        estado = str(item.get("estado") or "").strip().upper()
        if estado == "PRESENTE":
            o.setdefault(nome, item.get("valor"))
        elif estado == "NAO_APLICAVEL" and item.get("fallback"):
            origem = campos.get(item["fallback"])
            if isinstance(origem, dict):
                o.setdefault(item["fallback"], origem.get("valor"))
    return o


def _obs_do_probe(caminho):
    """Le o JSON do probe AUT-4 (cru ou normalizado) — somente leitura."""
    if not caminho or not os.path.isfile(caminho):
        return []
    try:
        with open(caminho, encoding="utf-8") as fh:
            dados = json.load(fh)
    except (OSError, ValueError):
        return []
    obs = dados.get("observacoes") if isinstance(dados, dict) else dados
    if not isinstance(obs, list):
        return []
    saida = []
    for o in obs:
        if not isinstance(o, dict):
            continue
        o = _achata_campos(dict(o))
        o.setdefault("evidencia", caminho)
        saida.append(o)
    return saida


def criterios_guards(plano, leitura):
    """Guardas de turno/chat/mira.

    SEPARACAO QUE NAO SE DOBRA:
      * a PROVA de comportamento e runtime — so uma rodada (com sessao) fecha; o
        log nao diz EM QUE ESTADO do turno o clique aconteceu, entao recusa lida
        no log NUNCA promove o criterio;
      * o log entra como (i) evidencia anexada e (ii) detector de defeito: recusa
        com motivo fora do plano declarado e inconsistencia real -> REPROVADO.

    A-1 (AUT5-F2): o confronto do motivo e pela CHAVE (`chave_motivo` = texto ate o
    primeiro ` (`), a MESMA normalizacao que a checagem de fonte usa. Por igualdade
    exata, a recusa LEGITIMA de `mira-skill` (o produto emite o literal completo,
    com o sufixo `: abrir aqui cancelaria o apontar hex`) caia em "fora do plano".
    """
    itens = [g for g in (plano.get("guards_run") or {}).get("itens") or []]
    recusas = list(leitura.get("recusas") or [])
    ev_log = _ev([leitura["caminho"]]) if leitura.get("existe") else []
    out = []

    # A-8 (AUT5-F2): o item do atalho de texto nao pode aparecer em `recusas` — o
    # produto o registra como "RSTV-11: atalho F10 IGNORADO — <motivo>"
    # (SkillTreeShortcut.cs:69), nunca como "RSTV-5: abertura RECUSADA". Ele fica
    # no plano (e cobrado do produto como guarda), mas nao conta como cena
    # confrontavel por esta via.
    confrontaveis = [g for g in itens if g.get("confrontavel_em_recusas", True)]
    excluidos = [g["id"] for g in itens if not g.get("confrontavel_em_recusas", True)]
    motivos = {chave_motivo(g["motivo"]): g["id"] for g in itens}
    fora = sorted({m for m in recusas if chave_motivo(m) not in motivos})
    if fora:
        out.append(_crit(
            "AUT5-guards-motivo-fora-do-plano", MOD, REPROVADO, "offline", "execucao",
            "toda recusa registrada corresponde a uma guarda declarada no plano",
            "recusas com motivo nao declarado: %s" % fora,
            "DEFEITO: recusa com motivo fora do plano de risco (texto da guarda mudou ou "
            "existe guarda nova nao documentada)",
            ev_log, "RSTV-6"))

    exercitadas = sorted({motivos[chave_motivo(m)] for m in recusas
                          if chave_motivo(m) in motivos})
    c = _crit(
        "AUT5-guards-run-exercicio", MOD, NAO_EXERCITADO, "offline", "execucao",
        "cada cena de risco do RSTV-6 (turno de inimigo, mira de hex, mira de skill, "
        "janela aberta, agindo/movendo, posicionamento) produz a recusa com o motivo EXATO",
        "recusas no log: %s (confrontaveis em `recusas`: %d de %d itens declarados%s)"
        % (exercitadas or "nenhuma", len(confrontaveis), len(itens),
           "; fora desta via: " + ", ".join(excluidos) if excluidos else ""),
        "sem rodada autorizada: o log nao diz em que estado do turno o clique ocorreu, "
        "entao recusa lida no log nao prova a CENA; a prova e runtime",
        ev_log, "RSTV-6",
        {"campos_necessarios": ["RSTV-5: abertura RECUSADA — <motivo> por cena",
                                "sessao da rodada"],
         "cenarios": ["S3-level-up", "S4-run"],
         "guards_declaradas": len(itens),
         "guards_confrontaveis_em_recusas": len(confrontaveis),
         "guards_fora_desta_via": excluidos,
         "guards_exercitadas_no_log": exercitadas})
    out.append(_marcar_pendencia_runtime(
        c, "autorizacao",
        "Autorizar UMA rodada na run e clicar o botao 'Skills' em cada cena de risco: "
        "(b) durante o turno de um inimigo, (c) com a mira de hex ligada, (d) com o turno "
        "pronto, (e) abrir duas vezes, (f) fechar com X e com Esc."))
    return out


def criterios_falhas_produto(leitura):
    """A-2 (AUT5-F2): falha do PROPRIO mod no log -> REPROVADO.

    `leitura["falhas"]` era coletado e NENHUM criterio/decisao consumia: com uma
    falha real do gate de leitura-somente no log o delta de estados era ZERO e
    `AUT5-travas-readonly` seguia OK — o padrao "trava que passa a proteger menos
    continua verde".

    O criterio so EXISTE quando ha falha a reportar: "log sem falha do produto"
    nao e um criterio novo (nao se inventa OK nem se polui a contagem), e o vazio
    fica registrado em `relatorio["falhas_produto"]` para ser rastreavel.
    """
    falhas = list(leitura.get("falhas") or [])
    if not leitura.get("existe") or not falhas:
        return []
    return [_crit(
        "AUT5-falhas-produto-log", MOD, REPROVADO, "offline", "execucao",
        "nenhuma falha do proprio mod registrada no log da sessao",
        "%d linha(s) de falha do mod no log" % len(falhas),
        "FALHA DO PRODUTO no log: " + " | ".join(f[-240:] for f in falhas[:3])
        + (" (+%d)" % (len(falhas) - 3) if len(falhas) > 3 else ""),
        _ev([leitura["caminho"]]), "AUT-5",
        {"total_falhas": len(falhas), "falhas": falhas[:20]})]


def criterios_aceite_visual(plano, leitura):
    """Aceite de DESIGN: so olho humano — a automacao NAO aprova (DoD item 4)."""
    cenas = [c["id"] for c in plano.get("cenarios") or []]
    c = _crit(
        "AUT5-aceite-visual-design", MOD, NAO_EXERCITADO, "offline", "execucao",
        "bbox/clipping/ordem/hover/contraste conferidos em PNG por objeto",
        "nenhum PNG desta rodada (nenhum jogo aberto nesta tarefa)",
        "aceite de design exige olho humano sobre PNG do jogo (leitura de log nao basta)",
        _ev([leitura["caminho"]]) if leitura.get("existe") else [], "AUT-5",
        {"cenarios": cenas,
         "julgamento_humano": "Anexar PNG por cena (%s): janela aberta/fechada, hover por "
                              "objeto, arvore inteira (bbox/clipping) e o HUD da run."
                              % ", ".join(cenas)})
    return [_marcar_pendencia_runtime(c, "julgamento_visual")]


# ------------------------------------------------------------------- decisao ---

def carregar_decisao():
    cam = os.path.join(RAIZ_CICLO, "decisao.py")
    if not os.path.isfile(cam):
        return None, "decisao.py ausente"
    try:
        spec = importlib.util.spec_from_file_location("ciclo_decisao", cam)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, None
    except Exception as erro:
        return None, "%s: %s" % (type(erro).__name__, erro)


# ---------------------------------------------------------------- relatorio ----

def _resumo(criterios):
    cont = {}
    for c in criterios:
        cont[c["estado"]] = cont.get(c["estado"], 0) + 1
    return cont


def conduzir(repo, log, plano_cam, probe=None, perfil=None, com_decisao=True):
    with open(plano_cam, encoding="utf-8") as fh:
        plano = json.load(fh)
    ident = identidade_do_repo(repo, perfil)
    leitura = ler_log(log, dll_sha_conhecido=ident.get("dll_sha"),
                      dll_sha_declarado=ident.get("dll_perfil_sha"))

    criterios = []
    criterios += criterios_instrumentacao(repo, ident, leitura, plano)
    criterios += criterios_guardas_offline(plano)
    rstv_crit, erro_rstv = criterios_rstv(ident, leitura, plano, probe)
    criterios += rstv_crit
    criterios += criterios_guards(plano, leitura)
    # A-2 (AUT5-F2): falha do PROPRIO mod no log deixa de ser campo morto.
    criterios += criterios_falhas_produto(leitura)
    criterios += criterios_aceite_visual(plano, leitura)

    rel = {
        "esquema": "AUT5/relatorio/1",
        "tarefa": TAREFA,
        "mod": MOD,
        "identidade": {k: v for k, v in ident.items() if k != "fontes"},
        "identidade_contrato": identidade_do_cenario(ident),
        "fontes": ident.get("fontes"),
        "log": {k: v for k, v in leitura.items()
                if k not in ("contagens",) or True},
        # A-2: rastreabilidade do campo mesmo quando NAO ha falha (o criterio
        # `AUT5-falhas-produto-log` so existe quando ha o que reportar).
        "falhas_produto": {
            "total": len(leitura.get("falhas") or []),
            "linhas": (leitura.get("falhas") or [])[:20],
            "criterio": "AUT5-falhas-produto-log",
            "regra": "falha do proprio mod no log => criterio REPROVADO (exit 1); "
                     "ausencia de falha nao cria criterio",
        },
        "plano": plano_cam,
        "resumo": _resumo(criterios),
        "nao_exercitado": [{"id": c["id"], "estado": c["estado"], "motivo": c["motivo"],
                            "tipo_pendencia": c.get("tipo_pendencia"),
                            "tarefa_origem": c["tarefa_origem"]}
                           for c in criterios
                           if c["estado"] in (NAO_EXERCITADO, INDETERMINADO)],
        "reprovado": [{"id": c["id"], "motivo": c["motivo"]} for c in criterios
                      if c["estado"] == REPROVADO],
        "criterios": criterios,
        "erro_rstv": erro_rstv,
        "aviso": "AUSENTE/NAO_EXERCITADO/INDETERMINADO nunca sao OK. Automacao NAO "
                 "substitui aceite humano nem publicacao do DoD.",
    }

    if com_decisao and erro_rstv is None:
        mod, erro = carregar_decisao()
        if mod is None:
            rel["erro_decisao"] = erro
        else:
            try:
                dec = mod.consolidar(criterios, identidade_do_cenario(ident))
                rel["decisao"] = dec
                rel["decisao_sha256"] = sha256_file(os.path.join(RAIZ_CICLO, "decisao.py"))
            except Exception as erro2:
                rel["erro_decisao"] = "%s: %s" % (type(erro2).__name__, erro2)
    rel["exit"] = exit_de(criterios, rel)
    return rel


def criterios_guardas_offline(plano):
    """Nada aqui: as guardas sao cobradas na fonte (instrumentacao) e na rodada."""
    return []


def exit_de(criterios, rel):
    if rel.get("erro_rstv") or rel.get("erro_decisao"):
        return EXIT_NAO_RODOU
    if any(c["estado"] == REPROVADO for c in criterios):
        return EXIT_FALHOU
    if any(c["estado"] in (NAO_EXERCITADO, INDETERMINADO) for c in criterios):
        return EXIT_NAO_RODOU
    return EXIT_OK


def texto_humano(rel):
    l = []
    l.append("AUT-5 | %s | versao=%s | fonte_sha=%s | dll_sha=%s"
             % (rel["mod"], rel["identidade"].get("versao"),
                (rel["identidade"].get("fonte_sha") or "")[:16],
                (rel["identidade"].get("dll_sha") or "")[:16]))
    l.append("log: %s (%s bytes) | dll do perfil == repo: %s"
             % (os.path.basename(rel["log"].get("caminho") or "-"),
                rel["log"].get("bytes"), rel["identidade"].get("dll_perfil_igual_repo")))
    l.append("resumo: %s" % json.dumps(rel["resumo"], ensure_ascii=False))
    for c in rel["criterios"]:
        l.append("  [%s] %s (%s) — %s" % (c["estado"], c["id"], c["classe"], c["motivo"][:150]))
    if rel.get("decisao"):
        d = rel["decisao"]
        l.append("decisao: pronto_para_decisao=%s | falhas_automaticas=%d | pendencias_humanas=%d"
                 % (d.get("pronto_para_decisao"), len(d.get("falhas_automaticas") or []),
                    len(d.get("pendencias_humanas") or [])))
    if rel.get("erro_rstv"):
        l.append("ERRO rstv: %s" % rel["erro_rstv"])
    if rel.get("erro_decisao"):
        l.append("ERRO decisao: %s" % rel["erro_decisao"])
    return "\n".join(l)


def main(argv=None):
    ap = argparse.ArgumentParser(description="AUT-5: cenarios RSTV + prova de leitura somente.")
    ap.add_argument("--repo", default="C:/dev/stolen-realm")
    ap.add_argument("--log", default=None, help="LogOutput.log (somente leitura)")
    ap.add_argument("--plano", default=os.path.join(AQUI, "cenarios-rstv.json"))
    ap.add_argument("--probe", default=None, help="aut4probe.json (somente leitura)")
    ap.add_argument("--perfil", default=None, help="pasta BepInEx do perfil (so leitura)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--texto", action="store_true")
    ap.add_argument("--sem-decisao", action="store_true")
    args = ap.parse_args(argv)

    log = args.log
    if not log:
        perfil = args.perfil or os.path.join(
            os.environ.get("APPDATA", ""), "r2modmanPlus-local", "StolenRealm",
            "profiles", "Default", "BepInEx")
        log = os.path.join(perfil, "LogOutput.log")
        args.perfil = args.perfil or perfil
    if not os.path.isfile(log):
        print("AUT-5: LogOutput.log nao encontrado em %s" % log, file=sys.stderr)
        return EXIT_NAO_RODOU

    rel = conduzir(args.repo, log, args.plano, args.probe, args.perfil,
                   com_decisao=not args.sem_decisao)
    saida = json.dumps(rel, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(saida + "\n")
    if args.texto:
        print(texto_humano(rel))
    else:
        print(saida)
    return rel["exit"]


if __name__ == "__main__":
    sys.exit(main())
