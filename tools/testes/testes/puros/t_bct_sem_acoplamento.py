#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONVIVENCIA COM O BETTERFONT, DO LADO DO BCT (TST-8, cenario 9).

O QUE ESTE TESTE GARANTE
------------------------
O BetterCombatText e o BetterFont convivem (o halo dos textos de combate + a fonte serifada),
e a regra do projeto (invariante 3) e que mods NAO se referenciam entre si: zero ocorrencia do
nome/GUID de um no CODIGO do outro. Deste lado, isso significa que nada aqui pode ESCREVER no
material do outro nem DEPENDER dele:

  * o codigo do BCT nao cita o nome nem o GUID do BetterFont (varredura dos .cs);
  * a DLL construida tambem nao: nem em TypeRef/AssemblyRef/MemberRef (a busca em UTF-8 e
    UTF-16LE acha um literal; o leitor de IL acha uma referencia de tipo/assembly);
  * a unica ligacao e na FRENTE: os dois mexem no MESMO material por componente do texto, cada
    um na sua copia - o BetterFont RECOPIA o estilo que estava la (seja dele ou de quem veio
    antes). Nada aqui le tipo ou campo do BetterFont.

O PACOTE declara `DefRuivo_StolenRealmMods-BetterFont-1.0.2` como dependencia no
`manifest.json`, e o README diz "Needs: BepInEx 5 and BetterFont". Isso e escolha de
EMPACOTAMENTO (a combinacao serifa + halo e o que o dono quer entregar), nao acoplamento de
codigo: e por isso a varredura e dos .cs e da DLL, nunca do manifest/README, que CITAM o outro
mod de proposito.

ONDE A VARREDURA E FEITA (comentario x codigo): o invariante 3 e sobre o CODIGO - mods nao se
conhecem. Um comentario nao cria dependencia e nao vai para o assembly, entao a checagem forte e
o texto SEM comentario (`regras_bct.sem_comentarios`) mais o IL da DLL. A varredura do texto CRU
continua rodando, mas para REPORTAR (e nao reprovar) mencao em comentario: hoje ha UMA, em
`Plugin.cs` (o exemplo do padrao gancho-a-gancho do repositorio lista "BetterFont"), registrada
como achado em `tools/testes/bct-prova-reprovando.log`. O `BetterFont/Plugin.cs` nao tem
nenhuma mencao, nem em comentario.

A contra-prova embutida injeta o nome E o GUID do outro mod EM CODIGO (dois literais, que vao
para o assembly) no TextStyler: a varredura TEM de acusar os dois. A rodada fisica esta em
`tools/testes/bct-prova-reprovando.log`.
"""
import os

import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-sem-acoplamento",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/9: do lado do BCT, o codigo e a DLL nao citam o BetterFont (nem escrevem no material dele) - a ligacao e so o material por componente da frente",
}


def corpo():
    fontes = reg.fontes()
    menciones_em_comentario = []
    for nome, texto in sorted(fontes.items()):
        arc.exigir(len(texto) > 1000, "o %s veio vazio/curto: a leitura mudou de lugar?" % nome)
        # A regra e sobre o CODIGO (comentario nao cria dependencia e nao vai para o assembly):
        # a varredura forte e no texto SEM comentario, e no IL da DLL.
        achados = reg.ocorrencias_de_acoplamento(reg.sem_comentarios(texto))
        arc.exigir(not achados,
                   "o CODIGO do BCT cita o outro mod em %s: %s (o invariante 3 proibe; a copia "
                   "por componente vale para qualquer mod, nao para um caso especifico)"
                   % (nome, achados))
        # Mencao em COMENTARIO nao e acoplamento, mas fica REGISTRADA (achado) - o BetterFont
        # nao tem nenhuma; aqui ha uma, de documentacao, num exemplo de padrao do repositorio.
        em_comentario = reg.mencionados_no_texto(texto)
        if em_comentario:
            menciones_em_comentario.append((nome, em_comentario))

    # A DLL: TypeRef/AssemblyRef/MemberRef nao podem citar o outro mod.
    origem, dados = reg.dll_do_pacote()
    acoplamento_dll = []
    if dados is not None:
        meta = reg.ler_metadados(dados)
        acoplamento_dll = reg.referencia_ao_outro_mod_nos_metadados(meta)
        arc.exigir(not acoplamento_dll,
                   "a DLL (%s) cita o outro mod: %s" % (origem, acoplamento_dll))

    # CONTRA-PROVA: o nome E o GUID injetados em CODIGO no TextStyler tem de ser acusados.
    com_acoplamento = reg.defeito_acopla_betterfont(fontes[reg.STYLER])
    arc.exigir(com_acoplamento != fontes[reg.STYLER],
               "o plantio do acoplamento nao achou onde agir")
    acusados = reg.ocorrencias_de_acoplamento(reg.sem_comentarios(com_acoplamento))
    arc.exigir(len(acusados) >= 2,
               "o plantio citou o nome E o GUID do outro mod NO CODIGO, mas a varredura acusou "
               "so %r" % acusados)

    resumo_comentario = ("; mencao(oes) em comentario (nao e dependencia, registrada como achado): "
                         + ", ".join("%s=%s" % (n, a) for n, a in menciones_em_comentario)
                         ) if menciones_em_comentario else "; nenhuma mencao em comentario"
    print("fonte limpo no CODIGO (%d arquivo(s), %d termo(s) proibido(s)); detector provado com "
          "o acoplamento plantado em codigo (%d termo(s) acusado(s)); DLL (%s) sem referencia ao "
          "outro mod em TypeRef/AssemblyRef/MemberRef%s"
          % (len(fontes), len(reg.PROIBIDOS), len(acusados),
             os.path.basename(origem) if origem else "ausente", resumo_comentario))


if __name__ == "__main__":
    arc.main(META, corpo)
