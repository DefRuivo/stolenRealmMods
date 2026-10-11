#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-30 (parte 1 de 2): O BOTAO MUDOU PARA A BARRA DE BAIXO, E NADA DE POSICAO CHUTADA.

O PEDIDO DO DONO (06/10, em jogo)
---------------------------------
"Faca com que ele, ao inves de ser renderizado ao lado do botao de marcar o hex, seja renderizado na
barra de baixo na esquerda ao lado dos botoes de inventario e skills e entre o botao de rotacionar a
barra de skills."

Este teste confere o CONSERTO no fonte VIVO e o MODELO PURO da conta de posicao:

  1. o clone tem de sair da linha do `Ping Button` e passar a ser filho do container NATIVO dos
     botoes de inventario e de skills (`ui.skillsBtn.transform.parent` — medido em runtime, nao
     digitado), com `LayoutElement.ignoreLayout = true` (o `HorizontalLayoutGroup` do container,
     medido LIGADO no prefab, nao reflui e nenhum botao nativo se move);
  2. a posicao tem de ser MEDIDA (`GetWorldCorners` + `InverseTransformPoint`) e o corpo de
     `ColocarNaLinha` NAO pode ter literal de posicao (`125.59f` seria posicao chutada). TODA medicao
     do metodo tem de sair do MESMO referencial — o espaco LOCAL do container, cuja origem e' o
     PIVOR (RSTV-30F: medir o vizinho da direita no espaco do PAI e comparar com a borda ESQUERDA
     empurrava o clone para depois do rotador);
  3. a conta de posicao, transcrita em `regras_rstv30.posicao`, tem de manter o clone DENTRO do vao
     livre: sem invadir o ultimo botao nativo nem o vizinho da direita (`Skillbar Index Controls`, o
     controle que rotaciona a barra de skills), em varios cenarios — inclusive com os numeros LIDOS
     do prefab do HUD em `regras_rstv30.PREFAB`, todos no MESMO referencial (a fixture ainda carrega
     os numeros crus e o teste CONFERE a travessia entre os dois);
  3b. a ISCA DO REFERENCIAL: alimentado com o par misturado que o codigo usava antes do conserto
     (`regras_rstv30.par_de_referenciais_misturados`), o modelo tem de REPROVAR — o clone cai depois
     do rotador. Sem isso, a checagem de referencial unico poderia estar passando por acidente;
  4. a FAMILIA de guardas: as que sairam nao podem voltar e cada uma que ficou tem de trazer, no
     fonte, o marcador e a linha `Justificativa:` (guarda sem justificativa e' defeito);
  5. a ISCA EMBUTIDA: os tres defeitos plantados em memoria (a visibilidade presa ao portao, a
     guarda do piscar de volta e a justificativa apagada) tem de REPROVAR pelas checagens certas.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv30.py`, lidas do fonte VIVO do mod; as medidas do prefab
estao em `regras_rstv30.PREFAB`, com a procedencia item a item em
`docs/RSTV-30-botao-na-barra-de-baixo.md`. A isca externa e'
`tools/testes/contra-prova/cp_rstv30_visibilidade_por_estado.py`. O que NAO se prova aqui (e so o dono
confirma, em tela): a posicao final AOS OLHOS, com a barra de baixo real — a conferencia visual pedida
pelo DoD.
"""
import regras_rstv30 as reg

import arcabouco as arc

META = {
    "nome": "rstv30-barra-de-baixo",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-30: o botao da run mora no container NATIVO da barra de baixo "
                  "(ignoreLayout, sem empurrar ninguem), a posicao e' MEDIDA (sem literal), a conta "
                  "nao invade ninguem e as guardas que ficaram tem justificativa"),
}


def corpo():
    arquivos = reg.fontes()
    run = arquivos.get(reg.ARQUIVO_RUN, "")
    arc.exigir(len(run) > 3000, "RunButton.cs veio vazio/curto: a leitura mudou de lugar?")

    # 1) O FONTE: o conserto esta de pe (casa nova, ignoreLayout, medicao, guardas, justificativas).
    falhas = reg.falhas_da_fonte(arquivos)
    arc.exigir(not falhas, "o conserto da RSTV-30 regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) A CONTA DE POSICAO (modelo puro) — com os numeros LIDOS do prefab, TODOS no MESMO
    #    referencial (o espaco LOCAL do container, origem no PIVOR — ver regras_rstv30.PREFAB).
    prefab = reg.PREFAB

    # 2a) CONTROLE DA PROPRIA FIXTURA: os numeros crus do prefab tem de FECHAR entre si na travessia
    #     borda-esquerda -> espaco local (a MESMA conversao que a RSTV-30F acrescentou ao codigo).
    #     Isto amarra o referencial dos dois lados: se alguem "re-fixar" o vao mexendo so' num numero,
    #     a conta aqui denuncia.
    arc.exigir(abs(reg.converte_para_o_local(prefab["limite_medido_na_borda_esquerda"],
                                             prefab["canto_esquerdo"]) - prefab["limite_do_vizinho"]) < 1e-9,
               "a fixture do prefab nao fecha: o limite do rotador, convertido para o espaco local "
               "(134.3 + rect.xMin), deveria dar %.2f e deu %.2f"
               % (prefab["limite_do_vizinho"],
                  reg.converte_para_o_local(prefab["limite_medido_na_borda_esquerda"],
                                            prefab["canto_esquerdo"])))
    arc.exigir(abs(prefab["canto_esquerdo"] + (prefab["largura_do_container"] / 2.0)) < 1e-9,
               "a fixture do prefab nao fecha: `rect.xMin` (%.2f) deveria ser -largura/2 (%.2f)"
               % (prefab["canto_esquerdo"], -prefab["largura_do_container"] / 2.0))
    arc.exigir(abs((prefab["fim_dos_nativos"] - prefab["limite_do_vizinho"]) * -1.0
                   - prefab["vao_do_prefab"]) < 1e-9,
               "a fixture do prefab nao fecha: o vao (limite - fim) deveria ser %.2f e deu %.2f"
               % (prefab["vao_do_prefab"], prefab["limite_do_vizinho"] - prefab["fim_dos_nativos"]))

    largura, centro = reg.posicao(prefab["fim_dos_nativos"], prefab["limite_do_vizinho"],
                                  prefab["largura_nativa"])
    esq, direita = reg.bordas(centro, largura)

    # A area dos NATIVOS, na MESMA referencia: do `rect.xMin` do container ate' a borda direita deles.
    esq_nativos = prefab["canto_esquerdo"]
    arc.exigir(esq >= prefab["fim_dos_nativos"] - 1e-6,
               "com os numeros do prefab o clone invade os botoes NATIVOS (borda esquerda %.2f < "
               "fim dos nativos %.2f)" % (esq, prefab["fim_dos_nativos"]))
    arc.exigir(direita <= prefab["limite_do_vizinho"] + 1e-6,
               "com os numeros do prefab o clone invade o VIZINHO (borda direita %.2f > limite "
               "%.2f) — o pedido era 'sem sobrepor os botoes nativos'" % (direita, prefab["limite_do_vizinho"]))
    arc.exigir(largura <= prefab["largura_nativa"] + 1e-6,
               "o clone ficou maior que um botao nativo (%.2f > %.2f)" % (largura, prefab["largura_nativa"]))
    arc.exigir(largura > 0.0, "o clone ficou com largura nao positiva (%.2f)" % largura)

    # 2b) A EXPECTATIVA DO DOC (§3): o clone tem de ficar MENOR que um botao nativo porque o vao real
    #     (23.0 px) menos as duas margens (2x2.0) da' 19.0 px — o numero prometido ao dono.
    esperada = prefab["vao_do_prefab"] - (2.0 * reg.MARGEM)
    arc.exigir(abs(largura - esperada) < 1e-6,
               "a largura do clone (%.2f) nao e' a prometida pelo doc (vao %.2f - 2x margem %.2f = "
               "%.2f)" % (largura, prefab["vao_do_prefab"], reg.MARGEM, esperada))
    arc.exigir(esq >= esq_nativos - 1e-6,
               "o clone saiu do container pela esquerda (borda esquerda %.2f < %.2f)"
               % (esq, esq_nativos))

    # 3) A CONTA EM VARIOS CENARIOS: com vao livre, o clone NAO pode invadir nativo nem vizinho.
    #    (Todos os numeros no mesmo referencial do prefab convertido.)
    cenarios = (
        ("vao folgado (sobra espaco)", prefab["fim_dos_nativos"], prefab["limite_do_vizinho"] + 30.0,
         prefab["largura_nativa"]),
        ("vao justo (o medido no prefab)", prefab["fim_dos_nativos"], prefab["limite_do_vizinho"],
         prefab["largura_nativa"]),
        ("vao apertado", prefab["fim_dos_nativos"], prefab["fim_dos_nativos"] + 15.0, 27.02),
        ("botao nativo mais largo", prefab["fim_dos_nativos"], prefab["limite_do_vizinho"], 40.0),
    )
    for nome, fim, limite, largura_nativa in cenarios:
        l, c = reg.posicao(fim, limite, largura_nativa)
        e, d = reg.bordas(c, l)
        arc.exigir(not reg.invade(e, d, esq_nativos, fim),
                   "%s: o clone invadiu a area dos botoes NATIVOS (clone %.2f..%.2f x nativos "
                   "%.2f..%.2f)" % (nome, e, d, esq_nativos, fim))
        arc.exigir(not reg.invade(e, d, limite, limite + 100.0),
                   "%s: o clone invadiu o VIZINHO da direita (clone %.2f..%.2f x vizinho a partir "
                   "de %.2f)" % (nome, e, d, limite))
        arc.exigir(l <= max(largura_nativa, 1.0) + 1e-6,
                   "%s: o clone ficou maior que o molde (%.2f > %.2f)" % (nome, l, largura_nativa))

    # 3b) O CASO DEGENERADO (a linha nao tem vao nenhum: o vizinho comeca ANTES do fim dos nativos).
    #     Nao se inventa espaco: o clone fica logo depois dos nativos (NUNCA por cima deles) e o
    #     AVISO vai para o log — o codigo tem de ter esse caminho (`largura < LarguraMinima`).
    l, c = reg.posicao(prefab["fim_dos_nativos"], prefab["fim_dos_nativos"] - 3.3, prefab["largura_nativa"])
    e, d = reg.bordas(c, l)
    arc.exigir(not reg.invade(e, d, esq_nativos, prefab["fim_dos_nativos"]),
               "no caso degenerado o clone INVADIU os botoes NATIVOS (clone %.2f..%.2f x nativos "
               "%.2f..%.2f) — sobrepor botao nativo nunca e' aceitavel"
               % (e, d, esq_nativos, prefab["fim_dos_nativos"]))
    arc.exigir("LarguraMinima" in run,
               "o codigo nao tem o AVISO do caso degenerado (`LarguraMinima` no log) — uma linha "
               "sem vao seria tratada em silencio")

    # 3c) A ISCA DO REFERENCIAL (RSTV-30F) — o VERMELHO que prova a checagem 3b de `falhas_da_fonte`.
    #     Com o par MISTURADO que o codigo alimentava (fim no espaco local/pivor x limite medido a
    #     partir da BORDA ESQUERDA), a MESMA conta joga o clone para DEPOIS do rotador — fora da
    #     linha, onde o dono NAO pediu. O modelo tem de REPROVAR esse par; se ele passar, a isca nao
    #     esta medindo o defeito que ela diz medir.
    fim_misto, limite_misto, larg_mista = reg.par_de_referenciais_misturados(prefab)
    l_m, c_m = reg.posicao(fim_misto, limite_misto, larg_mista)
    e_m, d_m = reg.bordas(c_m, l_m)
    arc.exigir(reg.invade(e_m, d_m, prefab["limite_do_vizinho"], prefab["limite_do_vizinho"] + 100.0),
               "a isca do referencial NAO reprovou: com o par misturado (fim %.2f local x limite "
               "%.2f a partir da borda esquerda) o clone deveria cair DEPOIS do rotador (%.2f) e caiu "
               "em %.2f..%.2f — a checagem de referencial unico nao pega o defeito RSTV-30F"
               % (fim_misto, limite_misto, prefab["limite_do_vizinho"], e_m, d_m))
    arc.exigir(e_m > prefab["fim_dos_nativos"] and d_m > prefab["largura_do_container"],
               "a isca do referencial nao ficou fora da linha na borda direita (clone %.2f..%.2f x "
               "container ate' %.2f)" % (e_m, d_m, prefab["largura_do_container"]))

    # 4) A ISCA EMBUTIDA — cada defeito plantado em MEMORIA tem de reprovar pela razao certa.
    com_visibilidade = reg.fonte_com_visibilidade_por_estado(run)
    arc.exigir(com_visibilidade != run,
               "o plantio da 'visibilidade presa ao portao' nao encontrou o trecho do Mirror: a "
               "checagem nao esta lendo o conserto")
    falhas_visibilidade = reg.falhas_da_fonte(dict(arquivos, **{reg.ARQUIVO_RUN: com_visibilidade}))
    arc.exigir(any("Mirror chama `RunTargets.GateOk`" in f for f in falhas_visibilidade),
               "as checagens NAO pegaram o portao decidindo a presenca do botao: %s"
               % " | ".join(falhas_visibilidade))

    targets = arquivos.get(reg.ARQUIVO_TARGETS, "")
    com_guarda = reg.fonte_com_guarda_de_volta(targets)
    arc.exigir(com_guarda != targets,
               "o plantio da guarda do piscar nao encontrou a ancora no RunTargets.cs")
    falhas_guarda = reg.falhas_da_fonte(dict(arquivos, **{reg.ARQUIVO_TARGETS: com_guarda}))
    arc.exigir(any("AnyActingCharactersInBattle" in f for f in falhas_guarda),
               "as checagens NAO pegaram a guarda do piscar de volta: %s" % " | ".join(falhas_guarda))

    sem_justificativa = reg.fonte_sem_justificativa(targets)
    arc.exigir(sem_justificativa != targets,
               "o plantio da 'justificativa apagada' nao encontrou o comentario da GUARDA 3")
    falhas_just = reg.falhas_da_fonte(dict(arquivos, **{reg.ARQUIVO_TARGETS: sem_justificativa}))
    arc.exigir(any("Justificativa" in f for f in falhas_just),
               "as checagens NAO pegaram a guarda sem justificativa: %s" % " | ".join(falhas_just))

    print("casa nova conferida no fonte; conta de posicao sem invasao em %d cenario(s) (prefab: "
          "largura %.1f px no vao de %.1f..%.1f); 3 defeitos plantados reprovam"
          % (len(cenarios), largura, prefab["fim_dos_nativos"], prefab["limite_do_vizinho"]))


if __name__ == "__main__":
    arc.main(META, corpo)
