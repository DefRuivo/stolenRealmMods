#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-29: a superficie do botao 'Skills' da tela Select Party NAO existe mais em lugar nenhum.

O QUE ISTO TRAVA (uma AUSENCIA)
-------------------------------
Em 06/10 o dono decidiu, em jogo, REMOVER o botao 'Skills' da tela Select Party (o botao do modal
'Remove Skill Trees', RSTV-20, e' o que fica). A decisao cobriu tudo o que existia SO' para servir
aquela superficie: a classe `SelectPartyButton`, os DOIS ganchos da tela (`OpenCharacterChoiceManager`
e o `OpenWindow` da RSTV-28, que perdeu o sentido), a descricao do config `AtivarBotao` e a linha de
boot que a anunciava. Este teste prende a AUSENCIA: apagar a feature e deixar os anuncios de pe' e'
uma remocao pela metade, e um log de "botao injetado" mantem viva uma tela que nao tem botao.

AS REGRAS (viram checagem)
--------------------------
1. `SelectPartyButton.cs` NAO existe;
2. nenhum `.cs` cita `SelectPartyButton`/`RstvSkillTreeButton`/`CharacterChoiceOpenPatch`/
   `CharacterChoiceOpenWindowPatch` no CODIGO EFETIVO (comentario historico nao conta);
3. `Patches.cs` nao tem gancho em `CharacterChoiceManager.OpenCharacterChoiceManager` nem `.OpenWindow`
   — em NENHUMA forma (nameof, string ou nu): vale a propriedade "nenhum patch aponta para a tela";
4. `Plugin.cs` nao tem o texto antigo do config nem a linha de boot da tela.

CONTROLE POSITIVO: o botao do MODAL (`RemovalWindowSkillsButton.cs`) tem de continuar — a remocao
cobrir o que FICA seria ir longe demais.

A PROVA DE FOGO e' EMBUTIDA: cada pedaco da superficie e' plantado de volta numa copia EM MEMORIA e a
MESMA checagem tem de REPROVAR pela marca daquele pedaco. A bancada FISICA (arquivos numa copia FORA
do repo, `vermelho -> verde`) e' `tools/testes/prova-sandbox-rstv28.py`.

DE ONDE VEM O ESPERADO
----------------------
Regras em `tools/testes/regras_rstv28.py`; os fontes sao lidos AO VIVO do mod (nunca copia). O que
NAO se prova aqui: nao executa o C# do mod nem mede a tela — o dono confirma que o botao nao aparece
mais na tela de party.
"""
import regras_rstv28 as reg

import arcabouco as arc

META = {
    "nome": "rstv28-tela-select-party",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-29: a superficie do botao 'Skills' da tela Select Party NAO existe mais — o "
                  "arquivo/classe, os dois ganchos da tela (incl. o `OpenWindow` da RSTV-28), o texto "
                  "do config e a linha de boot sumiram; o botao do modal continua; cada pedaco "
                  "plantado de volta REPROVA pela marca certa"),
}


def corpo():
    arquivos = reg.le_arquivos_cs()
    arc.exigir(len(arquivos) >= 5,
               "leu poucos .cs do mod (%d): a leitura mudou de lugar?" % len(arquivos))

    # 1) A AUSENCIA — nenhum vestigio da superficie.
    falhas = reg.falhas_da_ausencia(arquivos)
    arc.exigir(not falhas,
               "a superficie Select Party ainda existe em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) CONTROLE POSITIVO: o que FICA tem de continuar (o botao do modal, RSTV-20).
    arc.exigir("RemovalWindowSkillsButton.cs" in arquivos,
               "o botao do modal 'Remove Skill Trees' sumiu junto — a remocao foi longe demais")
    arc.exigir(reg.ARQUIVO_REMOVIDO not in arquivos,
               "%s nao podia existir" % reg.ARQUIVO_REMOVIDO)

    # 3) PROVA DE FOGO EMBUTIDA: cada pedaco plantado de volta REPROVA pela marca certa.
    casos = (
        ("o arquivo/classe SelectPartyButton", reg.com_botao_de_volta, "SelectPartyButton"),
        ("a chamada SelectPartyButton.Ensure", reg.com_ensure_de_volta, "SelectPartyButton"),
        ("o gancho de OpenWindow (a RSTV-28)", reg.com_hook_da_janela_de_volta, "OpenWindow"),
        ("o gancho por STRING com classe neutra (RSTV-29F/achado C)",
         reg.com_hook_string_de_volta, "OpenWindow"),
        ("o gancho por STRING em atributos irmaos (RSTV-29F/achado C)",
         reg.com_hook_string_espalhado_de_volta, "OpenWindow"),
        ("a linha de boot da tela", reg.com_diag_de_volta, "Select Party"),
    )
    for rotulo, funcao, marca in casos:
        defeituoso = funcao(arquivos)
        arc.exigir(defeituoso != arquivos,
                   "o plantio '%s' nao mudou nada — a checagem nao esta lendo o trecho certo" % rotulo)
        f = reg.falhas_da_ausencia(defeituoso)
        arc.exigir(len(f) >= 1 and any(marca in x for x in f),
                   "com '%s' plantado de volta a checagem NAO reprovou pela marca %r (falhas=%s)"
                   % (rotulo, marca, " | ".join(f)))

    print("RSTV-29: a superficie do botao 'Skills' da tela Select Party NAO existe mais em nenhum .cs "
          "do mod (nem gancho da tela — em NENHUMA forma de escrita —, nem config/boot log); o botao "
          "do modal continua; os 6 pedacos plantados de volta REPROVAM pela marca certa.")


if __name__ == "__main__":
    arc.main(META, corpo)
