#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A TRAVA DO ARTEFATO x FONTE (REL-1): o empacotador nao aceita DLL que nao e da fonte.

POR QUE ESTE TESTE EXISTE
-------------------------
O `tools/pack-thunderstore.py` conferia que a DLL EXISTIA em `bin/<Config>/` e nunca que ela
CORRESPONDIA a fonte. Em 01/10/2026 isso entregou o defeito: a Release que o empacotador
usava ainda era de 30/09 22:52 e carregava um `HarmonyPriority(600)` que a correcao do dia
(COR-2) ja tinha removido da fonte - empacotar teria publicado o defeito, com a versao nova
no manifest, e nada no caminho dizia nada.

Este teste roda o pre-flight REAL (`verificar`) contra um mod plantado com a relacao de
mtime escolhida, e cobra tres coisas:

  1. fonte ANTES da DLL (build em dia) -> o pre-flight PASSA. Sem isso a trava viraria um
     "reprova sempre", que ninguem usa e todo mundo desliga;
  2. fonte DEPOIS da DLL (o defeito) -> o pre-flight REPROVA citando "ARTEFATO VELHO", o
     arquivo de fonte que ficou para tras e os dois tempos;
  3. o gerado do build em `obj/` NAO conta como fonte - ele nasce com mtime do proprio
     build, DEPOIS da DLL: se contasse, a trava reprovaria todo build recem-feito. Ele fica
     plantado, mais novo que todo mundo, e mesmo assim o caso 1 passa.

E a mensagem de reprovacao tem de ENSINAR o comando certo, com `-p:DeployToBepInEx=false`:
sem a flag o alvo `DeployToBepInEx` do .csproj copia a DLL para o perfil do r2modman e o
jogo passa a rodar o build - foi o acidente medido com a ARM-1.

As duas contra-provas ao lado (`cp_rel_artefato_velho_*`) sao o MESMO teste: fora do bloco
`BLOCO-DO-DEFEITO` os arquivos sao identicos, e quem confere isso e a parte 4 daqui.
"""
import os
import tempfile

import arcabouco as arc
import regras_rel as rel

META = {
    "nome": "trava-artefato-fonte",
    "categoria": "pura",
    "requer": [],
    "descricao": "a trava REL-1 recusa a DLL mais antiga que a fonte, passa com o build em dia e ignora o gerado de obj/",
}


def corpo():
    with tempfile.TemporaryDirectory(prefix="rel1-") as raiz:
        # ---- 1. build em dia: a DLL e posterior a fonte -> PASSA ----
        plantio = rel.monta_mod(raiz, fonte_mais_nova=False)
        passou, mensagem = rel.roda_preflight(raiz, usar_guarda=True)
        arc.exigir(passou,
                   "o pre-flight REPROVOU um artefato em dia (fonte antes da DLL): %s"
                   % mensagem[-300:])
        arc.exigir(os.path.getmtime(plantio["gerado"]) > os.path.getmtime(plantio["dll"]),
                   "o plantio nao pos o gerado de obj/ depois da DLL - o caso 3 nao testa nada")

        # ---- 2. a fonte mexeu e ninguem reconstruiu -> REPROVA ----
        with tempfile.TemporaryDirectory(prefix="rel1-") as raiz2:
            rel.monta_mod(raiz2, fonte_mais_nova=True)
            passou, mensagem = rel.roda_preflight(raiz2, usar_guarda=True)
            arc.exigir(not passou,
                       "o pre-flight ACEITOU a DLL mais antiga que a fonte - e o defeito do "
                       "REL-1 (Release de 30/09 com o defeito no lugar do conserto)")
            arc.exigir("ARTEFATO VELHO" in mensagem,
                       "reprovou, mas nao disse que o motivo e o artefato velho: %s"
                       % mensagem[:200])
            arc.exigir("LocalizePatch.cs" in mensagem,
                       "nao citou o arquivo de fonte que ficou para tras: %s" % mensagem)
            arc.exigir("-p:DeployToBepInEx=false" in mensagem,
                       "nao ensinou o comando com a flag que IMPEDE o deploy no perfil "
                       "do r2modman: %s" % mensagem)

        # ---- 3. o gerado de obj/ e irrelevante: so a FONTE conta ----
        with tempfile.TemporaryDirectory(prefix="rel1-") as raiz3:
            p3 = rel.monta_mod(raiz3, fonte_mais_nova=False)
            # o gerado e 10 min mais novo que a DLL; a fonte continua antiga -> PASSA
            arc.exigir(os.path.getmtime(p3["gerado"]) > os.path.getmtime(p3["dll"]),
                       "o gerado de obj/ nao ficou mais novo que a DLL no plantio")
            passou, mensagem = rel.roda_preflight(raiz3, usar_guarda=True)
            arc.exigir(passou,
                       "o gerado de obj/ esta sendo contado como fonte (a trava reprovaria "
                       "todo build recem-feito): %s" % mensagem[-300:])

    # ---- 4. o par de contra-prova so pode diferir no BLOCO-DO-DEFEITO ----
    dir_cp = arc.DIR_CONTRA_PROVA
    isca = os.path.join(dir_cp, "cp_rel_artefato_velho_aceito.py")
    conserto = os.path.join(dir_cp, "cp_rel_artefato_velho_recusado.py")
    arc.exigir(os.path.isfile(isca) and os.path.isfile(conserto),
               "faltam as contra-provas do REL-1 em %s" % dir_cp)
    arc.igual(rel.fontes_fora_do_bloco_do_defeito(isca),
              rel.fontes_fora_do_bloco_do_defeito(conserto),
              "o par de contra-prova do REL-1 fora do BLOCO-DO-DEFEITO")


if __name__ == "__main__":
    arc.main(META, corpo)
