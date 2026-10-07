#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""log_rstv.py — AUT-5: leitura SOMENTE LEITURA do `LogOutput.log` do RSTV.

O QUE ESTE ARQUIVO E
--------------------
O modulo de cenario RSTV (`tools/automacao/cenarios/rstv.py`, CIC-3) sabe julgar
as 7 capacidades RSTV-6/21/26/25b **se** receber as observacoes no formato do
contrato. Hoje o probe AUT-4 (CIC-5) so emite uma leitura por `TMP_Text`; ele NAO
emite o ciclo da janela, o pai/indice do tooltip, o snapshot antes/depois de
skills/pontos, nem as linhas por tier.

O `LogOutput.log` do proprio mod JA carrega parte disso — em marcadores que o mod
escreve para diagnostico (`RSTV-21: janela read-only ABERTA ...`,
`RSTV-25: nos com Dependency por tier — ...`, `RSTV-24b: N linha(s) ...`,
`RSTV-5: abertura RECUSADA — <motivo>`, `RSTV: gancho aplicado — ...`). Ler esse
arquivo e **somente leitura**, nao abre jogo, nao carrega save, nao instala nada e
usa instrumentacao que JA esta carregada — e exatamente o que a tarefa permite.

REGRA DE HONESTIDADE
--------------------
* Este modulo NUNCA promove nada a OK. Ele traduz bytes de log em (a)
  OBSERVACOES para o avaliador RSTV e (b) FATOS de boot/guarda com a linha
  literal. Quem decide OK/REPROVADO/NAO_EXERCITADO e o avaliador + a decisao.
* Marcador AUSENTE no log nao vira "ausencia legitima": vira `lacuna` com o
  marcador esperado declarado (e o texto do defeito correspondente na fonte).
* O log nao identifica a rodada (nao tem `sessao` desta tarefa). A identidade
  dele e a DLL que o escreveu — por isso `ler_log` aceita `dll_sha_conhecido`
  para confrontar os bytes; sem esse confronto a leitura e so `execucao`.
* Nenhum campo e inventado: se o log nao traz, sai em `lacunas`.

FORMATOS (fonte, nao suposicao). Cada regex abaixo foi transcrita de um
`Plugin.Log.LogInfo/LogWarning` do produto:
  * `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs:549`   RSTV-21 ABERTA
  * `RoguelikeSkillTreeVisualizer/SkillTreesWindow.cs:153` RSTV-21 fechada
  * `RoguelikeSkillTreeVisualizer/SkillTreesWindow.cs:274` RSTV-21 montada
  * `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs:1938`  RSTV-24b (o `por tier: T1:n, ...`
    e o AUT5-F1: e o unico lugar onde as linhas ATIVAS existem POR TIER)
  * `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs:1963`  RSTV-25
  * `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs:2032`  RSTV-24a
  * `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs:2052`  RSTV-23i
  * `RoguelikeSkillTreeVisualizer/RunButton.cs:410`       RSTV-5 RECUSADA
  * `RoguelikeSkillTreeVisualizer/RunTargets.cs:148`      motivos das guardas
  * `RoguelikeSkillTreeVisualizer/SkillTreeReadOnly.cs:50` RSTV-16 ATIVO
  * `RoguelikeSkillTreeVisualizer/Patches.cs:183`         RSTV-2 commit higienizado
"""
import hashlib
import os
import re

MOD = "RoguelikeSkillTreeVisualizer"

# Marcadores que a automacao EXIGE para poder julgar (chave -> (regex, tarefa)).
# Chave = o que a automacao perde quando o marcador desaparece.
MARCADORES = {
    "boot-versao": (
        re.compile(r"Roguelike Skill Tree Visualizer (?P<versao>[0-9][\w.\-]*) carregado"),
        "RSTV-6"),
    "gancho-aplicado": (
        re.compile(r"RSTV: gancho aplicado — (?P<nome>\S+) \((?P<metodos>\d+) metodo\(s\) do jogo\)"),
        "RSTV-6"),
    "readonly-ativo": (
        re.compile(r"RSTV-16: modo somente leitura ATIVO \(contexto=(?P<contexto>[^,]*), "
                   r"alvo=(?P<alvo>.*?)\)"),
        "RSTV-6"),
    "commit-higienizado": (
        re.compile(r"RSTV-2: commit higienizado \(read-only, closeMenu=(?P<close>[^)]*)\) — "
                   r"nenhuma escrita no personagem \((?P<n>\d+) skills no snapshot\)"),
        "RSTV-6"),
    "modal-gancho": (
        re.compile(r"RSTV-20: gancho do modal 'Remove Skill Trees' ATIVO"),
        "RSTV-21"),
    "modal-botao": (
        re.compile(r"RSTV-20: botao '(?P<rotulo>[^']*)' injetado no cabecalho do modal "
                   r"'Remove Skill Trees' \((?P<lado>[0-9.]+)x(?P<lado2>[0-9.]+) px, (?P<resto>.*)\)"),
        "RSTV-21"),
    "janela-aberta": (
        re.compile(r"RSTV-21: janela read-only ABERTA com TODAS as arvores "
                   r"\(alvo=(?P<alvo>.*?), contexto=(?P<contexto>.*?)\) — sem depender do inventario"),
        "RSTV-21"),
    "janela-fechada": (
        re.compile(r"RSTV-21: janela read-only fechada\."),
        "RSTV-21"),
    "janela-montada": (
        re.compile(r"RSTV-21: janela read-only montada — Canvas overlay \(sortingOrder (?P<ordem>-?\d+)"),
        "RSTV-21"),
    "tooltip-movido": (
        re.compile(r"RSTV-21: tooltip do jogo movido para DENTRO da janela"),
        "RSTV-21"),
    "hud-gancho": (
        re.compile(r"RSTV-5: gancho do HUD da run ATIVO \(CurrentCharacterUI\.InitSingleton\)"),
        "RSTV-6"),
    "hud-botao": (
        # RSTV-30: o botao da run mudou de casa (barra de baixo) e o log de injecao passou a publicar
        # TODOS os numeros da colocacao MEDIDA em runtime — a linha antiga ("a direita do Ping
        # Button / largura da linha") deixou de existir junto com a receita que a produzia.
        re.compile(r"RSTV-30: botao 'Skills' injetado na BARRA DE BAIXO do HUD \(largura=(?P<largura>[0-9.]+) px "
                   r"\(nativo (?P<nativo>[0-9.]+) px\), altura=(?P<altura>[0-9.]+) px; borda direita dos "
                   r"nativos=(?P<nativos>[0-9.]+) px, limite do vizinho '(?P<vizinho>[^']*)'=(?P<limite>[0-9.]+) px, "
                   r"vao livre=(?P<vao>-?[0-9.]+) px, margem=(?P<margem>[0-9.]+) px no espaco local de "
                   r"'(?P<container>[^']*)'\); pai=(?P<pai>[^ ]*)"),
        "RSTV-6"),
    "recusa-abertura": (
        re.compile(r"RSTV-5: abertura RECUSADA — (?P<motivo>.*?)\. Nada foi aberto\."),
        "RSTV-6"),
    "linhas-dependencia": (
        # AUT5-F1: o `por tier` e OPCIONAL — log de build anterior traz so o total
        # (e ai o confronto por tier continua impossivel, declarado como lacuna).
        re.compile(r"RSTV-24b: (?P<ativas>\d+) linha\(s\) de dependencia ativa\(s\), "
                   r"(?P<com_sprite>\d+) com sprite \(de (?P<nos>\d+) no\(s\)\); cor da 1a = (?P<cor>[^;]+)"
                   r"(?:; por tier: (?P<tiers>T\d+:\d+(?:,\s*T\d+:\d+)*))?\.\s*$"),
        "RSTV-25b"),
    "dependency-por-tier": (
        re.compile(r"RSTV-25: nos com Dependency por tier — (?P<tiers>T\d+:\d+/\d+(?:,\s*T\d+:\d+/\d+)*)\."),
        "RSTV-25b"),
    "arvore-centralizada": (
        re.compile(r"RSTV-24a: arvore centralizada na AREA \(bbox local (?P<minx>-?[0-9.]+)\.\.(?P<maxx>-?[0-9.]+) "
                   r"x (?P<miny>-?[0-9.]+)\.\.(?P<maxy>-[0-9.]+|[0-9.]+), pos (?P<posx>-?[0-9.]+),(?P<posy>-?[0-9.]+)u\)"),
        "RSTV-25b"),
    "arvore-excede-area": (
        re.compile(r"RSTV-23i: arvore excede a area \((?P<lb>[0-9.]+)x(?P<ab>[0-9.]+) > "
                   r"(?P<la>[0-9.]+)x(?P<aa>[0-9.]+)\) — escala do container reduzida por (?P<fator>[0-9.]+)x"),
        "RSTV-25b"),
    # A-2 (AUT5-F2, `t_9cee7d21`): o produto escreve a MAIORIA dos LogError como
    # "RSTV: falha ..." — SEM hifen (Patches.cs:41/113/189/.../697, Plugin.cs:172,
    # RunButton.cs:427, RstvHost.cs:78, ...) — e alguns como "RSTV-16: falha ...".
    # Exigir o hifen (regex antiga `RSTV-[0-9a-zA-Z]*: falha`) deixava a falha do
    # PROPRIO mod fora do relatorio: a trava que passa a proteger menos continuava
    # verde. Captura agora:
    #   (a) qualquer linha de LogError do logger do mod ([Error  :Roguelike Skill
    #       Tree Visualizer]) — inclusive "RSTV: FALHA ao aplicar o gancho" e o
    #       resumo "GANCHOS QUE FALHARAM";
    #   (b) o padrao RSTV[:|-]<id>: falha/FALHA em QUALQUER nivel de log (o produto
    #       tambem usa LogWarning/LogInfo para falha em alguns pontos).
    "falha": (
        re.compile(r"^\[Error\s*:\s*Roguelike Skill Tree Visualizer\]"
                   r"|RSTV-?[0-9a-zA-Z]*:\s*[Ff][Aa][Ll][Hh][Aa]"
                   r"|GANCHOS QUE FALHARAM"),
        None),
}

# Marcadores que a automacao EXIGE que existam NA FONTE (observabilidade).
# Se um deles desaparecer do fonte, a automacao deixa de conseguir julgar a
# capacidade correspondente -> REPROVADO (regressao de observabilidade).
MARCADORES_FONTE = {
    "RSTV-21: janela read-only ABERTA com TODAS as arvores": "RSTV-21",
    "RSTV-21: janela read-only fechada.": "RSTV-21",
    "RSTV-24b: ": "RSTV-25b",
    "RSTV-25: nos com Dependency por tier": "RSTV-25b",
    "RSTV-23i: arvore excede a area": "RSTV-25b",
    "RSTV-24a: arvore centralizada na AREA": "RSTV-25b",
    "RSTV-5: abertura RECUSADA — ": "RSTV-6",
    "RSTV-16: modo somente leitura ATIVO": "RSTV-6",
    "RSTV-2: commit higienizado": "RSTV-6",
}

# Guardas do botao da run (RSTV-6, itens (a)-(d) do roteiro do dono). Cada motivo
# e literal de `RunTargets.GateOk` — a automacao cobra que ele EXISTA na fonte,
# LIGADO a condicao que o protege, e, na rodada autorizada, que a recusa tenha
# saido com esse motivo.
#
# RSTV-30 (t_2cef3e03): a lista ENCOLHEU. Saíram `turno-inimigo`, `agindo` e
# `movendo` (`Root.IsPlayerTurnAndReady`, `Root.AnyActingCharactersInBattle`,
# `Root.AnyMovingCharactersInBattle`): o portao deixou de decidir a VISIBILIDADE do
# botao (passou a decidir so' o CLIQUE) e eram essas tres que faziam o botao piscar
# quando qualquer personagem agia — o defeito que o dono relatou em jogo em 06/10.
# Ficaram as guardas de DANO REAL (mira de hex, mira de skill, janela de UI aberta,
# posicionamento inicial), cada uma com a justificativa no proprio fonte
# (`GUARDA n` + `Justificativa:`), cobrada por `tools/testes/regras_rstv30.py`.
#
# A-1 (AUT5-F2): o motivo de `mira-skill` era declarado TRUNCADO aqui e no plano
# (sem o sufixo `: abrir aqui cancelaria o apontar hex`) enquanto
# `RunTargets.cs:231` emite o literal COMPLETO -> a recusa LEGITIMA caia em
# "fora do plano" (falso REPROVADO). O literal agora e o COMPLETO, e o confronto
# normaliza os dois lados pela MESMA chave (`chave_motivo`).
#
# `condicao` e o texto EXATO dentro do `if (...)` que produz aquele motivo
# (`RunTargets.GateOk`): e o que a checagem de fonte passou a exigir. Sem ela a
# checagem era de PRESENCA de texto: com `if (false && gui.PingModeActive)` na
# fonte o criterio continuava OK (A-3).
GUARDAS = (
    ("mira-hex", "modo de apontar o hex ligado (GUIManager.PingModeActive)",
     "gui.PingModeActive"),
    ("janela-aberta", "ja existe uma janela de UI aberta (UIWindowManager.OpenedWindows)",
     "wm != null && wm.AnyUIWindowOpen"),
    ("mira-skill",
     "mira de skill ativa (HexCellManager.CurrentState=Action): abrir aqui cancelaria o apontar hex",
     "hcm != null && hcm.CurrentState == PlayerState.Action"),
    ("posicionamento", "posicionamento inicial em andamento (Root.SpawnPlacementActive)",
     "root.SpawnPlacementActive"),
)

# A-3 (AUT5-F2): bloco da guarda — `if (<condicao>) { ... motivo = "<texto>"; ...
# return false; ... }`. A condicao entre parenteses NAO pode conter outro
# parentese (nenhuma das guardas tem), o que deixa o casamento EXATO: uma guarda
# neutralizada (`if (false && gui.PingModeActive)`) deixa de casar.
_RX_BLOCO_GUARDA = re.compile(r"if\s*\((?P<cond>[^()\n]*)\)\s*\{(?P<corpo>[^{}]*)\}")
_RX_MOTIVO_NO_BLOCO = re.compile(r'motivo\s*=\s*"([^"]*)"')


def chave_motivo(motivo):
    """Chave de confronto do motivo: o texto ATE o primeiro ` (`.

    E a MESMA normalizacao que a checagem de FONTE ja usava. O produto acrescenta
    a excecao entre parenteses (`... (Root.IsPlayerTurnAndReady=false)`) e, em
    `mira-skill`, um sufixo depois dela (`: abrir aqui cancelaria o apontar hex`);
    nada disso e a IDENTIDADE da guarda. Comparar por igualdade exata (log) contra
    o texto do plano fazia a recusa LEGITIMA cair em "fora do plano" (A-1).
    """
    return (motivo or "").split(" (")[0].strip()


def guarda_ligada(texto, condicao, motivo):
    """A guarda esta na fonte LIGADA a condicao esperada e fechando o caminho?

    Devolve `(True, None)` ou `(False, <por que>)`. Conservador: exige o `if`
    com a condicao EXATA, o `motivo = "<...>"` no MESMO bloco e o `return false;`
    que fecha o caminho. Presenca do texto do motivo em qualquer lugar do arquivo
    NAO basta (era o furo A-3).
    """
    if not texto:
        return False, "fonte ausente"
    chave = chave_motivo(motivo)
    tem_condicao = False
    for m in _RX_BLOCO_GUARDA.finditer(texto):
        if m.group("cond").strip() != condicao:
            continue
        tem_condicao = True
        corpo = m.group("corpo")
        citados = [chave_motivo(t) for t in _RX_MOTIVO_NO_BLOCO.findall(corpo)]
        if chave not in citados:
            continue
        if "return false;" not in corpo:
            return False, "bloco da condicao sem 'return false' (guarda nao fecha o caminho)"
        return True, None
    if tem_condicao:
        return False, "condicao presente mas sem 'motivo = \"%s\"' no mesmo bloco" % chave
    return False, "condicao 'if (%s)' ausente ou alterada na fonte" % condicao

# Marcadores de fonte das guardas de leitura somente (nenhuma escrita no personagem).
GATES_READONLY = ("SkillTreeManagerAcceptSkillChangesPatch",
                  "SkillTreeManagerResetSkillPointsPatch")


def sha256_file(caminho):
    if not caminho or not os.path.isfile(caminho):
        return None
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _linhas(caminho):
    with open(caminho, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def ler_log(caminho, dll_sha_conhecido=None, dll_sha_declarado=None):
    """Le o `LogOutput.log` (SOMENTE LEITURA) e devolve os fatos do RSTV.

    `dll_sha_conhecido` = sha da DLL atual (bytes da build em analise). Se o log
    nao identifica a DLL, a leitura fica `identifica_build=False` e NADA dela
    pode virar prova — o chamador tem de tratar isso como lacuna.
    """
    saida = {
        "caminho": os.path.abspath(caminho) if os.path.isfile(caminho) else caminho,
        "existe": os.path.isfile(caminho),
        "sha256": sha256_file(caminho),
        "bytes": os.path.getsize(caminho) if os.path.isfile(caminho) else 0,
        "linhas": 0,
        "versao": None,
        "ganchos": [],
        "ganchos_ro_ok": False,
        "gancho_ro_ausente": [],
        "modais": {"gancho": False, "botoes": []},
        "hud": {"gancho": False, "botao": None},
        "sessoes_readonly": [],
        "commits_higienizados": 0,
        "janelas": [],
        "tooltip_movido": 0,
        "linhas_dependencia": None,
        # AUT5-F1: contagem de linhas ATIVAS por tier (`RSTV-24b` com o `por tier`)
        # — sem ela o confronto com o Dependency real (RSTV-25) so fecha no TOTAL.
        "linhas_por_tier": None,
        "dependency_por_tier": None,
        "geometria_arvore": None,
        "recusas": [],
        "falhas": [],
        "contagens": {},
        "marcadores_ausentes": [],
        "lacunas": [],
        "dll_sha_declarado": dll_sha_declarado,
        "dll_sha_conhecido": dll_sha_conhecido,
        "identifica_build": bool(dll_sha_declarado) and bool(dll_sha_conhecido)
        and dll_sha_declarado == dll_sha_conhecido,
    }
    if not saida["existe"]:
        saida["lacunas"].append({"id": "log-ausente",
                                 "motivo": "LogOutput.log nao encontrado em %s" % caminho,
                                 "marcadores": sorted(MARCADORES)})
        return saida

    cont = {k: 0 for k in MARCADORES}
    janela_atual = None
    saida["janelas_montadas"] = 0
    saida["fechamentos_orfaos"] = 0
    pendente_montagem = 0
    for linha in _linhas(caminho):
        achou = False
        for chave, (rx, _tarefa) in MARCADORES.items():
            m = rx.search(linha)
            if not m:
                continue
            achou = True
            cont[chave] += 1
            g = m.groupdict()
            if chave == "boot-versao":
                saida["versao"] = g["versao"]
            elif chave == "gancho-aplicado":
                saida["ganchos"].append(g["nome"])
            elif chave == "readonly-ativo":
                saida["sessoes_readonly"].append({"contexto": g["contexto"].strip(),
                                                  "alvo": g["alvo"].strip()})
            elif chave == "commit-higienizado":
                saida["commits_higienizados"] += 1
            elif chave == "modal-gancho":
                saida["modais"]["gancho"] = True
            elif chave == "modal-botao":
                saida["modais"]["botoes"].append(
                    {"rotulo": g["rotulo"], "lado_px": float(g["lado"]),
                     "pai": g["resto"][:120]})
            elif chave == "janela-aberta":
                # SO a abertura cria um ciclo: `montada`/`fechada` se anexam a ele.
                janela_atual = {"alvo": g["alvo"].strip(), "contexto": g["contexto"].strip(),
                                "aberta": True, "fechada": False,
                                "montada": pendente_montagem > 0}
                pendente_montagem = 0
                saida["janelas"].append(janela_atual)
            elif chave == "janela-montada":
                # a montagem precede a abertura na ordem real do mod (RSTV-21 monta e
                # depois ABRE): se ainda nao ha ciclo aberto, fica pendente e se anexa
                # ao proximo ciclo; nunca vira um ciclo "sem abertura" (seria um
                # DEFEITO inventado pela leitura).
                saida["janelas_montadas"] += 1
                if janela_atual is None:
                    pendente_montagem += 1
                else:
                    janela_atual["montada"] = True
                    janela_atual["sorting_order"] = int(g["ordem"])
            elif chave == "janela-fechada":
                if janela_atual is not None:
                    janela_atual["fechada"] = True
                else:
                    saida["fechamentos_orfaos"] += 1
            elif chave == "tooltip-movido":
                saida["tooltip_movido"] += 1
            elif chave == "hud-gancho":
                saida["hud"]["gancho"] = True
            elif chave == "hud-botao":
                # RSTV-30: a linha de injecao publica a colocacao MEDIDA (barra de baixo) — largura do
                # clone, largura NATIVA, vao livre, limite do vizinho e container. O par antigo
                # "linha_antes/linha_depois" (largura da linha do Ping) deixou de existir junto com a
                # receita que o produzia; o que garante "nao empurrou nem sobrepoe nada" passou a ser
                # a largura caber no vao livre.
                saida["hud"]["botao"] = {
                    "largura_px": float(g["largura"]), "nativo_px": float(g["nativo"]),
                    "altura_px": float(g["altura"]), "vao_px": float(g["vao"]),
                    "limite_px": float(g["limite"]), "nativos_px": float(g["nativos"]),
                    "pai": g["pai"].strip(), "vizinho": g["vizinho"].strip(),
                    "container": g["container"].strip()}
            elif chave == "recusa-abertura":
                saida["recusas"].append(g["motivo"].strip())
            elif chave == "linhas-dependencia":
                saida["linhas_dependencia"] = {"ativas": int(g["ativas"]),
                                               "com_sprite": int(g["com_sprite"]),
                                               "nos": int(g["nos"]), "cor": g["cor"]}
                linhas_por_tier = {tier: int(n)
                                   for tier, n in re.findall(r"(T\d+):(\d+)", g.get("tiers") or "")}
                saida["linhas_por_tier"] = linhas_por_tier or None
            elif chave == "dependency-por-tier":
                por = {}
                for tier, com, total in re.findall(r"(T\d+):(\d+)/(\d+)", g["tiers"] or ""):
                    por[tier] = {"com_dependency": int(com), "nos": int(total)}
                saida["dependency_por_tier"] = por
            elif chave == "arvore-centralizada":
                # merge por DICIONARIO (nao por substituicao): a ordem das duas linhas
                # no log nao pode decidir o resultado (RSTV-24a/RSTV-23i sao independentes)
                geo = saida["geometria_arvore"] or {}
                geo.update({"bbox_local": {"minx": float(g["minx"]), "maxx": float(g["maxx"]),
                                           "miny": float(g["miny"]), "maxy": float(g["maxy"])},
                            "pos": {"x": float(g["posx"]), "y": float(g["posy"])}})
                geo.setdefault("excede_area", False)
                geo.setdefault("fator_escala", None)
                saida["geometria_arvore"] = geo
            elif chave == "arvore-excede-area":
                geo = saida["geometria_arvore"] or {}
                geo.update({"excede_area": True, "fator_escala": float(g["fator"]),
                            "bbox_px": {"largura": float(g["lb"]), "altura": float(g["ab"])},
                            "area_px": {"largura": float(g["la"]), "altura": float(g["aa"])}})
                geo.setdefault("bbox_local", None)
                geo.setdefault("pos", None)
                saida["geometria_arvore"] = geo
            elif chave == "falha":
                saida["falhas"].append(linha.strip()[-200:])
        if not achou and ("RSTV-" in linha or "Roguelike Skill Tree Visualizer" in linha):
            # linha do mod que nenhum marcador reconhece — registra so o prefixo,
            # para o relatorio poder dizer "ha log do mod que a automacao nao le".
            m = re.search(r"(RSTV-[0-9a-zA-Z]*)", linha)
            if m:
                cont.setdefault("nao-reconhecido:" + m.group(1), 0)
                cont["nao-reconhecido:" + m.group(1)] += 1

    saida["linhas"] = len(_linhas(caminho))
    saida["contagens"] = cont
    nomes = set(saida["ganchos"])
    saida["gancho_ro_ausente"] = [g for g in GATES_READONLY if g not in nomes]
    saida["ganchos_ro_ok"] = not saida["gancho_ro_ausente"]

    # marcadores esperados que nao apareceram em NENHUMA linha
    for chave, (rx, tarefa) in MARCADORES.items():
        if chave in ("falha", "recusa-abertura", "commit-higienizado"):
            continue  # eventos legitimamente ausentes numa sessao
        if cont.get(chave, 0) == 0:
            saida["marcadores_ausentes"].append({"marcador": chave, "tarefa": tarefa})

    # lacunas declaradas (o log NAO traz isto) — nada de inventar campo
    if saida["dependency_por_tier"] and saida["linhas_dependencia"] is not None \
            and not saida["linhas_por_tier"]:
        saida["lacunas"].append({
            "id": "linhas-por-tier",
            "motivo": "RSTV-24b so da o TOTAL de linhas ativas; NAO da a contagem por tier "
                      "-> o confronto linhas x Dependency por tier segue impossivel pelo log "
                      "(log de build ANTERIOR ao AUT5-F1, que passou a emitir o 'por tier')",
            "marcador": "RSTV-24b/RSTV-25",
            "tarefa": "RSTV-25b"})
    if saida["dependency_por_tier"] and saida["linhas_dependencia"] is None:
        saida["lacunas"].append({
            "id": "linhas-dependencia",
            "motivo": "o log tem o RSTV-25 (Dependency por tier) mas nenhum RSTV-24b "
                      "(linhas ativas): sem os dois lados nao ha confronto",
            "marcador": "RSTV-24b",
            "tarefa": "RSTV-25b"})
    if not saida["janelas"]:
        saida["lacunas"].append({
            "id": "janela-nao-exercitada",
            "motivo": "nenhum 'RSTV-21: janela read-only ABERTA' na sessao: o ciclo "
                      "abrir/fechar e a restauracao do tooltip NAO foram exercitados",
            "marcador": "RSTV-21", "tarefa": "RSTV-21"})
    if cont.get("commit-higienizado", 0) == 0:
        saida["lacunas"].append({
            "id": "sem-commit-na-sessao",
            "motivo": "nenhum 'RSTV-2: commit higienizado' na sessao: a guarda de leitura "
                      "somente existe na fonte, mas NAO foi exercitada nesta sessao",
            "marcador": "RSTV-2", "tarefa": "RSTV-6"})
    return saida


def _defeitos_por_tier(linhas_por_tier, dep):
    """Confronto POR TIER: linhas ATIVAS do tier x nos COM Dependency do tier.

    Mesma regra derivada do codigo (nao inventada), aplicada tier a tier: cada no
    com `SkillInfo.Dependency != null` tem de ter a `DependencyLine` ATIVA — logo
    linhas ATIVAS do tier == nos COM Dependency do tier, EXATAMENTE (faltando
    linha = conector ausente; sobrando = aresta inventada). `T5` sem Dependency e
    AUSENCIA LEGITIMA: com 0 nos e 0 linhas, casa.
    Devolve a lista de inconsistencias (vazia = tier a tier consistente).
    """
    inconsistencias = []
    tiers = sorted(set(list(linhas_por_tier or {}) + list(dep or {})),
                   key=lambda t: int(str(t)[1:]) if str(t)[1:].isdigit() else 0)
    for tier in tiers:
        n_lin = (linhas_por_tier or {}).get(tier)
        n_dep = ((dep or {}).get(tier) or {}).get("com_dependency")
        if n_lin is None:
            inconsistencias.append({"tier": tier, "linhas": None, "dependency": n_dep,
                                    "defeito": "tier SEM contagem de linhas no RSTV-24b"})
            continue
        if n_dep is None:
            inconsistencias.append({"tier": tier, "linhas": n_lin, "dependency": None,
                                    "defeito": "Dependency do tier AUSENTE no RSTV-25"})
            continue
        if n_lin == n_dep:
            continue
        if n_lin < n_dep:
            inconsistencias.append({"tier": tier, "linhas": n_lin, "dependency": n_dep,
                                    "defeito": "%s com Dependency=%d e apenas %d linha(s) ativa(s) "
                                               "(conector AUSENTE)" % (tier, n_dep, n_lin)})
        else:
            inconsistencias.append({"tier": tier, "linhas": n_lin, "dependency": n_dep,
                                    "defeito": "%s com %d linha(s) ativa(s) e Dependency=%d "
                                               "(aresta INVENTADA)" % (tier, n_lin, n_dep)})
    return inconsistencias


def consistencia_dependencia(leitura):
    """Confronto LOG-side entre o Dependency REAL (RSTV-25) e os conectores (RSTV-24b).

    Regra (conservadora, derivada do codigo, nao inventada): `SkillTreesTab` monta
    um `DependencyLine` por item e a ativa exatamente quando o item tem
    `SkillInfo.Dependency != null` (l.1923-1937); o RSTV-25 conta os nos COM
    Dependency por tier (l.1941-1963). Logo a soma dos nos com Dependency tem de
    casar com o numero de linhas ativas. Faltando linha para no com Dependency real
    = o sintoma do RSTV-25b (conector ausente); sobrando linha = conector sem
    Dependency (aresta inventada).

    AUT5-F1: quando o log traz a contagem POR TIER (`RSTV-24b ... por tier:`), o
    confronto e feito TIER A TIER — e o que fecha o `RSTV-25b-dependencia`; sem ela
    (build anterior) so o TOTAL e confrontavel.

    Devolve dict ou None quando o log nao traz os dois lados.
    """
    dep = leitura.get("dependency_por_tier")
    lin = leitura.get("linhas_dependencia")
    if not dep or not lin:
        return None
    por_tier_linhas = leitura.get("linhas_por_tier")
    soma = sum(t["com_dependency"] for t in dep.values())
    t5 = dep.get("T5") or {}
    inconsistencias = _defeitos_por_tier(por_tier_linhas, dep) if por_tier_linhas else []
    return {
        "soma_com_dependency": soma,
        "linhas_ativas": lin["ativas"],
        "nos": lin["nos"],
        "com_sprite": lin["com_sprite"],
        "por_tier": dep,
        "por_tier_linhas": por_tier_linhas,
        "por_tier_ok": (bool(por_tier_linhas) and not inconsistencias) if por_tier_linhas else None,
        "inconsistencias_por_tier": inconsistencias,
        "t5_sem_dependency": bool(t5) and t5.get("com_dependency", 0) == 0,
        "t5_nos": (t5 or {}).get("nos", 0),
        "conector_ausente": lin["ativas"] < soma,
        "conector_sem_dependency": lin["ativas"] > soma,
    }


def observacoes(leitura, evidencia=None, dll_sha=None):
    """Traduz a leitura do log em OBSERVACOES do contrato do avaliador RSTV.

    `dll_sha` (opcional) entra na observacao para o avaliador confrontar com a
    identidade: se a DLL que escreveu o log nao for a build atual, o avaliador
    marca INDETERMINADO ("bytes diferentes") — exatamente o que se quer.

    NUNCA devolve `procedencia='runtime'`: o log nao tem `sessao` desta rodada.
    """
    ev = [evidencia] if isinstance(evidencia, str) else list(evidencia or [])
    obs = []

    for janela in leitura.get("janelas") or []:
        o = {"objeto": "SkillTreesWindow (RSTV-21)", "procedencia": "execucao",
             "evidencia": ev,
             "janela": {"aberta": bool(janela.get("aberta")),
                        "fechada": bool(janela.get("fechada"))}}
        if dll_sha:
            o["dll_sha"] = dll_sha
        # o ALVO vem do log; o ESPERADO e do cenario (nunca do proprio log).
        o["personagem_logado"] = janela.get("alvo")
        if janela.get("aberta"):
            o["personagem"] = {"personagem": janela.get("alvo"),
                               "gui_state": janela.get("contexto")}
        obs.append(o)

    if leitura.get("linhas_dependencia") and leitura.get("dependency_por_tier"):
        o = {"objeto": "SkillTreesTab (RSTV-25b)", "procedencia": "execucao",
             "evidencia": ev,
             "dependency_por_tier": {k: v["com_dependency"]
                                     for k, v in leitura["dependency_por_tier"].items()},
             "dependency_nos_por_tier": {k: v["nos"]
                                         for k, v in leitura["dependency_por_tier"].items()},
             "linhas_ativas_total": leitura["linhas_dependencia"]["ativas"],
             "linhas_com_sprite": leitura["linhas_dependencia"]["com_sprite"],
             "nos_total": leitura["linhas_dependencia"]["nos"]}
        # AUT5-F1: as linhas ATIVAS por tier existem no log (RSTV-24b com o
        # `por tier`) -> o confronto por tier do avaliador deixa de ser impossivel.
        # Sem o campo (build anterior) NAO se inventa zero: fica AUSENTE.
        if leitura.get("linhas_por_tier"):
            o["linhas_dependencia"] = dict(leitura["linhas_por_tier"])
            o["linhas_por_tier_fonte"] = "RSTV-24b (por tier, AUT5-F1)"
        if dll_sha:
            o["dll_sha"] = dll_sha
        obs.append(o)

    if leitura.get("geometria_arvore"):
        g = leitura["geometria_arvore"]
        bbox = g.get("bbox_local") or {}
        o = {"objeto": "SkillTreesTab (geometria)", "procedencia": "execucao",
             "evidencia": ev, "geometria_arvore": g,
             "bbox_local": bbox}
        if dll_sha:
            o["dll_sha"] = dll_sha
        obs.append(o)

    return obs
