#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A ABA "All Skill Trees" NO INVENTARIO (todas as classes menos Bard) E A APOSENTADORIA DA JANELA (RSTV-16).

O QUE ISTO TRAVA
----------------
Decisao do dono (02/10): parar de empilhar a janela read-only SEPARADA (RSTV-2/5/15) e colocar uma ABA
na barra do inventario (`CharacterMenusManager` / `MenuTabManager`), com TODAS as arvores menos a do
Bard (nao esta no jogo). O atalho (F10 / botao do HUD / botao do level-up) passa a abrir o inventario
NESSa aba.

AS 8 PREMISSAS CORRIGIDAS PELOS REVISORES (todas viram checagem aqui)
----------------------------------------------------------------------
1. o read-only NAO e automatico (a `SkillTreeManager` e pre-carregada -> `Instance` nunca e nulo): quem
   barra e `ReadOnlySession.Active` + `SkillTreesTab.Aberto` no `SkillTreeItemTogglePatch`;
2. a fonte do conteudo NAO e `SkillsByTreeDict` (omite `DontIncludeInTree`/DLC): e `Game.Instance.Skills`
   com o predicado de `RefreshAvailableSkillTrees`;
3. NAO se reusa `PopulateTree`/`ProcessDependencyLines` (dependem do Instance): layout reimplementado;
4. a lista de classes espelha `RefreshAvailableSkillTrees` (Bard fora, Basic/Innate fora, DLC);
5. a `Underline` (largura fixa ~74.5) e ajustada ao rotulo e restaurada;
6. o rotulo esta numa constante so (fallback curto documentado);
7. a fileira de classes reusa o `SkillTreeTab` nativo (icone+nome);
8. a aba ENTRA no array publico `MenuTabs`; o handler usa `SelectButton`; o inventario abre PRIMEIRO.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv16.py`; os fontes sao lidos AO VIVO do mod (nunca copias).
Os modelos puros `classes_da_aba` (o filtro) e `conteudo_apos_clique` (a 4a aba troca o conteudo com
`SelectButtonAndInvoke`, e so realca com `SelectButton`) sao a transcricao do jogo; os plantios
(`fonte_com_bard_incluido`, `fonte_com_aba_fora_do_array`, `fonte_com_predicado_fraco`) provam que as
checagens pegam o defeito. O que NAO se prova aqui (e so o dono confirma, em tela): a aba APARECER, a
fileira de classes e as arvores desenharem com a metragem certa.
"""
import regras_rstv16 as reg

import arcabouco as arc

META = {
    "nome": "rstv16-aba-arvores",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-16: a aba 'All Skill Trees' entra no array publico MenuTabs, o conteudo vem de "
                  "Game.Instance.Skills (todas as classes menos Bard/Basic/Innate, com DLC), o read-only "
                  "vem da sessao e a janela separada (ZOrder/LifecycleBlock/AjustarZOrder) foi aposentada; "
                  "os defeitos 'Bard incluido', 'aba fora do array' e 'predicado fraco' reprovam"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_aba())
    src_run = reg.fonte(reg.caminho_run())
    src_atalho = reg.fonte(reg.caminho_atalho())
    src_patches = reg.fonte(reg.caminho_patches())
    src_plugin = reg.fonte(reg.caminho_plugin())
    src_readonly = reg.fonte(reg.caminho_readonly())

    for nome, src in (("SkillTreesTab.cs", src_tab), ("RunButton.cs", src_run),
                      ("SkillTreeShortcut.cs", src_atalho), ("Patches.cs", src_patches),
                      ("Plugin.cs", src_plugin), ("SkillTreeReadOnly.cs", src_readonly)):
        arc.exigir(len(src) > 1000, "o fonte %s veio vazio/curto: a leitura mudou de lugar?" % nome)

    # 1) O DESENHO DA ABA: clone, idempotencia por nome, array publico, onClick limpo, conteudo certo.
    falhas = reg.falhas_da_aba(src_tab)
    arc.exigir(not falhas, "a aba regrediu em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # 2) O READ-ONLY PELA SESSAO e o atalho abrindo a aba.
    falhas_ro = reg.falhas_do_readonly_e_atalho(src_tab, src_run, src_atalho, src_patches)
    arc.exigir(not falhas_ro, "o read-only/atalho regrediu em %d ponto(s): %s"
               % (len(falhas_ro), " | ".join(falhas_ro)))

    # 3) A APOSENTADORIA: a janela separada saiu e os alicerces ficaram.
    falhas_ap = reg.falhas_da_aposentadoria(src_readonly, src_plugin, src_run, src_patches)
    arc.exigir(not falhas_ap, "a aposentadoria regrediu em %d ponto(s): %s"
               % (len(falhas_ap), " | ".join(falhas_ap)))

    # 4) O FILTRO DAS CLASSES: 11 (Bard/Basic/Innate fora), e o defeito do Bard e' diferente.
    classes = reg.classes_da_aba(reg.TIPOS_ASSET)
    arc.exigir("Bard" not in classes, "o filtro deixou o Bard entrar: %s" % classes)
    arc.exigir("Basic" not in classes and "Innate" not in classes,
               "o filtro deixou Basic/Innate entrarem (nao sao arvores): %s" % classes)
    arc.igual(len(classes), 11, "o numero de classes da aba (14 no asset - Bard - Basic - Innate)")
    arc.exigir(classes != reg.classes_com_bard(reg.TIPOS_ASSET),
               "o modelo nao distingue a regra nova da que inclui o Bard — nao prova nada")

    # 4b) DLC e skill visivel CORTAM a classe (o Chaos condicional do jogo).
    sem_dlc = reg.classes_da_aba(reg.TIPOS_ASSET, dlc_ok={"Chaos": False})
    arc.exigir("Chaos" not in sem_dlc, "classe sem DLC continuou na lista: %s" % sem_dlc)
    sem_skill = reg.classes_da_aba(reg.TIPOS_ASSET, com_skill={"Nature": False})
    arc.exigir("Nature" not in sem_skill, "classe sem skill visivel continuou na lista: %s" % sem_skill)

    # 5) A 4a ABA: `SelectButtonAndInvoke` troca o CONTEUDO; `SelectButton` so realca (o ponto 8).
    arc.igual(len(reg.ABAS), 4, "a barra tem de ter a 4a aba")
    arc.exigir(reg.aba_no_array(reg.ABAS, 3), "a 4a aba nao esta no array publico MenuTabs")
    arc.igual(reg.conteudo_apos_clique(3, True), "AllSkillTrees",
              "o conteudo ao clicar na 4a aba COM SelectButtonAndInvoke")
    arc.igual(reg.conteudo_apos_clique(3, False), "Character",
              "o conteudo ao clicar na 4a aba COM SelectButton (so realca) — o defeito")
    arc.exigir(reg.conteudo_apos_clique(3, True) != reg.conteudo_apos_clique(3, False),
               "os dois caminhos dao o mesmo conteudo: o modelo nao prove a diferenca do ponto 8")

    # 6) PROVA DE FOGO NO FONTE 1: com o FILTRO do Bard removido, as checagens reprovam pelo motivo certo.
    com_bard = reg.fonte_com_bard_incluido(src_tab)
    arc.exigir(com_bard != src_tab,
               "o plantio do defeito 'Bard' nao encontrou a ancora (`if (tipo == SkillType.Bard)`): a "
               "checagem nao le o trecho certo")
    falhas_bard = reg.falhas_da_aba(com_bard)
    arc.exigir(len(falhas_bard) >= 1 and any("Bard" in f for f in falhas_bard),
               "as checagens PASSARAM (ou reprovaram por outro motivo) com o Bard incluido: %s"
               % " | ".join(falhas_bard))

    # 7) PROVA DE FOGO NO FONTE 2: com a aba FORA do array publico (o "Tabbing broke"), reprova.
    fora = reg.fonte_com_aba_fora_do_array(src_tab)
    arc.exigir(fora != src_tab,
               "o plantio do defeito 'fora do array' nao encontrou a ancora (`MenuTabs = novo`): a "
               "checagem nao le o trecho certo")
    falhas_fora = reg.falhas_da_aba(fora)
    arc.exigir(len(falhas_fora) >= 1 and any("MenuTabs" in f or "array" in f for f in falhas_fora),
               "as checagens PASSARAM com a aba fora do MenuTabs: %s" % " | ".join(falhas_fora))

    # 8) PROVA DE FOGO NO FONTE 3: com o predicado fraco (o defeito do SkillsByTreeDict), reprova.
    fraco = reg.fonte_com_predicado_fraco(src_tab)
    arc.exigir(fraco != src_tab,
               "o plantio do defeito 'predicado fraco' nao encontrou a ancora do predicado: a "
               "checagem nao le o trecho certo")
    falhas_fraco = reg.falhas_da_aba(fraco)
    arc.exigir(len(falhas_fraco) >= 1 and any("DontIncludeInTree" in f or "Disabled" in f for f in falhas_fraco),
               "as checagens PASSARAM com o predicado fraco: %s" % " | ".join(falhas_fraco))

    print("RSTV-16: a aba entra no MenuTabs e no read-only pela sessao, o conteudo vem de "
          "Game.Instance.Skills (Bard/Basic/Innate fora; DLC/FullRelease respeitados), a janela "
          "separada (ZOrder/LifecycleBlock/AjustarZOrder) foi aposentada; os defeitos plantados "
          "reprovam")


if __name__ == "__main__":
    arc.main(META, corpo)
