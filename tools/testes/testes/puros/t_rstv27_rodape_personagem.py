#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O RODAPE da tooltip read-only (mana/cooldown/alcance/duracao) resolve para o personagem do MODAL — RSTV-27.

O QUE ISTO TRAVA
----------------
Na janela read-only do modal "Remove Skill Trees" (tela Party Select), o CORPO da tooltip ja' resolve o
'*N'/'[N]' contra o personagem do modal (RSTV-26), mas o RODAPE nao: o `ShowSkillTooltip` monta
`tooltipCharacter = TooltipCharacter` — propriedade GET-ONLY = `GameLogic.CurrentlySelectedCharacter`,
NULL na Party Select — e le' mana/cooldown/alcance/blast/duracao desse local. Com ele null o rodape cai
nos overloads SEM personagem (valores de BASE) enquanto o corpo mostra os numeros do personagem.

AS REGRAS (viram checagem)
--------------------------
1. o hover ARMA o alvo do modal (`ReadOnlySession.Target`) SO' em volta da montagem da tooltip
   (`try`/`finally` com `ComAlvo`/`SemAlvo`);
2. o gancho e' um POSTFIX de `Tooltip.get_TooltipCharacter` que so' PREENCHE o null, na ORDEM: valor do
   jogo vence -> le' o alvo armado -> fallback se nao houver alvo -> preenche;
3. o `Postfix` e' fail-safe (try/catch).

O QUE O TESTE PRENDE E' A SAIDA, NAO A CHAMADA
----------------------------------------------
Os modelos puros (`personagem_do_rodape` + `valor_do_rodape`) devolvem o VALOR que o rodape mostra: com
o conserto, na Party Select (singleton null) o rodape vale os numeros DO ALVO DO MODAL; com o defeito
(sem o armado, sem o preenchimento, sobrescrevendo o jogo ou sem fallback) o valor cai na BASE — e o
teste REPROVA. A prova de fogo e' EMBUTIDA (cada defeito plantado em memoria tem de reprovar pelo
motivo certo), como no BT-10, no MAN-2 e na RSTV-8.

DE ONDE VEM O ESPERADO
----------------------
Regras em `tools/testes/regras_rstv27.py`; fonte lido AO VIVO do mod (nunca copia). A tabela do caso
(`CASO`) e' sintetica e declara a procedencia: a MECANICA lida do decompilado da DLL do jogo mostra
que os dois caminhos do motor divergem (`GetManaCost(Character)` x `GetManaCost()`, etc.). O numero
REAL na tela sai em jogo — e' o gate do DoD, nao deste teste.
"""
import regras_rstv27 as reg

import arcabouco as arc

META = {
    "nome": "rstv27-rodape-personagem",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-27: o rodape da tooltip read-only (mana/cooldown/alcance/duracao) resolve para o "
                  "personagem do MODAL — o hover arma `ReadOnlySession.Target` em volta da montagem e o "
                  "postfix de `Tooltip.get_TooltipCharacter` so' PREENCHE o null (o valor do jogo vence; "
                  "sem alvo, fallback ao comportamento antigo); a SAIDA e' o valor do alvo do modal, "
                  "nunca a base do overload sem personagem"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    src_patches = reg.fonte(reg.caminho_patches())
    arc.exigir(len(src_tab) > 1000 and len(src_patches) > 1000,
               "o fonte do mod veio vazio/curto: a leitura mudou de lugar?")

    # 1) A CORRECAO: o hover arma o alvo do modal em volta da chamada e o gancho preenche o null.
    falhas_armado = reg.falhas_do_armado(src_tab)
    arc.exigir(not falhas_armado,
               "o hover nao passa o alvo do modal ao rodape em %d ponto(s): %s"
               % (len(falhas_armado), " | ".join(falhas_armado)))

    falhas_gancho = reg.falhas_do_gancho(src_patches)
    arc.exigir(not falhas_gancho,
               "o gancho do getter regrediu em %d ponto(s): %s"
               % (len(falhas_gancho), " | ".join(falhas_gancho)))

    # 2) O MODELO PURO — a SAIDA. Na Party Select o `TooltipCharacter` do jogo e' null.
    arc.igual(reg.personagem_do_rodape(None, "Raven"), "Raven",
              "com o alvo do modal armado e o jogo devolvendo null, o rodape tem de consultar o ALVO "
              "DO MODAL")
    arc.igual(reg.personagem_do_rodape("Outro", "Raven"), "Outro",
              "o valor do JOGO tem de vencer: o gancho nao pode sobrescrever um personagem que o jogo "
              "ja' resolveu (o inventario se comporta como sempre)")
    arc.igual(reg.personagem_do_rodape(None, None), None,
              "sem alvo armado o rodape tem de continuar como o jogo faz (FALLBACK)")

    valores_alvo = reg.valor_do_rodape(reg.personagem_do_rodape(None, "Raven"))
    valores_base = reg.valor_do_rodape(reg.personagem_do_rodape(None, None))
    arc.exigir(valores_alvo != valores_base,
               "o CASO nao separa o valor do alvo do valor de BASE (%r x %r): a checagem nao morderia "
               "nada" % (valores_alvo, valores_base))
    arc.igual(valores_alvo, reg.valor_do_rodape("Raven"),
              "o rodape tem de mostrar o numero DO PERSONAGEM DO MODAL, campo a campo")
    arc.igual(valores_base, reg.valor_do_rodape(None),
              "sem o conserto o rodape mostra o valor de BASE (o defeito) — e isso tem de ser DIFERENTE "
              "do valor do alvo")

    # 3) A ORDEM do gancho: sem a guarda do valor do jogo, o inventario regride (o modelo tambem).
    arc.igual(reg.personagem_do_rodape("Outro", None), "Outro",
              "fora da nossa tooltip (sem alvo armado) o personagem do jogo continua valendo")

    # 4) PROVA DE FOGO EMBUTIDA: cada defeito plantado em memoria tem de REPROVAR pelo motivo certo.
    defeito_hover = reg.hover_sem_armado(src_tab)
    arc.exigir(defeito_hover != src_tab,
               "o plantio 'hover sem o armado' nao encontrou a ancora (`ComAlvo(alvo)`): a checagem nao "
               "le o trecho certo")
    f = reg.falhas_do_armado(defeito_hover)
    arc.exigir(len(f) >= 1 and any("ComAlvo" in x or "armado" in x for x in f),
               "as checagens PASSARAM (ou reprovaram por outro motivo) com o hover SEM armar o alvo: %s"
               % " | ".join(f))

    for nome, plantio, marca in (
            ("gancho sem preenchimento", reg.gancho_sem_preenchimento, "PREENCHE"),
            ("gancho que sobrescreve o jogo", reg.gancho_sobrescreve, "valor do jogo"),
            ("gancho sem fallback", reg.gancho_sem_fallback, "FALLBACK")):
        defeito = plantio(src_patches)
        arc.exigir(defeito != src_patches,
                   "o plantio '%s' nao mudou o fonte: a ancora sumiu do gancho?" % nome)
        f = reg.falhas_do_gancho(defeito)
        arc.exigir(len(f) >= 1 and any(marca in x for x in f),
                   "o defeito '%s' NAO foi pego pela marca %r (falhas=%s)"
                   % (nome, marca, " | ".join(f)))

    print("RSTV-27: o rodape da tooltip read-only recebe o personagem do MODAL — o hover arma "
          "`ReadOnlySession.Target` em `try/finally` em volta do `ShowSkillTooltip` e o postfix de "
          "`Tooltip.get_TooltipCharacter` so' PREENCHE o null (o valor do jogo vence; sem alvo, o "
          "comportamento do jogo fica intacto). A SAIDA presa e' o VALOR: na Party Select o rodape vale "
          "o alvo do modal, nao a base do overload sem personagem; os 4 defeitos plantados REPROVAM.")


if __name__ == "__main__":
    arc.main(META, corpo)
