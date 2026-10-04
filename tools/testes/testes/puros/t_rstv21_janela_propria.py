#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A JANELA read-only PROPRIA DO MOD (sem o inventario) — RSTV-21.

O QUE ISTO TRAVA
----------------
O botao 'Skills' injetado no modal 'Remove Skill Trees' aparecia e o clique nao abria nada: o
`onClick` chamava `SkillTreesTab.Abrir`, que abre o INVENTARIO — e na tela de PARTY SELECT o
`CharacterMenusManager.OpenCharacterMenu` nao abre (o personagem nao esta em `AllMyCharacters`).
Log do defeito (03/10):

    RSTV-20: clique no botao Skills do modal -> ... na aba All Trees do inventario.
    RSTV-16: abrindo o inventario (CharacterMenusManager.OpenCharacterMenu) ...
    RSTV-16: o inventario nao abriu em 5 s ... o pedido foi descartado.

A RSTV-21 faz o clique abrir uma JANELA PROPRIA (Canvas em overlay, escalado como o jogo) que
hospeda o MESMO painel "All Skill Trees" da run — sem o inventario.

AS 6 REGRAS (viram checagem)
----------------------------
1. `SkillTreesTab.AbrirJanela(alvo, contexto, dono)` NAO abre o inventario (nem seleciona aba);
   o `Abrir` do inventario (RSTV-16) continua intacto;
2. a janela tem raiz propria `DontDestroyOnLoad` + Canvas overlay + GraphicRaycaster + CanvasScaler
   copiado do jogo + fundo que consome o clique;
3. a vida da janela segue o DONO: `DonoVivo` exige o dono em cena e `Atualizar` FECHA quando ele
   sai;
4. o canvas do TOOLTIP do jogo sobe acima da janela enquanto ela esta aberta e VOLTA ao lugar no
   `Fechar` (senao o hover do noh mostraria um tooltip ilegivel atras do fundo);
5. o botao do modal chama `AbrirJanela` (nunca o `Abrir` do inventario);
6. nenhum arquivo novo tem caminho de ESCRITA no personagem (read-only de verdade).

DE ONDE VEM O ESPERADO
----------------------
Regras em `tools/testes/regras_rstv21.py`; fontes lidos AO VIVO do mod (nunca copias). O que NAO se
prova aqui (so o dono confirma, em tela): a janela APARECER, as arvores desenharem e o tooltip
ficar legivel.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "rstv21-janela-propria",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-21: o clique do botao do modal abre uma JANELA read-only PROPRIA (Canvas "
                  "overlay escalado como o jogo) com TODAS as arvores, sem depender do inventario; a "
                  "janela segue o dono (fecha quando o modal sai), o tooltip do jogo sobe acima dela e "
                  "nenhum arquivo tem caminho de escrita no personagem"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    src_janela = reg.fonte(reg.caminho_janela())
    src_remocao = reg.fonte(reg.caminho_remocao())

    for nome, src in (("SkillTreesTab.cs", src_tab), ("SkillTreesWindow.cs", src_janela),
                      ("RemovalWindowSkillsButton.cs", src_remocao)):
        arc.exigir(len(src) > 1000, "o fonte %s veio vazio/curto: a leitura mudou de lugar?" % nome)

    # 1) O CAMINHO DO MODAL: abre a JANELA, nunca o inventario (a causa raiz do clique morto).
    falhas = reg.falhas_do_abrirjanela(src_tab)
    arc.exigir(not falhas, "o caminho do modal regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) O DESVIO DO HOSPEDEIRO: o painel nasce sob a janela e a vida da visao muda com o modo.
    falhas = reg.falhas_do_desvio_do_hospedeiro(src_tab)
    arc.exigir(not falhas, "o desvio de hospedeiro regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 3) A JANELA: canvas proprio acima do jogo, fundo que come clique, dono e tooltip.
    falhas = reg.falhas_da_janela(src_janela)
    arc.exigir(not falhas, "a janela regrediu em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # 3b) O FECHAMENTO (RSTV-21R): o `_modoJanela` e LARGADO nos DOIS caminhos — o botao Close e o
    #     `Atualizar`/dono fora. Os dois passam pelo funil `Fechar` -> aviso `Fechou` -> `AoFecharJanela`.
    falhas = reg.falhas_do_fechamento(src_tab, src_janela)
    arc.exigir(not falhas, "o fechamento regrediu em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # 3c) O MODELO PURO DO RESET: fechou a janela -> o modo janela e largado; sem o reset, fica pendurado.
    arc.exigir(not reg.modo_janela_apos_fechar(True, True),
               "o modelo nao larga o modo janela quando a janela fecha com o reset de pe")
    arc.exigir(reg.modo_janela_apos_fechar(True, False) is True,
               "o modelo do defeito nao deixa o modo PENDURADO sem o reset: ele nao prova nada")
    arc.exigir(reg.modo_janela_sem_reset(True) is True,
               "o modelo do defeito do RSTV-21A nao reproduz o flag pendurado")
    arc.exigir(reg.reset_ao_fechar_ok(True, True, True), "a corrente inteira do reset devia valer")
    arc.exigir(not reg.reset_ao_fechar_ok(True, False, True),
               "sem o `Fechar` avisar, a corrente do reset nao pode valer")
    arc.exigir(not reg.reset_ao_fechar_ok(True, True, False),
               "sem o reset no aviso, a corrente do reset nao pode valer")
    arc.exigir(not reg.reset_ao_fechar_ok(False, True, True),
               "sem a inscricao no aviso, a corrente do reset nao pode valer")

    # 4) O CLIQUE DO MODAL: AbrirJanela, com o contexto certo.
    falhas = reg.falhas_do_clique_do_modal(src_remocao)
    arc.exigir(not falhas, "o clique do modal regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 5) READ-ONLY DE VERDADE: nenhum caminho de escrita no personagem nos arquivos da RSTV-21.
    falhas = reg.falhas_de_escrita((("SkillTreesTab.cs", src_tab), ("SkillTreesWindow.cs", src_janela),
                                    ("RemovalWindowSkillsButton.cs", src_remocao)))
    arc.exigir(not falhas, "a RSTV-21 ganhou caminho de ESCRITA: %s" % " | ".join(falhas))

    # 6) O MODELO PURO DO HOSPEDEIRO: o modo janela NAO abre o inventario — e o defeito DIVERGE.
    arc.igual(reg.host_escolhido(True), reg.HOST_JANELA, "o hospedeiro no modo janela")
    arc.igual(reg.host_escolhido(False), reg.HOST_ABA, "o hospedeiro no modo aba")
    arc.exigir(not reg.abre_inventario(reg.host_escolhido(True)),
               "o modelo diz que o modo janela abre o inventario — e a causa raiz do clique morto")
    arc.exigir(reg.abre_inventario(reg.host_escolhido(False)),
               "o modelo diz que o modo aba NAO abre o inventario — a aba do RSTV-16 regrediu")
    arc.igual(reg.host_com_inventario_sempre(True), reg.HOST_ABA,
              "o modelo do defeito (todo hospedeiro abre o inventario)")
    arc.exigir(reg.abre_inventario(reg.host_com_inventario_sempre(True)),
               "o modelo do defeito nao abre o inventario: ele nao prova nada")

    # 6b) O MODELO PURO DO CICLO DE VIDA: a janela segue o dono.
    arc.exigir(reg.janela_visivel(True, True), "a janela some com a raiz ligada e o dono vivo")
    arc.exigir(not reg.janela_visivel(True, False), "a janela fica visivel com o dono FORA de cena")
    arc.exigir(reg.deve_fechar(True, False), "o `Atualizar` nao fecharia a janela com o dono fora")
    arc.exigir(not reg.deve_fechar(True, True), "o `Atualizar` fecharia a janela com o dono vivo")
    arc.exigir(not reg.deve_fechar(False, False), "o `Atualizar` fecharia uma janela ja desligada")

    # 7) PROVA DE FOGO 1: o clique de volta no `Abrir` do inventario (o defeito original) REPROVA.
    volta = reg.fonte_com_volta_ao_inventario(src_remocao)
    arc.exigir(volta != src_remocao,
               "o plantio 'volta ao inventario' nao encontrou a ancora do clique: a checagem nao le "
               "o trecho certo")
    falhas = reg.falhas_do_clique_do_modal(volta)
    arc.exigir(len(falhas) >= 1 and any("Abrir(" in f or "inventario" in f for f in falhas),
               "as checagens PASSARAM (ou reprovaram por outro motivo) com o clique de volta no "
               "inventario: %s" % " | ".join(falhas))

    # 8) PROVA DE FOGO 2: `OpenCharacterMenu` dentro do `AbrirJanela` REPROVA pelo motivo certo.
    com_menu = reg.fonte_com_inventario_no_abrirjanela(src_tab)
    arc.exigir(com_menu != src_tab,
               "o plantio 'inventario no AbrirJanela' nao encontrou a ancora (`IniciarSessaoReadOnly/"
               "Mostrar`): a checagem nao le o trecho certo")
    falhas = reg.falhas_do_abrirjanela(com_menu)
    arc.exigir(len(falhas) >= 1 and any("OpenCharacterMenu" in f for f in falhas),
               "as checagens PASSARAM com o inventario de volta no AbrirJanela: %s" % " | ".join(falhas))

    # 9) PROVA DE FOGO 3: sem a raiz propria (DontDestroyOnLoad), a janela REPROVA.
    sem_raiz = reg.fonte_sem_raiz_propria(src_janela)
    arc.exigir(sem_raiz != src_janela,
               "o plantio 'sem raiz propria' nao encontrou a ancora (`DontDestroyOnLoad`): a checagem "
               "nao le o trecho certo")
    falhas = reg.falhas_da_janela(sem_raiz)
    arc.exigir(len(falhas) >= 1 and any("DontDestroyOnLoad" in f for f in falhas),
               "as checagens PASSARAM sem a raiz DontDestroyOnLoad: %s" % " | ".join(falhas))

    # 10) PROVA DE FOGO 4: sem o dono no `Atualizar`, a janela nao se fecharia — REPROVA.
    sem_dono = reg.fonte_sem_dono_no_atualizar(src_janela)
    arc.exigir(sem_dono != src_janela,
               "o plantio 'sem dono no Atualizar' nao encontrou a ancora (`!DonoVivo()`): a checagem "
               "nao le o trecho certo")
    falhas = reg.falhas_da_janela(sem_dono)
    arc.exigir(len(falhas) >= 1 and any("DonoVivo" in f or "dono" in f for f in falhas),
               "as checagens PASSARAM com o `Atualizar` sem olhar o dono: %s" % " | ".join(falhas))

    # 10b) PROVA DE FOGO 4b (ACHADO da RSTV-21CR): a checagem antiga prendia o caminho (b) so pela
    #      PRESENCA do token `DonoVivo()`. INVERTER a polaridade (`!DonoVivo()` -> `DonoVivo()`) —
    #      fechar com o modal ABERTO e deixar a janela pendurada quando o dono saisse — passava em
    #      BRANCO. Agora os DOIS lados do caminho (b) (`falhas_da_janela` E `falhas_do_fechamento`)
    #      tem de REPROVAR pelo motivo do gatilho.
    invertida = reg.fonte_com_polaridade_invertida_no_atualizar(src_janela)
    arc.exigir(invertida != src_janela,
               "o plantio 'polaridade invertida' nao encontrou `!DonoVivo()` no `Atualizar`: a "
               "checagem nao le o trecho certo")
    for nome, falhas in (("falhas_da_janela", reg.falhas_da_janela(invertida)),
                         ("falhas_do_fechamento", reg.falhas_do_fechamento(src_tab, invertida))):
        arc.exigir(len(falhas) >= 1,
                   "`%s` PASSOU em BRANCO com o `Atualizar` de polaridade INVERTIDA (`DonoVivo()` "
                   "em vez de `!DonoVivo()`): a checagem nao prende a polaridade do gatilho"
                   % nome)
        arc.exigir(any("dono" in f or "DonoVivo" in f or "polaridade" in f for f in falhas),
                   "`%s` reprovou a polaridade invertida, mas nao pelo gatilho: %s"
                   % (nome, " | ".join(falhas)))

    # 10c) PROVA DE FOGO 4c (ACHADO da RSTV-21CR): remover `_root.activeSelf` da condicao do
    #      `Atualizar` tambem passava em BRANCO. Agora REPROVA nos dois lados do caminho (b).
    sem_active = reg.fonte_sem_active_self_no_atualizar(src_janela)
    arc.exigir(sem_active != src_janela,
               "o plantio 'sem _root.activeSelf' nao encontrou `_root.activeSelf` no `Atualizar`: "
               "a checagem nao le o trecho certo")
    for nome, falhas in (("falhas_da_janela", reg.falhas_da_janela(sem_active)),
                         ("falhas_do_fechamento", reg.falhas_do_fechamento(src_tab, sem_active))):
        arc.exigir(len(falhas) >= 1,
                   "`%s` PASSOU em BRANCO com o `Atualizar` SEM exigir `_root.activeSelf`: a "
                   "checagem nao prende a guarda do gatilho" % nome)
        arc.exigir(any("activeSelf" in f or "dono" in f or "DonoVivo" in f for f in falhas),
                   "`%s` reprovou a guarda sem `_root.activeSelf`, mas nao pelo gatilho: %s"
                   % (nome, " | ".join(falhas)))

    # 11) PROVA DE FOGO 5 (bug real de 03/10): SEM o reparent, o tooltip fica atras do fundo — REPROVA.
    raiz = reg.fonte_com_tooltip_raiz(src_janela)
    arc.exigir(raiz != src_janela,
               "o plantio 'tooltip sem reparent' nao encontrou a ancora (o `SetParent`): a checagem "
               "nao le o trecho certo")
    falhas = reg.falhas_da_janela(raiz)
    arc.exigir(len(falhas) >= 1 and any("REPARENTA" in f or "SetParent" in f or "tooltip" in f for f in falhas),
               "as checagens PASSARAM com o `ElevarTooltip` sem reparentar o tooltip (ele ficaria atras "
               "do fundo, ilegivel): %s" % " | ".join(falhas))

    # 12) PROVA DE FOGO 6: o FUNDO deixa de consumir o clique — a MOLDURA mantem `raycastTarget =
    #     true`, que era justamente o que enganava a checagem antiga por texto solto. A checagem
    #     nova amarra a Image DO FUNDO (`RstvWindowBackdrop`) e REPROVA.
    sem_fundo = reg.fonte_com_fundo_sem_raycast(src_janela)
    arc.exigir(sem_fundo != src_janela,
               "o plantio 'fundo sem raycast' nao encontrou a Image do FUNDO (`RstvWindowBackdrop`): "
               "a checagem nao le o trecho certo")
    arc.exigir("raycastTarget = true" in sem_fundo,
               "a isca 'fundo sem raycast' perdeu tambem a moldura: ela nao reproduz o caso que "
               "enganava a checagem antiga")
    falhas = reg.falhas_da_janela(sem_fundo)
    arc.exigir(len(falhas) >= 1 and any("FUNDO" in f or "RstvWindowBackdrop" in f for f in falhas),
               "as checagens PASSARAM com o FUNDO sem consumir o clique: %s" % " | ".join(falhas))

    # 13) PROVA DE FOGO 7: `ElevarTooltip` sem GUARDAR os valores antigos REPROVA (nao basta o nome).
    sem_guarda = reg.fonte_sem_guardar_tooltip(src_janela)
    arc.exigir(sem_guarda != src_janela,
               "o plantio 'ElevarTooltip sem guardar' nao encontrou as atribuicoes dos valores "
               "antigos (ordem/override): a checagem nao le o trecho certo")
    falhas = reg.falhas_da_janela(sem_guarda)
    arc.exigir(len(falhas) >= 1 and any("guarda" in f or "ElevarTooltip" in f for f in falhas),
               "as checagens PASSARAM com o `ElevarTooltip` sem guardar os valores antigos: %s"
               % " | ".join(falhas))

    # 14) PROVA DE FOGO 8: `RestaurarTooltip` virado no-op REPROVA — a SIMETRIA (guardar -> devolver)
    #     e exigida, nao a mera presenca do nome.
    noop = reg.fonte_com_restaurar_noop(src_janela)
    arc.exigir(noop != src_janela,
               "o plantio 'RestaurarTooltip no-op' nao encontrou as atribuicoes que devolvem os "
               "valores antigos: a checagem nao le o trecho certo")
    falhas = reg.falhas_da_janela(noop)
    arc.exigir(len(falhas) >= 1 and any("RestaurarTooltip" in f or "devolve" in f for f in falhas),
               "as checagens PASSARAM com o `RestaurarTooltip` virado no-op: %s" % " | ".join(falhas))

    # 15) PROVA DE FOGO 9: `Abrir` (o caminho do inventario) SEM chamar `SairDoModoJanela` REPROVA.
    abrir_sem = reg.fonte_sem_sair_do_modo_no_abrir(src_tab)
    arc.exigir(abrir_sem != src_tab,
               "o plantio 'Abrir sem SairDoModoJanela' nao encontrou a chamada: a checagem nao le "
               "o trecho certo")
    falhas = reg.falhas_do_desvio_do_hospedeiro(abrir_sem)
    arc.exigir(len(falhas) >= 1 and any("SairDoModoJanela" in f and "`Abrir`" in f for f in falhas),
               "as checagens PASSARAM com o `Abrir` sem `SairDoModoJanela()`: %s" % " | ".join(falhas))

    # 16) PROVA DE FOGO 10: `SelecionarEMostrar` (clique da aba) sem `SairDoModoJanela` REPROVA.
    sel_sem = reg.fonte_sem_sair_do_modo_no_selecionar(src_tab)
    arc.exigir(sel_sem != src_tab,
               "o plantio 'SelecionarEMostrar sem SairDoModoJanela' nao encontrou a chamada: a "
               "checagem nao le o trecho certo")
    falhas = reg.falhas_do_desvio_do_hospedeiro(sel_sem)
    arc.exigir(len(falhas) >= 1 and any("SairDoModoJanela" in f and "SelecionarEMostrar" in f
                                        for f in falhas),
               "as checagens PASSARAM com o `SelecionarEMostrar` sem `SairDoModoJanela()`: %s"
               % " | ".join(falhas))

    # 17) PROVA DE FOGO 11: `Mostrar` sem `ConstruirPainel()` REPROVA (o painel nunca nasceria).
    mostrar_sem = reg.fonte_sem_construir_no_mostrar(src_tab)
    arc.exigir(mostrar_sem != src_tab,
               "o plantio 'Mostrar sem ConstruirPainel' nao encontrou a guarda `_painel == null` "
               "com a chamada: a checagem nao le o trecho certo")
    falhas = reg.falhas_do_desvio_do_hospedeiro(mostrar_sem)
    arc.exigir(len(falhas) >= 1 and any("Mostrar" in f and "ConstruirPainel" in f for f in falhas),
               "as checagens PASSARAM com o `Mostrar` sem `ConstruirPainel()`: %s" % " | ".join(falhas))

    # 17b) PROVA DE FOGO 11b (o ACHADO da RSTV-21TR): a checagem por TOKEN SOLTO `_painel == null`
    #      era satisfeita pelo SEGUNDO `if (_painel == null) { return; }` do `Mostrar`. Remover SO a
    #      guarda IMEDIATAMENTE antes de `ConstruirPainel()` — deixando a chamada solta e o segundo
    #      `if` intacto — tem de REPROVAR. Os dois tokens continuam no corpo (e e isso que enganava
    #      a checagem antiga), entao so o PAR guarda->chamada pode dar o verde.
    sem_guarda = reg.fonte_com_mostrar_sem_guarda(src_tab)
    arc.exigir(sem_guarda != src_tab,
               "o plantio 'Mostrar sem a guarda antes da chamada' nao encontrou o par "
               "`if (_painel == null) { ConstruirPainel(); }`: a checagem nao le o trecho certo")
    arc.exigir("ConstruirPainel()" in sem_guarda and "_painel == null" in sem_guarda,
               "a isca 'sem a guarda antes da chamada' perdeu a CHAMADA ou o token solto "
               "`_painel == null` (o SEGUNDO `if`): ela nao reproduz mais a lacuna que enganava a "
               "checagem antiga")
    falhas = reg.falhas_do_desvio_do_hospedeiro(sem_guarda)
    arc.exigir(len(falhas) >= 1 and any("Mostrar" in f and "ConstruirPainel" in f for f in falhas),
               "as checagens PASSARAM com o `Mostrar` chamando `ConstruirPainel()` SEM a guarda "
               "imediatamente antes (o token solto do segundo `if` ainda engana — o painel seria "
               "reconstruido a cada Mostrar): %s" % " | ".join(falhas))

    # 18) PROVA DE FOGO 12: `Fechar` SEM disparar o aviso `Fechou` REPROVA — sem ele nenhum caminho
    #     de fechamento largaria o `_modoJanela`.
    sem_aviso = reg.fonte_sem_aviso_no_fechar(src_janela)
    arc.exigir(sem_aviso != src_janela,
               "o plantio 'Fechar sem aviso' nao encontrou o disparo `Fechou()`: a checagem nao le "
               "o trecho certo")
    falhas = reg.falhas_do_fechamento(src_tab, sem_aviso)
    arc.exigir(len(falhas) >= 1 and any("Fechou()" in f for f in falhas),
               "as checagens PASSARAM com o `Fechar` sem disparar `Fechou()`: %s" % " | ".join(falhas))

    # 19) PROVA DE FOGO 13: o botao CLOSE sem chamar `Fechar` REPROVA (o caminho do botao nao passaria
    #     pelo aviso).
    botao_sem = reg.fonte_botao_fechar_sem_fechar(src_janela)
    arc.exigir(botao_sem != src_janela,
               "o plantio 'botao Close sem Fechar' nao encontrou o `AddListener(new UnityAction("
               "Fechar))`: a checagem nao le o trecho certo")
    falhas = reg.falhas_do_fechamento(src_tab, botao_sem)
    arc.exigir(len(falhas) >= 1 and any("botao Close" in f for f in falhas),
               "as checagens PASSARAM com o botao Close sem chamar `Fechar`: %s" % " | ".join(falhas))

    # 20) PROVA DE FOGO 14: `AbrirJanela` SEM se inscrever no aviso REPROVA (o hospedeiro nunca seria
    #     avisado do fechamento).
    sem_inscricao = reg.fonte_sem_inscrever_fechou(src_tab)
    arc.exigir(sem_inscricao != src_tab,
               "o plantio 'AbrirJanela sem inscricao' nao encontrou `SkillTreesWindow.Fechou = "
               "AoFecharJanela`: a checagem nao le o trecho certo")
    falhas = reg.falhas_do_fechamento(sem_inscricao, src_janela)
    arc.exigir(len(falhas) >= 1 and any("INSCREVE" in f or "inscreve" in f for f in falhas),
               "as checagens PASSARAM com o `AbrirJanela` sem se inscrever no aviso: %s"
               % " | ".join(falhas))

    # 21) PROVA DE FOGO 15: `AoFecharJanela` SEM zerar o `_modoJanela` REPROVA — e' o defeito do
    #     RSTV-21A (o flag ficava pendurado depois do fechamento).
    sem_reset = reg.fonte_ao_fechar_sem_reset(src_tab)
    arc.exigir(sem_reset != src_tab,
               "o plantio 'AoFecharJanela sem reset' nao encontrou `_modoJanela = false`: a "
               "checagem nao le o trecho certo")
    falhas = reg.falhas_do_fechamento(sem_reset, src_janela)
    arc.exigir(len(falhas) >= 1 and any("zera" in f or "PENDURADO" in f for f in falhas),
               "as checagens PASSARAM com o `AoFecharJanela` sem zerar o `_modoJanela`: %s"
               % " | ".join(falhas))

    print("RSTV-21: o clique do modal abre a JANELA propria (Canvas overlay escalado como o jogo) "
          "com todas as arvores, sem o inventario; a janela segue o dono, o tooltip sobe acima dela "
          "E volta ao lugar, os pontos de entrada saem do modo janela, o `Mostrar` constroi o painel "
          "e nenhum arquivo tem caminho de escrita — os defeitos plantados reprovam")


if __name__ == "__main__":
    arc.main(META, corpo)
