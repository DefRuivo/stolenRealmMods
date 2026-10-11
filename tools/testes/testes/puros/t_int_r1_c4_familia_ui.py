#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INT-R1-C4: a plumbing de UI generica do RSTV vem da familia `UI` da API, e o mod passa a
DEPENDER dela de forma explicita.

O QUE ESTE TESTE PROVA (e como)
-------------------------------
1. OS PONTOS MIGRADOS: os 5 clones e os 2 cliques que a API cobre de forma EQUIVALENTE passam por
   `RstvApiUi` -> `UIFactory.Clone` / `UIFactory.BindClick`. A forma antiga (`Instantiate` direto,
   `.onClick.AddListener` direto) some DESSES pontos.
2. O ESCOPO PELO NUMERO: a contagem, arquivo a arquivo, do codigo EFETIVO (sem comentario) de
   `UnityEngine.Object.Instantiate`, `.onClick.AddListener`, `RstvApiUi.Clonar(` e
   `RstvApiUi.LigarClique(` e' EXATAMENTE a da migracao. E' o que impede o diff de crescer sem
   alguem decidir, e o que prova que a migracao nao reabriu nenhum aceite anterior.
3. OS PONTOS PRESOS: o texto que os aceites anteriores do RSTV prendem (`regras_rstv11b.py:214`,
   `regras_rstv16.py:69`, `regras_rstv18.py:136`, `regras_rstv30.py:116`) continua no lugar — a
   migracao NAO tocou neles.
4. A PONTE: existe, vincula com `allowMutation: true`, delega (`UIFactory.Clone`/`BindClick`) e NAO
   reimplementa a plumbing a mao; a familia `UI` da API entra por ela e por mais nenhum arquivo.
5. O RISCO CONHECIDO (fechar o viewer nativo COMMITA): a guarda do commit continua nos ganchos
   (`Patches.cs`, patch de `SkillTreeManager.AcceptSkillChanges`) e os ganchos NAO citam a familia
   `UI` — a migracao nao abriu caminho novo para dentro da janela que grava. O ponto de observacao
   em jogo (`ui.skill-tree.updated` -> `SkillTreeManager::UpdateSkillTreeItems`) existe no catalogo
   da API (provedor INT-R1-C1). A observacao EM JOGO esta NAO_EXERCITADA (runtime fora do escopo).
6. A DEPENDENCIA EXPLICITA: o `.csproj` referencia as duas DLLs da API com `Private=false`; o
   plugin declara `[BepInDependency(ApiGuid, ApiVersionMinima)]` com o GUID e a versao minima; o
   README do mod diz o que acontece sem a API.
7. AS ISCAS (caso negativo): oito defeitos plantados EM MEMORIA tem de REPROVAR pelas checagens
   certas. Sem isso, as checagens poderiam estar passando por acidente.

DE ONDE VEM O ESPERADO
----------------------
Regras em `tools/testes/regras_int_r1_c4.py` (fontes lidos AO VIVO do mod e da API). A prova da
EQUIVALENCIA dos dois primitivos (o overload de 2 argumentos do jogo cai em
`instantiateInWorldSpace: false`, o mesmo argumento de `UIFactory.Clone`) esta em
`docs/automacao/INT-R1-C4-parte02.md`. O que NAO se prova aqui: o comportamento EM JOGO — a
conferencia visual e' do dono, e nada foi chamado dentro do jogo.
"""
import os

import regras_int_r1_c4 as reg

import arcabouco as arc

META = {
    "nome": "int-r1-c4-familia-ui",
    "categoria": "pura",
    "requer": [],
    "descricao": ("INT-R1-C4: o RSTV clona/liga clique pela familia `UI` da API (5 clones + 2 "
                  "cliques), a contagem por arquivo prova o escopo, os pontos presos por aceites "
                  "anteriores continuam presos, a API entra por uma ponte so', a guarda do commit "
                  "segue nos ganchos e a dependencia esta declarada (csproj + BepInDependency + "
                  "README); 8 defeitos plantados reprovam"),
}


def corpo():
    arquivos = reg.fontes_do_mod()
    ponte = arquivos.get(reg.ARQUIVO_PONTE, "")
    arc.exigir(len(ponte) > 1000,
               "RstvApiUi.cs veio vazio/curto: a ponte para a familia UI da API nao esta no mod?")
    arc.exigir(len(arquivos.get(reg.ARQUIVO_GANCHOS, "")) > 1000,
               "Patches.cs veio vazio/curto: a leitura mudou de lugar?")

    csproj = reg.fonte(reg.ARQUIVO_CSPROJ)
    readme = reg.fonte(reg.ARQUIVO_README)

    # 1..5) A MIGRACAO NO FONTE (pontos, contagem, presos, ponte, risco conhecido).
    falhas = reg.falhas_da_migracao(arquivos)
    arc.exigir(not falhas, "a migracao regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 6) A DEPENDENCIA EXPLICITA (build + runtime + README).
    falhas = reg.falhas_da_dependencia(arquivos, csproj, readme)
    arc.exigir(not falhas, "a dependencia da API regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 5b) O PONTO DE OBSERVACAO do risco conhecido existe na API (o provedor C1).
    falhas = reg.falhas_do_ponto_de_observacao()
    arc.exigir(not falhas, "o ponto de observacao do commit regrediu: %s" % " | ".join(falhas))

    # 5c) A PROVA DO CONTRATO da familia UI (inventario com 5 tipos + veredito CONFORME da API).
    falhas = reg.falhas_da_prova_do_contrato()
    arc.exigir(not falhas, "a prova do contrato da familia UI regrediu: %s" % " | ".join(falhas))

    docs_api = os.path.join(arc.raiz_do_repo(), "api", "docs")
    if os.path.isdir(docs_api):
        import json
        import shutil
        import tempfile

        copia = tempfile.mkdtemp(prefix="int_r1_c4_contrato_")
        try:
            for nome in ("contract-inventory.json", "ui-contract-diff.json"):
                shutil.copyfile(os.path.join(docs_api, nome), os.path.join(copia, nome))
            caminho_diff = os.path.join(copia, "ui-contract-diff.json")
            with open(caminho_diff, encoding="utf-8") as fh:
                conteudo = json.load(fh)
            conteudo["verdict"] = "DIVERGENTE"
            with open(caminho_diff, "w", encoding="utf-8") as fh:
                json.dump(conteudo, fh)

            falhas = reg.falhas_da_prova_do_contrato(copia)
            arc.exigir(any("nao e `CONFORME`" in f for f in falhas),
                       "a checagem NAO pegou o veredito divergente da familia UI: %s"
                       % " | ".join(falhas))
        finally:
            shutil.rmtree(copia, ignore_errors=True)

    # ------------------------------------------------------------------ AS ISCAS ---
    # 7a) O PONTO MIGRADO VOLTANDO AO UNITY DIRETO — um por familia de primitivo (clone do HUD,
    #     clone da janela, clique do modal). Cada um tem de reprovar por um motivo ESPECIFICO.
    iscas_de_ponto = (
        ("RunButton.cs",
         "RstvApiUi.Clonar(molde.gameObject, parent, ButtonName)"),
        ("SkillTreesWindow.cs",
         "RstvApiUi.Clonar(molde.gameObject, cabecalho, null)"),
        ("RemovalWindowSkillsButton.cs",
         "RstvApiUi.LigarClique(botao.gameObject, new UnityAction(OnClick))"),
    )
    for nome, chamada in iscas_de_ponto:
        original = arquivos[nome]
        plantado = reg.fonte_com_ponto_antigo(nome, original)
        arc.exigir(plantado != original,
                   "o plantio do 'ponto antigo' em %s nao encontrou a chamada da API: a isca nao "
                   "esta lendo o ponto migrado" % nome)
        falhas = reg.falhas_da_migracao(dict(arquivos, **{nome: plantado}))
        arc.exigir(any(chamada in f for f in falhas),
                   "a checagem NAO pegou %s voltando a escrever a plumbing a mao: %s"
                   % (nome, " | ".join(falhas)))

    # 7b) A PONTE SEM O OPT-IN DE MUTACAO (a API lanca em todo metodo que muta a UI).
    sem_optin = reg.fonte_sem_optin_de_mutacao(ponte)
    arc.exigir(sem_optin != ponte, "o plantio do 'sem allowMutation' nao encontrou o vinculo")
    falhas = reg.falhas_da_migracao(dict(arquivos, **{reg.ARQUIVO_PONTE: sem_optin}))
    arc.exigir(any("allowMutation" in f for f in falhas),
               "a checagem NAO pegou o vinculo sem `allowMutation: true`: %s" % " | ".join(falhas))

    # 7c) A PONTE QUE VOLTA A FAZER A MAO (deixa de delegar para a API).
    ponte_a_mao = reg.fonte_ponte_que_faz_a_mao(ponte)
    arc.exigir(ponte_a_mao != ponte, "o plantio da 'ponte a mao' nao encontrou a delegacao")
    falhas = reg.falhas_da_migracao(dict(arquivos, **{reg.ARQUIVO_PONTE: ponte_a_mao}))
    arc.exigir(any("MAO" in f or "a mao" in f for f in falhas),
               "a checagem NAO pegou a ponte reimplementando a plumbing: %s" % " | ".join(falhas))

    # 7d) A DEPENDENCIA APAGADA no plugin.
    sem_dep = reg.fonte_sem_dependencia(arquivos[reg.ARQUIVO_PLUGIN])
    arc.exigir(sem_dep != arquivos[reg.ARQUIVO_PLUGIN],
               "o plantio da 'dependencia apagada' nao encontrou o [BepInDependency]")
    falhas = reg.falhas_da_dependencia(dict(arquivos, **{reg.ARQUIVO_PLUGIN: sem_dep}),
                                       csproj, readme)
    arc.exigir(any("BepInDependency" in f for f in falhas),
               "a checagem NAO pegou a dependencia sem a declaracao explicita: %s"
               % " | ".join(falhas))

    # 7e) OS GANCHOS CITANDO A PONTE (a familia UI entrando no arquivo que guarda o COMMIT).
    ganchos = arquivos[reg.ARQUIVO_GANCHOS]
    ganchos_com_ponte = reg.fonte_ganchos_com_a_ponte(ganchos)
    arc.exigir(ganchos_com_ponte != ganchos,
               "o plantio 'ganchos com a ponte' nao encontrou o cabecalho do namespace")
    falhas = reg.falhas_da_migracao(dict(arquivos, **{reg.ARQUIVO_GANCHOS: ganchos_com_ponte}))
    arc.exigir(any("GANCHOS" in f for f in falhas),
               "a checagem NAO pegou a familia UI citada no arquivo dos ganchos: %s"
               % " | ".join(falhas))

    # 7f) O README SEM A DEPENDENCIA.
    readme_sem = reg.fonte_readme_sem_dependencia(readme)
    arc.exigir(readme_sem != readme, "o plantio do 'README sem dependencia' nao encontrou o GUID")
    falhas = reg.falhas_da_dependencia(arquivos, csproj, readme_sem)
    arc.exigir(any(reg.GUID_API in f for f in falhas),
               "a checagem NAO pegou o README sem a dependencia: %s" % " | ".join(falhas))

    print("migracao conferida: %d clone(s) + %d clique(s) pela familia UI da API; pontos presos "
          "intactos; %d iscas em memoria + o veredito do contrato reprovam"
          % (sum(reg.CLONAR_ESPERADO.values()), sum(reg.CLIQUE_ESPERADO.values()), 8))


if __name__ == "__main__":
    arc.main(META, corpo)
